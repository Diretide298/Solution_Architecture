# WS164 — Resource Management Configuration board 10

**10 screens · 11 operations · 12 schemas · 5 permissions**

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
  `PRODUCT_VIEW, REPORT_VIEW_TENANT, RESOURCE_CONFIGURE, RESOURCE_MANAGE, RESOURCE_VIEW`. A control nobody can use must say so,
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
| `BO-943` | Resource Analytics Command Center | B–D | 0 | 30 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-944` | Resource Utilization & Capacity Analytics | B–D | 3 | 12 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-945` | Resource Cost, Revenue & Efficiency Analytics | B–D | 11 | 9 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-946` | Demand Forecast Accuracy & Planning Performance | B–D | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `BO-947` | Resource KPI, SLA & Performance Framework | B–D | 0 | 44 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-948` | Resource Governance & Policy Center | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-949` | Approval, Exception & Override Control Center | B–D | 0 | 20 | 6 | 0 | 0 | 3 | — | notStarted (—) |
| `BO-950` | Audit Trail & Resource Decision History | B–D | 23 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-951` | Resource Integration & System Health Center | B–D | 0 | 12 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-952` | Executive Resource Intelligence & AI Improvement Center | B–D | 0 | 14 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-947, BO-948, BO-949, BO-951 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-943` Resource Analytics Command Center

**Provide executives and operational managers with a single enterprise dashboard showing the overall health and performance of Resource Management.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/resource-analytics-command-center-bo-943` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Cabana · Lounger · Locker · Wheelchair · Stroller · Equipment · Room · Auditorium · Vehicle · Instructor · Staff · Table … | `listResources` ?kind |
| Available from | date and time picker | — | — | `listResources` ?availableFrom |
| Available to | date and time picker | — | — | `listResources` ?availableTo |
| From | date and time picker | — | — | `getResourceUtilisation` ?from |
| To | date and time picker | — | — | `getResourceUtilisation` ?to |
| Group by | radio group | — | Resource · Resource type · Category · Venue | `getResourceUtilisation` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every resource analytics** (data table)

| Shows | Format | Notes |
|---|---|---|
| Total active resources | text | not in the schema: `Total active resources` |
| Available resources | text | not in the schema: `Available resources` |
| Currently assigned | text | not in the schema: `Currently assigned` |
| Utilization % | text | not in the schema: `Utilization %` |
| Resource readiness % | text | not in the schema: `Resource readiness %` |
| Staff utilization | text | not in the schema: `Staff utilization` |
| Physical asset utilization | text | not in the schema: `Physical asset utilization` |
| Resource conflicts | text | not in the schema: `Resource conflicts` |
| Unfulfilled resource demand | text | not in the schema: `Unfulfilled resource demand` |
| Overtime | text | not in the schema: `Overtime` |
| Maintenance downtime | text | not in the schema: `Maintenance downtime` |
| Resource related operational cost | text | not in the schema: `Resource-related operational cost` |
| Forecast vs actual demand | text | not in the schema: `Forecast vs actual demand` |
| AI recommendations implemented | text | not in the schema: `AI recommendations implemented` |
| Resource breakdown | text | not in the schema: `Resource Breakdown` |

**The selected resource analytics** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Total active resources | text | not in the schema: `Total active resources` |
| Available resources | text | not in the schema: `Available resources` |
| Currently assigned | text | not in the schema: `Currently assigned` |
| Utilization % | text | not in the schema: `Utilization %` |
| Resource readiness % | text | not in the schema: `Resource readiness %` |
| Staff utilization | text | not in the schema: `Staff utilization` |
| Physical asset utilization | text | not in the schema: `Physical asset utilization` |
| Resource conflicts | text | not in the schema: `Resource conflicts` |
| Unfulfilled resource demand | text | not in the schema: `Unfulfilled resource demand` |
| Overtime | text | not in the schema: `Overtime` |
| Maintenance downtime | text | not in the schema: `Maintenance downtime` |
| Resource related operational cost | text | not in the schema: `Resource-related operational cost` |
| Forecast vs actual demand | text | not in the schema: `Forecast vs actual demand` |
| AI recommendations implemented | text | not in the schema: `AI recommendations implemented` |
| Resource breakdown | text | not in the schema: `Resource Breakdown` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Venue (primary button) | navigation or local | — | — | — | — |
| Attraction (secondary button) | navigation or local | — | — | — | — |
| Event (secondary button) | navigation or local | — | — | — | — |
| Resource category (secondary button) | navigation or local | — | — | — | — |
| Resource type (secondary button) | navigation or local | — | — | — | — |
| Equipment (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listResources` (onLoad, Resources at this venue); `getResourceUtilisation` (onLoad, Utilisation across the estate)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-944` Resource Utilization & Capacity Analytics: *Resource Utilization & Capacity Analytics*
- → `BO-945` Resource Cost, Revenue & Efficiency Analytics: *Resource Cost, Revenue & Efficiency Analytics*
- → `BO-946` Demand Forecast Accuracy & Planning Performance: *Demand Forecast Accuracy & Planning Performance*
- → `BO-947` Resource KPI, SLA & Performance Framework: *Resource KPI, SLA & Performance Framework*
- → `BO-948` Resource Governance & Policy Center: *Resource Governance & Policy Center*
- → `BO-949` Approval, Exception & Override Control Center: *Approval, Exception & Override Control Center*
- → `BO-950` Audit Trail & Resource Decision History: *Audit Trail & Resource Decision History*; carries `resourceId`
- → `BO-951` Resource Integration & System Health Center: *Resource Integration & System Health Center*
- → `BO-952` Executive Resource Intelligence & AI Improvement Center: *Executive Resource Intelligence & AI Improvement Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource analytics list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listResources` → `RESOURCE_VIEW` (read) · staff
- `getResourceUtilisation` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-943` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-943`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 1: Opens Resource Analytics Command Center → Provide executives and operational managers with a single enterprise dashboard showing the overall health and performance of Resource Management.
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F273 branch at step 1 (expected): when Nothing has been set up on Resource Analytics Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F273 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-943?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Venue, Attraction, Event, Resource category, Resource type, Equipment.
- [ ] Every transition is wired: `BO-100`, `BO-944`, `BO-945`, `BO-946`, `BO-947`, `BO-948`, `BO-949`, `BO-950`, `BO-951`, `BO-952`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-944` Resource Utilization & Capacity Analytics

**Measure how effectively resources are being utilized and identify overused or underused capacity.**

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
| Route | `/rentals/resource-utilization-capacity-analytics-bo-944` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | — | — | — | — | Sends `?from=` (required). | — |
| To | date picker | — | — | — | — | Sends `?to=` (required). | — |
| Group by | select field | — | — | — | — | Sends `?groupBy=`; venue gives the pack's venue comparison. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceUtilisation` ?from |
| To | date and time picker | — | — | `getResourceUtilisation` ?to |
| Group by | radio group | — | Resource · Resource type · Category · Venue | `getResourceUtilisation` ?groupBy |

#### Outputs: what the screen shows and produces

**Shown**

**Available capacity** (metric tile, from `getResourceUtilisation`): Summed and shown in hours.

| Shows | Format | Notes |
|---|---|---|
| Available minutes | 1,234 | — |

**Scheduled** (metric tile, from `getResourceUtilisation`): Summed and shown in hours.

| Shows | Format | Notes |
|---|---|---|
| Booked minutes | 1,234 | — |

**Utilization** (metric tile, from `getResourceUtilisation`)

| Shows | Format | Notes |
|---|---|---|
| Utilisation percent | 1,234.5 | — |

**Actual usage** (metric tile): The pack's formula is actual utilised hours over available; the contract has booked, not actual.

| Shows | Format | Notes |
|---|---|---|
| Actual usage | text | not in the schema: `Actual usage` |

**Resource ranking by utilization** (chart, from `getResourceUtilisation`): Under- and over-utilised resources stand out against the configured target, which has no field.

| Shows | Format | Notes |
|---|---|---|
| Label | text | — |
| Utilisation percent | 1,234.5 | — |

**Utilization by resource** (data table, from `getResourceUtilisation`)

| Shows | Format | Notes |
|---|---|---|
| Label | text | — |
| Available minutes | 1,234 | — |
| Booked minutes | 1,234 | — |
| Blocked minutes | 1,234 | — |
| Utilisation percent | 1,234.5 | — |
| Booking count | 1,234 | — |

**Data it reads**: `getResourceUtilisation` (onLoad, Utilisation and capacity)

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource utilization capacity list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource utilization capacity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource utilization capacity yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource utilization capacity are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getResourceUtilisation` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-944` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-944`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 2: Works in Resource Utilization & Capacity Analytics → Measure how effectively resources are being utilized and identify overused or underused capacity.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-944?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-943`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-945` Resource Cost, Revenue & Efficiency Analytics

**Measure the financial and operational efficiency of resources.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_MANAGE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `costId` (navigation) |
| Route | `/rentals/resource-cost-revenue-efficiency-analytics-bo-945` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Resource id | picker: choose a resource (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?resourceId=` to `listResourceCosts`. | `listResourceCosts` ?resourceId |
| Kind | segmented control | optional | — | Transfer · Operating · Replacement | — | Sends `?kind=` to `listResourceCosts`. | `listResourceCosts` ?kind |
| From | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?from=` to `listResourceCosts`. | `listResourceCosts` ?from |
| To | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?to=` to `listResourceCosts`. | `listResourceCosts` ?to |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceUtilisation` ?from |
| To | date and time picker | — | — | `getResourceUtilisation` ?to |
| Group by | radio group | — | Resource · Resource type · Category · Venue | `getResourceUtilisation` ?groupBy |
| From | date and time picker | — | — | `getResourceCostAnalytics` ?from |
| To | date and time picker | — | — | `getResourceCostAnalytics` ?to |
| Group by | radio group | Resource type | Resource · Resource type · Category · Venue | `getResourceCostAnalytics` ?groupBy |

**Form: Create resource cost** (modal, opened by *Create resource cost*; *Create resource cost* calls `createResourceCost`, *Cancel* sends nothing)

**Collects what `createResourceCost` sends before it is called.** Required: `id`, `resourceId`, `kind`, `amount`, `incurredOn`. Optional: `fromVenueId`, `toVenueId`, `note`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Resource `resourceId` | picker: choose a resource | required | — | — | shows names, sends the id | — | `createResourceCost` body |
| Kind `kind` | segmented control | required | — | Transfer · Operating · Replacement | — | — | `createResourceCost` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createResourceCost` body |
| Incurred on `incurredOn` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createResourceCost` body |
| From venue `fromVenueId` | picker: choose a from venue | optional | — | — | shows names, sends the id | A `transfer` only, with `toVenueId`. | `createResourceCost` body |
| To venue `toVenueId` | picker: choose a to venue | optional | — | — | shows names, sends the id | — | `createResourceCost` body |
| Note `note` | text area | optional | — | — | — | — | `createResourceCost` body |

Errors to draw in the form: 422 Unknown resource at this venue; a `transfer` without both venues or with the same venue twice; a non-positive amount.

#### Outputs: what the screen shows and produces

**Shown**

**Every resource cost entry** (data table, from `listResourceCosts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Resource | the name it points at, never the id | — |
| Kind | chip: Transfer, Operating, Replacement | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Incurred on | 1 Oct 2026 | — |
| From venue | the name it points at, never the id | A `transfer` only, with `toVenueId`. |
| To venue | the name it points at, never the id | — |
| Note | text | — |
| Scope path | text | The partition key (ADR-0005), written at `venue` scope. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Transfer cost (primary button) | navigation or local | — | — | — | — |
| Asset operating cost (secondary button) | navigation or local | — | — | — | — |
| Resource replacement cost (secondary button) | navigation or local | — | — | — | — |
| Create resource cost (secondary button) | `createResourceCost` POST `/resource-costs` | ResourceCostEntry | ResourceCostEntry | 422 Unknown resource at this venue; a `transfer` without both venues or with the same venue twice; a non-positive amount. | gated `RESOURCE_MANAGE`; opens modal first |
| Delete resource cost (destructive button) | `deleteResourceCost` DELETE `/resource-costs/{costId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `RESOURCE_MANAGE` |

**Data it reads**: `getResourceUtilisation` (onLoad, Cost and efficiency against use); `getResourceCostAnalytics` (onLoad, What resources cost and earn, grouped); `listResourceCosts` (onLoad, Cost entries booked against resources)

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

**What opens over it**

- confirmDialog *Delete resource cost*: **Names what `deleteResourceCost` changes and what it leaves alone**, in the consequence rather than the verb. A record this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource cost revenue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource cost revenue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource cost revenue yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource cost revenue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 Unknown resource at this venue; a `transfer` without both venues or with the same venue twice; a non-positive amount. |

#### Permissions

- `getResourceUtilisation` → `RESOURCE_VIEW` (read) · staff
- `getResourceCostAnalytics` → `RESOURCE_VIEW` (read) · staff
- `listResourceCosts` → `RESOURCE_VIEW` (read) · staff
- `createResourceCost` → `RESOURCE_MANAGE` (configure) · staff
- `deleteResourceCost` → `RESOURCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI forecasting from historical bookings recommends staffing levels for upcoming periods (e.g. "you will need this many resources over the next week") so leave and availability can be planned. Analytics show total cost and revenue by resource and by event. *(client request · MoM 26 Aug 2026, 4.9 AI Optimization, Mobile App & Analytics · DI-501)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-945` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-945`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 4: Works in Resource Cost, Revenue & Efficiency Analytics → Measure the financial and operational efficiency of resources.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400, 404, 422).
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-945?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Transfer cost, Asset operating cost, Resource replacement cost, Create resource cost, Delete resource cost.
- [ ] Every transition is wired: `BO-943`.
- [ ] Every gated control is gated: `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-946` Demand Forecast Accuracy & Planning Performance

**Measure how accurately TICVAI's forecasting and planning engines predicted actual resource demand.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Display; Track) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/demand-forecast-accuracy-planning-performance-bo-946` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listDemandBookingCurve` ?venue |
| Product | text field | — | — | `listDemandBookingCurve` ?product |
| Event | text field | — | — | `listDemandBookingCurve` ?event |
| Performance | text field | — | — | `listDemandBookingCurve` ?performance |
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listDemandBookingCurve` ?channel |
| Horizon | select | — | Intraday · Tomorrow · Days7 · Days30 · Event horizon · Seasonal horizon | `listDemandBookingCurve` ?horizon |
| Date from | date picker | — | — | `listDemandBookingCurve` ?dateFrom |
| Date to | date picker | — | — | `listDemandBookingCurve` ?dateTo |
| Price category | picker: choose a price category | — | — | `listDemandBookingCurve` ?priceCategory |
| Section code | text field | — | — | `listDemandBookingCurve` ?sectionCode |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Forecast Demand** (metric tile)

**Planned Resources** (metric tile)

**Actual Demand** (metric tile)

**Actual Resources Used** (metric tile)

**Attendance forecast accuracy** (metric tile)

**Resource demand forecast accuracy** (metric tile)

**Staffing forecast accuracy** (metric tile)

**Equipment forecast accuracy** (metric tile)

**Forecast shortage rate** (metric tile)

**Overstaffing rate** (metric tile)

**Understaffing rate** (metric tile)

**Data it reads**: `listDemandBookingCurve` (onLoad, Forecast accuracy)

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The demand forecast accuracy list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the demand forecast accuracy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No demand forecast accuracy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the demand forecast accuracy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listDemandBookingCurve` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.11.2 | Seat Demand Forecasting | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |
| 21.11.3 | Seat Inventory Forecasting | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |
| 21.11.4 | Revenue Forecasting by Section | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-946` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-946`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 6: Works in Demand Forecast Accuracy & Planning Performance → Measure how accurately TICVAI's forecasting and planning engines predicted actual resource demand.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-946?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-943`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-947` Resource KPI, SLA & Performance Framework

**Allow organizations to define measurable Resource Management performance standards.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§KPI Library; Each KPI shall support) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/resource-kpi-sla-performance-framework-bo-947` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceUtilisation` ?from |
| To | date and time picker | — | — | `getResourceUtilisation` ?to |
| Group by | radio group | — | Resource · Resource type · Category · Venue | `getResourceUtilisation` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every resource kpi sla** (data table)

| Shows | Format | Notes |
|---|---|---|
| Resource utilization | text | not in the schema: `Resource utilization` |
| Assignment fulfillment | text | not in the schema: `Assignment fulfillment` |
| Staffing coverage | text | not in the schema: `Staffing coverage` |
| Resource readiness | text | not in the schema: `Resource readiness` |
| Equipment availability | text | not in the schema: `Equipment availability` |
| Maintenance downtime | text | not in the schema: `Maintenance downtime` |
| Conflict resolution time | text | not in the schema: `Conflict resolution time` |
| Resource replacement time | text | not in the schema: `Resource replacement time` |
| Attendance compliance | text | not in the schema: `Attendance compliance` |
| Overtime | text | not in the schema: `Overtime` |
| Rental return rate | text | not in the schema: `Rental return rate` |
| Forecast accuracy | text | not in the schema: `Forecast accuracy` |
| Name | text | not in the schema: `Name` |
| Description | text | not in the schema: `Description` |
| Formula | text | not in the schema: `Formula` |
| Target | text | not in the schema: `Target` |
| Warning threshold | text | not in the schema: `Warning threshold` |
| Critical threshold | text | not in the schema: `Critical threshold` |
| Applicable venue | text | not in the schema: `Applicable venue` |
| Applicable resource | text | not in the schema: `Applicable resource` |
| Effective period | text | not in the schema: `Effective period` |
| Owner | text | not in the schema: `Owner` |

**The selected resource kpi sla** (detail panel): The pack groups this record's detail under its own headings: “Target”.

| Shows | Format | Notes |
|---|---|---|
| Resource utilization | text | not in the schema: `Resource utilization` |
| Assignment fulfillment | text | not in the schema: `Assignment fulfillment` |
| Staffing coverage | text | not in the schema: `Staffing coverage` |
| Resource readiness | text | not in the schema: `Resource readiness` |
| Equipment availability | text | not in the schema: `Equipment availability` |
| Maintenance downtime | text | not in the schema: `Maintenance downtime` |
| Conflict resolution time | text | not in the schema: `Conflict resolution time` |
| Resource replacement time | text | not in the schema: `Resource replacement time` |
| Attendance compliance | text | not in the schema: `Attendance compliance` |
| Overtime | text | not in the schema: `Overtime` |
| Rental return rate | text | not in the schema: `Rental return rate` |
| Forecast accuracy | text | not in the schema: `Forecast accuracy` |
| Name | text | not in the schema: `Name` |
| Description | text | not in the schema: `Description` |
| Formula | text | not in the schema: `Formula` |
| Target | text | not in the schema: `Target` |
| Warning threshold | text | not in the schema: `Warning threshold` |
| Critical threshold | text | not in the schema: `Critical threshold` |
| Applicable venue | text | not in the schema: `Applicable venue` |
| Applicable resource | text | not in the schema: `Applicable resource` |
| Effective period | text | not in the schema: `Effective period` |
| Owner | text | not in the schema: `Owner` |

**Data it reads**: `getResourceUtilisation` (onLoad, The KPI base)

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource kpi sla list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource kpi sla untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource kpi sla yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource kpi sla are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getResourceUtilisation` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-947` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-947`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 8: Works in Resource KPI, SLA & Performance Framework → Allow organizations to define measurable Resource Management performance standards.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-947?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-943`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-948` Resource Governance & Policy Center

**Centralize the administrative policies controlling how Resource Management behaves.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_CONFIGURE`, `RESOURCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/resource-governance-policy-center-bo-948` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getResourceAllocationPolicy` (onLoad, Policy in force)

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource governance policy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource governance policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource governance policy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource governance policy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getResourceAllocationPolicy` → `RESOURCE_VIEW` (read) · staff
- `setResourceAllocationPolicy` → `RESOURCE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-948` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-948`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 10: Works in Resource Governance & Policy Center → Centralize the administrative policies controlling how Resource Management behaves.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-948?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-943`.
- [ ] Every gated control is gated: `RESOURCE_CONFIGURE`, `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-949` Approval, Exception & Override Control Center

**Provide one centralized workspace for governed Resource Management exceptions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each request shall show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/approval-exception-override-control-center-bo-949` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every approval exception override** (data table)

| Shows | Format | Notes |
|---|---|---|
| Request | text | not in the schema: `Request` |
| Resource | text | not in the schema: `Resource` |
| Requester | text | not in the schema: `Requester` |
| Venue | text | not in the schema: `Venue` |
| Reason | text | not in the schema: `Reason` |
| Operational impact | text | not in the schema: `Operational impact` |
| Financial impact | text | not in the schema: `Financial impact` |
| Risk | text | not in the schema: `Risk` |
| AI recommendation | text | not in the schema: `AI recommendation` |
| Required approver | text | not in the schema: `Required approver` |

**The selected approval exception override** (detail panel): The pack groups this record's detail under its own headings: “Include”, “Request”, “Issue”.

| Shows | Format | Notes |
|---|---|---|
| Request | text | not in the schema: `Request` |
| Resource | text | not in the schema: `Resource` |
| Requester | text | not in the schema: `Requester` |
| Venue | text | not in the schema: `Venue` |
| Reason | text | not in the schema: `Reason` |
| Operational impact | text | not in the schema: `Operational impact` |
| Financial impact | text | not in the schema: `Financial impact` |
| Risk | text | not in the schema: `Risk` |
| AI recommendation | text | not in the schema: `AI recommendation` |
| Required approver | text | not in the schema: `Required approver` |

**Data it reads**: `listMemberExceptionOverride` (onLoad, Member Exceptions, Overrides & Service Recovery)

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval exception override list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval exception override untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval exception override yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval exception override are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-949` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-949`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 12: Works in Approval, Exception & Override Control Center → Provide one centralized workspace for governed Resource Management exceptions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-949?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-943`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-950` Audit Trail & Resource Decision History

**Provide immutable traceability of significant Resource Management changes and decisions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture; Each event shall capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/audit-trail-resource-decision-history-bo-950` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Resource creation | select field | — | — | — | — | — | — |
| Resource modification | select field | — | — | — | — | — | — |
| Availability change | select field | — | — | — | — | — | — |
| Assignment | select field | — | — | — | — | — | — |
| Reassignment | select field | — | — | — | — | — | — |
| Cancellation | select field | — | — | — | — | — | — |
| Staff override | select field | — | — | — | — | — | — |
| Maintenance block | select field | — | — | — | — | — | — |
| Rental transaction | select field | — | — | — | — | — | — |
| Deposit adjustment | select field | — | — | — | — | — | — |
| Event allocation | select field | — | — | — | — | — | — |
| AI recommendation | select field | — | — | — | — | — | — |
| AI execution | select field | — | — | — | — | — | — |
| Approval | select field | — | — | — | — | — | — |
| Policy change | select field | — | — | — | — | — | — |
| Who | select field | — | — | — | — | — | — |
| What | select field | — | — | — | — | — | — |
| When | select field | — | — | — | — | — | — |
| Where | select field | — | — | — | — | — | — |
| Previous Value | select field | — | — | — | — | — | — |
| New Value | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |
| Source | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The audit trail resource configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the audit trail resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No audit trail resource configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getResourceAuditTrail` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-950` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-950`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 14: Works in Audit Trail & Resource Decision History → Provide immutable traceability of significant Resource Management changes and decisions.

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-950?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-943`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-951` Resource Integration & System Health Center

**Monitor all technical integrations and synchronization services supporting Resource Management.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/resource-integration-system-health-center-bo-951` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every resource integration system** (data table)

| Shows | Format | Notes |
|---|---|---|
| System | text | not in the schema: `System` |
| Status | text | not in the schema: `Status` |
| Last sync | text | not in the schema: `Last Sync` |
| Transactions | text | not in the schema: `Transactions` |
| Errors | text | not in the schema: `Errors` |
| Latency | text | not in the schema: `Latency` |

**The selected resource integration system** (detail panel): The pack groups this record's detail under its own headings: “Potential connections include”, “HRMS”, “Workforce Provider”, “Operational Impact”, “It should explain”.

| Shows | Format | Notes |
|---|---|---|
| System | text | not in the schema: `System` |
| Status | text | not in the schema: `Status` |
| Last sync | text | not in the schema: `Last Sync` |
| Transactions | text | not in the schema: `Transactions` |
| Errors | text | not in the schema: `Errors` |
| Latency | text | not in the schema: `Latency` |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Retry, View error, Inspect payload/reference, Reprocess, Escalate, Open affected records. Each needs attaching to the control it gates, or the screen needs the control.

**Data it reads**: `listAnalyticsPipelines` (onLoad, Integration and data health)

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource integration system list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource integration system untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource integration system yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource integration system are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAnalyticsPipelines` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-951` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-951`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 16: Works in Resource Integration & System Health Center → Monitor all technical integrations and synchronization services supporting Resource Management.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-951?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-943`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-952` Executive Resource Intelligence & AI Improvement Center

**Complete the Resource Management module with an executive AI workspace that converts operational data into management recommendations. This should be the hero screen of Board 10.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Track) and a per-row directory (§Each recommendation shall show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/executive-resource-intelligence-ai-improvement-center-bo-952` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceUtilisation` ?from |
| To | date and time picker | — | — | `getResourceUtilisation` ?to |
| Group by | radio group | — | Resource · Resource type · Category · Venue | `getResourceUtilisation` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Recommendations generated** (metric tile)

**Recommendations accepted** (metric tile)

**Recommendations rejected** (metric tile)

**Auto-actions executed** (metric tile)

**Forecast accuracy** (metric tile)

**Optimization savings predicted** (metric tile)

**Optimization savings realized** (metric tile)

**Replacement success** (metric tile)

**Conflict-resolution success** (metric tile)

**Every executive resource intelligence** (data table)

| Shows | Format | Notes |
|---|---|---|
| Evidence | text | not in the schema: `Evidence` |
| Confidence | text | not in the schema: `Confidence` |
| Expected benefit | text | not in the schema: `Expected benefit` |
| Risk | text | not in the schema: `Risk` |
| Affected resources | text | not in the schema: `Affected resources` |
| Financial impact | text | not in the schema: `Financial impact` |
| Operational impact | text | not in the schema: `Operational impact` |

**The selected executive resource intelligence** (detail panel): The pack groups this record's detail under its own headings: “Executive Question”, “Overall Utilization”, “Resource Readiness”, “Assignment Fulfillment”, “Overtime”, “Resource-Related Cost”.

| Shows | Format | Notes |
|---|---|---|
| Evidence | text | not in the schema: `Evidence` |
| Confidence | text | not in the schema: `Confidence` |
| Expected benefit | text | not in the schema: `Expected benefit` |
| Risk | text | not in the schema: `Risk` |
| Affected resources | text | not in the schema: `Affected resources` |
| Financial impact | text | not in the schema: `Financial impact` |
| Operational impact | text | not in the schema: `Operational impact` |

**Data it reads**: `getResourceUtilisation` (onLoad, Executive resource view)

**Where the user goes next**

- → `BO-943` Resource Analytics Command Center: *Back to Resource Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The executive resource intelligence list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the executive resource intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No executive resource intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the executive resource intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getResourceUtilisation` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-952` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS135 Resource Management Configuration Board 10.dc.html#bo-952`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 10
- Flow F273 *Resource Management Configuration board 10: Resource Analytics Command Center*, step 18: Works in Executive Resource Intelligence & AI Improvement Center → Complete the Resource Management module with an executive AI workspace that converts operational data into management recommendations. This should be the hero screen of Board 10.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-952?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-943`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
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

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createResourceCost": {"method":"POST","path":"/resource-costs","contract":"resources","summary":"Book a transfer, operating or replacement cost against a resource","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceCostEntry","responds":"ResourceCostEntry"},
"deleteResourceCost": {"method":"DELETE","path":"/resource-costs/{costId}","contract":"resources","summary":"Remove a cost entry booked in error","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getResourceAllocationPolicy": {"method":"GET","path":"/resource-allocation-policy","contract":"resources","summary":"How the platform chooses between equally valid resources","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceAllocationPolicy"},
"getResourceAuditTrail": {"method":"GET","path":"/resources/{resourceId}/audit","contract":"resources","summary":"Every material change, with who and why","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceAuditEntry"},
"getResourceCostAnalytics": {"method":"GET","path":"/resource-cost-analytics","contract":"resources","summary":"What resources cost and earn, grouped","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"ResourceCostAnalytics"},
"getResourceUtilisation": {"method":"GET","path":"/resource-utilisation","contract":"resources","summary":"How much of each resource's available time was used","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"ResourceUtilisation"},
"listAnalyticsPipelines": {"method":"GET","path":"/analytics-pipelines","contract":"reporting","summary":"Data sources, refresh state and freshness","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AnalyticsPipeline"},
"listDemandBookingCurve": {"method":"GET","path":"/demand-booking-curve","contract":"catalogue","summary":"AI Demand Forecasting & Booking Curve Studio","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"performance","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"horizon","in":"query","required":false},{"name":"dateFrom","in":"query","required":false},{"name":"dateTo","in":"query","required":false},{"name":"priceCategory","in":"query","required":false},{"name":"sectionCode","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listResourceCosts": {"method":"GET","path":"/resource-costs","contract":"resources","summary":"Cost entries booked against resources","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"resourceId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listResources": {"method":"GET","path":"/resources","contract":"resources","summary":"Resources at this venue","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"availableFrom","in":"query","required":null},{"name":"availableTo","in":"query","required":null}],"requestBody":null,"responds":"Resource"},
"setResourceAllocationPolicy": {"method":"PUT","path":"/resource-allocation-policy","contract":"resources","summary":"Rotation, priority and scoring","permission":"RESOURCE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceAllocationPolicy","responds":"ResourceAllocationPolicy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiDemandForecastingBookingCurveStudioView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What AI Demand Forecasting & Booking Curve Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venue":{"type":"string","description":"Venue id"},"product":{"type":"string","description":"Product id","nullable":true},"event":{"type":"string","description":"Event id","nullable":true},"performance":{"type":"string","description":"Performance id","nullable":true},"date":{"type":"string","description":"Date","format":"date"},"timeslot":{"type":"string","description":"Timeslot","nullable":true},"priceCategory":{"type":"string","description":"Price category","nullable":true},"sectionCode":{"type":"string","nullable":true,"description":"Seat-map section (`seating.Section.code`) the row forecasts; null for a row at price-category or performance level (29 September, build pass, group G2; 21.11.4)"},"channel":{"$ref":"#/components/schemas/Channel","description":"Channel"},"confidence":{"type":"number","description":"Forecast Confidence, percent"},"forecastFinalOccupancy":{"type":"number","description":"Forecast Final Occupancy, percent"},"demand":{"type":"integer","description":"Forecast demand"},"attendance":{"type":"integer","description":"Forecast attendance"},"occupancy":{"type":"number","description":"Forecast occupancy, percent"},"sellThrough":{"type":"number","description":"Forecast sell-through, percent"},"expectedSellOutTime":{"type":"string","description":"Expected Sell-Out Time; empty if no sell-out forecast","format":"date-time","nullable":true},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Forecast revenue"},"conversion":{"type":"number","description":"Forecast conversion, percent"},"remainingInventory":{"type":"integer","description":"Forecast remaining inventory at event"},"mape":{"type":"number","description":"MAPE over closed forecasts at this level, percent"},"forecastBias":{"type":"number","description":"Forecast Bias (positive = over-forecast), percent"},"overForecast":{"type":"number","description":"Share of closed forecasts that over-forecast, percent"},"underForecast":{"type":"number","description":"Share of closed forecasts that under-forecast, percent"},"forecastId":{"type":"string","description":"Forecast id"},"horizon":{"type":"string","description":"Forecast Horizon","enum":["intraday","tomorrow","days7","days30","eventHorizon","seasonalHorizon"]},"bookingCurve":{"type":"array","items":{"type":"object","properties":{"daysBeforeEvent":{"type":"integer","description":"T minus days"},"historicalExpectedPercentSold":{"type":"number","description":"Historical expected curve, percent sold"},"actualPercentSold":{"type":"number","nullable":true,"description":"Current actual curve, percent sold (empty for future points)"},"forecastPercentSold":{"type":"number","description":"AI forecast curve, percent sold"}}},"description":"Booking Curve"},"signalContributions":{"type":"array","items":{"type":"object","properties":{"signal":{"type":"string","enum":["internalSales","bookingVelocity","occupancy","historicalEvents","nearbyEvent","weather","marketTourism","competitor","priceElasticity","other"],"description":"Signal category"},"contributionPercent":{"type":"number","description":"Explanatory share of the forecast"}}},"description":"Model Inputs: which signals contributed"},"confidenceReasons":{"type":"array","items":{"type":"string","enum":["strongHistoricalData","stableBookingPattern","reliableExternalSignals","limitedHistoricalData","volatileBookingPattern","degradedExternalSignals"]},"description":"Reasons behind the forecast confidence"},"modelVersion":{"type":"string","description":"Model version that produced the forecast"},"generatedAt":{"type":"string","description":"When the forecast was produced","format":"date-time"}}},
"AnalyticsPipeline": {"type":"object","x-ticvai-persistence":"reporting.pipeline","description":"BI board 10.7. **Freshness decides whether a dashboard can be trusted.**","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"sourceKind":{"type":"string"},"datasets":{"type":"array","items":{"type":"string"}},"schedule":{"type":"string","nullable":true},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"lastSuccessAt":{"type":"string","format":"date-time","nullable":true},"freshnessMinutes":{"type":"integer","nullable":true},"expectedFreshnessMinutes":{"type":"integer","nullable":true},"status":{"type":"string","enum":["healthy","degraded","stale","failed","paused"]},"lastError":{"type":"string","nullable":true},"rowsLastRun":{"type":"integer","nullable":true},"scopePath":{"type":"string"}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Resource": {"type":"object","x-ticvai-persistence":"resources.resource","description":"**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n","required":["id","code","name","kind","venueId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"$ref":"#/components/schemas/ResourceKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentResourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"},"attributes":{"type":"object","additionalProperties":true,"description":"Configurable per kind — capacity, size, shade, power, poolside."},"setupMinutes":{"type":"integer","default":0,"description":"**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"},"teardownMinutes":{"type":"integer","default":0,"description":"After the booking. **Kept as it is** (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added after the teardown, so a room with no teardown and a 15-minute clean is free 15 minutes after each booking ends.\n"},"cleaningPolicy":{"allOf":[{"$ref":"#/components/schemas/ResourceCleaningPolicy"}],"nullable":true,"description":"How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`."},"requiresQualification":{"type":"array","items":{"type":"string"},"description":"Qualification codes a person must hold to be assigned to this."},"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["available","booked","checkedOut","maintenance","retired"]},"isActive":{"type":"boolean","default":true}}},
"ResourceAllocationPolicy": {"type":"object","x-ticvai-persistence":"resources.allocation_policy","description":"Board 5.08, and the 26 August rotation decision. **Named rather than hidden in the allocator**, so somebody can answer why cabana three never gets used.\n","properties":{"strategy":{"type":"string","enum":["rotate","leastUtilised","priorityOrder","nearestFirst"],"default":"rotate","description":"**`rotate` is the default because 26 August made it one.** *\"rotate across all available resources… rather than repeatedly reusing the same resource, to avoid overburdening any single resource while others remain unused.\"*\n"},"respectResourcePriority":{"type":"boolean","default":true},"scoringWeights":{"type":"object","additionalProperties":{"type":"number"}},"allowPartialAllocation":{"type":"boolean","default":false,"description":"**False by default.** A stage allocated without its sound system is worse than no allocation, because it looks finished.\n"},"scopePath":{"type":"string"}}},
"ResourceAuditEntry": {"type":"object","x-ticvai-persistence":"resources.resource_audit","description":"Board 1.10. **Immutable, and it carries the previous value.**","properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"actorId":{"type":"string","format":"uuid","nullable":true},"action":{"type":"string"},"field":{"type":"string","nullable":true},"previousValue":{"nullable":true},"newValue":{"nullable":true},"reason":{"type":"string","nullable":true},"sourceChannel":{"type":"string","nullable":true},"apiOrigin":{"type":"string","nullable":true},"correlationId":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"ResourceCleaningPolicy": {"x-ticvai-persistence":"none — columns on resources.resource","type":"object","description":"**When the resource is cleaned, and what that takes out of availability** (decided 29 September, W10; the meeting-room case from the 29 September website review).\n- `afterEveryBooking` (option A): `bufferMinutes` blocked after every booking, after its teardown. - `timesPerDay` (option B): `cleaningsPerDay` cleanings of `bufferMinutes` each, between `windowStart` and `windowEnd`, **placed by the system**. The targets are spread evenly across the window; each is put in the free gap nearest its target that is long enough, and never on a booking, a hold or a block. **A confirmed booking is never moved for a cleaning.** Placement is computed on read from the day's bookings, so it moves when bookings change, and a start time is offered only if every cleaning of that day can still be placed after it is booked.\n`createResource` and `updateResource` refuse a policy with `timesPerDay` and no `cleaningsPerDay`, or a window that ends before it starts, with `422`.\n","required":["mode","bufferMinutes"],"properties":{"mode":{"type":"string","enum":["afterEveryBooking","timesPerDay"]},"bufferMinutes":{"type":"integer","minimum":5,"maximum":240,"description":"Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct)."},"cleaningsPerDay":{"type":"integer","minimum":1,"maximum":24,"nullable":true,"description":"Required for `timesPerDay`; ignored for `afterEveryBooking`."},"windowStart":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window opens. Null means the resource's opening time."},"windowEnd":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window closes. Null means the resource's closing time."}}},
"ResourceCostAnalytics": {"type":"object","x-ticvai-persistence":"none — projection over resources.resource_cost, bookings and maintenance work orders, computed at read time","description":"One group's cost and revenue for the window (decided 29 September, readiness close-out; BO-945).","required":["key","label"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"transferCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"operatingCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"replacementCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"bookedHours":{"type":"number"},"costPerBookedHour":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total cost over booked hours; null when nothing was booked."}}},
"ResourceCostEntry": {"type":"object","x-ticvai-persistence":"resources.resource_cost","description":"**One cost booked against a resource**: a transfer between locations, an operating cost or a replacement. `getResourceCostAnalytics` sums these per group and window (decided 29 September, data model DM4).\n","required":["id","resourceId","kind","amount","incurredOn"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"resourceId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["transfer","operating","replacement"]},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incurredOn":{"type":"string","format":"date"},"fromVenueId":{"type":"string","format":"uuid","nullable":true,"description":"A `transfer` only, with `toVenueId`."},"toVenueId":{"type":"string","format":"uuid","nullable":true},"note":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005), written at `venue` scope."}}},
"ResourceKind": {"type":"string","description":"BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n","enum":["cabana","lounger","locker","wheelchair","stroller","equipment","room","auditorium","vehicle","instructor","staff","table","pitch","studio","other"],"x-ticvai-refuses":{"mealPlan":"**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."}},
"ResourceUtilisation": {"type":"object","description":"Board 10.02. **Booked time over available time**, where available knows about schedules, blocks, setup and travel.\n","properties":{"key":{"type":"string"},"label":{"type":"string"},"availableMinutes":{"type":"integer"},"bookedMinutes":{"type":"integer"},"blockedMinutes":{"type":"integer"},"utilisationPercent":{"type":"number"},"bookingCount":{"type":"integer"}}}
}
```
