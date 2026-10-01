# WS167 — Seat Management Venue Mapping Reference v1.0 board 3

**10 screens · 17 operations · 20 schemas · 4 permissions**

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
  `ACCESS_POINT_CONFIGURE, AI_USE, CAPACITY_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `BO-973` | Layout Command Center | B–D | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-974` | Template Library | B–D | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `BO-975` | Event-Specific Layout | B–D | 0 | 0 | 6 | 6 | 0 | 0 | — | notStarted (—) |
| `BO-976` | Clone & Inheritance | B–D | 0 | 0 | 6 | 3 | 1 | 0 | — | notStarted (—) |
| `BO-977` | Version Compare | B–D | 2 | 16 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-978` | Multi-Performance Assignment | B–D | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `BO-979` | Temporary Seat Blocking | B–D | 0 | 0 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-980` | Scheduled Seat Release | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-981` | Conflict & Impact Simulation | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-982` | Approval, Publish & Rollback | B–D | 0 | 0 | 6 | 5 | 0 | 3 | — | notStarted (—) |

## Thin screens in this batch

**BO-973, BO-974, BO-976, BO-979, BO-981, BO-982 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-973` Layout Command Center

**Manage layouts, versions and performance assignments from one operational view. Show active layouts, draft versions, total capacity, utilization, upcoming changes, validation issues and approval status. List layouts by venue, template, event, performance, version, owner, status and effective period. Surface urgent sold-seat impact, missing assignment and publication conflicts with direct remediation links. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/layout-command-center-bo-973` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Draft · Validated · Published · Archived | `listSeatMaps` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listSeatMaps` (onLoad, Layouts in use)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-974` Template Library: *Template Library*
- → `BO-975` Event-Specific Layout: *Event-Specific Layout*
- → `BO-976` Clone & Inheritance: *Clone & Inheritance*
- → `BO-977` Version Compare: *Version Compare*
- → `BO-978` Multi-Performance Assignment: *Multi-Performance Assignment*
- → `BO-979` Temporary Seat Blocking: *Temporary Seat Blocking*
- → `BO-980` Scheduled Seat Release: *Scheduled Seat Release*
- → `BO-981` Conflict & Impact Simulation: *Conflict & Impact Simulation*
- → `BO-982` Approval, Publish & Rollback: *Approval, Publish & Rollback*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The layout list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the layout untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No layout yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the layout are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listSeatMaps` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.13.3 | Seat Management APIs | Seat Management & Venue Mapping | CONTRACTED | `listSeatMaps` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-973` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-973`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 3
- Flow F276 *Seat Management Venue Mapping Reference v1.0 board 3: Layout Command Center*, step 1: Opens Layout Command Center → Manage layouts, versions and performance assignments from one operational view. Show active layouts, draft versions, total capacity, utilization, upcoming changes, validation issues and approval …
- Flow F276 *Seat Management Venue Mapping Reference v1.0 board 3: Layout Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F276 *Seat Management Venue Mapping Reference v1.0 board 3: Layout Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F276 *Seat Management Venue Mapping Reference v1.0 board 3: Layout Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F276 *Seat Management Venue Mapping Reference v1.0 board 3: Layout Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F276 *Seat Management Venue Mapping Reference v1.0 board 3: Layout Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F276 *Seat Management Venue Mapping Reference v1.0 board 3: Layout Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F276 *Seat Management Venue Mapping Reference v1.0 board 3: Layout Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F276 branch at step 1 (expected): when Nothing has been set up on Layout Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F276 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-973?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-974`, `BO-975`, `BO-976`, `BO-977`, `BO-978`, `BO-979`, `BO-980`, `BO-981`, `BO-982`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-974` Template Library

**Maintain reusable layouts for common venue configurations. Provide templates for end-stage, center-stage, sports, theatre, banquet, classroom and venue-defined patterns. Store capacity, focal point, production footprint, section availability, access routes and default blocked inventory. Support preview, clone, compare, archive, ownership and controlled sharing across authorized tenants or venues. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/template-library-bo-974` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create seat map template (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listSeatMapTemplates` (onLoad, The library)

**Where the user goes next**

- → `BO-973` Layout Command Center: *Back to Layout Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The template list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the template untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No template yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the template are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listSeatMapTemplates` → `PRODUCT_VIEW` (read) · staff
- `createSeatMapTemplate` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.1.9 | Venue Template Management | Seat Management & Venue Mapping | CONTRACTED | `createSeatMapTemplate` |
| 21.3.1 | Layout Templates | Seat Management & Venue Mapping | CONTRACTED | `createSeatMapTemplate` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: saved seat maps can be reused, copied in full, or partially copied (one section's layout/seating into another map); a template library and a layout version-comparison view show seat-count/configuration differences. *(agreed · MoM 21 Aug 2026, 4.4 AI-Assisted Seat Map Import & Layout/Template Management · DI-418)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-974` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-974`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 3
- Flow F276 *Seat Management Venue Mapping Reference v1.0 board 3: Layout Command Center*, step 2: Works in Template Library → Maintain reusable layouts for common venue configurations. Provide templates for end-stage, center-stage, sports, theatre, banquet, classroom and venue-defined patterns. Store capacity, focal point …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-974?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create seat map template, Cancel.
- [ ] Every transition is wired: `BO-973`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-975` Event-Specific Layout

**Create a seating layout tailored to one event or production. Start from the current venue map or approved template and adjust stage, field, sections, rows, seats, aisles and facilities. Display live capacity by section/category and affected pricing, products, access gates and operational resources. Support drafts, notes, attachments, production requirements and validation before performance assignment. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Configuration Scope of Work / Version 1.0 14 Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `CAPACITY_CONFIGURE`, `PRODUCT_VIEW` (1 operate, 1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `seatMapId` (navigation), `actionId` (navigation), `planId` (navigation) |
| Route | `/access-venue/event-specific-layout-bo-975` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish seat map (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-973` Layout Command Center: *Back to Layout Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The event-specific layout list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the event-specific layout untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No event-specific layout yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the event-specific layout are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213).; 409 Validation failed. (ValidationProblem); 422 The input the kind needs is missing (`numberingScheme` for `numbering`, `stagePosition` for `stageVariant`), or the map has no focal zone for `categories` … |

#### Permissions

- `getSeatMap` → `PRODUCT_VIEW` (read) · staff
- `publishSeatMap` → `CAPACITY_CONFIGURE` (configure) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff
- `proposeSeatMapChanges` → `CAPACITY_CONFIGURE` (configure) · staff
- `getActionPlan` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.2.16 | One-Click Publishing | Seat Management & Venue Mapping | CONTRACTED | `publishSeatMap` |
| 8.1.4 | Approval Before Execution AI recommendations affecting pricing or financial operations shall require approval before execution | Unified Operations Dashboard | CONTRACTED | `decideProposedAction` |
| 1.4.23 | Event-Specific Configurations For multi-purpose venues, AI can: Create different seat maps for concerts, sports events, exhibitions, and conferences. Configure temporary seating arrangements. … | Ticketing Catalogue | CONTRACTED | `proposeSeatMapChanges` |
| 1.4.25 | Intelligent Seat Numbering Automatically assign row names (A, B, C, etc.) and seat numbers based on configurable rules. Validate numbering sequences and identify duplicates or missing seats. Apply … | Ticketing Catalogue | CONTRACTED | `proposeSeatMapChanges` |
| 1.4.26 | Seat Category Configuration AI can recommend seat categories based on: Distance from the stage or attraction. Viewing angles and sightlines. Elevation and seating tier. Historical sales performance. … | Ticketing Catalogue | CONTRACTED | `proposeSeatMapChanges` |
| 1.4.29 | Validation and Quality Assurance AI can automatically identify: Duplicate seat numbers. Missing rows or seats. Incorrect category assignments. Accessibility compliance issues. Capacity mismatches … | Ticketing Catalogue | CONTRACTED | `proposeSeatMapChanges` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-975` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-975`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 3
- Flow F276 *Seat Management Venue Mapping Reference v1.0 board 3: Layout Command Center*, step 4: Works in Event-Specific Layout → Create a seating layout tailored to one event or production. Start from the current venue map or approved template and adjust stage, field, sections, rows, seats, aisles and facilities. Display live …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-975?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish seat map, Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-973`.
- [ ] Every gated control is gated: `AI_USE`, `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-976` Clone & Inheritance

**Reuse a layout without losing the relationship to its approved source. Clone a layout for another event, venue or performance and select which settings are inherited, copied or excluded. Show inherited versus overridden geometry, categories, holds, accessibility, pricing and production settings. Warn when later source changes could affect dependent clones and require explicit synchronization decisions. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `seatMapId` (navigation) |
| Route | `/access-venue/clone-inheritance-bo-976` |

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

- → `BO-973` Layout Command Center: *Back to Layout Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The clone inheritance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the clone inheritance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No clone inheritance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the clone inheritance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `cloneSeatMap` → `CAPACITY_CONFIGURE` (configure) · staff
- `copySeatMapSection` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.3.2 | Event-Specific Layouts | Seat Management & Venue Mapping | CONTRACTED | `cloneSeatMap` |
| 21.3.3 | Layout Cloning | Seat Management & Venue Mapping | CONTRACTED | `cloneSeatMap` |
| 21.3.7 | Multi-Performance Layouts | Seat Management & Venue Mapping | CONTRACTED | `cloneSeatMap` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: saved seat maps can be reused, copied in full, or partially copied (one section's layout/seating into another map); a template library and a layout version-comparison view show seat-count/configuration differences. *(agreed · MoM 21 Aug 2026, 4.4 AI-Assisted Seat Map Import & Layout/Template Management · DI-418)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-976` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-976`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 3
- Flow F276 *Seat Management Venue Mapping Reference v1.0 board 3: Layout Command Center*, step 6: Works in Clone & Inheritance → Reuse a layout without losing the relationship to its approved source. Clone a layout for another event, venue or performance and select which settings are inherited, copied or excluded. Show …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-976?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-973`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-977` Version Compare

**Review exact differences between layout versions before approval or rollback. Provide side-by-side and overlay comparisons of added, removed, moved and changed sections, rows, seats and routes. Summarize capacity, accessible inventory, pricing, hold, product and revenue impact by category. Link each change to actor, timestamp, request, reason, approval and impacted performance. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `seatMapId` (navigation) |
| Route | `/access-venue/version-compare-bo-977` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From version | select field | — | — | — | — | Sends `?fromVersion=` (required); `seatMapId` is the path. | — |
| To version | select field | — | — | — | — | Sends `?toVersion=` (required). | — |

#### Outputs: what the screen shows and produces

**Shown**

**Seats** (metric tile, from `diffSeatMapVersions`)

| Shows | Format | Notes |
|---|---|---|
| Seat count before | 1,234 | — |
| Seat count after | 1,234 | — |

**Accessible seats** (metric tile, from `diffSeatMapVersions`)

| Shows | Format | Notes |
|---|---|---|
| Accessible seats before | 1,234 | — |
| Accessible seats after | 1,234 | Called out separately because it is a compliance number, not a capacity one. A reconfiguration that quietly loses two wheelchair spaces is … |

**Changed sections** (data table, from `diffSeatMapVersions`): The pack links each change to actor, timestamp, request, reason and approval; the diff does not.

| Shows | Format | Notes |
|---|---|---|
| Section | text | — |
| Seats before | 1,234 | — |
| Seats after | 1,234 | — |
| Summary | text | One sentence a person reads — *row H moved back two, two seats removed at the aisle.* |
| Actor | text | not in the schema: `Actor` |
| Timestamp | text | not in the schema: `Timestamp` |
| Reason | text | not in the schema: `Reason` |
| Approval | text | not in the schema: `Approval` |

**Added and removed sections** (detail panel, from `diffSeatMapVersions`)

| Shows | Format | Notes |
|---|---|---|
| From version | 1,234 | — |
| To version | 1,234 | — |
| Sections added | list or chips (count when long) | — |
| Sections removed | list or chips (count when long) | — |

**Where the user goes next**

- → `BO-973` Layout Command Center: *Back to Layout Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The version compare list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the version compare untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No version compare yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the version compare are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `diffSeatMapVersions` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: saved seat maps can be reused, copied in full, or partially copied (one section's layout/seating into another map); a template library and a layout version-comparison view show seat-count/configuration differences. *(agreed · MoM 21 Aug 2026, 4.4 AI-Assisted Seat Map Import & Layout/Template Management · DI-418)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-977` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-977`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 3
- Flow F276 *Seat Management Venue Mapping Reference v1.0 board 3: Layout Command Center*, step 8: Works in Version Compare → Review exact differences between layout versions before approval or rollback. Provide side-by-side and overlay comparisons of added, removed, moved and changed sections, rows, seats and routes. …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-977?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-973`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-978` Multi-Performance Assignment

**Assign approved layouts to one or many event performances. Provide calendar and grid views of event, date, venue, performance, assigned layout/version and status. Support bulk assignment, date range, recurrence, exception dates and different layouts across performances. Prevent assignment when a performance has incompatible sales, capacity, access or already-issued inventory. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `seatMapId` (navigation) |
| Route | `/access-venue/multi-performance-assignment-bo-978` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Draft · Validated · Published · Archived | `listSeatMaps` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish seat map (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listSeatMaps` (onLoad, Maps available)

**Where the user goes next**

- → `BO-973` Layout Command Center: *Back to Layout Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-performance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-performance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the multi-performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Validation failed. (ValidationProblem) |

#### Permissions

- `listSeatMaps` → `PRODUCT_VIEW` (read) · staff
- `publishSeatMap` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.13.3 | Seat Management APIs | Seat Management & Venue Mapping | CONTRACTED | `listSeatMaps` |
| 21.2.16 | One-Click Publishing | Seat Management & Venue Mapping | CONTRACTED | `publishSeatMap` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A seat map is configured independently, then associated with one or more events/performances on a separate event-configuration screen that links seat map, pricing and performance date-time. *(client request · MoM 21 Aug 2026, 4.5 Multi-Performance Assignment, Temporary Blocking & Tiered/Early-Bird Release · DI-419)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-978` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-978`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 3
- Flow F276 *Seat Management Venue Mapping Reference v1.0 board 3: Layout Command Center*, step 10: Works in Multi-Performance Assignment → Assign approved layouts to one or many event performances. Provide calendar and grid views of event, date, venue, performance, assigned layout/version and status. Support bulk assignment, date range …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-978?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish seat map, Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-973`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-979` Temporary Seat Blocking

**Temporarily remove seats from sale for production or operational reasons. Select section, row, seat or polygon on the map and define block type, reason, owner and effective period. Preview affected available, held, reserved and sold inventory with required remediation or approval. Support camera, equipment, safety, maintenance, sightline, house and event-production block categories. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 15**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/temporary-seat-blocking-bo-979` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Performance | picker: choose a performance | — | — | `listSeatHoldPools` ?performanceId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create seat hold pool (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listSeatHoldPools` (onLoad, What is blocked)

**Where the user goes next**

- → `BO-973` Layout Command Center: *Back to Layout Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The temporary seat blocking list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the temporary seat blocking untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No temporary seat blocking yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the temporary seat blocking are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `createSeatHoldPool` → `CAPACITY_CONFIGURE` (configure) · staff
- `listSeatHoldPools` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: inventory is released per section in tranches — temporary blocking (VIP/maintenance), scheduled release of held sections, and tiered/early-bird volumes (e.g. 30–40 of 100 seats at an early-bird price, then further tranches) — not full section capacity at go-live. *(agreed · MoM 21 Aug 2026, 4.5 Multi-Performance Assignment; 5. Key Decisions · DI-420)*
- Chinmay: reservations/holds are made section-wise (choose section → choose/hold seats within it), not by a freeform polygon selection as in the AI-generated reference mockup. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules & Social Distancing Configuration · DI-415)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-979` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-979`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 3
- Flow F276 *Seat Management Venue Mapping Reference v1.0 board 3: Layout Command Center*, step 12: Works in Temporary Seat Blocking → Temporarily remove seats from sale for production or operational reasons. Select section, row, seat or polygon on the map and define block type, reason, owner and effective period. Preview affected …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-979?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create seat hold pool, Cancel.
- [ ] Every transition is wired: `BO-973`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-980` Scheduled Seat Release

**Return temporarily blocked inventory to sale at a controlled time. Create release schedules by event, performance, hold/block type, seat set, time before event and condition. Preview release quantity, new capacity, pricing/category mapping and affected sales channels. Support reschedule, cancel, manual run, partial failure recovery and stakeholder notifications. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `poolId` (navigation) |
| Route | `/access-venue/scheduled-seat-release-bo-980` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Release seat hold pool (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listSeatHoldTypes` (onLoad, The release rules)

**Where the user goes next**

- → `BO-973` Layout Command Center: *Back to Layout Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The scheduled seat release list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the scheduled seat release untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No scheduled seat release yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the scheduled seat release are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `releaseSeatHoldPool` → `CAPACITY_CONFIGURE` (configure) · staff
- `listSeatHoldTypes` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: inventory is released per section in tranches — temporary blocking (VIP/maintenance), scheduled release of held sections, and tiered/early-bird volumes (e.g. 30–40 of 100 seats at an early-bird price, then further tranches) — not full section capacity at go-live. *(agreed · MoM 21 Aug 2026, 4.5 Multi-Performance Assignment; 5. Key Decisions · DI-420)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-980` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-980`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 3
- Flow F276 *Seat Management Venue Mapping Reference v1.0 board 3: Layout Command Center*, step 14: Works in Scheduled Seat Release → Return temporarily blocked inventory to sale at a controlled time. Create release schedules by event, performance, hold/block type, seat set, time before event and condition. Preview release …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-980?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Release seat hold pool, Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-973`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-981` Conflict & Impact Simulation

**Identify operational and commercial risk before a layout change becomes effective. Simulate seat removal, addition, movement, category change, stage change, route change and block/release actions. Calculate affected sold seats, holds, reservations, carts, products, access gates, capacity and forecast revenue. Provide resolution options such as reseating, alternative inventory, delayed release, refund workflow or rejected change. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/conflict-impact-simulation-bo-981` |

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

- → `BO-973` Layout Command Center: *Back to Layout Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The conflict impact simulation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the conflict impact simulation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No conflict impact simulation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the conflict impact simulation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `simulatePolicyConflictImpact` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-981` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-981`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 3
- Flow F276 *Seat Management Venue Mapping Reference v1.0 board 3: Layout Command Center*, step 16: Works in Conflict & Impact Simulation → Identify operational and commercial risk before a layout change becomes effective. Simulate seat removal, addition, movement, category change, stage change, route change and block/release actions. …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-981?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-973`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-982` Approval, Publish & Rollback

**Govern the complete release lifecycle for layout changes. Configure draft, review, operations, ticketing, finance and final approval stages by impact and venue policy. Schedule publication, notify dependent systems and verify synchronized version across channels. Maintain version history, failed-publication recovery, emergency unpublish and safe rollback with impact confirmation. Preserve version lineage and require impact analysis for every change affecting capacity, products, sold seats, holds, access routes or pricing. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 16 Board 4 - Seat Inventory, Status & Audit Figure 4. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work / Version 1.0 17**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CAPACITY_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `seatMapId` (navigation) |
| Route | `/access-venue/approval-publish-rollback-bo-982` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-973` Layout Command Center: *Back to Layout Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval publish rollback list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval publish rollback untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval publish rollback yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval publish rollback are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Validation failed. (ValidationProblem); 422 The input the kind needs is missing (`numberingScheme` for `numbering`, `stagePosition` for `stageVariant`), or the map has no focal zone for `categories` … |

#### Permissions

- `validateSeatMap` → `PRODUCT_VIEW` (read) · staff
- `publishSeatMap` → `CAPACITY_CONFIGURE` (configure) · staff
- `proposeSeatMapChanges` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.2.16 | One-Click Publishing | Seat Management & Venue Mapping | CONTRACTED | `publishSeatMap` |
| 1.4.23 | Event-Specific Configurations For multi-purpose venues, AI can: Create different seat maps for concerts, sports events, exhibitions, and conferences. Configure temporary seating arrangements. … | Ticketing Catalogue | CONTRACTED | `proposeSeatMapChanges` |
| 1.4.25 | Intelligent Seat Numbering Automatically assign row names (A, B, C, etc.) and seat numbers based on configurable rules. Validate numbering sequences and identify duplicates or missing seats. Apply … | Ticketing Catalogue | CONTRACTED | `proposeSeatMapChanges` |
| 1.4.26 | Seat Category Configuration AI can recommend seat categories based on: Distance from the stage or attraction. Viewing angles and sightlines. Elevation and seating tier. Historical sales performance. … | Ticketing Catalogue | CONTRACTED | `proposeSeatMapChanges` |
| 1.4.29 | Validation and Quality Assurance AI can automatically identify: Duplicate seat numbers. Missing rows or seats. Incorrect category assignments. Accessibility compliance issues. Capacity mismatches … | Ticketing Catalogue | CONTRACTED | `proposeSeatMapChanges` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-982` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS142 Seat Management Venue Mapping Reference v1.0 Board 3.dc.html#bo-982`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 3
- Flow F276 *Seat Management Venue Mapping Reference v1.0 board 3: Layout Command Center*, step 18: Works in Approval, Publish & Rollback → Govern the complete release lifecycle for layout changes. Configure draft, review, operations, ticketing, finance and final approval stages by impact and venue policy. Schedule publication, notify …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-982?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-973`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
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

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"cloneSeatMap": {"method":"POST","path":"/seat-maps/{seatMapId}/clone","contract":"seating","summary":"Clone a map, optionally into another venue","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SeatMap"},
"copySeatMapSection": {"method":"POST","path":"/seat-maps/{seatMapId}/sections/copy","contract":"seating","summary":"Copy one section into another map","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SeatMap"},
"createSeatHoldPool": {"method":"POST","path":"/seat-hold-pools","contract":"seating","summary":"Take a set of seats out of sale, for a reason, until a date","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SeatHoldPool","responds":"SeatHoldPool"},
"createSeatMapTemplate": {"method":"POST","path":"/seat-map-templates","contract":"seating","summary":"Save a map as a reusable template","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SeatMapTemplate"},
"decideProposedAction": {"method":"POST","path":"/proposed-actions/{actionId}/decide","contract":"ai","summary":"Approve or reject a proposal","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProposedAction"},
"diffSeatMapVersions": {"method":"GET","path":"/seat-maps/{seatMapId}/diff","contract":"seating","summary":"Compare two versions of a layout","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"fromVersion","in":"query","required":true},{"name":"toVersion","in":"query","required":true}],"requestBody":null,"responds":"SeatMapDiff"},
"getActionPlan": {"method":"GET","path":"/action-plans/{planId}","contract":"ai","summary":"A plan with its steps","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiActionPlanDetail"},
"getSeatMap": {"method":"GET","path":"/seat-maps/{seatMapId}","contract":"seating","summary":"Read a seat map with its structure","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"SeatMap"},
"listSeatHoldPools": {"method":"GET","path":"/seat-hold-pools","contract":"seating","summary":"Held seats, by pool, with what is left and when it releases","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"performanceId","in":"query","required":null}],"requestBody":null,"responds":"SeatHoldPool"},
"listSeatHoldTypes": {"method":"GET","path":"/seat-hold-types","contract":"seating","summary":"The kinds of hold a venue places, and who may release them","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"SeatHoldType"},
"listSeatMapTemplates": {"method":"GET","path":"/seat-map-templates","contract":"seating","summary":"List reusable layout templates","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"SeatMapTemplate"},
"listSeatMaps": {"method":"GET","path":"/seat-maps","contract":"seating","summary":"List seat maps","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"proposeSeatMapChanges": {"method":"POST","path":"/ai/seat-maps/{seatMapId}/proposals","contract":"ai","summary":"Propose changes to an existing seat map, as a plan a person approves","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiSeatMapProposal"},
"publishSeatMap": {"method":"POST","path":"/seat-maps/{seatMapId}/publish","contract":"seating","summary":"Validate and publish a seat map","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SeatMap"},
"releaseSeatHoldPool": {"method":"POST","path":"/seat-hold-pools/{poolId}/release","contract":"seating","summary":"Put held seats back on sale, convert them, or reassign them","permission":"CAPACITY_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SeatHoldPool"},
"simulatePolicyConflictImpact": {"method":"PUT","path":"/policy-conflict-impact","contract":"access","summary":"Policy Simulation, Conflict & Impact Analysis","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PolicySimulationConflictImpactAnalysisInput","responds":"PolicySimulationConflictImpactAnalysisView"},
"validateSeatMap": {"method":"POST","path":"/seat-maps/{seatMapId}/validate","contract":"seating","summary":"Run validation without publishing","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationReport"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiActionPlan": {"type":"object","x-ticvai-persistence":"ai.action_plan","description":"**A plan: plan, validate, simulate, approve, execute, with rollback** (design 2.2 D, 3.8; AIC-086..107). Independent of any conversation (AIC-102). Its steps are `ai.action_step`; the change set is hashed so what was approved is what runs (AIC-181).","required":["origin","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"origin":{"type":"string","enum":["configurationSession","generateConfiguration","assistant","riskCase","operationalRequirement","rollback"]},"originRef":{"type":"string","nullable":true},"summary":{"type":"string"},"status":{"type":"string","enum":["draft","validated","simulated","awaitingApproval","approved","executing","paused","completed","partiallyCompleted","failed","compensated","cancelled","rolledBack"],"readOnly":true},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"},"approvalTier":{"type":"integer","minimum":1,"maximum":2,"description":"The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). Not an autonomy level."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request, where tier 2 or the matrix caught the plan."},"proposedActionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.proposed_action","description":"The `ai.proposed_action` the plan is presented as for a decision."},"changeSetHash":{"type":"string","readOnly":true},"governanceOutcome":{"allOf":[{"$ref":"#/components/schemas/AiGovernanceOutcome"}],"readOnly":true},"policyVersionRef":{"type":"string","readOnly":true,"description":"The governance policy version that decided it."},"simulation":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4)."},"partialCompletionAllowed":{"type":"boolean","default":false,"description":"Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134)."},"rollbackOfPlanId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.action_plan"},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiActionPlanDetail": {"type":"object","x-ticvai-persistence":"none — ai.action_plan with its ai.action_step rows","description":"A plan with its steps in DAG order.","required":["plan","steps"],"properties":{"plan":{"$ref":"#/components/schemas/AiActionPlan"},"steps":{"type":"array","items":{"$ref":"#/components/schemas/AiActionStep"}}}},
"AiActionStep": {"type":"object","x-ticvai-persistence":"ai.action_step","description":"One step of a plan: a registered tool against `targetContract.targetOperation` at a contract version (AIC-095), with payload, provenance, compensation and the idempotency key `plan:{id}:step:{n}`. **Scoped through its plan** (`platform.apply_parent_rls`). Each step records its target object's version; drift pauses the plan (AIC-182).","required":["planId","stepNumber","toolKey","targetContract","targetOperation","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"planId":{"type":"string","format":"uuid","x-ticvai-references":"ai.action_plan"},"stepNumber":{"type":"integer","minimum":1},"dependsOn":{"type":"array","items":{"type":"integer","minimum":1},"description":"Step numbers that must succeed first. The plan is a DAG."},"toolKey":{"type":"string"},"targetContract":{"type":"string"},"targetOperation":{"type":"string"},"contractVersion":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body of `targetOperation`, validated against it before the plan is approved."},"provenance":{"$ref":"#/components/schemas/AiProvenance"},"idempotencyKey":{"type":"string","readOnly":true},"targetObjectRef":{"type":"string","nullable":true},"targetObjectVersion":{"type":"string","nullable":true,"description":"The version the step was planned against. A different version at execution is drift."},"reversible":{"type":"boolean"},"compensation":{"type":"object","additionalProperties":true,"nullable":true},"status":{"type":"string","enum":["pending","validated","running","succeeded","failed","compensated","skipped","paused"],"readOnly":true},"attempts":{"type":"integer","minimum":0,"maximum":3,"readOnly":true,"description":"Bounded at 3 (AIC-135)."},"lastError":{"type":"string","nullable":true,"readOnly":true},"resultRef":{"type":"string","nullable":true,"readOnly":true,"description":"The owning service's response: success is its answer, not a model's judgement (AIC-097)."},"startedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"AiSeatMapProposal": {"type":"object","x-ticvai-persistence":"none — the plan is ai.action_plan and ai.action_step, presented as one ai.proposed_action; the findings are the evidence of its decision record","description":"What `proposeSeatMapChanges` proposed: findings with the seats they concern, and except for `consistency` the plan a person approves (1.4.23, 1.4.25, 1.4.26, 1.4.29).","required":["kind","findings"],"properties":{"kind":{"type":"string","enum":["categories","numbering","stageVariant","consistency"]},"seatMapId":{"type":"string","format":"uuid"},"planId":{"type":"string","format":"uuid","nullable":true,"description":"The `ai.action_plan`, readable with `getActionPlan`. Null for `consistency`."},"proposedActionId":{"type":"string","format":"uuid","nullable":true,"description":"The `ai.proposed_action` a person decides. Null for `consistency`."},"summary":{"type":"object","additionalProperties":true,"description":"Counts: seats re-categorised or relabelled, seats blocked, capacity by category before and after."},"findings":{"type":"array","items":{"type":"object","required":["code","severity"],"properties":{"code":{"type":"string","description":"e.g. `accessibleSeatWithoutAccessiblePrice`, `restrictedViewInPremium`, `companionWithoutWheelchairSpace`, `sightLineLost`, `behindStage`, `numberingGap`, `duplicateLabel`, `categoryChange`, `labelChange`."},"severity":{"type":"string","enum":["blocking","warning","info"]},"seatIds":{"type":"array","items":{"type":"string","format":"uuid"}},"sectionId":{"type":"string","format":"uuid","nullable":true},"current":{"type":"string","nullable":true},"proposed":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true}}}},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"decisionRecordId":{"type":"string","format":"uuid"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Point": {"type":"object","required":["x","y"],"properties":{"x":{"type":"number"},"y":{"type":"number"}}},
"PolicySimulationConflictImpactAnalysisInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Policy Simulation, Conflict & Impact Analysis submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"policyId":{"type":"string"},"policyVersion":{"type":"string"},"scenarioTime":{"type":"string","format":"date-time","description":"Simulated moment of the scan"},"credentialId":{"type":"string","description":"Optional credential to simulate"},"runSavedScenarios":{"type":"boolean","description":"Regression: run saved scenarios against this policy version"},"scenarioCount":{"type":"integer"},"passedCount":{"type":"integer"},"changedOutcomeCount":{"type":"integer"},"affectedCredentials":{"type":"integer"}},"required":["policyId"]},
"PolicySimulationConflictImpactAnalysisView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Policy Simulation, Conflict & Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"policyId":{"type":"string"},"occupancy":{"type":"integer","description":"Occupancy (the pack shows 82%)"},"policiesInvolved":{"type":"array","items":{"type":"string"},"description":"policies involved"},"hierarchy":{"type":"string","description":"hierarchy"},"priority":{"type":"integer","description":"priority"},"resultingDecision":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"],"description":"resulting decision"},"affectedProducts":{"type":"integer","description":"affected products"},"affectedVenues":{"type":"integer","description":"affected venues"},"estimatedGuestsImpacted":{"type":"integer","description":"estimated guests impacted"},"policyVersion":{"type":"string"},"scenarioTime":{"type":"string","format":"date-time","description":"Simulated moment of the scan"},"credentialId":{"type":"string","description":"Optional credential to simulate"},"runSavedScenarios":{"type":"boolean","description":"Regression: run saved scenarios against this policy version"},"scenarioCount":{"type":"integer"},"passedCount":{"type":"integer"},"changedOutcomeCount":{"type":"integer"},"affectedCredentials":{"type":"integer"}},"required":["policyId"]},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"SeatHoldPool": {"type":"object","x-ticvai-persistence":"seating.hold_pool","description":"Board 6.3. **Utilisation decides next season's allocation.**","required":["holdTypeId","performanceId"],"properties":{"id":{"type":"string","format":"uuid"},"holdTypeId":{"type":"string","format":"uuid"},"performanceId":{"type":"string","format":"uuid"},"seatIds":{"type":"array","items":{"type":"string","format":"uuid"}},"seatCount":{"type":"integer","readOnly":true},"usedCount":{"type":"integer","readOnly":true},"releasedCount":{"type":"integer","readOnly":true},"holderName":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"releaseAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["active","partiallyReleased","released","expired"]},"createdBy":{"type":"string","format":"uuid"},"scopePath":{"type":"string"}}},
"SeatHoldType": {"type":"object","x-ticvai-persistence":"seating.hold_type","description":"Board 6.2. **A hold with no release rule becomes a permanent hole in the map.**","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"purpose":{"type":"string","enum":["production","house","accessibility","press","sponsor","contractual","maintenance","distancing"]},"ownerRole":{"type":"string","nullable":true},"releaseRule":{"type":"string","enum":["manual","hoursBeforePerformance","onDate","onSelloutThreshold"],"default":"hoursBeforePerformance"},"releaseHoursBefore":{"type":"integer","nullable":true},"releaseTo":{"type":"string","enum":["generalSale","anotherPool","remainsHeld"],"default":"generalSale"},"countsAgainstCapacity":{"type":"boolean","default":true,"description":"**Whether held seats are still \"sold out\".** A production hold that reads as availability puts a show on sale it cannot honour.\n"},"visibleToGuest":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"SeatMap": {"x-ticvai-persistence":"seating.seat_map","allOf":[{"$ref":"#/components/schemas/SeatMapSummary"},{"type":"object","required":["sections"],"properties":{"description":{"type":"string","nullable":true},"viewBox":{"type":"object","description":"Coordinate space for rendering. Absent when there is no geometry.","nullable":true,"properties":{"width":{"type":"number"},"height":{"type":"number"}}},"stagePosition":{"$ref":"#/components/schemas/Point"},"sections":{"type":"array","items":{"$ref":"#/components/schemas/Section"}},"isActive":{"type":"boolean"}}}]},
"SeatMapDiff": {"type":"object","description":"**A diff a person can read, not 396 changed cells.** `Seating_Manifest_1.xlsx` is 396 rows and a comparison that lists every one is noise — *row H moved back two* is what a venue manager needs, and it only exists if the diff understands sections and rows rather than treating a map as a grid of values.\n\n**Counts first, then the shape, then the detail.** A reconfiguration is judged on whether the house got bigger or smaller before anything else.","required":["fromVersion","toVersion","seatCountBefore","seatCountAfter"],"properties":{"fromVersion":{"type":"integer"},"toVersion":{"type":"integer"},"seatCountBefore":{"type":"integer"},"seatCountAfter":{"type":"integer"},"sectionsAdded":{"type":"array","items":{"type":"string"}},"sectionsRemoved":{"type":"array","items":{"type":"string"}},"sectionsChanged":{"type":"array","items":{"type":"object","properties":{"section":{"type":"string"},"seatsBefore":{"type":"integer"},"seatsAfter":{"type":"integer"},"summary":{"type":"string","description":"**One sentence a person reads** — *row H moved back two, two seats removed at the aisle.*"}}}},"accessibleSeatsBefore":{"type":"integer","nullable":true},"accessibleSeatsAfter":{"type":"integer","nullable":true,"description":"**Called out separately because it is a compliance number, not a capacity one.** A reconfiguration that quietly loses two wheelchair spaces is the change nobody notices in a seat count."}}},
"SeatMapStatus": {"type":"string","enum":["draft","validated","published","archived"]},
"SeatMapSummary": {"x-ticvai-persistence":"seating.seat_map","type":"object","required":["id","name","venueId","status","seatCount"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/SeatMapStatus"},"seatCount":{"type":"integer"},"sectionCount":{"type":"integer"},"hasGeometry":{"type":"boolean","description":"False when only a manifest has been imported. Such a map can be sold from a list but not rendered.\n"},"publishedAt":{"type":"string","format":"date-time","nullable":true}}},
"SeatMapTemplate": {"x-ticvai-persistence":"seating.seat_map_template","type":"object","required":["id","name","seatCount","sectionCount"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"seatCount":{"type":"integer"},"sectionCount":{"type":"integer"},"hasGeometry":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"}}},
"Section": {"x-ticvai-persistence":"seating.section","type":"object","required":["code","name","rowCount","seatCount"],"properties":{"code":{"type":"string"},"name":{"type":"string"},"rowCount":{"type":"integer"},"seatCount":{"type":"integer"},"boundary":{"type":"array","items":{"$ref":"#/components/schemas/Point"},"description":"Polygon for rendering. Absent without geometry."},"viewAssetId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"assets.MediaAsset","description":"**The view of the stage from this section, as a photo**, uploaded through `assets` like any other media (decided 29 September, rev 3 23SEP-14). Optional: where it is null the client renders the view from the imported geometry (the section `boundary`, the map's `stagePosition` and the seat positions), so a closer section shows a larger stage and fewer rows ahead. Set with `updateSeatMap` `sectionViews`, which is allowed on a published map because a photo does not change the map's shape.\n"},"rows":{"type":"array","items":{"type":"object","required":["label","seatCount"],"properties":{"label":{"type":"string"},"seatCount":{"type":"integer"},"numberingDirection":{"type":"string","enum":["leftToRight","rightToLeft"],"description":"Which end row numbering starts from. Not recoverable from a manifest and must be stated — it determines whether a guest finds their seat.\n"}}}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"ValidationFinding": {"x-ticvai-persistence":"none — computed","type":"object","required":["kind","severity","message"],"properties":{"kind":{"$ref":"#/components/schemas/ValidationFindingKind"},"severity":{"$ref":"#/components/schemas/ValidationSeverity"},"message":{"type":"string"},"sectionCode":{"type":"string","nullable":true},"rowLabel":{"type":"string","nullable":true},"seatNumbers":{"type":"array","items":{"type":"string"}},"affectedCount":{"type":"integer"}}},
"ValidationReport": {"x-ticvai-persistence":"none — computed","type":"object","required":["seatMapId","passed","errorCount","warningCount","findings"],"properties":{"seatMapId":{"type":"string","format":"uuid"},"passed":{"type":"boolean","description":"False when any finding has severity `error`."},"errorCount":{"type":"integer"},"warningCount":{"type":"integer"},"findings":{"type":"array","items":{"$ref":"#/components/schemas/ValidationFinding"}}}}
}
```
