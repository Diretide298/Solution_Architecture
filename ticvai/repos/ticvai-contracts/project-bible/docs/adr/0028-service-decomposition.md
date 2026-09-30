# ADR-0028: Seventeen modules, and the data boundary decides where they split

**Status:** Accepted · amended by [ADR-0055](0055-a-modular-monolith-deployed-as-five-units.md), 30 September 2026: the 17 services are modules of one .NET solution, deployed as five units, and the ownership rule below is rewritten so it is true. **The data topology reopened by CF-161 on 24 August is settled by
[ADR-0038](0038-cell-is-a-region-database-per-tenant.md) — amended by ADR-0040 on how many
instances a region holds, which changes nothing here:** the decomposition below is unchanged —
no service spans a schema it does not own — and the 26 schemas now live once per tenant database
rather than once per cell.
**Date:** 24 August 2026
**Related:** [ADR-0016](0016-read-write-separation.md) · [ADR-0020](0020-ai-isolation-boundary.md) · [ADR-0013](0013-local-first-point-of-sale.md) · [ADR-0010](0010-cross-jurisdiction-entitlements.md)

---

## Amended 30 September 2026 by ADR-0055

**The module map below stands. Two things in this ADR no longer hold.**

1. **The deployment shape.** The 17 services (sixteen when this was written; WalletService made
   seventeen) are **modules** of one .NET solution, deployed as five units: `commerce` (Identity,
   Tenancy, Catalogue, Order, Ledger, Wallet), `access` (Access), `operations` (F&B, Retail, Inventory,
   VenueOps, Marketing, WhiteLabel, Reporting, Platform, CrossRegion), `ticvai-ai` (AI) and `workers`
   (the outbox relay, event consumers and scheduled jobs). `handoff/service-decomposition.json` carries
   the `deployable` of each module.
2. **"No schema is written by two services" was not true.** On 30 September the lineage showed 35
   tables written by more than one service and 894 cross-schema reads in 493 operations. The rule is
   now: **the owner migrates its schemas; other modules read them only through views the owner
   publishes (or its in-process query interface) and write them only through the owner's in-process
   API, inside the caller's transaction; across deployables, modules talk by event or by the published
   contract.** Enforcement is by architecture tests, a lineage check and one Postgres role per
   deployable, not by per-schema grants.

**The modular-monolith rejection under "Alternatives" is answered, not reversed.** Its two reasons
stand, and both are now separate deployables: Access runs as its own unit (and at the edge), and AI
stays isolated in `ticvai-ai` (ADR-0020, amended by ADR-0049).

---

## 🔴 Reopened 24 August — the deployment shape, not the service split

**The 24 August infrastructure workshop decided the opposite of what this ADR assumes.** Dinesh
recommended **segregating databases per service from the start**, on the grounds that splitting a
centralized database after two or three years in production is significantly harder than starting
isolated and merging later.

**This ADR says one Postgres per cell with 26 schemas inside it.** Both were written the same day
and neither knew about the other.

**The service boundaries below are unaffected.** Sixteen services (now seventeen modules), five tiers, the rule that the
owner defines a row and a foreign writer may only append — none of that depends on whether those
schemas share a database. **What is reopened is the deployment of the data, not the decomposition
of the code**, and this ADR should be read as a service decomposition with an open question about
where its schemas live.

Tracked as **CF-161**. Do not generate DDL against either answer until it closes — writing it
against an undecided topology is writing it twice.

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

**Seventeen modules (sixteen services when this was written). The data boundary decides where they split.**

**No service spans a schema it does not own, and no schema is written by two services.** *No longer
true, and amended by ADR-0055: see the amendment at the top for the rule that replaced it.* That was
thought true before this document existed — the work was finding it, not creating it — and it is what makes
the split safe.

### The rule

**A service owns its schemas outright.** It defines the rows, it migrates the tables, and nothing
else writes them except by appending through a path the owner published.

**22 tables have two writing contracts and all are correct.** A till closing posts to
`ledger.posting` because settling a shift *is* a ledger act. `orders` writes `access.entitlement`
because a sale issues a ticket. **The owner defines the row; a foreign writer may only append to
it.**

### The tiers

| Tier | Services | What it means |
|---|---|---|
| **Foundation** | Identity, Tenancy | Read by everything, reads nothing above. **Deploys first and alone.** |
| **Commerce** | Catalogue, Order, Access, Ledger | The sale path. Highest availability and write rate. |
| **Operations** | Inventory, F&B, Retail, VenueOps | What a venue does with what it sold. Licensed per module. |
| **Engagement** | Marketing, AI | **Nothing that takes money depends on these.** |
| **Platform** | Control, WhiteLabel, Reporting, CrossRegion | Provisioning, publishing, reporting, and the one cross-region path. |

---

## The four decisions that are not obvious

### `shift` is not a service

**It owns no tables.** Its rows live in `orders.pos_shift`, `orders.cash_movement`,
`orders.deposit_box` and `orders.no_sale_event` — 19 operations, zero schemas.

**A service with no data is not a service; it is a set of operations**, and they belong with the
scope they resolve against. Folded into TenancyService alongside `workforce` and `approvals`, all
three of which read `platform.scope` constantly and write it rarely — **splitting them means
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

**Four services can be down without stopping a sale**: Marketing, AI, Reporting, CrossRegion. That is
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
