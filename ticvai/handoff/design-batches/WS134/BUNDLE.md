# WS134 — F&B Backend Structure Module Sample Reference v1.0 board 1

**7 screens · 11 operations · 22 schemas · 5 permissions**

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
  `ORDER_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, REPORT_VIEW_VENUE, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-727` | F&B Command Center | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-728` | Outlet Management | B–D | 0 | 0 | 6 | 0 | 3 | 0 | — | notStarted (—) |
| `BO-729` | Create / Edit Outlet | B–D | 0 | 0 | 6 | 0 | 3 | 0 | — | notStarted (—) |
| `BO-730` | Outlet Types & Templates | B–D | 10 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-731` | Operating Hours & Service Periods | B–D | 0 | 0 | 6 | 3 | 1 | 0 | — | notStarted (—) |
| `BO-732` | POS & Device Assignment | B–D | 0 | 2 | 6 | 0 | 3 | 0 | — | notStarted (—) |
| `BO-733` | Service Channel Configuration | B–D | 0 | 22 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-728, BO-729, BO-730, BO-731, BO-732, BO-733 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-727` F&B Command Center

**F&B Command Center**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Operations · wave 3 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Top KPI cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/operations/f-b-command-center-bo-727` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Shop · Restaurant · Bar · Cafe · Kiosk · Game floor · Ticket office · Mobile | `listOutlets` ?kind |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Today's Sales** (metric tile)

**Orders Today** (metric tile)

**Average Order Value** (metric tile)

**Open Outlets** (metric tile)

**Active POS** (metric tile)

**Orders in Preparation** (metric tile)

**Average Preparation Time** (metric tile)

**Unavailable Items** (metric tile)

**Critical Stock Alerts** (metric tile)

**Operational Alerts** (metric tile)

**Data it reads**: `listOutlets` (onLoad, F&B outlets)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-728` Outlet Management: *Outlet Management*
- → `BO-729` Create / Edit Outlet: *Create / Edit Outlet*
- → `BO-730` Outlet Types & Templates: *Outlet Types & Templates*
- → `BO-731` Operating Hours & Service Periods: *Operating Hours & Service Periods*
- → `BO-732` POS & Device Assignment: *POS & Device Assignment*
- → `BO-733` Service Channel Configuration: *Service Channel Configuration*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The record list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the record untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No record yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the record are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listOutlets` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** F&B dashboards are role-based: the F&B Director sees all outlets, an outlet manager sees only their own outlet. Detailed design of the role-based dashboards (Director vs. outlet-level roles) is still to be finalised. *(open · MoM 18 Aug 2026, 4.10 F&B Stock, Wastage & Requisitions; 6. Open Items · DI-318)*
- F&B Command Center gives a real-time consolidated view across all outlets: total sales, orders, average order value, average preparation time, kitchen load, top-selling items, operational alerts, food cost and gross margin, with breakdowns by sales channel and by hour. *(client request · MoM 18 Aug 2026, 4.1 F&B Command Center — Overview & Outlet Setup; 4.10 F&B Stock, Wastage & Requisitions · DI-317)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-727` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-727`
- Workshop pack: F&B_Backend_Structure_Module Sample Reference v1.0.pdf board 1
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 1: Opens F&B Command Center → F&B Command Center
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F243 branch at step 1 (expected): when Nothing has been set up on F&B Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F243 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-727?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-728`, `BO-729`, `BO-730`, `BO-731`, `BO-732`, `BO-733`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-728` Outlet Management

**Outlet Management**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Operations · wave 3 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/operations/outlet-management-bo-728` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Shop · Restaurant · Bar · Cafe · Kiosk · Game floor · Ticket office · Mobile | `listOutlets` ?kind |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listOutlets` (onLoad, List outlets)

**Where the user goes next**

- → `BO-727` F&B Command Center: *Back to F&B Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The outlet list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the outlet untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No outlet yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the outlet are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listOutlets` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Retail store setup reuses the F&B department/venue/zone structure with department type "Retail" and the shop as a sub-department; retail needs no sub-classification (unlike fine dining vs. QSR) since operations are scan-and-sell. Inventory stays outlet-level. *(agreed · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-350)*
- Decision: F&B configuration (menus, recipes, costing, inventory) is managed at outlet level, and Retail follows the same segregation. Venue-owned homogeneous outlets (e.g. popcorn/ice-cream booths) may be set up centrally once and applied across outlets, but the model stays outlet-level. *(agreed · MoM 18 Aug 2026, 4.5 Outlet-Level vs. Venue-Level Configuration — Key Discussion · DI-330)*
- Outlets are categorised by type (fine dining, quick service, coffee, etc.), each type switching features on or off — e.g. quick-service outlets need no table booking, fine-dining outlets need a table layout. Each outlet is linked to a department (Food & Beverage), sub-department (outlet name), cost centre and status. *(client request · MoM 18 Aug 2026, 4.1 F&B Command Center — Overview & Outlet Setup · DI-319)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-728` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-728`
- Workshop pack: F&B_Backend_Structure_Module Sample Reference v1.0.pdf board 1
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 2: Works in Outlet Management → Outlet Management

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-728?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-727`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-729` Create / Edit Outlet

**Create / Edit Outlet**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Operations · wave 3 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `outletId` (BO-727), `tableId` (navigation) · cold entry: Opened from BO-727 with the outlet picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says … |
| Route | `/operations/create-edit-outlet-bo-729` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Outlet | picker: choose an outlet | — | — | `listMenus` ?outletId |
| Active at | date and time picker | — | — | `listMenus` ?activeAt |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create table (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listMenus` (onLoad, Menus)

**Where the user goes next**

- → `BO-727` F&B Command Center: *Back to F&B Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The create edit outlet list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the create edit outlet untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No create edit outlet yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the create edit outlet are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 409 A visit is open on the table (names the visit), or the new `label` is already used by another table in this venue (`duplicate-code`, audit R108). |

#### Permissions

- `listMenus` → `PRODUCT_VIEW` (read) · staff
- `createTable` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateTable` → `PRODUCT_CONFIGURE` (configure) · staff
- `setSectionLayout` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Retail store setup reuses the F&B department/venue/zone structure with department type "Retail" and the shop as a sub-department; retail needs no sub-classification (unlike fine dining vs. QSR) since operations are scan-and-sell. Inventory stays outlet-level. *(agreed · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-350)*
- Operating hours and service periods (breakfast, lunch, dinner, late night) are defined per outlet so revenue can be analysed by time slot. Recipe-based stock depletion is set per outlet, real-time or end-of-day, by outlet type. *(client request · MoM 18 Aug 2026, 4.2 Recipes, Operating Hours & Service Channels · DI-320)*
- Outlets are categorised by type (fine dining, quick service, coffee, etc.), each type switching features on or off — e.g. quick-service outlets need no table booking, fine-dining outlets need a table layout. Each outlet is linked to a department (Food & Beverage), sub-department (outlet name), cost centre and status. *(client request · MoM 18 Aug 2026, 4.1 F&B Command Center — Overview & Outlet Setup · DI-319)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-729` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-729`
- Workshop pack: F&B_Backend_Structure_Module Sample Reference v1.0.pdf board 1
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 4: Works in Create / Edit Outlet → Create / Edit Outlet

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 409, 412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-729?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create table, Cancel.
- [ ] Every transition is wired: `BO-727`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-730` Outlet Types & Templates

**Outlet Types & Templates**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Operations · wave 3 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/operations/outlet-types-templates-bo-730` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Outlet | picker: choose an outlet | — | — | `listMenus` ?outletId |
| Active at | date and time picker | — | — | `listMenus` ?activeAt |
| Outlet type | radio group | — | Restaurant · Bar · Cafe · Kiosk · Mobile | `listOutletTemplates` ?outletType |
| Include inactive | toggle | off | — | `listOutletTemplates` ?includeInactive |

**Sent by *+ Create Template*** (`setOutletTemplate`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64; pattern `^[A-Za-z0-9_-]+$` | — | — | `setOutletTemplate` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setOutletTemplate` body |
| Outlet type `outletType` | radio group | required | — | Restaurant · Bar · Cafe · Kiosk · Mobile | — | The F&B kinds of `tenancy.OutletKind`, repeated here because a satellite does not reference another contract's schema. | `setOutletTemplate` body |
| Service model `serviceModel` | multi-select chips | required | — | Quick service · Table service · Room service · Collection · Delivery; at least 1 | — | The service modes the outlet offers, e.g. `[tableService, collection]`. | `setOutletTemplate` body |
| Default menus `defaultMenuIds` | multi-picker: choose default menus | optional | — | at most 20 | — | — | `setOutletTemplate` body |
| Course rules `courseRules` | group | optional | — | — | — | The coursing default a new outlet starts with; the same shape `setCourseRules` stores per outlet. | `setOutletTemplate` body |
| Default coursing `courseRules.defaultCoursing` | radio group | optional | — | Fire and forget · Hold and fire · Phased · Timed · Delayed | — | How a ticket's courses are fired. `fireAndForget` sends every course at once, which is no coursing; `holdAndFire` waits for a server to call each course; `timed` fires on a clock … | `setOutletTemplate` body |
| Kitchen sla minutes `kitchenSlaMinutes` | number field (minutes) | optional | — | min 1; max 240 | — | The default ticket target, in minutes, before `setKitchenSla` sets per-mode targets. | `setOutletTemplate` body |
| Delivery policy `deliveryPolicyId` | picker: choose a delivery policy | optional | — | — | shows names, sends the id | — | `setOutletTemplate` body |
| Is active `isActive` | toggle | optional | on | — | — | — | `setOutletTemplate` body |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| + Create Template (primary button) | `setOutletTemplate` PUT `/outlet-templates` | OutletTemplateInput | OutletTemplate | 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.; 422 A `defaultMenuIds` entry that is not an active menu at this venue (`unknownMenu`), or a … | — |

**Data it reads**: `listMenus` (onLoad, Menu items); `listOutletTemplates` (onLoad, The outlet templates)

**Where the user goes next**

- → `BO-727` F&B Command Center: *Back to F&B Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The outlet types templates list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the outlet types templates untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No outlet types templates yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the outlet types templates are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A `defaultMenuIds` entry that is not an active menu at this venue (`unknownMenu`), or a `deliveryPolicyId` that does not exist (`unknownDeliveryPolicy`). |

#### Permissions

- `listMenus` → `PRODUCT_VIEW` (read) · staff
- `listOutletTemplates` → `PRODUCT_VIEW` (read) · staff
- `setOutletTemplate` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Decision: F&B configuration (menus, recipes, costing, inventory) is managed at outlet level, and Retail follows the same segregation. Venue-owned homogeneous outlets (e.g. popcorn/ice-cream booths) may be set up centrally once and applied across outlets, but the model stays outlet-level. *(agreed · MoM 18 Aug 2026, 4.5 Outlet-Level vs. Venue-Level Configuration — Key Discussion · DI-330)*
- Outlets are categorised by type (fine dining, quick service, coffee, etc.), each type switching features on or off — e.g. quick-service outlets need no table booking, fine-dining outlets need a table layout. Each outlet is linked to a department (Food & Beverage), sub-department (outlet name), cost centre and status. *(client request · MoM 18 Aug 2026, 4.1 F&B Command Center — Overview & Outlet Setup · DI-319)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-730` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-730`
- Workshop pack: F&B_Backend_Structure_Module Sample Reference v1.0.pdf board 1
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 6: Works in Outlet Types & Templates → Outlet Types & Templates

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (400, 403, 412, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-730?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: + Create Template.
- [ ] Every transition is wired: `BO-727`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-731` Operating Hours & Service Periods

**Operating Hours & Service Periods**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Operations · wave 3 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/operations/operating-hours-service-periods-bo-731` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Station | picker: choose a station | — | — | `listKitchenTickets` ?stationId |
| Status | select | — | Received · Preparing · Ready · Served · Recalled · Cancelled | `listKitchenTickets` ?status |
| Course | number field | — | min 1 | `listKitchenTickets` ?course |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listKitchenTickets` (onLoad, Kitchen operations)

**Where the user goes next**

- → `BO-727` F&B Command Center: *Back to F&B Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operating hours service list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operating hours service untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operating hours service yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the operating hours service are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listKitchenTickets` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.6.20 | The system should be able to create a new Check with table numbers and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants). | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.6.21 | The system should be able to send order information consisting of table number and guest count and added items with condiments to multiple parts of the restaurant with additional prints (being … | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |
| 4.7.1 | The system should be able to create a new Check with table and guest numbers, add items to print in kitchen or on QSR(Quick service restaurants), void items and ensure they don't appear in kitchen. | Bundles and Promotions | CONTRACTED | `listKitchenTickets` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Operating hours and service periods (breakfast, lunch, dinner, late night) are defined per outlet so revenue can be analysed by time slot. Recipe-based stock depletion is set per outlet, real-time or end-of-day, by outlet type. *(client request · MoM 18 Aug 2026, 4.2 Recipes, Operating Hours & Service Channels · DI-320)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-731` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-731`
- Workshop pack: F&B_Backend_Structure_Module Sample Reference v1.0.pdf board 1
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 8: Works in Operating Hours & Service Periods → Operating Hours & Service Periods

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-731?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-727`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-732` POS & Device Assignment

**POS & Device Assignment**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Operations · wave 3 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Device cards/table) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/operations/pos-device-assignment-bo-732` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Shop · Restaurant · Bar · Cafe · Kiosk · Game floor · Ticket office · Mobile | `listOutlets` ?kind |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every pos device** (data table)

| Shows | Format | Notes |
|---|---|---|
| Terminal outlet type cashier payment printer status | text | not in the schema: `Terminal Outlet Type Cashier Payment Printer Status` |

**The selected pos device** (detail panel): The pack groups this record's detail under its own headings: “Main”, “Restaurant”, “I would also display”.

| Shows | Format | Notes |
|---|---|---|
| Terminal outlet type cashier payment printer status | text | not in the schema: `Terminal Outlet Type Cashier Payment Printer Status` |

**Data it reads**: `listOutlets` (onLoad, Outlet configuration)

**Where the user goes next**

- → `BO-727` F&B Command Center: *Back to F&B Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pos device list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pos device untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pos device yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pos device are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listOutlets` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Device directory: search and add devices (printers, scanners, customer displays, cash drawers, turnstiles, handhelds, mobile POS) capturing serial number, type and model; adding generates a secure enrolment code; devices are assigned to workstations (e.g. A has ticket printer, receipt printer and cash drawer). *(client request · MoM 15 Sep 2026, 4.3 Device Management - Registration, Enrollment & Workstation Assignment · DI-892)*
- Retail POS/device assignment covers workstation name/code, receipt printer, barcode scanner and cash drawer; global retail settings include sales channels, primary/replenishment store and offline sales support. *(client request · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-352)*
- POS & device management configures receipt printers, kitchen printers and KDS devices per outlet/terminal. *(client request · MoM 18 Aug 2026, 4.2 Recipes, Operating Hours & Service Channels · DI-321)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-732` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-732`
- Workshop pack: F&B_Backend_Structure_Module Sample Reference v1.0.pdf board 1
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 10: Works in POS & Device Assignment → POS & Device Assignment

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-732?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-727`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-733` Service Channel Configuration

**Service Channel Configuration**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Operations · wave 3 · needs the `fnb` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `REPORT_VIEW_VENUE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/operations/service-channel-configuration-bo-733` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

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

**Service channels** (data table): POS Counter, Dine-In, QR Table Order, Mobile App, B2C Web, Kiosk, Takeaway, Delivery, VIP / Hospitality, Event Catering. The bound read is `getKpiValues`, which carries no channel configuration.

| Shows | Format | Notes |
|---|---|---|
| Channel | text | not in the schema: `Channel` |
| Status | text | not in the schema: `Status` |
| Available outlets | text | not in the schema: `Available outlets` |
| Menu | text | not in the schema: `Menu` |
| Price book | text | not in the schema: `Price book` |
| Payment | text | not in the schema: `Payment` |
| Guest login | text | not in the schema: `Guest login` |
| Operating hours | text | not in the schema: `Operating hours` |
| Maximum items per order | text | not in the schema: `Maximum items per order` |
| Minimum order | text | not in the schema: `Minimum order` |

**The selected channel rules** (detail panel): The pack's QR Table Ordering example (page 10).

| Shows | Format | Notes |
|---|---|---|
| Status | text | not in the schema: `Status` |
| Available outlets | text | not in the schema: `Available outlets` |
| Menu | text | not in the schema: `Menu` |
| Price book | text | not in the schema: `Price book` |
| Payment | text | not in the schema: `Payment` |
| Guest login | text | not in the schema: `Guest login` |
| Operating hours | text | not in the schema: `Operating hours` |
| Maximum items per order | text | not in the schema: `Maximum items per order` |
| Minimum order | text | not in the schema: `Minimum order` |

**Orders by channel** (metric tile, from `getKpiValues`): The only use `getKpiValues` has here; needs a per-channel KPI code, which is not seeded.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |

**Data it reads**: `getKpiValues` (onLoad, F&B performance)

**Where the user goes next**

- → `BO-727` F&B Command Center: *Back to F&B Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The service channel list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the service channel untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No service channel yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the service channel are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `setFnbReservationPolicy` → `PRODUCT_CONFIGURE` (configure) · staff
- `setFnbServiceChargePolicy` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Service channel configuration enables/disables specific items per sales channel (POS, kiosk, QR ordering, online) per outlet. *(client request · MoM 18 Aug 2026, 4.2 Recipes, Operating Hours & Service Channels · DI-322)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-733` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS57 F&B Backend Structure Module Sample Reference v1.0 Board 1.dc.html#bo-733`
- Workshop pack: F&B_Backend_Structure_Module Sample Reference v1.0.pdf board 1
- Flow F243 *F&B Backend Structure Module Sample Reference v1.0 board 1: F&B Command Center*, step 12: Works in Service Channel Configuration → Service Channel Configuration

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 412).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-733?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-727`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `REPORT_VIEW_VENUE`.
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

**15 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createTable": {"method":"POST","path":"/tables","contract":"fnb","summary":"A table as a thing, not an inference","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TableDefinition","responds":"TableDefinition"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"listKitchenTickets": {"method":"GET","path":"/kitchen/tickets","contract":"fnb","summary":"Kitchen ticket queue","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"stationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"course","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMenus": {"method":"GET","path":"/menus","contract":"fnb","summary":"List menus","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":"activeAt","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOutletTemplates": {"method":"GET","path":"/outlet-templates","contract":"fnb","summary":"List outlet templates","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletType","in":"query","required":false},{"name":"includeInactive","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOutlets": {"method":"GET","path":"/outlets","contract":"tenancy","summary":"List outlets","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"Outlet"},
"setFnbReservationPolicy": {"method":"PUT","path":"/reservation-policy","contract":"fnb","summary":"Set turn times and seating buffers","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"FnbReservationPolicy","responds":"FnbReservationPolicy"},
"setFnbServiceChargePolicy": {"method":"PUT","path":"/service-charge-policy","contract":"fnb","summary":"Set the service charge","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"FnbServiceChargePolicy","responds":"FnbServiceChargePolicy"},
"setOutletTemplate": {"method":"PUT","path":"/outlet-templates","contract":"fnb","summary":"Create or replace an outlet template","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"OutletTemplateInput","responds":"OutletTemplate"},
"setSectionLayout": {"method":"PUT","path":"/outlets/{outletId}/sections","contract":"fnb","summary":"Divide the floor into sections and give each a server","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"SectionLayout","responds":"SectionLayout"},
"updateTable": {"method":"PUT","path":"/tables/{tableId}","contract":"fnb","summary":"Change what a table is","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"TableDefinition","responds":"TableDefinition"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AllergenCode": {"type":"string","description":"**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n","enum":["gluten","crustaceans","eggs","fish","peanuts","soybeans","milk","nuts","celery","mustard","sesame","sulphites","lupin","molluscs"]},
"CoursingPolicy": {"type":"string","description":"How a ticket's courses are fired. `fireAndForget` sends every course at once, which is no coursing; `holdAndFire` waits for a server to call each course; `timed` fires on a clock; `phased` staggers by course. **One vocabulary for the ticket (`KitchenTicket.coursing`) and the outlet default (`CourseRules.defaultCoursing`)** — the default said `none` for `fireAndForget` and had no `delayed` until 26 September, so a default could not be copied onto the field it defaults.\n","enum":["fireAndForget","holdAndFire","phased","timed","delayed"]},
"FnbReservationPolicy": {"type":"object","x-ticvai-persistence":"fnb.reservation_policy","description":"**How long a table is held, and what sits between one seating and the next.** The source of `TableReservation.durationMinutes`, which keeps its own value as the snapshot.","required":["defaultTurnMinutes","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"Null is the venue default; an outlet's own policy overrides it."},"defaultTurnMinutes":{"type":"integer","minimum":15,"description":"The turn time when no party-size band matches."},"turnTimeBands":{"type":"array","description":"**Turn time by party size** — a two-top and a table of eight do not turn at the same speed, and a single default is how a restaurant ends up double-booking its large tables. The first band whose range contains the party size wins.","items":{"type":"object","required":["fromPartySize","turnMinutes"],"properties":{"fromPartySize":{"type":"integer","minimum":1},"toPartySize":{"type":"integer","nullable":true,"description":"Null means no upper bound."},"turnMinutes":{"type":"integer","minimum":15}}}},"seatingBufferMinutes":{"type":"integer","minimum":0,"default":0,"description":"**The reset between seatings** — clearing, laying and a moment for the floor. Zero is a legitimate answer and a stated one."},"maximumDurationMinutes":{"type":"integer","nullable":true,"description":"**The ceiling on a single booking.** A reservation extended by hand past this needs the manager, because the table after it is somebody else's booking."},"isActive":{"type":"boolean"},"scopePath":{"type":"string"}}},
"FnbServiceChargePolicy": {"type":"object","x-ticvai-persistence":"fnb.service_charge_policy","description":"**What the service charge on a bill is, and where it came from.** Every field here answers a question `fnb.sub_bill.service_charge` was being asked and could not answer.\n**Tax and service charge recompute per bill on a split** (`F29`), so the policy is resolved per bill rather than apportioned from the visit — which only works if there is a policy to resolve.","required":["basis","isTaxable","isDiscretionary","distribution"],"properties":{"id":{"type":"string","format":"uuid"},"basis":{"type":"string","enum":["none","percentOfSubtotal","fixedPerCover","fixedPerBill"],"description":"`none` is a real answer and the default. **A venue that does not levy one should say so**, rather than leaving a null that reads as unconfigured."},"ratePercent":{"type":"number","nullable":true,"description":"Set when `basis` is `percentOfSubtotal`."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"minimumPartySize":{"type":"integer","nullable":true,"description":"**The common case for an automatic charge** — parties of six and above. Null applies it to every cover."},"serviceTypes":{"type":"array","items":{"type":"string","enum":["dineIn","takeaway","delivery","roomService"]},"description":"**A delivery order charged a dine-in service charge is a complaint.** Empty means every service type."},"isTaxable":{"type":"boolean","description":"**Whether VAT applies to the charge itself.** It does in the UAE, and a bill that taxes the subtotal but not the charge is understated."},"includedInDisplayPrice":{"type":"boolean","description":"**Menu-price inclusive or added at the bill.** The pair of this and `shownSeparately` is what a guest is entitled to see before ordering."},"shownSeparately":{"type":"boolean"},"isDiscretionary":{"type":"boolean","description":"**Whether a guest may have it removed.** A charge that cannot be declined is a price; a charge that can is a request, and the bill has to say which."},"distribution":{"type":"string","enum":["venueRevenue","staffPool","split"],"description":"**Not a tip.** `orders` separates `serviceCharge` from a gratuity because it is revenue in most jurisdictions and pooling the two is how a payroll dispute starts. This is the field that carries the distinction into payroll."},"staffPoolPercent":{"type":"number","nullable":true,"description":"Set when `distribution` is `split`."},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"KitchenTicket": {"x-ticvai-persistence":"fnb.kitchen_ticket + fnb.kitchen_ticket_line","type":"object","required":["id","orderId","outletId","status","lines","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","description":"The F&B order the ticket was created from on acceptance (`FnbOrder.id`)."},"orderNumber":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"tableLabel":{"type":"string","nullable":true},"serviceMode":{"$ref":"#/components/schemas/ServiceMode"},"coursing":{"allOf":[{"$ref":"#/components/schemas/CoursingPolicy"}],"nullable":true,"description":"BL-131. **Starters before mains is the entire job of a kitchen pass**, and the model fired everything at once.\n`holdAndFire` waits for a server to call it; `timed` fires on a clock; `phased` staggers by course. **Without this a table gets its dessert while eating its starter.**\n"},"buzzerCode":{"type":"string","nullable":true,"description":"BL-128. **The pager number handed to a guest at a counter.** Recorded against the order so a lost buzzer is a lookup rather than an argument.\n"},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"},"priority":{"type":"integer","description":"Higher fires sooner. Raised by Fast Pass or supervisor override."},"prioritisedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"prioritiseReason":{"type":"string","nullable":true},"lines":{"type":"array","items":{"type":"object","required":["lineId","name","quantity","status"],"properties":{"lineId":{"type":"string","format":"uuid"},"name":{"type":"string"},"quantity":{"type":"integer"},"modifiers":{"type":"array","items":{"type":"string"}},"note":{"type":"string","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}},"refireOfLineId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Set on a refire.** The line it remakes, which stays — food cost counts both, the bill counts one (`refireItem`)."},"refireReason":{"allOf":[{"$ref":"#/components/schemas/RefireReason"}],"nullable":true,"readOnly":true},"isChargeable":{"type":"boolean","nullable":true,"readOnly":true,"description":"A refire's `chargeable` flag. Null on a line that is not a refire."},"course":{"type":"integer","nullable":true},"stationId":{"type":"string","format":"uuid","nullable":true},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"}}}},"createdAt":{"type":"string","format":"date-time"},"targetReadyAt":{"type":"string","format":"date-time","nullable":true},"elapsedSeconds":{"type":"integer"}}},
"KitchenTicketStatus": {"type":"string","enum":["received","preparing","ready","served","recalled","cancelled"]},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"Menu": {"x-ticvai-persistence":"fnb.menu","type":"object","required":["id","code","name","outletId","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"outletId":{"type":"string","format":"uuid"},"availability":{"$ref":"#/components/schemas/MenuAvailability"},"sections":{"type":"array","items":{"$ref":"#/components/schemas/MenuSection"}},"isActive":{"type":"boolean"},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `MenuVersion.version` live now. Null for a menu never published."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"MenuAvailability": {"x-ticvai-persistence":"none — embedded in menu","type":"object","description":"When this menu is in force. Absent means always. Days, times and dates are all read in the Region's time zone, not UTC.","properties":{"daysOfWeek":{"type":"array","items":{"type":"integer","minimum":0,"maximum":6}},"startTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"endTime":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$","description":"Wall-clock time, in the Region's time zone."},"validFrom":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."},"validTo":{"type":"string","format":"date","nullable":true,"description":"Calendar day, in the Region's time zone, not UTC."}}},
"MenuSection": {"x-ticvai-persistence":"fnb.menu_section","type":"object","required":["code","name","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string"},"name":{"type":"string"},"sortOrder":{"type":"integer"},"items":{"type":"array","description":"The section's items, in sale-board order. An item's membership is `MenuItem.menuSectionId`.","items":{"$ref":"#/components/schemas/MenuItem"}}}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"OpeningHoursWindow": {"type":"object","description":"26 September, pull audit R088. **One weekly window an outlet is open.** `Outlet.openingHours` was an array of untyped objects. The shape is the one `supportHours.windows` already uses — a day and a from/to — with the times as local `HH:MM` in the region's time zone. Several windows on one day are a split shift, such as lunch and dinner.\n","required":["day","from","to"],"properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet opens."},"to":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet closes."}}},
"Outlet": {"type":"object","x-ticvai-persistence":"platform.outlet","required":["id","code","name","venueId","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/OutletKind"},"zone":{"type":"string","nullable":true},"stockLocationId":{"type":"string","format":"uuid","nullable":true,"description":"Where this outlet draws stock from. A shop and its stockroom are one location; a bar drawing from a central cellar is not.\n"},"costCenterId":{"type":"string","format":"uuid","nullable":true,"description":"Revenue and cost attribution. Outlet is the natural grain for both."},"openingHours":{"type":"array","description":"The weekly pattern, one entry per window. Several windows on a day are allowed.","items":{"$ref":"#/components/schemas/OpeningHoursWindow"}},"isActive":{"type":"boolean"}}},
"OutletKind": {"type":"string","enum":["shop","restaurant","bar","cafe","kiosk","gameFloor","ticketOffice","mobile"]},
"OutletTemplate": {"type":"object","x-ticvai-persistence":"fnb.outlet_template","description":"**The configuration a new outlet is created from** (decided 29 September, readiness close-out; BO-730). New table. Copied into the outlet at creation and never linked after, so changing a template does not change existing outlets.\n","required":["id","code","name","outletType","serviceModel","scopePath"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64,"x-ticvai-unique":"venue"},"name":{"type":"string","maxLength":200},"outletType":{"$ref":"#/components/schemas/OutletTemplateType"},"serviceModel":{"type":"array","items":{"$ref":"#/components/schemas/ServiceMode"}},"defaultMenuIds":{"type":"array","items":{"type":"string","format":"uuid"}},"courseRules":{"type":"object","nullable":true,"properties":{"defaultCoursing":{"$ref":"#/components/schemas/CoursingPolicy"}}},"kitchenSlaMinutes":{"type":"integer","nullable":true},"deliveryPolicyId":{"type":"string","format":"uuid","nullable":true},"isActive":{"type":"boolean"},"scopePath":{"type":"string","readOnly":true,"description":"The venue it belongs to; server-set."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"OutletTemplateInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `setOutletTemplate` takes (decided 29 September, readiness close-out).","required":["code","name","outletType","serviceModel"],"properties":{"code":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","x-ticvai-unique":"venue"},"name":{"type":"string","maxLength":200},"outletType":{"$ref":"#/components/schemas/OutletTemplateType"},"serviceModel":{"type":"array","minItems":1,"description":"The service modes the outlet offers, e.g. `[tableService, collection]`.","items":{"$ref":"#/components/schemas/ServiceMode"}},"defaultMenuIds":{"type":"array","maxItems":20,"items":{"type":"string","format":"uuid"}},"courseRules":{"type":"object","nullable":true,"description":"The coursing default a new outlet starts with; the same shape `setCourseRules` stores per outlet.","properties":{"defaultCoursing":{"$ref":"#/components/schemas/CoursingPolicy"}}},"kitchenSlaMinutes":{"type":"integer","minimum":1,"maximum":240,"nullable":true,"description":"The default ticket target, in minutes, before `setKitchenSla` sets per-mode targets."},"deliveryPolicyId":{"type":"string","format":"uuid","nullable":true},"isActive":{"type":"boolean","default":true}}},
"OutletTemplateType": {"type":"string","enum":["restaurant","bar","cafe","kiosk","mobile"],"description":"The F&B kinds of `tenancy.OutletKind`, repeated here because a satellite does not reference another contract's schema."},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RefireReason": {"type":"string","description":"Why a line was made again (`refireItem`). The reasons are the data.","enum":["overcooked","undercooked","wrongItem","dropped","cold","allergyRisk","guestChangedMind","lateAdd"]},
"SectionLayout": {"type":"object","description":"An outlet's floor divided into sections, each with its server (`setSectionLayout`).","required":["sections"],"properties":{"sections":{"type":"array","items":{"type":"object","required":["name","tableIds"],"properties":{"name":{"type":"string"},"tableIds":{"type":"array","items":{"type":"string","format":"uuid"}},"serverPrincipalId":{"type":"string","format":"uuid","nullable":true},"servicePeriod":{"type":"string","nullable":true}}}}}},
"ServiceMode": {"type":"string","enum":["quickService","tableService","roomService","collection","delivery"]},
"TableDefinition": {"x-ticvai-persistence":"fnb.dining_table","type":"object","description":"A restaurant (dining) table, reserved with `createTableReservation`. Not a map-bookable `resources` table, which is a non-dining spot sold like a cabana (decided 29 September, rev 3 GAP-C2).","required":["id","label","capacity"],"properties":{"id":{"type":"string","format":"uuid"},"label":{"type":"string","maxLength":32,"x-ticvai-unique":"venue","description":"**The table code, unique per venue** (decided 28 September, audit R108). Two tables in one venue never share a label, across all its outlets, so *T12* names one table wherever it is read. `createTable` and `updateTable` refuse a duplicate with `409` `duplicate-code`.\n"},"capacity":{"type":"integer","minimum":1},"zone":{"type":"string","nullable":true},"position":{"type":"object","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"shape":{"type":"string","enum":["round","square","rectangle","booth","bar"]},"isOutOfService":{"type":"boolean","default":false,"description":"**Damaged, or its section closed.** `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`."}}}
}
```
