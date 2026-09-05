# Burst variants — four configurations, one number that decides

**`deploy/c-flash-sale.yml` is A. The other three are in `deploy/variants/`.**

**Everything is identical except the one thing named.** Same images, same schema, same Postgres
flags, same replica floors — **anything else differing invalidates the comparison**, and it is easy
to do by accident while tuning one of them.

---

## Why these four

**9 of 55 calls per buyer touch a contended row.** That is the wall, and it does not move with
replicas, Redis size or pooler settings.

| | Changes | Attacks |
|---|---|---|
| **A** baseline | nothing | — |
| **B** read cache | 23 of 35 read calls served from Redis | database load |
| **C** lease shards | 16 sub-pools per performance | **the wall** |
| **D** write batching | 50 ms coalescing window | lock acquisitions |

### Two things deliberately not built

**Redis scale-up alone.** Redis is not the constraint — nothing treats a cache entry as truth and a
flush costs latency rather than correctness. **A bigger Redis makes misses cheaper and the misses
are not what is failing.** B is the useful version of that instinct: the lever is *what* is cached,
not the tier size.

**pgbouncer turned up.** Already handling everything in A, at **640 connections against 5,000
capacity — eight times headroom.** It stops being the bottleneck long before the lease does, and
raising a limit nothing is reaching changes nothing.

---

## Run them

```bash
for v in c-flash-sale variants/B-read-cache variants/C-lease-shards variants/D-write-batching; do
  docker compose -f deploy/$v.yml up -d
  python3 tools/bench.py --variant ${v##*/} --pattern hot-venue --rps 5000 --seconds 600 \
      --out results-${v##*/}.json
  docker compose -f deploy/$v.yml down
done
```

**`--pattern hot-venue` sends 90% of load to one venue.** That is the Bahrain distribution and the
only pattern that separates the four.

**Ten minutes, not one.** Autoscaling behaviour is the point; a sixty-second run measures a cold
start.

---

## The number

**`holdsPerSecond` — holds acquired per second on a single hot performance.**

**A, B and D will move p95 and leave it flat.** They reduce work nobody was queuing behind.

**C is the only one that should move it.** If it does not, **the ceiling is Postgres row locking
itself** — and that is worth knowing before anybody buys more replicas, because no application
change reaches it.

**`holdContentionMs` is recorded separately from general latency** for the same reason: a lease
taking 400 ms while every read takes 12 ms is invisible in a p95 across all requests.

---

## What each variant costs if it wins

**B** — a cache that must be invalidated on nothing, because the snapshot cannot change. **Almost
free**, and the only risk is somebody later caching `getAvailability`, **which is how two people buy
the same seat.**

**C** — 🔴 **reconciliation.** Sixteen sub-pools sum to the performance capacity and each can empty
separately, so the last seats fragment: fifteen shards empty and one holding four is a performance
that looks sold out to most buyers. **Rebalancing is the hard part and this variant does not
implement it.** It exists to find the ceiling, not to ship.

**D** — up to 50 ms on the first write in a window. **Invisible on a read path and not on a
checkout**, which is why the window is small and why it is measured rather than assumed good.
