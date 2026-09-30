# ADR-0052: One recommendation engine; runtime in AI, configuration in Promotions

**Status:** Accepted · 1 October 2026 · Chinmay Parab — records AI-D07, AI-D08 and AI-D09, decided 29 September
**Date:** 2026-10-01 (drafted 30 September from the system-design review) · **Deciders:** Chinmay Parab
**Finding:** SD-060 (high)
**Source:** `docs/architecture/ai-system-design.md` sections 2.2 A, 2.3, 3.10 and 5.4; decisions AI-D07, AI-D08, AI-D09 (29 September); six-month plan decision 2
**Related:** ADR-0051 (baseline and learning) · ADR-0020 (AI boundary, amended by ADR-0049) · ADR-0055 (five deployables) · ADR-0059 (AI phasing)

---

## Context

**Recommendations are scattered across four operations with their own logic:**
`promotions.getRecommendations`, `getUpsellSuggestions`, `fnb.listFnbRecommendations`,
`retail.listRetailRecommendations`.

- AIR-053 (must): one central service with channel adapters.
- The minutes' cross-channel decline rule (AIR-065) cannot be enforced by four engines. AI-D07: only an explicit decline counts; "ignored" is not a decline.
- AI-D08: no recommendations to OTA or reseller channels in the first release. AI-D09: guest-visible reasons from templates.
- Plan decision 2: Block A upsell comes from the Promotions relationship map (rules). ADR-0059 puts the recommendation runtime in Block B.
- Merchandising (strategy, relationships, suppression) is commercial ownership, and its boards are already contracted in Promotions.

**The AI design was decided on 29 September and is committed**, so this ADR no longer waits on a
review of the design.

---

## Decision

**One engine in `ticvai-ai` owns the recommendation runtime. Promotions keeps the configuration.**

- **Runtime in AI** (the `ai-realtime` process group of the `ticvai-ai` deployable, ADR-0055): eligibility, ranking, the decline store, decision records, experiments, features and models.
- **Configuration in Promotions:** strategies, the relationship map, business priority, suppression.
- **Channel adapters:** the four existing operations stay as the channel surfaces and forward to the engine as placements (design 2.3). Checkout never waits on it: a hard time budget (200 ms) and fail-open to the rules answer.
- **Seat selection stays in Seating** (`seating.recommendSeats`, deterministic best-available). Seat *upgrades* are upsell placements in the engine.
- **Block A:** the Promotions module answers from the relationship map behind the same operations. In Block B the producer moves behind the engine without a contract change (ADR-0051's producer interface).

---

## Options Considered

### Option A: Keep four engines

| Dimension | Assessment |
|---|---|
| Complexity | High over time: four sets of rules |
| Cost | Four times the tests |
| Scalability | Poor. No shared decline or experiment |
| Team familiarity | High today |
| Time to Block A | Fast |

**Pros:** No change now.
**Cons:** Breaks AIR-053 and the decline rule.

### Option B: Runtime in AI, configuration in Promotions (decided)

| Dimension | Assessment |
|---|---|
| Complexity | Medium |
| Cost | 6 dev-weeks in Block B (design section 7) |
| Scalability | One engine, one budget, one experiment framework |
| Team familiarity | Medium |
| Time to Block A | No Block A cost: rules in Promotions first |

**Pros:** Meets AIR-053; configuration stays with the commercial owner.
**Cons:** A network hop at checkout (`commerce` to `ticvai-ai`), bounded by the budget.

### Option C: Everything, configuration included, in AI

| Dimension | Assessment |
|---|---|
| Complexity | Medium |
| Cost | Moves contracted boards |
| Scalability | Same as B |
| Team familiarity | Low for merchandisers |
| Time to Block A | Slower |

**Pros:** One owner.
**Cons:** Puts commercial configuration in the Engagement tier, which nothing taking money may depend on (ADR-0028's tier rule, unchanged by its amendment in ADR-0055).

---

## Trade-off Analysis

B is the only option that satisfies AIR-053 without moving commercial configuration into AI. Its
checkout hop is bounded by a budget and fails open.

---

## Consequences

**Easier:** one decline rule, one experiment framework, one decision record.
**Harder:** four operations become adapters; their descriptions change.
**Revisit:** above 5,000 decisions per second in a region, precompute candidate lists (design section 6).

---

## Action Items

**Before tickets are cut**

1. [x] Chinmay: accepted 1 October 2026 (AI-D07 to AI-D09 already taken on 29 September).
2. [x] Package: mark the four operations as channel adapters in their descriptions; Block A tickets implement the rules producer in Promotions. (1 pt) — **Authored 1 October**: `getRecommendations`, `getUpsellSuggestions`, `listFnbRecommendations` and `listRetailRecommendations` say they are channel adapters, and their 29 September deprecation is withdrawn, since they stay as the channel surfaces. The Block A ticket text is the planner's. Re-derive, mirrors and check at the next refresh.

**Block B (S5)**

3. [ ] Engine runtime, decline store, events, attribution, experiment assignment, POS bundle list; `recommendationId` on cart lines.

## Note, 1 October 2026 (Chinmay)

Confirmed: the four recommendation operations stay as channel surfaces; the 29 September `deprecated` / `x-ticvai-superseded-by` flags are removed.
