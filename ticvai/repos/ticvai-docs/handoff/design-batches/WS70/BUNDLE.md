# WS70 — Unified BI Reporting and AI Analytics Platform board 9

**10 screens · 24 operations · 48 schemas · 5 permissions**

Platform P16 Venue Analytics · ships as **venue-management** ·
staff audience · web ·
online only

## Who this is for

**staff on web.** Everything below is how you know what is
true. **None of it is the subject.** The subject is the person in front of the screen and the one
thing they came to do.

## What to build

**A working surface, not a drawing of one.** Two references, both built from these same sources:

- `sources/designs/TICVAI_Mobile.dc.html` — 54 screens in one navigable file, 133 animations,
  a live seat map, a five-stage payment flow. **This is the bar for finish.**
- `sources/designs/TICVAI_POS_Terminal_client_approved.html` — the client-approved POS build. **This is the bar for operator density.**

`sources/designs/ticvai-motion-and-interaction.md` names every mechanism in them. Open them and
match their depth. Do not describe them, read them.

## The one rule that outranks the rest

**Nothing in this bundle may appear as text a user can read.** Not an operation id, not a schema
field name, not a permission key, not a screen id, not a file path, not a finding reference.

A homepage that prints `getTenantAppStatus → listProducts` under its header, or labels a column
`venueId · scopePath`, has published its own homework. It happened on `WEB-001`: four products on
sale and not a single price on the page, because the build rendered what `listProducts` returns
instead of what a guest wants — a photo, a name, a price, and a way to book.

**The test: would the person this screen is for understand every word on it?** If a line would
confuse them, it is spec leakage, not design. `bindsTo` tells you what data to invent
convincingly. It is never a caption.

## What is in this folder

| file | what it is |
|---|---|
| `BUNDLE.md` | **The one file to hand a design session.** This brief; then **Screen by screen**, a full specification of each screen (what the user enters and picks, what it shows and produces, every state, who may do what, the requirements it meets, what the client said about it in the meetings, the tracker items, what the tenant configures, the references and an acceptance checklist); then what applies to the whole batch; then the raw data. |
| `screens.json` | Every field of every screen in the batch, as the package holds it. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `AI_AUDIT_VIEW, AI_CONFIGURE, AI_USE, REPORT_MANAGE, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.
- **How input should be, how output should be.** Each screen's block in `BUNDLE.md` says, field by
  field, the control, whether it is required, its default, its limits and allowed values, its format
  and its error; and, element by element, what is shown and in what format, what each action
  produces and where the user goes next. Draw exactly that.

## The processes these screens belong to

Written by the owner of each process (`handoff/design-notes/`). Read before any screen: it says how the process runs end to end and which words the screens must use.

### Finance, Ledger & Tax · Reporting & Analytics

Finance and insights run underneath every sale. A sale at a till (P04), kiosk, web storefront (P01) or guest app (P02) is priced and taxed per line at the moment of sale, recorded in the venue's base currency (AED in the UAE; 2 decimals, or 3 for BHD, KWD and OMR, never rounded away), and posted to an append-only dual ledger through account mappings per money event; anything unmapped lands in suspense. Tax follows the jurisdiction's tax profile: inclusive or exclusive, compound where a tax applies on another, zero-rated or exempt with verified evidence, and computed on the discounted price by default or on the price before discount where the region requires it (Egypt). A guest may select a currency the venue charges and pay in it: the rate is locked on the order, the payment partner is asked in that currency, the ledger keeps the base amount with the rate, and a refund goes back in the currency paid (decided 2 October 2026, Chinmay); a currency shown but not charged is an approximate price. Foreign cash at a till is recorded at its base equivalent and change is given in base currency. A paid order can carry a VAT receipt (simplified tax invoice), a full tax invoice with the buyer's TRN, or a consolidated invoice for a company, each numbered without gaps and never edited; corrections are credit memos. Revenue is recognised by rule: POS-style immediate, tickets on the visit, gift cards and wallet on use, annual passes straight-line or per visit, breakage on expiry; deferred revenue is a balance that ages. Each venue's day is reconciled (POS cash, gateways, bank, wallet against the ledger, provider files matched automatically, only genuine mismatches to a person); chargebacks are defended against the bank's deadline; month end runs seven close checks and goes to a finance approver. Nothing posted is deleted: a correction is a reversal, an approver is never the preparer, and ledger approval needs a second factor. Back-office finance lives in Venue Management (P08: chart of accounts, mapping, FX, journals, recognition, reconciliation, period close, chargebacks); tax profiles, calculation validation and platform reconciliation in the TICVAI Console (P09); partner settlement in P10. Reporting is one consolidated, permission-based area (Analytics, P16): seeded standard dashboards and reports plus no-code builders over a governed business catalogue; the P08 report screens, the POS terminal day view and the kitchen performance view are scoped windows onto the same definitions and must show the same numbers. Every figure is read from a lag-tolerant reporting copy and shows its "as of" time; scope comes from the person's rights, never from a filter; AI explains and recommends but never acts, answers only within the person's role, labels forecasts, and is phase two for finance ledgers.

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Base currency | The venue's region currency; the currency every record and ledger posting is in. A guest may pay in a currency they select (where the venue charges it); the books still hold the base amount and the rate. | Home currency, Local price, Default currency | DI-211 / DI-282 / contracts/spine/orders.yaml#/components/schemas/Order |
| Pay in USD (a currency the venue charges) | The guest's selected payment currency; the card is charged in it at the rate locked on the order, and refunds go back in it. | Converted price, Approx. (for a charged currency) | contracts/spine/orders.yaml#checkoutCart / … |
| ≈ (approx.) price in USD / SAR / … | A conversion of a base-currency price for a currency the venue shows but does not charge, always next to the base price. | Converted price, USD price | DI-211 / screens/P02-guest-mobile-app.yaml#GST-044 |
| Takings | Money received in the period less refunds (cash-basis); the seeded KPI on hubs. | Revenue, Sales, Income | contracts/satellite/reporting.yaml#/components/schemas/ReportingSystemKpi / R283 |
| Gross sales | Issued sales before discounts and refunds; whether tax is included must be stated on the tile. | Revenue, Turnover | MATRIX 6.1.78 |
| Net revenue | Gross sales less discounts less refunds, adjusted per finance policy. | Net sales, Revenue, Income | MATRIX 6.1.78 |
| Recognised revenue / Deferred revenue | Earned under the recognition rules / paid for but not yet earned. Kept distinct from sales. | Realised revenue, Unearned income, Wallet revenue | MATRIX 5.12.6 / DI-260 / contracts/spine/finance.yaml#getDeferredRevenue |
| VAT receipt | The simplified tax invoice issued on a paid order. | Receipt (when it is a tax document), Bill | contracts/spine/finance.yaml#issueTaxInvoice |
| Tax invoice / Combined tax invoice | A full invoice with the buyer's details / one invoice for several paid orders of one buyer. | Bill, Statement | contracts/spine/finance.yaml#/components/schemas/FinTaxInvoiceType |
| Credit memo | The document that corrects an issued invoice after a refund; the invoice itself is never edited. | Credit note (until the client's tax adviser chooses "Tax credit note"), Edit invoice | contracts/spine/finance.yaml#/components/schemas/FinTaxInvoice |
| VAT (or the jurisdiction's tax name) | Use the tax profile's own name on every surface; "Tax" only where several kinds are summed. | GST in UAE, Service charge for a tax | contracts/spine/catalogue.yaml#setTaxProfileJurisdiction |
| Price before discount | The taxable base where the jurisdiction taxes the undiscounted price. | Gross price, List tax | DI-598 |
| Post / Reverse | A journal reaches the ledger when approved and posted; a correction is a reversal, never an edit or delete. | Edit entry, Delete entry, Undo | contracts/spine/finance.yaml#reverseJournalEntry |
| Period (Open / Closing / Closed) | A fiscal period's state; closing stops postings, closed locks them. | Month locked, Frozen | contracts/spine/finance.yaml#/components/schemas/PeriodStatus |
| Variance (Over / Short) | The difference between expected and counted or recorded, always saying between which two figures. | Discrepancy, Error, Loss | DI-275 / contracts/spine/finance.yaml#/components/schemas/UnifiedReconciliation |
| Settlement / Exception / Resolve | A provider's file for a day / a line that did not match / the recorded explanation. | Payout file, Error, Close | contracts/spine/finance.yaml#/components/schemas/SettlementException |
| Chargeback | A bank-initiated reversal with an evidence deadline; not a refund. | Dispute refund, Reversal | contracts/spine/orders.yaml#/components/schemas/Chargeback |
| Report / Dashboard / Tile / KPI | A runnable, exportable, schedulable definition / a page of tiles / one visual bound to a report / a company-wide measure defined once. | Widget (outside the builder's library), Board (for a user-facing dashboard) | contracts/satellite/reporting.yaml#/components/schemas/DashboardTile / … |
| Warning / Critical | KPI status bands set by a target's amber and red thresholds; always words plus colour. | Amber, Red (alone), Bad | contracts/satellite/reporting.yaml#/components/schemas/KpiTarget |
| As of HH:MM / Updated N sec ago | The freshness of every figure read from the reporting copy; stale shows a warning. | Live (unless refreshed), Real-time | MATRIX 8.7.22 |
| Forecast | Any projected figure, with its range; never shown as a fact. | Expected, Will be | DI-973 |
| Outlet / Workstation (till) | A sales point / the device; staff copy may say "till" for the workstation. | Store, POS (in copy), Drawer (for the device) | R156 |
| Channel | POS, Web, App, Kiosk, B2B, OTA, from one closed list. | Source, Platform | MoM 2026-08-18 4.2 Recipes, Operating Hours & Service Channels / MATRIX 1.4.7 |

### AI & Intelligence

AI in TICVAI is one governed engine behind many screens. The guest meets it as Sahli, the concierge (WEB-044, GST-031, GST-033), as the planner agent that refines a rules-built day plan by chat (GST-054), and as upsell and cross-sell offers on a separate Extras step (WEB-008, GST-048). Staff meet it as the Staff App's AI tab (EMP-019/020, knowledge EMP-040/041), the kiosk assistant (KSK-015) and the support copilot (SUP-006, SUP-018). Venue managers meet it in Venue Management (BO-091 policy and spend, BO-919/BO-925..932 resource and staffing forecasts, BO-597/598 configuration drafts, BO-772/782 marketing optimisation, BO-793 translations, BO-970/975 seat-map generation, BO-1048 seat upsell, BO-1160 fraud cases) and in Analytics (ANL-010 suggestions, ANL-019 management insights, ANL-055 anomalies, ANL-057 forecasting studio, ANL-059 insight history, ANL-060 governance, ANL-071 AI maturity). The governance, configuration-assistant, forecasting, oversight, audit and monitoring boards sit on the TICVAI Console (P09: ADM-037 providers, ADM-469..498 configuration assistant, ADM-499..518 forecasting, ADM-519..558 governance, ADM-633/637 fraud, ADM-680..697 recommendation governance). Five rules hold on every one of these screens. (1) Baseline first, then it learns per tenant: every data-driven answer (forecast, suggestion, risk score, recommendation) exists from day one, from the venue AI profile, a starting pattern for the venue type, the UAE calendar and the weather, and shifts to the venue's own data as it trades; nothing says "comes later" or refuses for lack of history - a refusal only names a missing setting. (2) Every answer shows its basis and maturity: a "Based on" line, a stage badge (Starting, Learning, Established, Trained on your data), "Limited historical data" while the starting pattern carries more than half the weight, ranges or bands rather than a bare percentage, a confidence only where the producer really has one, a plain-words explanation always. (3) A trained model replaces the baseline only when it beats it in a shadow run of at least six weeks and an admin promotes it; the platform raises "Ready to promote" and never switches by itself. (4) The LLM never reads raw data: numbers come only from query results the platform runs (the answer shows the query), only the masked prompt and retrieved context leave the platform, and AI only drafts - the owning screen applies. (5) One autonomy scale, L0 Disabled to L4 Controlled auto, with first-release ceilings, separate from user permission and from the approval tier; impactful actions route to a person, who sees current against proposed, impact, risk and what is affected, and can approve within a limit, challenge, override or roll back; every decision is traceable (data, model, approver, time) and searchable by customer, venue and capability. In Block A (5 October to 20 November 2026) the guest concierge with retrieval, Help me choose, translations, the planner agent, the gateway and …
*(source: ADR-0051; ADR-0050; ADR-0020; ADR-0052; ADR-0053; ADR-0054; ADR-0059; ADR-0051 (AI-D01..AI-D20); ADR-0051 (AI functions review 30 Sep §2 §4 §9); MoM 18 Sep 4.1-4.10; MoM 21 Sep 4.1-4.14; MoM 30 Sep 4.1 4.7; ADR-0059 (Block A slice: tasks.csv))*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Sahli | The guest concierge's name; the entry reads "Ask Sahli" and shows as mascot art when the venue's Concierge mascot setting is on (default), otherwise a plain button. | Chatbot, Bot, AI Concierge (as a visible label), Virtual agent | DI-1069 / screens/P01-guest-web-storefront.yaml#WEB-044 |
| Based on | The line on every AI answer that says what it was computed from, e.g. "Based on: your venue profile, UAE calendar, weather, 23 days of your sales". Always present. | Data sources, Model inputs, Powered by AI | ADR-0051 Maturity / contracts/satellite/ai.yaml#/components/schemas/AiMaturity |
| Starting / Learning / Established / Trained on your data | The four maturity stages (enum starting, learning, established, learned), shown as one badge. Moves by itself from Starting to Established as own data arrives; Trained on your data only after an admin promotion. | Beta, Experimental, Low confidence, Cold start (in UI), Not enough data | ADR-0051 / ADR-0051 (AI functions review 30 Sep §2) |
| Limited historical data | Shown while own data carries less than half the weight (AiMaturity.limitedHistory, ownDataShare < 0.5). An honest qualifier, never a refusal. | Insufficient data, Not available until, Comes later | ADR-0051 / contracts/satellite/ai.yaml#/components/schemas/AiMaturity |
| Range | The 10th-90th percentile band a forecast or estimate is shown with (e.g. "1,850-3,400 guests, most likely 2,600"). Never a bare accuracy percentage on an answer; measured accuracy (WAPE, bias, coverage) appears only on accuracy screens … | Accuracy 92%, Confidence 0.87 (on a heuristic), Exact | ADR-0051 / contracts/satellite/ai.yaml#getForecast / … |
| Running in the background | A trained model in shadow next to the live answer (AiRelease.stage shadow); it changes nothing a person sees. | Live, Active model, Testing in production | ADR-0051 Promotion / ADR-0051 (AI functions review 30 Sep §2) |
| Ready to promote / Promote | A shadow model passed its gate (governance alert promotionReady); an admin promotes it one stage at a time (canary, then production). The only way a model replaces the baseline. | Deploy, Go live, Auto-switch, Activate model, Upgrade AI | ADR-0051 (AI-D16) / contracts/satellite/ai.yaml#promoteAiRelease |
| L0 Disabled / L1 Advisory / L2 Prepare / L3 Execute with … | The one autonomy scale for every AI capability, shown as "L2 Prepare" etc. with the capability's ceiling beside it. Lower scopes tighten, never raise. | Autopilot, Copilot mode, Level 0-3 (CFG book), Approval level (for autonomy), Manual/Semi/Auto | ADR-0050 / ADR-0050 (AI-D04) / … |
| Approval tier | How many people must approve a proposed action (ProposedAction.approvalLevel, 1 or 2). Not an autonomy level. | Autonomy level, Approval level (ambiguous) | ADR-0050 |
| Suggestion / Draft | What AI produces. A suggestion advises; a draft is a ready-to-review change that a person applies in the owning screen. Copy says "Nothing is applied until you approve it." | AI changed, Auto-applied, AI updated your prices | ADR-0020 / ADR-0051 (AI functions review 30 Sep §4 Configuration assistant) / … |
| Why this? | The link or expander that opens an answer's explanation (Suggestion.explanation, recommendation template reason, decision trace). Plain words; for guests a template reason. | Explainability, SHAP, Feature importance (in operator copy) | ADR-0052 (AI-D09) / contracts/satellite/ai.yaml#/components/schemas/Suggestion |
| No thanks | The explicit decline on an offer. Only this counts as a decline and it is remembered across channels; scrolling past or closing the step is not a decline. | Dismiss (as a decline), Skip (as a decline), X (as a decline) | ADR-0052 (AI-D07) / DI-962 / … |
| Hold for review | What a high fraud or risk score does to a payment or order. The transaction goes through; it is held for a person. | Decline, Block, Reject (for a risk score), Fraud detected | ADR-0053 / ADR-0053 (AI-D06) |
| Hand over to a person | The concierge passes the whole conversation and its own summary to a live agent; the guest does not repeat themselves. | Escalate, Transfer, Contact bot | contracts/satellite/marketing-crm.yaml#handoverToAgent |
| Not available yet | The analytics assistant's answer to a question outside the semantic model; it records a knowledge gap and never improvises a number. | I cannot answer, Error, Unknown | ADR-0054 |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `ANL-051` | AI Analytics Command Center | D | 0 | 40 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-052` | Ask TICVAI — Natural Language Analytics | D | 0 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `ANL-053` | AI-Generated Dashboard Studio | D | 0 | 0 | 6 | 18 | 1 | 0 | — | notStarted (—) |
| `ANL-054` | AI Report Generator | D | 0 | 14 | 6 | 82 | 1 | 0 | — | notStarted (—) |
| `ANL-055` | Anomaly Detection Center | D | 0 | 20 | 6 | 4 | 0 | 0 | — | notStarted (—) |
| `ANL-056` | Root-Cause Analysis Explorer | D | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `ANL-057` | Forecasting & Predictive Analytics Studio | D | 7 | 0 | 5 | 39 | 0 | 0 | — | notStarted (—) |
| `ANL-058` | AI Recommendation & Next-Best-Action Center | D | 0 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `ANL-059` | AI Insight History, Evidence & Explainability | D | 5 | 40 | 5 | 8 | 0 | 0 | — | notStarted (—) |
| `ANL-060` | AI Analytics Governance & Model Control | D | 0 | 26 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ANL-051, ANL-052, ANL-053, ANL-054, ANL-055, ANL-056, ANL-058, ANL-060 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ANL-051` AI Analytics Command Center

**Provide a centralized landing page for all AI-generated analytical intelligence across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-051 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/ai-analytics-command-center-anl-051` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The landing for AI analytics: the prioritised list of what the models noticed — anomalies, trends, opportunities, forecast deviations — across the domains the user may see, each leading to "why" (root cause), "what to do" (recommendations) or "evidence". The one thing to get right: an insight is a prompt for a person, with its evidence and its reliability, never an automatic action.

**Known correction pending (do not draw the wrong version)**

- **The only read is listAnalyticsAnomalies; the insight layer (listAiInsights) is not declared.** Why: Trends, opportunities, forecast deviations and the insight lifecycle live in ai.listAiInsights; anomalies alone cannot fill a command centre. *(source: screens/P16-venue-analytics.yaml#ANL-051 / contracts/satellite/ai.yaml#listAiInsights; Finance, Ledger & Tax · Reporting & Analytics)*
- **Three severity vocabularies meet here (anomaly low/medium/high, insight priority low–critical, alert info/warning/critical).** Why: One screen must not show three scales; map anomaly severity onto insight priority for display. *(source: contracts/satellite/reporting.yaml#/components/schemas/AnomalySeverity / contracts/satellite/ai.yaml#/components/schemas/AiInsight; Finance, Ledger & Tax · Reporting & Analytics)*
- **A 20-column unbound table and "Carries the create action" in emptyFirstRun.** Why: Nothing is created here; the content is a card list. *(source: screens/P16-venue-analytics.yaml#ANL-051; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listAnalyticsAnomalies` ?from |
| Severity | segmented control | — | Low · Medium · High | `listAnalyticsAnomalies` ?severity |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every analytics** (data table)

| Shows | Format | Notes |
|---|---|---|
| Executive insights | text | not in the schema: `Executive Insights` |
| Revenue insights | text | not in the schema: `Revenue Insights` |
| Operations insights | text | not in the schema: `Operations Insights` |
| Customer insights | text | not in the schema: `Customer Insights` |
| Finance insights | text | not in the schema: `Finance Insights` |
| Marketing insights | text | not in the schema: `Marketing Insights` |
| Access insights | text | not in the schema: `Access Insights` |
| Membership/loyalty insights | text | not in the schema: `Membership/Loyalty Insights` |
| Forecasts | text | not in the schema: `Forecasts` |
| Anomalies | text | not in the schema: `Anomalies` |
| Opportunities | text | not in the schema: `Opportunities` |
| Risks | text | not in the schema: `Risks` |
| New AI insights | text | not in the schema: `New AI Insights` |
| Critical insights | text | not in the schema: `Critical Insights` |
| Opportunities detected | text | not in the schema: `Opportunities Detected` |
| Risks detected | text | not in the schema: `Risks Detected` |
| Active anomalies | text | not in the schema: `Active Anomalies` |
| Forecast alerts | text | not in the schema: `Forecast Alerts` |
| Recommendations pending review | text | not in the schema: `Recommendations Pending Review` |
| AI queries today | text | not in the schema: `AI Queries Today` |

**The selected analytics** (detail panel): The pack groups this record's detail under its own headings: “Revenue Opportunity”.

| Shows | Format | Notes |
|---|---|---|
| Executive insights | text | not in the schema: `Executive Insights` |
| Revenue insights | text | not in the schema: `Revenue Insights` |
| Operations insights | text | not in the schema: `Operations Insights` |
| Customer insights | text | not in the schema: `Customer Insights` |
| Finance insights | text | not in the schema: `Finance Insights` |
| Marketing insights | text | not in the schema: `Marketing Insights` |
| Access insights | text | not in the schema: `Access Insights` |
| Membership/loyalty insights | text | not in the schema: `Membership/Loyalty Insights` |
| Forecasts | text | not in the schema: `Forecasts` |
| Anomalies | text | not in the schema: `Anomalies` |
| Opportunities | text | not in the schema: `Opportunities` |
| Risks | text | not in the schema: `Risks` |
| New AI insights | text | not in the schema: `New AI Insights` |
| Critical insights | text | not in the schema: `Critical Insights` |
| Opportunities detected | text | not in the schema: `Opportunities Detected` |
| Risks detected | text | not in the schema: `Risks Detected` |
| Active anomalies | text | not in the schema: `Active Anomalies` |
| Forecast alerts | text | not in the schema: `Forecast Alerts` |
| Recommendations pending review | text | not in the schema: `Recommendations Pending Review` |
| AI queries today | text | not in the schema: `AI Queries Today` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **insight list**: Sorted by priority (Critical, High, Medium, Low) then newest; each card shows kind (Anomaly, Trend, Opportunity, Forecast deviation), the metric, observed vs expected, scope and detected time, and its status (New, Reviewed, Accepted, Rejected, Actioned, Measured). *(source: contracts/satellite/ai.yaml#/components/schemas/AiInsight / contracts/satellite/reporting.yaml#/components/schemas/AnalyticsAnomaly)*
- **evidence**: Each figure in a narrative links to its evidence; evidence is labelled Source, Derived or Model-inferred. *(source: contracts/satellite/ai.yaml#/components/schemas/AiEvidenceItem)*
- **maturity**: Detectors in their first weeks show "Limited historical data" on their insights. *(source: contracts/satellite/ai.yaml#/components/schemas/AiMaturity)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Why did this change?**: Opens root-cause analysis with metric, period and comparison carried. *(source: screens/P16-venue-analytics.yaml#ANL-056)*
- **What should we do?**: Opens recommendations filtered to the insight. *(source: screens/P16-venue-analytics.yaml#ANL-058)*

**Data it reads**: `listAnalyticsAnomalies` (onLoad, What the models noticed)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Back to Executive Command Center*
- → `ANL-060` AI Analytics Governance & Model Control: *AI Analytics Governance & Model Control*
- → `ANL-052` Ask TICVAI — Natural Language Analytics: *Ask TICVAI — Natural Language Analytics*
- → `ANL-053` AI-Generated Dashboard Studio: *AI-Generated Dashboard Studio*
- → `ANL-054` AI Report Generator: *AI Report Generator*
- → `ANL-055` Anomaly Detection Center: *Anomaly Detection Center*
- → `ANL-056` Root-Cause Analysis Explorer: *Root-Cause Analysis Explorer*
- → `ANL-057` Forecasting & Predictive Analytics Studio: *Forecasting & Predictive Analytics Studio*
- → `ANL-058` AI Recommendation & Next-Best-Action Center: *AI Recommendation & Next-Best-Action Center*
- → `ANL-059` AI Insight History, Evidence & Explainability: *AI Insight History, Evidence & Explainability*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The analytics list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **New tenant, no history**: "Insights appear once your venue has a few weeks of trading" — not an empty table. *(source: DI-280 / contracts/satellite/ai.yaml#/components/schemas/AiMaturity)*
- **A finance user in phase one**: No AI panels on finance reporting; revenue anomalies are still shown on the analytics side. *(source: DI-278)*

#### Consistency with other screens

- Match `ANL-019`: AI Management Insights shows the same insights inside Board 1; one card component, same priority words.
- Match `ANL-018`: Alerts (thresholds someone set) and anomalies (departures from the series) are different; keep separate lists and words.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
insights:
- High · Anomaly · Net revenue at Beach Kiosk 38% below expected (AED 6,210.00 vs AED 10,050.00) · 29 Sep
- Medium · Opportunity · Fast Pass sells out by 11:00 on Fridays at Motiongate
- Low · Trend · Average basket at Coffee House up 6% over 4 weeks
```

#### Permissions

- `listAnalyticsAnomalies` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-051` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-051`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 1: Opens AI Analytics Command Center → Provide a centralized landing page for all AI-generated analytical intelligence across TICVAI.
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F179 branch at step 1 (expected): when Nothing has been set up on AI Analytics Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F179 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-051?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-001`, `ANL-060`, `ANL-052`, `ANL-053`, `ANL-054`, `ANL-055`, `ANL-056`, `ANL-057`, `ANL-058`, `ANL-059`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-052` Ask TICVAI — Natural Language Analytics

**Allow users to query TICVAI business information using normal language instead of manually building reports.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-052 |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_VENUE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `conversationId` (navigation) |
| Route | `/analytics/ask-ticvai-natural-language-analytics-anl-052` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Ask TICVAI: a business user asks in plain English or Arabic and gets a governed answer — the number, how it was worked out, how far it can be relied on, and suggested follow-ups — without knowing report names or fields. The one thing to get right: when the question lacks a timeframe, venue or metric, the assistant asks a clarifying question instead of guessing, and every answer is limited to what the user's role may see.

**Known correction pending (do not draw the wrong version)**

- **The answer contract has no clarifying-question shape.** Why: DI-712 (agreed) requires the AI to ask when timeframe, venue or metric is missing; askReportingQuestion returns only an answer, a 400 with suggestions, or "insufficient evidence". *(source: DI-712 / contracts/satellite/reporting.yaml#/components/schemas/NaturalLanguageAnswer / TRACKER Actions row 258; Finance, Ledger & Tax · Reporting & Analytics)*
- **The screen has no content region and no answer state is drawn.** Why: The gap stands; the answer card above is the content. *(source: screens/P16-venue-analytics.yaml#ANL-052; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **question**: 3–1,000 characters; Arabic input renders right-to-left; conversation context is kept for follow-ups. *(source: contracts/satellite/reporting.yaml#askReportingQuestion / DI-019 / DI-964)*
- **venue**: Optional narrowing; omitted answers over everything the user's scope permits, never beyond. *(source: contracts/satellite/reporting.yaml#askReportingQuestion)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **answer card**: Answer sentence, a small result table or chart, "What I understood" (interpretation), "Data as of", and a reliability word: Grounded / Partly answered / Sources disagree / Not enough evidence. *(source: contracts/satellite/reporting.yaml#/components/schemas/NaturalLanguageAnswer / contracts/satellite/reporting.yaml#/components/schemas/ReportingAnswerReliability)*
- **how it was calculated**: Metric, dimensions, filters and period in words; the query itself behind "Show query" for finance users who want to check. *(source: contracts/satellite/reporting.yaml#/components/schemas/GeneratedQuery / contracts/satellite/reporting.yaml#askReportingQuestion)*
- **not available yet**: Names the missing part (metric, breakdown, filter, comparison, or period before history starts) and says the data owner has been told. *(source: contracts/satellite/reporting.yaml#/components/schemas/ReportingUnavailableReason)*
- **citations**: Document-based parts name the policy or document; numbers only from the query result. *(source: DI-964 / contracts/satellite/reporting.yaml#askReportingQuestion)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Save as report**: Saves the latest answer in the conversation as a report definition (name required); offered only to users who manage reports. *(source: contracts/satellite/reporting.yaml#saveNaturalLanguageQuery)*
- **Did you mean…**: When the question cannot be interpreted, up to three close questions are offered as chips. *(source: contracts/satellite/reporting.yaml#/components/schemas/ReportQuestionProblem)*

**Where the user goes next**

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ask ticvai natural list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ask ticvai natural untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ask ticvai natural yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the ask ticvai natural are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Question could not be interpreted. (ReportQuestionProblem) |

#### Edge cases to draw

- **"Show me the top 10 products" (no period)**: The assistant asks "For which period — yesterday, last week, this month?" with chips; nothing is run until answered. *(source: DI-712)*
- **A question about a metric outside the user's role**: Answered as "not available", without revealing that the metric exists. *(source: contracts/satellite/reporting.yaml#/components/schemas/ReportingUnavailableReason / DI-964)*

#### Consistency with other screens

- Match `ANL-009`: Same answer card and reliability words.
- Match `ANL-054`: Saving an answer here and generating a report on ANL-054 produce the same kind of report definition.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
question: What was yesterday's net revenue at Aquaventure by channel?
understood: Net revenue · by channel · Tue 29 Sep 2026 · Aquaventure Waterpark
answer: AED 1,104,220.40 — Web AED 498,300.00, POS AED 352,910.40, OTA AED 201,010.00, Kiosk AED 52,000.00
reliability: Grounded · data as of 30 Sep 06:00
clarifying: 'Q: Show me the top 10 products → A: For which period: yesterday, last week or this month?'
arabic: ما هو صافي الإيرادات أمس؟
```

#### Permissions

- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `saveNaturalLanguageQuery` → `REPORT_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.7.30 | System shall support natural language reporting. | Unified Operations Dashboard | CONTRACTED | `askReportingQuestion` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Conversational report building (Qossai): user asks e.g. "show me the top 10 products sold last week"; the AI asks clarifying questions when timeframe, venue or metric are missing instead of guessing or regenerating. *(agreed · MoM 8 Sep 2026, 4.7 AI-Assisted Report & Configuration Generation · DI-712)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-052` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-052`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 2: Works in Ask TICVAI — Natural Language Analytics → Allow users to query TICVAI business information using normal language instead of manually building reports.
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)
- ADR-0059 *AI phasing against the six-month plan* (`docs/adr/0059-ai-phasing-against-the-six-month-plan.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-052?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-053` AI-Generated Dashboard Studio

**Allow users to generate dashboards from natural-language requests.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-053 |
| Who uses it | venue staff holding `REPORT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/ai-generated-dashboard-studio-anl-053` |

**Known gaps.** **AI-Generated Dashboard Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** AI-generated dashboard studio: a user describes a dashboard ("a weekly sales board for F&B outlets") and gets a draft of tiles to review, adjust and save. The one thing to get right: the draft obeys the same rules as a hand-built dashboard — certified measures only, marks that can bind, at most 24 tiles, refresh no faster than 30 seconds, a module, and approval before it is published to others.

**Known correction pending (do not draw the wrong version)**

- **No operation generates a dashboard draft from a request; only createDashboard (which persists) is declared.** Why: The screen's purpose cannot be met; the gap note already says the write is missing. *(source: screens/P16-venue-analytics.yaml#ANL-053 / contracts/satellite/reporting.yaml#createDashboard; Finance, Ledger & Tax · Reporting & Analytics)*
- **Approval before publishing (DI-706) has no operation — no publish, approve or version operation on dashboards, only create / update / delete and isShared.** Why: A generated dashboard can be shared without the agreed approval step. *(source: DI-706 / contracts/satellite/reporting.yaml#/components/schemas/Dashboard / contracts/satellite/reporting.yaml#updateDashboard; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Until an approval operation exists, may a generated dashboard be shared at all?** → Drawn default accepted: Save private only; the share control is shown disabled with "Needs approval". *(decided by Chinmay, 2026-10-02; DEC-349 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **request**: Plain-language description; the AI asks back when audience, period or measures are missing. *(source: DI-712)*
- **module**: Required; only modules the user may author for are offered ("Core" when it belongs to none). *(source: contracts/satellite/reporting.yaml#/components/schemas/CreateDashboardRequest / contracts/satellite/reporting.yaml#/components/schemas/CommandCentre)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create dashboard (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **draft preview**: Live preview of the proposed tiles with real data, each tile showing its measure, mark and refresh; tiles whose mark cannot bind yet (combo, scatter, waterfall, treemap, funnel, map, ribbon, matrix, decomposition tree) are not proposed. *(source: contracts/satellite/reporting.yaml#/components/schemas/DashboardTile / MATRIX 7.4.45 / MATRIX 11.1.2)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Save dashboard**: Saves as a private dashboard; sharing goes through the approval step. Refused for a module the user may not author (409) with that reason. *(source: contracts/satellite/reporting.yaml#createDashboard / DI-706)*

**Where the user goes next**

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ai-generated list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ai-generated untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ai-generated yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the ai-generated are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094); 409 The caller is not entitled to the dashboard's module — the tenant has not licensed it, or the principal holds no permission in it.; 422 A tile's report lacks the column encodings its visualisation needs (problem type `tile-encoding-missing`, CHG-FIN-007; the … |

#### Edge cases to draw

- **The request implies more than 24 tiles**: The AI proposes 24 and lists what it left out. *(source: contracts/satellite/reporting.yaml#/components/schemas/CreateDashboardRequest)*
- **The request asks for "live every second"**: Tiles set to 30 seconds, with a note. *(source: contracts/satellite/reporting.yaml#/components/schemas/DashboardTile)*

#### Consistency with other screens

- Match `ANL-022`: Output lands in the same structure as the dashboard creation wizard; the user can continue there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
request: Weekly F&B sales board for the Aquaventure outlets
draft:
- Net revenue this week · number · vs last week
- Net revenue by outlet · bar
- Orders by hour × day · heatmap
- Top 10 products · table
```

#### Permissions

- `createDashboard` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.79 | System shall monitor operational service levels. | Ticketing Catalogue | CONTRACTED | `createDashboard` |
| 1.3.27 | System shall provide real-time dashboards showing attendance, check-ins, occupancy, sales, capacity utilization and operational KPIs. | Ticketing Catalogue | CONTRACTED | `createDashboard` |
| 1.3.28 | System shall provide event performance analytics including attendance, revenue, conversion rates, capacity utilization and customer engagement. | Ticketing Catalogue | CONTRACTED | `createDashboard` |
| 8.7.1 | System shall provide executive dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.2 | System shall provide operational dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.3 | System shall provide financial dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.4 | System shall provide sales dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.5 | System shall provide marketing dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.6 | System shall provide ticketing dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.7 | System shall provide access control dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.8 | System shall provide membership dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.9 | System shall provide loyalty dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Conversational report building (Qossai): user asks e.g. "show me the top 10 products sold last week"; the AI asks clarifying questions when timeframe, venue or metric are missing instead of guessing or regenerating. *(agreed · MoM 8 Sep 2026, 4.7 AI-Assisted Report & Configuration Generation · DI-712)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-053` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-053`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 4: Works in AI-Generated Dashboard Studio → Allow users to generate dashboards from natural-language requests.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-053?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create dashboard, Cancel.
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `REPORT_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-054` AI Report Generator

**Generate detailed reports from natural-language instructions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-054 |
| Who uses it | venue staff holding `REPORT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/ai-report-generator-anl-054` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** AI report generator: a user describes a report ("weekly refunds by venue and reason") and gets a report built on the same semantic model, permissions and calculations as a hand-built one, to preview, save and schedule. The one thing to get right: the user sees the dimensions and measures the AI chose and can correct them before saving, and a missing period or measure is asked for, not guessed.

**Known correction pending (do not draw the wrong version)**

- **The screen declares createReport for accepting a generated report.** Why: The contracted AI path is askReportingQuestion (which keeps the generated query) then saveNaturalLanguageQuery; createReport has no AI input and the screen has no source for the definition it would send. *(source: screens/P16-venue-analytics.yaml#ANL-054 / contracts/satellite/reporting.yaml#saveNaturalLanguageQuery; Finance, Ledger & Tax · Reporting & Analytics)*
- **Clarifying questions have no contract shape.** Why: As on ANL-052, DI-712 cannot be met by the current answer schema. *(source: DI-712; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every report generator** (data table)

| Shows | Format | Notes |
|---|---|---|
| Selected dataset | text | not in the schema: `Selected Dataset` |
| Fields | text | not in the schema: `Fields` |
| Filters | text | not in the schema: `Filters` |
| Grouping | text | not in the schema: `Grouping` |
| Calculations | text | not in the schema: `Calculations` |
| Sort | text | not in the schema: `Sort` |
| Output | text | not in the schema: `Output` |

**The selected report generator** (detail panel): The pack groups this record's detail under its own headings: “User asks”, “Dimensions”, “Measures”, “Relationship to Board 3”.

| Shows | Format | Notes |
|---|---|---|
| Selected dataset | text | not in the schema: `Selected Dataset` |
| Fields | text | not in the schema: `Fields` |
| Filters | text | not in the schema: `Filters` |
| Grouping | text | not in the schema: `Grouping` |
| Calculations | text | not in the schema: `Calculations` |
| Sort | text | not in the schema: `Sort` |
| Output | text | not in the schema: `Output` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **interpretation**: "You asked", Dimensions, Measures, Filters, Period shown as editable chips before the preview runs. *(source: screens/P16-venue-analytics.yaml#ANL-054 / contracts/satellite/reporting.yaml#/components/schemas/ReportingSemanticQuerySpec)*
- **preview**: First page of rows with totals and "Data as of"; full results run asynchronously when large. *(source: contracts/satellite/reporting.yaml#runReport / contracts/satellite/reporting.yaml#/components/schemas/ReportResult)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Save report**: Saves as a versioned report definition (name required); then Schedule or Export (PDF, Excel, CSV). *(source: contracts/satellite/reporting.yaml#saveNaturalLanguageQuery / DI-708 / DI-714)*

**Where the user goes next**

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report generator list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the report generator untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report generator yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the report generator are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Unknown field, invalid filter, or estimated cost beyond the limit |

#### Edge cases to draw

- **The report includes guest names or contacts**: Export of personal data requires the audited permission; otherwise those columns are masked. *(source: contracts/shared/permissions.yaml#/components/schemas/Permission)*
- **Finance ledger report requested in phase one**: "Not available yet" — AI-assisted finance reporting is phase two. *(source: DI-278)*

#### Consistency with other screens

- Match `ANL-052`: Same interpretation chips and reliability words.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
request: Weekly refunds by venue and reason for September
dimensions: Venue · Refund reason · Week
measures: Refunds (AED) · Refund count
preview: Aquaventure · Weather closure · week 39 · AED 12,840.00 · 61 refunds
```

#### Permissions

- `createReport` → `REPORT_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

82 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.40 | System shall provide analytics and dashboards covering ticket sales, attendance, utilization, conversion rates, capacity utilization and revenue performance. | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.104 | Membership analytics | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.135 | Required Reports Operational Reports Donations by Campaign. Donations by Site. Donations by Product. Donations by Sales Channel. Donations by Date. Donations by User/Cashier. Donations by Payment … | Ticketing Catalogue | CONTRACTED | `createReport` |
| 3.2.65 | An Entry or Exit report is expected presenting the readings per outcome (ok/ko), per time and per access point. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.66 | The in park report showing the difference between the Entries and the Exits. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.68 | The length of stay report shall present the difference between the time in scan and the time out scan. | Admission and Access | CONTRACTED | `createReport` |
| 3.5.12 | System shall provide analytics showing bundle sales volume, revenue contribution, conversion rate, redemption rate, average order value impact, profitability, and performance by channel. | Admission and Access | CONTRACTED | `createReport` |
| 3.7.11 | System shall provide reporting on upsell impressions, conversion rates, revenue generated, average order value uplift, and campaign effectiveness across channels. | Admission and Access | CONTRACTED | `createReport` |
| 5.6.28 | Provide reporting on wait times, abandonment rates, no-shows, throughput, utilization, and satisfaction. | F&B & Guest Management | CONTRACTED | `createReport` |
| 6.1.5 | The system should be able to Generate reports with admission types/information. | Retail POS | CONTRACTED | `createReport` |
| 6.1.8 | The system should have the ability to retrieve information "on the fly" for items, (e.g., keyword, item #, description, category etc.) in user-friendly format such as pull-down menus and/or auto fill … | Retail POS | CONTRACTED | `createReport` |
| 6.1.9 | The system should be able to report historical sales look up by item, ticket number etc.. | Retail POS | CONTRACTED | `createReport` |
| … 70 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Conversational report building (Qossai): user asks e.g. "show me the top 10 products sold last week"; the AI asks clarifying questions when timeframe, venue or metric are missing instead of guessing or regenerating. *(agreed · MoM 8 Sep 2026, 4.7 AI-Assisted Report & Configuration Generation · DI-712)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-054` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-054`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 6: Works in AI Report Generator → Generate detailed reports from natural-language instructions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-054?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `REPORT_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-055` Anomaly Detection Center

**Automatically identify unusual behavior across TICVAI data without requiring users to manually monitor every KPI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-055 |
| Who uses it | venue staff holding `AI_CONFIGURE`, `AI_USE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each Anomaly Displays) and no metric row |
| Offline | online only |
| Opens with | `detectorKey` (navigation) |
| Route | `/analytics/anomaly-detection-center-anl-055` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-012): The same duplication as ANL-019; listAiInsights (kind anomaly) is the one list (ADR-0053; design-notes correction ai ANL-055).

**From the AI & Intelligence process.** Anomaly detection centre: unusual movements across KPIs, flagged from the first week against limits the venue sets and against the forecast, then against its own normal as history builds. Configure detectors per KPI. The one thing to get right: each anomaly shows its expected range and what it was compared with (stage), and aggregate deviations live here while one cashier's or one till's pattern is a risk case, not an anomaly.

**Known correction pending (do not draw the wrong version)**

- **Columns are board labels bound to no operation, including "Confidence".** Why: Bind to listAiInsights (kind anomaly); replace Confidence with the basis (ranges, never a bare percentage). *(source: screens/P16-venue-analytics.yaml#ANL-055 / ADR-0051; AI & Intelligence)*
- **requiresModule analytics.** Why: Anomaly detection is an AI capability (family anomalyDetection). *(source: contracts/satellite/ai.yaml#/components/schemas/AiPolicy (enabledCapabilities); AI & Intelligence)*

**Fixed on main** (the package already carries these; draw what it says): Declares listAnalyticsAnomalies and listAiInsights. (CHG-WIR-012).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | New · Reviewed · Accepted · Rejected · Actioned · Measured | `listAiInsights` ?status |
| Kind | select | — | Anomaly · Forecast deviation · Trend · Opportunity · Executive summary · Root cause · Forecast threshold · Marketing recommendation | `listAiInsights` ?kind |
| Priority | radio group | — | Low · Medium · High · Critical | `listAiInsights` ?priority |
| From | date and time picker | — | — | `listAiInsights` ?from |
| Metric key | text field | — | — | `listAnomalyDetectors` ?metricKey |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **detector (metric, method, thresholds, sensitivity, dimensions, cadence)**: Day one method threshold with defaults the venue edits (refund rate, void rate, cash variance) plus "attendance below the forecast's low end"; seasonal and peer methods offered once history allows, marked with the stage they need. *(source: contracts/satellite/ai.yaml#configureAnomalyDetector / ADR-0051 (AI functions review 30 Sep §4 Anomaly detection))*

#### Outputs: what the screen shows and produces

**Shown**

**Every anomaly detection** (data table)

| Shows | Format | Notes |
|---|---|---|
| KPI | text | not in the schema: `KPI` |
| Expected range | text | not in the schema: `Expected Range` |
| Actual value | text | not in the schema: `Actual Value` |
| Variance | text | not in the schema: `Variance` |
| Severity | text | not in the schema: `Severity` |
| Start time | text | not in the schema: `Start Time` |
| Duration | text | not in the schema: `Duration` |
| Affected site | text | not in the schema: `Affected Site` |
| Affected domain | text | not in the schema: `Affected Domain` |
| Confidence | text | not in the schema: `Confidence` |

**The selected anomaly detection** (detail panel): The pack groups this record's detail under its own headings: “Detect abnormal patterns involving”, “High Refund Anomaly”, “Detection Methods”.

| Shows | Format | Notes |
|---|---|---|
| KPI | text | not in the schema: `KPI` |
| Expected range | text | not in the schema: `Expected Range` |
| Actual value | text | not in the schema: `Actual Value` |
| Variance | text | not in the schema: `Variance` |
| Severity | text | not in the schema: `Severity` |
| Start time | text | not in the schema: `Start Time` |
| Duration | text | not in the schema: `Duration` |
| Affected site | text | not in the schema: `Affected Site` |
| Affected domain | text | not in the schema: `Affected Domain` |
| Confidence | text | not in the schema: `Confidence` |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **anomaly rows**: KPI, expected range (not a single expected value), actual, variance, severity, start and duration, site, domain; no "confidence" column - the basis label instead (threshold you set, same weekday over N weeks, peer venues). *(source: contracts/satellite/ai.yaml#listAiInsights / ADR-0051)*
- **detector health**: Each detector's measured false-alarm rate (from rejected insights). *(source: contracts/satellite/ai.yaml#listAnomalyDetectors)*

**Data it reads**: `listAiInsights` (onLoad, Insights and anomalies); `listAnomalyDetectors` (onLoad, Anomaly detectors)

**Where the user goes next**

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The anomaly detection list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the anomaly detection untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No anomaly detection yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the anomaly detection are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **The anomaly is one actor (a cashier's refunds)**: Not shown here; routed as a risk alert (link to the fraud and risk case screen). *(source: ADR-0053)*

#### Consistency with other screens

- Match `ANL-019`: Anomalies are insights of kind anomaly; same card and lifecycle.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- kpi: Refund rate
  expected: 0.8-1.6%
  actual: 4.2%
  severity: high
  site: Coastal Aqua
  started: Sat 26 Sep 14:00
  basis: Threshold you set (2%)
- kpi: Attendance
  expected: 2,100-3,300
  actual: 1,640
  severity: medium
  basis: Below forecast low end
```

#### Permissions

- `listAiInsights` → `AI_USE` (operate) · staff
- `configureAnomalyDetector` → `AI_CONFIGURE` (configure) · staff
- `listAnomalyDetectors` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.4.17 | System shall support AI-powered anomaly explanations. | Unified Operations Dashboard | CONTRACTED | `listAiInsights` |
| 8.2.20 | System shall generate attendance forecast alerts when predefined thresholds are exceeded. | Unified Operations Dashboard | CONTRACTED | `configureAnomalyDetector` |
| 8.2.41 | System shall generate capacity alerts. | Unified Operations Dashboard | CONTRACTED | `configureAnomalyDetector` |
| 8.3.16 | System shall detect abnormal refund volumes. | Unified Operations Dashboard | CONTRACTED | `configureAnomalyDetector` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-055` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-055`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 8: Works in Anomaly Detection Center → Automatically identify unusual behavior across TICVAI data without requiring users to manually monitor every KPI.
- ADR-0053 *Owners keep their deterministic rules; AI owns cross-entity risk, alerts and cases* (`docs/adr/0053-risk-layer-ownership.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-055?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-056` Root-Cause Analysis Explorer

**Help users understand why a KPI changed. This is one of the most important AI capabilities in the entire platform.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-056 |
| Who uses it | venue staff holding `AI_USE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/root-cause-analysis-explorer-anl-056` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Root-cause explorer: from a KPI change ("net revenue down 14% on Tuesday") to the contributing factors — which channels, products, venues or hours moved it, and by how much. The client calls it one of the most important AI capabilities. The one thing to get right: the breakdown is arithmetic over governed metrics; the AI only words it, and the screen says "contributing factors", never "causes".

**Known correction pending (do not draw the wrong version)**

- **The derived primary action is askReportingQuestion; explainMetricChange is listed as an action but no control is drawn for it.** Why: The act this screen exists for is "explain this change". *(source: screens/P16-venue-analytics.yaml#ANL-056 / contracts/satellite/ai.yaml#explainMetricChange; Finance, Ledger & Tax · Reporting & Analytics)*
- **The comparison options differ from the KPI read (forecast here; target and benchmark there).** Why: A user arriving from a KPI tile compared "vs target" cannot carry that comparison into the explanation. *(source: contracts/satellite/ai.yaml#explainMetricChange / contracts/satellite/reporting.yaml#getKpiValues; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listAnalyticsAnomalies` ?from |
| Severity | segmented control | — | Low · Medium · High | `listAnalyticsAnomalies` ?severity |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **metric and period**: Metric from the governed KPI list; period as a date range; comparison Previous period (default), Same period last year, or Forecast. *(source: contracts/satellite/ai.yaml#explainMetricChange)*
- **dimensions**: Channel, product, venue, hour (user may choose up to the dimensions the metric carries). *(source: contracts/satellite/ai.yaml#explainMetricChange / MATRIX 8.4.18 / MATRIX 8.7.28)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **change header**: "Net revenue −AED 61,240.00 (−14.2%) vs previous Tuesday" with "Data as of" and reliability word. *(source: contracts/satellite/ai.yaml#/components/schemas/AiMetricChangeExplanation)*
- **drivers**: Bar of contributions sorted by absolute size, negatives left in red, positives right; each driver links to its evidence. Decomposition tree and waterfall cannot bind yet. *(source: contracts/satellite/ai.yaml#/components/schemas/AiMetricChangeExplanation / contracts/satellite/reporting.yaml#/components/schemas/DashboardTile)*
- **narrative**: Two or three sentences whose figures all come from the drivers; labelled "Contributing factors". *(source: contracts/satellite/ai.yaml#explainMetricChange)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Keep this analysis**: Saved as a root-cause insight visible in insight history. *(source: contracts/satellite/ai.yaml#explainMetricChange)*
- **Ask a follow-up**: Opens the assistant with the metric and period carried. *(source: contracts/satellite/reporting.yaml#askReportingQuestion)*

**Data it reads**: `listAnalyticsAnomalies` (onLoad, Candidate causes)

**Where the user goes next**

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The root-cause analysis list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the root-cause analysis untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No root-cause analysis yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the root-cause analysis are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Question could not be interpreted. (ReportQuestionProblem) |

#### Edge cases to draw

- **The change is within normal variation**: "No single factor stands out" with the drivers still listed, reliability "Partly answered". *(source: contracts/satellite/reporting.yaml#/components/schemas/ReportingAnswerReliability)*
- **The comparison period predates the venue's history**: "Not enough history for this comparison". *(source: contracts/satellite/reporting.yaml#/components/schemas/ReportingUnavailableReason)*

#### Consistency with other screens

- Match `ANL-019`: AI Management Insights' "possible reasons" opens this screen; same driver bars.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
header: Net revenue Tue 29 Sep −AED 61,240.00 (−14.2%) vs Tue 22 Sep · Aquaventure
drivers:
- Channel OTA −AED 38,900.00
- Product Wave Pool Cabana −AED 14,200.00
- Hour 15:00–17:00 −AED 9,800.00 (rain)
- Channel Web +AED 1,660.00
reliability: Grounded · data as of 30 Sep 06:00
```

#### Permissions

- `listAnalyticsAnomalies` → `REPORT_VIEW_VENUE` (operate) · staff
- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `explainMetricChange` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.7.30 | System shall support natural language reporting. | Unified Operations Dashboard | CONTRACTED | `askReportingQuestion` |
| 8.4.18 | System shall support AI-powered root cause analysis. | Unified Operations Dashboard | CONTRACTED | `explainMetricChange` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- An AI layer across all dashboards explains why a metric changed (e.g. why revenue dropped on a given day) and recommends management actions from sales, revenue and attendance trends. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-719)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-056` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-056`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 10: Works in Root-Cause Analysis Explorer → Help users understand why a KPI changed. This is one of the most important AI capabilities in the entire platform.
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)
- ADR-0059 *AI phasing against the six-month plan* (`docs/adr/0059-ai-phasing-against-the-six-month-plan.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-056?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `AI_USE`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-057` Forecasting & Predictive Analytics Studio

**Provide configurable forward-looking analytics across business domains.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-057 |
| Who uses it | venue staff holding `AI_USE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `versionId` (navigation) |
| Route | `/analytics/forecasting-predictive-analytics-studio-anl-057` |

**What the spec says about it.** **Measure names, not "Revenue"** (decided 2 October 2026, Chinmay; CHG-FIN-002; BOARDREQ MOM-2758..2761). Takings (money taken less money paid back, a cash-control figure), Gross sales (before discounts, excluding VAT), Net revenue (gross sales less discounts and refunds), Recognised revenue and Deferred revenue are different numbers and never share a label; a tile takes its label from the seeded KPI it is bound to (`ReportingSystemKpi`).

**Known gaps.** **The pack names 11 actions on this screen and the screen declares 0 operations.** Unserved: Revenue, Ticket Sales, Attendance, Capacity, Queue Demand, Cash Collection, Membership Renewals, Customer … **Forecasting & Predictive Analytics Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so …

**From the AI & Intelligence process.** The venue analytics forecasting studio: pick a subject (revenue, ticket sales, attendance, capacity, queue demand, cash collection, membership renewals, churn) and a horizon (next hour to quarter), see the forecast with its range and basis against current KPIs, run a what-if and export. The one thing to get right: it reuses the console's forecast components and wording; on a new venue it shows Starting forecasts, not "comes later".

**Known correction pending (do not draw the wrong version)**

- **Subjects and horizons drawn as buttons and selectFields bound to nothing.** Why: Subject and horizon are two pickers over listForecastDefinitions; only definitions that exist are offered. *(source: contracts/satellite/ai.yaml#listForecastDefinitions; AI & Intelligence)*
- **DI-280 is attached ("cannot be delivered in phase one").** Why: Superseded by ADR-0051; see BO-919. *(source: DI-280 / ADR-0051; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Next Hour | select field | — | — | — | — | — | — |
| Today | select field | — | — | — | — | — | — |
| Tomorrow | select field | — | — | — | — | — | — |
| Next 7 Days | select field | — | — | — | — | — | — |
| Month End | select field | — | — | — | — | — | — |
| Quarter | select field | — | — | — | — | — | — |
| Custom | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |
| Subject | select | — | Attendance · Arrival pattern · Product demand · Timeslot demand · Channel pace · Revenue · Occupancy · Attraction utilisation · Queue · Entry flow · Staffing · POS demand … | `listForecastDefinitions` ?subject |
| Definition key | text field | — | — | `getForecast` ?definitionKey |
| Version | picker: choose a version | — | — | `getForecast` ?versionId |
| From | date and time picker | — | — | `getForecast` ?from |
| To | date and time picker | — | — | `getForecast` ?to |
| Dimension key | text field | — | — | `getForecast` ?dimensionKey |
| Scenario | picker: choose a scenario | — | — | `getForecast` ?scenarioId |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Net revenue (primary button) | navigation or local | — | — | — | — |
| Ticket Sales (secondary button) | navigation or local | — | — | — | — |
| Attendance (secondary button) | navigation or local | — | — | — | — |
| Capacity (secondary button) | navigation or local | — | — | — | — |
| Queue Demand (secondary button) | navigation or local | — | — | — | — |
| Cash Collection (secondary button) | navigation or local | — | — | — | — |
| Membership Renewals (secondary button) | navigation or local | — | — | — | — |
| Customer Churn (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **forecast with KPI**: Current KPI value against target beside the forecast range for the chosen horizon; stage badge and Based on. *(source: contracts/satellite/reporting.yaml#getKpiValues / contracts/satellite/ai.yaml#getForecast / ADR-0051)*

**Data it reads**: `getKpiValues` (onLoad, The series being forecast); `listForecastDefinitions` (onLoad, What is forecast); `getForecast` (onLoad, Forecast values)

**Where the user goes next**

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The forecasting predictive analytics configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the forecasting predictive analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No forecasting predictive analytics configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
subject: Membership renewals, next 30 days
forecast: 410 renewals (330-490)
stage: Learning
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `listForecastDefinitions` → `AI_USE` (operate) · staff
- `getForecast` → `AI_USE` (operate) · staff
- `createForecastScenario` → `AI_USE` (operate) · staff
- `exportForecastVersion` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

39 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.55 | AI shall forecast future resource demand. | Ticketing Catalogue | CONTRACTED | `getForecast` |
| 4.1.17 | Forecast demand based on historical and operational data. | Bundles and Promotions | CONTRACTED | `getForecast` |
| 5.6.26 | Predict queue lengths, wait times, peak demand, and capacity shortages. | F&B & Guest Management | CONTRACTED | `getForecast` |
| 8.2.1 | System shall forecast attendance based on historical attendance patterns. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.2 | System shall forecast attendance by venue. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.3 | System shall forecast attendance by attraction. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.4 | System shall forecast attendance by event. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.5 | System shall forecast attendance by session. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.6 | System shall forecast attendance by date range. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.7 | System shall forecast attendance by day of week. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.8 | System shall forecast attendance by month. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.9 | System shall forecast attendance by season. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| … 27 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-057` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-057`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 12: Works in Forecasting & Predictive Analytics Studio → Provide configurable forward-looking analytics across business domains.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-057?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Net revenue, Ticket Sales, Attendance, Capacity, Queue Demand, Cash Collection, Membership Renewals, Customer Churn.
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `AI_USE`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-058` AI Recommendation & Next-Best-Action Center

**Convert analytical insights into prioritized business recommendations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-058 |
| Who uses it | venue staff holding `AI_USE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/ai-recommendation-next-best-action-center-anl-058` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Recommendations and next-best actions: insights turned into prioritised, explained and measurable recommendations for management, each with expected impact and evidence. The one thing to get right: a recommendation never acts — Review, Simulate or "Open in …" takes the person to the owning module to make the change, and every recommendation's effect is measured afterwards.

**Known correction pending (do not draw the wrong version)**

- **The table is implied by listNextBestAction, which the screen does not declare.** Why: listNextBestAction is a promotions read gated by price-view permission and bound to ADM-236; the screen's declared reads are listAnalyticsAnomalies and listAiInsights. *(source: screens/P16-venue-analytics.yaml#ANL-058 / contracts/satellite/promotions.yaml#listNextBestAction; Finance, Ledger & Tax · Reporting & Analytics)*
- **Accept / reject is not declared (decideAiInsight).** Why: The lifecycle and measured effect need the insight decision operation. *(source: contracts/satellite/ai.yaml#listAiInsights; Finance, Ledger & Tax · Reporting & Analytics)*
- **The client asks for a confidence percentage and a single AED impact per recommendation.** Why: The contract shows impact as a range and forbids a bare percentage; the client should be told why. *(source: MATRIX 8.6.19 / MATRIX 8.3.68 / MATRIX 8.6.21 / MATRIX 3.6.37 / contracts/satellite/ai.yaml#/components/schemas/AiInsight; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What is the impact shape (amount, unit, basis, period) used to rank and total recommendations?** → Drawn default accepted: A range on a named metric per month. *(decided by Chinmay, 2026-10-02; DEC-350 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listAnalyticsAnomalies` ?from |
| Severity | segmented control | — | Low · Medium · High | `listAnalyticsAnomalies` ?severity |
| Status | select | — | New · Reviewed · Accepted · Rejected · Actioned · Measured | `listAiInsights` ?status |
| Kind | select | — | Anomaly · Forecast deviation · Trend · Opportunity · Executive summary · Root cause · Forecast threshold · Marketing recommendation | `listAiInsights` ?kind |
| Priority | radio group | — | Low · Medium · High · Critical | `listAiInsights` ?priority |
| From | date and time picker | — | — | `listAiInsights` ?from |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **recommendation card**: Domain (Revenue, Production, Operations, Pricing, Menu), what to do, expected impact as a range ("AED 4,200 – 6,800 a month"), basis and maturity, evidence; sorted by priority then impact. *(source: MATRIX 8.6.19 / MATRIX 8.3.68 / MATRIX 8.6.21 / MATRIX 3.6.37 / contracts/satellite/ai.yaml#/components/schemas/AiInsight / contracts/satellite/ai.yaml#/components/schemas/AiMaturity)*
- **lifecycle**: New → Reviewed → Accepted / Rejected → Actioned → Measured, with the measured effect once known. *(source: contracts/satellite/ai.yaml#/components/schemas/AiInsight)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Accept / Reject**: Records the decision; a rejection asks for a reason (the false-alarm signal). Accepting does not change anything in trading. *(source: contracts/satellite/ai.yaml#listAiInsights / DI-719)*
- **Open in pricing / F&B / inventory**: Opens the owning module with a draft prepared; the change is made and approved there. *(source: contracts/satellite/ai.yaml#/components/schemas/Suggestion / MATRIX 11.1.37 / MATRIX 3.6.37)*

**Data it reads**: `listAnalyticsAnomalies` (onLoad, What to act on); `listAiInsights` (onLoad, Insights and anomalies)

**Where the user goes next**

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation next-best-action list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation next-best-action untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation next-best-action yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation next-best-action are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A recommendation touches an approval request**: Not produced — AI does not recommend approving or rejecting requests. *(source: DI-735)*
- **Starting maturity**: "Limited historical data" on each card; impact range wider. *(source: contracts/satellite/ai.yaml#/components/schemas/AiMaturity)*

#### Consistency with other screens

- Match `ANL-009`: Recommendations here are insights (decided via the insight lifecycle); proposals on ANL-009 are approval-gated actions. Different words — "Accept" vs "Approve".
- Match `ADM-236`: Pricing next-best actions are shown in P09; the same impact format.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
recommendations:
- High · Pricing · Raise Fast Pass at Motiongate from AED 75.00 to AED 85.00 on Fri–Sat · expected AED 4,200 – 6,800
  a month
- Medium · Production · Prepare 120 fewer burger portions on Thu at Central Kitchen · expected waste saving AED
  540 – 820
- Medium · Revenue · Launch a member offer for inactive annual pass holders · expected AED 18,000 – 31,000
```

#### Permissions

- `listAnalyticsAnomalies` → `REPORT_VIEW_VENUE` (operate) · staff
- `listAiInsights` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.4.17 | System shall support AI-powered anomaly explanations. | Unified Operations Dashboard | CONTRACTED | `listAiInsights` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- An AI layer across all dashboards explains why a metric changed (e.g. why revenue dropped on a given day) and recommends management actions from sales, revenue and attendance trends. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-719)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-058` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-058`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 14: Works in AI Recommendation & Next-Best-Action Center → Convert analytical insights into prioritized business recommendations.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-058?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `AI_USE`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-059` AI Insight History, Evidence & Explainability

**Create a full governance trail for AI-generated analytics and recommendations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-059 |
| Who uses it | venue staff holding `AI_AUDIT_VIEW`, `AI_USE`, `REPORT_VIEW_VENUE` (1 read, 2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `insightId` (navigation) |
| Route | `/analytics/ai-insight-history-evidence-explainability-anl-059` |

**From the AI & Intelligence process.** The governance trail of AI analytics: for each insight or answer - who asked, what data was accessed, what was generated, whether it was exported or shared and whether the recommendation was accepted - with its evidence. The one thing to get right: it is a read-only history with evidence labelled source, calculated or AI-inferred, not a form to fill in.

**Known correction pending (do not draw the wrong version)**

- **pattern configEditor with text fields "Who asked", "What data was accessed", "What answer was generated".** Why: These are columns of a history, read-only; nothing is entered. *(source: screens/P16-venue-analytics.yaml#ANL-059; AI & Intelligence)*

**Fixed on main** (the package already carries these; draw what it says): No operation returns who asked, what was accessed or whether it was exported. (CHG-WIR-012).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Who asked | select field | — | — | — | — | — | — |
| What data was accessed | text field | — | — | — | — | — | — |
| What answer was generated | text field | — | — | — | — | — | — |
| Whether it was exported/shared | text field | — | — | — | — | — | — |
| Whether recommendation was accepted | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listAnalyticsAnomalies` ?from |
| Severity | segmented control | — | Low · Medium · High | `listAnalyticsAnomalies` ?severity |
| Status | select | — | New · Reviewed · Accepted · Rejected · Actioned · Measured | `listAiInsights` ?status |
| Kind | select | — | Anomaly · Forecast deviation · Trend · Opportunity · Executive summary · Root cause · Forecast threshold · Marketing recommendation | `listAiInsights` ?kind |
| Priority | radio group | — | Low · Medium · High · Critical | `listAiInsights` ?priority |
| From | date and time picker | — | — | `listAiInsights` ?from |
| Capability key | text field | — | — | `searchAiDecisions` ?capabilityKey |
| Outcome | select | — | Answered · Refused · Allowed · Blocked · Executed · Failed · Approved then failed · Published · Suggested | `searchAiDecisions` ?outcome |
| Subject ref | text field | — | — | `searchAiDecisions` ?subjectRef |
| Trace | text field | — | — | `searchAiDecisions` ?traceId |
| Policy version | text field | — | — | `searchAiDecisions` ?policyVersion |
| Model version | text field | — | — | `searchAiDecisions` ?modelVersion |
| From | date and time picker | — | — | `searchAiDecisions` ?from |
| To | date and time picker | — | — | `searchAiDecisions` ?to |
| Principal | picker: choose a principal | — | — | `listAiInteractions` ?principalId |
| Outcome | radio group | — | Answered · Refused · Applied · Rejected · Failed | `listAiInteractions` ?outcome |
| … 1 more | | | | `operations.json` |

#### Outputs: what the screen shows and produces

**Shown**

**Decisions** (data table, from `searchAiDecisions`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Trace | text | — |
| Capability key | text | — |
| Task | text | — |
| Subject kind | text | — |
| Subject ref | text | — |
| Inputs ref | text | Where the inputs are kept (Blob or `ai.activity`), never the prompt text itself. |
| Evidence | list or chips (count when long) | The evidence of one decision record, stored with it. |
| Label | chip: Source, Derived, Model inferred | — |
| Kind | text | What it is: `feature`, `rule`, `document`, `metric`, `transaction`, `candidateSet`. |
| Ref | text | Where it came from: a table and id, a document chunk, a metric key. |
| Name | text | — |
| Value | grouped details | — |
| Observed at | 1 Oct 2026, 14:30 | — |
| Producer | text | — |
| Model version | text | — |
| Prompt template version | text | — |
| Feature set version | text | — |
| Knowledge version | text | — |

**Interactions** (data table, from `listAiInteractions`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Conversation | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Audience | chip: Staff, Guest | Billing divides on this. Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop … |
| Subject | the name it points at, never the id | The guest, where the audience is `guest`. `principalId` is null in that case — a guest is not a principal, and attributing their tokens to … |
| Billable to tenant | the name it points at, never the id | Resolved from `scopePath` at write time, not derived later. Billing must not depend on walking a scope tree that has since been reorganised. |
| Capability | text | — |
| Prompt | text | — |
| Response | text | — |
| Sources | list or chips (count when long) | The sources an answer was grounded in, stored with the answer (8.3.70). One `jsonb` column on the row that carries it — … |
| Kind | chip: Document, Product, Entitlement, Report, Record | — |
| ID | text | — |
| Title | text | — |
| Collection | the name it points at, never the id | — |
| Excerpt | text | — |
| Relevance | 1,234.5 | — |
| Outcome | chip: Answered, Refused, Applied, Rejected, Failed | — |
| Refusal reason | text | — |
| Provider | chip: Openai, Gemini, Anthropic, Azure openai, Local llm, Openai compatible | `openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development … |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **history row**: Time, person, question or insight, data accessed (metrics and venues), answer, exported/shared, decision and measured impact; filters by person, venue and kind. *(source: contracts/satellite/ai.yaml#listAiInsights / MoM 18 Sep 4.3)*
- **evidence**: Each evidence item labelled From your data / Calculated / AI inferred, with when it was observed. *(source: contracts/satellite/ai.yaml#/components/schemas/AiEvidenceItem)*

**Data it reads**: `listAnalyticsAnomalies` (onLoad, Past insights and their evidence); `listAiInsights` (onLoad, Insights and anomalies); `searchAiDecisions` (onLoad, The decision records behind each insight); `listAiInteractions` (onLoad, Who asked and what was accessed)

**Where the user goes next**

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The insight history evidence configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the insight history evidence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No insight history evidence configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The move is not allowed from the insight's state. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row:
  when: Mon 28 Sep 09:12
  who: Fatima Al Mansoori
  insight: Online revenue down 14% last weekend
  data: Revenue by channel, Coastal Aqua, 19-27 Sep
  exported: PDF to Omar Haddad
  decision: accepted
```

#### Permissions

- `listAnalyticsAnomalies` → `REPORT_VIEW_VENUE` (operate) · staff
- `listAiInsights` → `AI_USE` (operate) · staff
- `decideAiInsight` → `AI_USE` (operate) · staff
- `searchAiDecisions` → `AI_AUDIT_VIEW` (read) · staff
- `listAiInteractions` → `AI_AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.4.17 | System shall support AI-powered anomaly explanations. | Unified Operations Dashboard | CONTRACTED | `listAiInsights` |
| 8.1.6 | AI-based Dynamic Pricing Promotion | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 8.2.58 | System shall maintain forecasting audit logs. | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 8.3.53 | System shall maintain fraud audit trails. | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 8.6.29 | System shall support recommendation audit trails. | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 8.1.2 | Prompt Logging System shall store prompts submitted to AI services. | Unified Operations Dashboard | CONTRACTED | `listAiInteractions` |
| 8.1.3 | Response Logging System shall store AI-generated responses. | Unified Operations Dashboard | CONTRACTED | `listAiInteractions` |
| 8.1.6 | AI Audit Trail System shall maintain a history of AI-generated actions and user decisions. | Unified Operations Dashboard | CONTRACTED | `listAiInteractions` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-059` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-059`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 16: Works in AI Insight History, Evidence & Explainability → Create a full governance trail for AI-generated analytics and recommendations.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-059?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`, `AI_USE`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-060` AI Analytics Governance & Model Control

**Provide administrators with centralized control over how AI may access and use TICVAI analytics. This screen is critical because Board 9 should not give an LLM unrestricted access to the TICVAI database.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-060 |
| Who uses it | venue staff holding `AI_CONFIGURE`, `AI_USE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Track) and no metric row |
| Offline | online only |
| Opens with | `capabilityKey` (navigation), `templateKey` (navigation) |
| Route | `/analytics/ai-analytics-governance-model-control-anl-060` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-012): publishPromptTemplate (AI_APPROVE) is model governance on the console (ADM-037); on a venue analytics screen prompts are read-only (design-notes correction ai …

**From the AI & Intelligence process.** How AI may use analytics: which AI capabilities touch analytics, their model, autonomy and status, usage and cost, the prompt templates in use and their evaluations - so no LLM has unrestricted access to the database. The one thing to get right: the screen states the rule (the model writes a query spec, Reporting runs it; numbers only from query results) and shows each analytics capability against it.

**Known correction pending (do not draw the wrong version)**

- **Columns are board labels bound to nothing (User, Tenant columns on a venue analytics screen).** Why: Bind to listAiCapabilities filtered to analyticsInsights and getAiUsage grouped by capability. *(source: screens/P16-venue-analytics.yaml#ANL-060; AI & Intelligence)*

**Fixed on main** (the package already carries these; draw what it says): publishPromptTemplate (AI_APPROVE) on a venue analytics screen. (CHG-WIR-012).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Family | select | — | Gateway and models · Governance · Action pipeline · Knowledge retrieval · Assistants · Analytics insights · Configuration assistant · Forecasting · Anomaly detection · Risk intelligence · Recommendations · Decision records … | `listAiCapabilities` ?family |
| Status | segmented control | — | Active · Paused | `listAiCapabilities` ?status |
| Risk class | radio group | — | Low · Medium · High · Critical | `listAiCapabilities` ?riskClass |
| Capability key | text field | — | — | `getEffectiveAiPolicy` ?capabilityKey |
| Scope path | text field | — | — | `getEffectiveAiPolicy` ?scopePath |
| Environment | radio group | — | Development · Sandbox · Staging · Production | `getEffectiveAiPolicy` ?environment |
| Layer | segmented control | — | Platform · Tenant | `listAiModels` ?layer |
| Producer type | radio group | — | Llm · Embedding · Reranker · Classical · Rule | `listAiModels` ?producerType |
| Task | text field | — | — | `listPromptTemplates` ?task |
| Layer | segmented control | — | Platform · Tenant | `listPromptTemplates` ?layer |
| Status | segmented control | — | Draft · Published · Retired | `listPromptTemplates` ?status |
| Release | picker: choose a release | — | — | `listAiEvaluations` ?releaseId |
| Capability key | text field | — | — | `listAiEvaluations` ?capabilityKey |
| Status | radio group | — | Queued · Running · Passed · Failed · Error | `listAiEvaluations` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every analytics governance model** (data table)

| Shows | Format | Notes |
|---|---|---|
| AI service | text | not in the schema: `AI Service` |
| Model | text | not in the schema: `Model` |
| Use case | text | not in the schema: `Use Case` |
| Status | text | not in the schema: `Status` |
| Consumption | text | not in the schema: `Consumption` |
| Cost | text | not in the schema: `Cost` |
| Response time | text | not in the schema: `Response Time` |
| Error rate | text | not in the schema: `Error Rate` |
| Queries | text | not in the schema: `Queries` |
| Tokens/units | text | not in the schema: `Tokens/Units` |
| User | text | not in the schema: `User` |
| Tenant | text | not in the schema: `Tenant` |
| Module | text | not in the schema: `Module` |

**The selected analytics governance model** (detail panel): The pack groups this record's detail under its own headings: “Administrators can enable/disable”, “User”, “Ask TICVAI”, “Analytics / Data Platform”, “Authorized Result”.

| Shows | Format | Notes |
|---|---|---|
| AI service | text | not in the schema: `AI Service` |
| Model | text | not in the schema: `Model` |
| Use case | text | not in the schema: `Use Case` |
| Status | text | not in the schema: `Status` |
| Consumption | text | not in the schema: `Consumption` |
| Cost | text | not in the schema: `Cost` |
| Response time | text | not in the schema: `Response Time` |
| Error rate | text | not in the schema: `Error Rate` |
| Queries | text | not in the schema: `Queries` |
| Tokens/units | text | not in the schema: `Tokens/Units` |
| User | text | not in the schema: `User` |
| Tenant | text | not in the schema: `Tenant` |
| Module | text | not in the schema: `Module` |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** ↓. Each needs attaching to the control it gates, or the screen needs the control.

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **capability rows**: Capability, model, use case, status, autonomy vs ceiling, usage (queries, tokens, cost), p95 response time, error rate. *(source: contracts/satellite/ai.yaml#listAiCapabilities / contracts/satellite/ai.yaml#getAiUsage)*
- **rule banner**: "AI never reads your database directly. It writes a query the platform runs with your permissions; every number comes from that query." *(source: ADR-0054)*
- **evaluations**: Per prompt template version, the evaluation runs and gate results; isolation and permission cases must pass 100%. *(source: contracts/satellite/ai.yaml#listAiEvaluations / contracts/satellite/ai.yaml#runAiEvaluation)*

**Data it reads**: `listAiCapabilities` (onLoad, The capability registry); `getEffectiveAiPolicy` (onLoad, The policy in force for a capability at a scope); `listAiModels` (onLoad, The model catalogue); `listPromptTemplates` (onLoad, The prompt registry); `listAiEvaluations` (onLoad, Evaluation runs)

**Where the user goes next**

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The analytics governance model list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the analytics governance model untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No analytics governance model yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the analytics governance model are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The requested `autonomyLevel` is above the capability's `autonomyCeiling` (AIC-151). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- capability: analytics.ask
  model: gpt-4o (Azure OpenAI, UAE North)
  status: Flagged off until Feb 2027
  autonomy: L1 Advisory
- capability: insights.explain
  model: gpt-4o-mini
  autonomy: L1 Advisory
  queries: 412
  cost: AED 38.40
```

#### Permissions

- `listAiCapabilities` → `AI_USE` (operate) · staff
- `configureAiCapability` → `AI_CONFIGURE` (configure) · staff
- `getEffectiveAiPolicy` → `AI_USE` (operate) · staff
- `listAiModels` → `AI_USE` (operate) · staff
- `listPromptTemplates` → `AI_USE` (operate) · staff
- `runAiEvaluation` → `AI_CONFIGURE` (configure) · staff
- `listAiEvaluations` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-060` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-060`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 18: Works in AI Analytics Governance & Model Control → Provide administrators with centralized control over how AI may access and use TICVAI analytics. This screen is critical because Board 9 should not give an LLM unrestricted access to the TICVAI …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-060?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P16 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-043, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

## Design inputs from the client meetings

**What the client asked for in the meetings and design reviews, for these screens.** Apply every item. They are the client's own requirements and they are later than the reference files: where a reference design or a screen's fields disagree with an item here, the item wins. Newest first; where two items disagree, the newer one wins (anything a later meeting replaced is already left out). An **Open question** is not settled: build the default it states and keep it easy to change. The text in brackets is for traceability and, like everything else in this bundle, never appears on a screen.

### Everywhere, on every app

- Allam (platform-wide requirement): every calendar throughout the platform, not just maintenance, must support day, week and month views, with the day view further broken down by hour from a defined start hour through the day. *(agreed · MoM 17 Sep 2026, 4.2 Preventive Maintenance Planning · DI-907)*
- Minimise the number of separate screens an end user navigates: consolidate related information wherever it can reasonably be shown together, rather than mirroring every workshop board as its own screen. *(agreed · MoM 7 Sep 2026, 4.10 Screen consolidation / 5. Key Decisions · DI-671)*
- Region-configurable tax on pre-discount price (e.g. Egypt: AED 100 ticket with 20% off is paid at AED 80 but taxed on AED 100). Rounding must support up to three decimal places without dropping the third decimal where the currency requires it. *(agreed · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-598)*
- "Powered by TICVAI" is shown consistently across staff and guest-facing surfaces. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-297)*
- Full multi-language support (Arabic and others such as Chinese) consistent with the agreed i18n/RTL architecture. *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-210)*
- The reference system is a functional reference only: its dated UI/UX is not to be replicated; TICVAI delivers equivalent depth with a modern, AI-friendly, easy-to-configure experience. *(agreed · MoM 7 Aug 2026, 23. Reference System Access & Documentation · DI-186)*
- Direction: modern, minimalistic, spacious, cross-device designs that still convey a sense of place (venue or park); Softlabs proposes two to three enhanced visual concepts for TICVAI to steer. *(agreed · MoM 3 Aug 2026, 11. Design Alignment & Team Input · DI-126)*
- Languages: English and Arabic at minimum, with Russian, Spanish and Mandarin. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-080)*
- Clarity first; reduce cognitive load (simple layouts, familiar patterns); consistency ("Use the system. Do not recreate."); accessibility; hierarchy (guide attention with contrast, spacing and visual weight); feedback (every action has a clear response). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - Design Principles in Action · DI-051)*
- Standard components: search bar with Cmd+K; tabs (Overview, Events, Sales, Reports); pagination; badges (New, Pending, Sold Out, Completed); toggle (Off/On); dropdown; removable chip ("VIP x"). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - Example UI Components · DI-050)*
- Spacing on an 8px base grid: 4, 8, 12, 16, 24, 32, 40, 48, 64, 80. Border radius scale 4, 8, 12, 16, 24px, consistent across the platform. Soft shadows: sm 0 1px 2px rgba(0,0,0,.05); md 0 4px 6px rgba(0,0,0,.08); lg 0 10px 15px rgba(0,0,0,.10); xl 0 20px 40px rgba(0,0,0,.14). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 6. Spacing / 7. Border Radius / 8. Shadows · DI-049)*
- Icons: line style, outline, 2px stroke, round corners, clean and consistent. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 5. Icons · DI-048)*
- Component principles: clarity first; consistent spacing on an 8px grid; meaningful colour (colours communicate status and guide the user); accessible by design; mobile ready (components adapt across all screen sizes). Components are consistent, flexible, accessible and composable. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Component principles · DI-045)*
- Empty states have a title, one explanatory line and one action: "No events yet / Create your first event to get started / Create Event"; "No data available / We couldn't find anything to show here / Refresh". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Empty States · DI-044)*
- Notification list: status icon, title, one-line detail and relative time (e.g. "Payment received ... 2m ago", "High demand detected ... 10m ago"), with "View all notifications". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Notifications · DI-042)*
- Forms: label above field; text input, select ("Choose an option"), date picker, toggle, checkbox. Input states: Default, Focused, Filled, Disabled and Error with inline message (e.g. "This field is required"). *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Forms; 08 Design System (p8) - 4. Inputs · DI-040)*
- Card types: event card (title, date and time, venue, "From 120.00 AED"); KPI card (label, value, delta, "vs last 7 days"); onboarding checklist card ("3 of 6 completed": Create Event, Add Staff, Configure Seating, Connect Payment). *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Cards · DI-038)*
- Button hierarchy Primary, Secondary, Tertiary (text) and Icon buttons, each with Default, Hover, Pressed and Disabled states. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Buttons; 08 Design System (p8) - 3. Buttons · DI-036)*
- Regardless of the module a user is working in, the experience should feel like one product, not a collection of separate applications. *(agreed · Design Vision Book 29 Jul 2026, 07 Modules Overview (p7) · DI-034)*
- DO: focus on clarity and hierarchy, use clear simple interactive elements, give relevant information at a glance (card example: "Annual Membership / All Venues / 4.4 (388) / BESTSELLER"). DON'T: clutter and overload (e.g. "-10% NEW PROMO AED 450.00 !!! BOOK NOW!!!"), complex forms and flows, hard-to-read data visualisations. *(agreed · Design Vision Book 29 Jul 2026, 05 Design Principles (p5) - DO / DON'T · DI-033)*
- Eight principles on every screen: User-Centric, AI-First, Simple & Clear (clean layouts, clear hierarchy, minimal noise), Fast & Efficient (optimised for quick actions), Reliable & Secure (permissions, data protection), Data-Driven (data visual, actionable, easy to understand), Scalable, Consistent (same patterns, components and interactions across the ecosystem). *(agreed · Design Vision Book 29 Jul 2026, 05 Design Principles (p5) - Our Design Principles · DI-032)*
- Accessibility: high contrast, readable text, keyboard navigation and inclusive components throughout; WCAG AA standards minimum ("Design for everyone"). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Better Accessibility; 06 Component principles (p6); 08 Design principles in action (p8) · DI-029)*
- AI everywhere: AI insights, recommendations and smart assistance are embedded across the platform, not hidden. AI is not an add-on: it assists, predicts, recommends and automates. *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - How TICVAI improves this concept; 05 Design Principles (p5) - 2. AI-First · DI-027)*
- Global Search: prominent, AI-powered search that finds anything, in the top bar with a Cmd+K shortcut (placeholder e.g. "Search events, customers, orders, venues or ask AI..."). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, item 1; 08 Design System (p8) - Search Bar · DI-025)*
- Visual direction: Purposeful (every element has a clear purpose), Consistent (one visual system across all modules and devices), Clear (easy to scan, understand and act on), Modern. Key takeaway: clean, modern, product-first layout with clear hierarchy and minimal visual noise; deep, modern, trustworthy; built for enterprise scale. *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) · DI-024)*
- The brand is presented consistently across Web Platform, Mobile App and Admin Portal (and print). Ticvai identity, colours and typography are applied consistently across all screens and devices. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand in action; 03 Visual Direction (p3) - Consistent Branding · DI-023)*
- Copy is Professional, Friendly, Clear, Confident, Concise and Helpful. Avoid jargon, overly technical language, clutter, outdated language and complexity. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand voice · DI-022)*
- Brand personality: Modern, AI-First, Enterprise, Premium, Reliable, Minimal, Scalable, Human-Centred. Visual essence: intelligent and forward-thinking, clean and minimal, trustworthy and secure, modern and timeless, scalable and flexible. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand personality / Visual essence · DI-021)*
- Arabic is a core requirement, not later localisation: full Arabic RTL across web, mobile, POS, reports, emails, WhatsApp, SMS, notifications, tickets and receipts, and administrative interfaces. *(agreed · MoM 28 Jul 2026, 27. Internationalisation and Arabic Support · DI-019)*

### Across P16 Venue Analytics

- One consolidated, permission-based reporting/dashboard area: a user opens "dashboards" once and sees all dashboards their access allows (finance sees finance; a CEO sees sales, admissions, access control), with dashboard settings there too - not duplicated dashboard screens inside each functional module. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-721)*
- Dashboards should refresh near-real-time (seconds) so management can monitor sales continuously rather than wait for periodic or end-of-day refreshes. *(agreed · MoM 8 Sep 2026, 4.6 Real-Time Reporting Architecture · DI-711)*
- Dashboards must be mobile-responsive so management (e.g. a CEO outside the venue) can log in from a smartphone via a URL rather than needing a laptop. *(agreed · MoM 8 Sep 2026, 4.1 Rationale for a Native BI/Reporting Platform · DI-696)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- Back office is role-driven from any device: a finance user signing in from a workstation, laptop or home sees only finance reports and related information. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-248)*
- Load/traffic dashboards respect the tenancy model: a venue manager sees traffic for their own venue only. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-061)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- AI Assistant panel: a short framing ("Based on last 30 days, here are 3 actions that can improve your revenue") then actionable recommendations, each with its potential impact (e.g. "Increase pricing for VIP seats, +12%") and a chevron, plus "View all recommendations". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - AI Panels · DI-043)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*
- Reports and historical searches must still retrieve archived transactions when required; the retention period (e.g. keep 3 of 5+ years live) is configurable per customer, archival manual or automated. *(agreed · MoM 28 Jul 2026, 23. Database Optimisation and Archiving · DI-018)*

### In P16 · Analytics

- Finance board: revenue by department and cost centre, shift-closing details, and payment gateway reconciliation, shown as bar and pie charts. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-716)*

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"askReportingQuestion": {"method":"POST","path":"/reports/ask","contract":"reporting","summary":"Natural-language reporting query","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"NaturalLanguageAnswer"},
"configureAiCapability": {"method":"PUT","path":"/governance/capabilities/{capabilityKey}","contract":"ai","summary":"Register a capability, or change its owner, risk class or autonomy","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiCapabilityRegistration","responds":"AiCapabilityRegistration"},
"configureAnomalyDetector": {"method":"PUT","path":"/anomaly-detectors/{detectorKey}","contract":"ai","summary":"Set up anomaly detection on a KPI","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiAnomalyDetector","responds":"AiAnomalyDetector"},
"createDashboard": {"method":"POST","path":"/dashboards","contract":"reporting","summary":"Create a dashboard","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateDashboardRequest","responds":"Dashboard"},
"createForecastScenario": {"method":"POST","path":"/forecast-scenarios","contract":"ai","summary":"Run a what-if","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiForecastScenario","responds":null},
"createReport": {"method":"POST","path":"/reports","contract":"reporting","summary":"Create a custom report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportRequest","responds":"ReportDefinition"},
"decideAiInsight": {"method":"POST","path":"/insights/{insightId}/decide","contract":"ai","summary":"Review, accept, reject or mark an insight actioned","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiInsight"},
"explainMetricChange": {"method":"POST","path":"/insights/explain-metric-change","contract":"ai","summary":"Why did this metric change","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiMetricChangeExplanation"},
"exportForecastVersion": {"method":"POST","path":"/forecast-versions/{versionId}/exports","contract":"ai","summary":"Export a forecast version as a file","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getEffectiveAiPolicy": {"method":"GET","path":"/governance/effective-policy","contract":"ai","summary":"The policy in force for a capability at a scope","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"capabilityKey","in":"query","required":true},{"name":"scopePath","in":"query","required":null},{"name":"environment","in":"query","required":null}],"requestBody":null,"responds":"AiEffectivePolicy"},
"getForecast": {"method":"GET","path":"/forecasts","contract":"ai","summary":"Forecast values","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"definitionKey","in":"query","required":true},{"name":"versionId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"dimensionKey","in":"query","required":null},{"name":"scenarioId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null},{"name":"module","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"listAiCapabilities": {"method":"GET","path":"/governance/capabilities","contract":"ai","summary":"The capability registry","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"family","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"riskClass","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiEvaluations": {"method":"GET","path":"/evaluations","contract":"ai","summary":"Evaluation runs","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"releaseId","in":"query","required":null},{"name":"capabilityKey","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiInsights": {"method":"GET","path":"/insights","contract":"ai","summary":"Insights and anomalies","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiInteractions": {"method":"GET","path":"/interactions","contract":"ai","summary":"Every prompt, response and action","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"principalId","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiModels": {"method":"GET","path":"/models","contract":"ai","summary":"The model catalogue","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"layer","in":"query","required":null},{"name":"producerType","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAnalyticsAnomalies": {"method":"GET","path":"/analytics-anomalies","contract":"reporting","summary":"Numbers that moved more than they should have","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"severity","in":"query","required":null}],"requestBody":null,"responds":"AnalyticsAnomaly"},
"listAnomalyDetectors": {"method":"GET","path":"/anomaly-detectors","contract":"ai","summary":"Anomaly detectors","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"metricKey","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listForecastDefinitions": {"method":"GET","path":"/forecast-definitions","contract":"ai","summary":"What is forecast","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"subject","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPromptTemplates": {"method":"GET","path":"/prompt-templates","contract":"ai","summary":"The prompt registry","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"task","in":"query","required":null},{"name":"layer","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"runAiEvaluation": {"method":"POST","path":"/evaluations","contract":"ai","summary":"Evaluate a candidate","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"saveNaturalLanguageQuery": {"method":"POST","path":"/reports/ask/{conversationId}/save","contract":"reporting","summary":"Save a natural-language answer as a report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReportDefinition"},
"searchAiDecisions": {"method":"GET","path":"/decision-records","contract":"ai","summary":"Find AI decisions","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"capabilityKey","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"subjectRef","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"traceId","in":"query","required":null},{"name":"policyVersion","in":"query","required":null},{"name":"modelVersion","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiAnomalyDetector": {"type":"object","x-ticvai-persistence":"ai.anomaly_detector","description":"**An anomaly detector on one KPI** (C9, AIP-080..095). Configured thresholds on day one; a seasonal robust baseline (median/MAD) and peer comparison across venues as history builds. Detects **aggregate** deviations; actor-level patterns belong to risk, and both share one correlation key (AIP-090).","required":["detectorKey","method"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"detectorKey":{"type":"string"},"source":{"type":"string","enum":["metric","forecast","deviceHealth"],"default":"metric","description":"What is watched (29 September, build): a semantic-layer KPI, a published forecast (8.2.20, 8.2.41), or device status events (8.9.9)."},"metricKey":{"type":"string","nullable":true,"description":"A metric of the semantic layer (Reporting KPI). Required where `source` is `metric`."},"forecastSource":{"type":"object","nullable":true,"description":"Required where `source` is `forecast`; `method` is then `threshold`.","required":["definitionKey","comparator","threshold"],"properties":{"definitionKey":{"type":"string"},"dimensionKey":{"type":"string","nullable":true},"percentile":{"type":"string","enum":["p10","p50","p90"],"default":"p50"},"comparator":{"type":"string","enum":["above","atOrAbove","below","atOrBelow"]},"threshold":{"type":"number"},"thresholdKind":{"type":"string","enum":["absolute","percentOfCapacity"],"default":"absolute","description":"`percentOfCapacity` compares with the period's capacity (occupancy, 8.2.41)."},"horizonDays":{"type":"integer","minimum":1,"maximum":365,"nullable":true,"description":"Only points this many days ahead are compared. Null means the whole horizon."}}},"deviceHealthSource":{"type":"object","nullable":true,"description":"Required where `source` is `deviceHealth`.","properties":{"deviceKinds":{"type":"array","items":{"type":"string"},"description":"DeviceKind values; empty means every kind."},"failureRatePercent":{"type":"number","minimum":0,"maximum":100},"windowMinutes":{"type":"integer","minimum":5,"maximum":1440,"default":60}}},"method":{"type":"string","enum":["threshold","seasonalRobustZ","peerComparison","model"]},"thresholds":{"type":"object","additionalProperties":true,"nullable":true},"sensitivity":{"type":"string","enum":["low","medium","high"],"default":"medium"},"dimensions":{"type":"array","items":{"type":"string"}},"cadence":{"type":"string","enum":["hourly","daily"]},"isActive":{"type":"boolean","default":true},"falseAlarmRate":{"type":"number","nullable":true,"readOnly":true,"description":"Share of its insights rejected over 90 days. The number that decides whether a model is worth it."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiAutonomyLevel": {"type":"integer","minimum":0,"maximum":4,"description":"**One autonomy scale for every capability** (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). 0 disabled; 1 advisory (explains and recommends, nothing is drafted to run); 2 prepare (drafts a proposal a person applies in the owning screen); 3 execute with approval (the plan runs after approval, through owning APIs); 4 controlled auto (runs without approval, only for listed low-risk reversible actions inside pre-approved ranges). **Not the approval tier**: `ProposedAction.approvalLevel` is the tier."},
"AiCapability": {"type":"string","description":"What a capability needs, not which provider serves it. This indirection is what makes \"no provider SDK in capability code\" enforceable.\n**`speechToText` and `textToSpeech` added 18 August (BL-164)** — voice added rather than declined. **Speech is the capability where UAE residency is hardest to satisfy**: the major providers run it in fewer regions than text, and a guest speaking into a kiosk is producing personal data in the moment. `AiProvider.residency` already carries the constraint and **speech is the capability most likely to fail it**, which is why it is separate rather than folded into `chat`.\n","enum":["chat","embedding","vision","rerank","speechToText","textToSpeech"]},
"AiCapabilityFamily": {"type":"string","enum":["gatewayAndModels","governance","actionPipeline","knowledgeRetrieval","assistants","analyticsInsights","configurationAssistant","forecasting","anomalyDetection","riskIntelligence","recommendations","decisionRecords","operationsEvaluation","residencyPrivacy"],"description":"The fourteen capabilities of the AI system design (section 1.1), C1 to C14 in order: gateway and model registry, governance decision point, action pipeline and human oversight, knowledge and retrieval, assistants, analytics assistant and insights, configuration assistant, forecasting and operational requirements, anomaly detection, fraud and risk intelligence, recommendation and upsell engine, decision records and audit, operations/evaluation/cost, residency/privacy/tenancy. **Every registered capability belongs to exactly one**, which is what `AiPolicy.enabledCapabilities` and the usage report group by."},
"AiCapabilityRegistration": {"type":"object","x-ticvai-persistence":"ai.capability","description":"**An entry in the capability registry** (design 3.1 Registry, AIC-144, AIC-145; ADM-520). Nothing becomes an operational AI capability without a row here: owner, function, risk class, autonomy, data categories and lifecycle per environment. `autonomyCeiling` is the platform ceiling for the tenant; a tenant or venue may lower `autonomyLevel`, never raise it (AIC-151).","required":["capabilityKey","family","riskClass","autonomyLevel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string","description":"Stable key, unique per tenant: `assistant.guest`, `forecast.attendance`, `risk.transaction`, `config.assistant`, `recommend.checkout`."},"family":{"$ref":"#/components/schemas/AiCapabilityFamily"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal","description":"The accountable business owner (AIC-144)."},"businessFunction":{"type":"string","nullable":true},"riskClass":{"$ref":"#/components/schemas/AiRiskClass"},"autonomyCeiling":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"readOnly":true,"description":"The first-release ceiling for this capability (design 3.8 table). Read-only to a tenant."},"autonomyLevel":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"description":"The level in force at this scope. At most `autonomyCeiling`."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories the capability reads (ADM-524)."},"lifecycle":{"type":"object","description":"Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.","properties":{"development":{"type":"string","enum":["draft","pilot","active","retired"]},"staging":{"type":"string","enum":["draft","pilot","active","retired"]},"production":{"type":"string","enum":["draft","pilot","active","retired"]}}},"degradationMode":{"type":"string","enum":["rulesOnly","searchOnly","humanHandoff","hidden","failOpen","lastPublished"],"description":"What the capability does when its model or the service is unavailable (design 3.7, AIC-241)."},"status":{"type":"string","enum":["active","paused"],"readOnly":true,"description":"Paused by `pauseAiCapability`: the capability answers from its degradation mode until resumed."},"pausedReason":{"type":"string","nullable":true,"readOnly":true},"pausedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiDecisionRecord": {"type":"object","x-ticvai-persistence":"ai.decision_record","description":"**The standard record for every governed decision** (design 3.9, C12; AIC-193..209): a recommendation summary, a risk assessment, a forecast publication, a plan step, an assistant answer at significant depth, a governance block, a Help me choose suggestion. **Append-only; corrections are annotations; hash-chained per tenant** so tampering is detectable (AIC-203, AIC-204). **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["traceId","capabilityKey","outcome","recordHash"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"traceId":{"type":"string"},"capabilityKey":{"type":"string"},"task":{"type":"string","nullable":true},"subjectKind":{"type":"string","nullable":true},"subjectRef":{"type":"string","nullable":true},"inputsRef":{"type":"string","nullable":true,"description":"Where the inputs are kept (Blob or `ai.activity`), never the prompt text itself."},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"producer":{"type":"string","nullable":true},"modelVersion":{"type":"string","nullable":true},"promptTemplateVersion":{"type":"string","nullable":true},"featureSetVersion":{"type":"string","nullable":true},"knowledgeVersion":{"type":"string","nullable":true},"ruleVersions":{"type":"object","additionalProperties":true,"nullable":true},"governanceOutcome":{"allOf":[{"$ref":"#/components/schemas/AiGovernanceOutcome"}],"nullable":true},"policyVersion":{"type":"string","nullable":true},"approvals":{"type":"object","additionalProperties":true,"nullable":true,"description":"Approval requests and their decisions."},"humanDecision":{"type":"object","additionalProperties":true,"nullable":true,"description":"Override or intervention, where a person changed the outcome."},"executionResult":{"type":"object","additionalProperties":true,"nullable":true},"outcomeRef":{"type":"string","nullable":true,"description":"The business outcome it links to (an order, a published version, a closed case)."},"outcome":{"type":"string","enum":["answered","refused","allowed","blocked","executed","failed","approvedThenFailed","published","suggested"],"description":"`approvedThenFailed` is kept distinct from `executed` (design 1.2 Audit)."},"annotations":{"type":"array","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"byPrincipalId":{"type":"string","format":"uuid"},"note":{"type":"string"}}},"readOnly":true,"description":"Corrections, appended; the original fields are never edited."},"previousHash":{"type":"string","readOnly":true},"recordHash":{"type":"string","readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiEffectivePolicy": {"type":"object","x-ticvai-persistence":"none — resolved from published policy versions, exceptions and ai.policy","description":"**The policy in force for a capability at a scope** (AIC-153, AIC-165; ADM-525, ADM-528): the intersection of the capability, governance policy and the tenant or venue AI policy, with where each part came from.","required":["capabilityKey","autonomyLevel","rules"],"properties":{"capabilityKey":{"type":"string"},"scopePath":{"type":"string"},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"},"autonomyCeiling":{"$ref":"#/components/schemas/AiAutonomyLevel"},"rules":{"type":"array","items":{"type":"object","properties":{"rule":{"$ref":"#/components/schemas/AiGovernanceRule"},"policyKey":{"type":"string"},"version":{"type":"integer"},"scopePath":{"type":"string"}}}},"exceptions":{"type":"array","items":{"$ref":"#/components/schemas/AiPolicyException"}},"conflicts":{"type":"array","items":{"type":"object","properties":{"description":{"type":"string"},"resolvedTo":{"$ref":"#/components/schemas/AiGovernanceOutcome"}}},"description":"Conflicting rules and the more restrictive result they resolved to (AIC-161)."},"resolvedAt":{"type":"string","format":"date-time"}}},
"AiEvaluationRun": {"type":"object","x-ticvai-persistence":"ai.eval_run","description":"One evaluation of a candidate against its baseline: offline golden set, backtest or shadow comparison. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["suiteId","kind","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"suiteId":{"type":"string","format":"uuid","x-ticvai-references":"ai.eval_suite"},"releaseId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.release"},"kind":{"type":"string","enum":["offline","backtest","shadow"]},"candidateRef":{"type":"string"},"baselineRef":{"type":"string","nullable":true},"status":{"type":"string","enum":["queued","running","passed","failed","error"],"readOnly":true},"metrics":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true},"gate":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"The promotion gate thresholds (design 3.5 table) and whether each passed."},"isolationCasesPassed":{"type":"boolean","readOnly":true,"description":"False blocks release, whatever the other metrics say."},"requestedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"startedAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiEvidenceItem": {"type":"object","x-ticvai-persistence":"none — held in jsonb on ai.decision_record.evidence, through AiEvidenceItemList","description":"One piece of evidence behind a decision, **labelled by origin** (AIC-197): read from a source system, derived by a rule or feature, or inferred by a model. An explanation is built from these, never from a model's chain of thought (AIC-192).","required":["label","kind"],"properties":{"label":{"type":"string","enum":["source","derived","modelInferred"]},"kind":{"type":"string","description":"What it is: `feature`, `rule`, `document`, `metric`, `transaction`, `candidateSet`."},"ref":{"type":"string","nullable":true,"description":"Where it came from: a table and id, a document chunk, a metric key."},"name":{"type":"string"},"value":{"type":"object","additionalProperties":true,"nullable":true},"observedAt":{"type":"string","format":"date-time","nullable":true}}},
"AiEvidenceItemList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The evidence of one decision record, stored with it.","items":{"$ref":"#/components/schemas/AiEvidenceItem"}},
"AiForecastDefinition": {"type":"object","x-ticvai-persistence":"ai.forecast_definition","description":"**What is forecast, at what grain, for what horizon, how often and by which producer** (design 3.1 Forecast, 5.2; ADM-500). One forecasting service for the platform: BI's extra subjects are definitions here, not a second forecaster (AIP-036, AIP-037).","required":["definitionKey","subject","grain","horizonDays","producer"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"definitionKey":{"type":"string"},"name":{"type":"string"},"subject":{"type":"string","enum":["attendance","arrivalPattern","productDemand","timeslotDemand","channelPace","revenue","occupancy","attractionUtilisation","queue","entryFlow","staffing","posDemand","fnbDemand","retailDemand","stockDemand","resourceDemand","refunds","cashCollection","membershipRenewals","churn"]},"module":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"}],"description":"**Whose AI this forecast is, and so who publishes it** (Chinmay, 2 October, workbook Q3: \"the permission holder for that module's AI\"; CHG-FUP-004). `publishForecastVersion` requires the permission `contracts/shared/permissions.yaml` `x-ticvai-module-ai-publish` names for this module. Absent on a write, the server takes it from `subject`: ticketing for `attendance`, `arrivalPattern`, `productDemand`, `timeslotDemand`, `channelPace`, `occupancy` and `refunds`; access for `entryFlow` and `attractionUtilisation`; queue for `queue`; fnb for `fnbDemand`; retail for `retailDemand`; inventory for `stockDemand`; resources for `resourceDemand`; membership for `membershipRenewals` and `churn`; core for `revenue`, `staffing`, `posDemand` and `cashCollection`. Proposed, client to correct; a venue may name the module itself. Always present on a read."},"grain":{"type":"string","enum":["hour","day","week","month"]},"dimensions":{"type":"array","items":{"type":"string"},"description":"Breakdowns forecast directly or reconciled to. **Documented keys (29 September, build; 8.2.12, 8.2.14, 8.2.27):** `product`, `channel`, `timeslot`, `gate`, `outlet`, `customerSegment` and `originCountry`. `customerSegment` is the marketing-crm segment (of those in `segmentIds`, else the membership tier) the guest belonged to on the day of the booking; `originCountry` is the guest profile's country, else the order's billing country, else the channel's market, recorded as `unknown` rather than guessed. **The nightly snapshot (design 2.2 C step 1) carries both for every booking and admission**, so a definition that names them is forecast and reconciled by them. Any other key is accepted and forecast only where the snapshot carries it."},"segmentIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"The marketing-crm segments `customerSegment` breaks down by, in priority order where a guest is in several. Empty means membership tiers."},"horizonDays":{"type":"integer","minimum":1,"maximum":730},"refreshCadence":{"type":"string","enum":["hourly","daily","weekly"]},"producer":{"type":"string","enum":["rule","statistical","model","ensemble"],"description":"Which producer is live (design 3.10). A model is promoted only through `promoteAiRelease`. **`ensemble`** (18 September minutes, M18-16): a weighted blend of the rule and statistical producers, and of a promoted model where one exists; the weights are recorded on each version. Setting `ensemble` never brings in an unpromoted model."},"historyWindowMonths":{"type":"integer","minimum":1,"maximum":60,"default":36,"description":"How much of the venue's own history the statistical producer reads (18 September minutes, M18-16: \"36 months of history\"). Imported history (`importVenueHistory`) counts. Less than the window is not an error: the cold-start setting fills the gap."},"coldStart":{"type":"object","description":"**What the forecast stands on before the venue has history** (29 September, AI functions review; forecasting book p.27 \"New Venue / New Product Problem\"). Day one is never empty: the prior is the venue AI settings (typical weekday and weekend attendance, capacity, opening hours) x the starting pattern for the venue type x the UAE calendar x weather, with bookings on hand as a floor. The statistical producer blends own data in as `(k x prior + n x own) / (k + n)`, with `k` = `priorWeightObservations`. The version's `maturity` says which stage it reached.","properties":{"strategy":{"type":"string","enum":["venueSettings","startingPattern","sisterVenue","categoryBaseline","importedHistory"],"default":"venueSettings","description":"`venueSettings` uses the onboarding figures with the venue-type pattern; `sisterVenue` a venue of the same tenant; `categoryBaseline` a product category's own history; `importedHistory` means an import covers the window and the prior only fills unseen holidays."},"sisterVenueId":{"type":"string","format":"uuid","nullable":true,"description":"For `sisterVenue`. Same tenant only (no data is pooled across tenants, AIP-149)."},"priorWeightObservations":{"type":"integer","minimum":1,"maximum":52,"default":4,"description":"`k`: how many own observations the prior is worth (4 same weekdays by default)."},"startingBandPercent":{"type":"integer","minimum":5,"maximum":80,"default":40,"description":"The width of the range while the prior carries most of the weight (about +/-40%)."}}},"producerRef":{"type":"string","readOnly":true},"shadowProducerRef":{"type":"string","nullable":true,"readOnly":true,"description":"Runs alongside and is recorded, never shown (design 3.5)."},"autoPublish":{"type":"boolean","default":false,"description":"Publish without approval when the quality gates pass (autonomy L4, design 3.8). Otherwise an `AI_APPROVE` holder publishes."},"qualityGates":{"type":"object","additionalProperties":true,"nullable":true,"description":"Completeness, blocking signals and accuracy-regression thresholds a version must pass to publish."},"signalKeys":{"type":"array","items":{"type":"string"},"description":"Signal sources this definition may use (ADM-501)."},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastPoint": {"type":"object","x-ticvai-persistence":"ai.forecast_point","description":"One forecast value with its interval: 10th, 50th and 90th percentile (design 5.6: a range, never a bare percentage). Partitioned by target month. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["versionId","targetStart","p50"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"versionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_version"},"scenarioId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.forecast_scenario","description":"Set where the point belongs to a what-if scenario rather than the version itself."},"targetStart":{"type":"string","format":"date-time"},"targetEnd":{"type":"string","format":"date-time"},"dimensionKey":{"type":"string","nullable":true,"description":"Canonical key of the breakdown, e.g. `product=…;channel=web`."},"p10":{"type":"number","nullable":true},"p50":{"type":"number"},"p90":{"type":"number","nullable":true},"unit":{"type":"string"},"drivers":{"type":"object","additionalProperties":true,"nullable":true,"description":"Component decomposition or SHAP contributions, largest first (ADM-506)."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastScenario": {"type":"object","x-ticvai-persistence":"ai.forecast_scenario","description":"**A what-if against a published version** (ADM-507, ADM-517, BO-931). Changes nothing in production; its points are written with `scenarioId`.","required":["baseVersionId","changes"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string"},"baseVersionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_version"},"changes":{"type":"array","items":{"type":"object","required":["lever"],"properties":{"lever":{"type":"string","enum":["price","capacity","openingHours","weather","event","marketing","staffing","closure"]},"target":{"type":"string","nullable":true},"value":{"type":"object","additionalProperties":true,"nullable":true}}},"minItems":1},"status":{"type":"string","enum":["computing","ready","failed"],"readOnly":true},"result":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"Deltas against the base version by subject and period."},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastVersion": {"type":"object","x-ticvai-persistence":"ai.forecast_version","description":"**An immutable forecast version** (AIP-032): producer, model version, data cut-off, horizon and status. Nothing is overwritten; yesterday's actuals are scored against every earlier version.","required":["definitionId","versionNumber","status","basis"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"definitionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_definition"},"versionNumber":{"type":"integer","minimum":1},"module":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"}],"readOnly":true,"description":"The module of the version's definition (`AiForecastDefinition.module`), copied when the version is produced; the module whose AI publish permission `publishForecastVersion` requires (CHG-FUP-004)."},"status":{"type":"string","enum":["running","draft","awaitingApproval","published","superseded","rejected","failed"],"readOnly":true},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producerRef":{"type":"string"},"modelVersion":{"type":"string","nullable":true},"dataCutoffAt":{"type":"string","format":"date-time","description":"The analytical replica watermark the snapshot was taken at."},"horizonStart":{"type":"string","format":"date-time"},"horizonEnd":{"type":"string","format":"date-time"},"qualityChecks":{"type":"object","additionalProperties":true,"readOnly":true,"description":"Each gate and whether it passed."},"publishedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal","description":"Null where the definition auto-published."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiGovernanceOutcome": {"type":"string","enum":["allow","allowWithConditions","prepareOnly","approvalRequired","escalate","block"],"description":"What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). `block` is an answer, not an error, and is logged as outcome `refused`."},
"AiGovernanceRule": {"type":"object","x-ticvai-persistence":"none — held in the jsonb rules column of ai.governance_policy_version, through AiGovernanceRuleList","description":"One rule of a governance policy version: which actions on which data, under which conditions, get which outcome (AIC-147..160).","required":["effect"],"properties":{"effect":{"$ref":"#/components/schemas/AiGovernanceOutcome"},"capabilityKeys":{"type":"array","items":{"type":"string"},"description":"Registered capabilities it applies to. Empty means every capability the policy names."},"actions":{"type":"array","items":{"type":"string","enum":["read","analyze","recommend","generate","prepare","create","modify","publish","execute","delete"]},"description":"ADM-523: what AI may do, from reading to executing."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories (ADM-524), e.g. `customerContact`, `payment`, `financial`, `operational`."},"purposes":{"type":"array","items":{"type":"string"},"description":"Permitted purposes for those categories (AIC-156, AIR-182)."},"maxAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Above this value the effect escalates one step (for example to `approvalRequired`)."},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Roles the rule applies to; empty means every role."},"environments":{"type":"array","items":{"type":"string","enum":["development","sandbox","staging","production"]},"description":"ADM-525. Empty means every environment. **`sandbox`** (18 September minutes, M18-01): the developer sandbox and a tenant's trial environment, governed apart from staging so a rule can allow in sandbox what it blocks in production."},"conditions":{"type":"object","additionalProperties":true,"nullable":true,"description":"Conditions attached to an `allowWithConditions` effect, for example `maskFields` or `requireCitation`."}}},
"AiInsight": {"type":"object","x-ticvai-persistence":"ai.insight","description":"**An insight with a lifecycle** (AIP-181): new, reviewed, accepted or rejected, actioned, measured. Anomalies, forecast deviations, trends and opportunities land here; the narrative binds numbers to results, so a figure can only come from a query (design 8, 5.10).","required":["kind","title","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["anomaly","forecastDeviation","trend","opportunity","executiveSummary","rootCause","forecastThreshold","marketingRecommendation"]},"detectorId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.anomaly_detector"},"metricKey":{"type":"string","nullable":true},"subjectKind":{"type":"string","nullable":true,"enum":["campaign","journey","forecastDefinition","venue"],"description":"What the insight is about where it is not a KPI (29 September, build): a marketing-crm campaign or journey for `marketingRecommendation`, a forecast definition for `forecastThreshold`."},"subjectRef":{"type":"string","nullable":true},"recommendedAction":{"type":"object","additionalProperties":true,"nullable":true,"description":"For `marketingRecommendation`: `{recommendation, parameters}` as `AiMarketingRecommendation`. Applied by a person in the owning module, never here."},"expectedImpact":{"type":"object","additionalProperties":true,"nullable":true,"description":"A range on a named metric (`metric`, `low`, `high`), never a single number (design 5.6)."},"title":{"type":"string"},"narrative":{"type":"string","nullable":true},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"magnitude":{"type":"number","nullable":true},"priority":{"type":"string","enum":["low","medium","high","critical"]},"correlationKey":{"type":"string","nullable":true},"status":{"type":"string","enum":["new","reviewed","accepted","rejected","actioned","measured"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"actionRef":{"type":"string","nullable":true},"measuredImpact":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"detectedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiInteraction": {"type":"object","x-ticvai-persistence":"ai.activity","required":["id","principalId","capability","outcome","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"conversationId":{"type":"string","format":"uuid","nullable":true},"principalId":{"type":"string","format":"uuid"},"audience":{"type":"string","enum":["staff","guest"],"description":"**Billing divides on this.** Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop guests asking questions.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest, where the audience is `guest`. `principalId` is null in that case — **a guest is not a principal**, and attributing their tokens to a staff member would be wrong twice.\n"},"billableToTenantId":{"type":"string","format":"uuid","description":"Resolved from `scopePath` at write time, not derived later. **Billing must not depend on walking a scope tree that has since been reorganised.**\n"},"scopePath":{"type":"string"},"capability":{"type":"string"},"prompt":{"type":"string"},"response":{"type":"string"},"sources":{"$ref":"#/components/schemas/AiSourceList"},"outcome":{"type":"string","enum":["answered","refused","applied","rejected","failed"]},"refusalReason":{"type":"string","nullable":true},"provider":{"$ref":"#/components/schemas/AiProviderKind"},"model":{"type":"string"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"cost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"x-ticvai-column":"cost_amount","description":"What the call cost at the provider. **Money like every other amount** (naming-and-style 5.1) — it replaces an integer `costMinor` that carried no currency or scale, which AED and OMR read differently.\n"},"latencyMs":{"type":"integer"},"maskedFieldCount":{"type":"integer","description":"How many fields were redacted. Zero on a prompt touching guest data is a defect."},"traceId":{"type":"string"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"description":"The `ai.decision_record` this call belongs to, where it was part of a governed decision (AI design 2.3, 3.9). Null for a call audited by this row alone."},"cacheLayer":{"type":"string","nullable":true,"enum":["guardrail","semantic","exact","negative","analytics"],"description":"Which cache answered, where one did (AI design 3.6). Null for a model call."},"createdAt":{"type":"string","format":"date-time"}}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"AiMetricChangeExplanation": {"type":"object","x-ticvai-persistence":"none — computed; written as an ai.insight of kind rootCause when kept","description":"**Why a metric changed** (AIP-176..180, ANL-056): drivers with their contribution, computed from the semantic layer. The narrative binds every figure to a result placeholder (design 8, 5.10).","required":["metricKey","change","drivers"],"properties":{"metricKey":{"type":"string"},"period":{"type":"string"},"comparison":{"type":"string"},"change":{"type":"number"},"changePercent":{"type":"number","nullable":true},"drivers":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string"},"member":{"type":"string"},"contribution":{"type":"number"},"evidence":{"$ref":"#/components/schemas/AiEvidenceItem"}}}},"narrative":{"type":"string","nullable":true},"reliability":{"type":"string","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},"dataAsOf":{"type":"string","format":"date-time"}}},
"AiModel": {"type":"object","x-ticvai-persistence":"ai.model","description":"**The model catalogue** (design 3.1 Registry, 3.3; AIC-013, AIC-026). One row per model a task can be routed to: large language models, embedding and reranking models, and classical models (LightGBM, statistical forecasters) registered the same way so lifecycle, release and audit are uniform. **Platform rows** are mastered in the control plane and replicated read-only into each tenant database with the tenant root as `scopePath`; a tenant row exists only where bring-your-own-key is enabled for the tenant.","required":["layer","modelName","producerType"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"layer":{"type":"string","enum":["platform","tenant"]},"providerKind":{"allOf":[{"$ref":"#/components/schemas/AiProviderKind"}],"nullable":true},"vendor":{"type":"string","nullable":true,"pattern":"^[a-z0-9][a-z0-9-]{1,49}$","description":"**Whose model this is** (CHG-FUP-008): the provider company as `AiProvider.vendor` names it. Bring-your-own-key accepts any vendor, so the curated range carries each vendor's models with the tier they serve; the task-to-tier map (`AiByokEnablement.taskModelMap`) picks the row whose `vendor` matches the tenant's provider. TICVAI adds a new vendor's models after evaluating them (`runAiEvaluation`)."},"producerType":{"type":"string","enum":["llm","embedding","reranker","classical","rule"]},"modelName":{"type":"string","description":"The deployment or model name as the provider knows it, or the package and version for a classical model."},"capabilities":{"type":"array","items":{"$ref":"#/components/schemas/AiCapability"}},"contextTokens":{"type":"integer","nullable":true},"toolCalling":{"type":"boolean","default":false},"structuredOutput":{"type":"boolean","default":false},"languages":{"type":"array","items":{"type":"string"}},"residency":{"type":"string","nullable":true,"description":"Where inference happens. Checked against `tenancy.RegionSettings.allowedAiResidencies`."},"inputCostPerMillionTokens":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"outputCostPerMillionTokens":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"lifecycle":{"type":"object","description":"Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.","properties":{"development":{"type":"string","enum":["draft","pilot","active","retired"]},"staging":{"type":"string","enum":["draft","pilot","active","retired"]},"production":{"type":"string","enum":["draft","pilot","active","retired"]}}},"isDefaultForTasks":{"type":"array","items":{"type":"string"},"description":"Tasks this model is the default for (AIC-010), e.g. `assistant.guest.answer`, `config.extract`."},"curatedRange":{"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**TICVAI's curated range: the tasks this model may serve** (Chinmay, 2 October, workbook Q1, Q2 and Q9; the AI/ML model selection of 2 October; CHG-CSA-001). For each task: the tier it serves at and its rank, 1 being the best-suited model and 2 to 5 the alternatives. **A model may serve a task only where this lists it**: `setAiProvider` refuses any other choice (`422 model-not-curated`), and bring-your-own-key maps each task to the tenant provider's model at the same tier. `byokEligible` false marks the platform-owned tiers (embeddings, reranking, moderation, PII detection, OCR, speech), never served by a tenant key. Money paths (pricing, fraud scores, settlements) stay on classical models.\n","items":{"type":"object","description":"Every entry names `taskKey`, `tier` and `rank`.","properties":{"taskKey":{"type":"string"},"tier":{"type":"string","enum":["small","strong","reasoning","vision","embedding","reranking","moderation","piiDetection","ocr","speech","classical"]},"rank":{"type":"integer","minimum":1,"maximum":5},"byokEligible":{"type":"boolean","default":true}}}},"residencyClasses":{"type":"array","items":{"$ref":"../shared/common.yaml#/components/schemas/AiResidencyClass"},"description":"The tenant residency classes whose calls this model may serve (CHG-CSA-002)."},"taskFitness":{"type":"array","readOnly":true,"description":"**Evaluated fitness per task** (21 September minutes, M21-09, our proposal): a score from the task's golden set (`runAiEvaluation`) and the band the task needs. Below `floor` the model is underpowered for the task; far above `ceiling` it is overpowered (it costs more than the task needs). `setAiProvider` returns a warning (`AiProvider.fitnessWarnings`) when a choice falls outside the band, and ADM-037 shows the band beside `setAiModel`; neither refuses on it.","items":{"type":"object","required":["taskKey","score"],"properties":{"taskKey":{"type":"string"},"score":{"type":"number","minimum":0,"maximum":1},"floor":{"type":"number","minimum":0,"maximum":1},"ceiling":{"type":"number","minimum":0,"maximum":1,"nullable":true},"evaluationRunId":{"type":"string","format":"uuid","nullable":true},"evaluatedAt":{"type":"string","format":"date-time"}}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiPolicyException": {"type":"object","x-ticvai-persistence":"ai.policy_exception","description":"**A temporary, recorded exception to a governance policy** (AIC-162, ADM-526): an expiry, an approver and compensating controls. Governance is never bypassed silently.","required":["policyId","reason","expiresAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"policyId":{"type":"string","format":"uuid","x-ticvai-references":"ai.governance_policy"},"capabilityKey":{"type":"string","nullable":true},"reason":{"type":"string","maxLength":2000},"compensatingControls":{"type":"array","items":{"type":"string"}},"startsAt":{"type":"string","format":"date-time","nullable":true},"expiresAt":{"type":"string","format":"date-time","description":"Required. An exception with no end is a policy change, and goes through publication."},"status":{"type":"string","enum":["active","expired","revoked"],"readOnly":true},"approvedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"revokedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"revokedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"revokeReason":{"type":"string","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiPromptTemplate": {"type":"object","x-ticvai-persistence":"ai.prompt_template","description":"**The prompt registry** (design 3.1 Registry, AIC-022). Versioned and **immutable once published**: a change is a new version, so every decision record can name the exact template it used. Platform templates are replicated read-only like platform models; a tenant may publish its own variant of a task's template.","required":["templateKey","version","layer","task","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"templateKey":{"type":"string"},"version":{"type":"integer","minimum":1},"layer":{"type":"string","enum":["platform","tenant"]},"task":{"type":"string","description":"The gateway task it serves (design 3.3), e.g. `assistant.guest.answer`, `case.summarise`, `guidedChoice.wording`."},"body":{"type":"string","description":"The template text. Stable content first, so the provider's prefix cache applies (ADR-0034)."},"variables":{"type":"array","items":{"type":"string"}},"outputSchema":{"type":"object","additionalProperties":true,"nullable":true,"description":"JSON Schema the structured output must satisfy, where the task has one."},"status":{"type":"string","enum":["draft","published","retired"]},"contentHash":{"type":"string","readOnly":true},"publishedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiProviderKind": {"type":"string","enum":["openai","gemini","anthropic","azureOpenai","localLlm","openaiCompatible"],"description":"`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n**Core42 Compass is reached through `openaiCompatible`** (Chinmay, 2 October: the AI residency decision, amending AI-D02; CHG-CSA-002). Compass is the provider of the `uaeOnly` residency class (common `AiResidencyClass`): Small tier Compass GPT-4.1 mini (or Seraj), Strong tier Compass GPT-5, with OpenAI UAE and then the in-cell open-weights model as the fallback chain. OpenAI UAE is `openai` with a UAE `endpoint`; the in-cell model is `localLlm`.\n**A kind is a protocol, not a vendor** (Chinmay, 2 October, contract follow-ups: BYOK accepts any provider; CHG-FUP-008). Any vendor is accepted, named in `AiProvider.vendor`: Mistral, Cohere or any other is reached through `openaiCompatible` where its API speaks it, which the compatibility test confirms before activation (`AiProviderCompatibility`). A new native adapter is a new value here, a breaking change for a client built earlier that goes out with an approval (`docs/active/breaking-changes.yaml`); until then a vendor without either protocol is refused `422 provider-protocol-unsupported`.\n"},
"AiRiskClass": {"type":"string","enum":["low","medium","high","critical"],"description":"Business, customer, financial, operational, security and compliance impact of a capability or action type (AIC-144, ADM-521). The governance decision point scores against it."},
"AiSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n","items":{"$ref":"#/components/schemas/AiSource"}},
"AnalyticsAnomaly": {"type":"object","x-ticvai-persistence":"reporting.anomaly","description":"BI boards 9.5 and 9.6. **A departure from the series' own behaviour**, which catches what no threshold was set for.\n","properties":{"id":{"type":"string","format":"uuid"},"kpiId":{"type":"string","format":"uuid","nullable":true},"metric":{"type":"string"},"scopePath":{"type":"string"},"detectedAt":{"type":"string","format":"date-time"},"observed":{"$ref":"#/components/schemas/MetricValue"},"expected":{"$ref":"#/components/schemas/MetricValue"},"deviationSigma":{"type":"number","nullable":true},"severity":{"$ref":"#/components/schemas/AnomalySeverity"},"candidateCauses":{"type":"array","description":"**The beginning of the question, not the end of it.**","items":{"type":"object","properties":{"dimension":{"type":"string"},"value":{"type":"string"},"contribution":{"type":"number"}}}},"acknowledgedBy":{"type":"string","format":"uuid","nullable":true},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true}}},
"AnomalySeverity": {"type":"string","description":"Shared by `AnalyticsAnomaly` and the `listAnalyticsAnomalies` filter.","enum":["low","medium","high"]},
"CreateDashboardRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","module","tiles"],"properties":{"name":{"type":"string","maxLength":200},"module":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey","description":"**Which module this dashboard belongs to, and therefore who may see it.** Added 22 September for the command centre: one shell that shows each login the dashboards of the modules it is entitled to. **A dashboard with no module could not be placed in that shell at all** — the field the whole design hangs on did not exist.\n**Required, and `core` is the answer for a dashboard that belongs to no optional module.** An empty field and *belongs everywhere* look identical, and only one of them is a decision — the rule `ModuleKey` already states for screens.\n**Creating one is gated twice**, by `REPORT_MANAGE` and by the module: a principal cannot build a dashboard for a module the tenant has not licensed or that the principal holds no permission in. The server refuses with `409`; a client that hides the option has not enforced anything.\n"},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid","description":"Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. The same rule as `RunReportRequest.venueId`.\n"},"isShared":{"type":"boolean","default":false},"tiles":{"type":"array","minItems":1,"maxItems":24,"items":{"$ref":"#/components/schemas/DashboardTile"}}}},
"CreateReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","category","dataSource","columns","requiredPermission"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"category":{"$ref":"#/components/schemas/ReportCategory"},"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"parameters":{"type":"array","items":{"$ref":"#/components/schemas/ReportParameter"}},"requiredPermission":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission","description":"Permission needed to run this report, from the shared `Permission` vocabulary. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"},"maxDateRangeDays":{"type":"integer","nullable":true,"minimum":1,"default":366,"description":"Guards against a query spanning years of scan events. **When a report sets none, 366 days applies (decided 28 September, audit R158)**, so `runReport`'s date-range 400 always has a limit."}}},
"Dashboard": {"x-ticvai-persistence":"reporting.dashboard + reporting.dashboard_tile","allOf":[{"$ref":"#/components/schemas/CreateDashboardRequest"},{"type":"object","required":["id","ownerPrincipalId","aggregateCost","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid"},"aggregateCost":{"type":"string","enum":["low","medium","high"],"description":"Combined refresh load of every tile."},"archivedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"},"createdAt":{"type":"string","format":"date-time"}}}]},
"DashboardTile": {"x-ticvai-persistence":"reporting.dashboard_tile","type":"object","required":["id","reportId","visualisation","position"],"properties":{"id":{"type":"string","format":"uuid"},"title":{"type":"string"},"reportId":{"type":"string","format":"uuid"},"visualisation":{"type":"string","description":"**Extended 22 September from eight marks to twenty** against `Ticketing_Platform_Native_Dashboard_Visualization_Requirements.pdf`, which names eighteen components and marks every one MVP. Nine were genuinely missing — `combo`, `matrix`, `funnel`, `waterfall`, `treemap`, `scatter`, `map`, `ribbon`, `decompositionTree` — and three are layout variants of marks already here: `area` beside `line`, `donut` beside `pie`, `stackedBar100` beside `stackedBar`.\n**`number` is the source's KPI / card.** Its comparison, variance, trend sparkline and status icon are tile parameters rather than separate marks.\n**Two of the eighteen are deliberately not here** — see `x-ticvai-refuses`. The source lists them as components; the platform already models each of them elsewhere, and a second model of either is the drift this enum exists to prevent.\n","enum":["number","line","area","bar","stackedBar","stackedBar100","combo","pie","donut","table","matrix","gauge","heatmap","funnel","waterfall","treemap","scatter","map","ribbon","decompositionTree"],"x-ticvai-refuses":{"slicer":"**A control, not a mark.** The source's slicer / filter is already `ReportFilter.isParameter` plus `ReportParameter` — a run-time prompt bound to the report. A slicer on the canvas places that parameter; it does not render a result, so it is not a visualisation and a second filter model beside `ReportFilter` would be one somebody keeps in step by hand.","narrative":"**Generated prose belongs with `ai.Suggestion`.** The source's narrative / insight text (*\"Admissions are 12% above last Tuesday\"*) is model output with traceability requirements, not a way of drawing a query result.","cohort":"**Not one of the eighteen.** It appears once in the source as a *usage* — *\"the Customer & Membership dashboard shall use cards, cohort and trend charts\"* — never as a specified component. A cohort view is a `matrix` or `heatmap` over a cohort dimension."},"x-ticvai-note":"**The marks bind through the report's column encodings** (decided 2 October 2026, Chinmay; CHG-FIN-007: build the nine). Superseding the note of 22 September, which left `ReportColumn.role` undecided. Each column of the tile's report carries `role` and `encoding` (and `axis`, `seriesType`, `hierarchyLevel`, `unitLabel` where the mark needs them), and `createDashboard` / `updateDashboard` refuse 422 `tile-encoding-missing` a tile whose report lacks what its mark requires:\n\n| Mark | Requires | |---|---| | `combo` | one `x` dimension; two or more measures, each with `axis` and `seriesType`; `unitLabel` on a secondary axis | | `matrix` | `row` dimensions (with `hierarchyLevel`), optional `column` dimensions, one or more `value` measures | | `funnel` | one `stage` dimension in order (`sortOrder`), one `value` measure | | `waterfall` | one `category` dimension of ordered steps, one `value` measure; the steps are a named measure set (for example Gross sales, Discounts, Refunds, Net revenue) and the last is the total | | `treemap` | one or more `category` dimensions with `hierarchyLevel`, one `size` measure, optional `colour` measure | | `scatter` | an `x` and a `y` measure, a `label` dimension, optional `size` and `colour` | | `map` | one `location` dimension (venue, zone or venue-map point), one `value` measure | | `ribbon` | an `x` dimension (period), a `series` dimension, one `value` measure (rank flow) | | `decompositionTree` | one `value` measure and two or more dimensions with `hierarchyLevel` |\n\nThe other eleven marks bind as before (`number` one measure; `line`, `area`, `bar` and the stacked bars an `x` dimension, optional `series`, one or more `y` measures; `pie`, `donut`, `gauge`, `heatmap`, `table` as their names). **Unchanged**: at most 24 tiles a dashboard, and every tile shows its as-of time and goes stale past its refresh (`KpiValue.asOf`, `stale`; BOARDREQ MOM-2713/2714).\n"},"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose, and not yet specified.** Holds the tile's run parameters (keyed by the report's `ReportParameter.key`, as `RunReportRequest.parameters`) and its display settings — for `number`, the comparison, variance, sparkline and status icon. The per-visualisation display shape waits on the field-wells decision in `visualisation`'s `x-ticvai-note`.\n"},"refreshSeconds":{"type":"integer","minimum":30,"description":"Minimum thirty seconds. A tile refreshing every second is a load problem wearing a convenience costume.\n"},"position":{"type":"object","required":["row","column","width","height"],"properties":{"row":{"type":"integer"},"column":{"type":"integer"},"width":{"type":"integer"},"height":{"type":"integer"}}}}},
"DataSource": {"type":"string","description":"What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n\n**`forecastPoints` added 29 September** (8.2.55, build pass, group G2): the points of published AI forecast versions; see `x-ticvai-forecast-points`.\n\n**Three accreditation sources added 29 September** (12.1.50, build pass): `accreditationApplications`, `accreditationHolders` and `accreditationCredentials`, over `accreditation.application`, `accreditation.holder` and `accreditation.credential`. They are what the accreditation KPIs and any accreditation report or export (`exportReportResult`, csv or xlsx) are built over. **All three name a person**, and `REPORT_EXPORT_PII` gates them as it gates `guests`.\n","enum":["orders","orderLines","payments","refunds","shifts","scanEvents","entitlements","products","inventory","stockMovements","stockCounts","waste","workstations","devices","principals","loyalty","reviews","queueEntries","guests","campaigns","cases","ledgerEntries","workOrders","approvals","purchaseOrders","receipts","requisitions","stockBatches","resourceBookings","delegations","forms","challenges","wallets","resaleListings","accreditationApplications","accreditationHolders","accreditationCredentials","forecastPoints"],"x-ticvai-forecast-points":"**`forecastPoints` added 29 September (build pass, group G2; 8.2.55)**: one row per forecast point (`ai.forecast_point`) of a **published** forecast version (`ai.forecast_version` status `published`), with the definition it belongs to (`ai.forecast_definition`: subject, grain, unit), the period, the dimension key and the p10, p50 and p90 values. Draft, awaiting-approval and superseded versions are not reachable, and scenario points (`scenarioId` set) only with the scenario named as a filter: **a forecast leaves the platform as the one somebody published**. It is how a forecast is exported (`runReport` then `exportReportResult`, csv or xlsx), scheduled or put on a dashboard. Names no person, so `REPORT_EXPORT` is enough. Read from the reporting replica of the AI log database (design 2.4), never from the model service.\n"},
"GeneratedQuery": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n","properties":{"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"compiledSql":{"type":"string","nullable":true,"description":"The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"}}},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"NaturalLanguageAnswer": {"x-ticvai-persistence":"none — computed","type":"object","required":["conversationId","question","interpretation","result","reliability"],"properties":{"conversationId":{"type":"string"},"question":{"type":"string"},"interpretation":{"type":"string","description":"What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."},"semanticSpec":{"allOf":[{"$ref":"#/components/schemas/ReportingSemanticQuerySpec"}],"nullable":true,"description":"What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"},"generatedQuery":{"allOf":[{"$ref":"#/components/schemas/GeneratedQuery"}],"nullable":true,"description":"The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"},"result":{"allOf":[{"$ref":"#/components/schemas/ReportResult"}],"nullable":true,"description":"Null when the question is outside the semantic model."},"dataAsOf":{"type":"string","format":"date-time","nullable":true,"description":"Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."},"reliability":{"$ref":"#/components/schemas/ReportingAnswerReliability"},"unavailableReason":{"allOf":[{"$ref":"#/components/schemas/ReportingUnavailableReason"}],"nullable":true,"description":"Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."},"confidence":{"type":"number","minimum":0,"maximum":1,"deprecated":true,"description":"Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."},"suggestedFollowUps":{"type":"array","items":{"type":"string"}},"modelVersion":{"type":"string"},"tokensUsed":{"type":"integer"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ReportCategory": {"type":"string","enum":["sales","admission","financial","inventory","guest","operations","marketing","workforce","compliance","custom"]},
"ReportColumn": {"x-ticvai-persistence":"reporting.report_column","type":"object","required":["field"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"field":{"type":"string"},"label":{"type":"string"},"aggregation":{"allOf":[{"$ref":"#/components/schemas/Aggregation"}],"default":"none"},"sortOrder":{"type":"integer"},"sortDirection":{"type":"string","enum":["asc","desc"]},"format":{"type":"string","nullable":true},"role":{"type":"string","nullable":true,"enum":["dimension","measure"],"description":"**What the column is to a chart** (decided 2 October 2026, Chinmay; CHG-FIN-007). A `dimension` groups (date, venue, channel, product); a `measure` is aggregated (sum of net revenue, count of admissions). Null on a column only a table shows."},"encoding":{"type":"string","nullable":true,"enum":["category","x","y","series","value","size","colour","location","stage","source","target","row","column","hierarchyLevel","label","tooltip"],"description":"**Which field well the column fills** (CHG-FIN-007), the binding the twenty marks of `DashboardTile.visualisation` need. The per-mark rule is on that field."},"axis":{"type":"string","nullable":true,"enum":["primary","secondary"],"description":"For a measure on a `combo`, the axis it is drawn against. A secondary axis needs its own `unitLabel` (CHG-FIN-007)."},"seriesType":{"type":"string","nullable":true,"enum":["bar","line","area"],"description":"For a measure on a `combo`, how that series is drawn (CHG-FIN-007)."},"hierarchyLevel":{"type":"integer","nullable":true,"minimum":1,"description":"For `matrix` rows and columns, `treemap` nesting and `decompositionTree` levels, the depth of this dimension, 1 outermost. Levels must follow a real hierarchy (DI-709), for example year, month, day, or region, venue, outlet (CHG-FIN-007)."},"unitLabel":{"type":"string","nullable":true,"maxLength":40,"description":"The unit an axis states, for example \"AED\" or \"Admissions\". Required on a secondary axis (CHG-FIN-007)."}}},
"ReportDefinition": {"x-ticvai-persistence":"reporting.report_definition + reporting.report_column + reporting.report_filter","allOf":[{"$ref":"#/components/schemas/CreateReportRequest"},{"type":"object","required":["id","version","isSystem","isRetired","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"version":{"type":"string","description":"The current version. Assigned by the server on each publish; earlier ones are kept as `ReportDefinitionVersion`."},"isSystem":{"type":"boolean","description":"Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). **Clone-only (decided 28 September, audit R096)**: `updateReport` and `deleteReport` refuse it with 409 `system-report`; a venue changes a copy made with `createReport`.\n"},"isRetired":{"type":"boolean"},"estimatedCost":{"type":"string","enum":["low","medium","high"],"description":"Informs whether it may run inline or must be queued."},"createdByPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}}]},
"ReportFilter": {"x-ticvai-persistence":"reporting.report_filter","type":"object","required":["field","operator"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"field":{"type":"string"},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","contains","isNull","isNotNull"]},"value":{"description":"**Open on purpose; its type is the field's.** One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a string. Absent for `in`, `notIn`, `between`, `isNull` and `isNotNull`.\n"},"values":{"type":"array","description":"The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`.","items":{}},"isParameter":{"type":"boolean","default":false,"description":"Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope.\n"}}},
"ReportParameter": {"x-ticvai-persistence":"reporting.report_parameter","type":"object","required":["key","label","type","isRequired"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"},"isRequired":{"type":"boolean"},"defaultValue":{"description":"Open on purpose. A value of this parameter's `type`, used when a run supplies none."}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"ReportingAnswerReliability": {"type":"string","description":"**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},
"ReportingSemanticQuerySpec": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n","required":["metric","period"],"properties":{"metric":{"type":"string","description":"A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."},"dimensions":{"type":"array","maxItems":5,"description":"Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.","items":{"type":"string"}},"filters":{"type":"array","items":{"type":"object","required":["field","operator"],"properties":{"field":{"type":"string","description":"A `SemanticModel` field code."},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","isNull","isNotNull"]},"values":{"type":"array","description":"**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n","items":{}}}}},"period":{"type":"string","description":"ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."},"comparison":{"type":"string","nullable":true,"description":"As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.","enum":["previousPeriod","samePeriodLastYear","target","benchmark"]},"semanticModelVersion":{"type":"integer","readOnly":true,"description":"The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."}}},
"ReportingUnavailableReason": {"type":"string","description":"Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.","enum":["metricNotModelled","dimensionNotModelled","filterNotModelled","comparisonNotAvailable","periodOutsideHistory"]},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]}
}
```
