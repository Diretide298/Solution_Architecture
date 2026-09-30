# ADR-0054: Natural-language analytics goes through the semantic layer

**Status:** Accepted · 1 October 2026 · Chinmay Parab — records AI-D13 and AI-D15, decided 29 September
**Date:** 2026-10-01 (drafted 30 September from the system-design review) · **Deciders:** Chinmay Parab
**Finding:** SD-060 (high)
**Source:** `docs/architecture/ai-system-design.md` sections 2.2 E, 5.7 and 5.10; decisions AI-D13 and AI-D15 (29 September)
**Related:** ADR-0016 (read routing) · ADR-0059 (AI phasing) · ADR-0049 (vectors)

---

## Context

**`askReportingQuestion` is free text-to-SQL on the analytical replica today** (design 5.7, option a).

- BI's AIP-170 (must): answer from the semantic layer and match the official dashboards.
- Free SQL cannot guarantee that "revenue" means the dashboard's revenue, and it has to put venue scope inside generated text.
- AI-D13: a number in an answer comes only from a query result, never from a document chunk.
- AI-D15: the model never works on the data directly; figures are computed first and bound into text, or the model writes a query the platform runs.

**It is in the Block A slice** (ReportingService) and bound to 14 screens, including POS-008, BO-029,
KIT-010, ANL-019 and SUP-008. `explainMetricChange` is in the slice too (ADM-506, ANL-019, ANL-056).
Plan decision 10 (30 September) brings the analytics assistant back inside the six months, and
ADR-0059 schedules it in S7 (8–26 February). So the operation is in Block A while the assistant
behind it is in Block B.

---

## Decision

- **The model produces a semantic query spec** over the governed KPI layer (metric, dimensions, filters, period). **Reporting compiles and runs it deterministically**, with RLS and the official metric definitions.
- The answer shows the query it ran.
- A question outside the semantic model gets "not available yet" and a knowledge-gap record. No improvised SQL.
- `explainMetricChange` decomposes a change by channel, product and time with plain arithmetic; the model only words the result.
- Mixed questions: knowledge from the vector store (Qdrant, the tenant's own collection, ADR-0049), numbers from the semantic layer (AI-D13).
- **Block A:** the screens bound to `askReportingQuestion` ship their saved-report and KPI views; the free-text box is behind a flag until S7 (ADR-0059).

---

## Options Considered

### Option A: Free text-to-SQL on the analytical replica (today)

| Dimension | Assessment |
|---|---|
| Complexity | Low to build, high to make safe |
| Cost | Low |
| Scalability | Fine |
| Team familiarity | Medium |
| Time to Block A | Fast |

**Pros:** Answers anything.
**Cons:** Numbers can disagree with dashboards; scope lives in generated text.

### Option B: Approved APIs only (CORE p.33)

| Dimension | Assessment |
|---|---|
| Complexity | Low |
| Cost | Low |
| Scalability | Limited to what APIs expose |
| Team familiarity | High |
| Time to Block A | Fast |

**Pros:** Safe.
**Cons:** Most questions have no API.

### Option C: Semantic query spec compiled by Reporting (decided)

| Dimension | Assessment |
|---|---|
| Complexity | Medium. Needs the semantic model defined |
| Cost | 3 dev-weeks (design section 7) plus Reporting compile |
| Scalability | Inherits the replica routing |
| Team familiarity | Medium |
| Time to Block A | Not in Block A under the plan; behind a flag until S7 |

**Pros:** Matches dashboards; RLS applies; checkable query.
**Cons:** Only answers what the semantic model covers.

---

## Trade-off Analysis

C gives up breadth for numbers that match the dashboards. For a finance or operations manager, a
wrong number is worse than "not available yet".

---

## Consequences

**Easier:** one definition of each metric for dashboards and answers.
**Harder:** the semantic model must be written before the assistant is useful.
**Revisit:** AI dashboard and report generation (AIP-186, AIP-187) only after this is proven.

---

## Action Items

**Before tickets are cut**

1. [x] Chinmay: accepted 1 October 2026 (AI-D13 and AI-D15 already taken on 29 September).
2. [x] Package: `askReportingQuestion` description changes from SQL to semantic spec; Block A screen tickets hide the free-text box behind a flag. (1 pt) — **Authored 1 October**: the description says semantic spec, not text-to-SQL, and that Block A ships the bound screens with the free-text box behind a flag until S7; `explainMetricChange` says the decomposition is plain arithmetic. The screen tickets' flag is the planner's. Re-derive, mirrors and check at the next refresh.

**S7 (8–26 February, ADR-0059)**

3. [ ] The semantic spec, Reporting compile, the assistant.
