# ADR-0053: Owners keep their deterministic rules; AI owns cross-entity risk, alerts and cases

**Status:** Accepted · 1 October 2026 · Chinmay Parab — records AI-D06, decided 29 September
**Date:** 2026-10-01 (drafted 30 September from the system-design review) · **Deciders:** Chinmay Parab
**Finding:** SD-060 (high)
**Source:** `docs/architecture/ai-system-design.md` sections 2.2 B, 3.10 and 5.3; decision AI-D06 (29 September); six-month plan decision 2
**Related:** ADR-0050 (autonomy) · ADR-0051 (baseline and learning) · ADR-0055 (five deployables) · ADR-0059 (AI phasing)

---

## Context

**Risk rules exist in several owners already.** Orders, payments, wallet and access each have
deterministic checks (limits, velocity, expired-ticket reuse). The client's books ask for one fraud
and risk capability with alerts, cases and a relationship graph.

- Scoring per customer (M21 section 4.12), per transaction (FRAUD Board 1) or per entity (FRAUD p.59).
- AI-D06: fail open with holds, not declines.
- Anomaly detection and risk overlap (req-predict conflict 7): the refund rate at a venue versus this cashier's refunds.
- Plan decision 2: Block A fraud comes from Orders' own rules. ADR-0059 puts the fraud runtime in Block B.

---

## Decision

- **Owners keep their deterministic rules.** Orders, payments, wallet and access still refuse what their own rules refuse. No owner waits on AI to enforce a limit.
- **AI owns cross-entity risk.** Entity risk (customer, account, device, token, credential, cluster) is computed asynchronously. Transaction risk is computed synchronously within **80 ms** and reads entity risk as a feature. It runs in `ai-realtime`, inside the `ticvai-ai` deployable (ADR-0055).
- **Fail open with holds** (AI-D06). A timeout or outage lets the payment through; a high score places a hold for review, never a decline.
- **AI owns alerts and cases.** One correlation key, so one situation produces one alert.
- **Anomaly owns aggregate deviations; risk owns actor-level patterns.** Staff leakage (one cashier's refunds, one till's voids) is risk.
- **Autonomy ceiling L1** for restrictive actions (ADR-0050).

---

## Options Considered

### Option A: Risk stays inside each owner

| Dimension | Assessment |
|---|---|
| Complexity | Low now, high later |
| Cost | Duplicate velocity and graph logic |
| Scalability | No cross-module view |
| Team familiarity | High |
| Time to Block A | Fast (it is Block A's position) |

**Pros:** No dependency on AI.
**Cons:** No entity view, no cases, no shared alerts.

### Option B: Owners keep rules; AI owns cross-entity risk, alerts and cases (decided)

| Dimension | Assessment |
|---|---|
| Complexity | Medium |
| Cost | 6 dev-weeks in Block B (design section 7), plus owner events |
| Scalability | Entity risk precomputed; transaction scoring bounded at 80 ms |
| Team familiarity | Medium |
| Time to Block A | No Block A cost |

**Pros:** Deterministic limits stay reliable; AI adds what no single owner sees.
**Cons:** Needs five new owner events (design 3.2).

### Option C: All risk, owner rules included, in AI

| Dimension | Assessment |
|---|---|
| Complexity | High |
| Cost | Moves working rules |
| Scalability | Same as B |
| Team familiarity | Low |
| Time to Block A | Slow |

**Pros:** One place for all risk.
**Cons:** Money paths would depend on the Engagement tier, which ADR-0028's tier rule forbids (unchanged by its amendment in ADR-0055).

---

## Trade-off Analysis

B keeps every hard limit where it is enforced today and adds the cross-entity layer where AI's data
lives. C would put money paths behind AI. A leaves the client's fraud books unanswered.

---

## Consequences

**Easier:** one alert per situation; analysts work cases in one place.
**Harder:** owners must emit the events AI needs.
**Revisit:** above about 5,000 confirmed fraud labels in a tenant, graph or sequence models (design section 6).

---

## Action Items

**Before tickets are cut**

1. [x] Chinmay: accepted 1 October 2026 (AI-D06 already taken on 29 September). Block A keeps Orders' rules.

**Block B (S4, S6)**

2. [ ] Scoring call from Orders, entity risk, graph edges, alerts, cases, `proposeRiskAction`; the five owner events.
