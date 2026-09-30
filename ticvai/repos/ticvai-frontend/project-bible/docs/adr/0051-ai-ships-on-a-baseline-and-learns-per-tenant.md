# ADR-0051: Every AI function ships on a baseline and learns per tenant; a model goes live only on evidence

**Status:** Accepted · 30 September 2026 · Chinmay Parab
**Date:** 2026-09-30 · **Deciders:** Chinmay Parab
**Finding:** SD-060 (high), with SD-061
**Source:** `docs/architecture/ai-system-design.md` sections 3.5, 3.10, 3.12 and 5.1; decisions AI-D01 and AI-D16 (29 September); `audit/ticvai/steps/AI2/ai-functions-review.md`; six-month plan decision 10 (30 September)
**Related:** ADR-0050 (autonomy) · ADR-0059 (AI phasing) · ADR-0049 (vectors)

---

## Context

**The design already separates the capability from the producer.** Section 5.1 chose *"ship the
capabilities now with rules and statistics as producers, capture labels from day one, and promote a
model per tenant only when a shadow run proves it beats the rule."* AI-D01: our own models, trained
per tenant, no bought scoring service. AI-D16: when a shadow model passes, raise it to the admin;
never switch automatically.

**But the rules themselves need history, so a new tenant gets refusals.**

- `requestSuggestion` returns **422 `InsufficientDataProblem`** below a minimum history: 8 weeks (demand, staffing, anomaly) to 90 days (upsell, segmentation, menu engineering, send time).
- `requestSuggestion` is in the Block A slice, bound to BO-005, GST-031, BO-115, BO-117 and WEB-044. A new tenant would see refusals on Block A screens for weeks.
- The first-week forecast needs "the same weekday over 8 weeks, or a sister venue". A single new venue has neither.
- There is no operation to import a venue's own history, and `AiForecastDefinition` has no cold-start setting.

**The product owner's direction, now plan decision 10 (30 September):** every AI function is built
inside the six months; data-driven AI ships with a working baseline on day one and grows more
accurate as the tenant's data builds up; no customer hears "this arrives when you have data".

**The learning machinery is missing** (SD-061): no common producer interface, no model or version
registry (`ai.release.candidate_ref` is free text), no training-run record, no data-sufficiency
thresholds per tenant.

---

## Decision

**Every data-driven AI function answers from day one, from a baseline, and learns the tenant as it
trades. A trained model goes live for a tenant only when it beats the current answer and an admin
promotes it.** The direction was decided on 30 September (plan decision 10); this ADR records the
mechanism.

### One producer interface, three producers

Behind every forecast, suggestion, risk score and recommendation:

| Producer | Uses | When it leads |
|---|---|---|
| **Prior** | Venue AI profile, a starting-pattern pack for the venue type, the UAE calendar, weather | Day 1 |
| **Statistical** | The tenant's own data, pulled toward the prior until there is enough | From about 4 weeks; leading by about 3 months |
| **Learned** | A model trained on this tenant's data, run in shadow | Only after promotion by an admin |

The statistical producer blends: estimate = (k × prior + n × own average) / (k + n), where n is the
number of own observations and k is the trust in the prior. It is re-estimated nightly and each run
is a recorded version. **This is not online learning** (design 3.5): no model switches itself.

### Maturity on every answer

Each answer carries a stage (Starting, Learning, Established, Trained on your data), what it is based
on, how much is own data, and what the next stage needs. Ranges or bands, never a bare percentage
(design 5.6). "Limited historical data" while the prior carries more than half the weight.

### What makes day one useful

- **Venue AI profile**, captured at onboarding: capacity, hours, typical attendance, peak months, average spend, attach rates, staff productivity.
- **Historical import** of the venue's own exports into AI data only. **Never into the ledger.** Twelve months or more moves a venue straight to "Established".
- **Starting-pattern packs** per venue type (water park, theme park, family entertainment centre, museum, arena, zoo or aquarium), written by TICVAI from published sources and example curves. **No other tenant's data is used** (AI-D01, AIP-149).

### Promotion

- A per-tenant training and backtest job runs the learned producer in shadow for at least 6 weeks.
- Gates are the design's (section 3.5): forecast WAPE at least 10% better at 7 days with bias within ±3%; fraud recall at least equal with precision at least 20% better at the same review rate; recommendations win a controlled experiment.
- Passing raises an `ai.governance_alert` of kind `promotionReady`. **The admin decides** (AI-D16).

### Contract change

`requestSuggestion` returns 422 **only when a required setting is missing**, never for lack of
history. The minimum-history figures become the point where own data takes over.

### New tables

`ai.model_version` (registry, replacing free-text `candidate_ref`), `ai.training_run` (training and
backtest record), `ai.data_sufficiency` (per capability, per tenant).

---

## Options Considered

### Option A: The design's rules-first as written (422 below minimum history)

| Dimension | Assessment |
|---|---|
| Complexity | Medium |
| Cost | In the plan |
| Scalability | Fine |
| Team familiarity | Medium |
| Time to Block A | Fits, but Block A screens refuse for weeks |

**Pros:** Already designed.
**Cons:** "Not enough data" on Block A screens; exactly what the product owner wants gone.

### Option B: Baseline, then learn (recommended)

| Dimension | Assessment |
|---|---|
| Complexity | Medium. One shared layer used by every function |
| Cost | About 2,220 points over the six months (AI2 review): about 445 developer points and about 37 AI-engineer weeks |
| Scalability | Per tenant by construction |
| Team familiarity | Medium. Classical statistics, no deep learning |
| Time to Block A | The Block A part is small: starting answers for the Block A suggestion kinds (about 1.5 AI-weeks) |

**Pros:** Useful on day one. Honest about its basis. Same shape for every function.
**Cons:** A starting pattern can be wrong for an unusual venue. Mitigated by wide ranges, a visible basis, an editable profile, and a person on every money or configuration change.

### Option C: Defer data-driven AI until data exists

| Dimension | Assessment |
|---|---|
| Complexity | Lowest |
| Cost | Lowest |
| Scalability | n/a |
| Team familiarity | n/a |
| Time to Block A | Fastest |

**Pros:** No wrong numbers.
**Cons:** Features the minutes treat as real are missing; customers see "comes later".

### Option D: Trained models from day one (pooled or bought)

| Dimension | Assessment |
|---|---|
| Complexity | High |
| Cost | Licences or pooled-data contracts |
| Scalability | High |
| Team familiarity | Low |
| Time to Block A | Not feasible |

**Pros:** Looks most "AI".
**Cons:** Rejected by AI-D01 and AIP-149. Confident numbers that happen to be wrong.

---

## Trade-off Analysis

A and B share the same promotion discipline. B adds a prior so the answer exists from day one, at a
cost of about 2,220 points spread over Block B. C is cheapest and fails the product owner's test. D
breaks two decisions already taken.

---

## Consequences

**Easier:** no refusal screens; one interface and one maturity component for every AI screen.
**Harder:** starting-pattern packs must be written and kept honest; two AI engineers carry all the engine work (plan decision 11), and ADR-0059 records what gives first if Block B is short.
**Revisit:** promotion gates per capability once real shadow results exist.
**What cannot happen by 2 April 2027:** a trained model live for any tenant, unless it imports 12 months or more of history. The code ships; promotion follows the data.

---

## Action Items

**Before Monday 5 October 2026** (ticket text for Block A)

1. [x] Accepted 30 September 2026 (Chinmay Parab), with plan decision 10.
2. [ ] Package: `requestSuggestion` 422 narrowed to missing settings; maturity block on AI answers; cold-start setting on `AiForecastDefinition`; historical import operations (3); `ai.model_version`, `ai.training_run`, `ai.data_sufficiency`. New operations need a vocabulary permission and paging on lists. Re-derive, mirrors, check. (3 pts)

**Sprint 2 (26 October – 13 November)**

3. [ ] Producer interface, maturity block, starting answers for the Block A suggestion kinds (queue balancing, prep plan, upsell). (about 1.5 AI-weeks, second AI engineer)

**Block B** — per the AI2 sprint plan: packs, venue profile and forecast prior (S3), statistical producers (S4–S5), training and backtest job (S6), promotion rule (S7), learned producers in shadow (S8).
