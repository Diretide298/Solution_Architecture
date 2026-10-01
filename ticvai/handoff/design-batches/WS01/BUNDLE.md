# WS01 — Access Control board 1

**10 screens · 19 operations · 29 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `ACCESS_POINT_CONFIGURE, SCOPE_MANAGE, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-144` | Access Control Command Center | B–D | 0 | 30 | 6 | 2 | 2 | 0 | — | notStarted (generated) |
| `BO-145` | Venue & Park Access Structure | B–D | 0 | 0 | 6 | 6 | 0 | 0 | — | notStarted (generated) |
| `BO-146` | Access Area & Zone Builder | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-147` | Attraction Access Configuration | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-148` | Access Point Directory | B–D | 6 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-149` | Gate & Lane Configuration | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-150` | Access Control Graphical Map Designer | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-151` | Access Location Grouping | A | 6 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-152` | Operating Calendar & Special Access Days | B–D | 21 | 7 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-153` | Topology Validation & Publication | B–D | 1 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-144, BO-145, BO-146, BO-147, BO-149, BO-150, BO-151, BO-153 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-144` Access Control Command Center

**Central operational/configuration landing page for the complete Access Control module.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Dashboard should show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/access-control-command-center-bo-144` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every access** (data table, from `listAccess`)

| Shows | Format | Notes |
|---|---|---|
| Total venues | 1,234 | Total venues |
| Active access points | 1,234 | Active access points |
| Entry gates | 1,234 | Entry gates |
| Exit gates | 1,234 | Exit gates |
| Attraction gates | 1,234 | Attraction gates |
| Turnstiles | 1,234 | Turnstiles |
| Handheld devices | 1,234 | Handheld devices |
| Devices online/offline | text | not in the schema: `Devices online/offline` |
| Gates open/closed | text | not in the schema: `Gates open/closed` |
| Current in venue occupancy | 1,234 | Current in-venue occupancy |
| Current admission rate | 12.5% | Admissions per minute across the estate |
| Failed scans | 1,234 | Failed scans |
| Overrides | 1,234 | Overrides |
| Security alerts | 1,234 | Security alerts |
| Synchronization status | chip: In sync, Sync pending, Sync failed | Estate-wide offline sync state of devices |

**The selected access** (detail panel): The pack groups this record's detail under its own headings: “Display hierarchy such as”.

| Shows | Format | Notes |
|---|---|---|
| Total venues | 1,234 | Total venues |
| Active access points | 1,234 | Active access points |
| Entry gates | 1,234 | Entry gates |
| Exit gates | 1,234 | Exit gates |
| Attraction gates | 1,234 | Attraction gates |
| Turnstiles | 1,234 | Turnstiles |
| Handheld devices | 1,234 | Handheld devices |
| Devices online/offline | text | not in the schema: `Devices online/offline` |
| Gates open/closed | text | not in the schema: `Gates open/closed` |
| Current in venue occupancy | 1,234 | Current in-venue occupancy |
| Current admission rate | 12.5% | Admissions per minute across the estate |
| Failed scans | 1,234 | Failed scans |
| Overrides | 1,234 | Overrides |
| Security alerts | 1,234 | Security alerts |
| Synchronization status | chip: In sync, Sync pending, Sync failed | Estate-wide offline sync state of devices |

**Data it reads**: `listAccess` (onLoad, Access Control Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-145` Venue & Park Access Structure: *Works in Venue & Park Access Structure*; calls `listAccess`
- → `BO-146` Access Area & Zone Builder: *Works in Access Area & Zone Builder*; calls `listAccess`
- → `BO-147` Attraction Access Configuration: *Works in Attraction Access Configuration*; calls `listAccess`
- → `BO-148` Access Point Directory: *Works in Access Point Directory*; calls `listAccess`
- → `BO-149` Gate & Lane Configuration: *Works in Gate & Lane Configuration*; calls `listAccess`
- → `BO-150` Access Control Graphical Map Designer: *Works in Access Control Graphical Map Designer*; calls `listAccess`
- → `BO-151` Access Location Grouping: *Works in Access Location Grouping*; calls `listAccess`
- → `BO-152` Operating Calendar & Special Access Days: *Works in Operating Calendar & Special Access Days*; calls `listAccess`
- → `BO-153` Topology Validation & Publication: *Works in Topology Validation & Publication*; calls `listAccess`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listAccess` → `SCOPE_VIEW` (read) · staff
- `createAccessPoint` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.60 | Check-in / Check-out entitlement control | Ticketing Catalogue | CONTRACTED | `createAccessPoint` |
| 3.2.11 | The system should be able to define and configure all access control rules, all gates (entrances of access-control areas), access points and locations (a group of areas). | Admission and Access | CONTRACTED | `createAccessPoint` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Venue-wide attendance overview (open/closed gates, offline/maintenance status, graphed) and a visual map of all access-control locations across venues/tenants, including entry and exit turnstile layouts that vary by venue. *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-623)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-144` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-144`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 1: Opens Access Control Command Center → Central operational/configuration landing page for the complete Access Control module.
- Flow F111 *Access Control board 1: Access Control Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F111 *Access Control board 1: Access Control Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F111 *Access Control board 1: Access Control Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F111 *Access Control board 1: Access Control Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F111 *Access Control board 1: Access Control Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F111 *Access Control board 1: Access Control Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F111 *Access Control board 1: Access Control Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F111 branch at step 1 (expected): when Nothing has been set up on Access Control Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F111 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-144?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-145`, `BO-146`, `BO-147`, `BO-148`, `BO-149`, `BO-150`, `BO-151`, `BO-152`, `BO-153`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-145` Venue & Park Access Structure

**Define the highest-level physical access hierarchy.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_MANAGE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `orgUnitId` (navigation) |
| Route | `/access-venue/venue-park-access-structure-bo-145` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Under | text field | — | — | `listOrgUnits` ?under |
| Level | select | — | Tenant · Brand · Region · Venue · Department · Sub department · Workstation · Outlet · Subject | `listOrgUnits` ?level |
| Include inactive | toggle | off | — | `listOrgUnits` ?includeInactive |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create org unit (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listVenueParkAccess` (onLoad, Venue & Park Access Structure); `listOrgUnits` (onLoad, The venue, park and zone tree the access structure hangs …)

**Where the user goes next**

- → `BO-144` Access Control Command Center: *Returns to the board's landing screen*; calls `listVenueParkAccess`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue park access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue park access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue park access yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the venue park access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types. |

#### Permissions

- `listVenueParkAccess` → `SCOPE_VIEW` (read) · staff
- `listOrgUnits` → `SCOPE_VIEW` (read) · staff
- `createOrgUnit` → `SCOPE_MANAGE` (configure) · staff
- `updateOrgUnit` → `SCOPE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.41 | Venue-Specific Policies - System shall support venue-specific access policies. | Admission and Access | CONTRACTED | `listOrgUnits` |
| 3.3.43 | Policy Inheritance - System shall support inheritance of policies across organizational structures. | Admission and Access | CONTRACTED | `listOrgUnits` |
| 7.1.13 | The system shall support permission assignment at company, department, venue, park, attraction, facility, event, sales channel, POS terminal, and product levels. | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.27 | The system shall support management of companies, business units, departments, parks, venues, attractions, facilities, cost centers, and reporting structures. | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.37 | Allow administrators to restrict access by venue, park, facility, attraction, sales channel, POS terminal, country, region, IP address and network range. Policies should support allow/deny logic and … | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.52 | Support policies spanning multiple parks, venues, attractions, departments and business units while maintaining centralized governance. | F&B POS | CONTRACTED | `listOrgUnits` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-145` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-145`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 2: Works in Venue & Park Access Structure → Define the highest-level physical access hierarchy.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-145?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create org unit, Cancel.
- [ ] Every transition is wired: `BO-144`.
- [ ] Every gated control is gated: `SCOPE_MANAGE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-146` Access Area & Zone Builder

**Divide a venue into controlled access areas.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/access-area-zone-builder-bo-146` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-144` Access Control Command Center: *Returns to the board's landing screen*; calls `setAccessAreaZone`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access area zone list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access area zone untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access area zone yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access area zone are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setAccessAreaZone` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-146` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-146`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 4: Works in Access Area & Zone Builder → Divide a venue into controlled access areas.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-146?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-144`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-147` Attraction Access Configuration

**Configure attractions as access-controlled destinations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/attraction-access-configuration-bo-147` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-144` Access Control Command Center: *Returns to the board's landing screen*; calls `setAttractionAccess`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attraction access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attraction access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attraction access yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the attraction access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setAttractionAccess` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-147` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-147`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 6: Works in Attraction Access Configuration → Configure attractions as access-controlled destinations.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-147?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-144`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-148` Access Point Directory

**Create the logical access points where validation occurs. An Access Point is different from a physical reader/device.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Additional settings) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/access-point-directory-bo-148` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| operating schedule | select field | — | — | — | — | — | — |
| allowed direction | select field | — | — | — | — | — | — |
| capacity | select field | — | — | — | — | — | — |
| default mode | select field | — | — | — | — | — | — |
| associated zone | select field | — | — | — | — | — | — |
| allowed ticket categories | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listAccessPoints` (onLoad, List access points)

**Where the user goes next**

- → `BO-144` Access Control Command Center: *Returns to the board's landing screen*; calls `listAccessPoints`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access point configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access point untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access point configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAccessPoints` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Gate & zone management shows gates per location (e.g. three at a main entry plaza, two at a main entry zone); device inventory lists turnstiles and handhelds assignable per gate; a device is added by choosing an integrated turnstile model and entering connection details (IP address). *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-624)*
- Tiered access (e.g. Bronze/Silver/Gold): the client fills a matrix of which gates/attractions each tier may scan into; configured as location → admission profile → gate → access point, with explicit deny rules (e.g. Gold denied at the Silver/Bronze entrance). *(agreed · MoM 7 Aug 2026, 24. Tiered Ticketing & Access Control Deep Dive · DI-185)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-148` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-148`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 8: Works in Access Point Directory → Create the logical access points where validation occurs. An Access Point is different from a physical reader/device.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-148?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-144`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-149` Gate & Lane Configuration

**Configure individual physical gates/lanes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/gate-lane-configuration-bo-149` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-144` Access Control Command Center: *Returns to the board's landing screen*; calls `setGateLane`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gate lane list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gate lane untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gate lane yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the gate lane are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGateLane` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Gate & zone management shows gates per location (e.g. three at a main entry plaza, two at a main entry zone); device inventory lists turnstiles and handhelds assignable per gate; a device is added by choosing an integrated turnstile model and entering connection details (IP address). *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-624)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-149` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-149`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 10: Works in Gate & Lane Configuration → Configure individual physical gates/lanes.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-149?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-144`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-150` Access Control Graphical Map Designer

**Create a graphical digital twin of the access-control environment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/access-control-graphical-map-designer-bo-150` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-144` Access Control Command Center: *Returns to the board's landing screen*; calls `setAccessGraphicalMap`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access graphical map list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access graphical map untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access graphical map yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access graphical map are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setAccessGraphicalMap` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Venue-wide attendance overview (open/closed gates, offline/maintenance status, graphed) and a visual map of all access-control locations across venues/tenants, including entry and exit turnstile layouts that vary by venue. *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-623)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-150` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-150`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 12: Works in Access Control Graphical Map Designer → Create a graphical digital twin of the access-control environment.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-150?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-144`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-151` Access Location Grouping

**Group multiple access points for operational and capacity purposes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | Block A · ticket #20671 (APP-SETUP-BO-151) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `groupId` (navigation) |
| Route | `/access-venue/access-location-grouping-bo-151` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Form: Save access point group** (modal, opened by *Save access point group*; *Save access point group* calls `setAccessPointGroup`, *Cancel* sends nothing)

**Collects what `setAccessPointGroup` sends before it is called.** Required: `id`, `venueId`, `name`, `scopePath`. Optional: `parentGroupId`, `accessPointIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setAccessPointGroup` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setAccessPointGroup` body |
| Name `name` | text field | required | — | — | — | Group name, e.g. | `setAccessPointGroup` body |
| Parent group `parentGroupId` | picker: choose a parent group | optional | — | — | shows names, sends the id | Enclosing group, for nested groups | `setAccessPointGroup` body |
| Access points `accessPointIds` | multi-picker: choose access points | optional | — | — | — | Member access points (access.access_point) | `setAccessPointGroup` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `setAccessPointGroup` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `group-cycle`: the parent named would make the group its own ancestor.; 422 A member access point is not in the group's venue.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save access point group (primary button) | `setAccessPointGroup` PUT `/access-point-groups` | AccessAccessPointGroup | AccessAccessPointGroup | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |
| Delete access point group (destructive button) | `deleteAccessPointGroup` DELETE `/access-point-groups/{groupId}` | — | — | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE` |

**Data it reads**: `listAccessLocationGrouping` (onLoad, Access Location Grouping)

**Where the user goes next**

- → `BO-144` Access Control Command Center: *Returns to the board's landing screen*; calls `listAccessLocationGrouping`

**What opens over it**

- confirmDialog *Delete access point group*: **Names what `deleteAccessPointGroup` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access location grouping list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access location grouping untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access location grouping yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access location grouping are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `group-cycle`: the parent named would make the group its own ancestor.; 409 `group-in-use`: a nested group or a gate mode policy still names this group.; 422 A member access point is not in the group's venue. |

#### Permissions

- `listAccessLocationGrouping` → `SCOPE_VIEW` (read) · staff
- `setAccessPointGroup` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `deleteAccessPointGroup` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-151` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-151`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 14: Works in Access Location Grouping → Group multiple access points for operational and capacity purposes.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-151?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save access point group, Delete access point group.
- [ ] Every transition is wired: `BO-144`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-152` Operating Calendar & Special Access Days

**Allow access topology and operating behavior to change by date/time.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `entryId` (navigation) |
| Route | `/access-venue/operating-calendar-special-access-days-bo-152` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| normal operating days | select field | — | — | — | — | — | — |
| weekends | select field | — | — | — | — | — | — |
| holidays | select field | — | — | — | — | — | — |
| seasonal schedules | select field | — | — | — | — | — | — |
| private events | select field | — | — | — | — | — | — |
| free-entry days | select field | — | — | — | — | — | — |
| maintenance periods | select field | — | — | — | — | — | — |
| special events | select field | — | — | — | — | — | — |
| ladies-only sessions | select field | — | — | — | — | — | — |
| school/group sessions | select field | — | — | — | — | — | — |

**Form: Save operating calendar entry** (modal, opened by *Save operating calendar entry*; *Save operating calendar entry* calls `setOperatingCalendarEntry`, *Cancel* sends nothing)

**Collects what `setOperatingCalendarEntry` sends before it is called.** Required: `id`, `venueId`, `dayType`, `startsAt`, `endsAt`, `scopePath`. Optional: `name`, `ticketValidationRequired`, `admissionType`, `attractionValidation`, `manualAttendanceRequired`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setOperatingCalendarEntry` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setOperatingCalendarEntry` body |
| Day type `dayType` | select | required | — | Normal operating day · Weekend · Holiday · Seasonal schedule · Private event · Free entry day · Maintenance period · Special event · Ladies only session · School group session · After hours event | — | Kind of calendar entry | `setOperatingCalendarEntry` body |
| Name `name` | text field | optional | — | — | — | — | `setOperatingCalendarEntry` body |
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setOperatingCalendarEntry` body |
| Ends at `endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setOperatingCalendarEntry` body |
| Ticket validation required `ticketValidationRequired` | toggle | optional | on | — | — | False on free-entry days | `setOperatingCalendarEntry` body |
| Admission type `admissionType` | segmented control | optional | — | Free view day · Special event | — | Set on special admission windows only | `setOperatingCalendarEntry` body |
| Attraction validation `attractionValidation` | toggle | optional | — | — | — | Special windows: attraction gates keep validating tickets | `setOperatingCalendarEntry` body |
| Manual attendance required `manualAttendanceRequired` | toggle | optional | — | — | — | Special windows: operator enters attendance count | `setOperatingCalendarEntry` body |
| Scope path `scopePath` | text field | required | — | — | — | ltree of the owning scope node (ADR-0005) | `setOperatingCalendarEntry` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 `endsAt` is not after `startsAt`.

#### Outputs: what the screen shows and produces

**Shown**

**Calendar** (calendar view, from `listOperatingCalendarSpecial`): Operating days and special access days on the month view. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Filters the category on what it read.

| Shows | Format | Notes |
|---|---|---|
| Ends at | 1 Oct 2026, 14:30 | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Entry | text | — |
| Day type | chip: Normal operating day, Weekend, Holiday, Seasonal schedule, Private event, Free … | Kind of calendar entry |
| Venue | text | — |
| Name | text | — |
| Ticket validation required | yes / no (icon or chip) | False on free-entry days |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save operating calendar entry (primary button) | `setOperatingCalendarEntry` PUT `/operating-calendar-entries` | AccessOperatingCalendarEntry | AccessOperatingCalendarEntry | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |
| Delete operating calendar entry (destructive button) | `deleteOperatingCalendarEntry` DELETE `/operating-calendar-entries/{entryId}` | — | — | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE` |

**Data it reads**: `listOperatingCalendarSpecial` (onLoad, Operating Calendar & Special Access Days)

**Where the user goes next**

- → `BO-144` Access Control Command Center: *Returns to the board's landing screen*; calls `listOperatingCalendarSpecial`

**What opens over it**

- confirmDialog *Delete operating calendar entry*: **Names what `deleteOperatingCalendarEntry` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operating calendar special configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operating calendar special untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operating calendar special configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `entry-in-progress`: the entry has already started.; 422 `endsAt` is not after `startsAt`. |

#### Permissions

- `listOperatingCalendarSpecial` → `SCOPE_VIEW` (read) · staff
- `setOperatingCalendarEntry` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `deleteOperatingCalendarEntry` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Validity date range plus blockout dates (e.g. public holidays, special event days); entry allowance consumption blocks use once exhausted; multi-park crossover (how many parks, same-day or one per day, consecutive or flexible days); companion rules (child ticket needs a qualifying adult). *(client request · MoM 2 Sep 2026, 4.3 / 4.4 Validity, Crossover & Companion Rules · DI-628)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-152` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-152`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 16: Works in Operating Calendar & Special Access Days → Allow access topology and operating behavior to change by date/time.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-152?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save operating calendar entry, Delete operating calendar entry.
- [ ] Every transition is wired: `BO-144`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-153` Topology Validation & Publication

**Final validation and controlled deployment of access configuration. Before publication, TICVAI automatically validates: orphan gates devices without access points access points without zones incorrect entry/exit direction missing offline configuration conflicting operating calendars inaccessible zones missing emergency configuration capacity inconsistencies missing reader/device association policy dependencies.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `versionId` (navigation) |
| Route | `/access-venue/topology-validation-publication-bo-153` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Form: Rollback configuration version** (modal, opened by *Rollback configuration version*; *Rollback configuration version* calls `rollbackConfigurationVersion`, *Cancel* sends nothing)

**Collects what `rollbackConfigurationVersion` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `rollbackConfigurationVersion` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `not-active` or `no-previous-version`.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish (primary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |
| Rollback configuration version (secondary button) | `rollbackConfigurationVersion` POST `/configuration-versions/{versionId}/rollback` | inline | AccessConfigurationVersion | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ACCESS_POINT_CONFIGURE`; opens modal first |

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The topology validation publication list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the topology validation publication untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No topology validation publication yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the topology validation publication are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `not-active` or `no-previous-version`. |

#### Permissions

- `publishTopologyValidation` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `rollbackConfigurationVersion` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-153` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS18 Access Control Board 1.dc.html#bo-153`
- Workshop pack: Access Control Module_Reference.pdf board 1
- Flow F111 *Access Control board 1: Access Control Command Center*, step 18: Works in Topology Validation & Publication → Final validation and controlled deployment of access configuration. Before publication, TICVAI automatically validates: orphan gates devices without access points access points without zones …

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-153?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish, What publishing changes, Rollback configuration version.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createAccessPoint": {"method":"POST","path":"/access-points","contract":"access","summary":"Create an access point","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateAccessPointRequest","responds":"AccessPoint"},
"createOrgUnit": {"method":"POST","path":"/org-units","contract":"tenancy","summary":"Create a scope node","permission":"SCOPE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"brand","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateScopeNodeRequest","responds":"OrgUnit"},
"deleteAccessPointGroup": {"method":"DELETE","path":"/access-point-groups/{groupId}","contract":"access","summary":"Delete an access-point group","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"deleteOperatingCalendarEntry": {"method":"DELETE","path":"/operating-calendar-entries/{entryId}","contract":"access","summary":"Delete an operating calendar entry","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listAccess": {"method":"GET","path":"/access","contract":"access","summary":"Access Control Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessControlCommandCenterView"},
"listAccessLocationGrouping": {"method":"GET","path":"/access-location-grouping","contract":"access","summary":"Access Location Grouping","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessLocationGroupingView"},
"listAccessPoints": {"method":"GET","path":"/access-points","contract":"access","summary":"List access points","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOperatingCalendarSpecial": {"method":"GET","path":"/operating-calendar-special","contract":"access","summary":"Operating Calendar & Special Access Days","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OperatingCalendarSpecialAccessDaysView"},
"listOrgUnits": {"method":"GET","path":"/org-units","contract":"tenancy","summary":"List scope nodes visible to the session","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"under","in":"query","required":null},{"name":"level","in":"query","required":null},{"name":"includeInactive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVenueParkAccess": {"method":"GET","path":"/venue-park-access","contract":"access","summary":"Venue & Park Access Structure","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"VenueParkAccessStructureView"},
"publishTopologyValidation": {"method":"PUT","path":"/topology-validation","contract":"access","summary":"Topology Validation & Publication","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TopologyValidationPublicationInput","responds":"TopologyValidationPublicationView"},
"rollbackConfigurationVersion": {"method":"POST","path":"/configuration-versions/{versionId}/rollback","contract":"access","summary":"Roll back an active access configuration version","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessConfigurationVersion"},
"setAccessAreaZone": {"method":"PUT","path":"/access-area-zone","contract":"access","summary":"Access Area & Zone Builder","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessAreaZoneBuilderInput","responds":"AccessAreaZoneBuilderView"},
"setAccessGraphicalMap": {"method":"PUT","path":"/access-graphical-map","contract":"access","summary":"Access Control Graphical Map Designer","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessControlGraphicalMapDesignerInput","responds":"AccessControlGraphicalMapDesignerView"},
"setAccessPointGroup": {"method":"PUT","path":"/access-point-groups","contract":"access","summary":"Create or replace an access-point group","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessAccessPointGroup","responds":"AccessAccessPointGroup"},
"setAttractionAccess": {"method":"PUT","path":"/attraction-access","contract":"access","summary":"Attraction Access Configuration","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AttractionAccessConfigurationInput","responds":"AttractionAccessConfigurationView"},
"setGateLane": {"method":"PUT","path":"/gate-lane","contract":"access","summary":"Gate & Lane Configuration","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GateLaneConfigurationInput","responds":"GateLaneConfigurationView"},
"setOperatingCalendarEntry": {"method":"PUT","path":"/operating-calendar-entries","contract":"access","summary":"Create or replace an operating calendar entry","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessOperatingCalendarEntry","responds":"AccessOperatingCalendarEntry"},
"updateOrgUnit": {"method":"PATCH","path":"/org-units/{orgUnitId}","contract":"tenancy","summary":"Rename or deactivate a scope node","permission":"SCOPE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"brand","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrgUnit"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessAccessPointGroup": {"type":"object","x-ticvai-persistence":"access.access_point_group","description":"A named group of access points in one venue (e.g. Main Entrance), optionally nested, whose counts roll up to a common occupancy (declared 29 September, data-model close-out DM1)","required":["id","venueId","name","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"name":{"type":"string","description":"Group name, e.g. Main Entrance"},"parentGroupId":{"type":"string","format":"uuid","nullable":true,"description":"Enclosing group, for nested groups"},"accessPointIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Member access points (access.access_point)"},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessAreaZoneBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is access.parking_facility at 14%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Access Area & Zone Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *Each zone receives* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.","properties":{"name":{"type":"string","description":"Zone name, e.g. VIP Lounge"},"venueId":{"type":"string","description":"Venue the zone belongs to"},"zoneId":{"type":"string","description":"Zone being written"},"zoneType":{"type":"string","enum":["public","ticketed","vip","staff","backOfHouse","attraction","restricted","fastPass","event","temporary"],"description":"Vocabulary listed under Create."},"capacity":{"type":"integer","description":"capacity"},"operatingSchedule":{"type":"string","description":"operating schedule"},"securityClassification":{"type":"string","description":"security classification"},"entryRequirements":{"type":"string","description":"entry requirements"},"exitRequirements":{"type":"string","description":"exit requirements"},"allowedCredentialClasses":{"type":"array","items":{"type":"string"},"description":"Credential classes admitted to the zone"},"parentId":{"type":"string","description":"Park or zone this zone sits under in the venue structure"}},"x-ticvai-record-definition":"Each zone receives","required":["zoneId","venueId","name","zoneType"]},
"AccessAreaZoneBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Area & Zone Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string","description":"Zone name, e.g. VIP Lounge"},"venueId":{"type":"string","description":"Venue the zone belongs to"},"zoneId":{"type":"string","description":"Zone being written"},"zoneType":{"type":"string","enum":["public","ticketed","vip","staff","backOfHouse","attraction","restricted","fastPass","event","temporary"],"description":"Vocabulary listed under Create."},"capacity":{"type":"integer","description":"capacity"},"operatingSchedule":{"type":"string","description":"operating schedule"},"securityClassification":{"type":"string","description":"security classification"},"entryRequirements":{"type":"string","description":"entry requirements"},"exitRequirements":{"type":"string","description":"exit requirements"},"allowedCredentialClasses":{"type":"array","items":{"type":"string"},"description":"Credential classes admitted to the zone"},"parentId":{"type":"string","description":"Park or zone this zone sits under in the venue structure"}},"required":["zoneId","venueId","name","zoneType"]},
"AccessConfigurationVersion": {"type":"object","x-ticvai-persistence":"access.configuration_version","description":"One version of access configuration (a topology or a rule set) moving through simulate, validate, schedule, publish and roll back, with its target, schedule, validation findings and the previous version kept for rollback (declared 29 September, data-model close-out DM1)","required":["id","configurationKind","version","status","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid","nullable":true},"configurationKind":{"type":"string","enum":["topology","ruleSet"]},"version":{"type":"string","description":"Version label"},"snapshot":{"type":"object","description":"The configuration captured by this version, restored on rollback"},"status":{"type":"string","enum":["draft","validated","pendingApproval","scheduled","active","inactive","rolledBack"],"default":"draft"},"lastStep":{"type":"string","enum":["simulate","validate","schedule","publish","rollBack"],"nullable":true,"description":"Last lifecycle step run on this version"},"targetScope":{"type":"string","enum":["tenant","venue","park","zone","accessPoint","selectedGates","selectedDevices"],"nullable":true,"description":"What the publication covers"},"targetIds":{"type":"array","items":{"type":"string"},"description":"IDs within the target scope"},"publishMode":{"type":"string","enum":["now","scheduled"],"nullable":true},"scheduledAt":{"type":"string","format":"date-time","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"validationIssues":{"type":"array","items":{"type":"string"},"description":"Blocking findings from pre-publication validation"},"conflicts":{"type":"array","items":{"type":"string"},"description":"Rule conflicts found by the conflict check (advisory)"},"previousVersionId":{"type":"string","format":"uuid","nullable":true,"description":"Version this one replaces, for rollback"},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"description":"Approval request raised in the approvals engine"},"createdByPrincipalId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessControlCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Control Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"totalVenues":{"type":"integer","description":"Total venues"},"activeAccessPoints":{"type":"integer","description":"Active access points"},"entryGates":{"type":"integer","description":"Entry gates"},"exitGates":{"type":"integer","description":"Exit gates"},"attractionGates":{"type":"integer","description":"Attraction gates"},"turnstiles":{"type":"integer","description":"Turnstiles"},"handheldDevices":{"type":"integer","description":"Handheld devices"},"devicesOnline":{"type":"integer","description":"Devices online"},"devicesOffline":{"type":"integer","description":"Devices offline"},"gatesOpen":{"type":"integer","description":"Gates open"},"gatesClosed":{"type":"integer","description":"Gates closed"},"currentInVenueOccupancy":{"type":"integer","description":"Current in-venue occupancy"},"currentAdmissionRate":{"type":"number","description":"Admissions per minute across the estate"},"failedScans":{"type":"integer","description":"Failed scans"},"overrides":{"type":"integer","description":"Overrides"},"securityAlerts":{"type":"integer","description":"Security alerts"},"synchronizationStatus":{"type":"string","enum":["inSync","syncPending","syncFailed"],"description":"Estate-wide offline sync state of devices"}}},
"AccessControlGraphicalMapDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Access Control Graphical Map Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"venueId":{"type":"string","description":"Venue the map belongs to"},"mapId":{"type":"string","description":"Map being written"},"sourceFileType":{"type":"string","enum":["cad","pdf","image","venuePlan","architecturalDrawing"],"description":"Kind of drawing uploaded as the map base"},"sourceFile":{"type":"string","description":"Reference to the uploaded drawing"}},"required":["mapId","venueId"]},
"AccessControlGraphicalMapDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Control Graphical Map Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venueId":{"type":"string","description":"Venue the map belongs to"},"mapId":{"type":"string","description":"Map being written"},"sourceFileType":{"type":"string","enum":["cad","pdf","image","venuePlan","architecturalDrawing"],"description":"Kind of drawing uploaded as the map base"},"sourceFile":{"type":"string","description":"Reference to the uploaded drawing"}},"required":["mapId","venueId"]},
"AccessLocationGroupingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Location Grouping displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string","description":"Group name, e.g. Main Entrance"},"groupId":{"type":"string"},"venueId":{"type":"string"},"parentGroupId":{"type":"string","description":"Enclosing group, for nested groups"},"accessPointIds":{"type":"array","items":{"type":"string"},"description":"Access points whose counts roll up into this group"}},"required":["groupId","name"]},
"AccessOperatingCalendarEntry": {"type":"object","x-ticvai-persistence":"access.operating_calendar_entry","description":"One dated entry in a venue operating calendar (normal day, holiday, private event, free-entry day, special event and so on), with whether tickets must be validated. Merges access.special_admission_window, whose free-view and special-event windows are entries carrying an admission type (declared 29 September, data-model close-out DM1)","required":["id","venueId","dayType","startsAt","endsAt","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"dayType":{"type":"string","enum":["normalOperatingDay","weekend","holiday","seasonalSchedule","privateEvent","freeEntryDay","maintenancePeriod","specialEvent","ladiesOnlySession","schoolGroupSession","afterHoursEvent"],"description":"Kind of calendar entry"},"name":{"type":"string","nullable":true},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"ticketValidationRequired":{"type":"boolean","default":true,"description":"False on free-entry days"},"admissionType":{"type":"string","enum":["freeViewDay","specialEvent"],"nullable":true,"description":"Set on special admission windows only"},"attractionValidation":{"type":"boolean","nullable":true,"description":"Special windows: attraction gates keep validating tickets"},"manualAttendanceRequired":{"type":"boolean","nullable":true,"description":"Special windows: operator enters attendance count"},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessPoint": {"x-ticvai-persistence":"access.access_point","type":"object","required":["id","code","name","venueId","operatingMode","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"externalCredentialSources":{"allOf":[{"$ref":"#/components/schemas/ExternalCredentialSourceList"}],"description":"BL-108. **A hotel room card admitting a guest to a water park** — externally issued, and the platform validates it without having sold it.\n**The entitlement is created on first use, not on check-in.** A hotel with 400 rooms does not want 400 entitlements a night for guests who never visit.\n"},"scanAnomalyRules":{"allOf":[{"$ref":"#/components/schemas/ScanAnomalyRuleList"}],"description":"BL-104. **Rule-based scan anomalies, separated from the parked model-based engine** — device sharing, simultaneous entries at two gates, an impossible walking time between them.\n**These are deterministic and need no model**, which is why they are here and not in `ai`: two entries eight seconds apart at gates four hundred metres apart is arithmetic.\n"},"operatingMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}],"default":"normal","description":"**Set by the podium with `setTurnstileMode`, and it wins** (audit R221). BL-107 and BL-109. **A closed turnstile and one in emergency drop-arm mode look the same in the model and are opposite in meaning.** Closed refuses everybody; drop-arm lets everybody through, and it is the state that exists for an evacuation.\n**`podium` is a supervised validation position** — a member of staff directing a group through a lane, validating by eye against a list. It scans nothing and it is how school parties actually enter.\n**`freeFlow` counts without validating.** Useful at a free event, and a mode that must be visibly distinct from a broken reader.\n"},"vehicleLocationCapture":{"type":"boolean","default":false,"description":"BL-023. **Nothing helped a guest find their vehicle.** Where the access point is a car park entry, the level and zone are captured against the visit so the app can answer it — **the guest who cannot find their car at 11pm is the last impression of the day.**\n"},"mode":{"allOf":[{"$ref":"#/components/schemas/TurnstileMode"}],"nullable":true,"description":"Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates in its fixed `direction` (audit R221).\n"},"direction":{"allOf":[{"$ref":"#/components/schemas/Direction"}],"description":"**Fixed per access point** (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium.\n"},"antiPassbackEnabled":{"type":"boolean"},"requiresExitBeforeReentry":{"type":"boolean","default":false,"description":"Written by `createAccessPoint` and `updateAccessPoint`, and returned so the edit form reads back what it wrote."},"driver":{"type":"string","nullable":true,"description":"Driver identifier for the controller behind this access point, as written by `createAccessPoint` and `updateAccessPoint`. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific.\n"},"geofence":{"allOf":[{"$ref":"#/components/schemas/AccessPointGeofence"}],"nullable":true,"description":"Written by `setAccessPointGeofence`; null until one is set. **One `jsonb` column on the access point row** (`access.access_point.geofence`), read with the point when a handheld validates against it.\n"},"isActive":{"type":"boolean"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true}}},
"AccessPointGeofence": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"Where a handheld may validate for one access point, and what happens outside it. The body of `setAccessPointGeofence` and the value of `AccessPoint.geofence`.\n","required":["enforcement"],"properties":{"latitude":{"type":"number"},"longitude":{"type":"number"},"radiusMetres":{"type":"integer","minimum":5,"maximum":5000},"enforcement":{"type":"string","enum":["off","warn","deny"],"description":"`off` keeps the fence on record and checks nothing; `warn` lets a validation from outside the fence through with a warning; `deny` refuses it.\n"},"allowProximityBeacon":{"type":"boolean","description":"Accept a BLE proximity assertion in place of GPS. Better indoors."}}},
"AccessPointOperatingMode": {"type":"string","description":"BL-107 and BL-109. **What the gate does, and what the podium sets** (`setTurnstileMode`, decided 28 September, audit R221). `closed` refuses everybody; `dropArm` lets everybody through and exists for an evacuation; `podium` is supervised validation by eye; `freeFlow` counts without validating; `maintenance` takes the lane out of use.\n","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"]},
"AttractionAccessConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is access.parking_facility at 6%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Attraction Access Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each attraction* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.","properties":{"attractionId":{"type":"string","description":"Attraction ID"},"name":{"type":"string","description":"Name"},"venue":{"type":"string","description":"Venue"},"zone":{"type":"string","description":"Zone"},"capacity":{"type":"integer","description":"Capacity"},"entryPoints":{"type":"array","items":{"type":"string"},"description":"Access point IDs used to enter"},"exitPoints":{"type":"array","items":{"type":"string"},"description":"Access point IDs used to exit"},"fastPassSupport":{"type":"boolean","description":"Fast Pass support"},"heightRestriction":{"type":"integer","description":"Minimum rider height in cm, e.g. 130"},"ageRestriction":{"type":"integer","description":"Minimum age in years"},"adultCompanionRequirement":{"type":"boolean","description":"Adult companion requirement"},"membershipAccess":{"type":"boolean","description":"Membership access"},"vipAccess":{"type":"boolean","description":"VIP access"},"entitlementRequirement":{"type":"string","description":"entitlement requirement"},"biometricRequirement":{"type":"boolean","description":"biometric requirement"},"operatingCalendar":{"type":"string","description":"operating calendar"},"temporaryClosureBehavior":{"type":"string","description":"temporary closure behavior"}},"x-ticvai-record-definition":"For each attraction","required":["attractionId","name","venue"]},
"AttractionAccessConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Attraction Access Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"attractionId":{"type":"string","description":"Attraction ID"},"name":{"type":"string","description":"Name"},"venue":{"type":"string","description":"Venue"},"zone":{"type":"string","description":"Zone"},"capacity":{"type":"integer","description":"Capacity"},"entryPoints":{"type":"array","items":{"type":"string"},"description":"Access point IDs used to enter"},"exitPoints":{"type":"array","items":{"type":"string"},"description":"Access point IDs used to exit"},"fastPassSupport":{"type":"boolean","description":"Fast Pass support"},"heightRestriction":{"type":"integer","description":"Minimum rider height in cm, e.g. 130"},"ageRestriction":{"type":"integer","description":"Minimum age in years"},"adultCompanionRequirement":{"type":"boolean","description":"Adult companion requirement"},"membershipAccess":{"type":"boolean","description":"Membership access"},"vipAccess":{"type":"boolean","description":"VIP access"},"entitlementRequirement":{"type":"string","description":"entitlement requirement"},"biometricRequirement":{"type":"boolean","description":"biometric requirement"},"operatingCalendar":{"type":"string","description":"operating calendar"},"temporaryClosureBehavior":{"type":"string","description":"temporary closure behavior"}},"required":["attractionId","name","venue"]},
"CreateAccessPointRequest": {"type":"object","required":["code","name","venueId","direction"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"direction":{"$ref":"#/components/schemas/Direction"},"antiPassbackEnabled":{"type":"boolean","default":false},"requiresExitBeforeReentry":{"type":"boolean","default":false},"driver":{"type":"string"}}},
"CreateScopeNodeRequest": {"type":"object","required":["level","parentId","code","name"],"properties":{"level":{"$ref":"#/components/schemas/ScopeLevel"},"parentId":{"type":"string","format":"uuid","description":"Required for every level except tenant, which the cell creates at provisioning."},"code":{"type":"string","maxLength":64,"pattern":"^[a-z0-9_]+$","description":"Becomes the final ltree segment. Immutable once created."},"name":{"type":"string","maxLength":200}}},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"ExternalCredentialSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.external_credential_sources`). Read with the access point when a credential is presented; a source is never queried on its own.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["hotelRoomCard","corporateBadge","cityPass","transitCard","partnerToken"]},"providerName":{"type":"string"},"endpoint":{"type":"string"},"credentialRef":{"type":"string"},"grantsProductId":{"type":"string","format":"uuid"}}}},
"GateLaneConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Gate & Lane Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"gateId":{"type":"string","description":"Gate ID"},"gateName":{"type":"string","description":"Gate name"},"accessPoint":{"type":"string","description":"Access point"},"location":{"type":"string","description":"Location"},"laneNumber":{"type":"string","description":"lane number"},"direction":{"type":"string","enum":["entry","exit","bidirectional"],"description":"Lane direction, inherited from the access point unless set"},"reEntry":{"type":"boolean","description":"Lane accepts re-entry scans"},"crossover":{"type":"boolean","description":"Lane is a crossover lane between parks"},"type":{"type":"string","enum":["standard","vip","fastPass","accessible","group","staff","attraction"],"description":"Vocabulary listed under Gate type."},"operationalMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}],"description":"Default operating mode of the lane, in the AccessPointOperatingMode vocabulary the podium sets (R221). Aligned (decided 29 September, writers pass): the old validation, freeSpin, emergencyDropArm, manual and countOnly are normal, freeFlow, dropArm, podium and freeFlow."},"laneSize":{"type":"string","enum":["standard","wide"],"description":"Wide lanes take buggies and wheelchairs"}},"required":["gateId","accessPoint"]},
"GateLaneConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Gate & Lane Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"gateId":{"type":"string","description":"Gate ID"},"gateName":{"type":"string","description":"Gate name"},"accessPoint":{"type":"string","description":"Access point"},"location":{"type":"string","description":"Location"},"laneNumber":{"type":"string","description":"lane number"},"direction":{"type":"string","enum":["entry","exit","bidirectional"],"description":"Lane direction, inherited from the access point unless set"},"reEntry":{"type":"boolean","description":"Lane accepts re-entry scans"},"crossover":{"type":"boolean","description":"Lane is a crossover lane between parks"},"type":{"type":"string","enum":["standard","vip","fastPass","accessible","group","staff","attraction"],"description":"Vocabulary listed under Gate type."},"operationalMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}],"description":"Default operating mode of the lane, in the AccessPointOperatingMode vocabulary the podium sets (R221). Aligned (decided 29 September, writers pass): the old validation, freeSpin, emergencyDropArm, manual and countOnly are normal, freeFlow, dropArm, podium and freeFlow."},"laneSize":{"type":"string","enum":["standard","wide"],"description":"Wide lanes take buggies and wheelchairs"}},"required":["gateId","accessPoint"]},
"OperatingCalendarSpecialAccessDaysView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Operating Calendar & Special Access Days displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"endsAt":{"type":"string","format":"date-time"},"startsAt":{"type":"string","format":"date-time"},"entryId":{"type":"string"},"dayType":{"type":"string","enum":["normalOperatingDay","weekend","holiday","seasonalSchedule","privateEvent","freeEntryDay","maintenancePeriod","specialEvent","ladiesOnlySession","schoolGroupSession","afterHoursEvent"],"description":"Kind of calendar entry"},"venueId":{"type":"string"},"name":{"type":"string"},"ticketValidationRequired":{"type":"boolean","description":"False on free-entry days"}},"required":["entryId","dayType","startsAt","endsAt"]},
"OrgUnit": {"x-ticvai-persistence":"platform.scope","type":"object","required":["id","level","path","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"level":{"$ref":"#/components/schemas/ScopeLevel"},"parentId":{"type":"string","format":"uuid","nullable":true},"path":{"type":"string","description":"Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`.","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"isActive":{"type":"boolean","description":"False causes every permission query at or beneath this node to resolve to DENY.\n"},"childCount":{"type":"integer","minimum":0}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ScanAnomalyRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.scan_anomaly_rules`). Read with the access point at validation, and a rule is never queried on its own.\n","items":{"type":"object","properties":{"rule":{"type":"string","enum":["simultaneousEntry","impossibleTravelTime","rapidReentry","sharedDevice","velocityBreach"]},"action":{"type":"string","enum":["log","flag","requireSupervisor","deny"]},"thresholdSeconds":{"type":"integer","nullable":true}}}},
"ScopeLevel": {"type":"string","description":"**The eight organisational levels, plus `subject`.** Restored 24 August.\n`tenancy.yaml` holds the authoritative definition of the eight levels and this mirrors them so a contract can reference a level without depending on the whole tenancy surface. **Seven organisational levels plus `outlet`** — a commercial branch beside the organisational one (CF-138, ADR-0018). **A department has requisitions and rotas; an outlet has a menu and stock**, and modelling a restaurant as a department would put it in the staffing tree.\n\n**`subject` is the one value tenancy does not have, and it is not a level.** It is here because `check-package` reads this enum as the closed vocabulary for `x-ticvai-scope-level`, and some operations act on one guest's own resources, which sit in no node of the venue hierarchy. So `subject` is valid as an operation's scope level and never as a `ScopeRef.level`: every `ScopeRef` is a row of `platform.scope`, and those carry one of the eight.\n","enum":["tenant","brand","region","venue","department","subDepartment","workstation","outlet","subject"]},
"TopologyValidationPublicationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Topology Validation & Publication submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"publishMode":{"type":"string","enum":["now","scheduled"]},"configurationVersionId":{"type":"string","description":"Topology version being published"},"targetScope":{"type":"string","enum":["tenant","venue","park","zone","accessPoint","selectedGates","selectedDevices"],"description":"What the publication covers"},"targetIds":{"type":"array","items":{"type":"string"},"description":"IDs within the target scope"},"scheduledAt":{"type":"string","format":"date-time"},"validationIssues":{"type":"array","items":{"type":"string"},"description":"Blocking findings from pre-publication validation"}},"required":["configurationVersionId","targetScope","publishMode"]},
"TopologyValidationPublicationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Topology Validation & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"publishMode":{"type":"string","enum":["now","scheduled"]},"configurationVersionId":{"type":"string","description":"Topology version being published"},"targetScope":{"type":"string","enum":["tenant","venue","park","zone","accessPoint","selectedGates","selectedDevices"],"description":"What the publication covers"},"targetIds":{"type":"array","items":{"type":"string"},"description":"IDs within the target scope"},"scheduledAt":{"type":"string","format":"date-time"},"validationIssues":{"type":"array","items":{"type":"string"},"description":"Blocking findings from pre-publication validation"}},"required":["configurationVersionId","targetScope","publishMode"]},
"TurnstileMode": {"type":"string","description":"**Reduced to two values — decided 28 September, audit R221.** Entry, exit, re-entry and crossover were the access point's `Direction` under another name, and two fields that could disagree left the gate to guess. Direction is fixed per access point; within `normal` or `podium` operation the turnstile may only be let spin free or held closed.\n","enum":["freeRotation","closed"]},
"VenueParkAccessStructureView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Venue & Park Access Structure displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"entityType":{"type":"string","enum":["venue","park","building","eventSpace","waterpark","themePark","museum","arena","stadium","exhibition","temporaryVenue"],"description":"What kind of place this entity is"},"name":{"type":"string","description":"Name"},"code":{"type":"string","description":"Code"},"tenant":{"type":"string","description":"Tenant"},"parentEntity":{"type":"string","description":"Parent entity"},"timeZone":{"type":"string","description":"IANA time zone, e.g. Asia/Dubai"},"operatingCalendar":{"type":"string","description":"Operating calendar"},"capacity":{"type":"integer","description":"Capacity"},"accessControlEnabled":{"type":"boolean","description":"Access-control enabled"},"defaultEntryPolicy":{"type":"string","description":"Default entry policy"},"defaultExitPolicy":{"type":"string","description":"Default exit policy"},"defaultCredentialRules":{"type":"string","description":"Default credential rules"},"offlinePolicy":{"type":"string","description":"Reference to the offline validation policy the entity inherits"},"emergencyBehavior":{"type":"string","description":"Emergency behavior"},"supportMultiParkEnvironments":{"type":"boolean","description":"Support multi-park environments"}},"required":["code","name","entityType"]}
}
```
