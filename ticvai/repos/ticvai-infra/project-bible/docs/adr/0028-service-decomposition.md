# ADR-0028: Sixteen services, and the data boundary decides where they split

**Status:** Accepted
**Date:** 24 August 2026
**Related:** [ADR-0016](0016-read-write-separation.md) · [ADR-0020](0020-ai-isolation-boundary.md) · [ADR-0013](0013-local-first-point-of-sale.md) · [ADR-0010](0010-cross-jurisdiction-entitlements.md)

---

## Context

The package has 28 OpenAPI contracts, 1,007 operations and 378 tables across 26 schemas. **The
lineage names a service on every operation and it named 31** — three of which were the same service
spelled two ways: `OrderService`/`OrdersService`, `LedgerService`/`FinanceService`,
`MarketingService`/`MarketingCrmService`. **That is how one contract becomes two repositories**, and
it was fixed before this decision was written.

That left 28 services, one per contract, which is a mapping rather than a decision.

---

## Decision

**Sixteen services. The data boundary decides where they split.**

**No service spans a schema it does not own, and no schema is written by two services.** That was
true before this document existed — the work was finding it, not creating it — and it is what makes
the split safe.

### The rule

**A service owns its schemas outright.** It defines the rows, it migrates the tables, and nothing
else writes them except by appending through a path the owner published.

**22 tables have two writing contracts and all are correct.** A till closing posts to
`ledger.entry` because settling a shift *is* a ledger act. `orders` writes `access.entitlement`
because a sale issues a ticket. **The owner defines the row; a foreign writer may only append to
it.**

### The tiers

| Tier | Services | What it means |
|---|---|---|
| **Foundation** | Identity, Tenancy | Read by everything, reads nothing above. **Deploys first and alone.** |
| **Commerce** | Catalogue, Order, Access, Ledger | The sale path. Highest availability and write rate. |
| **Operations** | Inventory, F&B, Retail, VenueOps | What a venue does with what it sold. Licensed per module. |
| **Engagement** | Marketing, AI | **Nothing that takes money depends on these.** |
| **Platform** | Control, WhiteLabel, Reporting, CrossCell | Provisioning, publishing, reporting, and the one cross-region path. |

---

## The four decisions that are not obvious

### `shift` is not a service

**It owns no tables.** Its rows live in `orders.shift`, `orders.cash_movement`,
`orders.deposit_box` and `orders.no_sale_event` — 19 operations, zero schemas.

**A service with no data is not a service; it is a set of operations**, and they belong with the
scope they resolve against. Folded into TenancyService alongside `workforce` and `approvals`, all
three of which read `platform.scope_node` constantly and write it rarely — **splitting them means
four services doing the same joins.**

### Subscription, platform-ops and public-api are one service

**Three contracts, one schema, 41 tables.** All three write `control.*` — 34, 18 and 14 operations
respectively.

**They are one bounded context split into three contracts for API-surface reasons, not for data
reasons.** A developer portal and a tenant licensing console are different audiences and the same
data. Splitting them gives three services writing one schema, **which is the arrangement every
guide to distributed data warns about.**

### AI is separate at any size, and not because of size

**30 operations. It would fold into anything on volume alone.**

ADR-0020 makes it a hard boundary: only this service writes AI tables, and it is read-only against
the transactional core. **That boundary caught four wrongly-placed writes in one week** — including
two I wrote myself, in operations that looked entirely reasonable.

**It survives because it is enforced, and enforcing a boundary across a network is easier than
enforcing it across a shared deployment.**

### Marketing stays whole, and is the one to watch

**93 operations and 37 tables — the largest single domain.** CRM and campaigns have different write
patterns: a guest profile is read constantly and written rarely; a campaign send is a burst of
millions of rows nobody reads again.

**Kept as one because splitting a service before it has a load profile is guessing.** The split is
pre-drawn along `marketing.guest_profile` and `marketing.campaign`, and it is a decision for the
first month of production traffic rather than for a design document.

---

## Consequences

**Deploy order is the tier order.** Foundation first and alone — **a restart of Identity is an
outage everywhere**, and twelve contracts read it.

**Four services can be down without stopping a sale**: Marketing, AI, Reporting, CrossCell. That is
a deliberate property and it should be tested rather than assumed.

**Order autoscales and nothing else needs to.** A Saturday evening is ten times a Tuesday morning
and **nothing else in the platform has that shape** — Access is high-rate and flat, F&B is two sharp
peaks a day, Ledger is batch.

**Access and F&B run offline-capable.** ADR-0013 for the till; the kitchen display because the
kitchen still has to send food out. **Both hold local state and reconcile**, which is a different
operational posture from everything else and a reason not to share a deployment with services that
do not.

**Ledger is correctness over availability.** A ledger briefly unavailable is recoverable; one
briefly wrong is not. It is the only service in the platform where that trade runs the other way.

---

## Alternatives considered

**One service per contract — 28.** The mapping the lineage already had. **Six of them would own
fewer than fifteen operations**, and `shift` would own none. Twenty-eight deployments to run a
venue that licensed four modules is an operational cost with no corresponding benefit.

**A modular monolith.** Genuinely defensible for the first year, and it fails on two properties
the platform already has: **Access must run at the edge** with a sub-300ms local decision, and
**AI must be isolated** by ADR-0020. Both are boundaries in the design already; a monolith would
have to reintroduce them as conventions.

**Splitting by module rather than by data.** F&B, Retail and Ticketing as three vertical services.
It reads well against the licence model and **it cuts straight through `catalogue` and `orders`,
which all three write.** The module boundary is a commercial one and the service boundary is a
data one, and they are not the same line.

---

## Provenance

**The service names came from the lineage, which had them from the start.** What this ADR adds is
the grouping, the tiers, and the four decisions above — and it could only be written once the data
ownership was clean enough to read off. **On 20 August, four operations were writing a derived
table and `identity.role_permission` had one column.** Neither would have shown up in a service
decomposition drawn before then.
