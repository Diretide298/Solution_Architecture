# Three deployment scenarios — CF-162

**Requested by the client on 24 August**, each with an architecture, autoscaling behaviour and
failure handling. **Open since.**

**Runnable configurations in `deploy/`.** Numbers below are sizing hypotheses with a named way to
falsify each one — `tools/bench.py` is the way.

---

## The number that decides all three

**250,000 requests a day is 2.9 per second. Five thousand per second is 1,700 times that.**

**At 5k RPS the entire daily volume arrives in fifty seconds.**

Every scale in the brief — 10k through 250k — sits between 0.1 and 2.9 RPS at steady state. **Daily
volume sizes nothing.** The burst does, and the burst is not a bigger version of the day.

---

## (a) Independent tenant — 18 containers

**One tenant, one database, one of everything.**

| | |
|---|---|
| **Right for** | A tenant who requires isolation contractually · a tenant alone in a jurisdiction · one large enough that its own load justifies the stack |
| **Wrong for** | Everybody else. **100–200 tenants this way is 3,000 containers** against 2.9 RPS each |
| **Blast radius** | One tenant. A failure takes them down and nobody else |
| **Scaling** | Vertical first. Horizontal means a second stack, which is scenario (b) |

**Postgres 2 CPU / 4 GB, `max_connections=200`.** Redis 1 GB. Every service one replica.

**Autoscale: none.** At 2.9 RPS there is nothing to scale on, and a replica that never activates is
a cost with no purpose.

**Expected p95 200 ms read, 400 ms order.** If it is worse than that at this load, the problem is
the query and not the topology.

---

## (b) Shared platform — 27 containers

**The hybrid placement, sized for many tenants in one cell.** This is the default and should be.

**Shared and autoscaled** — Catalogue 4–20, Order 4–16, Identity 3–8, Access 2–6. **Their load is a
function of requests.**

**At the venue** — F&B, Inventory, Retail, VenueOps, one per venue. **123 of their operations work
offline**, and a shared service cannot be locally available. A kitchen also runs at the speed of a
kitchen: no spike makes food faster.

**At the region** — Ledger and CrossRegion. **Currency, fiscal year and tax are region properties**
(ADR-0018), and region is neither tenant nor venue.

### pgbouncer is not optional here

**20 Catalogue replicas at 20 connections each is 400 against a primary that will not want them.**
Transaction pooling is what makes horizontal scaling of the shared tier possible at all — without
it the shared tier stops scaling at about six replicas and the bottleneck looks like the database.

**Postgres 8 CPU / 16 GB, `max_connections=500` behind the pooler.** Redis 8 GB.

### The trade, stated rather than assumed

**Blast radius is the cell — every tenant in it.** Mitigated by `scope_path` partitioning, which is
correctness rather than isolation: a bug reaches one tenant's rows, an outage reaches all of them.

**That belongs in a tenant contract**, not in an architecture document nobody reads.

---

## (c) Flash sale — 6 containers, and most of the platform absent

**Three services, not sixteen.**

**The burst path is eleven operations** — `listProducts`, `getProduct`, `listPerformances`,
`getAvailability`, `acquireInventoryHold`, `createSeatHold`, `addCartLine`, `evaluatePromotions`,
`getCart`, `createOrder`, `createPayment` — **across Catalogue and Order, plus authentication.**

**Marketing, Reporting, Inventory, F&B, Retail, Maintenance, VenueOps, WhiteLabel and AI see no
part of a ticket sale and are not deployed.**

**17 tables of 380.**

```
catalogue.product · variant · performance · channel_capacity · price_list · inventory_hold
orders.cart · cart_line · sales_order · order_line · payment
seating.seat_hold · promotions.promotion
ledger.fx_rate · journal_entry · posting · platform.workstation
```

**Catalogue 20 replicas, Order 16, Identity 6.** Postgres 16 CPU / 32 GB with
`synchronous_commit=off`. pgbouncer at 5,000 client connections.

### `synchronous_commit=off` is a decision, not a flag

**A crash loses the last few milliseconds of commits.** For a sale lasting fifty seconds that
reconciles afterwards, the throughput is worth more than the durability window.

**It must be somebody's decision.** Copied from a tuning guide it is a data-loss bug waiting for an
incident review.

### 🔴 `acquireInventoryHold` is where this fails

**Every buyer wants the same rows.** The lease path serialises on contention, and **no amount of
horizontal scaling helps a contended row** — twenty Catalogue replicas all queue behind the same
lock.

**Load-test this before anything else.** It is the only number that decides whether the scenario
works, and it cannot be estimated from a per-instance figure.

### 🔴 And the reconciliation route back has no design

**Orders taken in an ephemeral environment have to land in the permanent platform afterwards.**
Nothing in the package models it, and it is the open half of CF-162.

**The shape is already in the package one layer down.** `syncOrders` reconciles a till's offline
journal: a device id, a monotonic sequence, idempotent replay, and `sync.rejection` for what will
not apply — *kept, because a till that loses a rejected sale silently is worse than one that
reports it.*

**The same three properties apply**: an environment id in place of a device id, a sequence that
orders the replay, and a rejection table somebody works afterwards.

**What is genuinely new**: the ephemeral environment holds a *snapshot* of the catalogue, not a
replica. **If the permanent platform changed a price during the sale, the reconciliation has to
decide which one the guest paid.** That is a policy question and it is unanswered.

---

## Scale matrix

| Scale | Daily | Target RPS | Scenario | Catalogue | Order | Identity | Postgres |
|---|---:|---:|---|---|---|---|---|
| Small | 10k | 1k | (b) | 2–6 | 2–6 | 2–4 | 2 CPU / 8 GB |
| | 25k | 1k–2k | (b) | 2–8 | 2–8 | 2–4 | 4 / 8 |
| | 50k | 2k | (b) | 4–10 | 4–8 | 3–6 | 4 / 16 |
| Medium | 100k | 2k–3k | (b) | 4–12 | 4–10 | 3–6 | 8 / 16 |
| | 150k | 3k | (b) + replica | 6–16 | 4–12 | 4–8 | 8 / 32 |
| Large | 200k | 3k–4k | (b) + pooler | 6–20 | 6–16 | 4–8 | 8 / 32 |
| Maximum | 250k | 5k | **(c)** | 20 | 16 | 6 | 16 / 32 |

**Only the last row changes architecture**, and it changes it because the shape of the traffic is
different rather than because there is more of it.

**Autoscale on RPS, not CPU.** CPU lags a burst by the time it takes to fill a queue, and a
fifty-second sale is over before a CPU-triggered scale-out serves anything.

---

## What each scenario needs measured

**All three**: RPS per instance at p95 under 200 ms · connections per instance under load · cache
hit ratio on the real key distribution · cold start to a filled pool.

**(b) specifically**: the replica count at which pgbouncer becomes the bottleneck instead of
Postgres, and whether `scope_path` partitioning holds its plan as the table grows.

**(c) specifically**: **lease contention throughput on one hot performance.** Everything else is
arithmetic once that number exists.

```bash
python3 tools/bench.py --topology hybrid --pattern hot-venue --rps 5000 --seconds 600
```

**`hot-venue` sends 90% of load to one venue.** That is the Bahrain distribution, and it is the
pattern that distinguishes the three scenarios most sharply.

---

## Still blocking

**CF-161** — one database per cell or one per service. **Every connection number above assumes
shared-schema.** Per-service databases change the pooling arithmetic entirely, and ADR-0028 still
reads Accepted while contradicting a client-facing recommendation.

**CF-64** — AWS or Azure. **Everything here is provider-neutral; the managed Postgres tier, the
Redis offering, autoscale semantics and cost are not.** CF-64 also carries RPO and RTO, which are
stated nowhere.
