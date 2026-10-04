# WS119 — AI Forecasting and Predictive Intelligence board 1

**10 screens · 18 operations · 21 schemas · 4 permissions**

Platform P09 TICVAI Web · ships as **ticvai-control** ·
platformAdmin audience · web ·
online only

## Who this is for

**platformAdmin on web.** Everything below is how you know what is
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
  `AI_CONFIGURE, AI_USE, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_VIEW`. A control nobody can use must say so,
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
| `ADM-499` | Forecasting Command Center | D | 6 | 6 | 7 | 39 | 0 | 0 | — | notStarted (—) |
| `ADM-500` | Forecast Configuration & Forecasting Strategy | A | 39 | 6 | 7 | 10 | 1 | 0 | — | notStarted (—) |
| `ADM-501` | Forecast Data & Signal Configuration | D | 6 | 6 | 7 | 9 | 0 | 0 | — | notStarted (—) |
| `ADM-502` | Attendance & Visitation Forecast | D | 6 | 6 | 7 | 43 | 0 | 0 | — | notStarted (—) |
| `ADM-503` | Ticket, Product & Timeslot Demand Forecast | B | 9 | 26 | 7 | 44 | 1 | 0 | — | notStarted (—) |
| `ADM-504` | Channel & Booking Pace Forecast | B | 9 | 22 | 7 | 41 | 0 | 6 | — | notStarted (—) |
| `ADM-505` | Revenue & Commercial Forecast | B | 14 | 26 | 7 | 42 | 0 | 0 | — | notStarted (—) |
| `ADM-506` | Forecast Drivers, Confidence & Explainability | A | 14 | 36 | 7 | 46 | 0 | 0 | — | notStarted (—) |
| `ADM-507` | Forecast Scenario & What-If Simulator | D | 6 | 20 | 7 | 40 | 0 | 0 | — | notStarted (—) |
| `ADM-508` | Forecast Accuracy, Review & Publication Center | A | 13 | 24 | 7 | 6 | 0 | 0 | — | notStarted (—) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-499` Forecasting Command Center

**Provide management with one central view of expected attendance, demand and revenue across venues and future periods.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-499 |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `versionId` (navigation), `tenantId` (navigation) |
| Route | `/analytics/forecasting-command-center-adm-499` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listForecastDefinitions` (AI_USE), `getForecast` (AI_USE), `exportForecastVersion` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**From the AI & Intelligence process.** Forecasting command centre: one view of expected attendance, demand and revenue across venues and the coming days, with how far each forecast has matured and which forecast alerts are open. Forecasts exist from day one on the venue profile, the venue-type pattern, the UAE calendar and the weather, so the tiles are never empty. The one thing to get right: every tile is a range with a most-likely figure and a stage badge, never a bare number and never a "confidence %".

**Known correction pending (do not draw the wrong version)**

- **Tiles "Forecast Confidence" and "Demand Index" bound to nothing.** Why: Confidence is shown as a range and a stage, never a single figure (ADR-0051); no operation defines a demand index - drop it or define it. *(source: ADR-0051 / screens/P09-platform-admin-console.yaml#ADM-499; AI & Intelligence)*
- **The P09 console shows a tenant's venues' forecasts with requiresModule analytics and no tenant picker or grant.** Why: Forecasting is an AI capability; and see the ADM-520 correction on tenant scope. *(source: screens/P09-platform-admin-console.yaml#ADM-037 (notes, R098); AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Subject | select | — | Attendance · Arrival pattern · Product demand · Timeslot demand · Channel pace · Revenue · Occupancy · Attraction utilisation · Queue · Entry flow · Staffing · POS demand … | `listForecastDefinitions` ?subject |
| Definition key | text field | — | — | `getForecast` ?definitionKey |
| Version | picker: choose a version | — | — | `getForecast` ?versionId |
| From | date and time picker | — | — | `getForecast` ?from |
| To | date and time picker | — | — | `getForecast` ?to |
| Dimension key | text field | — | — | `getForecast` ?dimensionKey |
| Scenario | picker: choose a scenario | — | — | `getForecast` ?scenarioId |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Forecast Attendance Today** (metric tile)

**Forecast Attendance Tomorrow** (metric tile)

**Forecast Attendance Next 7 Days** (metric tile)

**Forecast Revenue** (metric tile)

**Current Bookings** (metric tile)

**Expected Walk-In** (metric tile)

**Forecast Occupancy** (metric tile)

**Demand Index** (metric tile)

**Forecast Confidence** (metric tile)

**Forecast vs Actual** (metric tile)

**Revenue Forecast Accuracy** (metric tile)

**Active Forecast Alerts** (metric tile)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **attendance and revenue tiles**: "2,600 guests (1,850-3,400)" for today, tomorrow and next 7 days; revenue likewise in AED. A small stage badge and "Based on" on hover; "Forecast is out of date" when stale (36 hours). *(source: contracts/satellite/ai.yaml#getForecast / ADR-0051 / ADR-0051 (AI functions review 30 Sep §4 Forecasting))*
- **current bookings vs forecast**: Bookings on hand shown as the floor of the forecast range (a forecast never shows fewer guests than are already booked). *(source: ADR-0051 (AI functions review 30 Sep §4 Forecasting))*
- **Forecast vs Actual / Revenue Forecast Accuracy tiles**: Labelled "measured over <period>"; until 4 weeks of actuals exist the tile reads "Measuring". *(source: contracts/satellite/ai.yaml#getForecastAccuracy / ADR-0051)*
- **active forecast alerts**: Count of open alerts (forecast not published, deviation beyond range) linking to their screens. *(source: contracts/satellite/ai.yaml#/components/schemas/AiGovernanceAlert (forecastNotPublished) / contracts/satellite/ai.yaml#listAiInsights)*

**Data it reads**: `listForecastDefinitions` (onLoad, What is forecast); `getForecast` (onLoad, Forecast values); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-500` Forecast Configuration & Forecasting Strategy: *Forecast Configuration & Forecasting Strategy*; carries `definitionKey`
- → `ADM-501` Forecast Data & Signal Configuration: *Forecast Data & Signal Configuration*; carries `definitionKey`
- → `ADM-502` Attendance & Visitation Forecast: *Attendance & Visitation Forecast*; carries `tenantId`
- → `ADM-503` Ticket, Product & Timeslot Demand Forecast: *Ticket, Product & Timeslot Demand Forecast*; carries `tenantId`
- → `ADM-504` Channel & Booking Pace Forecast: *Channel & Booking Pace Forecast*; carries `tenantId`
- → `ADM-505` Revenue & Commercial Forecast: *Revenue & Commercial Forecast*; carries `tenantId`
- → `ADM-506` Forecast Drivers, Confidence & Explainability: *Forecast Drivers, Confidence & Explainability*; carries `tenantId`
- → `ADM-507` Forecast Scenario & What-If Simulator: *Forecast Scenario & What-If Simulator*; carries `tenantId`
- → `ADM-508` Forecast Accuracy, Review & Publication Center: *Forecast Accuracy, Review & Publication Center*; carries `definitionKey`, `versionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The forecasting list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the forecasting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No forecasting yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the forecasting are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **A venue with less than 4 weeks of trading**: All tiles still show ranges, wider, with "Starting - Limited historical data". *(source: ADR-0051)*

#### Consistency with other screens

- Match `ANL-057`: Same tiles on the venue analytics studio; one component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
today:
  venue: Coastal Aqua
  attendance: 2,600 (1,850-3,400)
  stage: Starting
  basedOn: venue profile, water-park pattern, UAE calendar, weather 34°C
next7: 15,900 guests (12,300-19,600)
revenue7: AED 2.31m (AED 1.78m-2.84m)
bookingsOnHand: 6420
```

#### Permissions

- `listForecastDefinitions` → `AI_USE` (operate) · staff
- `getForecast` → `AI_USE` (operate) · staff
- `exportForecastVersion` → `AI_USE` (operate) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

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

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-499` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-499`
- Workshop pack: AI_Forecasting_and_Predictive_Intelligence_Reference.pdf board 1
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 1: Opens Forecasting Command Center → Provide management with one central view of expected attendance, demand and revenue across venues and future periods.
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F228 branch at step 1 (expected): when Nothing has been set up on Forecasting Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F228 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-499?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-002`, `ADM-500`, `ADM-501`, `ADM-502`, `ADM-503`, `ADM-504`, `ADM-505`, `ADM-506`, `ADM-507`, `ADM-508`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-500` Forecast Configuration & Forecasting Strategy

**Configure what TICVAI should forecast, at what level of detail, for what horizon and how frequently forecasts should be refreshed. This screen establishes the forecasting object.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 1 · needs the `core` module |
| Block | Block A · ticket #28971 (APP-SETUP-ADM-500) |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Fields; Options conceptually) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `definitionKey` (navigation), `tenantId` (navigation) |
| Route | `/analytics/forecast-configuration-forecasting-strategy-adm-500` |

**What the spec says about it.** **Measure names, not "Revenue"** (decided 2 October 2026, Chinmay; CHG-FIN-002; BOARDREQ MOM-2758..2761). Takings (money taken less money paid back, a cash-control figure), Gross sales (before discounts, excluding VAT), Net revenue (gross sales less discounts and refunds), Recognised revenue and Deferred revenue are different numbers and never share a label; a tile takes its label from the seeded KPI it is bound to (`ReportingSystemKpi`). **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listForecastDefinitions` (AI_USE), `setForecastDefinition` (AI_CONFIGURE), `runForecast` (AI_CONFIGURE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**From the AI & Intelligence process.** Define what is forecast: subject (attendance, timeslot demand, channel pace, revenue, occupancy, queue, staffing and others), grain, breakdowns, horizon, refresh cadence, which producer is live, how much own history to read, what the forecast stands on before history exists (cold start), whether it auto-publishes and its quality gates. The one thing to get right: the producer choice offers rule, statistical or ensemble - a trained model is never chosen here, it arrives only through promotion.

**Known correction pending (do not draw the wrong version)**

- **30 selectFields lifted from the board (each forecast type and each horizon as its own select, plus Tenant, Status, Effective Dates).** Why: Subject is one enum, horizon one number, grain one enum; Tenant comes from the scope. Use the contract's fields. *(source: contracts/satellite/ai.yaml#setForecastDefinition / screens/P09-platform-admin-console.yaml#ADM-500; AI & Intelligence)*
- **"Confidence Policy" select.** Why: The contract has the starting band and quality gates, not a confidence policy; map it or drop it. *(source: contracts/satellite/ai.yaml#setForecastDefinition (coldStart.startingBandPercent, qualityGates); AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Forecast Name | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Forecast Type | select field | — | — | — | — | — | — |
| Forecast Target | select field | — | — | — | — | — | — |
| Forecast Horizon | select field | — | — | — | — | — | — |
| Time Granularity | select field | — | — | — | — | — | — |
| Refresh Frequency | select field | — | — | — | — | — | — |
| Historical Window | select field | — | — | — | — | — | — |
| Model Strategy | select field | — | — | — | — | — | — |
| Confidence Policy | select field | — | — | — | — | — | — |
| Effective Dates | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Forecast Types | select field | — | — | — | — | — | — |
| Attendance | select field | — | — | — | — | — | — |
| Ticket Demand | select field | — | — | — | — | — | — |
| Product Demand | select field | — | — | — | — | — | — |
| Net revenue | select field | — | — | — | — | (CHG-FIN-002: never a bare "Revenue") | — |
| Channel Demand | select field | — | — | — | — | — | — |
| Timeslot Demand | select field | — | — | — | — | — | — |
| Event Demand | select field | — | — | — | — | — | — |
| Membership Demand | select field | — | — | — | — | — | — |
| Add-On Demand | select field | — | — | — | — | — | — |
| Experience Demand | select field | — | — | — | — | — | — |
| Intraday | select field | — | — | — | — | — | — |
| Next Day | select field | — | — | — | — | — | — |
| 7 Days | select field | — | — | — | — | — | — |
| 14 Days | select field | — | — | — | — | — | — |
| 30 Days | select field | — | — | — | — | — | — |
| 90 Days | select field | — | — | — | — | — | — |
| Producer | radio group | optional | — | Rule · Statistical · Model · Ensemble | — | `rule`, `statistical` or `ensemble` (M18-16). A model only arrives by promotion. | `AiForecastDefinition.producer` |
| History window (months) | stepper or slider | optional | 36 | min 1; max 60 | — | Default 36 (M18-16). | `AiForecastDefinition.historyWindowMonths` |
| Cold start | group | optional | — | — | — | **What the forecast stands on before there is history** (AI functions review): the venue AI profile with the venue-type pattern, a sister venue, a category, or imported history; the starting range … | `AiForecastDefinition.coldStart` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Subject | select | — | Attendance · Arrival pattern · Product demand · Timeslot demand · Channel pace · Revenue · Occupancy · Attraction utilisation · Queue · Entry flow · Staffing · POS demand … | `listForecastDefinitions` ?subject |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_CONFIGURE`, `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **producer**: Rule, Statistical or Ensemble (a weighted blend); "Model" is shown disabled with "A trained model goes live only when your admin promotes it". *(source: DI-958 / contracts/satellite/ai.yaml#setForecastDefinition (producer))*
- **historyWindowMonths**: Default 36 months (1-60); imported history counts; less history than the window is fine and said. *(source: DI-958 / contracts/satellite/ai.yaml#setForecastDefinition)*
- **coldStart**: Strategy (venue settings with the venue-type pattern - default; sister venue of the same tenant; category baseline; imported history), prior weight k (default 4 same weekdays) and starting band (default ±40%). A sister venue must be the same tenant; no data is pooled across tenants. *(source: contracts/satellite/ai.yaml#setForecastDefinition (coldStart) / ADR-0051)*
- **autoPublish**: Off by default; on means L4 Controlled auto - publishes without approval only when the gates pass; the switch states that. *(source: ADR-0050 / contracts/satellite/ai.yaml#setForecastDefinition)*
- **horizon / grain / refresh**: Horizon in days (1-730) offered as presets (intraday, next day, 7, 14, 30, 90); hourly grain only with hourly refresh. *(source: contracts/satellite/ai.yaml#setForecastDefinition / designer default)*

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Data it reads**: `listForecastDefinitions` (onLoad, What is forecast); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-499` Forecasting Command Center: *Back to Forecasting Command Center*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The forecast forecasting strategy configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the forecast forecasting strategy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No forecast forecasting strategy configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A `model` producer was requested directly; models are promoted, not set (`model-needs-promotion`).; 409 A run of this definition is in progress. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
definition:
  key: attendance.daily.coastal-aqua
  subject: attendance
  grain: day
  horizonDays: 90
  refresh: daily
  producer: statistical
  historyWindowMonths: 36
  coldStart:
    strategy: venueSettings
    k: 4
    band: ±40%
  autoPublish: true
  dimensions:
  - channel
  - product
```

#### Permissions

- `listForecastDefinitions` → `AI_USE` (operate) · staff
- `setForecastDefinition` → `AI_CONFIGURE` (configure) · staff
- `runForecast` → `AI_CONFIGURE` (configure) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.2.12 | System shall forecast attendance by customer segment. | Unified Operations Dashboard | CONTRACTED | `setForecastDefinition` |
| 8.2.14 | System shall forecast attendance by geography. | Unified Operations Dashboard | CONTRACTED | `setForecastDefinition` |
| 8.2.16 | System shall forecast attendance using historical booking trends. | Unified Operations Dashboard | CONTRACTED | `setForecastDefinition` |
| 8.2.27 | System shall forecast revenue by customer segment. | Unified Operations Dashboard | CONTRACTED | `setForecastDefinition` |
| 8.2.51 | System shall support configurable forecasting models. | Unified Operations Dashboard | CONTRACTED | `setForecastDefinition` |
| 8.2.57 | System shall support forecasting permissions. | Unified Operations Dashboard | CONTRACTED | `setForecastDefinition` |
| 8.2.15 | System shall forecast attendance using real-time booking trends. | Unified Operations Dashboard | CONTRACTED | `runForecast` |
| 5.6.37 | The system shall forecast queue congestion and capacity utilization for attractions, ticketing counters and service locations. | F&B & Guest Management | CONTRACTED | data `AiForecastDefinition` |
| 15.4.3 | Seasonal Demand Forecasting - System shall forecast seasonal demand. | Inventory Management | CONTRACTED | data `AiForecastDefinition` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Forecast configuration offers producer rule, statistical or ensemble, and a history window defaulting to 36 months. *(agreed · MoM 18 Sep 2026, M18-16 · DI-958)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-500` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-500`
- Workshop pack: AI_Forecasting_and_Predictive_Intelligence_Reference.pdf board 1
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 2: Works in Forecast Configuration & Forecasting Strategy → Configure what TICVAI should forecast, at what level of detail, for what horizon and how frequently forecasts should be refreshed. This screen establishes the forecasting object.

#### Acceptance for the design

- [ ] Every input above is drawn (39), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-500?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-501` Forecast Data & Signal Configuration

**Define which historical, current and contextual signals may contribute to each forecast.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-501 |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `definitionKey` (navigation), `signalKey` (navigation), `tenantId` (navigation) |
| Route | `/analytics/forecast-data-signal-configuration-adm-501` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `setForecastDefinition` (AI_CONFIGURE), `listForecastSignals` (AI_USE), `configureForecastSignalSource` (AI_CONFIGURE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Signals a forecast may use: weather, public holidays, the school calendar, the religious calendar (Ramadan and Eid by Hijri date), events, marketing and internal series - each with its provider, refresh cadence and freshness. The one thing to get right: a stale or failing signal is visible per forecast, because a missing blocking signal stops publication.

**Known correction pending (do not draw the wrong version)**

- **Buttons "Save forecast definition" and an unbound table.** Why: Bind the table to listForecastSignals and the editor to configureForecastSignalSource. *(source: screens/P09-platform-admin-console.yaml#ADM-501; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Weather · Public holiday · School calendar · Religious calendar · Event · Marketing · Internal | `listForecastSignals` ?kind |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_CONFIGURE`, `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **signal source**: Kind, provider, credential reference (never a secret), refresh cadence (hourly, daily, weekly, manual), active. The weather provider carries a cost (agreed). *(source: contracts/satellite/ai.yaml#configureForecastSignalSource / ADR-0051 (AI-D10 weather API with its cost))*
- **signals per definition**: Which signal keys each forecast definition may use, as checkboxes per definition. *(source: contracts/satellite/ai.yaml#setForecastDefinition (signalKeys))*

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Save forecast definition (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **freshness**: Last refreshed and next due per signal; amber when late, red when a blocking signal is missing. *(source: contracts/satellite/ai.yaml#listForecastSignals / contracts/satellite/ai.yaml#publishForecastVersion)*

**Data it reads**: `listForecastSignals` (onLoad, Forecast signals and their freshness); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-499` Forecasting Command Center: *Back to Forecasting Command Center*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The forecast data signal list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the forecast data signal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No forecast data signal yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the forecast data signal are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A `model` producer was requested directly; models are promoted, not set (`model-needs-promotion`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
signals:
- key: weather.dubai
  kind: weather
  provider: Weather API
  cadence: hourly
  last: '10:00'
- key: uae.holidays
  kind: publicHoliday
  cadence: manual
- key: hijri.calendar
  kind: religiousCalendar
  cadence: weekly
- key: uae.school
  kind: schoolCalendar
  cadence: weekly
```

#### Permissions

- `setForecastDefinition` → `AI_CONFIGURE` (configure) · staff
- `listForecastSignals` → `AI_USE` (operate) · staff
- `configureForecastSignalSource` → `AI_CONFIGURE` (configure) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.2.12 | System shall forecast attendance by customer segment. | Unified Operations Dashboard | CONTRACTED | `setForecastDefinition` |
| 8.2.14 | System shall forecast attendance by geography. | Unified Operations Dashboard | CONTRACTED | `setForecastDefinition` |
| 8.2.16 | System shall forecast attendance using historical booking trends. | Unified Operations Dashboard | CONTRACTED | `setForecastDefinition` |
| 8.2.27 | System shall forecast revenue by customer segment. | Unified Operations Dashboard | CONTRACTED | `setForecastDefinition` |
| 8.2.51 | System shall support configurable forecasting models. | Unified Operations Dashboard | CONTRACTED | `setForecastDefinition` |
| 8.2.57 | System shall support forecasting permissions. | Unified Operations Dashboard | CONTRACTED | `setForecastDefinition` |
| 8.2.10 | System shall forecast attendance during holidays and special periods. | Unified Operations Dashboard | CONTRACTED | `configureForecastSignalSource` |
| 8.2.11 | System shall forecast attendance based on weather conditions. | Unified Operations Dashboard | CONTRACTED | `configureForecastSignalSource` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-501` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-501`
- Workshop pack: AI_Forecasting_and_Predictive_Intelligence_Reference.pdf board 1
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 4: Works in Forecast Data & Signal Configuration → Define which historical, current and contextual signals may contribute to each forecast.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-501?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Save forecast definition, Cancel.
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-502` Attendance & Visitation Forecast

**Provide detailed prediction of future venue attendance.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-502 |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `detectorKey` (navigation), `tenantId` (navigation) |
| Route | `/analytics/attendance-visitation-forecast-adm-502` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getForecast` (AI_USE), `configureAnomalyDetector` (AI_CONFIGURE), `listAiInsights` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Attendance forecast in detail: by day and hour, venue and breakdown, with range, drivers and how it compares with actuals so far. The one thing to get right: the chart shows the P10-P90 band and the most-likely line, actuals as points, and the stage of the forecast (Starting with a wide band on day one, tightening as own data builds).

**Known correction pending (do not draw the wrong version)**

- **Layout is an unbound table with unlabelled buttons.** Why: Bind the chart and table to getForecast for the attendance definition. *(source: screens/P09-platform-admin-console.yaml#ADM-502; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Definition key | text field | — | — | `getForecast` ?definitionKey |
| Version | picker: choose a version | — | — | `getForecast` ?versionId |
| From | date and time picker | — | — | `getForecast` ?from |
| To | date and time picker | — | — | `getForecast` ?to |
| Dimension key | text field | — | — | `getForecast` ?dimensionKey |
| Scenario | picker: choose a scenario | — | — | `getForecast` ?scenarioId |
| Status | select | — | New · Reviewed · Accepted · Rejected · Actioned · Measured | `listAiInsights` ?status |
| Kind | select | — | Anomaly · Forecast deviation · Trend · Opportunity · Executive summary · Root cause · Forecast threshold · Marketing recommendation | `listAiInsights` ?kind |
| Priority | radio group | — | Low · Medium · High · Critical | `listAiInsights` ?priority |
| From | date and time picker | — | — | `listAiInsights` ?from |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_CONFIGURE`, `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **attendance chart**: Band (P10-P90), P50 line, actuals; bookings on hand as a floor line; weekends (Sat-Sun) and holidays marked. *(source: contracts/satellite/ai.yaml#getForecast / ADR-0051)*
- **alerts**: Attendance below the forecast's low end raises an insight; the detector on the forecast can be set up from here. *(source: contracts/satellite/ai.yaml#configureAnomalyDetector (source forecast) / ADR-0051 (AI functions review 30 Sep §4 Anomaly detection))*

**Data it reads**: `getForecast` (onLoad, Forecast values); `listAiInsights` (onLoad, Forecast threshold alerts (kind forecastThreshold)); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-499` Forecasting Command Center: *Back to Forecasting Command Center*; carries `versionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attendance visitation forecast list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attendance visitation forecast untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attendance visitation forecast yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the attendance visitation forecast are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
days:
- date: Sat 17 Oct
  p10: 2100
  p50: 2900
  p90: 3600
  booked: 1980
- date: Sun 18 Oct
  p10: 1900
  p50: 2600
  p90: 3300
stage: Learning
```

#### Permissions

- `getForecast` → `AI_USE` (operate) · staff
- `configureAnomalyDetector` → `AI_CONFIGURE` (configure) · staff
- `listAiInsights` → `AI_USE` (operate) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

43 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 31 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-502` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-502`
- Workshop pack: AI_Forecasting_and_Predictive_Intelligence_Reference.pdf board 1
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 6: Works in Attendance & Visitation Forecast → Provide detailed prediction of future venue attendance.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-502?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, , Cancel.
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-503` Ticket, Product & Timeslot Demand Forecast

**Predict demand at the product and inventory level so TICVAI can understand what customers are likely to buy, not only total attendance.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 3 · needs the `core` module |
| Block | Block B · ticket #29073 (APP-CONSOLE-ADM-503) |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): Forecast values of one product and timeslot demand definition, picked on the screen (4 October 2026, CHG-FXS-004). |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/analytics/ticket-product-timeslot-demand-forecast-adm-503` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getForecast` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it. **Forecast definition picked on the screen 4 October 2026: listForecastDefinitions (subject productDemand or timeslotDemand) supplies the definitionKey getForecast requires; columns are AiForecastPoint's (p10, p50, p90). Pack labels with no contract field left the screen** (CHG-FXS-004)

**From the AI & Intelligence process.** Demand by ticket, product and timeslot: the booking curve so far, the expected final demand and the remaining opportunity per slot, so slots can be added, merged or repriced. The one thing to get right: a suggested slot or price change is a suggestion with a person's approval, never applied from the forecast.

**Known correction pending (do not draw the wrong version)**

- **Column "Product Relationships" in a demand table.** Why: Relationships belong to recommendations configuration; drop it here. *(source: screens/P09-platform-admin-console.yaml#ADM-503; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | — | `Tenant.id` |
| Forecast | text field | optional | — | — | — | Query subject productDemand or timeslotDemand; the first active definition is picked by default. | `AiForecastDefinition.definitionKey` |
| From | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Query from; today by default. | `AiForecastPoint.targetStart` |
| To | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Query to; the definition's horizon by default. | `AiForecastPoint.targetEnd` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Definition key | text field | — | — | `getForecast` ?definitionKey |
| Version | picker: choose a version | — | — | `getForecast` ?versionId |
| From | date and time picker | — | — | `getForecast` ?from |
| To | date and time picker | — | — | `getForecast` ?to |
| Dimension key | text field | — | — | `getForecast` ?dimensionKey |
| Scenario | picker: choose a scenario | — | — | `getForecast` ?scenarioId |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |
| Subject | select | — | Attendance · Arrival pattern · Product demand · Timeslot demand · Channel pace · Revenue · Occupancy · Attraction utilisation · Queue · Entry flow · Staffing · POS demand … | `listForecastDefinitions` ?subject |
| Definition key | text field | — | — | `getForecastAccuracy` ?definitionKey |
| Horizon days | number field (days) | — | — | `getForecastAccuracy` ?horizonDays |
| From | date and time picker | — | — | `getForecastAccuracy` ?from |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`)

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Forecast** (data table, from `getForecast`): a range, never a bare number (design 5.6).

| Shows | Format | Notes |
|---|---|---|
| Target start | 1 Oct 2026, 14:30 | — |
| Dimension key | text | Canonical key of the breakdown, e.g. `product=…;channel=web`. |
| P10 | 1,234.5 | — |
| P50 | 1,234.5 | — |
| P90 | 1,234.5 | — |
| Unit | text | — |

**The selected value** (detail panel, from `getForecast`)

| Shows | Format | Notes |
|---|---|---|
| Target start | 1 Oct 2026, 14:30 | — |
| Target end | 1 Oct 2026, 14:30 | — |
| P10 | 1,234.5 | — |
| P50 | 1,234.5 | — |
| P90 | 1,234.5 | — |
| Drivers | grouped details | Component decomposition or SHAP contributions, largest first (ADM-506). |

**Version** (detail panel, from `getForecast`)

| Shows | Format | Notes |
|---|---|---|
| Version number | 1,234 | — |
| Status | chip: Running, Draft, Awaiting approval, Published, Superseded, Rejected… | — |
| Basis | chip: Heuristic, Statistical, Model, Hybrid, Manual | How the answer was reached, and this is the field the whole design exists for. A venue must be able to see that today's price suggestion is … |
| Maturity | grouped details | Where an answer stands, on every answer (29 September, AI functions review; baseline then learn). |
| Data cutoff at | 1 Oct 2026, 14:30 | The analytical replica watermark the snapshot was taken at. |

**Accuracy by horizon** (data table, from `getForecastAccuracy`)

| Shows | Format | Notes |
|---|---|---|
| Horizon days | 1,234 | — |
| Wape | 1,234.5 | — |
| Bias | 1,234.5 | — |
| Interval coverage | 1,234.5 | Share of actuals inside the 10th-90th percentile band. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **booking curve**: Days before visit on the x-axis, cumulative sales, the historical average curve (or the starting pattern's while history is short) and the forecast final demand as a range. *(source: contracts/satellite/ai.yaml#getForecast / screens/P09-platform-admin-console.yaml#ADM-503)*
- **slot suggestions**: Add, remove or merge an under-sold slot (with guest notification of the time change), raise price above about 80% sold, lower below about 20-30% - each shown as a suggestion that opens the owning screen; approval by a person. *(source: DI-454 / ADR-0050 (pricing inputs L2))*

**Data it reads**: `getForecast` (onLoad, Forecast values); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …); `listForecastDefinitions` (onLoad, The product and timeslot demand forecast definitions …); `getForecastAccuracy` (onLoad, How accurate the picked demand forecast has been, by …)

**Where the user goes next**

- → `ADM-499` Forecasting Command Center: *Back to Forecasting Command Center*; carries `versionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list skeleton, with the filters already drawn. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves what is on screen untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product and timeslot demand forecast defined for this tenant yet. |
| Empty, no results (`?state=emptyNoResults`) | No values in this window. Names the window and offers the definition's horizon. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AI_USE`, which `getForecast` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_ACCESS` for `listOwnPlatformStaffGrants` … |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
slot:
  product: Dolphin Show 16:00
  capacity: 400
  sold: 312
  daysBefore: 3
  forecastFinal: 380-420
  suggestion: Raise to AED 95 (sold 78%)
```

#### Permissions

- `getForecast` → `AI_USE` (operate) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `listForecastDefinitions` → `AI_USE` (operate) · staff
- `getForecastAccuracy` → `AI_USE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `AI_USE`, which `getForecast` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_ACCESS` for `listOwnPlatformStaffGrants` …

#### Requirements it meets

44 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 32 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI suggestions from sales forecasts: add/remove time slots, merge under-sold adjacent slots (with guest notification of the time change), and dynamic pricing (raise when a slot is >~80% sold, lower when <~20–30%). *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-454)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-503` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-503`
- Workshop pack: AI_Forecasting_and_Predictive_Intelligence_Reference.pdf board 1
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 8: Works in Ticket, Product & Timeslot Demand Forecast → Predict demand at the product and inventory level so TICVAI can understand what customers are likely to buy, not only total attendance.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-503?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-504` Channel & Booking Pace Forecast

**Predict where and when future sales are expected to arrive. This is particularly useful because a venue with 10,000 current bookings may still receive significant B2C, POS, reseller and walk-in volume.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 3 · needs the `core` module |
| Block | Block B · ticket #29074 (APP-CONSOLE-ADM-504) |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): Forecast values of one channel booking pace definition, picked on the screen (4 October 2026, CHG-FXS-004). |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/analytics/channel-booking-pace-forecast-adm-504` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getForecast` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it. **Forecast definition picked on the screen 4 October 2026: listForecastDefinitions (subject channelPace) supplies the definitionKey getForecast requires; columns are AiForecastPoint's (p10, p50, p90). Pack labels with no contract field left the screen** (CHG-FXS-004)

**From the AI & Intelligence process.** Where and when the remaining sales will come from: per channel (website, app, POS, flying POS, kiosk, B2B, reseller, OTA/API, call centre, walk-in) the bookings so far, the expected additional and the expected final. The one thing to get right: current + expected additional = forecast final, shown per channel, with walk-in as its own line.

**Known correction pending (do not draw the wrong version)**

- **Channels are drawn as columns, with a mangled column "Channel Current Expected Additional Final Forecast".** Why: Channels are rows; current, additional and final are the columns. *(source: screens/P09-platform-admin-console.yaml#ADM-504; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | — | `Tenant.id` |
| Forecast | text field | optional | — | — | — | Query subject channelPace; the first active definition is picked by default. | `AiForecastDefinition.definitionKey` |
| From | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Query from; today by default. | `AiForecastPoint.targetStart` |
| To | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Query to; the definition's horizon by default. | `AiForecastPoint.targetEnd` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Definition key | text field | — | — | `getForecast` ?definitionKey |
| Version | picker: choose a version | — | — | `getForecast` ?versionId |
| From | date and time picker | — | — | `getForecast` ?from |
| To | date and time picker | — | — | `getForecast` ?to |
| Dimension key | text field | — | — | `getForecast` ?dimensionKey |
| Scenario | picker: choose a scenario | — | — | `getForecast` ?scenarioId |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |
| Subject | select | — | Attendance · Arrival pattern · Product demand · Timeslot demand · Channel pace · Revenue · Occupancy · Attraction utilisation · Queue · Entry flow · Staffing · POS demand … | `listForecastDefinitions` ?subject |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`)

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Forecast** (data table, from `getForecast`): dimensionKey is the sales channel; a range, never a bare number (design 5.6).

| Shows | Format | Notes |
|---|---|---|
| Target start | 1 Oct 2026, 14:30 | — |
| Dimension key | text | Canonical key of the breakdown, e.g. `product=…;channel=web`. |
| P10 | 1,234.5 | — |
| P50 | 1,234.5 | — |
| P90 | 1,234.5 | — |
| Unit | text | — |

**The selected value** (detail panel, from `getForecast`)

| Shows | Format | Notes |
|---|---|---|
| Target start | 1 Oct 2026, 14:30 | — |
| Target end | 1 Oct 2026, 14:30 | — |
| P10 | 1,234.5 | — |
| P50 | 1,234.5 | — |
| P90 | 1,234.5 | — |
| Drivers | grouped details | Component decomposition or SHAP contributions, largest first (ADM-506). |

**Version** (detail panel, from `getForecast`)

| Shows | Format | Notes |
|---|---|---|
| Version number | 1,234 | — |
| Status | chip: Running, Draft, Awaiting approval, Published, Superseded, Rejected… | — |
| Basis | chip: Heuristic, Statistical, Model, Hybrid, Manual | How the answer was reached, and this is the field the whole design exists for. A venue must be able to see that today's price suggestion is … |
| Maturity | grouped details | Where an answer stands, on every answer (29 September, AI functions review; baseline then learn). |
| Data cutoff at | 1 Oct 2026, 14:30 | The analytical replica watermark the snapshot was taken at. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **channel table**: Channel rows (not columns): current, expected additional (range), forecast final (range), pace vs usual. *(source: contracts/satellite/ai.yaml#getForecast (dimensionKey "channel=web") / screens/P09-platform-admin-console.yaml#ADM-504)*

**Data it reads**: `getForecast` (onLoad, Forecast values); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …); `listForecastDefinitions` (onLoad, The channel booking pace forecast definitions (subject …)

**Where the user goes next**

- → `ADM-499` Forecasting Command Center: *Back to Forecasting Command Center*; carries `versionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list skeleton, with the filters already drawn. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves what is on screen untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel booking pace forecast defined for this tenant yet. |
| Empty, no results (`?state=emptyNoResults`) | No values in this window. Names the window and offers the definition's horizon. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AI_USE`, which `getForecast` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_ACCESS` for `listOwnPlatformStaffGrants` … |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- channel: Website
  current: 3120
  additional: 600-950
  final: 3,720-4,070
- channel: Walk-in
  current: 0
  additional: 700-1,300
```

#### Permissions

- `getForecast` → `AI_USE` (operate) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `listForecastDefinitions` → `AI_USE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `AI_USE`, which `getForecast` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_ACCESS` for `listOwnPlatformStaffGrants` …

#### Requirements it meets

41 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 29 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-504` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-504`
- Workshop pack: AI_Forecasting_and_Predictive_Intelligence_Reference.pdf board 1
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 10: Works in Channel & Booking Pace Forecast → Predict where and when future sales are expected to arrive. This is particularly useful because a venue with 10,000 current bookings may still receive significant B2C, POS, reseller and walk-in …

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-504?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-505` Revenue & Commercial Forecast

**Forecast future revenue based on predicted sales, attendance, product mix, current pricing and other approved commercial signals.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 3 · needs the `core` module |
| Block | Block B · ticket #29075 (APP-CONSOLE-ADM-505) |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): Forecast values of one revenue definition, picked on the screen (4 October 2026, CHG-FXS-004). |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/analytics/revenue-commercial-forecast-adm-505` |

**What the spec says about it.** **Measure names, not "Revenue"** (decided 2 October 2026, Chinmay; CHG-FIN-002; BOARDREQ MOM-2758..2761). Takings (money taken less money paid back, a cash-control figure), Gross sales (before discounts, excluding VAT), Net revenue (gross sales less discounts and refunds), Recognised revenue and Deferred revenue are different numbers and never share a label; a tile takes its label from the seeded KPI it is bound to (`ReportingSystemKpi`). **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getForecast` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it. **Forecast definition picked on the screen 4 October 2026: listForecastDefinitions (subject revenue) supplies the definitionKey getForecast requires; columns are AiForecastPoint's (p10, p50, p90). Pack labels with no contract field left the screen** (CHG-FXS-004)

**From the AI & Intelligence process.** Revenue forecast: ticket, membership, add-on, F&B and retail revenue, revenue per visitor and against budget, each as a range. The one thing to get right: revenue is forecast from forecast volume and current published prices; it never invents prices and always shows the range.

**Known correction pending (do not draw the wrong version)**

- **Tile "Revenue Confidence Range" as a separate metric.** Why: The range belongs on each figure, not on its own tile. *(source: ADR-0051; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | — | `Tenant.id` |
| Forecast | text field | optional | — | — | — | Query subject revenue; the first active definition is picked by default. | `AiForecastDefinition.definitionKey` |
| From | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Query from; today by default. | `AiForecastPoint.targetStart` |
| To | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Query to; the definition's horizon by default. | `AiForecastPoint.targetEnd` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Definition key | text field | — | — | `getForecast` ?definitionKey |
| Version | picker: choose a version | — | — | `getForecast` ?versionId |
| From | date and time picker | — | — | `getForecast` ?from |
| To | date and time picker | — | — | `getForecast` ?to |
| Dimension key | text field | — | — | `getForecast` ?dimensionKey |
| Scenario | picker: choose a scenario | — | — | `getForecast` ?scenarioId |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |
| Subject | select | — | Attendance · Arrival pattern · Product demand · Timeslot demand · Channel pace · Revenue · Occupancy · Attraction utilisation · Queue · Entry flow · Staffing · POS demand … | `listForecastDefinitions` ?subject |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Sent by *Why did it change*** (`explainMetricChange`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Metric key `metricKey` | text field | required | — | — | — | — | `explainMetricChange` body |
| Period `period` | text field | required | — | — | — | ISO period, e.g. `2026-09-21/2026-09-27`. | `explainMetricChange` body |
| Comparison `comparison` | segmented control | optional | Previous period | Previous period · Same period last year · Forecast | — | — | `explainMetricChange` body |
| Dimensions `dimensions` | list of values (chips) | optional | — | — | — | — | `explainMetricChange` body |
| Keep `keep` | toggle | optional | off | — | — | — | `explainMetricChange` body |

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`)

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Forecast** (data table, from `getForecast`): dimensionKey is the revenue stream (ticket, membership, add-on, F&B, retail); a range, never a bare number (design 5.6).

| Shows | Format | Notes |
|---|---|---|
| Target start | 1 Oct 2026, 14:30 | — |
| Dimension key | text | Canonical key of the breakdown, e.g. `product=…;channel=web`. |
| P10 | 1,234.5 | — |
| P50 | 1,234.5 | — |
| P90 | 1,234.5 | — |
| Unit | text | — |

**The selected value** (detail panel, from `getForecast`)

| Shows | Format | Notes |
|---|---|---|
| Target start | 1 Oct 2026, 14:30 | — |
| Target end | 1 Oct 2026, 14:30 | — |
| P10 | 1,234.5 | — |
| P50 | 1,234.5 | — |
| P90 | 1,234.5 | — |
| Drivers | grouped details | Component decomposition or SHAP contributions, largest first (ADM-506). |

**Version** (detail panel, from `getForecast`)

| Shows | Format | Notes |
|---|---|---|
| Version number | 1,234 | — |
| Status | chip: Running, Draft, Awaiting approval, Published, Superseded, Rejected… | — |
| Basis | chip: Heuristic, Statistical, Model, Hybrid, Manual | How the answer was reached, and this is the field the whole design exists for. A venue must be able to see that today's price suggestion is … |
| Maturity | grouped details | Where an answer stands, on every answer (29 September, AI functions review; baseline then learn). |
| Data cutoff at | 1 Oct 2026, 14:30 | The analytical replica watermark the snapshot was taken at. |

**Explanation** (detail panel, from `explainMetricChange`)

| Shows | Format | Notes |
|---|---|---|
| Change | 1,234.5 | — |
| Change percent | 1,234.5 | — |
| Drivers | list or chips (count when long) | — |
| Narrative | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Why did it change (secondary button) | `explainMetricChange` POST `/insights/explain-metric-change` | inline | AiMetricChangeExplanation | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **revenue tiles**: "AED 412,000 (AED 318,000-503,000)" per line; F&B and retail only where those modules are licensed; vs budget only where a budget exists. *(source: contracts/satellite/ai.yaml#getForecast / ADR-0051)*

**Data it reads**: `getForecast` (onLoad, Forecast values); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …); `listForecastDefinitions` (onLoad, The revenue forecast definitions (subject revenue); the …)

**Where the user goes next**

- → `ADM-499` Forecasting Command Center: *Back to Forecasting Command Center*; carries `versionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list skeleton, with the filters already drawn. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves what is on screen untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No revenue forecast defined for this tenant yet. |
| Empty, no results (`?state=emptyNoResults`) | No values in this window. Names the window and offers the definition's horizon. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AI_USE`, which `getForecast` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_ACCESS` for `listOwnPlatformStaffGrants` … |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
next7:
  tickets: AED 1.62m (1.25m-1.98m)
  fnb: AED 0.41m (0.31m-0.50m)
  perVisitor: AED 145 (AED 132-158)
```

#### Permissions

- `getForecast` → `AI_USE` (operate) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `listForecastDefinitions` → `AI_USE` (operate) · staff
- `explainMetricChange` → `AI_USE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `AI_USE`, which `getForecast` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_ACCESS` for `listOwnPlatformStaffGrants` …

#### Requirements it meets

42 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 30 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-505` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-505`
- Workshop pack: AI_Forecasting_and_Predictive_Intelligence_Reference.pdf board 1
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 12: Works in Revenue & Commercial Forecast → Forecast future revenue based on predicted sales, attendance, product mix, current pricing and other approved commercial signals.
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-505?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Why did it change.
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-506` Forecast Drivers, Confidence & Explainability

**Explain why the forecast changed and how much uncertainty it carries.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 1 · needs the `core` module |
| Block | Block A · ticket #28972 (APP-SETUP-ADM-506) |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): Forecast values of one any definition, picked on the screen (4 October 2026, CHG-FXS-004). |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/analytics/forecast-drivers-confidence-explainability-adm-506` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `explainMetricChange` (AI_USE), `listForecastVersions` (AI_USE), `getForecast` (AI_USE), `getForecastAccuracy` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it. **Forecast definition picked on the screen 4 October 2026: listForecastDefinitions (subject any) supplies the definitionKey getForecast requires; columns are AiForecastPoint's (p10, p50, p90). Pack labels with no contract field left the screen** (CHG-FXS-004)

**From the AI & Intelligence process.** Why the forecast is what it is and why it changed: the drivers (booking pace, weekday pattern, events, weather, price, cancellations) with direction and strength, the change from the previous version, the uncertainty by horizon and what limits it (limited history, a new product, a missing signal). The one thing to get right: uncertainty is shown as ranges by horizon and measured accuracy, not as "92% / High".

**Fixed on main** (the package already carries these; draw what it says): Columns "92% / High", "84% / High", "71% / Medium", "58% / Lower" (confidence by horizon) and "Confidence Status High" in purpose. (CHG-WIR-013); The board example is pasted into purpose. (CHG-WIR-013).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | — | `Tenant.id` |
| Forecast | text field | optional | — | — | — | Query subject any; the first active definition is picked by default. | `AiForecastDefinition.definitionKey` |
| From | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Query from; today by default. | `AiForecastPoint.targetStart` |
| To | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Query to; the definition's horizon by default. | `AiForecastPoint.targetEnd` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Definition key | text field | — | — | `listForecastVersions` ?definitionKey |
| Status | select | — | Running · Draft · Awaiting approval · Published · Superseded · Rejected · Failed | `listForecastVersions` ?status |
| Definition key | text field | — | — | `getForecast` ?definitionKey |
| Version | picker: choose a version | — | — | `getForecast` ?versionId |
| From | date and time picker | — | — | `getForecast` ?from |
| To | date and time picker | — | — | `getForecast` ?to |
| Dimension key | text field | — | — | `getForecast` ?dimensionKey |
| Scenario | picker: choose a scenario | — | — | `getForecast` ?scenarioId |
| Definition key | text field | — | — | `getForecastAccuracy` ?definitionKey |
| Horizon days | number field (days) | — | — | `getForecastAccuracy` ?horizonDays |
| From | date and time picker | — | — | `getForecastAccuracy` ?from |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |
| Subject | select | — | Attendance · Arrival pattern · Product demand · Timeslot demand · Channel pace · Revenue · Occupancy · Attraction utilisation · Queue · Entry flow · Staffing · POS demand … | `listForecastDefinitions` ?subject |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Sent by *Why did it change*** (`explainMetricChange`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Metric key `metricKey` | text field | required | — | — | — | — | `explainMetricChange` body |
| Period `period` | text field | required | — | — | — | ISO period, e.g. `2026-09-21/2026-09-27`. | `explainMetricChange` body |
| Comparison `comparison` | segmented control | optional | Previous period | Previous period · Same period last year · Forecast | — | — | `explainMetricChange` body |
| Dimensions `dimensions` | list of values (chips) | optional | — | — | — | — | `explainMetricChange` body |
| Keep `keep` | toggle | optional | off | — | — | — | `explainMetricChange` body |

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`)

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Forecast** (data table, from `getForecast`): a range, never a bare number (design 5.6).

| Shows | Format | Notes |
|---|---|---|
| Target start | 1 Oct 2026, 14:30 | — |
| Dimension key | text | Canonical key of the breakdown, e.g. `product=…;channel=web`. |
| P10 | 1,234.5 | — |
| P50 | 1,234.5 | — |
| P90 | 1,234.5 | — |
| Unit | text | — |

**The selected value** (detail panel, from `getForecast`)

| Shows | Format | Notes |
|---|---|---|
| Target start | 1 Oct 2026, 14:30 | — |
| Target end | 1 Oct 2026, 14:30 | — |
| P10 | 1,234.5 | — |
| P50 | 1,234.5 | — |
| P90 | 1,234.5 | — |
| Drivers | grouped details | Component decomposition or SHAP contributions, largest first (ADM-506). |

**Version** (detail panel, from `getForecast`)

| Shows | Format | Notes |
|---|---|---|
| Version number | 1,234 | — |
| Status | chip: Running, Draft, Awaiting approval, Published, Superseded, Rejected… | — |
| Basis | chip: Heuristic, Statistical, Model, Hybrid, Manual | How the answer was reached, and this is the field the whole design exists for. A venue must be able to see that today's price suggestion is … |
| Maturity | grouped details | Where an answer stands, on every answer (29 September, AI functions review; baseline then learn). |
| Data cutoff at | 1 Oct 2026, 14:30 | The analytical replica watermark the snapshot was taken at. |

**Accuracy by horizon** (data table, from `getForecastAccuracy`)

| Shows | Format | Notes |
|---|---|---|
| Horizon days | 1,234 | — |
| Period start | 1 Oct 2026, 14:30 | — |
| Wape | 1,234.5 | — |
| Bias | 1,234.5 | — |
| Interval coverage | 1,234.5 | Share of actuals inside the 10th-90th percentile band. |

**Versions** (data table, from `listForecastVersions`)

| Shows | Format | Notes |
|---|---|---|
| Version number | 1,234 | — |
| Status | chip: Running, Draft, Awaiting approval, Published, Superseded, Rejected… | — |
| Basis | chip: Heuristic, Statistical, Model, Hybrid, Manual | How the answer was reached, and this is the field the whole design exists for. A venue must be able to see that today's price suggestion is … |
| Data cutoff at | 1 Oct 2026, 14:30 | The analytical replica watermark the snapshot was taken at. |

**Explanation** (detail panel, from `explainMetricChange`)

| Shows | Format | Notes |
|---|---|---|
| Change | 1,234.5 | — |
| Change percent | 1,234.5 | — |
| Drivers | list or chips (count when long) | — |
| Narrative | text | — |
| Reliability | chip: Grounded, Partial, Conflicting sources, Insufficient evidence | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Why did it change (secondary button) | `explainMetricChange` POST `/insights/explain-metric-change` | inline | AiMetricChangeExplanation | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **change explanation**: Previous vs current most-likely and range, with the drivers that moved it; the decomposition is plain arithmetic and the model only words it. *(source: contracts/satellite/ai.yaml#explainMetricChange / ADR-0054)*
- **uncertainty by horizon**: Range width at 1, 7, 28 days and measured WAPE/coverage where it exists; flags such as "Limited historical data", "New product", "Missing weather" as chips. *(source: contracts/satellite/ai.yaml#getForecastAccuracy / contracts/satellite/ai.yaml#/components/schemas/AiMaturity)*

**Data it reads**: `listForecastVersions` (onLoad, Forecast versions); `getForecast` (onLoad, Forecast values); `getForecastAccuracy` (onLoad, Measured forecast accuracy); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …); `listForecastDefinitions` (onLoad, The any forecast definitions (subject any); the picked …)

**Where the user goes next**

- → `ADM-499` Forecasting Command Center: *Back to Forecasting Command Center*; carries `versionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list skeleton, with the filters already drawn. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves what is on screen untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No any forecast defined for this tenant yet. |
| Empty, no results (`?state=emptyNoResults`) | No values in this window. Names the window and offers the definition's horizon. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `AI_USE`, which `listForecastVersions` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_ACCESS` for `listOwnPlatformStaffGrants` … |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
forecast:
  value: 16120
  range: 15,300-17,050
  previous: 15640
  change: '+480'
drivers:
- driver: Booking pace
  effect: + strong
- driver: Saturday pattern
  effect: + strong
- driver: Special event
  effect: + medium
- driver: Weather
  effect: + medium
- driver: Price
  effect: neutral
- driver: Cancellation rate
  effect: '- medium'
narrative: Booking pace is above the usual Saturday pattern and the weather forecast improved, so the forecast moved
  up.
```

#### Permissions

- `explainMetricChange` → `AI_USE` (operate) · staff
- `listForecastVersions` → `AI_USE` (operate) · staff
- `getForecast` → `AI_USE` (operate) · staff
- `getForecastAccuracy` → `AI_USE` (operate) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `listForecastDefinitions` → `AI_USE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `AI_USE`, which `listForecastVersions` requires to show this screen, and names that permission (the screen's other reads need `PLATFORM_TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_ACCESS` for `listOwnPlatformStaffGrants` …

#### Requirements it meets

46 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.4.18 | System shall support AI-powered root cause analysis. | Unified Operations Dashboard | CONTRACTED | `explainMetricChange` |
| 8.2.53 | System shall maintain forecast history. | Unified Operations Dashboard | CONTRACTED | `listForecastVersions` |
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
| … 34 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-506` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-506`
- Workshop pack: AI_Forecasting_and_Predictive_Intelligence_Reference.pdf board 1
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 14: Works in Forecast Drivers, Confidence & Explainability → Explain why the forecast changed and how much uncertainty exists. This is essential because management should not receive only: “Tomorrow attendance = 16,120.” They need to understand the basis and …
- ADR-0051 *Every AI function ships on a baseline and learns per tenant; a model goes live only on evidence* (`docs/adr/0051-ai-ships-on-a-baseline-and-learns-per-tenant.md`)
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (36 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-506?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Why did it change.
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-507` Forecast Scenario & What-If Simulator

**Allow management to test possible future conditions without changing production configuration. This is one of the most important screens.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 3 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-507 |
| Who uses it | ticvai staff holding `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/analytics/forecast-scenario-what-if-simulator-adm-507` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `getForecast` (AI_USE), `createForecastScenario` (AI_USE), `compareForecastScenarios` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the AI & Intelligence process.** What-if simulator: test a change - a 10% price decrease, shorter opening hours, rain, an event, a marketing push, more or fewer staff, a closure - against a published forecast, and compare scenarios side by side, without changing anything live. The one thing to get right: scenario results are deltas against the base version, as ranges, clearly labelled "What-if".

**Known correction pending (do not draw the wrong version)**

- **Column "Confidence" in the results.** Why: Show the delta as a range; no confidence figure. *(source: ADR-0051; AI & Intelligence)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Definition key | text field | — | — | `getForecast` ?definitionKey |
| Version | picker: choose a version | — | — | `getForecast` ?versionId |
| From | date and time picker | — | — | `getForecast` ?from |
| To | date and time picker | — | — | `getForecast` ?to |
| Dimension key | text field | — | — | `getForecast` ?dimensionKey |
| Scenario | picker: choose a scenario | — | — | `getForecast` ?scenarioId |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **changes**: One row per lever (price, capacity, opening hours, weather, event, marketing, staffing, closure) with its target and value; the base is a published version picked by date. *(source: contracts/satellite/ai.yaml#createForecastScenario / MoM 18 Sep 4.10)*

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Every forecast scenario what-if** (data table)

| Shows | Format | Notes |
|---|---|---|
| Attendance | text | not in the schema: `Attendance` |
| Revenue | text | not in the schema: `Revenue` |
| Product demand | text | not in the schema: `Product Demand` |
| Peak time | text | not in the schema: `Peak Time` |
| Capacity pressure | text | not in the schema: `Capacity Pressure` |
| Confidence | text | not in the schema: `Confidence` |
| Operational implications | text | not in the schema: `Operational Implications` |

**The selected forecast scenario what-if** (detail panel): The pack groups this record's detail under its own headings: “Attendance”, “Simulation”, “Important Boundary”, “If management chooses a scenario”.

| Shows | Format | Notes |
|---|---|---|
| Attendance | text | not in the schema: `Attendance` |
| Revenue | text | not in the schema: `Revenue` |
| Product demand | text | not in the schema: `Product Demand` |
| Peak time | text | not in the schema: `Peak Time` |
| Capacity pressure | text | not in the schema: `Capacity Pressure` |
| Confidence | text | not in the schema: `Confidence` |
| Operational implications | text | not in the schema: `Operational Implications` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **result**: Attendance, revenue, product demand, peak time, capacity pressure as base vs what-if with the delta range; computing state while it runs (202). *(source: contracts/satellite/ai.yaml#createForecastScenario / contracts/satellite/ai.yaml#compareForecastScenarios)*

**Data it reads**: `getForecast` (onLoad, Forecast values); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-499` Forecasting Command Center: *Back to Forecasting Command Center*; carries `versionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The forecast scenario what-if list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the forecast scenario what-if untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No forecast scenario what-if yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the forecast scenario what-if are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
scenario:
  name: Price -10% weekdays in Nov
  base: Attendance v42
  result: Attendance +6% (+2% to +11%), revenue -4% (-8% to +1%)
```

#### Permissions

- `getForecast` → `AI_USE` (operate) · staff
- `createForecastScenario` → `AI_USE` (operate) · staff
- `compareForecastScenarios` → `AI_USE` (operate) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

40 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 28 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-507` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-507`
- Workshop pack: AI_Forecasting_and_Predictive_Intelligence_Reference.pdf board 1
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 16: Works in Forecast Scenario & What-If Simulator → Allow management to test possible future conditions without changing production configuration. This is one of the most important screens.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-507?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-508` Forecast Accuracy, Review & Publication Center

**Measure forecast quality over time and publish approved forecast outputs for use by other TICVAI modules.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | AI · wave 1 · needs the `core` module |
| Block | Block A · ticket #28973 (APP-SETUP-ADM-508) |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (1 configure, 2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Analyze) and no metric row |
| Offline | online only |
| Opens with | `definitionKey` (navigation), `versionId` (navigation), `tenantId` (navigation) |
| Route | `/analytics/forecast-accuracy-review-publication-center-adm-508` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `runForecast` (AI_CONFIGURE), `listForecastVersions` (AI_USE), `publishForecastVersion` (AI_USE), `getForecastAccuracy` (AI_USE), `exportForecastVersion` (AI_USE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**From the AI & Intelligence process.** Forecast accuracy, review and publication: how accurate the forecasts have actually been (measured against actuals, by horizon, against the baseline rule), and the place where a forecast version that does not auto-publish is reviewed and published for the rest of TICVAI to use. The one thing to get right: accuracy is a measured history, shown as WAPE, bias and range coverage with the period it was measured over - never a promise on a future forecast - and publishing is a person's decision with the quality gates in view.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- In Block A only runForecast and publishForecastVersion are in the slice. (CHG-SBO-006)

**Fixed on main** (the package already carries these; draw what it says): The table and detail columns are lifted from a board image ("Saturday Walk-In", "4%", "MODEL REVIEW RECOMMENDED"), bound to no operation. (CHG-SBO-007); purpose ends mid-sentence ("Forecast vs Actual Example:"). (CHG-WIR-013); module is Analytics and requiresModule analytics. (CHG-SBO-007).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Who approves forecast publication at a tenant - the console operator or the venue's own analyst?** → Forecast publication is approved by whoever holds that module's AI publish permission; no default role. Uses the per-module permission checklist with presets (see the ADM-554 decision). *(decided by Chinmay, 2026-10-02; DEC-003 / CHG-NOTE-001)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Definition key | text field | — | — | `listForecastVersions` ?definitionKey |
| Status | select | — | Running · Draft · Awaiting approval · Published · Superseded · Rejected · Failed | `listForecastVersions` ?status |
| Definition key | text field | — | — | `getForecastAccuracy` ?definitionKey |
| Horizon days | number field (days) | — | — | `getForecastAccuracy` ?horizonDays |
| From | date and time picker | — | — | `getForecastAccuracy` ?from |
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `AI_CONFIGURE`, `AI_USE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Publish forecast version** (modal, opened by *Publish forecast version*; *Publish forecast version* calls `publishForecastVersion`, *Cancel* sends nothing)

**Collects what `publishForecastVersion` sends before it is called.** Nothing in the body is required. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Note `note` | text area | optional | — | max length 1000 | — | — | `publishForecastVersion` body |

Errors to draw in the form: 403 The caller does not hold the AI publish permission of the version's module at its scope (`module-ai-publish-required`, CHG-FUP-004).; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Not publishable: a quality gate failed (`quality-gate-failed`), the version is not the latest draft (`version-not-current`), or its definition names no module …

**Form: Export forecast version** (modal, opened by *Export forecast version*; *Export forecast version* calls `exportForecastVersion`, *Cancel* sends nothing)

**Collects what `exportForecastVersion` sends before it is called.** Required: `format`. Optional: `from`, `to`, `dimensionKey`, `scenarioId`, `includeDrivers`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Format `format` | segmented control | required | — | Csv · Xlsx · Json | — | — | `exportForecastVersion` body |
| From `from` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `exportForecastVersion` body |
| To `to` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `exportForecastVersion` body |
| Dimension key `dimensionKey` | text field | optional | — | — | — | One breakdown only. Omitted, every breakdown of the version. | `exportForecastVersion` body |
| Scenario `scenarioId` | picker: choose a scenario | optional | — | — | shows names, sends the id | — | `exportForecastVersion` body |
| Include drivers `includeDrivers` | toggle | optional | off | — | — | — | `exportForecastVersion` body |

Errors to draw in the form: 403 The version is not published and the caller does not hold `AI_APPROVE` (`draft-export-refused`).; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Run forecast now**: Choose a forecast definition; the run starts outside the nightly schedule and returns a version in Running. 409 if a run of that definition is already running. *(source: contracts/satellite/ai.yaml#runForecast)*
- **publication note**: Optional note (shown in the version history) on Publish. *(source: contracts/satellite/ai.yaml#publishForecastVersion)*

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Forecast versions** (data table, from `listForecastVersions`): The versions of the picked definition, newest first. The board's example values ("Saturday Walk-In", "7.4%", "MODEL REVIEW RECOMMENDED") are sample data, not columns.

| Shows | Format | Notes |
|---|---|---|
| Version number | 1,234 | — |
| Status | chip: Running, Draft, Awaiting approval, Published, Superseded, Rejected… | — |
| Model version | text | — |
| Data cutoff at | 1 Oct 2026, 14:30 | The analytical replica watermark the snapshot was taken at. |
| Horizon start | 1 Oct 2026, 14:30 | — |
| Published at | 1 Oct 2026, 14:30 | — |

**Measured accuracy** (detail panel, from `getForecastAccuracy`)

| Shows | Format | Notes |
|---|---|---|
| Horizon days | 1,234 | — |
| Period start | 1 Oct 2026, 14:30 | — |
| Period end | 1 Oct 2026, 14:30 | — |
| Wape | 1,234.5 | — |
| Bias | 1,234.5 | — |
| Interval coverage | 1,234.5 | Share of actuals inside the 10th-90th percentile band. |
| Baseline wape | 1,234.5 | — |
| Measured at | 1 Oct 2026, 14:30 | — |

**The selected version** (detail panel, from `listForecastVersions`)

| Shows | Format | Notes |
|---|---|---|
| Producer ref | text | — |
| Quality checks | grouped details | Each gate and whether it passed. |
| Published by principal | the name it points at, never the id | Null where the definition auto-published. |
| Decision record | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
|  (publish gate) | navigation or local | — | — | — | — |
| Run forecast (secondary button) | `runForecast` POST `/forecast-definitions/{definitionKey}/runs` | — | AiForecastVersion | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 A run of this definition is in progress. | — |
| Publish forecast version (primary button) | `publishForecastVersion` POST `/forecast-versions/{versionId}/publish` | inline | AiForecastVersion | 403 The caller does not hold the AI publish permission of the version's module at its scope (`module-ai-publish-required`, CHG-FUP-004).; 404 The resource does not exist, or is outside the caller's scope. This includes … | opens modal first |
| Export forecast version (secondary button) | `exportForecastVersion` POST `/forecast-versions/{versionId}/exports` | inline | AiForecastExport | 403 The version is not published and the caller does not hold `AI_APPROVE` (`draft-export-refused`).; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **versions list**: Immutable versions newest first: number, definition, status (Running, Draft, Awaiting approval, Published, Superseded, Rejected, Failed), producer and basis, stage badge, data cut-off, quality checks (completeness, blocking signals, accuracy regression) as pass/fail chips. The published one is pinned. *(source: contracts/satellite/ai.yaml#/components/schemas/AiForecastVersion / contracts/satellite/ai.yaml#listForecastVersions)*
- **accuracy**: Per horizon (1, 7, 28 days): WAPE, bias and interval coverage, each labelled "measured over <dates>", with the baseline rule's figures beside the current producer's. Under 4 weeks of actuals the panel says "Measuring - accuracy appears once 4 weeks of actuals exist" rather than showing a figure. *(source: contracts/satellite/ai.yaml#getForecastAccuracy / ADR-0051 (AI functions review 30 Sep §4 Forecasting) / ADR-0051)*
- **forecast vs actual**: A line of actuals over the published forecast's range band (P10-P90) and most-likely line, so misses are visible as points outside the band. *(source: contracts/satellite/ai.yaml#getForecast / designer default)*
- **Who may approve publication**: Whoever holds that module's AI publish permission (the per-module "Publish AI model" check in the role builder; roles are preset permission configurations, never fixed default roles). TICVAI staff only through a grant. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-001))*

**What each action does** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **Publish**: Allowed only when the quality gates pass; the previous published version becomes Superseded and operational requirements are re-derived from the new one (a toast says so). 409 names the failing gate. *(source: contracts/satellite/ai.yaml#publishForecastVersion)*
- **Export**: CSV, Excel or JSON with a header naming definition, version, producer, basis and data cut-off; built asynchronously, the file arrives in downloads. *(source: contracts/satellite/ai.yaml#exportForecastVersion)*

**Data it reads**: `listForecastVersions` (onLoad, Forecast versions); `getForecastAccuracy` (onLoad, Measured forecast accuracy); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-499` Forecasting Command Center: *Back to Forecasting Command Center*; carries `versionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The forecast accuracy review list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the forecast accuracy review untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No forecast version for this definition yet. Offers Run forecast (`runForecast`); the baseline forecast exists from day one (ADR-0051), so a first run always has something to show. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the forecast accuracy review are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `AI_CONFIGURE`, `AI_USE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A run of this definition is in progress.; 409 Not publishable: a quality gate failed (`quality-gate-failed`), the version is not the latest draft (`version-not-current`), or its definition names no module … |

#### Edge cases to draw

- **Definition auto-publishes (L4)**: Its versions show "Published automatically - gates passed" and no Publish button; a failed gate leaves it in Draft for a person with a forecastNotPublished alert. *(source: ADR-0050 / contracts/satellite/ai.yaml#runForecast / contracts/satellite/ai.yaml#/components/schemas/AiGovernanceAlert (forecastNotPublished))*
- **Learned producer passes its gate in shadow**: A link "Ready to promote - review on drift and releases" (ADM-554); this screen never promotes a model. *(source: ADR-0051 (AI-D16) / contracts/satellite/ai.yaml#promoteAiRelease)*

#### Consistency with other screens

- Match `ADM-506`: Same accuracy figures and labels; ADM-506 explains drivers, ADM-508 measures and publishes.
- Match `ADM-554`: Promotion of a learned producer happens there, from the same accuracy figures (the gate reads them).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
definition: Daily attendance - Coastal Aqua
versions:
- version: 42
  status: Awaiting approval
  producer: statistical v3 (blend k=4)
  stage: Learning
  basedOn: venue profile, UAE calendar, weather, 6 weeks of your sales
  cutoff: 30 Sep 2026 23:00
  gates: completeness ✓, signals ✓, regression ✓
- version: 41
  status: Published
  stage: Learning
accuracy:
  horizon: 7 days
  WAPE: 16.8% (baseline rule 21.5%)
  bias: +2.1%
  coverage: 81% of actuals inside the range
  measured: 18 Aug-27 Sep 2026
```

#### Permissions

- `runForecast` → `AI_CONFIGURE` (configure) · staff
- `listForecastVersions` → `AI_USE` (operate) · staff
- `publishForecastVersion` → `AI_USE` (operate) · staff
- `getForecastAccuracy` → `AI_USE` (operate) · staff
- `exportForecastVersion` → `AI_USE` (operate) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.2.15 | System shall forecast attendance using real-time booking trends. | Unified Operations Dashboard | CONTRACTED | `runForecast` |
| 8.2.53 | System shall maintain forecast history. | Unified Operations Dashboard | CONTRACTED | `listForecastVersions` |
| 8.2.18 | System shall provide forecast accuracy measurements. | Unified Operations Dashboard | CONTRACTED | `getForecastAccuracy` |
| 8.2.19 | System shall compare forecasted attendance against actual attendance. | Unified Operations Dashboard | CONTRACTED | `getForecastAccuracy` |
| 8.2.34 | System shall compare forecasted revenue against actual revenue. | Unified Operations Dashboard | CONTRACTED | `getForecastAccuracy` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-508` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-508`
- Workshop pack: AI_Forecasting_and_Predictive_Intelligence_Reference.pdf board 1
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 18: Works in Forecast Accuracy, Review & Publication Center → Measure forecast quality over time and publish approved forecast outputs for use by other TICVAI modules. A forecasting system should continuously answer: How accurate have our forecasts actually …
- ADR-0051 *Every AI function ships on a baseline and learns per tenant; a model goes live only on evidence* (`docs/adr/0051-ai-ships-on-a-baseline-and-learns-per-tenant.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-508?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, , Run forecast, Publish forecast version, Export forecast version.
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P09 reference designs** (from `handoff/design-batches/apps/6-ticvai-controller/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P09 TICVAI Web

- Portal access exposes TICVAI pricing, so prospects submit contact details and a trade license as proof of a real venue, reviewed and approved by TICVAI before access is granted. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-827)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"compareForecastScenarios": {"method":"POST","path":"/forecast-scenarios/compare","contract":"ai","summary":"Compare scenarios","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiScenarioComparison"},
"configureAnomalyDetector": {"method":"PUT","path":"/anomaly-detectors/{detectorKey}","contract":"ai","summary":"Set up anomaly detection on a KPI","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiAnomalyDetector","responds":"AiAnomalyDetector"},
"configureForecastSignalSource": {"method":"PUT","path":"/forecast-signals/{signalKey}","contract":"ai","summary":"Set up a forecast signal","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiSignalSource","responds":"AiSignalSource"},
"createForecastScenario": {"method":"POST","path":"/forecast-scenarios","contract":"ai","summary":"Run a what-if","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiForecastScenario","responds":null},
"explainMetricChange": {"method":"POST","path":"/insights/explain-metric-change","contract":"ai","summary":"Why did this metric change","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiMetricChangeExplanation"},
"exportForecastVersion": {"method":"POST","path":"/forecast-versions/{versionId}/exports","contract":"ai","summary":"Export a forecast version as a file","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getForecast": {"method":"GET","path":"/forecasts","contract":"ai","summary":"Forecast values","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"definitionKey","in":"query","required":true},{"name":"versionId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"dimensionKey","in":"query","required":null},{"name":"scenarioId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getForecastAccuracy": {"method":"GET","path":"/forecast-accuracy","contract":"ai","summary":"Measured forecast accuracy","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"definitionKey","in":"query","required":true},{"name":"horizonDays","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiInsights": {"method":"GET","path":"/insights","contract":"ai","summary":"Insights and anomalies","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listForecastDefinitions": {"method":"GET","path":"/forecast-definitions","contract":"ai","summary":"What is forecast","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"subject","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listForecastSignals": {"method":"GET","path":"/forecast-signals","contract":"ai","summary":"Forecast signals and their freshness","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listForecastVersions": {"method":"GET","path":"/forecast-versions","contract":"ai","summary":"Forecast versions","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"definitionKey","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOwnPlatformStaffGrants": {"method":"GET","path":"/platform-staff-grants/mine","contract":"identity","summary":"The calling platform operator's own grants into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"activeOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTenants": {"method":"GET","path":"/tenants","contract":"subscription","summary":"List tenants","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"planId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"openPlatformStaffGrant": {"method":"POST","path":"/platform-staff-grants","contract":"identity","summary":"A platform operator opens a time-boxed grant into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PlatformStaffGrant"},
"publishForecastVersion": {"method":"POST","path":"/forecast-versions/{versionId}/publish","contract":"ai","summary":"Publish a forecast version","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiForecastVersion"},
"runForecast": {"method":"POST","path":"/forecast-definitions/{definitionKey}/runs","contract":"ai","summary":"Run a forecast now","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setForecastDefinition": {"method":"PUT","path":"/forecast-definitions/{definitionKey}","contract":"ai","summary":"Define a forecast","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiForecastDefinition","responds":"AiForecastDefinition"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiAnomalyDetector": {"type":"object","x-ticvai-persistence":"ai.anomaly_detector","description":"**An anomaly detector on one KPI** (C9, AIP-080..095). Configured thresholds on day one; a seasonal robust baseline (median/MAD) and peer comparison across venues as history builds. Detects **aggregate** deviations; actor-level patterns belong to risk, and both share one correlation key (AIP-090).","required":["detectorKey","method"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"detectorKey":{"type":"string"},"source":{"type":"string","enum":["metric","forecast","deviceHealth"],"default":"metric","description":"What is watched (29 September, build): a semantic-layer KPI, a published forecast (8.2.20, 8.2.41), or device status events (8.9.9)."},"metricKey":{"type":"string","nullable":true,"description":"A metric of the semantic layer (Reporting KPI). Required where `source` is `metric`."},"forecastSource":{"type":"object","nullable":true,"description":"Required where `source` is `forecast`; `method` is then `threshold`.","required":["definitionKey","comparator","threshold"],"properties":{"definitionKey":{"type":"string"},"dimensionKey":{"type":"string","nullable":true},"percentile":{"type":"string","enum":["p10","p50","p90"],"default":"p50"},"comparator":{"type":"string","enum":["above","atOrAbove","below","atOrBelow"]},"threshold":{"type":"number"},"thresholdKind":{"type":"string","enum":["absolute","percentOfCapacity"],"default":"absolute","description":"`percentOfCapacity` compares with the period's capacity (occupancy, 8.2.41)."},"horizonDays":{"type":"integer","minimum":1,"maximum":365,"nullable":true,"description":"Only points this many days ahead are compared. Null means the whole horizon."}}},"deviceHealthSource":{"type":"object","nullable":true,"description":"Required where `source` is `deviceHealth`.","properties":{"deviceKinds":{"type":"array","items":{"type":"string"},"description":"DeviceKind values; empty means every kind."},"failureRatePercent":{"type":"number","minimum":0,"maximum":100},"windowMinutes":{"type":"integer","minimum":5,"maximum":1440,"default":60}}},"method":{"type":"string","enum":["threshold","seasonalRobustZ","peerComparison","model"]},"thresholds":{"type":"object","additionalProperties":true,"nullable":true},"sensitivity":{"type":"string","enum":["low","medium","high"],"default":"medium"},"dimensions":{"type":"array","items":{"type":"string"}},"cadence":{"type":"string","enum":["hourly","daily"]},"isActive":{"type":"boolean","default":true},"falseAlarmRate":{"type":"number","nullable":true,"readOnly":true,"description":"Share of its insights rejected over 90 days. The number that decides whether a model is worth it."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiEvidenceItem": {"type":"object","x-ticvai-persistence":"none — held in jsonb on ai.decision_record.evidence, through AiEvidenceItemList","description":"One piece of evidence behind a decision, **labelled by origin** (AIC-197): read from a source system, derived by a rule or feature, or inferred by a model. An explanation is built from these, never from a model's chain of thought (AIC-192).","required":["label","kind"],"properties":{"label":{"type":"string","enum":["source","derived","modelInferred"]},"kind":{"type":"string","description":"What it is: `feature`, `rule`, `document`, `metric`, `transaction`, `candidateSet`."},"ref":{"type":"string","nullable":true,"description":"Where it came from: a table and id, a document chunk, a metric key."},"name":{"type":"string"},"value":{"type":"object","additionalProperties":true,"nullable":true},"observedAt":{"type":"string","format":"date-time","nullable":true}}},
"AiEvidenceItemList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The evidence of one decision record, stored with it.","items":{"$ref":"#/components/schemas/AiEvidenceItem"}},
"AiForecastAccuracy": {"type":"object","x-ticvai-persistence":"ai.forecast_accuracy","description":"**Measured accuracy by horizon** (AIP-044, ADM-508), labelled measured: WAPE, bias and interval coverage against the baseline rule. These are the numbers the promotion gate reads (design 3.5).","required":["definitionId","horizonDays","periodStart"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"definitionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_definition"},"versionId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.forecast_version"},"producerRef":{"type":"string"},"horizonDays":{"type":"integer","minimum":0},"periodStart":{"type":"string","format":"date-time"},"periodEnd":{"type":"string","format":"date-time"},"wape":{"type":"number","nullable":true},"bias":{"type":"number","nullable":true},"intervalCoverage":{"type":"number","minimum":0,"maximum":1,"nullable":true,"description":"Share of actuals inside the 10th-90th percentile band."},"baselineWape":{"type":"number","nullable":true},"measuredAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastDefinition": {"type":"object","x-ticvai-persistence":"ai.forecast_definition","description":"**What is forecast, at what grain, for what horizon, how often and by which producer** (design 3.1 Forecast, 5.2; ADM-500). One forecasting service for the platform: BI's extra subjects are definitions here, not a second forecaster (AIP-036, AIP-037).","required":["definitionKey","subject","grain","horizonDays","producer"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"definitionKey":{"type":"string"},"name":{"type":"string"},"subject":{"type":"string","enum":["attendance","arrivalPattern","productDemand","timeslotDemand","channelPace","revenue","occupancy","attractionUtilisation","queue","entryFlow","staffing","posDemand","fnbDemand","retailDemand","stockDemand","resourceDemand","refunds","cashCollection","membershipRenewals","churn"]},"module":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"}],"description":"**Whose AI this forecast is, and so who publishes it** (Chinmay, 2 October, workbook Q3: \"the permission holder for that module's AI\"; CHG-FUP-004). `publishForecastVersion` requires the permission `contracts/shared/permissions.yaml` `x-ticvai-module-ai-publish` names for this module. Absent on a write, the server takes it from `subject`: ticketing for `attendance`, `arrivalPattern`, `productDemand`, `timeslotDemand`, `channelPace`, `occupancy` and `refunds`; access for `entryFlow` and `attractionUtilisation`; queue for `queue`; fnb for `fnbDemand`; retail for `retailDemand`; inventory for `stockDemand`; resources for `resourceDemand`; membership for `membershipRenewals` and `churn`; core for `revenue`, `staffing`, `posDemand` and `cashCollection`. Proposed, client to correct; a venue may name the module itself. Always present on a read."},"grain":{"type":"string","enum":["hour","day","week","month"]},"dimensions":{"type":"array","items":{"type":"string"},"description":"Breakdowns forecast directly or reconciled to. **Documented keys (29 September, build; 8.2.12, 8.2.14, 8.2.27):** `product`, `channel`, `timeslot`, `gate`, `outlet`, `customerSegment` and `originCountry`. `customerSegment` is the marketing-crm segment (of those in `segmentIds`, else the membership tier) the guest belonged to on the day of the booking; `originCountry` is the guest profile's country, else the order's billing country, else the channel's market, recorded as `unknown` rather than guessed. **The nightly snapshot (design 2.2 C step 1) carries both for every booking and admission**, so a definition that names them is forecast and reconciled by them. Any other key is accepted and forecast only where the snapshot carries it."},"segmentIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"The marketing-crm segments `customerSegment` breaks down by, in priority order where a guest is in several. Empty means membership tiers."},"horizonDays":{"type":"integer","minimum":1,"maximum":730},"refreshCadence":{"type":"string","enum":["hourly","daily","weekly"]},"producer":{"type":"string","enum":["rule","statistical","model","ensemble"],"description":"Which producer is live (design 3.10). A model is promoted only through `promoteAiRelease`. **`ensemble`** (18 September minutes, M18-16): a weighted blend of the rule and statistical producers, and of a promoted model where one exists; the weights are recorded on each version. Setting `ensemble` never brings in an unpromoted model."},"historyWindowMonths":{"type":"integer","minimum":1,"maximum":60,"default":36,"description":"How much of the venue's own history the statistical producer reads (18 September minutes, M18-16: \"36 months of history\"). Imported history (`importVenueHistory`) counts. Less than the window is not an error: the cold-start setting fills the gap."},"coldStart":{"type":"object","description":"**What the forecast stands on before the venue has history** (29 September, AI functions review; forecasting book p.27 \"New Venue / New Product Problem\"). Day one is never empty: the prior is the venue AI settings (typical weekday and weekend attendance, capacity, opening hours) x the starting pattern for the venue type x the UAE calendar x weather, with bookings on hand as a floor. The statistical producer blends own data in as `(k x prior + n x own) / (k + n)`, with `k` = `priorWeightObservations`. The version's `maturity` says which stage it reached.","properties":{"strategy":{"type":"string","enum":["venueSettings","startingPattern","sisterVenue","categoryBaseline","importedHistory"],"default":"venueSettings","description":"`venueSettings` uses the onboarding figures with the venue-type pattern; `sisterVenue` a venue of the same tenant; `categoryBaseline` a product category's own history; `importedHistory` means an import covers the window and the prior only fills unseen holidays."},"sisterVenueId":{"type":"string","format":"uuid","nullable":true,"description":"For `sisterVenue`. Same tenant only (no data is pooled across tenants, AIP-149)."},"priorWeightObservations":{"type":"integer","minimum":1,"maximum":52,"default":4,"description":"`k`: how many own observations the prior is worth (4 same weekdays by default)."},"startingBandPercent":{"type":"integer","minimum":5,"maximum":80,"default":40,"description":"The width of the range while the prior carries most of the weight (about +/-40%)."}}},"producerRef":{"type":"string","readOnly":true},"shadowProducerRef":{"type":"string","nullable":true,"readOnly":true,"description":"Runs alongside and is recorded, never shown (design 3.5)."},"autoPublish":{"type":"boolean","default":false,"description":"Publish without approval when the quality gates pass (autonomy L4, design 3.8). Otherwise an `AI_APPROVE` holder publishes."},"qualityGates":{"type":"object","additionalProperties":true,"nullable":true,"description":"Completeness, blocking signals and accuracy-regression thresholds a version must pass to publish."},"signalKeys":{"type":"array","items":{"type":"string"},"description":"Signal sources this definition may use (ADM-501)."},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastPoint": {"type":"object","x-ticvai-persistence":"ai.forecast_point","description":"One forecast value with its interval: 10th, 50th and 90th percentile (design 5.6: a range, never a bare percentage). Partitioned by target month. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["versionId","targetStart","p50"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"versionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_version"},"scenarioId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.forecast_scenario","description":"Set where the point belongs to a what-if scenario rather than the version itself."},"targetStart":{"type":"string","format":"date-time"},"targetEnd":{"type":"string","format":"date-time"},"dimensionKey":{"type":"string","nullable":true,"description":"Canonical key of the breakdown, e.g. `product=…;channel=web`."},"p10":{"type":"number","nullable":true},"p50":{"type":"number"},"p90":{"type":"number","nullable":true},"unit":{"type":"string"},"drivers":{"type":"object","additionalProperties":true,"nullable":true,"description":"Component decomposition or SHAP contributions, largest first (ADM-506)."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastScenario": {"type":"object","x-ticvai-persistence":"ai.forecast_scenario","description":"**A what-if against a published version** (ADM-507, ADM-517, BO-931). Changes nothing in production; its points are written with `scenarioId`.","required":["baseVersionId","changes"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string"},"baseVersionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_version"},"changes":{"type":"array","items":{"type":"object","required":["lever"],"properties":{"lever":{"type":"string","enum":["price","capacity","openingHours","weather","event","marketing","staffing","closure"]},"target":{"type":"string","nullable":true},"value":{"type":"object","additionalProperties":true,"nullable":true}}},"minItems":1},"status":{"type":"string","enum":["computing","ready","failed"],"readOnly":true},"result":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"Deltas against the base version by subject and period."},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastVersion": {"type":"object","x-ticvai-persistence":"ai.forecast_version","description":"**An immutable forecast version** (AIP-032): producer, model version, data cut-off, horizon and status. Nothing is overwritten; yesterday's actuals are scored against every earlier version.","required":["definitionId","versionNumber","status","basis"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"definitionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_definition"},"versionNumber":{"type":"integer","minimum":1},"module":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"}],"readOnly":true,"description":"The module of the version's definition (`AiForecastDefinition.module`), copied when the version is produced; the module whose AI publish permission `publishForecastVersion` requires (CHG-FUP-004)."},"status":{"type":"string","enum":["running","draft","awaitingApproval","published","superseded","rejected","failed"],"readOnly":true},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producerRef":{"type":"string"},"modelVersion":{"type":"string","nullable":true},"dataCutoffAt":{"type":"string","format":"date-time","description":"The analytical replica watermark the snapshot was taken at."},"horizonStart":{"type":"string","format":"date-time"},"horizonEnd":{"type":"string","format":"date-time"},"qualityChecks":{"type":"object","additionalProperties":true,"readOnly":true,"description":"Each gate and whether it passed."},"publishedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal","description":"Null where the definition auto-published."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiInsight": {"type":"object","x-ticvai-persistence":"ai.insight","description":"**An insight with a lifecycle** (AIP-181): new, reviewed, accepted or rejected, actioned, measured. Anomalies, forecast deviations, trends and opportunities land here; the narrative binds numbers to results, so a figure can only come from a query (design 8, 5.10).","required":["kind","title","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["anomaly","forecastDeviation","trend","opportunity","executiveSummary","rootCause","forecastThreshold","marketingRecommendation"]},"detectorId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.anomaly_detector"},"metricKey":{"type":"string","nullable":true},"subjectKind":{"type":"string","nullable":true,"enum":["campaign","journey","forecastDefinition","venue"],"description":"What the insight is about where it is not a KPI (29 September, build): a marketing-crm campaign or journey for `marketingRecommendation`, a forecast definition for `forecastThreshold`."},"subjectRef":{"type":"string","nullable":true},"recommendedAction":{"type":"object","additionalProperties":true,"nullable":true,"description":"For `marketingRecommendation`: `{recommendation, parameters}` as `AiMarketingRecommendation`. Applied by a person in the owning module, never here."},"expectedImpact":{"type":"object","additionalProperties":true,"nullable":true,"description":"A range on a named metric (`metric`, `low`, `high`), never a single number (design 5.6)."},"title":{"type":"string"},"narrative":{"type":"string","nullable":true},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"magnitude":{"type":"number","nullable":true},"priority":{"type":"string","enum":["low","medium","high","critical"]},"correlationKey":{"type":"string","nullable":true},"status":{"type":"string","enum":["new","reviewed","accepted","rejected","actioned","measured"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"actionRef":{"type":"string","nullable":true},"measuredImpact":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"detectedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"AiMetricChangeExplanation": {"type":"object","x-ticvai-persistence":"none — computed; written as an ai.insight of kind rootCause when kept","description":"**Why a metric changed** (AIP-176..180, ANL-056): drivers with their contribution, computed from the semantic layer. The narrative binds every figure to a result placeholder (design 8, 5.10).","required":["metricKey","change","drivers"],"properties":{"metricKey":{"type":"string"},"period":{"type":"string"},"comparison":{"type":"string"},"change":{"type":"number"},"changePercent":{"type":"number","nullable":true},"drivers":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string"},"member":{"type":"string"},"contribution":{"type":"number"},"evidence":{"$ref":"#/components/schemas/AiEvidenceItem"}}}},"narrative":{"type":"string","nullable":true},"reliability":{"type":"string","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},"dataAsOf":{"type":"string","format":"date-time"}}},
"AiScenarioComparison": {"type":"object","x-ticvai-persistence":"none — computed from ai.forecast_point","description":"Scenarios side by side against their base version.","required":["scenarios"],"properties":{"scenarios":{"type":"array","items":{"$ref":"#/components/schemas/AiForecastScenario"}},"rows":{"type":"array","items":{"type":"object","properties":{"subject":{"type":"string"},"periodStart":{"type":"string","format":"date-time"},"base":{"type":"number"},"values":{"type":"object","additionalProperties":true,"description":"Scenario id to value."}}}}}},
"AiSignalSource": {"type":"object","x-ticvai-persistence":"ai.signal_source","description":"**A forecast signal** (AIP-199..203, ADM-501): weather (a commercial API, decided 29 September), holidays, calendar, events. Freshness and coverage are recorded; **missing data is stored as unavailable, never defaulted** (AIP-203).","required":["signalKey","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"signalKey":{"type":"string"},"kind":{"type":"string","enum":["weather","publicHoliday","schoolCalendar","religiousCalendar","event","marketing","internal"]},"provider":{"type":"string","nullable":true},"credentialRef":{"type":"string","nullable":true,"description":"A key-vault reference for a paid API, never the key."},"refreshCadence":{"type":"string","enum":["hourly","daily","weekly","manual"]},"coverage":{"type":"number","minimum":0,"maximum":1,"readOnly":true},"freshAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE","CORE_AI_PUBLISH","TICKETING_AI_PUBLISH","ACCESS_AI_PUBLISH","FNB_AI_PUBLISH","RETAIL_AI_PUBLISH","INVENTORY_AI_PUBLISH","SEATING_AI_PUBLISH","MEMBERSHIP_AI_PUBLISH","MARKETING_AI_PUBLISH","RESOURCES_AI_PUBLISH","QUEUE_AI_PUBLISH","TRANSPORT_AI_PUBLISH","GAMES_AI_PUBLISH","MAINTENANCE_AI_PUBLISH","ACCREDITATION_AI_PUBLISH","PARTNER_AI_PUBLISH","ANALYTICS_AI_PUBLISH","BIOMETRIC_IMAGE_VIEW","ACCESS_DIRECTION_SET","REPORT_GOVERNANCE_MANAGE"]},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"SuspensionMode": {"type":"string","description":"Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n","enum":["readOnly","noNewSales","fullLockout"]},
"Tenant": {"x-ticvai-persistence":"control.tenant","type":"object","required":["id","code","name","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"status":{"$ref":"#/components/schemas/TenantStatus"},"suspensionMode":{"$ref":"#/components/schemas/SuspensionMode"},"suspensionReason":{"type":"string","nullable":true},"suspensionEffectiveAt":{"type":"string","format":"date-time","nullable":true,"description":"When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."},"suspensionNoticeMessage":{"$ref":"#/components/schemas/LocalisedText","description":"The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."},"terminationScheduledAt":{"type":"string","format":"date-time","nullable":true,"description":"When `terminateTenant` started the retention window. Null when no termination is under way."},"terminationRetentionUntil":{"type":"string","format":"date-time","nullable":true,"description":"`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."},"terminationReason":{"type":"string","maxLength":1000,"nullable":true},"terminationRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"planId":{"type":"string","format":"uuid","nullable":true},"planName":{"type":"string","nullable":true},"cellCount":{"type":"integer"},"venueCount":{"type":"integer"},"regionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"},"billingEmail":{"type":"string"},"billingAddress":{"type":"string","maxLength":500,"nullable":true,"description":"Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."},"accountManagerPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"activatedAt":{"type":"string","format":"date-time","nullable":true}}},
"TenantStatus": {"type":"string","enum":["onboarding","active","suspended","terminating","terminated"]}
}
```
