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
