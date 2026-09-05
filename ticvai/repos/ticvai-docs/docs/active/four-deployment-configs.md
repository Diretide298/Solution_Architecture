# Four deployment configurations, priced against each other

**Runnable in `deploy/`. All four use the same images, the same schema and the same limits — only
placement changes.**

---

## What a cell is, before the comparison

**A cell is a deployment and a legal boundary at once** (ADR-0001). `control.cell` carries
`region_id`, `country_code` **and** `tenant_id` — because a cell is *in* one region and holds one
tenant or many.

**`CellKind` already exists**: `shared · dedicated · onPremise · controlPlane` (ADR-0017), and
`tenantId` is documented as *"null on a shared cell, which holds many — nullable since the ADR-0014
amendment, it was required when a cell meant one tenant."*

**So "a cell per tenant" is `dedicated` and already modelled.** What is not modelled is a cell per
*venue*, and that is where the interesting question sits.

---

## The four, measured on one basis

| Config | Containers | vCPU | GB | Databases |
|---|---:|---:|---:|---:|
| **a** independent tenant | 18 | 19 | 13 | 1 |
| **b** shared platform | 39 | 67 | 53 | 1 |
| **c** flash sale (ephemeral) | 45 | 177 | 127 | 1 |
| **d′** shared burst + venue-local offline | 44 | 74 | 61 | 4 |

**At 200 tenants averaging three venues:**

| Config | Containers | Databases | |
|---|---:|---:|---|
| **a** | **3,600** | **200** | one full stack per tenant |
| **b** | 815 | 1 | one cell, venue services per venue |
| **d′** | 1,412 | **601** | shared tier plus 600 venue cells |
| **c** | 45 | 1 | ephemeral, one event, then gone |

**Config (a) is 4.4× config (b) in containers and 200× in databases**, against a steady state of 2.9
requests per second per tenant.

---

## 🔴 The config you named that does not work

**"All tenants, cells created at venue level."**

**A venue is safely inside one jurisdiction, so residency holds** — that part is fine and it is why
this is worth taking seriously at all.

**But it multiplies the wrong thing.** A cell carries a Postgres, a Redis and a control-plane
registration. **600 cells is 600 databases to migrate, back up, monitor and connection-pool**, and
`CrossRegionService` would need a counterpart in every one.

**And the isolation is aimed where the risk is not.** A venue's spike is contained — but **the spike
is in that venue**. Its cell absorbs 5,000 RPS alone while 599 others sit idle, and there is no
shared capacity to burst into.

---

## 🔴 And the one that is inverted

**"Venue-level cells holding only the horizontal-scaling services."**

**Those four are Catalogue, Order, Identity and Access — the ones that carry the burst.**

**Per venue, each must absorb its own venue's spike.** A flash sale for one event means that venue
needs twenty Catalogue replicas while every other cell is idle. **The problem has moved, not gone,
and the pooling that would have absorbed it is gone with it.**

**The data says the inverse.** Burst services shared; **offline services at the venue.**

---

## d′ — shared burst tier, venue-local offline tier

**Four services at the venue, and they are the offline ones.**

**103 of their 286 operations work offline.** A venue with no network still cooks, still counts
stock, still sells merchandise. **That is the product, not a resilience feature** — and a shared
service cannot be locally available.

**Four services shared, and they are the burst.** A spike pools across venues instead of being
trapped in one.

### The design constraint, and how it resolves

**The venue tier owns 80 tables and reads 100.** It reaches ten foreign schemas — **43 reads and 15
writes across the boundary.**

**Foreign reads are cached, not fetched.** 12 into `platform`, 8 into `identity`, 6 into
`catalogue` — the org tree, who a principal is, what a menu item is. **All slow-changing, and all
already published to a till as a bundle** (ADR-0013). The same mechanism serves a venue cell.

**Foreign writes are journalled, not written.** 5 into `orders`, 4 into `marketing`, 4 into
`catalogue`. A food order becomes an order; a guest note becomes a profile update. **Those go
through `syncOrders` and `sync.rejection`** — the mechanism exists and F33 walks it.

### What it costs and what it buys

**601 databases at 200 tenants.** Small ones, but 601 to migrate and back up.

**A venue keeps trading through a regional outage**, and the burst pools.

**🔴 CF-161 has to be settled before that is a sentence anybody can cost.** If databases are
segregated per service as well, 601 becomes several thousand.

---

## What I would recommend

**Default to (b).** One cell per jurisdiction, shared burst tier, venue services per venue but not
per-venue *cells*. **815 containers and one database at 200 tenants.**

**Offer (a) as `dedicated`, per tenant per region.** A tenant in UAE and Saudi gets two cells, not
one — **the client's request survives ADR-0001 that way and not otherwise.**

**Offer (d′) as an upgrade to (b)**, not an alternative. **The only reason to take it is a venue
that must trade through a regional outage**, and that is a conversation about what a venue is
paying for.

**Keep (c) ephemeral and separate.** It is not a bigger platform; it is three services, 17 tables of
380, and fifty seconds.

---

## What would falsify any of this

**Every number above is a container count and a limit, not a measurement.**

**The one that decides d′**: whether a venue-local Postgres at 1 CPU / 2 GB sustains the F&B and
Inventory workload during service. If it does not, the venue tier needs more and the arithmetic
changes.

**The one that decides b at scale**: the replica count at which pgbouncer becomes the bottleneck
instead of Postgres.

**The one that decides c**: lease contention throughput on a single hot performance. **No amount of
horizontal scaling helps a contended row**, and that number is a property of the contention model
rather than of any instance size.

```bash
python3 tools/bench.py --pattern hot-venue --rps 5000 --seconds 600
```
