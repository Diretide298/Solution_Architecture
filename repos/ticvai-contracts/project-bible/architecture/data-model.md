# Data Model

> **Purpose:** Spine aggregates and the two decisions that dominate  
> **Owner:** Backend  
> **Status:** **Week 3**


## Spine contexts

| Context | Owns |
|---|---|
| Tenancy & Org Hierarchy | Scope tree, region settings, placement |
| Identity & AuthZ | Principal, Role, Grant, Session |
| Product & Entitlement | Product, Component, Attribute, Price List, Envelope, Event, Performance, Entitlement |
| Order & Payment | Order, OrderLine, Payment, Refund, Void, Till, Shift, DepositBox |
| Access Control | AccessPoint, AdmissionProfile, ScanEvent, Media |
| Finance & Ledger | Account, JournalEntry, TaxCode, RecognitionSchedule |

**Schema per module, database per tenant.** Each service connects with a role granted access only to its own schema — enforced by Postgres grants, not convention.

Normally a microservice anti-pattern. Correct here because the tenancy decision outranks it, and because **order + payment + entitlement + ledger must be one transaction**.

## The two decisions that dominate

### Data mask

Arbitrary typed custom fields at account, event, ticket or metric-cell level — multi-language, validated, with reusable value sets (07 Aug §6).

**`JSONB` value column + a relational field-definition registry** (type, labels, validation, mask-table reference), GIN-indexed on declared query-critical paths.

**Never dynamic DDL.** A schema change per tenant field makes migrations unrunnable at N cells.

Declare at design time which paths are query-critical; index those. Reporting over arbitrary custom fields needs a separate read model.

### Component / attribute variants

Adding an attribute value auto-creates sellable variants (07 Aug §12).

**Product template + attribute axes + a materialised variant table**, regenerated on axis change. A static product table cannot express it; pure runtime expansion kills pricing queries.

## Invariants

| Invariant | Settled |
|---|---|
| Identity ≠ Entitlement | 05 Aug 2026 |
| Ticket ID ≠ Media Code | 07 Aug 2026 |
| Ledger is append-only; corrections are entries | 12 Aug 2026 |
| PII lives in a separate erasable store, referenced by opaque subject ID | Derived — reconciles append-only with erasure |
| Order ≠ Reservation ≠ Ticket | Glossary |

## Conventions

| Concern | Rule |
|---|---|
| Money | `numeric(18,4)` + explicit currency and scale. OMR is 3dp, AED 2dp |
| IDs | ULID `char(26)` for edge-created entities; UUID for configuration; **never `bigserial` on a partitioned table** |
| Scope | `scope_path ltree` + denormalised `venue_id`, `region_id`, `brand_id` |
| Partitioning | List on `venue_id` for hot tables; partition key in the primary key |
| RLS | `ENABLE` **and** `FORCE` on every tenant-scoped table |
| Timestamps | `timestamptz` UTC; `recorded_at` vs `synced_at` vs `created_at` distinguished |
| Outbox | Publication atomic with the state change |

## Migrations

Forward-only, numbered, checksummed, with a **per-cell schema-version register**. Every migration runs N times — once per cell — so rollback is tested before merge, and rollout is canary-first.

Long-running DDL uses `CONCURRENTLY`. A migration holding a lock on `sales_order` during trading is an outage across every venue in the cell.

---

## Currency — three questions, not one

**Corrected 18 August.** Multi-currency was treated as a guest display feature until then. It is a
payment concern on every surface that takes money, and it is three separate questions that were
being answered as one.

| | | |
|---|---|---|
| **Display currency** | What a guest sees a price in | `WEB-035`, `GST-044`. Comparison only |
| **Tender currency** | **What the guest actually handed over** | `Payment.tenderCurrency`, with the rate stored on the payment |
| **Base currency** | What the venue books and settles | `Money.currency` on the order and the ledger |

**They differ for the same sale.** A tourist sees a price in USD, pays in USD cash at a till, and
the venue books AED — three currencies, one transaction.

### What the requirements ask, and the asymmetry in them

**4.6.11 is deliberately one-directional**: *"accept foreign currency and offer refunds/negative
sales in local currencies."* Foreign cash comes in; change and refunds go out in base currency
only.

**That asymmetry is what keeps a till reconcilable.** A till giving change in five currencies
needs five floats and five counts, and a variance becomes unattributable to the currency that
caused it. Taking foreign cash needs one number per currency: what came in.

**4.2.8** requires rates maintained manually or on a schedule. **5.11.6** requires accounting
entries across currencies. **6.1.10** requires daily transactions summarised by currency amount —
which is `getForeignTenderReport`, and **it promised *what was taken in which currency* while
`Payment` recorded no currency at all.** The report had no source until 18 August.

### The rate is stored, never looked up

`Payment.fxRate` and `fxRateSource` sit on the payment. **A payment reconciled next month is
reconciled at the rate of the day it was taken** (CF-37), and a rate that has moved since is not
the rate the guest was given.

`fxRateSource: cardScheme` is the case worth naming: **the terminal did the conversion and told
us.** That is dynamic currency conversion, the rate is the scheme's rather than ours, and
recording it as if it were ours would misstate the margin.

### Where foreign cash is and is not accepted

**POS: yes.** `POS-002` and `POS-004` record tender currency and rate; `POS-009` counts each
currency separately through `DepositBox.foreignHoldings`.

**Kiosk: no.** A machine accepting foreign notes needs a note reader and a per-currency float, and
neither is specified. A guest paying by card in a foreign currency is converted by their own
issuer, which is not our rate and not our problem.

**Web, app, partner, back office: card only**, so the tender currency is the base currency and the
issuer handles the rest.

