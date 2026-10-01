# WS67 — Unified BI Reporting and AI Analytics Platform board 2

**10 screens · 11 operations · 12 schemas · 3 permissions**

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
| `ANL-021` | Dashboard Library | B–D | 0 | 62 | 6 | 18 | 2 | 0 | — | notStarted (—) |
| `ANL-022` | Dashboard Creation Wizard | B–D | 18 | 0 | 5 | 18 | 1 | 0 | — | notStarted (—) |
| `ANL-023` | Drag-and-Drop Dashboard Canvas | A | 0 | 0 | 6 | 0 | 3 | 0 | — | notStarted (—) |
| `ANL-024` | Widget & Visualization Library | B–D | 0 | 12 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `ANL-025` | KPI Builder | A | 21 | 0 | 5 | 0 | 1 | 0 | — | notStarted (—) |
| `ANL-026` | Targets, Thresholds & KPI Status Rules | B–D | 0 | 16 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `ANL-027` | Data & Filter Configuration | B–D | 18 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `ANL-028` | Drill-Down & Interaction Designer | B–D | 9 | 0 | 5 | 0 | 3 | 0 | — | notStarted (—) |
| `ANL-029` | Dashboard Access, Publishing & Versioning | B–D | 0 | 12 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `ANL-030` | Dashboard Preview, Validation & Health | B–D | 0 | 18 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ANL-021, ANL-023, ANL-024, ANL-029, ANL-030 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ANL-021` Dashboard Library

**Provide a centralized catalogue for all standard, custom, AI-generated and embedded TICVAI dashboards.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_VENUE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display dashboard cards/table containing; Dashboard Categories; Dashboard Types) and no metric row |
| Offline | online only |
| Opens with | `dashboardId` (navigation) |
| Route | `/analytics/dashboard-library-anl-021` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | select | — | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | `listDashboards` ?module |
| Include archived | toggle | off | — | `listDashboards` ?includeArchived |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every record** (data table)

| Shows | Format | Notes |
|---|---|---|
| Dashboard name | text | not in the schema: `Dashboard Name` |
| Dashboard ID | text | not in the schema: `Dashboard ID` |
| Category | text | not in the schema: `Category` |
| Business domain | text | not in the schema: `Business Domain` |
| Owner | text | not in the schema: `Owner` |
| Sites/venues | text | not in the schema: `Sites/Venues` |
| Audience/role | text | not in the schema: `Audience/Role` |
| Status | text | not in the schema: `Status` |
| Version | text | not in the schema: `Version` |
| Last modified | text | not in the schema: `Last Modified` |
| Last published | text | not in the schema: `Last Published` |
| Usage count | text | not in the schema: `Usage Count` |
| Data refresh status | text | not in the schema: `Data Refresh Status` |
| Executive | text | not in the schema: `Executive` |
| Operations | text | not in the schema: `Operations` |
| Finance | text | not in the schema: `Finance` |
| Sales | text | not in the schema: `Sales` |
| Ticketing | text | not in the schema: `Ticketing` |
| Access control | text | not in the schema: `Access Control` |
| CRM | text | not in the schema: `CRM` |
| Marketing | text | not in the schema: `Marketing` |
| Membership | text | not in the schema: `Membership` |
| Loyalty | text | not in the schema: `Loyalty` |
| F&B | text | not in the schema: `F&B` |
| Retail | text | not in the schema: `Retail` |
| Inventory | text | not in the schema: `Inventory` |
| Resources | text | not in the schema: `Resources` |
| Custom | text | not in the schema: `Custom` |
| System dashboard — TICVAI standard dashboard | text | not in the schema: `System Dashboard — TICVAI standard dashboard` |
| Custom dashboard — customer created | text | not in the schema: `Custom Dashboard — customer-created` |
| … 1 more | | `schemas.json` |

**The selected record** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Dashboard name | text | not in the schema: `Dashboard Name` |
| Dashboard ID | text | not in the schema: `Dashboard ID` |
| Category | text | not in the schema: `Category` |
| Business domain | text | not in the schema: `Business Domain` |
| Owner | text | not in the schema: `Owner` |
| Sites/venues | text | not in the schema: `Sites/Venues` |
| Audience/role | text | not in the schema: `Audience/Role` |
| Status | text | not in the schema: `Status` |
| Version | text | not in the schema: `Version` |
| Last modified | text | not in the schema: `Last Modified` |
| Last published | text | not in the schema: `Last Published` |
| Usage count | text | not in the schema: `Usage Count` |
| Data refresh status | text | not in the schema: `Data Refresh Status` |
| Executive | text | not in the schema: `Executive` |
| Operations | text | not in the schema: `Operations` |
| Finance | text | not in the schema: `Finance` |
| Sales | text | not in the schema: `Sales` |
| Ticketing | text | not in the schema: `Ticketing` |
| Access control | text | not in the schema: `Access Control` |
| CRM | text | not in the schema: `CRM` |
| Marketing | text | not in the schema: `Marketing` |
| Membership | text | not in the schema: `Membership` |
| Loyalty | text | not in the schema: `Loyalty` |
| F&B | text | not in the schema: `F&B` |
| Retail | text | not in the schema: `Retail` |
| Inventory | text | not in the schema: `Inventory` |
| Resources | text | not in the schema: `Resources` |
| Custom | text | not in the schema: `Custom` |
| System dashboard — TICVAI standard dashboard | text | not in the schema: `System Dashboard — TICVAI standard dashboard` |
| Custom dashboard — customer created | text | not in the schema: `Custom Dashboard — customer-created` |
| … 1 more | | `schemas.json` |

**Data it reads**: `listDashboards` (onLoad, The library); `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Back to Executive Command Center*; carries `dashboardId`, `reportId`
- → `ANL-030` Dashboard Preview, Validation & Health: *Dashboard Preview, Validation & Health*; carries `dashboardId`
- → `ANL-022` Dashboard Creation Wizard: *Dashboard Creation Wizard*
- → `ANL-023` Drag-and-Drop Dashboard Canvas: *Drag-and-Drop Dashboard Canvas*; carries `dashboardId`
- → `ANL-024` Widget & Visualization Library: *Widget & Visualization Library*
- → `ANL-025` KPI Builder: *KPI Builder*
- → `ANL-026` Targets, Thresholds & KPI Status Rules: *Targets, Thresholds & KPI Status Rules*
- → `ANL-027` Data & Filter Configuration: *Data & Filter Configuration*; carries `dashboardId`
- → `ANL-028` Drill-Down & Interaction Designer: *Drill-Down & Interaction Designer*; carries `dashboardId`
- → `ANL-029` Dashboard Access, Publishing & Versioning: *Dashboard Access, Publishing & Versioning*; carries `dashboardId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The record list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the record untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No record yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the record are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094); 409 The caller is not entitled to the dashboard's module — the tenant has not licensed it, or the principal holds no permission in it. |

#### Permissions

- `listDashboards` → `REPORT_VIEW_VENUE` (operate) · staff
- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `createDashboard` → `REPORT_MANAGE` (configure) · staff
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff

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

- Business can build additional dashboards (e.g. separate finance, sales, operations dashboards) with role-based access so only the relevant team can view a given dashboard. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-702)*
- The platform ships a standard set of default dashboards out of the box, plus the ability for the business to design additional custom dashboards without SQL or programming knowledge. *(agreed · MoM 8 Sep 2026, 4.1 Rationale for a Native BI/Reporting Platform · DI-697)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-021` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-021`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 1: Opens Dashboard Library → Provide a centralized catalogue for all standard, custom, AI-generated and embedded TICVAI dashboards.
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F176 branch at step 1 (expected): when Nothing has been set up on Dashboard Library yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F176 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (62 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-021?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-001`, `ANL-030`, `ANL-022`, `ANL-023`, `ANL-024`, `ANL-025`, `ANL-026`, `ANL-027`, `ANL-028`, `ANL-029`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-022` Dashboard Creation Wizard

**Guide users through creation of a new dashboard.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Select; Select one or multiple domains) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/dashboard-creation-wizard-anl-022` |

**Known gaps.** **Dashboard Creation Wizard declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Dashboard Name | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Category | select field | — | — | — | — | — | — |
| Business Domain | select field | — | — | — | — | — | — |
| Dashboard Owner | select field | — | — | — | — | — | — |
| Tags | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Default Currency | select field | — | — | — | — | — | — |
| Step 2 — Scope | text field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Organization | select field | — | — | — | — | — | — |
| Site(s) | select field | — | — | — | — | — | — |
| Venue(s) | select field | — | — | — | — | — | — |
| Attraction(s) | select field | — | — | — | — | — | — |
| Business Unit(s) | select field | — | — | — | — | — | — |
| Step 3 — Data Domains | text field | — | — | — | — | — | — |
| Queue • Accreditation | select field | — | — | — | — | — | — |
| Step 4 — Template | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*; carries `dashboardId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The creation wizard configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the creation wizard untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No creation wizard configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094); 409 The caller is not entitled to the dashboard's module — the tenant has not licensed it, or the principal holds no permission in it. |

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

- The platform ships a standard set of default dashboards out of the box, plus the ability for the business to design additional custom dashboards without SQL or programming knowledge. *(agreed · MoM 8 Sep 2026, 4.1 Rationale for a Native BI/Reporting Platform · DI-697)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-022` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-022`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 2: Works in Dashboard Creation Wizard → Guide users through creation of a new dashboard.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-022?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-023` Drag-and-Drop Dashboard Canvas

**Provide the main visual workspace for dashboard construction.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block A · ticket #20782 (APP-SETUP-ANL-023) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_VENUE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `dashboardId` (navigation) |
| Route | `/analytics/drag-and-drop-dashboard-canvas-anl-023` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save dashboard (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …)

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*; carries `dashboardId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The drag-and-drop canvas list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the drag-and-drop canvas untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No drag-and-drop canvas yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the drag-and-drop canvas are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Moving a dashboard to a module the caller is not entitled to. The same guard as `createDashboard` — without it, an update would be the way round the create …; 409 The dashboard is shared. Un-share it first. |

#### Permissions

- `updateDashboard` → `REPORT_MANAGE` (configure) · staff
- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `deleteDashboard` → `REPORT_MANAGE` (configure) · staff
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Allam shared the itemised dashboard-component document (chart types, drill-down tool, heat map, etc.) with a suggested reference architecture - explicitly a suggestion Softlabs may adopt, adapt or replace. *(agreed · MoM 9 Sep 2026, 4.11 Follow-Ups from Prior Sessions · DI-750)*
- Dashboard creation is drag-and-drop against predefined data sets (revenue, sales quantity, sales channel, department, etc.); the user picks a visual format (bar chart, pie chart, etc.) without writing queries. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-703)*
- The platform ships a standard set of default dashboards out of the box, plus the ability for the business to design additional custom dashboards without SQL or programming knowledge. *(agreed · MoM 8 Sep 2026, 4.1 Rationale for a Native BI/Reporting Platform · DI-697)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-023` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-023`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 4: Works in Drag-and-Drop Dashboard Canvas → Provide the main visual workspace for dashboard construction.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-023?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save dashboard, Cancel.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_VENUE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-024` Widget & Visualization Library

**Provide reusable visual components for dashboard construction.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§KPI Components) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/widget-visualization-library-anl-024` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every widget visualization** (data table)

| Shows | Format | Notes |
|---|---|---|
| KPI card | text | not in the schema: `KPI Card` |
| Target card | text | not in the schema: `Target Card` |
| Variance card | text | not in the schema: `Variance Card` |
| Scorecard | text | not in the schema: `Scorecard` |
| Gauge | text | not in the schema: `Gauge` |
| Progress indicator | text | not in the schema: `Progress Indicator` |

**The selected widget visualization** (detail panel): The pack groups this record's detail under its own headings: “Chart Components”, “Operational Components”.

| Shows | Format | Notes |
|---|---|---|
| KPI card | text | not in the schema: `KPI Card` |
| Target card | text | not in the schema: `Target Card` |
| Variance card | text | not in the schema: `Variance Card` |
| Scorecard | text | not in the schema: `Scorecard` |
| Gauge | text | not in the schema: `Gauge` |
| Progress indicator | text | not in the schema: `Progress Indicator` |

**Data it reads**: `getSemanticModel` (onLoad, What a widget can be bound to)

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The widget visualization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the widget visualization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No widget visualization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the widget visualization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getSemanticModel` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Allam shared the itemised dashboard-component document (chart types, drill-down tool, heat map, etc.) with a suggested reference architecture - explicitly a suggestion Softlabs may adopt, adapt or replace. *(agreed · MoM 9 Sep 2026, 4.11 Follow-Ups from Prior Sessions · DI-750)*
- Dashboard creation is drag-and-drop against predefined data sets (revenue, sales quantity, sales channel, department, etc.); the user picks a visual format (bar chart, pie chart, etc.) without writing queries. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-703)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-024` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-024`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 6: Works in Widget & Visualization Library → Provide reusable visual components for dashboard construction.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-024?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-025` KPI Builder

**Allow authorized business users to create standardized enterprise KPIs.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block A · ticket #20783 (APP-SETUP-ANL-025) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_TENANT` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Define whether) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/kpi-builder-anl-025` |

**Known gaps.** **KPI Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| KPI Name | select field | — | — | — | — | — | — |
| KPI Code | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Business Domain | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |
| Data Source | select field | — | — | — | — | — | — |
| Measure | select field | — | — | — | — | — | — |
| Formula | select field | — | — | — | — | — | — |
| Aggregation | select field | — | — | — | — | — | — |
| Unit | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Decimal Precision | select field | — | — | — | — | — | — |
| Effective Date | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Higher = Better | select field | — | — | — | — | — | — |
| Lower = Better | select field | — | — | — | — | — | — |
| Revenue ↑ | select field | — | — | — | — | — | — |
| Conversion ↑ | select field | — | — | — | — | — | — |
| Refund Rate ↓ | select field | — | — | — | — | — | — |
| Gate Rejection Rate ↓ | text field | — | — | — | — | — | — |
| Queue Time ↓ | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listKpis` (onLoad, KPIs already defined)

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The kpi configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the kpi untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No kpi configured yet. Carries the create action and says what the platform does in the meantime. |
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

- KPI threshold configuration defines normal/warning/critical bands per metric (e.g. capacity below 80% normal, 80-90% warning, above 95% critical), shown as status on the dashboard. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-704)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-025` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-025`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 8: Works in KPI Builder → Allow authorized business users to create standardized enterprise KPIs.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-025?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_TENANT`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-026` Targets, Thresholds & KPI Status Rules

**Configure how TICVAI determines whether KPI performance is healthy, warning or critical.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_TENANT` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§For each KPI) and no metric row |
| Offline | online only |
| Opens with | `kpiId` (navigation) |
| Route | `/analytics/targets-thresholds-kpi-status-rules-anl-026` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: If Critical → Generate Alert, Notify responsible user, Create operational task, Trigger AI analysis. Each … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every targets thresholds kpi** (data table)

| Shows | Format | Notes |
|---|---|---|
| Target | text | not in the schema: `Target` |
| Minimum | text | not in the schema: `Minimum` |
| Maximum | text | not in the schema: `Maximum` |
| Warning threshold | text | not in the schema: `Warning Threshold` |
| Critical threshold | text | not in the schema: `Critical Threshold` |
| Benchmark | text | not in the schema: `Benchmark` |
| Tolerance | text | not in the schema: `Tolerance` |
| Evaluation frequency | text | not in the schema: `Evaluation Frequency` |

**The selected targets thresholds kpi** (detail panel): The pack groups this record's detail under its own headings: “Capacity Utilization”.

| Shows | Format | Notes |
|---|---|---|
| Target | text | not in the schema: `Target` |
| Minimum | text | not in the schema: `Minimum` |
| Maximum | text | not in the schema: `Maximum` |
| Warning threshold | text | not in the schema: `Warning Threshold` |
| Critical threshold | text | not in the schema: `Critical Threshold` |
| Benchmark | text | not in the schema: `Benchmark` |
| Tolerance | text | not in the schema: `Tolerance` |
| Evaluation frequency | text | not in the schema: `Evaluation Frequency` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| If Critical → Generate Alert (primary button) | navigation or local | — | — | — | — |
| Notify responsible user (secondary button) | navigation or local | — | — | — | — |
| Create operational task (secondary button) | navigation or local | — | — | — | — |
| Trigger AI analysis (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listKpis` (onLoad, The KPI being targeted)

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The targets thresholds kpi list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the targets thresholds kpi untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No targets thresholds kpi yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the targets thresholds kpi are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setKpiTargets` → `REPORT_MANAGE` (configure) · staff
- `listKpis` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- KPI threshold configuration defines normal/warning/critical bands per metric (e.g. capacity below 80% normal, 80-90% warning, above 95% critical), shown as status on the dashboard. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-704)*
- Retail intelligence shows sales and outlet performance, top-performing stores, demand forecasting (from retail sales history and online ticket booking trends) and target-vs-actual per outlet (e.g. monthly target vs. achieved, with variance). *(client request · MoM 19 Aug 2026, 4.9 Retail Intelligence & Reporting · DI-368)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-026` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-026`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 10: Works in Targets, Thresholds & KPI Status Rules → Configure how TICVAI determines whether KPI performance is healthy, warning or critical.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-026?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: If Critical → Generate Alert, Notify responsible user, Create operational task, Trigger AI analysis.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_TENANT`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-027` Data & Filter Configuration

**Control what data a dashboard/widget uses and how users can filter it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_TENANT` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `dashboardId` (navigation) |
| Route | `/analytics/data-filter-configuration-anl-027` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search data filter | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by global, widget-level, mandatory, optional, hidden, defaulted — which are present is a decision the pack already made. | — |
| Data Domain | select field | — | — | — | — | — | — |
| Dataset | select field | — | — | — | — | — | — |
| Measure | select field | — | — | — | — | — | — |
| Dimension | select field | — | — | — | — | — | — |
| Aggregation | select field | — | — | — | — | — | — |
| Date Field | select field | — | — | — | — | — | — |
| Relationship | select field | — | — | — | — | — | — |
| Calculation | select field | — | — | — | — | — | — |
| Date Range | select field | — | — | — | — | — | — |
| Site | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Attraction | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Customer Segment | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `getSemanticModel` (onLoad, Datasets and fields to filter on)

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*; carries `dashboardId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data filter configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data filter untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data filter configured yet. Carries the create action and says what the platform does in the meantime. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data filter are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Moving a dashboard to a module the caller is not entitled to. The same guard as `createDashboard` — without it, an update would be the way round the create … |

#### Permissions

- `getSemanticModel` → `REPORT_VIEW_TENANT` (operate) · staff
- `updateDashboard` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Date/filter configuration lets a dashboard be filtered by sales channel, department or period. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-705)*
- Dashboard creation is drag-and-drop against predefined data sets (revenue, sales quantity, sales channel, department, etc.); the user picks a visual format (bar chart, pie chart, etc.) without writing queries. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-703)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-027` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-027`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 12: Works in Data & Filter Configuration → Control what data a dashboard/widget uses and how users can filter it.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-027?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_TENANT`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-028` Drill-Down & Interaction Designer

**Configure how users move from high-level KPIs into deeper analytics.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `dashboardId` (navigation) |
| Route | `/analytics/drill-down-interaction-designer-anl-028` |

**Known gaps.** **Drill-Down & Interaction Designer declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Click behavior | select field | — | — | — | — | — | — |
| Cross-filtering | select field | — | — | — | — | — | — |
| Drill-down | select field | — | — | — | — | — | — |
| Drill-up | select field | — | — | — | — | — | — |
| Drill-through | select field | — | — | — | — | — | — |
| Tooltip | select field | — | — | — | — | — | — |
| Detail page | select field | — | — | — | — | — | — |
| Related dashboard | select field | — | — | — | — | — | — |
| Underlying report | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*; carries `dashboardId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The drill-down interaction designer configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the drill-down interaction designer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No drill-down interaction designer configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Moving a dashboard to a module the caller is not entitled to. The same guard as `createDashboard` — without it, an update would be the way round the create … |

#### Permissions

- `updateDashboard` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Allam shared the itemised dashboard-component document (chart types, drill-down tool, heat map, etc.) with a suggested reference architecture - explicitly a suggestion Softlabs may adopt, adapt or replace. *(agreed · MoM 9 Sep 2026, 4.11 Follow-Ups from Prior Sessions · DI-750)*
- Very large drill-down result sets (e.g. 10,000 transactions in a single day) must be handled without the interface crashing or becoming unresponsive. *(agreed · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-710)*
- Drill-down from a high-level figure to transaction detail - yearly sales -> monthly -> daily -> sales channel -> individual transaction -> transaction detail (which customer, which ticket) - only where the data has a genuine hierarchy. *(agreed · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-709)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-028` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-028`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 14: Works in Drill-Down & Interaction Designer → Configure how users move from high-level KPIs into deeper analytics.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-028?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_MANAGE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-029` Dashboard Access, Publishing & Versioning

**Govern who can access dashboards and how dashboard changes reach production.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `dashboardId` (navigation) |
| Route | `/analytics/dashboard-access-publishing-versioning-anl-029` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every access publishing versioning** (data table)

| Shows | Format | Notes |
|---|---|---|
| Version number | text | not in the schema: `Version Number` |
| Changed by | text | not in the schema: `Changed By` |
| Date/time | text | not in the schema: `Date/Time` |
| Change description | text | not in the schema: `Change Description` |
| Approval status | text | not in the schema: `Approval Status` |
| Published version | text | not in the schema: `Published Version` |

**The selected access publishing versioning** (detail panel): The pack groups this record's detail under its own headings: “Assign dashboards to”, “Administer”, “Rollback”.

| Shows | Format | Notes |
|---|---|---|
| Version number | text | not in the schema: `Version Number` |
| Changed by | text | not in the schema: `Changed By` |
| Date/time | text | not in the schema: `Date/Time` |
| Change description | text | not in the schema: `Change Description` |
| Approval status | text | not in the schema: `Approval Status` |
| Published version | text | not in the schema: `Published Version` |

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*; carries `dashboardId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access publishing versioning list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access publishing versioning untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access publishing versioning yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access publishing versioning are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Moving a dashboard to a module the caller is not entitled to. The same guard as `createDashboard` — without it, an update would be the way round the create … |

#### Permissions

- `updateDashboard` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Dashboards go through an approval step before publishing. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-706)*
- Business can build additional dashboards (e.g. separate finance, sales, operations dashboards) with role-based access so only the relevant team can view a given dashboard. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-702)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-029` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-029`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 16: Works in Dashboard Access, Publishing & Versioning → Govern who can access dashboards and how dashboard changes reach production.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-029?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_MANAGE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-030` Dashboard Preview, Validation & Health

**Validate dashboards before publication and monitor their technical/analytical health afterward.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `dashboardId` (navigation) |
| Route | `/analytics/dashboard-preview-validation-health-anl-030` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every preview validation health** (data table)

| Shows | Format | Notes |
|---|---|---|
| Data last refreshed | text | not in the schema: `Data Last Refreshed` |
| Refresh frequency | text | not in the schema: `Refresh Frequency` |
| Dataset status | text | not in the schema: `Dataset Status` |
| Query performance | text | not in the schema: `Query Performance` |
| Widget load time | text | not in the schema: `Widget Load Time` |
| Failed widgets | text | not in the schema: `Failed Widgets` |
| API status | text | not in the schema: `API Status` |
| User count | text | not in the schema: `User Count` |
| Usage frequency | text | not in the schema: `Usage Frequency` |

**The selected preview validation health** (detail panel): The pack groups this record's detail under its own headings: “Preview Modes”, “Ready to Publish”, “Issues Detected”, “The end user should experience”.

| Shows | Format | Notes |
|---|---|---|
| Data last refreshed | text | not in the schema: `Data Last Refreshed` |
| Refresh frequency | text | not in the schema: `Refresh Frequency` |
| Dataset status | text | not in the schema: `Dataset Status` |
| Query performance | text | not in the schema: `Query Performance` |
| Widget load time | text | not in the schema: `Widget Load Time` |
| Failed widgets | text | not in the schema: `Failed Widgets` |
| API status | text | not in the schema: `API Status` |
| User count | text | not in the schema: `User Count` |
| Usage frequency | text | not in the schema: `Usage Frequency` |

**Data it reads**: `listAnalyticsPipelines` (onLoad, Whether its data is fresh); `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …)

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*; carries `dashboardId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The preview validation health list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the preview validation health untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No preview validation health yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the preview validation health are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `listAnalyticsPipelines` → `REPORT_VIEW_TENANT` (operate) · staff
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-030` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-030`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 18: Works in Dashboard Preview, Validation & Health → Validate dashboards before publication and monitor their technical/analytical health afterward.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-030?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`, `REPORT_VIEW_VENUE`.
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

**18 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createDashboard": {"method":"POST","path":"/dashboards","contract":"reporting","summary":"Create a dashboard","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateDashboardRequest","responds":"Dashboard"},
"createKpi": {"method":"POST","path":"/kpis","contract":"reporting","summary":"Define a KPI once, for everywhere","permission":"REPORT_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"KpiDefinition","responds":"KpiDefinition"},
"deleteDashboard": {"method":"DELETE","path":"/dashboards/{dashboardId}","contract":"reporting","summary":"Archive a dashboard","permission":"REPORT_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getDashboard": {"method":"GET","path":"/dashboards/{dashboardId}","contract":"reporting","summary":"Read a dashboard with tile data","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"refresh","in":"query","required":null}],"requestBody":null,"responds":"DashboardData"},
"getSemanticModel": {"method":"GET","path":"/semantic-model","contract":"reporting","summary":"The business data catalogue reports are built from","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SemanticModel"},
"listAnalyticsPipelines": {"method":"GET","path":"/analytics-pipelines","contract":"reporting","summary":"Data sources, refresh state and freshness","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AnalyticsPipeline"},
"listDashboards": {"method":"GET","path":"/dashboards","contract":"reporting","summary":"List dashboards","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"module","in":"query","required":false},{"name":"includeArchived","in":"query","required":false}],"requestBody":null,"responds":"Dashboard"},
"listKpis": {"method":"GET","path":"/kpis","contract":"reporting","summary":"The enterprise KPI library","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"KpiDefinition"},
"recordDashboardView": {"method":"POST","path":"/dashboards/{dashboardId}/views","contract":"reporting","summary":"Record that a dashboard was opened","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setKpiTargets": {"method":"PUT","path":"/kpis/{kpiId}/targets","contract":"reporting","summary":"Targets, thresholds and what red means","permission":"REPORT_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KpiTarget"},
"updateDashboard": {"method":"PUT","path":"/dashboards/{dashboardId}","contract":"reporting","summary":"Update a dashboard","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateDashboardRequest","responds":"Dashboard"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Aggregation": {"type":"string","enum":["none","count","countDistinct","sum","average","min","max"]},
"AnalyticsPipeline": {"type":"object","x-ticvai-persistence":"reporting.pipeline","description":"BI board 10.7. **Freshness decides whether a dashboard can be trusted.**","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"sourceKind":{"type":"string"},"datasets":{"type":"array","items":{"type":"string"}},"schedule":{"type":"string","nullable":true},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"lastSuccessAt":{"type":"string","format":"date-time","nullable":true},"freshnessMinutes":{"type":"integer","nullable":true},"expectedFreshnessMinutes":{"type":"integer","nullable":true},"status":{"type":"string","enum":["healthy","degraded","stale","failed","paused"]},"lastError":{"type":"string","nullable":true},"rowsLastRun":{"type":"integer","nullable":true},"scopePath":{"type":"string"}}},
"CreateDashboardRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","module","tiles"],"properties":{"name":{"type":"string","maxLength":200},"module":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey","description":"**Which module this dashboard belongs to, and therefore who may see it.** Added 22 September for the command centre: one shell that shows each login the dashboards of the modules it is entitled to. **A dashboard with no module could not be placed in that shell at all** — the field the whole design hangs on did not exist.\n**Required, and `core` is the answer for a dashboard that belongs to no optional module.** An empty field and *belongs everywhere* look identical, and only one of them is a decision — the rule `ModuleKey` already states for screens.\n**Creating one is gated twice**, by `REPORT_MANAGE` and by the module: a principal cannot build a dashboard for a module the tenant has not licensed or that the principal holds no permission in. The server refuses with `409`; a client that hides the option has not enforced anything.\n"},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid","description":"Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. The same rule as `RunReportRequest.venueId`.\n"},"isShared":{"type":"boolean","default":false},"tiles":{"type":"array","minItems":1,"maxItems":24,"items":{"$ref":"#/components/schemas/DashboardTile"}}}},
"Dashboard": {"x-ticvai-persistence":"reporting.dashboard + reporting.dashboard_tile","allOf":[{"$ref":"#/components/schemas/CreateDashboardRequest"},{"type":"object","required":["id","ownerPrincipalId","aggregateCost","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid"},"aggregateCost":{"type":"string","enum":["low","medium","high"],"description":"Combined refresh load of every tile."},"archivedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"},"createdAt":{"type":"string","format":"date-time"}}}]},
"DashboardData": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/Dashboard"},{"type":"object","properties":{"tileData":{"type":"array","items":{"type":"object","properties":{"tileId":{"type":"string","format":"uuid"},"result":{"$ref":"#/components/schemas/ReportResult"},"isCached":{"type":"boolean"},"error":{"type":"string","nullable":true}}}}}}]},
"DashboardTile": {"x-ticvai-persistence":"reporting.dashboard_tile","type":"object","required":["id","reportId","visualisation","position"],"properties":{"id":{"type":"string","format":"uuid"},"title":{"type":"string"},"reportId":{"type":"string","format":"uuid"},"visualisation":{"type":"string","description":"**Extended 22 September from eight marks to twenty** against `Ticketing_Platform_Native_Dashboard_Visualization_Requirements.pdf`, which names eighteen components and marks every one MVP. Nine were genuinely missing — `combo`, `matrix`, `funnel`, `waterfall`, `treemap`, `scatter`, `map`, `ribbon`, `decompositionTree` — and three are layout variants of marks already here: `area` beside `line`, `donut` beside `pie`, `stackedBar100` beside `stackedBar`.\n**`number` is the source's KPI / card.** Its comparison, variance, trend sparkline and status icon are tile parameters rather than separate marks.\n**Two of the eighteen are deliberately not here** — see `x-ticvai-refuses`. The source lists them as components; the platform already models each of them elsewhere, and a second model of either is the drift this enum exists to prevent.\n","enum":["number","line","area","bar","stackedBar","stackedBar100","combo","pie","donut","table","matrix","gauge","heatmap","funnel","waterfall","treemap","scatter","map","ribbon","decompositionTree"],"x-ticvai-refuses":{"slicer":"**A control, not a mark.** The source's slicer / filter is already `ReportFilter.isParameter` plus `ReportParameter` — a run-time prompt bound to the report. A slicer on the canvas places that parameter; it does not render a result, so it is not a visualisation and a second filter model beside `ReportFilter` would be one somebody keeps in step by hand.","narrative":"**Generated prose belongs with `ai.Suggestion`.** The source's narrative / insight text (*\"Admissions are 12% above last Tuesday\"*) is model output with traceability requirements, not a way of drawing a query result.","cohort":"**Not one of the eighteen.** It appears once in the source as a *usage* — *\"the Customer & Membership dashboard shall use cards, cohort and trend charts\"* — never as a specified component. A cohort view is a `matrix` or `heatmap` over a cohort dimension."},"x-ticvai-note":"**These marks cannot yet bind data.** `ReportColumn` carries `field`, `label`, `aggregation` and `format` and **no encoding role** — no axis, series, size or colour. A `number` needs none and an eight-mark enum survived without one; a `scatter` needs x, y, size and colour, and a `combo` needs a secondary axis with stated units. **Adding `ReportColumn.role` is the harder half of this decision and is deliberately not made here** — it is the field-wells model the source's builder specifies, and it belongs with the engine and semantic-layer split that needs an ADR first.\n"},"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose, and not yet specified.** Holds the tile's run parameters (keyed by the report's `ReportParameter.key`, as `RunReportRequest.parameters`) and its display settings — for `number`, the comparison, variance, sparkline and status icon. The per-visualisation display shape waits on the field-wells decision in `visualisation`'s `x-ticvai-note`.\n"},"refreshSeconds":{"type":"integer","minimum":30,"description":"Minimum thirty seconds. A tile refreshing every second is a load problem wearing a convenience costume.\n"},"position":{"type":"object","required":["row","column","width","height"],"properties":{"row":{"type":"integer"},"column":{"type":"integer"},"width":{"type":"integer"},"height":{"type":"integer"}}}}},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"KpiDefinition": {"type":"object","x-ticvai-persistence":"reporting.kpi_definition","description":"BI boards 2.5 and 10.2. **One definition, referenced everywhere** — otherwise *revenue* means two things in the same meeting.\n","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","description":"`takings` and `admissions` are seeded for every tenant as system KPIs (decided 28 September, audit R283), and the five accreditation KPIs for every tenant with the accreditation module (29 September, build pass). The seeded codes are `ReportingSystemKpi`.\n"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"domain":{"type":"string","nullable":true},"formula":{"type":"string","description":"**Expressed against the semantic model, not against tables.** A KPI written in SQL is a KPI that breaks when the warehouse is reshaped.\n"},"unit":{"type":"string","enum":["currency","count","percentage","duration","ratio","score"]},"higherIsBetter":{"type":"boolean","default":true,"description":"**Refund rate and revenue both go up.** Without this the status colour is a coin toss.\n"},"defaultPeriod":{"type":"string","nullable":true},"owner":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"KpiTarget": {"type":"object","x-ticvai-persistence":"reporting.kpi_target","description":"BI board 2.6. **The threshold is what turns a number into a status.**","required":["scopePath","period","target"],"properties":{"kpiId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","description":"The scope this target applies to. With `period`, the key `setKpiTargets` matches on."},"period":{"type":"string"},"target":{"$ref":"#/components/schemas/MetricValue"},"amberAt":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"redAt":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"stretch":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true}}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"SemanticModel": {"type":"object","x-ticvai-persistence":"reporting.semantic_model","description":"BI boards 3.3 and 10.6. **A vocabulary, not a schema.** Exposing joins to report authors produces reports that are wrong invisibly.\n","properties":{"version":{"type":"integer","readOnly":true,"description":"Assigned by the server on each publish."},"domains":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"datasets":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"name":{"type":"string"},"grain":{"type":"string","description":"**What one row means.** The single most common cause of a wrong report is a join that silently multiplied the grain.\n"},"fields":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"label":{"type":"string"},"dataType":{"$ref":"#/components/schemas/FieldType"},"aggregation":{"allOf":[{"$ref":"#/components/schemas/Aggregation"}],"nullable":true,"description":"The default aggregation for the field, where it has one."},"sensitive":{"type":"boolean","default":false},"description":{"type":"string","nullable":true}}}}}}}}}},"relationships":{"type":"array","items":{"type":"object","properties":{"fromDataset":{"type":"string"},"toDataset":{"type":"string"},"cardinality":{"type":"string","enum":["oneToOne","oneToMany","manyToOne","manyToMany"]}}}},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string"}}}
}
```
