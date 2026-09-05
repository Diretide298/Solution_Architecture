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
| `deploy/c-flash-sale.yml` | replicas, cpu and memory limits, pgbouncer, postgres-hot, one database |
| `deploy/variants/*.yml` + README | variants B, C and D, and the two the README declines to build |
| `states/burst-environment.yaml` | nine states, twelve transitions, triggers, guards, the 409 |
| ADR-0031 … 0035 | contention, load shedding, the outbox, the burst environment, the four cost points |
| ADR-0037 | what may be inside a lock — the lease hold, and the acceptance criterion for it |
| ADR-0038 · ADR-0039 | a cell is a region, one database per tenant; the control plane's own home |
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

- ~~**the lease hold time**~~ — no longer mine. ADR-0037 decides it: the lock
  reads the row, decides and writes it, nothing else is inside, and
  `holdContentionMs` under 1ms is the acceptance criterion. The default is
  **0.5ms** and the contracts implement it — all four operations declaring
  `x-ticvai-lock` carry `x-ticvai-lock-excludes`. It was 6ms and mine.
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

**The baseline moved on 3 September** and every row below moved with it. It was
167/s, from a 6ms lease that ADR-0037 forbids and the contracts no longer
describe. At 0.5ms the wall is 2,000/s and **the hottest row at the hardest load
this model runs asks for 405** — so the wall is at 20% and most of this table is
now a list of limits nothing reaches.

| | changes | lease ceiling | note |
|---|---|---|---|
| **A** | nothing | **2,000/s** | the baseline, ADR-0037 |
| **B** | 23 of 35 reads from Redis | 2,000/s | relieves a limit nothing reaches |
| **C** | 16 lease shards | 26,000/s | multiplies a ceiling at 20% — and fragments the last seats |
| **D** | 50ms write coalescing | 2,000/s | fewer lock acquisitions, same holds |
| **R** | Redis as the pooler | 2,000/s | the README declines this, and it is right |
| **E** | idempotency and both reads back **inside** the lock | **167/s** | what it measured before ADR-0037 |
| **F** | guarded single-statement decrement | **5,000/s** | removes the lock entirely |
| **X** | read-then-update guard | 2,000/s | **oversells** |
| **N** | no pre-warm, reactive scaling | 2,000/s | scales into a peak already over |
| **M** | compose taken literally, 4/4/3 fixed | 2,000/s | **lost to capacity** |

**Run E first.** It is the only row that makes anything fail on the lease path,
and it is what this environment looked like two days before the simulator was
written — the whole argument for ADR-0037, in one slider.

C no longer competes with anything. It multiplies a ceiling already five times
the peak demand and pays sub-pool fragmentation for it, which is why ADR-0037
files it as a measurement rather than a candidate. F is still the better answer
and still deferred, because it commits the reservation immediately and needs the
sweeper CF-115 chose leases to avoid.

*(The oversell and capacity-loss figures were run at the old baseline and are
left unquoted rather than restated from memory. `X` and `M` still fail; the
numbers need a run.)*

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
4. **The per-statement `synchronous_commit` split is written nowhere.** The
   server-wide flag was the finding and it is gone — all four configurations
   dropped it on 31 August, because at a fraction of the statement ceiling it
   bought headroom this environment already had and paid acknowledged-commit
   durability on the money path for it. What replaces it is `SET LOCAL`, for
   telemetry and analytics writes only, stated in one compose header and
   declared by no operation. **`ADR-0035` still states the server-wide setting
   as its decision** and is amended rather than rewritten.
5. **One `postgres-hot`, one database** — settled twice while this board was
   being drawn. ADR-0036 made the burst cell a stated exception on 31 August;
   ADR-0038 superseded it on 3 September with one instance and one database,
   because a burst cell is one tenant and one event. What is open is not the
   decision but the artefacts: no `CREATE DATABASE`, no `PARTITION BY venue_id`,
   and `control` still inside the tenant template.
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
