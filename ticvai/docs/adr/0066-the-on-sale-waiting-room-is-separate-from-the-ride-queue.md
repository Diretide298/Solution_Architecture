# ADR-0066: The on-sale waiting room sits at the edge, apart from the ride queue

**Status:** Accepted · 1 October 2026 · Chinmay Parab — a vendor stays the fallback, and only a vendor would need the client
**Date:** 2026-10-01 (drafted 30 September from the system-design review) · **Deciders:** Chinmay Parab (the client only if a vendor is bought)
**Finding:** SD-039 (high)
**Amends:** ADR-0012 (queue integration, amended by this ADR) — Q2 gets its own endpoints and screens, not Q1's
**Related:** ADR-0035, amended 3 September (burst environments) · ADR-0064 (per-tenant limits) · ADR-0065 (availability cache, proposed) · ADR-0055 (`commerce`)

---

## Context

**ADR-0012 separated the two queues, and the contracts bound them together again.**

- ADR-0012 (now amended by this ADR), section "Q2 Virtual Waiting Room — in-house infrastructure, Wave 1": Q2 is owned by infrastructure, not product. It *"keeps the platform standing at peak concurrency during an on-sale"*.
- `queue.yaml:77–78`: *"This contract is Q1 — ride queues. Q2 throttles traffic at on-sale, is infrastructure."*
- But `joinQueue` (`queue.yaml:399`) and `getWaitingGuest` (`queue.yaml:469`) are consumed by WEB-015, WEB-040, GST-023 and GST-046, which include "Branded Queue / Waiting Room". These operations are in the Block A slice.
- `joinQueue` runs in the VenueOps module (the `operations` deployable, ADR-0055) and **writes `queue.entry` in Postgres** (`010-queue.sql:6`) for every arriving guest.
- No admission token is checked by `addCartLine` or `acquireInventoryHold`. A guest who skips the waiting page goes straight to the sale.

**At an on-sale, the waiting room would be a database write per arrival**, which is the load it
exists to keep away. ADR-0035 (amended 3 September) sizes for 30,000 buyers at once, after the
Bahrain failure the client described on 31 July.

---

## Decision

**An in-house waiting room at the edge, with a signed admission token enforced at the cart. It is
separate from the ride queue (Q1).**

- **Arrival** gets a position from a Redis counter (Azure Managed Redis, ADR-0032's product amendment). No database write.
- **The waiting page** is static and branded, served from Front Door's cache. It polls a cached position endpoint. Front Door is global and stores nothing: the page holds no personal data, and the WAF logs stay in the UAE North workspace.
- **A release controller** admits a number of guests per second, set from the health of `commerce` (latency and 429 rate, ADR-0064).
- **An admitted guest** receives a short-lived signed token: tenant, performance, expiry, a unique id. The signing key is a Key Vault secret.
- **`addCartLine` and `acquireInventoryHold` require a valid token** for performances with the waiting room on. The check is a signature check in middleware, with no database read.
- **Activation** follows the performance's on-sale window (`onSaleFrom`/`onSaleTo`, which ADR-0035 already uses), or an operator switches it on.
- **Screens:** the waiting-room parts of WEB-015 and GST-046 bind to new waiting-room endpoints (for example `enterWaitingRoom`, `getWaitingRoomPosition`). `joinQueue` stays Q1, ride queues only.
- **Fallback:** if a large on-sale is booked before the in-house room is proven, use a vendor (such as Queue-it). The token check at the cart works the same way with a vendor's token. Buying one is the client's decision.

---

## Options Considered

### Option A: Keep using `joinQueue` for the waiting room (status quo)

| Dimension | Assessment |
|---|---|
| Complexity | None now |
| Cost | A Postgres write per arriving guest |
| Scalability | Fails at the moment it is needed |
| Team familiarity | High |
| Time to Block A | n/a |

**Pros:** Already contracted. **Cons:** The waiting room becomes the outage. No enforcement at the cart.

### Option B: In-house edge room: Redis, Front Door, signed token (decided)

| Dimension | Assessment |
|---|---|
| Complexity | Medium. A small service, a controller, a middleware check |
| Cost | Redis and Front Door already exist |
| Scalability | Arrivals cost a Redis increment and a cached page |
| Team familiarity | Medium to high |
| Time to Block A | About 8 points; built in B1 unless an on-sale lands in Block A |

**Pros:** Matches ADR-0012 (in-house). No per-sale fee. **Cons:** Ours to prove under load before the first big sale.

### Option C: A waiting-room vendor (such as Queue-it)

| Dimension | Assessment |
|---|---|
| Complexity | Low to integrate |
| Cost | Licence or per-event fee |
| Scalability | Proven at very large on-sales |
| Team familiarity | Medium |
| Time to Block A | Fast to integrate; contract time |

**Pros:** Proven. **Cons:** A vendor for a Wave 1 in-house commitment; visitor data at a third party (residency review).

### Option D: Cloudflare Waiting Room

| Dimension | Assessment |
|---|---|
| Complexity | Medium: a second edge in front of Azure |
| Cost | Cloudflare plan |
| Scalability | High |
| Team familiarity | Low |
| Time to Block A | Slower |

**Pros:** Managed and built in. **Cons:** A second edge network; residency review for traffic handled outside Azure.

---

## Trade-off Analysis

The essential part is the same in B, C and D: nobody reaches the cart without a token, and waiting
costs no database write. B keeps ADR-0012's in-house decision and adds no vendor. C is the safe
fallback for a very large sale before B is proven.

---

## Consequences

**Easier:** the sale path only sees admitted buyers; ADR-0064's limits rarely trigger during a sale.
**Harder:** a token check on two operations; a release controller to tune.
**Revisit:** on-sales above 5,000 rps, or more than one a week (review section 6): consider the vendor.

---

## Action Items

**Before tickets are cut (Block A)**

1. [x] Chinmay: accepted 1 October 2026. ADR-0012 marked amended.
2. [ ] Package: re-point the waiting-room parts of WEB-015 and GST-046 away from `joinQueue` to new waiting-room operations, or defer those parts of the screens; admission-token requirement on `addCartLine` and `acquireInventoryHold`. New operations need a vocabulary permission. Re-derive, mirrors, check. (5 pts, the finding's estimate) — **Contracts authored 1 October**: catalogue `enterWaitingRoom`, `getWaitingRoomPosition` (public), `getWaitingRoomStatus` (`PRODUCT_VIEW`) and `setWaitingRoomSetting` (`PERFORMANCE_CONFIGURE`), the table `catalogue.waiting_room_setting`, the shared `X-Admission-Token` parameter and `403 admission-required` on `addCartLine` and `acquireInventoryHold`; `joinQueue` says Q1 only. **Still open:** re-pointing the waiting-room parts of WEB-015 (P01) and GST-046 (P02), which belong to the guest import.

**B1 (or Block A, if an on-sale is booked in Block A)**

3. [ ] **EDGE-WAITING-ROOM**: Redis positions, cached page, release controller, token issue and check. (8 pts)
4. [ ] Load test at 30,000 arrivals in the burst environment before the first large sale.
