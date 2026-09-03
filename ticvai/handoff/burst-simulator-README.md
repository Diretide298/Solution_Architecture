# Burst environment simulator — handoff

Two pages and a model. Both pages open directly in a browser; no build step, no
server, no dependencies.

```
Burst Simulator.dc.html    the flash-sale environment, simulated
Shared Cell.dc.html        the shared cell at rest, two across the board
burst-model.js             the model — every number on both pages comes from here
support.js                 the runtime the pages load (do not edit)
brand/                     the Adam lockup, copied from viewer/public/brand
```

Open `Burst Simulator.dc.html`. The other page is linked from its header.

---

## What the model is

`burst-model.js` solves a whole run as one value rather than integrating per
animation frame. That is what makes the timeline scrubbable and a result
reproducible: `solve(cfg, script)` returns samples, phases, named failures, a
summary and a recommendation. Free-run mode steps the same `stepWorld`, so a
scripted scenario and a hand-driven one cannot disagree about the model.

**Queueing** is M/M/c per cluster on the per-replica rates. **Row wait** is
M/D/1 on the lease — a held row is a deterministic service time — and it is
added to the p99 of the service that takes the locks, because a p99 that
excludes lock wait reads comfortably while every buyer convoys on one row.

**The sizing algorithm is the package's**, stated in `tools/derive-sizing.py`:

```
replicas = max(floor, ceil(load_rps × share / (rps_per_replica × target_utilisation)))
```

It is applied to the peak that is *coming* rather than the load that is
present, so the environment is standing and warm before the sale opens.
Provisioning takes minutes and a sale takes seconds.

---

## Where every figure comes from

| Source | What it provides |
|---|---|
| `handoff/burst-scope.json` | services, weighted shares, 34 operations, callsPerBuyer, contended tables, the two routing paths |
| `tools/derive-sizing.py` output | the algorithm, target utilisation, the two mixes, three cell sizes, per-service scale-out triggers |
| `deploy/c-flash-sale.yml` | replicas, cpu and memory limits, pgbouncer, postgres-hot, `synchronous_commit = off` |
| `deploy/variants/*.yml` + README | variants B, C and D, and the two the README declines to build |
| `states/burst-environment.yaml` | nine states, twelve transitions, triggers, guards, the 409 |
| ADR-0031 … 0035 | contention, load shedding, the outbox, the burst environment, the four cost points |
| `TICVAI_Deployment_Technical.pdf` | three venue tiers, 22 calls a buyer, the compression arithmetic |
| `TICVAI_Hosting_Summary.pdf` | $11.76/h AWS and $9.76 GCP for option 3, $3,485/mo for the shared cell, the search index |

The model reproduces the documents' own derived figures exactly: 60,000 seats
at 95% buying × 22 calls ÷ 2h × 6 = **1,045 RPS**, and ÷ 20 min = **6,270 RPS**.
At the package's own inputs the calculator lands on the package's own floors,
**14 / 8 / 2**.

---

## What is NOT from the package

Marked `mine` wherever it appears in the UI, because the package measures no
latency and states no distribution for these:

- **the lease hold time** (6ms default) — the ceiling is one over it
- **the container start time** (20s) — cold start to ready
- **the p99 SLO** (800ms) — what a buyer would tolerate
- **the hold TTL** (45s) — the package states none at all
- **shard unevenness** (25%) — how sharded stock depletes, for variant C
- **the insert cost multiple** (1/0.15 of a lease) — index tail versus row lock
- **the shed channel mix** (70/15/10/5 guest/public/staff/service)

`rpsPerReplica` (400 / 250 / 600) is ADR-0032's autoscale trigger, which the
package itself calls a hypothesis until `tools/bench.py` runs. Everything
derived from it — including the service times, and therefore every p99 —
carries that caveat.

---

## The ten configurations

Everything identical except the one thing named; anything else differing
invalidates the comparison.

| | changes | lease ceiling | note |
|---|---|---|---|
| **A** | nothing | 167/s | the baseline |
| **B** | 23 of 35 reads from Redis | 167/s | relieves a limit nothing reaches |
| **C** | 16 lease shards | 2,167/s | moves the wall — and fragments the last seats |
| **D** | 50ms write coalescing | 167/s | fewer lock acquisitions, same holds |
| **R** | Redis as the pooler | 167/s | the README declines this, and it is right |
| **P** | pgbouncer tripled | 167/s | raises a limit nothing reaches |
| **E** | idempotency and reads moved out of the lock | **2,000/s** | the cheap fix, and it beats sharding |
| **F** | guarded single-statement decrement | **5,000/s** | removes the lock entirely |
| **X** | read-then-update guard | 167/s | **oversells 46,502 seats** |
| **N** | no pre-warm, reactive scaling | 167/s | scales into a peak already over |
| **M** | compose taken literally, 4/4/3 fixed | 167/s | **63,302 lost to capacity** |

E dominates C: same ceiling, none of the fragmentation, no rebalancer, no
reconciliation obligation. F dominates E. Shard third, if at all.

---

## Findings the simulator surfaces

1. **`catalogue.channel_capacity` is worse than the lease** and is not flagged
   `contended` in `burst-scope.json`. Four calls a buyer reach it against
   three for `inventory_hold`, so it refuses more.
2. **Two generated files disagree** about the sale floors: `derive-sizing.py`
   says 14 / 8 / 2, `burst-scope.json` says `min` 4 / 4 / 3 and
   `expectedAtTarget` 8 / 5 / 3, and compose is told 4 / 4 / 3.
3. **`seating.seat_hold` is modelled as one row a performance** because the
   package flags it contended — but its own note describes a per-seat claim,
   which would be many independent locks. The two cannot both be true, and it
   changes which row is the wall.
4. **`synchronous_commit = off` buys throughput this environment does not
   need** — it runs at a fraction of its statement ceiling — while converting
   any crash into lost acknowledged orders.
5. **One `postgres-hot` for three services** asserts an answer to database
   segregation, which is open.
6. **Draining has no checkout TTL**, which makes it a correctness dependency
   rather than housekeeping: it must exceed worst-case lock wait plus the
   gateway round trip.

Items 3 to 6 are listed on the page under *"What this board asserts that isn't
settled"*. They need a decision, not a code change.

## Three things to verify in the package

In priority order, and none of them takes long:

1. **Is the inventory guard in the `WHERE` clause or in application code?**
   `UPDATE … SET remaining = remaining - 1 WHERE id = ? AND remaining > 0
   RETURNING remaining` is safe at any contention level. Anything that reads
   first is variant X.
2. **Is payment authorisation inside or outside the hold transaction?** If
   outside, the money-versus-seat split is live and needs a compensating
   reversal, not a longer TTL.
3. **What is the idempotency key on order replay, and is it stable across a
   client-side retry?** Under saturation the replay count will not be zero,
   and that is the first time the key sees real traffic.
