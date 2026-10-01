# WS156 — Resource Management Configuration board 2

**9 screens · 14 operations · 10 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `RESOURCE_BOOK, RESOURCE_CONFIGURE, RESOURCE_MANAGE, RESOURCE_VIEW`. A control nobody can use must say so,
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
| `BO-864` | Resource Calendar Command Center | B–D | 0 | 10 | 6 | 0 | 3 | 0 | — | notStarted (—) |
| `BO-865` | Calendar Filters, Search & Smart Discovery | B–D | 2 | 0 | 6 | 3 | 1 | 0 | — | notStarted (—) |
| `BO-866` | Resource Availability Schedule Configuration | A | 30 | 2 | 6 | 47 | 1 | 0 | — | notStarted (—) |
| `BO-867` | Resource Time-Slot Configuration | B–D | 13 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `BO-868` | Advance Reservation Management | B–D | 26 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-869` | Recurring Reservation Configuration | B–D | 10 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-870` | Operational Time & Resource Blocking | A | 12 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-871` | Multi-Event Resource Planning | B–D | 0 | 18 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `BO-872` | Smart Assignment & Drag-and-Drop Reallocation | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-864, BO-865, BO-871, BO-872 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-864` Resource Calendar Command Center

**Provide the main operational calendar from which users can see and manage resource availability, reservations, assignments and operational blocks.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_BOOK`, `RESOURCE_MANAGE`, `RESOURCE_VIEW` (1 operate, 1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/resource-calendar-command-center-bo-864` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceCalendar` ?from |
| To | date and time picker | — | — | `getResourceCalendar` ?to |
| Resource type | picker: choose a resource type | — | — | `getResourceCalendar` ?resourceTypeId |
| Category | picker: choose a category | — | — | `getResourceCalendar` ?categoryId |
| Granularity | radio group | — | Day · Week · Month · Agenda | `getResourceCalendar` ?granularity |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Calendar** (calendar view, from `getResourceCalendar`): Every resource's bookings and blocks on one calendar. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Filters the category on what it read.

| Shows | Format | Notes |
|---|---|---|
| Resource | the name it points at, never the id | — |
| Resource name | text | — |
| Resource type | the name it points at, never the id | — |
| Utilisation percent | 1,234.5 | — |
| Segments | list or chips (count when long) | — |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| State | chip: Available, Reserved, Assigned, Partially utilised, Fully utilised, Unavailable… | — |
| Booking | the name it points at, never the id | — |
| Conflicts with | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getResourceCalendar` (onLoad, Every resource against time)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-865` Calendar Filters, Search & Smart Discovery: *Calendar Filters, Search & Smart Discovery*
- → `BO-866` Resource Availability Schedule Configuration: *Resource Availability Schedule Configuration*; carries `resourceId`
- → `BO-867` Resource Time-Slot Configuration: *Resource Time-Slot Configuration*; carries `resourceId`
- → `BO-868` Advance Reservation Management: *Advance Reservation Management*; carries `bookingId`
- → `BO-869` Recurring Reservation Configuration: *Recurring Reservation Configuration*; carries `bookingId`
- → `BO-870` Operational Time & Resource Blocking: *Operational Time & Resource Blocking*
- → `BO-871` Multi-Event Resource Planning: *Multi-Event Resource Planning*
- → `BO-872` Smart Assignment & Drag-and-Drop Reallocation: *Smart Assignment & Drag-and-Drop Reallocation*; carries `bookingId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource calendar list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource calendar untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource calendar yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource calendar are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Bookings already exist in the window. They are listed, because blocking over a booked resource is sometimes right and must never be silent. (ResourceConflictProblem); 409 Conflicts, and the response names them with times. *"Not available"* on a resource a guest can see in front of them is not an answer. (ResourceConflictProblem) |

#### Permissions

- `getResourceCalendar` → `RESOURCE_VIEW` (read) · staff
- `bookResource` → `RESOURCE_BOOK` (operate) · staff
- `createResourceBlock` → `RESOURCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Resource calendar is an inquiry/planning screen showing availability by date range (e.g. which of 10 vehicles are free between a start and end time), filterable and searchable across resource types. Schedules set each resource's working pattern (e.g. Monday–Friday, off weekends). *(client request · MoM 26 Aug 2026, 4.3 Resource Calendar & Scheduling · DI-480)*
- Resource management command centre: calendar-based overview of all resources' booking status (e.g. an instructor booked for a lesson, date and time), filterable by resource type and venue, with a switchable revenue view; view by day, week, month or custom period (planner style). *(client request · MoM 26 Aug 2026, 4.1 Resource Management Overview · DI-475)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-864` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-864`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 2
- Flow F265 *Resource Management Configuration board 2: Resource Calendar Command Center*, step 1: Opens Resource Calendar Command Center → Provide the main operational calendar from which users can see and manage resource availability, reservations, assignments and operational blocks.
- Flow F265 *Resource Management Configuration board 2: Resource Calendar Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F265 *Resource Management Configuration board 2: Resource Calendar Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F265 *Resource Management Configuration board 2: Resource Calendar Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F265 *Resource Management Configuration board 2: Resource Calendar Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F265 *Resource Management Configuration board 2: Resource Calendar Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F265 *Resource Management Configuration board 2: Resource Calendar Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F265 *Resource Management Configuration board 2: Resource Calendar Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F265 branch at step 1 (expected): when Nothing has been set up on Resource Calendar Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F265 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-864?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-100`, `BO-865`, `BO-866`, `BO-867`, `BO-868`, `BO-869`, `BO-870`, `BO-871`, `BO-872`.
- [ ] Every gated control is gated: `RESOURCE_BOOK`, `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-865` Calendar Filters, Search & Smart Discovery

**Allow users to quickly locate the correct resource instead of manually searching through hundreds or thousands of resources.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/calendar-filters-search-smart-discovery-bo-865` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search calendar filters search | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by date range, time range, resource type, resource category, resource name, venue and 7 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceCalendar` ?from |
| To | date and time picker | — | — | `getResourceCalendar` ?to |
| Resource type | picker: choose a resource type | — | — | `getResourceCalendar` ?resourceTypeId |
| Category | picker: choose a category | — | — | `getResourceCalendar` ?categoryId |
| Granularity | radio group | — | Day · Week · Month · Agenda | `getResourceCalendar` ?granularity |

#### Outputs: what the screen shows and produces

**Data it reads**: `getResourceCalendar` (onLoad, The filtered grid)

**Where the user goes next**

- → `BO-864` Resource Calendar Command Center: *Back to Resource Calendar Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The calendar filters search list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the calendar filters search untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No calendar filters search yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the calendar filters search are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getResourceCalendar` → `RESOURCE_VIEW` (read) · staff
- `suggestResources` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.53 | AI shall recommend optimal resources. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 1.2.54 | AI shall recommend suitable staff based on skills and availability. | Ticketing Catalogue | CONTRACTED | `suggestResources` |
| 1.2.56 | AI shall propose alternatives for scheduling conflicts. | Ticketing Catalogue | CONTRACTED | `suggestResources` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resource calendar is an inquiry/planning screen showing availability by date range (e.g. which of 10 vehicles are free between a start and end time), filterable and searchable across resource types. Schedules set each resource's working pattern (e.g. Monday–Friday, off weekends). *(client request · MoM 26 Aug 2026, 4.3 Resource Calendar & Scheduling · DI-480)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-865` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-865`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 2
- Flow F265 *Resource Management Configuration board 2: Resource Calendar Command Center*, step 2: Works in Calendar Filters, Search & Smart Discovery → Allow users to quickly locate the correct resource instead of manually searching through hundreds or thousands of resources.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-865?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-864`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-866` Resource Availability Schedule Configuration

**Define the baseline schedule controlling when each resource can be used.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block A · ticket #20730 (APP-SETUP-BO-866) |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_MANAGE`, `RESOURCE_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure; Availability may be configured using) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/resource-availability-schedule-configuration-bo-866` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Available days | select field | — | — | — | — | — | — |
| Opening time | select field | — | — | — | — | — | — |
| Closing time | select field | — | — | — | — | — | — |
| Effective date | select field | — | — | — | — | — | — |
| Expiry date | select field | — | — | — | — | — | — |
| Time zone | select field | — | — | — | — | — | — |
| Seasonal availability | select field | — | — | — | — | — | — |
| Venue operating hours | select field | — | — | — | — | — | — |
| Resource-specific operating hours | select field | — | — | — | — | — | — |
| Public holidays | select field | — | — | — | — | — | — |
| Venue closures | select field | — | — | — | — | — | — |
| Maintenance periods | select field | — | — | — | — | — | — |
| Staff leave | select field | — | — | — | — | — | — |
| Training | select field | — | — | — | — | — | — |
| Private blocks | select field | — | — | — | — | — | — |
| Operational shutdowns | select field | — | — | — | — | — | — |
| Special events | select field | — | — | — | — | — | — |
| Inheritance | select field | — | — | — | — | — | — |
| Standard weekly schedules | select field | — | — | — | — | — | — |
| Specific dates | select field | — | — | — | — | — | — |
| Seasonal schedules | select field | — | — | — | — | — | — |
| Exception dates | select field | — | — | — | — | — | — |
| Imported schedules | select field | — | — | — | — | — | — |
| External workforce schedules | select field | — | — | — | — | — | — |
| Availability Exceptions | select field | — | — | — | — | — | — |
| Cleaning | segmented control | optional | — | After every booking · Times per day | — | **How the room is cleaned between uses** (decided 29 September, W10). *After every booking* blocks a fixed buffer after each booking (e.g. 15 minutes); *N times a day* lets the system place N … | `Resource.cleaningPolicy.mode` |
| Minutes per cleaning | number field (minutes) | optional | — | min 5; max 240 | — | Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct). | `Resource.cleaningPolicy.bufferMinutes` |
| Cleanings per day | stepper or slider | optional | — | min 1; max 24 | — | Shown for *N times a day* only. | `Resource.cleaningPolicy.cleaningsPerDay` |
| Cleaning window from | time picker | optional | — | — | HH:mm, 24-hour | Venue-local time the cleaning window opens. Null means the resource's opening time. | `Resource.cleaningPolicy.windowStart` |
| Cleaning window to | time picker | optional | — | — | HH:mm, 24-hour | Venue-local time the cleaning window closes. Null means the resource's closing time. | `Resource.cleaningPolicy.windowEnd` |

#### Outputs: what the screen shows and produces

**Shown**

**Day preview** (timeline, from `getResourceAvailability`): **A day preview before saving** (W10): bookings, holds and the cleanings the policy places, as `cleaning` blocked windows, so an operator sees what the policy takes out of availability.

| Shows | Format | Notes |
|---|---|---|
| Free windows | list or chips (count when long) | — |
| Blocked windows | list or chips (count when long) | With a reason, because they are not the same. Booked and under repair need different responses from an operator looking for something free … |

**Where the user goes next**

- → `BO-864` Resource Calendar Command Center: *Back to Resource Calendar Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource availability schedule configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource availability schedule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource availability schedule configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A `cleaningPolicy` with `timesPerDay` and no `cleaningsPerDay`, or whose window ends before it starts (W10, 29 September). |

#### Permissions

- `getResourceAvailability` → `RESOURCE_VIEW` (read) · staff, guest
- `updateResource` → `RESOURCE_MANAGE` (configure) · staff
- `getResourceSchedule` → `RESOURCE_VIEW` (read) · staff
- `setResourceSchedule` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

47 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.6 | The system should provide a calendar view for all the resources (e.g. instructors) and associated time slots (e.g. ski school session by an instructor). The calendar should support application of … | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.7 | The system should show the booked capacity of different time-slots to provide their availability. The capacity can be color-coded to indicate if not busy, moderately busy, or crowded within each … | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.13 | Using the calendar view, system should provide an drag and drop interface to reassign the resources from one resource to another available resources. System should automatically assign the next … | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.18 | Resource Calendar: Centralized calendar view (daily/weekly/monthly). | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.19 | Availability Management: Check conflicts before assigning resources. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.20 | Recurring Reservations: Block resources for repeated sessions/shows. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.21 | Time Slot Management: Allocate setup, event, teardown, and maintenance times. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.22 | Multi-event Handling: Manage shared resources across parallel events. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.27 | System shall provide centralized resource calendars. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.28 | System shall manage resource time slots and availability. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.29 | System shall manage availability and conflict detection. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| 1.2.30 | System shall support advance resource reservations. | Ticketing Catalogue | CONTRACTED | `getResourceAvailability` |
| … 35 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resource calendar is an inquiry/planning screen showing availability by date range (e.g. which of 10 vehicles are free between a start and end time), filterable and searchable across resource types. Schedules set each resource's working pattern (e.g. Monday–Friday, off weekends). *(client request · MoM 26 Aug 2026, 4.3 Resource Calendar & Scheduling · DI-480)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-866` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-866`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 2
- Flow F265 *Resource Management Configuration board 2: Resource Calendar Command Center*, step 4: Works in Resource Availability Schedule Configuration → Define the baseline schedule controlling when each resource can be used.

#### Acceptance for the design

- [ ] Every input above is drawn (30), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-866?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-864`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-867` Resource Time-Slot Configuration

**Control how available resource time is converted into reservable or assignable time slots.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/resource-time-slot-configuration-bo-867` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Slot duration | select field | — | — | — | — | — | — |
| Slot interval | select field | — | — | — | — | — | — |
| Start time | select field | — | — | — | — | — | — |
| End time | select field | — | — | — | — | — | — |
| Minimum duration | select field | — | — | — | — | — | — |
| Maximum duration | select field | — | — | — | — | — | — |
| Booking increments | select field | — | — | — | — | — | — |
| Buffer before | select field | — | — | — | — | — | — |
| Buffer after | select field | — | — | — | — | — | — |
| Capacity per slot | select field | — | — | — | — | — | — |
| Concurrent reservations | select field | — | — | — | — | — | — |
| Minimum notice | select field | — | — | — | — | — | — |
| Maximum advance booking period | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-864` Resource Calendar Command Center: *Back to Resource Calendar Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource time-slot configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource time-slot untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource time-slot configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setResourceSchedule` → `RESOURCE_CONFIGURE` (configure) · staff
- `getResourceSchedule` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.59 | Users shall manage resources through conversational AI commands. | Ticketing Catalogue | CONTRACTED | `setResourceSchedule` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Clarified: time slots are not created for resources; they are created for performances/events, and resources are associated with those performance time slots. *(agreed · MoM 26 Aug 2026, 4.3 Resource Calendar & Scheduling · DI-481)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-867` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-867`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 2
- Flow F265 *Resource Management Configuration board 2: Resource Calendar Command Center*, step 6: Works in Resource Time-Slot Configuration → Control how available resource time is converted into reservable or assignable time slots.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-867?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-864`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-868` Advance Reservation Management

**Allow resources to be reserved before final operational assignment or ticket transaction.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_BOOK`, `RESOURCE_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Users shall configure; Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/advance-reservation-management-bo-868` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Reservation reference | select field | — | — | — | — | — | — |
| Resource | select field | — | — | — | — | — | — |
| Resource type | select field | — | — | — | — | — | — |
| Date | select field | — | — | — | — | — | — |
| Start time | select field | — | — | — | — | — | — |
| End time | select field | — | — | — | — | — | — |
| Customer/event/experience | select field | — | — | — | — | — | — |
| Quantity | select field | — | — | — | — | — | — |
| Capacity | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |
| Reservation status | select field | — | — | — | — | — | — |
| Expiry | select field | — | — | — | — | — | — |
| Notes | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |
| Reservation States | select field | — | — | — | — | — | — |
| Hold duration | select field | — | — | — | — | — | — |
| Automatic expiry | select field | — | — | — | — | — | — |
| Extension permissions | select field | — | — | — | — | — | — |
| Release rules | select field | — | — | — | — | — | — |
| Smart Availability | select field | — | — | — | — | — | — |
| Availability | select field | — | — | — | — | — | — |
| Existing bookings | select field | — | — | — | — | — | — |
| Dependencies | select field | — | — | — | — | — | — |
| Venue restrictions | select field | — | — | — | — | — | — |
| Resource status | select field | — | — | — | — | — | — |
| Operational blocks | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Resource | picker: choose a resource | — | — | `listResourceBookings` ?resourceId |
| From | date and time picker | — | — | `listResourceBookings` ?from |
| To | date and time picker | — | — | `listResourceBookings` ?to |
| Status | select | — | Reserved · Checked out · Returned · Overdue · Cancelled · No show | `listResourceBookings` ?status |

#### Outputs: what the screen shows and produces

**Data it reads**: `listResourceBookings` (onLoad, Reservations ahead)

**Where the user goes next**

- → `BO-864` Resource Calendar Command Center: *Back to Resource Calendar Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The advance reservation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the advance reservation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No advance reservation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Conflicts, and the response names them with times. *"Not available"* on a resource a guest can see in front of them is not an answer. (ResourceConflictProblem); 409 The change conflicts; the response names the times (ResourceConflictProblem) |

#### Permissions

- `listResourceBookings` → `RESOURCE_VIEW` (read) · staff
- `bookResource` → `RESOURCE_BOOK` (operate) · staff
- `updateResourceBooking` → `RESOURCE_BOOK` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resources are normally booked automatically as a consequence of selling the associated package; manually reserving/blocking a specific resource outside a sale is only for exceptional cases (e.g. holding it for a future booking). *(agreed · MoM 26 Aug 2026, 4.4 Resource Assignment Models · DI-483)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-868` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-868`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 2
- Flow F265 *Resource Management Configuration board 2: Resource Calendar Command Center*, step 8: Works in Advance Reservation Management → Allow resources to be reserved before final operational assignment or ticket transaction.

#### Acceptance for the design

- [ ] Every input above is drawn (26), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-868?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-864`.
- [ ] Every gated control is gated: `RESOURCE_BOOK`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-869` Recurring Reservation Configuration

**Allow resources to be reserved repeatedly without creating each reservation individually.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_BOOK` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Users shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/recurring-reservation-configuration-bo-869` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Start date | select field | — | — | — | — | — | — |
| End date | select field | — | — | — | — | — | — |
| Frequency | select field | — | — | — | — | — | — |
| Days | select field | — | — | — | — | — | — |
| Times | select field | — | — | — | — | — | — |
| Number of occurrences | select field | — | — | — | — | — | — |
| Resource | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Exceptions | select field | — | — | — | — | — | — |
| Conflict Handling | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Selected weekdays (primary button) | navigation or local | — | — | — | — |
| Selected dates (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-864` Resource Calendar Command Center: *Back to Resource Calendar Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recurring reservation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recurring reservation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recurring reservation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Conflicts, and the response names them with times. *"Not available"* on a resource a guest can see in front of them is not an answer. (ResourceConflictProblem) |

#### Permissions

- `bookResource` → `RESOURCE_BOOK` (operate) · staff
- `cancelResourceBooking` → `RESOURCE_BOOK` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-869` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-869`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 2
- Flow F265 *Resource Management Configuration board 2: Resource Calendar Command Center*, step 10: Works in Recurring Reservation Configuration → Allow resources to be reserved repeatedly without creating each reservation individually.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-869?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Selected weekdays, Selected dates.
- [ ] Every transition is wired: `BO-864`.
- [ ] Every gated control is gated: `RESOURCE_BOOK`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-870` Operational Time & Resource Blocking

**Protect non-customer-facing time required for preparation, movement, maintenance and operational activities.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block A · ticket #20710 (APP-SETUP-BO-870) |
| Who uses it | venue staff holding `RESOURCE_MANAGE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Users shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `blockId` (navigation) |
| Route | `/rentals/operational-time-resource-blocking-bo-870` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Setup | select field | — | — | — | — | — | — |
| Teardown | select field | — | — | — | — | — | — |
| Cleaning | select field | — | — | — | — | — | — |
| Maintenance | select field | — | — | — | — | — | — |
| Inspection | select field | — | — | — | — | — | — |
| Travel | select field | — | — | — | — | — | — |
| Break | select field | — | — | — | — | — | — |
| Training | select field | — | — | — | — | — | — |
| Private use | select field | — | — | — | — | — | — |
| Venue closure | select field | — | — | — | — | — | — |
| Operational hold | select field | — | — | — | — | — | — |
| Custom block | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Resource | picker: choose a resource | — | — | `listResourceBlocks` ?resourceId |
| From | date and time picker | — | — | `listResourceBlocks` ?from |
| To | date and time picker | — | — | `listResourceBlocks` ?to |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listResourceBlocks` (onLoad, Blocks in force)

**Where the user goes next**

- → `BO-864` Resource Calendar Command Center: *Back to Resource Calendar Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operational time resource configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operational time resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operational time resource configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Bookings already exist in the window. They are listed, because blocking over a booked resource is sometimes right and must never be silent. (ResourceConflictProblem) |

#### Permissions

- `listResourceBlocks` → `RESOURCE_VIEW` (read) · staff
- `createResourceBlock` → `RESOURCE_MANAGE` (configure) · staff
- `releaseResourceBlock` → `RESOURCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resources are normally booked automatically as a consequence of selling the associated package; manually reserving/blocking a specific resource outside a sale is only for exceptional cases (e.g. holding it for a future booking). *(agreed · MoM 26 Aug 2026, 4.4 Resource Assignment Models · DI-483)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-870` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-870`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 2
- Flow F265 *Resource Management Configuration board 2: Resource Calendar Command Center*, step 12: Works in Operational Time & Resource Blocking → Protect non-customer-facing time required for preparation, movement, maintenance and operational activities.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-870?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: What publishing changes.
- [ ] Every transition is wired: `BO-864`.
- [ ] Every gated control is gated: `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-871` Multi-Event Resource Planning

**Allow operations teams to manage shared resources across multiple simultaneous events, experiences and operational activities.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_BOOK`, `RESOURCE_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§The screen shall display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/multi-event-resource-planning-bo-871` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceCalendar` ?from |
| To | date and time picker | — | — | `getResourceCalendar` ?to |
| Resource type | picker: choose a resource type | — | — | `getResourceCalendar` ?resourceTypeId |
| Category | picker: choose a category | — | — | `getResourceCalendar` ?categoryId |
| Granularity | radio group | — | Day · Week · Month · Agenda | `getResourceCalendar` ?granularity |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every multi-event resource planning** (data table)

| Shows | Format | Notes |
|---|---|---|
| Events | text | not in the schema: `Events` |
| Experiences | text | not in the schema: `Experiences` |
| Resources | text | not in the schema: `Resources` |
| Venues | text | not in the schema: `Venues` |
| Time periods | text | not in the schema: `Time periods` |
| Assignments | text | not in the schema: `Assignments` |
| Conflicts | text | not in the schema: `Conflicts` |
| Capacity | text | not in the schema: `Capacity` |
| Resource gaps | text | not in the schema: `Resource gaps` |

**The selected multi-event resource planning** (detail panel): The pack groups this record's detail under its own headings: “Event A”, “Event B”, “Events may be assigned”, “Resource allocation can consider”.

| Shows | Format | Notes |
|---|---|---|
| Events | text | not in the schema: `Events` |
| Experiences | text | not in the schema: `Experiences` |
| Resources | text | not in the schema: `Resources` |
| Venues | text | not in the schema: `Venues` |
| Time periods | text | not in the schema: `Time periods` |
| Assignments | text | not in the schema: `Assignments` |
| Conflicts | text | not in the schema: `Conflicts` |
| Capacity | text | not in the schema: `Capacity` |
| Resource gaps | text | not in the schema: `Resource gaps` |

**Data it reads**: `getResourceCalendar` (onLoad, Several events at once)

**Where the user goes next**

- → `BO-864` Resource Calendar Command Center: *Back to Resource Calendar Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-event resource planning list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-event resource planning untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-event resource planning yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the multi-event resource planning are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Nothing available, or a dependency is missing. Both are named — "no instructor free" and "the stage has no sound system" need different actions from the person … (ResourceAllocationProblem) |

#### Permissions

- `getResourceCalendar` → `RESOURCE_VIEW` (read) · staff
- `allocateResources` → `RESOURCE_BOOK` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.57 | AI shall optimize schedules automatically. | Ticketing Catalogue | CONTRACTED_PARTIAL | `allocateResources` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The system must prevent the same resource being double-booked or assigned to overlapping bookings (conflict detection and resolution). Multi-event planning and drag-and-drop allocation assign resources visually, alongside rule-based automatic assignment. *(agreed · MoM 26 Aug 2026, 4.4 Resource Assignment Models · DI-484)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-871` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-871`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 2
- Flow F265 *Resource Management Configuration board 2: Resource Calendar Command Center*, step 14: Works in Multi-Event Resource Planning → Allow operations teams to manage shared resources across multiple simultaneous events, experiences and operational activities.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-871?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-864`.
- [ ] Every gated control is gated: `RESOURCE_BOOK`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-872` Smart Assignment & Drag-and-Drop Reallocation

**Provide the fast, visual assignment experience that operational users and cashiers can use when assigning or changing resources. This should become one of the signature TICVAI Resource Management experiences. Provide TICVAI with a centralized backend configuration environment for treating employees, instructors, contractors, technicians, security personnel, event staff, and other personnel as intelligent operational resources.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_BOOK`, `RESOURCE_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/smart-assignment-drag-and-drop-reallocation-bo-872` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceCalendar` ?from |
| To | date and time picker | — | — | `getResourceCalendar` ?to |
| Resource type | picker: choose a resource type | — | — | `getResourceCalendar` ?resourceTypeId |
| Category | picker: choose a category | — | — | `getResourceCalendar` ?categoryId |
| Granularity | radio group | — | Day · Week · Month · Agenda | `getResourceCalendar` ?granularity |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save resource booking (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getResourceCalendar` (onLoad, The grid being dragged on)

**Where the user goes next**

- → `BO-864` Resource Calendar Command Center: *Back to Resource Calendar Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The smart drag-and-drop reallocation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the smart drag-and-drop reallocation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No smart drag-and-drop reallocation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the smart drag-and-drop reallocation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The change conflicts; the response names the times (ResourceConflictProblem) |

#### Permissions

- `updateResourceBooking` → `RESOURCE_BOOK` (operate) · staff
- `getResourceCalendar` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The system must prevent the same resource being double-booked or assigned to overlapping bookings (conflict detection and resolution). Multi-event planning and drag-and-drop allocation assign resources visually, alongside rule-based automatic assignment. *(agreed · MoM 26 Aug 2026, 4.4 Resource Assignment Models · DI-484)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-872` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS127 Resource Management Configuration Board 2.dc.html#bo-872`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 2
- Flow F265 *Resource Management Configuration board 2: Resource Calendar Command Center*, step 16: Works in Smart Assignment & Drag-and-Drop Reallocation → Provide the fast, visual assignment experience that operational users and cashiers can use when assigning or changing resources. This should become one of the signature TICVAI Resource Management …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-872?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save resource booking, Cancel.
- [ ] Every transition is wired: `BO-864`.
- [ ] Every gated control is gated: `RESOURCE_BOOK`, `RESOURCE_VIEW`.
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

**10 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"allocateResources": {"method":"POST","path":"/resource-allocations","contract":"resources","summary":"Fill a requirement from the pool, rotating rather than repeating","permission":"RESOURCE_BOOK","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceBooking"},
"bookResource": {"method":"POST","path":"/resource-bookings","contract":"resources","summary":"Reserve a specific resource for a window — staff only","permission":"RESOURCE_BOOK","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceBooking"},
"cancelResourceBooking": {"method":"DELETE","path":"/resource-bookings/{bookingId}","contract":"resources","summary":"Cancel one occurrence, or the whole series","permission":"RESOURCE_BOOK","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"scope","in":"query","required":true},{"name":"reason","in":"query","required":null}],"requestBody":null,"responds":"ResourceBooking"},
"createResourceBlock": {"method":"POST","path":"/resource-blocks","contract":"resources","summary":"Take a resource out of service for a window, with a reason","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceBlock","responds":"ResourceBlock"},
"getResourceAvailability": {"method":"GET","path":"/resources/{resourceId}/availability","contract":"resources","summary":"When it is free, with conflicts already resolved","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true}],"requestBody":null,"responds":"ResourceAvailability"},
"getResourceCalendar": {"method":"GET","path":"/resource-calendar","contract":"resources","summary":"Every resource against time, with conflicts already marked","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"resourceTypeId","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"granularity","in":"query","required":null}],"requestBody":null,"responds":"ResourceCalendarRow"},
"getResourceSchedule": {"method":"GET","path":"/resources/{resourceId}/schedule","contract":"resources","summary":"The pattern of when it is normally available","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceSchedule"},
"listResourceBlocks": {"method":"GET","path":"/resource-blocks","contract":"resources","summary":"Operational, setup and maintenance blocks","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"resourceId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"ResourceBlock"},
"listResourceBookings": {"method":"GET","path":"/resource-bookings","contract":"resources","summary":"Bookings, filtered","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"resourceId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"ResourceBooking"},
"releaseResourceBlock": {"method":"DELETE","path":"/resource-blocks/{blockId}","contract":"resources","summary":"Put it back into service","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setResourceSchedule": {"method":"PUT","path":"/resources/{resourceId}/schedule","contract":"resources","summary":"Operating hours, working pattern and bookable slots","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"ResourceSchedule","responds":"ResourceSchedule"},
"suggestResources": {"method":"GET","path":"/resource-suggestions","contract":"resources","summary":"Resources matching a requirement, by attribute","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"resourceTypeId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"attributes","in":"query","required":null}],"requestBody":null,"responds":"Resource"},
"updateResource": {"method":"PUT","path":"/resources/{resourceId}","contract":"resources","summary":"Change a resource","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Resource","responds":"Resource"},
"updateResourceBooking": {"method":"PATCH","path":"/resource-bookings/{bookingId}","contract":"resources","summary":"Extend, shorten or reassign a booking","permission":"RESOURCE_BOOK","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceBooking"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Resource": {"type":"object","x-ticvai-persistence":"resources.resource","description":"**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n","required":["id","code","name","kind","venueId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"$ref":"#/components/schemas/ResourceKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentResourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"},"attributes":{"type":"object","additionalProperties":true,"description":"Configurable per kind — capacity, size, shade, power, poolside."},"setupMinutes":{"type":"integer","default":0,"description":"**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"},"teardownMinutes":{"type":"integer","default":0,"description":"After the booking. **Kept as it is** (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added after the teardown, so a room with no teardown and a 15-minute clean is free 15 minutes after each booking ends.\n"},"cleaningPolicy":{"allOf":[{"$ref":"#/components/schemas/ResourceCleaningPolicy"}],"nullable":true,"description":"How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`."},"requiresQualification":{"type":"array","items":{"type":"string"},"description":"Qualification codes a person must hold to be assigned to this."},"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["available","booked","checkedOut","maintenance","retired"]},"isActive":{"type":"boolean","default":true}}},
"ResourceAvailability": {"type":"object","description":"**Free windows, with setup and teardown already subtracted.** A client computing this from bookings will forget the turnaround.\n","properties":{"resourceId":{"type":"string","format":"uuid"},"freeWindows":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"}}}},"blockedWindows":{"type":"array","description":"**With a reason, because they are not the same.** Booked and under repair need different responses from an operator looking for something free — wait, or look elsewhere.\n","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"reason":{"type":"string","enum":["booked","held","setup","teardown","maintenance","blackout","closed","cleaning"],"description":"`held` is a live `ResourceHold` (rev 3 REV3-15): taken now, free again if it expires. `cleaning` is a cleaning the resource's `cleaningPolicy` places (W10, 29 September).\n"}}}}}},
"ResourceBlock": {"type":"object","x-ticvai-persistence":"resources.resource_block","description":"Board 2.07. **A block is not a booking**, and the reason travels with it so an operator knows whether to wait or to look elsewhere.\n","required":["resourceId","from","to","reason"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid"},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"reason":{"type":"string","enum":["setup","teardown","maintenance","blackout","closed","operational","training"]},"note":{"type":"string","nullable":true},"createdBy":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"ResourceBooking": {"type":"object","x-ticvai-persistence":"resources.booking","required":["id","resourceId","from","to","status"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"status":{"$ref":"#/components/schemas/ResourceBookingStatus"},"holdId":{"type":"string","format":"uuid","nullable":true,"description":"The `ResourceHold` this booking was converted from, where a guest picked the resource on a venue map (rev 3 REV3-15). Null for a staff booking or an allocation.\n"},"recurrenceGroupId":{"type":"string","format":"uuid","nullable":true,"description":"Ties the occurrences of a recurring booking. **Cancelling one week does not cancel the series**, and cancelling the series is a separate act with a separate confirmation.\n"},"depositAuthorisationId":{"type":"string","format":"uuid","nullable":true,"description":"The hold, through `orders.authoriseStoredValue` (CF-126). **A deposit taken and refunded is two transactions and a fee; held and released is neither.**\n"},"checkedOutAt":{"type":"string","format":"date-time","nullable":true},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"returnedAt":{"type":"string","format":"date-time","nullable":true},"conditionOut":{"type":"string","nullable":true},"conditionIn":{"type":"string","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the latest offline check-out or check-in write reached the server. **The device times are `checkedOutAt` and `returnedAt`**, taken from each write's `recordedAt`; this is the server's half of the pair naming-and-style 5.2 requires. Null while pending.\n"}}},
"ResourceBookingStatus": {"type":"string","enum":["reserved","checkedOut","returned","overdue","cancelled","noShow"]},
"ResourceCalendarRow": {"type":"object","description":"Board 2.01. **One resource across the window, with its states already computed** — including conflict, which a client cannot derive from a booking list.\n","properties":{"resourceId":{"type":"string","format":"uuid"},"resourceName":{"type":"string"},"resourceTypeId":{"type":"string","format":"uuid"},"utilisationPercent":{"type":"number"},"segments":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"state":{"type":"string","enum":["available","reserved","assigned","partiallyUtilised","fullyUtilised","unavailable","onBreak","onLeave","underMaintenance","operationallyBlocked","pendingApproval","conflict"]},"bookingId":{"type":"string","format":"uuid","nullable":true},"conflictsWith":{"type":"array","items":{"type":"string","format":"uuid"}}}}}}},
"ResourceCleaningPolicy": {"x-ticvai-persistence":"none — columns on resources.resource","type":"object","description":"**When the resource is cleaned, and what that takes out of availability** (decided 29 September, W10; the meeting-room case from the 29 September website review).\n- `afterEveryBooking` (option A): `bufferMinutes` blocked after every booking, after its teardown. - `timesPerDay` (option B): `cleaningsPerDay` cleanings of `bufferMinutes` each, between `windowStart` and `windowEnd`, **placed by the system**. The targets are spread evenly across the window; each is put in the free gap nearest its target that is long enough, and never on a booking, a hold or a block. **A confirmed booking is never moved for a cleaning.** Placement is computed on read from the day's bookings, so it moves when bookings change, and a start time is offered only if every cleaning of that day can still be placed after it is booked.\n`createResource` and `updateResource` refuse a policy with `timesPerDay` and no `cleaningsPerDay`, or a window that ends before it starts, with `422`.\n","required":["mode","bufferMinutes"],"properties":{"mode":{"type":"string","enum":["afterEveryBooking","timesPerDay"]},"bufferMinutes":{"type":"integer","minimum":5,"maximum":240,"description":"Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct)."},"cleaningsPerDay":{"type":"integer","minimum":1,"maximum":24,"nullable":true,"description":"Required for `timesPerDay`; ignored for `afterEveryBooking`."},"windowStart":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window opens. Null means the resource's opening time."},"windowEnd":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window closes. Null means the resource's closing time."}}},
"ResourceKind": {"type":"string","description":"BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n","enum":["cabana","lounger","locker","wheelchair","stroller","equipment","room","auditorium","vehicle","instructor","staff","table","pitch","studio","other"],"x-ticvai-refuses":{"mealPlan":"**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."}},
"ResourceRequirement": {"type":"object","x-ticvai-persistence":"resources.resource_requirement","description":"**A type and a quantity, never a named resource.** This is what makes the 26 August rule enforceable — the product states what it needs and the platform decides which one.\nFor resources placed on a published venue map the rule is superseded (decided 29 September, rev 3 REV3-15): the guest names the resource through a `ResourceHold`, and no requirement is needed.\n","required":["quantity"],"properties":{"id":{"type":"string","format":"uuid"},"resourceTypeId":{"type":"string","format":"uuid","nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"resourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A fixed component, and the exception rather than the rule.** Meeting Room A really is Meeting Room A; the technician is not.\n"},"quantity":{"type":"integer","default":1},"mandatory":{"type":"boolean","default":true},"requiredQualifications":{"type":"array","items":{"type":"string"}},"requiredAttributes":{"type":"object","additionalProperties":true},"substituteResourceIds":{"type":"array","items":{"type":"string","format":"uuid"}},"scopePath":{"type":"string"}}},
"ResourceSchedule": {"type":"object","x-ticvai-persistence":"resources.resource_schedule","description":"Boards 2.03 and 2.04. **A recurring pattern with exceptions, not a list of dates.** A schedule written as concrete dates silently expires.\n","properties":{"resourceId":{"type":"string","format":"uuid"},"availabilityMode":{"type":"string","enum":["alwaysAvailable","scheduled","onRequest"]},"windows":{"type":"array","items":{"type":"object","properties":{"daysOfWeek":{"type":"array","items":{"type":"string"}},"from":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Local time of day, HH:MM."},"to":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Local time of day, HH:MM."},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true}}}},"slotMinutes":{"type":"integer","nullable":true,"description":"**How finely this resource's time can be cut**, which is a property of the resource and not of the product sold against it.\n"},"minimumBookingMinutes":{"type":"integer","nullable":true},"maximumBookingMinutes":{"type":"integer","nullable":true},"advanceBookingDays":{"type":"integer","nullable":true},"exceptions":{"type":"array","items":{"type":"object","properties":{"date":{"type":"string","format":"date"},"closed":{"type":"boolean"},"from":{"type":"string","nullable":true,"pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Local time of day, HH:MM."},"to":{"type":"string","nullable":true,"pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Local time of day, HH:MM."}}}},"scopePath":{"type":"string"}}}
}
```
