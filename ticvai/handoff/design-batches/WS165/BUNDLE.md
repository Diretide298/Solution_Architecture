# WS165 — Seat Management Venue Mapping Reference v1.0 board 1

**10 screens · 14 operations · 22 schemas · 3 permissions**

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
  `ASSET_LIBRARY_MANAGE, CAPACITY_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `BO-953` | Seat Map Command Center | B–D | 0 | 0 | 6 | 1 | 4 | 6 | — | notStarted (—) |
| `BO-954` | Venue Canvas | B–D | 0 | 0 | 6 | 3 | 3 | 0 | — | notStarted (—) |
| `BO-955` | Sections & Zones | B–D | 7 | 0 | 6 | 2 | 2 | 0 | — | notStarted (—) |
| `BO-956` | Rows & Seats | B–D | 0 | 0 | 6 | 9 | 2 | 6 | — | notStarted (—) |
| `BO-957` | Standing Zones | B–D | 0 | 0 | 6 | 0 | 3 | 0 | — | notStarted (—) |
| `BO-958` | Suites & Boxes | B–D | 0 | 0 | 6 | 0 | 3 | 0 | — | notStarted (—) |
| `BO-959` | Stage & Focal Point | B–D | 0 | 0 | 6 | 4 | 0 | 0 | — | notStarted (—) |
| `BO-960` | Entrances, Exits & Aisles | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-961` | Amenities & Obstructions | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-962` | Templates, Validation & Publish | B–D | 0 | 0 | 6 | 3 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-953, BO-954, BO-956, BO-957, BO-958, BO-959, BO-960, BO-961 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-953` Seat Map Command Center

**Provide a role-specific overview of every venue map and its operational readiness. Show total venues, active maps, seats, sections, capacity, drafts, approvals, validation errors and upcoming layout changes. Filter and compare by tenant, brand, region, venue, map type, status, owner and last-published date. Open recent maps, validation alerts, approval tasks and impacted performances directly from the dashboard. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/seat-map-command-center-bo-953` |

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

**Data it reads**: `listSeatMaps` (onLoad, List seat maps); `listSeatMapTemplates` (onLoad, List reusable layout templates)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-954` Venue Canvas: *Venue Canvas*
- → `BO-955` Sections & Zones: *Sections & Zones*
- → `BO-956` Rows & Seats: *Rows & Seats*
- → `BO-957` Standing Zones: *Standing Zones*
- → `BO-958` Suites & Boxes: *Suites & Boxes*
- → `BO-959` Stage & Focal Point: *Stage & Focal Point*
- → `BO-960` Entrances, Exits & Aisles: *Entrances, Exits & Aisles*
- → `BO-961` Amenities & Obstructions: *Amenities & Obstructions*
- → `BO-962` Templates, Validation & Publish: *Templates, Validation & Publish*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The seat map list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the seat map untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No seat map yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the seat map are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listSeatMaps` → `PRODUCT_VIEW` (read) · staff
- `listSeatMapTemplates` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.13.3 | Seat Management APIs | Seat Management & Venue Mapping | CONTRACTED | `listSeatMaps` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Movie/cinema ticketing is in scope through the seat management module (e.g. a Kuwait museum's educational cinema: assigned seats, a film, a time slot). *(agreed · MoM 14 Aug 2026, 5. Movie Ticketing · DI-286)*
- Chinmay: near-term AI can generate a map/seating layout and the related ticket configuration once a venue uploads its map schema and layout image. *(client request · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-281)*
- Qossai: AI-assisted layout generation from AutoCAD/DXF (best) or PDF (fallback, via OCR), targeting ~90–95% automation with the client correcting the rest; sample input is a PDF seating diagram plus an Excel manifest of section/row/seat numbers. *(agreed · MoM 5 Aug 2026, 9. Seat Mapping & Venue Builder · DI-145)*
- A one-time, canvas-based venue/seat-map builder is required per venue. *(agreed · MoM 5 Aug 2026, 9. Seat Mapping & Venue Builder · DI-144)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-953` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-953`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 1
- Flow F274 *Seat Management Venue Mapping Reference v1.0 board 1: Seat Map Command Center*, step 1: Opens Seat Map Command Center → Provide a role-specific overview of every venue map and its operational readiness. Show total venues, active maps, seats, sections, capacity, drafts, approvals, validation errors and upcoming layout …
- Flow F274 *Seat Management Venue Mapping Reference v1.0 board 1: Seat Map Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F274 *Seat Management Venue Mapping Reference v1.0 board 1: Seat Map Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F274 *Seat Management Venue Mapping Reference v1.0 board 1: Seat Map Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F274 *Seat Management Venue Mapping Reference v1.0 board 1: Seat Map Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F274 *Seat Management Venue Mapping Reference v1.0 board 1: Seat Map Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F274 *Seat Management Venue Mapping Reference v1.0 board 1: Seat Map Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F274 *Seat Management Venue Mapping Reference v1.0 board 1: Seat Map Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F274 branch at step 1 (expected): when Nothing has been set up on Seat Map Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F274 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-953?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-954`, `BO-955`, `BO-956`, `BO-957`, `BO-958`, `BO-959`, `BO-960`, `BO-961`, `BO-962`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-954` Venue Canvas

**Provide the primary drag-and-drop workspace for constructing a venue map. Offer components for section, row, seat, standing zone, suite, stage, entrance, exit, aisle, facility, obstruction and label. Support zoom, pan, snap-to-grid, rulers, coordinates, layers, alignment, grouping, undo/redo and background- reference controls. Configure venue name, dimensions, unit, scale, orientation, origin, focal point and canvas boundaries in a properties inspector. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/venue-canvas-bo-954` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create seat map (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-953` Seat Map Command Center: *Back to Seat Map Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue canvas list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue canvas untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue canvas yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the venue canvas are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Structural change attempted on a published map |

#### Permissions

- `getSeatMap` → `PRODUCT_VIEW` (read) · staff
- `createSeatMap` → `CAPACITY_CONFIGURE` (configure) · staff
- `updateSeatMap` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.8 | The system should allow sales of a seating map selection and easy, flexible space design set-up/configuration, both in full graphical display. | Ticketing Catalogue | CONTRACTED | `createSeatMap` |
| 1.3.9 | The system should allow a seating plan to be created for each space. Different type of seats can be configured within the seating plan and a space can have multiple seating arrangements. The system … | Ticketing Catalogue | CONTRACTED | `createSeatMap` |
| 21.3.4 | Layout Versioning | Seat Management & Venue Mapping | CONTRACTED | `updateSeatMap` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Open: how the seat map builder consolidates the reference tool's separate screens (canvas, standing zone, suite, best-seats, entrances/exits) into one unified screen — Chinmay's team to confirm. *(open · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types (action) · DI-413)*
- Decision: section type (seated / non-seated-zone / standing / suite) is an attribute set at section level within ONE seat map builder screen, not separate configuration screens per type as in the reference tool. *(agreed · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types · DI-412)*
- One seat map can mix section types — e.g. 8 of 10 sections seated and 2 standing ("fan pit" near the stage); suites sell either as a private bulk-priced suite or as individual seats within the suite. *(agreed · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types · DI-411)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-954` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-954`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 1
- Flow F274 *Seat Management Venue Mapping Reference v1.0 board 1: Seat Map Command Center*, step 2: Works in Venue Canvas → Provide the primary drag-and-drop workspace for constructing a venue map. Offer components for section, row, seat, standing zone, suite, stage, entrance, exit, aisle, facility, obstruction and label. …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-954?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create seat map, Cancel.
- [ ] Every transition is wired: `BO-953`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-955` Sections & Zones

**Define the commercial and operational hierarchy of the venue. Create, draw and edit section or zone polygons with name, code, level, capacity, color, category and parent hierarchy. Support curved, rectangular, freeform and imported boundaries with duplication, alignment and bulk-property updates. Configuration Scope of Work / Version 1.0 5 Map sections to pricing, access gates, sales channels, accessibility attributes and reporting dimensions. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `seating` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `CAPACITY_CONFIGURE`, `PRODUCT_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `seatMapId` (navigation), `uploadId` (navigation) |
| Route | `/access-venue/sections-zones-bo-955` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| View from this section | file upload | — | — | — | — | **An optional photo per section** (decided 29 September, rev 3 23SEP-14): the view a guest sees on the seat map when they pick the section. Uploaded to the asset library (`createUpload`, then … | — |

**Sent by *Save section views*** (`updateSeatMap`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateSeatMap` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `updateSeatMap` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateSeatMap` body |
| Section views `sectionViews` | repeatable rows | optional | — | — | — | Set or clear the view photo of one or more sections (`Section.viewAssetId`, decided 29 September, rev 3 23SEP-14). | `updateSeatMap` body |
| Section code `sectionViews[].sectionCode` | text field | required | — | — | — | — | `updateSeatMap` body |
| View image `sectionViews[].viewAssetId` | upload, or pick from the media library | required | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `updateSeatMap` body |

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save map zones (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Save section views (secondary button) | `updateSeatMap` PATCH `/seat-maps/{seatMapId}` | inline | SeatMap | 409 Structural change attempted on a published map | — |

**Where the user goes next**

- → `BO-953` Seat Map Command Center: *Back to Seat Map Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sections zones list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sections zones untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sections zones yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the sections zones are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes.; 409 Structural change attempted on a published map; 409 The transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is larger than the ticket allowed … (UploadRefusedProblem) |

#### Permissions

- `getSeatMap` → `PRODUCT_VIEW` (read) · staff
- `setMapZones` → `CAPACITY_CONFIGURE` (configure) · staff
- `updateSeatMap` → `CAPACITY_CONFIGURE` (configure) · staff
- `createUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `completeUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.3.4 | Layout Versioning | Seat Management & Venue Mapping | CONTRACTED | `updateSeatMap` |
| 23.1.4 | Authorized users shall upload assets individually or in bulk through web interfaces and APIs. | Digital Asset Management | CONTRACTED | `createUpload` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Open: how the seat map builder consolidates the reference tool's separate screens (canvas, standing zone, suite, best-seats, entrances/exits) into one unified screen — Chinmay's team to confirm. *(open · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types (action) · DI-413)*
- Decision: section type (seated / non-seated-zone / standing / suite) is an attribute set at section level within ONE seat map builder screen, not separate configuration screens per type as in the reference tool. *(agreed · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types · DI-412)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-955` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-955`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 1
- Flow F274 *Seat Management Venue Mapping Reference v1.0 board 1: Seat Map Command Center*, step 4: Works in Sections & Zones → Define the commercial and operational hierarchy of the venue. Create, draw and edit section or zone polygons with name, code, level, capacity, color, category and parent hierarchy. Support curved …

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-955?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save map zones, Cancel, Save section views.
- [ ] Every transition is wired: `BO-953`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-956` Rows & Seats

**Build and maintain numbered rows and individual seat positions at scale. Generate straight, curved, radial or custom rows using seat count, spacing, radius, angle, direction and offset parameters. Configure seat number, label, type, category, coordinate, status default, accessibility, view quality and amenity attributes. Support bulk add, renumber, reverse, insert, remove, copy, align and spacing changes with collision and duplicate detection. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/rows-seats-bo-956` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save seats (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-953` Seat Map Command Center: *Back to Seat Map Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rows seats list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rows seats untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rows seats yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rows seats are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Map is published and the change is structural |

#### Permissions

- `listSeats` → `PRODUCT_VIEW` (read) · staff
- `updateSeats` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.4.7 | Seat Audit Trail | Seat Management & Venue Mapping | CONTRACTED | `listSeats` |
| 21.4.8 | Seat History | Seat Management & Venue Mapping | CONTRACTED | `listSeats` |
| 21.13.5 | Seat Audit Logs | Seat Management & Venue Mapping | CONTRACTED | `listSeats` |
| 1.4.30 | Bulk Configuration and Updates AI can: Apply seat categories to thousands of seats simultaneously. Update pricing zones across multiple venues. Clone and modify existing seat maps. Generate … | Ticketing Catalogue | CONTRACTED | `updateSeats` |
| 21.1.1 | Drag & Drop Venue Builder | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |
| 21.1.2 | Section Builder | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |
| 21.1.3 | Row Builder | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |
| 21.1.4 | Seat Builder | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |
| 21.2.15 | Manual Adjustment Layer | Seat Management & Venue Mapping | CONTRACTED | `updateSeats` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Open: how the seat map builder consolidates the reference tool's separate screens (canvas, standing zone, suite, best-seats, entrances/exits) into one unified screen — Chinmay's team to confirm. *(open · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types (action) · DI-413)*
- A one-time, canvas-based venue/seat-map builder is required per venue. *(agreed · MoM 5 Aug 2026, 9. Seat Mapping & Venue Builder · DI-144)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-956` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-956`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 1
- Flow F274 *Seat Management Venue Mapping Reference v1.0 board 1: Seat Map Command Center*, step 6: Works in Rows & Seats → Build and maintain numbered rows and individual seat positions at scale. Generate straight, curved, radial or custom rows using seat count, spacing, radius, angle, direction and offset parameters. …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-956?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save seats, Cancel.
- [ ] Every transition is wired: `BO-953`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-957` Standing Zones

**Configure non-assigned areas with controlled capacity and density. Draw standing, general-admission, pit, dance-floor or hospitality zones and assign type, capacity, density and color. Calculate capacity from area and approved density while allowing an authorized lower operating limit. Associate entrances, exits, age rules, access products, pricing bands and event-specific restrictions. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/standing-zones-bo-957` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save map zones (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-953` Seat Map Command Center: *Back to Seat Map Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The standing zones list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the standing zones untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No standing zones yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the standing zones are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setMapZones` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Open: how the seat map builder consolidates the reference tool's separate screens (canvas, standing zone, suite, best-seats, entrances/exits) into one unified screen — Chinmay's team to confirm. *(open · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types (action) · DI-413)*
- Decision: section type (seated / non-seated-zone / standing / suite) is an attribute set at section level within ONE seat map builder screen, not separate configuration screens per type as in the reference tool. *(agreed · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types · DI-412)*
- One seat map can mix section types — e.g. 8 of 10 sections seated and 2 standing ("fan pit" near the stage); suites sell either as a private bulk-priced suite or as individual seats within the suite. *(agreed · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types · DI-411)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-957` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-957`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 1
- Flow F274 *Seat Management Venue Mapping Reference v1.0 board 1: Seat Map Command Center*, step 8: Works in Standing Zones → Configure non-assigned areas with controlled capacity and density. Draw standing, general-admission, pit, dance-floor or hospitality zones and assign type, capacity, density and color. Calculate …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-957?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save map zones, Cancel.
- [ ] Every transition is wired: `BO-953`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-958` Suites & Boxes

**Model suites, boxes and hospitality spaces as sellable seating inventory. Create suites and boxes with code, capacity, internal seat layout, standing allowance, amenities and accessibility attributes. Support whole-suite, per-seat, shared and configurable sales models with linked products and price categories. Maintain owner, contract, allocation, entrance, service area and operational-status references without duplicating CRM or contract data. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 6**

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
| Route | `/access-venue/suites-boxes-bo-958` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save map zones (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-953` Seat Map Command Center: *Back to Seat Map Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The suites boxes list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the suites boxes untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No suites boxes yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the suites boxes are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setMapZones` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Open: how the seat map builder consolidates the reference tool's separate screens (canvas, standing zone, suite, best-seats, entrances/exits) into one unified screen — Chinmay's team to confirm. *(open · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types (action) · DI-413)*
- Decision: section type (seated / non-seated-zone / standing / suite) is an attribute set at section level within ONE seat map builder screen, not separate configuration screens per type as in the reference tool. *(agreed · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types · DI-412)*
- One seat map can mix section types — e.g. 8 of 10 sections seated and 2 standing ("fan pit" near the stage); suites sell either as a private bulk-priced suite or as individual seats within the suite. *(agreed · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types · DI-411)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-958` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-958`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 1
- Flow F274 *Seat Management Venue Mapping Reference v1.0 board 1: Seat Map Command Center*, step 10: Works in Suites & Boxes → Model suites, boxes and hospitality spaces as sellable seating inventory. Create suites and boxes with code, capacity, internal seat layout, standing allowance, amenities and accessibility …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-958?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save map zones, Cancel.
- [ ] Every transition is wired: `BO-953`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-959` Stage & Focal Point

**Define the viewing focal point and production footprint used by seating logic. Add stage, field, screen, court, track or custom focal areas with position, dimensions, rotation, height and event- specific variant. Configure one or multiple focal points for distance, orientation, best-seat and closest-to-stage calculations. Preview sightline coverage, obstructed areas and seats affected by production structures before publication. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/stage-focal-point-bo-959` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save map zones (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-953` Seat Map Command Center: *Back to Seat Map Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The stage focal point list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the stage focal point untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No stage focal point yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the stage focal point are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 The input the kind needs is missing (`numberingScheme` for `numbering`, `stagePosition` for `stageVariant`), or the map has no focal zone for `categories` … |

#### Permissions

- `setMapZones` → `CAPACITY_CONFIGURE` (configure) · staff
- `proposeSeatMapChanges` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-959` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-959`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 1
- Flow F274 *Seat Management Venue Mapping Reference v1.0 board 1: Seat Map Command Center*, step 12: Works in Stage & Focal Point → Define the viewing focal point and production footprint used by seating logic. Add stage, field, screen, court, track or custom focal areas with position, dimensions, rotation, height and event- …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-959?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save map zones, Cancel.
- [ ] Every transition is wired: `BO-953`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-960` Entrances, Exits & Aisles

**Map circulation elements used by access, accessibility and safety operations. Create entrances, exits, gates, portals, vomitories, concourses, stairways and aisles with unique identifiers and attributes. Define width, direction, level, connected zones, access-control device, accessible status and emergency designation. Validate disconnected zones, blocked paths, minimum aisle width and route continuity against configured venue rules. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/entrances-exits-aisles-bo-960` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save map zones (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-953` Seat Map Command Center: *Back to Seat Map Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The entrances exits aisles list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the entrances exits aisles untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No entrances exits aisles yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the entrances exits aisles are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setMapZones` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Open: how the seat map builder consolidates the reference tool's separate screens (canvas, standing zone, suite, best-seats, entrances/exits) into one unified screen — Chinmay's team to confirm. *(open · MoM 21 Aug 2026, 4.2 Seat Map Builder — Section Types (action) · DI-413)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-960` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-960`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 1
- Flow F274 *Seat Management Venue Mapping Reference v1.0 board 1: Seat Map Command Center*, step 14: Works in Entrances, Exits & Aisles → Map circulation elements used by access, accessibility and safety operations. Create entrances, exits, gates, portals, vomitories, concourses, stairways and aisles with unique identifiers and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-960?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save map zones, Cancel.
- [ ] Every transition is wired: `BO-953`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-961` Amenities & Obstructions

**Add guest facilities, service points and view-affecting objects to the venue map. Place restrooms, concessions, bars, first aid, merchandise, lifts, escalators, information, prayer and accessibility facilities. Map pillars, cameras, speaker arrays, lighting trusses, barriers and production structures with obstruction type and dimensions. Expose approved amenity and view attributes to filters, seat previews, operations and accessibility routing. Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history.**

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
| Route | `/access-venue/amenities-obstructions-bo-961` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save map zones (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-953` Seat Map Command Center: *Back to Seat Map Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The amenities obstructions list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the amenities obstructions untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No amenities obstructions yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the amenities obstructions are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setMapZones` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-961` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-961`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 1
- Flow F274 *Seat Management Venue Mapping Reference v1.0 board 1: Seat Map Command Center*, step 16: Works in Amenities & Obstructions → Add guest facilities, service points and view-affecting objects to the venue map. Place restrooms, concessions, bars, first aid, merchandise, lifts, escalators, information, prayer and accessibility …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-961?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save map zones, Cancel.
- [ ] Every transition is wired: `BO-953`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-962` Templates, Validation & Publish

**Govern reusable venue templates and release a map only when it is operationally complete. Create, classify, clone, archive and reuse venue templates while preserving lineage and ownership. Run checks for geometry, capacity, duplicate numbering, overlaps, missing routes, accessibility, sightlines and dependent products. Provide draft, review, approval, scheduled publication, preview, version comparison and rollback with impact confirmation. Configuration Scope of Work / Version 1.0 7 Version geometry and property changes, enforce venue-scoped permissions, validate affected capacity and preserve before/after audit evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the immutable audit history. Configuration Scope of Work / Version 1.0 8 Board 2 - AI Seat Map Import & Designer Figure 2. High-definition configuration board with all 10 screens. Visual reference: information architecture and configuration coverage; detailed production behavior is defined in the following scope. Configuration Scope of Work / Version 1.0 9**

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
| Route | `/access-venue/templates-validation-publish-bo-962` |

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
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listSeatMapTemplates` (onLoad, Templates to start from)

**Where the user goes next**

- → `BO-953` Seat Map Command Center: *Back to Seat Map Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The templates validation publish list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the templates validation publish untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No templates validation publish yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the templates validation publish are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Validation failed. (ValidationProblem) |

#### Permissions

- `listSeatMapTemplates` → `PRODUCT_VIEW` (read) · staff
- `createSeatMapTemplate` → `CAPACITY_CONFIGURE` (configure) · staff
- `validateSeatMap` → `PRODUCT_VIEW` (read) · staff
- `publishSeatMap` → `CAPACITY_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.1.9 | Venue Template Management | Seat Management & Venue Mapping | CONTRACTED | `createSeatMapTemplate` |
| 21.3.1 | Layout Templates | Seat Management & Venue Mapping | CONTRACTED | `createSeatMapTemplate` |
| 21.2.16 | One-Click Publishing | Seat Management & Venue Mapping | CONTRACTED | `publishSeatMap` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A one-time, canvas-based venue/seat-map builder is required per venue. *(agreed · MoM 5 Aug 2026, 9. Seat Mapping & Venue Builder · DI-144)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-962` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS140 Seat Management Venue Mapping Reference v1.0 Board 1.dc.html#bo-962`
- Workshop pack: Seat_Management_Venue_Mapping_Reference v1.0.pdf board 1
- Flow F274 *Seat Management Venue Mapping Reference v1.0 board 1: Seat Map Command Center*, step 18: Works in Templates, Validation & Publish → Govern reusable venue templates and release a map only when it is operationally complete. Create, classify, clone, archive and reuse venue templates while preserving lineage and ownership. Run checks …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-962?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create seat map template, Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-953`.
- [ ] Every gated control is gated: `CAPACITY_CONFIGURE`, `PRODUCT_VIEW`.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**19 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"completeUpload": {"method":"POST","path":"/media/uploads/{uploadId}/complete","contract":"assets","summary":"Confirm an upload and create the asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaAsset"},
"createSeatMap": {"method":"POST","path":"/seat-maps","contract":"seating","summary":"Create a seat map","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CreateSeatMapRequest","responds":"SeatMap"},
"createSeatMapTemplate": {"method":"POST","path":"/seat-map-templates","contract":"seating","summary":"Save a map as a reusable template","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SeatMapTemplate"},
"createUpload": {"method":"POST","path":"/media/uploads","contract":"assets","summary":"Request a signed upload URL","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"UploadTicket"},
"getSeatMap": {"method":"GET","path":"/seat-maps/{seatMapId}","contract":"seating","summary":"Read a seat map with its structure","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"SeatMap"},
"listSeatMapTemplates": {"method":"GET","path":"/seat-map-templates","contract":"seating","summary":"List reusable layout templates","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"SeatMapTemplate"},
"listSeatMaps": {"method":"GET","path":"/seat-maps","contract":"seating","summary":"List seat maps","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSeats": {"method":"GET","path":"/seat-maps/{seatMapId}/seats","contract":"seating","summary":"List seats in a map","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"sectionCode","in":"query","required":null},{"name":"rowLabel","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"attribute","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"proposeSeatMapChanges": {"method":"POST","path":"/ai/seat-maps/{seatMapId}/proposals","contract":"ai","summary":"Propose changes to an existing seat map, as a plan a person approves","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiSeatMapProposal"},
"publishSeatMap": {"method":"POST","path":"/seat-maps/{seatMapId}/publish","contract":"seating","summary":"Validate and publish a seat map","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SeatMap"},
"setMapZones": {"method":"PUT","path":"/seat-maps/{seatMapId}/zones","contract":"seating","summary":"Standing areas, suites, stages and obstructions","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MapZone"},
"updateSeatMap": {"method":"PATCH","path":"/seat-maps/{seatMapId}","contract":"seating","summary":"Rename or amend a seat map","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SeatMap"},
"updateSeats": {"method":"PATCH","path":"/seat-maps/{seatMapId}/seats","contract":"seating","summary":"Bulk-amend seats","permission":"CAPACITY_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"BulkUpdateSeatsRequest","responds":null},
"validateSeatMap": {"method":"POST","path":"/seat-maps/{seatMapId}/validate","contract":"seating","summary":"Run validation without publishing","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationReport"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiSeatMapProposal": {"type":"object","x-ticvai-persistence":"none — the plan is ai.action_plan and ai.action_step, presented as one ai.proposed_action; the findings are the evidence of its decision record","description":"What `proposeSeatMapChanges` proposed: findings with the seats they concern, and except for `consistency` the plan a person approves (1.4.23, 1.4.25, 1.4.26, 1.4.29).","required":["kind","findings"],"properties":{"kind":{"type":"string","enum":["categories","numbering","stageVariant","consistency"]},"seatMapId":{"type":"string","format":"uuid"},"planId":{"type":"string","format":"uuid","nullable":true,"description":"The `ai.action_plan`, readable with `getActionPlan`. Null for `consistency`."},"proposedActionId":{"type":"string","format":"uuid","nullable":true,"description":"The `ai.proposed_action` a person decides. Null for `consistency`."},"summary":{"type":"object","additionalProperties":true,"description":"Counts: seats re-categorised or relabelled, seats blocked, capacity by category before and after."},"findings":{"type":"array","items":{"type":"object","required":["code","severity"],"properties":{"code":{"type":"string","description":"e.g. `accessibleSeatWithoutAccessiblePrice`, `restrictedViewInPremium`, `companionWithoutWheelchairSpace`, `sightLineLost`, `behindStage`, `numberingGap`, `duplicateLabel`, `categoryChange`, `labelChange`."},"severity":{"type":"string","enum":["blocking","warning","info"]},"seatIds":{"type":"array","items":{"type":"string","format":"uuid"}},"sectionId":{"type":"string","format":"uuid","nullable":true},"current":{"type":"string","nullable":true},"proposed":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true}}}},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"decisionRecordId":{"type":"string","format":"uuid"}}},
"BulkUpdateSeatsRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["selection"],"properties":{"selection":{"type":"object","description":"Seats to amend. Combine filters; an empty selection is rejected.","properties":{"seatIds":{"type":"array","items":{"type":"string"}},"sectionCodes":{"type":"array","items":{"type":"string"}},"rowLabels":{"type":"array","items":{"type":"string"}}}},"categoryId":{"type":"string","format":"uuid"},"attribute":{"$ref":"#/components/schemas/SeatAttribute"},"isActive":{"type":"boolean"}}},
"CreateSeatMapRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","venueId"],"properties":{"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"description":{"type":"string","maxLength":1000},"templateId":{"type":"string","format":"uuid","description":"Create from a template rather than empty."}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MapZone": {"type":"object","x-ticvai-persistence":"seating.zone","description":"BL-166. **`seating` is strong on everything that is a seat and the map itself was only seats.**\n**A standing area is a capacity without individual seats**, and modelling it as seats means inventing seat numbers nobody prints and a guest cannot find. A suite is the opposite — one sellable unit containing many seats, sold whole.\nNon-sellable zones matter too: **a stage, an entry and a sightline obstruction are not inventory and they change what the seats beside them are worth.**\n","required":["id","seatMapId","kind","name"],"properties":{"id":{"type":"string","format":"uuid"},"seatMapId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["standing","suite","box","lounge","accessiblePlatform","stage","entry","exit","concourse","obstruction","camera","aisle"]},"name":{"type":"string"},"capacity":{"type":"integer","nullable":true,"description":"**For a standing zone this is the inventory** — sold as a count rather than as seats. Null for a stage or an obstruction, which sell nothing.\n"},"seatCategoryId":{"type":"string","format":"uuid","nullable":true},"containsSeatIds":{"type":"array","description":"For a suite or box. **Sold whole, so the seats inside are held together** — selling one seat of a suite is not a thing a venue does.\n","items":{"type":"string","format":"uuid"}},"obstructsZoneIds":{"type":"array","description":"What this blocks the view of. **A pillar is not inventory and it decides what the seats behind it are worth**, which is the only reason to draw it.\n","items":{"type":"string","format":"uuid"}},"geometry":{"type":"string","nullable":true}}},
"MediaAsset": {"x-ticvai-persistence":"assets.media_asset","type":"object","required":["id","kind","status","filename","contentType","sizeBytes","referenceCount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MediaKind"},"status":{"$ref":"#/components/schemas/MediaStatus"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"title":{"$ref":"#/components/schemas/LocalisedText"},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Required before use in a guest-facing surface. WCAG 2.2 AA."},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"durationSeconds":{"type":"number","nullable":true},"customMetadata":{"type":"object","nullable":true,"additionalProperties":true,"description":"BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"},"sharedWithTenantIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"},"tags":{"type":"array","items":{"type":"string"}},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"url":{"type":"string","description":"Signed and expiring for private assets; stable CDN URL for public ones."},"thumbnailUrl":{"type":"string","nullable":true},"referenceCount":{"type":"integer","description":"How many surfaces reference this asset. Non-zero refuses deletion.\n"},"rights":{"$ref":"#/components/schemas/MediaRights"},"isRightsExpired":{"type":"boolean"},"version":{"type":"integer"},"uploadedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"MediaKind": {"type":"string","enum":["image","video","audio","document","vector","font","archive"]},
"MediaRights": {"x-ticvai-persistence":"none — embedded in asset","type":"object","description":"Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item.\n","properties":{"licenceKind":{"type":"string","enum":["owned","royaltyFree","rightsManaged","creativeCommons","editorialOnly","unknown"]},"licensor":{"type":"string","nullable":true},"licenceReference":{"type":"string","nullable":true},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"permittedUses":{"type":"array","items":{"type":"string","enum":["web","print","socialMedia","inVenue","advertising","internal"]}},"attributionRequired":{"type":"boolean","default":false},"attributionText":{"type":"string","nullable":true},"permittedTerritories":{"type":"array","items":{"type":"string"},"description":"ISO country or region codes. **Empty means unrestricted, which is a claim rather than an absence** — an unknown territory and a worldwide licence are not the same thing, and `licenceKind: unknown` is how the second is said.\n"},"permittedChannels":{"type":"array","items":{"type":"string"},"description":"Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route.\n"},"modelReleaseHeld":{"type":"boolean","default":false},"renewalOwner":{"type":"string","format":"uuid","nullable":true}}},
"MediaStatus": {"type":"string","enum":["processing","ready","quarantined","failed","archived"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Point": {"type":"object","required":["x","y"],"properties":{"x":{"type":"number"},"y":{"type":"number"}}},
"Seat": {"x-ticvai-persistence":"seating.seat","type":"object","required":["id","sectionCode","rowLabel","seatNumber","attribute"],"properties":{"id":{"type":"string","format":"uuid","description":"**Stable for the life of the seat.** Section, row and number are display labels that change on a refit; this does not. A ticket sold today must still resolve after a renumbering.\n"},"sectionCode":{"type":"string"},"rowLabel":{"type":"string"},"seatNumber":{"type":"string"},"displayLabel":{"type":"string","description":"What the guest sees, e.g. `A2-7-11`."},"position":{"allOf":[{"$ref":"#/components/schemas/Point"}],"nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"attribute":{"$ref":"#/components/schemas/SeatAttribute"},"companionSeatIds":{"type":"array","items":{"type":"string"},"description":"Present on accessible seats. Sold together, released together."},"isActive":{"type":"boolean"}}},
"SeatAttribute": {"type":"string","description":"BL-168. **Extended from eight values on 18 August.** Amenity and view filters needed attributes the original set did not carry, and a guest filtering for *aisle seat with power* was filtering on something the model could not express.\n","enum":["standard","accessible","companion","obstructedView","restrictedLegroom","premium","houseSeat","buffer","aisle","endOfRow","extraLegroom","powerOutlet","tableService","shaded","covered","nearExit","nearAccessibleWc","wheelchairTransfer","limitedRecline","sofa","beanbag"]},
"SeatMap": {"x-ticvai-persistence":"seating.seat_map","allOf":[{"$ref":"#/components/schemas/SeatMapSummary"},{"type":"object","required":["sections"],"properties":{"description":{"type":"string","nullable":true},"viewBox":{"type":"object","description":"Coordinate space for rendering. Absent when there is no geometry.","nullable":true,"properties":{"width":{"type":"number"},"height":{"type":"number"}}},"stagePosition":{"$ref":"#/components/schemas/Point"},"sections":{"type":"array","items":{"$ref":"#/components/schemas/Section"}},"isActive":{"type":"boolean"}}}]},
"SeatMapStatus": {"type":"string","enum":["draft","validated","published","archived"]},
"SeatMapSummary": {"x-ticvai-persistence":"seating.seat_map","type":"object","required":["id","name","venueId","status","seatCount"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/SeatMapStatus"},"seatCount":{"type":"integer"},"sectionCount":{"type":"integer"},"hasGeometry":{"type":"boolean","description":"False when only a manifest has been imported. Such a map can be sold from a list but not rendered.\n"},"publishedAt":{"type":"string","format":"date-time","nullable":true}}},
"SeatMapTemplate": {"x-ticvai-persistence":"seating.seat_map_template","type":"object","required":["id","name","seatCount","sectionCount"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"seatCount":{"type":"integer"},"sectionCount":{"type":"integer"},"hasGeometry":{"type":"boolean"},"createdAt":{"type":"string","format":"date-time"}}},
"Section": {"x-ticvai-persistence":"seating.section","type":"object","required":["code","name","rowCount","seatCount"],"properties":{"code":{"type":"string"},"name":{"type":"string"},"rowCount":{"type":"integer"},"seatCount":{"type":"integer"},"boundary":{"type":"array","items":{"$ref":"#/components/schemas/Point"},"description":"Polygon for rendering. Absent without geometry."},"viewAssetId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"assets.MediaAsset","description":"**The view of the stage from this section, as a photo**, uploaded through `assets` like any other media (decided 29 September, rev 3 23SEP-14). Optional: where it is null the client renders the view from the imported geometry (the section `boundary`, the map's `stagePosition` and the seat positions), so a closer section shows a larger stage and fewer rows ahead. Set with `updateSeatMap` `sectionViews`, which is allowed on a published map because a photo does not change the map's shape.\n"},"rows":{"type":"array","items":{"type":"object","required":["label","seatCount"],"properties":{"label":{"type":"string"},"seatCount":{"type":"integer"},"numberingDirection":{"type":"string","enum":["leftToRight","rightToLeft"],"description":"Which end row numbering starts from. Not recoverable from a manifest and must be stated — it determines whether a guest finds their seat.\n"}}}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"UploadTicket": {"x-ticvai-persistence":"assets.media_upload","type":"object","required":["uploadId","uploadUrl","method","expiresAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"uploadId":{"type":"string","format":"uuid"},"uploadUrl":{"type":"string","description":"Signed. PUT the file here, then confirm with `/complete`."},"method":{"type":"string","enum":["PUT","POST"]},"headers":{"type":"object","additionalProperties":{"type":"string"}},"maxSizeBytes":{"type":"integer"},"expiresAt":{"type":"string","format":"date-time"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"venueId":{"type":"string","format":"uuid","nullable":true},"assetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The asset this upload became — created by `completeUpload`, or the asset whose file `replaceMediaAsset` swapped. Null while the transfer is outstanding.\n"}}},
"ValidationFinding": {"x-ticvai-persistence":"none — computed","type":"object","required":["kind","severity","message"],"properties":{"kind":{"$ref":"#/components/schemas/ValidationFindingKind"},"severity":{"$ref":"#/components/schemas/ValidationSeverity"},"message":{"type":"string"},"sectionCode":{"type":"string","nullable":true},"rowLabel":{"type":"string","nullable":true},"seatNumbers":{"type":"array","items":{"type":"string"}},"affectedCount":{"type":"integer"}}},
"ValidationReport": {"x-ticvai-persistence":"none — computed","type":"object","required":["seatMapId","passed","errorCount","warningCount","findings"],"properties":{"seatMapId":{"type":"string","format":"uuid"},"passed":{"type":"boolean","description":"False when any finding has severity `error`."},"errorCount":{"type":"integer"},"warningCount":{"type":"integer"},"findings":{"type":"array","items":{"$ref":"#/components/schemas/ValidationFinding"}}}}
}
```
