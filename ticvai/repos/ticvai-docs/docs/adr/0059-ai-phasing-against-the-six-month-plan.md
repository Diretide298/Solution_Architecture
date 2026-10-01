# ADR-0059: AI phasing against the six-month plan

**Status:** Accepted · 30 September 2026 · Chinmay Parab
**Date:** 2026-09-30 · **Deciders:** Chinmay Parab (product owner), with the project manager on capacity
**Finding:** SD-062 (medium)
**Source:** `docs/architecture/ai-system-design.md` section 7; `docs/active/six-month-plan-29-september.md` decisions 2, 3 and **10–11 (30 September)**; `audit/ticvai/steps/AI2/ai-functions-review.md` sections 5–6
**Closes:** the "AI phasing" item under "Still needed" in the ADR index (CF-57, CF-14)
**Related:** ADR-0051 (baseline and learning) · ADR-0054 (analytics, accepted 1 October) · ADR-0049 (vectors)

---

## Context

**The scope question was settled on 30 September.** Plan decision 10: every AI function is built
inside the six months, data-driven AI ships on a baseline and learns per tenant, and the analytics
assistant, configuration assistant and anomaly detection come back (reversing decision 6). Decision
11: the second AI engineer starts on 5 October; **no third AI engineer**; the two AI engineers carry
the engine work, and developers build the AI endpoints and screens like any other module.

**What is still open is fit: what goes in Block A, and what gives if Block B is short.**

| Source | Block A AI | Capacity |
|---|---|---|
| AI design section 7 | 32 dev-weeks, both assistants included | Does not fit 7 weeks |
| AI2 review | About 13 AI-weeks for the Block A list | Written for a second engineer from 2 November |
| Plan decisions 10–11 | Block A as decision 2 and 3 | Two AI engineers from 5 October: **about 14 AI-weeks** in Block A |

**Block B arithmetic (AI2 section 5).** About 50 AI-engineer weeks of engine work against about 35
available to two engineers after holidays. AI2 already counted endpoints and screens as developer
work (about 445 points), so decision 11 does not close the gap on its own. Starting the second
engineer in October adds about 4 weeks, in Block A. **A gap of roughly 10–15 AI-weeks remains in
Block B**, to be measured, not assumed.

**Gaps in the slice** (AI2 section 8): translations and the planner agent have no operations;
`evaluateAiGovernance`, `getAiUsage` and `getAiPolicy` are not in the slice; BO-093 lacks
`proposeVenueLabels`; `team.json` says Kalpita has no AI work in the first release.

---

## Decision

**Decided 30 September 2026: the Block A engine list below; Block B per the AI2 sprint plan, re-cut
for two engineers; and a slip order agreed now for the case where 23 October confirms the gap.**

**Two AI engineers, and only two (plan decision 11).** The second AI engineer starts on Monday
5 October. There is no third AI engineer, so hiring one is not on the slip order.

### Block A engine work (5 October – 20 November): about 13.5 of 14 AI-weeks

| Work | AI-weeks | Who |
|---|---:|---|
| Gateway: routing, masking, budgets, breaker, telemetry (semantic cache later) | 3 | Kalpita |
| Governance decision point with the autonomy ceilings (ADR-0050) | 1.5 | Kalpita |
| Decision records: write path and trace id (search and export later) | 1 | Kalpita |
| Guest concierge with retrieval on Qdrant, a collection per tenant (ADR-0049) | 2.5 | Second AI engineer |
| Evaluation harness and the concierge's golden set | 1 | Second AI engineer |
| Qdrant tenancy: a collection and a scoped token per tenant, the retrieval client's venue filter, erasure, offboarding, snapshots (ADR-0049, added 30 September) | 1 | Second AI engineer |
| Help me choose suggestion | 1 | Kalpita |
| Translations and the planner agent | 1 | Kalpita |
| Producer interface, maturity block, starting answers for the Block A suggestion kinds (ADR-0051) | 1.5 | Second AI engineer |
| **Total** | **13.5** | |

The spare half week pulls Block B's first items forward (starting-pattern packs, venue profile). The
planner agent is the first item to move if the 23 October pace check is behind; the rules-based Plan
tab ships either way. `askReportingQuestion` screens ship with the free-text box behind a flag until
S7 (ADR-0054).

### Block B (23 November – 2 April)

The AI2 sprint plan (section 5) with the third-engineer column redistributed to the two engineers:
baseline-then-learn (ADR-0051), configuration assistant S3–S5, seat-map S6, analytics assistant S7,
fraud and recommendation runtimes, learned producers in shadow by S8–S9.

### Slip order, if 23 October confirms the gap

1. **Learned-model producers** (forecast gradient boosting, fraud classifier, learning-to-rank; about 9 AI-weeks) finish after 2 April. No customer sees a difference before mid-2027, because no tenant can pass a promotion gate before then. **This conflicts with decision 10's "the code ships"**; it is the least harmful slip, and it is Chinmay's call.
2. If decision 10 must hold as written: a customer-visible cut instead, such as seat-map generation (about 161 points) or marketing AI (about 72 points).

A third AI engineer is not an option: decision 11 closed it.

---

## Options Considered

### Option A: AI design section 7 as written

| Dimension | Assessment |
|---|---|
| Complexity | High |
| Cost | 32 AI dev-weeks in Block A |
| Scalability | n/a |
| Team familiarity | Medium |
| Time to Block A | Does not fit: about 14 AI-weeks exist |

**Pros:** Everything early.
**Cons:** Guaranteed overrun; tickets cut ad hoc.

### Option B: Plan decisions 10–11, Block A list above, slip order agreed now (recommended)

| Dimension | Assessment |
|---|---|
| Complexity | Medium |
| Cost | No hire. About 2,220 points over Block B (AI2), of which about 445 are developer points |
| Scalability | n/a |
| Team familiarity | Medium. Engine work with the two AI engineers; endpoints with the module owners |
| Time to Block A | Fits with about half a week spare (after the Qdrant work added by ADR-0049) |

**Pros:** Honours both 30 September decisions. The gap has a pre-agreed answer instead of an ad hoc cut.
**Cons:** The most likely slip bends decision 10's "the code ships".

### Option C: Plan decisions 10–11 with no slip order

| Dimension | Assessment |
|---|---|
| Complexity | Low now |
| Cost | No hire |
| Scalability | n/a |
| Team familiarity | Medium |
| Time to Block A | Fits |

**Pros:** Nothing to decide today.
**Cons:** If the gap is real, the cut is made in February under pressure, probably on something customers see.

### Option D: Reopen the third AI engineer from 7 December (rejected by decision 11)

| Dimension | Assessment |
|---|---|
| Complexity | Medium |
| Cost | One more engineer for four months |
| Scalability | n/a |
| Team familiarity | Onboarding in the busiest block |
| Time to Block A | No effect on Block A |

**Pros:** Closes the gap with no slip (AI2's plan).
**Cons:** Reverses decision 11; hiring risk.

---

## Trade-off Analysis

A does not fit. C postpones a decision that is cheap now and expensive in February. D reverses a
decision taken yesterday. B keeps both 30 September decisions, sizes Block A to real capacity, and
writes down what gives first. Its one tension is with "the code ships": the models that would slip
are the ones no customer can use before mid-2027 anyway.

---

## Consequences

**Easier:** Block A AI tickets are sized to real capacity; engine and endpoint work are split by role.
**Harder:** Block B has no AI slack; the 23 October checkpoint must look at AI pace specifically.
**Revisit:** 23 October (pace) and 18 December (the plan's deferral checkpoint).

---

## Action Items

**Before Monday 5 October 2026**

1. [x] Chinmay's yes on the Block A engine list and on the slip order (30 September 2026).
2. [ ] Package: add translations and planner-agent operations to `ai.yaml`; add `evaluateAiGovernance`, `getAiUsage`, `getAiPolicy` to the slice; add `proposeVenueLabels` for BO-093; update `team.json` (Kalpita and the second engineer have AI work; AI endpoints go to module owners per decision 11). Re-derive, mirrors, check. (2 pts)
3. [ ] Update the AI design's section 7 to this phasing before the design is accepted.

**By 23 October**

4. [ ] Measure AI engine pace separately from the team pace; confirm or dismiss the Block B gap; apply the slip order if needed.
