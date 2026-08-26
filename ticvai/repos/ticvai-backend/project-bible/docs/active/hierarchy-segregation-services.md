# TICVAI — Hierarchy, Data Segregation and Services

**Architecture note · 24 August 2026 · Softlabs**

---

## 1. Overview

Three questions, answered against a package of 1,014 operations, 379 tables and 477 screens.

**Where does configuration live?** Eight scope levels, each earning its place by owning something
nothing above or below can own.

**How is the data divided?** 26 schemas in one Postgres per cell — not one database per tenant, and
not one shared table with a tenant column.

**What ships together?** Sixteen services, and the data boundary decides where they split.

**The three answers are not independent.** Service boundaries follow schema boundaries; schema
boundaries follow the scope model. **Getting the order wrong means drawing service boundaries and
then discovering the tables disagree** — which is exactly what happened once during this work, and
section 4 says so.

---

## 2. The hierarchy

![The eight scope levels and what resolves at each](FIG:scope-hierarchy)

### 2.1 Why a hierarchy at all

A venue operator does not have one set of settings. **A tenant with four brands across two countries
and eleven venues has settings belonging at four different heights.** Flattening them produces one
of two failures: every venue configures everything from scratch, or one change at the top breaks a
venue that needed to differ.

`platform.scope_node` is the answer, and **it is reached by 304 of 379 tables** — the tenancy spine.
A node has a `level`, a `parent_id` and a materialised `path`; configuration resolves by walking
that path upward until something answers.

**ADR-0011 made the hierarchy binding.** Seven levels were confirmed with the client; `outlet` was
added on 18 August as an eighth.

### 2.2 Why each level exists

| Level | Operations | Owns | Why here |
|---|---:|---|---|
| `tenant` | 238 | Plans, licences, roles, templates | **Bought here.** A role defined at venue would be defined eleven times |
| `brand` | 2 | Brand identity | **Optional and free when unused** — a tenant with one brand never creates a node |
| `region` | 46 | Currency, decimal scale, timezone, fiscal year | **Not overridable below.** One venue on a different decimal scale is a ledger that cannot consolidate |
| `venue` | 675 | Almost everything operational | **Two thirds of all operations.** The platform's default |
| `department` | — | Requisitions, rotas, cost centres | The staffing and budget tree |
| `subDepartment` | — | A second tier | Optional |
| `workstation` | 45 | Config profile, offline policy, deposit box | **A till is a scope, not just a device** |
| `outlet` | — (5 configs) | Menu, tables, return policy, hours | **A sibling of department** — see below |

### 2.3 Why `outlet` is a sibling and not a child

**This is the decision worth defending.**

A restaurant inside a venue has a menu, hours, a table layout, a return policy and stock. On the
face of it that is a department.

**Modelling it as one puts the restaurant in the staffing tree.** Departments carry requisitions,
rotas and cost centres — and **a venue whose restaurant is run by a concession would be describing
staff it does not employ.**

**A department answers *who works where*; an outlet answers *what is sold where*.** The same
physical restaurant can be one department and two outlets — a kitchen and a bar.

**Only five configurations resolve at outlet**, and everything else has no outlet on its path.
That is what made an eighth level cheap enough to add after the hierarchy was already binding.

Raised as CF-138, decided in ADR-0018.

---

## 3. Data segregation

![Twenty-six schemas and who owns them](FIG:schema-ownership)

### 3.1 The shape

**26 schemas in one Postgres per cell.** One cell per jurisdiction (ADR-0001); within a cell,
segregation by domain rather than by tenant.

**Not one database per tenant** (ADR-0005). A venue operator with eleven venues is one tenant, and
four hundred tenants would be four hundred databases to migrate, back up and monitor. **Tenancy is
a partition key, not a deployment boundary.**

**Not one shared schema either.** 379 tables in one namespace is a namespace nobody can reason
about, and it makes the service boundary impossible to enforce.

### 3.2 Every schema

| Schema | Tables | Owner | Stores | Written by |
|---|---:|---|---|---|
| `access` | 8 | Access | postgres | access, catalogue, orders |
| `ai` | 15 | Ai | postgres, postgres-analytical | ai, reporting |
| `approvals` | 6 | Tenancy | postgres | approvals, subscription, workforce |
| `assets` | 4 | VenueOps | postgres | assets |
| `catalogue` | 18 | Catalogue | postgres | catalogue, fnb, inventory, orders |
| `control` | 41 | Control | postgres | marketing-crm, platform-ops, public-api, subscription, white-label |
| `fnb` | 34 | Fnb | postgres | fnb |
| `games` | 8 | VenueOps | postgres | games |
| `identity` | 16 | Identity | postgres, redis | identity, orders, public-api, tenancy |
| `inventory` | 19 | Inventory | derived, postgres | fnb, inventory, maintenance, retail |
| `ledger` | 18 | Ledger | postgres | finance, orders, shift |
| `maintenance` | 8 | VenueOps | postgres | maintenance |
| `marketing` | 37 | Marketing | postgres | access, fnb, identity, marketing-crm, orders, public-api, workforce |
| `orders` | 34 | Order | postgres | fnb, identity, marketing-crm, orders, resources, shift |
| `pii` | 4 | Identity | postgres | access, identity, marketing-crm |
| `platform` | 24 | Tenancy | postgres | cross-cell, identity, inventory, tenancy |
| `promotions` | 11 | Catalogue | postgres | promotions |
| `queue` | 4 | VenueOps | postgres | queue |
| `reporting` | 13 | Reporting | derived, postgres | reporting |
| `resources` | 4 | VenueOps | postgres | resources |
| `retail` | 14 | Retail | postgres | orders, retail |
| `seating` | 11 | Catalogue | postgres | seating |
| `sync` | 1 | CrossCell | postgres | access, games |
| `venuemap` | 4 | VenueOps | postgres | venue-map |
| `whitelabel` | 13 | WhiteLabel | postgres | white-label |
| `workforce` | 5 | Tenancy | postgres | workforce |

### 3.3 The five that need stating

**`pii` is separate from `identity`.** A principal is who may act; a subject is who they are
(ADR-0023). **Three writers, narrowly scoped** — identity mints the subject, access enrols a face,
marketing updates a profile the subject owns. That narrowness is what makes a subject-access export
and a deletion request answerable.

**`ledger` is append-only.** Never updated, never deleted — a different discipline from everything
around it, and one that should not share a schema with tables that mutate.

**`platform` holds the spine.** `scope_node`, reached by 289 tables.

**`inventory.stock_level` is derived and never stored.** Four operations wrote it directly and were
found on 20 August. **A stored level and a movement ledger that disagree is a stock count nobody can
reconcile** — `check-package` now refuses any write to a derived table.

**`ai` is written by one contract only** (ADR-0020). That boundary caught four wrongly-placed writes
in a single week.

### 3.4 Cross-schema writes

**22 tables are written by more than one contract, and all 22 are correct.**

**The rule: the owner defines the row; a foreign writer may only append to it.** A till closing
posts to `ledger.entry` because settling a shift *is* a ledger act. `orders` writes
`access.entitlement` because a sale issues a ticket.

---

## 4. Sixteen services

![The service map and the writes that cross between services](FIG:service-map)

### 4.1 How the number was reached

The lineage named a service on every operation and named 31. **Three were the same service spelled
two ways** — `OrderService`/`OrdersService`, `LedgerService`/`FinanceService`,
`MarketingService`/`MarketingCrmService`. **That is how one contract becomes two repositories.**

That left 28, one per contract, which is a mapping rather than a decision.

### 4.2 The correction worth reading

**`shift` was folded into TenancyService and moved to OrderService the same day.**

The reasoning was that a shift owns no tables of its own. **That is true, and the conclusion was
wrong.** A service with no data belongs where its data is — and a shift's data is entirely in
`orders`: `orders.shift`, `orders.deposit_box`, `orders.cash_movement`, `orders.cash_count_line`.

**A shift is venue-scoped, which is what made it look like a tenancy concern.** But **venue scope
is the platform's default rather than a service boundary** — 675 of 1,014 operations are
venue-scoped.

**Scope answers *whose configuration is this*. Schema answers *whose data is this*.** The first was
allowed to decide the second, and the coupling made it visible: **all 43 of Tenancy's cross-service
touches into `orders` were the `shift` contract.** Moving it took Tenancy's cross-service writes
from 23 to 2.

### 4.3 The sixteen

| Service | Tier | Ops | Tables | Screens | Journeys | Flows % | Schemas owned |
|---------------------|--------|-------|----------|-----------|---------|----------|--------------------------------------|
| **Tenancy** | Fnd | 52 | 35 | 71 | 18 | 62% | `platform`, `workforce`, `approvals` |
| **Identity** | Fnd | 44 | 20 | 36 | 13 | 48% | `identity`, `pii` |
| **Catalogue** | Com | 132 | 40 | 73 | 30 | 43% | `catalogue`, `promotions`, `seating` |
| **Order** | Com | 96 | 34 | 101 | 37 | 55% | `orders` |
| **Ledger** | Com | 54 | 18 | 20 | 6 | 61% | `ledger` |
| **Access** | Com | 30 | 8 | 29 | 13 | 57% | `access` |
| **VenueOps** | Ops | 102 | 32 | 53 | 15 | 47% | `queue`, `maintenance`, `resources`, `venuemap`, `assets`, `games` |
| **Fnb** | Ops | 96 | 34 | 57 | 17 | 73% | `fnb` |
| **Inventory** | Ops | 50 | 19 | 28 | 12 | 96% | `inventory` |
| **Retail** | Ops | 35 | 14 | 19 | 10 | 43% | `retail` |
| **Marketing** | Eng | 96 | 37 | 40 | 18 | 41% | `marketing` |
| **Ai** | Eng | 30 | 15 | 21 | 10 | 57% | `ai`, `qdrant` |
| **Control** | Plat | 102 | 41 | 42 | 10 | 39% | `control` |
| **White label** | Plat | 50 | 13 | 25 | 6 | 44% | `whitelabel` |
| **Reporting** | Plat | 29 | 13 | 31 | 10 | 62% | `reporting` |
| **CrossCell** | Plat | 16 | 1 | 4 | 1 | 31% | `sync` |

**Flows %** is flow coverage — how much of each service a journey has traced end to end. **Not
tests, not build.** Every flow written in this project has found a defect, so **a service under 40%
is unwalked rather than under-documented**: its defects are still in it.

### 4.4 The eight worth defending

The other eight are what they look like — a domain with its own schema, its own scaling profile and
its own licence. **These eight are not.**

**Tenancy** — **`platform.scope_node` is reached by 304 of 379 tables** — the tenancy spine. Workforce and approvals are folded in because each is small, both read `scope_node` constantly and write it rarely, and splitting them means three services doing the same joins.

**`shift` was folded in here on 24 August and moved to OrderService the same day.** The reasoning was that a shift owns no tables of its own — which is true — and the conclusion was wrong. **A service with no data belongs where its data is**, and a shift's data is entirely in `orders`: `orders.shift`, `orders.deposit_box`, `orders.cash_movement`, `orders.cash_count_line`.

**The coupling made it visible.** All 43 of Tenancy's cross-service touches into `orders` were the `shift` contract — 19 writes and 24 reads, the heaviest coupling in the platform, created to solve a cosmetic problem.

*Scale.* Read-heavy and highly cacheable. Config changes are rare. *If it is down.* Same as identity — nothing runs without a scope.

**Order** — **The transactional core.** 96 operations, 34 tables, and the highest write rate in the platform. Separate because its scaling profile is unlike anything else — a Saturday evening is ten times a Tuesday morning.

**`shift` belongs here and not in Tenancy.** A shift is venue-scoped, which is what made it look like a tenancy concern — but **venue scope is the platform's default rather than a service boundary**: 675 of 1,014 operations are venue-scoped.

**What decides the service is who owns the tables.** A shift holds cash, `orders.deposit_box` reconciles against payments, and `orders.cash_movement` posts to `ledger.entry` at close. **A till's takings and a till's drawer are the same money counted twice** — separating them makes every settlement a distributed join.

*Scale.* Write-heavy, spiky, latency-critical. **The one that autoscales.** *If it is down.* **Down means no sales.** Highest availability target in the platform.

**Ai** — **Separate at any size, and not because of size.** ADR-0020 makes it a hard boundary: only this service writes AI tables, and it is read-only against the transactional core. **That boundary caught four wrongly-placed writes in one week** — it survives because it is enforced, and enforcing it across a shared deployment is harder than across a network.

*Scale.* Latency-tolerant, cost-sensitive, token-metered. Different hardware from everything else. *If it is down.* Down degrades suggestions and the concierge. **Nothing that takes money depends on it.**

**Marketing** — **93 operations and 37 tables — the biggest thing in the package, and probably two services eventually.** CRM and campaigns have different write patterns: a guest profile is read constantly and written rarely; a campaign send is a burst of millions of rows nobody reads again.

**Kept as one for now** because splitting a service before it has a load profile is guessing.

*Scale.* Bursty on send, read-heavy otherwise. **The one to watch for a split.** *If it is down.* Down stops campaigns and guest lookup. Neither stops trading.

**Control** — **Three contracts, one schema, 41 tables.** Subscription, platform operations and the public API all write `control.*` — **they are one bounded context that was split into three contracts for API-surface reasons, not for data reasons.**

Splitting them would give three services writing one schema, which is the arrangement every distributed-data guide warns about.

*Scale.* Low volume, high consequence. Tenant provisioning and licensing. *If it is down.* Down blocks provisioning and the developer API. **Trading is unaffected.**

**CrossCell** — **The only service that reaches another region** (ADR-0010, ADR-0014). Separate because it is the one place where data crosses a jurisdiction, and **a boundary that matters legally should be a boundary that exists physically.**

It moves a pseudonymous guest link rather than a guest, which is the whole design.

*Scale.* Low volume, high scrutiny. *If it is down.* Down blocks cross-region entitlements. Each region continues alone.

**Ledger** — **Money, and it is append-only.** 54 operations over 18 tables that are never updated and never deleted — a different discipline from everything around it, and one that should not share a deploy with anything that does mutate.

*Scale.* Write-heavy, batch-tolerant, not latency-critical. Recognition and revaluation are jobs. *If it is down.* **Correctness over availability.** A ledger that is briefly unavailable is recoverable; one that is briefly wrong is not.

**Access** — **The gate.** Validating an entitlement is a sub-300ms decision made forty times a minute per lane, and it must work when the network does not.

*Scale.* Read-heavy, extreme latency sensitivity, edge-cached. **`frozenDays` is held rather than replayed** precisely because the gate cannot afford the arithmetic. *If it is down.* Down means the gates stop. Runs at the edge with a local decision cache.

---

## 5. Consequences

**Deploy order is the tier order.** Foundation first and alone — twelve contracts read Identity, and
289 tables anchor on `platform.scope_node`.

**Four services can be down without stopping a sale**: Marketing, AI, Reporting, CrossCell. **A
deliberate property that should be tested rather than assumed.**

**Order autoscales and nothing else needs to.** A Saturday evening is ten times a Tuesday morning.

**Ledger is correctness over availability** — the only service where that trade runs the other way.

---

## 6. Merges considered

**CrossCell into Tenancy is the closest call.** 16 operations, one table, and 11 of its writes go
into `platform.*`. **Kept separate** because it is the only service reaching another jurisdiction,
and putting that code inside the service everything depends on widens the blast radius of a mistake.

**Ledger into Order** — kept separate. Append-only versus mutable is a different discipline.

**Retail into Inventory** — kept separate. Licensed separately; a venue running ticketing with no
shop should not deploy retail.

**`control` is worth splitting rather than merging.** 41 tables and three writing contracts — the
largest schema in the package. **Developer accounts have a different audience and cadence**, and
P14 is the only platform that touches them.

---

## 7. Limitations

**Build is 0%.** 379 tables specified, none written. **The first month of production traffic will
move at least one boundary** — most likely Marketing, which is 93 operations with two clearly
different write patterns.

**The cloud provider is undecided (CF-64).** Everything above is provider-neutral; nothing below it
can be.

**Flow coverage is 53%** across 93 flows, up from 21% on the same day. **Coverage is uneven and the
spread is the useful number**: `InventoryService` at 96%, `CrossCellService` at 31%.

---

## 8. Accompanying material

| Artefact | What it holds |
|---|---|
| `TICVAI_Services_and_Data_Segregation.xlsx` | Five sheets: services with coverage, schema segregation, cross-service writes, deploy order, hierarchy |
| `docs/adr/0028-service-decomposition.md` | The decision, its alternatives, its provenance |
| `docs/adr/0011-hierarchy-is-binding.md` | The seven organisational levels |
| `docs/adr/0018-configuration-scope.md` | Resolution rules and the outlet decision |
| `handoff/service-sections.json` | Sixteen viewer sections with operations, tables, screens, flows, coverage |
| `docs/active/flow-coverage-plan.md` | The three passes and where the ceiling is |
