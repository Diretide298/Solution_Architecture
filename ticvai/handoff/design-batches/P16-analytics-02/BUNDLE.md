# P16-analytics-02 — P16 · Analytics (2 of 2)

**2 screens · 11 operations · 20 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `AI_CONFIGURE, AI_USE, LEDGER_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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
| `ANL-071` | AI Maturity & Learning | D | 20 | 42 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ANL-072` | Finance Dashboard | C | 4 | 97 | 6 | 7 | 0 | 0 | — | notStarted (—) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ANL-071` AI Maturity & Learning

**See where each AI answer stands, what it is based on and what it needs next; set the venue AI profile; import the venue's own history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `ai` module |
| Block | Block D · task APP-ANALYTICS-ANL-071 |
| Who uses it | venue staff holding `AI_CONFIGURE`, `AI_USE` (1 configure, 1 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAiCapabilityMaturity` reads a population (one row per question the AI answers) and the detail is the row |
| Offline | online only |
| Opens with | `venueId` (session), `importId` (deepLink) · cold entry: A link from an import-finished notification opens the import named by `importId`; without it the page opens on the maturity list. |
| Route | `/analytics/ai-maturity` |

**What the spec says about it.** **Added 29 September (AI functions review, the product owner's "build it right, it gets more accurate with time").** No customer is told an AI feature "comes later": every answer starts from a baseline and learns. This is where the venue sees how far each answer has come, gives the figures the baseline stands on, and imports its own history from the systems it used before TICVAI. Importing 12 months or more moves the answers it covers straight to Established.

**From the AI & Intelligence process.** The AI maturity page: for every question the venue's AI answers, where it stands (Starting, Learning, Established, Trained on your data), what it is based on, how much is the venue's own data and what the next stage needs; the venue AI profile the baselines stand on; and the import of the venue's own history from before TICVAI. The one thing to get right: this is where the customer sees "Learning your venue" instead of "comes later" - each row is honest about its basis, and nothing here changes an answer already given.

**Known correction pending (do not draw the wrong version)**

- **The maturity block is on Suggestion and AiForecastVersion, but AiOperationalRequirement, AiRecommendationResult and transaction risk answers do not carry it.** Why: ADR-0051 says every answer carries maturity; requirements, recommendations and risk scores need it (or a reference to the row here) for the shared component. *(source: ADR-0051 / contracts/satellite/ai.yaml#/components/schemas/AiOperationalRequirement / contracts/satellite/ai.yaml#/components/schemas/AiRecommendationResult; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Stage | multi select | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Stage | radio group | — | Starting · Learning · Established · Learned | `listAiCapabilityMaturity` ?stage |
| Capability key | text field | — | — | `listAiCapabilityMaturity` ?capabilityKey |

**Form: Save venue AI profile** (modal, opened by *Save venue AI profile*; *Save venue AI profile* calls `setAiVenueSettings`, *Cancel* sends nothing)

**Collects what `setAiVenueSettings` sends before it is called.** Required: `venueId`, `venueType`. Any figure left empty takes the starting pattern's default for the venue type.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setAiVenueSettings` body |
| Venue type `venueType` | select | required | — | Water park · Theme park · Family entertainment centre · Museum · Arena · Zoo aquarium · Other | — | — | `setAiVenueSettings` body |
| Is outdoor `isOutdoor` | toggle | optional | on | — | — | Outdoor venues take the summer-heat and weather effects. | `setAiVenueSettings` body |
| Capacity `capacity` | number field | optional | — | min 1 | — | — | `setAiVenueSettings` body |
| Opening hours `openingHours` | repeatable rows | optional | — | — | — | The usual week. Exceptions come from the venue calendar. | `setAiVenueSettings` body |
| Day of week `openingHours[].dayOfWeek` | stepper or slider | optional | — | min 1; max 7 | — | — | `setAiVenueSettings` body |
| Opens at `openingHours[].opensAt` | text field | optional | — | — | — | — | `setAiVenueSettings` body |
| Closes at `openingHours[].closesAt` | text field | optional | — | — | — | — | `setAiVenueSettings` body |
| Typical weekday attendance `typicalWeekdayAttendance` | number field | optional | — | min 0 | — | — | `setAiVenueSettings` body |
| Typical weekend attendance `typicalWeekendAttendance` | number field | optional | — | min 0 | — | — | `setAiVenueSettings` body |
| Peak months `peakMonths` | list of values (chips) | optional | — | — | — | — | `setAiVenueSettings` body |
| Average spend `averageSpend` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setAiVenueSettings` body |
| Fnb attach rate `fnbAttachRate` | stepper or slider (%) | optional | — | min 0; max 1 | — | — | `setAiVenueSettings` body |
| Staff productivity `staffProductivity` | key and value settings | optional | — | — | — | Per role, units per staff hour, e.g. `{"cashier": 40, "gate": 300}`. | `setAiVenueSettings` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Import history** (modal, opened by *Import history*; *Import history* calls `importVenueHistory`, *Cancel* sends nothing)

**Collects what `importVenueHistory` sends before it is called.** Required: `dataKind`, `assetId` (the uploaded export), `columnMapping`. Optional: `sourceSystem`, `dryRun` (check without loading). A second import of the same kind and period replaces the first.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Data kind `dataKind` | select | required | — | Attendance · Admissions · Ticket sales · Fnb sales · Retail sales · Queue readings · Staff shifts | — | — | `importVenueHistory` body |
| Asset `assetId` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | The uploaded export, in the asset library. | `importVenueHistory` body |
| Source system `sourceSystem` | text field | optional | — | — | — | What produced the file, e.g. the previous POS's name. | `importVenueHistory` body |
| Column mapping `columnMapping` | key and value settings | required | — | — | — | Target field to source column, e.g. `{"date": "Txn Date", "value": "Net Sales", "product": "Item"}`. | `importVenueHistory` body |
| Dry run `dryRun` | toggle | optional | off | — | — | Validate and report without loading. | `importVenueHistory` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 An import of this venue and kind is already running (`history-import-in-progress`).; 422 The mapping names no date or no measure column, or the asset is not a CSV or spreadsheet (`history-mapping-invalid`).

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **venue AI profile**: Venue type (water park, theme park, family entertainment centre, museum, arena, zoo or aquarium, other), outdoor, capacity, opening hours, typical weekday and weekend attendance, peak months, average spend, F&B attach rate, staff productivity per role. Each empty field shows the starting pattern's default in grey ("Water-park default: 35%"). Saving takes effect at the next nightly re-estimate. *(source: contracts/satellite/ai.yaml#setAiVenueSettings / ADR-0051)*
- **history import**: Data kind (attendance, admissions, ticket sales, F&B sales, retail sales, queue readings, staff shifts), the uploaded export, source system, column mapping (date, measure, dimensions) with a preview of the first rows, and Dry run first (default on). States "Used for AI only - never posted to your ledger". *(source: contracts/satellite/ai.yaml#importVenueHistory / ADR-0051)*

#### Outputs: what the screen shows and produces

**Shown**

**Every AI answer, by stage** (data table, from `listAiCapabilityMaturity`): Stage badge, the "Based on" line, the share of own data and what the next stage needs.

| Shows | Format | Notes |
|---|---|---|
| Capability key | text | — |
| Suggestion kind | chip: Price, Replenishment, Requisition, Demand forecast, Prep plan, Menu engineering… | What is being suggested. A closed set, and the reason it is closed is the swap. |
| Forecast definition key | text | — |
| Stage | chip: Starting, Learning, Established, Learned | — |
| Maturity | grouped details | Where an answer stands, on every answer (29 September, AI functions review; baseline then learn). |
| Since | 1 Oct 2026, 14:30 | — |

**Venue AI profile** (detail panel, from `getAiVenueSettings`): **The venue can correct its profile at any time** — the honest answer to a baseline that is wrong for an unusual venue in the first weeks.

| Shows | Format | Notes |
|---|---|---|
| Venue type | chip: Water park, Theme park, Family entertainment centre, Museum, Arena, Zoo aquarium… | — |
| Capacity | 1,234 | — |
| Opening hours | list or chips (count when long) | The usual week. Exceptions come from the venue calendar. |
| Typical weekday attendance | 1,234 | — |
| Typical weekend attendance | 1,234 | — |
| Peak months | list or chips (count when long) | — |
| Average spend | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Fnb attach rate | 12.5% | — |
| Staff productivity | grouped details | Per role, units per staff hour, e.g. `{"cashier": 40, "gate": 300}`. |

**History imports** (data table, from `listVenueHistoryImports`)

| Shows | Format | Notes |
|---|---|---|
| Data kind | chip: Attendance, Admissions, Ticket sales, Fnb sales, Retail sales, Queue readings… | — |
| Status | chip: Queued, Validating, Loading, Completed, Completed with rejections, Failed | — |
| Period from | 1 Oct 2026 | — |
| Period to | 1 Oct 2026 | — |
| Months covered | 1,234 | — |
| Rows loaded | 1,234 | — |
| Rows rejected | 1,234 | — |

**Import findings** (detail panel, from `getVenueHistoryImport`): Each rejected row and why, so the venue can fix the export and import again.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Data kind | chip: Attendance, Admissions, Ticket sales, Fnb sales, Retail sales, Queue readings… | — |
| Asset | the image or video | — |
| Source system | text | — |
| Column mapping | grouped details | — |
| Dry run | yes / no (icon or chip) | — |
| Status | chip: Queued, Validating, Loading, Completed, Completed with rejections, Failed | — |
| Period from | 1 Oct 2026 | — |
| Period to | 1 Oct 2026 | — |
| Months covered | 1,234 | — |
| Rows read | 1,234 | — |
| Rows loaded | 1,234 | — |
| Rows rejected | 1,234 | — |
| Findings | list or chips (count when long) | — |
| Row | 1,234 | — |
| Code | chip: Bad date, Bad number, Negative value, Duplicate day, Unmapped column, Out of range | — |
| Detail | text | — |
| Requested by principal | the name it points at, never the id | — |
| Completed at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save venue AI profile (primary button) | `setAiVenueSettings` PUT `/venues/{venueId}/ai-settings` | AiVenueSettings | AiVenueSettings | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Import history (secondary button) | `importVenueHistory` POST `/venues/{venueId}/history-imports` | inline | AiHistoryImport | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 An import of this venue and kind is already running (`history-import-in-progress`).; 422 The mapping names no … | opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **maturity rows**: Question (e.g. "Attendance forecast", "Replenishment suggestions", "Checkout recommendations", "Fraud scoring"), stage badge, Based on, own-data share as a bar, next stage needs ("8 more Saturdays of sales", "an admin promotion"), since. *(source: contracts/satellite/ai.yaml#listAiCapabilityMaturity / contracts/satellite/ai.yaml#/components/schemas/AiMaturity)*
- **import result**: Rows read, loaded, rejected, months covered; findings with their row (bad date, negative quantity, duplicate day). 12 months or more says "Answers covered by this import move to Established". *(source: contracts/satellite/ai.yaml#getVenueHistoryImport / ADR-0051)*

**Data it reads**: `listAiCapabilityMaturity` (onLoad, Where each answer stands); `getAiVenueSettings` (onLoad, The venue AI profile); `listVenueHistoryImports` (onLoad, Past imports and their result)

**Where the user goes next**

- → `ANL-010` Suggestions & Advice: *Suggestions & Advice*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The stage of each answer; the venue profile resolves separately. |
| Error (`?state=error`) | Could not load. **Every AI answer still works** — this page reports on them and changes none. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing answered yet.** Every question starts at Starting from the venue AI profile and the starting pattern for the venue type. The action fills in the profile, or imports history. |
| Empty, no results (`?state=emptyNoResults`) | No answer is at this stage. Names the filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | You do not have AI permission at this venue. Names `AI_USE`, and `AI_CONFIGURE` for the profile and imports. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 An import of this venue and kind is already running (`history-import-in-progress`).; 422 The mapping names no date or no measure column, or the asset is not a CSV or spreadsheet (`history-mapping-invalid`). |

#### Edge cases to draw

- **A learned model is ready to promote**: Row shows "Ready to promote - your administrator decides"; no promote button here. *(source: ADR-0051 / contracts/satellite/ai.yaml#promoteAiRelease)*
- **Second import of an overlapping period**: 409 explained as overlapping months, with the earlier import named. *(source: contracts/satellite/ai.yaml#importVenueHistory (409))*

#### Consistency with other screens

- Match `ADM-554`: Same stages; promotion controls live there.
- Match `ADM-471`: The configuration assistant collects the same venue profile during onboarding.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profile:
  venueType: waterPark
  outdoor: true
  capacity: 6000
  weekday: 1800
  weekend: 3200
  peakMonths:
  - 11
  - 12
  - 1
  - 2
  - 3
  - 4
  averageSpend: AED 145.00
  fnbAttach: 62%
  productivity:
    cashier: 40 transactions/h
    gate: 300 scans/h
rows:
- question: Daily attendance forecast
  stage: Learning
  basedOn: venue profile, UAE calendar, weather, 6 weeks of your sales
  ownData: 41%
  next: about 6 more weeks for Established
  limited: true
- question: Checkout recommendations
  stage: Starting
  basedOn: your product relationships and business priorities
  next: take-up rates from 4 weeks of offers
import:
  kind: ticketSales
  sourceSystem: Previous ticketing system export
  months: 18
  loaded: 41230
  rejected: 37
```

#### Permissions

- `listAiCapabilityMaturity` → `AI_USE` (operate) · staff
- `getAiVenueSettings` → `AI_USE` (operate) · staff
- `setAiVenueSettings` → `AI_CONFIGURE` (configure) · staff
- `listVenueHistoryImports` → `AI_USE` (operate) · staff
- `getVenueHistoryImport` → `AI_USE` (operate) · staff
- `importVenueHistory` → `AI_CONFIGURE` (configure) · staff

**A refused user sees:** You do not have AI permission at this venue. Names `AI_USE`, and `AI_CONFIGURE` for the profile and imports.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-071` · status **notStarted** · provenance generated
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (42 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-071?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save venue AI profile, Import history.
- [ ] Every transition is wired: `ANL-010`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-072` Finance Dashboard

**The finance team's one-glance position for one legal entity and one period: the six finance measures as separate tiles, where the money stands, and the health of tax documents.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `core` module |
| Block | Block C · task APP-ANALYTICS-ANL-072 |
| Who uses it | venue staff holding `LEDGER_VIEW`, `REPORT_VIEW_VENUE` (1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the Finance standard dashboard of the reporting area (DI-721): seeded finance measures over a period, not a population the screen lists |
| Offline | online only |
| Opens with | `legalEntityId` (navigation) · cold entry: Resolves the legal entity from the caller's scope when none is passed; the Orders & Money link card (P08) opens it with the venue's legal entity. |
| Route | `/analytics/finance-dashboard-anl-072` |

**What the spec says about it.** **Issued 2 October 2026 (CHG-SOT-008, DEC-219).** The Finance standard dashboard of the one reporting area (DI-721), carrying DI-260's content from BO-1081, which becomes a link card on Orders & Money (P08, the back-office agent's change). The design notes of BO-1081 (finance-insights) apply here in full: tile order, definitions, the money-position sentence, tax-document counts and freshness. **Measure names, not "Revenue"** (CHG-FIN-002): Gross sales, Net revenue, Recognised revenue and Deferred revenue never share a label, and the tiles never bind `takings`. **One reporting area, one set of numbers** (CHG-FIN-006): this screen reads the same seeded KPIs as the till report (POS-008) and the back-office reports for the same scope, period and as-of time, computes no total of its own and shows the as-of time on every figure. **The guard is the frontend comparison test TEST-SAME-NUMBERS** (decided 2 October 2026, DEC-559; `docs/active/block-a-extra-tasks.json`), which compares takings, gross sales, net revenue and refunds here with POS-008 and the back office for the same period and scope, and fails when they differ.

**Known gaps.** **No service-fee measure is seeded.** DEC-217 shows fees as their own line under Gross sales with a footnote; `ReportingSystemKpi` has no fee code yet, so the line is drawn "Definition pending" until …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Legal entity | select field | — | — | — | — | Required, first in the filter bar. It fixes the base currency, shown read-only beside it, never offered as a choice (DI-211, DI-282). | — |
| Venue | select field | — | — | — | — | Sends the scope as `scopePath`. Lists only the venues the signed-in user may see; a venue manager arrives locked to their venue (DI-061, DI-248). | — |
| Product category | select field | — | — | — | — | The pack's "Attraction" filter is a product category under the venue, not a scope node (decided 2 October 2026, DEC-218). | — |
| Period | date picker | — | — | — | — | Sends `period`. Month by default; day, week, month, quarter, fiscal year and a custom range (DI-260, DI-263). | — |

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
| From | date picker | — | — | `getUnifiedReconciliation` ?from |
| To | date picker | — | — | `getUnifiedReconciliation` ?to |
| Order | picker: choose an order | — | — | `listTaxInvoices` ?orderId |
| Legal entity | picker: choose a legal entity | — | — | `listTaxInvoices` ?legalEntityId |
| Invoice type | segmented control | — | Simplified · Full · Consolidated | `listTaxInvoices` ?invoiceType |
| Status | radio group | — | Issued · Partially credited · Fully credited · Superseded | `listTaxInvoices` ?status |
| Issued from | date picker | — | — | `listTaxInvoices` ?issuedFrom |
| Issued to | date picker | — | — | `listTaxInvoices` ?issuedTo |
| … 8 more | | | | `operations.json` |

#### Outputs: what the screen shows and produces

**Shown**

**Gross sales** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=grossSales` for the chosen legal entity, venue and period, with its as-of time; formula in `ReportingSystemKpi` (D-185 default, client finance sign-off pending; CHG-FIN-007). Excluding VAT; service fees are not inside it and are footnoted as their own line (decided 2 October 2026, DEC-217).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Discounts** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=discounts` for the chosen legal entity, venue and period, with its as-of time; formula in `ReportingSystemKpi` (D-185 default, client finance sign-off pending; CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Refunds** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=refunds` for the chosen legal entity, venue and period, with its as-of time; formula in `ReportingSystemKpi` (D-185 default, client finance sign-off pending; CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Net revenue** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=netRevenue` for the chosen legal entity, venue and period, with its as-of time; formula in `ReportingSystemKpi` (D-185 default, client finance sign-off pending; CHG-FIN-007). Gross sales less discounts and refunds.

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Recognised revenue** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=recognisedRevenue` for the chosen legal entity, venue and period, with its as-of time; formula in `ReportingSystemKpi` (D-185 default, client finance sign-off pending; CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Deferred revenue** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=deferredRevenue` for the chosen legal entity, venue and period, with its as-of time; formula in `ReportingSystemKpi` (D-185 default, client finance sign-off pending; CHG-FIN-007). The balance at period end.

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**VAT collected** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=taxCollected` for the chosen legal entity, venue and period, with its as-of time; formula in `ReportingSystemKpi` (D-185 default, client finance sign-off pending; CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Gross sales to net revenue** (chart, from `getKpiValues`): The `waterfall` mark (CHG-FIN-007): Gross sales, minus Discounts, minus Refunds, equals Net revenue, from the same seeded KPIs as the tiles. Never gross and net stacked in one bar.

| Shows | Format | Notes |
|---|---|---|
| Kpi | the name it points at, never the id | — |
| Code | text | — |
| Bucket start | 1 Oct 2026, 14:30 | The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise. |
| Group key | text | The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked. |
| Name | text | — |
| Period | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Target | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Variance percent | 1,234.5 | — |
| Direction | chip: Up, Down, Flat | — |
| Status | chip: Green, Amber, Red, No target | — |
| As of | 1 Oct 2026, 14:30 | — |
| Stale | yes / no (icon or chip) | True when the pipeline behind it has not refreshed. A number nobody flagged as stale is a number somebody will act on. |

**Where the money stands** (detail panel, from `getUnifiedReconciliation`): POS, gateway, bank, wallet and ledger, each with its total and count, then each variance naming the two sources that disagree ("Gateway vs Ledger, short AED 500.00"). Shown as "Not available with your access" without ledger access, never as zeros.

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| To | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| Sources | list or chips (count when long) | — |
| Variances | list or chips (count when long) | Where two sources disagree, named. A discrepancy is usually the gap between two of them rather than inside one, and *"out by 240"* without … |

**Tax invoices issued** (metric tile, from `listTaxInvoices`): Count for the legal entity and period.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Invoice number | text | Server-assigned from the legal entity's series for the document kind, in sequence and without gaps, e.g. |
| Invoice type | chip: Simplified, Full, Consolidated | 5.7.93. `simplified` for one order with no recipient details, `full` for one order with them, `consolidated` for several paid orders of one … |
| Status | chip: Issued, Partially credited, Fully credited, Superseded | `issued` until a credit memo is issued against it; `superseded` where a full invoice replaced a simplified one for the same supply (only if … |
| Legal entity | the name it points at, never the id | — |
| Template | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Orders | list or chips (count when long) | — |
| Supplier name | text | — |
| Supplier address | text | — |
| Supplier tax registration number | text | — |
| Buyer subject | the name it points at, never the id | The guest the orders belong to; the key a guest's own reads filter on. |
| Buyer name | text | — |
| Buyer address | text | — |
| Buyer country code | text | — |
| Buyer tax registration number | text | — |
| Customer account | the name it points at, never the id | — |
| Issued at | 1 Oct 2026, 14:30 | — |
| Supply date | 1 Oct 2026 | The date of supply where it differs from the issue date (the latest order's payment date on a consolidated invoice). |

**Credit memos** (metric tile, from `listCreditMemos`): Count and value for the legal entity and period. "Credit memo", not "Tax credit note", until the label is decided.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Credit memo number | text | Server-assigned from the legal entity's credit memo series, in sequence without gaps. |
| Tax invoice | the name it points at, never the id | — |
| Tax invoice number | text | — |
| Kind | chip: Full, Partial | — |
| Reason | chip: Refund, Cancellation, Price adjustment, Return of goods, Billing error, Other | — |
| Refund | the name it points at, never the id | — |
| Cancelled order | the name it points at, never the id | — |
| Legal entity | the name it points at, never the id | — |
| Buyer subject | the name it points at, never the id | — |
| Issued at | 1 Oct 2026, 14:30 | — |
| Currency | text | — |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount in legal currency | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Legal FX rate | text | The invoice's own `legalFxRate`, never today's (CHG-FIN-011). |
| Invoice supply value | AED 1,234.50 | The value of the supply shown on the tax invoice (Executive Regulation Art. 60(1)(e)), adjusted by any earlier credit note on the same … |
| Corrected supply value | AED 1,234.50 | The correct value of the supply after this credit note (Art. 60(1)(e)). |

**E-invoice transmissions failed** (metric tile, from `listEInvoiceTransmissions`): `status=failed`; red above zero and links to the transmission log.

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Document kind | chip: Tax invoice, Credit memo | — |
| Document | the name it points at, never the id | — |
| Document number | text | — |
| Legal entity | the name it points at, never the id | — |
| Provider | the name it points at, never the id | — |
| Mode | chip: Test, Live | — |
| Status | chip: Not required, Queued, Sent, Accepted, Rejected, Failed | 6.1.1. `notRequired` where the legal entity's provider is `disabled` or absent. |
| Payload hash | text | SHA-256 of the document as sent, so a resend can be shown to be the same document. |
| Provider message | text | — |
| Attempt | 1,234 | — |
| Error codes | list or chips (count when long) | — |
| Error message | text | — |
| Sent at | 1 Oct 2026, 14:30 | — |
| Answered at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Data it reads**: `getKpiValues` (onLoad, The finance measures, with their as-of time); `getUnifiedReconciliation` (onLoad, Where the money stands); `listTaxInvoices` (onLoad, Tax invoices issued in the period); `listCreditMemos` (onLoad, Credit memos issued in the period); `listEInvoiceTransmissions` (onLoad, E-invoicing transmission failures)

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The finance measures for the chosen legal entity and period. |
| Error (`?state=error`) | Could not load. Names which read failed (the measures, the money position or the tax documents) and leaves the others on screen. |
| Empty, first run (`?state=emptyFirstRun`) | No postings for this period yet. Offers no create action: a dashboard has nothing to create; it says which period is empty and offers the previous one. |
| Empty, no results (`?state=emptyNoResults`) | The venue or product category filter matched no sales in the period. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `LEDGER_VIEW`, which the money position and tax documents require, and names that permission. **Never an empty table** — that reads as *there is no data*. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `getUnifiedReconciliation` → `LEDGER_VIEW` (read) · staff
- `listTaxInvoices` → `LEDGER_VIEW` (read) · staff, guest
- `listCreditMemos` → `LEDGER_VIEW` (read) · staff, guest
- `listEInvoiceTransmissions` → `LEDGER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `LEDGER_VIEW`, which the money position and tax documents require, and names that permission. **Never an empty table** — that reads as *there is no data*.

Screen guard: `LEDGER_VIEW`

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.2.19 | The system shall automatically reconcile transactions between POS, online sales, payment gateways, banks, wallets, loyalty systems, and financial records while identifying discrepancies. | Bundles and Promotions | CONTRACTED | data `UnifiedReconciliation` |
| 5.7.9 | The system should provide full visibility of all codes as well as an easy and automated way to reconcile credit card payments (VPOS, POS) versus ticketing payments. | F&B & Guest Management | CONTRACTED | data `UnifiedReconciliation` |
| 5.7.21 | The system should be able to push cash, credit card and voucher payments to the Bulk Reconciliation system. | F&B & Guest Management | CONTRACTED | data `UnifiedReconciliation` |
| 5.7.90 | The system shall support reconciliation between bank statements, payment gateways, POS transactions, ticketing transactions, wallets, and ERP transactions. Support automatic matching, manual … | F&B & Guest Management | CONTRACTED | data `UnifiedReconciliation` |
| 6.1.7 | The system should be able to report supporting nightly balancing: 1.Tender balancing with export in batch file. 2.Handling consecutive days of open transactions / exceptions report. | Retail POS | CONTRACTED | data `UnifiedReconciliation` |
| 6.1.33 | The system should be able to report the full reconciliations with Payment gateway, refund, used, liability etc. | Retail POS | CONTRACTED | data `UnifiedReconciliation` |
| 6.1.41 | The system should be able to report on daily, weekly and monthly reconciliation reports between (Finance(ERP) reported , Ticketing engine and other integrated systems). | Retail POS | CONTRACTED | data `UnifiedReconciliation` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-072` · status **notStarted** · provenance — · The client's workshop frame for this dashboard is the one drawn for BO-1081 (the same pack, board 1, number 1), whose content ANL-072 carries since DEC-219 (CHG-SOT-008; CHG-GTB-006).
- Client workshop board: `wireframes/WS163 TICVAI Finance Backend Structure Reference v1.0 Board 1.dc.html#bo-1081`
- Workshop pack: TICVAI Finance Backend Structure Reference v1.0.pdf board 1
- Flow F303 *TICVAI Finance Backend Structure Reference v1.0 board 1: Finance Dashboard*, step 2: Works in Finance Dashboard → The finance team's one-glance position for one legal entity and one period: the six finance measures as separate tiles, where the money stands, and the health of tax documents.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (97 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-072?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `LEDGER_VIEW`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
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

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getAiVenueSettings": {"method":"GET","path":"/venues/{venueId}/ai-settings","contract":"ai","summary":"The venue AI profile the baselines stand on","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiVenueSettings"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null},{"name":"module","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getUnifiedReconciliation": {"method":"GET","path":"/reconciliation/unified","contract":"finance","summary":"Every money source against the ledger, in one view","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true}],"requestBody":null,"responds":"UnifiedReconciliation"},
"getVenueHistoryImport": {"method":"GET","path":"/history-imports/{importId}","contract":"ai","summary":"One history import, with its findings","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiHistoryImport"},
"importVenueHistory": {"method":"POST","path":"/venues/{venueId}/history-imports","contract":"ai","summary":"Import the venue's own historical exports for the AI baselines","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listAiCapabilityMaturity": {"method":"GET","path":"/capability-maturity","contract":"ai","summary":"Where each AI answer stands on the way from baseline to learned","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"stage","in":"query","required":null},{"name":"capabilityKey","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCreditMemos": {"method":"GET","path":"/credit-memos","contract":"finance","summary":"Credit memos issued, newest first","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"taxInvoiceId","in":"query","required":null},{"name":"refundId","in":"query","required":null},{"name":"legalEntityId","in":"query","required":null},{"name":"issuedFrom","in":"query","required":null},{"name":"issuedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listEInvoiceTransmissions": {"method":"GET","path":"/e-invoicing/transmissions","contract":"finance","summary":"What was sent to the e-invoicing provider, and what came back","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"legalEntityId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"documentId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTaxInvoices": {"method":"GET","path":"/tax-invoices","contract":"finance","summary":"Tax invoices issued, newest first","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"orderId","in":"query","required":null},{"name":"legalEntityId","in":"query","required":null},{"name":"invoiceType","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"issuedFrom","in":"query","required":null},{"name":"issuedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVenueHistoryImports": {"method":"GET","path":"/venues/{venueId}/history-imports","contract":"ai","summary":"The venue's history imports","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setAiVenueSettings": {"method":"PUT","path":"/venues/{venueId}/ai-settings","contract":"ai","summary":"Set the venue AI profile","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiVenueSettings","responds":"AiVenueSettings"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiCapabilityMaturity": {"type":"object","x-ticvai-persistence":"ai.capability_maturity","description":"**The stage of each question the venue's AI answers** (29 September, AI functions review). Written by the nightly re-estimate; a stage change is a new row, so the page can show when each answer moved.","required":["capabilityKey","stage"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string"},"suggestionKind":{"allOf":[{"$ref":"#/components/schemas/SuggestionKind"}],"nullable":true},"forecastDefinitionKey":{"type":"string","nullable":true},"stage":{"type":"string","enum":["starting","learning","established","learned"]},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producerRef":{"type":"string","description":"The producer and version answering now."},"since":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiHistoryImport": {"type":"object","x-ticvai-persistence":"ai.history_import","description":"**One import of a venue's own history** (29 September, AI functions review). A job: validated, then loaded into `ai.history_observation`, never into the ledger.","required":["id","venueId","dataKind","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"dataKind":{"type":"string","enum":["attendance","admissions","ticketSales","fnbSales","retailSales","queueReadings","staffShifts"]},"assetId":{"type":"string","format":"uuid","x-ticvai-references":"assets.media_asset"},"sourceSystem":{"type":"string","nullable":true},"columnMapping":{"type":"object","additionalProperties":{"type":"string"}},"dryRun":{"type":"boolean","default":false},"status":{"type":"string","enum":["queued","validating","loading","completed","completedWithRejections","failed"],"readOnly":true},"periodFrom":{"type":"string","format":"date","nullable":true,"readOnly":true},"periodTo":{"type":"string","format":"date","nullable":true,"readOnly":true},"monthsCovered":{"type":"integer","readOnly":true},"rowsRead":{"type":"integer","readOnly":true},"rowsLoaded":{"type":"integer","readOnly":true},"rowsRejected":{"type":"integer","readOnly":true},"findings":{"type":"array","readOnly":true,"items":{"type":"object","properties":{"row":{"type":"integer"},"code":{"type":"string","enum":["badDate","badNumber","negativeValue","duplicateDay","unmappedColumn","outOfRange"]},"detail":{"type":"string"}}}},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"AiVenueSettings": {"type":"object","x-ticvai-persistence":"ai.venue_settings","description":"**The venue AI profile** (29 September, AI functions review): the figures a venue gives at onboarding so every data-driven answer is useful before it has history. One row per venue; configuration, not history. Defaults come from the starting pattern for `venueType`, which TICVAI writes from published sources and made-up example curves, **never from another tenant's data** (AI-D01, AIP-149).","required":["venueId","venueType"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"venueType":{"type":"string","enum":["waterPark","themePark","familyEntertainmentCentre","museum","arena","zooAquarium","other"]},"isOutdoor":{"type":"boolean","default":true,"description":"Outdoor venues take the summer-heat and weather effects."},"capacity":{"type":"integer","minimum":1,"nullable":true},"openingHours":{"type":"array","description":"The usual week. Exceptions come from the venue calendar.","items":{"type":"object","properties":{"dayOfWeek":{"type":"integer","minimum":1,"maximum":7},"opensAt":{"type":"string"},"closesAt":{"type":"string"}}}},"typicalWeekdayAttendance":{"type":"integer","minimum":0,"nullable":true},"typicalWeekendAttendance":{"type":"integer","minimum":0,"nullable":true},"peakMonths":{"type":"array","items":{"type":"integer","minimum":1,"maximum":12}},"averageSpend":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"fnbAttachRate":{"type":"number","minimum":0,"maximum":1,"nullable":true},"staffProductivity":{"type":"object","additionalProperties":{"type":"number"},"description":"Per role, units per staff hour, e.g. `{\"cashier\": 40, \"gate\": 300}`. Defaults from the pattern."},"startingPatternKey":{"type":"string","readOnly":true,"description":"The pattern and version in use, e.g. `waterPark@3`."},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"FinCreditMemo": {"x-ticvai-persistence":"ledger.credit_memo + ledger.credit_memo_line","type":"object","description":"5.7.94. **A tax credit note against one tax invoice**, with its own series. Never edited.","required":["id","creditMemoNumber","taxInvoiceId","kind","reason","legalEntityId","issuedAt","currency","netAmount","taxAmount","grossAmount","lines"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"creditMemoNumber":{"type":"string","readOnly":true,"description":"Server-assigned from the legal entity's credit memo series, in sequence without gaps."},"taxInvoiceId":{"type":"string","format":"uuid"},"taxInvoiceNumber":{"type":"string","readOnly":true},"kind":{"type":"string","enum":["full","partial"]},"reason":{"type":"string","enum":["refund","cancellation","priceAdjustment","returnOfGoods","billingError","other"]},"refundId":{"type":"string","format":"uuid","nullable":true},"cancelledOrderId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid"},"buyerSubjectId":{"type":"string","format":"uuid","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmountInLegalCurrency":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"legalFxRate":{"allOf":[{"$ref":"#/components/schemas/FxRateValue"}],"nullable":true,"readOnly":true,"description":"The invoice's own `legalFxRate`, never today's (CHG-FIN-011)."},"invoiceSupplyValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"**The value of the supply shown on the tax invoice** (Executive Regulation Art. 60(1)(e)), adjusted by any earlier credit note on the same invoice. With `correctedSupplyValue` and `netAmount` (the difference) and `taxAmountInLegalCurrency` (the tax on the difference in AED), the four figures the law requires (CHG-FIN-011)."},"correctedSupplyValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The correct value of the supply after this credit note (Art. 60(1)(e))."},"supplierName":{"type":"string","readOnly":true,"description":"Snapshot of the legal entity at issue, as on the invoice (Art. 60(1)(b))."},"supplierAddress":{"type":"string","nullable":true,"readOnly":true},"supplierTaxRegistrationNumber":{"type":"string","nullable":true,"readOnly":true},"buyerName":{"type":"string","nullable":true,"readOnly":true,"description":"The recipient as on the invoice; name, address and TRN where they are registered (Art. 60(1)(c))."},"buyerAddress":{"type":"string","nullable":true,"readOnly":true},"buyerTaxRegistrationNumber":{"type":"string","nullable":true,"readOnly":true},"note":{"type":"string","nullable":true,"description":"The brief explanation of why the credit note was issued, printed on it (Art. 60(1)(f)); the reason's own wording when no note is given (CHG-FIN-011)."},"renditionAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"eInvoiceStatus":{"$ref":"#/components/schemas/FinEInvoiceTransmissionStatus"},"issuedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"lines":{"type":"array","items":{"$ref":"#/components/schemas/FinCreditMemoLine"}},"scopePath":{"type":"string","readOnly":true}}},
"FinCreditMemoLine": {"type":"object","required":["invoiceLineNumber","netAmount","taxAmount","grossAmount"],"properties":{"invoiceLineNumber":{"type":"integer","minimum":1},"description":{"type":"string","maxLength":500},"quantity":{"type":"number","nullable":true},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxRate":{"type":"number"},"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"FinEInvoiceTransmission": {"x-ticvai-persistence":"ledger.einvoice_transmission","type":"object","description":"6.1.1. One attempt to send one tax document to the provider, and its answer.","required":["id","documentKind","documentId","legalEntityId","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"documentKind":{"type":"string","enum":["taxInvoice","creditMemo"]},"documentId":{"type":"string","format":"uuid"},"documentNumber":{"type":"string"},"legalEntityId":{"type":"string","format":"uuid"},"providerId":{"type":"string","format":"uuid","nullable":true},"mode":{"type":"string","enum":["test","live"]},"status":{"$ref":"#/components/schemas/FinEInvoiceTransmissionStatus"},"payloadHash":{"type":"string","nullable":true,"description":"SHA-256 of the document as sent, so a resend can be shown to be the same document."},"providerMessageId":{"type":"string","nullable":true},"attempt":{"type":"integer","minimum":1},"errorCodes":{"type":"array","items":{"type":"string"}},"errorMessage":{"type":"string","nullable":true},"sentAt":{"type":"string","format":"date-time","nullable":true},"answeredAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true}}},
"FinEInvoiceTransmissionStatus": {"type":"string","description":"6.1.1. `notRequired` where the legal entity's provider is `disabled` or absent.","enum":["notRequired","queued","sent","accepted","rejected","failed"]},
"FinTaxCategory": {"type":"string","description":"How a line is treated for VAT. Taken from the tax code the line was posted with.","enum":["standardRated","zeroRated","exempt","outOfScope","reverseCharge"]},
"FinTaxInvoice": {"x-ticvai-persistence":"ledger.tax_invoice + ledger.tax_invoice_line","type":"object","description":"5.7.93, 5.10.3. **A guest tax invoice, as issued, never edited.** Corrections are credit memos. The supplier block is a snapshot of the legal entity at issue, so a later change of address does not change a document already given to a guest.","required":["id","invoiceNumber","invoiceType","status","legalEntityId","issuedAt","supplyDate","currency","netAmount","taxAmount","grossAmount","lines"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"invoiceNumber":{"type":"string","readOnly":true,"description":"Server-assigned from the legal entity's series for the document kind, in sequence and without gaps, e.g. `INV-2026-000123`. Never reused."},"invoiceType":{"$ref":"#/components/schemas/FinTaxInvoiceType"},"status":{"$ref":"#/components/schemas/FinTaxInvoiceStatus"},"legalEntityId":{"type":"string","format":"uuid"},"templateId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"orderIds":{"type":"array","items":{"type":"string","format":"uuid"}},"supplierName":{"type":"string"},"supplierAddress":{"type":"string","nullable":true},"supplierTaxRegistrationNumber":{"type":"string","nullable":true},"buyerSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest the orders belong to; the key a guest's own reads filter on."},"buyerName":{"type":"string","nullable":true},"buyerAddress":{"type":"string","nullable":true},"buyerCountryCode":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"buyerTaxRegistrationNumber":{"type":"string","nullable":true},"customerAccountId":{"type":"string","format":"uuid","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"supplyDate":{"type":"string","format":"date","description":"The date of supply where it differs from the issue date (the latest order's payment date on a consolidated invoice). A day in the region's time zone."},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmountInLegalCurrency":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"The tax in the legal entity's currency (AED in the UAE) where the invoice currency differs. **In the UAE the converted amounts use the UAE Central Bank rate at the date of supply** (Decree-Law Art. 69) and the rate is printed (`legalFxRate`, Executive Regulation Art. 59(1)(k)); CHG-FIN-011."},"legalCurrency":{"type":"string","pattern":"^[A-Z]{3}$","readOnly":true,"description":"The legal entity's currency (AED in the UAE), in which the law requires the tax and the gross amount (CHG-FIN-011)."},"grossAmountInLegalCurrency":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The gross amount payable in the legal currency (Executive Regulation Art. 59(1)(j); for a simplified invoice the total consideration, Art. 59(2)(e)). Equal to `grossAmount` when the invoice is in the legal currency (CHG-FIN-011)."},"legalFxRate":{"allOf":[{"$ref":"#/components/schemas/FxRateValue"}],"nullable":true,"readOnly":true,"description":"Units of the legal currency per one unit of `currency`, printed with the tax where the invoice is not in the legal currency (Art. 59(1)(k)). Null when it is (CHG-FIN-011)."},"legalFxRateSource":{"allOf":[{"$ref":"#/components/schemas/FxRateSource"}],"nullable":true,"readOnly":true,"description":"`uaeCentralBank` for a UAE legal entity (Decree-Law Art. 69)."},"paidCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"Where the guest paid in a currency they selected (`orders.Order.chargeCurrency`, CHG-FIN-001), printed as payment information with `paidAmount` and the charge rate. The invoice itself is in the base currency, so the AED amounts the law requires are the invoice's own figures (CHG-FIN-011)."},"paidAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"What the guest paid in `paidCurrency` (`orders.Order.chargeTotal`)."},"reverseChargeStatement":{"type":"string","nullable":true,"readOnly":true,"description":"Where the recipient must account for the tax, the statement saying so and the Decree-Law provision (Art. 59(1)(l), Art. 48). Null otherwise (CHG-FIN-011)."},"creditedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"languages":{"type":"array","items":{"type":"string"}},"supersedesInvoiceId":{"type":"string","format":"uuid","nullable":true},"renditionAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The PDF rendered at issue; read through getTaxDocumentRendition."},"eInvoiceStatus":{"$ref":"#/components/schemas/FinEInvoiceTransmissionStatus"},"issuedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Null where the platform issued it."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/FinTaxInvoiceLine"}},"taxSummary":{"type":"array","x-ticvai-persisted":false,"description":"VAT per rate and category, summed from the lines for the response.","items":{"type":"object","properties":{"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxRate":{"type":"number"},"taxableAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Written at the scope of the venue the orders were sold at, or the region for a consolidated invoice across venues."}}},
"FinTaxInvoiceLine": {"type":"object","description":"One line as it was sold and taxed. Amounts are in the invoice currency.","required":["lineNumber","description","quantity","netAmount","taxAmount","grossAmount","taxCategory"],"properties":{"lineNumber":{"type":"integer","minimum":1},"orderId":{"type":"string","format":"uuid"},"orderLineId":{"type":"string","format":"uuid","nullable":true},"description":{"type":"string","maxLength":500},"quantity":{"type":"number"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeId":{"type":"string","format":"uuid","nullable":true},"taxRate":{"type":"number","minimum":0,"maximum":100},"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"creditedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmountInLegalCurrency":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The amount payable for the line in the legal currency (AED), Executive Regulation Art. 59(1)(h); equal to `grossAmount` on an invoice in the legal currency (CHG-FIN-011)."}}},
"FinTaxInvoiceStatus": {"type":"string","description":"`issued` until a credit memo is issued against it; `superseded` where a full invoice replaced a simplified one for the same supply (only if the law allows it; see issueTaxInvoice).","enum":["issued","partiallyCredited","fullyCredited","superseded"]},
"FinTaxInvoiceType": {"type":"string","description":"5.7.93. `simplified` for one order with no recipient details, `full` for one order with them, `consolidated` for several paid orders of one buyer on one invoice.\n**When a simplified tax invoice is allowed in the UAE** (research 2 October 2026, CHG-FIN-011; Executive Regulation, Cabinet Decision 52 of 2017 as amended, Art. 59(5)): the recipient is not VAT-registered, or is registered and the consideration does not exceed AED 10,000, and the reverse charge does not apply. Otherwise the invoice is `full`. Both kinds carry the title \"Tax Invoice\" (Art. 59(1)(a), 59(2)(a)); a simplified one is issued on the date of supply (Art. 59(13)(1)), a full one within 14 days (Decree-Law Art. 67(1)).","enum":["simplified","full","consolidated"]},
"FxRateSource": {"type":"string","description":"**Where the rate came from, and which provider specifically.** `source: provider` said a feed set it and not which one — two tenants on different feeds were indistinguishable in the ledger, and a rate cannot be defended in an audit without naming its origin.\n\n**`uaeCentralBank` is the default for AED pairs.** The UAE Central Bank publishes an official daily rate and it is what a UAE auditor expects to see — a commercial feed is defensible for tender and awkward for statutory reporting.\n\n**`openExchangeRates` and `ecb` are the commercial and reference options.** ECB publishes daily reference rates free and is the usual fallback for non-AED pairs; Open Exchange Rates is the common commercial feed with intraday granularity. **The choice is per purpose, not per platform** — a tender rate wants intraday, a reporting rate wants the official daily close.","enum":["manual","uaeCentralBank","ecb","openExchangeRates","cardScheme","provider"]},
"FxRateValue": {"x-ticvai-persistence-column":"numeric(18,6)","type":"string","pattern":"^\\d+(\\.\\d{1,6})?$","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one (naming-and-style 5.1). Up to six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly — and stored as `numeric(18,6)` so the six places the wire carries survive the database.\n"},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]},
"UnifiedReconciliation": {"type":"object","description":"4.2.19. **Four sources and the variances between them.** A view showing each balanced against itself has not reconciled anything.\n","properties":{"from":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"to":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"sources":{"type":"array","items":{"type":"object","properties":{"source":{"type":"string","enum":["pos","gateway","bank","wallet","ledger"]},"providerName":{"type":"string","nullable":true},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"transactionCount":{"type":"integer"}}}},"variances":{"type":"array","description":"**Where two sources disagree, named.** A discrepancy is usually the gap between two of them rather than inside one, and *\"out by 240\"* without saying between what is not actionable.\n","items":{"type":"object","properties":{"between":{"type":"array","description":"The two sources that disagree, as named in `sources[].source`.","minItems":2,"maxItems":2,"items":{"type":"string","enum":["pos","gateway","bank","wallet","ledger"]}},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"likelyCause":{"type":"string","nullable":true}}}}}}
}
```
