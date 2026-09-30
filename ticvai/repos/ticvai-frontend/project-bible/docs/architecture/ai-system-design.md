# TICVAI AI subsystem: system design

> **Status:** Draft, 28 September 2026. Decisions taken 29 September (section 8); awaiting final review before commit. **Updated 30 September** for the 29 September pass: baseline then learn (section 3.13), the visit planner in Block A, the minutes of 17, 18 and 21 September, and the staffing decision of 30 September (section 7)
> **Owner:** Chinmay
> **Inputs:** `audit/ticvai/steps/AI/req-core.md` (AIC-001..271), `req-predict.md` (AIP-001..219), `req-personal.md` (AIR-001..211); ADR-0009, 0020, 0021, 0033, 0034, 0038, 0041, 0046; `contracts/satellite/ai.yaml` (31 operations); `ai-platform.md`, `ai-credentials.md`; `registers/ai-applications.md`; `active/ai-scope-for-confirmation.md`, `active/ai-suggestion-rules-proposal.md`.
> **Precedence used throughout:** a decided (Accepted) ADR beats the minutes and the books unless the client overruled it in the minutes; the minutes (M18, M21) beat the books; among the books, the governance books (GOV, CORE) beat the capability books (CFG, BI, R&P, UCS) on governance questions, because CORE says its modes "should align" to governance. Where this document departs from an ADR, section 8 lists the ADR change.

The client's books describe AI screen by screen. This document does not. It designs one AI platform with a small number of engines, and the ninety-odd P09 screens (ADM-469..558), the P16 analytics screens and the recommendation boards bind to the operations named in section 2.3.

**The design in eight sentences.** One Python service, `ticvai-ai`, deployed in three process groups (real-time, interactive, batch), owns every AI table and every model call. Every AI capability passes one governance decision point, one gateway to models, and writes one standard decision record. Large language models never sit on a path that takes money: recommendations and fraud scoring are rules plus classical ML with hard time budgets, and checkout continues without them. Forecasting, anomaly detection, fraud and recommendations ship rules-first and statistical, and each moves to a trained model per tenant only when a shadow run proves it beats the rule. Anything that changes configuration goes plan, validate, simulate, approve (through the shared approvals service), execute through the owning module's API, with rollback. Vectors live in pgvector inside each tenant's own database, not in Qdrant. The default model provider is TICVAI-managed Azure OpenAI in UAE North, re-billed to the tenant per token, with bring-your-own-key as an override. One autonomy scale (GOV's 0 to 4) applies to every capability.

---

## 1. Requirements

### 1.1 Functional, grouped into capabilities

Fourteen capabilities. Every requirement id in the three pull files maps to one of them; section 9 is the full coverage table.

| # | Capability | What it does | Requirement ids |
|---|---|---|---|
| C1 | **AI gateway and model registry** | One entry point for every model call: provider and model catalogue, routing, fallback, prompt registry, masking, budgets | AIC-005..031, AIC-236..239, AIR-050, AIR-097, AIP-194 |
| C2 | **Governance decision point** | Capability registry, risk classes, autonomy, action/data/scope policies, policy lifecycle, exceptions | AIC-143..171, AIP-192, AIP-193, AIP-206 |
| C3 | **Action pipeline and human oversight** | Plans, tools, validation, simulation, approval, execution, rollback, intervention | AIC-086..107, AIC-172..192 |
| C4 | **Knowledge and retrieval** | Source registry, controlled ingestion, permission-filtered hybrid retrieval | AIC-046..068, AIC-261..263 |
| C5 | **Assistants** | Staff assistant profiles, guest concierge, support chatbot on one runtime | AIC-069..080, AIC-084 |
| C6 | **Analytics assistant and insights** | Natural-language questions over the semantic layer, insight layer, executive summaries, root cause | AIC-081..083, AIC-085, AIP-166..198, AIP-218, AIP-219, AIR-081, AIR-178 |
| C7 | **Configuration assistant and tenant self-service** | Discovery, blueprint, build plan, change and rollback of configuration | AIC-108..142, AIR-157..177 |
| C8 | **Forecasting and operational requirements** | One forecasting service: versions, horizons, accuracy, scenarios, operational requirements | AIP-001..079, AIP-199..204, AIP-211..214 |
| C9 | **Anomaly detection** | KPI anomalies, correlation into incidents, prioritisation | AIP-080..095 |
| C10 | **Fraud and risk intelligence** | Transaction and entity risk, relationship graph, alerts, cases | AIP-096..165, AIP-205, AIP-207, AIP-208, AIP-216, AIP-217 |
| C11 | **Recommendation and upsell engine** | One engine for every placement and channel: strategy, eligibility, ranking, delivery, measurement, experiments | AIR-001..156, AIR-203..211 |
| C12 | **Decision records, explainability and audit** | Standard decision record, trace, explanation depths, evidence packages, replay | AIC-193..209, AIP-215..217, AIR-193..202 |
| C13 | **Operations, evaluation, cost** | Telemetry, SLOs, evaluation and release, usage and cost attribution, governance monitoring | AIC-210..260, AIP-195, AIP-196 |
| C14 | **Residency, privacy, consent, tenancy** | In-region processing, masking, purpose limits, erasure, isolation | AIC-032..045, AIC-264..271, AIR-180..192, AIP-197, AIP-198 |

Scope and phasing statements (AIC-001..004) are answered in sections 5.1 and 7.

### 1.2 Non-functional

No source agrees a number for any of these (req-predict "left to us"; AIR-203 gives 300 ms as an example). These are ours, stated so they can be tested.

| Area | Target |
|---|---|
| **Recommendation latency** | Server 95th-percentile 120 ms, 99th-percentile 180 ms; caller hard timeout 200 ms; ML ranking budget 30 ms inside that |
| **Fraud scoring latency** | Server 95th-percentile 50 ms; Orders' timeout 80 ms (CORE's example is 95th-percentile < 300 ms for the whole screen) |
| **Assistant latency** | Time to first token 95th-percentile 1.5 s; total 95th-percentile 8 s staff, 5 s guest (ADR-0034: separate targets) |
| **Analytics answer** | 95th-percentile 6 s including the query on the analytical replica |
| **Configuration assistant turn** | 95th-percentile 10 s, not streamed |
| **Governance decision** | 95th-percentile 5 ms, in-process with cached policy; it sits on every path above |
| **Nightly forecast** | Published for every tenant by 05:00 tenant-local |
| **Availability** | `ticvai-ai` 99.5% (Engagement tier, ADR-0028). Recommendation and fraud: 99.95% "answered or fell back within budget"; the fallback carries the sale path |
| **Accuracy** | No single figure (AIC-251); per-capability release gates in 3.5 |
| **Cost** | Per-tenant spend visible daily; per-request token budget; month-end projection labelled a forecast |
| **Residency** | Every store and default model endpoint in UAE North; cross-border only per tenant behind the ADR-0009 gate |
| **Audit** | Every model call writes `ai.activity`; every governed decision writes one decision record; approved-then-failed kept distinct from succeeded |

### 1.3 Constraints

1. **17 .NET services own their schemas** (ADR-0028). The AI service writes only AI stores; everything else changes through the owning module's API (ADR-0020 addendum, AIC-087).
2. **Python/FastAPI for all AI and ML** (AIC-030), repository `ticvai-ai`.
3. **Azure UAE North** for compute, databases, cache, blob and the default model endpoint. Cloud-agnostic application code (AIC-031): Azure is a deployment target, not an SDK dependency outside adapters.
4. **Each tenant has its own database** inside its cell, shared or dedicated (ADR-0038). Row-level security enforces venue scope through `ticvai.scope_paths`.
5. **Every AI operation is `x-ticvai-offline-capable: false`.** POS, scanner and kitchen are offline-first (ADR-0013); anything they need from AI must arrive in their local bundle.
6. **Permissions:** `AI_USE`, `AI_CONFIGURE`, `AI_APPROVE`, `AI_AUDIT_VIEW`. `PLATFORM_*` permissions come only from the platform token; acting inside a tenant also needs an open platform-staff grant (`openPlatformStaffGrant`).
7. **Card data and payment tokens never reach a model** (AIC-039); fraud uses provider token references and derived signals only (AIP-112).
8. **The masking list fails closed** (ADR-0020 §2, `AiPolicy.maskedFields`).
9. **A residency refusal is never failed over** (ADR-0034, AIC-021).

---

## 2. High-level design

### 2.1 Component diagram

```
  Guest web/app  Kiosk   POS (offline bundle)  Staff app  Back office  Admin console  Analytics
   P01/P02       P05     P04                   P06        P08          P09            P16
      │            │       │                      │          │            │             │
      └────────────┴───────┴──── HTTPS, no provider key on any surface ───┴─────────────┘
                                          │
  ┌──────────────── .NET services (17), each owns its schemas ─────────────────────────────┐
  │ Orders ─(scoreTransactionRisk, 80 ms)─┐    Promotions: strategies, relationships,       │
  │ Reporting: semantic layer, SQL compile│    suppression config                           │
  │ Approvals: matrices, requests         │    Identity: grants, on-behalf-of tokens        │
  │ Catalogue, Access, Payments, Wallet, F&B, Retail, Inventory, Workforce, ...             │
  └───────┬──────────── outbox ──► broker (ADR-0033) ────────────────────────▲──────────────┘
          │ domain events                                                    │ owning-module APIs
          ▼                                                                  │ (plan execution)
  ┌──────────────────────────── ticvai-ai (Python / FastAPI), per cell ──────┴──────────────┐
  │  ai-realtime     Recommendation engine · Risk scorer · Feature updater (stream)         │
  │  ai-interactive  Assistant runtime · Configuration assistant · Analytics assistant ·    │
  │                  Plan executor · Governance/admin API                                   │
  │  ai-batch        Ingestion · Forecasting · Anomaly · Accuracy · Training · Evaluation   │
  │  ─────────────── shared libraries, imported by all three ───────────────────────────── │
  │  Governance decision point (PDP) · AI gateway (router, masking, budgets, caches,        │
  │  breaker, telemetry) · Retrieval client (no scope parameter) · Feature library ·        │
  │  Decision-record writer · Prompt registry client                                        │
  └──────┬─────────────┬──────────────┬──────────────┬─────────────┬───────────────────────┘
         ▼             ▼              ▼              ▼             ▼
   Tenant DB       AI log DB       Redis          Blob storage   Key Vault ──► Model endpoints
   `ai` schema:    per tenant,     features,      model files,   credentialRef   Azure OpenAI UAE North
   config, state,  append-only,    counters,      Parquet        only            (TICVAI-managed or BYOK)
   pgvector, RLS   partitioned     caches         snapshots,                     In-cell CPU: BGE-M3,
   (replica for    by month                       evidence (WORM)                reranker
   vector reads)                                                                 Customer endpoint
```

Three process groups share one codebase and one set of libraries. They are split because their failure and scaling profiles differ (AIC-247): real-time scales on requests per second and never calls an LLM; interactive is I/O-bound on model calls; batch is queue-driven and can starve without hurting either.

### 2.2 Data flow for the main paths

#### A. Guest recommendation at checkout

1. The checkout page requests the recommendation slot **in parallel**; the pay button never waits. The client calls `decideRecommendations` (placement, `cartId`, session, optional `subjectId`) with a 200 ms deadline.
2. `ai-realtime` resolves tenant and scope from the session and loads the placement's published strategy from Redis (kept current from Promotions' strategy events).
3. **Context:** basket, derived party ("likely family", AIR-111), identity, consent flags, customer features. A sufficiency check picks personalised or contextual mode (AIR-114, AIR-187).
4. **Candidates** from the relationship map and nightly affinity lists, then **hard eligibility**: saleable, channel, date, capacity, inventory, owned or in cart, conflicts, cross-channel declines, frequency caps, guardrails. Every removal keeps its reason (AIR-032).
5. **Rank:** business priority and rule scores always; a learning-to-rank model only where the strategy allows it and a model is promoted for this tenant, within 30 ms, else rules.
6. **Ranking policy** (counts, diversity), confidence band, final validation, decision TTL.
7. Return items with tracking ids, template reasons (no LLM) and a Pricing price reference, never a computed price (AIR-029). The decision record is written after the response.
8. Interactions arrive through `recordRecommendationEvents`; `orders.addCartLine` carries `recommendationId`, so `order.completed` attributes purchases without guessing.

**Budget miss or AI down:** the slot stays empty. At POS offline, the bundle's precomputed "offer with" list per product (built nightly, rules only) is shown instead.

#### B. Fraud score on payment

1. `orders.checkoutCart` evaluates `orders.fraud_rule` in-process, as today, then calls `scoreTransactionRisk` (service audience, 80 ms timeout) with amount, channel, product mix, token reference, hashed device id, account and customer ids, attempt number.
2. `ai-realtime` reads entity risk and velocity counters from Redis, applies the tenant's risk strategy (weighted rule contributions), adds the ML score if one is promoted, and returns a composite 0..100 with band and reason codes.
3. The decision point maps band to outcome for this tenant, channel and value (AIP-100): allow, monitor, step-up, or hold for review. **Decline only where the tenant has explicitly governed it.** Orders acts: 3DS step-up through Payments, or its existing hold.
4. **Timeout or AI down:** Orders proceeds on its own rules (fail-open); a fail-closed tenant gets a hold, never a silent decline (AIP-110).
5. Afterwards, payment, refund, login and scan events update entity risk and graph edges, and re-scoring raises alerts (AIP-109). Restrictive actions go to the owning module through the action pipeline, never straight from review (AIP-136).

No LLM is on this path. An LLM writes case summaries later, from structured evidence only (AIP-153).

#### C. Nightly forecast

1. At 02:00 tenant-local, once the analytical replica's watermark covers midnight, extract sales, admissions, bookings on hand, capacity and calendar, plus weather and holiday signals, into a Parquet snapshot with its data cut-off.
2. Run each definition's assigned producer (rule, statistical or model) with 10th-percentile/50th-percentile/90th-percentile intervals. Shadow producers run too and are recorded, not shown.
3. **Reconcile** bottom-up to venue level, top-down where a level is forecast directly (AIP-034). Drivers come from component decomposition or SHAP.
4. Write an immutable `forecast_version`; nothing is overwritten (AIP-032). Score yesterday's actuals against every earlier version (T-30..T-1) and flag bias (AIP-044).
5. **Publish** automatically where the definition's autonomy allows and the quality gates pass (completeness, no blocking signal missing, no accuracy regression); otherwise wait for an `AI_APPROVE` holder. `ai.forecastPublished` notifies consumers.
6. **Operational requirements** (staff, POS, gates, F&B, stock) are derived with the tenant's productivity standards and sent to owning modules as recommendations bound to that version (AIP-067).

#### D. Configuration-assistant proposal through approval to apply

1. **Discovery.** `startConfigurationSession`. The configuration knowledge model (objects, dependencies, required/recommended/optional decisions, conditional questions) picks each question; the LLM only extracts structured answers against a schema (AIC-029, AIC-111). Every value carries provenance: confirmed, AI-recommended, inferred or unknown.
2. **Blueprint.** Decisions, severity-graded issues and a dependency map; never ready while a required decision is deferred (AIC-115). Each recommendation is accepted, modified, rejected or deferred.
3. **Plan.** `buildConfigurationPlan` compiles a DAG of steps, each bound to `targetContract.targetOperation` at a contract version (AIC-095), with payload, provenance, compensation and idempotency key `plan:{id}:step:{n}`.
4. **Validate** against the target request schema, the knowledge model's cross-module rules, and the owner's validate-only mode (2.3). **Simulate** current versus proposed state, channels, future orders, issued tickets.
5. **Govern.** The decision point scores risk and applies the autonomy ceiling; `approvals.evaluateApprovalRequirement` gives the approver chain. The plan becomes one `ProposedAction` with a hashed change set (AIC-181).
6. **Approve.** Tier 1: the requester confirms. Tier 2 or matrix-caught: `approvals.createApprovalRequest`, with separation of duties, thresholds and escalation in the shared service (AIC-190). `approval.granted` resumes the plan.
7. **Execute.** Revalidate first: each step recorded its target object's version, and drift pauses the plan (AIC-182). Steps run in DAG order through owning APIs with an on-behalf-of token for the requester, bounded by the approver's authority. Success is the service's response, not a model's judgement (AIC-097); publishing follows the owner's lifecycle.
8. **Failure:** retry at most 3 times, then compensate or pause. **Rollback** is its own plan with a safety analysis and a forward-fix option (AIC-139).

#### E. Staff natural-language question

1. `sendAiMessage` on a staff profile; the decision point confirms the capability for this role and scope.
2. A small model plus rules classify it: knowledge, live data, mixed, or a change request, which goes to the configuration assistant because the assistant only reads (AIC-078).
3. **Live data.** The LLM sees only the semantic-model metrics and dimensions this user may see, and returns a **semantic query spec** (metric, dimensions, filters, period, comparison), not SQL. Reporting validates and compiles it deterministically and runs it on the analytical replica, where RLS applies (AIP-170). Mixed questions add permission-filtered retrieval.
4. **Answer.** Numbers in the narrative are bound to result placeholders, so a figure can only come from the result. The response carries the compiled SQL, `dataAsOf`, citations and a reliability category; `ai.activity` and `reporting.natural_language_query` are written.
5. A follow-up ("compare that to this week") edits the stored spec, and permissions are re-checked every turn (AIC-073).

### 2.3 Contract surface

**Kept as they are (31):** all current `ai.yaml` operations. Their behaviour widens as described below.

**Changed:**

| Operation | Change |
|---|---|
| `requestSuggestion` | `demandForecast`, `staffing`, `scenario`, `anomaly` and `upsell` route to the forecasting, anomaly and recommendation engines. The kinds and `SuggestionBasis` are unchanged; only the producer changes |
| `setSuggestionProvider` | Also written by `promoteAiRelease`; shadow mode becomes the release pipeline's shadow stage |
| `setAiProvider` | Adds `managedBy` (`ticvai` or `tenant`), which decides who pays (section 5.9), and `modelId` into the model catalogue |
| `setAiPolicy` / `getAiPolicy` | `enabledCapabilities` extends to the fourteen capabilities; `ceilingBehaviour` becomes per capability; adds `autonomyOverrides` (tighten only) |
| `decideProposedAction` | Decides tier 1 in place; tier 2 and matrix-caught actions return the linked `approvalRequestId` and are decided in Approvals |
| `generateConfiguration` | Produces a one-step plan through the same pipeline as flow D |
| `askReportingQuestion` | The model returns a semantic query spec; Reporting compiles it; the compiled SQL is still returned |
| `getAiUsage` | `groupBy` adds `agent`, `model`, `task`; a month-end projection field labelled `forecast` |
| `listAiInteractions` | Each row links its `decisionRecordId` |
| `IndexSource.collection`, `ai.yaml` info | "Qdrant collection" becomes "embedding table"; the isolation rule text follows section 5.8 |
| `promotions.getRecommendations`, `recordRecommendationOutcome`, `explainRecommendation`, `getUpsellSuggestions`; `fnb.listFnbRecommendations`; `retail.listRetailRecommendations` | Deprecated for one release and forwarded to the engine as placements (section 5.4). `promotions.simulateRecommendationStrategy` stays and calls the engine in simulation mode |
| `orders.addCartLine` | Optional `recommendationId` |
| Registered tool operations in owning contracts | Accept `Prefer: validate-only`, which validates and returns what would change without writing. About 40 operations, named by the tool registry |

**New (grouped by tag, package naming; every list is paged; permissions from the existing vocabulary):**

- **governance** (C2): `listAiCapabilities`, `configureAiCapability`, `getEffectiveAiPolicy`, `createAiGovernancePolicyDraft`, `simulateAiGovernancePolicy`, `publishAiGovernancePolicy`, `listAiGovernancePolicyVersions`, `createAiPolicyException`, `revokeAiPolicyException`, `pauseAiCapability`, `resumeAiCapability`, `evaluateAiGovernance` (service audience).
- **actions** (C3): `getActionPlan`, `simulateActionPlan`, `pauseActionPlan`, `resumeActionPlan`, `cancelActionPlan`, `retryActionStep`, `rollbackActionPlan`, `overrideAiDecision`, `listAiTools`, `setAiTool`.
- **configure** (C7): `startConfigurationSession`, `answerConfigurationQuestion`, `getConfigurationBlueprint`, `decideBlueprintRecommendation`, `buildConfigurationPlan`, `listConfigurationSessions`.
- **knowledge** (C4, C5): `listKnowledgeGaps`, `recordAnswerFeedback`, `configureAssistantProfile`, `listAssistantProfiles`.
- **insights** (C6, C9): `listAiInsights`, `decideAiInsight`, `explainMetricChange`, `configureAnomalyDetector`, `listAnomalyDetectors`.
- **forecast** (C8): `listForecastDefinitions`, `setForecastDefinition`, `runForecast`, `listForecastVersions`, `getForecast`, `publishForecastVersion`, `createForecastScenario`, `compareForecastScenarios`, `getForecastAccuracy`, `listForecastSignals`, `configureForecastSignalSource`, `listOperationalRequirements`, `decideOperationalRequirement`.
- **risk** (C10): `scoreTransactionRisk` (service audience), `getEntityRisk`, `configureRiskStrategy`, `backtestRiskStrategy`, `listRiskAlerts`, `decideRiskAlert`, `createRiskCase`, `getRiskCase`, `addRiskCaseEvidence`, `expandRiskNetwork`, `proposeRiskAction`, `closeRiskCase`.
- **recommend** (C11): `decideRecommendations` (guest-callable), `recordRecommendationEvents`, `explainRecommendationDecision`, `getCustomerRecommendationProfile`, `simulateRecommendationDecision` (service audience, for Promotions).
- **models** (C1, C13): `listAiModels`, `setAiModel`, `listPromptTemplates`, `publishPromptTemplate`, `runAiEvaluation`, `listAiEvaluations`, `promoteAiRelease`, `rollbackAiRelease`.
- **audit** (C12): `searchAiDecisions`, `getAiDecisionTrace`, `exportAiEvidencePackage`, `replayAiDecision`.
- **monitoring** (C13): `listAiGovernanceAlerts`, `decideAiGovernanceAlert`, `listAiIncidents`, `openAiIncident`, `containAiIncident`, `closeAiIncident`, `listAiRiskRegister`, `setAiRiskRegisterEntry`, `listAiControls`, `runAiControlTest`.

That is 89 new operations. The P09 blocks bind as follows: configuration assistant ADM-469..498 to **configure** and **actions**; forecasting ADM-499..518 to **forecast**; governance ADM-519..528 to **governance**, ADM-529..538 to **actions** and Approvals, ADM-539..548 to **audit**, and ADM-549..558 to **monitoring**.

**Added 29 September (the 29 September pass, group A).**

| Operation | Why |
|---|---|
| `requestSuggestion` (changed) | **Answers on day one** from the baseline and carries `maturity` on every answer; the 422 is narrowed to a missing setting (`AiMissingSettingProblem`). New guest-allowed kind `itinerary` for the visit planner (MOB-6; supersedes the deferral in R187 and R209) |
| `getAiVenueSettings`, `setAiVenueSettings` | The venue AI profile entered at onboarding (capacity, opening hours, typical attendance, venue type, average spend, productivity), `ai.venue_settings` |
| `importVenueHistory`, `listVenueHistoryImports`, `getVenueHistoryImport` | The venue's own historical exports, into `ai.history_import` and `ai.history_observation`, never the ledger |
| `listAiCapabilityMaturity` | The AI maturity page: each answer's stage, `ai.capability_maturity` |
| `listAiTrainingRuns` | The per-tenant training and backtest run registry, `ai.training_run`; a passed gate raises `promotionReady` (AI-D16) |
| `listAiCapabilityHealth` | Availability, latency, error rate, breaker and freshness per capability (M21-13) |
| `AiForecastDefinition` (changed) | `producer` adds `ensemble`; `historyWindowMonths` (default 36) and `coldStart` (M18-16) |
| `AiProvider.taskKeys`, `fitnessWarnings`; `AiModel.taskFitness` (changed) | A provider bound per agent task (M21-03) and a fitness warning when a model is under- or over-powered for it (M21-09) |
| `AiGovernanceRule.environments`, `searchAiDecisions` (changed) | `sandbox` environment (M18-01); search by `venueId` and by customer as `subjectRef` (M18-03) |
| `AiTool` registrations | The planner agent's five tools, all in `venue-map`: `generateVisitPlan`, `getVisitPlan`, `updateVisitPlan`, `listVisitPlanAlternatives`, `bookVisitPlan`, always called as the guest |

The visit plan itself lives in `venue-map` (`venuemap.visit_plan`, `venuemap.visit_plan_item`), because a plan is laid out on the map and is the guest's own, like a cart. **The planner agent never writes it directly**: it proposes changes through `requestSuggestion` kind `itinerary` or calls the plan operations as the guest, so AI still writes only `ai.*`, pgvector and `cache:*` (ADR-0020).

**The planner agent is grounded in each day's venue** (client meeting 30 September, MoM 4.7, Allam's requirement). In a multi-venue tenant each plan day is at one venue (`VisitPlanRequest.dayVenues`, `VisitPlan.days[].venueId`, `VisitPlanItem.venueId`), and the agent's candidates are only what its plan tools return for that day: the rides, dining and **retail (shops and kiosks, added alongside F&B the same day)** on that venue's published map. It never proposes a point from general knowledge or from another venue, and a wish the day's venue cannot meet is answered from `VisitPlan.unmatchedPreferences` (naming the venue that has it) rather than filled. `updateVisitPlan` refuses a point from another venue (422 `point-not-at-day-venue`) as the deterministic backstop, so grounding does not depend on the prompt alone.

**Three new permissions, no more.** `PLATFORM_AI_MANAGE`, from the platform token, for the platform layer of the model catalogue, tool registry and prompt registry. `RISK_REVIEW` and `RISK_INVESTIGATE` for fraud analysts, who are not "AI users" and must not need `AI_USE` to work a case. Everything else uses the four `AI_*` permissions: read with `AI_USE`, configure with `AI_CONFIGURE`, publish or approve with `AI_APPROVE`, audit with `AI_AUDIT_VIEW`. Platform staff reach tenant AI data only through an open platform-staff grant (AIC-265).

### 2.4 Storage choices

| Data | Store | Why |
|---|---|---|
| Configuration and current state (policy, providers, capabilities, governance versions, plans, blueprints, cases, alerts, forecast headers, entity risk) | **Tenant database, `ai` schema**, primary | Small, hot, needs RLS and transactions (ADR-0020 §3) |
| **Vectors**, dense and sparse | **pgvector in the tenant database**; reads on the replica | The database is the tenant boundary; RLS carries venue scope (5.8) |
| Append-only logs (`ai.activity`, messages, decision records, recommendation decisions and events, risk assessments, forecast points) | **AI log database**: one Postgres database per tenant on a regional AI log server, monthly partitions | ADR-0020 §3 moves history off the primary; a replica cannot be written, so it needs its own server (AIC-248) |
| Features, velocity counters, caches, snapshots | **Azure Managed Redis** (not Azure Cache for Redis, which is retiring; ADR-0032 amendment), keys prefixed `{tenant}:{scope}` | Sub-millisecond reads |
| Offline features, training snapshots, model files | **Blob**, a container per tenant; released models immutable | Reproducible training |
| Case evidence | Postgres `jsonb` plus immutable Blob | AIP-155 |
| Relationship graph | Postgres edge table, bounded 1..3-hop queries | A graph database is a fifth store for no gain at this size |
| Telemetry | OpenTelemetry to the in-region observability stack, **no prompt text** | Content stays in `ai.activity` under retention |
| Secrets | Key Vault; only `credentialRef` in the database | `ai-credentials.md` |

---

## 3. Deep dive

### 3.1 Data model

All new tables are owned by the AI service. Scoped tables get `platform.apply_scope_rls`; child tables get `platform.apply_parent_rls`. **The four existing AI tables with no policy** (`index_failure`, `knowledge_document`, `proposed_action`, `suggestion_outcome`; a fifth, `chunk_ref`, was merged into `ai.chunk_embedding` on 30 September) gain `scope_path` or a mandatory parent, closing an existing gap. **Platform rows** (the platform model catalogue, tool registry, platform prompts) are mastered in the control plane, which holds no personal data (ADR-0043), and replicated read-only into each tenant database by the release.

| Group | Table (tenant DB unless marked **log**) | RLS | Notes |
|---|---|---|---|
| Registry | `ai.capability` | scope | Owner, function, risk class, autonomy ceiling, data categories, lifecycle per environment (AIC-144, AIC-145) |
| | `ai.model` | platform rows + tenant scope | Catalogue: provider, capabilities, context limit, tool calling, structured output, region, cost profile, lifecycle per environment (AIC-013, AIC-026) |
| | `ai.prompt_template` | platform + scope | Versioned, immutable once published (AIC-022) |
| | `ai.tool` | platform | Tool registry: target operation and version, read/write/destructive, risk, permission, compensation, timeout, idempotency (AIC-089) |
| Governance | `ai.governance_policy`, `ai.governance_policy_version` | scope | Draft, simulated, published, superseded; the effective policy is resolved and cached (AIC-165) |
| | `ai.policy_exception` | scope | Expiry, approver, compensating controls (AIC-162) |
| Actions | `ai.action_plan`, `ai.action_step` | scope; step via parent | DAG, checkpoints, object versions, change-set hash, status; independent of any conversation (AIC-102) |
| | `ai.intervention` | scope | Override, pause or stop, with original and human decision (AIC-187) |
| | `ai.proposed_action` (existing) | adds `scope_path` | Gains `planId`, `approvalRequestId`, `changeSetHash` |
| Configuration | `ai.config_session`, `ai.blueprint`, `ai.blueprint_decision` | scope; decision via parent | Provenance on every value |
| Knowledge | `ai.chunk_embedding` | parent (document) | `halfvec(1024)` dense and `sparsevec` from BGE-M3; one table per embedding model |
| | `ai.knowledge_gap`, `ai.answer_feedback` | scope | Unanswered questions become tasks for the content owner (AIC-061, AIC-062) |
| | `ai.assistant_profile` | scope | Role or audience, tools, sources, model task, guest scope |
| Forecast | `ai.forecast_definition`, `ai.forecast_version` | scope | Version header: producer, model version, data cut-off, horizon, status |
| | **log** `ai.forecast_point` | scope | Partitioned by target month |
| | `ai.forecast_accuracy`, `ai.forecast_scenario`, `ai.operational_requirement` | scope | Requirement bound to its forecast version |
| | `ai.signal_source`, **log** `ai.signal_observation` | scope | Weather and calendar, with freshness and coverage |
| Insights | `ai.anomaly_detector`, `ai.insight` | scope | Insight lifecycle new → reviewed → accepted/rejected → actioned → measured (AIP-181) |
| Risk | `ai.risk_strategy` | scope | Thresholds, weights, modes, outcome map |
| | **log** `ai.risk_assessment` | scope | One per evaluation (AIP-147) |
| | `ai.entity_risk`, `ai.risk_edge` | scope | Current score per entity; graph edges with strength |
| | `ai.risk_alert`, `ai.risk_case`, `ai.case_evidence`, `ai.case_action` | scope; evidence and action via case | Alert, case and confirmed fraud kept distinct (AIP-163) |
| Recommendation | **log** `ai.rec_decision`, **log** `ai.rec_event` | scope | Compact decision (funnel counts, exclusion reasons, versions, scores, final set) plus the interaction lifecycle |
| | `ai.rec_decline` | scope | Cross-channel decline store keyed on customer or session (AIR-065) |
| Audit | **log** `ai.decision_record` | scope | The standard record for every governed decision, hash-chained per tenant (AIC-204) |
| Monitoring | `ai.governance_alert`, `ai.incident`, `ai.risk_register`, `ai.control`, **log** `ai.control_test` | scope | Deterministic control checks (AIC-219) |
| Evaluation | `ai.eval_suite`, **log** `ai.eval_run`, `ai.release` | platform + scope | Shadow, canary, production pointer per capability and tenant |

The AI log database uses the same `platform.apply_scope_rls` function. The AI service sets `ticvai.scope_paths` from the resolved session on both connections, so auditors scoped to a venue see only that venue's traces.

### 3.2 Events

**Consumed** (existing events that gain an `ai` consumer, plus existing AI consumers):

| Event | Why AI consumes it |
|---|---|
| `catalogue.productPublished`, `fnb.menuPublished`, `retail.merchandisePublished`, `whitelabel.contentPublished`, `assets.documentIndexed`, `maintenance.templatePublished`, `reporting.definitionPublished`, `marketing.caseClosed` | Re-index; invalidate answer and candidate caches (existing) |
| `order.completed`, `order.paid`, `order.refunded`, `cart.abandoned` | Recommendation attribution; risk velocity and entity risk; forecasting actuals |
| `access.validated` | Journey state for in-venue recommendations; scan abuse; attendance actuals |
| `seat.sold`, `stock.depleted`, `performance.cancelled` | Candidate availability; forecast and risk context |
| `entitlement.issued`, `shift.closed`, `ledger.periodClosed` | Membership conversion; staff leakage (voids, refunds, cash variance); accuracy windows |
| `approval.granted`, `approval.rejected` | Resume or close action plans (existing consumer on `granted`) |
| `conversation.handedOver` | Close the assistant conversation's decision record |
| `tenant.suspended` | Stop batch work; freeze plans |

**New events the owners must publish** (through ADR-0033's outbox): `payment.attemptFailed` (Payments), `identity.loginRecorded` with a hashed device id (Identity), `order.cancelled` and `order.exchanged` (Orders), `entitlement.transferred` (Catalogue), `access.rejected` with reason (Access), `approval.expired` (Approvals), and `promotions.recommendationStrategyPublished` (Promotions). Without the first five, most of the fraud requirements (AIP-111, AIP-118, AIP-122, AIP-124) have no signal.

**Emitted by AI:** `ai.ceilingApproaching` (existing), `ai.forecastPublished`, `ai.operationalRequirementIssued`, `ai.riskAlertRaised`, `ai.riskCaseClosed`, `ai.insightRaised`, `ai.planExecuted`, `ai.planFailed`, `ai.capabilityPaused`, `ai.incidentOpened`. Every event carries ids and scope, never prompt text or personal data beyond ids (ADR-0043's spirit applied to the broker).

Consumers are idempotent and dead-letter after five attempts (ADR-0033). Velocity counters run in `ai-realtime`, so the real-time path is never behind a re-index backlog in `ai-batch`.

### 3.3 Model serving and the provider abstraction

**One call shape.** Capability code calls `gateway.run(task, inputs, schema?)`. A *task* (for example `assistant.guest.answer`, `config.extract`, `analytics.spec`, `case.summarise`) is registered with its capability, required features (tool calling, structured output, context size, language), data classification, streaming flag and default model. Capability code never names a provider (ai-platform rule 1).

**Routing, in order:**

1. **Allowed set.** The intersection of the platform catalogue (production status in this environment), the region's `allowedAiResidencies`, tenant policy (a tenant may restrict itself to private models, AIC-038), the task's data classification and the governance data policy (AIC-018).
2. **Pre-selection.** Each task has a default model chosen by us (AIC-010). The tenant may override it per task with its own key; every override is logged, and the fitness check warns when the new model lacks a required feature or is far outside the task's evaluated class (AIC-011, AIC-012).
3. **Cascade** (ADR-0034): the small model answers; the gateway escalates only where the task defines a checkable signal. Examples: schema validation failed twice, retrieval reliability "partial", or the classifier's margin below threshold. We do not route on a model's self-reported confidence, because none of the sources accept it as meaningful.
4. **Fallback:** a circuit breaker per endpoint (opens at 50% errors over 20 calls, or 95th-percentile above twice the task budget for 60 s; half-open after 30 s). The next model in the chain must support every required feature (AIC-020). `residencyRefused` is returned, never failed over.
5. **Controlled degraded mode** when nothing answers: search-only, rules-only, or "a person will help" (AIC-243).

**Before the call** the gateway checks the per-request budget and ceiling behaviour, applies `maskedFields` (fail closed), blocks a payload carrying a customer identifier the data policy does not allow (AIC-214), orders the prompt stable-first, and short-circuits refusals a rule can decide. **After it**, it validates structured output, writes `ai.activity` and emits telemetry (AIC-244).

**Endpoints:**

- **Default LLM:** Azure OpenAI in UAE North under TICVAI's subscription, with per-tenant keys for attribution: a small model for guest answers, extraction and classification, a stronger one for staff analysis and configuration planning. Which models UAE North offers at go-live is ours to confirm against the task list (section 8).

**"Multiple providers", read against AI-D02 (21 September minutes, M21-03).** The minute asks for several providers with each agent on the model that fits its task. AI-D02 is the later decision and stands: **one managed provider by default**, and the choice per agent is a choice of model inside it. More providers and bring-your-own models are added only when TICVAI enables them for a tenant (AI-D14). `AiProvider.taskKeys` binds a provider to named agent tasks, so a second provider can serve one agent without touching the others. The default model per agent:

| Agent | Tasks | Default model (Azure OpenAI, UAE North) |
|---|---|---|
| Guest (concierge, Help me choose wording, visit planner) | `assistant.guest.answer`, `planner.guest.refine` | Small |
| Operations (staff assistant, configuration assistant, seat-map labels) | `assistant.staff.answer`, `config.extract`, `config.plan` | Stronger for planning, small for extraction |
| Finance and analytics (analytics assistant, metric explanation wording) | `analytics.spec`, `analytics.narrate` | Stronger |
| Marketing (content drafts, translations) | `content.draft`, `content.translate` | Small |
| Security and risk (case summaries) | `case.summarise` | Stronger |

**Model fitness (M21-09, our proposal).** Each task has a golden set; `runAiEvaluation` scores a model on it and the score lands in `AiModel.taskFitness` with the task's band. Binding a model outside the band returns `fitnessWarnings` on `setAiProvider` (underpowered, overpowered or never scored). A warning is recorded and shown on ADM-037; it never blocks.
- **Embeddings and reranking:** BGE-M3 (dense plus sparse in one pass) and a multilingual cross-encoder, **self-hosted on CPU in the cell**, so search and retrieval call no external API (AIC-042). BGE-M3 is the default pending ADR-0021's two-stage evaluation (AIC-067).
- **Customer endpoint:** any OpenAI-compatible or Azure OpenAI endpoint plus key, with no custom development (AIC-009). Any other protocol needs an adapter, and we say so.
- **Self-hosted open LLM** (vLLM on GPU) for private-only tenants and `onPremiseIsolated` sites with a client GPU (ADR-0046), through the same gateway.
- **Classical models** (LightGBM, statistical forecasters) load in-process from Blob and score in under 5 ms. They are registered in the same catalogue, so lifecycle, release and audit are uniform (AIC-013, AIC-015).

### 3.4 Feature computation

We do not buy a feature store; with one AI engineer it costs more to run than it saves.

- **Feature definitions as code:** one versioned Python package of pure functions over events and reference data, each with freshness, a business-configurable lookback (AIR-109), data category and permitted purposes (AIC-156, AIR-182).
- **Online:** stream consumers apply those functions into Redis: sliding-window velocity counters (per token, device, account; 10 min, 1 h, 24 h), recency-frequency-spend, affinity, session context, entity risk. Every value is freshness-stamped; stale values are excluded (AIR-115).
- **Offline:** nightly, the same functions run over the analytical replica into per-tenant Parquet. One function for both means training/serving skew is a bug in one place.
- **The feature-set version** goes on every decision record (AIC-199).
- **Forecast signals** record coverage, freshness and a missing-data rule; missing is stored as unavailable, never defaulted (AIP-203).
- **Identity** keys on the deduplicated guest profile (M18, AIP-207); anonymous sessions are enriched on login, not discarded (AIR-107).
- **Sensitive data never becomes a feature automatically** (AIR-185); a new customer-level feature is a governed change (AIR-192).

### 3.5 Evaluation and release

**Golden sets per capability**, in the repository for platform behaviour and in Blob for tenant-specific sets. They include permission and tenant-isolation cases ("show revenue for another tenant" must be refused), Arabic, English and code-mixed queries. **Isolation and permission cases must pass 100%**; a single failure blocks release (AIC-255).

**Release stages for any model, prompt, routing, embedding or retrieval change** (AIC-260):

```
draft → offline eval (golden sets + backtest) → shadow (recorded, not shown)
      → canary (venues or % of traffic) → production → monitored   · rollback = pointer switch
```

Approval: `PLATFORM_AI_MANAGE` for platform-level releases, `AI_APPROVE` in the tenant for tenant-level ones. The existing `setSuggestionProvider` shadow mode is this pipeline's shadow stage.

**Promotion gates (ours, client to correct):**

| Capability | A model replaces the rule when, over a shadow period of at least 6 weeks |
|---|---|
| Forecast | WAPE at least 10% better than the baseline rule at the 7-day horizon; bias within ±3%; 10th-percentile–90th-percentile interval coverage between 70% and 90% |
| Fraud | At the same review rate: recall at least equal to rules-only, precision at least 20% better; no segment slice (family, B2B, reseller) with a false-positive rate above the rules' (AIP-143) |
| Recommendation | A controlled experiment against rules with a minimum sample, with guardrails on refund rate, abandonment and checkout time (AIR-145..147) |
| Assistant | Groundedness ≥ 95%, citation accuracy ≥ 95%, no regression on the previous release's set |
| Configuration | Plan validation pass rate ≥ 90% on the golden set; zero unsafe steps |

**No online learning, anywhere.** Labels (suggestion outcomes, analyst dispositions, recommendation interactions, forecast actuals) are collected continuously and used only by the next candidate model, and only the outcomes the strategy selects (AIR-082, AIP-139). Monitoring never switches a model; it only raises a review (AIC-252).

### 3.6 Caching (ADR-0034)

Layers, in the order a request meets them:

| Layer | Applies to | Key | Invalidation |
|---|---|---|---|
| Guardrail short-circuit | All assistants | n/a | Policy publish |
| Semantic, then exact, answer cache | Guest FAQ-class answers only (semantic threshold 0.95, per capability) | tenant, scope path, locale, policy version | Source events (same as the index), TTL cap 60 min |
| Negative cache; single-flight | "No answer found" (5 min); identical concurrent calls | request hash | TTL |
| Analytics result cache | NL analytics | semantic spec hash, scope, data watermark | New watermark |
| Embedding cache | Ingestion | content hash, model | Model change |
| Candidate cache | Recommendations | placement, product, scope | `catalogue.productPublished`, `stock.depleted`, `seat.sold`, strategy publish |
| Feature cache | Real-time | entity | Stream updates plus freshness stamp |
| Decision TTL | Recommendations | decision id | 30 s capacity-sensitive, 30 min otherwise (AIR-208) |

Prompt-prefix ordering and the model cascade apply to every LLM call (3.3). **Two rules we add to ADR-0034:** the semantic cache never serves recommendations, fraud, or answers with live numbers; and every key carries the policy version, so a policy publish invalidates what it shaped. `ai.activity` records which cache answered.

### 3.7 Error handling and degradation

**The rule:** every capability declares its degradation mode (AIC-241), and the sale path never waits on AI beyond a stated budget.

| Capability | Model/provider down | `ticvai-ai` down | Budget or ceiling reached |
|---|---|---|---|
| Recommendation | n/a (no LLM) | Slot empty; POS uses bundle list | n/a |
| Fraud scoring | n/a (no LLM) | Orders' rules only; fail-open unless tenant policy says hold | n/a, never disabled by cost |
| Guest concierge | Fallback model, then search-only answers with links, then "ask a person" | Surface hides the assistant | Per `ceilingBehaviour`; default warn and keep answering |
| Staff assistant, analytics | Fallback, then the report builder link | Hidden | Warn; non-critical may be restricted |
| Configuration assistant | Session pauses; the admin configures by hand | Plans already approved wait; none half-applied | Pause new sessions |
| Plan execution | n/a | Checkpointed; resumes; revalidates first | n/a |
| Forecast | Narrative omitted | Last published version stays live, marked stale after 36 h | n/a |
| Governance decision point | n/a | In-process with cached policy; if policy cannot load: low-risk advisory continues, anything at L3 or above is refused (AIC-168) | n/a |

**Error shapes:** the existing problem types stand (`insufficient-data`, `residency-refused`, `quota-exceeded`, `proposal-not-open`). New ones are `governance-blocked` (names the policy and version), `plan-drifted` (names the changed object), `budget-exceeded` (per request), and `capability-paused`. **A refusal is an answer, not an error**, and is logged as outcome `refused`.

### 3.8 Governance, autonomy and the action pipeline

**The decision point** is a library, not a network hop. Given capability, action, scope, principal, data categories and amounts, it returns one of allow, allow with conditions, prepare only, approval required, escalate or block. The answer carries the policy version, conditions, required approvals and an explanation (AIC-166). Effective permission is the intersection of the user's RBAC, the capability's permission, governance policy and the owning module's policy (AIC-153). Conflicts resolve to the more restrictive (AIC-161).

**One autonomy scale (section 5.5):**

| Level | Name | Meaning | First-release ceiling applied to |
|---|---|---|---|
| L0 | Disabled | Not available | Any capability a tenant switches off |
| L1 | Advisory | Explains and recommends; nothing is drafted to run | Fraud restrictive actions; access-security changes; finance actions (AIP-183) |
| L2 | Prepare | Drafts a proposal a person applies in the owning screen | Operational requirements; dynamic-pricing inputs; campaigns (AIP-185) |
| L3 | Execute with approval | The plan runs after approval, through owning APIs | Configuration assistant; forecast publication where not auto |
| L4 | Controlled auto | Runs without approval, only for listed low-risk, reversible actions inside pre-approved ranges | Forecast auto-publish; ranking inside a published strategy; the fraud hold-for-review mapping, if the tenant turns it on |

Lower scopes may tighten a ceiling, never raise it (AIC-151). Autonomy is separate from user permission (AIC-154): a manager who may change a price by hand still gets an AI-prepared price change routed for approval. `ProposedAction.approvalLevel` (1 or 2) is **the approval tier, not an autonomy level**, and the documentation is corrected to say so. It is the floor; the approvals matrix adds thresholds and escalation (M18 decision, AIC-174).

**A step that breaks the owning module's limit is governance-blocked (18 September minutes, M18-01).** Plan validation checks every step against the owning module's own limits (a price above the configured maximum, a discount above the role's ceiling) as well as against governance policy. Such a step is marked governance-blocked, shown on ADM-526 with the conflict it met, and never applied; the rest of the plan may continue only where governance allows partial completion. Purely informational actions (explaining a report) are low risk and need no approval. Environments are `development`, `sandbox`, `staging` and `production`, so a rule can allow in a sandbox what it blocks in production.

**Approval authority is the shared approvals service (M18-02).** AI actions are approval kind `aiRecommendation` in the approval matrix: an approver is authorised up to a value, anything above escalates, and delegation and SLA apply as they do to every other approval. ADM-530, ADM-532 and ADM-534 bind `setApprovalMatrix`, `evaluateApprovalRequirement`, `escalateApprovalRequest`, `createApprovalDelegation` and `setApprovalSlaPolicy` rather than keeping a second approval model for AI.

**The executor** is the only component that calls owning modules, and only for tools registered in `ai.tool` (AIC-088). A step has success criteria, a retry policy (bounded at 3, AIC-135), compensation, and a reversibility flag. Non-reversible steps (a refund, a publish) require the stronger approval tier (AIC-099). A plan may complete partially only where governance allows it; otherwise it compensates in reverse dependency order (AIC-098, AIC-134).

### 3.9 Decision records, explainability and audit

Every governed decision writes one `ai.decision_record` to the log database. That covers a recommendation decision summary, a risk assessment, a forecast publication, a plan step, an assistant answer at "significant" depth, and a governance block. Its fields: trace id, capability, task, inputs reference, evidence (each item labelled source, derived or model-inferred, AIC-197), producer and model version, prompt template version, feature-set version, knowledge version, rule versions, governance decision and policy version, approvals, human decision, execution result and business outcome link. Audit depth is configurable by risk (AIC-202): a guest FAQ answer gets `ai.activity` only.

**Immutability:** append-only, corrections as annotations, and a per-tenant hash chain so tampering is detectable (AIC-203, AIC-204). **Explanations** come at three depths (business, governance, technical), each gated by permission (AIC-195). They are built from structured evidence, never from a model's chain of thought (AIC-192). **Replay** (`replayAiDecision`) is labelled a re-simulation, runs no production action, and is never presented as proof of what happened (AIC-206). **Evidence packages** export as PDF, CSV or JSON with masking and tenant isolation applied (AIC-205).

### 3.10 The engines, rules-first

| Engine | Day-one producer | Statistical producer (first release) | Model producer (promoted per tenant, section 3.5) |
|---|---|---|---|
| Forecast | The baseline (section 3.13): venue AI profile x venue-type pattern x UAE calendar x weather, bookings on hand as a floor; then the same-weekday average as own weeks arrive | Seasonal exponential smoothing with holiday and Ramadan regressors; pace-based pickup for T-7..T-0; cold start from category or sister-venue baselines with reduced confidence (AIP-041) | Global gradient-boosted model per tenant with weather, calendar, pace and price features |
| Anomaly | Configured thresholds | Seasonal baseline with robust z-score (median/MAD) per KPI; peer comparison across venues (AIP-082) | Only where a KPI's false-alarm rate warrants it |
| Risk | Weighted rules (orders, payments, wallet, access rules stay with their owners) plus cross-module velocity | Entity baselines per entity type (AIP-128); graph features: shared device, token, account (AIP-111) | Gradient-boosted classifier on analyst-labelled outcomes |
| Recommendation | Relationship map plus business priority | Co-purchase affinity with minimum-support thresholds (AIR-137); popularity by segment and daypart | Learning-to-rank on interaction outcomes |

**Ownership of overlapping detections** (req-predict conflict 7): anomaly detection owns **aggregate** deviations (the refund rate at a venue); risk owns **actor-level** patterns (this cashier, this card, this device). Staff leakage (repeated refunds by one cashier, voids at one till, repeat cash shortages) is therefore risk. Both write through one correlation key, so one situation produces one alert (AIP-090).

---

### 3.11 Help me choose, suggested from the catalogue (rev 3, decided 29 September)

The client's rev 3 prototype asks a guest one or two questions and opens the matching product or flow. Help me choose is a venue configuration: `GuidedChoice` in `white-label.yaml`, with draft and published states. Chinmay decided on 29 September that once a venue's products are uploaded, AI proposes the sections and the venue reviews them. **It is a suggestion under capability C7 (the configuration assistant), at autonomy level "suggest"**, so nothing is ever published without a person.

**How a suggestion is made, rules first (section 5.1):**
1. **Read the catalogue.** For each product the venue sells to guests, read its category and subcategory, segment tags (level, audience), minimum height and age, duration, price band, info-only flag, language and format. This uses the catalogue API with the venue's permissions, not the database.
2. **Pick the questions.** Choose the one or two attributes that split the products most evenly. Ask first about the attribute that most reduces the choice, such as who is coming, then level. Drop any attribute where one answer would leave nothing bookable. This is deterministic, so the same catalogue gives the same questions.
3. **Map each answer** to a product, a category or a flow. An answer that would lead to more than one product leads to its category.
4. **Write the wording.** A language model writes the question, the answer titles and the one-liners in the tenant's languages. It is sent the attributes only, never guest data. If the model is not available, the attribute names are used as they are, so the rules alone still make a usable draft.
5. **Save a draft** `GuidedChoice` with `source: aiSuggested`, and a decision record (C12) holding the inputs, the split each question makes, and the model and prompt versions.

**Review and publish.** The venue sees the draft in Venue Management beside a preview. It can edit the draft, discard it, or publish it. Publishing is an ordinary configuration change by a person, audited like any other.

A catalogue change after publishing does not rewrite the published version. It raises a new suggestion when a mapped product is withdrawn, or when new products are left out by every answer.

**Contract surface.** The draft lands through `proposeGuidedChoice` in `white-label.yaml`, a service-only call added on 29 September that saves a draft with `source: aiSuggested` and a `suggestionRef`. Publishing is `publishGuidedChoice`, which only a person holding `TENANT_PUBLISH` can call. The AI side still needs to be added to `ai.yaml` when this design is approved: a job that reads a venue's products and calls `proposeGuidedChoice`, and a read for the reasons behind a suggestion. Cost is one short text-model call per suggestion, well inside the per-tenant budget (section 4.5).


### 3.12 What a tenant sees over time (added 29 September)

Nothing on a dashboard waits for a trained model. Every engine ships with a rules or statistical producer, so forecasts, risk scores, anomalies and recommendations exist from the first week, each labelled with its basis. As history builds, the statistical producers improve on their own: they read whatever data exists. A trained model is different. It is trained and run in shadow automatically, but **it goes live only when a person promotes it**. Chinmay confirmed on 29 September: when a shadow model passes its threshold, raise it to the admin; never switch automatically.

| Capability | First week | Improves by itself with | A trained model needs |
|---|---|---|---|
| Forecast | Same-weekday average plus bookings on hand; cold start from a sister venue or category, with a wide band | Seasonal smoothing, holiday and Ramadan regressors, pace-based pickup | About one season of actuals, then a six-week shadow that beats the rule (3.5) |
| Anomaly | Configured thresholds | A seasonal baseline per KPI after a few weeks of history; peer comparison across venues | Only where a KPI's false-alarm rate warrants it |
| Fraud | Weighted rules plus velocity counters | Entity baselines and graph features as events accumulate | Analyst-labelled cases, in the thousands |
| Recommendation | Relationship map plus business priority | Co-purchase affinity once orders clear the minimum-support threshold; popularity by segment and daypart | Interaction outcomes and a controlled experiment against the rules |
| Assistants, analytics, configuration | Full function; they read the catalogue, the knowledge base and the semantic layer, not history | Knowledge gaps filled by content owners; golden sets grow | Not applicable: no per-tenant training |

**The sequence for a new tenant:** rules, then statistics improve quietly, then a shadow model earns its place, then a person flips it. The dashboards look the same throughout; only the producer behind the number changes, and the decision record says which. The review lands as an `ai.governance_alert` of kind `promotionReady` and a tile on the P09 governance area, so nobody has to go looking for it.

**What this table left open** is the first week of a new venue with one site and no history: "same weekday over 8 weeks, or a sister venue" has neither, and the contract answered 422 below each kind's minimum history. Section 3.13 closes it.

### 3.13 Baseline, then learn: maturity stages and the estimator interface (added 30 September)

The product owner's rule (29 September): data-driven AI is built right now and gets more accurate with time, and **no customer is told a feature comes later because they have no data**. The AI functions review (`audit/ticvai/steps/AI2/ai-functions-review.md`, its "packageFindings") showed that the rules themselves needed history, that `requestSuggestion` refused with 422 on Block A screens, and that there was no historical import and no cold-start setting. Decision 10 of 30 September adopted the review.

**One estimator interface per question.** A question is a suggestion kind, a forecast definition, a risk score or a recommendation rank. Behind it sit three producers with the same contract:

| Producer | What it reads | When it answers |
|---|---|---|
| **Prior** (baseline) | The venue AI profile (`setAiVenueSettings`), the starting pattern for the venue type (water park, theme park, family entertainment centre, museum, arena, zoo or aquarium; TICVAI-written from published sources and made-up curves, **never another tenant's data**, AIP-149), the UAE calendar (Sat–Sun weekend, public holidays, Ramadan and Eid by Hijri date, school holidays, summer heat for outdoor venues) and the weather (AI-D10) | Day one |
| **Statistical** | Own data, imported history included, pulled toward the prior: `(k x prior + n x own mean) / (k + n)`, with `k` the prior's weight in observations (4 same weekdays by default, `coldStart.priorWeightObservations`) | Re-estimated nightly, each run a recorded producer version |
| **Learned** | A model trained per tenant, weekly (`listAiTrainingRuns`), backtested, then run in shadow | Only after an admin promotes it (AI-D16) |

The routing already existed (`setSuggestionProvider`, the forecast `producer`, the release pointer); what is new is the prior, the import and the maturity signal. Nightly re-estimation is not the online learning section 3.5 rules out: no model switches itself, and every re-estimate is a recorded version.

**Maturity on every answer** (`AiMaturity` on `Suggestion` and `AiForecastVersion`; one row per question in `ai.capability_maturity`):

| Stage | When | Behaviour | Switch |
|---|---|---|---|
| `starting` | Day 1 | The prior; wide range (forecast about +/-40%); "Limited historical data" | — |
| `learning` | About 4 weeks | Weekly patterns and short-range answers come mostly from own data; accuracy is measured and shown | Automatic, recorded |
| `established` | About 3 months, or at once with 12+ months imported | Own level and trend lead; the prior fills gaps such as a holiday not yet seen | Automatic, recorded |
| `learned` | A season, plus a 6-week shadow that passes the gate in 3.5 | The trained model answers | **An admin promotes it** after a `promotionReady` alert |

Every answer carries a "Based on" line (*your venue profile, UAE calendar, weather, 23 days of your sales*), the share of own data, and what the next stage needs. **422 survives for one case only: a missing setting** (no current cost for a price, no par level, no ride capacity), and the problem names the setting and the screen that sets it. The venue sees every question's stage on ANL-071 AI Maturity & Learning, where it also corrects its profile and imports history; platform staff see it on ADM-519.

**What still cannot happen by 2 April:** a trained model live for a tenant, because promotion needs about a season of that tenant's data (or 12 months imported) and a 6-week shadow. The code for every model ships; promotion happens tenant by tenant.

---

## 4. Scale and reliability

### 4.1 Load estimates

**Assumptions (stated, not known):** 30 tenants per region at 18 months (ADR-0021 says "tens"; CF-97 still open). The mix is 10 large, 10 medium and 10 small. A large tenant has 6 venues, 40,000 visitors on a peak day, 25,000 orders a day, peak 20 checkouts per second and 250 staff users.

| Load (large tenant, peak day) | Estimate | Basis |
|---|---|---|
| Recommendation decisions | 240,000/day; peak 60/s | 60,000 sessions × 4 placements |
| Fraud scores (sync) | 35,000/day; peak 15/s | Orders plus retries |
| Stream events into AI | ~1.5 million/day | Orders, scans, interactions |
| LLM calls | ~3,750/day | 2,000 staff questions; 2,400 guest questions at 50% cache hit; 300 analytics; 50 configuration turns; 200 insight narratives |
| Forecast series | ~12,000 daily series × 90 days, plus hourly venue series | 6 venues × 200 products × 10 channels |
| AI log growth | ~0.6 GB/day | Decisions 1.2 KB each, events 200 B, assessments 2 KB, activity 12 KB |

**Region aggregate design targets:** 1,000 recommendation decisions per second at 95th-percentile 120 ms; 250 fraud scores per second at 95th-percentile 50 ms; 150,000 LLM calls per day; about 6 GB per day of logs, kept 90 days hot (roughly 550 GB), then aggregated.

**Sizing:** `ai-realtime` 4–12 pods of 2 vCPU (a decision is ~3 ms CPU and ~10 Redis reads); `ai-interactive` 3–10 pods; `ai-batch` 2–8 workers on queue depth; 2 × 4 vCPU nodes for embedding and reranking; 13 GB Redis; a 4 vCPU, 1 TB AI log server. All 30 tenants' forecasts finish in about 90 minutes on 4 workers.

### 4.2 Per-tenant isolation

The tenant database is the vector, configuration and state boundary; RLS carries venue scope. Every log row carries scope and passes RLS. Redis keys, Blob containers, model files and caches are namespaced per tenant. Queue partitions are keyed by tenant, so one tenant's re-index cannot delay another's velocity counters. Per-tenant token budgets and rate limits sit in the gateway, and the tenant's concurrency share on `ai-interactive` is capped at 25% of the pool. **No model is trained on pooled tenant data** (AIP-149). A platform baseline for cold start is trained only on data tenants have contractually allowed, and by default uses rules, not pooled data (AIP-148).

### 4.3 Failover

- **Model endpoints:** breaker and fallback as in 3.3. The secondary is a second Azure OpenAI deployment with its own quota, then the in-cell open model for the tasks it passes evaluation on. Cross-border fallback exists only for a tenant with a recorded transfer mechanism (ADR-0009 §3).
- **Service:** `ai-realtime` runs across three availability zones. Callers own the budget, so a zone loss shows up as fallbacks, not errors.
- **Region:** AI follows the platform's regional disaster recovery; the AI log database is geo-backed-up. AI is Engagement tier: RTO 4 h, RPO 15 min for configuration and state, 24 h for logs.
- **Data:** a rebuildable cache is never the only copy of anything (ADR-0020's cache exemption).

### 4.4 Monitoring and alerting

Every capability has SLOs (availability, latency, error rate, freshness) and an error budget. A provider missing its contract is tracked separately from our SLO (AIC-246). Alerts are grouped into operational incidents, kept separate from governance incidents and linked where both apply (AIC-250).

| Alert | Threshold |
|---|---|
| Recommendation fallback rate | > 5% for 10 min |
| Fraud scoring timeouts | > 1% for 5 min |
| Provider breaker open | Any, immediate |
| Masked-field count zero on a prompt touching guest data | Any: a defect, page |
| Cross-tenant or cross-scope attempt refused | Any: governance alert |
| Spend | 80% and 100% of ceiling (`ai.ceilingApproaching`) |
| Forecast not published by 05:00 | Per tenant |
| Forecast bias, input drift (PSI > 0.2), override rate shift | Governance review, never an automatic switch |
| Index lag | > 15 min behind source events |
| Evaluation regression | Blocks release |

**Deterministic controls** run nightly as SQL over system records (AIC-219). Examples: every applied tier-2 action has an approval by someone other than the requester; no L3+ action executed without approval; no card field in any prompt.

### 4.5 Cost per tenant

Illustrative token prices, to be confirmed against the Azure UAE North price sheet before anything is quoted: small-model class about $0.15 / $0.60 per million input/output tokens; large-model class about $2.50 / $10. Average call: 3,500 input and 350 output tokens, 80% on the small model, before prefix-cache discount.

| Tenant | LLM tokens / month | Infra share / month | Notes |
|---|---:|---:|---|
| Small (1 venue, 3,000 visitors/day) | $20–40 | $60–120 | Dominated by the fixed platform share |
| Medium (3 venues, 15,000/day) | $90–150 | $200–350 | |
| Large (6 venues, 40,000/day) | $250–400 | $600–900 | Tokens driven by guest questions; cache hit rate is the lever |

Embeddings and reranking are self-hosted, so their marginal cost is CPU, not tokens: a 20,000-chunk corpus embeds in minutes. The regional AI tier (pods, embedding nodes, Redis, AI log server) is about $2,500–3,500 a month, shared by usage. **ML and rules cost almost nothing per decision**, which is part of why they, not LLMs, sit on the high-volume paths.

---

## 5. Trade-offs

### 5.1 Rules-first, then ML

**Options.** (a) Ship ML forecasting, fraud and recommendation from day one, as the client's books imply. (b) Defer the capabilities entirely until 6–12 months of data exist (CH05 §5.1, §5.11; the 14 August agreement in principle; the 194 parked requirements). (c) **Ship the capabilities now with rules and statistics as producers, capture labels from day one, and promote a model per tenant only when a shadow run proves it beats the rule.**

**Choice: (c).** The minutes (M18, M21) walk these capabilities through as governed platform features and never phase them. So (b) would leave the client without capabilities the minutes treat as real. (a) produces "confident numbers that happen to be wrong" (scope paper §1). The package already has the mechanism in `requestSuggestion`, `SuggestionBasis` and shadow mode. **The gate is evidence, not a calendar.** A high-volume tenant may earn its fraud model at month four, and a quiet one never.

The minutes win on "these capabilities exist". CH05 and the 14 August principle win on "no trained model without data". They do not conflict once "capability" and "producer" are separated.

### 5.2 One forecasting service, not BI's own studio

**Options.** (a) FCST: one shared forecasting service; BI consumes published values. (b) BI Board 9.7's own forecasting studio with its own models and accuracy. (c) Both.

**Choice: (a).** Two forecasters produce two different numbers for the same Saturday, and the operations manager then trusts neither. BI's extra subjects (refunds, cash collection, membership renewals, churn, next-hour, month-end and quarter-end horizons) become forecast definitions in the one service. BI's studio screens bind to the forecast operations, and Reporting reads published versions. FCST's recommendation stands because the minutes are silent and it is the only structure that satisfies AIP-036 and AIP-037 together.

### 5.3 Fraud scored per transaction and per entity

**Options.** Per customer (M21 §4.12), per transaction (FRAUD Board 1), or per entity (FRAUD p.59).

**Choice: both, layered.** Entity risk (customer, account, device, token, credential, cluster) is computed asynchronously from composite signals. That is the minutes' customer-level composite, and it satisfies the M21 decision "no single signal decides". Transaction risk is computed synchronously and reads entity risk as a feature. The minutes are narrower than FRAUD, not contrary to it, so both hold (req-predict conflict 5). Scoring only per customer would miss anonymous and guest checkouts; scoring only per transaction would re-derive history inside an 80 ms budget.

### 5.4 One recommendation and upsell engine

**Options.** (a) Keep today's scatter: `promotions.getRecommendations`, `getUpsellSuggestions`, `fnb.listFnbRecommendations`, `retail.listRetailRecommendations`, each with its own logic. (b) **One engine in `ticvai-ai` owning the runtime; Promotions keeps strategy, relationship and suppression configuration.** (c) Move everything, configuration included, into AI.

**Choice: (b).** AIR-053 is a must: one central service with channel adapters. The minutes' cross-channel decline rule (AIR-065) cannot be enforced by four engines. Configuration stays in Promotions because merchandising is commercial ownership, and the boards for it are already contracted there. Runtime moves because decision records, experiments, features and models are AI stores (ADR-0020 lineage). R&P governs where it and UCS differ, and UCS adds depth (req-personal C1). Seat *selection* (`seating.recommendSeats`) stays in Seating as a deterministic best-available service; seat *upgrades* are upsell placements in the engine.

### 5.5 One autonomy scale

**Options.** GOV's 0–4, CFG's 0–3, or CORE's unnumbered modes.

**Choice: GOV's 0–4** (table in 3.8). GOV is the governance authority and CORE says execution modes "should align" to governance. Under it, GOV p.5's "Configuration Assistant Level 2" means Prepare, and we ship the configuration assistant at L3 (execute with approval) as its ceiling. For access-security changes, GOV's L1 advisory wins over CFG's "elevated approval" because the more restrictive policy wins (AIC-161). UCS's "governed optimisation" (AIR-090) is L4, and it stays off in the first release, following R&P's deferral (AIR-091).

### 5.6 Confidence display

**Options.** One universal percentage everywhere (CFG, BI "Confidence 91%"), or per-capability representations.

**Choice: per capability, and never a bare percentage.** CORE p.23, GOV p.76 and FCST p.18 forbid a universal figure. `ai.yaml` already makes confidence null for heuristics. BI and CFG lose on this point.

| Capability | Shown |
|---|---|
| Forecast | 10th-percentile–90th-percentile range, plus measured accuracy by horizon from backtests, labelled "measured" |
| Fraud | Risk score 0–100 and band, labelled "risk score", never a probability |
| Recommendation | High/medium/low band from separation and context completeness; numeric normalised score for administrators only |
| Assistant, analytics | Reliability category: grounded, partial, conflicting sources, insufficient evidence |
| Configuration | Provenance per value; no confidence number |

### 5.7 Text-to-SQL or approved services for staff questions

**Options.** (a) Free text-to-SQL on the analytical replica (CH05 §5.9, the current `askReportingQuestion`). (b) Only approved APIs and services (CORE p.33). (c) **The model produces a semantic query spec over the governed KPI layer, and Reporting compiles it deterministically.**

**Choice: (c).** BI's AIP-170 is a must: answer from the semantic layer, and match the official dashboards. Free SQL cannot guarantee that "revenue" means the dashboard's revenue, and it needs venue scoping inside generated text. (c) inherits RLS and metric definitions, keeps the checkable SQL (CH05's intent), and is what CORE means by approved services. Questions outside the semantic model get "not available yet" plus a knowledge-gap record, not an improvised query.

### 5.8 The vector store: pgvector, not Qdrant

**Positions on record.** CH02 has Qdrant everywhere with a payload filter. ADR-0009 §2 has Qdrant for dedicated cells and pgvector for the shared tier. ADR-0020 says "a cell without Qdrant has no AI". ADR-0021 (Proposed) has Qdrant with one shard per tenant.

**Choice: pgvector in each tenant's own database, everywhere; Qdrant kept as the documented scale-out.** ADR-0038 (Accepted, after all four) gives every tenant its own database, even in a shared cell. That makes the database the strongest isolation boundary we have, and it sits exactly where ADR-0021 wanted a shard. It also brings three things Qdrant cannot give:

- **RLS enforces venue scope.** ADR-0021's central worry, "Qdrant enforces nothing", disappears.
- **Erasure and offboarding follow the tenant database lifecycle**, not a second store's (AIC-266, AIC-268).
- **One store fewer** needing DESC approval (AIC-045), costing $600–700 a month in HA, and still awaiting the 12 August compliance confirmation.

The sizes are well inside pgvector's comfort zone: about 20,000 chunks per tenant, 1024-dimension half-precision. Hybrid retrieval uses BGE-M3's learned sparse vectors in `sparsevec` fused with dense by reciprocal rank. Learned sparse weights need no corpus IDF, which also dissolves ADR-0021's IDF-scope problem.

**What survives from ADR-0021:** one table per embedding model; the single retrieval client with no scope parameter (kept even with RLS, as defence in depth); shadow re-embed on model change; and the two-stage model evaluation. On-premise (ADR-0046) gets simpler: no fourth store to ship.

**Revisit trigger:** section 6.

### 5.9 Who pays for tokens

**Positions.** ADR-0034 (Accepted 31 August): "tokens are billed to the tenant … BYOK is settled". M21 §5 (21 September): the system selects the model by default, and the client *may override* with its own key.

**Choice.** The minutes are later and the client decided them, so the default follows M21. **TICVAI-managed provider accounts (Azure OpenAI, UAE North), metered per tenant and re-billed per token through Subscription & Licensing** (AIC-232). BYOK is an override per task or per tenant; the tenant then pays the provider directly and we meter for visibility only.

ADR-0034's substance survives: the tenant bears token cost, per-tenant keys give independent reconciliation, and ceilings and `quotaExceeded` stay. Only "BYOK is the default" is corrected. Ceiling behaviour becomes per capability, so a budget never silently disables fraud scoring (which has no tokens) or a critical capability (AIC-227). The guest concierge defaults to warn (decided 17 August).

### 5.10 Other decisions worth recording

- **LLMs off every money path.** Recommendation, fraud, forecasting and anomaly engines use no LLM for decisions (AIC-028, AIP-146, AIR-049). LLMs explain, summarise, extract and converse.
- **Where AI monitoring lives** (M18: "Softlabs' call"). **One governance area in P09**, bound to the operations above, **plus module widgets** built as saved dashboards from the same operations (ADR-0041). Not 40 bespoke dashboards.
- **Guest chatbot versus staff assistant** (req-core conflict 13). One assistant runtime with profiles: guest concierge, support chatbot, staff by role. The profile decides sources, tools, model task and scope.

---

## 6. What we'd revisit as it grows

| Trigger | Revisit |
|---|---|
| A tenant passes ~2 million chunks, or retrieval 95th-percentile exceeds 150 ms at the replica | Move that tenant's vectors to Qdrant with a shard per tenant (ADR-0021's design) behind the same retrieval client |
| More than 3 people building ML | A managed feature store and experiment tracking instead of features-as-code |
| More than 60 tenants in a region, or LLM calls above 500,000 a day | Split `ai-interactive` into assistant and configuration deployments; dedicated Azure OpenAI capacity (provisioned throughput) |
| Fraud labels above ~5,000 confirmed cases in a tenant | Graph neural or sequence models on the relationship graph; a streaming engine instead of Redis counters |
| Recommendation traffic above 5,000 decisions/s in a region | Precomputed per-customer candidate lists; an online ranking service separate from `ai-realtime` |
| Six months of clean L3 operation with low override rates | Enable L4 governed optimisation for named low-risk parameters (AIR-090) |
| A client asks for pooled cross-tenant models | Contract, consent and federated or anonymised training; not before |
| Azure UAE North lacks a model a tenant needs | Self-hosted open model on GPU in-region before any cross-border route |

---

## 7. Phasing

Effort is in developer-weeks at the AI-assisted pace assumed in the six-month plan. It covers the AI service and the owner-side .NET changes; front-end binding is shown separately.

**Block A: first release, months 1–2. Governed LLM capabilities on the platform core.**

| Work | Capabilities | Dev-weeks |
|---|---|---:|
| Gateway: routing, catalogue, masking, budgets, breaker, caches, telemetry | C1, C13 | 4 |
| Governance decision point, capability registry, autonomy, policy versions | C2 | 4 |
| Action pipeline, executor, Approvals integration, tool registry, `validate-only` on the first 15 tools | C3 | 5 |
| pgvector migration, BGE-M3 and reranker in-cell, hybrid retrieval | C4 | 3 |
| Assistant profiles: staff, guest concierge, support | C5 | 3 |
| Configuration assistant: discovery, blueprint, plan (seating and ticketing first, then general; the ai-scope paper's Reading B) | C7 | 5 |
| Analytics assistant via semantic spec | C6 | 3 |
| Decision records, trace, audit search, evidence export | C12 | 3 |
| Evaluation harness, golden sets, release pointer | C13 | 2 |
| **Block A total** | | **32** |

**Block A also carries the visit planner (29 September, MOB-6):** the rules planner in `venue-map` and the AI planner agent on top of it (the `itinerary` kind and the agent's five plan tools), about 1 dev-week of AI work beside the planner's own back end. It supersedes the deferral of 28 September (audits R187, R209; rev 3 GAP-C3).

**Block B: first release, months 3–6. Rules-first engines and label capture.**

| Work | Capabilities | Dev-weeks |
|---|---|---:|
| Event consumers, feature library, Redis counters, Parquet snapshots | all engines | 3 |
| Forecasting service: definitions, baseline and statistical producers, versions, accuracy, publication, scenarios, weather adapter | C8 | 6 |
| Operational requirements from forecasts | C8 | 2 |
| Anomaly detectors and the insight lifecycle | C9, C6 | 3 |
| Risk: sync scoring, entity risk, graph edges, alerts, cases, `proposeRiskAction` | C10 | 6 |
| Recommendation engine runtime, decline store, events, attribution, experiment assignment, POS bundle list | C11 | 6 |
| Governance monitoring: alerts, incidents, controls, risk register | C13 | 2 |
| Owner-side .NET: Orders scoring call, Promotions forwarding, seven new events, `recommendationId` on cart lines | — | 4 |
| **Baseline then learn (section 3.13):** estimator interface and maturity block, venue AI profile, starting-pattern packs, historical import, per-tenant training and backtest job, promotion rule | all engines | 8 |
| **Block B total** | | **40** |

**Inside the six months, baseline first (decision 10, 30 September).** The six-month plan of 29 September had moved the configuration assistant, the analytics assistant and anomaly detection past month 6. They are back: none needs history, and each ships with its baseline. The configuration assistant runs in S3–S5 (seating and ticketing first), seat-map and layout generation in S6, anomaly detection in S6 from the venue's configured thresholds and "actual against the forecast", and the analytics assistant in S7. The `requestSuggestion` change (no refusal for little history) lands in S2, because its kinds sit on Block A screens.

**Front-end binding** for ADM-469..558, the P16 AI screens and the recommendation boards is about 16 front-end weeks with generated screens.

**Later (after first release):**

| Work | Dev-weeks |
|---|---:|
| Model producers going **live** per tenant: forecast GBM, fraud classifier, learning-to-rank. The code, training and shadow run are built inside the six months (section 3.13); promotion waits for each tenant's evidence | 12 |
| L4 governed optimisation | 3 |
| External knowledge connectors (SharePoint and similar), once their residency is settled | 3 |
| AI dashboard and report generation (AIP-186, AIP-187) | 3 |
| Partner and external product cross-sell; in-venue location triggers | 4 |
| On-premise local-model packaging | 3 |
| Qdrant scale-out, only if triggered | 3 |

**Staffing, decided (AI-D11, and the plan decision of 30 September).** Staffing is ours to decide, not the client's (AI-D11). **The second AI engineer starts Monday 5 October with Block A, and there is no third.** The two AI engineers carry the engine work: models, pipelines, backtests and the baseline-then-learn layer. The AI endpoints and screens are built by the developers like any other module (six-month plan, decision 11).

**What that leaves.** The AI functions review needed about 50 AI-engineer weeks in Block B against about 35 with two engineers, and assumed the second engineer from 2 November and a third from 7 December. Starting the second engineer on 5 October recovers about four weeks; without a third, about 11 AI-weeks remain short. **The work that gives way first is the trained model producers** (forecast, fraud and ranking, about 9 AI-weeks): their code and training job are built, and they finish running in the background around April to June 2027. No customer notices, because no tenant can pass a promotion gate before then anyway (section 3.13). Everything with a baseline ships inside the six months. The gap is re-measured at the 23 October pace checkpoint.

**The AI sessions with the client (21 September minutes, M21-07).** With risk and fraud covered, the AI workshop topics are complete. AI sessions pause until the conventional modules (POS, guest web, guest mobile) have their build readiness and UI sign-off, and resume later with the smaller AI team.

---

## 8. Decisions taken on 29 September, and what remains

> **30 September 2026:** ADR-0049 decided vectors go to Qdrant from day one, one collection per tenant with a collection-scoped token, reversing AI-D12's pgvector; the pgvector sections below are superseded on that point.

Chinmay answered every question in this section on 29 September, following the readiness rule of the same day: the questions are ours to answer, and only make-or-break questions go to the client. None of these is make-or-break, so **nothing in this design now waits on the client.** Each answer and what it changed:

| # | Question | Decision (29 September) | Effect on the design |
|---|---|---|---|
| 1 | Rules-first, evidence-gated ML | **Yes.** The models are our own, trained per tenant on that tenant's data; no bought scoring service | 5.1, 3.5 stand. ADR-0051 |
| 2 | Default provider and billing | **Yes: managed Azure OpenAI, re-billed per token.** Billing is per module the tenant selects: three packages exist, and a custom package is allowed. TICVAI configures each module's price on the platform, with the subscription and billing settings | AI tokens are one metered line in the tenant's bill (`settleAiUsage`, `recordUsage`). Packages, module listings and simulation are already in `subscription.yaml` (`listPlans`, `setModuleListing`, `simulateCommercialPackage`); the markup is a module-listing setting, not a code constant |
| 3 | Models in UAE North; cross-border | **UAE North for now.** Another region is configured tenant by tenant when it is needed | The region's `allowedAiResidencies` stays the gate; no cross-border route is built for the first release |
| 4 | One autonomy scale, access-security at advisory | **Yes** | 3.8, 5.5 stand. ADR-0050 |
| 5 | Retention | **90 days by default; the tenant may set it longer or shorter.** All AI data retention is one tenant configuration: prompts, responses and conversations, and decision records and approvals too, each with its own period. The audit period (ADR-0047) is the default for decision records, not a fixed rule. AI keeps metadata (summaries, embeddings, indexes) so a question is answered from the index, not by reading the whole history | Retention moves to tenant configuration, beside the other tenant data-retention settings, with a period per data class. Only where law sets a floor (the biometric retention question, kept make-or-break) does the platform refuse a shorter value. 3.9 gains a memory rule (below) |
| 6 | Fraud default | **Fail-open with holds, not declines** | 2.2 B stands |
| 7 | Cross-channel decline | **"Ignored" is not a decline.** Only an explicit decline counts | 3.1 `rec_decline` stands |
| 8 | OTA and reseller channels | **No recommendations in the first release** | AIR-052 stays excluded |
| 9 | Guest-visible reasons | **Yes, from templates, where the channel supports them** | 2.2 A stands |
| 10 | Weather signal | **Yes, a commercial weather API, and its cost** | 3.10 stands; the adapter is in Block B |
| 11 | Staffing | **Start with the minuted team.** If the pace does not meet Block B, we recommend the second back-end engineer at that point; risk and recommendation are the work that would move. **Updated 30 September:** a second AI engineer from 5 October, no third (six-month plan, decision 11) | Section 7: the trained model producers are what slips first; everything with a baseline ships in the six months |
| 12 | Which AI ships in six months (30 September, AI-D17) | **Every AI function inside the six months, baseline first, then it learns per tenant.** Rules and starting patterns answer on day one; the tenant's own data takes over as it accumulates | Every suggestion carries its maturity stage (`Suggestion.maturity`); the minimums per kind are where own data takes over, not a refusal |
| 13 | Model fitness scoring (30 September, AI-D18, our proposal) | **A task-fitness band per model and agent task; warn, never block** | `AiModel.taskFitness`; `setAiProvider` returns `fitnessWarnings` (underpowered, overpowered, unscored); ADM-037 shows them |
| 14 | Second AI engineer (30 September, AI-D19) | **From 5 October; no third** | As decision 11: trained model producers slip first |
| 15 | Billing for a client-chosen provider or model (30 September client meeting, MoM 4.1, AI-D20) | **Deferred, not decided: to the dedicated AI workshop** (Allam). Position stated on the call, for the workshop to confirm: the agents behave the same whichever model a client selects (minor performance variation only); we propose a recommended model per function; any extra cost of a provider or model the client chooses (for example ChatGPT) is borne by the client | None yet. Decision 2 (managed Azure OpenAI, re-billed per token) stays the default until the workshop; the per-function recommendation fits decision 13's fitness bands, and BYOK (5.9) is the existing route for a client's own provider |

**The trade-offs in section 5 were reviewed at the same time.** All were accepted, with these additions:

- **5.7, staff questions.** The question "could it fetch from the vector store?" has a split answer, and it is already how flow E works: a question about *knowledge* (policies, how-to, documents) is answered from the vector store; a question about *live numbers* (revenue, attendance) is answered from the semantic layer, because the vector store holds text, not the ledger. A mixed question does both. The rule is that a number in an answer can only come from a query result, never from a document chunk.
- **5.9, BYOK.** Bring-your-own-key is available, and **TICVAI decides whether to enable it for a tenant** (`PLATFORM_AI_MANAGE`). It is not tenant self-service. Once enabled, the tenant supplies its key per task or for everything, and we meter for visibility only.
- **5.10, LLM-based reports.** Some reports and narratives will be LLM-written. **The model never works on the data directly.** Either the figures are computed first and bound into the text as placeholders, with personal data scrubbed before any model sees the inputs, or the model writes the query or code and the platform executes it deterministically. This is the same rule as 5.7 applied to AIP-186 and AIP-187 when they are built.
- **3.12, promotion.** A shadow model that passes its gate raises an alert to the admin. Nothing switches itself.

**Memory rule (added to 3.9).** Conversations, decision records and activity older than the retention window are not read at question time. As they age, AI writes compact metadata (a summary, the entities and outcomes, an embedding) that stays under the audit period, so a later question is answered from the index. This keeps answers accurate without keeping prompt text, and it is what makes a longer retention affordable and a shorter one safe: the index outlives the raw text either way. The index itself follows the decision-record period.

**Remaining, ours:** confirm the models on offer in UAE North against the task list in 3.3 (an Azure fact, not a client question); set the markup figure in the module listing; price the weather API.

**ADR changes this implies:**

| ADR | Change |
|---|---|
| **ADR-0020** Proposed → **Accepted, with corrections** | §1: vectors in the tenant database (pgvector), not "Qdrant per cell". §3: "the analytical store" is the writable per-tenant AI log database, not the reporting replica. Consequences: "a cell without Qdrant has no AI" becomes "a tenant without the AI entitlement has no AI"; cost is per tenant, not per cell. The lineage rule is extended to the new AI-owned tables. The CF-61 table is unchanged |
| **ADR-0021** Proposed → **Superseded in part** | By the new ADR-0049. The retrieval client rule, one table per model, shadow re-embed and the two-stage evaluation survive. The shard design becomes the scale-out path |
| **ADR-0009** (Accepted) **amended** | §2: pgvector is the default on every tier. Qdrant only past the section 6 trigger |
| **ADR-0034** (Accepted) **amended** | BYOK is an override, not the default (M21). `ceilingBehaviour` per capability. Semantic cache barred from live-number answers. Cache keys carry the policy version |
| **ADR-0046** | No change. On-premise needs no vector service |
| New **ADR-0049** | Vectors live in the tenant database |
| New **ADR-0050** | One autonomy scale; the approval tier is not an autonomy level |
| New **ADR-0051** | Capabilities now, models on evidence (rules-first promotion gates) |
| New **ADR-0052** | One recommendation engine; runtime in AI, configuration in Promotions |
| New **ADR-0053** | Risk layer ownership: owners keep deterministic rules, AI owns cross-entity risk, alerts and cases |
| New **ADR-0054** | Natural-language analytics goes through the semantic layer |

---

## 9. Coverage

| Requirement ids | Covered in |
|---|---|
| AIC-001..004 | 5.1, 7 |
| AIC-005..031 | 3.3, 3.5, 5.9 |
| AIC-032..045 | 1.3, 3.3, 5.8, 8 |
| AIC-046..068 | 2.4, 3.1, 3.6, 5.8 |
| AIC-069..080 | 2.2 E, 3.3, 5.6, 5.10 |
| AIC-081..085 | 2.2 E, 5.7 |
| AIC-086..107 | 2.2 D, 3.8 |
| AIC-108..142 | 2.2 D, 3.8 |
| AIC-143..171 | 3.8, 5.5 |
| AIC-172..192 | 2.2 D, 3.8, 3.9 |
| AIC-193..209 | 3.9 |
| AIC-210..223 | 4.4, 3.1 (monitoring tables) |
| AIC-224..240 | 3.3, 3.6, 4.5, 5.9 |
| AIC-241..253 | 3.7, 4 |
| AIC-254..260 | 3.5 |
| AIC-261..271 | 3.1, 4.2, 5.8 |
| AIP-001..079 | 2.2 C, 3.4, 3.10, 5.2 |
| AIP-080..095 | 3.10, 4.4 |
| AIP-096..165 | 2.2 B, 3.10, 5.3 |
| AIP-166..198 | 2.2 E, 3.1 (insights), 5.7 |
| AIP-199..219 | 3.4, 3.9, 5.6 |
| AIR-001..101 | 2.2 A, 3.5, 3.10, 5.4 |
| AIR-102..123 | 2.2 A, 3.4 |
| AIR-124..156 | 2.2 A, 3.10, 5.4 |
| AIR-157..179 | 2.2 D, 3.8 |
| AIR-180..192 | 3.3, 3.4, 4.2 |
| AIR-193..202 | 3.9, 5.6 |
| AIR-203..211 | 1.2, 2.2 A, 3.7 |

**Deliberately excluded or deferred, with the reason:**

| Id | Treatment | Reason |
|---|---|---|
| AIC-046 (external enterprise sources) | Deferred | SharePoint and Drive connectors raise residency questions no source answers |
| AIC-063, AIC-064 (Qdrant shard, Qdrant retrieval client) | Met differently | Database-per-tenant plus RLS (5.8); the client rule is kept |
| AIC-045 (DESC for Qdrant) | Moot for Qdrant | pgvector sits in the already-approved Postgres; DESC still applies to Redis and Blob |
| AIC-091 (autonomous agents per function) | Partial | Agents are assistant profiles with tool allow-lists; no autonomous multi-agent planning in the first release |
| AIC-012 (model fitness check) | Partial | A warning on feature mismatch now; scored fitness later |
| AIP-071, AIR-091, AIR-090 level 3 (AI-initiated operational changes, auto-optimisation) | Deferred | L4 stays off until six months of L3 evidence (5.5) |
| AIP-075 (deferred and recognised revenue forecasts) | Excluded | Accounting measures belong to Finance (AIP-016). Cash collection, refunds and settlement stay in scope |
| AIP-095 (suspicious reporting behaviour) | Moved | A security-monitoring rule for the SIEM (AIC-223), not an AI detector |
| AIP-186, AIP-187 (AI dashboard and report generation) | Deferred | Needs the semantic layer proven by NL analytics first |
| AIR-136 (partner and external cross-sell) | Deferred | Needs live sellability integrations that do not exist |
| AIR-189 (location and zone triggers) | Deferred | In-venue location signals are not governed yet |
| AIR-052 third-party channels (OTA, reseller) | Excluded from first release | Pending client decision 8 |
| Guest itinerary planning | **Superseded 29 September** | Now Block A (MOB-6): the rules planner in `venue-map` and the AI planner agent (`requestSuggestion` kind `itinerary`) |
