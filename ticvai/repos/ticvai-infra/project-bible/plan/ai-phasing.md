# TICVAI — AI Delivery Phasing

## Position Paper

**Version:** 1.0
**Date:** 12 August 2026
**Prepared by:** Softlabs Group
**For:** TICVAI — Qossai, Allam Allam
**Reference:** `TICVAI_AI_Application_Register.md` (AI-01 → AI-67); requirement matrix `Ticvai_matrix_20260621_2.xlsx`

---

## 1. Executive Summary

The requirement matrix contains **399 AI-related requirements — 12.5% of total scope —
mapped to 67 distinct AI applications across 19 of 21 domains.**

Delivering all 67 at launch is not achievable, and more importantly it would not be
useful. The majority depend on trained models, and a trained model requires historical
operating data that does not exist before the platform is live. Attempting to ship
forecasting, dynamic pricing, recommendation or fraud detection at go-live produces
models trained on nothing, which generate confident and incorrect outputs against real
money and real guests.

We therefore propose scoping **Phase 1 to the AI capabilities that function correctly
from day one with no historical dataset**: conversational assistants, natural-language
reporting, and the mandatory AI governance layer.

**Phase 1: 15 of 67 applications.** All remaining 52 are deferred to Phase 2 and Phase 3,
sequenced against data maturity rather than against development capacity.

This is not a reduction in scope. It is a reordering that puts each capability where it
can actually work.

---

## 2. Objectives

1. Deliver visible, high-value AI at launch without depending on data that will not exist.
2. Establish the AI governance layer before any AI output reaches a guest or a ledger.
3. Begin accumulating the operational data that later phases require, from day one.
4. Give TICVAI a defensible sequence to present to tenants, tied to data availability
   rather than to arbitrary release milestones.

---

## 3. The Governing Principle

The discriminator is **cold-start viability**, not the type of AI.

| | Works at launch | Requires history |
|---|---|---|
| **Grounding** | Configuration data that exists at go-live — products, prices, schedules, venue information, policies, entitlement rules | Transaction history, guest behaviour, attendance patterns, labelled outcomes |
| **Method** | Retrieval-augmented generation over current state | Statistical models trained on accumulated observations |
| **Failure mode if forced early** | None | Confidently wrong outputs against live pricing, refunds and guest journeys |
| **Examples** | Conversational assistants, NL reporting, translation | Forecasting, dynamic pricing, recommendations, fraud detection, churn |

A conversational assistant answering *"what time does Venue Alpha-1 open on Friday and
what does a family ticket cost"* needs the configuration database, which is populated
before launch. A demand forecast for next August needs last August, which does not exist
until the platform has run for a year.

---

## 4. Phase 1 Scope — 15 Applications

### 4.1 Conversational AI — 8

Grounded on configuration and current-state data through retrieval. No training required.

| ID | Application | Module | Refs |
|---|---|---|---|
| AI-01 | Platform Conversational Assistant | Unified Ops / AI Engine | 8.4.1–8.4.9 |
| AI-02 | Guest AI Concierge | Guest Mobile App | 19.2.72 |
| AI-03 | Omnichannel AI Chatbot | Marketing & CRM | 22.8.4, 22.8.5, 19.2.68 |
| AI-04 | Kiosk AI Assistant | Ticketing Sales | 2.1.28 |
| AI-05 | POS AI Assistant | POS | 03 Aug 2026 §65 |
| AI-06 | Employee Assistant & Voice Interface | Employee Mobile App | 18.10.1–18.10.5 |
| AI-07 | Call Centre Agent Assist | Ticketing Sales | 2.8.3 |
| AI-08 | AI Financial Assistant | Finance | 12 Aug 2026 §22 |

**AI-01 is the substrate for the other seven.** They are role- and channel-scoped
configurations of one assistant framework, not seven separate products. This is what
makes eight applications deliverable in a single phase.

### 4.2 Reporting — 1

| ID | Application | Module | Refs |
|---|---|---|---|
| AI-57 | Natural Language Reporting & AI-Generated Dashboards | Unified Ops / BI | 8.7.10, 8.7.30, 8.7.31 |

Queries data that already exists and renders it. A tenant with one day of trading can ask
*"show me yesterday's revenue by venue and payment method"* and receive a correct answer.

**AI-58 Forecasting Analytics is explicitly excluded** from Phase 1. It sits in the same
BI sub-domain but is a different capability class — it projects forward from history
rather than reporting on what happened, and inherits the data prerequisites in §5.

### 4.3 AI Governance — 6 (mandatory)

Not features. Preconditions. No AI output may reach a guest, an operator or a ledger
before these exist.

| ID | Application | Refs |
|---|---|---|
| AI-61 | Prompt, Response & Action Logging | 8.1.2, 8.1.3, 8.3.55–8.3.57 |
| AI-62 | Approval Before Execution | 8.1.4, 8.3.61–8.3.63, 11.1.37 |
| AI-63 | Explainability & Confidence Indicators | 8.1.5 |
| AI-64 | AI Audit Trail | 8.1.6, 8.3.58–8.3.60 |
| AI-65 | AI Usage Analytics | 8.1.7 |
| AI-66 | AI Consent Controls | 22.13.9, 22.13.19 |

Retrofitting an audit trail across sixty applications is not a thing that can be done
twice. AI-65 also produces the per-tenant token accounting needed to settle the AI
billing model, which remains an open commercial question.

---

## 5. Why the Remaining 52 Are Deferred

Each class below has a concrete data prerequisite. These are not development-effort
estimates — the models can be built quickly. They are the point at which the model
produces a defensible answer.

| Class | Applications | Data prerequisite | Earliest viable |
|---|---|---|---|
| **Demand & attendance forecasting** | AI-19, AI-20, AI-25, AI-58 | Two complete annual cycles to separate seasonality from trend. Gulf operations carry strong Eid, National Day, school-holiday and weather effects that a single year cannot distinguish from noise | Phase 3 |
| **Dynamic pricing** | AI-28, AI-29, AI-30, AI-31 | Demand forecasting must exist first, plus observed price-elasticity data. **Also blocked on a commercial decision — see §7** | Phase 3 |
| **Recommendation & personalisation** | AI-35 to AI-43 | Guest-item interaction history. Classic cold-start: recommendations from an empty matrix are effectively random and erode trust in the feature permanently | Phase 2 (late) |
| **Fraud detection** | AI-44 to AI-49 | Labelled fraud cases. Fraud base rates are low, so a usable model needs high transaction volume before enough positive examples accumulate | Phase 2 (late) |
| **Churn & guest insight** | AI-26, AI-52, AI-53 | At least one full membership cycle, since churn cannot be observed before members have had the opportunity to lapse | Phase 3 |
| **Inventory & production forecasting** | AI-21, AI-22, AI-23, AI-43 | Consumption history per outlet, per season | Phase 3 |
| **Resource & staffing optimisation** | AI-24, AI-32, AI-42 | Rostering and utilisation history | Phase 3 |
| **Content & site generation** | AI-12 to AI-15, AI-17, AI-18 | No data dependency, but each requires a substantial host module first — CMS, campaign engine, newsletter platform, SEO layer. **Module-blocked rather than data-blocked** | Phase 2–3 |
| **Computer vision** | AI-11, AI-54, AI-55 | Requires the seat-map and venue-mapping module, plus a separate CV model strategy not yet defined | Phase 3 |
| **Analysis of guest feedback** | AI-50, AI-51 | Requires the review and survey modules, then accumulated response volume | Phase 3 |
| **Platform optimisation** | AI-27, AI-59, AI-60 | Tenant usage history | Phase 3 |
| **API exposure** | AI-67 | Exposes the above; nothing to expose until they exist | Phase 3 |

### 5.1 Dependency chain

Several deferred applications cannot be pulled forward even with unlimited effort,
because they consume the output of other deferred applications:

```
AI-19 Demand Forecasting ──> AI-28 Dynamic Pricing ──> AI-30 Pricing Recommendations
AI-35 Recommendation Engine ──> AI-34 Offer Optimisation ──> AI-38 Next Best Action
AI-52 Audience Classification ──> AI-33 Send-Time Optimisation
AI-44 Fraud Detection ──> AI-48 Approval Risk Scoring
```

---

## 6. Candidates for Phase 1 — For TICVAI's Decision

Four applications meet the same cold-start test as the Phase 1 set but fall outside
"conversational AI and reporting". We raise them for consideration rather than adding
them unilaterally.

| ID | Application | Why it qualifies | Recommendation |
|---|---|---|---|
| AI-16 | **AI Translation** | Zero-shot. Needs no tenant history. Directly supports the multi-language requirement and the Arabic/English obligation across receipts and guest-facing content. Human review before publish is already the specified workflow | **Include** |
| AI-09 | Catalogue Generation from Documents | Zero-shot document extraction. Materially accelerates tenant onboarding — a new venue uploads its existing price list rather than keying several hundred products | Consider |
| AI-10 | Event Configuration Generation | Same mechanism as AI-09, applied to event briefs and schedules | Consider |
| AI-56 | Digital Asset Semantic Search & Tagging | Zero-shot. Small module (15 requirements) and improves usability of brand assets from launch | Consider |

AI-09 and AI-10 are worth particular attention: onboarding effort is a recurring cost per
tenant, and these reduce it at exactly the point when TICVAI is signing new tenants.

---

## 7. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| **Tenant expectation of full AI at launch** | Commercial | Present the phasing as data-driven and publish the maturity schedule alongside the subscription tiers |
| **Data capture not designed for later phases** | Deferred models arrive and find the data was never retained in a usable shape | **Design the event and telemetry schema in Phase 1**, capturing what Phase 2 and 3 models will need. This is the single most important consequence of this phasing |
| **AI-28 Dynamic Pricing has no guardrails specified** | Commercial and reputational | 46 requirements describe the pricing mechanism; none define price floors, ceilings or maximum movement per period. **Requires a TICVAI decision before design, independent of phasing** |
| Vector store residency unresolved | Architectural | Abstraction implemented with both Qdrant and pgvector; the decision is a configuration change |
| Assistant hallucination in a commercial path | Financial | AI-62 makes anything touching price, refund, entitlement or financial state recommendation-only pending human approval |
| Token cost unbounded | Commercial | AI-65 provides per-tenant accounting; caching and model tiering applied from Phase 1 |

---

## 8. Acceptance Criteria — Phase 1

1. AI-61 to AI-66 operational before any assistant is enabled for a tenant.
2. Every AI response carries a trace identifier, model version, token count and
   retrieval sources.
3. No AI application writes to the transactional database. Read-only, scoped by the
   caller's resolved permission set.
4. Tenant isolation in the vector store is partition-level, not filter-level, and is
   penetration-tested before any tenant is enabled.
5. All AI data — vector stores, prompt logs, retrieval indices — resides in the tenant's
   jurisdiction.
6. Each Phase 1 application ships with an evaluation baseline, regression-gated in the
   build pipeline.
7. Anything affecting price, refund, entitlement or financial state is
   recommendation-only until a human approves.

---

## 9. Out of Scope for Phase 1

The 52 applications listed in §5, and specifically:

- Demand, attendance, queue, inventory, seat and revenue forecasting
- Dynamic pricing and discount optimisation
- Product, seat, bundle and loyalty recommendation engines
- Payment, wallet and access fraud detection
- Churn prediction and audience discovery
- AI website builder, mobile content builder, campaign and newsletter content generation
- SEO optimisation
- Computer vision for seat map recognition and venue design
- Review and survey sentiment analysis
- Subscription optimisation and AI setup wizard
- AI services API exposure

---

## 10. Phase Summary

| Phase | Trigger | Applications | Focus |
|---|---|---|---|
| **1 — Launch** | Go-live | **15** | Conversational AI, natural-language reporting, governance layer |
| **2 — Post-launch** | 6–12 months of operating data; host modules delivered | **~20** | Recommendations, fraud detection, content generation, translation extensions |
| **3 — Mature** | 18–24 months; two seasonal cycles | **~32** | Forecasting, dynamic pricing, computer vision, optimisation, API exposure |

---

## 11. Next Steps

1. TICVAI to confirm the Phase 1 scope of 15 applications.
2. TICVAI to decide on the four §6 candidates, in particular AI-16 Translation.
3. TICVAI to define dynamic pricing guardrails — floors, ceilings, maximum movement per
   period — ahead of any Phase 3 design work.
4. Softlabs to design the Phase 1 event and telemetry schema against Phase 2 and 3 model
   requirements, so the data those phases need is captured from launch.
5. Both teams to resolve the AI token billing model in the scheduled workshop.
