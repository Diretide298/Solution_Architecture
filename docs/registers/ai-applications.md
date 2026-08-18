# TICVAI — AI Application Register

**Version:** 1.0
**Date:** 12 August 2026
**Source:** `Ticvai_matrix_20260621_2.xlsx` (all sheets) + MoM decisions 30 Jul – 12 Aug 2026
**Status:** Reference register. Entries are scope only where traced to a Requirement ID or a dated MoM decision.

---

## 1. Headline Finding

**399 of 3,184 requirements (12.5%) are AI-related, spread across 19 of 21 domains.**

AI is not a module. It is a capability layer consumed by nearly every domain in the
platform. Only 232 of those requirements sit inside the *Unified Operations Dashboard*
domain; the remaining **167 are scattered across 18 other domains** — seat map import,
resource scheduling, wallet monitoring, procurement, permission review, access control,
digital asset tagging.

Two consequences:

1. **Treating AI as a Wave-3 module is wrong.** Guest checkout, POS upsell, seat map
   import and fraud screening all carry AI requirements inside Wave-1 and Wave-2 flows.
2. **The AI service must be a shared platform, not a set of features.** Forty-plus
   distinct applications sharing one governance, logging, consent and cost-attribution
   layer — built once, or rebuilt forty times.

### Distribution

| Domain | AI reqs | Share of domain |
|---|---|---|
| Unified Operations Dashboard | 232 | 70% |
| Marketing & CRM | 62 | 19% |
| Seat Management & Venue Mapping | 20 | 18% |
| Ticketing Catalogue | 27 | 9% |
| Ticketing Sales | 11 | 3% |
| Admission and Access | 8 | 4% |
| F&B & Guest Management | 10 | 2% |
| Bundles and Promotions | 12 | 5% |
| Subscription & Licensing | 7 | 12% |
| Inventory Management | 7 | 7% |
| Approval Workflows | 6 | 8% |
| Employee Mobile App | 5 | 10% |
| F&B POS | 3 | 2% |
| Retail POS · Guest Mobile App · Developer API · Device Mgmt · Maintenance · DAM | 10 | — |

---

## 2. Register

Type key: **LLM** generative/conversational · **ML** predictive/statistical ·
**CV** computer vision · **NLP** classification/extraction · **OPT** optimisation

### 2.1 Conversational & Assistive — 8

| ID | Application | Purpose | Module / Domain | Refs | Type | Wave |
|---|---|---|---|---|---|---|
| AI-01 | **Platform Conversational Assistant** | Natural-language assistance across every module; multilingual; tenant-, venue- and role-specific configuration | Unified Ops / AI Engine | 8.4.1–8.4.9 | LLM | 2 |
| AI-02 | **Guest AI Concierge** | Itinerary help, venue info, purchase assistance in the guest-app app | Guest Mobile App | 19.2.72; 10 Aug §4.2 | LLM | 2 |
| AI-03 | **Omnichannel AI Chatbot** | FAQs, purchases, recommendations across WhatsApp, web chat, app chat, Messenger, Instagram, email, SMS — with live-agent handover preserving context | Marketing & CRM | 22.8.4, 22.8.5; 19.2.68; 12 Aug §10 | LLM | 2 |
| AI-04 | **Kiosk AI Assistant** | Guides guests through selection, promotions, FAQs, checkout | Ticketing Sales | 2.1.28 | LLM | 3 |
| AI-05 | **POS AI Assistant** | Cashier queries — promo code lookup, refund process, theme switching | POS *(MoM only)* | 03 Aug §65 | LLM | 2 |
| AI-06 | **Employee Assistant + Voice** | Voice-driven operational queries, work-order assistance, knowledge base | Employee Mobile App | 18.10.1–18.10.5 | LLM | 2 |
| AI-07 | **Call Centre Agent Assist** | Live upsell/cross-sell prompts from guest-app profile during a call | Ticketing Sales | 2.8.3 | LLM | 3 |
| AI-08 | **AI Financial Assistant** | Natural-language reporting for accountants and finance managers | Finance *(MoM only)* | 12 Aug §22 | LLM | 3 |

> AI-01 is the substrate for AI-02, AI-04, AI-05, AI-06 and AI-08. Build the assistant
> framework once with role- and tenant-scoped tool access; the others are configurations
> of it, not separate products.

### 2.2 Generative & Authoring — 10

| ID | Application | Purpose | Module / Domain | Refs | Type | Wave |
|---|---|---|---|---|---|---|
| AI-09 | **Catalogue Generation from Documents** | Upload spreadsheets, brochures, PDFs or price lists; generate products, pricing structures, rules and entitlements | Ticketing Catalogue | 1.1.41, 1.4.21 | LLM | 3 |
| AI-10 | **Event Configuration Generation** | Upload event briefs, schedules or spreadsheets; generate event configurations and sessions | Ticketing Catalogue | 1.3.31 | LLM | 3 |
| AI-11 | **AI Venue Designer** | Generate seat maps from prompts and floor plans; event-specific layouts for concerts, sports, exhibitions | Seat Mgmt / Catalogue | 21.2.17; 1.4.22, 1.4.23 | LLM+CV | 3 |
| AI-12 | **AI Website Builder** | Upload logos, brand guidelines, brochures, decks; generate a complete white-label site with navigation, pages and content | Marketing & CRM | 22.10.16; 2.6.50 | LLM | 3 |
| AI-13 | **Mobile App Content Builder** | Generate app homepages, menus, banners, announcements and content structures | Marketing & CRM | 22.10.17 | LLM | 3 |
| AI-14 | **Marketing Content Generation** | Email bodies, SMS, WhatsApp templates, push notifications, landing pages, promotional offers | Marketing & CRM | 22.3.18, 22.4.9, 22.9.17, 22.10.14 | LLM | 3 |
| AI-15 | **Subject Line Generation & Testing** | Generate and A/B test subject lines, notification titles, campaign messaging | Marketing & CRM | 22.1.17, 22.4.10 | LLM | 3 |
| AI-16 | **AI Translation** | Initial translation of website, newsletter and notification content with human review before publish | Marketing & CRM / Sales | 2.6.34, 22.4.11, 22.9.18, 22.10.15 | LLM | 2 |
| AI-17 | **SEO Optimisation** | Recommend titles, descriptions, keywords, content improvements and internal links | Marketing & CRM | 22.11.3, 22.11.9 | LLM | 3 |
| AI-18 | **Dynamic SEO Metadata** | Auto-generate metadata for events, attractions, memberships, ticket types, promotions | Marketing & CRM | 22.11.2 | LLM | 3 |

### 2.3 Forecasting & Prediction — 9

| ID | Application | Purpose | Module / Domain | Refs | Type | Wave |
|---|---|---|---|---|---|---|
| AI-19 | **Attendance & Demand Forecasting** | Forecast attendance by venue, attraction, event, session, date range, day, month, season | Unified Ops | 8.2.1–8.2.58 (58) | ML | 3 |
| AI-20 | **Queue Congestion Forecasting** | Forecast congestion and capacity utilisation for attractions, counters and service locations | F&B & Guest / Virtual Queue | 5.6.37 | ML | 3 |
| AI-21 | **Inventory Demand Forecasting** | Forecast inventory demand, consumption and seasonal demand | Inventory Management | 15.4.1–15.4.3 | ML | 3 |
| AI-22 | **F&B Production Forecasting** | Forecast production quantities from historical demand and attendance | Bundles & Promotions / F&B | 4.8.14, 4.8.19 | ML | 3 |
| AI-23 | **Food Waste Prediction** | Predict potential waste and recommend mitigating actions | Bundles & Promotions / F&B | 4.8.15, 4.1.19 | ML | 3 |
| AI-24 | **Staffing & Resource Forecasting** | Forecast staffing requirements, event resource needs and future resource demand | Ticketing Catalogue / Resource Mgmt | 1.2.39, 1.2.48, 1.2.55 | ML | 3 |
| AI-25 | **Seat Demand & Revenue Forecasting** | Forecast seat demand, seat inventory and revenue by section | Seat Management | 21.11.2–21.11.4 | ML | 3 |
| AI-26 | **Churn & Disengagement Prediction** | Identify guests at risk of inactivity, cancellation or reduced spend; recommend retention actions | Marketing & CRM / Loyalty | 22.2.23, 22.14.13, 5.4.22 | ML | 3 |
| AI-27 | **Platform Usage Forecasting** | Forecast tenant platform consumption for subscription planning | Subscription & Licensing | 20.8.3 | ML | 3 |

### 2.4 Pricing & Optimisation — 7

| ID | Application | Purpose | Module / Domain | Refs | Type | Wave |
|---|---|---|---|---|---|---|
| AI-28 | **Dynamic Pricing Engine** | Demand-, occupancy-, availability-, seasonal-, event-, day-, time-slot- and segment-based pricing | Unified Ops | 8.5.1–8.5.46 (46) | ML+OPT | 3 |
| AI-29 | **Discount Assistant** | Recommend seasonal, early-bird, bulk and last-minute discount structures | Unified Ops | 8.1.1, 8.1.6 | OPT | 3 |
| AI-30 | **Pricing Recommendations** | Recommend adjustments from demand forecasts, occupancy, sales performance, seasonality, holidays, weather; suggest pricing per seat category | Ticketing Sales / Catalogue | 2.9.18, 1.4.27 | ML+OPT | 3 |
| AI-31 | **B2B Allocation Optimisation** | Optimise inventory and quota allocation across partners by sales performance, demand and unused allocation | Ticketing Sales / B2B | 2.7.54 | OPT | 3 |
| AI-32 | **Schedule Optimisation** | Optimise resource schedules automatically; propose alternatives for conflicts; simulate scenarios | Ticketing Catalogue / Resource Mgmt | 1.2.56–1.2.58 | OPT | 3 |
| AI-33 | **Send-Time Optimisation** | Determine optimal communication time per guest-app from engagement, location, language and behaviour | Marketing & CRM | 22.3.19, 22.9.16 | ML | 3 |
| AI-34 | **Offer Optimisation** | Recommend discounts, promotions, rewards and bundles maximising conversion within business constraints | Marketing & CRM | 22.3.20, 3.6.40 | OPT | 3 |

### 2.5 Recommendation & Personalisation — 9

| ID | Application | Purpose | Module / Domain | Refs | Type | Wave |
|---|---|---|---|---|---|---|
| AI-35 | **Product Recommendation Engine** | Personalised ticket, membership, attraction, event and package recommendations; next-best-offer; checkout recommendations | Unified Ops | 8.6.1–8.6.36 (36) | ML | 2 |
| AI-36 | **Upsell & Cross-Sell Engine** | Recommendations during booking and checkout from cart contents, guest-app profile and context; **synchronised across B2C, B2B, app, POS, kiosk, call centre, API, membership, loyalty, wallet** | Admission / Sales / Bundles | 3.7.5, 3.7.9, 3.7.12, 2.1.22, 4.4.30, 1.1.33–1.1.35 | ML | 2 |
| AI-37 | **Bundle Recommendations** | Recommend bundle combinations from historical sales, behaviour, demographics, seasonality and attraction popularity | Admission / Bundles | 3.5.13, 4.1.14, 4.1.15 | ML | 3 |
| AI-38 | **Next Best Action** | Recommend the next action, offer, campaign, membership, reward or product per guest-app | Marketing & CRM / Loyalty | 22.2.24, 5.4.23, 5.4.33 | ML | 3 |
| AI-39 | **Seat Recommendations** | Best seat, best value, closest-to-stage, family seating, accessibility, seat upgrade; interactive selection assistant | Seat Management | 21.10.1–21.10.6, 21.5.22 | ML | 2 |
| AI-40 | **Membership Upgrade Recommendations** | Analyse profile, purchase history, visit frequency, spend and loyalty to recommend upgrades and renewals | Ticketing Sales / Membership | 2.14.18, 3.7.8 | ML | 3 |
| AI-41 | **Loyalty Reward Recommendations** | Personalised rewards, campaigns, offers, challenges and achievements | F&B & Guest / Marketing | 5.4.21, 22.6.18, 22.6.19 | ML | 3 |
| AI-42 | **Resource Recommendations** | Recommend optimal resources and suitable staff by skills and availability | Ticketing Catalogue / Resource Mgmt | 1.2.53, 1.2.54 | ML | 3 |
| AI-43 | **Procurement & Replenishment Recommendations** | Procurement, reorder and putaway recommendations; auto-generated replenishment from forecasts and stock levels | Inventory Management | 15.4.5, 15.4.6, 15.2.9, 4.8.18 | ML | 3 |

### 2.6 Detection & Risk — 6

| ID | Application | Purpose | Module / Domain | Refs | Type | Wave |
|---|---|---|---|---|---|---|
| AI-44 | **Payment Fraud Detection** | Abnormal payment activity, excessive failed attempts, high-risk transactions, unusual values and patterns, blocked countries, high-risk IPs, risk scoring | Unified Ops | 8.3.1–8.3.54 (54) | ML | 2 |
| AI-45 | **Wallet Fraud Detection** | Unusual top-ups, abnormal spending, account sharing | Bundles & Promotions / Wallet | 4.3.32 | ML | 3 |
| AI-46 | **Access Anomaly Detection** | Detect anomalous access behaviour; AI-assisted access-policy recommendations | Admission and Access | 3.3.45, 3.3.46 | ML | 3 |
| AI-47 | **Permission Risk Analysis** | Recommend user provisioning, permission optimisation, excessive-privilege detection, access reviews | F&B POS / Retail POS | 7.1.35, 7.1.56 | ML | 3 |
| AI-48 | **Approval Risk & Priority Scoring** | Risk assessments, priority scoring and escalation recommendations for approval requests | Approval Workflows | 11.1.72–11.1.75 | ML | 3 |
| AI-49 | **Operational Anomaly Detection** | Identify operational risks, congestion, capacity issues, device failures, staffing shortages and service disruptions with recommendations | Unified Ops / Command Centre | 8.9.9 | ML | 3 |

### 2.7 Understanding & Classification — 7

| ID | Application | Purpose | Module / Domain | Refs | Type | Wave |
|---|---|---|---|---|---|---|
| AI-50 | **Review Analysis** | Sentiment classification, topic detection, issue detection and summarisation across review volumes | Marketing & CRM | 22.5.9–22.5.12 | NLP | 3 |
| AI-51 | **Survey Analysis** | Sentiment, emotions, topic detection and insight generation from free-text responses | Marketing & CRM | 22.7.16–22.7.18 | NLP | 3 |
| AI-52 | **Audience Discovery & Classification** | Auto-classify guests into audiences; discover high-value clusters and hidden patterns; generate lookalike audiences | Marketing & CRM | 22.2.25, 22.14.11, 22.14.12, 5.4.24 | ML | 3 |
| AI-53 | **Guest Insights** | Predicted next visit, churn risk, preferred products and attractions, lifetime value, upsell opportunities | Marketing & CRM / Profile | 22.2.22, 5.3.25 | ML | 3 |
| AI-54 | **Seat Map Recognition** | Detect sections, rows, seats, aisles and premium zones from uploaded plans; generate numbering; validate maps; suggest corrections | Seat Management | 21.2.7–21.2.14 | **CV** | 3 |
| AI-55 | **Seat Map Validation & QA** | Identify duplicate seat numbers, missing rows, incorrect category assignment, accessibility compliance gaps; bulk categorisation across thousands of seats | Ticketing Catalogue / Seat Mgmt | 1.4.26, 1.4.29, 1.4.30 | CV+OPT | 3 |
| AI-56 | **Digital Asset Intelligence** | Semantic search over assets via natural language; auto-generate tags, keywords and classifications | Digital Asset Management | 23.1.6, 23.1.7 | NLP+CV | 3 |

### 2.8 Analytics & Reporting — 2

| ID | Application | Purpose | Module / Domain | Refs | Type | Wave |
|---|---|---|---|---|---|---|
| AI-57 | **Natural Language Reporting** | Query reports conversationally; AI-generated dashboards and analytics views | Unified Ops / BI | 8.7.10, 8.7.30, 8.7.31 | LLM | 3 |
| AI-58 | **Forecasting Analytics** | Forecast views embedded in the BI layer | Unified Ops / BI | 8.7.26 | ML | 3 |

### 2.9 Configuration & Onboarding — 2

| ID | Application | Purpose | Module / Domain | Refs | Type | Wave |
|---|---|---|---|---|---|---|
| AI-59 | **AI Setup Wizard** | AI-assisted tenant onboarding | Subscription & Licensing | 20.1.3 | LLM | 3 |
| AI-60 | **Subscription Optimisation** | Recommend optimal plans, marketplace modules, upgrades and cost-optimisation opportunities | Subscription & Licensing | 20.8.1, 20.8.2, 20.8.4, 20.8.5 | ML | 3 |

### 2.10 Governance — 6 (cross-cutting, **mandatory**)

Not features. Preconditions. **No AI application in §2.1–2.9 may ship before these exist.**

| ID | Application | Purpose | Module / Domain | Refs | Wave |
|---|---|---|---|---|---|
| AI-61 | **Prompt, Response & Action Logging** | Store every prompt submitted, every response generated and every action taken | Unified Ops / AI Governance | 8.1.2, 8.1.3, 8.3.55–8.3.57 | **1** |
| AI-62 | **Approval Before Execution** | AI recommendations affecting pricing, promotions, financial or operational changes require human approval before execution | Unified Ops / Approval Workflows | 8.1.4, 8.3.61–8.3.63, 11.1.37 | **1** |
| AI-63 | **Explainability & Confidence** | Provide reasoning and confidence indicators with AI output | Unified Ops | 8.1.5 | **1** |
| AI-64 | **AI Audit Trail** | History of AI-generated actions, decisions, executions and the user decisions taken against them | Unified Ops | 8.1.6, 8.3.58–8.3.60 | **1** |
| AI-65 | **AI Usage Analytics** | Reporting on AI usage and outcomes; underpins per-tenant cost attribution | Unified Ops | 8.1.7 | **1** |
| AI-66 | **AI Consent Controls** | Tenant admin control over use of guest-app data in recommendations, personalisation, segmentation and prediction; guest-level consent for AI processing | Marketing & CRM / Consent | 22.13.9, 22.13.19 | **1** |

### 2.11 Exposure — 1

| ID | Application | Purpose | Module / Domain | Refs | Wave |
|---|---|---|---|---|---|
| AI-67 | **AI Services API** | Expose forecasting, recommendations, dynamic pricing, fraud detection and assistant functions to partners | Developer & API Mgmt | 13.3.12, 13.3.13 | 3 |

---

## 3. Non-Negotiables

Apply to every entry above. Derived from the matrix, MoM decisions and the Project Direction.

| # | Rule | Basis |
|---|---|---|
| 1 | **AI never writes to the transactional database.** Read-only, scoped by the caller's resolved permission set | An AI capability must not become a permission bypass |
| 2 | **Tenant isolation is the cell where a cell holds one tenant, and a dedicated shard where it does not** | **Corrected 17 August, ADR-0021 and CF-97.** The original rule was right about shared placement for the wrong stated reason. A collection is per embedding model, not per tenant — a collection carries its own vector configuration and a shard cannot |
| 3 | **All AI data stays in-jurisdiction** — vector stores, prompt logs, training data | Project Direction §3.3.10; CF-20 |
| 4 | **No provider SDK calls in application code** | Provider swap must be configuration, not a rewrite |
| 5 | **Every response carries trace ID, model version, token count and retrieval sources** | AI-65; cost attribution for CF-14 |
| 6 | **No application ships without an eval baseline**, regression-gated in CI | Hallucination in a pricing or refund path is a financial defect |
| 7 | **Anything affecting price, refund, entitlement or financial state is recommendation-only** until a human approves | AI-62 |
| 8 | **PII scrubbed on ingress and egress**, with audit trail | 10 Aug §4.2 |
| 9 | **Guest data use in AI is consent-gated** at tenant and guest-app level | AI-66 |

---

## 4. Open Questions

| ID | Question | Owner |
|---|---|---|
| CF-14 | Token billing model — who pays, how metered, how surfaced to tenants | Both — dedicated workshop |
| CF-20 | Vector store residency (Qdrant vs pgvector); UAE ruling pending | Allam — Compliance Authority |
| **New** | **AI-11 / AI-54 require computer vision on uploaded floor plans.** This is a different capability class from the LLM and ML work and needs its own model strategy | Chinmay |
| **New** | **AI-28 Dynamic Pricing has no stated guardrails** — floor/ceiling prices, maximum move per period, fairness constraints. 46 requirements describe the mechanism, none the limits | Qossai |
| **New** | **AI-36 requires upsell synchronisation across 10 channels** (3.7.12). That is an architectural constraint on the recommendation service, not a feature | Chinmay |

---

## 5. Coverage Contribution

| | Before | After |
|---|---|---|
| AI requirements with a mapped capability | ~40 of 399 (10%) | **399 of 399 (100%)** |
| Capability catalogue entries | 40 | 40 + 67 AI = **107** |
| Matrix requirements covered | 1,827 (57.4%) | **2,186 (68.7%)** |

Remaining uncovered after this register: **998 requirements (31.3%)** — concentrated in
finance and ledger (225), seat management non-AI (92), guest-app authentication (81),
marketing non-AI (257), developer platform (92), subscription non-AI (52), resource
management non-AI (73), and product lifecycle and resale (49).

Those are addressed by capabilities C41–C83 in the main catalogue, which is the next
artefact to complete.
