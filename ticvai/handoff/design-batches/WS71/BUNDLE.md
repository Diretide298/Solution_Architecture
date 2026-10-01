# WS71 — Unified BI Reporting and AI Analytics Platform board 10

**10 screens · 13 operations · 16 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `REPORT_MANAGE, REPORT_VIEW_TENANT, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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
| `ANL-061` | BI & Analytics Administration Command Center | B–D | 0 | 2 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ANL-062` | Enterprise KPI Library | B–D | 0 | 28 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ANL-063` | KPI Targets, Thresholds & Scorecards | B–D | 8 | 0 | 5 | 0 | 2 | 0 | — | notStarted (—) |
| `ANL-064` | Benchmark & Comparative Analytics Configuration | B–D | 12 | 8 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ANL-065` | Data Source & Integration Registry | B–D | 0 | 20 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-066` | Semantic Model & Business Data Catalogue | A | 0 | 10 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-067` | Data Refresh, Pipeline & Data Health Monitor | B–D | 0 | 14 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-068` | Embedded BI, Workspace & Tenant Administration | B–D | 7 | 0 | 5 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-069` | Analytics Performance, Usage & Cost Monitor | B–D | 0 | 12 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-070` | Analytics Governance, Security & Audit Center | B–D | 0 | 34 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ANL-062, ANL-065, ANL-066, ANL-070 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ANL-061` BI & Analytics Administration Command Center

**Provide administrators with one consolidated view of the health and governance of the TICVAI analytics platform.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each component shall show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/bi-analytics-administration-command-center-anl-061` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getAnalyticsUsage` ?from |
| Group by | radio group | — | Report · Dashboard · User · Venue | `getAnalyticsUsage` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Dashboards** (metric tile)

**Active Reports** (metric tile)

**Published KPIs** (metric tile)

**Connected Data Sources** (metric tile)

**Active Datasets** (metric tile)

**Data Refresh Success %** (metric tile)

**Data Quality Score** (metric tile)

**Failed Refreshes** (metric tile)

**BI Service Health** (metric tile)

**AI Analytics Health** (metric tile)

**Active Alerts** (metric tile)

**Analytics Users** (metric tile)

**Every analytics administration** (data table)

| Shows | Format | Notes |
|---|---|---|
| Healthy / warning / critical / offline | text | not in the schema: `Healthy / Warning / Critical / Offline` |

**The selected analytics administration** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Healthy / warning / critical / offline | text | not in the schema: `Healthy / Warning / Critical / Offline` |

**Data it reads**: `getAnalyticsUsage` (onLoad, Estate at a glance); `listAnalyticsPipelines` (onLoad, Data health)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Back to Executive Command Center*
- → `ANL-070` Analytics Governance, Security & Audit Center: *Analytics Governance, Security & Audit Center*
- → `ANL-062` Enterprise KPI Library: *Enterprise KPI Library*
- → `ANL-063` KPI Targets, Thresholds & Scorecards: *KPI Targets, Thresholds & Scorecards*
- → `ANL-064` Benchmark & Comparative Analytics Configuration: *Benchmark & Comparative Analytics Configuration*
- → `ANL-065` Data Source & Integration Registry: *Data Source & Integration Registry*
- → `ANL-066` Semantic Model & Business Data Catalogue: *Semantic Model & Business Data Catalogue*
- → `ANL-067` Data Refresh, Pipeline & Data Health Monitor: *Data Refresh, Pipeline & Data Health Monitor*
- → `ANL-068` Embedded BI, Workspace & Tenant Administration: *Embedded BI, Workspace & Tenant Administration*
- → `ANL-069` Analytics Performance, Usage & Cost Monitor: *Analytics Performance, Usage & Cost Monitor*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The analytics administration list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the analytics administration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No analytics administration yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the analytics administration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getAnalyticsUsage` → `REPORT_VIEW_TENANT` (operate) · staff
- `listAnalyticsPipelines` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- KPI/benchmarking admin board defines each KPI's target, data sources and rules, and shows why a KPI is failing and what actions could help meet it. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-720)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-061` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-061`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 1: Opens BI & Analytics Administration Command Center → Provide administrators with one consolidated view of the health and governance of the TICVAI analytics platform.
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F180 branch at step 1 (expected): when Nothing has been set up on BI & Analytics Administration Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F180 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-061?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-001`, `ANL-070`, `ANL-062`, `ANL-063`, `ANL-064`, `ANL-065`, `ANL-066`, `ANL-067`, `ANL-068`, `ANL-069`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-062` Enterprise KPI Library

**Maintain the authoritative catalogue of approved TICVAI business KPIs. This is essential because every dashboard must use the same definition of a metric.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_TENANT` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§KPI Categories; KPI Status) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/enterprise-kpi-library-anl-062` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every enterprise kpi** (data table)

| Shows | Format | Notes |
|---|---|---|
| Executive | text | not in the schema: `Executive` |
| Sales | text | not in the schema: `Sales` |
| Revenue | text | not in the schema: `Revenue` |
| Finance | text | not in the schema: `Finance` |
| Operations | text | not in the schema: `Operations` |
| Access | text | not in the schema: `Access` |
| Customer | text | not in the schema: `Customer` |
| Membership | text | not in the schema: `Membership` |
| Loyalty | text | not in the schema: `Loyalty` |
| Marketing | text | not in the schema: `Marketing` |
| F&B | text | not in the schema: `F&B` |
| Retail | text | not in the schema: `Retail` |
| Inventory | text | not in the schema: `Inventory` |
| Resources | text | not in the schema: `Resources` |

**The selected enterprise kpi** (detail panel): The pack groups this record's detail under its own headings: “Formula”.

| Shows | Format | Notes |
|---|---|---|
| Executive | text | not in the schema: `Executive` |
| Sales | text | not in the schema: `Sales` |
| Revenue | text | not in the schema: `Revenue` |
| Finance | text | not in the schema: `Finance` |
| Operations | text | not in the schema: `Operations` |
| Access | text | not in the schema: `Access` |
| Customer | text | not in the schema: `Customer` |
| Membership | text | not in the schema: `Membership` |
| Loyalty | text | not in the schema: `Loyalty` |
| Marketing | text | not in the schema: `Marketing` |
| F&B | text | not in the schema: `F&B` |
| Retail | text | not in the schema: `Retail` |
| Inventory | text | not in the schema: `Inventory` |
| Resources | text | not in the schema: `Resources` |

**Data it reads**: `listKpis` (onLoad, The enterprise library)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The enterprise kpi list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the enterprise kpi untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No enterprise kpi yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the enterprise kpi are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listKpis` → `REPORT_VIEW_TENANT` (operate) · staff
- `createKpi` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- KPI/benchmarking admin board defines each KPI's target, data sources and rules, and shows why a KPI is failing and what actions could help meet it. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-720)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-062` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-062`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 2: Works in Enterprise KPI Library → Maintain the authoritative catalogue of approved TICVAI business KPIs. This is essential because every dashboard must use the same definition of a metric.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-062?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_TENANT`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-063` KPI Targets, Thresholds & Scorecards

**Centrally configure performance targets and thresholds used throughout TICVAI analytics.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_VENUE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Targets may be configured by) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `kpiId` (navigation) |
| Route | `/analytics/kpi-targets-thresholds-scorecards-anl-063` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Organization | select field | — | — | — | — | — | — |
| Site | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Attraction | select field | — | — | — | — | — | — |
| Business Unit | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Period | select field | — | — | — | — | — | — |

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

#### Outputs: what the screen shows and produces

**Data it reads**: `getKpiValues` (onLoad, Where they stand)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The kpi targets thresholds configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the kpi targets thresholds untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No kpi targets thresholds configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `setKpiTargets` → `REPORT_MANAGE` (configure) · staff
- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- KPI/benchmarking admin board defines each KPI's target, data sources and rules, and shows why a KPI is failing and what actions could help meet it. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-720)*
- KPI threshold configuration defines normal/warning/critical bands per metric (e.g. capacity below 80% normal, 80-90% warning, above 95% critical), shown as status on the dashboard. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-704)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-063` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-063`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 4: Works in KPI Targets, Thresholds & Scorecards → Centrally configure performance targets and thresholds used throughout TICVAI analytics.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-063?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-064` Benchmark & Comparative Analytics Configuration

**Define how TICVAI compares performance between sites, periods and peer groups.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_TENANT` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Support metrics such as) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/benchmark-comparative-analytics-configuration-anl-064` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Scope path | text field | optional | — | — | — | Sends `?scopePath=` to `listSiteNormalisationBases`. | `listSiteNormalisationBases` ?scopePath |
| Period from | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?periodFrom=` to `listSiteNormalisationBases`. | `listSiteNormalisationBases` ?periodFrom |
| Period to | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?periodTo=` to `listSiteNormalisationBases`. | `listSiteNormalisationBases` ?periodTo |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpi | picker: choose a kpi | — | — | `getAnalyticsBenchmark` ?kpiId |
| Scope paths | text field | — | — | `getAnalyticsBenchmark` ?scopePaths |
| Normalise by | radio group | — | None · Per visitor · Per operating hour · Per staffed position · Per square metre | `getAnalyticsBenchmark` ?normaliseBy |

**Form: Save site normalisation basis** (modal, opened by *Save site normalisation basis*; *Save site normalisation basis* calls `setSiteNormalisationBasis`, *Cancel* sends nothing)

**Collects what `setSiteNormalisationBasis` sends before it is called.** Required: `bases`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Bases `bases` | repeatable rows | required | — | at least 1 | — | — | `setSiteNormalisationBasis` body |
| ID `bases[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `setSiteNormalisationBasis` body |
| Scope path `bases[].scopePath` | text field | required | — | — | — | The site (venue scope) the basis applies to. | `setSiteNormalisationBasis` body |
| Period start `bases[].periodStart` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setSiteNormalisationBasis` body |
| Period end `bases[].periodEnd` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setSiteNormalisationBasis` body |
| Visitors `bases[].visitors` | number field | optional | — | min 0 | — | `perVisitor`. | `setSiteNormalisationBasis` body |
| Operating hours `bases[].operatingHours` | number field (hours) | optional | — | min 0 | — | `perOperatingHour`. | `setSiteNormalisationBasis` body |
| Staffed positions `bases[].staffedPositions` | number field | optional | — | min 0 | — | `perStaffedPosition`. Average positions staffed over the period. | `setSiteNormalisationBasis` body |
| Area square metres `bases[].areaSquareMetres` | number field | optional | — | min 0 | — | `perSquareMetre`. Operated area. | `setSiteNormalisationBasis` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 422 A period ends before it starts, or overlaps another basis for the same site.

#### Outputs: what the screen shows and produces

**Shown**

**Revenue per Visitor** (metric tile)

**Transactions per 1,000 Visitors** (metric tile)

**Entries per Gate per Hour** (metric tile)

**Incidents per 10,000 Visitors** (metric tile)

**Revenue per m² where applicable** (metric tile)

**Revenue per Operating Hour** (metric tile)

**Utilization %** (metric tile)

**Every site normalisation basis** (data table, from `listSiteNormalisationBases`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Scope path | text | The site (venue scope) the basis applies to. |
| Period start | 1 Oct 2026 | — |
| Period end | 1 Oct 2026 | — |
| Visitors | 1,234 | `perVisitor`. |
| Operating hours | 1,234.5 | `perOperatingHour`. |
| Staffed positions | 1,234.5 | `perStaffedPosition`. Average positions staffed over the period. |
| Area square metres | 1,234.5 | `perSquareMetre`. Operated area. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save site normalisation basis (primary button) | `setSiteNormalisationBasis` PUT `/site-normalisation-bases` | inline | SiteNormalisationBasis[] | 403 Authenticated but not permitted at the requested scope; 422 A period ends before it starts, or overlaps another basis for the same site. | gated `REPORT_MANAGE`; opens modal first |

**Data it reads**: `getAnalyticsBenchmark` (onLoad, Configure the comparison basis); `listSiteNormalisationBases` (onLoad, The denominators each site is benchmarked by)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The benchmark comparative analytics list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the benchmark comparative analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No benchmark comparative analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the benchmark comparative analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A period ends before it starts, or overlaps another basis for the same site. |

#### Permissions

- `getAnalyticsBenchmark` → `REPORT_VIEW_TENANT` (operate) · staff
- `listSiteNormalisationBases` → `REPORT_VIEW_TENANT` (operate) · staff
- `setSiteNormalisationBasis` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- KPI/benchmarking admin board defines each KPI's target, data sources and rules, and shows why a KPI is failing and what actions could help meet it. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-720)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-064` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-064`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 6: Works in Benchmark & Comparative Analytics Configuration → Define how TICVAI compares performance between sites, periods and peer groups.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (403, 422).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-064?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save site normalisation basis.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_TENANT`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-065` Data Source & Integration Registry

**Maintain a centralized catalogue of data sources feeding the analytics platform.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/data-source-integration-registry-anl-065` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every data source integration** (data table)

| Shows | Format | Notes |
|---|---|---|
| Source name | text | not in the schema: `Source Name` |
| Source type | text | not in the schema: `Source Type` |
| Owner | text | not in the schema: `Owner` |
| Connection | text | not in the schema: `Connection` |
| Authentication method | text | not in the schema: `Authentication Method` |
| Refresh type | text | not in the schema: `Refresh Type` |
| Last sync | text | not in the schema: `Last Sync` |
| Records processed | text | not in the schema: `Records Processed` |
| Status | text | not in the schema: `Status` |
| Data classification | text | not in the schema: `Data Classification` |

**The selected data source integration** (detail panel): The pack groups this record's detail under its own headings: “Important Security Principle”.

| Shows | Format | Notes |
|---|---|---|
| Source name | text | not in the schema: `Source Name` |
| Source type | text | not in the schema: `Source Type` |
| Owner | text | not in the schema: `Owner` |
| Connection | text | not in the schema: `Connection` |
| Authentication method | text | not in the schema: `Authentication Method` |
| Refresh type | text | not in the schema: `Refresh Type` |
| Last sync | text | not in the schema: `Last Sync` |
| Records processed | text | not in the schema: `Records Processed` |
| Status | text | not in the schema: `Status` |
| Data classification | text | not in the schema: `Data Classification` |

**Data it reads**: `listAnalyticsPipelines` (onLoad, Sources and integrations)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data source integration list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data source integration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data source integration yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data source integration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAnalyticsPipelines` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-065` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-065`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 8: Works in Data Source & Integration Registry → Maintain a centralized catalogue of data sources feeding the analytics platform.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-065?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-066` Semantic Model & Business Data Catalogue

**Create the governed business layer between raw data and dashboards/AI. This is one of the most important technical screens in Board 10.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block A · ticket #20784 (APP-SETUP-ANL-066) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_TENANT` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Detect) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/semantic-model-business-data-catalogue-anl-066` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every semantic model business** (data table)

| Shows | Format | Notes |
|---|---|---|
| Missing relationships | text | not in the schema: `Missing relationships` |
| Circular relationships | text | not in the schema: `Circular relationships` |
| Duplicate aggregation risk | text | not in the schema: `Duplicate aggregation risk` |
| Invalid cardinality | text | not in the schema: `Invalid cardinality` |
| Broken references | text | not in the schema: `Broken references` |

**The selected semantic model business** (detail panel): The pack groups this record's detail under its own headings: “Customer”, “Order”, “Ticket”, “Admission”, “F&B Sale”.

| Shows | Format | Notes |
|---|---|---|
| Missing relationships | text | not in the schema: `Missing relationships` |
| Circular relationships | text | not in the schema: `Circular relationships` |
| Duplicate aggregation risk | text | not in the schema: `Duplicate aggregation risk` |
| Invalid cardinality | text | not in the schema: `Invalid cardinality` |
| Broken references | text | not in the schema: `Broken references` |

**Data it reads**: `getSemanticModel` (onLoad, The catalogue)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The semantic model business list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the semantic model business untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No semantic model business yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the semantic model business are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getSemanticModel` → `REPORT_VIEW_TENANT` (operate) · staff
- `setSemanticModel` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-066` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-066`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 10: Works in Semantic Model & Business Data Catalogue → Create the governed business layer between raw data and dashboards/AI. This is one of the most important technical screens in Board 10.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-066?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-067` Data Refresh, Pipeline & Data Health Monitor

**Monitor movement of information from operational systems into the analytics platform.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Monitor) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/data-refresh-pipeline-data-health-monitor-anl-067` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Pipelines Running** (metric tile)

**Successful Refreshes** (metric tile)

**Failed Refreshes** (metric tile)

**Average Refresh Duration** (metric tile)

**Data Latency** (metric tile)

**Stale Datasets** (metric tile)

**Records Processed** (metric tile)

**Every data refresh pipeline** (data table)

| Shows | Format | Notes |
|---|---|---|
| Completeness | text | not in the schema: `Completeness` |
| Timeliness | text | not in the schema: `Timeliness` |
| Accuracy checks | text | not in the schema: `Accuracy checks` |
| Duplicate records | text | not in the schema: `Duplicate records` |
| Missing values | text | not in the schema: `Missing values` |
| Schema changes | text | not in the schema: `Schema changes` |
| Reconciliation status | text | not in the schema: `Reconciliation status` |

**The selected data refresh pipeline** (detail panel): The pack groups this record's detail under its own headings: “Source”, “Ticketing Dataset Delayed”, “Affected”.

| Shows | Format | Notes |
|---|---|---|
| Completeness | text | not in the schema: `Completeness` |
| Timeliness | text | not in the schema: `Timeliness` |
| Accuracy checks | text | not in the schema: `Accuracy checks` |
| Duplicate records | text | not in the schema: `Duplicate records` |
| Missing values | text | not in the schema: `Missing values` |
| Schema changes | text | not in the schema: `Schema changes` |
| Reconciliation status | text | not in the schema: `Reconciliation status` |

**Data it reads**: `listAnalyticsPipelines` (onLoad, Refresh and freshness)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data refresh pipeline list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data refresh pipeline untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data refresh pipeline yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data refresh pipeline are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAnalyticsPipelines` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-067` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-067`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 12: Works in Data Refresh, Pipeline & Data Health Monitor → Monitor movement of information from operational systems into the analytics platform.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-067?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-068` Embedded BI, Workspace & Tenant Administration

**Configure how BI technology is embedded inside TICVAI and separated across clients/tenants.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/embedded-bi-workspace-tenant-administration-anl-068` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Navigation | select field | — | — | — | — | — | — |
| Theme | select field | — | — | — | — | — | — |
| Branding | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Default Dashboard | select field | — | — | — | — | — | — |
| Mobile behavior | select field | — | — | — | — | — | — |
| Full-screen mode | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | select | — | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | `listDashboards` ?module |
| Include archived | toggle | off | — | `listDashboards` ?includeArchived |

#### Outputs: what the screen shows and produces

**Data it reads**: `listDashboards` (onLoad, Workspaces and embedding)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The embedded tenant administration configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the embedded tenant administration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No embedded tenant administration configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listDashboards` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-068` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-068`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 14: Works in Embedded BI, Workspace & Tenant Administration → Configure how BI technology is embedded inside TICVAI and separated across clients/tenants.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-068?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-069` Analytics Performance, Usage & Cost Monitor

**Monitor BI adoption, system performance, capacity consumption and analytical operating costs.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Usage KPIs; Performance KPIs) and a per-row directory (§Identify) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/analytics-performance-usage-cost-monitor-anl-069` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getAnalyticsUsage` ?from |
| Group by | radio group | — | Report · Dashboard · User · Venue | `getAnalyticsUsage` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Analytics Users** (metric tile)

**Dashboard Views** (metric tile)

**Report Runs** (metric tile)

**AI Queries** (metric tile)

**Exports** (metric tile)

**API Requests** (metric tile)

**Peak Concurrent Users** (metric tile)

**Average Dashboard Load Time** (metric tile)

**Query Duration** (metric tile)

**Slowest Reports** (metric tile)

**Failed Queries** (metric tile)

**Dataset Size** (metric tile)

**Refresh Duration** (metric tile)

**Embedded BI Availability** (metric tile)

**Every analytics performance usage** (data table)

| Shows | Format | Notes |
|---|---|---|
| Most used dashboards | text | not in the schema: `Most Used Dashboards` |
| Least used dashboards | text | not in the schema: `Least Used Dashboards` |
| Most used reports | text | not in the schema: `Most Used Reports` |
| Unused reports | text | not in the schema: `Unused Reports` |
| Most queried KP is | text | not in the schema: `Most Queried KPIs` |
| Most active users/roles | text | not in the schema: `Most Active Users/Roles` |

**The selected analytics performance usage** (detail panel): The pack groups this record's detail under its own headings: “Where supported, monitor”, “Tenant Usage”.

| Shows | Format | Notes |
|---|---|---|
| Most used dashboards | text | not in the schema: `Most Used Dashboards` |
| Least used dashboards | text | not in the schema: `Least Used Dashboards` |
| Most used reports | text | not in the schema: `Most Used Reports` |
| Unused reports | text | not in the schema: `Unused Reports` |
| Most queried KP is | text | not in the schema: `Most Queried KPIs` |
| Most active users/roles | text | not in the schema: `Most Active Users/Roles` |

**Data it reads**: `getAnalyticsUsage` (onLoad, Usage, runtime and cost)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The analytics performance usage list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the analytics performance usage untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No analytics performance usage yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the analytics performance usage are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getAnalyticsUsage` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-069` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-069`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 16: Works in Analytics Performance, Usage & Cost Monitor → Monitor BI adoption, system performance, capacity consumption and analytical operating costs.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-069?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-070` Analytics Governance, Security & Audit Center

**Provide final governance over the entire BI and analytics environment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Monitor; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/analytics-governance-security-audit-center-anl-070` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listSecurityDetectionGovernance` ?venue |
| Park | text field | — | — | `listSecurityDetectionGovernance` ?park |
| Event | text field | — | — | `listSecurityDetectionGovernance` ?event |
| Product | text field | — | — | `listSecurityDetectionGovernance` ?product |
| Channel | text field | — | — | `listSecurityDetectionGovernance` ?channel |
| Reseller | text field | — | — | `listSecurityDetectionGovernance` ?reseller |
| Credential type | text field | — | — | `listSecurityDetectionGovernance` ?credentialType |
| Media | text field | — | — | `listSecurityDetectionGovernance` ?media |
| Device | text field | — | — | `listSecurityDetectionGovernance` ?device |
| Gate | text field | — | — | `listSecurityDetectionGovernance` ?gate |
| Time day | text field | — | — | `listSecurityDetectionGovernance` ?timeDay |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every analytics governance security** (data table)

| Shows | Format | Notes |
|---|---|---|
| Dashboard permissions | text | not in the schema: `Dashboard Permissions` |
| Report permissions | text | not in the schema: `Report Permissions` |
| Dataset permissions | text | not in the schema: `Dataset Permissions` |
| KPI changes | text | not in the schema: `KPI Changes` |
| Data exports | text | not in the schema: `Data Exports` |
| API access | text | not in the schema: `API Access` |
| AI access | text | not in the schema: `AI Access` |
| Sensitive data usage | text | not in the schema: `Sensitive Data Usage` |
| Configuration changes | text | not in the schema: `Configuration Changes` |
| Administrative actions | text | not in the schema: `Administrative Actions` |
| AI queries | text | not in the schema: `AI Queries` |
| Blocked queries | text | not in the schema: `Blocked Queries` |
| Sensitive data requests | text | not in the schema: `Sensitive-Data Requests` |
| AI cost | text | not in the schema: `AI Cost` |
| Model errors | text | not in the schema: `Model Errors` |
| Low confidence answers | text | not in the schema: `Low-Confidence Answers` |
| User feedback | text | not in the schema: `User Feedback` |

**The selected analytics governance security** (detail panel): The pack groups this record's detail under its own headings: “The desired structure is”, “Unified Data Integration Layer”, “Analytics Data Platform”, “Instead”, “Board 10 Benchmarking”.

| Shows | Format | Notes |
|---|---|---|
| Dashboard permissions | text | not in the schema: `Dashboard Permissions` |
| Report permissions | text | not in the schema: `Report Permissions` |
| Dataset permissions | text | not in the schema: `Dataset Permissions` |
| KPI changes | text | not in the schema: `KPI Changes` |
| Data exports | text | not in the schema: `Data Exports` |
| API access | text | not in the schema: `API Access` |
| AI access | text | not in the schema: `AI Access` |
| Sensitive data usage | text | not in the schema: `Sensitive Data Usage` |
| Configuration changes | text | not in the schema: `Configuration Changes` |
| Administrative actions | text | not in the schema: `Administrative Actions` |
| AI queries | text | not in the schema: `AI Queries` |
| Blocked queries | text | not in the schema: `Blocked Queries` |
| Sensitive data requests | text | not in the schema: `Sensitive-Data Requests` |
| AI cost | text | not in the schema: `AI Cost` |
| Model errors | text | not in the schema: `Model Errors` |
| Low confidence answers | text | not in the schema: `Low-Confidence Answers` |
| User feedback | text | not in the schema: `User Feedback` |

**Data it reads**: `listSecurityDetectionGovernance` (onLoad, Security Analytics, AI Detection & Governance)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The analytics governance security list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the analytics governance security untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No analytics governance security yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the analytics governance security are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listSecurityDetectionGovernance` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-070` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-070`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 18: Works in Analytics Governance, Security & Audit Center → Provide final governance over the entire BI and analytics environment.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (34 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-070?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
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

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createKpi": {"method":"POST","path":"/kpis","contract":"reporting","summary":"Define a KPI once, for everywhere","permission":"REPORT_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"KpiDefinition","responds":"KpiDefinition"},
"getAnalyticsBenchmark": {"method":"GET","path":"/analytics-benchmarks","contract":"reporting","summary":"One site against another, on a like-for-like basis","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"kpiId","in":"query","required":true},{"name":"scopePaths","in":"query","required":null},{"name":"normaliseBy","in":"query","required":null}],"requestBody":null,"responds":"BenchmarkRow"},
"getAnalyticsUsage": {"method":"GET","path":"/analytics-usage","contract":"reporting","summary":"Which dashboards and reports are actually used, and what they cost","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"AnalyticsUsageRow"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getSemanticModel": {"method":"GET","path":"/semantic-model","contract":"reporting","summary":"The business data catalogue reports are built from","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SemanticModel"},
"listAnalyticsPipelines": {"method":"GET","path":"/analytics-pipelines","contract":"reporting","summary":"Data sources, refresh state and freshness","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AnalyticsPipeline"},
"listDashboards": {"method":"GET","path":"/dashboards","contract":"reporting","summary":"List dashboards","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"module","in":"query","required":false},{"name":"includeArchived","in":"query","required":false}],"requestBody":null,"responds":"Dashboard"},
"listKpis": {"method":"GET","path":"/kpis","contract":"reporting","summary":"The enterprise KPI library","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"KpiDefinition"},
"listSecurityDetectionGovernance": {"method":"GET","path":"/security-detection-governance","contract":"access","summary":"Security Analytics, AI Detection & Governance","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venue","in":"query","required":false},{"name":"park","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"reseller","in":"query","required":false},{"name":"credentialType","in":"query","required":false},{"name":"media","in":"query","required":false},{"name":"device","in":"query","required":false},{"name":"gate","in":"query","required":false},{"name":"timeDay","in":"query","required":false}],"requestBody":null,"responds":"SecurityAnalyticsAiDetectionGovernanceView"},
"listSiteNormalisationBases": {"method":"GET","path":"/site-normalisation-bases","contract":"reporting","summary":"The denominators each site is benchmarked by","permission":"REPORT_VIEW_TENANT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"scopePath","in":"query","required":null},{"name":"periodFrom","in":"query","required":null},{"name":"periodTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setKpiTargets": {"method":"PUT","path":"/kpis/{kpiId}/targets","contract":"reporting","summary":"Targets, thresholds and what red means","permission":"REPORT_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KpiTarget"},
"setSemanticModel": {"method":"PUT","path":"/semantic-model","contract":"reporting","summary":"Publish the catalogue","permission":"REPORT_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SemanticModel","responds":"SemanticModel"},
"setSiteNormalisationBasis": {"method":"PUT","path":"/site-normalisation-bases","contract":"reporting","summary":"Set the denominators a site is benchmarked by","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SiteNormalisationBasis"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Aggregation": {"type":"string","enum":["none","count","countDistinct","sum","average","min","max"]},
"AnalyticsPipeline": {"type":"object","x-ticvai-persistence":"reporting.pipeline","description":"BI board 10.7. **Freshness decides whether a dashboard can be trusted.**","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"sourceKind":{"type":"string"},"datasets":{"type":"array","items":{"type":"string"}},"schedule":{"type":"string","nullable":true},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"lastSuccessAt":{"type":"string","format":"date-time","nullable":true},"freshnessMinutes":{"type":"integer","nullable":true},"expectedFreshnessMinutes":{"type":"integer","nullable":true},"status":{"type":"string","enum":["healthy","degraded","stale","failed","paused"]},"lastError":{"type":"string","nullable":true},"rowsLastRun":{"type":"integer","nullable":true},"scopePath":{"type":"string"}}},
"AnalyticsUsageRow": {"type":"object","description":"BI board 10.9. **The number that lets a BI estate be pruned.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"opens":{"type":"integer"},"distinctUsers":{"type":"integer"},"lastOpenedAt":{"type":"string","format":"date-time","nullable":true},"averageRuntimeMs":{"type":"integer","nullable":true},"rowsScanned":{"type":"integer","nullable":true},"neverOpened":{"type":"boolean"}}},
"BenchmarkNormalisation": {"type":"string","description":"The basis a benchmark is compared on. Shared by `getAnalyticsBenchmark` and `BenchmarkRow`.","enum":["none","perVisitor","perOperatingHour","perStaffedPosition","perSquareMetre"]},
"BenchmarkRow": {"type":"object","description":"BI board 10.4. **The normalisation travels with the comparison.**","properties":{"scopePath":{"type":"string"},"label":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"normalisedValue":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"normaliseBy":{"$ref":"#/components/schemas/BenchmarkNormalisation"},"rank":{"type":"integer"},"percentile":{"type":"number","nullable":true}}},
"CreateDashboardRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","module","tiles"],"properties":{"name":{"type":"string","maxLength":200},"module":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey","description":"**Which module this dashboard belongs to, and therefore who may see it.** Added 22 September for the command centre: one shell that shows each login the dashboards of the modules it is entitled to. **A dashboard with no module could not be placed in that shell at all** — the field the whole design hangs on did not exist.\n**Required, and `core` is the answer for a dashboard that belongs to no optional module.** An empty field and *belongs everywhere* look identical, and only one of them is a decision — the rule `ModuleKey` already states for screens.\n**Creating one is gated twice**, by `REPORT_MANAGE` and by the module: a principal cannot build a dashboard for a module the tenant has not licensed or that the principal holds no permission in. The server refuses with `409`; a client that hides the option has not enforced anything.\n"},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid","description":"Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. The same rule as `RunReportRequest.venueId`.\n"},"isShared":{"type":"boolean","default":false},"tiles":{"type":"array","minItems":1,"maxItems":24,"items":{"$ref":"#/components/schemas/DashboardTile"}}}},
"Dashboard": {"x-ticvai-persistence":"reporting.dashboard + reporting.dashboard_tile","allOf":[{"$ref":"#/components/schemas/CreateDashboardRequest"},{"type":"object","required":["id","ownerPrincipalId","aggregateCost","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid"},"aggregateCost":{"type":"string","enum":["low","medium","high"],"description":"Combined refresh load of every tile."},"archivedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"},"createdAt":{"type":"string","format":"date-time"}}}]},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"KpiDefinition": {"type":"object","x-ticvai-persistence":"reporting.kpi_definition","description":"BI boards 2.5 and 10.2. **One definition, referenced everywhere** — otherwise *revenue* means two things in the same meeting.\n","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","description":"`takings` and `admissions` are seeded for every tenant as system KPIs (decided 28 September, audit R283), and the five accreditation KPIs for every tenant with the accreditation module (29 September, build pass). The seeded codes are `ReportingSystemKpi`.\n"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"domain":{"type":"string","nullable":true},"formula":{"type":"string","description":"**Expressed against the semantic model, not against tables.** A KPI written in SQL is a KPI that breaks when the warehouse is reshaped.\n"},"unit":{"type":"string","enum":["currency","count","percentage","duration","ratio","score"]},"higherIsBetter":{"type":"boolean","default":true,"description":"**Refund rate and revenue both go up.** Without this the status colour is a coin toss.\n"},"defaultPeriod":{"type":"string","nullable":true},"owner":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"KpiTarget": {"type":"object","x-ticvai-persistence":"reporting.kpi_target","description":"BI board 2.6. **The threshold is what turns a number into a status.**","required":["scopePath","period","target"],"properties":{"kpiId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","description":"The scope this target applies to. With `period`, the key `setKpiTargets` matches on."},"period":{"type":"string"},"target":{"$ref":"#/components/schemas/MetricValue"},"amberAt":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"redAt":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"stretch":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true}}},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"SecurityAnalyticsAiDetectionGovernanceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Security Analytics, AI Detection & Governance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"fraudAttempts":{"type":"integer","description":"Fraud Attempts"},"preventedFraud":{"type":"integer","description":"Prevented Fraud"},"credentialSharing":{"type":"integer","description":"Credential Sharing"},"biometricAlerts":{"type":"integer","description":"Biometric Alerts"},"deviceBindingViolations":{"type":"integer","description":"Device-Binding Violations"},"companionViolations":{"type":"integer","description":"Companion Violations"},"blacklistHits":{"type":"integer","description":"Blacklist Hits"},"identityLocks":{"type":"integer","description":"Identity Locks"},"securityOverrides":{"type":"integer","description":"Security Overrides"},"detectionRate":{"type":"number","description":"Detection Rate"},"falsePositiveIndicator":{"type":"number","description":"False Positive Indicator"},"operatorOverrideRate":{"type":"number","description":"Operator Override Rate"},"averageInvestigationTime":{"type":"integer","description":"Minutes"},"averageResponseTime":{"type":"integer","description":"Minutes"},"recurringFraudRate":{"type":"number","description":"Recurring Fraud Rate"},"financialExposure":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Financial Exposure"},"estimatedFraudPrevented":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated Fraud Prevented"},"duplicateUsage":{"type":"integer"}}},
"SemanticModel": {"type":"object","x-ticvai-persistence":"reporting.semantic_model","description":"BI boards 3.3 and 10.6. **A vocabulary, not a schema.** Exposing joins to report authors produces reports that are wrong invisibly.\n","properties":{"version":{"type":"integer","readOnly":true,"description":"Assigned by the server on each publish."},"domains":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"datasets":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"name":{"type":"string"},"grain":{"type":"string","description":"**What one row means.** The single most common cause of a wrong report is a join that silently multiplied the grain.\n"},"fields":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"label":{"type":"string"},"dataType":{"$ref":"#/components/schemas/FieldType"},"aggregation":{"allOf":[{"$ref":"#/components/schemas/Aggregation"}],"nullable":true,"description":"The default aggregation for the field, where it has one."},"sensitive":{"type":"boolean","default":false},"description":{"type":"string","nullable":true}}}}}}}}}},"relationships":{"type":"array","items":{"type":"object","properties":{"fromDataset":{"type":"string"},"toDataset":{"type":"string"},"cardinality":{"type":"string","enum":["oneToOne","oneToMany","manyToOne","manyToMany"]}}}},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string"}}},
"SiteNormalisationBasis": {"type":"object","x-ticvai-persistence":"reporting.site_normalisation_basis","description":"BI boards 7.9 and 10.4. **The denominators a benchmark divides by**, per site and period: visitors, operating hours, staffed positions and area, one for each `BenchmarkNormalisation` other than `none`. Read by `getAnalyticsBenchmark` for the period that covers the benchmark (data model, 29 September).\n","required":["scopePath","periodStart","periodEnd"],"properties":{"id":{"type":"string","format":"uuid"},"scopePath":{"type":"string","description":"The site (venue scope) the basis applies to."},"periodStart":{"type":"string","format":"date"},"periodEnd":{"type":"string","format":"date"},"visitors":{"type":"integer","nullable":true,"minimum":0,"description":"`perVisitor`."},"operatingHours":{"type":"number","nullable":true,"minimum":0,"description":"`perOperatingHour`."},"staffedPositions":{"type":"number","nullable":true,"minimum":0,"description":"`perStaffedPosition`. Average positions staffed over the period."},"areaSquareMetres":{"type":"number","nullable":true,"minimum":0,"description":"`perSquareMetre`. Operated area."}}}
}
```
