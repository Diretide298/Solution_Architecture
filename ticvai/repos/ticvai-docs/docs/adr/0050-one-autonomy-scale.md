# ADR-0050: One autonomy scale; the approval tier is not an autonomy level

**Status:** Accepted · 30 September 2026 · Chinmay Parab — records AI-D04, decided 29 September
**Date:** 2026-09-30 · **Deciders:** Chinmay Parab
**Finding:** SD-060 (high)
**Source:** `docs/architecture/ai-system-design.md` sections 3.8 and 5.5; decision AI-D04 (29 September)
**Related:** ADR-0020 (AI boundary, amended by ADR-0049) · ADR-0051 (baseline and learning)

---

## Context

**The client's books use three autonomy scales.** GOV has levels 0–4. CFG has 0–3. CORE has
unnumbered modes and says they "should align" to governance.

**The package confuses autonomy with approval.** `ProposedAction.approvalLevel` (1 or 2) is read as
an autonomy level in places. It is the approval tier: how many people must approve.

**Some capabilities need a hard ceiling.** Fraud restrictive actions, access-security changes and
finance actions must never run on their own (AIC-161: the more restrictive policy wins).

**Decided 29 September (AI-D04):** GOV's 0–4 scale; access-security capped at advisory.

---

## Decision

**Every AI capability sits on GOV's scale, with a first-release ceiling.**

| Level | Name | Meaning | First-release ceiling applies to |
|---|---|---|---|
| L0 | Disabled | Not available | Any capability a tenant switches off |
| L1 | Advisory | Explains and recommends | Fraud restrictive actions; access-security changes; finance actions |
| L2 | Prepare | Drafts a proposal a person applies | Operational requirements; pricing inputs; campaigns; Help me choose |
| L3 | Execute with approval | Runs after approval, through owning APIs | Configuration assistant; forecast publication where not automatic |
| L4 | Controlled auto | Runs without approval, only for listed reversible actions inside set ranges | Forecast auto-publish; ranking inside a published strategy; the fraud hold mapping if the tenant turns it on |

- **Lower scopes may tighten a ceiling, never raise it** (AIC-151).
- **Autonomy is separate from permission** (AIC-154). A manager who may change a price by hand still gets an AI-prepared change routed for approval.
- **`approvalLevel` is the approval tier**, a floor that the approvals matrix can raise. The documentation says so.
- **L4 governed optimisation stays off** in the first release beyond the listed actions, until six months of clean L3 evidence.

---

## Options Considered

### Option A: GOV 0–4 (recommended)

| Dimension | Assessment |
|---|---|
| Complexity | Low. One scale in the decision point |
| Cost | None extra |
| Scalability | Covers every capability, including L4 later |
| Team familiarity | Medium. New vocabulary, one table |
| Time to Block A | Fits the governance decision point work (Block A) |

**Pros:** GOV is the governance authority; CORE defers to it. Has room for L4.
**Cons:** CFG's screens use 0–3 and need relabelling.

### Option B: CFG 0–3

| Dimension | Assessment |
|---|---|
| Complexity | Low |
| Cost | None |
| Scalability | No level for controlled automation |
| Team familiarity | Medium |
| Time to Block A | Same |

**Pros:** Matches the configuration assistant book.
**Cons:** No room for L4. Conflicts with GOV.

### Option C: A mode per capability (CORE)

| Dimension | Assessment |
|---|---|
| Complexity | High. Each capability defines its own modes |
| Cost | More tests |
| Scalability | Poor. No common ceiling to enforce |
| Team familiarity | Low |
| Time to Block A | Slower |

**Pros:** Fits each capability exactly.
**Cons:** The decision point cannot compare or cap modes across capabilities.

---

## Trade-off Analysis

One scale is what lets one decision point enforce one ceiling. GOV's has the most room and the most
authority. The cost is relabelling CFG's screens.

---

## Consequences

**Easier:** one ceiling rule, testable in the decision point.
**Harder:** CFG screens and `ProposedAction` documentation change.
**Revisit:** L4 after six months of L3 evidence with low override rates.

---

## Action Items

**Before tickets are cut (ticket text only)**

1. [x] Accepted 30 September 2026: the decision is AI-D04 (29 September); this ADR records it.
2. [ ] Package: correct the `approvalLevel` description in `ai.yaml`; autonomy enum `L0..L4` on the capability registry. Re-derive, mirrors, check. (1 pt)

**Sprint 1**

3. [ ] Governance decision point with the ceiling table (part of the Block A decision-point work, ADR-0059).
