# WS96 — Rental Management board 9

**10 screens · 26 operations · 29 schemas · 9 permissions**

Platform P08 Venue Management · ships as **venue-management** ·
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

- **Every control that can be refused must be gated.** 9 permissions apply here:
  `ASSET_MANAGE, ASSET_VIEW, INSPECTION_SUBMIT, MAINTENANCE_EXECUTE, PROCUREMENT_REQUEST, PRODUCT_VIEW, WORK_ORDER_MANAGE, WORK_ORDER_VERIFY, WORK_ORDER_VIEW`. A control nobody can use must say so,
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
| `BO-574` | Maintenance Command Center | B–D | 2 | 0 | 6 | 1 | 0 | 2 | — | notStarted (—) |
| `BO-575` | Maintenance Rule & Service Plan Configuration | B–D | 8 | 0 | 6 | 4 | 1 | 2 | — | notStarted (—) |
| `BO-576` | Maintenance Calendar & Scheduling | B–D | 7 | 10 | 6 | 10 | 3 | 2 | — | notStarted (—) |
| `BO-577` | Maintenance Work Order | B–D | 29 | 20 | 6 | 22 | 3 | 2 | — | notStarted (—) |
| `BO-578` | Technician Repair Workspace | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-579` | Parts, Cost & Maintenance Expense Tracking | B–D | 9 | 5 | 6 | 2 | 2 | 2 | — | notStarted (—) |
| `BO-580` | Asset Maintenance History & Lifecycle | B–D | 0 | 0 | 6 | 5 | 1 | 2 | — | notStarted (—) |
| `BO-581` | Return-to-Service Inspection & Approval | B–D | 0 | 0 | 6 | 3 | 1 | 3 | — | notStarted (—) |
| `BO-582` | Asset Retirement, Write-Off & Replacement Recommendation | B–D | 0 | 0 | 6 | 5 | 1 | 0 | — | notStarted (—) |
| `BO-583` | Maintenance Intelligence & Predictive AI | B–D | 0 | 18 | 6 | 1 | 2 | 2 | — | notStarted (—) |

## Thin screens in this batch

**BO-578, BO-580, BO-581, BO-582, BO-583 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-574` Maintenance Command Center

**Provide maintenance teams and rental management with a real-time view of rental asset health and maintenance workload.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_VIEW`, `WORK_ORDER_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/maintenance-command-center-bo-574` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search maintenance | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, location, product, asset, maintenance type, priority and 3 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Assigned to principal | picker: choose an assigned to principal | — | — | `listWorkOrders` ?assignedToPrincipalId |
| Status | select | — | Open · Assigned · In progress · Paused · Awaiting parts · Completed · Verified · Closed · Cancelled | `listWorkOrders` ?status |
| Priority | radio group | — | Low · Normal · High · Urgent · Emergency | `listWorkOrders` ?priority |
| Asset | upload, or pick from the media library | — | — | `listWorkOrders` ?assetId |
| Overdue only | toggle | off | — | `listWorkOrders` ?overdueOnly |
| From | date and time picker | — | — | `listWorkOrders` ?from |
| To | date and time picker | — | — | `listWorkOrders` ?to |
| Category | picker: choose a category | — | — | `listWorkOrders` ?categoryId |
| Within days | number field (days) | 14 | — | `getDueMaintenance` ?withinDays |
| From | date and time picker | — | — | `getDueMaintenance` ?from |
| To | date and time picker | — | — | `getDueMaintenance` ?to |
| Category | picker: choose a category | — | — | `getDueMaintenance` ?categoryId |

#### Outputs: what the screen shows and produces

**Shown**

**Assets Under Maintenance** (metric tile)

**Inspection Required** (metric tile)

**Preventive Maintenance Due** (metric tile)

**Overdue Maintenance** (metric tile)

**Corrective Repairs** (metric tile)

**Damage Repairs** (metric tile)

**Awaiting Parts** (metric tile)

**Ready for Return to Service** (metric tile)

**Average Downtime** (metric tile)

**Maintenance Alerts** (metric tile)

**Data it reads**: `listWorkOrders` (onLoad, Open work orders); `getDueMaintenance` (onLoad, What is due)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-575` Maintenance Rule & Service Plan Configuration: *Maintenance Rule & Service Plan Configuration*; carries `planId`
- → `BO-576` Maintenance Calendar & Scheduling: *Maintenance Calendar & Scheduling*
- → `BO-577` Maintenance Work Order: *Maintenance Work Order*; carries `workOrderId`
- → `BO-578` Technician Repair Workspace: *Technician Repair Workspace*; carries `workOrderId`
- → `BO-579` Parts, Cost & Maintenance Expense Tracking: *Parts, Cost & Maintenance Expense Tracking*; carries `workOrderId`
- → `BO-580` Asset Maintenance History & Lifecycle: *Asset Maintenance History & Lifecycle*; carries `assetId`
- → `BO-581` Return-to-Service Inspection & Approval: *Return-to-Service Inspection & Approval*; carries `workOrderId`
- → `BO-582` Asset Retirement, Write-Off & Replacement Recommendation: *Asset Retirement, Write-Off & Replacement Recommendation*; carries `assetId`
- → `BO-583` Maintenance Intelligence & Predictive AI: *Maintenance Intelligence & Predictive AI*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The maintenance list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the maintenance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No maintenance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the maintenance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listWorkOrders` → `WORK_ORDER_VIEW` (read) · staff
- `getDueMaintenance` → `ASSET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.2.4 | Automated Work Order Generation - System shall automatically generate preventive maintenance work orders. | Maintenance & Safety Management | CONTRACTED | `getDueMaintenance` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-574` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-574`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 1: Opens Maintenance Command Center → Provide maintenance teams and rental management with a real-time view of rental asset health and maintenance workload.
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F205 branch at step 1 (expected): when Nothing has been set up on Maintenance Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F205 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-574?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-575`, `BO-576`, `BO-577`, `BO-578`, `BO-579`, `BO-580`, `BO-581`, `BO-582`, `BO-583`.
- [ ] Every gated control is gated: `ASSET_VIEW`, `WORK_ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-575` Maintenance Rule & Service Plan Configuration

**Define when different rental products/assets require preventive maintenance. This is important because maintenance should not depend only on staff manually noticing a problem.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_MANAGE`, `ASSET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `planId` (navigation) |
| Route | `/rentals/maintenance-rule-service-plan-configuration-bo-575` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Product / Category | select field | — | — | — | — | — | — |
| Maintenance Type | select field | — | — | — | — | — | — |
| Trigger | select field | — | — | — | — | — | — |
| Service Checklist | select field | — | — | — | — | — | — |
| Estimated Duration | select field | — | — | — | — | — | — |
| Required Technician Skill | select field | — | — | — | — | — | — |
| Required Approval | select field | — | — | — | — | — | — |
| Post-Maintenance Inspection | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listMaintenancePlans` (onLoad, Service plans)

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The maintenance rule service configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the maintenance rule service untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No maintenance rule service configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither an interval nor a usage trigger supplied |

#### Permissions

- `listMaintenancePlans` → `ASSET_VIEW` (read) · staff
- `createMaintenancePlan` → `ASSET_MANAGE` (configure) · staff
- `updateMaintenancePlan` → `ASSET_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 16.5.24 | Preventive Maintenance - System shall support preventive maintenance schedules. | Device Management | CONTRACTED | `createMaintenancePlan` |
| 17.2.1 | Maintenance Plans - System shall support preventive maintenance plans. | Maintenance & Safety Management | CONTRACTED | `createMaintenancePlan` |
| 17.2.2 | Maintenance Schedules - System shall support maintenance scheduling. | Maintenance & Safety Management | CONTRACTED | `createMaintenancePlan` |
| 17.2.3 | Maintenance Frequencies - System shall support daily, weekly, monthly and annual schedules. | Maintenance & Safety Management | CONTRACTED | `createMaintenancePlan` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Preventive maintenance schedules (e.g. every 30 or 60 days) and periodic counts that flag shortages (e.g. 500 life jackets last month vs 495 this month). *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-768)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-575` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-575`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 2: Works in Maintenance Rule & Service Plan Configuration → Define when different rental products/assets require preventive maintenance. This is important because maintenance should not depend only on staff manually noticing a problem.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-575?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `ASSET_MANAGE`, `ASSET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-576` Maintenance Calendar & Scheduling

**Plan preventive and corrective maintenance while understanding its effect on rental capacity. The original requirement specifically calls for scheduled maintenance periods.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_VIEW`, `WORK_ORDER_MANAGE` (1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/maintenance-calendar-scheduling-bo-576` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Asset | select field | — | — | — | — | — | — |
| Maintenance Type | select field | — | — | — | — | — | — |
| Start Date/Time | select field | — | — | — | — | — | — |
| Expected Completion | select field | — | — | — | — | — | — |
| Technician | select field | — | — | — | — | — | — |
| Workshop/Location | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Within days | number field (days) | 14 | — | `getDueMaintenance` ?withinDays |
| From | date and time picker | — | — | `getDueMaintenance` ?from |
| To | date and time picker | — | — | `getDueMaintenance` ?to |
| Category | picker: choose a category | — | — | `getDueMaintenance` ?categoryId |

#### Outputs: what the screen shows and produces

**Shown**

**Calendar** (calendar view, from `getDueMaintenance`): Maintenance falling due, by day, week or month; a task opens a work order. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Sends the visible window as `from`/`to` and the category filter as `categoryId`.

| Shows | Format | Notes |
|---|---|---|
| Plan | the name it points at, never the id | — |
| Plan name | text | — |
| Asset | the image or video | — |
| Asset name | text | — |
| Criticality | chip: Safety critical, Revenue critical, Standard, Low | — |
| Due at | 1 Oct 2026, 14:30 | — |
| Is overdue | yes / no (icon or chip) | — |
| Days overdue | 1,234 | — |
| Triggered by | chip: Interval, Usage | — |
| Work order | the name it points at, never the id | — |

**Data it reads**: `getDueMaintenance` (onLoad, The maintenance calendar)

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The maintenance calendar scheduling configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the maintenance calendar scheduling untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No maintenance calendar scheduling configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getDueMaintenance` → `ASSET_VIEW` (read) · staff
- `createWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.2.4 | Automated Work Order Generation - System shall automatically generate preventive maintenance work orders. | Maintenance & Safety Management | CONTRACTED | `getDueMaintenance` |
| 16.5.25 | Corrective Maintenance - System shall support corrective maintenance tracking. | Device Management | CONTRACTED | `createWorkOrder` |
| 16.5.26 | Maintenance Work Orders - System shall support device maintenance work orders. | Device Management | CONTRACTED | `createWorkOrder` |
| 17.3.1 | Maintenance Requests - System shall support maintenance requests. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.3.2 | Breakdown Management - System shall support equipment breakdown management. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.3.3 | Emergency Maintenance - System shall support emergency maintenance requests. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.1 | Work Order Creation - System shall support work order creation. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.2 | Work Order Assignment - System shall support work order assignment. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.3 | Work Order Prioritization - System shall support work order prioritization. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.4 | Work Order Status Management - System shall support work order lifecycle management. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Calendars must support filtering by asset category so a team only sees maintenance relevant to them, e.g. an IT team sees turnstiles, printers and POS terminals, not unrelated categories. *(agreed · MoM 17 Sep 2026, 4.2 Preventive Maintenance Planning · DI-908)*
- Preventive maintenance schedules (e.g. every 30 or 60 days) and periodic counts that flag shortages (e.g. 500 life jackets last month vs 495 this month). *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-768)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-576` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-576`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 4: Works in Maintenance Calendar & Scheduling → Plan preventive and corrective maintenance while understanding its effect on rental capacity. The original requirement specifically calls for scheduled maintenance periods.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-576?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `ASSET_VIEW`, `WORK_ORDER_MANAGE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-577` Maintenance Work Order

**Create and manage the actual repair/service job.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VIEW` (1 operate, 1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `workOrderId` (navigation), `vendorServiceRequestId` (navigation) |
| Route | `/rentals/maintenance-work-order-bo-577` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Assigned to principal | picker: choose an assigned to principal | — | — | `listWorkOrders` ?assignedToPrincipalId |
| Status | select | — | Open · Assigned · In progress · Paused · Awaiting parts · Completed · Verified · Closed · Cancelled | `listWorkOrders` ?status |
| Priority | radio group | — | Low · Normal · High · Urgent · Emergency | `listWorkOrders` ?priority |
| Asset | upload, or pick from the media library | — | — | `listWorkOrders` ?assetId |
| Overdue only | toggle | off | — | `listWorkOrders` ?overdueOnly |
| From | date and time picker | — | — | `listWorkOrders` ?from |
| To | date and time picker | — | — | `listWorkOrders` ?to |
| Category | picker: choose a category | — | — | `listWorkOrders` ?categoryId |

**Sent by *Assign suggested technician*** (`updateWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | How the maintenance head confirms a `suggestWorkOrderAssignee` candidate (M17-13). | `updateWorkOrder` body |
| Priority `priority` | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | — | `updateWorkOrder` body |
| Required qualification codes `requiredQualificationCodes` | list of values (chips) | optional | — | at most 10 | — | — | `updateWorkOrder` body |
| Due at `dueAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateWorkOrder` body |
| Description `description` | text area | optional | — | max length 5000 | — | — | `updateWorkOrder` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateWorkOrder` body |

**Sent by *Request a vendor*** (`createVendorServiceRequest`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Work order `workOrderId` | picker: choose a work order | required | — | — | shows names, sends the id | — | `createVendorServiceRequest` body |
| Supplier `supplierId` | picker: choose a supplier | required | — | — | shows names, sends the id | — | `createVendorServiceRequest` body |
| Scope `scope` | text area | required | — | max length 2000 | — | What the vendor is asked to do. | `createVendorServiceRequest` body |
| Status `status` | select | optional | Draft | Draft · Sent · Accepted · Scheduled · Completed · Cancelled | — | — | `createVendorServiceRequest` body |
| Vendor reference `vendorReference` | text field | optional | — | max length 100 | — | — | `createVendorServiceRequest` body |
| Quoted cost `quotedCost` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createVendorServiceRequest` body |
| Final cost `finalCost` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createVendorServiceRequest` body |
| Scheduled visit at `scheduledVisitAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createVendorServiceRequest` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `createVendorServiceRequest` body |

**Sent by *Update vendor request*** (`updateVendorServiceRequest`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | optional | — | Draft · Sent · Accepted · Scheduled · Completed · Cancelled | — | — | `updateVendorServiceRequest` body |
| Vendor reference `vendorReference` | text field | optional | — | max length 100 | — | — | `updateVendorServiceRequest` body |
| Quoted cost `quotedCost` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `updateVendorServiceRequest` body |
| Final cost `finalCost` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `updateVendorServiceRequest` body |
| Scheduled visit at `scheduledVisitAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateVendorServiceRequest` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `updateVendorServiceRequest` body |

**Sent by *Save priority scoring*** (`setWorkOrderPriorityPolicy`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Weights `weights` | group | required | — | — | — | — | `setWorkOrderPriorityPolicy` body |
| Safety `weights.safety` | stepper or slider | required | — | min 0; max 100 | — | — | `setWorkOrderPriorityPolicy` body |
| Guest operations `weights.guestOperations` | stepper or slider | required | — | min 0; max 100 | — | — | `setWorkOrderPriorityPolicy` body |
| Revenue `weights.revenue` | stepper or slider | required | — | min 0; max 100 | — | — | `setWorkOrderPriorityPolicy` body |
| Criticality `weights.criticality` | stepper or slider | required | — | min 0; max 100 | — | — | `setWorkOrderPriorityPolicy` body |
| Bands `bands` | repeatable rows | required | — | at least 1; at most 5 | — | Highest first. A score at or above `minScore` takes `priority`. | `setWorkOrderPriorityPolicy` body |
| Min score `bands[].minScore` | stepper or slider | required | — | min 0; max 100 | — | — | `setWorkOrderPriorityPolicy` body |
| Priority `bands[].priority` | radio group | required | — | Low · Normal · High · Urgent · Emergency | — | — | `setWorkOrderPriorityPolicy` body |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Detail panel** (detail panel): One record, read-only.

**Priority and how it was set** (detail panel, from `getWorkOrder`): **The score and its source side by side** (decided 17 September, M17-01): *scored* (the venue policy), *asset override* or *manual*, so a supervisor sees why a fault is urgent.

| Shows | Format | Notes |
|---|---|---|
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |
| Priority score | 1,234 | The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01). |
| Priority source | chip: Scored, Asset override, Manual | Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`. |
| Fault assessment | grouped details | What the person raising a fault says about it, which the priority score reads (M17-01). |
| Required qualification codes | list or chips (count when long) | Skills the job needs (M17-13). |

**Suggested technicians** (data table, from `suggestWorkOrderAssignee`): **Smart assignment, confirmed by the maintenance head** (decided 17 September, M17-13). The ranking assigns nothing; *Assign* on a row sends its principal with `updateWorkOrder`.

| Shows | Format | Notes |
|---|---|---|
| Rank | 1,234 | — |
| Name | text | — |
| Has all qualifications | yes / no (icon or chip) | — |
| Missing qualification codes | list or chips (count when long) | — |
| On shift | yes / no (icon or chip) | On shift now or before the work order is due. |
| Open work order count | 1,234 | — |

**Vendor requests** (data table, from `listVendorServiceRequests`): Outside vendors engaged on this work order (decided 17 September, M17-13).

| Shows | Format | Notes |
|---|---|---|
| Supplier | the name it points at, never the id | — |
| Scope | text | What the vendor is asked to do. |
| Status | chip: Draft, Sent, Accepted, Scheduled, Completed, Cancelled | — |
| Vendor reference | text | — |
| Quoted cost | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Scheduled visit at | 1 Oct 2026, 14:30 | — |

**How fault priority is scored** (detail panel, from `getWorkOrderPriorityPolicy`): **The venue's weights and bands** (decided 17 September, M17-01): safety, guest operations, revenue and asset criticality, summing to 100.

| Shows | Format | Notes |
|---|---|---|
| Weights | grouped details | — |
| Bands | list or chips (count when long) | Highest first. A score at or above `minScore` takes `priority`. |
| Updated at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create work order (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Assign suggested technician (secondary button) | `updateWorkOrder` PATCH `/work-orders/{workOrderId}` | inline | WorkOrder | — | — |
| Request a vendor (secondary button) | `createVendorServiceRequest` POST `/vendor-service-requests` | VendorServiceRequest | VendorServiceRequest | 400 Validation failed; 409 The work order is closed or cancelled. | — |
| Update vendor request (secondary button) | `updateVendorServiceRequest` PATCH `/vendor-service-requests/{vendorServiceRequestId}` | inline | VendorServiceRequest | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The request is already `completed` or `cancelled`. | — |
| Save priority scoring (secondary button) | `setWorkOrderPriorityPolicy` PUT `/work-order-priority-policy` | WorkOrderPriorityPolicy | WorkOrderPriorityPolicy | 400 Weights that do not sum to 100, or bands that do not descend. | — |

**Data it reads**: `listWorkOrders` (onLoad, List work orders)

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The maintenance work order list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the maintenance work order untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No maintenance work order yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the maintenance work order are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 400 Weights that do not sum to 100, or bands that do not descend.; 409 The request is already `completed` or `cancelled`.; 409 The work order is closed or cancelled. |

#### Permissions

- `getWorkOrderPriorityPolicy` → `WORK_ORDER_VIEW` (read) · staff
- `setWorkOrderPriorityPolicy` → `WORK_ORDER_MANAGE` (configure) · staff
- `suggestWorkOrderAssignee` → `WORK_ORDER_VIEW` (read) · staff
- `listVendorServiceRequests` → `WORK_ORDER_VIEW` (read) · staff
- `createVendorServiceRequest` → `WORK_ORDER_MANAGE` (configure) · staff
- `updateVendorServiceRequest` → `WORK_ORDER_MANAGE` (configure) · staff
- `listWorkOrders` → `WORK_ORDER_VIEW` (read) · staff
- `getWorkOrder` → `WORK_ORDER_VIEW` (read) · staff
- `createWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `updateWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `attachWorkOrderEvidence` → `MAINTENANCE_EXECUTE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

22 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.4.8 | Work Order Audit Trail - System shall maintain work order audit logs. | Maintenance & Safety Management | CONTRACTED | `getWorkOrder` |
| 16.5.25 | Corrective Maintenance - System shall support corrective maintenance tracking. | Device Management | CONTRACTED | `createWorkOrder` |
| 16.5.26 | Maintenance Work Orders - System shall support device maintenance work orders. | Device Management | CONTRACTED | `createWorkOrder` |
| 17.3.1 | Maintenance Requests - System shall support maintenance requests. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.3.2 | Breakdown Management - System shall support equipment breakdown management. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.3.3 | Emergency Maintenance - System shall support emergency maintenance requests. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.1 | Work Order Creation - System shall support work order creation. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.2 | Work Order Assignment - System shall support work order assignment. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.3 | Work Order Prioritization - System shall support work order prioritization. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.4 | Work Order Status Management - System shall support work order lifecycle management. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 18.5.1 | Photo Capture - Users shall capture photos. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.2 | Video Capture - Users shall capture videos. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| … 10 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Smart assignment (confirmed by the maintenance head): technicians ranked by skill, shift and load; the ranking assigns nothing and Assign on a row does; outside vendor requests listed on the work order. *(agreed · MoM 17 Sep 2026, M17-13 · DI-924)*
- Work-order priority is shown with its source side by side (scored by venue policy, asset override, or manual); an asset carries a "fault priority override"; a new work order leaves priority empty to be scored; the venue sets weights and bands (safety, guest operations, revenue, asset criticality, summing to 100). *(agreed · MoM 17 Sep 2026, M17-01 · DI-923)*
- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-577` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-577`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 6: Works in Maintenance Work Order → Create and manage the actual repair/service job.

#### Acceptance for the design

- [ ] Every input above is drawn (29), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-577?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create work order, Cancel, Assign suggested technician, Request a vendor, Update vendor request, Save priority scoring.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-578` Technician Repair Workspace

**Provide the technician with a focused operational screen for executing maintenance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE` (1 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `workOrderId` (navigation) |
| Route | `/rentals/technician-repair-workspace-bo-578` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The technician repair list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the technician repair untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No technician repair yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the technician repair are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Completion photographs required for this category and none supplied; 400 Validation failed; 409 Action inconsistent with the current timer state |

#### Permissions

- `startWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `recordWorkOrderTime` → `WORK_ORDER_MANAGE` (configure) · staff
- `completeWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-578` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-578`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 8: Works in Technician Repair Workspace → Provide the technician with a focused operational screen for executing maintenance.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-578?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-579` Parts, Cost & Maintenance Expense Tracking

**Capture the operational cost associated with maintaining rental equipment. This should integrate with the broader Inventory/Procurement and Finance modules rather than recreate them.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PROCUREMENT_REQUEST`, `PRODUCT_VIEW`, `WORK_ORDER_MANAGE` (1 operate, 1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `workOrderId` (navigation), `stockReservationId` (navigation) |
| Route | `/rentals/parts-cost-maintenance-expense-tracking-bo-579` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Sent by *Reserve parts*** (`createStockReservation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `createStockReservation` body |
| Item `itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `createStockReservation` body |
| Location `locationId` | picker: choose a location | required | — | — | shows names, sends the id | — | `createStockReservation` body |
| Quantity `quantity` | number field | required | — | more than 0 | — | — | `createStockReservation` body |
| Source type `sourceType` | radio group | required | — | Work order · Rental agreement · Order · Transfer · Other | — | What a stock reservation is for (decided 17 September, M17-02; `rentalAgreement` is the existing use from `rental.agreement_item`). | `createStockReservation` body |
| Source `sourceId` | picker: choose a source | required | — | — | shows names, sends the id | The id of what the stock is reserved for: a work order, a rental agreement or an order. | `createStockReservation` body |
| Expires at `expiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createStockReservation` body |
| Released at `releasedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createStockReservation` body |

**Sent by *Release reservation*** (`releaseStockReservation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 300 | — | — | `releaseStockReservation` body |

#### Outputs: what the screen shows and produces

**Shown**

**Parts reserved for this work order** (data table, from `listStockReservations`): **Reserved in the general inventory, not a maintenance stock** (decided 17 September, M17-02). Sends `?sourceType=workOrder&sourceId=` the work order. Recording parts issues from the reservation first.

| Shows | Format | Notes |
|---|---|---|
| Item | the name it points at, never the id | — |
| Location | the name it points at, never the id | — |
| Quantity | 1,234.5 | — |
| Status | chip: Active, Consumed, Released, Expired | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Reserve parts (secondary button) | `createStockReservation` POST `/stock-reservations` | InventoryStockReservation | InventoryStockReservation | 400 Validation failed; 409 Not enough free stock at the location. | — |
| Release reservation (secondary button) | `releaseStockReservation` POST `/stock-reservations/{stockReservationId}/release` | inline | InventoryStockReservation | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The reservation is not `active`. | — |

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The parts cost maintenance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the parts cost maintenance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No parts cost maintenance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the parts cost maintenance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Insufficient stock; 409 Not enough free stock at the location.; 409 The reservation is not `active`. |

#### Permissions

- `listStockReservations` → `PRODUCT_VIEW` (read) · staff
- `createStockReservation` → `PROCUREMENT_REQUEST` (operate) · staff
- `releaseStockReservation` → `PROCUREMENT_REQUEST` (operate) · staff
- `recordWorkOrderParts` → `WORK_ORDER_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.6.1 | Spare Parts Management - System shall support maintenance spare parts management. | Maintenance & Safety Management | CONTRACTED | `recordWorkOrderParts` |
| 17.6.3 | Spare Parts Consumption - System shall record spare parts consumption. | Maintenance & Safety Management | CONTRACTED | `recordWorkOrderParts` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Work-order parts are reserved in the general inventory; the reserve action is hidden offline, and a refusal for short stock names the part. *(agreed · MoM 17 Sep 2026, M17-02 · DI-925)*
- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-579` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-579`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 10: Works in Parts, Cost & Maintenance Expense Tracking → Capture the operational cost associated with maintaining rental equipment. This should integrate with the broader Inventory/Procurement and Finance modules rather than recreate them.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-579?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel, Reserve parts, Release reservation.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `PROCUREMENT_REQUEST`, `PRODUCT_VIEW`, `WORK_ORDER_MANAGE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-580` Asset Maintenance History & Lifecycle

**Provide the complete maintenance history of an individual serialized rental asset. The original requirement specifically requires maintenance history tracking.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/rentals/asset-maintenance-history-lifecycle-bo-580` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset maintenance history list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset maintenance history untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No asset maintenance history yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the asset maintenance history are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getAssetHistory` → `ASSET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 16.5.27 | Maintenance History - System shall maintain maintenance history. | Device Management | CONTRACTED | `getAssetHistory` |
| 17.1.8 | Asset History - System shall maintain complete asset history. | Maintenance & Safety Management | CONTRACTED | `getAssetHistory` |
| 17.3.7 | Service History - System shall maintain service history. | Maintenance & Safety Management | CONTRACTED | `getAssetHistory` |
| 18.3.4 | Asset History - Users shall view maintenance history. | Employee Mobile App & AI Assistant | CONTRACTED | `getAssetHistory` |
| 18.3.5 | Asset Documentation - Users shall access manuals and documents. | Employee Mobile App & AI Assistant | CONTRACTED | `getAssetHistory` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-580` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-580`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 12: Works in Asset Maintenance History & Lifecycle → Provide the complete maintenance history of an individual serialized rental asset. The original requirement specifically requires maintenance history tracking.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-580?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `ASSET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-581` Return-to-Service Inspection & Approval

**Ensure repaired equipment does not automatically become rentable when a technician clicks “Repair Complete.” This is one of the most important controls in Board 9.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `INSPECTION_SUBMIT`, `WORK_ORDER_VERIFY` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `workOrderId` (navigation) |
| Route | `/rentals/return-to-service-inspection-approval-bo-581` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Submit inspection (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The return-to-service inspection approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the return-to-service inspection approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No return-to-service inspection approval yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the return-to-service inspection approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A required item was not answered |

#### Permissions

- `submitInspection` → `INSPECTION_SUBMIT` (operate) · staff
- `verifyWorkOrder` → `WORK_ORDER_VERIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.5.7 | Safety Audits - System shall support safety audits. | Maintenance & Safety Management | CONTRACTED | `submitInspection` |
| 17.4.6 | Work Order Approval - System shall support work order approvals. | Maintenance & Safety Management | CONTRACTED | `verifyWorkOrder` |
| 17.4.7 | Work Order Closure - System shall support work order closure workflows. | Maintenance & Safety Management | CONTRACTED | `verifyWorkOrder` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Serviced items return to service; retirement/write-off records the write-off value; maintenance AI view shows at-risk assets, upcoming maintenance cost and total spend. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-770)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-581` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-581`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 14: Works in Return-to-Service Inspection & Approval → Ensure repaired equipment does not automatically become rentable when a technician clicks “Repair Complete.” This is one of the most important controls in Board 9.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-581?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Submit inspection, Cancel.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `INSPECTION_SUBMIT`, `WORK_ORDER_VERIFY`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-582` Asset Retirement, Write-Off & Replacement Recommendation

**Manage assets that should no longer remain in the active rental fleet.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_MANAGE`, `ASSET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/rentals/asset-retirement-write-off-replacement-recommendation-bo-582` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save asset status (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset retirement write-off list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset retirement write-off untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No asset retirement write-off yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the asset retirement write-off are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Return to service attempted without the inspection this asset category requires. |

#### Permissions

- `setAssetStatus` → `ASSET_MANAGE` (configure) · staff
- `getAssetHistory` → `ASSET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 16.5.27 | Maintenance History - System shall maintain maintenance history. | Device Management | CONTRACTED | `getAssetHistory` |
| 17.1.8 | Asset History - System shall maintain complete asset history. | Maintenance & Safety Management | CONTRACTED | `getAssetHistory` |
| 17.3.7 | Service History - System shall maintain service history. | Maintenance & Safety Management | CONTRACTED | `getAssetHistory` |
| 18.3.4 | Asset History - Users shall view maintenance history. | Employee Mobile App & AI Assistant | CONTRACTED | `getAssetHistory` |
| 18.3.5 | Asset Documentation - Users shall access manuals and documents. | Employee Mobile App & AI Assistant | CONTRACTED | `getAssetHistory` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Serviced items return to service; retirement/write-off records the write-off value; maintenance AI view shows at-risk assets, upcoming maintenance cost and total spend. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-770)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-582` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-582`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 16: Works in Asset Retirement, Write-Off & Replacement Recommendation → Manage assets that should no longer remain in the active rental fleet.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-582?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save asset status, Cancel.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `ASSET_MANAGE`, `ASSET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-583` Maintenance Intelligence & Predictive AI

**Use AI to move TICVAI from reactive maintenance toward predictive maintenance. This is where I recommend making the module significantly stronger than the original matrix.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/maintenance-intelligence-predictive-ai-bo-583` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Within days | number field (days) | 14 | — | `getDueMaintenance` ?withinDays |
| From | date and time picker | — | — | `getDueMaintenance` ?from |
| To | date and time picker | — | — | `getDueMaintenance` ?to |
| Category | picker: choose a category | — | — | `getDueMaintenance` ?categoryId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every maintenance intelligence predictive** (data table)

| Shows | Format | Notes |
|---|---|---|
| Assets at risk | text | not in the schema: `Assets at Risk` |
| Predicted failures | text | not in the schema: `Predicted Failures` |
| Upcoming preventive maintenance | text | not in the schema: `Upcoming Preventive Maintenance` |
| Repeat failures | text | not in the schema: `Repeat Failures` |
| High maintenance cost assets | text | not in the schema: `High Maintenance Cost Assets` |
| Downtime by product | text | not in the schema: `Downtime by Product` |
| Maintenance impact on availability | text | not in the schema: `Maintenance Impact on Availability` |
| Mean time between failures | text | not in the schema: `Mean Time Between Failures` |
| Mean time to repair | text | not in the schema: `Mean Time to Repair` |

**The selected maintenance intelligence predictive** (detail panel): The pack groups this record's detail under its own headings: “BIKE-018”, “Instead of simply saying”, “Every 30 Days”, “Every 50 Rentals”, “Every 100 Rental Hours”, “Whichever Happens First”.

| Shows | Format | Notes |
|---|---|---|
| Assets at risk | text | not in the schema: `Assets at Risk` |
| Predicted failures | text | not in the schema: `Predicted Failures` |
| Upcoming preventive maintenance | text | not in the schema: `Upcoming Preventive Maintenance` |
| Repeat failures | text | not in the schema: `Repeat Failures` |
| High maintenance cost assets | text | not in the schema: `High Maintenance Cost Assets` |
| Downtime by product | text | not in the schema: `Downtime by Product` |
| Maintenance impact on availability | text | not in the schema: `Maintenance Impact on Availability` |
| Mean time between failures | text | not in the schema: `Mean Time Between Failures` |
| Mean time to repair | text | not in the schema: `Mean Time to Repair` |

**Data it reads**: `getDueMaintenance` (onLoad, Predictive maintenance)

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The maintenance intelligence predictive list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the maintenance intelligence predictive untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No maintenance intelligence predictive yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the maintenance intelligence predictive are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getDueMaintenance` → `ASSET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.2.4 | Automated Work Order Generation - System shall automatically generate preventive maintenance work orders. | Maintenance & Safety Management | CONTRACTED | `getDueMaintenance` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- In rentals AI's practical role is reporting and maintenance-scheduling recommendations; day-to-day rental operations stay staff-managed. *(agreed · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-772)*
- Serviced items return to service; retirement/write-off records the write-off value; maintenance AI view shows at-risk assets, upcoming maintenance cost and total spend. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-770)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-583` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-583`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 18: Works in Maintenance Intelligence & Predictive AI → Use AI to move TICVAI from reactive maintenance toward predictive maintenance. This is where I recommend making the module significantly stronger than the original matrix.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-583?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `ASSET_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P08 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-030, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-043, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051, DI-052 (each is in the design inputs below).

**Workshop tracker rows about P08 as a whole** (1: 1 open, 0 closed). Open first; a closed row says where it went on 30 September.

- **S8** Venue Management back-end configuration wireframes *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*

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

### Across P08 Venue Management

- Qossai: configuration screens should consolidate related functionality, potentially merging 3-4 previously separate screens into one, rather than the repetitive one-screen-per-concept pattern of the AI-built reference system. *(agreed · MoM 24 Sep 2026, 4.5 Screen Consolidation Philosophy · DI-987)*
- **Open question.** Open: should AI monitoring live in one centralised AI command dashboard or be distributed as widgets in each functional module's own dashboard? Allam: Softlabs' call; the current proposal is illustrative and Softlabs may propose a better structure. *(open · MoM 18 Sep 2026, 4.4 AI Governance — Risk, Compliance & Continuous Monitoring · DI-936)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- **Open question.** Allam: a user's visibility must be restrictable to specific outlets (an F&B manager of one outlet should not see other outlets' items); also relevant for ticketing/event-specific access. Implementation approach still open. *(open · MoM 18 Aug 2026, 4.6 Role-Based & Outlet-Level Access Control — Open Item · DI-331)*
- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*
- Back office is role-driven from any device: a finance user signing in from a workstation, laptop or home sees only finance reports and related information. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-248)*
- Built-in help menu with step-by-step tutorials with screenshots for common tasks (e.g. how to sell a ticket at the POS). *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-160)*
- Custom data-capture fields ("data mask") at account, event, extended-ticket and product level: field types text, dropdown, radio, true/false; multi-language labels; validation (min/max length, required/optional); reusable value lists (e.g. country list). Standard fields come out of the box. *(agreed · MoM 7 Aug 2026, 6. Data Mask: Flexible Custom Data Capture · DI-155)*
- Load/traffic dashboards respect the tenancy model: a venue manager sees traffic for their own venue only. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-061)*
- Allam: queue management is built into the system (not third-party) so traffic entering the site can be throttled from the back office itself. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-060)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Documentation deliverable includes user guides and help content; the preview shows a TICVAI Help Center with categories (Getting Started, Events, Tickets, Orders, Payments, Memberships, Access Control, Reports, Integrations), a "Welcome to TICVAI" getting-started article and Quick Links (Create an Event, Set Pricing, Manage Access, View Reports). *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - What We Deliver / Key Deliverables Preview · DI-052)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- AI Assistant panel: a short framing ("Based on last 30 days, here are 3 actions that can improve your revenue") then actionable recommendations, each with its potential impact (e.g. "Increase pricing for VIP seats, +12%") and a chevron, plus "View all recommendations". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - AI Panels · DI-043)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Back-office shell: collapsible left sidebar with Overview, Events, Tickets, Orders, Customers, Memberships, Access Control, POS, Reports, Analytics, AI Assistant, Settings, and the signed-in user (name, role) at the bottom; top bar with global search (Cmd+K), current time and date, Notifications with unread dot, and user menu. *(agreed · Design Vision Book 29 Jul 2026, 04 Dashboard Vision (p4) - navigation shell · DI-030)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*
- Reports and historical searches must still retrieve archived transactions when required; the retention period (e.g. keep 3 of 5+ years live) is configurable per customer, archival manual or automated. *(agreed · MoM 28 Jul 2026, 23. Database Optimisation and Archiving · DI-018)*
- Back-office controls for the waiting room: configurable maximum active users and admission intervals, set per customer and venue. *(agreed · MoM 28 Jul 2026, 19. Auto-scaling and Virtual Waiting Room · DI-017)*

**15 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"attachWorkOrderEvidence": {"method":"POST","path":"/work-orders/{workOrderId}/attachments","contract":"maintenance","summary":"Photo, video, document, note or signature","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrderAttachment"},
"completeWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/complete","contract":"maintenance","summary":"Complete a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"createMaintenancePlan": {"method":"POST","path":"/maintenance-plans","contract":"maintenance","summary":"Create a planned maintenance schedule","permission":"ASSET_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MaintenancePlan","responds":"MaintenancePlan"},
"createStockReservation": {"method":"POST","path":"/stock-reservations","contract":"inventory","summary":"Reserve stock for a work order or another need","permission":"PROCUREMENT_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"InventoryStockReservation","responds":"InventoryStockReservation"},
"createVendorServiceRequest": {"method":"POST","path":"/vendor-service-requests","contract":"maintenance","summary":"Engage an outside vendor on a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VendorServiceRequest","responds":"VendorServiceRequest"},
"createWorkOrder": {"method":"POST","path":"/work-orders","contract":"maintenance","summary":"Raise a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateWorkOrderRequest","responds":"WorkOrder"},
"getAssetHistory": {"method":"GET","path":"/assets/{assetId}/history","contract":"maintenance","summary":"Service history","permission":"ASSET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getDueMaintenance": {"method":"GET","path":"/maintenance-plans/due","contract":"maintenance","summary":"Planned tasks due or overdue","permission":"ASSET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"withinDays","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null}],"requestBody":null,"responds":"DueMaintenanceTask"},
"getWorkOrder": {"method":"GET","path":"/work-orders/{workOrderId}","contract":"maintenance","summary":"Read a work order","permission":"WORK_ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WorkOrderDetail"},
"getWorkOrderPriorityPolicy": {"method":"GET","path":"/work-order-priority-policy","contract":"maintenance","summary":"Read how a fault's priority is scored","permission":"WORK_ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WorkOrderPriorityPolicy"},
"listMaintenancePlans": {"method":"GET","path":"/maintenance-plans","contract":"maintenance","summary":"List planned maintenance schedules","permission":"ASSET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listStockReservations": {"method":"GET","path":"/stock-reservations","contract":"inventory","summary":"Soft holds on stock","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"sourceType","in":"query","required":null},{"name":"sourceId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVendorServiceRequests": {"method":"GET","path":"/vendor-service-requests","contract":"maintenance","summary":"Requests sent to outside vendors","permission":"WORK_ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workOrderId","in":"query","required":null},{"name":"supplierId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkOrders": {"method":"GET","path":"/work-orders","contract":"maintenance","summary":"List work orders","permission":"WORK_ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assignedToPrincipalId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"assetId","in":"query","required":null},{"name":"overdueOnly","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"recordWorkOrderParts": {"method":"POST","path":"/work-orders/{workOrderId}/parts","contract":"maintenance","summary":"Record parts consumed","permission":"WORK_ORDER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrderDetail"},
"recordWorkOrderTime": {"method":"POST","path":"/work-orders/{workOrderId}/time","contract":"maintenance","summary":"Start, pause or stop work","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"releaseStockReservation": {"method":"POST","path":"/stock-reservations/{stockReservationId}/release","contract":"inventory","summary":"Give reserved stock back","permission":"PROCUREMENT_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"InventoryStockReservation"},
"setAssetStatus": {"method":"PUT","path":"/assets/{assetId}/status","contract":"maintenance","summary":"Take an asset out of service or return it","permission":"ASSET_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetAssetStatusRequest","responds":"AssetStatusResult"},
"setWorkOrderPriorityPolicy": {"method":"PUT","path":"/work-order-priority-policy","contract":"maintenance","summary":"Set how a fault's priority is scored","permission":"WORK_ORDER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkOrderPriorityPolicy","responds":"WorkOrderPriorityPolicy"},
"startWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/start","contract":"maintenance","summary":"Work has begun","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"submitInspection": {"method":"POST","path":"/inspections","contract":"maintenance","summary":"Submit a completed inspection","permission":"INSPECTION_SUBMIT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SubmitInspectionRequest","responds":"InspectionResult"},
"suggestWorkOrderAssignee": {"method":"GET","path":"/work-orders/{workOrderId}/assignee-suggestions","contract":"maintenance","summary":"Who should take this work order, ranked","permission":"WORK_ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"updateMaintenancePlan": {"method":"PATCH","path":"/maintenance-plans/{planId}","contract":"maintenance","summary":"Amend or suspend a plan","permission":"ASSET_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MaintenancePlan"},
"updateVendorServiceRequest": {"method":"PATCH","path":"/vendor-service-requests/{vendorServiceRequestId}","contract":"maintenance","summary":"Move a vendor request along","permission":"WORK_ORDER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"VendorServiceRequest"},
"updateWorkOrder": {"method":"PATCH","path":"/work-orders/{workOrderId}","contract":"maintenance","summary":"Assign, reprioritise or amend","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"verifyWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/verify","contract":"maintenance","summary":"Supervisor verification","permission":"WORK_ORDER_VERIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Asset": {"x-ticvai-persistence":"maintenance.asset","allOf":[{"$ref":"#/components/schemas/CreateAssetRequest"},{"type":"object","x-ticvai-retired-columns":["is_maintenance_overdue","document_refs"],"required":["id","status"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid","nullable":true,"description":"1.2.x. **Where this asset is also bookable.** An AV rig is an asset to maintain and a resource to allocate, and they are the same object seen from two sides.\n**`resources` owns the calendar and this owns the condition.** An asset out of service makes its resource unbookable, which is one link rather than two models of availability.\n"},"deviceId":{"type":"string","format":"uuid","nullable":true,"description":"BL-160. **Where this asset is also a registered device.** A turnstile is an asset to maintain and a device to operate, and — exactly as with `resourceId` above — they are the same object seen from two sides.\n**Nothing joined them before this.** A turnstile controller reporting `needsAttention` could not raise a work order against itself, and an engineer closing one had no way back to the device whose firmware caused it.\n**Null for most assets and for most devices.** A chiller is not a device and a signature pad is not on the asset register; the link is sparse, and it lives here rather than on `platform.device` because `platform` is the foundation tier and a foreign key pointing from it into `maintenance` would invert the tiers — every cell running a spine would carry a column for a satellite it may not deploy.\n"},"acquisitionCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"acquiredOn":{"type":"string","format":"date","nullable":true},"depreciation":{"type":"object","nullable":true,"description":"**Recorded here and posted by `finance`.** Depreciation is an accounting act and the asset register is where the useful life is actually known — an engineer knows a chiller lasts fifteen years and an accountant knows what to do about it.\n","properties":{"method":{"type":"string","enum":["straightLine","reducingBalance","unitsOfProduction","none"]},"usefulLifeMonths":{"type":"integer"},"residualValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accumulatedDepreciation":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"retiredOn":{"type":"string","format":"date","nullable":true,"description":"**Retirement is not deletion.** A work order from three years ago still names this asset, and an inspection record with no asset is an inspection of nothing.\n"},"disposalProceeds":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"$ref":"#/components/schemas/AssetStatus"},"statusReason":{"type":"string","nullable":true},"openWorkOrderCount":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Work orders on this asset whose status is `open`, `assigned`, `inProgress`, `paused` or `awaitingParts` — the same set `AssetDetail.openWorkOrders` returns. **Maintained on write**: `createWorkOrder` and every transition into or out of that set (complete, cancel, close, reject back to open) adjust it in the same transaction as the work-order row.\n"},"nextMaintenanceDueAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The earliest `nextDueAt` among this asset's active maintenance plans; null when none has one. **Maintained on write**: recomputed whenever one of those plans is created, amended, suspended or has its `nextDueAt` moved by a completed work order. `listAssets?maintenanceDue` filters on this column against the clock.\n"},"isMaintenanceOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`nextMaintenanceDueAt` is in the past at the moment of the read. **Computed on read and not stored** — it depends on the clock, so a stored copy is stale the minute after it is written.\n"},"lastInspectionAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`performedAt` of the latest inspection submitted against this asset. **Maintained on write** by `submitInspection`, in the same transaction as the inspection row; an inspection synced late with an earlier `performedAt` does not move it back.\n"},"usageCounter":{"type":"number","nullable":true,"description":"Cycles, hours or kilometres. Drives usage-based maintenance."}}}]},
"AssetCriticality": {"type":"string","enum":["safetyCritical","revenueCritical","standard","low"]},
"AssetHistoryEntry": {"x-ticvai-persistence":"none — union view over work orders, inspections, incidents and asset status changes","type":"object","description":"**Every kind has a source.** `workOrder` is a work-order row, `inspection` an inspection, `incident` an incident, `statusChange` a `maintenance.asset_status_change` row. `partReplaced` is a completed work order whose `resolutionCode` is `partReplaced`, and `planCompleted` a completed work order with a `sourcePlanId` — both read from `maintenance.work_order`, not stored twice.\n","required":["kind","occurredAt","summary"],"properties":{"kind":{"type":"string","enum":["workOrder","inspection","incident","statusChange","partReplaced","planCompleted"]},"referenceId":{"type":"string","format":"uuid","nullable":true,"description":"The source row's id: a work order, inspection or incident, or an `asset_status_change` id. A uuid, as every id is (ADR-0056).\n"},"summary":{"type":"string"},"principalId":{"type":"string","format":"uuid","nullable":true},"occurredAt":{"type":"string","format":"date-time"}}},
"AssetStatus": {"type":"string","enum":["inService","outOfService","underMaintenance","awaitingParts","retired","disposed"]},
"AssetStatusResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["asset","downstreamEffects"],"properties":{"asset":{"$ref":"#/components/schemas/Asset"},"downstreamEffects":{"type":"object","description":"What else changed. Surfaced so the person taking a ride out of service sees the commercial consequence at the moment they do it.\n","properties":{"productsSuspended":{"type":"array","items":{"type":"string","format":"uuid"}},"accessPointBlocked":{"type":"boolean"},"performancesAffected":{"type":"integer"},"workOrderId":{"type":"string","format":"uuid","nullable":true}}}}},
"CreateWorkOrderRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","title","venueId","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"title":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":5000},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"kind":{"allOf":[{"$ref":"#/components/schemas/WorkOrderKind"}],"default":"corrective"},"priority":{"allOf":[{"$ref":"#/components/schemas/WorkOrderPriority"}],"description":"**Optional since 29 September** (M17-01). Sent, it is `manual` and wins. Absent, the asset's `priorityOverride` applies, and failing that the venue's `WorkOrderPriorityPolicy` scores the fault.\n"},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","maxItems":10,"items":{"type":"string"},"description":"Skills the job needs, as qualification codes; `suggestWorkOrderAssignee` ranks by them (M17-13)."},"categoryId":{"type":"string","format":"uuid"},"assignedToPrincipalId":{"type":"string","format":"uuid"},"dueAt":{"type":"string","format":"date-time"},"attachmentRefs":{"type":"array","description":"Photo-first. Expected at creation, not added later from memory.","items":{"type":"string"}},"takeAssetOutOfService":{"type":"boolean","default":false,"description":"Raise and immediately suspend the asset. For a fault found on a live ride, the two are one action.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"DueMaintenanceTask": {"x-ticvai-persistence":"none — computed","type":"object","required":["planId","assetId","assetName","dueAt","isOverdue","criticality"],"properties":{"planId":{"type":"string","format":"uuid"},"planName":{"type":"string"},"assetId":{"type":"string","format":"uuid"},"assetName":{"type":"string"},"criticality":{"$ref":"#/components/schemas/AssetCriticality"},"dueAt":{"type":"string","format":"date-time"},"isOverdue":{"type":"boolean"},"daysOverdue":{"type":"integer"},"triggeredBy":{"type":"string","enum":["interval","usage"]},"workOrderId":{"type":"string","format":"uuid","nullable":true}}},
"Inspection": {"x-ticvai-persistence":"maintenance.inspection","type":"object","required":["id","templateId","venueId","outcome","performedByPrincipalId","performedAt"],"properties":{"id":{"type":"string","format":"uuid"},"templateId":{"type":"string","format":"uuid"},"templateName":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"outcome":{"$ref":"#/components/schemas/InspectionOutcome"},"failedItemCount":{"type":"integer"},"failedSafetyCriticalCount":{"type":"integer"},"performedByPrincipalId":{"type":"string","format":"uuid","description":"An inspection nobody signed is not an inspection."},"performedAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true},"retainUntil":{"type":"string","format":"date","nullable":true}}},
"InspectionItem": {"x-ticvai-persistence":"maintenance.inspection_item","type":"object","description":"**One answer to one question, which the API has always accepted and never stored.** `SubmitInspectionRequest.responses[]` takes a key, a value, a pass flag, a note and attachments; the only persistence ever claimed for them was `maintenance.inspection_response`, a table that does not exist.\nSo `maintenance.inspection_template_item` held the questions, `maintenance.inspection` held `failedItemCount` and `failedSafetyCriticalCount`, and **which check failed was accepted over the wire and dropped** — on a record that takes an asset out of service.\nReturned on `InspectionResult`, not on `Inspection`: `listInspections` returns the latter in a list, and twenty item rows per inspection on a list screen is the wrong trade. The counts stay for exactly that reason.\n","required":["id","inspectionId","itemKey"],"properties":{"id":{"type":"string","format":"uuid"},"inspectionId":{"type":"string","format":"uuid"},"templateItemId":{"type":"string","format":"uuid","nullable":true,"description":"**Nullable because a template changes and an inspection does not.** An answer recorded against an item that was later removed still has to be readable, so the key below is the durable record and this is the live link.\n"},"itemKey":{"type":"string","maxLength":120,"description":"The template item's `key`, copied at submission and never updated."},"label":{"type":"string","nullable":true,"description":"The question as it was asked, copied at submission. **A template reworded next season must not silently reword last season's inspection.**\n"},"value":{"nullable":true,"description":"Whatever the item's `kind` calls for — a boolean, a number, a string."},"passed":{"type":"boolean","nullable":true,"description":"Null where the item is informational rather than pass or fail."},"isSafetyCritical":{"type":"boolean","default":false,"description":"Copied from the template item at submission, for the same reason as `label`: it is what makes `failedSafetyCriticalCount` reproducible, and the template can change.\n"},"note":{"type":"string","maxLength":1000,"nullable":true},"attachmentAssetIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"**A deliberate array, and the same exception as `workforce.sync_conflict.affectedAssignmentIds`**: evidence attached to this answer at the moment it was recorded. It is never queried from the other end — nobody asks which inspection items reference a photograph — and it must not change when an asset library is reorganised.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"InspectionResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["inspection","consequences"],"properties":{"inspection":{"$ref":"#/components/schemas/Inspection"},"items":{"type":"array","description":"**The answers, which had nowhere to live until 20 September.** A failed safety-critical item takes an asset out of service and `consequences` below says it happened; this says which check caused it.\n","items":{"$ref":"#/components/schemas/InspectionItem"}},"consequences":{"type":"object","description":"What the submission triggered. A failed safety-critical item takes the asset out of service without waiting for anyone to decide.\n","properties":{"assetTakenOutOfService":{"type":"boolean"},"workOrdersRaised":{"type":"array","items":{"type":"string","format":"uuid"}},"productsSuspended":{"type":"array","items":{"type":"string","format":"uuid"}},"escalatedToPrincipalId":{"type":"string","format":"uuid","nullable":true}}}}},
"InventoryStockReservation": {"type":"object","x-ticvai-persistence":"inventory.stock_reservation","description":"**Taken from the backend workbook, 20 September.** Temporarily reserves stock for an order or operational requirement so it cannot be allocated elsewhere.","required":["itemId","locationId","quantity","sourceType","sourceId","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"itemId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"quantity":{"type":"number","exclusiveMinimum":0},"sourceType":{"$ref":"#/components/schemas/StockReservationSourceType"},"sourceId":{"type":"string","format":"uuid","description":"The id of what the stock is reserved for: a work order, a rental agreement or an order. A uuid, as every id is (ADR-0056); it was text from 29 September to 30 September because a work order id was then 26-character text (M17-02)."},"status":{"type":"string","enum":["active","consumed","released","expired"],"readOnly":true},"expiresAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"releasedAt":{"type":"string","format":"date-time","nullable":true}}},
"MaintenancePlan": {"x-ticvai-persistence":"maintenance.preventive_plan","type":"object","required":["id","name","assetId","taskTemplate"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":200},"assetId":{"type":"string","format":"uuid"},"assetCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"Applies to every asset in the category rather than one."},"intervalDays":{"type":"integer","nullable":true,"description":"Elapsed-time trigger."},"usageInterval":{"type":"number","nullable":true,"description":"Usage trigger — cycles, hours, kilometres. **Whichever comes first** when both are set. A ride serviced every three months or ten thousand cycles is one plan.\n"},"leadTimeDays":{"type":"integer","default":7,"description":"How far ahead the work order is generated, so parts can be ordered before the job is already late.\n"},"taskTemplate":{"type":"object","required":["title","priority"],"properties":{"title":{"type":"string"},"description":{"type":"string"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"estimatedMinutes":{"type":"integer"},"inspectionTemplateId":{"type":"string","format":"uuid"},"requiredPartIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},"lastCompletedAt":{"type":"string","format":"date-time","nullable":true},"nextDueAt":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ResolutionCode": {"type":"string","enum":["repaired","partReplaced","adjusted","cleaned","noFaultFound","referredExternal","replaced","deferred"]},
"SetAssetStatusRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["status","reason","recordedAt"],"properties":{"status":{"$ref":"#/components/schemas/AssetStatus"},"reason":{"type":"string","minLength":3,"maxLength":1000},"inspectionId":{"type":"string","format":"uuid","nullable":true,"description":"Required for return to service where the asset demands it."},"raiseWorkOrder":{"type":"boolean","default":false},"recordedAt":{"type":"string","format":"date-time"}}},
"StockReservationSourceType": {"type":"string","enum":["workOrder","rentalAgreement","order","transfer","other"],"description":"What a stock reservation is for (decided 17 September, M17-02; `rentalAgreement` is the existing use from `rental.agreement_item`)."},
"SubmitInspectionRequest": {"x-ticvai-persistence":"maintenance.inspection + maintenance.inspection_item","type":"object","required":["id","templateId","venueId","responses","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"templateId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"responses":{"type":"array","minItems":1,"items":{"type":"object","required":["key","value"],"properties":{"key":{"type":"string"},"value":{},"passed":{"type":"boolean","nullable":true},"note":{"type":"string","maxLength":1000},"attachmentRefs":{"type":"array","items":{"type":"string"}}}}},"signatureRef":{"type":"string","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"VendorServiceRequest": {"x-ticvai-persistence":"maintenance.vendor_service_request","type":"object","description":"**An outside vendor engaged on a work order** (decided 17 September, M17-13). The supplier is an `inventory.supplier`.\n","required":["workOrderId","supplierId","scope"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","readOnly":true},"workOrderId":{"type":"string","format":"uuid"},"supplierId":{"type":"string","format":"uuid"},"scope":{"type":"string","maxLength":2000,"description":"What the vendor is asked to do."},"status":{"allOf":[{"$ref":"#/components/schemas/VendorServiceRequestStatus"}],"default":"draft"},"vendorReference":{"type":"string","maxLength":100,"nullable":true},"quotedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"finalCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scheduledVisitAt":{"type":"string","format":"date-time","nullable":true},"note":{"type":"string","maxLength":1000,"nullable":true},"raisedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"VendorServiceRequestStatus": {"type":"string","enum":["draft","sent","accepted","scheduled","completed","cancelled"]},
"WorkOrder": {"x-ticvai-persistence":"maintenance.work_order","x-ticvai-retired-columns":["is_overdue"],"type":"object","required":["id","workOrderNumber","title","venueId","status","priority","kind","createdAt"],"properties":{"downtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"},"rootCause":{"type":"string","nullable":true,"enum":["wearAndTear","operatorError","guestDamage","manufacturingDefect","environmental","softwareFault","powerFailure","deferredMaintenance","unknown"],"description":"**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"},"rootCauseNote":{"type":"string","nullable":true},"escalatedAt":{"type":"string","format":"date-time","nullable":true},"escalationLevel":{"type":"integer","default":0,"description":"**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"},"id":{"type":"string","format":"uuid"},"workOrderNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"title":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"assetName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"},"status":{"$ref":"#/components/schemas/WorkOrderStatus"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"priorityScore":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"readOnly":true,"description":"The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."},"prioritySource":{"type":"string","enum":["scored","assetOverride","manual"],"readOnly":true,"description":"Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","items":{"type":"string"},"description":"Skills the job needs (M17-13)."},"kind":{"$ref":"#/components/schemas/WorkOrderKind"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"raisedByPrincipalId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"},"locationDescription":{"type":"string","maxLength":500,"nullable":true,"description":"Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"},"elapsedMinutes":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"},"isTimerRunning":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"},"dueAt":{"type":"string","format":"date-time","nullable":true},"isOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"},"requiresVerification":{"type":"boolean"},"sourcePlanId":{"type":"string","format":"uuid","nullable":true},"sourceInspectionId":{"type":"string","format":"uuid","nullable":true},"sourceIncidentId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrderAssigneeSuggestion": {"x-ticvai-persistence":"none — computed on read","type":"object","required":["principalId","rank"],"properties":{"principalId":{"type":"string","format":"uuid"},"name":{"type":"string"},"rank":{"type":"integer","minimum":1},"hasAllQualifications":{"type":"boolean"},"missingQualificationCodes":{"type":"array","items":{"type":"string"}},"onShift":{"type":"boolean","description":"On shift now or before the work order is due."},"openWorkOrderCount":{"type":"integer"}}},
"WorkOrderAttachment": {"type":"object","x-ticvai-persistence":"maintenance.work_order_attachment","required":["id","workOrderId","kind","capturedAt"],"properties":{"id":{"type":"string","format":"uuid"},"workOrderId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["photo","video","document","note","signature"]},"assetRef":{"type":"string","format":"uuid","nullable":true},"text":{"type":"string","nullable":true},"stage":{"type":"string","enum":["before","during","after","signOff"],"nullable":true},"capturedByPrincipalId":{"type":"string","format":"uuid"},"capturedAt":{"type":"string","format":"date-time","description":"Device time. **Distinct from when it synced** — a photo taken at 09:14 in a basement and uploaded at 11:40 is evidence of the first, not the second.\n"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrderDetail": {"x-ticvai-persistence":"maintenance.work_order","allOf":[{"$ref":"#/components/schemas/WorkOrder"},{"type":"object","properties":{"description":{"type":"string","nullable":true},"resolution":{"type":"string","nullable":true},"resolutionCode":{"$ref":"#/components/schemas/ResolutionCode"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"timeEntries":{"type":"array","items":{"type":"object","properties":{"action":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"pauseReason":{"type":"string","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}}},"parts":{"type":"array","items":{"type":"object","properties":{"inventoryItemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"quantity":{"type":"number"},"reservedQuantity":{"type":"number","description":"Still reserved for this work order and not yet issued (M17-02)."},"cost":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"labourCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"partsCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","x-ticvai-column":"net_cost_amount"},"completedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who called `completeWorkOrder`. **What `verifyWorkOrder` compares against** — the verifier may not be the technician who completed the work, and the assignee is not necessarily that person.\n"},"followUpRequired":{"type":"boolean","default":false},"followUpNote":{"type":"string","maxLength":1000,"nullable":true},"verificationOutcome":{"type":"string","enum":["verified","rejected"],"nullable":true,"description":"The latest `verifyWorkOrder` outcome."},"verificationNote":{"type":"string","maxLength":1000,"nullable":true},"verifiedAt":{"type":"string","format":"date-time","nullable":true},"verifiedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"cancelReason":{"type":"string","enum":["raisedInError","duplicate","superseded","noLongerRequired"],"nullable":true},"cancelNote":{"type":"string","maxLength":300,"nullable":true},"supersededByWorkOrderId":{"type":"string","format":"uuid","nullable":true,"description":"Set by `cancelWorkOrder` where the reason is `superseded`."},"cancelledAt":{"type":"string","format":"date-time","nullable":true},"closeOutcome":{"type":"string","enum":["completedAndVerified","notReproducible","supersededByReplacement","noLongerApplicable","duplicate"],"nullable":true},"closeNote":{"type":"string","maxLength":500,"nullable":true},"duplicateOfWorkOrderId":{"type":"string","format":"uuid","nullable":true,"description":"Set by `closeWorkOrder` where the outcome is `duplicate`."},"closedAt":{"type":"string","format":"date-time","nullable":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true}}}]},
"WorkOrderFaultAssessment": {"x-ticvai-persistence":"none — columns on maintenance.work_order","type":"object","description":"What the person raising a fault says about it, which the priority score reads (M17-01).","properties":{"safetyRisk":{"type":"boolean","default":false},"guestImpact":{"type":"string","enum":["none","degraded","closed"],"default":"none"}}},
"WorkOrderKind": {"type":"string","enum":["corrective","planned","inspectionFollowUp","incidentCorrective","improvement"]},
"WorkOrderPriority": {"type":"string","enum":["low","normal","high","urgent","emergency"]},
"WorkOrderPriorityPolicy": {"x-ticvai-persistence":"maintenance.priority_scoring_model","type":"object","description":"**How a corrective fault's priority is scored** (decided 17 September, M17-01). One per venue. The score is 0 to 100: each weight times its factor, where safety is the fault's `faultAssessment.safetyRisk`, guest operations is `faultAssessment.guestImpact` (and whether the asset has a linked access point), revenue is whether the asset has linked products, and criticality is the asset's `criticality`. The band the score falls in is the priority. **An asset's `priorityOverride` wins over the score**, and a priority a person sets wins over both.\n","required":["weights","bands"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","readOnly":true},"weights":{"type":"object","required":["safety","guestOperations","revenue","criticality"],"properties":{"safety":{"type":"integer","minimum":0,"maximum":100},"guestOperations":{"type":"integer","minimum":0,"maximum":100},"revenue":{"type":"integer","minimum":0,"maximum":100},"criticality":{"type":"integer","minimum":0,"maximum":100}}},"bands":{"type":"array","minItems":1,"maxItems":5,"description":"Highest first. A score at or above `minScore` takes `priority`.","items":{"type":"object","required":["minScore","priority"],"properties":{"minScore":{"type":"integer","minimum":0,"maximum":100},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"}}}},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"updatedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"nullable":true}}},
"WorkOrderStatus": {"type":"string","enum":["open","assigned","inProgress","paused","awaitingParts","completed","verified","closed","cancelled"]}
}
```
