# WS158 — Resource Management Configuration board 4

**10 screens · 15 operations · 17 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `ATTENDANCE_RECORD, REPORT_MANAGE, REPORT_VIEW_VENUE, WORKFORCE_MANAGE, WORKFORCE_VIEW`. A control nobody can use must say so,
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
| `BO-883` | Workforce Roster Command Center | B–D | 0 | 0 | 6 | 10 | 1 | 0 | — | notStarted (—) |
| `BO-884` | Attraction & Operational Staffing Roster | B–D | 0 | 20 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-885` | Minimum Staffing & Coverage Rule Configuration | B–D | 5 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-886` | Staffing Gap & Coverage Control Center | B–D | 4 | 27 | 6 | 1 | 2 | 0 | — | notStarted (—) |
| `BO-887` | Shift Marketplace & Workforce Requests | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-888` | Attendance & Live Workforce Command Center | B–D | 0 | 22 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `BO-889` | Staff Check-In, Check-Out & Attendance Exceptions | B–D | 19 | 5 | 6 | 4 | 1 | 0 | — | notStarted (—) |
| `BO-890` | Workforce Compliance Validation Center | B–D | 0 | 12 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-891` | Labor Cost & Staffing Budget Control | B–D | 10 | 17 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-892` | AI Workforce Planner & Roster Optimization | B–D | 4 | 18 | 6 | 1 | 1 | 1 | — | notStarted (—) |

## Thin screens in this batch

**BO-883, BO-884, BO-887, BO-888, BO-890 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-883` Workforce Roster Command Center

**Provide managers with the primary operational workspace for viewing and managing workforce deployment across venues, attractions, events, departments, and shifts.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/workforce-roster-command-center-bo-883` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `listRotaAssignments` ?from |
| To | date picker | — | — | `listRotaAssignments` ?to |
| Principal | picker: choose a principal | — | — | `listRotaAssignments` ?principalId |
| Department | picker: choose a department | — | — | `listRotaAssignments` ?departmentId |
| From | date picker | — | — | `getStaffingCoverage` ?from |
| To | date picker | — | — | `getStaffingCoverage` ?to |
| Basis | segmented control | Minimum | Minimum · Forecast requirement · Higher of both | `getStaffingCoverage` ?basis |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listRotaAssignments` (onLoad, The roster); `getStaffingCoverage` (onLoad, Where it is short)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-884` Attraction & Operational Staffing Roster: *Attraction & Operational Staffing Roster*
- → `BO-885` Minimum Staffing & Coverage Rule Configuration: *Minimum Staffing & Coverage Rule Configuration*
- → `BO-886` Staffing Gap & Coverage Control Center: *Staffing Gap & Coverage Control Center*
- → `BO-887` Shift Marketplace & Workforce Requests: *Shift Marketplace & Workforce Requests*
- → `BO-888` Attendance & Live Workforce Command Center: *Attendance & Live Workforce Command Center*
- → `BO-889` Staff Check-In, Check-Out & Attendance Exceptions: *Staff Check-In, Check-Out & Attendance Exceptions*
- → `BO-890` Workforce Compliance Validation Center: *Workforce Compliance Validation Center*
- → `BO-891` Labor Cost & Staffing Budget Control: *Labor Cost & Staffing Budget Control*
- → `BO-892` AI Workforce Planner & Roster Optimization: *AI Workforce Planner & Roster Optimization*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workforce roster list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workforce roster untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workforce roster yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workforce roster are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listRotaAssignments` → `WORKFORCE_VIEW` (read) · staff
- `getStaffingCoverage` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.11 | The system should be able to generate operational rosters for staff resources. The rosters should provide information on the staff resources associated with an attraction, their availability, booked … | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.32 | System shall support staff scheduling and assignment. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.33 | System shall manage employee shifts. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.60 | Employees shall receive assignments on mobile devices. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.61 | Employees shall check into assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.62 | Employees shall check out assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.63 | Employees shall view schedules via mobile app. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 18.1.1 | iOS Mobile Application - System shall provide a native iOS application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 18.1.2 | Android Mobile Application - System shall provide a native Android application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 8.2.49 | System shall generate staffing shortage alerts. | Unified Operations Dashboard | CONTRACTED | `getStaffingCoverage` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staffing dashboard shows checked-in, on-shift, on-leave, open-shift and closed-shift counts from check-in/out logs, plus staffing cost including overtime. *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-488)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-883` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-883`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 1: Opens Workforce Roster Command Center → Provide managers with the primary operational workspace for viewing and managing workforce deployment across venues, attractions, events, departments, and shifts.
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F267 branch at step 1 (expected): when Nothing has been set up on Workforce Roster Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F267 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-883?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-884`, `BO-885`, `BO-886`, `BO-887`, `BO-888`, `BO-889`, `BO-890`, `BO-891`, `BO-892`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-884` Attraction & Operational Staffing Roster

**Create detailed staffing plans for individual attractions, experiences, venues, departments, and events.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORKFORCE_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each candidate shall show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/attraction-operational-staffing-roster-bo-884` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every attraction operational staffing** (data table)

| Shows | Format | Notes |
|---|---|---|
| Name | text | not in the schema: `Name` |
| Photograph | text | not in the schema: `Photograph` |
| Role | text | not in the schema: `Role` |
| Skill level | text | not in the schema: `Skill level` |
| Certifications | text | not in the schema: `Certifications` |
| Availability | text | not in the schema: `Availability` |
| Current hours | text | not in the schema: `Current hours` |
| Venue | text | not in the schema: `Venue` |
| Overtime impact | text | not in the schema: `Overtime impact` |
| AI suitability score | text | not in the schema: `AI suitability score` |

**The selected attraction operational staffing** (detail panel): The pack groups this record's detail under its own headings: “Managers shall select”, “Required”, “Scheduled”, “Managers may assign employees through”, “Ticket/Experience Visibility”.

| Shows | Format | Notes |
|---|---|---|
| Name | text | not in the schema: `Name` |
| Photograph | text | not in the schema: `Photograph` |
| Role | text | not in the schema: `Role` |
| Skill level | text | not in the schema: `Skill level` |
| Certifications | text | not in the schema: `Certifications` |
| Availability | text | not in the schema: `Availability` |
| Current hours | text | not in the schema: `Current hours` |
| Venue | text | not in the schema: `Venue` |
| Overtime impact | text | not in the schema: `Overtime impact` |
| AI suitability score | text | not in the schema: `AI suitability score` |

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attraction operational staffing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attraction operational staffing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attraction operational staffing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the attraction operational staffing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Overlaps an existing assignment, or the person lacks the required role |

#### Permissions

- `createRotaAssignment` → `WORKFORCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Roster view per resource shows required vs. scheduled vs. checked-in counts for the day, surfacing discrepancies (e.g. 10 ski trainers scheduled, only 8 checked in). Minimum staffing/coverage rules are set per venue and day (e.g. minimum instructors per level). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-489)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-884` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-884`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 2: Works in Attraction & Operational Staffing Roster → Create detailed staffing plans for individual attractions, experiences, venues, departments, and events.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-884?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `WORKFORCE_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-885` Minimum Staffing & Coverage Rule Configuration

**Define the minimum personnel required to operate safely and effectively.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORKFORCE_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/minimum-staffing-coverage-rule-configuration-bo-885` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Minimum | select field | — | — | — | — | — | — |
| Target | select field | — | — | — | — | — | — |
| Recommended | select field | — | — | — | — | — | — |
| Maximum | select field | — | — | — | — | — | — |
| Enforcement | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The minimum staffing coverage configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the minimum staffing coverage untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No minimum staffing coverage configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setStaffingRules` → `WORKFORCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Roster view per resource shows required vs. scheduled vs. checked-in counts for the day, surfacing discrepancies (e.g. 10 ski trainers scheduled, only 8 checked in). Minimum staffing/coverage rules are set per venue and day (e.g. minimum instructors per level). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-489)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-885` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-885`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 4: Works in Minimum Staffing & Coverage Rule Configuration → Define the minimum personnel required to operate safely and effectively.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-885?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `WORKFORCE_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-886` Staffing Gap & Coverage Control Center

**Identify workforce shortages before they create operational problems.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_VENUE`, `WORKFORCE_VIEW` (1 configure, 1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/staffing-gap-coverage-control-center-bo-886` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | — | — | — | — | Sends `?from=` (required). | — |
| To | date picker | — | — | — | — | Sends `?to=` (required). | — |
| Venue | select field | — | — | — | — | Sends `?venueId=`. | — |
| Severity | select field | — | — | — | — | Client-side on `severity` (covered, tight, short, blocking); the pack's Informational / Warning / High / Critical scale does not map one to one. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getStaffingCoverage` ?from |
| To | date picker | — | — | `getStaffingCoverage` ?to |
| Basis | segmented control | Minimum | Minimum · Forecast requirement · Higher of both | `getStaffingCoverage` ?basis |
| Status | radio group | — | Raised · Acknowledged · Resolved · Expired | `listAlerts` ?status |
| Severity | segmented control | — | Info · Warning · Critical | `listAlerts` ?severity |
| Workstation | picker: choose a workstation | — | — | `listAlerts` ?workstationId |
| Shift | picker: choose a shift | — | — | `listAlerts` ?shiftId |
| Item | picker: choose an item | — | — | `listAlerts` ?itemId |

#### Outputs: what the screen shows and produces

**Shown**

**Planned gap** (metric tile, from `getStaffingCoverage`): Summed across positions.

| Shows | Format | Notes |
|---|---|---|
| Gap | 1,234 | — |

**Blocking gaps** (metric tile, from `getStaffingCoverage`): Count where `severity` is blocking.

| Shows | Format | Notes |
|---|---|---|
| Severity | chip: Covered, Tight, Short, Blocking | — |

**Live operational gap** (metric tile): Required against checked-in staff (the pack's 12 required / 9 checked in = 3); no attendance field is returned.

| Shows | Format | Notes |
|---|---|---|
| Live operational gap | text | not in the schema: `Live operational gap` |

**Coverage by position** (data table, from `getStaffingCoverage`)

| Shows | Format | Notes |
|---|---|---|
| Date | 1 Oct 2026 | — |
| Label | text | — |
| Position code | text | — |
| From | text | — |
| To | text | — |
| Required | 1,234 | — |
| Rostered | 1,234 | — |
| Qualified | 1,234 | A position filled by somebody not qualified for it is still a gap. |
| Checked in | text | not in the schema: `Checked in` |
| Gap | 1,234 | — |
| Severity | chip: Covered, Tight, Short, Blocking | — |

**The selected gap** (detail panel, from `getStaffingCoverage`): Gap type (missing staff / role / skill / certification, absence- or demand-created) and the AI recommendation are pack labels.

| Shows | Format | Notes |
|---|---|---|
| Venue | the name it points at, never the id | — |
| Label | text | — |
| From | text | — |
| To | text | — |
| Required | 1,234 | — |
| Rostered | 1,234 | — |
| Qualified | 1,234 | A position filled by somebody not qualified for it is still a gap. |
| Gap | 1,234 | — |
| Severity | chip: Covered, Tight, Short, Blocking | — |
| Open shifts | list or chips (count when long) | — |
| Gap type | text | not in the schema: `Gap type` |
| Recommended employee | text | not in the schema: `Recommended employee` |
| Match score | text | not in the schema: `Match score` |

**Data it reads**: `getStaffingCoverage` (onLoad, Gaps, by severity); `listAlerts` (onLoad, Staffing shortage alerts (metric staffingShortfall))

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staffing gap coverage list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staffing gap coverage untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No staffing gap coverage yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the staffing gap coverage are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 An `outsideRange` rule without both `threshold` and `thresholdUpper`, or with the upper not above the lower (audit R158) |

#### Permissions

- `getStaffingCoverage` → `WORKFORCE_VIEW` (read) · staff
- `listAlerts` → `REPORT_VIEW_VENUE` (operate) · staff
- `setAlertRule` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.2.49 | System shall generate staffing shortage alerts. | Unified Operations Dashboard | CONTRACTED | `getStaffingCoverage` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- If a scheduled resource fails to check in, the shortfall is flagged for operations and AI can recommend reassigning that resource's bookings. A compliance/validation centre flags events where required staffing is not met, with labour cost tracked. *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-490)*
- Roster view per resource shows required vs. scheduled vs. checked-in counts for the day, surfacing discrepancies (e.g. 10 ski trainers scheduled, only 8 checked in). Minimum staffing/coverage rules are set per venue and day (e.g. minimum instructors per level). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-489)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-886` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-886`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 6: Works in Staffing Gap & Coverage Control Center → Identify workforce shortages before they create operational problems.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (27 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-886?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_VENUE`, `WORKFORCE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-887` Shift Marketplace & Workforce Requests

**Allow employees and managers to manage shift changes through controlled workflows rather than informal manual communication.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/shift-marketplace-workforce-requests-bo-887` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Claim open shift (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listOpenShifts` (onLoad, The shift marketplace)

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The shift marketplace workforce list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the shift marketplace workforce untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No shift marketplace workforce yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the shift marketplace workforce are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already taken, not eligible, or it would breach a working-hour rule |

#### Permissions

- `listOpenShifts` → `WORKFORCE_VIEW` (read) · staff
- `claimOpenShift` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staff can request a swap (e.g. break coverage) from another resource; attendance exceptions are marked manually (active, not active, absent, other). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering; 4.9 AI Optimization, Mobile App & Analytics · DI-491)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-887` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-887`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 8: Works in Shift Marketplace & Workforce Requests → Allow employees and managers to manage shift changes through controlled workflows rather than informal manual communication.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-887?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Claim open shift, Cancel.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-888` Attendance & Live Workforce Command Center

**Provide real-time visibility into whether scheduled employees actually reported and are available for operation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/attendance-live-workforce-command-center-bo-888` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Date | date picker | — | — | `listAttendance` ?date |
| Principal | picker: choose a principal | — | — | `listAttendance` ?principalId |
| Exceptions only | toggle | — | — | `listAttendance` ?exceptionsOnly |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every attendance live workforce** (data table)

| Shows | Format | Notes |
|---|---|---|
| Scheduled today | text | not in the schema: `Scheduled today` |
| Checked in | text | not in the schema: `Checked in` |
| Not yet arrived | text | not in the schema: `Not yet arrived` |
| Late | text | not in the schema: `Late` |
| Absent | text | not in the schema: `Absent` |
| No show | text | not in the schema: `No-show` |
| On break | text | not in the schema: `On break` |
| Checked out | text | not in the schema: `Checked out` |
| Overtime | text | not in the schema: `Overtime` |
| Attendance exceptions | text | not in the schema: `Attendance exceptions` |
| Planned vs actual | text | not in the schema: `Planned vs Actual` |

**The selected attendance live workforce** (detail panel): The pack groups this record's detail under its own headings: “For each employee”.

| Shows | Format | Notes |
|---|---|---|
| Scheduled today | text | not in the schema: `Scheduled today` |
| Checked in | text | not in the schema: `Checked in` |
| Not yet arrived | text | not in the schema: `Not yet arrived` |
| Late | text | not in the schema: `Late` |
| Absent | text | not in the schema: `Absent` |
| No show | text | not in the schema: `No-show` |
| On break | text | not in the schema: `On break` |
| Checked out | text | not in the schema: `Checked out` |
| Overtime | text | not in the schema: `Overtime` |
| Attendance exceptions | text | not in the schema: `Attendance exceptions` |
| Planned vs actual | text | not in the schema: `Planned vs Actual` |

**Data it reads**: `listAttendance` (onLoad, Live attendance)

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attendance live workforce list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attendance live workforce untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attendance live workforce yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the attendance live workforce are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAttendance` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.9.7 | System shall display staffing levels, shift attendance, assignments, absences, overtime, and workforce utilization. | Unified Operations Dashboard | CONTRACTED | `listAttendance` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staffing dashboard shows checked-in, on-shift, on-leave, open-shift and closed-shift counts from check-in/out logs, plus staffing cost including overtime. *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-488)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-888` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-888`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 10: Works in Attendance & Live Workforce Command Center → Provide real-time visibility into whether scheduled employees actually reported and are available for operation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-888?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-889` Staff Check-In, Check-Out & Attendance Exceptions

**Record actual employee working activity and manage exceptions to scheduled attendance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ATTENDANCE_RECORD`, `WORKFORCE_MANAGE` (1 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§The system shall capture; Every correction shall capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `recordId` (navigation) |
| Route | `/rentals/staff-check-in-check-out-attendance-exceptions-bo-889` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Planned check-in | select field | — | — | — | — | — | — |
| Actual check-in | select field | — | — | — | — | — | — |
| Planned check-out | select field | — | — | — | — | — | — |
| Actual check-out | select field | — | — | — | — | — | — |
| Attendance status | select field | — | — | — | — | — | — |
| Lateness | select field | — | — | — | — | — | — |
| Early departure | select field | — | — | — | — | — | — |
| Overtime | select field | — | — | — | — | — | — |
| No-show | select field | — | — | — | — | — | — |
| Exception | select field | — | — | — | — | — | — |
| Source/device | select field | — | — | — | — | — | — |
| Exception Types | select field | — | — | — | — | — | — |
| Original value | select field | — | — | — | — | — | — |
| New value | select field | — | — | — | — | — | — |
| User | select field | — | — | — | — | — | — |
| Timestamp | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |
| Approval where required | select field | — | — | — | — | — | — |
| Mobile Assignment Check-In | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Amendment history** (data table, from `amendAttendance`): **Every correction, not only the last** (decided 28 September, audit R129 (7)) — read from `AttendanceRecord.amendments`: who, when, before, after and why.

| Shows | Format | Notes |
|---|---|---|
| Amended at | 1 Oct 2026, 14:30 | — |
| Amended by principal | the name it points at, never the id | — |
| Occurred at before | 1 Oct 2026, 14:30 | The record's time before this correction. |
| Occurred at after | 1 Oct 2026, 14:30 | The time this correction set (`correctedAt` on the request). |
| Reason | text | — |

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staff check-in check-out configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staff check-in check-out untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No staff check-in check-out configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported rather than silently corrected. |

#### Permissions

- `recordAttendance` → `ATTENDANCE_RECORD` (operate) · staff
- `amendAttendance` → `WORKFORCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.81 | System shall record planned shifts, actual check-in times, actual check-out times, attendance status, lateness, early departures, no-shows, overtime hours, attendance exceptions, and workforce … | Ticketing Catalogue | CONTRACTED | `recordAttendance` |
| 18.9.1 | Attendance Management - Users shall clock in and clock out. | Employee Mobile App & AI Assistant | CONTRACTED | `recordAttendance` |
| 18.9.2 | Shift Management - Users shall view assigned shifts. | Employee Mobile App & AI Assistant | CONTRACTED | `recordAttendance` |
| 1.2.75 | System shall maintain complete audit logs. | Ticketing Catalogue | CONTRACTED | `amendAttendance` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staff can request a swap (e.g. break coverage) from another resource; attendance exceptions are marked manually (active, not active, absent, other). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering; 4.9 AI Optimization, Mobile App & Analytics · DI-491)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-889` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-889`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 12: Works in Staff Check-In, Check-Out & Attendance Exceptions → Record actual employee working activity and manage exceptions to scheduled attendance.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-889?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `ATTENDANCE_RECORD`, `WORKFORCE_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-890` Workforce Compliance Validation Center

**Validate planned workforce schedules against legal, safety, certification, and organizational rules before roster publication or assignment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each issue shall display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/workforce-compliance-validation-center-bo-890` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `validateWorkforceCompliance` ?from |
| To | date picker | — | — | `validateWorkforceCompliance` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every workforce compliance validation** (data table)

| Shows | Format | Notes |
|---|---|---|
| Employee | text | not in the schema: `Employee` |
| Rule violated | text | not in the schema: `Rule violated` |
| Severity | text | not in the schema: `Severity` |
| Affected shift | text | not in the schema: `Affected shift` |
| Operational impact | text | not in the schema: `Operational impact` |
| Recommended action | text | not in the schema: `Recommended action` |

**The selected workforce compliance validation** (detail panel): The pack groups this record's detail under its own headings: “The engine shall support”.

| Shows | Format | Notes |
|---|---|---|
| Employee | text | not in the schema: `Employee` |
| Rule violated | text | not in the schema: `Rule violated` |
| Severity | text | not in the schema: `Severity` |
| Affected shift | text | not in the schema: `Affected shift` |
| Operational impact | text | not in the schema: `Operational impact` |
| Recommended action | text | not in the schema: `Recommended action` |

**Data it reads**: `validateWorkforceCompliance` (onLoad, Where the rota breaks a rule)

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workforce compliance validation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workforce compliance validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workforce compliance validation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workforce compliance validation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `validateWorkforceCompliance` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- If a scheduled resource fails to check in, the shortfall is flagged for operations and AI can recommend reassigning that resource's bookings. A compliance/validation centre flags events where required staffing is not met, with labour cost tracked. *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-490)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-890` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-890`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 14: Works in Workforce Compliance Validation Center → Validate planned workforce schedules against legal, safety, certification, and organizational rules before roster publication or assignment.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-890?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-891` Labor Cost & Staffing Budget Control

**Give managers visibility into the financial impact of staffing decisions before and after roster publication.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/labor-cost-staffing-budget-control-bo-891` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listLabourBudgets`. | `listLabourBudgets` ?venueId |
| Department id | picker: choose a department (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?departmentId=` to `listLabourBudgets`. | `listLabourBudgets` ?departmentId |
| From | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?from=` to `listLabourBudgets`. | `listLabourBudgets` ?from |
| To | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?to=` to `listLabourBudgets`. | `listLabourBudgets` ?to |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getLabourCost` ?from |
| To | date picker | — | — | `getLabourCost` ?to |
| Group by | radio group | — | Venue · Department · Role · Day · Person | `getLabourCost` ?groupBy |

**Form: Save labour budget** (modal, opened by *Save labour budget*; *Save labour budget* calls `setLabourBudget`, *Cancel* sends nothing)

**Collects what `setLabourBudget` sends before it is called.** Required: `id`, `venueId`, `periodStart`, `periodEnd`, `budgetAmount`. Optional: `departmentId`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setLabourBudget` body |
| Department `departmentId` | picker: choose a department | optional | — | — | shows names, sends the id | — | `setLabourBudget` body |
| Period start `periodStart` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | First day of the period, in the Region's time zone | `setLabourBudget` body |
| Period end `periodEnd` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | Last day of the period, in the Region's time zone | `setLabourBudget` body |
| Budget amount `budgetAmount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setLabourBudget` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setLabourBudget` body |

Errors to draw in the form: 409 The period overlaps another budget for the same venue and department; 422 periodEnd is before periodStart

#### Outputs: what the screen shows and produces

**Shown**

**Every labor cost staffing** (data table)

| Shows | Format | Notes |
|---|---|---|
| Budget | text | not in the schema: `Budget` |
| Scheduled | text | not in the schema: `Scheduled` |
| Forecast | text | not in the schema: `Forecast` |
| Actual | text | not in the schema: `Actual` |
| Variance | text | not in the schema: `Variance` |

**Every labour budget** (data table, from `listLabourBudgets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Period start | 1 Oct 2026 | First day of the period, in the Region's time zone |
| Period end | 1 Oct 2026 | Last day of the period, in the Region's time zone |
| Budget amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Scope path | text | — |

**The selected labor cost staffing** (detail panel): The pack groups this record's detail under its own headings: “Cost Calculation”, “Managers shall understand”.

| Shows | Format | Notes |
|---|---|---|
| Budget | text | not in the schema: `Budget` |
| Scheduled | text | not in the schema: `Scheduled` |
| Forecast | text | not in the schema: `Forecast` |
| Actual | text | not in the schema: `Actual` |
| Variance | text | not in the schema: `Variance` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save labour budget (primary button) | `setLabourBudget` PUT `/labour-budgets` | LabourBudget | LabourBudget | 409 The period overlaps another budget for the same venue and department; 422 periodEnd is before periodStart | gated `WORKFORCE_MANAGE`; opens modal first |

**Data it reads**: `getLabourCost` (onLoad, Cost against budget); `listLabourBudgets` (onLoad, Labour budgets, per venue, department and period)

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The labor cost staffing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the labor cost staffing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No labor cost staffing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the labor cost staffing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The period overlaps another budget for the same venue and department; 422 periodEnd is before periodStart |

#### Permissions

- `getLabourCost` → `WORKFORCE_VIEW` (read) · staff
- `listLabourBudgets` → `WORKFORCE_VIEW` (read) · staff
- `setLabourBudget` → `WORKFORCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staffing dashboard shows checked-in, on-shift, on-leave, open-shift and closed-shift counts from check-in/out logs, plus staffing cost including overtime. *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-488)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-891` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-891`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 16: Works in Labor Cost & Staffing Budget Control → Give managers visibility into the financial impact of staffing decisions before and after roster publication.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-891?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save labour budget.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-892` AI Workforce Planner & Roster Optimization

**Provide TICVAI's intelligent workforce-planning experience by automatically generating or optimizing operational rosters. Administrators may configure optimization priorities such as: Best operational coverage Minimize overtime Minimize labor cost Balance employee hours Minimize cross-venue movement Maximize skill match Prioritize employee continuity Safety, compliance, and mandatory qualification rules shall remain hard constraints. AI Explanation Provide TICVAI with a centralized Resource Requirement & Assignment Engine that connects ticket products, attraction experiences, sessions, and time slots with the operational resources required to deliver them. Board 5 shall allow administrators to configure: Which resources an experience requires How many resources are required Which resource combinations are valid Which skills and qualifications are mandatory How resource requirements change with ticket quantity or capacity Whether customers may select a specific resource Whether customers may select a resource skill/type rather than a specific person Whether TICVAI should automatically allocate resources How resource priority is calculated What happens when the assigned resource becomes unavailable How assignments are exposed through POS, B2C, B2B, mobile, and APIs**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/ai-workforce-planner-roster-optimization-bo-892` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | — | — | — | — | Sends `?from=` (required). | — |
| To | date picker | — | — | — | — | Sends `?to=` (required). | — |
| Venue | select field | — | — | — | — | Sends `?venueId=`. | — |
| Optimization objective | select field | — | — | — | — | Best coverage, minimise overtime, minimise labour cost, balance hours, minimise cross-venue movement, maximise skill match, continuity. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getStaffingCoverage` ?from |
| To | date picker | — | — | `getStaffingCoverage` ?to |
| Basis | segmented control | Minimum | Minimum · Forecast requirement · Higher of both | `getStaffingCoverage` ?basis |

#### Outputs: what the screen shows and produces

**Shown**

**Staffing gaps (current roster)** (metric tile, from `getStaffingCoverage`): Summed; the AI-optimised side of the comparison has no read.

| Shows | Format | Notes |
|---|---|---|
| Gap | 1,234 | — |

**Coverage** (metric tile): The pack asks for coverage; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Coverage | text | not in the schema: `Coverage` |

**Overtime hours** (metric tile): The pack asks for overtime hours; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Overtime hours | text | not in the schema: `Overtime hours` |

**Projected labour cost** (metric tile): The pack asks for projected labour cost; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Projected labour cost | text | not in the schema: `Projected labour cost` |

**Projected saving** (metric tile): The pack asks for projected saving; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Projected saving | text | not in the schema: `Projected saving` |

**Current roster coverage** (data table, from `getStaffingCoverage`)

| Shows | Format | Notes |
|---|---|---|
| Date | 1 Oct 2026 | — |
| Label | text | — |
| From | text | — |
| To | text | — |
| Required | 1,234 | — |
| Rostered | 1,234 | — |
| Qualified | 1,234 | A position filled by somebody not qualified for it is still a gap. |
| Gap | 1,234 | — |
| Severity | chip: Covered, Tight, Short, Blocking | — |

**Why this assignment** (detail panel): The pack's explanation ("Available, Level 3 Instructor, certification valid, language match, already at venue, no overtime").

| Shows | Format | Notes |
|---|---|---|
| Employee | text | not in the schema: `Employee` |
| Assignment | text | not in the schema: `Assignment` |
| Reasons | text | not in the schema: `Reasons` |
| Hard constraints satisfied | text | not in the schema: `Hard constraints satisfied` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Generate roster with AI (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `getStaffingCoverage` (onLoad, What the planner is optimising)

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workforce planner roster list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workforce planner roster untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workforce planner roster yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workforce planner roster are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getStaffingCoverage` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.2.49 | System shall generate staffing shortage alerts. | Unified Operations Dashboard | CONTRACTED | `getStaffingCoverage` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI forecasting from historical bookings recommends staffing levels for upcoming periods (e.g. "you will need this many resources over the next week") so leave and availability can be planned. Analytics show total cost and revenue by resource and by event. *(client request · MoM 26 Aug 2026, 4.9 AI Optimization, Mobile App & Analytics · DI-501)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'plan your adventure')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-892` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-892`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 18: Works in AI Workforce Planner & Roster Optimization → Provide TICVAI's intelligent workforce-planning experience by automatically generating or optimizing operational rosters.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-892?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Generate roster with AI.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**11 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"amendAttendance": {"method":"POST","path":"/attendance/{recordId}/amend","contract":"workforce","summary":"A supervisor corrects a record","permission":"WORKFORCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"claimOpenShift": {"method":"POST","path":"/shift-marketplace","contract":"workforce","summary":"Pick up a released shift","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OpenShift"},
"createRotaAssignment": {"method":"POST","path":"/rota-assignments","contract":"workforce","summary":"Put someone on the rota","permission":"WORKFORCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RotaAssignment","responds":"RotaAssignment"},
"getLabourCost": {"method":"GET","path":"/labour-cost","contract":"workforce","summary":"Rostered and actual labour cost against budget","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"LabourCostRow"},
"getStaffingCoverage": {"method":"GET","path":"/staffing-coverage","contract":"workforce","summary":"Where the rota is short, and by how much","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"venueId","in":"query","required":null},{"name":"basis","in":"query","required":null}],"requestBody":null,"responds":"StaffingCoverage"},
"listAlerts": {"method":"GET","path":"/alerts","contract":"reporting","summary":"What is currently wrong","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"severity","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"itemId","in":"query","required":null}],"requestBody":null,"responds":"Alert"},
"listAttendance": {"method":"GET","path":"/attendance","contract":"workforce","summary":"Who was here","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"date","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"exceptionsOnly","in":"query","required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"listLabourBudgets": {"method":"GET","path":"/labour-budgets","contract":"workforce","summary":"Labour budgets, per venue, department and period","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"departmentId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOpenShifts": {"method":"GET","path":"/shift-marketplace","contract":"workforce","summary":"Shifts offered back, and who may take them","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"OpenShift"},
"listRotaAssignments": {"method":"GET","path":"/rota-assignments","contract":"workforce","summary":"The rota","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"departmentId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"recordAttendance": {"method":"POST","path":"/attendance/clock","contract":"workforce","summary":"Clock in, clock out, or take a break","permission":"ATTENDANCE_RECORD","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"setAlertRule": {"method":"PUT","path":"/alert-rules","contract":"reporting","summary":"Watch a metric and tell somebody","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AlertRule","responds":"AlertRule"},
"setLabourBudget": {"method":"PUT","path":"/labour-budgets","contract":"workforce","summary":"Set the labour budget for a venue, department and period","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LabourBudget","responds":"LabourBudget"},
"setStaffingRules": {"method":"PUT","path":"/staffing-rules","contract":"workforce","summary":"Minimum cover, working-hour limits and overtime","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"StaffingRules","responds":"StaffingRules"},
"validateWorkforceCompliance": {"method":"GET","path":"/workforce-compliance","contract":"workforce","summary":"Where the rota breaks a rule","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"WorkforceComplianceFinding"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Alert": {"type":"object","x-ticvai-persistence":"reporting.alert","description":"A raised alert. **Acknowledged rather than dismissed** — CF-134 asked for it markable, and the difference is that an acknowledgement records who saw it.\n","required":["id","ruleId","raisedAt","severity","status"],"properties":{"id":{"type":"string","format":"uuid"},"ruleId":{"type":"string","format":"uuid"},"ruleName":{"type":"string","description":"`AlertRule.name` as it stood when the alert was raised. **The line a person reads** — a list of rule ids is not an alert panel, and a screen should not need `listAlertRules` to label one.\n"},"metric":{"allOf":[{"$ref":"#/components/schemas/MetricSource"}],"description":"The rule's metric, carried so the alert says what went out of range."},"raisedAt":{"type":"string","format":"date-time"},"severity":{"$ref":"#/components/schemas/AlertSeverity"},"status":{"$ref":"#/components/schemas/AlertStatus"},"observedValue":{"$ref":"#/components/schemas/MetricValue"},"threshold":{"$ref":"#/components/schemas/MetricValue"},"scopePath":{"type":"string"},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation the reading was taken for, where the metric is measured per workstation (`salesByWorkstation`). Null otherwise. `listAlerts` filters on it."},"shiftId":{"type":"string","format":"uuid","nullable":true,"description":"The till shift (`orders.pos_shift`) the reading belongs to, where it was taken for a workstation with a shift open. Null otherwise. `listAlerts` filters on it."},"itemId":{"type":"string","format":"uuid","nullable":true,"description":"The inventory item the reading is about, where the metric is measured per item (`stockAgeing`, `stockTurnover`, `wastageRate`, `inventoryValuation`). Null otherwise. **What a replenishment screen prefills a requisition from.**\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true},"acknowledgementNote":{"type":"string","maxLength":300,"nullable":true,"description":"The `note` given to `acknowledgeAlert`. Kept, because an acknowledgement that says what is being done about it is the one escalation can skip."},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"description":"**Set when the metric returns to range, automatically.** An alert that only a person can close is an alert list that only grows.\n"},"escalatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. **A critical alert nobody acknowledged is the case escalation exists for.**\n"}}},
"AlertRule": {"type":"object","x-ticvai-persistence":"reporting.alert_rule","description":"BL-152, CF-134. **Six contracts detect their own trouble and none told a person.**\nFive sections ask for this and it is the same gap as `MessageTrigger`, seen from the operational side — **that one tells a guest something happened; this one tells an operator something is wrong.**\n**A threshold that nobody is watching is a threshold nobody set.** 6.1.57 wants an exception when a KPI leaves range, and an exception that arrives in a nightly report is an exception nobody acted on.\n","required":["id","name","metric","comparator","threshold","severity","isActive","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"metric":{"allOf":[{"$ref":"#/components/schemas/MetricSource"}],"description":"**From the closed set**, so a rule cannot watch something nothing produces — the same discipline `MetricSource` exists for.\n"},"comparator":{"type":"string","enum":["above","below","outsideRange","changesBy","equals"]},"threshold":{"$ref":"#/components/schemas/MetricValue"},"thresholdUpper":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true,"description":"**Required when `comparator` is `outsideRange`** (decided 28 September, audit R158): the range is `threshold` to `thresholdUpper`, and a rule missing either, or with the upper not above the lower, is refused by `setAlertRule` with 400. Ignored for every other comparator.\n"},"windowMinutes":{"type":"integer","default":15,"description":"**The window is what stops an alert firing on noise.** A queue that spikes for ninety seconds is not a queue that needs a manager, and a rule with no window is a rule somebody mutes within a week.\n"},"severity":{"$ref":"#/components/schemas/AlertSeverity"},"deliverTo":{"type":"array","description":"CF-134. **The dashboard panel is the default and the only one that always applies.** Email or WhatsApp where the matrix names them — an operational alert arriving by email is an alert nobody sees in time.\n","items":{"type":"string","enum":["dashboardPanel","email","whatsapp","sms","push"]},"x-ticvai-push-note":"**`push` added 29 September** (6.1.56, 18.1.5, build pass): delivered to every staff-app handset registered for a recipient (tenancy `RegisteredDevice`, kind `mobileHandset`, with a push token). It is how a daily revenue alert reaches a manager's phone, which a panel on a web dashboard does not.\n"},"recipientRoleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"cooldownMinutes":{"type":"integer","default":30,"description":"**How long before the same rule may fire again.** Without it, a metric hovering on a threshold produces forty alerts an hour and the panel becomes something people close.\n"},"isActive":{"type":"boolean"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**\n\n**Required, and it is the write target.** `setAlertRule` has no id in its path and a caller may hold several venues, so the rule names the venue it watches here — inside the caller's scope, or the write is refused."}}},
"AlertSeverity": {"type":"string","description":"How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter.","enum":["info","warning","critical"]},
"AlertStatus": {"type":"string","description":"Where a raised alert is. Shared by `Alert` and the `listAlerts` filter.","enum":["raised","acknowledged","resolved","expired"]},
"AttendanceAmendment": {"type":"object","x-ticvai-persistence":"workforce.attendance_amendment","description":"One correction to an attendance record, appended by `amendAttendance` and never updated (decided 28 September, audit R129 (7)).\n","required":["id","attendanceRecordId","amendedByPrincipalId","amendedAt","occurredAtBefore","occurredAtAfter","reason"],"properties":{"id":{"type":"string","format":"uuid"},"attendanceRecordId":{"type":"string","format":"uuid"},"amendedByPrincipalId":{"type":"string","format":"uuid"},"amendedAt":{"type":"string","format":"date-time"},"occurredAtBefore":{"type":"string","format":"date-time","description":"The record's time before this correction."},"occurredAtAfter":{"type":"string","format":"date-time","description":"The time this correction set (`correctedAt` on the request)."},"reason":{"type":"string","maxLength":300}}},
"AttendanceRecord": {"type":"object","x-ticvai-persistence":"workforce.attendance","required":["id","principalId","kind","occurredAt"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"assignmentId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["clockIn","clockOut","breakStart","breakEnd"]},"occurredAt":{"type":"string","format":"date-time","description":"Device time — when it happened."},"recordedAt":{"type":"string","format":"date-time","description":"When the server received it. **Both are kept**: a steward clocking in offline at a gate is not late because the sync was.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true},"latitude":{"type":"number","nullable":true},"longitude":{"type":"number","nullable":true},"isAmended":{"type":"boolean","readOnly":true},"amendedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who made the latest amendment. The full history is `amendments` (audit R129 (7))."},"amendmentReason":{"type":"string","nullable":true,"readOnly":true,"description":"The latest amendment's reason. The full history is `amendments` (audit R129 (7))."},"originalOccurredAt":{"type":"string","format":"date-time","nullable":true,"description":"**The original is never overwritten.** Attendance feeds pay, and a record that can be quietly rewritten is not evidence.\n"},"amendments":{"type":"array","readOnly":true,"description":"**Every correction, oldest first, one row each** (decided 28 September, audit R129 (7)). A single set of amendment columns holds only the last one, and the second correction to a record would erase the evidence of the first.\n","items":{"$ref":"#/components/schemas/AttendanceAmendment"}},"exception":{"type":"string","nullable":true,"enum":["late","earlyLeave","missingClockOut","noShow","outOfGeofence","unscheduled"],"description":"Computed against the rota. Null where the record matches what was expected."}}},
"LabourBudget": {"type":"object","x-ticvai-persistence":"workforce.labour_budget","description":"**The labour budget a general manager is held to, per venue, department and period** (resource board 4.9; data model for the agreed operations, 29 September). `getLabourCost` compares rostered and actual cost against it (`LabourCostRow.budget`). A null `departmentId` is the whole venue's budget. Periods for one venue and department do not overlap. Written by `setLabourBudget`, listed by `listLabourBudgets` (decided 29 September, writers pass).","required":["id","venueId","periodStart","periodEnd","budgetAmount"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"periodStart":{"type":"string","format":"date","description":"First day of the period, in the Region's time zone"},"periodEnd":{"type":"string","format":"date","description":"Last day of the period, in the Region's time zone"},"budgetAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scopePath":{"type":"string"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"LabourCostRow": {"type":"object","description":"Resource board 4.9. **Rostered and actual diverge every day.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"rosteredHours":{"type":"number"},"actualHours":{"type":"number"},"overtimeHours":{"type":"number"},"rosteredCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"actualCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"budget":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variancePercent":{"type":"number"},"headcount":{"type":"integer"}}},
"MetricSource": {"type":"string","description":"**A named metric with a verified source.** BL-053, 75 requirement rows.\n`reporting` is a generic builder, and **a generic builder makes every reporting requirement look covered** — it will happily assemble a report over data nobody produces. That is the shape to watch across the whole walk, and this enum is the answer to it: each value below was checked against the schema before being named.\n| Metric | Source | |---|---| | `occupancy` | `catalogue.channel_capacity.sold` and `leased` against `capacity` | | `capacityUtilisation` | `catalogue.channel_capacity.remaining` over the same window | | `admissionRate` | `access.scan_event.outcome`, in-direction | | `noShowRate` | Entitlements issued against scans that never arrived | | `conversion` | `orders.cart` against `orders.sales_order` | | `salesByOperator` | `orders.sales_order.principal_id` | | `salesByWorkstation` | The workstation on the shift that took it | | `waitTime` | `queue.waiting_guest.estimated_call_at` against `called_at` | | `throughput` | `queue.waiting_guest` completions per hour | | `abandonmentRate` | Queue entries that left before being called |\n**`salesByInstructor` was deliberately absent from the first cut** because it needed the staff-assignment link CL-01 covers. It was added on 18 August once `resources.Resource` produced it — see `x-ticvai-extension-note` below. Naming a metric with no source is still the defect this enum exists to prevent.\n**Money-valued metrics are listed in `x-ticvai-money-valued`.** A reading or threshold on one of them is a `Money`, never a float (`MetricValue`).\n","enum":["occupancy","capacityUtilisation","admissionRate","noShowRate","conversion","salesByOperator","salesByWorkstation","waitTime","throughput","abandonmentRate","inventoryValuation","stockTurnover","stockAgeing","wastageRate","resaleVolume","resaleCommission","salesByInstructor","resourceUtilisation","allocationUtilisation","channelAllocationBurn","membershipChurn","membershipRenewalRate","supplierDeliveryPerformance","revenuePerEntitlement","revenuePerVisitor","assetDowntime","meanTimeToRepair","challengeCompletionRate","attributedRevenue","loyaltyActiveMembers","loyaltyTierDistribution","loyaltyPointsLiability","loyaltyBreakageRate","loyaltyMemberRetention","challengeParticipationRate","gamificationLoyaltyImpact","gamificationMembershipImpact","gamificationRetention","accreditationApplications","accreditationTimeToDecision","accreditationCredentialsIssued","accreditationActiveHolders","accreditationRenewalsDue","staffingShortfall"],"x-ticvai-money-valued":["inventoryValuation","resaleCommission","revenuePerEntitlement","revenuePerVisitor","attributedRevenue","loyaltyPointsLiability"],"x-ticvai-extended-29-september":"**Fourteen metrics added 29 September (build pass)**, each checked against the schema of the contract that produces it.\n\n| Metric | Source | Requirement | |---|---|---| | `loyaltyActiveMembers` | `marketing.loyalty_position` members with a `marketing.loyalty_points` movement in the period | 5.4.27 | | `loyaltyTierDistribution` | `marketing.loyalty_position.tier_id` against `marketing.programme_tier`, members per tier | 5.4.27 | | `loyaltyPointsLiability` | the balance of `ledger.journal_line` on each programme's `pointsLiabilityAccountId`, where points post on accrual and release on redemption or expiry | 5.4.27 | | `loyaltyBreakageRate` | `marketing.loyalty_points` expiry movements over points earned, in the period | 5.4.27 | | `loyaltyMemberRetention` | members with a movement in the previous period who also have one in this period | 5.4.27 | | `challengeParticipationRate` | distinct `marketing.challenge_progress.subject_id` over active loyalty members | 22.6.20 | | `gamificationLoyaltyImpact` | points earned per member, challenge participants against non-participants (`marketing.loyalty_points` split by `marketing.challenge_progress`) | 22.6.20 | | `gamificationMembershipImpact` | joins and renewals in `identity.customer_membership`, participants against non-participants | 22.6.20 | | `gamificationRetention` | return visits (`access.scan_event`, in-direction) of participants against non-participants | 22.6.20 | | `accreditationApplications` | `accreditation.application` by `status` | 12.1.50 | | `accreditationTimeToDecision` | `accreditation.application.decided_at` minus `submitted_at` | 12.1.50 | | `accreditationCredentialsIssued` | `accreditation.credential.issued_at` | 12.1.50 | | `accreditationActiveHolders` | `accreditation.holder` `active`, by `category_code` | 12.1.50 | | `accreditationRenewalsDue` | `accreditation.holder.valid_to` inside `accreditation.validity.renewal_window_days` | 12.1.50 |\n\n**`staffingShortfall` added the same evening (build pass, group G2; 8.2.49)**: the largest gap in the window between the staff rostered and the staff the forecast requires, per venue and position, from `workforce.forecast_requirement` (the handed-over AI staff requirement) against `workforce.rota_assignment` and `workforce.open_shift`, computed as `workforce.getStaffingCoverage` with `basis` `forecastRequirement`. An `AlertRule` on it with `comparator` `above` and `threshold` 0 is the staffing shortage alert; `windowMinutes` looks ahead rather than back for this metric (the rota for the coming window), and `cooldownMinutes` stops one short shift alerting every quarter hour.\n\n**Points issued, points redeemed, campaign performance and reward redemption were already served** by the `loyalty` and `campaigns` sources, and challenge completion and revenue attribution by `challengeCompletionRate` and `attributedRevenue`.\n","x-ticvai-money-valued-note":"**`salesByOperator`, `salesByWorkstation` and `resaleVolume` are not listed because the package does not say whether they count sales or sum their value.** Until that is decided, a rule on them carries a plain number.\n","x-ticvai-extended":"18 August 2026","x-ticvai-extension-note":"**Nineteen metrics added when their upstream models landed**, which is how BL-053 was always going to close — not by changing `reporting` but by building the things it wanted to report on.\n`inventoryValuation`, `stockTurnover`, `stockAgeing` and `wastageRate` came from `inventory.StockBatch`; `resaleVolume` and `resaleCommission` from `orders.ResaleListing`; **`salesByInstructor` from `resources.Resource`, which was the one metric this enum deliberately refused to name in the morning** because nothing produced it. `allocationUtilisation` from `PartnerUser` and `ChannelListing`, `membershipChurn` from `Journey`, `supplierDeliveryPerformance` from `ProductionRun`, `assetDowntime` and `meanTimeToRepair` from `WorkOrder.downtimeMinutes`, `challengeCompletionRate` from `ChallengeProgress`, `attributedRevenue` from `AttributionTouch`.\n**Each was checked against the schema before being named.** That rule has not changed — naming a metric with no source is the defect this enum exists to prevent.\n"},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"OpenShift": {"type":"object","x-ticvai-persistence":"workforce.open_shift","description":"Resource board 4.6. **How a gap gets filled at nine on a Friday without a manager ringing round.**\n","properties":{"id":{"type":"string","format":"uuid"},"rotaAssignmentId":{"type":"string","format":"uuid","nullable":true},"shiftTemplateId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid"},"positionCode":{"type":"string"},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"releasedBy":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","nullable":true},"requiredQualifications":{"type":"array","items":{"type":"string"}},"eligiblePrincipalCount":{"type":"integer","readOnly":true},"incentiveRateMultiplier":{"type":"number","nullable":true},"status":{"type":"string","enum":["open","claimed","pendingApproval","filled","expired","withdrawn"]},"claimedBy":{"type":"string","format":"uuid","nullable":true},"claimedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RotaAssignment": {"type":"object","x-ticvai-persistence":"workforce.rota_assignment","required":["principalId","venueId","startsAt","endsAt","position"],"properties":{"overtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"description":"BL-044, 1.2.83. **UAE labour law limits working hours and mandates rest periods**, and nothing in the package counted either. Derived from attendance against the shift.\n"},"restPeriodBefore":{"type":"integer","nullable":true,"description":"Minutes since the previous shift ended. **The check that stops a closing shift followed by an opening one**, which is legal in most places and unsafe in all of them.\n"},"breachesWorkingHourLimit":{"type":"boolean","default":false,"readOnly":true,"description":"**Flagged at assignment, not discovered at payroll.** A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a month later means it was worked.\n"},"labourCost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**Cost at the point of scheduling.** A manager building a rota without seeing its cost is a manager who finds out from finance.\n"},"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string","readOnly":true},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"position":{"type":"string","description":"What they are rostered to do — gate steward, cashier, lifeguard, technician. **Most positions never touch a till**, which is why a rota assignment is not a shift.\n**A position code, not a label.** It is the same value as `StaffingRules.minimumCover[].positionCode`, `OpenShift.positionCode` and `StaffingCoverage.positionCode`: coverage counts rostered people per position, so an assignment spelled differently from the rule it fills is counted against nothing and the gap stays open. Tenant-defined, which is why it is not an enum here.\n"},"requiredRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Checked on assignment. A rota naming someone unqualified is a rota that gets overridden."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Where the position needs a till. **The link between a rota and a cash session**, without merging the two.\n"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"status":{"$ref":"#/components/schemas/RotaStatus"},"breakMinutes":{"type":"integer","nullable":true},"note":{"type":"string","nullable":true}}},
"RotaStatus": {"type":"string","enum":["planned","published","confirmed","swapPending","cancelled","completed","noShow"]},
"StaffingCoverage": {"type":"object","description":"Resource board 4.4. **The gap is the product.**","properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid"},"positionCode":{"type":"string"},"label":{"type":"string"},"from":{"type":"string"},"to":{"type":"string"},"required":{"type":"integer"},"rostered":{"type":"integer"},"qualified":{"type":"integer","description":"**A position filled by somebody not qualified for it is still a gap.**"},"gap":{"type":"integer"},"severity":{"type":"string","enum":["covered","tight","short","blocking"]},"openShiftIds":{"type":"array","items":{"type":"string","format":"uuid"}},"basisApplied":{"type":"string","enum":["minimum","forecastRequirement"],"description":"Which figure `required` is for this row. With `higherOfBoth`, the larger; with `forecastRequirement` and no handed-over requirement for the period, `minimum`."},"minimumRequired":{"type":"integer","nullable":true,"description":"The configured minimum for the position and window."},"forecastRequired":{"type":"number","nullable":true,"description":"The forecast staff requirement (p50) for the position and window, from `workforce.forecast_requirement`. Null where none was handed over."},"forecastRequiredP90":{"type":"number","nullable":true,"description":"The busy-case requirement, for planning to the busy case."},"forecastVersionId":{"type":"string","format":"uuid","nullable":true,"description":"The AI forecast version the requirement is bound to (AIP-067), so a manager can open the forecast behind it."}}},
"StaffingRules": {"type":"object","x-ticvai-persistence":"workforce.staffing_rules + workforce.position_requirement","description":"Resource board 4.3. **A safety rule before it is a cost rule.**","properties":{"minimumCover":{"type":"array","description":"**Minimum staffing per position, venue and time window, with the qualifications it requires**: the rows of `workforce.position_requirement` (data model for the agreed operations, 29 September). `getStaffingCoverage` measures the rota against them; before this they were an array with no table, so no minimum was stored.","items":{"type":"object","required":["id","positionCode","minimumHeadcount"],"properties":{"id":{"type":"string","format":"uuid"},"positionCode":{"type":"string"},"label":{"type":"string"},"venueId":{"type":"string","format":"uuid","nullable":true},"attractionId":{"type":"string","format":"uuid","nullable":true},"minimumHeadcount":{"type":"integer","minimum":0},"daysOfWeek":{"type":"array","nullable":true,"description":"Days the minimum applies; absent means every day the venue is open","items":{"type":"string","enum":["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]}},"startsAt":{"type":"string","nullable":true,"description":"Start of the time window, local time (HH:MM) as `ShiftTemplate.startsAt`; absent means opening"},"endsAt":{"type":"string","nullable":true,"description":"End of the time window, local time (HH:MM); absent means closing"},"requiredQualifications":{"type":"array","items":{"type":"string"}},"appliesWhenOpen":{"type":"boolean","default":true},"blocksOperation":{"type":"boolean","default":true,"description":"**A ride requiring two operators cannot run with one.** Where this is true the attraction closes rather than running short.\n"}}}},"maximumHoursPerDay":{"type":"integer","nullable":true},"maximumHoursPerWeek":{"type":"integer","nullable":true},"minimumRestHours":{"type":"integer","nullable":true},"maximumConsecutiveDays":{"type":"integer","nullable":true},"overtime":{"type":"object","properties":{"allowed":{"type":"boolean","default":true},"afterHoursPerWeek":{"type":"integer","nullable":true},"rateMultiplier":{"type":"number","nullable":true},"requiresApproval":{"type":"boolean","default":true}}},"minimumAgeForNightShift":{"type":"integer","nullable":true},"defaultIncentiveRateMultiplier":{"type":"number","nullable":true,"minimum":1,"description":"**What an open shift pays above base when it is released.** Added 22 September: `workforce.open_shift.incentive_rate_multiplier` was set per shift with nothing behind it, so two identical shifts could price differently and record no reason. The shift still carries its own value — **as the snapshot**, the rule-and-record split `payments.fee_rule` and `orders.order_fee` use — and this is where it comes from.\n**Top-level rather than beside `overtime`** so the value is its own column. Nested in an object it would be a key inside a JSON blob, which nothing can index, constrain or pair to the shift that uses it.\n"},"maximumIncentiveRateMultiplier":{"type":"number","nullable":true,"minimum":1,"description":"**The ceiling on an incentive.** A shift nobody claims is the moment somebody raises the multiplier in a hurry — the same reason `maximumDailyCharge` bounds a late fee."},"incentiveApprovalAbove":{"type":"number","nullable":true,"minimum":1,"description":"**Above this multiplier a second person approves the release.** Routed as an approval, not a boolean — `overtime.requiresApproval` beside it is one of 26 approval flags across the contracts that no approval kind, matrix row or SLA reaches."},"scopePath":{"type":"string"}}},
"WorkforceComplianceFinding": {"type":"object","description":"Resource board 4.8. **Checked before the rota is published, not in an inspection.**","properties":{"code":{"type":"string","enum":["expiredQualification","missingQualification","exceededDailyHours","exceededWeeklyHours","insufficientRest","missedBreak","consecutiveDaysExceeded","underAgeNightShift","belowMinimumCover"]},"severity":{"type":"string","enum":["breach","warning"]},"principalId":{"type":"string","format":"uuid","nullable":true},"principalName":{"type":"string","nullable":true},"date":{"type":"string","format":"date","nullable":true},"detail":{"type":"string"},"rotaAssignmentIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}
}
```
