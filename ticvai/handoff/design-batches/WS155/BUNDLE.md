# WS155 — Resource Management Configuration board 1

**10 screens · 28 operations · 21 schemas · 4 permissions**

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
  `APPROVAL_CONFIGURE, RESOURCE_CONFIGURE, RESOURCE_MANAGE, RESOURCE_VIEW`. A control nobody can use must say so,
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
| `BO-854` | Resource Management Command Center | B–D | 30 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-855` | Resource Type Configuration | B–D | 13 | 0 | 6 | 0 | 3 | 0 | — | notStarted (—) |
| `BO-856` | Resource Category Management | B–D | 15 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-857` | Resource Creation & Profile | B–D | 17 | 2 | 6 | 46 | 1 | 0 | — | notStarted (—) |
| `BO-858` | Configurable Attribute Builder | B–D | 15 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-859` | Resource Hierarchy & Parent–Child Relationships | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-860` | Resource Dependency Rules | B–D | 0 | 8 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-861` | Resource Package & Bundle Configuration | A | 14 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-862` | Multi-Venue Resource Assignment | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-863` | Resource Lifecycle, Governance & Audit | A | 9 | 0 | 6 | 49 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-859, BO-860, BO-862 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-854` Resource Management Command Center

**Provide administrators and operational managers with the main entry point for Resource Management and an instant overview of the organization's complete resource inventory.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Backend Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/resource-management-command-center-bo-854` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Total active resources | select field | — | — | — | — | — | — |
| Resources by type | select field | — | — | — | — | — | — |
| Resources by venue | select field | — | — | — | — | — | — |
| Available resources | select field | — | — | — | — | — | — |
| Assigned resources | select field | — | — | — | — | — | — |
| Reserved resources | select field | — | — | — | — | — | — |
| Resources under maintenance | select field | — | — | — | — | — | — |
| Suspended resources | select field | — | — | — | — | — | — |
| Retired resources | select field | — | — | — | — | — | — |
| Resources with expiring certifications | text field | — | — | — | — | — | — |
| Resources with unresolved configuration issues | text field | — | — | — | — | — | — |
| Recently created resources | select field | — | — | — | — | — | — |
| Recently modified resources | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Business unit | select field | — | — | — | — | — | — |
| Country | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Resource type | select field | — | — | — | — | — | — |
| Category | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |
| Department | select field | — | — | — | — | — | — |
| Tags | select field | — | — | — | — | — | — |
| Availability status | select field | — | — | — | — | — | — |
| Effective date | select field | — | — | — | — | — | — |
| Create resource | select field | — | — | — | — | — | — |
| Create resource type | select field | — | — | — | — | — | — |
| Create category | select field | — | — | — | — | — | — |
| Import resources | select field | — | — | — | — | — | — |
| Duplicate resource | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Cabana · Lounger · Locker · Wheelchair · Stroller · Equipment · Room · Auditorium · Vehicle · Instructor · Staff · Table … | `listResources` ?kind |
| Available from | date and time picker | — | — | `listResources` ?availableFrom |
| Available to | date and time picker | — | — | `listResources` ?availableTo |
| From | date and time picker | — | — | `getResourceUtilisation` ?from |
| To | date and time picker | — | — | `getResourceUtilisation` ?to |
| Group by | radio group | — | Resource · Resource type · Category · Venue | `getResourceUtilisation` ?groupBy |

#### Outputs: what the screen shows and produces

**Data it reads**: `listResources` (onLoad, Resources at this venue); `listResourceTypes` (onLoad, Resources by type); `getResourceUtilisation` (onLoad, Utilisation across the estate)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-855` Resource Type Configuration: *Resource Type Configuration*; carries `resourceTypeId`
- → `BO-856` Resource Category Management: *Resource Category Management*
- → `BO-857` Resource Creation & Profile: *Resource Creation & Profile*; carries `resourceId`
- → `BO-858` Configurable Attribute Builder: *Configurable Attribute Builder*
- → `BO-859` Resource Hierarchy & Parent–Child Relationships: *Resource Hierarchy & Parent–Child Relationships*; carries `resourceId`
- → `BO-860` Resource Dependency Rules: *Resource Dependency Rules*; carries `resourceId`
- → `BO-861` Resource Package & Bundle Configuration: *Resource Package & Bundle Configuration*
- → `BO-862` Multi-Venue Resource Assignment: *Multi-Venue Resource Assignment*; carries `resourceId`
- → `BO-863` Resource Lifecycle, Governance & Audit: *Resource Lifecycle, Governance & Audit*; carries `resourceId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listResources` → `RESOURCE_VIEW` (read) · staff
- `listResourceTypes` → `RESOURCE_VIEW` (read) · staff
- `getResourceUtilisation` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resource types (rooms, staff, equipment, vehicles, etc.) carry capacity control and a reservable flag; the command centre shows total vs. active/assigned resources and current availability. *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-476)*
- Resource management command centre: calendar-based overview of all resources' booking status (e.g. an instructor booked for a lesson, date and time), filterable by resource type and venue, with a switchable revenue view; view by day, week, month or custom period (planner style). *(client request · MoM 26 Aug 2026, 4.1 Resource Management Overview · DI-475)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-854` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-854`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 1: Opens Resource Management Command Center → Provide administrators and operational managers with the main entry point for Resource Management and an instant overview of the organization's complete resource inventory.
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F264 branch at step 1 (expected): when Nothing has been set up on Resource Management Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F264 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (30), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-854?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-855`, `BO-856`, `BO-857`, `BO-858`, `BO-859`, `BO-860`, `BO-861`, `BO-862`, `BO-863`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-855` Resource Type Configuration

**Allow administrators to define the different classes of resources supported by the organization without requiring software development.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Backend Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `resourceTypeId` (navigation) |
| Route | `/rentals/resource-type-configuration-bo-855` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Staff | select field | — | — | — | — | — | — |
| Instructor | select field | — | — | — | — | — | — |
| Security personnel | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Room | select field | — | — | — | — | — | — |
| Hall | select field | — | — | — | — | — | — |
| Area | select field | — | — | — | — | — | — |
| Cabana | select field | — | — | — | — | — | — |
| Equipment | select field | — | — | — | — | — | — |
| Asset | select field | — | — | — | — | — | — |
| Rental item | select field | — | — | — | — | — | — |
| Vehicle | select field | — | — | — | — | — | — |
| Locker | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listResourceTypes` (onLoad, The classes defined so far)

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource type configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource type untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource type configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Resources exist that the new definition would invalidate (ResourceInUseProblem) |

#### Permissions

- `listResourceTypes` → `RESOURCE_VIEW` (read) · staff
- `createResourceType` → `RESOURCE_CONFIGURE` (configure) · staff
- `updateResourceType` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resources are one-to-one (dedicated to a booking) or shared (e.g. a meeting room with bookable pods, a vehicle across sequential slots); further sales are blocked once a shared resource's capacity/slot is full and reopened if a booking is cancelled. *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-496)*
- Resource types (rooms, staff, equipment, vehicles, etc.) carry capacity control and a reservable flag; the command centre shows total vs. active/assigned resources and current availability. *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-476)*
- Optional resource module: a template defines the resource types a product needs (e.g. a vehicle and a driver); named resources have an availability calendar/roster; at sale (POS or online) both resource availability and capacity are checked before booking. *(agreed · MoM 7 Aug 2026, 18. Resource Management · DI-175)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-855` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-855`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 2: Works in Resource Type Configuration → Allow administrators to define the different classes of resources supported by the organization without requiring software development.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-855?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-856` Resource Category Management

**Provide a flexible classification structure beneath resource types so resources can be organized, searched, reported, and governed consistently.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Backend Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `categoryId` (navigation) |
| Route | `/rentals/resource-category-management-bo-856` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Equipment | select field | — | — | — | — | — | — |
| AV | select field | — | — | — | — | — | — |
| Lighting | select field | — | — | — | — | — | — |
| Sound | select field | — | — | — | — | — | — |
| Furniture | select field | — | — | — | — | — | — |
| Staff | select field | — | — | — | — | — | — |
| Instructor | select field | — | — | — | — | — | — |
| Operations | select field | — | — | — | — | — | — |
| Security | select field | — | — | — | — | — | — |
| Technical Crew | select field | — | — | — | — | — | — |
| Rental | select field | — | — | — | — | — | — |
| Towels | select field | — | — | — | — | — | — |
| Strollers | select field | — | — | — | — | — | — |
| Lockers | select field | — | — | — | — | — | — |
| Cabanas | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listResourceCategories` (onLoad, The classification tree)

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource category configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource category untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource category configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The category is in use, and the refusal carries how many resources sit beneath it so the warning can say so. (ResourceInUseProblem) |

#### Permissions

- `listResourceCategories` → `RESOURCE_VIEW` (read) · staff
- `createResourceCategory` → `RESOURCE_CONFIGURE` (configure) · staff
- `updateResourceCategory` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Categories/subcategories are configurable hierarchies (e.g. staff → employee/operations/instructor; equipment → lighting/sound; vehicles → SUV). Resource profile: name, category, capacity, active/inactive, images, category-specific details and custom attributes (e.g. a vehicle's plate number). *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-477)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-856` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-856`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 4: Works in Resource Category Management → Provide a flexible classification structure beneath resource types so resources can be organized, searched, reported, and governed consistently.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-856?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-857` Resource Creation & Profile

**Provide the principal workspace for creating and maintaining an individual resource.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_MANAGE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Backend Configuration; Operational Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/resource-creation-profile-bo-857` |

**Known gaps.** **Resource Creation & Profile declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Active status | select field | — | — | — | — | — | — |
| Reservable status | select field | — | — | — | — | — | — |
| Rentable status | select field | — | — | — | — | — | — |
| Capacity | select field | — | — | — | — | — | — |
| Unit of measure | select field | — | — | — | — | — | — |
| Customer selectable | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |
| Availability mode | select field | — | — | — | — | — | — |
| Scheduling mode | select field | — | — | — | — | — | — |
| Default duration | select field | — | — | — | — | — | — |
| Minimum booking duration | select field | — | — | — | — | — | — |
| Maximum booking duration | select field | — | — | — | — | — | — |
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

**Data it reads**: `getResourceQualifications` (onLoad, What the resource is certified to do, and until when)

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource creation profile configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource creation profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource creation profile configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The transition is not allowed from the current state, or an approval the configuration requires has not been given. (ResourceTransitionProblem); 422 A `cleaningPolicy` with `timesPerDay` and no `cleaningsPerDay`, or whose window ends before it starts (W10, 29 September). |

#### Permissions

- `getResourceAvailability` → `RESOURCE_VIEW` (read) · staff, guest
- `getResource` → `RESOURCE_VIEW` (read) · staff
- `getResourceQualifications` → `RESOURCE_VIEW` (read) · staff
- `createResource` → `RESOURCE_MANAGE` (configure) · staff
- `updateResource` → `RESOURCE_MANAGE` (configure) · staff
- `setResourceLifecycleState` → `RESOURCE_MANAGE` (configure) · staff
- `cloneResource` → `RESOURCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

46 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 34 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Categories/subcategories are configurable hierarchies (e.g. staff → employee/operations/instructor; equipment → lighting/sound; vehicles → SUV). Resource profile: name, category, capacity, active/inactive, images, category-specific details and custom attributes (e.g. a vehicle's plate number). *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-477)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-857` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-857`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 6: Works in Resource Creation & Profile → Provide the principal workspace for creating and maintaining an individual resource.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-857?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-858` Configurable Attribute Builder

**Allow customers to extend resource records with their own attributes without changing the core application.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Backend Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/configurable-attribute-builder-bo-858` |

**Known gaps.** **Configurable Attribute Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Skill level | select field | — | — | — | — | — | — |
| Height | select field | — | — | — | — | — | — |
| Weight | select field | — | — | — | — | — | — |
| Seating capacity | select field | — | — | — | — | — | — |
| Equipment model | select field | — | — | — | — | — | — |
| Serial number | select field | — | — | — | — | — | — |
| Size | select field | — | — | — | — | — | — |
| Manufacturer | select field | — | — | — | — | — | — |
| Color | select field | — | — | — | — | — | — |
| Power requirement | select field | — | — | — | — | — | — |
| Warranty expiry | select field | — | — | — | — | — | — |
| Maximum occupancy | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Certification level | select field | — | — | — | — | — | — |
| Rental condition | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listResourceAttributes` (onLoad, Attributes defined so far)

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The configurable attribute configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the configurable attribute untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No configurable attribute configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listResourceAttributes` → `RESOURCE_VIEW` (read) · staff
- `createResourceAttribute` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Categories/subcategories are configurable hierarchies (e.g. staff → employee/operations/instructor; equipment → lighting/sound; vehicles → SUV). Resource profile: name, category, capacity, active/inactive, images, category-specific details and custom attributes (e.g. a vehicle's plate number). *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-477)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-858` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-858`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 8: Works in Configurable Attribute Builder → Allow customers to extend resource records with their own attributes without changing the core application.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-858?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-859` Resource Hierarchy & Parent–Child Relationships

**Represent physical and operational relationships between resources.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_MANAGE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/resource-hierarchy-parent-child-relationships-bo-859` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save resource hierarchy (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource hierarchy parent–child list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource hierarchy parent–child untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource hierarchy parent–child yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource hierarchy parent–child are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Circular, invalid, or cross-tenant without authorisation (ResourceHierarchyProblem) |

#### Permissions

- `getResourceHierarchy` → `RESOURCE_VIEW` (read) · staff
- `setResourceHierarchy` → `RESOURCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resources link as main/sub-resources (e.g. "vehicle" with individual vehicles beneath). Dependency rules per product (e.g. a private ski lesson needs at least two resources, or at least one vehicle) are enforced when a resource-linked product is configured or sold. *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-478)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-859` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-859`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 10: Works in Resource Hierarchy & Parent–Child Relationships → Represent physical and operational relationships between resources.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-859?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save resource hierarchy, Cancel.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-860` Resource Dependency Rules

**Define operational relationships where one resource requires, depends upon, conflicts with, or influences another resource.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§The system shall display) and no metric row |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/resource-dependency-rules-bo-860` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every resource dependency rules** (data table)

| Shows | Format | Notes |
|---|---|---|
| Missing dependencies | text | not in the schema: `Missing dependencies` |
| Resource conflicts | text | not in the schema: `Resource conflicts` |
| Circular dependency warnings | text | not in the schema: `Circular dependency warnings` |
| Unavailable dependent resources | text | not in the schema: `Unavailable dependent resources` |

**The selected resource dependency rules** (detail panel): The pack groups this record's detail under its own headings: “Private Ski Lesson”.

| Shows | Format | Notes |
|---|---|---|
| Missing dependencies | text | not in the schema: `Missing dependencies` |
| Resource conflicts | text | not in the schema: `Resource conflicts` |
| Circular dependency warnings | text | not in the schema: `Circular dependency warnings` |
| Unavailable dependent resources | text | not in the schema: `Unavailable dependent resources` |

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource dependency rules list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource dependency rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource dependency rules yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource dependency rules are still there. The pack's own statuses are Sound System A — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getResourceDependencies` → `RESOURCE_VIEW` (read) · staff
- `setResourceDependencies` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resources link as main/sub-resources (e.g. "vehicle" with individual vehicles beneath). Dependency rules per product (e.g. a private ski lesson needs at least two resources, or at least one vehicle) are enforced when a resource-linked product is configured or sold. *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-478)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-860` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-860`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 12: Works in Resource Dependency Rules → Define operational relationships where one resource requires, depends upon, conflicts with, or influences another resource.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-860?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-861` Resource Package & Bundle Configuration

**Allow commonly used combinations of resources to be predefined and assigned as a single operational package.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block A · ticket #20729 (APP-SETUP-BO-861) |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `packageId` (navigation) |
| Route | `/rentals/resource-package-bundle-configuration-bo-861` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Package code | select field | — | — | — | — | — | — |
| Package name | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Applicable venues | select field | — | — | — | — | — | — |
| Included resources | select field | — | — | — | — | — | — |
| Included resource types | select field | — | — | — | — | — | — |
| Required quantities | select field | — | — | — | — | — | — |
| Mandatory/optional components | select field | — | — | — | — | — | — |
| Substitute resources | select field | — | — | — | — | — | — |
| Allocation priority | select field | — | — | — | — | — | — |
| Effective dates | select field | — | — | — | — | — | — |
| Minimum/maximum duration | select field | — | — | — | — | — | — |
| Approval requirement | select field | — | — | — | — | — | — |
| Internal package cost | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listResourcePackages` (onLoad, The packages)

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource package bundle configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource package bundle untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource package bundle configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listResourcePackages` → `RESOURCE_VIEW` (read) · staff
- `createResourcePackage` → `RESOURCE_CONFIGURE` (configure) · staff
- `updateResourcePackage` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Multiple resources can be bundled to one product (e.g. a VIP Cabana package = room + attendant) so the system knows every resource needed when it is booked. *(client request · MoM 26 Aug 2026, 4.2 Resource Master Data Configuration · DI-479)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-861` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-861`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 14: Works in Resource Package & Bundle Configuration → Allow commonly used combinations of resources to be predefined and assigned as a single operational package.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-861?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-862` Multi-Venue Resource Assignment

**Control where resources may operate and whether they can be shared across venues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_MANAGE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/multi-venue-resource-assignment-bo-862` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-venue resource list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-venue resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-venue resource yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the multi-venue resource are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Overlapping assignment, or the travel buffer cannot be met (ResourceConflictProblem) |

#### Permissions

- `setResourceVenueAssignment` → `RESOURCE_MANAGE` (configure) · staff
- `getResource` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-862` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-862`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 16: Works in Multi-Venue Resource Assignment → Control where resources may operate and whether they can be shared across venues.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-862?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-863` Resource Lifecycle, Governance & Audit

**Manage the entire operational lifecycle of a resource from creation through retirement while maintaining full traceability. Provide TICVAI with a centralized, real-time Resource Scheduling & Availability Engine where authorized users can visually see when resources are available, reserved, assigned, unavailable, under maintenance, or in conflict and can allocate or reassign them directly from the calendar. The calendar must operate as an interactive operational workspace, not simply a calendar display.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block A · ticket #20708 (APP-SETUP-BO-863) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE`, `RESOURCE_MANAGE`, `RESOURCE_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/resource-lifecycle-governance-audit-bo-863` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Allowed status transitions | select field | — | — | — | — | — | — |
| Approval requirements | select field | — | — | — | — | — | — |
| Effective dates | select field | — | — | — | — | — | — |
| Retirement reason | select field | — | — | — | — | — | — |
| Suspension reason | select field | — | — | — | — | — | — |
| Replacement resource | select field | — | — | — | — | — | — |
| Disposal information | select field | — | — | — | — | — | — |
| Depreciation reference | select field | — | — | — | — | — | — |
| Asset-retirement information | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Maker-checker approval (primary button) | navigation or local | — | — | — | — |
| Manager approval (secondary button) | navigation or local | — | — | — | — |
| Finance approval (secondary button) | navigation or local | — | — | — | — |
| Operations approval (secondary button) | navigation or local | — | — | — | — |
| Create (secondary button) | navigation or local | — | — | — | — |
| Edit (secondary button) | navigation or local | — | — | — | — |
| Approve (secondary button) | navigation or local | — | — | — | — |
| Activate (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-854` Resource Management Command Center: *Back to Resource Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource lifecycle governance configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource lifecycle governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource lifecycle governance configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says which: `loosensParentRule` — the matrix would loosen a rule set at a higher scope (a higher threshold … (ApprovalMatrixRefusedProblem); 409 The transition is not allowed from the current … |

#### Permissions

- `getResourceAuditTrail` → `RESOURCE_VIEW` (read) · staff
- `setResourceLifecycleState` → `RESOURCE_MANAGE` (configure) · staff
- `setApprovalControlPolicy` → `APPROVAL_CONFIGURE` (configure) · staff
- `setApprovalMatrix` → `APPROVAL_CONFIGURE` (configure) · staff
- `createResource` → `RESOURCE_MANAGE` (configure) · staff
- `updateResource` → `RESOURCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

49 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.51 | System shall support reservation approvals. | Ticketing Catalogue | CONTRACTED | `setApprovalMatrix` |
| 1.2.76 | System shall support configurable approval workflows. | Ticketing Catalogue | CONTRACTED | `setApprovalMatrix` |
| 2.12.4 | The system should support configuration of required access level to allow refund, exchange and/or void actions. At minimum, the system should provide: - Ability to enable/disable supervisor access … | Ticketing Sales | CONTRACTED | `setApprovalMatrix` |
| 3.3.31 | Segregation of Duties - System shall enforce segregation of duties in access policies. | Admission and Access | CONTRACTED | `setApprovalMatrix` |
| 7.1.22 | The system shall support approval workflows for user creation, role assignment, permission changes, privileged access requests, and user deactivation. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 7.1.24 | The system shall support configurable approval requirements for refunds, ticket cancellations, price changes, promotion changes, membership changes, wallet adjustments, and manual overrides. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 7.5.10 | Support multi-level approval processes for complimentary tickets, VIP invitations and sponsor allocations with full audit history. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 11.1.1 | Provides configurable workflows requiring one or more approvals before sensitive actions can be executed. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.2 | Approval Workflow Configuration System shall allow administrators to configure approval workflows for different business processes. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.3 | Multi-Level Approval System shall support single-level and multi-level approval chains. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.4 | Role-Based Approval Routing System shall automatically route approval requests based on organizational hierarchy and user roles. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.5 | Escalation Rules System shall automatically escalate pending approvals after configurable time thresholds. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| … 37 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-863` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS126 Resource Management Configuration Board 1.dc.html#bo-863`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 1
- Flow F264 *Resource Management Configuration board 1: Resource Management Command Center*, step 18: Works in Resource Lifecycle, Governance & Audit → Manage the entire operational lifecycle of a resource from creation through retirement while maintaining full traceability.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-863?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Maker-checker approval, Manager approval, Finance approval, Operations approval, Create, Edit, Approve, Activate.
- [ ] Every transition is wired: `BO-854`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
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

**11 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"cloneResource": {"method":"POST","path":"/resources/{resourceId}/clone","contract":"resources","summary":"Copy a resource and its configuration into new ones","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Resource"},
"createResource": {"method":"POST","path":"/resources","contract":"resources","summary":"Define a bookable resource","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Resource","responds":"Resource"},
"createResourceAttribute": {"method":"POST","path":"/resource-attributes","contract":"resources","summary":"Define a customer attribute","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceAttributeDefinition","responds":"ResourceAttributeDefinition"},
"createResourceCategory": {"method":"POST","path":"/resource-categories","contract":"resources","summary":"Add a category or subcategory","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceCategory","responds":"ResourceCategory"},
"createResourcePackage": {"method":"POST","path":"/resource-packages","contract":"resources","summary":"Define a reusable combination","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourcePackage","responds":"ResourcePackage"},
"createResourceType": {"method":"POST","path":"/resource-types","contract":"resources","summary":"Define a class of resource","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceType","responds":"ResourceType"},
"getResource": {"method":"GET","path":"/resources/{resourceId}","contract":"resources","summary":"One resource, with every configured section","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Resource"},
"getResourceAuditTrail": {"method":"GET","path":"/resources/{resourceId}/audit","contract":"resources","summary":"Every material change, with who and why","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceAuditEntry"},
"getResourceAvailability": {"method":"GET","path":"/resources/{resourceId}/availability","contract":"resources","summary":"When it is free, with conflicts already resolved","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true}],"requestBody":null,"responds":"ResourceAvailability"},
"getResourceDependencies": {"method":"GET","path":"/resources/{resourceId}/dependencies","contract":"resources","summary":"What this resource requires, conflicts with, or substitutes for","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceDependency"},
"getResourceHierarchy": {"method":"GET","path":"/resources/{resourceId}/hierarchy","contract":"resources","summary":"What this resource contains, and what contains it","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceHierarchy"},
"getResourceQualifications": {"method":"GET","path":"/resources/{resourceId}/qualifications","contract":"resources","summary":"What an instructor or staff resource is certified to do, and until when — as saved","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Qualification"},
"getResourceUtilisation": {"method":"GET","path":"/resource-utilisation","contract":"resources","summary":"How much of each resource's available time was used","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"ResourceUtilisation"},
"listResourceAttributes": {"method":"GET","path":"/resource-attributes","contract":"resources","summary":"The customer-defined fields on a resource","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceAttributeDefinition"},
"listResourceCategories": {"method":"GET","path":"/resource-categories","contract":"resources","summary":"The classification tree beneath the types","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceCategory"},
"listResourcePackages": {"method":"GET","path":"/resource-packages","contract":"resources","summary":"Predefined combinations assigned as one","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourcePackage"},
"listResourceTypes": {"method":"GET","path":"/resource-types","contract":"resources","summary":"The classes of resource this organisation supports","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceType"},
"listResources": {"method":"GET","path":"/resources","contract":"resources","summary":"Resources at this venue","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"availableFrom","in":"query","required":null},{"name":"availableTo","in":"query","required":null}],"requestBody":null,"responds":"Resource"},
"setApprovalControlPolicy": {"method":"PUT","path":"/approval-control-policies","contract":"approvals","summary":"Require a second, independent pair of eyes","permission":"APPROVAL_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalControlPolicy","responds":"ApprovalControlPolicy"},
"setApprovalMatrix": {"method":"PUT","path":"/approval-matrices","contract":"approvals","summary":"Configure what requires approval","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalMatrix","responds":"ApprovalMatrix"},
"setResourceDependencies": {"method":"PUT","path":"/resources/{resourceId}/dependencies","contract":"resources","summary":"Define what must come with it, and what cannot","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceDependency"},
"setResourceHierarchy": {"method":"PUT","path":"/resources/{resourceId}/hierarchy","contract":"resources","summary":"Re-parent a resource, or attach children to it","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceHierarchy","responds":"ResourceHierarchy"},
"setResourceLifecycleState": {"method":"POST","path":"/resources/{resourceId}/state","contract":"resources","summary":"Move a resource through its lifecycle, with a reason","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Resource"},
"setResourceVenueAssignment": {"method":"PUT","path":"/resources/{resourceId}/venues","contract":"resources","summary":"Where it may operate, and whether it travels","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceVenueAssignment","responds":"ResourceVenueAssignment"},
"updateResource": {"method":"PUT","path":"/resources/{resourceId}","contract":"resources","summary":"Change a resource","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Resource","responds":"Resource"},
"updateResourceCategory": {"method":"PUT","path":"/resource-categories/{categoryId}","contract":"resources","summary":"Change a category","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceCategory","responds":"ResourceCategory"},
"updateResourcePackage": {"method":"PUT","path":"/resource-packages/{packageId}","contract":"resources","summary":"Change a combination","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourcePackage","responds":"ResourcePackage"},
"updateResourceType": {"method":"PUT","path":"/resource-types/{resourceTypeId}","contract":"resources","summary":"Change a class of resource","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceType","responds":"ResourceType"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApprovalControlPolicy": {"type":"object","x-ticvai-persistence":"approvals.control_policy","description":"Approvals boards 6.2 and 6.3. **Which decisions one person may not take alone** — distinct from which roles one person may not hold, which is `identity.setSegregationRules`.\n","required":["code","control"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"appliesToRequestKinds":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalKind"}},"appliesAboveValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"control":{"type":"string","enum":["fourEyes","dualControl","separationFromRequester","separationFromExecutor"],"description":"**`fourEyes` is two different people; `dualControl` is two people from different groups.** The second is stronger and is what a finance auditor means, and collapsing them makes the stronger control unexpressible.\n"},"requiredApproverGroupIds":{"type":"array","items":{"type":"string","format":"uuid"}},"minimumApprovers":{"type":"integer","default":2},"requiresStepUp":{"type":"boolean","default":false},"requiresSignature":{"type":"boolean","default":false},"breakGlassAllowed":{"type":"boolean","default":false,"description":"**Whether the control may be overridden in an emergency**, and if so it raises an alert rather than passing quietly. A control with no break-glass will be worked around by hand at three in the morning, which is worse.\n"},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMatrix": {"type":"object","x-ticvai-persistence":"approvals.matrix","required":["kind","scopeLevel","rules"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"]},"scopePath":{"type":"string","readOnly":true},"version":{"type":"integer","readOnly":true,"description":"11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"},"rules":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalRule"}},"isActive":{"type":"boolean"}}},
"ApprovalRule": {"type":"object","x-ticvai-persistence":"approvals.rule","required":["order","approverRoleIds","mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"order":{"type":"integer","description":"**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"},"minAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"riskScoreAbove":{"type":"number","nullable":true,"description":"11.1.12. **Not matched against the AI risk score** (29 September, build pass, group G2). The AI assessment on a request (`ApprovalRequest.aiAssessment`, from `ai.scoreApprovalRequest`) is context for the reviewer only (MoM 8 September: AI never influences approve or reject), and routing a request to more approvers because of it would be influence. A rule with this set matches only a `riskScore` the requesting contract passes in `attributes` from its own deterministic rules (a payment's rule score, for example). Using the AI score here needs the client to say so.\n"},"condition":{"type":"string","nullable":true,"description":"11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"},"approverRoleIds":{"type":"array","minItems":1,"description":"Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n","items":{"type":"string","format":"uuid"}},"approverScopeLevel":{"type":"string","enum":["venue","department","region","tenant"],"description":"11.1.39. Which organisational level the approver must sit at."},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"levels":{"type":"integer","default":1,"description":"11.1.3. Multi-level chains ask each level in turn."},"requiresMfa":{"type":"boolean","default":false},"requiresSignature":{"type":"boolean","default":false},"slaMinutes":{"type":"integer","nullable":true,"description":"11.1.14. Null means no SLA, which is different from a long one."},"escalateAfterMinutes":{"type":"integer","nullable":true},"escalateToRoleIds":{"type":"array","description":"Role ids from `identity.listRoles`, as `approverRoleIds`.","items":{"type":"string","format":"uuid"}},"expiresAfterMinutes":{"type":"integer","nullable":true,"description":"11.1.53. An unanswered request eventually stops waiting."},"externalProviderId":{"type":"string","format":"uuid","nullable":true,"description":"11.1.65 (29 September). **This level is decided in an external workflow system** (`ApprovalExternalProvider`) rather than by a person in TICVAI. `approverRoleIds` stay required: they are who decides if the provider does not answer in time and its `onTimeout` is `fallBackToRoles`.\n"}}},
"Qualification": {"type":"object","x-ticvai-persistence":"resources.qualification","description":"1.2.36. **A role is not a skill**, and the check happens before assignment rather than after.\n","required":["code","name"],"properties":{"resourceId":{"type":"string","format":"uuid","readOnly":true,"description":"**The resource that holds this qualification.** Set from the path of `setResourceQualifications`; without it a stored qualification belongs to nobody and the check before assignment has nothing to check against. One row per resource and `code`.\n"},"code":{"type":"string"},"name":{"type":"string"},"issuedAt":{"type":"string","format":"date","nullable":true},"expiresAt":{"type":"string","format":"date","nullable":true,"description":"**The field that makes this worth having.** A certification with no expiry is one nobody renews, and a lifeguard certificate that lapsed last month is a safety failure rather than a data-quality one.\n"},"issuer":{"type":"string","nullable":true},"documentAssetId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"Resource": {"type":"object","x-ticvai-persistence":"resources.resource","description":"**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n","required":["id","code","name","kind","venueId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"$ref":"#/components/schemas/ResourceKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentResourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"},"attributes":{"type":"object","additionalProperties":true,"description":"Configurable per kind — capacity, size, shade, power, poolside."},"setupMinutes":{"type":"integer","default":0,"description":"**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"},"teardownMinutes":{"type":"integer","default":0,"description":"After the booking. **Kept as it is** (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added after the teardown, so a room with no teardown and a 15-minute clean is free 15 minutes after each booking ends.\n"},"cleaningPolicy":{"allOf":[{"$ref":"#/components/schemas/ResourceCleaningPolicy"}],"nullable":true,"description":"How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`."},"requiresQualification":{"type":"array","items":{"type":"string"},"description":"Qualification codes a person must hold to be assigned to this."},"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["available","booked","checkedOut","maintenance","retired"]},"isActive":{"type":"boolean","default":true}}},
"ResourceAttributeDefinition": {"type":"object","x-ticvai-persistence":"resources.attribute_definition","description":"Board 1.05. **A typed, validated field the customer adds.** The alternative was a column per customer request, which is a release per customer.\n","required":["code","label","dataType"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"label":{"type":"string"},"dataType":{"type":"string","enum":["text","number","decimal","currency","date","dateTime","boolean","singleSelect","multiSelect","lookup","attachment","url","measurement","formula"]},"applicableResourceTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"applicableCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"mandatory":{"type":"boolean","default":false},"defaultValue":{"nullable":true},"allowedValues":{"type":"array","items":{"type":"string"}},"minimum":{"type":"number","nullable":true},"maximum":{"type":"number","nullable":true},"validationExpression":{"type":"string","nullable":true},"searchable":{"type":"boolean","default":false,"description":"**The flag that decides whether `suggestResources` can use it.** An attribute nobody can filter by cannot take part in skill-based matching, which is the main reason the customer defined it.\n"},"scopePath":{"type":"string"}}},
"ResourceAuditEntry": {"type":"object","x-ticvai-persistence":"resources.resource_audit","description":"Board 1.10. **Immutable, and it carries the previous value.**","properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"actorId":{"type":"string","format":"uuid","nullable":true},"action":{"type":"string"},"field":{"type":"string","nullable":true},"previousValue":{"nullable":true},"newValue":{"nullable":true},"reason":{"type":"string","nullable":true},"sourceChannel":{"type":"string","nullable":true},"apiOrigin":{"type":"string","nullable":true},"correlationId":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"ResourceAvailability": {"type":"object","description":"**Free windows, with setup and teardown already subtracted.** A client computing this from bookings will forget the turnaround.\n","properties":{"resourceId":{"type":"string","format":"uuid"},"freeWindows":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"}}}},"blockedWindows":{"type":"array","description":"**With a reason, because they are not the same.** Booked and under repair need different responses from an operator looking for something free — wait, or look elsewhere.\n","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"reason":{"type":"string","enum":["booked","held","setup","teardown","maintenance","blackout","closed","cleaning"],"description":"`held` is a live `ResourceHold` (rev 3 REV3-15): taken now, free again if it expires. `cleaning` is a cleaning the resource's `cleaningPolicy` places (W10, 29 September).\n"}}}}}},
"ResourceCategory": {"type":"object","x-ticvai-persistence":"resources.resource_category","description":"Board 1.03. Beneath the type — *Equipment → AV → Lighting*, *Rental → Towels*. **Configuration cascades down the tree**, which is the reason it is a tree.\n","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"parentCategoryId":{"type":"string","format":"uuid","nullable":true},"applicableResourceTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"displayOrder":{"type":"integer","default":0},"tags":{"type":"array","items":{"type":"string"}},"reportingGroup":{"type":"string","nullable":true},"costCentre":{"type":"string","nullable":true},"defaultAttributes":{"type":"object","additionalProperties":true},"defaultApprovalWorkflowId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"ResourceCleaningPolicy": {"x-ticvai-persistence":"none — columns on resources.resource","type":"object","description":"**When the resource is cleaned, and what that takes out of availability** (decided 29 September, W10; the meeting-room case from the 29 September website review).\n- `afterEveryBooking` (option A): `bufferMinutes` blocked after every booking, after its teardown. - `timesPerDay` (option B): `cleaningsPerDay` cleanings of `bufferMinutes` each, between `windowStart` and `windowEnd`, **placed by the system**. The targets are spread evenly across the window; each is put in the free gap nearest its target that is long enough, and never on a booking, a hold or a block. **A confirmed booking is never moved for a cleaning.** Placement is computed on read from the day's bookings, so it moves when bookings change, and a start time is offered only if every cleaning of that day can still be placed after it is booked.\n`createResource` and `updateResource` refuse a policy with `timesPerDay` and no `cleaningsPerDay`, or a window that ends before it starts, with `422`.\n","required":["mode","bufferMinutes"],"properties":{"mode":{"type":"string","enum":["afterEveryBooking","timesPerDay"]},"bufferMinutes":{"type":"integer","minimum":5,"maximum":240,"description":"Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct)."},"cleaningsPerDay":{"type":"integer","minimum":1,"maximum":24,"nullable":true,"description":"Required for `timesPerDay`; ignored for `afterEveryBooking`."},"windowStart":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window opens. Null means the resource's opening time."},"windowEnd":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window closes. Null means the resource's closing time."}}},
"ResourceDependency": {"type":"object","x-ticvai-persistence":"resources.resource_dependency","description":"Board 1.07. **Evaluated before an assignment is confirmed.** *Stage A requires Sound System A and Lighting Rig A.*\n","required":["kind"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["requires","requiresOneOf","requiresAll","conflictsWith","cannotOperateSimultaneously","preferredWith","substituteFor","backupFor","sharesCapacityWith"]},"targetResourceId":{"type":"string","format":"uuid","nullable":true},"targetResourceTypeId":{"type":"string","format":"uuid","nullable":true},"minimumQuantity":{"type":"integer","default":1},"maximumQuantity":{"type":"integer","nullable":true},"mandatory":{"type":"boolean","default":true},"priority":{"type":"integer","default":0},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"ResourceHierarchy": {"type":"object","description":"Board 1.06. Ancestors and the immediate subtree, with the relationship named.","properties":{"resourceId":{"type":"string","format":"uuid"},"ancestors":{"type":"array","items":{"$ref":"#/components/schemas/ResourceRelation"}},"children":{"type":"array","items":{"$ref":"#/components/schemas/ResourceRelation"}}}},
"ResourceKind": {"type":"string","description":"BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n","enum":["cabana","lounger","locker","wheelchair","stroller","equipment","room","auditorium","vehicle","instructor","staff","table","pitch","studio","other"],"x-ticvai-refuses":{"mealPlan":"**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."}},
"ResourceLifecycleState": {"type":"string","description":"Board 1.10. **States of one machine**, whose allowed transitions are configuration.","enum":["draft","pendingApproval","approved","active","temporarilyUnavailable","underMaintenance","suspended","retired","archived"]},
"ResourcePackage": {"type":"object","x-ticvai-persistence":"resources.resource_package","description":"Board 1.08. **A package may hold placeholders.** \"One technician\" is a slot, and naming a person would make the package unbookable whenever they are off.\n","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"applicableVenueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"components":{"type":"array","items":{"$ref":"#/components/schemas/ResourceRequirement"}},"allocationPriority":{"type":"integer","default":0},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"minimumMinutes":{"type":"integer","nullable":true},"maximumMinutes":{"type":"integer","nullable":true},"requiresApproval":{"type":"boolean","default":false},"internalCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scopePath":{"type":"string"}}},
"ResourceRelation": {"type":"object","x-ticvai-persistence":"resources.resource_relation","required":["resourceId","relation"],"properties":{"resourceId":{"type":"string","format":"uuid"},"relation":{"type":"string","enum":["contains","belongsTo","locatedIn","operatedBy","supportedBy","partOf","dedicatedTo"]},"effectiveFrom":{"type":"string","format":"date","nullable":true},"priority":{"type":"integer","default":0},"scopePath":{"type":"string"}}},
"ResourceRequirement": {"type":"object","x-ticvai-persistence":"resources.resource_requirement","description":"**A type and a quantity, never a named resource.** This is what makes the 26 August rule enforceable — the product states what it needs and the platform decides which one.\nFor resources placed on a published venue map the rule is superseded (decided 29 September, rev 3 REV3-15): the guest names the resource through a `ResourceHold`, and no requirement is needed.\n","required":["quantity"],"properties":{"id":{"type":"string","format":"uuid"},"resourceTypeId":{"type":"string","format":"uuid","nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"resourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A fixed component, and the exception rather than the rule.** Meeting Room A really is Meeting Room A; the technician is not.\n"},"quantity":{"type":"integer","default":1},"mandatory":{"type":"boolean","default":true},"requiredQualifications":{"type":"array","items":{"type":"string"}},"requiredAttributes":{"type":"object","additionalProperties":true},"substituteResourceIds":{"type":"array","items":{"type":"string","format":"uuid"}},"scopePath":{"type":"string"}}},
"ResourceType": {"type":"object","x-ticvai-persistence":"resources.resource_type","description":"Board 1.02. **The class, and the ten switches that decide which parts of the platform a resource of this class touches.** `Resource.kind` was an enum and this is the table behind it — a customer adding \"Golf Buggy\" does not need a release.\n","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"icon":{"type":"string","nullable":true},"displayColour":{"type":"string","nullable":true},"nature":{"type":"string","enum":["physical","human","virtual"],"description":"**Human resources point at a principal and are rostered by `workforce`.** The nature decides which other context owns the thing, which is why it is not a free label.\n"},"reservable":{"type":"boolean","default":true},"rentable":{"type":"boolean","default":false},"capacityControlled":{"type":"boolean","default":false},"scheduleControlled":{"type":"boolean","default":true},"inventoryControlled":{"type":"boolean","default":false},"qualificationRequired":{"type":"boolean","default":false},"maintenanceControlled":{"type":"boolean","default":false},"checkInOutSupported":{"type":"boolean","default":false},"depositApplicable":{"type":"boolean","default":false},"customerSelectable":{"type":"boolean","default":false,"description":"**A ceiling, not a permission.** Whether a guest may actually choose is decided per ticket type by `setResourceSelectionPolicy`; a type with this false can never be choosable, and a type with it true still is not until a product says so.\n"},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"ResourceUtilisation": {"type":"object","description":"Board 10.02. **Booked time over available time**, where available knows about schedules, blocks, setup and travel.\n","properties":{"key":{"type":"string"},"label":{"type":"string"},"availableMinutes":{"type":"integer"},"bookedMinutes":{"type":"integer"},"blockedMinutes":{"type":"integer"},"utilisationPercent":{"type":"number"},"bookingCount":{"type":"integer"}}},
"ResourceVenueAssignment": {"type":"object","x-ticvai-persistence":"resources.venue_assignment","description":"Board 1.09. **The travel buffer is subtracted from availability**, like setup and teardown, so a shared instructor is not double-booked across a journey they cannot make.\n","required":["primaryVenueId"],"properties":{"primaryVenueId":{"type":"string","format":"uuid"},"secondaryVenueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"sharedPool":{"type":"boolean","default":false},"crossVenueBookingAllowed":{"type":"boolean","default":false},"travelBufferMinutes":{"type":"integer","default":0},"transferRequired":{"type":"boolean","default":false},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"scopePath":{"type":"string"}}}
}
```
