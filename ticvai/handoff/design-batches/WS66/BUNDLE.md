# WS66 — Unified BI Reporting and AI Analytics Platform board 1

**9 screens · 11 operations · 25 schemas · 4 permissions**

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
  `AI_USE, PRICE_VIEW, REPORT_VIEW_TENANT, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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
| `ANL-012` | Live Operations Dashboard | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ANL-013` | Revenue Pulse | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-014` | Attendance & Footfall Intelligence | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ANL-015` | Capacity & Utilization Monitor | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `ANL-016` | Sales & Channel Performance | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `ANL-017` | Customer, Membership & Loyalty Pulse | B–D | 2 | 30 | 6 | 0 | 2 | 2 | — | notStarted (—) |
| `ANL-018` | Alerts & Exception Center | B–D | 0 | 22 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-019` | AI Management Insights | A | 0 | 0 | 6 | 3 | 2 | 0 | — | notStarted (—) |
| `ANL-020` | Multi-Site & Performance Comparison | B–D | 3 | 8 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ANL-018, ANL-019 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ANL-012` Live Operations Dashboard

**Provide a real-time view of what is happening across all operating locations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/live-operations-dashboard-anl-012` |

#### Inputs: what the user enters or picks

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
| Status | radio group | — | Raised · Acknowledged · Resolved · Expired | `listAlerts` ?status |
| Severity | segmented control | — | Info · Warning · Critical | `listAlerts` ?severity |
| Workstation | picker: choose a workstation | — | — | `listAlerts` ?workstationId |
| Shift | picker: choose a shift | — | — | `listAlerts` ?shiftId |
| Item | picker: choose an item | — | — | `listAlerts` ?itemId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Visitors currently on-site** (metric tile)

**Entries today** (metric tile)

**Exits today** (metric tile)

**Current occupancy** (metric tile)

**Capacity remaining** (metric tile)

**Occupancy %** (metric tile)

**Active gates** (metric tile)

**Gate status** (metric tile)

**Active POS terminals** (metric tile)

**Active sessions/timeslots** (metric tile)

**Current queues** (metric tile)

**Resource utilization** (metric tile)

**Operational incidents** (metric tile)

**System/device exceptions** (metric tile)

**Data it reads**: `getKpiValues` (onLoad, Live operational KPIs); `listAlerts` (onLoad, What needs attention)

**Where the user goes next**

- → `ANL-020` Multi-Site & Performance Comparison: *Back to Multi-Site & Performance Comparison*
- → `ANL-001` Executive Command Center: *Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The live operations list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the live operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No live operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the live operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `listAlerts` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Live operations view shows sales, entries and exits per tenant/venue for multi-tenant setups, with a quick-glance access-control gate status (open / closed / offline gates). *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-699)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-012` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-012`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 2: Works in Live Operations Dashboard → Provide a real-time view of what is happening across all operating locations.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-012?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-020`, `ANL-001`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-013` Revenue Pulse

**Provide real-time visibility into revenue generation across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/revenue-pulse-anl-013` |

#### Inputs: what the user enters or picks

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

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Revenue Today** (metric tile)

**Revenue This Hour** (metric tile)

**Revenue vs Target** (metric tile)

**Revenue vs Yesterday** (metric tile)

**Revenue vs Same Day Last Week** (metric tile)

**Revenue vs Same Period Last Year** (metric tile)

**Revenue by Site** (metric tile)

**Revenue by Attraction** (metric tile)

**Revenue by Product** (metric tile)

**Revenue by Channel** (metric tile)

**Revenue by Business Unit** (metric tile)

**Revenue by Payment Method** (metric tile)

**Data it reads**: `getKpiValues` (onLoad, Revenue against target)

**Where the user goes next**

- → `ANL-020` Multi-Site & Performance Comparison: *Back to Multi-Site & Performance Comparison*
- → `ANL-001` Executive Command Center: *Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The revenue pulse list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the revenue pulse untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No revenue pulse yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the revenue pulse are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-013` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-013`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 4: Works in Revenue Pulse → Provide real-time visibility into revenue generation across TICVAI.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-013?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-020`, `ANL-001`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-014` Attendance & Footfall Intelligence

**Monitor visitor movement and attendance across venues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Display) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/attendance-footfall-intelligence-anl-014` |

#### Inputs: what the user enters or picks

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

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Total Visitors** (metric tile)

**Current Visitors On-Site** (metric tile)

**Entry Count** (metric tile)

**Exit Count** (metric tile)

**Hourly Footfall** (metric tile)

**Peak Entry Time** (metric tile)

**Average Visit Duration** (metric tile)

**Attendance by Site** (metric tile)

**Attendance by Attraction** (metric tile)

**Attendance by Ticket Type** (metric tile)

**Attendance by Product** (metric tile)

**Attendance by Timeslot** (metric tile)

**Repeat Visits** (metric tile)

**No-Show %** (metric tile)

**Ticketed vs Actual Attendance** (metric tile)

**Data it reads**: `getKpiValues` (onLoad, Attendance and footfall)

**Where the user goes next**

- → `ANL-020` Multi-Site & Performance Comparison: *Back to Multi-Site & Performance Comparison*
- → `ANL-001` Executive Command Center: *Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attendance footfall intelligence list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attendance footfall intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attendance footfall intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the attendance footfall intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Operations board: access-control metrics - total entries, attendance, exits, per-turnstile breakdowns, and park capacity utilisation. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-717)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-014` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-014`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 6: Works in Attendance & Footfall Intelligence → Monitor visitor movement and attendance across venues.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-014?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-020`, `ANL-001`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-015` Capacity & Utilization Monitor

**Provide centralized monitoring of available and consumed capacity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/capacity-utilization-monitor-anl-015` |

#### Inputs: what the user enters or picks

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

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Available Capacity** (metric tile)

**Booked Capacity** (metric tile)

**Used Capacity** (metric tile)

**Remaining Capacity** (metric tile)

**Utilization %** (metric tile)

**No-Show %** (metric tile)

**Peak Utilization** (metric tile)

**Forecast Utilization** (metric tile)

**Data it reads**: `getKpiValues` (onLoad, Capacity and utilisation)

**Where the user goes next**

- → `ANL-020` Multi-Site & Performance Comparison: *Back to Multi-Site & Performance Comparison*
- → `ANL-001` Executive Command Center: *Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The capacity utilization list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the capacity utilization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No capacity utilization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the capacity utilization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Operations board: access-control metrics - total entries, attendance, exits, per-turnstile breakdowns, and park capacity utilisation. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-717)*
- Further command-centre sections: revenue by sales channel; capacity utilisation by attraction/inventory item; top products by channel; conversion rate (site visits to completed purchase, cart abandonment, via Google Analytics); customer, membership and loyalty information. *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-700)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-015` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-015`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 8: Works in Capacity & Utilization Monitor → Provide centralized monitoring of available and consumed capacity.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-015?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-020`, `ANL-001`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-016` Sales & Channel Performance

**Provide management with consolidated commercial performance across every sales channel.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/sales-channel-performance-anl-016` |

#### Inputs: what the user enters or picks

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

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Gross Sales** (metric tile)

**Net Sales** (metric tile)

**Transactions** (metric tile)

**Tickets Sold** (metric tile)

**Average Order Value** (metric tile)

**Conversion Rate** (metric tile)

**Discount Value** (metric tile)

**Refunds** (metric tile)

**Cancellations** (metric tile)

**Commission** (metric tile)

**Upsell Revenue** (metric tile)

**Cross-Sell Revenue** (metric tile)

**Data it reads**: `getKpiValues` (onLoad, Sales by channel)

**Where the user goes next**

- → `ANL-020` Multi-Site & Performance Comparison: *Back to Multi-Site & Performance Comparison*
- → `ANL-001` Executive Command Center: *Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sales channel performance list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sales channel performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sales channel performance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the sales channel performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Sales board: product/attraction performance by sales channel, discounts, upsell/cross-sell results, deferred vs realised revenue, and sales forecast vs target. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-715)*
- Further command-centre sections: revenue by sales channel; capacity utilisation by attraction/inventory item; top products by channel; conversion rate (site visits to completed purchase, cart abandonment, via Google Analytics); customer, membership and loyalty information. *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-700)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-016` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-016`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 10: Works in Sales & Channel Performance → Provide management with consolidated commercial performance across every sales channel.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-016?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-020`, `ANL-001`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-017` Customer, Membership & Loyalty Pulse

**Provide a consolidated view of customer health and engagement.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `dashboardId` (navigation) |
| Route | `/analytics/customer-membership-loyalty-pulse-anl-017` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search customer membership loyalty | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by customer segment, membership type, geography, demographic group, acquisition source, visit frequency and 1 more — which are present is a decision the pack already made. | — |

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
| Refresh | toggle | off | — | `getDashboard` ?refresh |

#### Outputs: what the screen shows and produces

**Shown**

**Every customer membership loyalty** (data table)

| Shows | Format | Notes |
|---|---|---|
| Unique customers | text | not in the schema: `Unique Customers` |
| New customers | text | not in the schema: `New Customers` |
| Returning customers | text | not in the schema: `Returning Customers` |
| Repeat visit % | text | not in the schema: `Repeat Visit %` |
| Average customer spend | text | not in the schema: `Average Customer Spend` |
| Customer lifetime value | text | not in the schema: `Customer Lifetime Value` |
| Active members | text | not in the schema: `Active Members` |
| New memberships | text | not in the schema: `New Memberships` |
| Membership renewals | text | not in the schema: `Membership Renewals` |
| Membership expiring | text | not in the schema: `Membership Expiring` |
| Loyalty members | text | not in the schema: `Loyalty Members` |
| Loyalty earn | text | not in the schema: `Loyalty Earn` |
| Loyalty burn | text | not in the schema: `Loyalty Burn` |
| Outstanding loyalty liability | text | not in the schema: `Outstanding Loyalty Liability` |
| Customer satisfaction score | text | not in the schema: `Customer Satisfaction Score` |

**The selected customer membership loyalty** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Unique customers | text | not in the schema: `Unique Customers` |
| New customers | text | not in the schema: `New Customers` |
| Returning customers | text | not in the schema: `Returning Customers` |
| Repeat visit % | text | not in the schema: `Repeat Visit %` |
| Average customer spend | text | not in the schema: `Average Customer Spend` |
| Customer lifetime value | text | not in the schema: `Customer Lifetime Value` |
| Active members | text | not in the schema: `Active Members` |
| New memberships | text | not in the schema: `New Memberships` |
| Membership renewals | text | not in the schema: `Membership Renewals` |
| Membership expiring | text | not in the schema: `Membership Expiring` |
| Loyalty members | text | not in the schema: `Loyalty Members` |
| Loyalty earn | text | not in the schema: `Loyalty Earn` |
| Loyalty burn | text | not in the schema: `Loyalty Burn` |
| Outstanding loyalty liability | text | not in the schema: `Outstanding Loyalty Liability` |
| Customer satisfaction score | text | not in the schema: `Customer Satisfaction Score` |

**Data it reads**: `getKpiValues` (onLoad, Membership and loyalty); `getDashboard` (onLoad, Loyalty dashboard (active members, tiers, liability …)

**Where the user goes next**

- → `ANL-020` Multi-Site & Performance Comparison: *Back to Multi-Site & Performance Comparison*
- → `ANL-001` Executive Command Center: *Executive Command Center*; carries `dashboardId`, `reportId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer membership loyalty list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer membership loyalty untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer membership loyalty yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer membership loyalty are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- CRM board: membership/loyalty visit history; retention/churn section flagging inactive customers (e.g. an annual pass holder with no visit last quarter flagged for follow-up); campaign performance and customer behaviour analytics. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-718)*
- Further command-centre sections: revenue by sales channel; capacity utilisation by attraction/inventory item; top products by channel; conversion rate (site visits to completed purchase, cart abandonment, via Google Analytics); customer, membership and loyalty information. *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-700)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A94** Hold the loyalty workshop and define the full programme configuration (tiers, point accrual, redemption, expiry, benefit unlocks) *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'loyalty')*
- **A134** Build the eligibility rules engine (residency/nationality with ID capture, minimum age by DOB, VIP-only profiles, loyalty-points thresholds, purchase limits per order/guest/category/channel) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'loyalty')*

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-017` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-017`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 12: Works in Customer, Membership & Loyalty Pulse → Provide a consolidated view of customer health and engagement.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400, 404).
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-017?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-020`, `ANL-001`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-018` Alerts & Exception Center

**Create one centralized location for management-level KPI and operational exceptions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each Alert Shall Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/alerts-exception-center-anl-018` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every alerts exception** (data table)

| Shows | Format | Notes |
|---|---|---|
| Severity | text | not in the schema: `Severity` |
| KPI | text | not in the schema: `KPI` |
| Current value | text | not in the schema: `Current value` |
| Expected/target value | text | not in the schema: `Expected/target value` |
| Variance | text | not in the schema: `Variance` |
| Site | text | not in the schema: `Site` |
| Detection time | text | not in the schema: `Detection time` |
| Source system | text | not in the schema: `Source system` |
| Owner | text | not in the schema: `Owner` |
| Status | text | not in the schema: `Status` |
| Recommended action | text | not in the schema: `Recommended action` |

**The selected alerts exception** (detail panel): The pack groups this record's detail under its own headings: “Alert Categories”, “Alert Workflow”.

| Shows | Format | Notes |
|---|---|---|
| Severity | text | not in the schema: `Severity` |
| KPI | text | not in the schema: `KPI` |
| Current value | text | not in the schema: `Current value` |
| Expected/target value | text | not in the schema: `Expected/target value` |
| Variance | text | not in the schema: `Variance` |
| Site | text | not in the schema: `Site` |
| Detection time | text | not in the schema: `Detection time` |
| Source system | text | not in the schema: `Source system` |
| Owner | text | not in the schema: `Owner` |
| Status | text | not in the schema: `Status` |
| Recommended action | text | not in the schema: `Recommended action` |

**Data it reads**: `listPromotionAlertException` (onLoad, Promotion Alerts & Exception Center)

**Where the user goes next**

- → `ANL-020` Multi-Site & Performance Comparison: *Back to Multi-Site & Performance Comparison*
- → `ANL-001` Executive Command Center: *Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The alerts exception list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the alerts exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No alerts exception yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the alerts exception are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPromotionAlertException` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-018` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-018`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 14: Works in Alerts & Exception Center → Create one centralized location for management-level KPI and operational exceptions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-020`, `ANL-001`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-019` AI Management Insights

**Provide management with proactive AI-generated business intelligence rather than requiring users to manually analyze every dashboard.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block A · ticket #20757 (APP-SETUP-ANL-019) |
| Who uses it | venue staff holding `AI_USE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `insightId` (navigation) |
| Route | `/analytics/ai-management-insights-anl-019` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listAnalyticsAnomalies` (onLoad, What moved unexpectedly); `listAiInsights` (onLoad, Insights and anomalies)

**Where the user goes next**

- → `ANL-020` Multi-Site & Performance Comparison: *Back to Multi-Site & Performance Comparison*
- → `ANL-001` Executive Command Center: *Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The insights list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the insights untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No insights yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the insights are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Question could not be interpreted. (ReportQuestionProblem); 409 The move is not allowed from the insight's state. |

#### Permissions

- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `listAnalyticsAnomalies` → `REPORT_VIEW_VENUE` (operate) · staff
- `listAiInsights` → `AI_USE` (operate) · staff
- `decideAiInsight` → `AI_USE` (operate) · staff
- `explainMetricChange` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.7.30 | System shall support natural language reporting. | Unified Operations Dashboard | CONTRACTED | `askReportingQuestion` |
| 8.4.17 | System shall support AI-powered anomaly explanations. | Unified Operations Dashboard | CONTRACTED | `listAiInsights` |
| 8.4.18 | System shall support AI-powered root cause analysis. | Unified Operations Dashboard | CONTRACTED | `explainMetricChange` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- An AI layer across all dashboards explains why a metric changed (e.g. why revenue dropped on a given day) and recommends management actions from sales, revenue and attendance trends. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-719)*
- Multi-site performance comparison (this month vs last month, or vs the same period last year), and AI management insights that surface possible reasons behind a change (e.g. a drop in attendance or revenue). *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-701)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-019` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-019`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 16: Works in AI Management Insights → Provide management with proactive AI-generated business intelligence rather than requiring users to manually analyze every dashboard.
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)
- ADR-0059 *AI phasing against the six-month plan* (`docs/adr/0059-ai-phasing-against-the-six-month-plan.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ANL-020`, `ANL-001`.
- [ ] Every gated control is gated: `AI_USE`, `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-020` Multi-Site & Performance Comparison

**Allow enterprise management to compare sites, venues, attractions and business units.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Comparison KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/multi-site-performance-comparison-anl-020` |

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

#### Outputs: what the screen shows and produces

**Shown**

**Revenue** (metric tile)

**Revenue Growth** (metric tile)

**Attendance** (metric tile)

**Capacity Utilization** (metric tile)

**Revenue per Visitor** (metric tile)

**Average Transaction Value** (metric tile)

**Conversion** (metric tile)

**Refund %** (metric tile)

**Membership Conversion** (metric tile)

**Repeat Visitor %** (metric tile)

**Customer Satisfaction** (metric tile)

**F&B Spend** (metric tile)

**Retail Spend** (metric tile)

**Operational Exceptions** (metric tile)

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

**Data it reads**: `getAnalyticsBenchmark` (onLoad, Site against site, normalised); `listSiteNormalisationBases` (onLoad, The denominators each site is benchmarked by)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Back to Executive Command Center*
- → `ANL-012` Live Operations Dashboard: *Live Operations Dashboard*
- → `ANL-013` Revenue Pulse: *Revenue Pulse*
- → `ANL-014` Attendance & Footfall Intelligence: *Attendance & Footfall Intelligence*
- → `ANL-015` Capacity & Utilization Monitor: *Capacity & Utilization Monitor*
- → `ANL-016` Sales & Channel Performance: *Sales & Channel Performance*
- → `ANL-017` Customer, Membership & Loyalty Pulse: *Customer, Membership & Loyalty Pulse*
- → `ANL-018` Alerts & Exception Center: *Alerts & Exception Center*
- → `ANL-019` AI Management Insights: *AI Management Insights*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-site performance comparison list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-site performance comparison untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-site performance comparison yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the multi-site performance comparison are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getAnalyticsBenchmark` → `REPORT_VIEW_TENANT` (operate) · staff
- `listSiteNormalisationBases` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Multi-site performance comparison (this month vs last month, or vs the same period last year), and AI management insights that surface possible reasons behind a change (e.g. a drop in attendance or revenue). *(client request · MoM 8 Sep 2026, 4.2 Command Center Overview (Board 1) · DI-701)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-020` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS172 Unified BI Reporting and AI Analytics Platform Board 1.dc.html#anl-020`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 1
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 1: Opens Multi-Site & Performance Comparison → Allow enterprise management to compare sites, venues, attractions and business units.
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F175 *Unified BI Reporting and AI Analytics Platform board 1: Multi-Site & …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F175 branch at step 1 (expected): when Nothing has been set up on Multi-Site & Performance Comparison yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F175 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-020?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-001`, `ANL-012`, `ANL-013`, `ANL-014`, `ANL-015`, `ANL-016`, `ANL-017`, `ANL-018`, `ANL-019`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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
"askReportingQuestion": {"method":"POST","path":"/reports/ask","contract":"reporting","summary":"Natural-language reporting query","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"NaturalLanguageAnswer"},
"decideAiInsight": {"method":"POST","path":"/insights/{insightId}/decide","contract":"ai","summary":"Review, accept, reject or mark an insight actioned","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiInsight"},
"explainMetricChange": {"method":"POST","path":"/insights/explain-metric-change","contract":"ai","summary":"Why did this metric change","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiMetricChangeExplanation"},
"getAnalyticsBenchmark": {"method":"GET","path":"/analytics-benchmarks","contract":"reporting","summary":"One site against another, on a like-for-like basis","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"kpiId","in":"query","required":true},{"name":"scopePaths","in":"query","required":null},{"name":"normaliseBy","in":"query","required":null}],"requestBody":null,"responds":"BenchmarkRow"},
"getDashboard": {"method":"GET","path":"/dashboards/{dashboardId}","contract":"reporting","summary":"Read a dashboard with tile data","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"refresh","in":"query","required":null}],"requestBody":null,"responds":"DashboardData"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"listAiInsights": {"method":"GET","path":"/insights","contract":"ai","summary":"Insights and anomalies","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAlerts": {"method":"GET","path":"/alerts","contract":"reporting","summary":"What is currently wrong","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"severity","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"itemId","in":"query","required":null}],"requestBody":null,"responds":"Alert"},
"listAnalyticsAnomalies": {"method":"GET","path":"/analytics-anomalies","contract":"reporting","summary":"Numbers that moved more than they should have","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"severity","in":"query","required":null}],"requestBody":null,"responds":"AnalyticsAnomaly"},
"listPromotionAlertException": {"method":"GET","path":"/promotion-alert-exception","contract":"promotions","summary":"Promotion Alerts & Exception Center","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PromotionAlertsExceptionCenterView"},
"listSiteNormalisationBases": {"method":"GET","path":"/site-normalisation-bases","contract":"reporting","summary":"The denominators each site is benchmarked by","permission":"REPORT_VIEW_TENANT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"scopePath","in":"query","required":null},{"name":"periodFrom","in":"query","required":null},{"name":"periodTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiEvidenceItem": {"type":"object","x-ticvai-persistence":"none — held in jsonb on ai.decision_record.evidence, through AiEvidenceItemList","description":"One piece of evidence behind a decision, **labelled by origin** (AIC-197): read from a source system, derived by a rule or feature, or inferred by a model. An explanation is built from these, never from a model's chain of thought (AIC-192).","required":["label","kind"],"properties":{"label":{"type":"string","enum":["source","derived","modelInferred"]},"kind":{"type":"string","description":"What it is: `feature`, `rule`, `document`, `metric`, `transaction`, `candidateSet`."},"ref":{"type":"string","nullable":true,"description":"Where it came from: a table and id, a document chunk, a metric key."},"name":{"type":"string"},"value":{"type":"object","additionalProperties":true,"nullable":true},"observedAt":{"type":"string","format":"date-time","nullable":true}}},
"AiEvidenceItemList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The evidence of one decision record, stored with it.","items":{"$ref":"#/components/schemas/AiEvidenceItem"}},
"AiInsight": {"type":"object","x-ticvai-persistence":"ai.insight","description":"**An insight with a lifecycle** (AIP-181): new, reviewed, accepted or rejected, actioned, measured. Anomalies, forecast deviations, trends and opportunities land here; the narrative binds numbers to results, so a figure can only come from a query (design 8, 5.10).","required":["kind","title","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["anomaly","forecastDeviation","trend","opportunity","executiveSummary","rootCause","forecastThreshold","marketingRecommendation"]},"detectorId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.anomaly_detector"},"metricKey":{"type":"string","nullable":true},"subjectKind":{"type":"string","nullable":true,"enum":["campaign","journey","forecastDefinition","venue"],"description":"What the insight is about where it is not a KPI (29 September, build): a marketing-crm campaign or journey for `marketingRecommendation`, a forecast definition for `forecastThreshold`."},"subjectRef":{"type":"string","nullable":true},"recommendedAction":{"type":"object","additionalProperties":true,"nullable":true,"description":"For `marketingRecommendation`: `{recommendation, parameters}` as `AiMarketingRecommendation`. Applied by a person in the owning module, never here."},"expectedImpact":{"type":"object","additionalProperties":true,"nullable":true,"description":"A range on a named metric (`metric`, `low`, `high`), never a single number (design 5.6)."},"title":{"type":"string"},"narrative":{"type":"string","nullable":true},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"magnitude":{"type":"number","nullable":true},"priority":{"type":"string","enum":["low","medium","high","critical"]},"correlationKey":{"type":"string","nullable":true},"status":{"type":"string","enum":["new","reviewed","accepted","rejected","actioned","measured"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"actionRef":{"type":"string","nullable":true},"measuredImpact":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"detectedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiMetricChangeExplanation": {"type":"object","x-ticvai-persistence":"none — computed; written as an ai.insight of kind rootCause when kept","description":"**Why a metric changed** (AIP-176..180, ANL-056): drivers with their contribution, computed from the semantic layer. The narrative binds every figure to a result placeholder (design 8, 5.10).","required":["metricKey","change","drivers"],"properties":{"metricKey":{"type":"string"},"period":{"type":"string"},"comparison":{"type":"string"},"change":{"type":"number"},"changePercent":{"type":"number","nullable":true},"drivers":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string"},"member":{"type":"string"},"contribution":{"type":"number"},"evidence":{"$ref":"#/components/schemas/AiEvidenceItem"}}}},"narrative":{"type":"string","nullable":true},"reliability":{"type":"string","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},"dataAsOf":{"type":"string","format":"date-time"}}},
"Alert": {"type":"object","x-ticvai-persistence":"reporting.alert","description":"A raised alert. **Acknowledged rather than dismissed** — CF-134 asked for it markable, and the difference is that an acknowledgement records who saw it.\n","required":["id","ruleId","raisedAt","severity","status"],"properties":{"id":{"type":"string","format":"uuid"},"ruleId":{"type":"string","format":"uuid"},"ruleName":{"type":"string","description":"`AlertRule.name` as it stood when the alert was raised. **The line a person reads** — a list of rule ids is not an alert panel, and a screen should not need `listAlertRules` to label one.\n"},"metric":{"allOf":[{"$ref":"#/components/schemas/MetricSource"}],"description":"The rule's metric, carried so the alert says what went out of range."},"raisedAt":{"type":"string","format":"date-time"},"severity":{"$ref":"#/components/schemas/AlertSeverity"},"status":{"$ref":"#/components/schemas/AlertStatus"},"observedValue":{"$ref":"#/components/schemas/MetricValue"},"threshold":{"$ref":"#/components/schemas/MetricValue"},"scopePath":{"type":"string"},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation the reading was taken for, where the metric is measured per workstation (`salesByWorkstation`). Null otherwise. `listAlerts` filters on it."},"shiftId":{"type":"string","format":"uuid","nullable":true,"description":"The till shift (`orders.pos_shift`) the reading belongs to, where it was taken for a workstation with a shift open. Null otherwise. `listAlerts` filters on it."},"itemId":{"type":"string","format":"uuid","nullable":true,"description":"The inventory item the reading is about, where the metric is measured per item (`stockAgeing`, `stockTurnover`, `wastageRate`, `inventoryValuation`). Null otherwise. **What a replenishment screen prefills a requisition from.**\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true},"acknowledgementNote":{"type":"string","maxLength":300,"nullable":true,"description":"The `note` given to `acknowledgeAlert`. Kept, because an acknowledgement that says what is being done about it is the one escalation can skip."},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"description":"**Set when the metric returns to range, automatically.** An alert that only a person can close is an alert list that only grows.\n"},"escalatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. **A critical alert nobody acknowledged is the case escalation exists for.**\n"}}},
"AlertSeverity": {"type":"string","description":"How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter.","enum":["info","warning","critical"]},
"AlertStatus": {"type":"string","description":"Where a raised alert is. Shared by `Alert` and the `listAlerts` filter.","enum":["raised","acknowledged","resolved","expired"]},
"AnalyticsAnomaly": {"type":"object","x-ticvai-persistence":"reporting.anomaly","description":"BI boards 9.5 and 9.6. **A departure from the series' own behaviour**, which catches what no threshold was set for.\n","properties":{"id":{"type":"string","format":"uuid"},"kpiId":{"type":"string","format":"uuid","nullable":true},"metric":{"type":"string"},"scopePath":{"type":"string"},"detectedAt":{"type":"string","format":"date-time"},"observed":{"$ref":"#/components/schemas/MetricValue"},"expected":{"$ref":"#/components/schemas/MetricValue"},"deviationSigma":{"type":"number","nullable":true},"severity":{"$ref":"#/components/schemas/AnomalySeverity"},"candidateCauses":{"type":"array","description":"**The beginning of the question, not the end of it.**","items":{"type":"object","properties":{"dimension":{"type":"string"},"value":{"type":"string"},"contribution":{"type":"number"}}}},"acknowledgedBy":{"type":"string","format":"uuid","nullable":true},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true}}},
"AnomalySeverity": {"type":"string","description":"Shared by `AnalyticsAnomaly` and the `listAnalyticsAnomalies` filter.","enum":["low","medium","high"]},
"BenchmarkNormalisation": {"type":"string","description":"The basis a benchmark is compared on. Shared by `getAnalyticsBenchmark` and `BenchmarkRow`.","enum":["none","perVisitor","perOperatingHour","perStaffedPosition","perSquareMetre"]},
"BenchmarkRow": {"type":"object","description":"BI board 10.4. **The normalisation travels with the comparison.**","properties":{"scopePath":{"type":"string"},"label":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"normalisedValue":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"normaliseBy":{"$ref":"#/components/schemas/BenchmarkNormalisation"},"rank":{"type":"integer"},"percentile":{"type":"number","nullable":true}}},
"Dashboard": {"x-ticvai-persistence":"reporting.dashboard + reporting.dashboard_tile","allOf":[{"$ref":"#/components/schemas/CreateDashboardRequest"},{"type":"object","required":["id","ownerPrincipalId","aggregateCost","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid"},"aggregateCost":{"type":"string","enum":["low","medium","high"],"description":"Combined refresh load of every tile."},"archivedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"},"createdAt":{"type":"string","format":"date-time"}}}]},
"DashboardData": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/Dashboard"},{"type":"object","properties":{"tileData":{"type":"array","items":{"type":"object","properties":{"tileId":{"type":"string","format":"uuid"},"result":{"$ref":"#/components/schemas/ReportResult"},"isCached":{"type":"boolean"},"error":{"type":"string","nullable":true}}}}}}]},
"GeneratedQuery": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n","properties":{"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"compiledSql":{"type":"string","nullable":true,"description":"The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"}}},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"MetricSource": {"type":"string","description":"**A named metric with a verified source.** BL-053, 75 requirement rows.\n`reporting` is a generic builder, and **a generic builder makes every reporting requirement look covered** — it will happily assemble a report over data nobody produces. That is the shape to watch across the whole walk, and this enum is the answer to it: each value below was checked against the schema before being named.\n| Metric | Source | |---|---| | `occupancy` | `catalogue.channel_capacity.sold` and `leased` against `capacity` | | `capacityUtilisation` | `catalogue.channel_capacity.remaining` over the same window | | `admissionRate` | `access.scan_event.outcome`, in-direction | | `noShowRate` | Entitlements issued against scans that never arrived | | `conversion` | `orders.cart` against `orders.sales_order` | | `salesByOperator` | `orders.sales_order.principal_id` | | `salesByWorkstation` | The workstation on the shift that took it | | `waitTime` | `queue.waiting_guest.estimated_call_at` against `called_at` | | `throughput` | `queue.waiting_guest` completions per hour | | `abandonmentRate` | Queue entries that left before being called |\n**`salesByInstructor` was deliberately absent from the first cut** because it needed the staff-assignment link CL-01 covers. It was added on 18 August once `resources.Resource` produced it — see `x-ticvai-extension-note` below. Naming a metric with no source is still the defect this enum exists to prevent.\n**Money-valued metrics are listed in `x-ticvai-money-valued`.** A reading or threshold on one of them is a `Money`, never a float (`MetricValue`).\n","enum":["occupancy","capacityUtilisation","admissionRate","noShowRate","conversion","salesByOperator","salesByWorkstation","waitTime","throughput","abandonmentRate","inventoryValuation","stockTurnover","stockAgeing","wastageRate","resaleVolume","resaleCommission","salesByInstructor","resourceUtilisation","allocationUtilisation","channelAllocationBurn","membershipChurn","membershipRenewalRate","supplierDeliveryPerformance","revenuePerEntitlement","revenuePerVisitor","assetDowntime","meanTimeToRepair","challengeCompletionRate","attributedRevenue","loyaltyActiveMembers","loyaltyTierDistribution","loyaltyPointsLiability","loyaltyBreakageRate","loyaltyMemberRetention","challengeParticipationRate","gamificationLoyaltyImpact","gamificationMembershipImpact","gamificationRetention","accreditationApplications","accreditationTimeToDecision","accreditationCredentialsIssued","accreditationActiveHolders","accreditationRenewalsDue","staffingShortfall"],"x-ticvai-money-valued":["inventoryValuation","resaleCommission","revenuePerEntitlement","revenuePerVisitor","attributedRevenue","loyaltyPointsLiability"],"x-ticvai-extended-29-september":"**Fourteen metrics added 29 September (build pass)**, each checked against the schema of the contract that produces it.\n\n| Metric | Source | Requirement | |---|---|---| | `loyaltyActiveMembers` | `marketing.loyalty_position` members with a `marketing.loyalty_points` movement in the period | 5.4.27 | | `loyaltyTierDistribution` | `marketing.loyalty_position.tier_id` against `marketing.programme_tier`, members per tier | 5.4.27 | | `loyaltyPointsLiability` | the balance of `ledger.journal_line` on each programme's `pointsLiabilityAccountId`, where points post on accrual and release on redemption or expiry | 5.4.27 | | `loyaltyBreakageRate` | `marketing.loyalty_points` expiry movements over points earned, in the period | 5.4.27 | | `loyaltyMemberRetention` | members with a movement in the previous period who also have one in this period | 5.4.27 | | `challengeParticipationRate` | distinct `marketing.challenge_progress.subject_id` over active loyalty members | 22.6.20 | | `gamificationLoyaltyImpact` | points earned per member, challenge participants against non-participants (`marketing.loyalty_points` split by `marketing.challenge_progress`) | 22.6.20 | | `gamificationMembershipImpact` | joins and renewals in `identity.customer_membership`, participants against non-participants | 22.6.20 | | `gamificationRetention` | return visits (`access.scan_event`, in-direction) of participants against non-participants | 22.6.20 | | `accreditationApplications` | `accreditation.application` by `status` | 12.1.50 | | `accreditationTimeToDecision` | `accreditation.application.decided_at` minus `submitted_at` | 12.1.50 | | `accreditationCredentialsIssued` | `accreditation.credential.issued_at` | 12.1.50 | | `accreditationActiveHolders` | `accreditation.holder` `active`, by `category_code` | 12.1.50 | | `accreditationRenewalsDue` | `accreditation.holder.valid_to` inside `accreditation.validity.renewal_window_days` | 12.1.50 |\n\n**`staffingShortfall` added the same evening (build pass, group G2; 8.2.49)**: the largest gap in the window between the staff rostered and the staff the forecast requires, per venue and position, from `workforce.forecast_requirement` (the handed-over AI staff requirement) against `workforce.rota_assignment` and `workforce.open_shift`, computed as `workforce.getStaffingCoverage` with `basis` `forecastRequirement`. An `AlertRule` on it with `comparator` `above` and `threshold` 0 is the staffing shortage alert; `windowMinutes` looks ahead rather than back for this metric (the rota for the coming window), and `cooldownMinutes` stops one short shift alerting every quarter hour.\n\n**Points issued, points redeemed, campaign performance and reward redemption were already served** by the `loyalty` and `campaigns` sources, and challenge completion and revenue attribution by `challengeCompletionRate` and `attributedRevenue`.\n","x-ticvai-money-valued-note":"**`salesByOperator`, `salesByWorkstation` and `resaleVolume` are not listed because the package does not say whether they count sales or sum their value.** Until that is decided, a rule on them carries a plain number.\n","x-ticvai-extended":"18 August 2026","x-ticvai-extension-note":"**Nineteen metrics added when their upstream models landed**, which is how BL-053 was always going to close — not by changing `reporting` but by building the things it wanted to report on.\n`inventoryValuation`, `stockTurnover`, `stockAgeing` and `wastageRate` came from `inventory.StockBatch`; `resaleVolume` and `resaleCommission` from `orders.ResaleListing`; **`salesByInstructor` from `resources.Resource`, which was the one metric this enum deliberately refused to name in the morning** because nothing produced it. `allocationUtilisation` from `PartnerUser` and `ChannelListing`, `membershipChurn` from `Journey`, `supplierDeliveryPerformance` from `ProductionRun`, `assetDowntime` and `meanTimeToRepair` from `WorkOrder.downtimeMinutes`, `challengeCompletionRate` from `ChallengeProgress`, `attributedRevenue` from `AttributionTouch`.\n**Each was checked against the schema before being named.** That rule has not changed — naming a metric with no source is the defect this enum exists to prevent.\n"},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"NaturalLanguageAnswer": {"x-ticvai-persistence":"none — computed","type":"object","required":["conversationId","question","interpretation","result","reliability"],"properties":{"conversationId":{"type":"string"},"question":{"type":"string"},"interpretation":{"type":"string","description":"What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."},"semanticSpec":{"allOf":[{"$ref":"#/components/schemas/ReportingSemanticQuerySpec"}],"nullable":true,"description":"What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"},"generatedQuery":{"allOf":[{"$ref":"#/components/schemas/GeneratedQuery"}],"nullable":true,"description":"The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"},"result":{"allOf":[{"$ref":"#/components/schemas/ReportResult"}],"nullable":true,"description":"Null when the question is outside the semantic model."},"dataAsOf":{"type":"string","format":"date-time","nullable":true,"description":"Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."},"reliability":{"$ref":"#/components/schemas/ReportingAnswerReliability"},"unavailableReason":{"allOf":[{"$ref":"#/components/schemas/ReportingUnavailableReason"}],"nullable":true,"description":"Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."},"confidence":{"type":"number","minimum":0,"maximum":1,"deprecated":true,"description":"Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."},"suggestedFollowUps":{"type":"array","items":{"type":"string"}},"modelVersion":{"type":"string"},"tokensUsed":{"type":"integer"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PromotionAlertsExceptionCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Promotion Alerts & Exception Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"alertType":{"type":"string","enum":["missingProduct","missingEligibility","invalidDates","invalidDiscount","invalidCode","missingApproval","budgetNearLimit","budgetExceeded","marginBelowThreshold","excessiveDiscountExposure","promotionFailedToPublish","productUnavailable","bundleComponentUnavailable","channelSynchronizationFailure","lowConversion","lowRedemption","unexpectedHighRedemption","campaignUnderperforming","abnormalCouponUsage","excessiveRepeatRedemption","suspiciousCustomerBehavior","promoCodeLeakage"],"description":"What the alert is about."},"severity":{"type":"string","enum":["information","warning","critical"],"description":"Alert severity."},"alertId":{"type":"string","description":"Alert ID"},"promotionId":{"type":"string","description":"Promotion ID"},"alertCategory":{"type":"string","enum":["configuration","financial","operational","commercial","fraudRisk"],"description":"The pack's alert group."},"raisedAt":{"type":"string","format":"date-time","description":"When the alert was raised"}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"ReportingAnswerReliability": {"type":"string","description":"**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},
"ReportingSemanticQuerySpec": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n","required":["metric","period"],"properties":{"metric":{"type":"string","description":"A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."},"dimensions":{"type":"array","maxItems":5,"description":"Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.","items":{"type":"string"}},"filters":{"type":"array","items":{"type":"object","required":["field","operator"],"properties":{"field":{"type":"string","description":"A `SemanticModel` field code."},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","isNull","isNotNull"]},"values":{"type":"array","description":"**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n","items":{}}}}},"period":{"type":"string","description":"ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."},"comparison":{"type":"string","nullable":true,"description":"As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.","enum":["previousPeriod","samePeriodLastYear","target","benchmark"]},"semanticModelVersion":{"type":"integer","readOnly":true,"description":"The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."}}},
"ReportingUnavailableReason": {"type":"string","description":"Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.","enum":["metricNotModelled","dimensionNotModelled","filterNotModelled","comparisonNotAvailable","periodOutsideHistory"]},
"SiteNormalisationBasis": {"type":"object","x-ticvai-persistence":"reporting.site_normalisation_basis","description":"BI boards 7.9 and 10.4. **The denominators a benchmark divides by**, per site and period: visitors, operating hours, staffed positions and area, one for each `BenchmarkNormalisation` other than `none`. Read by `getAnalyticsBenchmark` for the period that covers the benchmark (data model, 29 September).\n","required":["scopePath","periodStart","periodEnd"],"properties":{"id":{"type":"string","format":"uuid"},"scopePath":{"type":"string","description":"The site (venue scope) the basis applies to."},"periodStart":{"type":"string","format":"date"},"periodEnd":{"type":"string","format":"date"},"visitors":{"type":"integer","nullable":true,"minimum":0,"description":"`perVisitor`."},"operatingHours":{"type":"number","nullable":true,"minimum":0,"description":"`perOperatingHour`."},"staffedPositions":{"type":"number","nullable":true,"minimum":0,"description":"`perStaffedPosition`. Average positions staffed over the period."},"areaSquareMetres":{"type":"number","nullable":true,"minimum":0,"description":"`perSquareMetre`. Operated area."}}}
}
```
