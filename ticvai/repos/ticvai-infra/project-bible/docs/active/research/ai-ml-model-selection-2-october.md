# TICVAI: AI and ML model selection per task

**Date:** 2 October 2026 · **For:** Chinmay Parab (lead) · **Status:** research, for decision. Nothing in the package has been changed.

> **The cited input (copied into git 2 October 2026, CHG-DOC-001).** Chinmay decided on this research the same day:
> the per-tenant AI residency class from section 2A (ADR-0009 amendment), the curated model range per task
> (AI-D21), BYOK mapped per task (AI-D20 closed), curation that blocks (AI-D18 amended), and mandatory offline PII
> scrubbing and a guard model (ADR-0020 amendment). The decisions are in `docs/registers/decisions-2-october.md`;
> the workbook beside this file is `ai-ml-model-selection-2-october.xlsx`. The text below is the research as delivered.

**Question (Chinmay, 2 October):** TICVAI curates the models for each AI and ML task. Clients do not pick models,
because a cheaper model could break the function. When a client brings its own key (BYOK), the agent maps each task to
that provider's equivalent model. *"It's not just AI models, ML models as well: forecasting, analysis and whatnot. Find
the best one suited for each task, and where applicable 3–4 more for each one."*

**Read from the package:** `docs/active/ai-functions-review-30-september.json` (22 capabilities),
`contracts/satellite/ai.yaml` (`SuggestionKind` 17 kinds, `AiCapability` chat/embedding/vision/rerank/speechToText/textToSpeech,
`AiProviderKind`, 141 operations), `docs/architecture/ai-system-design.md` (3.3 serving and agents, 3.10 engines,
3.13 baseline-then-learn, 4.5 cost), ADR-0009, 0034, 0046, 0051, 0052, 0054, 0059 (0020, 0021, 0049 as the design summarises them), the
design notes `handoff/design-notes/ai.yaml`, and `arabic-embed-eval/` (the August embedding benchmark: harness built,
only a failed smoke run, so **no Arabic retrieval number exists yet**).

**Web facts:** checked on 2 October 2026 and cited per row (section "Sources"). Prices are list prices in USD and change
often. Anything not confirmed on a primary page is marked **UNCONFIRMED**.

---

## The short answer

1. **Residency comes first, and it changes the plan.** Azure UAE North serves **no chat model in-region on pay-per-token**.
   It offers only Global Standard, where prompts may leave the UAE, or **Regional PTU**, which starts at about $8.5k a
   month. UAE apps get around this in one of three ways, as section 2A shows. Government and banks use G42/Core42's
   sovereign wrapper (Abu Dhabi's TAMM, FAB). Others use OpenAI's new UAE regional processing. Consumer apps, including
   our closest peer Miral, make no residency claim at all. **Recommended:** **Core42 Compass** (pay-per-token, in the UAE,
   OpenAI-compatible) for UAE-only tenants, with **OpenAI UAE** as the in-UAE fallback. Move to **Azure PTU** at scale,
   use **self-hosted open models** on-prem, and allow **Global** endpoints only for onshore private tenants that opt in
   under PDPL Art. 23. This would amend AI-D02 and is Chinmay's decision.
2. **Generative tasks run on curated tiers of one provider.** The default is Azure OpenAI (AI-D02). *Small* is
   `gpt-5-mini`, used for guest answers, wording, translation drafts, narratives and extraction. *Strong* is `gpt-6-sol`,
   used for analytics query specs, configuration plans, case summaries, plan reading and escalations. *Reasoning* is
   `o4-mini`, used only if a golden set shows the Strong tier fails. Both main picks are on the UAE North PTU list, so
   they survive a move to in-UAE processing. Arabic quality has no public Gulf benchmark for any of them, so the golden
   sets decide. For private and on-prem tenants the open-weight equivalents are Qwen3.5, Falcon-H1 Arabic and Jais 2.
3. **BYOK maps tiers, not model names** (section 2.3). The map is OpenAI gpt-6-luna/6.1-sol/6-astra, Anthropic
   haiku-4-5/sonnet-5-5/opus-5-5, Gemini 3.5-flash-lite/3.8-flash, and Mistral Small 4/Medium 3.5. No BYOK provider
   except OpenAI (gpt-5.2 only) offers inference in the UAE, so every other BYOK enablement is a cross-border transfer
   under ADR-0009 §3.
4. **Embeddings, reranking, moderation, PII masking, OCR and speech are platform-owned and never BYOK.** Changing an
   embedding model means re-embedding every tenant's Qdrant collection (ADR-0021), and masking must fail closed
   (ADR-0020). Newer open models beat the current picks at the same size and licence: Qwen3-Embedding-0.6B over BGE-M3
   and Qwen3-Reranker-0.6B over bge-reranker-v2-m3. The Arabic embedding eval (A-05) has still never produced a number.
5. **Every money path stays classical ML** (design 5.10). The learned producers are per-tenant LightGBM models: quantile
   models for forecasts and waits, Tweedie for F&B, a classifier for fraud and LambdaRank for upsell. The statistical
   producers are statsforecast-style smoothing and robust baselines; pricing is a hierarchical Bayesian elasticity model.
   **Chronos-2** (Apache 2.0, #1 on fev-bench) is the strongest new option for cold-start forecasts and should join the
   S6 backtest as a challenger.
6. **The 2 October decision overturns AI-D18.** AI-D18 says a model outside its fitness band "warns, never blocks". Under
   curation, `setAiProvider` should **refuse** a model that is not in the curated map. That is a contract change for the
   package owner (section 4).

## 1. Summary: one row per task

| # | Task | Type | Recommended | Alternatives | Avoid | Why the pick | Cost note | Residency / on-prem | Baseline it replaces (ADR-0051) |
|---|---|---|---|---|---|---|---|---|---|
| T01 | Guest concierge (Sahli), support chatbot and staff assistant | LLM chat + retrieval (RAG) | **Azure OpenAI gpt-5-mini (Small tier), cascade to the Strong tier** | Azure OpenAI gpt-6-luna; Self-hosted Qwen3.5-35B-A3B (or Qwen3.5-27B) on vLLM; Self-hosted Falcon-H1 Arabic 34B; Self-hosted Jais 2 70B Chat | — | Small tier answers grounded questions fast; cascade to Strong only on a checkable signal; Arabic quality set by the golden set | gpt-5-mini about $1.58 per 1k calls; cascade + semantic cache cut this further | Global Standard or regional PTU (gpt-5-mini is on the UAE North PTU list); self-hosted open model for on-prem | No ML baseline: the rules floor is search-only or "a person will help" (design 3.3 degraded mode) |
| T02 | Help me choose (question and answer wording) | LLM short generation, structured output | **Azure OpenAI gpt-5-mini** | Azure OpenAI gpt-5-nano; Azure OpenAI gpt-6-luna; Self-hosted Jais 2 8B Chat | — | Short, low-risk wording in the tenant's languages; any small model passes, so pick the cheapest that passes Arabic review | Pennies: one short call per suggestion (design 3.11) | No personal data in the prompt (catalogue attributes only), so Global processing is lowest-risk here | Attribute names used as-is (the rules alone make a usable draft) |
| T03 | Translations (proposeTranslations), EN/AR and other locales | LLM translation with tenant glossary / machine translation | **Azure OpenAI gpt-5-mini with the tenant glossary in the prompt** | Azure AI Translator (standard) / Custom Translator; Azure OpenAI gpt-6-sol (Strong tier); Self-hosted Jais 2 70B or Qwen3.5-122B-A10B | — | An LLM with the tenant glossary keeps brand terms and register; marked AI draft until a person saves | gpt-5-mini about $0.002 per short string; Azure Translator $10 per 1M characters | Azure Translator lists no Middle East endpoint (Custom Translator lists UAE North); LLM path as T01 | Blank field marked missing (no draft) |
| T04 | Guest planner agent (Plan tab, itinerary refine) | Optimisation + LLM (tool calling) | **OR-Tools CP-SAT (time-window routing) + Azure OpenAI gpt-5-mini for intent and rationale** | Greedy / insertion heuristic + gpt-5-mini; Azure OpenAI gpt-6-sol plans end-to-end with tool calls; Self-hosted Qwen3.5-35B-A3B (tool calling) + CP-SAT | — | The schedule is an optimisation problem: solve it deterministically, let the small LLM read intent and write the why | Solver: CPU only; LLM about $1.58 per 1k turns | Solver in-cell; LLM as T01 | The rules-based Plan tab (show times, configured capacity) |
| T05 | Configuration assistant (discovery, blueprint, build plan) | LLM extraction + planning (structured output, tool calls) | **Azure OpenAI gpt-6-sol for config.plan; gpt-5-mini for config.extract** | Azure OpenAI gpt-5.1; Azure OpenAI o4-mini (reasoning); Self-hosted Qwen3.5-397B-A17B or Mistral Medium 3.5 | — | Planning across 15+ tool operations is where small models fail; Strong tier for the plan, Small for extraction | About 50 turns per large tenant per day (design 4.1): about $0.50/day on the Strong tier | Prompts carry configuration, not guests: lowest residency risk of the chat tasks | None needed: full function on day one; validate-only calls in owning services check every step |
| T06 | Analytics NL to semantic query spec (Ask TICVAI, askReportingQuestion) | LLM structured output (semantic spec), deterministic compile | **Azure OpenAI gpt-6-sol, strict JSON schema of the semantic spec** | Azure OpenAI gpt-5-mini with cascade to gpt-6-sol on schema failure; Azure OpenAI gpt-5.1; Self-hosted Qwen3.5-122B-A10B | — | Mapping a question to metric, dimensions, filters and period needs the Strong tier's schema adherence; numbers come from the query, never the model | About 300 questions per large tenant per day: about $3/day on gpt-6-sol | Prompt holds the semantic model and the question, no rows | Saved reports and KPI views; free-text box behind a flag until S7 |
| T07 | Metric explanation and insight narratives (explainMetricChange, insights, summaries) | LLM wording over computed figures | **Azure OpenAI gpt-5-mini, figures as placeholders** | Azure OpenAI gpt-6-sol; Templates only; Self-hosted Qwen3.5-27B | — | The hard part is arithmetic, done first; wording is a Small-tier job | About 200 narratives per large tenant per day: about $0.30/day | Aggregates only, personal data scrubbed before the model (5.10) | Templated sentence over the decomposition table |
| T08 | Marketing content drafts (proposeMarketingContent) | LLM generation | **Azure OpenAI gpt-5-mini** | Azure OpenAI gpt-6-sol; Self-hosted Jais 2 70B Chat; Self-hosted Falcon-H1 Arabic 34B | — | Short promotional copy in EN/AR; small model with brand voice in the cached prefix | about $1.58 per 1k drafts | Segment attributes only, no recipient data in the prompt | Campaign templates |
| T09 | Risk case summaries (case.summarise) | LLM summarisation over case evidence | **Azure OpenAI gpt-6-sol** | Azure OpenAI gpt-5.1; Azure OpenAI gpt-5-mini; Self-hosted Qwen3.5-122B-A10B | — | Evidence is long and mixed; the Strong tier keeps facts straight; card data never reaches a model (AIC-039) | Low volume: cents per case | Masked evidence only (tokens, derived signals) | Structured case timeline without prose |
| T10 | Embeddings for RAG and the semantic cache | Embedding model (multilingual incl. Arabic) | **Qwen3-Embedding-0.6B (to confirm by A-05; BGE-M3 stays until then)** | BGE-M3 (current default); Microsoft harrier-oss-v1-0.6b (27b for GPU); IBM granite-embedding-311m-multilingual-r2; Azure OpenAI text-embedding-3-large | jina-embeddings-v3/v4/v5 | Qwen3-Embedding-0.6B beats BGE-M3 on multilingual retrieval at the same size and licence; BGE-M3 stays default until the Arabic eval confirms | Self-hosted on CPU: marginal cost is CPU (2 x 4 vCPU embedding nodes per region, design 4.1) | In-cell (UAE North or on-prem) by construction | Keyword search (degraded mode) |
| T11 | Reranking (two-stage retrieval) | Cross-encoder reranker | **Qwen3-Reranker-0.6B** | bge-reranker-v2-m3 (current plan); Qwen3-Reranker-4B; gte-multilingual-reranker-base; Cohere rerank-v4.0-fast (Azure Foundry) | jina-reranker-v2/v3/m0 | Qwen3-Reranker-0.6B scores 8 points above bge-reranker-v2-m3 on multilingual reranking at the same size and licence | Self-hosted CPU; latency per query on CPU to be measured | In-cell | Vector order only |
| T12 | Moderation and prompt-injection guard | Safety classifier | **Qwen3Guard-Gen-4B (Qwen3Guard-Stream for streamed answers)** | Azure AI Content Safety + Prompt Shields; gpt-oss-safeguard-20b; OpenAI omni-moderation-latest | Llama Guard 4 / Prompt Guard 2 | Qwen3Guard is the only open guard model that states Arabic coverage; Azure Content Safety's harm models were not trained on Arabic | Self-hosted 0.6B/4B: CPU or small GPU; Azure Content Safety $0.375 per 1k text records | In-cell (Qwen3Guard); Azure Content Safety and Prompt Shields are in UAE North | Rules and blocklists in ai.policy |
| T13 | PII detection and masking (maskedFields, fail closed) | Deterministic recognisers + NER | **Schema field masking + Microsoft Presidio with custom UAE/Arabic recognisers** | Azure AI Language PII; Qwen3Guard PII category (second check); Arabic GLiNER variants (NAMAA-Space gliner_arabic) | — | Most PII arrives in known fields; free-text PII (a guest typing a phone number) needs recognisers that know UAE formats and Arabic names | Self-hosted: CPU | In-cell | Field-level masking from the schema (data classification) — the primary control |
| T14 | OCR and document verification (accreditation documents, guest ID) | OCR / document AI + deterministic checks; a person decides | **Azure AI Document Intelligence v4 (prebuilt-idDocument, Read, Layout) + MRZ check-digit validation** | PaddleOCR PP-OCRv5 Arabic + PaddleOCR-VL-0.9B; NFC eMRTD chip read (ICAO 9303, JMRTD / nMRTD); Mistral OCR 3; Qwen3-VL-8B | AWS Textract; Google Document AI identity parser | Azure Document Intelligence reads printed and handwritten Arabic and has an ID model; the AI pre-fills and flags, a reviewer decides | Read $1.50, prebuilt ID/Layout $10 per 1k pages (UAE North meters) | Azure AI services in UAE North (meters exist; in-region processing to confirm); PaddleOCR on-prem | Manual review queue (method manualReview) |
| T15 | Seat-map and venue-layout generation (generateVenueLayout, proposeSeatMapChanges, proposeVenueLabels, proposeWalkways) | Vector parsing + vision LLM + rules validation | **Vector extraction (DXF/SVG/PDF) + Azure OpenAI gpt-6-sol vision for sections and labels + rules validation** | Azure Document Intelligence Layout (text and labels on raster plans); Qwen3-VL (8B–32B); Classical CV (OpenCV symbol detection) on raster plans | — | Parse the drawing's vectors where they exist; a vision model only labels and groups, and rules check the geometry | A few Strong-tier vision calls per plan: cents per plan | Venue plans are not personal data; Global processing is low-risk | Manual drawing in the seat-map editor |
| T16 | Speech: speech-to-text and text-to-speech (if voice is enabled) | ASR / TTS | **Azure AI Speech ar-AE (STT) + ar-AE-FatimaNeural / ar-AE-HamdanNeural (TTS)** | Cohere Transcribe Arabic (2B); Deepgram Nova-3 Arabic (ar-AE dialect model); Whisper large-v3; Chatterbox Multilingual (TTS) | — | Azure Speech runs STT and neural TTS inside UAE North with ar-AE voices; Cohere Transcribe Arabic is the best open Gulf ASR | STT $1.00/hour; TTS $15 per 1M characters (UAE North) | Azure Speech: data stays in the resource's region (UAE North) | Text only |
| T17 | Face match (Face Pass gates) | Biometric 1:1 / 1:N (vendor SDK) | **The client's contracted face vendor (adapter normalises scores)** | IDEMIA; NEC NeoFace; Paravision | AWS Rekognition; Azure Face; InsightFace pretrained models | Not TICVAI's to curate: the client names the vendor; if asked for a shortlist, use NIST FRTE leaders with on-prem SDKs | Vendor licence (per camera or per enrolment) | Must be on-prem or in-UAE: no hyperscaler face API is usable in the UAE | QR / card credential at the gate |
| T18 | Attendance, demand and revenue forecasting | Time-series forecasting (probabilistic) | **LightGBM global model per tenant (mlforecast), quantile objectives for P10/P50/P90** | Amazon Chronos-2 (120M; chronos-2-small 28M); Nixtla statsforecast: MSTL / AutoETS with holiday regressors (the statistical producer); Google TimesFM-2.5 (200M); NX-AI TiRex-2 | Prophet; TimesFM-3; Moirai-2 | A global LightGBM per tenant with calendar, Ramadan/Eid, weather, pace and price features is the strongest learned model on retail-like data (M5); Chronos-2 is the best zero-shot challenger | CPU minutes per tenant per night; 30 tenants in about 90 minutes on 4 workers (design 4.1) | In-cell, CPU; same code on-prem | Prior: venue profile x venue-type month curve x UAE calendar x weather, bookings as a floor; then statsforecast-style smoothing shrunk to the prior |
| T19 | F&B demand, prep plan, requisition, replenishment, waste risk, menu engineering | Intermittent-demand forecasting + rules | **LightGBM global model, Tweedie objective, per tenant (mlforecast)** | statsforecast intermittent models (Croston/SBA, TSB, ADIDA, IMAPA); hierarchicalforecast (MinTrace) reconciliation; Chronos-2 for new menu items and new outlets | — | Item-by-outlet sales are sparse and intermittent; a Tweedie-loss LightGBM handles zeros, and the plans themselves stay arithmetic over the forecast | CPU | In-cell, CPU; same code on-prem | Prior covers x menu mix; par minus on-hand plus expected use x lead time; margin-only menu ranking |
| T20 | Queue and wait-time prediction, queue balancing (waitTime, queueBalancing, F&B quoteWaitTime) | Queueing model + quantile regression | **Throughput now-cast + LightGBM quantile regression (P50/P90 wait) per attraction** | Erlang C / Erlang A (M/M/c with abandonment) via pyworkforce; Chronos-2 on the queue-load series; Markov / physics-informed neural queue model | — | The now-cast is arithmetic over measured throughput; the learned part predicts throughput and arrivals with quantiles | CPU, sub-millisecond | In-cell, CPU; same code on-prem | People ahead / configured capacity per hour; then measured throughput |
| T21 | Staffing and operational requirements | Workload conversion + optimisation (no learned model of its own) | **Forecast / measured productivity (shrunk from the default) + OR-Tools CP-SAT for coverage** | Erlang C (pyworkforce) for queue-facing roles; PuLP (CBC/HiGHS) | — | Staff = forecast / productivity, with Erlang C for queue-facing roles and CP-SAT to turn coverage into shifts | CPU | In-cell, CPU; same code on-prem | Forecast demand / standard covers per staff hour (benchmark pack, editable) |
| T22 | Anomaly detection (KPI anomalies, insight lifecycle) | Time-series anomaly detection | **STL decomposition + robust z (median/MAD) per KPI and weekday, plus forecast-residual bands** | Isolation Forest / ECOD (PyOD 3); statsforecast prediction intervals as detectors; Chronos-2 residuals for change points | Salesforce Merlion | On the largest benchmark, simple statistical detectors beat complex ones; forecast residuals from T18 do the rest | CPU | In-cell, CPU; same code on-prem | Configured thresholds per KPI and actual against the forecast's P10 |
| T23 | Fraud and risk scoring (transaction, entity, staff leakage) and approval-request scoring | Supervised classifier on analyst labels + unsupervised + graph features | **LightGBM classifier on analyst-labelled outcomes + graph features (shared device/card/account degree)** | CatBoost; XGBoost; Isolation Forest / ECOD (unlabelled entity baselines); TabPFN v2 (not 2.5/3.5) | — | Gradient-boosted trees remain the state of the art on tabular fraud; LightGBM scores in well under a millisecond in-process | CPU; <5 ms in-process | In-cell, CPU; same code on-prem | Weighted rules + velocity + provider signals from a venue-type strategy template |
| T24 | Recommendations and upsell (one engine, every placement) | Candidate generation + learning-to-rank | **Co-purchase lift / item-kNN (statistical) -> LightGBM LambdaRank (learned)** | implicit ALS / BPR (candidate generation); XGBoost rank:ndcg; Thompson-sampling bandit (in-house) for exploration | LightFM; SASRec/BERT4Rec; two-tower | Co-purchase lift from a few weeks of baskets, then LambdaMART reranking of 50–500 candidates fits the 30 ms budget on CPU | CPU | In-cell, CPU; same code on-prem | Promotions relationship map + business priority; attach-rate priors updated per event |
| T25 | Marketing ML: segmentation, lookalike segments, send time, propensity | Clustering / similarity / Bayesian rates / classifier | **RFM segments + Beta-Binomial send-hour model shrunk to segment + LightGBM propensity (in shadow)** | k-means / Gaussian mixture on RFM and attributes; kNN lookalike on attribute vectors; Logistic regression propensity | — | RFM plus a per-recipient Beta-Binomial open rate shrunk to the segment is the design's shrinkage idea applied to send time | CPU | In-cell, CPU; same code on-prem | Known attributes (member, first-time/returning, party type); channel's typical hour; playbooks |
| T26 | Dynamic pricing suggestions (L2: a person approves) | Demand elasticity + pace rule | **Hierarchical Bayesian log-log elasticity (PyMC / PyMC-Marketing), used inside the pace rule** | Double ML (EconML / DoubleML); Thompson-sampling price tests; LightGBM demand model with price as a feature + simulation | — | Hierarchical Bayesian elasticity pools product -> category -> venue: the same shrinkage idea, and honest with little price variation | CPU (MCMC nightly per tenant) | In-cell, CPU; same code on-prem | Pace above forecast P90 -> step up within the band; below P10 -> suggest a promotion |

Legend for the summary: **Type** says what kind of model it is. **Baseline** is the ADR-0051 day-one producer (or the
degraded mode for generative tasks) that the recommended model must beat or sit behind. Every option, with its reason,
cost and sources, is in section 3 and in the workbook (one row per task x option).

---

## 2. The residency fact, the tiers and the BYOK map

### 2.1 Azure UAE North does not serve any chat model in-region on pay-per-token

This is the single most important finding. The design assumes *"Default LLM: Azure OpenAI in UAE North"* (design 3.3),
*"every store and default model endpoint in UAE North"* (1.2), and ADR-0009 keeps *inference* in-jurisdiction by default.
Microsoft's region table (S01, updated 4 Sep 2026) says, for `uaenorth`:

| Deployment type | What runs in UAE North | Where prompts are processed |
|---|---|---|
| **Standard (regional)** | Only `text-embedding-3-large/small`, `ada-002` and `whisper`. **No chat or reasoning model.** | In UAE North |
| **Global Standard** | Almost everything: gpt-5/5-mini/5-nano, gpt-5.1–5.5, gpt-6-astra/sol/luna, o3, o4-mini, gpt-4.1 family, Mistral, Llama 4, DeepSeek, Cohere rerank (S01, S03) | "Might be processed in any Azure region where the model is deployed" |
| **Data Zone** | Not available: there is **no Middle East data zone** | — |
| **Regional Provisioned (PTU)** | gpt-4.1, gpt-4o, **gpt-5-mini, gpt-5.1, gpt-6-sol**, o1, o3-mini, o4-mini | In UAE North |

So there are four ways to run the chat tiers, and only B, C and D keep the design's residency promise:

| Option | In-UAE? | Cost basis (list, 2 Oct 2026) | Fit |
|---|---|---|---|
| **A. Global Standard** from a UAE North resource | No: data at rest in UAE, processing anywhere | Tokens. At the design's regional ceiling (150,000 calls/day, 80% Small / 20% Strong) about **$15k/month** before caching | Needs an ADR-0009 §3 transfer mechanism per tenant; contradicts AI-D03 ("UAE North for now", no cross-border route in the first release) |
| **B. Regional Provisioned (PTU)** | Yes | **$2.36 per PTU-hour** in UAE North (S04), about $1,723 per PTU per month. Minimum deployment size and tokens per PTU for these models: **UNCONFIRMED**; every 10 PTU is about $17k/month | Matches ADR-0009 and AI-D03 with no code change. Price it in the Azure capacity calculator before 5 October |
| **C. Self-hosted open model** (vLLM on UAE North GPU VMs) | Yes | NC40ads H100 v5 **$9.98/h** (S04): two for HA about $14.6k/month pay-as-you-go | The same stack `onPremiseIsolated` sites need anyway (ADR-0046) and the design's fallback (4.3). Arabic: Qwen3.5, Falcon-H1 Arabic, Jais 2 |
| **D. OpenAI direct, UAE inference residency** | Yes | **gpt-5.2 only**; API eligibility UNCONFIRMED (reported for Enterprise/Edu); 10% regional surcharge on newer models | Only with a TICVAI OpenAI contract; not the managed Azure default |

**Recommendation: see section 2A.** After Chinmay's question (*"how do UAE apps do it?"*), the routes were widened beyond
Azure. There are two pay-per-token routes with inference inside the UAE: **Core42 Compass** (UAE-region models, billed
through Azure Marketplace) and **OpenAI's API with UAE regional processing**. Section 2A recommends Compass for UAE-only
tenants now, OpenAI UAE as the in-UAE fallback, Azure regional PTU as the scale step, self-hosted open models on-prem, and
Global endpoints only for onshore private tenants that opt in. The model names per task (section 3) are the Azure tier
models. Each route serves its listed equivalent of the tier.

### 2.2 Tiers: what the curated catalogue holds

| Tier | Used by | TICVAI default (Azure) | Why this model |
|---|---|---|---|
| **Small** | T01, T02, T03, T07, T08, T04 (intent/rationale), extraction in T05 | `gpt-5-mini` | On the UAE North PTU list (so it survives option B), $0.25 / $2.00 per 1M Global |
| **Strong** | T05 plan, T06, T09, T15, T03 legal text, escalations | `gpt-6-sol` | Current mid/flagship model on the UAE North PTU list; OpenAI list $2 / $10 (Azure meter not checked) |
| **Reasoning** | T05 build plans, only if the golden set shows Strong under the 90% plan-validity gate | `o4-mini` (PTU list) or `gpt-6-sol` at high effort | Escalation only |
| **Fallback** | Every chat task when the breaker opens (design 3.3, 4.3) | `gpt-5.1` (PTU list) then the in-cell open model | A second in-UAE deployment, then the design's in-cell hop (4.3) |

Platform-owned and never BYOK: embeddings (T10), reranking (T11), moderation (T12), PII masking (T13), OCR (T14), speech
(T16) and every classical model (T18–T26).

### 2.3 BYOK equivalence map

When TICVAI enables BYOK for a tenant (`setAiByokEnablement`, AI-D14), the agent maps each **tier** to that provider's
curated equivalent. The tenant supplies a key, never a model name. Prices are per 1M input / output tokens, list, 2 October 2026.
"Cost per 1k calls" uses the design's average call (3,500 input, 350 output tokens).

| Tier / capability | TICVAI default (Azure OpenAI, UAE North) | OpenAI | Anthropic | Google Gemini | Mistral | OpenAI-compatible / self-hosted (private, on-prem) |
|---|---|---|---|---|---|---|
| Small chat (T01, T02, T03, T07, T08, T04 LLM part) | gpt-5-mini ($0.25 / $2.00; ~$1.58 per 1k calls) | gpt-6-luna ($0.10 / $0.50; ~$0.53 per 1k) | claude-haiku-4-5 ($1 / $5; ~$5.25 per 1k) | gemini-3.5-flash-lite ($0.30 / $2.50; ~$1.93 per 1k) | Mistral Small 4 ($0.15 / $0.60; ~$0.74 per 1k) | Qwen3.5-35B-A3B; Arabic-only wording: Jais 2 8B |
| Strong chat (T05 plan, T06, T09, T15, escalations) | gpt-6-sol (OpenAI list $2 / $10; ~$10.50 per 1k) | gpt-6.1-sol ($2 / $10; ~$10.50 per 1k) | claude-sonnet-5-5 ($2 / $10; ~$10.50 per 1k) | gemini-3.8-flash ($0.75 / $3.75 to 31 Dec 2026, then $1.50 / $7.50; ~$3.94 per 1k now) | Mistral Medium 3.5 ($1.50 / $7.50; ~$7.88 per 1k) | Qwen3.5-122B-A10B; Arabic-heavy: Jais 2 70B or Falcon-H1 Arabic 34B |
| Reasoning (T05 build plans, only if needed) | o4-mini ($1.10 / $4.40) or gpt-6-sol at high effort | gpt-6-astra ($10 / $50; ~$52.50 per 1k) | claude-opus-5-5 ($4 / $20; ~$21 per 1k) | gemini-3.8-flash, high thinking (3.1 Pro is preview: not curated) | Mistral Medium 3.5 | Qwen3.5-397B-A17B |
| Vision (T15 plans; T14 hard scans) | gpt-6-sol (vision quality on plans UNCONFIRMED) | gpt-6-sol | claude-sonnet-5-5 | gemini-3.8-flash | Mistral Medium 3.5 (vision UNCONFIRMED) | Qwen3-VL |
| Speech (T16): platform-owned, not mapped | Azure AI Speech ar-AE (in UAE North) | Not BYOK (gpt-transcribe and gpt-4o-mini-tts exist but run outside the UAE) | Not BYOK (no speech model) | Not BYOK (Chirp 3 serves ar-AE only from the eu region) | Not BYOK | On-prem: Cohere Transcribe Arabic (STT), Chatterbox (TTS) |
| Embeddings, reranking, moderation, PII, OCR (T10–T14) | Platform-owned, self-hosted in-cell | Not BYOK | Not BYOK | Not BYOK | Not BYOK | Not BYOK |
| Classical ML (T18–T26) | Platform-owned, in-process | Not BYOK | Not BYOK | Not BYOK | Not BYOK | Not BYOK |
| Where processing happens | Option A Global, B regional PTU or C self-hosted (section 2.1) | Outside UAE, except UAE inference residency for gpt-5.2 only (API eligibility UNCONFIRMED) | Outside UAE: first-party geo is us/global; Bedrock me-central-1 only via global cross-region; Foundry Global or US data zone | Outside UAE: no Gemini text model in any Middle East region (Doha, Dammam, Tel Aviv serve embeddings only) | Outside UAE (open weights can be self-hosted instead) | In UAE North or on the client's site |
| Contract fit (AiProviderKind) | azureOpenai | openai | anthropic | gemini | No `mistral` kind: needs an adapter or `openaiCompatible` (compatibility UNCONFIRMED) | localLlm / openaiCompatible |
| Sources | S01, S04 | S15, S16, S17 | S19, S20, S14 | S21, S22 | S23 | S24, S25, S26, S48, S49, S52 |

### 2.4 Mapping rules

1. **A task binds to a tier, and a tier to one curated model per provider.** The tenant chooses a provider; the map
   chooses the model. A model not in the map is refused (see section 4, the AI-D18 change).
2. **A model enters the map only after it passes the task's golden set** at or above the TICVAI default's band
   (`runAiEvaluation` -> `AiModel.taskFitness`; Arabic, English and code-mixed cases; isolation cases at 100%). The
   concierge is evaluated per task, not per tier, because Arabic quality varies most there.
3. **No preview models.** Gemini 3.1 Pro is preview only, so Google's Reasoning cell uses Gemini 3.8 Flash.
4. **No equivalent means no down-tiering.** If a provider has no model that passes a tier (Anthropic has no speech model,
   for example), that task stays on the TICVAI-managed default (metered) or stays off. It never drops to a cheaper tier.
5. **Residency is checked before enablement.** Only TICVAI's own options B/C, and OpenAI's gpt-5.2 UAE residency, keep
   processing in the UAE. Every other BYOK provider is a cross-border transfer: record the ADR-0009 §3 mechanism first.
   `residencyRefused` is never failed over (ADR-0034).
6. **Re-check monthly.** Models are retired (Mistral Saba, 30 Sep 2025) and repriced (Gemini 3.6–3.8 Flash double on
   1 Jan 2027). A retirement or a price change triggers re-evaluation of the mapped cell, not a silent swap.

---

## 2A. How UAE apps do it (added 2 October, after Chinmay's question)

> *"Check online — there are models running in many apps in the UAE; how do they do that?"*

They do it in one of three ways, and only the first two are true in-country inference:

1. **Through a UAE sovereign wrapper on Azure** (G42/Core42). Abu Dhabi's TAMM assistant runs on Azure OpenAI GPT-4
   and G42's Compass. First Abu Dhabi Bank runs Azure AI behind Core42's sovereign controls. This is the government and
   bank pattern (S117, S118).
2. **Through vendor programmes that began in 2025–2026.** OpenAI's API has offered UAE regional processing on
   `ae.api.openai.com` since August 2026 for a short list of models. Microsoft 365 Copilot in-country processing is
   promised "by the end of 2026", but it covers Copilot, not the Azure OpenAI API (S104, S106, S107).
3. **Without in-country inference at all.** The consumer and leisure apps make no residency claim: Miral's Yas Island park
   chatbots and DEWA's Rammas (both Azure OpenAI), Emirates (ChatGPT Enterprise) and Majid Al Futtaim (Azure AI). They
   rely on Azure's at-rest residency and contracts (S119–S123). **Our closest peer, Miral, is in this group.**

### Where a model can run inside the UAE today (2 October 2026)

| Route | In-UAE inference | Models in the UAE | Pricing / commitment | Minimum | Sign-up | Fit for TICVAI | Sources |
|---|---|---|---|---|---|---|---|
| R1 Core42 Compass (G42), UAE-region models | Yes, stated per model in the changelog | GPT-5, o3, GPT-4.1 mini, GPT-4.1 Arabic (Seraj), gpt-oss-20b/120b, K2 Think / K2 Horizon 375B, DeepSeek V4 Pro, GLM-5.2. NOT in UAE: GPT-5.5/5.6 (Sweden Central), Claude Opus 4.8 (Global). GPT-5.2 region not stated. Jais 30b retired 1 Apr 2026 | Pay-per-token, e.g. GPT-4.1 mini $0.40 / $1.60, GPT-5.2 $1.75 / $14, gpt-oss-120b $0.15–0.30 / $0.37–0.75, K2 $0.15 / $0.50 per 1M; billed through Azure Marketplace | Not published (UNCONFIRMED) | Subscribe on Azure Marketplace; the Compass team approves (about an hour after approval) | Best pay-per-token fit: OpenAI-compatible API (our `openaiCompatible` kind, no new adapter); used by Abu Dhabi's TAMM. gpt-oss is on Compass in the UAE *and* self-hostable, so cloud and on-prem can run the same model. Get retention, logging and sub-processor terms in writing first | S108, S109, S110, S112, S117 |
| R2 OpenAI API, UAE regional processing (ae.api.openai.com) | Yes for listed models | gpt-5.6-luna, gpt-5.5, gpt-5.5-pro (Responses), gpt-5.2, text-embedding-3-large | Pay-per-token, +10% for models released on or after 5 Mar 2026 | None published | Contact sales: UAE region approval, plus Modified Abuse Monitoring or Zero Data Retention approval and a retention amendment | Strong second in-UAE vendor and fallback; newest OpenAI models; not usable on-prem; outside Azure contracts (AI-D02) | S106, S107, S17 |
| R3 Azure OpenAI, UAE North Regional Provisioned (PTU) | Yes (regional processing in the geography) | gpt-5-mini, gpt-5.1, gpt-6-sol, gpt-4.1, gpt-4o, o4-mini, o3-mini, o1 | $2.36 per PTU-hour; reservation $338 per PTU per month (1-month) or $3,444 per PTU per year | gpt-5-mini / o4-mini: 25 PTU (about $8,450/month, or about $7,175/month on a 1-year term); gpt-6-sol / gpt-5.1 / gpt-4.1: 50 PTU (about $16,900/month) | Self-serve in the Azure portal; capacity not guaranteed by a reservation (create the deployment first) | Keeps AI-D02 and ADR-0009 exactly as written; a fixed cost pooled across tenants. Spillover can only target Global Standard, so it must be off for UAE-only tenants | S01, S101, S102, S103, S134 |
| R4 Self-hosted open weights (Azure UAE North GPU VMs, Core42 AI Cloud, e& sovereign compute, or the client's site) | Yes | Any open model: Qwen3.5, Falcon-H1 Arabic, Jais 2, K2 Horizon, gpt-oss, Llama 4 | GPU-hours: Azure NC40ads H100 v5 $9.98/h; Core42 AI Cloud H100 from $2.50/h (per-GPU-hour basis UNCONFIRMED); e& + Core42 compute price not public | One GPU node per model; two for HA | Azure: self-serve; Core42 AI Cloud: self-serve with vetting; e&: sales | The only route that also serves onPremiseIsolated sites (ADR-0046); TICVAI runs and patches the models. No hosted Jais 2 or Falcon-H1 Arabic API exists | S04, S111, S116, S24, S25 |
| R5 AWS Bedrock me-central-1 (UAE) | Only Amazon Nova Micro / Lite / Pro | Nova Micro, Lite, Pro. Claude and Nova 2 Lite via Global cross-region only; no in-region embeddings; no Llama / gpt-oss | Pay-per-token (UAE price not on the public page; US Nova Pro about $0.80 / $3.20) | None | Self-serve | Weak: one model family, no in-region embeddings, a second cloud to run | S113, S20 |
| R6 Oracle OCI Generative AI, UAE East (Dubai) and UAE Central (Abu Dhabi) | Yes | On-demand: Cohere Command A Vision, Cohere Embed 4. Dedicated clusters only: Command A, Llama 3.3/4, gpt-oss | On-demand per token (Command A about $1.56 per 1M, third-party, UNCONFIRMED); dedicated clusters per unit-hour | 744 unit-hours (one month) per dedicated cluster | Self-serve; also via du National Hypercloud and e& OneCloud (Oracle Alloy) | Weak for chat (one on-demand model); Embed 4 is an in-UAE managed embedding if ever needed | S114, S136 |
| R7 Global endpoints with legal safeguards (Azure Global Standard, OpenAI, Anthropic, Gemini) | No | Everything | Pay-per-token, cheapest and newest | None | Self-serve | What most UAE consumer apps do today (no residency claim). Lawful for onshore private tenants under PDPL Art. 23 with a DPA plus contract-necessity or consent, a DPIA and a notice. Not for government or semi-government, bank or payment, or health-service tenants; DIFC/ADGM only with their SCCs | S126, S127, S133 |
| (Not an API) Microsoft 365 Copilot in-country processing | Copilot prompts only | Copilot | Copilot licence | n/a | Microsoft | Not usable for TICVAI's own features: covers Copilot interactions, not the Azure OpenAI API; UAE date slipped to "by end of 2026" | S104 |

**How UAE organisations run them today** (public, dated sources only):

| Organisation | App | Provider / model | Where it runs | Residency statement | Source |
|---|---|---|---|---|---|
| Abu Dhabi government (DGE) | TAMM AI assistant | Azure OpenAI GPT-4 + G42 Compass 2.0 (Jais and open models) | G42/Core42 sovereign cloud on Azure | "Sovereign cloud"; region not named | S117 |
| First Abu Dhabi Bank | AI Innovation Hub | Azure OpenAI | Azure with Core42 sovereign controls | Core42 sovereign controls for data sovereignty | S118 |
| DEWA | Rammas virtual employee | ChatGPT via Azure OpenAI | Not stated | None | S119 |
| Miral (Yas Island parks: Ferrari World, Yas Waterworld, WB World) | Visitor chatbots | Azure OpenAI (ChatGPT) | Not stated | None | S120 |
| Emirates Group | ChatGPT Enterprise company-wide | OpenAI direct | Not stated (predates UAE inference residency) | None | S121 |
| Majid Al Futtaim | MAFGPT internal platform | Azure AI | Not stated | "Without compromising confidentiality" | S123 |
| Digital Dubai | DubaiAI concierge; LLM-as-a-service for government entities | Not disclosed | Central government-hosted LLMaaS | Follows Digital Dubai standards | S122 |
| flydubai | GenAI for operations and customer experience | AWS | Not stated | None | S125 |
| Dubai Parks and Resorts, DXB, Noon, Expo City | — | Nothing public found | — | — | — |

### What the law asks (summary; not legal advice)

| Who the tenant is | Global processing allowed? | What is needed |
|---|---|---|
| Onshore private company (most venues) under the federal PDPL | **Yes**, under Art. 23: a binding contract (DPA) with the LLM vendor that imposes PDPL-level duties, plus contract-necessity or express consent. Art. 22 adequacy cannot be used: no list has been published | DPA with no training and short or zero retention; transfer risk assessment; DPIA (Art. 21); privacy notice naming AI processing and countries; masking. **Masked prompts are pseudonymised, which is still personal data** (Art. 1) |
| Dubai government or semi-government entity (for example a Dubai Holding company) | **No** in practice: DESC CSP rules require a DESC-certified provider; Dubai government data reportedly may not leave the UAE (exact instrument UNCONFIRMED) | In-UAE route R1–R4 |
| Federal or Abu Dhabi government entity | **No** in practice: classified government data stays on certified in-country cloud (du National Hypercloud, e& + AWS Sovereign Launchpad; S115, S136) | In-UAE route |
| Bank or payment-licensed tenant (CBUAE) | **No**: confidential consumer data may not leave the UAE without CBUAE and consumer consent | In-UAE route |
| Health-service data (Federal Law 2/2019) | **No**, with narrow exceptions | In-UAE route, or keep it out of prompts |
| DIFC tenant | Only with DIFC SCCs (the US is not adequate, California excepted); Regulation 10 notice and register for AI systems | In-UAE is the safer default |
| ADGM tenant | Only with ADGM SCCs or listed safeguards | In-UAE is the safer default |

Context: the PDPL Executive Regulations and penalty schedule have **still not been issued**. A Federal Authority for
Artificial Intelligence and Data was created on 14 June 2026 and absorbs the UAE Data Office, so enforcement is likely to
tighten (S126, S127). Sources for this table: S126, S127, S128, S129, S130, S131, S132.

### Cost at TICVAI's scale: pay-per-token beats PTU until close to the regional ceiling

At the design's average call (3,500 input and 350 output tokens), the Small tier costs **$1.96 per 1,000 calls on Compass
GPT-4.1 mini**, processed in the UAE.

The **minimum Azure PTU for gpt-5-mini** is 25 PTU, about $8,450 a month on a 1-month reservation (S101, S102). Two
numbers matter:
- **Cost break-even.** The same $8,450 buys about 4.3 million Compass calls a month, about **144,000 a day**.
- **Capacity.** 25 PTU serves about 594,000 input-equivalent tokens a minute. One call counts as 3,500 + 8 × 350 = 6,300
  tokens, so 25 PTU handles at most about **136,000 Small calls a day**, even at 100% utilisation around the clock. Cached
  prompt prefixes do not count against capacity, so the real figure is somewhat higher.

Both numbers sit at the design's whole regional ceiling (150,000 calls a day across all tiers, design 4.1). So while TICVAI
has tens of tenants, pay-per-token in the UAE is clearly cheaper. PTU only pays once steady Small-tier traffic is near that
ceiling, and peaks then need more than the minimum. The Strong tier's minimum (50 PTU, about $16,900 a month) does not pay
at its volume.

### Recommendation: a combination, decided per tenant by residency class

| Residency class (set per tenant) | Small tier | Strong tier | Embeddings, rerank, guard | Fallback when the breaker opens |
|---|---|---|---|---|
| **UAE-only** (the default; mandatory for government, semi-government, bank/payment, health and DIFC/ADGM tenants) | **R1 Compass GPT-4.1 mini** (or GPT-4.1 Arabic "Seraj" if it wins the Arabic golden set) | **R1 Compass GPT-5** (UAE region) | Self-hosted in-cell (unchanged) | **R2 OpenAI UAE** (gpt-5.6-luna / gpt-5.5), then **R4** in-cell open model (gpt-oss-120b, the same model Compass serves) |
| **Global allowed** (onshore private tenant that accepts it in writing; PDPL Art. 23 DPA and notice) | Azure gpt-5-mini Global Standard, or the tenant's BYOK provider (section 2.3) | Azure gpt-6-sol Global Standard | Self-hosted in-cell (unchanged) | The UAE-only chain |
| **On-premise** (`onPremiseIsolated` / `onPremiseConnected`) | **R4** Qwen3.5-35B-A3B or gpt-oss-120b | **R4** Qwen3.5-122B-A10B; Falcon-H1 Arabic 34B or Jais 2 70B for Arabic-heavy tenants | Self-hosted (unchanged) | None outside the site |

**Scale step:** when Small-tier traffic in a region stays near 100,000+ calls a day, move the UAE-only Small tier to **R3
Azure UAE North PTU** (25–50 PTU of gpt-5-mini) with spillover disabled. This brings it back onto the default provider in
AI-D02 at a lower unit cost.

**Why not R3 now:** it is the only route that leaves every decision exactly as written, but it costs about $8.5k a month
before the first tenant asks a question, and the Strong tier would add $16.9k.
**Why not R5 or R6:** each offers one in-UAE model family, Arabic quality is unverified, and it adds a second cloud to run.

**What this changes in the package (for Chinmay to decide):**
- **AI-D02** (one managed provider: Azure OpenAI) becomes Core42 Compass for UAE-only tenants. Compass runs on Azure and
  is billed through Azure Marketplace.
- `AiProviderKind` already has `openaiCompatible`, which covers Compass.
- The per-tenant residency class extends the region's `allowedAiResidencies`.
- The ADR-0009 §3 transfer register records the Global-allowed tenants.

**Before signing, get these from the vendors in writing:**
- **Compass:** retention, logging and sub-processor terms; the pay-as-you-go minimum; the in-UAE region per model
  (GPT-5.2's is not stated).
- **OpenAI:** approval of the UAE region and of Modified Abuse Monitoring.
- **Microsoft:** the PTU calculator result for gpt-5-mini at our traffic mix.

---

## 3. Task by task

### T01 Guest concierge (Sahli), support chatbot and staff assistant

**Where it lives:** Guest agent / Operations agent; sendAiMessage, semanticSearch; WEB-044, GST-031..033  
**Type:** LLM chat + retrieval (RAG)  
**Package anchor:** ai-system-design 3.3 (Guest agent: Small), ADR-0034 cascade, ADR-0059 Block A (2.5 AI-weeks)

One assistant runtime with profiles (design 5.10): the guest concierge, the support chatbot and the staff assistant
share the model choice and differ by sources, tools and scope. Streams (TTFT p95 1.5 s, total p95 5 s guest, 8 s staff).
**No public Gulf-Arabic benchmark exists for any of these models** (the August harness found none); the concierge golden set,
with Arabic, English and code-mixed questions, is what decides (design 3.5, groundedness and citation accuracy at least 95%).

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Azure OpenAI gpt-5-mini (Small tier), cascade to the Strong tier** | Managed LLM (default provider) | Current small model Azure sells both as Global Standard and as Regional PTU in UAE North, so the same model survives a move to in-UAE processing. Cheap enough for the highest-volume LLM task. Arabic: no published Gulf score; golden set decides. | $0.25 / $2.00 per 1M (Global, UAE North meter); about $1.58 per 1k calls | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S01, S04 |
| Alternative | **Azure OpenAI gpt-6-luna** | Managed LLM | Newest small OpenAI model, about a third of gpt-5-mini's cost; reasoning effort none to max. Not on the UAE North PTU list, so Global processing only. | OpenAI list $0.10 / $0.50 per 1M; about $0.53 per 1k calls (Azure meter not checked) | Global Standard only in UAE North (S01) | S01, S16 |
| Alternative | **Self-hosted Qwen3.5-35B-A3B (or Qwen3.5-27B) on vLLM** | Open weights, Apache 2.0 | In-UAE by construction on a UAE North GPU VM, and the same model serves onPremiseIsolated sites (ADR-0046). 201 languages incl. Arabic, 262K context. Qwen3 family is the best open model on HELM Arabic. | GPU, not tokens: NC40ads H100 v5 $9.98/h in UAE North (~$7.3k/month per GPU); throughput needs a load test | In UAE North or on the client's site | S26, S27, S04 |
| Alternative | **Self-hosted Falcon-H1 Arabic 34B** | Open weights, TII Falcon licence | Top of the Open Arabic LLM Leaderboard v2 (75.36), 256K context: the strongest Arabic-first open model for a private or on-prem tenant. Licence is Apache-based with a usage policy (legal review). | GPU (as above) | In UAE North or on-prem | S25 |
| Alternative | **Self-hosted Jais 2 70B Chat** | Open weights, Apache 2.0 | UAE-built, Arabic-first incl. dialects and code-switching (AraGen 70.71). 8K context limits long retrieval prompts, so it fits short-context tasks better than RAG. | GPU (2x H100 class for 70B) | In UAE North or on-prem | S24 |

### T02 Help me choose (question and answer wording)

**Where it lives:** Guest agent wording; proposeGuidedChoice (white-label), BO-117  
**Type:** LLM short generation, structured output  
**Package anchor:** ai-system-design 3.11 (rules pick the questions; a model writes the wording; attributes only, never guest data)

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Azure OpenAI gpt-5-mini** | Managed LLM | Same deployment as the concierge (one model to evaluate and monitor); structured output for question/answer/one-liner fields. | about $1.58 per 1k calls at the design average; real calls are shorter | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S01, S04 |
| Alternative | **Azure OpenAI gpt-5-nano** | Managed LLM | Cheapest Azure model; adequate for short wording if Arabic tone passes review. Not on any PTU list. | $0.05 / $0.40 per 1M; about $0.32 per 1k calls | Global Standard only | S01, S04 |
| Alternative | **Azure OpenAI gpt-6-luna** | Managed LLM | Newer small model at a similar price to nano. | OpenAI list $0.10 / $0.50 per 1M | Global Standard only | S16 |
| Alternative | **Self-hosted Jais 2 8B Chat** | Open weights, Apache 2.0 | Arabic-first wording; 8K context is ample for this task; runs on a single A10-class GPU. | GPU (NV-A10 v5 from $0.649/h in UAE North) | In UAE North or on-prem | S24, S04 |

### T03 Translations (proposeTranslations), EN/AR and other locales

**Where it lives:** Marketing agent, content.translate; BO-793  
**Type:** LLM translation with tenant glossary / machine translation  
**Package anchor:** AI functions review: content-translation (S2, Block A); design 3.3 (Marketing: Small)

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Azure OpenAI gpt-5-mini with the tenant glossary in the prompt** | Managed LLM | Glossary-aware, keeps placeholders and markup, handles Gulf register and brand names; the glossary grows from edits (review: week 4). Escalate long legal text to the Strong tier. | about $1.58 per 1k calls (design average) | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S01, S04 |
| Alternative | **Azure AI Translator (standard) / Custom Translator** | Managed MT service | Purpose-built MT, deterministic, cheap at volume; Custom Translator trains on the tenant's approved pairs. Weaker on tone and placeholders than an LLM. Standard endpoints list no Middle East region; in-region processing UNCONFIRMED. | $10 / 1M chars standard; $40 / 1M custom | Custom Translator lists UAE North; standard: UNCONFIRMED | S08, S04 |
| Alternative | **Azure OpenAI gpt-6-sol (Strong tier)** | Managed LLM | For long or legal text (terms, waivers) where a small model drops nuance. | OpenAI list $2 / $10 per 1M; about $10.50 per 1k calls | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S01, S15 |
| Alternative | **Self-hosted Jais 2 70B or Qwen3.5-122B-A10B** | Open weights, Apache 2.0 | In-UAE or on-prem translation for private tenants; Jais for EN<->AR, Qwen for the other locales (201 languages). | GPU | In UAE North or on-prem | S24, S26 |

### T04 Guest planner agent (Plan tab, itinerary refine)

**Where it lives:** Guest agent, planner.guest.refine; requestSuggestion kind itinerary; GST-054  
**Type:** Optimisation + LLM (tool calling)  
**Package anchor:** SuggestionKind itinerary (rules plan is the baseline); ADR-0059 Block A (planner is first to move if behind)

Published evidence supports this split: a Tokyo Disney study combined gradient-boosted wait prediction with route
optimisation and saved 2 h 41 min on an 8-attraction plan (S84). The LLM should never invent a time or an attraction; every
change names a point or performance of that day's venue (MoM 4.7).

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **OR-Tools CP-SAT (time-window routing) + Azure OpenAI gpt-5-mini for intent and rationale** | Solver + managed LLM | CP-SAT handles show times, ride waits (from T20), meals and walking as hard constraints; the LLM turns "we have kids, lunch at 1" into constraints and explains the plan. Deterministic and auditable. | Solver CPU in ms to seconds; LLM about $1.58 per 1k turns | Solver in-cell; LLM as T01 | S86, S84 |
| Alternative | **Greedy / insertion heuristic + gpt-5-mini** | Rules + managed LLM | Simplest; good enough for small parks with few timed shows; the Block A fallback if the solver slips. | Negligible CPU | As above |  |
| Alternative | **Azure OpenAI gpt-6-sol plans end-to-end with tool calls** | Managed LLM | Flexible for odd requests, but plans are not provably feasible and cost about 7x per turn. Use as the escalation, not the planner. | about $10.50 per 1k turns | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S15 |
| Alternative | **Self-hosted Qwen3.5-35B-A3B (tool calling) + CP-SAT** | Open weights + solver | Same split, in-UAE or on-prem. | GPU | In UAE North or on-prem | S26 |

### T05 Configuration assistant (discovery, blueprint, build plan)

**Where it lives:** Operations agent, config.extract (Small) and config.plan (Strong); generateConfiguration, buildConfigurationPlan; ADM-469..498  
**Type:** LLM extraction + planning (structured output, tool calls)  
**Package anchor:** Design 3.3; release gate: plan validation at least 90% on the golden set, zero unsafe steps (3.5); S3-S5

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Azure OpenAI gpt-6-sol for config.plan; gpt-5-mini for config.extract** | Managed LLM | Strong tier is on the UAE North PTU list and Global Standard. Reasoning effort raised for build plans (effort control on sol: UNCONFIRMED; luna and astra document it). Strict schema output into validate-only calls. | OpenAI list $2 / $10 per 1M; about $10.50 per 1k turns (Azure meter not checked) | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S01, S15 |
| Alternative | **Azure OpenAI gpt-5.1** | Managed LLM | Previous Strong-class model, also on the UAE North regional PTU list; fallback deployment. | Azure meter not checked | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S01 |
| Alternative | **Azure OpenAI o4-mini (reasoning)** | Managed LLM | Reasoning model on the regional PTU list; only if the golden set shows gpt-6-sol under 90% plan validity. | OpenAI list $1.10 / $4.40 per 1M; about $5.39 per 1k turns | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S01, S15 |
| Alternative | **Self-hosted Qwen3.5-397B-A17B or Mistral Medium 3.5** | Open weights (Apache 2.0 / modified MIT) | Frontier-class open models for private and on-prem tenants; 397B needs a multi-GPU node. | ND H100 v5 $140.60/h in UAE North; only for dedicated cells | In UAE North or on-prem | S26, S23, S04 |

### T06 Analytics NL to semantic query spec (Ask TICVAI, askReportingQuestion)

**Where it lives:** Finance and analytics agent, analytics.spec; askReportingQuestion; ANL-009/051..056  
**Type:** LLM structured output (semantic spec), deterministic compile  
**Package anchor:** ADR-0054 (the model writes a spec; Reporting compiles it with RLS); AI-D13/D15 (the LLM never reads raw data); S7

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Azure OpenAI gpt-6-sol, strict JSON schema of the semantic spec** | Managed LLM | Strong tier for compositional questions and follow-ups; the spec is validated against the semantic model before Reporting compiles it; out-of-model questions return "not available yet". | about $10.50 per 1k questions | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S01, S15 |
| Alternative | **Azure OpenAI gpt-5-mini with cascade to gpt-6-sol on schema failure** | Managed LLM | Cheaper for simple single-metric questions; escalate when validation fails twice (design 3.3 cascade). | about $1.58 per 1k first-pass calls | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S04 |
| Alternative | **Azure OpenAI gpt-5.1** | Managed LLM | Fallback deployment on the regional PTU list. | Azure meter not checked | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S01 |
| Alternative | **Self-hosted Qwen3.5-122B-A10B** | Open weights, Apache 2.0 | Strong open model for private and on-prem tenants; structured output via vLLM guided decoding. | GPU | In UAE North or on-prem | S26 |

### T07 Metric explanation and insight narratives (explainMetricChange, insights, summaries)

**Where it lives:** Finance and analytics agent, analytics.narrate; explainMetricChange, listAiInsights  
**Type:** LLM wording over computed figures  
**Package anchor:** ADR-0054: decomposition is plain arithmetic; the model only words the result; figures bound as placeholders (5.10)

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Azure OpenAI gpt-5-mini, figures as placeholders** | Managed LLM | Small tier is enough when every number is a bound placeholder; a check rejects any digit the model adds. | about $1.58 per 1k | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S04 |
| Alternative | **Azure OpenAI gpt-6-sol** | Managed LLM | Executive summaries spanning several drivers. | about $10.50 per 1k | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S15 |
| Alternative | **Templates only** | Rules | Zero cost and zero risk; reads mechanically. The fallback when no provider answers. | None | In-cell |  |
| Alternative | **Self-hosted Qwen3.5-27B** | Open weights, Apache 2.0 | On-prem narratives. | GPU | In UAE North or on-prem | S26 |

### T08 Marketing content drafts (proposeMarketingContent)

**Where it lives:** Marketing agent, content.draft  
**Type:** LLM generation  
**Package anchor:** Design 3.3 (Marketing: Small); in the Block A slice

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Azure OpenAI gpt-5-mini** | Managed LLM | Adequate for short copy; tenant tone and banned phrases in the stable, cached prefix (ADR-0034). | about $1.58 per 1k | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S04 |
| Alternative | **Azure OpenAI gpt-6-sol** | Managed LLM | Long-form copy and journey content. | about $10.50 per 1k | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S15 |
| Alternative | **Self-hosted Jais 2 70B Chat** | Open weights, Apache 2.0 | Arabic-first copy with Gulf register. | GPU | In UAE North or on-prem | S24 |
| Alternative | **Self-hosted Falcon-H1 Arabic 34B** | Open weights, TII licence | Strongest open Arabic model on OALL v2. | GPU | In UAE North or on-prem | S25 |

### T09 Risk case summaries (case.summarise)

**Where it lives:** Security and risk agent; getRiskCase, addRiskCaseEvidence; BO-1160  
**Type:** LLM summarisation over case evidence  
**Package anchor:** Design 3.3 (Strong); LLM off the money path: it summarises, never scores (5.10)

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Azure OpenAI gpt-6-sol** | Managed LLM | Long context and factual consistency over many evidence items; citations back to evidence ids. | about $10.50 per 1k | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S15 |
| Alternative | **Azure OpenAI gpt-5.1** | Managed LLM | Fallback on the regional PTU list. | Azure meter not checked | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S01 |
| Alternative | **Azure OpenAI gpt-5-mini** | Managed LLM | Short cases only. | about $1.58 per 1k | Azure UAE North resource, Global Standard: data at rest in UAE, processing may be outside UAE (S01). In-UAE only as Regional Provisioned (PTU) (S01). | S04 |
| Alternative | **Self-hosted Qwen3.5-122B-A10B** | Open weights, Apache 2.0 | On-prem security teams. | GPU | In UAE North or on-prem | S26 |

### T10 Embeddings for RAG and the semantic cache

**Where it lives:** Platform (never BYOK); ingestKnowledgeDocument, semanticSearch, cache:answer; Qdrant collection per tenant  
**Type:** Embedding model (multilingual incl. Arabic)  
**Package anchor:** Design 3.3 (BGE-M3 self-hosted on CPU, default pending ADR-0021's evaluation, AIC-042/067); ADR-0034; ADR-0049; arabic-embed-eval A-05

**This is a creation decision**: a collection is built with one model and changing it means a shadow re-embed
(ADR-0021, ADR-0034). So it should not be BYOK. The August harness (`arabic-embed-eval/`) has never produced a number: its one
smoke run failed on an mteb argument (`hf_subsets`). Item A-05 (full local run) is still open. Add the newer candidates below to
`models.json` before running it, and keep the 30–50 query Gulf domain set as the deciding test.
BGE-M3 gives dense and sparse vectors in one pass; a dense-only model needs a separate sparse (BM25-style) index for hybrid retrieval.

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Qwen3-Embedding-0.6B (to confirm by A-05; BGE-M3 stays until then)** | Open weights, Apache 2.0 | MTEB multilingual retrieval 64.64 vs BGE-M3's 54.60 on Qwen's table; 1024 dims, 32K context, 100+ languages. CPU-feasible at 0.6B. Instruction-aware queries. | Self-hosted CPU | In-cell | S30 |
| Alternative | **BGE-M3 (current default)** | Open weights, MIT | Dense + sparse + multi-vector in one pass (hybrid retrieval without a second index); proven multilingual; 8K context. Lower retrieval score than the newer models. | Self-hosted CPU | In-cell | S31, S30 |
| Alternative | **Microsoft harrier-oss-v1-0.6b (27b for GPU)** | Open weights, MIT | New (Apr 2026) Multilingual MTEB v2 leader family; 0.6b scores 69.0, Arabic listed among 94 languages. | Self-hosted CPU (0.6b) | In-cell | S32 |
| Alternative | **IBM granite-embedding-311m-multilingual-r2** | Open weights, Apache 2.0 | Arabic among 52 enhanced languages; #2 under 500M on MTEB; smallest good CPU option, 32K context. | Self-hosted CPU | In-cell | S33 |
| Alternative | **Azure OpenAI text-embedding-3-large** | Managed API | The only Azure embedding sold as Regional Standard in UAE North, so in-UAE without self-hosting. Breaks AIC-042 (no external API for search) and adds per-token cost. | $0.13 / 1M (Global); regional price UNCONFIRMED (eastus2 regional is +10%) | Regional Standard in UAE North (S01) | S01, S04 |
| Avoid | **jina-embeddings-v3/v4/v5** | Open weights, non-commercial | CC-BY-NC (v3, v5) or Qwen Research licence (v4): cannot be self-hosted in a paid product. | n/a | n/a | S34 |

### T11 Reranking (two-stage retrieval)

**Where it lives:** Platform (never BYOK); AiProviderCapability rerank, a declared stage (ADR-0034)  
**Type:** Cross-encoder reranker  
**Package anchor:** ADR-0034 two-stage retrieval; design 3.3 (a multilingual cross-encoder, self-hosted on CPU)

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Qwen3-Reranker-0.6B** | Open weights, Apache 2.0 | MMTEB-R 66.36 vs 58.36 for bge-reranker-v2-m3; 32K context; Arabic via the Qwen3 base. CPU latency over 20–50 candidates is UNCONFIRMED: measure against the 1.5 s TTFT budget. | Self-hosted CPU | In-cell | S36, S30 |
| Alternative | **bge-reranker-v2-m3 (current plan)** | Open weights, Apache 2.0 | Proven, evaluated on MIRACL (includes Arabic), same size; lower scores. | Self-hosted CPU | In-cell | S37, S30 |
| Alternative | **Qwen3-Reranker-4B** | Open weights, Apache 2.0 | MMTEB-R 72.74; needs a GPU, so only where the cell has one. | GPU | In-cell | S36 |
| Alternative | **gte-multilingual-reranker-base** | Open weights (licence UNCONFIRMED) | 0.3B, faster on CPU; MMTEB-R 59.44. | Self-hosted CPU | In-cell | S30 |
| Alternative | **Cohere rerank-v4.0-fast (Azure Foundry)** | Managed API | Sold by Azure in UAE North as Global Standard; multilingual. Breaks AIC-042 and processing may leave the UAE. | about $2.00 per 1k searches | Global Standard only (S01) | S01, S35 |
| Avoid | **jina-reranker-v2/v3/m0** | Open weights, non-commercial | CC-BY-NC-4.0. | n/a | n/a | S38 |

### T12 Moderation and prompt-injection guard

**Where it lives:** Platform (never BYOK); gateway guardrail short-circuit (ADR-0034), before and after every guest-facing call  
**Type:** Safety classifier  
**Package anchor:** ADR-0034 guardrail short-circuit; design 3.3 (refusals a rule can decide never reach a model)

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Qwen3Guard-Gen-4B (Qwen3Guard-Stream for streamed answers)** | Open weights, Apache 2.0 | 119 languages incl. Arabic varieties; Safe/Controversial/Unsafe with categories incl. jailbreak and PII; the Stream variant checks tokens as the concierge streams. 0.6B for CPU. | Self-hosted | In-cell | S39 |
| Alternative | **Azure AI Content Safety + Prompt Shields** | Managed service | Available in UAE North (harms, Prompt Shields, protected material, blocklists). Harm models trained on 8 languages, not Arabic; Prompt Shields tested in English; groundedness detection not in UAE North. | $0.375 per 1k text records | UAE North | S05, S04 |
| Alternative | **gpt-oss-safeguard-20b** | Open weights, Apache 2.0 | Policy written as a prompt (the tenant's own content rules); fits a 16 GB GPU. Arabic-specific results UNCONFIRMED. | Self-hosted GPU | In-cell | S41 |
| Alternative | **OpenAI omni-moderation-latest** | Managed API | Free; only reachable with an OpenAI key; Arabic coverage not stated. | Free | Outside UAE | S43 |
| Avoid | **Llama Guard 4 / Prompt Guard 2** | Open weights, Llama licence | Supported languages exclude Arabic; English-only use at most. | n/a | n/a | S40 |

### T13 PII detection and masking (maskedFields, fail closed)

**Where it lives:** Platform (never BYOK); gateway before every call (ADR-0020 §2, AiPolicy.maskedFields)  
**Type:** Deterministic recognisers + NER  
**Package anchor:** ADR-0020 (masking fails closed); ADR-0023 PII separation; AIC-214

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Schema field masking + Microsoft Presidio with custom UAE/Arabic recognisers** | Open source, MIT + rules | Presidio has no built-in Arabic, so TICVAI writes recognisers (Emirates ID 784-…, +971 phones, passport, email, IBAN, card Luhn) and plugs in an Arabic NER engine. Deterministic, testable, fails closed. | CPU | In-cell | S42 |
| Alternative | **Azure AI Language PII** | Managed service | Arabic supported for text and document PII; Language says it does not process data outside the region. Conversation PII has no Arabic. Per-record UAE North price UNCONFIRMED. | Doc PII redaction $10 per 1k pages (UAE North meter) | UAE North | S06, S07, S04 |
| Alternative | **Qwen3Guard PII category (second check)** | Open weights, Apache 2.0 | Flags that a prompt carries PII; does not by itself return spans to mask (UNCONFIRMED), so it is a backstop, not the masker. | Self-hosted | In-cell | S39 |
| Alternative | **Arabic GLiNER variants (NAMAA-Space gliner_arabic)** | Open weights, licence UNCONFIRMED | Zero-shot Arabic entity spans; the mainstream GLiNER-PII models do not claim Arabic. | CPU | In-cell | S42 |

### T14 OCR and document verification (accreditation documents, guest ID)

**Where it lives:** verifyAccreditationDocument (BO-630, ACC-007), IdentityGuestVerification method documentScanner/provider  
**Type:** OCR / document AI + deterministic checks; a person decides  
**Package anchor:** accreditation.yaml (verifier and refusal reason recorded); identity.yaml 5.3.21; CF-35 (biometric/ID data is sensitive)

AI here pre-fills fields (name, document number, expiry), checks expiry and MRZ check digits, and flags mismatches with
the application; it never verifies on its own. **Emirates ID is not named in the Document Intelligence ID model**: test it.
Passports can be verified cryptographically from the chip (ICAO 9303 passive authentication), which is stronger than any OCR.

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Azure AI Document Intelligence v4 (prebuilt-idDocument, Read, Layout) + MRZ check-digit validation** | Managed service + rules | Arabic printed and handwritten text in Read/Layout; ID model covers passports worldwide plus ID cards and residence permits. Emirates ID: UNCONFIRMED. | Read $1.50; Layout and prebuilt $10; custom $30 per 1k pages | UAE North meters exist | S09, S10, S04 |
| Alternative | **PaddleOCR PP-OCRv5 Arabic + PaddleOCR-VL-0.9B** | Open weights (Apache 2.0, UNCONFIRMED this pass) | Arabic recogniser at 81.27% accuracy; runs on CPU; the on-prem and isolated-site option. | CPU | In-cell or on-prem | S45 |
| Alternative | **NFC eMRTD chip read (ICAO 9303, JMRTD / nMRTD)** | Deterministic (no AI) | Passive authentication proves the issuer signed the data; best for passports at a staffed desk with a reader. Emirates ID chip readability UNCONFIRMED. | Reader hardware | On device | S93 |
| Alternative | **Mistral OCR 3** | Managed API (self-host for enterprise) | Strong document OCR at low price; processing outside the UAE. | $2 per 1k pages ($1 batch) | Outside UAE | S44 |
| Alternative | **Qwen3-VL-8B** | Open weights, Apache 2.0 | Vision-language reading of messy scans and certificates; Arabic OCR UNCONFIRMED. | GPU | In-cell or on-prem | S48 |
| Avoid | **AWS Textract; Google Document AI identity parser** | Managed APIs | Textract has no Arabic; Google's identity parser is English-only. | n/a | n/a | S46, S47 |

### T15 Seat-map and venue-layout generation (generateVenueLayout, proposeSeatMapChanges, proposeVenueLabels, proposeWalkways)

**Where it lives:** Operations agent; BO-093, BO-970/975  
**Type:** Vector parsing + vision LLM + rules validation  
**Package anchor:** AI functions review: seat-map-layout (S6, 3 AI-weeks; slip candidate in ADR-0059); release gate on TICVAI's evaluation drawings

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Vector extraction (DXF/SVG/PDF) + Azure OpenAI gpt-6-sol vision for sections and labels + rules validation** | Parser + managed LLM | Seat coordinates should come from vectors, not pixels; the LLM proposes sections, rows and labels as a plan a person approves; what it guessed is highlighted. gpt-6-sol vision quality on plans UNCONFIRMED: evaluation drawings decide. | about $10.50 per 1k calls | Global Standard / regional PTU | S01, S15 |
| Alternative | **Azure Document Intelligence Layout (text and labels on raster plans)** | Managed service | Reads row/section text from scanned plans; no geometry understanding. | $10 per 1k pages | UAE North | S10, S04 |
| Alternative | **Qwen3-VL (8B–32B)** | Open weights, Apache 2.0 | Self-hosted vision-language model for plans; on-prem option. | GPU | In-cell or on-prem | S48 |
| Alternative | **Classical CV (OpenCV symbol detection) on raster plans** | Open source | Finds repeated seat glyphs on scans with no vectors; brittle across drawing styles. | CPU | In-cell |  |

### T16 Speech: speech-to-text and text-to-speech (if voice is enabled)

**Where it lives:** AiCapability speechToText, textToSpeech (BL-164); voice input on Sahli is not specified yet  
**Type:** ASR / TTS  
**Package anchor:** ai.yaml AiCapability note: speech is where UAE residency is hardest

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Azure AI Speech ar-AE (STT) + ar-AE-FatimaNeural / ar-AE-HamdanNeural (TTS)** | Managed service | Real-time and batch STT and neural TTS available in UAE North; data stays in region. No HD voices and no custom-speech training in UAE North. | STT $1.00/h; TTS $15 / 1M chars | UAE North | S11, S12, S04 |
| Alternative | **Cohere Transcribe Arabic (2B)** | Open weights, Apache 2.0 | Best open Arabic ASR: average WER 25.87, Gulf 24.36 (vs Whisper large-v3 36.86 / 46.14). Self-host for on-prem. | GPU | In-cell or on-prem | S49 |
| Alternative | **Deepgram Nova-3 Arabic (ar-AE dialect model)** | Managed API | Dialect-specific Gulf models; processing location and price UNCONFIRMED. | UNCONFIRMED | Outside UAE (assumed) | S50 |
| Alternative | **Whisper large-v3** | Open weights, MIT | Widely used, but much weaker on Gulf speech (WER 46.14). | GPU | In-cell | S49 |
| Alternative | **Chatterbox Multilingual (TTS)** | Open weights, MIT | On-prem Arabic TTS; dialect not specified. | GPU | In-cell | S52 |

### T17 Face match (Face Pass gates)

**Where it lives:** access.yaml Face Pass; template is the vendor's opaque format; scores normalised 0–1 by the adapter (R077)  
**Type:** Biometric 1:1 / 1:N (vendor SDK)  
**Package anchor:** access.yaml (the face vendor is the client's contracted vendor, audit R077); ADR-0063 biometric templates; CF-35

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **The client's contracted face vendor (adapter normalises scores)** | Vendor SDK, on-prem | Decided in the package (R077). TICVAI's job is the adapter, thresholds per context profile, consent, and template retention. | Client contract | On-prem |  |
| Alternative | **IDEMIA** | Vendor SDK | #1 on NIST FRTE 1:N mugshot at every gallery size to 12M (Aug–Sep 2026). | Commercial | On-prem | S88 |
| Alternative | **NEC NeoFace** | Vendor SDK | Leads FRTE 1:N border and visa-to-kiosk categories (Sep 2026). | Commercial | On-prem | S88 |
| Alternative | **Paravision** | Vendor SDK / Docker engines | Leads FRTE visa-to-border; on-prem SDKs with liveness; powers the GDRFA smart corridor at DXB with emaratech (Jan 2026). | Commercial | On-prem | S88, S89 |
| Avoid | **AWS Rekognition; Azure Face; InsightFace pretrained models** | Cloud APIs / open models | Rekognition has no Middle East endpoint; Azure Face is Limited Access and a 2025 Microsoft answer says not in UAE North (UAE North price meters exist: UNCONFIRMED); InsightFace models are non-commercial. | n/a | n/a | S91, S13, S90, S04 |

### T18 Attendance, demand and revenue forecasting

**Where it lives:** runForecast, getForecast, createForecastScenario; nightly by 05:00 tenant-local; requestSuggestion demandForecast/scenario  
**Type:** Time-series forecasting (probabilistic)  
**Package anchor:** Design 3.10 and 3.13; ADR-0051 (prior -> statistical -> learned; gate: WAPE at least 10% better at 7 days, bias within ±3%, P10–P90 coverage 70–90%)

Forecasts are a **nightly batch**, so the <5 ms in-process budget does not constrain the model here (it does for fraud and
ranking). That opens the door to zero-shot foundation models: Chronos-2 is #1 on the live fev-bench tables, is Apache 2.0, takes
known-future covariates (calendar, weather, promotions) and is pretrained on public data, not other tenants' (AIP-149 holds).
**Recommendation:** keep LightGBM as the learned producer the design names, and add Chronos-2 to the S6 backtest as the first
challenger *and* as a candidate statistical producer for tenants with less than three months of history. Let the shadow gate
choose. Licence traps: TimesFM-3 and Moirai-2 weights are non-commercial.

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **LightGBM global model per tenant (mlforecast), quantile objectives for P10/P50/P90** | Gradient boosting, MIT | Pools a tenant's ~12,000 series; features for Hijri holidays, weather, booking pace and price; the M5 accuracy winner was an ensemble of LightGBM models. Needs a season of own data to beat the prior: matches the gate. | CPU; training minutes per tenant weekly | In-cell, CPU; same code on-prem | S61, S62 |
| Alternative | **Amazon Chronos-2 (120M; chronos-2-small 28M)** | Zero-shot foundation model, Apache 2.0 | #1 on fev-bench (SQL win rate 91.4%); past and known-future covariates; works on short histories, which is exactly the cold-start gap. CPU inference feasible for nightly batch. | CPU/GPU batch | In-cell, CPU; same code on-prem | S53, S54 |
| Alternative | **Nixtla statsforecast: MSTL / AutoETS with holiday regressors (the statistical producer)** | Classical, Apache 2.0 | The design's statistical stage; fast and explainable; needs about two seasons to be at its best and wins only 27–41% of fev-bench pairings against foundation models. | CPU, seconds | In-cell, CPU; same code on-prem | S59, S54 |
| Alternative | **Google TimesFM-2.5 (200M)** | Zero-shot foundation model, Apache 2.0 | #3 on fev-bench; covariates through XReg; 16K context. (TimesFM-3 is non-commercial.) | CPU (~1.5 GB RAM) | In-cell, CPU; same code on-prem | S55, S54 |
| Alternative | **NX-AI TiRex-2** | Zero-shot foundation model, Apache 2.0 | Small (38M), CPU-documented, covariates; claims state of the art (Jul 2026) but no independent placement yet. | CPU | In-cell, CPU; same code on-prem | S56 |
| Avoid | **Prophet; TimesFM-3; Moirai-2** | — | Prophet is maintained (1.4.0) but slower and weaker than the above; TimesFM-3 and Moirai-2 weights are non-commercial. | n/a | n/a | S60, S55, S58 |

### T19 F&B demand, prep plan, requisition, replenishment, waste risk, menu engineering

**Where it lives:** requestSuggestion kinds prepPlan, requisition, replenishment, wasteRisk, menuEngineering; GST-031, KIT screens  
**Type:** Intermittent-demand forecasting + rules  
**Package anchor:** SuggestionKind descriptions (each kind's baseline and own-data take-over point); ADR-0051

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **LightGBM global model, Tweedie objective, per tenant (mlforecast)** | Gradient boosting, MIT | Item x outlet x service-period demand with attendance forecast (T18), daypart, weather and menu features; Tweedie loss suits many-zero series (M5 practice). Reconciled to the outlet total. | CPU | In-cell, CPU; same code on-prem | S61, S62 |
| Alternative | **statsforecast intermittent models (Croston/SBA, TSB, ADIDA, IMAPA)** | Classical, Apache 2.0 | The right statistical producer for slow movers and stock items; seconds per tenant. | CPU | In-cell, CPU; same code on-prem | S59 |
| Alternative | **hierarchicalforecast (MinTrace) reconciliation** | Reconciliation, Apache 2.0 | Makes item forecasts add up to outlet and venue covers, so the prep plan and the staffing view agree. | CPU | In-cell, CPU; same code on-prem | S63 |
| Alternative | **Chronos-2 for new menu items and new outlets** | Zero-shot FM, Apache 2.0 | Cold start for items with a few weeks of sales. | CPU batch | In-cell, CPU; same code on-prem | S53 |

### T20 Queue and wait-time prediction, queue balancing (waitTime, queueBalancing, F&B quoteWaitTime)

**Where it lives:** getWaitTimes, requestSuggestion waitTime/queueBalancing, fnb quoteWaitTime  
**Type:** Queueing model + quantile regression  
**Package anchor:** AI functions review: queue-wait-time (S5); SuggestionKind waitTime (people ahead / throughput of the last 30 min)

Train on observed waits (scan-in to ride or order to pickup), not posted waits: TouringPlans found Disney's actual waits
averaged 73% of posted in August 2026 (S85).

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Throughput now-cast + LightGBM quantile regression (P50/P90 wait) per attraction** | Rules + gradient boosting | Day one works from capacity; once readings exist, GBM learns throughput by hour, weather and crowd; quantiles give an honest range. Published theme-park work uses GBDT for waits. | CPU | In-cell, CPU; same code on-prem | S84 |
| Alternative | **Erlang C / Erlang A (M/M/c with abandonment) via pyworkforce** | Closed-form queueing, MIT | Needs no data; right for staffed counters (F&B, ticket windows) where servers vary. | CPU | In-cell, CPU; same code on-prem | S83 |
| Alternative | **Chronos-2 on the queue-load series** | Zero-shot FM, Apache 2.0 | Forecasts arrivals for queueBalancing horizons when history is short. | CPU batch | In-cell, CPU; same code on-prem | S53 |
| Alternative | **Markov / physics-informed neural queue model** | Research | Probabilistic waits tested on a Universal coaster (2026); research-grade, not for the first release. | GPU training | In-cell, CPU; same code on-prem | S94 |

### T21 Staffing and operational requirements

**Where it lives:** requestSuggestion staffing; decideOperationalRequirement; BO-927, ADM-518  
**Type:** Workload conversion + optimisation (no learned model of its own)  
**Package anchor:** AI functions review: operational-requirements (S5): it follows the forecast's promoted model

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Forecast / measured productivity (shrunk from the default) + OR-Tools CP-SAT for coverage** | Arithmetic + solver, Apache 2.0 | Exactly the design's rule, with a solver to respect shift lengths and breaks; output stays a coverage target a person applies in Workforce. | CPU | In-cell, CPU; same code on-prem | S86 |
| Alternative | **Erlang C (pyworkforce) for queue-facing roles** | Closed-form, MIT | Tills, gates and counters where service level, not covers, sets the headcount. | CPU | In-cell, CPU; same code on-prem | S83 |
| Alternative | **PuLP (CBC/HiGHS)** | LP/MIP, MIT | Simpler LP route; 4.0 (25 Sep 2026) has breaking changes and needs Python 3.12+. | CPU | In-cell, CPU; same code on-prem | S87 |

### T22 Anomaly detection (KPI anomalies, insight lifecycle)

**Where it lives:** configureAnomalyDetector, listAiInsights, reporting.listAnalyticsAnomalies; ANL-055/058/059  
**Type:** Time-series anomaly detection  
**Package anchor:** Design 3.10 (thresholds -> seasonal baseline with robust z per KPI -> model only where false alarms warrant); AI functions review S6

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **STL decomposition + robust z (median/MAD) per KPI and weekday, plus forecast-residual bands** | Statistical | TSB-AD (1,070 series, 40 algorithms): simpler statistical methods often perform best. Explainable ("3.4 MADs above a typical Tuesday"). | CPU | In-cell, CPU; same code on-prem | S65 |
| Alternative | **Isolation Forest / ECOD (PyOD 3)** | Unsupervised, BSD-2 | For multivariate patterns (refunds + voids + cash variance together); ADBench finds no single unsupervised winner, so keep it secondary. | CPU | In-cell, CPU; same code on-prem | S66 |
| Alternative | **statsforecast prediction intervals as detectors** | Classical, Apache 2.0 | Reuses the statistical producer's intervals. | CPU | In-cell, CPU; same code on-prem | S59 |
| Alternative | **Chronos-2 residuals for change points** | Zero-shot FM | Foundation models are not competitive as anomaly detectors on their own, but their errors peak at change points. | CPU batch | In-cell, CPU; same code on-prem | S68 |
| Avoid | **Salesforce Merlion** | Framework | Archived 11 Mar 2026. | n/a | n/a | S67 |

### T23 Fraud and risk scoring (transaction, entity, staff leakage) and approval-request scoring

**Where it lives:** scoreTransactionRisk (p95 50 ms), getEntityRisk, expandRiskNetwork, scoreApprovalRequest  
**Type:** Supervised classifier on analyst labels + unsupervised + graph features  
**Package anchor:** Design 3.10; ADR-0053; gate: recall at least equal to rules, precision at least 20% better at the same review rate, no segment slice worse

Many tenants will never collect enough analyst-labelled fraud to pass the gate and stay on rules, which the review accepts.
Approval scoring stays rules plus requester baselines; a model "probably never needed" (AI functions review).

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **LightGBM classifier on analyst-labelled outcomes + graph features (shared device/card/account degree)** | Gradient boosting, MIT | IEEE-CIS study (Jul 2026): LightGBM with good encoders AUC-ROC 0.961, tied with CatBoost; trees beat deep nets on medium tabular data; tune thresholds rather than resample. | CPU, <1 ms | In-cell, CPU; same code on-prem | S69, S70, S71 |
| Alternative | **CatBoost** | Gradient boosting, Apache 2.0 | Best AUC-PR in the same study (0.822 vs 0.793); native categorical handling (channel, venue, device type). | CPU | In-cell, CPU; same code on-prem | S69 |
| Alternative | **XGBoost** | Gradient boosting, Apache 2.0 | Used by the IEEE-CIS winning team; equivalent choice. | CPU | In-cell, CPU; same code on-prem | S69 |
| Alternative | **Isolation Forest / ECOD (unlabelled entity baselines)** | Unsupervised, BSD-2 | Before labels exist: unusual customers, devices, cashiers. A feature for the classifier later. | CPU | In-cell, CPU; same code on-prem | S66 |
| Alternative | **TabPFN v2 (not 2.5/3.5)** | Tabular foundation model, Apache 2.0 + attribution | Strong with a few hundred labels (up to ~10k rows); slower than GBM, so scoring off the sync path or as a teacher. 2.5 and 3.5 are non-commercial. | CPU (16 GB RAM) | In-cell, CPU; same code on-prem | S72 |

### T24 Recommendations and upsell (one engine, every placement)

**Where it lives:** decideRecommendations (p95 120 ms, ML budget 30 ms), recordRecommendationEvents; the four channel adapters  
**Type:** Candidate generation + learning-to-rank  
**Package anchor:** ADR-0052; design 3.10; gate: a controlled experiment against rules with guardrails (AIR-145..147)

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Co-purchase lift / item-kNN (statistical) -> LightGBM LambdaRank (learned)** | Statistics + gradient boosting, MIT | Simple kNN/graph baselines beat most neural recommenders in a reproducibility study; LambdaMART reranking is industry practice and fast on CPU. | CPU | In-cell, CPU; same code on-prem | S74, S77 |
| Alternative | **implicit ALS / BPR (candidate generation)** | Matrix factorisation, MIT (active, May 2026) | Personal candidates once guests have history; ANN-ready. | CPU | In-cell, CPU; same code on-prem | S75 |
| Alternative | **XGBoost rank:ndcg** | Gradient boosting, Apache 2.0 | Equivalent ranker. | CPU | In-cell, CPU; same code on-prem | S77 |
| Alternative | **Thompson-sampling bandit (in-house) for exploration** | Bandit | Explores new add-ons safely; Vowpal Wabbit has had no release since Sep 2024, so write the small sampler in-house. | CPU | In-cell, CPU; same code on-prem | S79 |
| Avoid | **LightFM; SASRec/BERT4Rec; two-tower** | — | LightFM unmaintained since 2023; sequential and two-tower models need volume most tenants lack. | n/a | n/a | S76, S78 |

### T25 Marketing ML: segmentation, lookalike segments, send time, propensity

**Where it lives:** requestSuggestion segmentation and sendTime; proposeLookalikeSegment; listMarketingRecommendations  
**Type:** Clustering / similarity / Bayesian rates / classifier  
**Package anchor:** AI functions review: marketing-ai (S7); SuggestionKind sendTime (fewer than three touches -> segment's modal hour)

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **RFM segments + Beta-Binomial send-hour model shrunk to segment + LightGBM propensity (in shadow)** | Statistics + gradient boosting | Each part works on little data and degrades to the segment; propensity promoted only after an A/B test against the playbook. | CPU | In-cell, CPU; same code on-prem | S80 |
| Alternative | **k-means / Gaussian mixture on RFM and attributes** | Clustering | Data-driven segments once 90 days exist. | CPU | In-cell, CPU; same code on-prem |  |
| Alternative | **kNN lookalike on attribute vectors** | Similarity | Transparent "guests like your seed"; no training. | CPU | In-cell, CPU; same code on-prem |  |
| Alternative | **Logistic regression propensity** | GLM | Explainable fallback where GBM overfits small campaigns. | CPU | In-cell, CPU; same code on-prem |  |

### T26 Dynamic pricing suggestions (L2: a person approves)

**Where it lives:** requestSuggestion (demand-based price kind); Catalogue pricing bands; ADM-088/089, BO-528  
**Type:** Demand elasticity + pace rule  
**Package anchor:** AI functions review: dynamic-pricing-ai (S7); design 6: L4 auto-pricing off until six months of clean L3 evidence

| Rank | Model / method | Kind | Why (accuracy, Arabic, latency, data needs) | Cost | UAE North / on-prem | Sources |
|---|---|---|---|---|---|---|
| Recommended | **Hierarchical Bayesian log-log elasticity (PyMC / PyMC-Marketing), used inside the pace rule** | Bayesian regression, Apache 2.0 | Partial pooling suits sparse price variation; gives uncertainty, so a suggestion can say "likely +4–9% revenue" rather than a bare number. | CPU | In-cell, CPU; same code on-prem | S80 |
| Alternative | **Double ML (EconML / DoubleML)** | Causal ML, MIT / BSD-3 | Debiases elasticity when prices were set in response to demand. | CPU | In-cell, CPU; same code on-prem | S81 |
| Alternative | **Thompson-sampling price tests** | Bandit | Learns price response by experiment; only where the venue accepts price tests. | CPU | In-cell, CPU; same code on-prem | S82 |
| Alternative | **LightGBM demand model with price as a feature + simulation** | Gradient boosting | Reuses T18's model; elasticity is implicit and less stable. | CPU | In-cell, CPU; same code on-prem | S61 |

---

## 4. What this means for the package (not changed; for the package owner)

1. **AI-D18 conflicts with the 2 October decision.** Design section 8 row 13 and `setAiProvider` say a fitness band
   "warns, never blocks", and the ADM-037 design note shows *"gpt-4o-mini is underpowered for the configuration assistant …
   You can still save."* Under curation, `setAiProvider` (and the BYOK path) should **refuse** a model outside the curated map
   for that task (a new problem type, for example `modelNotCurated`), `taskKeys` should bind tiers, and ADM-037's copy should
   change. A new or changed operation needs a vocabulary permission (existing `PLATFORM_AI_MANAGE`) and re-derive, mirrors, check.
2. **The residency decision (2.1 and 2A) is needed before Block A AI tickets are final.** Section 2A's route would amend AI-D02 (Compass for UAE-only tenants) and add a per-tenant residency class. Design 3.3 and 1.2, ADR-0009 §1 and
   AI-D03 all assume an in-region default endpoint that Azure sells only as regional PTU. Design 4.5's cost table assumes
   per-token prices; under option B or C it becomes a fixed monthly capacity cost per cell.
3. **The fallback chain must stay in-UAE too** (design 4.3): "a second Azure OpenAI deployment with its own quota" is only
   in-UAE if it is also regional PTU; the in-cell open model (option C) is the natural second hop.
4. **Embeddings: run A-05 before Block A's concierge golden set is frozen.** Add Qwen3-Embedding-0.6B, harrier-oss-v1-0.6b
   and granite-embedding-311m-multilingual-r2 to `arabic-embed-eval/models.json`; fix the `hf_subsets` failure first. The
   collection model is a creation decision (ADR-0021), so choosing late costs a re-embed of every tenant.
5. **Reranker: replace bge-reranker-v2-m3 with Qwen3-Reranker-0.6B** in design 3.3, subject to a CPU latency check.
6. **Moderation and groundedness:** Azure Content Safety's harm models are not trained on Arabic, and groundedness
   detection is not offered in UAE North. The design already gates assistants on its own golden-set groundedness (3.5),
   which stays the control; add Qwen3Guard as the in-cell Arabic guard.
7. **Speech:** gpt-4o-transcribe, TTS and realtime models are not deployable in UAE North; Azure AI Speech is. If voice
   comes to Sahli, it is Azure Speech or a self-hosted Cohere Transcribe Arabic.
8. **`AiProviderKind` has no `mistral` value.** A Mistral BYOK needs an adapter or must go through `openaiCompatible`.
9. **Forecasting:** add Chronos-2 to the S6 backtest as a challenger and as a statistical-stage candidate for short
   histories (T18). No contract change: it is another producer version behind the same interface.

### Licence traps (do not use in a paid product without a commercial licence)

TimesFM-3 weights (non-commercial), Moirai-2 (CC-BY-NC-4.0), TabPFN-2.5 and 3.5 (non-commercial), all Jina embeddings and
rerankers (CC-BY-NC or Qwen Research licence), InsightFace pretrained models, Surya OCR weights (free only under $5M
revenue), XTTS-v2 (Coqui public licence, believed non-commercial). Falcon-H1 Arabic uses the TII Falcon licence (Apache-based
with a usage policy): legal review before shipping. Llama 4 uses the Llama community licence (fine below 700M monthly users).

### Not confirmed (check before relying on it)

- Core42 Compass: retention, logging and sub-processor terms; pay-as-you-go minimums; the processing region of GPT-5.2 (others are stated per model).
- OpenAI UAE regional processing: which data centre serves it; approval terms for TICVAI as an API customer.
- PTU throughput at TICVAI's real traffic mix (run the Azure PTU calculator); the minimums themselves are confirmed (section 2A).
- Which tenants count as government or semi-government entities (Miral, Dubai Holding companies) for PDPL scope and DESC rules: a legal question.
- Azure prices for gpt-6-sol, gpt-6-luna and gpt-5.1 (OpenAI list prices used instead).
- Whether gpt-6-sol exposes reasoning-effort control, and its vision quality on venue plans.
- Emirates ID support in Document Intelligence's ID model; Emirates ID chip readability (ICAO 9303).
- Azure Translator in-region processing for a UAE North resource.
- Azure Face in UAE North (price meters exist; a 2025 Microsoft answer says unavailable).
- OpenAI UAE inference residency for API customers (reported for Enterprise/Edu).
- Arabic (especially Gulf) quality of every chat model in the map: no public benchmark covers it; the golden sets decide.
- Live GIFT-Eval leader; independent placement of TiRex-2 and Toto 2.0; CPU latency of Qwen3-Reranker-0.6B.

## Sources

Each source was read on the date shown (all dates 2026 unless stated). "Undated" means the page shows no update date.

| Key | Source | Page date / read on |
|---|---|---|
| S01 | [Microsoft Learn: Foundry Models sold by Azure, region availability (uaenorth tables, deployment types)](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure-region-availability) | updated 4 Sep 2026; read 2 Oct 2026 |
| S03 | [Microsoft Learn: Foundry Models from partners and community](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-from-partners) | updated 22 Sep 2026 |
| S04 | [Azure Retail Prices API (uaenorth and eastus2 meters)](https://prices.azure.com/api/retail/prices) | queried 2 Oct 2026 |
| S05 | [Microsoft Learn: Azure AI Content Safety region availability](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/region-availability) | 18 Sep 2026 |
| S06 | [Microsoft Learn: Azure AI Language regional support](https://learn.microsoft.com/en-us/azure/ai-services/language-service/concepts/regional-support) | updated 22 Jul 2026 |
| S07 | [Microsoft Learn: Azure AI Language PII language support](https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/language-support) | 17 Aug 2026 |
| S08 | [Microsoft Learn: Azure AI Translator region support](https://learn.microsoft.com/en-us/azure/ai-services/translator/region-support) | 21 Aug 2026 |
| S09 | [Microsoft Learn: Document Intelligence prebuilt ID document model](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/id-document) | 15 Aug 2026 |
| S10 | [Microsoft Learn: Document Intelligence OCR language support](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/language-support/ocr) | 18 Apr 2026 |
| S11 | [Microsoft Learn: Azure AI Speech regions](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/regions) | 30 Sep 2026 |
| S12 | [Microsoft Learn: Azure AI Speech language and voice support](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support) | 9 Sep 2026 |
| S13 | [Microsoft Learn: Face limited access; Microsoft Q&A on Face in UAE North](https://learn.microsoft.com/en-us/legal/cognitive-services/computer-vision/limited-access-identity) | updated 5 Jun 2026; Q&A 13 Apr 2025 (learn.microsoft.com/en-us/answers/questions/2247726) |
| S14 | [Microsoft Learn: Claude models in Foundry](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/claude-models) | 21 Sep 2026 |
| S15 | [OpenAI API pricing](https://developers.openai.com/api/docs/pricing) | read 2 Oct 2026 (undated) |
| S16 | [OpenAI model pages gpt-6-luna / gpt-6-sol / gpt-6-astra; vktr.com on GPT-6 Sol and Luna](https://developers.openai.com/api/docs/models/gpt-6-luna) | read 2 Oct 2026; vktr 22 Sep 2026 |
| S17 | [tbreak / Middle East AI News: OpenAI UAE inference residency (secondary)](https://tbreak.com/openai-uae-inference-residency) | 12 Aug 2026 |
| S19 | [Anthropic Claude model table and prices (Claude API reference bundled with Claude Code; inference_geo us/global)](https://platform.claude.com/docs/en/about-claude/pricing) | model table cached 25 Sep 2026 |
| S20 | [AWS: Bedrock global cross-region inference for Claude in the Middle East regions](https://aws.amazon.com/blogs/machine-learning/introducing-amazon-bedrock-global-cross-region-inference-for-anthropics-claude-models-in-the-middle-east-regions) | 24 Feb 2026 |
| S21 | [Google: Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) | updated 1 Oct 2026 |
| S22 | [Google Cloud: Vertex AI / Agent Platform locations and model-by-region table](https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/locations) | 1 Oct 2026 |
| S23 | [Mistral model docs (Small 4, Large 3, Medium 3.5; Saba retired)](https://docs.mistral.ai/models/mistral-small-4-0-26-03) | read 2 Oct 2026 |
| S24 | [Hugging Face: Jais 2 70B Chat model card](https://huggingface.co/inception42/Jais-2-70B-Chat) | read 2 Oct 2026 |
| S25 | [Business Wire / itbrief: Falcon-H1 Arabic tops the Open Arabic LLM Leaderboard](https://www.businesswire.com/news/home/20260105343577) | 5 Jan 2026 |
| S26 | [Hugging Face: Qwen3.5-397B-A17B model card (family sizes, licence, languages)](https://huggingface.co/Qwen/Qwen3.5-397B-A17B) | Feb 2026 |
| S27 | [Stanford CRFM: HELM Arabic](https://crfm.stanford.edu/2025/12/18/helm-arabic.html) | 18 Dec 2025; v2.0.0 results 3 Jun 2026 |
| S30 | [Qwen3-Embedding model card and repository (MTEB and reranker tables)](https://github.com/QwenLM/Qwen3-Embedding) | Jun 2025; read 2 Oct 2026 |
| S31 | [Hugging Face: BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) | undated; read 2 Oct 2026 |
| S32 | [Hugging Face: microsoft/harrier-oss-v1-27b; Bing blog, April 2026](https://huggingface.co/microsoft/harrier-oss-v1-27b) | Apr 2026 |
| S33 | [Hugging Face blog: IBM granite-embedding multilingual r2](https://huggingface.co/blog/ibm-granite/granite-embedding-multilingual-r2) | 14 May 2026 |
| S34 | [Hugging Face: jinaai/jina-embeddings-v4 (licence)](https://huggingface.co/jinaai/jina-embeddings-v4) | Jun 2025 |
| S35 | [Cohere docs: embed and rerank](https://docs.cohere.com/docs/rerank) | undated; read 2 Oct 2026 |
| S36 | [Hugging Face: Qwen/Qwen3-Reranker-0.6B](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B) | Jun 2025 |
| S37 | [Hugging Face: BAAI/bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3) | undated; read 2 Oct 2026 |
| S38 | [Hugging Face: jinaai/jina-reranker-v3 (licence)](https://huggingface.co/jinaai/jina-reranker-v3) | 29 Sep 2025 |
| S39 | [Hugging Face: Qwen/Qwen3Guard-Gen-8B](https://huggingface.co/Qwen/Qwen3Guard-Gen-8B) | Oct 2025 |
| S40 | [Hugging Face: meta-llama/Llama-Guard-4-12B (languages)](https://huggingface.co/meta-llama/Llama-Guard-4-12B) | Apr 2025 |
| S41 | [OpenAI: Introducing gpt-oss-safeguard](https://openai.com/index/introducing-gpt-oss-safeguard) | 29 Oct 2025 |
| S42 | [Microsoft Presidio: supported languages](https://github.com/microsoft/presidio/blob/main/docs/analyzer/languages.md) | undated; read 2 Oct 2026 |
| S43 | [OpenAI: moderation guide](https://developers.openai.com/api/docs/guides/moderation) | undated; read 2 Oct 2026 |
| S44 | [Mistral: Mistral OCR 3](https://mistral.ai/news/mistral-ocr-3) | 17 Dec 2025 |
| S45 | [PaddleOCR: PP-OCRv5 multi-language models (Arabic recogniser)](https://paddleocr.ai/) | undated; read 2 Oct 2026 |
| S46 | [AWS Textract FAQ (languages)](https://aws.amazon.com/textract/faqs/) | undated; read 2 Oct 2026 |
| S47 | [Google Document AI: supported languages](https://docs.cloud.google.com/document-ai/docs/languages) | 24 Sep 2026 |
| S48 | [Hugging Face: Qwen/Qwen3-VL-8B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct) | undated; read 2 Oct 2026 |
| S49 | [Hugging Face blog: Cohere Transcribe Arabic (Open Universal Arabic ASR results incl. Whisper)](https://huggingface.co/blog/CohereLabs/cohere-transcribe-arabic-07-2026-release) | 7 Jul 2026 |
| S50 | [Deepgram changelog: Nova-3 Arabic](https://developers.deepgram.com/changelog/2026/1/27) | 27 Jan 2026 |
| S52 | [GitHub: resemble-ai/chatterbox](https://github.com/resemble-ai/chatterbox) | Sep 2025 |
| S53 | [Hugging Face: amazon/chronos-2](https://huggingface.co/amazon/chronos-2) | read 2 Oct 2026 |
| S54 | [fev-bench leaderboard (SQL table CSV)](https://huggingface.co/spaces/autogluon/fev-bench/raw/main/tables/leaderboard_SQL.csv) | read 2 Oct 2026 |
| S55 | [GitHub: google-research/timesfm (2.5 Apache; 3 non-commercial weights)](https://github.com/google-research/timesfm) | read 2 Oct 2026 |
| S56 | [Hugging Face: NX-AI/TiRex-2; arXiv 2607.01204](https://huggingface.co/NX-AI/TiRex-2) | 1 Jul 2026 |
| S58 | [Hugging Face: Salesforce/moirai-2.0-R-small (licence)](https://huggingface.co/Salesforce/moirai-2.0-R-small) | Nov 2025 |
| S59 | [PyPI: statsforecast](https://pypi.org/project/statsforecast/) | v2.1.1, 16 Jul 2026 |
| S60 | [PyPI: prophet](https://pypi.org/project/prophet/) | v1.4.0, 15 Aug 2026 |
| S61 | [Makridakis et al., M5 accuracy competition results (IJF 38(4))](https://ideas.repec.org/a/eee/intfor/v38y2022i4p1346-1364.html) | 2022 |
| S62 | [PyPI: mlforecast](https://pypi.org/project/mlforecast/) | v1.0.31, 10 Mar 2026 |
| S63 | [GitHub: Nixtla/hierarchicalforecast](https://github.com/Nixtla/hierarchicalforecast) | read 2 Oct 2026 |
| S65 | [TSB-AD benchmark (NeurIPS 2024)](https://neurips.cc/virtual/2024/poster/97690) | 2024 |
| S66 | [PyOD repository; ADBench (arXiv 2206.09426)](https://github.com/yzhao062/pyod) | read 2 Oct 2026; ADBench 2022 |
| S67 | [GitHub: salesforce/Merlion (archived)](https://github.com/salesforce/Merlion) | archived 11 Mar 2026 |
| S68 | [arXiv 2607.12454: time-series foundation models for anomaly detection](https://arxiv.org/abs/2607.12454) | 14 Jul 2026 |
| S69 | [arXiv 2607.00477: encoders and GBDTs on IEEE-CIS fraud](https://arxiv.org/abs/2607.00477) | 1 Jul 2026 |
| S70 | [Grinsztajn et al., why tree models still outperform deep learning on tabular data](https://arxiv.org/abs/2207.08815) | NeurIPS 2022 |
| S71 | [arXiv 2201.08528: imbalanced classification with strong classifiers](https://arxiv.org/abs/2201.08528) | 2022 |
| S72 | [Hugging Face: Prior-Labs TabPFN-v2-clf (Apache + attribution) and tabpfn_2_5 (non-commercial)](https://huggingface.co/Prior-Labs/TabPFN-v2-clf) | read 2 Oct 2026 |
| S74 | [Dacrema et al., reproducibility of neural recommenders](https://arxiv.org/abs/1907.06902) | 2019 |
| S75 | [GitHub: benfred/implicit releases](https://github.com/benfred/implicit/releases) | v0.7.3, 8 May 2026 |
| S76 | [PyPI: lightfm (last release 1.17)](https://pypi.org/project/lightfm/) | 20 Mar 2023 |
| S77 | [Vespa blog: learning to rank (LambdaMART reranking)](https://blog.vespa.ai/improving-product-search-with-ltr-part-three/) | undated |
| S78 | [arXiv 2207.07483: BERT4Rec reproducibility](https://arxiv.org/abs/2207.07483) | 2022 |
| S79 | [GitHub: Vowpal Wabbit releases](https://github.com/VowpalWabbit/vowpal_wabbit/releases) | last release 27 Sep 2024 |
| S80 | [JOSS: PyMC-Marketing](https://joss.theoj.org/papers/10.21105/joss.10805) | 2026 |
| S81 | [PyPI: econml; DoubleML](https://pypi.org/project/econml/) | econml 0.17.0, 31 Jul 2026; DoubleML 0.11.4, 10 Aug 2026 |
| S82 | [Ferreira, Simchi-Levi, Wang: online network revenue management using Thompson sampling (Operations Research 66(6))](https://pubsonline.informs.org/doi/10.1287/opre.2018.1755) | 2018 |
| S83 | [GitHub: rodrigo-arenas/pyworkforce (Erlang C/A, CP-SAT scheduling)](https://github.com/rodrigo-arenas/pyworkforce) | read 2 Oct 2026 |
| S84 | [IPSJ: Tokyo Disney wait-time prediction with gradient boosting and route optimisation](https://ipsj.ixsq.nii.ac.jp/records/234928) | 2024 |
| S85 | [TouringPlans: Disney data dump, 19 August 2026 (actual vs posted waits)](https://touringplans.com/blog/disney-data-dump-august-19-2026/) | 19 Aug 2026 |
| S86 | [PyPI: ortools](https://pypi.org/project/ortools/) | 9.15, 14 Jan 2026 |
| S87 | [PyPI: PuLP](https://pypi.org/project/PuLP/) | 4.0.0, 25 Sep 2026 |
| S88 | [Biometric Update: NIST FRTE 1:N results, September 2026](https://www.biometricupdate.com/202609/new-nist-frte-1n-results-illustrate-facial-recognition-accuracys-multidimensionality) | 16 Sep 2026 |
| S89 | [Paravision news: collaboration with emaratech (GDRFA smart corridor)](https://www.paravision.ai/news/) | Jan 2026 |
| S90 | [InsightFace: commercial licensing of models](https://www.insightface.ai/services/models-commercial-licensing) | read 2 Oct 2026 |
| S91 | [AWS: Amazon Rekognition endpoints](https://docs.aws.amazon.com/general/latest/gr/rekognition.html) | read 2 Oct 2026 |
| S93 | [JMRTD (ICAO 9303 eMRTD reading)](https://jmrtd.org/) | undated; read 2 Oct 2026 |
| S94 | [AIMS Press ERA 34(6): Markov / physics-informed queue-wait model](https://www.aimspress.com/article/doi/10.3934/era.2026186) | 2026 |
| S101 | [Microsoft Learn: provisioned throughput sizing (minimums, increments, TPM per PTU)](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/provisioned-throughput-sizing) | updated 24 Sep 2026 |
| S102 | [Microsoft Learn: provisioned throughput billing and reservations; Azure Retail Prices API uaenorth PTU meters](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/provisioned-throughput-billing) | 5 Jun 2026; prices queried 2 Oct 2026 (effective 1 Sep 2026) |
| S103 | [Microsoft Learn: spillover traffic management](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/spillover-traffic-management) | 18 Jun 2026 |
| S104 | [Microsoft: in-country data processing for Microsoft 365 Copilot in the UAE (and the 15-country update)](https://news.microsoft.com/source/emea/2025/10/microsoft-announces-in-country-data-processing-for-microsoft-365-copilot-in-the-uae-to-accelerate-ai-adoption/) | 14 Oct 2025; update 3 Apr 2026 |
| S106 | [OpenAI API: your data (regional processing, ae.api.openai.com, model list, 10% uplift)](https://developers.openai.com/api/docs/guides/your-data) | read 2 Oct 2026 (undated) |
| S107 | [Zawya: OpenAI expands inference residency to the UAE](https://www.zawya.com/en/press-release/openai-expands-inference-residency-to-the-united-arab-emirates-428932) | Aug 2026 |
| S108 | [Core42 Compass: pricing models](https://www.core42.ai/compass/documentation/pricing-models) | read 2 Oct 2026 (undated) |
| S109 | [Core42 Compass: changelog (models and regions)](https://www.core42.ai/compass/documentation/compass-changelog) | read 2 Oct 2026 |
| S110 | [Core42 Compass: get started (Azure Marketplace subscription and approval)](https://www.core42.ai/compass/documentation/compass-get-started) | read 2 Oct 2026 |
| S111 | [Core42 AI Cloud (GPU prices)](https://aicloud.core42.ai/) | read 2 Oct 2026 |
| S112 | [Core42 Sovereign Public Cloud](https://www.core42.ai/products/sovereign-public-cloud) | read 2 Oct 2026 |
| S113 | [AWS: Bedrock model support by Region](https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.html) | read 2 Oct 2026 |
| S114 | [Oracle: OCI Generative AI models by region; paying for dedicated AI clusters](https://docs.oracle.com/iaas/Content/generative-ai/model-endpoint-regions.htm) | read 2 Oct 2026 |
| S115 | [PR Newswire: e& and AWS Sovereign Launchpad live](https://tools.prnewswire.com/en-us/live/20813/release/20251104EN14952) | 4 Nov 2025 |
| S116 | [e&: e& UAE and Core42 sovereign AI infrastructure](https://www.eand.com/en/news/20-07-26-eand-uae-core42-sovereign-ai-infrastructure.html) | 20 Jul 2026 |
| S117 | [Microsoft: TAMM app, Abu Dhabi government services (Azure OpenAI + G42 Compass)](https://news.microsoft.com/source/emea/features/tamm-app-abu-dhabi-government-services/) | 2025 (undated page) |
| S118 | [FAB: FAB and Microsoft announce strategic partnership](https://www.bankfab.com/en-ae/about-fab/group/in-the-media/fab-and-microsoft-announce-landmark-strategic-partnership) | 2 Apr 2024 |
| S119 | [DEWA: Rammas with ChatGPT technology](https://www.dewa.gov.ae/en/about-us/media-publications/latest-news/2023/02/chatgpt-technology) | 8 Feb 2023 |
| S120 | [Abu Dhabi Media Office: Miral partners with Microsoft](https://www.mediaoffice.abudhabi/en/tourism/miral-partners-with-microsoft-to-enhance-customer-experiences-in-abu-dhabis-culture-and-leisure-sectors/) | 8 May 2023 |
| S121 | [Emirates: Emirates Group collaborates with OpenAI](https://www.emirates.com/media-centre/emirates-group-collaborates-with-openai-to-accelerate-ai-adoption-and-innovation/) | 21 Nov 2025 |
| S122 | [Digital Dubai: LLM-as-a-service for government entities](https://connect.smartdubai.ae/Services/Details/6d80cad8-5a12-4caa-99c8-ced38919893f) | read 2 Oct 2026 |
| S123 | [DCPost: Microsoft expands partnership with Majid Al Futtaim](https://www.dcpostmea.com/2023/10/microsoft-expands-partnership-majid-al-futtaim/) | Oct 2023 |
| S125 | [flydubai: flydubai and AWS announce collaboration](https://news.flydubai.com/flydubai-and-amazon-web-services-aws-announce-collaboration) | 15 Dec 2025 |
| S126 | [UAE Federal Decree-Law 45/2021 (PDPL), official text; DLA Piper UAE data protection summary](https://uaelegislation.gov.ae/en/legislations/1972) | official text; DLA Piper 27 Jan 2025 (dlapiperdataprotection.com) |
| S127 | [Law-firm briefings on PDPL transfers and the 2026 Federal Authority for AI and Data: Clifford Chance (10 Mar 2025), Chambers UAE guide (10 Mar 2026), Morgan Lewis (15 Jun 2026), itsecnow check of the legislation portal (23 Sep 2026)](https://www.dlapiperdataprotection.com/countries/uae-general/law.html) | URLs of the other briefings not captured; publisher and date as listed |
| S128 | [UAE National Cloud Security Policy (Cyber Security Council) on u.ae](https://u.ae/) | page updated 18 Jun 2026 (exact URL not captured) |
| S129 | [AWS: DESC CSP Security Standard (Dubai government cloud)](https://aws.amazon.com/compliance/desc_csp_security_standard/) | undated; read 2 Oct 2026 |
| S130 | [DIFC Data Protection Law 2020 Arts. 26–27 and Regulation 10 (DIFC site; Baker McKenzie Cloud Compliance Center)](https://www.difc.com/) | Reg. 10 consultation 18 Jun 2026; exact URL not captured |
| S131 | [ADGM Data Protection Regulations 2021, guidance Part 6 (transfers)](https://assets.adgm.com/) | undated; exact URL not captured |
| S132 | [CBUAE outsourcing regulation and consumer protection (data localisation); CBUAE AI guidance note](https://www.centralbank.ae/) | Circular 14/2021; AI note 23 Feb 2026; exact URL not captured |
| S133 | [Microsoft Learn: deployment types (Global, Data Zone, Standard, Provisioned)](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types) | updated 12 Aug 2026 |
| S134 | [Microsoft Learn: data, privacy and security for Azure OpenAI](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy) | 5 Jun 2026 |
| S136 | [Oracle: Oracle Alloy sovereign cloud (du National Hypercloud)](https://www.oracle.com/ae/news/announcement/blog/oracle-alloy-enables-offer-sovereign-cloud-capabilities-2025-07-02/) | 2 Jul 2025 |
