# Deployment architecture — three topologies, and what the package already decides

**31 August 2026.**

---

## What cannot be delivered, and why

**Build is 0%.** 380 tables are specified and none is written as DDL; no service exists, no
container image exists, no endpoint answers. **There is nothing to load-test.**

A reproducible environment running one workload against three topologies needs three deployed
topologies. **Any table below reporting CPU utilisation, p99 latency or error rate would be
fabricated**, and a fabricated benchmark is worse than none — it gets planned against, and the first
real measurement contradicts a decision already made.

**What is deliverable is better than a benchmark for the placement question specifically**, and it
is this: **every one of the 1,025 operations already declares the scope it resolves at.** That is a
decision recorded in the contracts, not a number inferred from load. A benchmark would measure
consequences of the placement; the contracts state the placement.

**What is missing and only measurement can give**: the constants. Requests per second a single
instance sustains, connection cost per pool, cache hit ratio under the real key distribution,
autoscale reaction time. **Those are in section 7 as a test specification.**

---

## 1 · The two numbers do not describe the same system

**250,000 requests a day is 2.9 per second.** Five thousand per second is **1,700 times that**.

**At 5,000 RPS the entire daily volume arrives in fifty seconds.**

That is not a busy platform. **It is a flash sale**, and it is exactly the failure Qossai described on
31 July: a Bahrain theatre where roughly 30,000 people tried to buy at once, the platform went down,
and the outage cost the client relationship.

**So daily volume does not size anything here.** Every scale in the brief — 10k through 250k — sits
between 0.1 and 2.9 RPS at steady state. **The sizing question is entirely the burst**, and the burst
does not hit sixteen services evenly.

**A 5,000 RPS spike is a queue of people buying one thing.** From the flows already walked, it lands
on: catalogue read, availability, lease acquisition, order creation, payment. **Five paths across
four services.** Marketing, Reporting, Inventory, Maintenance and F&B see no part of it.

**Which means the honest answer to "how do we size for 5k RPS" is: you do not size the platform for
it. You size four services for it and leave twelve alone.**

---

## 2 · Agent 1 — every service per venue

**Refutable from the data before any test runs.**

**`IdentityService` carries 81 inbound cross-service touches, more than any other service.** Per
venue, a guest who signed in at one venue is unknown at the next. A staff member's role is granted
at a scope in a tree that spans venues, and 304 of 380 tables anchor on `platform.scope` — **the
hierarchy itself is not venue-scoped, so the service that resolves it cannot be.**

**`CrossRegionService` is incoherent per venue.** Its job is moving a pseudonymous guest link
*between jurisdictions* (ADR-0010). A per-venue instance has no counterpart to talk to.

**`WhiteLabelService` is 100% tenant-scoped** across all 50 of its operations. A per-venue instance
would hold one tenant's branding, replicated once per venue, and a publish would have to fan out to
every one.

**And the arithmetic.** Sixteen services × one venue = sixteen deployments. A tenant with eleven
venues is 176. **At 200 tenants averaging three venues, 9,600 service instances before a single
request arrives** — against a steady-state load of 2.9 RPS.

**Verdict: refuted.** Not on cost, though the cost is absurd. **On correctness** — three services
cannot be venue-scoped without breaking what they do.

---

## 3 · Agent 2 — every service per tenant

**Also refutable, and more subtly.**

**It contradicts ADR-0001.** A cell is one jurisdiction, and a tenant can operate in more than one.
A per-tenant stack spanning UAE and Saudi violates data residency — **the constraint that shapes the
entire platform.**

**`LedgerService` is 68% region-scoped**, and region is neither tenant nor venue. Currency, fiscal
year and tax rules are region properties (ADR-0018). **A per-tenant ledger holding two regions
either splits internally — which is the multi-tenancy it was meant to avoid — or gets it wrong.**

**And the isolation it buys is aimed at the wrong axis.** The spike is one *venue* on a Saturday, or
one *event* going on sale. A per-tenant stack scaling for that scales eleven venues' worth of every
service because one venue is busy.

**Verdict: refuted.** It isolates by the wrong boundary and breaks the jurisdiction rule.

---

## 4 · The three-way split is missing an axis

**The brief offers venue, tenant, shared. The platform has four.**

**venue 682 (67%) · tenant 247 (24%) · region 48 (5%) · workstation 45 (4%) · brand 2 ·
platform 1**

**Region is 48 operations and it is where the money lives** — FX rates, fiscal periods, legal
entities, tax codes, settlement. **`LedgerService` sits there and belongs in neither of the two
buckets offered.**

**Workstation is 45** and it is not a deployment scope at all — it is a till, and its operations run
against a shared service with the workstation as a parameter.

---

## 5 · The placement map, derived from declared scope

**Dominant scope is the contract's own declaration, not an inference.**

| Service | Scope | % | In | Off | Placement | Scaling driver |
|---|---|---:|---:|---:|---|---|
| Catalogue | venue | 94 | 71 | 18 | **SHARED/HPA** | request volume — read |
| Order | venue | 79 | 32 | 26 | **SHARED/HPA** | request volume — write |
| Identity | tenant | 59 | 81 | 4 | **SHARED/HPA** | request volume — auth |
| Access | venue | 84 | 38 | 12 | **SHARED + edge** | request rate, flat |
| Tenancy | venue | 79 | 64 | 10 | SHARED | read-mostly, cached |
| Ledger | **region** | 68 | 20 | 4 | **REGION** | region count, batch |
| Platform | tenant | 97 | 11 | 1 | SHARED | tenant count |
| WhiteLabel | tenant | 100 | 3 | 3 | **TENANT** | tenant count |
| CrossRegion | tenant | 56 | 3 | 3 | **REGION-PAIR** | region count |
| Fnb | venue | 97 | 2 | **47** | **VENUE** | venue count |
| Inventory | venue | 94 | 17 | 15 | **VENUE** | venue count |
| Retail | venue | 89 | 5 | 2 | **VENUE** | venue count |
| VenueOps | venue | 95 | 15 | **39** | **VENUE** | venue count |
| Marketing | venue | 73 | 25 | 9 | SHARED | queue/worker load |
| Ai | tenant | 53 | 12 | 0 | SHARED | external API limits |
| Reporting | venue | 93 | 1 | 0 | SHARED | replica load, batch |

### The rule, stated once

**A service is shared and horizontally scaled when its load is a function of requests. It is scoped
when its load is a function of how many of something exist.**

**Three tests, in order:**

**Does it appear on the burst path?** Catalogue, Order, Identity and Access do. Nothing else does.
**Those four scale on RPS and must be shared** — a per-venue Catalogue cannot absorb a spike aimed at
one venue, because the spike is *in* that venue.

**Is it read by everyone?** Identity at 81 inbound touches, Tenancy at 64, Catalogue at 71. **A
service most others depend on is a service that must be one thing.** Replicating it per venue
multiplies the reads without reducing them.

**Is its data confined to the boundary?** F&B at 97% venue-scoped, 47 offline operations, and two
inbound touches. **Nothing outside a venue reads its kitchen tickets.** That is a service that can
sit at the venue and should — because 47 offline operations means it must keep working when the
venue's network does not.

### Where the rule is uncomfortable, and why it still holds

**F&B, Inventory, Retail and VenueOps are venue-placed and they are the largest group** — 286
operations across four services. **The instinct is to share them for efficiency.**

**Offline is why not.** 123 of their operations work offline: a till trades from a local journal, a
kitchen display keeps sending food out, a stock count happens where the stock is. **A shared service
cannot be locally available**, and local availability is the product rather than a resilience
feature.

**They also do not need to scale.** A kitchen runs at the speed of a kitchen. **No traffic spike
makes food faster.**

---

## 6 · Deployment configurations by scale

**These are shapes, not measurements.** Instance counts assume a per-instance capacity that the
benchmark in section 7 exists to establish. **Treat every number as a hypothesis with a named way to
falsify it.**

**One thing holds across all seven rows**: steady state never exceeds 3 RPS, so **the whole matrix is
about burst headroom and nothing else.**

### Small — 10k to 50k/day, 1k–2k RPS

**Single cell. Shared services at minimum replicas, venue services co-located.**

Catalogue 2–6, Order 2–6, Identity 2–4, Access 2 + edge cache. Everything else 1–2.
**Postgres: one primary, one replica.** Redis: single node, 2 GB.
**Autoscale on RPS, not CPU** — CPU lags a burst by the time it takes to fill a queue.
**p95 target 200 ms on read, 400 ms on order creation.**

**Failure characteristic**: one cell, so a cell failure is total. **Acceptable at this scale and it
should be stated rather than assumed**, because 99.99% was agreed on 31 July and a single cell does
not deliver it.

### Medium — 100k to 150k/day, 2k–3k RPS

**Same topology, more headroom, and the first read replica that matters.**

Catalogue 4–12 with a replica behind it. Order 4–10. Identity 3–6.
**Postgres: primary plus two replicas**, Reporting pinned to the analytical one (ADR-0016).
Redis: 3-node cluster, 8 GB. **Marketing workers separate from its API** — a campaign send is queue
depth, not request rate, and mixing them makes both unpredictable.

### Large — 200k/day, 3k–4k RPS

**Catalogue and Order autoscale independently. The lease path becomes the constraint.**

**`acquireInventoryHold` is where a flash sale actually fails**: contended rows, and every buyer
wants the same ones. **This is the thing to load-test first**, not the catalogue read.

Catalogue 6–20, Order 6–16, Identity 4–8.
**Connection pooling in front of Postgres becomes mandatory** — 20 Order instances at 20 connections
is 400 against a primary that will not want them.

### Maximum — 250k/day, 5k RPS

**This is CF-162 scenario (c), and it is not a bigger version of the others.**

**Fifty seconds of the day's entire volume.** The right answer is a **short-lived environment for one
sale** — the client asked for exactly this on 24 August and the package does not model it.

**What it needs**: a catalogue replica or snapshot, a lease path that can serialise contention, and
**a reconciliation route for its orders back into the permanent platform.** The last is the hard
part and has no design. **Same shape as offline sync, one layer up.**

**What it does not need**: Marketing, Reporting, Inventory, Maintenance, F&B, Retail. **Six services
that see no part of a ticket sale.**

---

## 7 · The benchmark that would validate this

**Run it when there is something to run it against.** The workload does not need inventing — it is
in the package.

**Request mix from the flows.** F58 a ticket sold at a till, F59 a seat picked and held, F61 a gate
admitting a group, F43 the concurrency case. **Those are the real sequences with the real operation
counts, already walked.**

**Six patterns, and the fifth is the one that matters:**

steady · burst 2×–5× · venue-heavy · tenant-heavy · **one venue generating disproportionate load** ·
even.

**The fifth is the Bahrain case.** It is also the one that distinguishes the three topologies most
sharply, because it is where per-tenant isolation fails — one venue's spike scales a whole tenant.

**Establish these constants, which nothing else can supply:**

RPS per instance at p95 under 200 ms · connections per instance under load · cache hit ratio on the
real key distribution · **lease contention throughput on a single hot performance** · autoscale
reaction time from trigger to serving · cold start for each service image.

**The lease number is the one to get first.** Everything else is arithmetic once you have it; that
one is a property of the contention model and cannot be estimated from a per-instance figure.

---

## 8 · What this depends on that is still open

**CF-161** — one database per cell or one per service. **Open since 24 August, ADR-0028 still reads
Accepted, and it contradicts a client-facing recommendation.** Every instance count above assumes
shared-schema; per-service databases change the connection arithmetic entirely.

**CF-162** — the three scenarios. **This document is a partial answer to it** and should be attached
when it is closed.

**CF-64** — AWS or Azure, pending DESC. **Everything here is provider-neutral. Nothing below it can
be**: managed Postgres sizing, the Redis tier, autoscale semantics and cost are all provider
choices, and **CF-64 also carries the RPO and RTO targets, which are stated nowhere.**

---

## The single defensible sentence

**Scope where the data is confined and availability is local. Share where the load is a function of
requests rather than of how many venues or tenants exist. Place at region where the law does.**

**Four services scale on traffic. Four sit at the venue because they must keep working without a
network. Two sit at the tenant because their data is a tenant's. Two sit at the region because
currency and law do. Four are shared because everything reads them.**

**Nothing here needs a benchmark to decide. The benchmark decides how many, not where.**
