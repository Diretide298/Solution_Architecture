# TICVAI — deployment and scaling

**An onboarding brief for the CD engineer. 26 August 2026.**

---

# Part 1 · What TICVAI is

**A multi-tenant venue platform for the UAE and wider MENA market.** One tenant operates several
venues; a venue sells admission, food, retail and experiences; a guest arrives, is admitted, spends,
and leaves.

**Softlabs is building it for Miracle Star Trading L.L.C.** Client-side decisions come from
**Qossai** (commercial and finance) and **Allam** (product and compliance). **Dinesh Jadhav**, the
Softlabs CTO, owns the infrastructure position. **Chinmay Parab** leads the delivery.

## The scale of it

| | |
|---|---:|
| Operations across 28 OpenAPI contracts | **1,023** |
| Tables across 26 schemas | **379** |
| Screens across 15 platforms, 12 apps | **492** |
| Journeys traced end to end | **94** |
| State models | **122** |
| Architecture decisions recorded | **31** |
| Requirements, of which 2,647 contracted | **3,184** |

**Design is 93% of in-scope requirements. Build is 0%** — no DDL written, no service running.

**That gap is why you are here.** Everything else in this package can be wrong and corrected later.
**A database topology cannot**, and the decision is open.

## How the five layers join

**Screens name operations. Operations resolve against 28 contracts. Contracts persist to 26
schemas.** Every diagram, workbook and board is *derived* by resolving that join rather than written
twice.

**Nine validators enforce it and all nine pass.** If a figure in a diagram disagrees with a
contract, **the contract is right and the diagram has not been regenerated.**

---

# Part 2 · What the client has said about infrastructure

**Six workshops touched this. The quotations are from the minutes, not paraphrase.**

## 31 July — the founding constraint

**Read this minute first.** Qossai described a ticketing platform his team installed for a theatre
in Bahrain that **went down when roughly 30,000 people tried to buy tickets simultaneously** for a
concert by a popular regional singer.

> *"The outage took several days to resolve and ultimately cost the team the client relationship."*

**Allam added the reputational half** — an outage at a high-profile event spreads on social media
faster than it can be fixed.

**Qossai then scoped it honestly, and that matters for sizing:** only a small fraction of clients —
attractions, museums, exhibitions — will ever see that traffic. **It applies mainly to live events:
concerts, football matches.** But that segment is disproportionately high-risk.

**Softlabs' stated baseline is 2,000–3,000 concurrent users.** The gap to 30,000 is acknowledged in
the minute, and a consultant with Reliance Jio deployment experience was engaged for this concern
specifically.

**Agreed in that session:**

- **Target uptime 99.99%**
- **Read replicas are needed even without DR** — implying eventual rather than strict consistency,
  with liveness checks so a standby can take over
- **DR is a tenant-selectable module, not a default.** It carries cost, and some tenants will accept
  single-region UAE without it
- **High availability is separate from DR.** If one SQL instance or web service fails another takes
  over; DR is the full stack replicated to another region and configured separately
- **Redis clusters distributed across regions**, on Dinesh's BookMyShow precedent
- **Load testing built into the plan** — deliberately pushing traffic to observe behaviour, not
  capacity planning on paper

**And Dinesh's caution, which should shape how you present options:** cost has to be weighed
alongside scalability, and **firm user estimates are needed to size replica counts and load
balancing.** The team does not have them.

## 30 July — the release workflow

**Allam proposed and the group accepted:**

```
Development → Staging → Customer notification → Customer testing
            → Customer approval → Production
```

**Customer approval is a gate, not a courtesy.** Production deploys are not continuous in the usual
sense, and a tenant can withhold approval.

## 12 August — compliance and the stack

**.NET 8 and PostgreSQL**, for strong typing and ACID guarantees. **The ledger is append-only** —
transactions are never deleted; refunds and corrections are appended.

**The database is planned to scale horizontally** for peak season. The minute says plainly:
*"the specific approach for redeploying multiple database instances/clusters is still being worked
out."* **That is now your question.**

**Qdrant was proposed over Postgres native vectors** at expected volume — **subject to confirming
UAE compliance**, to avoid finding a limitation in production.

**Allam needed a component list for the Dubai Compliance Authority** — every AWS/Azure service
planned, so it can be validated. **That list is a deliverable and it does not exist.**

## 24 August — the meeting that reopened the database question

**Dinesh recommended segregating databases from the start:**

> *"Splitting a centralised database after 2–3 years in production is significantly more difficult
> than starting isolated and reconciling/merging later if needed."*

**This contradicts ADR-0005 and ADR-0028**, both of which say one Postgres per cell with 26 schemas.
**Recorded as CF-161. ADR-0028 still reads Accepted.**

**The client asked for three deployment scenarios**, each with a diagram, auto-scaling behaviour and
failure handling:

- **(a) independent tenant deployment**
- **(b) centralised/shared platform for small-to-medium tenants**
- **(c) dedicated infrastructure for large events and flash sales**

**Recorded as CF-162. Only (a) and (b) fit the current model.**

**They also asked for a transparent cost model at different scale levels, covering AWS and Azure.**
Not produced.

---

# Part 3 · What the design already decides

**These constrain you. Part 4 does not.**

## Sixteen services in five tiers

| Tier | Services | What it means for deployment |
|---|---|---|
| **Foundation** | Identity, Tenancy | **First and alone.** 304 of 379 tables anchor on `platform.scope_node`; twelve contracts read Identity. A restart here is an outage everywhere |
| **Commerce** | Catalogue, Order, Access, Ledger | The sale path. **Order autoscales; nothing else needs to** |
| **Operations** | Inventory, F&B, Retail, VenueOps | **Licensed per module** — a venue that bought none runs none |
| **Engagement** | Marketing, AI | **Nothing that takes money depends on these** |
| **Platform** | Control, WhiteLabel, Reporting, CrossCell | Provisioning, publishing, reporting, cross-region |

**Deploy order is tier order.** Catalogue before Order — a till pulls a bundle before it sells.
**Access last of the four**: it runs at the edge with a local cache and can lag safely.

**Four services can be down without stopping a sale**: Marketing, AI, Reporting, CrossCell. **A
deliberate property, and one that should be tested rather than assumed.**

## The stores

| Store | Operations | Notes |
|---|---:|---|
| postgres | 1,009 | One per cell, 26 schemas inside |
| redis | 675 | Sessions, resolution caches, idempotency |
| postgres-analytical | 20 | Reporting and AI. **Never the transactional primary** (ADR-0016) |
| qdrant | 9 | Vector search — the 12 August compliance question |
| derived | 5 | **Computed, never stored** |

**Redis is losable without consequence.** Nothing treats a cache entry as truth — a flush costs
latency, not correctness. **Size it for the hot path.**

**`derived` is not a store.** `inventory.stock_level` is computed from movements, and
`check-package` refuses any write to it: a stored level and a movement ledger that disagree is a
stock count nobody can reconcile.

## A cell is a jurisdiction

**One cell per jurisdiction** (ADR-0001) — a deployment and a legal boundary at once. **UAE data
residency is required.**

**Only CrossCellService reaches another region**, and it moves a pseudonymous guest link rather than
a guest (ADR-0010) — which is what lets a membership work in another country without moving personal
data.

**A cell is one jurisdiction, not one currency.** A GCC cell could hold AED and SAR; a UAE cell holds
Dubai and Abu Dhabi with different fiscal calendars. **Do not collapse the two.**

## Tenancy is a partition key

**Not one database per tenant** (ADR-0005). An operator with eleven venues is one tenant; four
hundred tenants would be four hundred databases to migrate, back up and monitor.

**Partitioning is by `scope_path`**, an ltree column that is prefix-comparable — `uae.dubai` contains
`uae.dubai.marina`.

**CF-161 reopens this. Read Part 4 before building against it.**

## 193 operations work offline, and it is the product

**A till trades from a local journal** (ADR-0013) and reconciles on sync. **A gate admits from a
package pulled before the session** — a scanner that fetches at first scan has already queued.

**A venue with no network still sells and still admits.**

**Your rollout strategy has to handle devices unreachable for hours that reconcile when they
return.** `syncOrders` carries a device id and a monotonic sequence rather than an idempotency
header, because a batch replay needs ordering and not just deduplication.

## Load is spiky and only one service has the spike

**Saturday evening is ten times Tuesday morning**, and that shape belongs to Order alone.

**Access is high-rate and flat** — forty scans a minute per lane, sub-300ms, edge-cached, offline-
capable. **F&B is two sharp peaks a day.** **Ledger is batch and correctness-over-availability**:
briefly unavailable is recoverable, briefly wrong is not.

## Configuration reaches devices

`ConfigurationProfile` and `ProfileDeployment` are state machines, not flags. **`deploying` is a real
state** — a fleet on two profiles is a venue where two tills disagree about a price — and
**`partiallyFailed` is deliberately not terminal.**

**You are inheriting a rollout model** expecting a target set, per-device acknowledgement, a named
list of failures rather than a count, and a rollback that reverts the devices that took it and
leaves the ones that did not.

---

# Part 4 · The three open decisions

## 🔴 CF-161 — one database or sixteen

**Dinesh's argument is asymmetric and correct on its own terms**: splitting later is harder than
merging later.

**The counter is operational cost** — sixteen databases to migrate, back up, monitor and
connection-pool **before a single table is written**, at 0% build.

**The scale figures from the same meeting point three ways:**

- 100–200 tenants centralised → schemas in one database
- Independent large tenants on their own infrastructure → whatever deploys simplest
- **Flash sales at 30,000 concurrent → neither**

**Open, and it blocks the DDL.** Writing migrations against an undecided topology means writing them
twice.

## 🔴 CF-162 — three scenarios, one modelled

**(a) and (b) fit the cell model. (c) does not.**

A short-lived environment for one flash sale, tens of thousands concurrent within hours, then gone.
**No tenancy of its own, reads a catalogue it does not own, and its orders have to land in the
permanent platform afterwards.**

**The reconciliation path back has no design** — the same shape as offline sync, one layer up.

## CF-64 — the cloud provider

**AWS or Azure, pending DESC.** Owned by Dinesh and Qossai.

**Everything above is provider-neutral. Nothing below it can be** — managed Postgres, the Redis
tier, Qdrant hosting, the CDN, the secret store.

**CF-64 also carries RPO and RTO, which are stated nowhere else.**

---

# Part 5 · What we need from you

**Ordered by what unblocks the most.**

**1 — A position on CF-161, with the cost of being wrong each way.** Not a preference. **What does it
cost to split a shared database in year two, and what does it cost to run sixteen from month one.**
That number decides it and nobody has produced it.

**2 — The three deployment scenarios**, each with a diagram, auto-scaling behaviour and failure
handling. **Scenario (c) has no precedent here** — and the hard half is not standing it up, it is
reconciling its orders back.

**3 — A cost model at three scale levels, AWS and Azure.** Requested 24 August. **Dinesh's point
stands: firm user estimates are needed**, and the only concrete numbers anyone has are 2,000–3,000
typical and 30,000 at a concert.

**4 — RPO and RTO per tier.** Ledger and Order do not tolerate the same loss and **nothing states
either.**

**5 — The component list for the Dubai Compliance Authority.** Every AWS/Azure service planned,
Qdrant included. Allam needed it in August.

**6 — Whether the rollout model in Part 3 is buildable as described**, or whether per-device
acknowledgement and `partiallyFailed` are more than the platform should own.

---

# Part 6 · Where to read

| | |
|---|---|
| `diagrams/hld/00-platform.yaml` | The whole platform — actors, surfaces, services, stores, externals, regions |
| `diagrams/hld/02-services.yaml` | Sixteen services, deploy order, 34 cross-service write edges |
| `docs/adr/0028-service-decomposition.md` | Why sixteen, and the four non-obvious decisions |
| `docs/adr/0001-cells-and-jurisdictions.md` | The cell model |
| `docs/adr/0013-local-first-point-of-sale.md` | Why a till trades offline |
| `docs/adr/0016-read-write-separation.md` | The replica rule |
| `handoff/TICVAI_Services_and_Data_Segregation.xlsx` | Services, schemas, cross-service writes, deploy order, hierarchy |
| `docs/registers/conflicts.md` | CF-161, CF-162, CF-64 in full |
| `sources/mom/TICVAI_MoM_31Jul2026__1_.docx` | **Read this one.** Bahrain, and the non-functional session |
| `sources/mom/TICVAI_MoM_2026-08-24_Infra_Cost_Ticketing.docx` | The database and costing workshop |

**Diagrams are derived, never hand-edited.** `check-package` fails a package whose diagrams are older
than their source.

---

## One thing worth saying plainly

**The client has been asking for infrastructure costing and deployment scenarios since 24 August and
has not had them.** Two of the three questions in Part 4 have been open for days, and **the entire
build sits behind them.**

**Nothing else in this package is blocked. This is.**
