# P16-analytics-01 — P16 · Analytics (1 of 2)

**10 screens · 25 operations · 58 schemas · 10 permissions**

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

- **Every control that can be refused must be gated.** 10 permissions apply here:
  `AI_USE, DEVICE_VIEW, LEDGER_VIEW, MARKETING_MANAGE, MARKETING_VIEW, ORDER_VIEW, PRODUCT_VIEW, REPORT_MANAGE, REPORT_VIEW_VENUE, USER_MANAGE`. A control nobody can use must say so,
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
| `ANL-001` | Executive Command Center | A | 15 | 17 | 6 | 17 | 2 | 0 | — | notStarted (generated) |
| `ANL-002` | Sales, Revenue & Channel | D | 6 | 1 | 6 | 5 | 1 | 0 | — | notStarted (generated) |
| `ANL-003` | Operational Performance | D | 11 | 27 | 6 | 12 | 1 | 0 | — | notStarted (generated) |
| `ANL-004` | Product Performance | D | 9 | 15 | 6 | 17 | 0 | 0 | — | notStarted (generated) |
| `ANL-005` | Cost, Margin & Profitability | D | 6 | 5 | 6 | 5 | 1 | 0 | — | notStarted (generated) |
| `ANL-006` | Inventory & Waste Intelligence | D | 7 | 17 | 6 | 23 | 1 | 4 | — | notStarted (generated) |
| `ANL-007` | Guest & Conversion Intelligence | D | 28 | 15 | 6 | 18 | 2 | 0 | — | notStarted (generated) |
| `ANL-008` | Demand Forecasting | D | 4 | 1 | 6 | 39 | 2 | 0 | — | notStarted (generated) |
| `ANL-009` | AI Assistant & Action Center | D | 30 | 30 | 6 | 15 | 1 | 0 | — | notStarted (generated) |
| `ANL-010` | Suggestions & Advice | D | 17 | 40 | 6 | 11 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ANL-001` Executive Command Center

**Executive Command Center — across F&B, retail, ticketing and frontline, filtered by domain.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 1 · needs the `analytics` module |
| Block | Block A · ticket #29014 (APP-ANALYTICS-ANL-001) |
| Who uses it | venue staff holding `AI_USE`, `REPORT_VIEW_VENUE` (2 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAlerts` reads the population and `getDashboard` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `domain` (session), `dashboardId` (deepLink), `reportId` (deepLink) · cold entry: **A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries … |
| Route | `/analytics/executive-command-center` |

**What the spec says about it.** **Built 20 August. Answers 3 board screens**: F&B Executive Command Center; Retail Executive Command Center; Enterprise Frontline Operations Dashboard. **Three board screens, one screen with a domain selector.** F&B, Retail and POS each drew an executive command centre and they differ only in which numbers fill the tiles. **Owns POS board frame(s) POS-6A** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Board repointed 24 August.** This screen pointed at `wireframes/POS Board 6.dc.html#pos-6a` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **`wireframe.status` corrected 25 August.** When these screens were repointed from the client pack to their own board on 24 August, the status stayed `designed` — **which claimed a client had drawn a board this package generated.** `derivedFrom` keeps the pack frame, which is where the design came from; `status` describes the file being pointed at, and those are different facts. **Combo, matrix, waterfall, treemap and scatter now bind** (CHG-FIN-007, 2 October 2026) through the report column encodings; the correction that they …

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The executive home of the one consolidated reporting area: a CEO or GM opens it (often on a phone) and in ten seconds knows today's gross sales, net revenue, visitors, transactions and occupancy against target and against the comparison period, plus the few things raised that need a person. It implements the client's Executive Performance board and the Board 1 command-centre first section, and the F&B / Retail / POS executive command centres through one domain selector. The one thing to get right: every money tile names its measure (Gross sales, Net revenue, Takings) and carries its comparison, status band and "as of" time.

**Known correction pending (do not draw the wrong version)**

- **The screen does not declare getKpiValues, yet every headline tile needs target, variance, status and asOf/stale, which only that read returns.** Why: getDashboard returns report results per tile with no target or status; the exec tiles cannot show bands or "vs target" without the KPI read. *(source: contracts/satellite/reporting.yaml#getKpiValues / screens/P16-venue-analytics.yaml#ANL-001; Finance, Ledger & Tax · Reporting & Analytics)*
- **The alert filters are raw text fields "Workstation id", "Shift id", "Item id" on an executive screen.** Why: They expose identifiers (spec leak) and are till/replenishment filters; an executive filters alerts by severity and status only. *(source: screens/P16-venue-analytics.yaml#ANL-001 / contracts/satellite/reporting.yaml#listAlerts; Finance, Ledger & Tax · Reporting & Analytics)*
- **The "Request suggestion" modal asks the user for kind, subjectRef, horizon and context.** Why: An executive cannot pick an internal suggestion kind; the request must be pre-scoped from the tile or alert it is launched from. *(source: screens/P16-venue-analytics.yaml#ANL-001 / contracts/satellite/ai.yaml#requestSuggestion; Finance, Ledger & Tax · Reporting & Analytics)*
- **emptyNoResults says "last week and last month are the useful defaults, not today".** Why: The client's executive boards are explicitly "today vs forecast / vs yesterday"; the default period for this board is Today. *(source: MATRIX 8.7.1 / MATRIX 8.9.8 / MATRIX 6.1.78 / MATRIX 8.2.34 / MATRIX 8.7.24; Finance, Ledger & Tax · Reporting & Analytics)*
- **The Executive Performance board is specified with combo, waterfall and matrix marks.** Why: These marks are in the enum but cannot bind (ReportColumn has no encoding role); draw them only as placeholders flagged "binding pending", or use line + bar + table meanwhile. *(source: MATRIX 8.7.1 / MATRIX 8.7.21 / contracts/satellite/reporting.yaml#/components/schemas/DashboardTile; Finance, Ledger & Tax · Reporting & Analytics)*
- **Gross sales, Net revenue, Refund %, Average ticket value and Tickets sold have no declared source.** Why: MetricSource names no finance measure, and the only seeded money KPI is takings — whose own description calls it "the gross value of payments" and "payments less refunds" in one sentence, which contradict each other. Every headline money tile on this board is unbound until these KPIs are defined. *(source: contracts/satellite/reporting.yaml#/components/schemas/MetricSource / contracts/satellite/reporting.yaml#/components/schemas/ReportingSystemKpi / contracts/satellite/reporting.yaml#getKpiValues / MoM …; Finance, Ledger & Tax · Reporting & Analytics)*
- **The gap note says "no schema with described properties", but KpiValue, Alert and CommandCentre are fully described.** Why: The gap is stale; the binding problem is the missing getKpiValues declaration, not the schemas. *(source: screens/P16-venue-analytics.yaml#ANL-001 / contracts/satellite/reporting.yaml#/components/schemas/KpiValue; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does Gross sales include VAT and fees?** → Gross sales exclude VAT (D-185 default). *(decided by Chinmay, 2026-10-02; DEC-308 / CHG-FIN-007 / CHG-NOTE-003)*
- **Which BI persona (executive viewer) maps to which REPORT_VIEW tier?** → Drawn default accepted: Draw the executive at tenant scope; venue managers see their venue only. *(decided by Chinmay, 2026-10-02; DEC-309 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | radio group | optional | — | Raised · Acknowledged · Resolved · Expired | — | Sends `?status=` to `listAlerts`. | `listAlerts` ?status |
| Severity | segmented control | optional | — | Info · Warning · Critical | — | Sends `?severity=` to `listAlerts`. | `listAlerts` ?severity |
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listAlerts`. | `listAlerts` ?workstationId |
| Shift id | picker: choose a shift (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?shiftId=` to `listAlerts`. | `listAlerts` ?shiftId |
| Item id | picker: choose an item (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?itemId=` to `listAlerts`. | `listAlerts` ?itemId |
| Domain | multi select | — | — | — | — | **The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Refresh | toggle | off | — | `getDashboard` ?refresh |
| Status | select | — | New · Reviewed · Accepted · Rejected · Actioned · Measured | `listAiInsights` ?status |
| Kind | select | — | Anomaly · Forecast deviation · Trend · Opportunity · Executive summary · Root cause · Forecast threshold · Marketing recommendation | `listAiInsights` ?kind |
| Priority | radio group | — | Low · Medium · High · Critical | `listAiInsights` ?priority |
| From | date and time picker | — | — | `listAiInsights` ?from |

**Form: Request suggestion** (modal, opened by *Request suggestion*; *Request suggestion* calls `requestSuggestion`, *Cancel* sends nothing)

**Collects what `requestSuggestion` sends before it is called.** Required: `kind`. Optional: `subjectRef`, `horizon`, `context`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Price · Replenishment · Requisition · Demand forecast · Prep plan · Menu engineering · Staffing · Sla target · Wait time · Upsell · Segmentation · Anomaly …; Anything else is refused — a guest asking for `price` is a guest asking what the venue is willing to … | — | A guest caller may ask for `prepPlan`, `upsell`, `waitTime` and `itinerary` only. | `requestSuggestion` body |
| Subject ref `subjectRef` | text field | optional | — | — | — | — | `requestSuggestion` body |
| Horizon `horizon` | text field | optional | — | — | — | For a forecast — `nextService`, `7d`, `28d`, or an ISO period. | `requestSuggestion` body |
| Context `context` | key and value settings | optional | — | — | — | What the caller already knows. Passed rather than re-fetched so a suggestion made from a screen uses the numbers the screen is showing — advice computed from data the manager … | `requestSuggestion` body |

Errors to draw in the form: 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem)

**Form: Run report** (modal, opened by *Run report*; *Run report* calls `runReport`, *Cancel* sends nothing)

**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Parameters `parameters` | key and value settings | optional | — | — | — | Open on purpose; its shape is the report's. Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. | `runReport` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | `runReport` body |
| Date from `dateFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158). | `runReport` body |
| Date to `dateTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (audit R158). | `runReport` body |
| Force async `forceAsync` | toggle | optional | off | — | — | Queue regardless of size, for a result to be collected later. | `runReport` body |

Errors to draw in the form: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **domain**: Multi-select of the modules this login is entitled to (licensed and holding a permission), never a fixed list; a module the tenant has not licensed is not shown, not greyed. A user with F&B, retail and ticketing sees one combined view by default (all selected). *(source: contracts/satellite/reporting.yaml#getCommandCentre / MoM 2026-09-08 4.11 Dashboard & Reporting Module Consolidation Strategy / DI-721 / DI-387)*
- **period**: Defaults to Today in the venue's time zone for this board (the client's executive tiles are "today vs forecast / vs yesterday"); offers Yesterday, This week, This month, Custom. The generic "last week by default" state text does not apply here (see corrections). *(source: MATRIX 8.7.1 / MATRIX 8.9.8 / MATRIX 8.2.34 / MATRIX 8.7.21 / MATRIX 6.1.78 / MATRIX 8.7.24)*
- **compareTo**: One comparison per view, chosen from Previous period, Same period last year, Target. Default Previous period; the delta and its arrow follow the KPI's "higher is better" flag (refund % going up is red). *(source: contracts/satellite/reporting.yaml#getKpiValues / contracts/satellite/reporting.yaml#/components/schemas/KpiDefinition)*

#### Outputs: what the screen shows and produces

**Shown**

**Every alert** (data table, from `listAlerts`)

| Shows | Format | Notes |
|---|---|---|
| Raised at | 1 Oct 2026, 14:30 | — |
| Severity | chip: Info, Warning, Critical | How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter. |
| Status | chip: Raised, Acknowledged, Resolved, Expired | Where a raised alert is. Shared by `Alert` and the `listAlerts` filter. |
| Acknowledged at | 1 Oct 2026, 14:30 | — |
| Resolved at | 1 Oct 2026, 14:30 | Set when the metric returns to range, automatically. An alert that only a person can close is an alert list that only grows. |
| Escalated at | 1 Oct 2026, 14:30 | Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. |

**Chart** (chart): **Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.

**The selected alert** (detail panel, from `listAlerts`)

| Shows | Format | Notes |
|---|---|---|
| Rule name | text | `AlertRule.name` as it stood when the alert was raised. The line a person reads — a list of rule ids is not an alert panel, and a screen … |
| Metric | chip: Occupancy, Capacity utilisation, Admission rate, No show rate, Conversion, Sales by … | The rule's metric, carried so the alert says what went out of range. |
| Raised at | 1 Oct 2026, 14:30 | — |
| Severity | chip: Info, Warning, Critical | How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter. |
| Status | chip: Raised, Acknowledged, Resolved, Expired | Where a raised alert is. Shared by `Alert` and the `listAlerts` filter. |
| Observed value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Threshold | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Acknowledged at | 1 Oct 2026, 14:30 | — |

**The command centre** (detail panel, from `getCommandCentre`)

| Shows | Format | Notes |
|---|---|---|
| Modules | list or chips (count when long) | — |
| Resolved at | 1 Oct 2026, 14:30 | When the entitlement was evaluated. A licence or role change after this is not reflected until the next read. |

**The dashboard data** (detail panel, from `getDashboard`)

| Shows | Format | Notes |
|---|---|---|
| Tile data | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Request suggestion (primary button) | `requestSuggestion` POST `/ai/suggestions` | inline | Suggestion | 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem) | opens modal first |
| Run report (secondary button) | `runReport` POST `/reports/{reportId}/run` | RunReportRequest | ReportResult | 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **headline KPI row**: In this order: Gross sales, Net revenue, Visitors (admissions), Transactions, Occupancy %. Then a second row: Tickets sold, Average ticket value, Refund %, Variance to target. Each is a number mark with comparison, variance, sparkline and status icon as tile parameters. Occupancy % is admitted-on-site over the configured park capacity, not tickets sold over capacity. *(source: DI-698 / MATRIX 8.7.1 / MATRIX 5.12.72 / MATRIX 8.7.27 / MATRIX 8.7.21 / MATRIX 8.7.25)*
- **measure labels**: Gross sales = issued sales before discounts and refunds; Net revenue = Gross sales minus Discounts minus Refunds (adjusted per finance policy). Never a bare "Revenue" tile. The seeded "takings" KPI is payments less refunds — show it only as "Takings", never as Net revenue. Recognised revenue does not belong on this board's operational row; if shown, it is its own labelled tile. *(source: MATRIX 5.12.6 / contracts/satellite/reporting.yaml#/components/schemas/ReportingSystemKpi)*
- **status band**: KPI status green / amber / red renders as Normal / Warning / Critical with an icon and text, never colour alone; "no target" shows no band at all rather than a neutral colour that reads as fine. *(source: contracts/satellite/reporting.yaml#/components/schemas/KpiValue / DI-704)*
- **freshness**: Each tile shows "As of HH:MM" (or "Updated 40 sec ago" when live) from its own asOf; a stale tile keeps its last number with a "Stale — last updated 09:12" warning instead of blanking. Tiles load independently. *(source: MATRIX 8.7.22 / contracts/satellite/reporting.yaml#/components/schemas/KpiValue)*
- **trend chart**: Line mark: Actual, Forecast, Last year across the day (Day / Week / Month toggle). The forecast series is dashed and labelled "Forecast" with its range band; it never extends the actual line. *(source: MATRIX 8.2.26 / MATRIX 8.7.1 / MATRIX 8.7.25 / MATRIX 8.2.34 / MATRIX 6.1.78 / DI-973 / contracts/satellite/ai.yaml#/components/schemas/AiForecastPoint)*
- **alerts panel**: Critical first, then unacknowledged, then by age; each line shows the rule's name, what went out of range and the observed value against the threshold. Max five on the home, "View all" opens the alert centre. *(source: contracts/satellite/reporting.yaml#listAlerts / contracts/satellite/reporting.yaml#/components/schemas/Alert)*
- **AI executive summary**: Short narrative insights with the time last updated; every figure in a sentence comes from a query result and links to its evidence. Shown as a panel, not as a tile mark (narrative is refused as a mark). *(source: MATRIX 8.4.14 / MATRIX 8.7.31 / MATRIX 8.9.9 / MATRIX 8.7.1 / contracts/satellite/ai.yaml#listAiInsights / contracts/satellite/reporting.yaml#/components/schemas/DashboardTile)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **open a KPI tile**: Drill-through to the owning dashboard with the filter context (domain, venue, period) carried and a visible Back: Net revenue opens Revenue Pulse, Visitors opens Attendance & Footfall, Occupancy opens Capacity & Utilization, Refund % opens refund transaction detail. *(source: MATRIX 8.7.28 / MATRIX 2.12.13 / MATRIX 6.1.78 / MATRIX 8.9.10)*
- **Ask for a suggestion**: Opens the AI panel pre-scoped to the selected tile or alert; the suggestion is advice only, applied by a person in the owning module. Nothing on this screen changes trading. *(source: contracts/satellite/ai.yaml#/components/schemas/Suggestion / DI-719)*

**Data it reads**: `getCommandCentre` (onLoad, The modules this login is entitled to, and each module's …); `getDashboard` (onLoad, Read a dashboard with tile data); `listAlerts` (onLoad, What is currently raised); `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …); `listAiInsights` (onLoad, Insights and anomalies)

**Where the user goes next**

- → `ANL-020` Multi-Site & Performance Comparison: *Multi-Site & Performance Comparison*
- → `ANL-061` BI & Analytics Administration Command Center: *BI & Analytics Administration Command Center*
- → `ANL-021` Dashboard Library: *Dashboard Library*; carries `dashboardId`
- → `ANL-031` Report Catalogue & Library: *Report Catalogue & Library*
- → `ANL-041` Reporting Governance Command Center: *Reporting Governance Command Center*
- → `ANL-051` AI Analytics Command Center: *AI Analytics Command Center*
- → `ANL-002` Sales, Revenue & Channel: *Sales, Revenue & Channel*; carries `dashboardId`, `reportId`
- → `ANL-003` Operational Performance: *Operational Performance*; carries `dashboardId`, `reportId`
- → `ANL-004` Product Performance: *Product Performance*; carries `dashboardId`, `reportId`
- → `ANL-005` Cost, Margin & Profitability: *Cost, Margin & Profitability*; carries `dashboardId`, `reportId`
- → `ANL-006` Inventory & Waste Intelligence: *Inventory & Waste Intelligence*; carries `dashboardId`, `reportId`
- → `ANL-007` Guest & Conversion Intelligence: *Guest & Conversion Intelligence*; carries `dashboardId`, `reportId`
- → `ANL-008` Demand Forecasting: *Demand Forecasting*; carries `dashboardId`
- → `ANL-009` AI Assistant & Action Center: *AI Assistant & Action Center*; carries `alertId`, `reportId`
- → `ANL-010` Suggestions & Advice: *Suggestions & Advice*; carries `suggestionId`
- → `ANL-012` Live Operations Dashboard: *Live Operations Dashboard*
- → `ANL-013` Revenue Pulse: *Revenue Pulse*
- → `ANL-014` Attendance & Footfall Intelligence: *Attendance & Footfall Intelligence*
- → `ANL-015` Capacity & Utilization Monitor: *Capacity & Utilization Monitor*
- → `ANL-016` Sales & Channel Performance: *Sales & Channel Performance*
- → `ANL-017` Customer, Membership & Loyalty Pulse: *Customer, Membership & Loyalty Pulse*; carries `dashboardId`
- → `ANL-018` Alerts & Exception Center: *Alerts & Exception Center*
- → `ANL-019` AI Management Insights: *AI Management Insights*; carries `insightId`
- → `ANL-023` Drag-and-Drop Dashboard Canvas: *Opens Drag-and-Drop Dashboard Canvas*; carries `dashboardId`, `reportId`
- → `ANL-025` KPI Builder: *Opens KPI Builder*
- → `ANL-066` Semantic Model & Business Data Catalogue: *Opens Semantic Model & Business Data Catalogue*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Tiles render in place; **each resolves on its own** so one slow source does not hold the page. |
| Error (`?state=error`) | Could not load. **Trading is unaffected** — this reads and writes nothing. |
| Empty, first run (`?state=emptyFirstRun`) | **A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period. |
| Permission denied (`?state=emptyNoAccess`) | You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem) |

#### Edge cases to draw

- **The CEO opens the bookmarked link on a phone**: KPI row becomes a 2-column stack, charts full-width, alerts collapse to a count; same numbers and freshness labels as desktop. *(source: DI-696 / MoM 2026-09-08 4.1 Rationale for a Native BI/Reporting Platform)*
- **The login holds venue scope only**: Figures cover only that venue; no tenant total and no venue switcher entries beyond its scope; hidden sections are absent, not greyed. *(source: DI-061 / contracts/satellite/reporting.yaml#getCommandCentre)*
- **A tenant with an AED venue and a BHD venue selects "All venues"**: Money tiles show one subtotal per base currency (AED 2 dp, BHD 3 dp); they are never summed into one figure. *(source: contracts/shared/common.yaml#/components/schemas/Money / DI-306)*
- **One tile's source pipeline has not refreshed**: That tile shows its stale warning; the rest render normally; the page is never blanked. *(source: MATRIX 6.1.78)*

#### Consistency with other screens

- Match `ANL-013`: ANL-001 owns the headline numbers only; ANL-013 Revenue Pulse owns the revenue breakdowns and intraday comparisons. The Gross sales and Net revenue tiles must use the same KPI definitions and labels on both.
- Match `ANL-020`: ANL-001 is the single-scope home; site-against-site comparison belongs to ANL-020, not a second table here.
- Match `BO-100`: The back-office venue hub reads the same seeded takings/admissions KPIs; same labels and same "as of" pattern.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Aquaventure Waterpark, Dubai (base currency AED)
asOf: Wed 30 Sep 2026, as of 14:32
grossSales: AED 1,284,350.00 (vs AED 1,190,200.00 same day last week, +7.9%)
discounts: AED 96,420.00
refunds: AED 18,240.00
netRevenue: AED 1,169,690.00 — target AED 1,250,000.00, −6.4%, Warning
ticketsSold: 9,412 (ticket revenue AED 1,113,910.20, average ticket value AED 118.35)
admissions: 8,876
refundRate: 1.42%
occupancy: 71.4% (7,140 on site of 10,000 configured capacity) — Normal
transactions: 6,318
bahrainVenue: Gross sales BHD 18,402.135 shown as its own subtotal
alerts:
- Critical · Wave Pool gate 3 offline · 14:05 · not acknowledged
- Warning · Refunds above threshold at Beach Kiosk · AED 2,140.00 against AED 1,500.00
aiSummary: Net revenue is 6.4% below target; Coffee House and Beach Kiosk account for most of the gap.
```

#### Permissions

- `getCommandCentre` → `REPORT_VIEW_VENUE` (operate) · staff
- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `listAlerts` → `REPORT_VIEW_VENUE` (operate) · staff
- `requestSuggestion` → `AI_USE` (operate) · staff, guest
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff
- `listAiInsights` → `AI_USE` (operate) · staff

**A refused user sees:** You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.28 | Kiosks shall provide an AI assistant to guide guests through ticket selection, promotions, FAQs, recommendations, and checkout. | Ticketing Sales | CONTRACTED | `requestSuggestion` |
| 4.1.16 | Analyze menu performance and profitability. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.19 | Recommend actions to reduce waste and spoilage. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.20 | Recommend pricing and promotion strategies. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.8.15 | AI predicts potential food waste and recommends actions. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 5.4.24 | Segment customers automatically. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| 5.6.27 | Recommend staffing adjustments, ride allocation, and queue balancing. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| 5.6.36 | The system shall estimate queue wait times using historical and real-time operational data. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| 8.9.9 | AI shall identify operational risks, anomalies, congestion, capacity issues, device failures, staffing shortages, and service disruptions and provide recommendations. | Unified Operations Dashboard | CONTRACTED | `requestSuggestion` |
| 15.4.7 | Inventory Optimization - System shall optimize inventory levels. | Inventory Management | CONTRACTED_PARTIAL | `requestSuggestion` |
| 22.2.25 | AI Audience Classification | Marketing & CRM | CONTRACTED | `requestSuggestion` |
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Command centre first section: facility-wide totals for revenue, visitors, transactions and occupancy % (calculated against configured park capacity). *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-698)*
- The platform ships a standard set of default dashboards out of the box, plus the ability for the business to design additional custom dashboards without SQL or programming knowledge. *(agreed · MoM 8 Sep 2026, 4.1 Rationale for a Native BI/Reporting Platform · DI-697)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-001` · status **notStarted** · provenance generated · **Drawn as POS-6A in the client POS pack.** The pack's frame is the specification — it carries operations, states, entry params and exits, and it is better specified than anything derived from the …
- Derived from `wireframes/POS Board 6.dc.html#pos-6a`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `FnB Board 6.dc.html#fnb-6a`, `POS Board 6.dc.html#pos-6a`, `Retail Board 6.dc.html#ret-6a`
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-001?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Request suggestion, Run report.
- [ ] Every transition is wired: `ANL-020`, `ANL-061`, `ANL-021`, `ANL-031`, `ANL-041`, `ANL-051`, `ANL-002`, `ANL-003`, `ANL-004`, `ANL-005`, `ANL-006`, `ANL-007`, `ANL-008`, `ANL-009`, `ANL-010`, `ANL-012`, `ANL-013`, `ANL-014`, `ANL-015`, `ANL-016`, `ANL-017`, `ANL-018`, `ANL-019`, `ANL-023`, `ANL-025`, `ANL-066`.
- [ ] Every gated control is gated: `AI_USE`, `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 7 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-002` Sales, Revenue & Channel

**Sales, Revenue & Channel — across F&B, retail, ticketing and frontline, filtered by domain.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-002 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (compact density): `getDashboard` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `venueId` (session), `domain` (session), `dashboardId` (deepLink), `reportId` (deepLink) · cold entry: **A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries … |
| Route | `/analytics/sales-revenue-channel` |

**What the spec says about it.** **Built 20 August. Answers 2 board screens**: Sales, Revenue & Channel Analytics; Sales, Revenue & Channel Analytics. **The same screen twice in the client set, word for word.** Revenue by channel is revenue by channel whether the line is a burger or a t-shirt. **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6l` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The sales board for a commercial or F&B/retail manager: how products and attractions sell by channel, what discounts and upsell/cross-sell did, deferred against recognised revenue, and sales forecast against target. It answers the 8 Sep "Sales board" input and the client packs' FNB-6B / RET-6L frame. The one thing to get right: sales measures (gross, net) and accounting measures (recognised, deferred) sit in separate, labelled sections and are never added together or drawn on one axis.

**Known correction pending (do not draw the wrong version)**

- **The screen declares no KPI read, but the board must show forecast vs target and variance.** Why: getDashboard tiles carry report results only; target, variance and status come from getKpiValues, and the forecast from ai.getForecast. *(source: screens/P16-venue-analytics.yaml#ANL-002 / contracts/satellite/reporting.yaml#getKpiValues / contracts/satellite/ai.yaml#getForecast; Finance, Ledger & Tax · Reporting & Analytics)*
- **The notes say the screen answers "Sales, Revenue & Channel Analytics" twice and is the same as the F&B and retail frames, but DI-715 scopes it together with ANL-016.** Why: Two sales boards with no stated ownership will drift; the split must be decided (see consistency). *(source: DI-715 / screens/P16-venue-analytics.yaml#ANL-002; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is "B2C" a reporting group (Web + Mobile + Kiosk) or should Channel gain a b2c value?** → Drawn default accepted: Show the platform channels, with B2C as a labelled group. *(decided by Chinmay, 2026-10-02; DEC-310 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **Merge ANL-002 into ANL-016, or keep both with the split proposed?** → Drawn default accepted: Keep both with the split proposed. *(decided by Chinmay, 2026-10-02; DEC-311 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Domain | multi select | — | — | — | — | **The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Refresh | toggle | off | — | `getDashboard` ?refresh |

**Form: Run report** (modal, opened by *Run report*; *Run report* calls `runReport`, *Cancel* sends nothing)

**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Parameters `parameters` | key and value settings | optional | — | — | — | Open on purpose; its shape is the report's. Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. | `runReport` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | `runReport` body |
| Date from `dateFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158). | `runReport` body |
| Date to `dateTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (audit R158). | `runReport` body |
| Force async `forceAsync` | toggle | optional | off | — | — | Queue regardless of size, for a result to be collected later. | `runReport` body |

Errors to draw in the form: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **channel filter**: Channel values are the platform's closed list — POS, Kiosk, Web, Mobile app, B2B, OTA, Call centre. When the client's "B2C" grouping is used, it is a named group of Web + Mobile app + Kiosk, shown as such in the legend. *(source: contracts/spine/catalogue.yaml#/components/schemas/Channel / MATRIX 8.7.4 / MoM 2026-08-18 4.2 Recipes, Operating Hours & Service Channels / MATRIX 1.4.7)*
- **domain**: Ticketing, F&B, Retail; the same product-by-channel analysis whatever the domain, only the item vocabulary differs. *(source: screens/P16-venue-analytics.yaml#ANL-002 / DI-721)*

#### Outputs: what the screen shows and produces

**Shown**

**The dashboard data** (detail panel, from `getDashboard`)

| Shows | Format | Notes |
|---|---|---|
| Tile data | list or chips (count when long) | — |

**Chart** (chart): **Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run report (primary button) | `runReport` POST `/reports/{reportId}/run` | RunReportRequest | ReportResult | 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **product / attraction by channel**: Table (or stacked bar for the top 10) of Net revenue and units per product by channel, sorted by Net revenue descending, with a totals row computed server-side. Top 10 by default, "Show all" pages. *(source: DI-715 / MoM 2026-09-08 4.9 Sales, Finance, Operations & CRM Boards)*
- **discounts and upsell / cross-sell**: Discounts shown as a negative bridge item against Gross sales, not as revenue. Upsell and cross-sell revenue is attributed revenue and labelled "Attributed to upsell" so it is not read as additional sales on top of Net revenue. *(source: DI-715 / MoM 2026-09-08 4.9 Sales, Finance, Operations & CRM Boards / contracts/satellite/reporting.yaml#/components/schemas/MetricSource)*
- **deferred vs recognised**: Separate section "Revenue recognition": Recognised revenue and Deferred revenue for the period, by channel. POS sales recognise at sale; online tickets on visit or redemption; gift cards on redemption; annual passes straight-line or per visit; breakage on expiry. Say "Recognised", never "Realised". *(source: MoM 2026-09-08 4.9 Sales, Finance, Operations & CRM Boards / MATRIX 5.12.6 / contracts/spine/finance.yaml#/components/schemas/RecognitionMethod)*
- **forecast vs target**: Line: Actual net revenue to date, Forecast (dashed, with its p10–p90 range band) and Target. The forecast series is always labelled "Forecast". *(source: MoM 2026-09-08 4.9 Sales, Finance, Operations & CRM Boards / DI-973 / contracts/satellite/ai.yaml#/components/schemas/AiForecastPoint)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **click a channel in any visual**: Cross-filters every subscribed visual and the product table to that channel; a filter breadcrumb shows it with Clear. *(source: MATRIX 6.1.78 / MATRIX 8.7.28 / MATRIX 8.9.10)*
- **drill a product row**: Product → performance/time slot → orders (drill-through to the order list with filters carried and Back visible). *(source: MATRIX 8.7.28 / MATRIX 8.9.10 / DI-709)*
- **Run report**: Runs the underlying report for export; large results return asynchronously with "We'll notify you when it is ready". *(source: contracts/satellite/reporting.yaml#runReport)*

**Data it reads**: `getDashboard` (onLoad, Read a dashboard with tile data); `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Executive Command Center*; carries `dashboardId`, `reportId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Tiles render in place; **each resolves on its own** so one slow source does not hold the page. |
| Error (`?state=error`) | Could not load. **Trading is unaffected** — this reads and writes nothing. |
| Empty, first run (`?state=emptyFirstRun`) | **A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period. |
| Permission denied (`?state=emptyNoAccess`) | You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158) |

#### Edge cases to draw

- **A day with 10,000+ order lines is drilled to transactions**: Paged, virtualised table; the UI stays responsive; totals come from the server, not summed on screen. *(source: DI-710)*
- **Refunds exceed sales for a product in the period**: Net revenue shows as a negative value in red with a minus sign; bars below zero baseline. *(source: MATRIX 6.1.78)*

#### Consistency with other screens

- Match `ANL-016`: Overlap (DI-715 is scoped to both). Proposed split: ANL-016 owns the cross-channel KPI scorecard and channel mix (gross, net, transactions, conversion, basket, discount use); ANL-002 owns product/attraction-by-channel detail, upsell/cross-sell and the revenue-recognition section. Both read the same KPI definitions.
- Match `BO-1081`: Recognised and deferred figures must equal the Finance Dashboard's for the same period and scope.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Dubai Parks — Motiongate (AED)
period: September 2026 to date
rows:
- Motiongate 1-Day Pass · Web · 21,406 units · Net revenue AED 6,250,552.00
- Motiongate 1-Day Pass · OTA · 9,880 units · Net revenue AED 2,617,212.00
- Fast Pass add-on · POS · 3,114 units · Net revenue AED 404,820.00 · attributed to upsell
recognition: Recognised revenue AED 7,912,400.00 · Deferred revenue AED 1,355,164.00 (tickets dated after today)
forecast: 'Forecast for 30 Sep: AED 412,000.00 (range AED 368,000.00 – AED 451,000.00)'
```

#### Permissions

- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 13.3.14 | APIs shall expose operational, financial, attendance, membership and sales reporting data. | Developer & API Management | CONTRACTED | `runReport` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Sales board: product/attraction performance by sales channel, discounts, upsell/cross-sell results, deferred vs realised revenue, and sales forecast vs target. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-715)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-002` · status **notStarted** · provenance generated · **Drawn as RET-6L in the client Retail pack.**
- Derived from `wireframes/Retail Board 6.dc.html#ret-6l`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `FnB Board 6.dc.html#fnb-6b`, `Retail Board 6.dc.html#ret-6l`

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (1 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-002?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run report.
- [ ] Every transition is wired: `ANL-001`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-003` Operational Performance

**Operational Performance — across F&B, retail, ticketing and frontline, filtered by domain.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-003 |
| Who uses it | venue staff holding `DEVICE_VIEW`, `REPORT_VIEW_VENUE`, `USER_MANAGE` (1 read, 1 operate, 1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAlerts` reads the population and `getDashboard` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `domain` (session), `dashboardId` (deepLink), `reportId` (deepLink) · cold entry: **A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries … |
| Route | `/analytics/operational-performance` |

**What the spec says about it.** **Built 20 August. Answers 4 board screens**: Outlet, Service & Guest Performance; Store & Operational Performance; Venue Operations Dashboard and 1 more. **Four board screens.** Outlet, store, venue and department are the same question at four levels of `scope_path` — which is a filter, not four screens. **Owns POS board frame(s) POS-6B, POS-6C, POS-6D** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Board repointed 24 August.** This screen pointed at `wireframes/POS Board 6.dc.html#pos-6b` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Period performance of operating units — outlet, store, venue or department — for an operations or F&B / retail manager: revenue, transactions, items sold, attachment rate, service and stock exceptions, ranked by unit. It answers the client's F&B / Retail board and the packs' outlet/store/venue operations frames (four board screens, one screen filtered by scope level). The one thing to get right: one table of units with the same columns at every scope level, drillable down the hierarchy, not four different layouts.

**Known correction pending (do not draw the wrong version)**

- **The screen lists every principal (identity listPrincipals, 9 columns) and every registered device (12 columns) as tables.** Why: A staff directory and a device inventory are not performance analytics; they expose personal data and duplicate admin screens. Device health belongs as a tile drilling to the device screen. *(source: screens/P16-venue-analytics.yaml#ANL-003 / MATRIX 8.3.73; Finance, Ledger & Tax · Reporting & Analytics)*
- **Alert filters "Workstation id", "Shift id", "Item id" are free-text id fields.** Why: Identifiers are spec leaks; use pickers (workstation, shift) or drop them. *(source: screens/P16-venue-analytics.yaml#ANL-003; Finance, Ledger & Tax · Reporting & Analytics)*
- **The screen has no KPI read for the cards it must show.** Why: Revenue, transactions and items sold by scope with comparison come from getKpiValues (groupBy/interval), not from getDashboard alone. *(source: contracts/satellite/reporting.yaml#getKpiValues; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How is attachment rate defined (items per transaction, share of tickets with an F&B purchase)?** → Drawn default accepted: Show the tile with "Definition pending". *(decided by Chinmay, 2026-10-02; DEC-312 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **How is the outlet performance score composed?** → Drawn default accepted: Omit the score column. *(decided by Chinmay, 2026-10-02; DEC-313 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | radio group | optional | — | Raised · Acknowledged · Resolved · Expired | — | Sends `?status=` to `listAlerts`. | `listAlerts` ?status |
| Severity | segmented control | optional | — | Info · Warning · Critical | — | Sends `?severity=` to `listAlerts`. | `listAlerts` ?severity |
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listAlerts`. | `listAlerts` ?workstationId |
| Shift id | picker: choose a shift (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?shiftId=` to `listAlerts`. | `listAlerts` ?shiftId |
| Item id | picker: choose an item (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?itemId=` to `listAlerts`. | `listAlerts` ?itemId |
| Domain | multi select | — | — | — | — | **The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Refresh | toggle | off | — | `getDashboard` ?refresh |
| Workstation | picker: choose a workstation | — | — | `listDevices` ?workstationId |
| Kind | select | — | Receipt printer · Ticket printer · Label printer · Cash drawer · Barcode scanner · RFID reader · NFC reader · Card reader · ID reader · Biometric reader · Access reader · Payment terminal … | `listDevices` ?kind |
| Scope path | text field | — | — | `listPrincipals` ?scopePath |
| Is active | toggle | — | — | `listPrincipals` ?isActive |

**Form: Run report** (modal, opened by *Run report*; *Run report* calls `runReport`, *Cancel* sends nothing)

**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Parameters `parameters` | key and value settings | optional | — | — | — | Open on purpose; its shape is the report's. Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. | `runReport` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | `runReport` body |
| Date from `dateFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158). | `runReport` body |
| Date to `dateTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (audit R158). | `runReport` body |
| Force async `forceAsync` | toggle | optional | off | — | — | Queue regardless of size, for a result to be collected later. | `runReport` body |

Errors to draw in the form: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **scope level**: Venue → department/outlet → workstation, following the declared drill hierarchy; the user cannot pick a level above their scope. *(source: MATRIX 8.7.28 / contracts/satellite/reporting.yaml#getKpiValues / DI-061)*
- **period**: Defaults to Yesterday (a performance review of a closed day); This week / Last week / This month / Custom. *(source: screens/P16-venue-analytics.yaml#ANL-003)*

#### Outputs: what the screen shows and produces

**Shown**

**Every alert** (data table, from `listAlerts`)

| Shows | Format | Notes |
|---|---|---|
| Raised at | 1 Oct 2026, 14:30 | — |
| Severity | chip: Info, Warning, Critical | How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter. |
| Status | chip: Raised, Acknowledged, Resolved, Expired | Where a raised alert is. Shared by `Alert` and the `listAlerts` filter. |
| Acknowledged at | 1 Oct 2026, 14:30 | — |
| Resolved at | 1 Oct 2026, 14:30 | Set when the metric returns to range, automatically. An alert that only a person can close is an alert list that only grows. |
| Escalated at | 1 Oct 2026, 14:30 | Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. |

**Every registered device** (data table, from `listDevices`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Receipt printer, Ticket printer, Label printer, Cash drawer, Barcode scanner, RFID … | `mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no … |
| Driver | text | Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change … |
| Identifier | text | — |
| Model | text | — |
| Push token | text | BL-163. Guest devices register for push and staff devices did not — `registerGuestDevice` exists with a token, platform and failure count … |
| Push failure count | 1,234 | Consecutive failures. A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a … |

**Every principal** (data table, from `listPrincipals`)

| Shows | Format | Notes |
|---|---|---|
| Username | text | — |
| Display name | text | — |
| Is active | yes / no (icon or chip) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Past this, resolution returns DENY regardless of grants. |
| Last login at | 1 Oct 2026, 14:30 | — |

**Chart** (chart): **Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.

**The selected alert** (detail panel, from `listAlerts`)

| Shows | Format | Notes |
|---|---|---|
| Rule name | text | `AlertRule.name` as it stood when the alert was raised. The line a person reads — a list of rule ids is not an alert panel, and a screen … |
| Metric | chip: Occupancy, Capacity utilisation, Admission rate, No show rate, Conversion, Sales by … | The rule's metric, carried so the alert says what went out of range. |
| Raised at | 1 Oct 2026, 14:30 | — |
| Severity | chip: Info, Warning, Critical | How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter. |
| Status | chip: Raised, Acknowledged, Resolved, Expired | Where a raised alert is. Shared by `Alert` and the `listAlerts` filter. |
| Observed value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Threshold | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Acknowledged at | 1 Oct 2026, 14:30 | — |

**The dashboard data** (detail panel, from `getDashboard`)

| Shows | Format | Notes |
|---|---|---|
| Tile data | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run report (primary button) | `runReport` POST `/reports/{reportId}/run` | RunReportRequest | ReportResult | 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **KPI cards**: Net revenue, Transactions, Items sold, Attachment rate, Stock and service exceptions, each against the previous period. *(source: MATRIX 8.7.34 / MATRIX 8.2.29 / MATRIX 6.1.10 / MATRIX 6.1.61 / MATRIX 6.1.63 / MATRIX 4.4.17 / MATRIX 8.9.4)*
- **outlet performance table**: Columns Outlet, Net revenue (AED), Orders, Average order value (AED), Margin %, Service level %, Availability, with a Total / Average row; sorted by Net revenue. A performance-score column and its Excellent / Good / At risk band appear only once the score is defined. *(source: MATRIX 4.5.25 / MATRIX 8.7.1)*
- **hourly heatmap**: Heatmap of net revenue (or orders) by hour × outlet, with a legend and the values available as an accessible table. *(source: MATRIX 6.1.58)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **select an outlet row**: Cross-filters the cards and heatmap to that outlet; drill-down goes to its workstations. *(source: MATRIX 6.1.78 / MATRIX 8.7.28)*
- **open a stock or service exception**: Drill-through to the owning screen (inventory exception, kitchen performance) with context carried. *(source: MATRIX 8.9.10 / MATRIX 2.12.1 / MATRIX 16.9.58)*

**Data it reads**: `getDashboard` (onLoad, Read a dashboard with tile data); `listAlerts` (onLoad, What is currently raised); `listDevices` (onLoad, List registered devices); `listPrincipals` (onLoad, List principals); `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Executive Command Center*; carries `dashboardId`, `reportId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Tiles render in place; **each resolves on its own** so one slow source does not hold the page. |
| Error (`?state=error`) | Could not load. **Trading is unaffected** — this reads and writes nothing. |
| Empty, first run (`?state=emptyFirstRun`) | **A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period. |
| Permission denied (`?state=emptyNoAccess`) | You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158) |

#### Edge cases to draw

- **A till on the selected day has not closed yet**: The outlet row is marked "Includes an open till" rather than presenting a partial figure as the day's total. *(source: F74 step 2)*
- **A department has no sales in the period**: Row shown with zeroes and a muted style, not dropped, so the ranking is complete. *(source: designer default)*

#### Consistency with other screens

- Match `ANL-012`: ANL-012 owns "now" (live, seconds); ANL-003 owns closed periods. Same outlet names and the same Net revenue definition.
- Match `ANL-014`: DI-717 (entries, exits, per-turnstile, park capacity) is scoped to ANL-003 but its numbers belong to ANL-014 / ANL-015; ANL-003 links to them rather than repeating access-control tiles.
- Match `ANL-006`: Stock exceptions here are counts that drill into ANL-006; the same exception definitions on both.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Aquaventure Waterpark (AED)
period: Yesterday, Tue 29 Sep 2026
outlets:
- Main Restaurant · AED 84,215.50 · 1,402 orders · AOV AED 60.07 · margin 68.2% · service level 94%
- Coffee House · AED 21,890.00 · 1,955 orders · AOV AED 11.20 · margin 74.5% · service level 97%
- Beach Kiosk · AED 15,320.25 · 1,288 orders · AOV AED 11.89 · margin 61.0% · service level 88%
- VIP Lounge · AED 32,600.00 · 214 orders · AOV AED 152.34 · margin 71.9% · service level 99%
total: AED 154,025.75 · 4,859 orders
```

#### Permissions

- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `listAlerts` → `REPORT_VIEW_VENUE` (operate) · staff
- `listDevices` → `DEVICE_VIEW` (read) · staff
- `listPrincipals` → `USER_MANAGE` (configure) · staff, partner
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 13.3.14 | APIs shall expose operational, financial, attendance, membership and sales reporting data. | Developer & API Management | CONTRACTED | `runReport` |
| 2.1.18 | POS and kiosk devices shall be linked to the Device Management module so administrators can monitor device status, location, software version, connectivity, errors, paper levels, and assigned … | Ticketing Sales | CONTRACTED | `listDevices` |
| 2.1.26 | System shall provide centralized monitoring of kiosk health including online status, stock levels, payment devices, printers, connectivity, and alerts. | Ticketing Sales | CONTRACTED | `listDevices` |
| 8.9.6 | System shall monitor scanners, POS devices, kiosks, handhelds, printers, gates, network connectivity, and infrastructure health. | Unified Operations Dashboard | CONTRACTED | `listDevices` |
| 16.2.7 | Device Inventory Management - System shall maintain device inventories. | Device Management | CONTRACTED | `listDevices` |
| 16.2.8 | Device Classification - System shall support device categorization. | Device Management | CONTRACTED | `listDevices` |
| 16.2.12 | Device Asset Tracking - System shall maintain device asset records. | Device Management | CONTRACTED | `listDevices` |
| 16.9.55 | Device APIs - System shall expose device management APIs. | Device Management | CONTRACTED | `listDevices` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Operations board: access-control metrics - total entries, attendance, exits, per-turnstile breakdowns, and park capacity utilisation. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-717)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-003` · status **notStarted** · provenance generated · **Drawn as POS-6B, POS-6C, POS-6D in the client POS pack.** The pack's frame is the specification — it carries operations, states, entry params and exits, and it is better specified than anything …
- Derived from `wireframes/POS Board 6.dc.html#pos-6b`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `FnB Board 4.dc.html#fnb-4k`, `FnB Board 6.dc.html#fnb-6c`, `FnB Board 6.dc.html#fnb-6g`, `POS Board 6.dc.html#pos-6b`, `POS Board 6.dc.html#pos-6c`, `POS Board 6.dc.html#pos-6d`
- ADR-0067 *One device register; Access keeps only where a device is placed* (`docs/adr/0067-one-device-register.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (27 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-003?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run report.
- [ ] Every transition is wired: `ANL-001`.
- [ ] Every gated control is gated: `DEVICE_VIEW`, `REPORT_VIEW_VENUE`, `USER_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-004` Product Performance

**Product Performance — across F&B, retail, ticketing and frontline, filtered by domain.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-004 |
| Who uses it | venue staff holding `PRODUCT_VIEW`, `REPORT_VIEW_VENUE` (1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listProducts` reads the population and `getDashboard` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `domain` (session), `dashboardId` (deepLink), `reportId` (deepLink) · cold entry: **A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries … |
| Route | `/analytics/product-performance` |

**What the spec says about it.** **Built 20 August. Answers 2 board screens**: Product Performance & Menu Engineering; Product, SKU & Merchandise Performance. **Menu engineering and SKU performance are one analysis.** Both rank products by margin against volume; only the vocabulary differs. **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6c` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Combo, matrix, waterfall, treemap and scatter now bind** (CHG-FIN-007, 2 October 2026) through the report column encodings; the correction that they could not is closed. **Measure names, not "Revenue"** (decided 2 October 2026, Chinmay; CHG-FIN-002; BOARDREQ MOM-2758..2761). Takings (money taken less money paid back, a cash-control figure), Gross sales (before discounts, excluding VAT), Net revenue (gross sales less discounts and refunds), Recognised revenue and Deferred revenue are different numbers and never share a label; a tile takes its label from the seeded KPI it is bound to (`ReportingSystemKpi`).

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Product performance for a commercial, F&B or retail manager: which products, price points and promotions earn the revenue and the margin, and which sell in volume but earn little (menu engineering / SKU performance). It implements the client's Product & Pricing board. The one thing to get right: performance measures per product (net revenue, units, margin) — not the catalogue's own fields.

**Known correction pending (do not draw the wrong version)**

- **The collection is listProducts with raw filters "Venue id", "Kind", "Is sellable" and 12 catalogue columns.** Why: A catalogue read has no sales, units or margin; the ranking must come from a report or KPI read. "Venue id" is a spec leak. *(source: screens/P16-venue-analytics.yaml#ANL-004 / contracts/spine/catalogue.yaml#listProducts; Finance, Ledger & Tax · Reporting & Analytics)*
- **Menu-engineering classification is not declared.** Why: It is produced by ai.requestSuggestion kind menuEngineering (popularity against margin over 90 days); the screen must declare it to draw the quadrant. *(source: MATRIX 4.1.16 / contracts/satellite/ai.yaml#requestSuggestion; Finance, Ledger & Tax · Reporting & Analytics)*
- **The Product & Pricing board is specified with treemap, scatter and waterfall.** Why: None can bind until ReportColumn carries an encoding role; use bar and table meanwhile. *(source: MATRIX 8.7.4 / contracts/satellite/reporting.yaml#/components/schemas/DashboardTile; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What is margin for admission tickets (no cost of sale) — excluded, or a contribution after commission?** → Drawn default accepted: Margin shown only where a cost exists. *(decided by Chinmay, 2026-10-02; DEC-314 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listProducts`. | `listProducts` ?venueId |
| Kind | select | optional | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | — | Sends `?kind=` to `listProducts`. | `listProducts` ?kind |
| Is sellable | toggle | optional | — | — | — | Sends `?isSellable=` to `listProducts`. | `listProducts` ?isSellable |
| Domain | multi select | — | — | — | — | **The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Refresh | toggle | off | — | `getDashboard` ?refresh |
| Category | picker: choose a category | — | — | `listProducts` ?categoryId |
| Segment tag | text field | — | max length 120 | `listProducts` ?segmentTag |
| Guided answers | multi-picker: choose guided answers | — | at most 10 | `listProducts` ?guidedAnswerIds |

**Form: Run report** (modal, opened by *Run report*; *Run report* calls `runReport`, *Cancel* sends nothing)

**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Parameters `parameters` | key and value settings | optional | — | — | — | Open on purpose; its shape is the report's. Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. | `runReport` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | `runReport` body |
| Date from `dateFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158). | `runReport` body |
| Date to `dateTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (audit R158). | `runReport` body |
| Force async `forceAsync` | toggle | optional | off | — | — | Queue regardless of size, for a result to be collected later. | `runReport` body |

Errors to draw in the form: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **breakdown**: By product (default), by price point, by promotion — three tabs over the same measures. *(source: MATRIX 8.7.4 / MATRIX 8.5.18)*
- **period**: Defaults to Last 30 days; menu engineering classification uses its own fixed 90-day window, stated on the panel. *(source: MATRIX 4.1.16)*

#### Outputs: what the screen shows and produces

**Shown**

**Every product** (data table, from `listProducts`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |

**Chart** (chart): **Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.

**The selected product** (detail panel, from `listProducts`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Kind | chip: Admission, Timed admission, Dated admission, Open dated, Seated, Membership… | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no … |
| On sale from | 1 Oct 2026, 14:30 | 1.4.8. A seasonal product should not need somebody awake at midnight. |
| On sale to | 1 Oct 2026, 14:30 | Retires the product automatically. Retirement is not deletion — the product stops selling and every order that referenced it still resolves. |
| Lifecycle state | chip: Draft, In review, Approved, Live, Withdrawn, Archived | — |
| Is sellable | yes / no (icon or chip) | True only when live and carried by a published bundle. Approval and publication are different acts. |

**The dashboard data** (detail panel, from `getDashboard`)

| Shows | Format | Notes |
|---|---|---|
| Tile data | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run report (primary button) | `runReport` POST `/reports/{reportId}/run` | RunReportRequest | ReportResult | 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **product ranking**: Bar of Net revenue by product (top 15, zero baseline), units and margin % beside it; Net revenue is after line discounts and excludes VAT. *(source: MATRIX 8.7.4)*
- **popularity vs margin (menu engineering)**: The client asks for a scatter; scatter cannot bind yet, so draw a table with a quadrant label per item (high/low popularity × high/low margin) from the menu-engineering suggestion, with "Based on the last 90 days" and the maturity badge. *(source: MATRIX 8.7.4 / MATRIX 4.1.16 / contracts/satellite/reporting.yaml#/components/schemas/DashboardTile / contracts/satellite/ai.yaml#/components/schemas/AiMaturity)*
- **revenue by promotion**: Net revenue and discount cost per promotion; discount cost shown in brackets as a negative. *(source: MATRIX 8.7.4)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **open a product**: Drill product → price point → performance/date → orders, filters carried. *(source: MATRIX 8.7.28 / MATRIX 8.9.10 / DI-709)*
- **go to Inventory & Waste for this product**: Opens ANL-006 with the product and period carried. *(source: F82 step 3 / F82 step 4)*

**Data it reads**: `getDashboard` (onLoad, Read a dashboard with tile data); `listProducts` (onLoad, List products); `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Executive Command Center*; carries `dashboardId`, `reportId`
- → `ANL-006` Inventory & Waste Intelligence: *Inventory & Waste Intelligence*; carries `dashboardId`, `reportId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Tiles render in place; **each resolves on its own** so one slow source does not hold the page. |
| Error (`?state=error`) | Could not load. **Trading is unaffected** — this reads and writes nothing. |
| Empty, first run (`?state=emptyFirstRun`) | **A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period. |
| Permission denied (`?state=emptyNoAccess`) | You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158) |

#### Edge cases to draw

- **A ticket product with no cost of sale**: Margin shows "—" with "No cost recorded", never 100%. *(source: designer default)*
- **The same product sold at three dynamic prices in one day**: The price-point tab shows three rows with their own units and revenue. *(source: MATRIX 8.7.4 / MATRIX 8.5.18)*

#### Consistency with other screens

- Match `ANL-005`: ANL-004 ranks products; ANL-005 owns the margin bridge and cost. Margin % per product must equal ANL-005's for the same item and period.
- Match `ANL-002`: Same Net revenue per product; ANL-002 adds the channel split.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Aquaventure Waterpark — F&B (AED)
period: Last 30 days
products:
- Classic Burger Meal · 6,420 sold · Net revenue AED 288,900.00 · margin 64.0% · Popular, high margin
- Shawarma Wrap · 5,105 sold · AED 137,835.00 · margin 71.5% · Popular, high margin
- Mango Smoothie · 1,240 sold · AED 29,760.00 · margin 58.2% · Less popular, lower margin
promotion: Family Combo −15% · Net revenue AED 92,400.00 · discount cost (AED 16,305.88)
```

#### Permissions

- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 13.3.14 | APIs shall expose operational, financial, attendance, membership and sales reporting data. | Developer & API Management | CONTRACTED | `runReport` |
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |
| 8.8.1 | A price for a PLU is changing depending on the date of visit. I can sell today a product to be used after a price change at the new price defined in the sales calendar. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.2 | System shall support future-dated pricing schedules. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.3 | System shall support pricing by visit date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| 8.8.4 | System shall support pricing by booking date. | Unified Operations Dashboard | CONTRACTED | data `Product` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-004` · status **notStarted** · provenance generated · **Drawn as RET-6C in the client Retail pack.**
- Derived from `wireframes/Retail Board 6.dc.html#ret-6c`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `FnB Board 6.dc.html#fnb-6d`, `Retail Board 6.dc.html#ret-6c`
- Flow F82 *A month is analysed from incrementality to a scheduled report*, step 3: Product Performance. → **Drawn by the client as RET-6C.** 3 operations on this step.
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-004?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run report.
- [ ] Every transition is wired: `ANL-001`, `ANL-006`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-005` Cost, Margin & Profitability

**Cost, Margin & Profitability — across F&B, retail, ticketing and frontline, filtered by domain.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-005 |
| Who uses it | venue staff holding `LEDGER_VIEW`, `REPORT_VIEW_VENUE` (1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (compact density): `getDashboard` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `venueId` (session), `domain` (session), `dashboardId` (deepLink), `reportId` (deepLink) · cold entry: **A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries … |
| Route | `/analytics/cost-margin-profitability` |

**What the spec says about it.** **Built 20 August. Answers 2 board screens**: Food Cost, Margin & Profitability Intelligence; Promotion, Pricing & Margin Intelligence. Cost against price against what actually sold. **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6f` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Combo, matrix, waterfall, treemap and scatter now bind** (CHG-FIN-007, 2 October 2026) through the report column encodings; the correction that they could not is closed. **Measure names, not "Revenue"** (decided 2 October 2026, Chinmay; CHG-FIN-002; BOARDREQ MOM-2758..2761). Takings (money taken less money paid back, a cash-control figure), Gross sales (before discounts, excluding VAT), Net revenue (gross sales less discounts and refunds), Recognised revenue and Deferred revenue are different numbers and never share a label; a tile takes its label from the seeded KPI it is bound to (`ReportingSystemKpi`).

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Cost, margin and profitability for F&B and retail managers: food cost %, gross margin %, and a bridge from gross sales to contribution margin, plus promotion and pricing margin erosion. It answers the packs' "Food Cost, Margin & Profitability" and "Promotion, Pricing & Margin" frames. The one thing to get right: every stage of the bridge is a named, ordered measure in base currency, excluding VAT, reconcilable to the P&L.

**Known correction pending (do not draw the wrong version)**

- **The only cost read declared is getStockValuation.** Why: Stock value is a balance at a date; margin needs cost of sales for the period (recipe cost × units sold) and waste, which come from the finance P&L or a report, not from stock valuation. *(source: contracts/satellite/inventory.yaml#getStockValuation / contracts/spine/finance.yaml#getFinancialReport / DI-276; Finance, Ledger & Tax · Reporting & Analytics)*
- **The margin bridge's stages are not a defined measure set and waterfall cannot bind.** Why: A bridge that cannot be totalled cannot be reconciled to the P&L. *(source: MATRIX 4.1.16 / MATRIX 8.7.28 / contracts/satellite/reporting.yaml#/components/schemas/DashboardTile; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the margin bridge fixed platform-wide or tenant-configurable (e.g. a venue without a food-cost stage)?** → Drawn default accepted: Fixed order, stage omitted when it has no value. *(decided by Chinmay, 2026-10-02; DEC-315 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Domain | multi select | — | — | — | — | **The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Refresh | toggle | off | — | `getDashboard` ?refresh |
| As at | date picker | — | — | `getStockValuation` ?asAt |
| Location | picker: choose a location | — | — | `getStockValuation` ?locationId |

**Form: Run report** (modal, opened by *Run report*; *Run report* calls `runReport`, *Cancel* sends nothing)

**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Parameters `parameters` | key and value settings | optional | — | — | — | Open on purpose; its shape is the report's. Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. | `runReport` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | `runReport` body |
| Date from `dateFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158). | `runReport` body |
| Date to `dateTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (audit R158). | `runReport` body |
| Force async `forceAsync` | toggle | optional | off | — | — | Queue regardless of size, for a result to be collected later. | `runReport` body |

Errors to draw in the form: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**The dashboard data** (detail panel, from `getDashboard`)

| Shows | Format | Notes |
|---|---|---|
| Tile data | list or chips (count when long) | — |

**The stock valuation** (detail panel, from `getStockValuation`)

| Shows | Format | Notes |
|---|---|---|
| As at | 1 Oct 2026 | — |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| By location | list or chips (count when long) | — |
| By category | list or chips (count when long) | — |

**Chart** (chart): **Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run report (primary button) | `runReport` POST `/reports/{reportId}/run` | RunReportRequest | ReportResult | 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **margin bridge**: Ordered stages: Gross sales → Discounts → Refunds → Net revenue → Food cost → Waste → Contribution margin, with the margin % at the end. The client draws it as a waterfall; until waterfall binds, draw a bar with signed values in that fixed order and the running total labelled. *(source: MATRIX 4.1.16 / MATRIX 8.7.28 / MATRIX 6.1.47 / MATRIX 6.1.67 / MATRIX 8.7.25 / contracts/satellite/reporting.yaml#/components/schemas/DashboardTile)*
- **KPI cards**: Food cost % and Gross margin % against forecast in percentage points (pp), not percent change. *(source: MATRIX 4.6.36 / MATRIX 8.7.1 / MATRIX 4.1.16)*
- **stock valuation**: Stock value by location and category at the period end, labelled "Stock on hand (value)" — a balance, not a cost of the period. *(source: contracts/satellite/inventory.yaml#getStockValuation)*
- **promotion margin**: Per promotion, net revenue, discount cost and margin % before/after; erosion shown in pp. *(source: screens/P16-venue-analytics.yaml#ANL-005)*

**Data it reads**: `getDashboard` (onLoad, Read a dashboard with tile data); `getStockValuation` (onLoad, Stock value by location and category); `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Executive Command Center*; carries `dashboardId`, `reportId`
- → `ANL-007` Guest & Conversion Intelligence: *Guest & Conversion Intelligence*; carries `dashboardId`, `reportId`; calls `getStockValuation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Tiles render in place; **each resolves on its own** so one slow source does not hold the page. |
| Error (`?state=error`) | Could not load. **Trading is unaffected** — this reads and writes nothing. |
| Empty, first run (`?state=emptyFirstRun`) | **A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period. |
| Permission denied (`?state=emptyNoAccess`) | You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158) |

#### Edge cases to draw

- **An Egypt venue where VAT is levied on the pre-discount price**: The bridge uses the tax actually charged (EGP 100 ticket, 20% off, paid EGP 80, VAT on EGP 100), so net revenue excl. VAT is lower than the discounted price suggests; the screen never recomputes VAT from the shown price. *(source: DI-598 / contracts/spine/catalogue.yaml#/components/schemas/TaxProfile)*
- **A Bahrain venue**: All bridge values to 3 decimals (BHD 1,204.375); the third decimal is never rounded away in totals. *(source: DI-306 / DI-598)*
- **Waste recorded after the period closed**: The figure lands in the open period by reversal/adjustment (a closed period is locked), and the bridge notes "Includes a prior-period adjustment"; nothing is silently edited. *(source: DI-263 / contracts/spine/finance.yaml#getFinancialReport)*

#### Consistency with other screens

- Match `ANL-004`: Same margin % per item.
- Match `BO-1081`: Net revenue and cost of sales must reconcile to the finance P&L (revenue per category less cost of sales).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Aquaventure Waterpark — F&B (AED)
period: Today, as of 15:10
bridge:
- Gross sales AED 48,620.00
- Discounts (AED 3,410.00)
- Refunds (AED 260.00)
- Net revenue AED 44,950.00
- Food cost (AED 13,935.00)
- Waste (AED 1,124.00)
- Contribution margin AED 29,891.00 · 66.5%
cards: Food cost 31.0% (+1.2 pp vs forecast) · Gross margin 69.0% (−1.2 pp)
```

#### Permissions

- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `getStockValuation` → `LEDGER_VIEW` (read) · staff
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 13.3.14 | APIs shall expose operational, financial, attendance, membership and sales reporting data. | Developer & API Management | CONTRACTED | `runReport` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Financial reports generated automatically: P&L (revenue per category less cost of sales), balance sheet, trial balance and ledger view, cash flow, revenue and deferred-revenue analytics, site-wise revenue; plus daily/weekly/monthly finance summaries. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-276)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-005` · status **notStarted** · provenance generated · **Drawn as RET-6F in the client Retail pack.**
- Derived from `wireframes/Retail Board 6.dc.html#ret-6f`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `FnB Board 6.dc.html#fnb-6e`, `Retail Board 6.dc.html#ret-6f`
- Flow F82 *A month is analysed from incrementality to a scheduled report*, step 1: Cost, Margin & Profitability. → **Drawn by the client as RET-6F.** 1 operations on this step.
- Flow F82 branch at step 1 (medium): when A step in the chain is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` on each screen decides — a tenant without the retail licence does not see the retail half, and the journey is shorter rather than broken.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-005?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run report.
- [ ] Every transition is wired: `ANL-001`, `ANL-007`.
- [ ] Every gated control is gated: `LEDGER_VIEW`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-006` Inventory & Waste Intelligence

**Inventory & Waste Intelligence — across F&B, retail, ticketing and frontline, filtered by domain.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-006 |
| Who uses it | venue staff holding `AI_USE`, `PRODUCT_VIEW`, `REPORT_VIEW_VENUE` (2 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listExpiringBatches` reads the population and `getDashboard` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `domain` (session), `countId` (deepLink), `dashboardId` (deepLink), `reportId` (deepLink) · cold entry: **A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries … |
| Route | `/analytics/inventory-waste-intelligence` |

**What the spec says about it.** **Built 20 August. Answers 2 board screens**: Inventory, Waste & Production Intelligence; Inventory, Sell-Through & Stock Intelligence. **Theoretical against actual is the whole analysis** — a recipe says 400 portions, the run says 380, and the gap is waste, theft or a wrong recipe. **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6d` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer. **Drawn 31 August** — `Retail Board 6.dc.html` frame `ret-6d`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Inventory &amp; Stock Intelligence* matched at 0.89. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Inventory and waste intelligence for F&B and retail managers: theoretical against actual usage, waste %, expiring batches, count variances and waste-risk suggestions. The one thing to get right: the gap between theoretical and actual is the analysis (a recipe says 400 portions, the run says 380), and an AI waste-risk suggestion is advice a person applies in the F&B or inventory module, never an action taken here.

**Known correction pending (do not draw the wrong version)**

- **The states say "this reads and writes nothing" but the screen offers a waste-risk suggestion request.** Why: The request writes an ai.suggestion row; the state text should say trading is unaffected, not that nothing is written. *(source: screens/P16-venue-analytics.yaml#ANL-006 / contracts/satellite/ai.yaml#requestSuggestion; Finance, Ledger & Tax · Reporting & Analytics)*
- **Theoretical vs actual usage has no declared read.** Why: The notes call it "the whole analysis" but only expiring batches and count variance are bound; consumption against recipe needs a report over stock movements and production. *(source: screens/P16-venue-analytics.yaml#ANL-006; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Within days | number field (days) | optional | 7 | — | — | Sends `?withinDays=` to `listExpiringBatches`. | `listExpiringBatches` ?withinDays |
| Domain | multi select | — | — | — | — | **The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Refresh | toggle | off | — | `getDashboard` ?refresh |

**Form: Run report** (modal, opened by *Run report*; *Run report* calls `runReport`, *Cancel* sends nothing)

**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Parameters `parameters` | key and value settings | optional | — | — | — | Open on purpose; its shape is the report's. Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. | `runReport` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | `runReport` body |
| Date from `dateFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158). | `runReport` body |
| Date to `dateTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (audit R158). | `runReport` body |
| Force async `forceAsync` | toggle | optional | off | — | — | Queue regardless of size, for a result to be collected later. | `runReport` body |

Errors to draw in the form: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **withinDays**: Label "Expiring within" with chips 3 / 7 / 14 days; default 7 (the contract default). *(source: contracts/satellite/inventory.yaml#listExpiringBatches)*
- **count**: The count-variance panel opens from a selected stock count; with none selected it shows "Choose a count to compare". *(source: contracts/satellite/inventory.yaml#getCountVariance / screens/P16-venue-analytics.yaml#ANL-006)*

#### Outputs: what the screen shows and produces

**Shown**

**Every stock batch** (data table, from `listExpiringBatches`)

| Shows | Format | Notes |
|---|---|---|
| Batch code | text | — |
| Lot number | text | The supplier's own reference. A recall names a lot number, and an inventory that cannot resolve one has to discard everything. |
| Quantity | 1,234.5 | — |
| Received at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026 | — |
| Status | chip: Available, Quarantined, Expired, Recalled, Consumed, Written off | — |

**Chart** (chart): **Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.

**The selected stock batch** (detail panel, from `listExpiringBatches`)

| Shows | Format | Notes |
|---|---|---|
| Batch code | text | — |
| Lot number | text | The supplier's own reference. A recall names a lot number, and an inventory that cannot resolve one has to discard everything. |
| Quantity | 1,234.5 | — |
| Received at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026 | — |
| Status | chip: Available, Quarantined, Expired, Recalled, Consumed, Written off | — |

**The count variance** (detail panel, from `getCountVariance`)

| Shows | Format | Notes |
|---|---|---|
| Count | the name it points at, never the id | — |
| Total variance value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Exception count | 1,234 | Lines beyond `VenueSettings.inventory.countVarianceTolerancePercent` (proposed default 2 per cent, audit R094), requiring review before … |
| Lines | list or chips (count when long) | — |

**The dashboard data** (detail panel, from `getDashboard`)

| Shows | Format | Notes |
|---|---|---|
| Tile data | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run report (primary button) | `runReport` POST `/reports/{reportId}/run` | RunReportRequest | ReportResult | 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **KPI cards**: Waste % (vs yesterday), Stock on hand (value, AED), Items below par, Batches expiring in 7 days. *(source: MATRIX 6.1.38 / MATRIX 8.7.1 / contracts/satellite/inventory.yaml#getStockValuation / MATRIX 4.4.17 / MATRIX 8.9.4)*
- **expiring batches**: Sorted by expiry date ascending, then by value at risk descending; expiry shown in the venue's time zone with "in 2 days". *(source: contracts/satellite/inventory.yaml#listExpiringBatches)*
- **count variance**: Counted vs expected per item with variance in units and value; variance before posting is the discrepancy report and is labelled "Not yet posted". *(source: MATRIX 6.1.21 / contracts/satellite/inventory.yaml#getCountVariance)*
- **waste-risk suggestions**: Items at risk with quantity and a recommended action (reduce prep, promote, transfer, use in a recipe), with the "Based on" line and maturity badge; buttons open the owning module, never apply. *(source: MATRIX 4.1.19 / MATRIX 4.8.15 / contracts/satellite/ai.yaml#/components/schemas/AiMaturity)*

**Data it reads**: `getDashboard` (onLoad, Read a dashboard with tile data); `getCountVariance` (onLoad, Variance between counted and expected); `listExpiringBatches` (onLoad, What is about to go out of date); `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Executive Command Center*; carries `dashboardId`, `reportId`
- → `BO-058` Reporting Home: *Reporting Home*; carries `reportId`; calls `listExpiringBatches`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Tiles render in place; **each resolves on its own** so one slow source does not hold the page. |
| Error (`?state=error`) | Could not load. **Trading is unaffected** — this reads and writes nothing. |
| Empty, first run (`?state=emptyFirstRun`) | **A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period. |
| Permission denied (`?state=emptyNoAccess`) | You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 409 Count is still open.; 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem) |

#### Edge cases to draw

- **A venue in its first weeks**: Waste-risk shows the "Starting" badge and "Limited historical data", not an empty panel and not a confident figure. *(source: contracts/satellite/ai.yaml#/components/schemas/AiMaturity / DI-280)*
- **A batch already expired but still on hand**: Shown at the top in Critical style with "Expired 1 day ago". *(source: designer default)*

#### Consistency with other screens

- Match `ANL-004`: Reached from Product Performance with the product carried (F82 step 3→4).
- Match `BO-058`: Continues to Reporting Home to schedule the report (F82 step 4→5).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Aquaventure Waterpark — Central Kitchen (AED)
cards: Waste 3.8% (+0.6 pp vs yesterday) · Stock on hand AED 412,580.00 · 14 items below par · 9 batches expiring
  in 7 days
batches:
- Chicken breast, batch CK-2209 · 42 kg · expires Thu 01 Oct · AED 1,134.00 at risk
- Brioche buns, batch BK-0930 · 600 units · expires Fri 02 Oct · AED 720.00 at risk
suggestion: 'Reduce burger prep by 120 portions on Thu (forecast 410, stock 530) · Based on: venue profile, UAE
  calendar, weather, 23 days of your sales'
```

#### Permissions

- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `getCountVariance` → `PRODUCT_VIEW` (read) · staff
- `listExpiringBatches` → `PRODUCT_VIEW` (read) · staff
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff
- `requestSuggestion` → `AI_USE` (operate) · staff, guest

**A refused user sees:** You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out.

#### Requirements it meets

23 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 13.3.14 | APIs shall expose operational, financial, attendance, membership and sales reporting data. | Developer & API Management | CONTRACTED | `runReport` |
| 6.1.21 | The system should be able to generate discrepancy report generated prior to making an inventory adjustment. | Retail POS | CONTRACTED | `getCountVariance` |
| 2.1.28 | Kiosks shall provide an AI assistant to guide guests through ticket selection, promotions, FAQs, recommendations, and checkout. | Ticketing Sales | CONTRACTED | `requestSuggestion` |
| 4.1.16 | Analyze menu performance and profitability. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.19 | Recommend actions to reduce waste and spoilage. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.20 | Recommend pricing and promotion strategies. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.8.15 | AI predicts potential food waste and recommends actions. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 5.4.24 | Segment customers automatically. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| … 11 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Retail intelligence shows sales and outlet performance, top-performing stores, demand forecasting (from retail sales history and online ticket booking trends) and target-vs-actual per outlet (e.g. monthly target vs. achieved, with variance). *(client request · MoM 19 Aug 2026, 4.9 Retail Intelligence & Reporting · DI-368)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-006` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 6.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/Retail Board 6.dc.html#ret-6d`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `FnB Board 6.dc.html#fnb-6f`, `Retail Board 6.dc.html#ret-6d`
- Flow F82 *A month is analysed from incrementality to a scheduled report*, step 4: Inventory & Waste Intelligence. → **Drawn by the client as RET-6D.** 1 operations on this step.
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-006?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run report.
- [ ] Every transition is wired: `ANL-001`, `BO-058`.
- [ ] Every gated control is gated: `AI_USE`, `PRODUCT_VIEW`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-007` Guest & Conversion Intelligence

**Guest & Conversion Intelligence — across F&B, retail, ticketing and frontline, filtered by domain.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-007 |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW`, `REPORT_VIEW_VENUE` (1 configure, 1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSegments` reads the population and `getDashboard` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `domain` (session), `dashboardId` (deepLink), `reportId` (deepLink), `segmentId` (deepLink) · cold entry: **A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries … |
| Route | `/analytics/guest-conversion-intelligence` |

**What the spec says about it.** **Built 20 August. Answers 2 board screens**: Guest, Conversion & Basket Intelligence; Kitchen, Service & Fulfilment Performance. Who bought, what else they nearly bought, and how long they waited. **Retail board operations wired 24 August.** **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6e` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Guest and conversion intelligence for a commercial or CRM manager: how visits convert to purchases, where carts are abandoned, basket size, and which guest segments buy what. The one thing to get right: there are two conversion measures — web visit-to-purchase (from web analytics) and checkout conversion (paid orders over checkout sessions) — and they must never share one label.

**Known correction pending (do not draw the wrong version)**

- **The notes say the screen answers "Kitchen, Service & Fulfilment Performance".** Why: No kitchen, service-time or fulfilment operation is declared; that board belongs with kitchen performance, not guest conversion. *(source: screens/P16-venue-analytics.yaml#ANL-007; Finance, Ledger & Tax · Reporting & Analytics)*
- **The states say "this reads and writes nothing" while the screen offers Create segment.** Why: createSegment writes a CRM record; the state text is wrong and the action needs the CRM permission check. *(source: screens/P16-venue-analytics.yaml#ANL-007 / contracts/satellite/marketing-crm.yaml#createSegment; Finance, Ledger & Tax · Reporting & Analytics)*
- **No conversion or basket read is declared — only segment operations.** Why: The tiles need getKpiValues (conversion is a MetricSource) or a report; listSegments alone draws none of them. *(source: contracts/satellite/reporting.yaml#getKpiValues; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which stages count in the funnel, and is "visits" sourced from web analytics?** → Drawn default accepted: Five stages as drawn, visits labelled "from web analytics". *(decided by Chinmay, 2026-10-02; DEC-316 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search | text field | optional | — | max length 200 | — | Sends `?search=` to `listSegments`. | `listSegments` ?search |
| Domain | multi select | — | — | — | — | **The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Refresh | toggle | off | — | `getDashboard` ?refresh |

**Form: Run report** (modal, opened by *Run report*; *Run report* calls `runReport`, *Cancel* sends nothing)

**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Parameters `parameters` | key and value settings | optional | — | — | — | Open on purpose; its shape is the report's. Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. | `runReport` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | `runReport` body |
| Date from `dateFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158). | `runReport` body |
| Date to `dateTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (audit R158). | `runReport` body |
| Force async `forceAsync` | toggle | optional | off | — | — | Queue regardless of size, for a result to be collected later. | `runReport` body |

Errors to draw in the form: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope

**Form: Create segment** (modal, opened by *Create segment*; *Create segment* calls `createSegment`, *Cancel* sends nothing)

**Collects what `createSegment` sends before it is called.** Required: `name`, `criteria`. Optional: `description`, `venueId`, `match`, `excludeSegmentIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createSegment` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `createSegment` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createSegment` body |
| Match `match` | segmented control | optional | All | All · Any | — | — | `createSegment` body |
| Criteria `criteria` | repeatable rows | required | — | at least 1 | — | — | `createSegment` body |
| Attribute `criteria[].attribute` | text field | required | — | — | — | Behavioural or profile attribute — visit count, last visit, lifetime value, product purchased, membership tier, venue visited, language. | `createSegment` body |
| Operator `criteria[].operator` | select | required | — | Equals · Not equals · Greater than · Less than · Between · In · Not in · Exists · Not exists · Within days | — | — | `createSegment` body |
| Value `criteria[].value` | field | optional | — | — | — | — | `createSegment` body |
| Values `criteria[].values` | list of values (chips) | optional | — | — | — | — | `createSegment` body |
| Exclude segments `excludeSegmentIds` | multi-picker: choose exclude segments | optional | — | — | — | — | `createSegment` body |
| Rule groups `ruleGroups` | repeatable rows | optional | — | — | — | Nested AND / OR / NOT groups (contract gap CHG-WIR-007, BO-755; CHG-CSA-045). Where present, the segment matches `criteria` (combined by `match`) AND every group here. | `createSegment` body |
| Operator `ruleGroups[].operator` | segmented control | optional | — | And · Or · Not | — | — | `createSegment` body |
| Criteria `ruleGroups[].criteria` | repeatable rows | optional | — | — | — | Each entry has the shape of `SegmentCriterion` (`attribute`, `operator`, `value`). | `createSegment` body |
| Groups `ruleGroups[].groups` | repeatable rows | optional | — | — | — | — | `createSegment` body |
| Operator `ruleGroups[].groups[].operator` | segmented control | optional | — | And · Or · Not | — | — | `createSegment` body |
| Criteria `ruleGroups[].groups[].criteria` | repeatable rows | optional | — | — | — | Each entry has the shape of `SegmentCriterion` (`attribute`, `operator`, `value`). | `createSegment` body |
| Groups `ruleGroups[].groups[].groups` | repeatable rows | optional | — | — | — | — | `createSegment` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | The segment is evaluated for sends only from this time. | `createSegment` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createSegment` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | Who answers for the segment; defaults to its creator. | `createSegment` body |
| Requires approval `requiresApproval` | toggle | optional | off | — | — | Where true, a campaign may use the segment only after an `approvals` request on it is approved. | `createSegment` body |

Errors to draw in the form: 400 Criteria are contradictory or reference unknown attributes

#### Outputs: what the screen shows and produces

**Shown**

**Every segment** (data table, from `listSegments`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Match | chip: All, Any | — |
| Last evaluated size | 1,234 | — |
| Last evaluated at | 1 Oct 2026, 14:30 | — |

**Chart** (chart): **Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.

**The selected segment** (detail panel, from `listSegments`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Venue | the name it points at, never the id | — |
| Match | chip: All, Any | — |
| Criteria | list or chips (count when long) | — |
| Exclude segments | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Last evaluated size | 1,234 | — |
| Last evaluated at | 1 Oct 2026, 14:30 | — |

**The dashboard data** (detail panel, from `getDashboard`)

| Shows | Format | Notes |
|---|---|---|
| Tile data | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run report (primary button) | `runReport` POST `/reports/{reportId}/run` | RunReportRequest | ReportResult | 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope | opens modal first |
| Create segment (secondary button) | `createSegment` POST `/segments` | CreateSegmentRequest | Segment | 400 Criteria are contradictory or reference unknown attributes | opens modal first |
| Preview segment (secondary button) | `previewSegment` POST `/segments/{segmentId}/preview` | — | SegmentPreview | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **conversion**: "Visit-to-purchase conversion" (site visits to completed purchase, from the web analytics integration) and "Checkout conversion" (completed paid orders over checkout sessions) as separate tiles, each stating its source; "Cart abandonment" beside them. *(source: DI-700 / MoM 2026-09-08 4.2 Command Center Overview (Board 1) / MATRIX 1.1.40 / MATRIX 6.1.66 / contracts/satellite/reporting.yaml#/components/schemas/MetricSource)*
- **funnel**: Visits → cart → checkout → payment → tickets issued; funnel cannot bind yet, so draw a horizontal bar of stage counts with the step conversion % between bars. *(source: MATRIX 1.1.40 / MATRIX 6.1.66 / MATRIX 8.7.1 / MATRIX 8.7.2 / contracts/satellite/reporting.yaml#/components/schemas/DashboardTile)*
- **segments**: Segment list shows size and reachable count only (aggregates); no guest names on this screen. *(source: contracts/satellite/marketing-crm.yaml#previewSegment / MATRIX 8.3.73)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Save as segment**: Saves the current filter as a dynamic segment (a definition, resolved at send time). Offered only to users holding the CRM segment permission; hidden otherwise. *(source: MATRIX 22.14.1 / MATRIX 5.4.24 / DI-387)*

**Data it reads**: `getDashboard` (onLoad, Read a dashboard with tile data); `listSegments` (onLoad, List segments); `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Executive Command Center*; carries `dashboardId`, `reportId`
- → `ANL-004` Product Performance: *Product Performance*; carries `dashboardId`, `reportId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Tiles render in place; **each resolves on its own** so one slow source does not hold the page. |
| Error (`?state=error`) | Could not load. **Trading is unaffected** — this reads and writes nothing. |
| Empty, first run (`?state=emptyFirstRun`) | **A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period. |
| Permission denied (`?state=emptyNoAccess`) | You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Criteria are contradictory or reference unknown attributes; 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158) |

#### Edge cases to draw

- **The web analytics integration is not connected**: Visit-to-purchase tiles show "Web analytics not connected" with a link for an admin; checkout conversion still shows. *(source: MoM 2026-09-08 4.2 Command Center Overview (Board 1))*

#### Consistency with other screens

- Match `ANL-017`: ANL-007 owns purchase behaviour (conversion, basket, segments' buying); ANL-017 owns membership, loyalty and retention. Same segment names on both.
- Match `ANL-016`: Conversion and basket size also appear on the Sales & Channel scorecard; same definitions and labels.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Aquaventure Waterpark — Web (AED)
period: Last 7 days
tiles: Visit-to-purchase 3.4% · Checkout conversion 61.2% · Cart abandonment 38.8% · Average basket AED 486.30
funnel: Visits 182,400 → Cart 21,950 → Checkout 10,140 → Paid 6,206 → Tickets issued 6,198
segment: Families with annual pass, Dubai · 4,812 guests · 4,120 reachable by email
```

#### Permissions

- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `listSegments` → `MARKETING_VIEW` (read) · staff
- `createSegment` → `MARKETING_MANAGE` (configure) · staff
- `previewSegment` → `MARKETING_VIEW` (read) · staff
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 13.3.14 | APIs shall expose operational, financial, attendance, membership and sales reporting data. | Developer & API Management | CONTRACTED | `runReport` |
| 22.14.25 | Segmentation & Attribution Audit Trail | Marketing & CRM | CONTRACTED | `listSegments` |
| 7.4.5 | The Customer categories or Segments can be described in segments with 3 possible levels such as BtoC / BtoB, Individual / Groups. | F&B POS | CONTRACTED | `createSegment` |
| 22.2.10 | Guest Segmentation Attributes | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.1 | Audience Segmentation Engine | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.2 | Dynamic Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.3 | Static Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.4 | Behavioral Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- CRM board: membership/loyalty visit history; retention/churn section flagging inactive customers (e.g. an annual pass holder with no visit last quarter flagged for follow-up); campaign performance and customer behaviour analytics. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-718)*
- Further command-centre sections: revenue by sales channel; capacity utilisation by attraction/inventory item; top products by channel; conversion rate (site visits to completed purchase, cart abandonment, via Google Analytics); customer, membership and loyalty information. *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-700)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-007` · status **notStarted** · provenance generated · **Drawn as RET-6E in the client Retail pack.**
- Derived from `wireframes/Retail Board 6.dc.html#ret-6e`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 6.dc.html#ret-6e`
- Flow F82 *A month is analysed from incrementality to a scheduled report*, step 2: Guest & Conversion Intelligence. → **Drawn by the client as RET-6E.** 3 operations on this step.

#### Acceptance for the design

- [ ] Every input above is drawn (28), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-007?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run report, Create segment, Preview segment.
- [ ] Every transition is wired: `ANL-001`, `ANL-004`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`, `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-008` Demand Forecasting

**Demand Forecasting — across F&B, retail, ticketing and frontline, filtered by domain.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-008 |
| Who uses it | venue staff holding `AI_USE`, `REPORT_VIEW_VENUE` (2 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (compact density): `getDashboard` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `venueId` (session), `domain` (session), `dashboardId` (deepLink) · cold entry: **A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries … |
| Route | `/analytics/demand-forecasting` |

**What the spec says about it.** **Built 20 August. Answers 2 board screens**: Demand Forecasting & Operational Planning; Demand Forecasting & Merchandise Planning. **A forecast is an input to a requisition, not a report.** Its value is that somebody orders differently because of it. **Board repointed 24 August.** This screen pointed at `wireframes/Retail Board 6.dc.html#ret-6g` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Demand forecasting for operations, F&B and retail planners: expected attendance, demand and revenue by day, hour, channel or product, as a range, so someone orders, staffs or prepares differently. The one thing to get right: every projected figure is labelled Forecast, shown as a range (p10–p90) with its basis and maturity, and an honest "limited history" state — the forecast is never presented as fact or as a bare percentage.

**Known correction pending (do not draw the wrong version)**

- **getForecast requires a definition key, but the screen has no selector or entry parameter for it.** Why: Without it the forecast cannot be read at all. *(source: contracts/satellite/ai.yaml#getForecast / screens/P16-venue-analytics.yaml#ANL-008; Finance, Ledger & Tax · Reporting & Analytics)*
- **The primary button is "Ask reporting question".** Why: The screen exists to read a forecast; asking is secondary, and the label is a spec phrase. Use "Ask a question" as a secondary action. *(source: screens/P16-venue-analytics.yaml#ANL-008; Finance, Ledger & Tax · Reporting & Analytics)*
- **Client frames ask for a "confidence percentage" on the demand forecast.** Why: The contract and design 5.6 forbid a bare percentage — a range and a maturity stage are shown instead; the client should be told. *(source: MATRIX 8.2.29 / MATRIX 8.2.33 / contracts/satellite/ai.yaml#/components/schemas/AiForecastPoint; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **DI-280 says data-dependent forecasting cannot be delivered in phase one; the 29 Sep design ships a baseline-first forecast with maturity stages. Which applies to this screen?** → Baseline-first forecast with maturity stages. *(decided by Chinmay, 2026-10-02; DEC-317 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Domain | multi select | — | — | — | — | **The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Refresh | toggle | off | — | `getDashboard` ?refresh |
| Definition key | text field | — | — | `getForecast` ?definitionKey |
| Version | picker: choose a version | — | — | `getForecast` ?versionId |
| From | date and time picker | — | — | `getForecast` ?from |
| To | date and time picker | — | — | `getForecast` ?to |
| Dimension key | text field | — | — | `getForecast` ?dimensionKey |
| Scenario | picker: choose a scenario | — | — | `getForecast` ?scenarioId |

**Form: Ask reporting question** (modal, opened by *Ask reporting question*; *Ask reporting question* calls `askReportingQuestion`, *Cancel* sends nothing)

**Collects what `askReportingQuestion` sends before it is called.** Required: `question`. Optional: `conversationId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Question `question` | text area | required | — | min length 3; max length 1000 | — | — | `askReportingQuestion` body |
| Conversation `conversationId` | text field | optional | — | — | — | Continue a prior exchange for follow-up questions. | `askReportingQuestion` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows the answer to one venue. Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | `askReportingQuestion` body |

Errors to draw in the form: 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **forecast for**: Selector of published forecast definitions in plain words (Attendance, Ticket demand by time slot, F&B demand, Retail demand, Revenue); with horizon (Next 7 days default) and grain (day / hour). *(source: contracts/satellite/ai.yaml#getForecast / MATRIX 8.2.1 / MATRIX 4.1.17 / MATRIX 8.2.29)*
- **breakdown**: Venue, attraction, channel, product or time slot, one at a time. *(source: MATRIX 8.2.2 / MATRIX 8.2.3 / MATRIX 8.2.5 / MATRIX 8.2.13)*

#### Outputs: what the screen shows and produces

**Shown**

**The dashboard data** (detail panel, from `getDashboard`)

| Shows | Format | Notes |
|---|---|---|
| Tile data | list or chips (count when long) | — |

**Chart** (chart): **Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Ask reporting question (primary button) | `askReportingQuestion` POST `/reports/ask` | inline | NaturalLanguageAnswer | 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **forecast chart**: Line of the median (p50) with a shaded p10–p90 band, actuals solid up to today and forecast dashed after; legend "Forecast (likely range)". No confidence percentage. *(source: MATRIX 8.2.17 / contracts/satellite/ai.yaml#/components/schemas/AiForecastPoint / DI-973 / MATRIX 8.2.29 / MATRIX 8.2.33)*
- **basis and maturity**: A stage badge (Starting / Learning / Established / Learned) and the "Based on" line on every forecast; "Limited historical data" while the starting pattern carries most of the weight. *(source: contracts/satellite/ai.yaml#/components/schemas/AiMaturity / contracts/satellite/ai.yaml#/components/schemas/SuggestionBasis)*
- **pace and remaining opportunity**: Per channel, sales to date (actual), forecast for the period and remaining opportunity (forecast minus actual), all labelled. *(source: DI-750)*
- **drivers**: The top drivers of the forecast in words (e.g. "UAE school holiday", "Weekend"), largest first. *(source: contracts/satellite/ai.yaml#/components/schemas/AiForecastPoint)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Plan from this forecast**: Opens the replenishment or staffing screen with the forecast carried; nothing is ordered or rostered from here. *(source: MATRIX 15.4.1 / MATRIX 15.4.2 / contracts/satellite/ai.yaml#/components/schemas/Suggestion)*
- **Ask a question**: Opens the assistant pre-scoped to this forecast; hidden until the assistant is enabled for the tenant. *(source: contracts/satellite/reporting.yaml#askReportingQuestion)*

**Data it reads**: `getDashboard` (onLoad, Read a dashboard with tile data); `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …); `getForecast` (onLoad, Forecast values)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Executive Command Center*; carries `dashboardId`, `reportId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Tiles render in place; **each resolves on its own** so one slow source does not hold the page. |
| Error (`?state=error`) | Could not load. **Trading is unaffected** — this reads and writes nothing. |
| Empty, first run (`?state=emptyFirstRun`) | **A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period. |
| Permission denied (`?state=emptyNoAccess`) | You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Question could not be interpreted. (ReportQuestionProblem) |

#### Edge cases to draw

- **No forecast version has been published for the definition**: "No forecast published yet" with what is needed (a definition and its first nightly run) — not a zero line. *(source: contracts/satellite/ai.yaml#getForecast / DI-280)*
- **The last publication is more than 36 hours old**: Stale banner "Forecast last published Mon 28 Sep 02:00 — may be out of date"; numbers stay visible. *(source: contracts/satellite/ai.yaml#getForecast)*
- **A user with report permission but without AI use**: The forecast area shows "Forecasts need AI access" rather than an empty chart. *(source: contracts/satellite/ai.yaml#getForecast)*

#### Consistency with other screens

- Match `ANL-057`: ANL-057 is the forecasting studio (definitions, scenarios, accuracy); ANL-008 is the read-only planner view. Same band style and labels.
- Match `ADM-505`: Revenue forecast figures must match the P09 revenue forecast for the same definition and version.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Aquaventure Waterpark (AED)
forecastFor: Attendance, next 7 days, by day
points:
- Thu 01 Oct · Forecast 8,900 (likely 8,100 – 9,650)
- 'Fri 02 Oct · Forecast 12,400 (likely 11,200 – 13,500) · driver: Weekend'
- Sat 03 Oct · Forecast 13,100 (likely 11,800 – 14,300)
maturity: 'Learning · Based on: your venue profile, UAE calendar, weather, 54 days of your sales'
pace: Web · sold 41,200 · forecast 58,000 · remaining opportunity 16,800
```

#### Permissions

- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff
- `getForecast` → `AI_USE` (operate) · staff

**A refused user sees:** You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out.

#### Requirements it meets

39 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.7.30 | System shall support natural language reporting. | Unified Operations Dashboard | CONTRACTED | `askReportingQuestion` |
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
| … 27 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Demand forecasts show current sales pace, forecast and remaining opportunity broken down by sales channel; revenue forecasts show drivers and confidence levels. A forecast simulator models a hypothetical change (e.g. a 10% price decrease, reduced operating hours, staffing changes) before it is made. *(client request · MoM 18 Sep 2026, 4.10 AI Forecasting — Attendance, Demand, Revenue & Capacity Forecasting · DI-943)*
- Retail intelligence shows sales and outlet performance, top-performing stores, demand forecasting (from retail sales history and online ticket booking trends) and target-vs-actual per outlet (e.g. monthly target vs. achieved, with variance). *(client request · MoM 19 Aug 2026, 4.9 Retail Intelligence & Reporting · DI-368)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-008` · status **notStarted** · provenance generated · **Drawn as RET-6G in the client Retail pack.**
- Derived from `wireframes/Retail Board 6.dc.html#ret-6g`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `FnB Board 6.dc.html#fnb-6h`, `Retail Board 6.dc.html#ret-6g`
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)
- ADR-0059 *AI phasing against the six-month plan* (`docs/adr/0059-ai-phasing-against-the-six-month-plan.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (1 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-008?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Ask reporting question.
- [ ] Every transition is wired: `ANL-001`.
- [ ] Every gated control is gated: `AI_USE`, `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-009` AI Assistant & Action Center

**AI Assistant & Action Center — across F&B, retail, ticketing and frontline, filtered by domain.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-009 |
| Who uses it | venue staff holding `AI_USE`, `ORDER_VIEW`, `REPORT_MANAGE`, `REPORT_VIEW_VENUE` (2 operate, 1 read, 1 configure); in the flows as marketer |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (compact density): `decideProposedAction` decides items that `listAlerts` queues — every row is waiting for a person, so the empty state is success |
| Offline | online only |
| Opens with | `venueId` (session), `domain` (session), `alertId` (deepLink), `reportId` (deepLink), `actionId` (deepLink), `planId` (navigation) · cold entry: **A bookmarked dashboard is the normal way in** — a manager opens the same view every Monday. The domain and the window come from the link where it carries … |
| Route | `/analytics/ai-assistant-action-center` |

**What the spec says about it.** **Built 20 August. Answers 5 board screens**: AI Recommendation, Simulation & Optimization Center; AI Assistant, Alerts & Management Action Center; Transaction & Exception Monitoring and 2 more. **Five board screens, and the collapse is the point.** Every domain drew an AI centre and an alert centre; **an alert nobody can act on from the screen showing it is a notification**, so recommendation and action are one place. **Owns POS board frame(s) POS-6E** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Retail board operations wired 24 August.** **Board repointed 24 August.** This screen pointed at `wireframes/POS Board 6.dc.html#pos-6e` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The assistant and action centre for managers: ask a business question in plain words, see what is raised, acknowledge alerts, and approve or reject what the assistant has proposed. It collapses five client board screens. The one thing to get right: answers stay inside the user's role and show how they were calculated, and nothing the assistant proposes happens until a person with the right authority approves it.

**Known correction pending (do not draw the wrong version)**

- **"Save alert rule" opens a form requiring id, scopePath, metric, comparator, isActive and more.** Why: An id and a scope path are spec leaks; alert-rule authoring belongs to the alert/KPI configuration screens, not the assistant. *(source: screens/P16-venue-analytics.yaml#ANL-009 / contracts/satellite/reporting.yaml#setAlertRule; Finance, Ledger & Tax · Reporting & Analytics)*
- **The screen lists every order (listOrders, 10 columns).** Why: A full order list has no role on an assistant screen and exposes guest data; orders are reached by drill-through from an answer. *(source: screens/P16-venue-analytics.yaml#ANL-009 / MATRIX 8.3.73; Finance, Ledger & Tax · Reporting & Analytics)*
- **Alert filters "Workstation id", "Shift id", "Item id" are free-text ids.** Why: Spec leak; use severity and status filters. *(source: screens/P16-venue-analytics.yaml#ANL-009; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **DI-278 makes AI-assisted finance reporting phase two. Should finance-ledger questions (deferred revenue, journals) be refused in phase one?** → Drawn default stands (answer: "From ADM-068: AI finance reporting in phase two; ledger questions answer 'not available yet'"): Answer sales and attendance questions; finance-ledger metrics answer "not available yet". *(decided by Chinmay, 2026-10-02; DEC-318 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | radio group | optional | — | Raised · Acknowledged · Resolved · Expired | — | Sends `?status=` to `listAlerts`. | `listAlerts` ?status |
| Severity | segmented control | optional | — | Info · Warning · Critical | — | Sends `?severity=` to `listAlerts`. | `listAlerts` ?severity |
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listAlerts`. | `listAlerts` ?workstationId |
| Shift id | picker: choose a shift (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?shiftId=` to `listAlerts`. | `listAlerts` ?shiftId |
| Item id | picker: choose an item (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?itemId=` to `listAlerts`. | `listAlerts` ?itemId |
| Domain | multi select | — | — | — | — | **The selector that collapses 26 board screens into nine.** A domain is a filter on an analytics screen, not a copy of it — building three sets means maintaining one screen three times and watching … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Principal | picker: choose a principal | — | — | `listOrders` ?principalId |
| Shift | picker: choose a shift | — | — | `listOrders` ?shiftId |
| Status | select | — | Pending · Held · Paid · Partially paid · Completed · Voided · Refunded · Partially refunded · Failed; It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed. | `listOrders` ?status |
| Created from | date and time picker | — | — | `listOrders` ?createdFrom |
| Created to | date and time picker | — | — | `listOrders` ?createdTo |
| Workstation | picker: choose a workstation | — | — | `listOrders` ?workstationId |
| Subject | picker: choose a subject | — | — | `listOrders` ?subjectId |
| Tender | select | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | `listOrders` ?tender |

**Form: Ask reporting question** (modal, opened by *Ask reporting question*; *Ask reporting question* calls `askReportingQuestion`, *Cancel* sends nothing)

**Collects what `askReportingQuestion` sends before it is called.** Required: `question`. Optional: `conversationId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Question `question` | text area | required | — | min length 3; max length 1000 | — | — | `askReportingQuestion` body |
| Conversation `conversationId` | text field | optional | — | — | — | Continue a prior exchange for follow-up questions. | `askReportingQuestion` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows the answer to one venue. Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | `askReportingQuestion` body |

Errors to draw in the form: 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope

**Form: Acknowledge alert** (modal, opened by *Acknowledge alert*; *Acknowledge alert* calls `acknowledgeAlert`, *Cancel* sends nothing)

**Collects what `acknowledgeAlert` sends before it is called.** Nothing in the body is required. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Note `note` | text area | optional | — | max length 300 | — | Stored as `Alert.acknowledgementNote`. | `acknowledgeAlert` body |

**Form: Run report** (modal, opened by *Run report*; *Run report* calls `runReport`, *Cancel* sends nothing)

**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Parameters `parameters` | key and value settings | optional | — | — | — | Open on purpose; its shape is the report's. Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. | `runReport` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | `runReport` body |
| Date from `dateFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158). | `runReport` body |
| Date to `dateTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (audit R158). | `runReport` body |
| Force async `forceAsync` | toggle | optional | off | — | — | Queue regardless of size, for a result to be collected later. | `runReport` body |

Errors to draw in the form: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope

**Form: Save alert rule** (modal, opened by *Save alert rule*; *Save alert rule* calls `setAlertRule`, *Cancel* sends nothing)

**Collects what `setAlertRule` sends before it is called.** Required: `id`, `name`, `metric`, `comparator`, `threshold`, `severity`, `isActive`, `scopePath`. Optional: `thresholdUpper`, `windowMinutes`, `deliverTo`, `recipientRoleIds`, `cooldownMinutes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setAlertRule` body |
| Name `name` | text field | required | — | — | — | — | `setAlertRule` body |
| Metric `metric` | select | required | — | Occupancy · Capacity utilisation · Admission rate · No show rate · Conversion · Sales by operator · Sales by workstation · Wait time · Throughput · Abandonment rate · Inventory valuation · Stock turnover … | — | From the closed set, so a rule cannot watch something nothing produces — the same discipline `MetricSource` exists for. | `setAlertRule` body |
| Comparator `comparator` | radio group | required | — | Above · Below · Outside range · Changes by · Equals | — | — | `setAlertRule` body |
| Threshold `threshold` | number field | required | — | — | — | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its … | `setAlertRule` body |
| Threshold upper `thresholdUpper` | number field | optional | — | Required when `comparator` is `outsideRange` (decided 28 September, audit R158): the range is `threshold` to `thresholdUpper`, and a rule missing either, or with the upper not above the lower, is … | — | Required when `comparator` is `outsideRange` (decided 28 September, audit R158): the range is `threshold` to `thresholdUpper`, and a rule missing either, or with the upper not … | `setAlertRule` body |
| Window minutes `windowMinutes` | number field (minutes) | optional | 15 | — | — | The window is what stops an alert firing on noise. A queue that spikes for ninety seconds is not a queue that needs a manager, and a rule with no window is a rule somebody mutes … | `setAlertRule` body |
| Severity `severity` | segmented control | required | — | Info · Warning · Critical | — | How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter. | `setAlertRule` body |
| Deliver to `deliverTo` | multi-select chips | optional | — | Dashboard panel · Email · Whatsapp · SMS · Push | — | CF-134. The dashboard panel is the default and the only one that always applies. | `setAlertRule` body |
| Recipient roles `recipientRoleIds` | multi-picker: choose recipient roles | optional | — | — | — | — | `setAlertRule` body |
| Cooldown minutes `cooldownMinutes` | number field (minutes) | optional | 30 | — | — | How long before the same rule may fire again. Without it, a metric hovering on a threshold produces forty alerts an hour and the panel becomes something people close. | `setAlertRule` body |
| Is active `isActive` | toggle | required | — | — | — | — | `setAlertRule` body |
| Scope path `scopePath` | text field | required | — | `setAlertRule` has no id in its path and a caller may hold several venues, so the rule names the venue it watches here — inside the caller's scope, or the write is refused. | — | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — 49 tables were in that state, so a row … | `setAlertRule` body |

Errors to draw in the form: 400 An `outsideRange` rule without both `threshold` and `thresholdUpper`, or with the upper not above the lower (audit R158)

**Form: Decide proposed action** (modal, opened by *Decide proposed action*; *Decide proposed action* calls `decideProposedAction`, *Cancel* sends nothing)

**Collects what `decideProposedAction` sends before it is called.** Required: `decision`. Optional: `reason` (asked for on a rejection). A refusal is a 403 named by its rule and shown as such (decided 28 September, audit R213 (3)): `approval-level-requires-manager` (level 2 needs a manager holding `AI_APPROVE`), `approver-is-requester` (a level 2 proposal cannot be approved by whoever prompted it), `not-own-proposal` (somebody else's level 1 proposal needs `AI_APPROVE`). An expired or already decided proposal is a 409. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | segmented control | required | — | Approve · Reject | — | — | `decideProposedAction` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `decideProposedAction` body |

Errors to draw in the form: 403 The caller may not decide this proposal (audit R213 (3)): a level 2 proposal and the caller lacks `AI_APPROVE` (`approval-level-requires-manager`), a level 2 …; 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213).

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **question**: 3–1,000 characters, English or Arabic; follow-ups keep the conversation ("compare that to this week"). When timeframe, venue or metric is missing, the assistant asks instead of guessing. *(source: contracts/satellite/reporting.yaml#askReportingQuestion / DI-964 / DI-712 / DI-019)*
- **acknowledgement note**: Optional, up to 300 characters, prompted as "What is being done about it?". *(source: contracts/satellite/reporting.yaml#/components/schemas/Alert)*
- **rejection reason**: Asked when rejecting a proposal. *(source: contracts/satellite/ai.yaml#decideProposedAction)*

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listAlerts`)

| Shows | Format | Notes |
|---|---|---|
| Raised at | 1 Oct 2026, 14:30 | — |
| Severity | chip: Info, Warning, Critical | How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter. |
| Status | chip: Raised, Acknowledged, Resolved, Expired | Where a raised alert is. Shared by `Alert` and the `listAlerts` filter. |
| Acknowledged at | 1 Oct 2026, 14:30 | — |
| Resolved at | 1 Oct 2026, 14:30 | Set when the metric returns to range, automatically. An alert that only a person can close is an alert list that only grows. |
| Escalated at | 1 Oct 2026, 14:30 | Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. |

**Every order** (data table, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |
| Hold label | text | As `Order.holdLabel`. |
| Held until | 1 Oct 2026, 14:30 | As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse. |

**Every proposed action** (data table, from `listProposedActions`): **What a caller sees follows who may decide** (decided 28 September, audit R213 (3)): with `AI_APPROVE`, every open proposal at the scope; with `AI_USE` only, the caller's own proposals, which are the level 1 ones they may approve themselves.

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Pricing, Promotion, Operational, Financial, Configuration, Content… | `content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from … |
| Target contract | text | Which contract would perform it. The assistant never performs it itself. |
| Target operation | text | — |
| Status | chip: Proposed, Approved, Rejected, Applied, Expired | Expiry (decided 28 September, audit R213): a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires … |
| Approval level | 1,234 | 8.3.65. Multi-level, because a discount and a pricing change differ in authority. |
| Proposed at | 1 Oct 2026, 14:30 | — |

**Chart** (chart): **Comparison against the previous period by default.** A number with nothing beside it is a number nobody can act on.

**The selected alert** (detail panel, from `listAlerts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Rule | the name it points at, never the id | — |
| Raised at | 1 Oct 2026, 14:30 | — |
| Severity | chip: Info, Warning, Critical | How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter. |
| Status | chip: Raised, Acknowledged, Resolved, Expired | Where a raised alert is. Shared by `Alert` and the `listAlerts` filter. |
| Observed value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Threshold | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Scope path | text | — |
| Acknowledged by principal | the name it points at, never the id | — |
| Acknowledged at | 1 Oct 2026, 14:30 | — |
| Resolved at | 1 Oct 2026, 14:30 | Set when the metric returns to range, automatically. An alert that only a person can close is an alert list that only grows. |
| Escalated at | 1 Oct 2026, 14:30 | Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Ask reporting question (primary button) | `askReportingQuestion` POST `/reports/ask` | inline | NaturalLanguageAnswer | 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope | opens modal first |
| Acknowledge alert (secondary button) | `acknowledgeAlert` POST `/alerts/{alertId}/acknowledge` | inline | Alert | — | opens modal first |
| Run report (secondary button) | `runReport` POST `/reports/{reportId}/run` | RunReportRequest | ReportResult | 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope | opens modal first |
| Save alert rule (secondary button) | `setAlertRule` PUT `/alert-rules` | AlertRule | AlertRule | 400 An `outsideRange` rule without both `threshold` and `thresholdUpper`, or with the upper not above the lower (audit R158) | opens modal first |
| Decide proposed action (secondary button) | `decideProposedAction` POST `/proposed-actions/{actionId}/decide` | inline | ProposedAction | 403 The caller may not decide this proposal (audit R213 (3)): a level 2 proposal and the caller lacks `AI_APPROVE` (`approval-level-requires-manager`), a level 2 …; 409 The action is no longer `proposed` — already … | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **answer**: The answer, then "How this was worked out" (metric, filters, period in words; the query behind a disclosure), "Data as of 14:32", and a reliability label in words — Grounded, Partly answered, Sources disagree, Not enough evidence. Never a percentage. *(source: contracts/satellite/reporting.yaml#/components/schemas/NaturalLanguageAnswer / contracts/satellite/reporting.yaml#/components/schemas/ReportingAnswerReliability)*
- **citations**: When an answer draws on a policy or document, the document is named and linked; numbers never come from a document. *(source: DI-964 / contracts/satellite/reporting.yaml#askReportingQuestion)*
- **proposals queue**: Users with approval rights see every open proposal at their scope; others see only their own. Each shows what it would change, its approval level, who proposed it and when it expires. *(source: contracts/satellite/ai.yaml#listProposedActions)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Approve / Reject a proposal**: Offered only where the rule allows (own level-1 proposal; level 2 or someone else's needs approval rights; never one's own level 2); hidden otherwise. Refusals show the named rule in words; an expired or already decided proposal shows "Already decided" (409). *(source: contracts/satellite/ai.yaml#decideProposedAction)*
- **Acknowledge alert**: Records who saw it and the note; the alert stays until its metric returns to range. *(source: contracts/satellite/reporting.yaml#acknowledgeAlert / contracts/satellite/reporting.yaml#/components/schemas/Alert)*

**Data it reads**: `listAlerts` (onLoad, What is currently raised); `listOrders` (onLoad, List orders); `listProposedActions` (onLoad, What the assistant has proposed and nobody has decided — …)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Executive Command Center*; carries `reportId`
- → `BO-010` Promotions & Coupons: *Promotions & Coupons*; carries `reportId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Tiles render in place; **each resolves on its own** so one slow source does not hold the page. |
| Error (`?state=error`) | Could not load. **Trading is unaffected** — this reads and writes nothing. |
| Empty, first run (`?state=emptyFirstRun`) | **A venue with no trading history.** Links to the seeded reports rather than showing zeroes — a dashboard of zeroes teaches a new manager nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing in this window. **Last week and last month are the useful defaults**, not today — an analytics screen opened on a Monday is asking about a period. |
| Permission denied (`?state=emptyNoAccess`) | You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 An `outsideRange` rule without both `threshold` and `thresholdUpper`, or with the upper not above the lower (audit R158); 400 Question could not be interpreted. (ReportQuestionProblem); 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 409 The action is no longer `proposed` — already decided, or expired (7 days … |

#### Edge cases to draw

- **A cashier asks for yesterday's total revenue**: The assistant answers only within the cashier's scope; a metric they may not see is answered "not available", without revealing it exists. *(source: DI-964 / contracts/satellite/reporting.yaml#askReportingQuestion)*
- **The question is outside what is modelled**: "This isn't available yet" naming the missing part; the gap is logged for the data owner; no improvised figure. *(source: contracts/satellite/reporting.yaml#askReportingQuestion)*
- **A proposal relates to an approval request (refund, discount)**: The assistant shows turnaround and bottleneck analytics only; it never recommends approve or reject. *(source: DI-735)*

#### Consistency with other screens

- Match `ANL-052`: Same answer card, reliability words and "How this was worked out" disclosure as Ask TICVAI.
- Match `ANL-018`: Alert severity labels (Info / Warning / Critical) identical to the alert centre.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Dubai Parks — Motiongate (AED)
question: What was yesterday's net revenue by channel?
answer: 'Net revenue on Tue 29 Sep was AED 386,410.50: Web AED 201,300.00, OTA AED 98,214.50, POS AED 86,896.00.'
howWorkedOut: Net revenue · by channel · 29 Sep 2026 · Motiongate · data as of 30 Sep 06:00 · Grounded
followUps:
- Compare that to last Tuesday
- Which OTA partner sold most?
proposal: Raise Fast Pass price from AED 75.00 to AED 85.00 for Fri–Sat · level 2 · proposed by Omar Haddad · expires
  02 Oct 18:00
```

#### Permissions

- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `listAlerts` → `REPORT_VIEW_VENUE` (operate) · staff
- `acknowledgeAlert` → `REPORT_VIEW_VENUE` (operate) · staff
- `listOrders` → `ORDER_VIEW` (read) · staff, guest, partner
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `setAlertRule` → `REPORT_MANAGE` (configure) · staff
- `listProposedActions` → `AI_USE` (operate) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff
- `getActionPlan` → `AI_USE` (operate) · staff

**A refused user sees:** You do not have reporting permission at this scope. **Sections you cannot see are not shown** rather than greyed out.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.7.30 | System shall support natural language reporting. | Unified Operations Dashboard | CONTRACTED | `askReportingQuestion` |
| 5.3.7 | The system should allow access to their purchase history and ongoing orders and preferences. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 5.9.4 | The system should be able to provide a detailed log of transactions for each till. Detailed log of transaction should be always accessible, searchable and printable at back office. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 22.2.11 | Ticketing History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.12 | Membership History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.15 | Reservation History | Marketing & CRM | CONTRACTED | `listOrders` |
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 13.3.14 | APIs shall expose operational, financial, attendance, membership and sales reporting data. | Developer & API Management | CONTRACTED | `runReport` |
| 8.1.4 | Approval Before Execution AI recommendations affecting pricing or financial operations shall require approval before execution | Unified Operations Dashboard | CONTRACTED | `decideProposedAction` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The AI assistant answers natural-language business queries (e.g. "what was yesterday's ticketing revenue?") only within the user's role (a CEO sees full revenue, a cashier does not), shows grounded citations naming the policy or document an answer came from, and keeps conversation context ("compare that to this week"). *(client request · MoM 21 Sep 2026, 4.8 Core AI Platform — AI Assistant (Query & Knowledge) · DI-964)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-009` · status **notStarted** · provenance generated · **Drawn as POS-6E in the client POS pack.** The pack's frame is the specification — it carries operations, states, entry params and exits, and it is better specified than anything derived from the …
- Derived from `wireframes/POS Board 6.dc.html#pos-6e`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `FnB Board 5.dc.html#fnb-5k`, `FnB Board 6.dc.html#fnb-6j`, `FnB Board 6.dc.html#fnb-6k`, `POS Board 6.dc.html#pos-6e`, `Retail Board 5.dc.html#ret-5k`, `Retail Board 6.dc.html#ret-6k`
- Flow F77 *A promotion is built, bundled, published and measured*, step 3: AI Assistant & Action Center. → **Drawn by the client as RET-5K.** 5 operations on this step.
- Flow F90 *An audience is built, offered to, and the result is judged*, step 3: AI Assistant & Action Center. → **Drawn by the client as RET-5C.**
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)
- ADR-0059 *AI phasing against the six-month plan* (`docs/adr/0059-ai-phasing-against-the-six-month-plan.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (30), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-009?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Ask reporting question, Acknowledge alert, Run report, Save alert rule, Decide proposed action.
- [ ] Every transition is wired: `ANL-001`, `BO-010`.
- [ ] Every gated control is gated: `AI_USE`, `ORDER_VIEW`, `REPORT_MANAGE`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-010` Suggestions & Advice

**Every open suggestion, what it is based on, and whether the venue took it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `ai` module |
| Block | Block D · task APP-ANALYTICS-ANL-010 |
| Who uses it | venue staff holding `AI_USE` (1 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`requestSuggestion`, `recordSuggestionOutcome`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `venueId` (session), `suggestionId` (deepLink) · cold entry: A bookmarked view opened weekly, or **a link from an alert naming one suggestion** — an alert that cannot take a manager to the thing it is about is a … |
| Route | `/analytics/suggestions` |

**What the spec says about it.** **Built 24 August.** The client F&B boards drew six suggestion endpoints — price, requisition, replenishment, scenario, SLA, demand plan. **One screen and one operation answer all six**, because a suggestion surface that differs per domain is six screens to change when the model changes. **Owns POS board frame(s) POS-6F** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Board repointed 24 August.** This screen pointed at `wireframes/POS Board 6.dc.html#pos-6f` — a frame in the client pack, which is where the design came from and not where this screen is drawn. **`P15 Kitchen Display.dc.html` and `P16 Venue Analytics.dc.html` carry one anchor per screen and nothing referenced either**, so both shipped correctly anchored and unreachable. The pack frame is kept in `derivedFrom` because provenance is worth more than the wrong pointer.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-014): No listSuggestions read of open suggestions.

**From the AI & Intelligence process.** Every open operational suggestion at the venue - replenishment, prep plan, menu engineering, staffing, send time, waste risk, price and the rest - what each is based on, and whether the venue took it. Every kind answers from day one on the venue profile and the venue-type starting pattern and says so. The one thing to get right: each card shows its stage and "Based on", a range or plain value, confidence only where a model has one, and the decision buttons record what the venue actually did.

**Known correction pending (do not draw the wrong version)**

- **Kind, Subject ref, Horizon and Context are free textFields.** Why: kind is a closed enum, subject is a picker and context is the numbers the screen shows; never typed JSON. *(source: contracts/satellite/ai.yaml#/components/schemas/SuggestionKind; AI & Intelligence)*
- **recordSuggestionOutcome asks the user for id, decidedByPrincipalId and decidedAt.** Why: Those come from the session and the server; the user gives the decision, actual value and note. *(source: contracts/satellite/ai.yaml#recordSuggestionOutcome; AI & Intelligence)*
- **There is no list operation for open suggestions; the screen can only request one.** Why: "Every open suggestion" needs a listSuggestions read. *(source: screens/P16-venue-analytics.yaml#ANL-010 (purpose); AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Kind | multi select | — | — | — | — | — | — |
| Kind | text field | — | — | — | — | Required. | — |
| Subject ref | text field | — | — | — | — | — | — |
| Horizon | text field | — | — | — | — | — | — |
| Context | text field | — | — | — | — | — | — |

**Form: Record suggestion outcome** (modal, opened by *Record suggestion outcome*; *Record suggestion outcome* calls `recordSuggestionOutcome`, *Cancel* sends nothing)

**Collects what `recordSuggestionOutcome` sends before it is called.** Required: `id`, `suggestionId`, `decision`. Optional: `actualValue`, `decidedByPrincipalId`, `decidedAt`, `realisedOutcome`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `recordSuggestionOutcome` body |
| Suggestion `suggestionId` | picker: choose a suggestion | required | — | — | shows names, sends the id | — | `recordSuggestionOutcome` body |
| Decision `decision` | radio group | required | — | Accepted · Modified · Rejected · Ignored · Expired | — | — | `recordSuggestionOutcome` body |
| Actual value `actualValue` | key and value settings | optional | — | — | — | What the venue did instead. The label. | `recordSuggestionOutcome` body |
| Decided by principal `decidedByPrincipalId` | picker: choose a decided by principal | optional | — | — | shows names, sends the id | — | `recordSuggestionOutcome` body |
| Decided at `decidedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordSuggestionOutcome` body |
| Realised outcome `realisedOutcome` | key and value settings | optional | — | — | — | Filled in later by a job, not by a person. Whether the stockout happened, whether the covers arrived, whether the margin held — nobody comes back to record this by hand, so … | `recordSuggestionOutcome` body |
| Note `note` | text area | optional | — | — | — | — | `recordSuggestionOutcome` body |

**Sent by *Request suggestion*** (`requestSuggestion`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Price · Replenishment · Requisition · Demand forecast · Prep plan · Menu engineering · Staffing · Sla target · Wait time · Upsell · Segmentation · Anomaly …; Anything else is refused — a guest asking for `price` is a guest asking what the venue is willing to … | — | A guest caller may ask for `prepPlan`, `upsell`, `waitTime` and `itinerary` only. | `requestSuggestion` body |
| Subject ref `subjectRef` | text field | optional | — | — | — | — | `requestSuggestion` body |
| Horizon `horizon` | text field | optional | — | — | — | For a forecast — `nextService`, `7d`, `28d`, or an ISO period. | `requestSuggestion` body |
| Context `context` | key and value settings | optional | — | — | — | What the caller already knows. Passed rather than re-fetched so a suggestion made from a screen uses the numbers the screen is showing — advice computed from data the manager … | `requestSuggestion` body |

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **decision (Take it / Do something else)**: Take it records accepted; Do something else asks what was done instead (actual value) and records modified or rejected with a note. Ignored and expired are recorded by the platform, not chosen. *(source: contracts/satellite/ai.yaml#recordSuggestionOutcome)*
- **ask for a suggestion**: Kind as a labelled picker (not a text field), subject (product, outlet, item), horizon (next service, 7 days, 28 days). *(source: contracts/satellite/ai.yaml#requestSuggestion)*

#### Outputs: what the screen shows and produces

**Shown**

**Card list** (card list, from `requestSuggestion`): **The basis and the stage are on the card, not behind a tap.** Every answer shows a "Based on" chip (*your venue profile, UAE calendar, weather, 23 days of your sales*) and a stage badge: Starting, Learning, Established or Trained on your data (29 September, AI functions review). "Limited historical data" while the starting pattern carries more than half the weight. Never a bare percentage.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Price, Replenishment, Requisition, Demand forecast, Prep plan, Menu engineering… | What is being suggested. A closed set, and the reason it is closed is the swap. |
| Basis | chip: Heuristic, Statistical, Model, Hybrid, Manual | How the answer was reached, and this is the field the whole design exists for. A venue must be able to see that today's price suggestion is … |
| Subject ref | text | What it is about — a product, an outlet, an item, a party. |
| Value | grouped details | The suggestion itself. Shape depends on `kind`. |
| Confidence | 1,234.5 | Null for a heuristic and that is honest. A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a … |
| Explanation | text | Plain words, always present, whatever the basis. *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain … |
| Inputs | grouped details | What went in. Recorded so the answer can be reproduced — and so that when a model replaces the rule, the two can be run against the same … |
| Producer ref | text | The rule name or the model id and version. A model version is part of the record: *the model said so* is not an answer to *which model … |
| Maturity | grouped details | Where an answer stands, on every answer (29 September, AI functions review; baseline then learn). |
| Stage | chip: Starting, Learning, Established, Learned | `starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). |
| Based on | text | The "Based on" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. |
| Sources | list or chips (count when long) | — |
| Source | chip: Venue settings, Starting pattern, Calendar, Weather, Bookings on hand, Own history… | — |
| Detail | text | e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*. |
| Observations | 1,234 | — |
| Own data share | 1,234.5 | The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked "Limited historical data". |
| Limited history | yes / no (icon or chip) | — |
| Next stage | grouped details | What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*. |
| Stage | chip: Learning, Established, Learned | — |

**Detail panel** (detail panel): The explanation in plain words and the inputs it used. **Advice computed from data the manager cannot see is advice they will not trust.**

**Missing setting** (banner, from `requestSuggestion`): Shown only on a 422 `missing-setting`: names the setting (a current cost, a par level, the venue AI profile) and links to the screen that sets it. Little history is never this banner.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Price, Replenishment, Requisition, Demand forecast, Prep plan, Menu engineering… | What is being suggested. A closed set, and the reason it is closed is the swap. |
| Basis | chip: Heuristic, Statistical, Model, Hybrid, Manual | How the answer was reached, and this is the field the whole design exists for. A venue must be able to see that today's price suggestion is … |
| Subject ref | text | What it is about — a product, an outlet, an item, a party. |
| Value | grouped details | The suggestion itself. Shape depends on `kind`. |
| Confidence | 1,234.5 | Null for a heuristic and that is honest. A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a … |
| Explanation | text | Plain words, always present, whatever the basis. *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain … |
| Inputs | grouped details | What went in. Recorded so the answer can be reproduced — and so that when a model replaces the rule, the two can be run against the same … |
| Producer ref | text | The rule name or the model id and version. A model version is part of the record: *the model said so* is not an answer to *which model … |
| Maturity | grouped details | Where an answer stands, on every answer (29 September, AI functions review; baseline then learn). |
| Stage | chip: Starting, Learning, Established, Learned | `starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). |
| Based on | text | The "Based on" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. |
| Sources | list or chips (count when long) | — |
| Source | chip: Venue settings, Starting pattern, Calendar, Weather, Bookings on hand, Own history… | — |
| Detail | text | e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*. |
| Observations | 1,234 | — |
| Own data share | 1,234.5 | The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked "Limited historical data". |
| Limited history | yes / no (icon or chip) | — |
| Next stage | grouped details | What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*. |
| Stage | chip: Learning, Established, Learned | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Request suggestion (primary button) | `requestSuggestion` POST `/ai/suggestions` | inline | Suggestion | 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem) | — |
| Record suggestion outcome (secondary button) | `recordSuggestionOutcome` POST `/ai/suggestions/{suggestionId}/outcome` | SuggestionOutcome | SuggestionOutcome | — | opens modal first |
| Take it (primary button) | navigation or local | — | — | — | — |
| Do something else (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **suggestion card**: Kind, subject, the value (e.g. "Order 18 cases of bottled water"), explanation in plain words, stage badge and Based on, "Limited historical data" where it applies, producer (rule or model version), expires at; confidence hidden when null. *(source: contracts/satellite/ai.yaml#/components/schemas/Suggestion / ADR-0051)*
- **missing setting**: A 422 shows as a banner naming the setting (e.g. "No par level for Bottled water 500 ml") with a link to set it; never "not enough data". *(source: contracts/satellite/ai.yaml#requestSuggestion (422))*

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Executive Command Center*
- → `ANL-071` AI Maturity & Learning: *AI maturity*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Open suggestions, newest first, grouped by kind. |
| Error (`?state=error`) | Could not load. **Trading is unaffected** — this advises and does not act. |
| Empty, first run (`?state=emptyFirstRun`) | **No suggestions asked for yet.** Every kind answers from day one, from the venue AI profile and the starting pattern for the venue type, and says so; the stage badge shows how much of the answer is the venue's own data. The action asks for the first one. |
| Permission denied (`?state=emptyNoAccess`) | You do not have AI permission at this venue. |
| Empty, no results (`?state=emptyNoResults`) | No suggestion of this kind. Names the kind filter and offers to clear it. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A setting the answer cannot do without is missing (29 September, AI functions review). (AiMissingSettingProblem) |

#### Edge cases to draw

- **Suggestion expired**: Hidden from the open list; visible under history as expired. *(source: contracts/satellite/ai.yaml#/components/schemas/Suggestion (expiresAt))*

#### Consistency with other screens

- Match `ANL-071`: Stage badge and Based on line are the same component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cards:
- kind: replenishment
  subject: Bottled water 500 ml - Lagoon Grill
  value: Order 18 cases by Thu
  explanation: Par 30, on hand 9, forecast use 21 over the 2-day lead time
  stage: Starting
  basedOn: your par levels, water-park pattern, weather (38°C)
  confidence: null
- kind: prepPlan
  subject: Lagoon Grill, Sat lunch
  value: Burgers 240, wraps 110, salads 60
  stage: Learning
  basedOn: forecast 2,600 guests × your menu mix over 5 weeks
```

#### Permissions

- `requestSuggestion` → `AI_USE` (operate) · staff, guest
- `recordSuggestionOutcome` → `AI_USE` (operate) · staff

**A refused user sees:** You do not have AI permission at this venue.

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.28 | Kiosks shall provide an AI assistant to guide guests through ticket selection, promotions, FAQs, recommendations, and checkout. | Ticketing Sales | CONTRACTED | `requestSuggestion` |
| 4.1.16 | Analyze menu performance and profitability. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.19 | Recommend actions to reduce waste and spoilage. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.1.20 | Recommend pricing and promotion strategies. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 4.8.15 | AI predicts potential food waste and recommends actions. | Bundles and Promotions | CONTRACTED | `requestSuggestion` |
| 5.4.24 | Segment customers automatically. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| 5.6.27 | Recommend staffing adjustments, ride allocation, and queue balancing. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| 5.6.36 | The system shall estimate queue wait times using historical and real-time operational data. | F&B & Guest Management | CONTRACTED | `requestSuggestion` |
| 8.9.9 | AI shall identify operational risks, anomalies, congestion, capacity issues, device failures, staffing shortages, and service disruptions and provide recommendations. | Unified Operations Dashboard | CONTRACTED | `requestSuggestion` |
| 15.4.7 | Inventory Optimization - System shall optimize inventory levels. | Inventory Management | CONTRACTED_PARTIAL | `requestSuggestion` |
| 22.2.25 | AI Audience Classification | Marketing & CRM | CONTRACTED | `requestSuggestion` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-010` · status **notStarted** · provenance generated · **Drawn as POS-6F in the client POS pack.** The pack's frame is the specification — it carries operations, states, entry params and exits, and it is better specified than anything derived from the …
- Derived from `wireframes/POS Board 6.dc.html#pos-6f`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 6.dc.html#pos-6f`
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-010?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Request suggestion, Record suggestion outcome, Take it, Do something else.
- [ ] Every transition is wired: `ANL-001`, `ANL-071`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**11 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"acknowledgeAlert": {"method":"POST","path":"/alerts/{alertId}/acknowledge","contract":"reporting","summary":"Mark it seen","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Alert"},
"askReportingQuestion": {"method":"POST","path":"/reports/ask","contract":"reporting","summary":"Natural-language reporting query","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"NaturalLanguageAnswer"},
"createSegment": {"method":"POST","path":"/segments","contract":"marketing-crm","summary":"Create a segment","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateSegmentRequest","responds":"Segment"},
"decideProposedAction": {"method":"POST","path":"/proposed-actions/{actionId}/decide","contract":"ai","summary":"Approve or reject a proposal","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProposedAction"},
"getActionPlan": {"method":"GET","path":"/action-plans/{planId}","contract":"ai","summary":"A plan with its steps","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiActionPlanDetail"},
"getCommandCentre": {"method":"GET","path":"/command-centre","contract":"reporting","summary":"The dashboards this login may see, grouped by module","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CommandCentre"},
"getCountVariance": {"method":"GET","path":"/stock-counts/{countId}/variance","contract":"inventory","summary":"Variance between counted and expected","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CountVariance"},
"getDashboard": {"method":"GET","path":"/dashboards/{dashboardId}","contract":"reporting","summary":"Read a dashboard with tile data","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"refresh","in":"query","required":null}],"requestBody":null,"responds":"DashboardData"},
"getForecast": {"method":"GET","path":"/forecasts","contract":"ai","summary":"Forecast values","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"definitionKey","in":"query","required":true},{"name":"versionId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"dimensionKey","in":"query","required":null},{"name":"scenarioId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getStockValuation": {"method":"GET","path":"/stock/valuation","contract":"inventory","summary":"Stock value by location and category","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"asAt","in":"query","required":null},{"name":"locationId","in":"query","required":null}],"requestBody":null,"responds":"StockValuation"},
"listAiInsights": {"method":"GET","path":"/insights","contract":"ai","summary":"Insights and anomalies","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAlerts": {"method":"GET","path":"/alerts","contract":"reporting","summary":"What is currently wrong","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"severity","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"itemId","in":"query","required":null}],"requestBody":null,"responds":"Alert"},
"listDevices": {"method":"GET","path":"/devices","contract":"tenancy","summary":"List registered devices","permission":"DEVICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listExpiringBatches": {"method":"GET","path":"/stock-batches/expiring","contract":"inventory","summary":"What is about to go out of date","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"withinDays","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrders": {"method":"GET","path":"/orders","contract":"orders","summary":"List orders","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"createdFrom","in":"query","required":null},{"name":"createdTo","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":"tender","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPrincipals": {"method":"GET","path":"/principals","contract":"identity","summary":"List principals","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"scopePath","in":"query","required":null},{"name":"isActive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProposedActions": {"method":"GET","path":"/proposed-actions","contract":"ai","summary":"What the assistant has proposed and nobody has decided","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProposedAction"},
"listSegments": {"method":"GET","path":"/segments","contract":"marketing-crm","summary":"List segments","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"previewSegment": {"method":"POST","path":"/segments/{segmentId}/preview","contract":"marketing-crm","summary":"Estimate segment size and reachability","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SegmentPreview"},
"recordDashboardView": {"method":"POST","path":"/dashboards/{dashboardId}/views","contract":"reporting","summary":"Record that a dashboard was opened","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"recordSuggestionOutcome": {"method":"POST","path":"/ai/suggestions/{suggestionId}/outcome","contract":"ai","summary":"What the venue actually did","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SuggestionOutcome","responds":"SuggestionOutcome"},
"requestSuggestion": {"method":"POST","path":"/ai/suggestions","contract":"ai","summary":"Ask for an answer, however it is currently produced","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Suggestion"},
"runReport": {"method":"POST","path":"/reports/{reportId}/run","contract":"reporting","summary":"Run a report","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RunReportRequest","responds":"ReportResult"},
"setAlertRule": {"method":"PUT","path":"/alert-rules","contract":"reporting","summary":"Watch a metric and tell somebody","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AlertRule","responds":"AlertRule"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiActionPlan": {"type":"object","x-ticvai-persistence":"ai.action_plan","description":"**A plan: plan, validate, simulate, approve, execute, with rollback** (design 2.2 D, 3.8; AIC-086..107). Independent of any conversation (AIC-102). Its steps are `ai.action_step`; the change set is hashed so what was approved is what runs (AIC-181).","required":["origin","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"origin":{"type":"string","enum":["configurationSession","generateConfiguration","assistant","riskCase","operationalRequirement","rollback"]},"originRef":{"type":"string","nullable":true},"summary":{"type":"string"},"status":{"type":"string","enum":["draft","validated","simulated","awaitingApproval","approved","executing","paused","completed","partiallyCompleted","failed","compensated","cancelled","rolledBack"],"readOnly":true},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"},"approvalTier":{"type":"integer","minimum":1,"maximum":2,"description":"The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). Not an autonomy level."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request, where tier 2 or the matrix caught the plan."},"proposedActionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.proposed_action","description":"The `ai.proposed_action` the plan is presented as for a decision."},"changeSetHash":{"type":"string","readOnly":true},"governanceOutcome":{"allOf":[{"$ref":"#/components/schemas/AiGovernanceOutcome"}],"readOnly":true},"policyVersionRef":{"type":"string","readOnly":true,"description":"The governance policy version that decided it."},"simulation":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4)."},"partialCompletionAllowed":{"type":"boolean","default":false,"description":"Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134)."},"rollbackOfPlanId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.action_plan"},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiActionPlanDetail": {"type":"object","x-ticvai-persistence":"none — ai.action_plan with its ai.action_step rows","description":"A plan with its steps in DAG order.","required":["plan","steps"],"properties":{"plan":{"$ref":"#/components/schemas/AiActionPlan"},"steps":{"type":"array","items":{"$ref":"#/components/schemas/AiActionStep"}}}},
"AiActionStep": {"type":"object","x-ticvai-persistence":"ai.action_step","description":"One step of a plan: a registered tool against `targetContract.targetOperation` at a contract version (AIC-095), with payload, provenance, compensation and the idempotency key `plan:{id}:step:{n}`. **Scoped through its plan** (`platform.apply_parent_rls`). Each step records its target object's version; drift pauses the plan (AIC-182).","required":["planId","stepNumber","toolKey","targetContract","targetOperation","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"planId":{"type":"string","format":"uuid","x-ticvai-references":"ai.action_plan"},"stepNumber":{"type":"integer","minimum":1},"dependsOn":{"type":"array","items":{"type":"integer","minimum":1},"description":"Step numbers that must succeed first. The plan is a DAG."},"toolKey":{"type":"string"},"targetContract":{"type":"string"},"targetOperation":{"type":"string"},"contractVersion":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body of `targetOperation`, validated against it before the plan is approved."},"provenance":{"$ref":"#/components/schemas/AiProvenance"},"idempotencyKey":{"type":"string","readOnly":true},"targetObjectRef":{"type":"string","nullable":true},"targetObjectVersion":{"type":"string","nullable":true,"description":"The version the step was planned against. A different version at execution is drift."},"reversible":{"type":"boolean"},"compensation":{"type":"object","additionalProperties":true,"nullable":true},"status":{"type":"string","enum":["pending","validated","running","succeeded","failed","compensated","skipped","paused"],"readOnly":true},"attempts":{"type":"integer","minimum":0,"maximum":3,"readOnly":true,"description":"Bounded at 3 (AIC-135)."},"lastError":{"type":"string","nullable":true,"readOnly":true},"resultRef":{"type":"string","nullable":true,"readOnly":true,"description":"The owning service's response: success is its answer, not a model's judgement (AIC-097)."},"startedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"AiEvidenceItemList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The evidence of one decision record, stored with it.","items":{"$ref":"#/components/schemas/AiEvidenceItem"}},
"AiForecastPoint": {"type":"object","x-ticvai-persistence":"ai.forecast_point","description":"One forecast value with its interval: 10th, 50th and 90th percentile (design 5.6: a range, never a bare percentage). Partitioned by target month. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["versionId","targetStart","p50"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"versionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_version"},"scenarioId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.forecast_scenario","description":"Set where the point belongs to a what-if scenario rather than the version itself."},"targetStart":{"type":"string","format":"date-time"},"targetEnd":{"type":"string","format":"date-time"},"dimensionKey":{"type":"string","nullable":true,"description":"Canonical key of the breakdown, e.g. `product=…;channel=web`."},"p10":{"type":"number","nullable":true},"p50":{"type":"number"},"p90":{"type":"number","nullable":true},"unit":{"type":"string"},"drivers":{"type":"object","additionalProperties":true,"nullable":true,"description":"Component decomposition or SHAP contributions, largest first (ADM-506)."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastVersion": {"type":"object","x-ticvai-persistence":"ai.forecast_version","description":"**An immutable forecast version** (AIP-032): producer, model version, data cut-off, horizon and status. Nothing is overwritten; yesterday's actuals are scored against every earlier version.","required":["definitionId","versionNumber","status","basis"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"definitionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_definition"},"versionNumber":{"type":"integer","minimum":1},"module":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"}],"readOnly":true,"description":"The module of the version's definition (`AiForecastDefinition.module`), copied when the version is produced; the module whose AI publish permission `publishForecastVersion` requires (CHG-FUP-004)."},"status":{"type":"string","enum":["running","draft","awaitingApproval","published","superseded","rejected","failed"],"readOnly":true},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producerRef":{"type":"string"},"modelVersion":{"type":"string","nullable":true},"dataCutoffAt":{"type":"string","format":"date-time","description":"The analytical replica watermark the snapshot was taken at."},"horizonStart":{"type":"string","format":"date-time"},"horizonEnd":{"type":"string","format":"date-time"},"qualityChecks":{"type":"object","additionalProperties":true,"readOnly":true,"description":"Each gate and whether it passed."},"publishedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal","description":"Null where the definition auto-published."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiInsight": {"type":"object","x-ticvai-persistence":"ai.insight","description":"**An insight with a lifecycle** (AIP-181): new, reviewed, accepted or rejected, actioned, measured. Anomalies, forecast deviations, trends and opportunities land here; the narrative binds numbers to results, so a figure can only come from a query (design 8, 5.10).","required":["kind","title","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["anomaly","forecastDeviation","trend","opportunity","executiveSummary","rootCause","forecastThreshold","marketingRecommendation"]},"detectorId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.anomaly_detector"},"metricKey":{"type":"string","nullable":true},"subjectKind":{"type":"string","nullable":true,"enum":["campaign","journey","forecastDefinition","venue"],"description":"What the insight is about where it is not a KPI (29 September, build): a marketing-crm campaign or journey for `marketingRecommendation`, a forecast definition for `forecastThreshold`."},"subjectRef":{"type":"string","nullable":true},"recommendedAction":{"type":"object","additionalProperties":true,"nullable":true,"description":"For `marketingRecommendation`: `{recommendation, parameters}` as `AiMarketingRecommendation`. Applied by a person in the owning module, never here."},"expectedImpact":{"type":"object","additionalProperties":true,"nullable":true,"description":"A range on a named metric (`metric`, `low`, `high`), never a single number (design 5.6)."},"title":{"type":"string"},"narrative":{"type":"string","nullable":true},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"magnitude":{"type":"number","nullable":true},"priority":{"type":"string","enum":["low","medium","high","critical"]},"correlationKey":{"type":"string","nullable":true},"status":{"type":"string","enum":["new","reviewed","accepted","rejected","actioned","measured"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"actionRef":{"type":"string","nullable":true},"measuredImpact":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"detectedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"Alert": {"type":"object","x-ticvai-persistence":"reporting.alert","description":"A raised alert. **Acknowledged rather than dismissed** — CF-134 asked for it markable, and the difference is that an acknowledgement records who saw it.\n","required":["id","ruleId","raisedAt","severity","status"],"properties":{"id":{"type":"string","format":"uuid"},"ruleId":{"type":"string","format":"uuid"},"ruleName":{"type":"string","description":"`AlertRule.name` as it stood when the alert was raised. **The line a person reads** — a list of rule ids is not an alert panel, and a screen should not need `listAlertRules` to label one.\n"},"metric":{"allOf":[{"$ref":"#/components/schemas/MetricSource"}],"description":"The rule's metric, carried so the alert says what went out of range."},"raisedAt":{"type":"string","format":"date-time"},"severity":{"$ref":"#/components/schemas/AlertSeverity"},"status":{"$ref":"#/components/schemas/AlertStatus"},"observedValue":{"$ref":"#/components/schemas/MetricValue"},"threshold":{"$ref":"#/components/schemas/MetricValue"},"scopePath":{"type":"string"},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation the reading was taken for, where the metric is measured per workstation (`salesByWorkstation`). Null otherwise. `listAlerts` filters on it."},"shiftId":{"type":"string","format":"uuid","nullable":true,"description":"The till shift (`orders.pos_shift`) the reading belongs to, where it was taken for a workstation with a shift open. Null otherwise. `listAlerts` filters on it."},"itemId":{"type":"string","format":"uuid","nullable":true,"description":"The inventory item the reading is about, where the metric is measured per item (`stockAgeing`, `stockTurnover`, `wastageRate`, `inventoryValuation`). Null otherwise. **What a replenishment screen prefills a requisition from.**\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true},"acknowledgementNote":{"type":"string","maxLength":300,"nullable":true,"description":"The `note` given to `acknowledgeAlert`. Kept, because an acknowledgement that says what is being done about it is the one escalation can skip."},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"description":"**Set when the metric returns to range, automatically.** An alert that only a person can close is an alert list that only grows.\n"},"escalatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. **A critical alert nobody acknowledged is the case escalation exists for.**\n"}}},
"AlertRule": {"type":"object","x-ticvai-persistence":"reporting.alert_rule","description":"BL-152, CF-134. **Six contracts detect their own trouble and none told a person.**\nFive sections ask for this and it is the same gap as `MessageTrigger`, seen from the operational side — **that one tells a guest something happened; this one tells an operator something is wrong.**\n**A threshold that nobody is watching is a threshold nobody set.** 6.1.57 wants an exception when a KPI leaves range, and an exception that arrives in a nightly report is an exception nobody acted on.\n","required":["id","name","metric","comparator","threshold","severity","isActive","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"metric":{"allOf":[{"$ref":"#/components/schemas/MetricSource"}],"description":"**From the closed set**, so a rule cannot watch something nothing produces — the same discipline `MetricSource` exists for.\n"},"comparator":{"type":"string","enum":["above","below","outsideRange","changesBy","equals"]},"threshold":{"$ref":"#/components/schemas/MetricValue"},"thresholdUpper":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true,"description":"**Required when `comparator` is `outsideRange`** (decided 28 September, audit R158): the range is `threshold` to `thresholdUpper`, and a rule missing either, or with the upper not above the lower, is refused by `setAlertRule` with 400. Ignored for every other comparator.\n"},"windowMinutes":{"type":"integer","default":15,"description":"**The window is what stops an alert firing on noise.** A queue that spikes for ninety seconds is not a queue that needs a manager, and a rule with no window is a rule somebody mutes within a week.\n"},"severity":{"$ref":"#/components/schemas/AlertSeverity"},"deliverTo":{"type":"array","description":"CF-134. **The dashboard panel is the default and the only one that always applies.** Email or WhatsApp where the matrix names them — an operational alert arriving by email is an alert nobody sees in time.\n","items":{"type":"string","enum":["dashboardPanel","email","whatsapp","sms","push"]},"x-ticvai-push-note":"**`push` added 29 September** (6.1.56, 18.1.5, build pass): delivered to every staff-app handset registered for a recipient (tenancy `RegisteredDevice`, kind `mobileHandset`, with a push token). It is how a daily revenue alert reaches a manager's phone, which a panel on a web dashboard does not.\n"},"recipientRoleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"cooldownMinutes":{"type":"integer","default":30,"description":"**How long before the same rule may fire again.** Without it, a metric hovering on a threshold produces forty alerts an hour and the panel becomes something people close.\n"},"isActive":{"type":"boolean"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**\n\n**Required, and it is the write target.** `setAlertRule` has no id in its path and a caller may hold several venues, so the rule names the venue it watches here — inside the caller's scope, or the write is refused."}}},
"AlertSeverity": {"type":"string","description":"How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter.","enum":["info","warning","critical"]},
"AlertStatus": {"type":"string","description":"Where a raised alert is. Shared by `Alert` and the `listAlerts` filter.","enum":["raised","acknowledged","resolved","expired"]},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"CommandCentre": {"x-ticvai-persistence":"none — computed per caller from `reporting.dashboard`, the tenant's licensed modules and the principal's permissions","type":"object","description":"**What one login sees in the command centre.** Not stored: two principals in the same venue receive different command centres, and a stored one would be wrong the moment a role or a licence changed.","required":["modules","resolvedAt"],"properties":{"modules":{"type":"array","items":{"type":"object","required":["module","dashboards"],"properties":{"module":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},"dashboards":{"type":"array","description":"Shared first, then the caller's own, each by name. Tile data is not included — `getDashboard` reads one with its data when it is opened.","items":{"$ref":"#/components/schemas/Dashboard"}},"canAuthor":{"type":"boolean","description":"**Whether the caller may build a dashboard for this module** — `REPORT_MANAGE` plus entitlement to the module. Returned so the shell can offer the drag-and-drop authoring entry point only where `createDashboard` would accept it; the server still enforces it on the write."}}}},"resolvedAt":{"type":"string","format":"date-time","description":"When the entitlement was evaluated. A licence or role change after this is not reflected until the next read."}}},
"CountVariance": {"x-ticvai-persistence":"none — computed at close","type":"object","required":["countId","totalVarianceValue","lines"],"properties":{"countId":{"type":"string","format":"uuid"},"totalVarianceValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"exceptionCount":{"type":"integer","description":"Lines beyond `VenueSettings.inventory.countVarianceTolerancePercent` (proposed default 2 per cent, audit R094), requiring review before posting."},"lines":{"type":"array","items":{"type":"object","required":["itemId","expectedQuantity","countedQuantity","variance","isException"],"properties":{"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"sku":{"type":"string"},"expectedQuantity":{"type":"number"},"countedQuantity":{"type":"number"},"variance":{"type":"number"},"variancePercentage":{"type":"number"},"varianceValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isException":{"type":"boolean"},"recountCount":{"type":"integer","description":"A line counted several times is itself a finding."},"note":{"type":"string","nullable":true}}}}}},
"CreateSegmentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","criteria"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid"},"match":{"type":"string","enum":["all","any"],"default":"all"},"criteria":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/SegmentCriterion"}},"excludeSegmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"ruleGroups":{"x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","type":"array","description":"**Nested AND / OR / NOT groups** (contract gap CHG-WIR-007, BO-755; CHG-CSA-045). Where present, the segment matches `criteria` (combined by `match`) AND every group here. Absent keeps the flat list.","items":{"$ref":"#/components/schemas/SegmentRuleGroup"}},"effectiveFrom":{"type":"string","format":"date-time","nullable":true,"description":"The segment is evaluated for sends only from this time."},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who answers for the segment; defaults to its creator."},"requiresApproval":{"type":"boolean","default":false,"description":"Where true, a campaign may use the segment only after an `approvals` request on it is approved."}}},
"Dashboard": {"x-ticvai-persistence":"reporting.dashboard + reporting.dashboard_tile","allOf":[{"$ref":"#/components/schemas/CreateDashboardRequest"},{"type":"object","required":["id","ownerPrincipalId","aggregateCost","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid"},"aggregateCost":{"type":"string","enum":["low","medium","high"],"description":"Combined refresh load of every tile."},"archivedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"},"createdAt":{"type":"string","format":"date-time"}}}]},
"DashboardData": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/Dashboard"},{"type":"object","properties":{"tileData":{"type":"array","items":{"type":"object","properties":{"tileId":{"type":"string","format":"uuid"},"result":{"$ref":"#/components/schemas/ReportResult"},"isCached":{"type":"boolean"},"error":{"type":"string","nullable":true}}}}}}]},
"DeviceApprovalStatus": {"type":"string","description":"Whether a registered device may go into production (DEC-241, DEC-245; CHG-CSP-011). The model is `states/registered-device-approval.yaml`.\n","enum":["pendingApproval","approved","rejected"]},
"DeviceCapability": {"type":"string","description":"BL-179. **Something a driver reports, not something the platform provides.** The list grows as vendors are added, which is ADR-0015's whole position: adding a vendor is a driver plus configuration rather than a core change.\n**`genderClassification` is here because `VenueSettings.segregatedAccess. genderVerification` already offers `deviceAssisted` and nothing answered it** — a switch with no driver behind it. Where a venue's access hardware performs the check and the venue chooses to use it, the result is **advisory to the steward and never decisive at the turnstile** (`ValidationResult.advisory`). 3.2.45 asks for rejection; the package deviates deliberately and CF-130 records why.\n**Access's capabilities merged in** (ADR-0067, 1 October): `dynamicQr`, `rfid`, `nfc`, `facePass`, `offline` and `heightCheck` were the access register's own list, from the compatibility matrix.\n","enum":["genderClassification","dynamicQr","rfid","nfc","facePass","offline","heightCheck"]},
"DeviceKind": {"type":"string","enum":["receiptPrinter","ticketPrinter","labelPrinter","cashDrawer","barcodeScanner","rfidReader","nfcReader","cardReader","idReader","biometricReader","accessReader","paymentTerminal","customerDisplay","signageDisplay","kitchenDisplay","turnstileController","wristbandEncoder","signaturePad","scale","camera","mobileHandset","handheldScanner","accessPodium","bleBeacon"],"description":"`mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation.\n**One kind vocabulary for every device** (ADR-0067, 1 October). `handheldScanner`, `accessPodium` and `bleBeacon` came from Access's register; the finer hardware type (a speed gate under `turnstileController`, a tablet under `handheldScanner`) is `RegisteredDevice.hardwareType` (common `DeviceHardwareType`).\n"},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"GeneratedQuery": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n","properties":{"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"compiledSql":{"type":"string","nullable":true,"description":"The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"}}},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MetricSource": {"type":"string","description":"**A named metric with a verified source.** BL-053, 75 requirement rows.\n`reporting` is a generic builder, and **a generic builder makes every reporting requirement look covered** — it will happily assemble a report over data nobody produces. That is the shape to watch across the whole walk, and this enum is the answer to it: each value below was checked against the schema before being named.\n| Metric | Source | |---|---| | `occupancy` | `catalogue.channel_capacity.sold` and `leased` against `capacity` | | `capacityUtilisation` | `catalogue.channel_capacity.remaining` over the same window | | `admissionRate` | `access.scan_event.outcome`, in-direction | | `noShowRate` | Entitlements issued against scans that never arrived | | `conversion` | `orders.cart` against `orders.sales_order` | | `salesByOperator` | `orders.sales_order.principal_id` | | `salesByWorkstation` | The workstation on the shift that took it | | `waitTime` | `queue.waiting_guest.estimated_call_at` against `called_at` | | `throughput` | `queue.waiting_guest` completions per hour | | `abandonmentRate` | Queue entries that left before being called |\n**`salesByInstructor` was deliberately absent from the first cut** because it needed the staff-assignment link CL-01 covers. It was added on 18 August once `resources.Resource` produced it — see `x-ticvai-extension-note` below. Naming a metric with no source is still the defect this enum exists to prevent.\n**Money-valued metrics are listed in `x-ticvai-money-valued`.** A reading or threshold on one of them is a `Money`, never a float (`MetricValue`).\n","enum":["occupancy","capacityUtilisation","admissionRate","noShowRate","conversion","salesByOperator","salesByWorkstation","waitTime","throughput","abandonmentRate","inventoryValuation","stockTurnover","stockAgeing","wastageRate","resaleVolume","resaleCommission","salesByInstructor","resourceUtilisation","allocationUtilisation","channelAllocationBurn","membershipChurn","membershipRenewalRate","supplierDeliveryPerformance","revenuePerEntitlement","revenuePerVisitor","assetDowntime","meanTimeToRepair","challengeCompletionRate","attributedRevenue","loyaltyActiveMembers","loyaltyTierDistribution","loyaltyPointsLiability","loyaltyBreakageRate","loyaltyMemberRetention","challengeParticipationRate","gamificationLoyaltyImpact","gamificationMembershipImpact","gamificationRetention","accreditationApplications","accreditationTimeToDecision","accreditationCredentialsIssued","accreditationActiveHolders","accreditationRenewalsDue","staffingShortfall","grossSales","discounts","refunds","netRevenue","recognisedRevenue","deferredRevenue","taxCollected","takings"],"x-ticvai-money-valued":["grossSales","discounts","refunds","netRevenue","recognisedRevenue","deferredRevenue","taxCollected","takings","inventoryValuation","resaleCommission","revenuePerEntitlement","revenuePerVisitor","attributedRevenue","loyaltyPointsLiability"],"x-ticvai-extended-29-september":"**Fourteen metrics added 29 September (build pass)**, each checked against the schema of the contract that produces it.\n\n| Metric | Source | Requirement | |---|---|---| | `loyaltyActiveMembers` | `marketing.loyalty_position` members with a `marketing.loyalty_points` movement in the period | 5.4.27 | | `loyaltyTierDistribution` | `marketing.loyalty_position.tier_id` against `marketing.programme_tier`, members per tier | 5.4.27 | | `loyaltyPointsLiability` | the balance of `ledger.journal_line` on each programme's `pointsLiabilityAccountId`, where points post on accrual and release on redemption or expiry | 5.4.27 | | `loyaltyBreakageRate` | `marketing.loyalty_points` expiry movements over points earned, in the period | 5.4.27 | | `loyaltyMemberRetention` | members with a movement in the previous period who also have one in this period | 5.4.27 | | `challengeParticipationRate` | distinct `marketing.challenge_progress.subject_id` over active loyalty members | 22.6.20 | | `gamificationLoyaltyImpact` | points earned per member, challenge participants against non-participants (`marketing.loyalty_points` split by `marketing.challenge_progress`) | 22.6.20 | | `gamificationMembershipImpact` | joins and renewals in `identity.customer_membership`, participants against non-participants | 22.6.20 | | `gamificationRetention` | return visits (`access.scan_event`, in-direction) of participants against non-participants | 22.6.20 | | `accreditationApplications` | `accreditation.application` by `status` | 12.1.50 | | `accreditationTimeToDecision` | `accreditation.application.decided_at` minus `submitted_at` | 12.1.50 | | `accreditationCredentialsIssued` | `accreditation.credential.issued_at` | 12.1.50 | | `accreditationActiveHolders` | `accreditation.holder` `active`, by `category_code` | 12.1.50 | | `accreditationRenewalsDue` | `accreditation.holder.valid_to` inside `accreditation.validity.renewal_window_days` | 12.1.50 |\n\n**`staffingShortfall` added the same evening (build pass, group G2; 8.2.49)**: the largest gap in the window between the staff rostered and the staff the forecast requires, per venue and position, from `workforce.forecast_requirement` (the handed-over AI staff requirement) against `workforce.rota_assignment` and `workforce.open_shift`, computed as `workforce.getStaffingCoverage` with `basis` `forecastRequirement`. An `AlertRule` on it with `comparator` `above` and `threshold` 0 is the staffing shortage alert; `windowMinutes` looks ahead rather than back for this metric (the rota for the coming window), and `cooldownMinutes` stops one short shift alerting every quarter hour.\n\n**Points issued, points redeemed, campaign performance and reward redemption were already served** by the `loyalty` and `campaigns` sources, and challenge completion and revenue attribution by `challengeCompletionRate` and `attributedRevenue`.\n","x-ticvai-extended-2-october":"**Eight finance measures added 2 October 2026** (Chinmay; CHG-FIN-007, CHG-FIN-010), each with the source and formula of the seeded KPI of the same code in `ReportingSystemKpi`: `grossSales`, `discounts`, `refunds`, `netRevenue`, `recognisedRevenue`, `deferredRevenue`, `taxCollected` and `takings`, so an alert rule can watch them (a refund spike, takings below a target). Formulas are the D-185 default; client finance sign-off is pending.","x-ticvai-money-valued-note":"**`salesByOperator`, `salesByWorkstation` and `resaleVolume` are not listed because the package does not say whether they count sales or sum their value.** Until that is decided, a rule on them carries a plain number.\n","x-ticvai-extended":"18 August 2026","x-ticvai-extension-note":"**Nineteen metrics added when their upstream models landed**, which is how BL-053 was always going to close — not by changing `reporting` but by building the things it wanted to report on.\n`inventoryValuation`, `stockTurnover`, `stockAgeing` and `wastageRate` came from `inventory.StockBatch`; `resaleVolume` and `resaleCommission` from `orders.ResaleListing`; **`salesByInstructor` from `resources.Resource`, which was the one metric this enum deliberately refused to name in the morning** because nothing produced it. `allocationUtilisation` from `PartnerUser` and `ChannelListing`, `membershipChurn` from `Journey`, `supplierDeliveryPerformance` from `ProductionRun`, `assetDowntime` and `meanTimeToRepair` from `WorkOrder.downtimeMinutes`, `challengeCompletionRate` from `ChallengeProgress`, `attributedRevenue` from `AttributionTouch`.\n**Each was checked against the schema before being named.** That rule has not changed — naming a metric with no source is the defect this enum exists to prevent.\n"},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"NaturalLanguageAnswer": {"x-ticvai-persistence":"none — computed","type":"object","required":["conversationId","question","interpretation","result","reliability"],"properties":{"conversationId":{"type":"string"},"question":{"type":"string"},"interpretation":{"type":"string","description":"What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."},"semanticSpec":{"allOf":[{"$ref":"#/components/schemas/ReportingSemanticQuerySpec"}],"nullable":true,"description":"What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"},"generatedQuery":{"allOf":[{"$ref":"#/components/schemas/GeneratedQuery"}],"nullable":true,"description":"The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"},"result":{"allOf":[{"$ref":"#/components/schemas/ReportResult"}],"nullable":true,"description":"Null when the question is outside the semantic model."},"dataAsOf":{"type":"string","format":"date-time","nullable":true,"description":"Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."},"reliability":{"$ref":"#/components/schemas/ReportingAnswerReliability"},"unavailableReason":{"allOf":[{"$ref":"#/components/schemas/ReportingUnavailableReason"}],"nullable":true,"description":"Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."},"confidence":{"type":"number","minimum":0,"maximum":1,"deprecated":true,"description":"Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."},"suggestedFollowUps":{"type":"array","items":{"type":"string"}},"modelVersion":{"type":"string"},"tokensUsed":{"type":"integer"}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"OrderSummary": {"x-ticvai-persistence":"none — projection","type":"object","required":["id","orderNumber","status","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"The same vocabulary as `Order.channel`, which this projects."},"lineCount":{"type":"integer"},"principalId":{"type":"string","format":"uuid","description":"The cashier who raised it — what the held-orders list shows."},"holdLabel":{"type":"string","nullable":true,"description":"As `Order.holdLabel`."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"description":"As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."},"createdAt":{"type":"string","format":"date-time"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Principal": {"x-ticvai-persistence":"identity.principal","type":"object","required":["id","username","displayName","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"username":{"type":"string"},"displayName":{"type":"string"},"isActive":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"Past this, resolution returns DENY regardless of grants."},"primaryRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Determines the landing screen when the principal holds several roles and picks one at login.\n"},"roles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"lastLoginAt":{"type":"string","format":"date-time","nullable":true}}},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true},"eventId":{"type":"string","format":"uuid","nullable":true,"description":"**The event this product sells admission to** (4 October 2026, CHG-FXC-011; WEB-002, WEB-004): a product page finds its event and the event's performances (`Performance.eventId`) give it dates. Null for a product not tied to an event (merchandise, a pass, a membership)."}}},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"translationJobId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `proposeTranslations` job that drafted this proposal; `getTranslationProposals` reads a job's rows by it. Null on every other proposal (CHG-RFM-004)."},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"RegisteredDevice": {"x-ticvai-persistence":"platform.device","type":"object","description":"**The only device register** (ADR-0067, accepted 1 October; the register of record since 29 September). Identity (kind, hardware type, model, serial), every version (firmware, configuration, rule package, credential package), health, heartbeat and one lifecycle (`enrolmentState`: registered, enrolled, provisioned, active, deactivated, retired) for every device in the estate live on this row. The access-control device row, which repeated serial, versions, health and lifecycle, is now `access.device_placement` and holds only where an access-control device is placed. Tenancy owns and migrates this table; Access reads it only through this contract.\n","required":["id","kind","driver"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change (ADR-0015).\n"},"identifier":{"type":"string","nullable":true},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control device (one with a `hardwareType`), which is placed in the gate topology by access `placeAccessDevice` rather than bound to a workstation (ADR-0067); `registerDevice` refuses either mistake with `422`.\n"},"model":{"type":"string","nullable":true},"hardwareType":{"$ref":"../shared/common.yaml#/components/schemas/DeviceHardwareType","nullable":true,"description":"**The specific hardware under `kind`** (ADR-0067, 1 October): Access's hardware types (a speed gate, a tripod turnstile, a podium) merged into the one register. Null for a device with no finer type than its kind.\n"},"hardwareModelId":{"type":"string","format":"uuid","nullable":true,"description":"The model in the hardware library (access `setHardwareModel`; ADR-0067). Access owns the library; this names a model in it.\n"},"serialNumber":{"type":"string","nullable":true,"maxLength":100,"description":"The manufacturer's serial (ADR-0067: was on the access-control device row, now `access.device_placement`). A serial already registered in the tenant is refused `409` by `registerDevice`.\n"},"ipNetworkReference":{"type":"string","nullable":true,"description":"Network address or reference the device is reached at (ADR-0067)."},"configurationVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Access configuration version the device reports running (ADR-0067)."},"localRuleVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Admission rule package the device reports running (ADR-0067)."},"credentialSecurityPackageVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Credential security package the device reports running (ADR-0067)."},"scannerHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Component health as the device or vendor reports it on its heartbeat (ADR-0067)."},"controllerHealth":{"type":"string","nullable":true,"readOnly":true},"cameraHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Where the device has a camera."},"connectivity":{"type":"string","nullable":true,"readOnly":true,"description":"Reported connectivity."},"pushToken":{"type":"string","format":"password","nullable":true,"writeOnly":true,"description":"BL-163. **Guest devices register for push and staff devices did not** — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has to walk to.\nWrite-only, and marked `writeOnly`: accepted by `registerDevice` and never returned by `listDevices` or `getDevice`. **A push token is a credential**, and the rule that no surface holds a provider key applies here too.\n"},"pushPlatform":{"type":"string","nullable":true,"enum":["ios","android","web","windows"]},"pushFailureCount":{"type":"integer","default":0,"readOnly":true,"description":"**Consecutive failures.** A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a notification queue fills with nothing.\n"},"offlineScope":{"type":"string","nullable":true,"enum":["none","readOnly","sellAndScan","fullVenue"],"description":"BL-163. **What this device may do with no connection**, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it settled.\n**`fullVenue` on a personal handset is a decision, not a default** — a device that can do everything offline is a device that carries the whole venue's data in somebody's pocket.\n"},"firmwareVersion":{"type":"string","nullable":true,"readOnly":true,"description":"As the device last reported it on its heartbeat."},"isRequired":{"type":"boolean","description":"True blocks shift open when the device is unreachable."},"status":{"type":"string","readOnly":true,"enum":["online","offline","error","consumableLow","needsAttention","localMode","unknown"],"description":"What the device last said on its heartbeat; `unknown` until it has. `localMode` is an access-control device validating from its offline package with its link down (ADR-0067).\n"},"batteryPercent":{"type":"integer","nullable":true,"readOnly":true,"minimum":0,"maximum":100,"description":"Board 1 of the client's POS design set, 20 August. **A wristband encoder at 8% is a gate that stops working in an hour**, and nothing in the package carried it.\n**Null where the device has no battery**, which is most of them — a receipt printer reporting 100% forever is worse than one reporting nothing.\n"},"lastCheckedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Distinct from `lastHeartbeatAt`.** A heartbeat is the workstation saying the device is attached; a check is the device answering. **A printer with no paper heartbeats perfectly**, which is why the client's board shows both columns.\n"},"health":{"type":"string","enum":["healthy","warning","degraded","offline","unknown"],"default":"unknown","readOnly":true,"description":"**Derived, not reported.** Computed from heartbeat age, battery, firmware currency and error rate — a device does not know whether it is healthy, and asking it produces a fleet that is 100% healthy and 12% broken.\n"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"capabilities":{"type":"array","readOnly":true,"items":{"$ref":"#/components/schemas/DeviceCapability"},"description":"BL-179. **What this driver reports it can do, beyond reading media.** ADR-0015 is standards-first — the device does what the device does — and until now a venue could switch on a feature that depended on hardware without anything being able to say whether the hardware was there.\n**A capability absent is a capability unavailable**, not a capability assumed. A venue setting that requires one is refused where no device in scope reports it, rather than silently doing nothing at the gate.\n"},"enrolmentState":{"type":"string","enum":["registered","enrolled","provisioned","active","deactivated","retired"],"default":"registered","readOnly":true,"description":"BL-160. **Where the device is in its life, which is not the same question as whether it is answering.** `enrolDevice` has taken the whole matrix — registered, enrolled, provisioned, active, deactivated, retired — since 16.1.2, and until now there was no column for it to land in, so the operation read this table and wrote nothing.\n**Distinct from `status` and from `health`.** `status` is what the device last said and `health` is what we computed from it; a decommissioned turnstile still sitting on the network is `online` and `retired` at once, and neither column contradicts the other. **A device that is `retired` is refused at the gate whatever its status says.**\nThe transition itself — who moved it, from what, and why — is a `tenancy.device_audit` record. It is not repeated here, because the latest transition stored in two places is one place to go stale.\n"},"retiredAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set when `enrolmentState` reaches `retired`, and null otherwise.** Derivable from `tenancy.device_audit`, and kept as a column for the same reason `maintenance.asset.retired_on` is one: a retirement date you reconstruct from an audit log is a date nobody filters a fleet by.\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**The profile this device was provisioned with.** `enrolDevice` has accepted one since 16.1.3 and there was nowhere to keep it, so the answer to *\"what is this reader configured as\"* lived only in the request that set it.\n"},"approvalStatus":{"allOf":[{"$ref":"#/components/schemas/DeviceApprovalStatus"}],"default":"pendingApproval","readOnly":true,"description":"**A new device waits for approval before it may go live** (decided 2 October 2026, Chinmay, critical set 1, BO-196: \"Secure enrolment code + pending approval\"; DEC-241; CHG-CSP-011; MoM 15 September, DI-892, DI-906). Every device registers `pendingApproval`. It may enrol and be provisioned and tested, but `enrolDevice` refuses `active` until `approveDevice` approves it (`409 device-approval-required`). A separate axis from `enrolmentState`, which keeps its r1 values; the model is `states/registered-device-approval.yaml`.\n"},"enrolmentCode":{"type":"string","nullable":true,"readOnly":true,"maxLength":12,"description":"**A one-time code the device must present to enrol** (DEC-241; CHG-CSP-011). Issued by `registerDevice` and returned once, in its response only; every later read returns null. The installer enters it on the device, and `enrolDevice` to `enrolled` must carry the same code before `enrolmentCodeExpiresAt` (`422 enrolment-code-invalid`). A device that never presents it never gets an identity, so a box plugged into the venue network cannot claim to be a reader.\n"},"enrolmentCodeExpiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the enrolment code stops working (24 hours after registration, proposed; client to correct)."},"testedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who recorded the device's acceptance test (`DeviceEnrolment.testResult` on the move to `provisioned`). The approver must be someone else (DEC-245).\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who approved the device into production, never the person who tested it** (decided 2 October 2026, Chinmay, critical set 1, BO-203: \"Approver must differ from the tester\"; DEC-245; CHG-CSP-011). `approveDevice` refuses the tester with `403 approver-is-tester`.\n"},"approvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"ReportingAnswerReliability": {"type":"string","description":"**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},
"ReportingSemanticQuerySpec": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n","required":["metric","period"],"properties":{"metric":{"type":"string","description":"A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."},"dimensions":{"type":"array","maxItems":5,"description":"Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.","items":{"type":"string"}},"filters":{"type":"array","items":{"type":"object","required":["field","operator"],"properties":{"field":{"type":"string","description":"A `SemanticModel` field code."},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","isNull","isNotNull"]},"values":{"type":"array","description":"**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n","items":{}}}}},"period":{"type":"string","description":"ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."},"comparison":{"type":"string","nullable":true,"description":"As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.","enum":["previousPeriod","samePeriodLastYear","target","benchmark"]},"semanticModelVersion":{"type":"integer","readOnly":true,"description":"The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."}}},
"ReportingUnavailableReason": {"type":"string","description":"Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.","enum":["metricNotModelled","dimensionNotModelled","filterNotModelled","comparisonNotAvailable","periodOutsideHistory"]},
"RoleSummary": {"x-ticvai-persistence":"none — projection over role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"isPrimary":{"type":"boolean"}}},
"RunReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","properties":{"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"},"venueId":{"type":"string","format":"uuid","description":"Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"},"dateFrom":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."},"dateTo":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (audit R158)."},"forceAsync":{"type":"boolean","default":false,"description":"Queue regardless of size, for a result to be collected later."}}},
"Segment": {"x-ticvai-persistence":"marketing.segment + marketing.segment_criterion","allOf":[{"$ref":"#/components/schemas/CreateSegmentRequest"},{"type":"object","required":["id","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"lastEvaluatedSize":{"type":"integer","nullable":true},"lastEvaluatedAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"}}}]},
"SegmentCriterion": {"x-ticvai-persistence":"marketing.segment_criterion","type":"object","required":["attribute","operator"],"properties":{"attribute":{"type":"string","description":"Behavioural or profile attribute — visit count, last visit, lifetime value, product purchased, membership tier, venue visited, language.\n**Free-form rather than an enum, which is why 22.14.8, 5.3.19 and 5.5.17b were readable as gaps and are not.** `walletBalance`, `engagementTier` and `portfolioScope` are expressible today; what was missing was anybody saying so.\n**Three that need saying, because the naive reading is wrong:**\n`walletBalance` should segment on **`cash` credit only**. A guest with 200 dirhams of promotional credit expiring Friday is a different campaign from one with 200 of their own money, and treating them alike sends a spend-it-now message to somebody who was given it.\n`walletBalance.expiringWithinDays` is the segment that earns the attribute — **credit about to expire unspent is a guest about to be disappointed and a venue about to book breakage**, and only one of those is worth a message.\n`portfolioScope` aggregates across a `DelegatedAccess` delegation (CF-132) and **must not message every member about a household total** — that is how a venue tells a teenager what their parent spends.\n`entitlementExpiringWithinDays` (29 September, build pass, group G2; 5.5.30): the guest holds a ticket or pass in `issued` or `partiallyConsumed` whose `validTo` is within that many days, kept current from `entitlement.expiringSoon` and the entitlement read model. **Unused passes about to lapse** are this attribute with `entitlementRemainingUses` greater than zero.\n"},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","exists","notExists","withinDays"]},"value":{},"values":{"type":"array","items":{}}}},
"SegmentPreview": {"x-ticvai-persistence":"none — evaluated live","type":"object","required":["segmentId","matchingCount","reachable"],"properties":{"segmentId":{"type":"string","format":"uuid"},"matchingCount":{"type":"integer"},"reachable":{"type":"array","description":"Per channel, after consent and suppression. A segment of 50,000 with 3,000 email consents is a 3,000-person campaign.\n","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/MessageChannel"},"reachableCount":{"type":"integer"},"excludedNoConsent":{"type":"integer"},"excludedSuppressed":{"type":"integer"},"excludedNoAddress":{"type":"integer"}}}},"evaluatedAt":{"type":"string","format":"date-time"}}},
"SegmentRuleGroup": {"x-ticvai-persistence":"none — stored with the segment as jsonb","type":"object","description":"One group of a segment's nested rules (CHG-CSA-045). `operator` combines the group's `criteria` and its child `groups`; `not` negates the group (it takes one child, criteria or group).","properties":{"operator":{"type":"string","enum":["and","or","not"]},"criteria":{"type":"array","description":"Each entry has the shape of `SegmentCriterion` (`attribute`, `operator`, `value`). Typed loosely here so the new optional field adds no required member to `createSegment`'s body for clients built at r1; the server validates each entry as a `SegmentCriterion` (400 otherwise).","items":{"type":"object","additionalProperties":true}},"groups":{"type":"array","items":{"$ref":"#/components/schemas/SegmentRuleGroup"}}}},
"StockBatch": {"type":"object","x-ticvai-persistence":"inventory.stock_batch","description":"BL-122. **`isPerishable` and `shelfLifeDays` are on the item, so a shelf life is declared and never instantiated.** Two deliveries of the same milk arriving a week apart are one stock level with one implied expiry, and the older one is invisible.\n**A batch is the instance that actually expires.** Without it, first-expiry-first-out is not computable and a venue discovers the problem by smell.\n","required":["id","itemId","locationId","quantity","receivedAt"],"properties":{"id":{"type":"string","format":"uuid"},"itemId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"batchCode":{"type":"string","nullable":true},"lotNumber":{"type":"string","nullable":true,"description":"The supplier's own reference. **A recall names a lot number**, and an inventory that cannot resolve one has to discard everything.\n"},"quantity":{"type":"number"},"receivedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date","nullable":true},"supplierId":{"type":"string","format":"uuid","nullable":true},"status":{"type":"string","enum":["available","quarantined","expired","recalled","consumed","written-off"]}}},
"StockValuation": {"x-ticvai-persistence":"none — computed","type":"object","required":["asAt","total","byLocation"],"properties":{"asAt":{"type":"string","format":"date"},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"byLocation":{"type":"array","items":{"type":"object","properties":{"locationId":{"type":"string","format":"uuid"},"locationName":{"type":"string"},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"itemCount":{"type":"integer"}}}},"byCategory":{"type":"array","items":{"type":"object","properties":{"categoryId":{"type":"string","format":"uuid"},"categoryName":{"type":"string"},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"Suggestion": {"type":"object","x-ticvai-persistence":"ai.suggestion","description":"One answer to one question, with its reasoning and its confidence. **Built 24 August so that machine learning can be swapped in without touching a screen.**\n**A suggestion is never an action.** It proposes; `ProposedAction` and its approval path decide. A model that can order stock is a model that will order stock wrongly at three in the morning.\n**`inputs` is recorded, not just referenced.** A suggestion that cannot be reproduced cannot be defended to a finance controller asking why the system said to order four hundred.\n","required":["id","kind","basis","maturity","producedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SuggestionKind"},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"scopePath":{"type":"string"},"subjectRef":{"type":"string","nullable":true,"description":"What it is about — a product, an outlet, an item, a party."},"value":{"type":"object","additionalProperties":true,"description":"The suggestion itself. Shape depends on `kind`."},"confidence":{"type":"number","nullable":true,"minimum":0,"maximum":1,"description":"**Null for a heuristic and that is honest.** A rule has no confidence — dressing one up with 0.85 is the fastest way to make a manager trust a number that means nothing.\n"},"explanation":{"type":"string","description":"**Plain words, always present, whatever the basis.** *Because covers are up 12% on this day last year* — a suggestion a manager cannot explain to their own boss is a suggestion they will not action.\n"},"inputs":{"type":"object","additionalProperties":true,"description":"What went in. **Recorded so the answer can be reproduced** — and so that when a model replaces the rule, the two can be run against the same inputs and compared.\n"},"producerRef":{"type":"string","description":"The rule name or the model id and version. **A model version is part of the record**: *the model said so* is not an answer to *which model, when*.\n"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**A demand forecast for Saturday is worthless on Sunday.** An expired suggestion is hidden rather than shown stale.\n"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]},
"SuggestionOutcome": {"type":"object","x-ticvai-persistence":"ai.suggestion_outcome","description":"**What actually happened, and this is the table that makes the swap possible at all.**\nA model needs labelled data and **the only source of labels is whether the venue took the advice and whether it worked.** A platform that suggests and never records the outcome has no training set a year later, and the swap he is planning for never happens.\n**Captured whether or not the suggestion was taken.** A rejected suggestion is a stronger signal than an accepted one — it is the case the rule got wrong.\n","required":["id","suggestionId","decision"],"properties":{"id":{"type":"string","format":"uuid"},"suggestionId":{"type":"string","format":"uuid"},"decision":{"type":"string","enum":["accepted","modified","rejected","ignored","expired"]},"actualValue":{"type":"object","nullable":true,"additionalProperties":true,"description":"What the venue did instead. **The label.** A suggestion of 400 units, an order of 250, and a stockout on Saturday is one training example worth more than a hundred accepted ones.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decidedAt":{"type":"string","format":"date-time"},"realisedOutcome":{"type":"object","nullable":true,"additionalProperties":true,"description":"**Filled in later by a job, not by a person.** Whether the stockout happened, whether the covers arrived, whether the margin held — nobody comes back to record this by hand, so nothing that depends on them doing so should be designed.\n"},"note":{"type":"string","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.suggestion_outcome` had no scope column and no declared owner, so no policy. The suggestion's scope, copied when the outcome is recorded.\n"}}}
}
```
