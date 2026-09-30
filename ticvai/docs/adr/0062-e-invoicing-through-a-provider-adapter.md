# ADR-0062: E-invoicing goes through a provider adapter, and a rejection stops for a person

**Status:** Proposed · waiting on the client (which accredited provider, which mandate date applies, whether B2C is outside the first phase, and the VAT 201 layout) and on Chinmay's yes to the adapter design
**Date:** 2026-10-01 (drafted 30 September from the system-design review) · **Deciders:** Chinmay Parab and the client (make-or-break: the provider, the dates and the field mapping are the client's and the regulator's)
**Finding:** SD-035 (high)
**Related:** ADR-0033 (outbox, amended by ADR-0058; financial postings halt rather than dead-letter) · ADR-0057 (broker, proposed) · ADR-0055 (`workers`) · CF-133

---

## What is open, and who answers

| Question | Who | Decisions Register |
|---|---|---|
| Which accredited e-invoicing provider (ASP) is appointed (account and Peppol ID)? | The client's finance team | Yes ("E-invoicing") |
| Which mandate date applies to the client (1 January 2027 for revenue of AED 50 million or more, or 1 July 2027)? | The client's finance team | Yes ("E-invoicing") |
| Are B2C transactions outside the first phase? | The client's tax adviser | **No.** In the client email of 30 September, item 1, but not in the register |
| The FTA VAT 201 box layout, and attribution to each emirate | The client's tax adviser | Yes ("VAT return") |
| The adapter design below (ours) | Chinmay | — |

The interface, the mock provider and the outbox job can be built before the client answers; only the
real adapter and the PINT AE mapping wait on the provider.

---

## Context

**Five operations are marked make-or-break, and four are in the Block A slice.**

| Operation | Where | In the slice | Notes |
|---|---|---|---|
| `issueTaxInvoice` | `finance.yaml:3491` | Yes (BO-022, GST-019, POS-026, WEB-019) | Make-or-break |
| `issueCreditMemo` | `finance.yaml:3637` | Yes | Make-or-break |
| `setEInvoicingProvider` | `finance.yaml:3954` | Yes (ADM-069) | *"Which accredited e-invoicing service provider (ASP) does the client appoint … The provider and the date are the client's; the PINT AE field mapping is the regulator's (CF-133)."* |
| `transmitEInvoices` | `finance.yaml:4058` | Yes (ADM-077) | Converts to PINT AE, hashes, sends; `queued` → `sent`; the answer arrives by callback; an `accepted` document is never sent again |
| `recordEInvoiceTransmissionStatus` | `finance.yaml:4148` | No | Service callback; `x-ticvai-permission: null` |
| `getVatReturn` | `finance.yaml:4219` | No | FTA VAT 201 box layout is make-or-break |

**No provider is named. Retry semantics for a rejected invoice are undefined.** ADR-0033 (amended by
ADR-0058) says a financial posting halts rather than dead-letters. A rejected tax document is not a
posting: the invoice was issued; the regulator's route refused it.

**Our understanding of the regulation, to confirm with the client and their tax adviser.** UAE
e-invoicing runs on Peppol through accredited service providers, using the PINT AE specification.
It is phased. Large businesses (revenue of AED 50 million or more) are mandated from 1 January 2027,
with a provider appointed by 31 July 2026; others from 1 July 2027. The first phase covers B2B and
B2G transactions; B2C is not in it. **If this is right:**

- a large client should already have appointed a provider;
- the mandate date falls inside B1, before the programme ends;
- most guest tickets (B2C) are outside the first phase. E-invoicing applies to partner, reseller, corporate and group sales, and government buyers.

---

## Decision

**Proposed: an in-house adapter per provider, transmission as an outbox-driven job, and a
rejection that stops for a person. The provider, dates and scope need the client's answer.**

- **Adapter.** `IEInvoicingProvider` with connect, transmit, status and test-endpoint calls. `setEInvoicingProvider` selects the adapter per legal entity. Build one adapter for the client's provider and a mock provider for tests.
- **Mapping.** PINT AE mapping as a versioned module, built from the published specification and proven against the provider's test endpoint (`test` mode already exists in the contract).
- **Transmission.** `issueTaxInvoice` and `issueCreditMemo` write the document and an outbox row in one transaction. A job in `workers` (ADR-0055) transmits. The provider call is HTTP from the job, not a broker message, so it does not depend on the client's broker choice (ADR-0057).
  - **Transport failures** (timeouts, 5xx) retry with backoff until the provider's `transmitWithinHours` deadline. An alert fires before the deadline.
  - **A business rejection is not retried.** The document stops in `rejected`, finance gets an alert, and a person fixes the master data and resends, or issues a credit memo. Nothing is dead-lettered silently (ADR-0033's rule, amended by ADR-0058, applied to tax documents).
- **Callback.** An inbound endpoint per provider, authenticated by that provider's mechanism (signature, mutual TLS or client credentials, whatever it offers). It calls `recordEInvoiceTransmissionStatus` as a named service caller on an allowlist. The `null` permission becomes a service-only permission. A repeated callback for the same document and status changes nothing.
- **Idempotency.** The document id is the key sent to the provider. `accepted` is terminal (already in the contract).
- **Egress.** Calls to the provider leave through the cell's NAT Gateway (`userAssignedNATGateway`), so the provider can allow-list one address.
- **Scope.** If the client confirms B2C is out of the first phase, guest sales still get a VAT tax invoice but no e-transmission.

---

## Options Considered

### Option A: In-house adapter per provider (recommended)

| Dimension | Assessment |
|---|---|
| Complexity | Medium. One adapter, one mapping, one job |
| Cost | Build only; the provider charges the client |
| Scalability | One adapter per extra provider |
| Team familiarity | Medium. HTTP integration, like the payment adapters |
| Time to Block A | Interface, mock and job in Block A; the real adapter when the provider's sandbox arrives |

**Pros:** We control retries and the rejection path. Fits the adapter pattern already used for payments.
**Cons:** Each new provider is a new adapter.

### Option B: An aggregator that connects to many providers

| Dimension | Assessment |
|---|---|
| Complexity | Low for us |
| Cost | Per-document fees and a second vendor contract |
| Scalability | Many providers through one integration |
| Team familiarity | Medium |
| Time to Block A | Depends on the aggregator's onboarding |

**Pros:** One integration for any client's provider.
**Cons:** Another processor of tax data; residency and contract review.

### Option C: Defer e-invoicing past the six months

| Dimension | Assessment |
|---|---|
| Complexity | None now |
| Cost | Risk of missing the mandate |
| Scalability | n/a |
| Team familiarity | n/a |
| Time to Block A | Frees Block A points |

**Pros:** Saves effort now.
**Cons:** Only possible if the client is below the large-business threshold (mandate from July 2027). Must be the client's answer.

### Option D: Become an accredited provider ourselves

Rejected. Accreditation is a regulated business, not a feature.

---

## Trade-off Analysis

A and B differ on who we depend on. With one client and one provider, A is simpler and keeps
tax data with fewer processors. B becomes attractive only if many tenants use many providers. C is
not ours to choose: it depends on the client's size and the mandate date.

---

## Consequences

**Easier:** a clear failure path finance can work; the same adapter pattern as payments.
**Harder:** the PINT AE mapping must be kept current as the regulator updates it.
**Revisit:** if tenants bring several different providers, consider Option B.

---

## Action Items

**Before Monday 5 October 2026**

1. [ ] Send the client the four questions: provider, mandate date, B2C scope, VAT 201 layout (drafted in the client email of 30 September, item 1).
2. [ ] Add "Is B2C outside the first phase?" to the Decisions Register; the other three are there.

**Sprint 1, week 2**

3. [ ] Chinmay's yes on the design; the client's answers recorded.
4. [ ] Package: service-only permission and caller allowlist on `recordEInvoiceTransmissionStatus`; a `rejected` alert event; the inbound callback operation per provider. New operations need a vocabulary permission. Re-derive, mirrors, check. (5 pts, the finding's estimate)

**Block A tickets**

5. [ ] **EINV-ADAPTER**: interface and mock provider. (3 pts)
6. [ ] **EINV-TRANSMIT**: outbox-driven job, retry to deadline, rejection alert. (5 pts)
7. [ ] **EINV-CALLBACK**: authenticated inbound endpoint. (3 pts)

**When the provider's sandbox arrives (B1 at the latest, if the mandate is 1 January 2027)**

8. [ ] **EINV-PINT-AE**: the mapping, proven on the test endpoint. (8 pts)
9. [ ] **EINV-PROVIDER**: the real adapter. (5 pts)
