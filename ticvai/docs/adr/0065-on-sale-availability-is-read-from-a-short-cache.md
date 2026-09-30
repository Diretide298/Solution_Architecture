# ADR-0065: Browse availability is read from a one-second cache; the hold decides

**Status:** Accepted · 1 October 2026 · Chinmay Parab: it reverses the "availability is read live, never cached" rule, and flows F01 and F07 now say so
**Date:** 2026-10-01 (drafted 30 September from the system-design review) · **Deciders:** Chinmay Parab
**Finding:** SD-038 (high)
**Depends on:** SD-023 (the capacity model: guarded decrement at hold and convert)
**Related:** ADR-0016 (read routing) · ADR-0031 and ADR-0037 (contention) · ADR-0032, pooling amended by ADR-0038 (single-flight, jittered TTL; Redis product amended 30 September) · ADR-0035, amended 3 September (burst environments) · ADR-0066 (waiting room)

---

## What is open, and who answers

**One question, for Chinmay:** do we reverse the written rule *"Availability is read live, never
cached"* (`flows/F01-guest-online-purchase.yaml:56`, `F07-guest-buys-at-a-kiosk.yaml:52`) for the
browse read, keeping the hold as the only correctness check? It is not a client question. Everything
else below is consistent with what is decided; this ADR is Proposed only because it overturns a rule
the package states.

---

## Context

**The browse read, not the hold, becomes the primary's load during a sale.**

- `getAvailability` (`catalogue.yaml`) declares `x-ticvai-read-routing: primary`. It reads `channel_capacity`, `inventory_hold` and `performance`.
- `flows/F01-guest-online-purchase.yaml:56`: *"Availability is read live, never cached"*. `F07-guest-buys-at-a-kiosk.yaml:52` says the same.
- `handoff/burst-scope.json`: 6 `getAvailability` calls per buyer.
- `handoff/sizing.json`, sale: 5,000 rps, Catalogue 63.6% = **3,180 rps**, all on the primary. The sale mix sums to 87.2%, so 12.8% of the load is unassigned.
- It is in the Block A slice on 11 screens, including WEB-004, GST-004, POS-003 and KSK-004.

**Correctness does not need a live browse read.** Whether a seat or ticket can be sold is decided at
the hold (`acquireInventoryHold`, `createSeatHold`), with a guarded decrement on the primary (SD-023).
A browse page that says "available" one second too long costs a guest a "just sold out" message. A
wrong hold costs an oversell.

---

## Decision

**Proposed: browse availability comes from a shared cache that is at most about one second old. The
hold stays the only correctness check.**

- **Key:** tenant, performance, channel (and section, for seat maps). **Value:** capacity minus sold minus active holds, computed from the primary.
- **TTL:** one second with ±10% jitter (ADR-0032). **Single-flight:** one request per key recomputes; the rest wait for it.
- **Stored in Azure Managed Redis** (ADR-0032's product amendment), so every replica of `commerce` shares one computation.
- During a sale that is **at most one primary read per key per second.** Fifty hot performances make about 50 reads a second instead of 3,180.
- Responses carry `asOf`. Below a threshold the UI shows "only a few left", not an exact count.
- If Redis is unavailable, fall back to single-flight in-process caching per replica.
- The hold path is unchanged: primary, guarded decrement, clear "sold out" when it fails.
- F01 and F07 change from "never cached" to "cached up to one second and labelled; the hold decides".

---

## Options Considered

### Option A: Primary, uncached (status quo)

| Dimension | Assessment |
|---|---|
| Complexity | None |
| Cost | Primary sized for 3,180 extra reads a second during a sale |
| Scalability | Worst. The browse read competes with the hold on the same primary |
| Team familiarity | n/a |
| Time to Block A | n/a |

**Pros:** Always exact. **Cons:** The primary is the bottleneck at exactly the wrong moment.

### Option B: Read from a replica

| Dimension | Assessment |
|---|---|
| Complexity | Low |
| Cost | Replica capacity |
| Scalability | Better, but every call still hits a database |
| Team familiarity | High |
| Time to Block A | Fast |

**Pros:** Simple. **Cons:** Replica lag under burst is unbounded; it can show seats the primary has sold minutes ago.

### Option C: One-second shared cache with single-flight (recommended)

| Dimension | Assessment |
|---|---|
| Complexity | Low. A cache wrapper with single-flight, already an ADR-0032 pattern |
| Cost | Negligible |
| Scalability | Primary reads scale with the number of hot keys, not buyers |
| Team familiarity | High |
| Time to Block A | About 3 points |

**Pros:** Bounded staleness. No second write path. **Cons:** Up to about one second stale.

### Option D: Redis counters updated on every hold, convert and expiry

| Dimension | Assessment |
|---|---|
| Complexity | Medium. A second write path that must match the database |
| Cost | Reconciliation job |
| Scalability | Best |
| Team familiarity | Medium |
| Time to Block A | Slower |

**Pros:** Accurate to the event. **Cons:** Counters drift if an update is lost; needs reconciliation. The review suggested this; C gives the same staleness bound with less to go wrong.

---

## Trade-off Analysis

A lie on the browse page is recoverable; a lie at the hold is not. C keeps the hold exact and makes
the browse read cheap with one mechanism the platform already uses. D is the upgrade if one second
proves too coarse for a very hot performance.

---

## Consequences

**Easier:** the primary survives the browse phase of a sale; burst sizing drops.
**Harder:** screens must label availability as approximate near sell-out.
**Revisit:** Option D, or sharded counters, if a single performance passes about 2,000 holds a second (review section 6).

---

## Action Items

**Before tickets are cut**

1. [ ] Chinmay's yes (it reverses F01's and F07's "never cached").
2. [ ] Package: F01 and F07 text; `getAvailability` routing note and `asOf` in the response; complete the sale mix in `sizing.json` (87.2% → 100%). Re-derive, mirrors, check. (3 pts, the finding's estimate)

**Sprint 2, before the first on-sale**

3. [ ] **CAT-AVAIL-CACHE**: the cached read with single-flight and jitter. (3 pts)
4. [ ] Include the browse phase in the burst benchmark.
