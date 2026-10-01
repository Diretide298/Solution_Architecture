# WS119 — AI Forecasting and Predictive Intelligence board 1

**10 screens · 15 operations · 15 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `AI_APPROVE, AI_CONFIGURE, AI_USE`. A control nobody can use must say so,
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

## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `ADM-499` | Forecasting Command Center | B–D | 0 | 0 | 6 | 38 | 0 | 0 | — | notStarted (—) |
| `ADM-500` | Forecast Configuration & Forecasting Strategy | B–D | 33 | 0 | 6 | 9 | 1 | 0 | — | notStarted (—) |
| `ADM-501` | Forecast Data & Signal Configuration | B–D | 0 | 0 | 6 | 8 | 0 | 0 | — | notStarted (—) |
| `ADM-502` | Attendance & Visitation Forecast | B–D | 0 | 0 | 6 | 42 | 0 | 0 | — | notStarted (—) |
| `ADM-503` | Ticket, Product & Timeslot Demand Forecast | B–D | 0 | 12 | 6 | 38 | 1 | 0 | — | notStarted (—) |
| `ADM-504` | Channel & Booking Pace Forecast | B–D | 0 | 24 | 6 | 38 | 0 | 6 | — | notStarted (—) |
| `ADM-505` | Revenue & Commercial Forecast | B–D | 0 | 0 | 6 | 38 | 0 | 0 | — | notStarted (—) |
| `ADM-506` | Forecast Drivers, Confidence & Explainability | B–D | 0 | 24 | 6 | 43 | 0 | 0 | — | notStarted (—) |
| `ADM-507` | Forecast Scenario & What-If Simulator | B–D | 0 | 14 | 6 | 39 | 0 | 0 | — | notStarted (—) |
| `ADM-508` | Forecast Accuracy, Review & Publication Center | A | 0 | 54 | 6 | 5 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-501, ADM-502, ADM-503, ADM-504, ADM-506, ADM-507, ADM-508 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-499` Forecasting Command Center

**Provide management with one central view of expected attendance, demand and revenue across venues and future periods.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `versionId` (navigation) |
| Route | `/analytics/forecasting-command-center-adm-499` |

#### Inputs: what the user enters or picks

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

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

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

**Data it reads**: `listForecastDefinitions` (onLoad, What is forecast); `getForecast` (onLoad, Forecast values)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-500` Forecast Configuration & Forecasting Strategy: *Forecast Configuration & Forecasting Strategy*; carries `definitionKey`
- → `ADM-501` Forecast Data & Signal Configuration: *Forecast Data & Signal Configuration*; carries `definitionKey`
- → `ADM-502` Attendance & Visitation Forecast: *Attendance & Visitation Forecast*
- → `ADM-503` Ticket, Product & Timeslot Demand Forecast: *Ticket, Product & Timeslot Demand Forecast*
- → `ADM-504` Channel & Booking Pace Forecast: *Channel & Booking Pace Forecast*
- → `ADM-505` Revenue & Commercial Forecast: *Revenue & Commercial Forecast*
- → `ADM-506` Forecast Drivers, Confidence & Explainability: *Forecast Drivers, Confidence & Explainability*
- → `ADM-507` Forecast Scenario & What-If Simulator: *Forecast Scenario & What-If Simulator*
- → `ADM-508` Forecast Accuracy, Review & Publication Center: *Forecast Accuracy, Review & Publication Center*; carries `definitionKey`, `versionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The forecasting list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the forecasting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No forecasting yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the forecasting are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listForecastDefinitions` → `AI_USE` (operate) · staff
- `getForecast` → `AI_USE` (operate) · staff
- `exportForecastVersion` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

38 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 26 more | | | | `traceability.json` |

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

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-499?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-500`, `ADM-501`, `ADM-502`, `ADM-503`, `ADM-504`, `ADM-505`, `ADM-506`, `ADM-507`, `ADM-508`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-500` Forecast Configuration & Forecasting Strategy

**Configure what TICVAI should forecast, at what level of detail, for what horizon and how frequently forecasts should be refreshed. This screen establishes the forecasting object.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE` (1 configure, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Fields; Options conceptually) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `definitionKey` (navigation) |
| Route | `/analytics/forecast-configuration-forecasting-strategy-adm-500` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
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
| Revenue | select field | — | — | — | — | — | — |
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

#### Outputs: what the screen shows and produces

**Data it reads**: `listForecastDefinitions` (onLoad, What is forecast)

**Where the user goes next**

- → `ADM-499` Forecasting Command Center: *Back to Forecasting Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The forecast forecasting strategy configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the forecast forecasting strategy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No forecast forecasting strategy configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A `model` producer was requested directly; models are promoted, not set (`model-needs-promotion`).; 409 A run of this definition is in progress. |

#### Permissions

- `listForecastDefinitions` → `AI_USE` (operate) · staff
- `setForecastDefinition` → `AI_CONFIGURE` (configure) · staff
- `runForecast` → `AI_CONFIGURE` (configure) · staff

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
| 8.2.15 | System shall forecast attendance using real-time booking trends. | Unified Operations Dashboard | CONTRACTED | `runForecast` |
| 5.6.37 | The system shall forecast queue congestion and capacity utilization for attractions, ticketing counters and service locations. | F&B & Guest Management | CONTRACTED | data `AiForecastDefinition` |
| 15.4.3 | Seasonal Demand Forecasting - System shall forecast seasonal demand. | Inventory Management | CONTRACTED | data `AiForecastDefinition` |

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

- [ ] Every input above is drawn (33), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-500?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-501` Forecast Data & Signal Configuration

**Define which historical, current and contextual signals may contribute to each forecast.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE` (1 configure, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `definitionKey` (navigation), `signalKey` (navigation) |
| Route | `/analytics/forecast-data-signal-configuration-adm-501` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Weather · Public holiday · School calendar · Religious calendar · Event · Marketing · Internal | `listForecastSignals` ?kind |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save forecast definition (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listForecastSignals` (onLoad, Forecast signals and their freshness)

**Where the user goes next**

- → `ADM-499` Forecasting Command Center: *Back to Forecasting Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The forecast data signal list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the forecast data signal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No forecast data signal yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the forecast data signal are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A `model` producer was requested directly; models are promoted, not set (`model-needs-promotion`). |

#### Permissions

- `setForecastDefinition` → `AI_CONFIGURE` (configure) · staff
- `listForecastSignals` → `AI_USE` (operate) · staff
- `configureForecastSignalSource` → `AI_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-501?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save forecast definition, Cancel.
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-502` Attendance & Visitation Forecast

**Provide detailed prediction of future venue attendance.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE` (1 configure, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `detectorKey` (navigation) |
| Route | `/analytics/attendance-visitation-forecast-adm-502` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

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

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getForecast` (onLoad, Forecast values); `listAiInsights` (onLoad, Forecast threshold alerts (kind forecastThreshold))

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
| Offline (`?state=offline`) | online only |

#### Permissions

- `getForecast` → `AI_USE` (operate) · staff
- `configureAnomalyDetector` → `AI_CONFIGURE` (configure) · staff
- `listAiInsights` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-502` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-502`
- Workshop pack: AI_Forecasting_and_Predictive_Intelligence_Reference.pdf board 1
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 6: Works in Attendance & Visitation Forecast → Provide detailed prediction of future venue attendance.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-502?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-503` Ticket, Product & Timeslot Demand Forecast

**Predict demand at the product and inventory level so TICVAI can understand what customers are likely to buy, not only total attendance.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/ticket-product-timeslot-demand-forecast-adm-503` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Definition key | text field | — | — | `getForecast` ?definitionKey |
| Version | picker: choose a version | — | — | `getForecast` ?versionId |
| From | date and time picker | — | — | `getForecast` ?from |
| To | date and time picker | — | — | `getForecast` ?to |
| Dimension key | text field | — | — | `getForecast` ?dimensionKey |
| Scenario | picker: choose a scenario | — | — | `getForecast` ?scenarioId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every ticket product timeslot** (data table)

| Shows | Format | Notes |
|---|---|---|
| Days before visit | text | not in the schema: `Days Before Visit` |
| Cumulative sales | text | not in the schema: `Cumulative Sales` |
| Current booking curve | text | not in the schema: `Current Booking Curve` |
| Historical average | text | not in the schema: `Historical Average` |
| Forecast final demand | text | not in the schema: `Forecast Final Demand` |
| Product relationships | text | not in the schema: `Product Relationships` |

**The selected ticket product timeslot** (detail panel): The pack groups this record's detail under its own headings: “Family Meal demand typically increases”, “Where enough evidence exists, estimate”.

| Shows | Format | Notes |
|---|---|---|
| Days before visit | text | not in the schema: `Days Before Visit` |
| Cumulative sales | text | not in the schema: `Cumulative Sales` |
| Current booking curve | text | not in the schema: `Current Booking Curve` |
| Historical average | text | not in the schema: `Historical Average` |
| Forecast final demand | text | not in the schema: `Forecast Final Demand` |
| Product relationships | text | not in the schema: `Product Relationships` |

**Data it reads**: `getForecast` (onLoad, Forecast values)

**Where the user goes next**

- → `ADM-499` Forecasting Command Center: *Back to Forecasting Command Center*; carries `versionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ticket product timeslot list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ticket product timeslot untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ticket product timeslot yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the ticket product timeslot are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getForecast` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

38 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 26 more | | | | `traceability.json` |

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

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-503?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-504` Channel & Booking Pace Forecast

**Predict where and when future sales are expected to arrive. This is particularly useful because a venue with 10,000 current bookings may still receive significant B2C, POS, reseller and walk-in volume.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Forecast) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/channel-booking-pace-forecast-adm-504` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Definition key | text field | — | — | `getForecast` ?definitionKey |
| Version | picker: choose a version | — | — | `getForecast` ?versionId |
| From | date and time picker | — | — | `getForecast` ?from |
| To | date and time picker | — | — | `getForecast` ?to |
| Dimension key | text field | — | — | `getForecast` ?dimensionKey |
| Scenario | picker: choose a scenario | — | — | `getForecast` ?scenarioId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every channel booking pace** (data table)

| Shows | Format | Notes |
|---|---|---|
| B2 c website | text | not in the schema: `B2C Website` |
| Mobile app | text | not in the schema: `Mobile App` |
| POS | text | not in the schema: `POS` |
| Flying POS | text | not in the schema: `Flying POS` |
| Kiosk | text | not in the schema: `Kiosk` |
| B2 b | text | not in the schema: `B2B` |
| Reseller | text | not in the schema: `Reseller` |
| OTA / API partners where applicable | text | not in the schema: `OTA / API Partners where applicable` |
| Call center / agent | text | not in the schema: `Call Center / Agent` |
| Walk in | text | not in the schema: `Walk-In` |
| Channel forecast | text | not in the schema: `Channel Forecast` |
| Channel current expected additional final forecast | text | not in the schema: `Channel Current Expected Additional Final Forecast` |

**The selected channel booking pace** (detail panel): The pack groups this record's detail under its own headings: “POS/Walk-In 0 2,950 2,950”.

| Shows | Format | Notes |
|---|---|---|
| B2 c website | text | not in the schema: `B2C Website` |
| Mobile app | text | not in the schema: `Mobile App` |
| POS | text | not in the schema: `POS` |
| Flying POS | text | not in the schema: `Flying POS` |
| Kiosk | text | not in the schema: `Kiosk` |
| B2 b | text | not in the schema: `B2B` |
| Reseller | text | not in the schema: `Reseller` |
| OTA / API partners where applicable | text | not in the schema: `OTA / API Partners where applicable` |
| Call center / agent | text | not in the schema: `Call Center / Agent` |
| Walk in | text | not in the schema: `Walk-In` |
| Channel forecast | text | not in the schema: `Channel Forecast` |
| Channel current expected additional final forecast | text | not in the schema: `Channel Current Expected Additional Final Forecast` |

**Data it reads**: `getForecast` (onLoad, Forecast values)

**Where the user goes next**

- → `ADM-499` Forecasting Command Center: *Back to Forecasting Command Center*; carries `versionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel booking pace list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel booking pace untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel booking pace yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the channel booking pace are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getForecast` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

38 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 26 more | | | | `traceability.json` |

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

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-504?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-505` Revenue & Commercial Forecast

**Forecast future revenue based on predicted sales, attendance, product mix, current pricing and other approved commercial signals.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Revenue KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/revenue-commercial-forecast-adm-505` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Definition key | text field | — | — | `getForecast` ?definitionKey |
| Version | picker: choose a version | — | — | `getForecast` ?versionId |
| From | date and time picker | — | — | `getForecast` ?from |
| To | date and time picker | — | — | `getForecast` ?to |
| Dimension key | text field | — | — | `getForecast` ?dimensionKey |
| Scenario | picker: choose a scenario | — | — | `getForecast` ?scenarioId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Forecast Ticket Revenue** (metric tile)

**Forecast Membership Revenue** (metric tile)

**Forecast Add-On Revenue** (metric tile)

**Forecast F&B Revenue where supported** (metric tile)

**Forecast Retail Revenue where supported** (metric tile)

**Total Forecast Revenue** (metric tile)

**Revenue per Visitor** (metric tile)

**Revenue vs Budget / Target where available** (metric tile)

**Revenue Confidence Range** (metric tile)

**Data it reads**: `getForecast` (onLoad, Forecast values)

**Where the user goes next**

- → `ADM-499` Forecasting Command Center: *Back to Forecasting Command Center*; carries `versionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The revenue commercial forecast list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the revenue commercial forecast untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No revenue commercial forecast yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the revenue commercial forecast are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getForecast` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

38 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 26 more | | | | `traceability.json` |

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

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-505?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-506` Forecast Drivers, Confidence & Explainability

**Explain why the forecast changed and how much uncertainty exists. This is essential because management should not receive only: “Tomorrow attendance = 16,120.” They need to understand the basis and uncertainty. Forecast Attendance 16,120 Confidence Range 15,300 – 17,050 Confidence Status High Key Drivers Example: Current Booking Pace Positive +Strong Saturday Historical Demand Positive +Strong Special Event Positive +Medium Weather Forecast Positive +Medium Current Price Neutral Recent Cancellation Rate Negative Medium Forecast Change Explanation Previous: 15,640 Current: 16,120 Change: +480 Structured explanation: Current booking pace increased above the historical Saturday pattern, while expected weather conditions improved. These signals contributed to an upward revision.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/forecast-drivers-confidence-explainability-adm-506` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

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

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every forecast drivers confidence** (data table)

| Shows | Format | Notes |
|---|---|---|
| Limited historical data | text | not in the schema: `Limited Historical Data` |
| New product | text | not in the schema: `New Product` |
| New event | text | not in the schema: `New Event` |
| Missing weather | text | not in the schema: `Missing Weather` |
| Abnormal promotion | text | not in the schema: `Abnormal Promotion` |
| High cancellation variability | text | not in the schema: `High Cancellation Variability` |
| Unusual booking pattern | text | not in the schema: `Unusual Booking Pattern` |
| Confidence by horizon | text | not in the schema: `Confidence by Horizon` |
| 92% / high | text | not in the schema: `92% / High` |
| 84% / high | text | not in the schema: `84% / High` |
| 71% / medium | text | not in the schema: `71% / Medium` |
| 58% / lower | text | not in the schema: `58% / Lower` |

**The selected forecast drivers confidence** (detail panel): The pack groups this record's detail under its own headings: “Where applicable”, “Ensemble”.

| Shows | Format | Notes |
|---|---|---|
| Limited historical data | text | not in the schema: `Limited Historical Data` |
| New product | text | not in the schema: `New Product` |
| New event | text | not in the schema: `New Event` |
| Missing weather | text | not in the schema: `Missing Weather` |
| Abnormal promotion | text | not in the schema: `Abnormal Promotion` |
| High cancellation variability | text | not in the schema: `High Cancellation Variability` |
| Unusual booking pattern | text | not in the schema: `Unusual Booking Pattern` |
| Confidence by horizon | text | not in the schema: `Confidence by Horizon` |
| 92% / high | text | not in the schema: `92% / High` |
| 84% / high | text | not in the schema: `84% / High` |
| 71% / medium | text | not in the schema: `71% / Medium` |
| 58% / lower | text | not in the schema: `58% / Lower` |

**Data it reads**: `listForecastVersions` (onLoad, Forecast versions); `getForecast` (onLoad, Forecast values); `getForecastAccuracy` (onLoad, Measured forecast accuracy)

**Where the user goes next**

- → `ADM-499` Forecasting Command Center: *Back to Forecasting Command Center*; carries `versionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The forecast drivers confidence list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the forecast drivers confidence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No forecast drivers confidence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the forecast drivers confidence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `explainMetricChange` → `AI_USE` (operate) · staff
- `listForecastVersions` → `AI_USE` (operate) · staff
- `getForecast` → `AI_USE` (operate) · staff
- `getForecastAccuracy` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

43 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 31 more | | | | `traceability.json` |

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
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-506?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-507` Forecast Scenario & What-If Simulator

**Allow management to test possible future conditions without changing production configuration. This is one of the most important screens.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/forecast-scenario-what-if-simulator-adm-507` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Definition key | text field | — | — | `getForecast` ?definitionKey |
| Version | picker: choose a version | — | — | `getForecast` ?versionId |
| From | date and time picker | — | — | `getForecast` ?from |
| To | date and time picker | — | — | `getForecast` ?to |
| Dimension key | text field | — | — | `getForecast` ?dimensionKey |
| Scenario | picker: choose a scenario | — | — | `getForecast` ?scenarioId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

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

**Data it reads**: `getForecast` (onLoad, Forecast values)

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
| Offline (`?state=offline`) | online only |

#### Permissions

- `getForecast` → `AI_USE` (operate) · staff
- `createForecastScenario` → `AI_USE` (operate) · staff
- `compareForecastScenarios` → `AI_USE` (operate) · staff

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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-507` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS12 AI Forecasting and Predictive Intelligence Board 1.dc.html#adm-507`
- Workshop pack: AI_Forecasting_and_Predictive_Intelligence_Reference.pdf board 1
- Flow F228 *AI Forecasting and Predictive Intelligence board 1: Forecasting Command Center*, step 16: Works in Forecast Scenario & What-If Simulator → Allow management to test possible future conditions without changing production configuration. This is one of the most important screens.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-507?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-508` Forecast Accuracy, Review & Publication Center

**Measure forecast quality over time and publish approved forecast outputs for use by other TICVAI modules. A forecasting system should continuously answer: How accurate have our forecasts actually been? Forecast vs Actual Example:**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block A · ticket #20751 (APP-SETUP-ADM-508) |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE` (2 operate, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Analyze) and no metric row |
| Offline | online only |
| Opens with | `definitionKey` (navigation), `versionId` (navigation) |
| Route | `/analytics/forecast-accuracy-review-publication-center-adm-508` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Definition key | text field | — | — | `listForecastVersions` ?definitionKey |
| Status | select | — | Running · Draft · Awaiting approval · Published · Superseded · Rejected · Failed | `listForecastVersions` ?status |
| Definition key | text field | — | — | `getForecastAccuracy` ?definitionKey |
| Horizon days | number field (days) | — | — | `getForecastAccuracy` ?horizonDays |
| From | date and time picker | — | — | `getForecastAccuracy` ?from |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every forecast accuracy review** (data table)

| Shows | Format | Notes |
|---|---|---|
| Venue | text | not in the schema: `Venue` |
| Product | text | not in the schema: `Product` |
| Channel | text | not in the schema: `Channel` |
| Timeslot | text | not in the schema: `Timeslot` |
| Day type | text | not in the schema: `Day Type` |
| Forecast horizon | text | not in the schema: `Forecast Horizon` |
| Model | text | not in the schema: `Model` |
| Event type | text | not in the schema: `Event Type` |
| Forecast bias | text | not in the schema: `Forecast Bias` |
| Saturday walk in | text | not in the schema: `Saturday Walk-In` |
| 4% | text | not in the schema: `7.4%` |
| MODEL REVIEW RECOMMENDED | text | not in the schema: `MODEL REVIEW RECOMMENDED` |
| Forecast version | text | not in the schema: `Forecast Version` |
| Forecast ID | text | not in the schema: `Forecast ID` |
| Version | text | not in the schema: `Version` |
| Generated time | text | not in the schema: `Generated Time` |
| Model version | text | not in the schema: `Model Version` |
| Data cut off | text | not in the schema: `Data Cut-Off` |
| Confidence | text | not in the schema: `Confidence` |
| Status | text | not in the schema: `Status` |
| Publication status | text | not in the schema: `Publication Status` |
| Draft | text | not in the schema: `Draft` |
| Generated | text | not in the schema: `Generated` |
| Reviewed | text | not in the schema: `Reviewed` |
| Published | text | not in the schema: `Published` |
| Superseded | text | not in the schema: `Superseded` |
| Archived | text | not in the schema: `Archived` |

**The selected forecast accuracy review** (detail panel): The pack groups this record's detail under its own headings: “Next Day”, “Consumers”, “DATA PREPARATION / FEATURE LAYER”, “CONFIDENCE & EXPLAINABILITY”, “SCENARIO ENGINE”, “Conceptually”.

| Shows | Format | Notes |
|---|---|---|
| Venue | text | not in the schema: `Venue` |
| Product | text | not in the schema: `Product` |
| Channel | text | not in the schema: `Channel` |
| Timeslot | text | not in the schema: `Timeslot` |
| Day type | text | not in the schema: `Day Type` |
| Forecast horizon | text | not in the schema: `Forecast Horizon` |
| Model | text | not in the schema: `Model` |
| Event type | text | not in the schema: `Event Type` |
| Forecast bias | text | not in the schema: `Forecast Bias` |
| Saturday walk in | text | not in the schema: `Saturday Walk-In` |
| 4% | text | not in the schema: `7.4%` |
| MODEL REVIEW RECOMMENDED | text | not in the schema: `MODEL REVIEW RECOMMENDED` |
| Forecast version | text | not in the schema: `Forecast Version` |
| Forecast ID | text | not in the schema: `Forecast ID` |
| Version | text | not in the schema: `Version` |
| Generated time | text | not in the schema: `Generated Time` |
| Model version | text | not in the schema: `Model Version` |
| Data cut off | text | not in the schema: `Data Cut-Off` |
| Confidence | text | not in the schema: `Confidence` |
| Status | text | not in the schema: `Status` |
| Publication status | text | not in the schema: `Publication Status` |
| Draft | text | not in the schema: `Draft` |
| Generated | text | not in the schema: `Generated` |
| Reviewed | text | not in the schema: `Reviewed` |
| Published | text | not in the schema: `Published` |
| Superseded | text | not in the schema: `Superseded` |
| Archived | text | not in the schema: `Archived` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listForecastVersions` (onLoad, Forecast versions); `getForecastAccuracy` (onLoad, Measured forecast accuracy)

**Where the user goes next**

- → `ADM-499` Forecasting Command Center: *Back to Forecasting Command Center*; carries `versionId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The forecast accuracy review list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the forecast accuracy review untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No forecast accuracy review yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the forecast accuracy review are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A run of this definition is in progress.; 409 Not publishable: a quality gate failed (`quality-gate-failed`) or the version is not the latest draft (`version-not-current`). |

#### Permissions

- `runForecast` → `AI_CONFIGURE` (configure) · staff
- `listForecastVersions` → `AI_USE` (operate) · staff
- `publishForecastVersion` → `AI_APPROVE` (operate) · staff
- `getForecastAccuracy` → `AI_USE` (operate) · staff
- `exportForecastVersion` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.2.15 | System shall forecast attendance using real-time booking trends. | Unified Operations Dashboard | CONTRACTED | `runForecast` |
| 8.2.53 | System shall maintain forecast history. | Unified Operations Dashboard | CONTRACTED | `listForecastVersions` |
| 8.2.18 | System shall provide forecast accuracy measurements. | Unified Operations Dashboard | CONTRACTED | `getForecastAccuracy` |
| 8.2.19 | System shall compare forecasted attendance against actual attendance. | Unified Operations Dashboard | CONTRACTED | `getForecastAccuracy` |
| 8.2.34 | System shall compare forecasted revenue against actual revenue. | Unified Operations Dashboard | CONTRACTED | `getForecastAccuracy` |

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

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (54 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-508?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: .
- [ ] Every transition is wired: `ADM-499`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
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
"publishForecastVersion": {"method":"POST","path":"/forecast-versions/{versionId}/publish","contract":"ai","summary":"Publish a forecast version","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiForecastVersion"},
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
"AiForecastDefinition": {"type":"object","x-ticvai-persistence":"ai.forecast_definition","description":"**What is forecast, at what grain, for what horizon, how often and by which producer** (design 3.1 Forecast, 5.2; ADM-500). One forecasting service for the platform: BI's extra subjects are definitions here, not a second forecaster (AIP-036, AIP-037).","required":["definitionKey","subject","grain","horizonDays","producer"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"definitionKey":{"type":"string"},"name":{"type":"string"},"subject":{"type":"string","enum":["attendance","arrivalPattern","productDemand","timeslotDemand","channelPace","revenue","occupancy","attractionUtilisation","queue","entryFlow","staffing","posDemand","fnbDemand","retailDemand","stockDemand","resourceDemand","refunds","cashCollection","membershipRenewals","churn"]},"grain":{"type":"string","enum":["hour","day","week","month"]},"dimensions":{"type":"array","items":{"type":"string"},"description":"Breakdowns forecast directly or reconciled to. **Documented keys (29 September, build; 8.2.12, 8.2.14, 8.2.27):** `product`, `channel`, `timeslot`, `gate`, `outlet`, `customerSegment` and `originCountry`. `customerSegment` is the marketing-crm segment (of those in `segmentIds`, else the membership tier) the guest belonged to on the day of the booking; `originCountry` is the guest profile's country, else the order's billing country, else the channel's market, recorded as `unknown` rather than guessed. **The nightly snapshot (design 2.2 C step 1) carries both for every booking and admission**, so a definition that names them is forecast and reconciled by them. Any other key is accepted and forecast only where the snapshot carries it."},"segmentIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"The marketing-crm segments `customerSegment` breaks down by, in priority order where a guest is in several. Empty means membership tiers."},"horizonDays":{"type":"integer","minimum":1,"maximum":730},"refreshCadence":{"type":"string","enum":["hourly","daily","weekly"]},"producer":{"type":"string","enum":["rule","statistical","model","ensemble"],"description":"Which producer is live (design 3.10). A model is promoted only through `promoteAiRelease`. **`ensemble`** (18 September minutes, M18-16): a weighted blend of the rule and statistical producers, and of a promoted model where one exists; the weights are recorded on each version. Setting `ensemble` never brings in an unpromoted model."},"historyWindowMonths":{"type":"integer","minimum":1,"maximum":60,"default":36,"description":"How much of the venue's own history the statistical producer reads (18 September minutes, M18-16: \"36 months of history\"). Imported history (`importVenueHistory`) counts. Less than the window is not an error: the cold-start setting fills the gap."},"coldStart":{"type":"object","description":"**What the forecast stands on before the venue has history** (29 September, AI functions review; forecasting book p.27 \"New Venue / New Product Problem\"). Day one is never empty: the prior is the venue AI settings (typical weekday and weekend attendance, capacity, opening hours) x the starting pattern for the venue type x the UAE calendar x weather, with bookings on hand as a floor. The statistical producer blends own data in as `(k x prior + n x own) / (k + n)`, with `k` = `priorWeightObservations`. The version's `maturity` says which stage it reached.","properties":{"strategy":{"type":"string","enum":["venueSettings","startingPattern","sisterVenue","categoryBaseline","importedHistory"],"default":"venueSettings","description":"`venueSettings` uses the onboarding figures with the venue-type pattern; `sisterVenue` a venue of the same tenant; `categoryBaseline` a product category's own history; `importedHistory` means an import covers the window and the prior only fills unseen holidays."},"sisterVenueId":{"type":"string","format":"uuid","nullable":true,"description":"For `sisterVenue`. Same tenant only (no data is pooled across tenants, AIP-149)."},"priorWeightObservations":{"type":"integer","minimum":1,"maximum":52,"default":4,"description":"`k`: how many own observations the prior is worth (4 same weekdays by default)."},"startingBandPercent":{"type":"integer","minimum":5,"maximum":80,"default":40,"description":"The width of the range while the prior carries most of the weight (about +/-40%)."}}},"producerRef":{"type":"string","readOnly":true},"shadowProducerRef":{"type":"string","nullable":true,"readOnly":true,"description":"Runs alongside and is recorded, never shown (design 3.5)."},"autoPublish":{"type":"boolean","default":false,"description":"Publish without approval when the quality gates pass (autonomy L4, design 3.8). Otherwise an `AI_APPROVE` holder publishes."},"qualityGates":{"type":"object","additionalProperties":true,"nullable":true,"description":"Completeness, blocking signals and accuracy-regression thresholds a version must pass to publish."},"signalKeys":{"type":"array","items":{"type":"string"},"description":"Signal sources this definition may use (ADM-501)."},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastPoint": {"type":"object","x-ticvai-persistence":"ai.forecast_point","description":"One forecast value with its interval: 10th, 50th and 90th percentile (design 5.6: a range, never a bare percentage). Partitioned by target month. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["versionId","targetStart","p50"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"versionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_version"},"scenarioId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.forecast_scenario","description":"Set where the point belongs to a what-if scenario rather than the version itself."},"targetStart":{"type":"string","format":"date-time"},"targetEnd":{"type":"string","format":"date-time"},"dimensionKey":{"type":"string","nullable":true,"description":"Canonical key of the breakdown, e.g. `product=…;channel=web`."},"p10":{"type":"number","nullable":true},"p50":{"type":"number"},"p90":{"type":"number","nullable":true},"unit":{"type":"string"},"drivers":{"type":"object","additionalProperties":true,"nullable":true,"description":"Component decomposition or SHAP contributions, largest first (ADM-506)."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastScenario": {"type":"object","x-ticvai-persistence":"ai.forecast_scenario","description":"**A what-if against a published version** (ADM-507, ADM-517, BO-931). Changes nothing in production; its points are written with `scenarioId`.","required":["baseVersionId","changes"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string"},"baseVersionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_version"},"changes":{"type":"array","items":{"type":"object","required":["lever"],"properties":{"lever":{"type":"string","enum":["price","capacity","openingHours","weather","event","marketing","staffing","closure"]},"target":{"type":"string","nullable":true},"value":{"type":"object","additionalProperties":true,"nullable":true}}},"minItems":1},"status":{"type":"string","enum":["computing","ready","failed"],"readOnly":true},"result":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"Deltas against the base version by subject and period."},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastVersion": {"type":"object","x-ticvai-persistence":"ai.forecast_version","description":"**An immutable forecast version** (AIP-032): producer, model version, data cut-off, horizon and status. Nothing is overwritten; yesterday's actuals are scored against every earlier version.","required":["definitionId","versionNumber","status","basis"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"definitionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_definition"},"versionNumber":{"type":"integer","minimum":1},"status":{"type":"string","enum":["running","draft","awaitingApproval","published","superseded","rejected","failed"],"readOnly":true},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producerRef":{"type":"string"},"modelVersion":{"type":"string","nullable":true},"dataCutoffAt":{"type":"string","format":"date-time","description":"The analytical replica watermark the snapshot was taken at."},"horizonStart":{"type":"string","format":"date-time"},"horizonEnd":{"type":"string","format":"date-time"},"qualityChecks":{"type":"object","additionalProperties":true,"readOnly":true,"description":"Each gate and whether it passed."},"publishedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal","description":"Null where the definition auto-published."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiInsight": {"type":"object","x-ticvai-persistence":"ai.insight","description":"**An insight with a lifecycle** (AIP-181): new, reviewed, accepted or rejected, actioned, measured. Anomalies, forecast deviations, trends and opportunities land here; the narrative binds numbers to results, so a figure can only come from a query (design 8, 5.10).","required":["kind","title","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["anomaly","forecastDeviation","trend","opportunity","executiveSummary","rootCause","forecastThreshold","marketingRecommendation"]},"detectorId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.anomaly_detector"},"metricKey":{"type":"string","nullable":true},"subjectKind":{"type":"string","nullable":true,"enum":["campaign","journey","forecastDefinition","venue"],"description":"What the insight is about where it is not a KPI (29 September, build): a marketing-crm campaign or journey for `marketingRecommendation`, a forecast definition for `forecastThreshold`."},"subjectRef":{"type":"string","nullable":true},"recommendedAction":{"type":"object","additionalProperties":true,"nullable":true,"description":"For `marketingRecommendation`: `{recommendation, parameters}` as `AiMarketingRecommendation`. Applied by a person in the owning module, never here."},"expectedImpact":{"type":"object","additionalProperties":true,"nullable":true,"description":"A range on a named metric (`metric`, `low`, `high`), never a single number (design 5.6)."},"title":{"type":"string"},"narrative":{"type":"string","nullable":true},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"magnitude":{"type":"number","nullable":true},"priority":{"type":"string","enum":["low","medium","high","critical"]},"correlationKey":{"type":"string","nullable":true},"status":{"type":"string","enum":["new","reviewed","accepted","rejected","actioned","measured"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"actionRef":{"type":"string","nullable":true},"measuredImpact":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"detectedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"AiMetricChangeExplanation": {"type":"object","x-ticvai-persistence":"none — computed; written as an ai.insight of kind rootCause when kept","description":"**Why a metric changed** (AIP-176..180, ANL-056): drivers with their contribution, computed from the semantic layer. The narrative binds every figure to a result placeholder (design 8, 5.10).","required":["metricKey","change","drivers"],"properties":{"metricKey":{"type":"string"},"period":{"type":"string"},"comparison":{"type":"string"},"change":{"type":"number"},"changePercent":{"type":"number","nullable":true},"drivers":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string"},"member":{"type":"string"},"contribution":{"type":"number"},"evidence":{"$ref":"#/components/schemas/AiEvidenceItem"}}}},"narrative":{"type":"string","nullable":true},"reliability":{"type":"string","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},"dataAsOf":{"type":"string","format":"date-time"}}},
"AiScenarioComparison": {"type":"object","x-ticvai-persistence":"none — computed from ai.forecast_point","description":"Scenarios side by side against their base version.","required":["scenarios"],"properties":{"scenarios":{"type":"array","items":{"$ref":"#/components/schemas/AiForecastScenario"}},"rows":{"type":"array","items":{"type":"object","properties":{"subject":{"type":"string"},"periodStart":{"type":"string","format":"date-time"},"base":{"type":"number"},"values":{"type":"object","additionalProperties":true,"description":"Scenario id to value."}}}}}},
"AiSignalSource": {"type":"object","x-ticvai-persistence":"ai.signal_source","description":"**A forecast signal** (AIP-199..203, ADM-501): weather (a commercial API, decided 29 September), holidays, calendar, events. Freshness and coverage are recorded; **missing data is stored as unavailable, never defaulted** (AIP-203).","required":["signalKey","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"signalKey":{"type":"string"},"kind":{"type":"string","enum":["weather","publicHoliday","schoolCalendar","religiousCalendar","event","marketing","internal"]},"provider":{"type":"string","nullable":true},"credentialRef":{"type":"string","nullable":true,"description":"A key-vault reference for a paid API, never the key."},"refreshCadence":{"type":"string","enum":["hourly","daily","weekly","manual"]},"coverage":{"type":"number","minimum":0,"maximum":1,"readOnly":true},"freshAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]}
}
```
