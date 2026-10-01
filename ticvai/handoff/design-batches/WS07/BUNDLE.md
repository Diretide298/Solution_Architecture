# WS07 — Access Control board 7

**10 screens · 15 operations · 24 schemas · 5 permissions**

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
  `ACCESS_POINT_CONFIGURE, ACCESS_VALIDATE, INCIDENT_MANAGE, SCOPE_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
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
| `BO-204` | Offline & Edge Operations Command Center | B–D | 0 | 182 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-205` | Edge Node & Local Processing Configuration | B–D | 10 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-206` | Offline Validation Policy Builder | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-207` | Edge Package & Data Distribution | B–D | 16 | 0 | 5 | 7 | 0 | 0 | — | notStarted (generated) |
| `BO-208` | Offline Credential & Revocation Cache | B–D | 7 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-209` | Offline Entitlement & Usage Ledger | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-210` | Connectivity Failure & Degraded Mode Policy | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-211` | Reconnection, Synchronization & Conflict Resolution | B–D | 0 | 14 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-212` | Offline Simulation & Resilience Testing | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-213` | Edge Security, Audit & Deployment | B–D | 3 | 110 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-206, BO-208, BO-209, BO-210, BO-211, BO-212 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-204` Offline & Edge Operations Command Center

**Provide a real-time overview of offline readiness across the entire access-control estate.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/offline-edge-operations-command-center-bo-204` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Offline-Ready Devices** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Currently Online** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Currently Offline** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Devices in Degraded Mode** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Edge Nodes Online** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Packages Current** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Packages Expiring** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Pending Offline Transactions** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Offline Security Alerts** (metric tile, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | Venue |
| Rules cached | yes / no (icon or chip) | ✓ Rules cached |
| Verification material current | yes / no (icon or chip) | ✓ Verification material current |
| Revocation data current | yes / no (icon or chip) | ✓ Revocation data current |
| Credential definitions available | yes / no (icon or chip) | ✓ Credential definitions available |
| Device storage healthy | yes / no (icon or chip) | ✓ Device storage healthy |
| Last synchronization successful | yes / no (icon or chip) | ✓ Last synchronization successful |
| Venue name | text | Venue name |
| Devices | 1,234 | Devices at the venue |
| Offline ready | 1,234 | Devices ready to operate offline |
| Readiness percent | 1,234.5 | Share of devices offline ready |
| Package status | chip: Current, Expiring, Expired | Edge package status |
| Pending transactions | 1,234 | Offline transactions not yet synchronized |
| Readiness status | chip: Ready, Warning, Not ready | Venue readiness |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Offline ready devices | 1,234 | Offline-Ready Devices |
| Currently online | 1,234 | Currently Online |

**Every offline edge operations** (data table, from `listOfflineEdge`)

| Shows | Format | Notes |
|---|---|---|
| Sync conflicts | text | not in the schema: `Sync Conflicts` |

**The selected offline edge operations** (detail panel): The pack groups this record's detail under its own headings: “Venue Readiness”, “Checks”.

| Shows | Format | Notes |
|---|---|---|
| Sync conflicts | text | not in the schema: `Sync Conflicts` |

**Data it reads**: `listOfflineEdge` (onLoad, Offline & Edge Operations Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-205` Edge Node & Local Processing Configuration: *Works in Edge Node & Local Processing Configuration*; calls `listOfflineEdge`
- → `BO-206` Offline Validation Policy Builder: *Works in Offline Validation Policy Builder*; calls `listOfflineEdge`
- → `BO-207` Edge Package & Data Distribution: *Works in Edge Package & Data Distribution*; calls `listOfflineEdge`
- → `BO-208` Offline Credential & Revocation Cache: *Works in Offline Credential & Revocation Cache*; calls `listOfflineEdge`
- → `BO-209` Offline Entitlement & Usage Ledger: *Works in Offline Entitlement & Usage Ledger*; calls `listOfflineEdge`
- → `BO-210` Connectivity Failure & Degraded Mode Policy: *Works in Connectivity Failure & Degraded Mode Policy*; calls `listOfflineEdge`
- → `BO-211` Reconnection, Synchronization & Conflict Resolution: *Works in Reconnection, Synchronization & Conflict Resolution*; calls `listOfflineEdge`
- → `BO-212` Offline Simulation & Resilience Testing: *Works in Offline Simulation & Resilience Testing*; calls `listOfflineEdge`
- → `BO-213` Edge Security, Audit & Deployment: *Works in Edge Security, Audit & Deployment*; calls `listOfflineEdge`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline edge operations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline edge operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline edge operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the offline edge operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listOfflineEdge` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-204` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-204`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 1: Opens Offline & Edge Operations Command Center → Provide a real-time overview of offline readiness across the entire access-control estate.
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F117 branch at step 1 (expected): when Nothing has been set up on Offline & Edge Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F117 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (182 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-204?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-205`, `BO-206`, `BO-207`, `BO-208`, `BO-209`, `BO-210`, `BO-211`, `BO-212`, `BO-213`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-205` Edge Node & Local Processing Configuration

**Configure where local access decisions are processed when central services cannot be reached.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Fields) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/edge-node-local-processing-configuration-bo-205` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Edge Node ID | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Network | select field | — | — | — | — | — | — |
| Device Group | select field | — | — | — | — | — | — |
| Processing Mode | select field | — | — | — | — | — | — |
| Storage allocation | select field | — | — | — | — | — | — |
| redundancy | select field | — | — | — | — | — | — |
| last heartbeat | select field | — | — | — | — | — | — |
| software version | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-204` Offline & Edge Operations Command Center: *Returns to the board's landing screen*; calls `setEdgeNodeLocal`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The edge node local configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the edge node local untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No edge node local configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setEdgeNodeLocal` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-205` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-205`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 2: Works in Edge Node & Local Processing Configuration → Configure where local access decisions are processed when central services cannot be reached.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-205?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-204`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-206` Offline Validation Policy Builder

**Define exactly which access checks are allowed to run locally. The matrix identifies key offline criteria including eligible media, eligible site, eligible time, ticket validity and eligible access mode.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/offline-validation-policy-builder-bo-206` |

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

- → `BO-204` Offline & Edge Operations Command Center: *Returns to the board's landing screen*; calls `setOfflinePolicy`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline validation policy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline validation policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline validation policy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the offline validation policy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setOfflinePolicy` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-206` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-206`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 4: Works in Offline Validation Policy Builder → Define exactly which access checks are allowed to run locally. The matrix identifies key offline criteria including eligible media, eligible site, eligible time, ticket validity and eligible access …
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-206?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `BO-204`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-207` Edge Package & Data Distribution

**Define what configuration and operational data is securely distributed to edge devices.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `ACCESS_VALIDATE`, `SCOPE_VIEW` (1 configure, 1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Access Configuration; Credential Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/edge-package-data-distribution-bo-207` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| venues | select field | — | — | — | — | — | — |
| zones | select field | — | — | — | — | — | — |
| gates | select field | — | — | — | — | — | — |
| access rules | select field | — | — | — | — | — | — |
| calendars | select field | — | — | — | — | — | — |
| media profiles | select field | — | — | — | — | — | — |
| verification profiles | select field | — | — | — | — | — | — |
| entitlement definitions | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Since version | number field | — | — | `getOfflinePackage` ?sinceVersion |
| Valid from | date and time picker | — | — | `getOfflinePackage` ?validFrom |
| Valid to | date and time picker | — | — | `getOfflinePackage` ?validTo |

**Sent by *What publishing changes*** (`publishHardwareDeployment`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated deployment id | `publishHardwareDeployment` body |
| Configuration version `configurationVersion` | text field | required | — | — | — | The access configuration version being deployed | `publishHardwareDeployment` body |
| Target scope `targetScope` | radio group | required | — | Pilot · Selected gates · Device group · Venue | — | — | `publishHardwareDeployment` body |
| Venue `venueId` | text field | required | — | — | — | — | `publishHardwareDeployment` body |
| Gates `gateIds` | list of values (chips) | optional | — | — | — | Required for pilot and selectedGates | `publishHardwareDeployment` body |
| Device group `deviceGroupId` | text field | optional | — | — | — | Required for deviceGroup | `publishHardwareDeployment` body |
| Run compatibility test first `runCompatibilityTestFirst` | toggle | optional | on | — | — | Devices that fail the compatibility test are skipped and named in the result | `publishHardwareDeployment` body |
| Scheduled at `scheduledAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Empty deploys now | `publishHardwareDeployment` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing changes (publish gate) | `publishHardwareDeployment` POST `/hardware-deployments` | HardwareDeploymentInput | HardwareDeploymentView | 409 A deployment to an overlapping target set is still queued or in progress; 422 gateIds or deviceGroupId missing for the chosen targetScope | — |

**Data it reads**: `listEdgePackageData` (onLoad, Edge Package & Data Distribution); `getOfflinePackage` (onLoad, The access package an edge node holds, with its version)

**Where the user goes next**

- → `BO-204` Offline & Edge Operations Command Center: *Returns to the board's landing screen*; calls `listEdgePackageData`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The edge package data configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the edge package data untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No edge package data configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A deployment to an overlapping target set is still queued or in progress; 422 gateIds or deviceGroupId missing for the chosen targetScope |

#### Permissions

- `listEdgePackageData` → `SCOPE_VIEW` (read) · staff
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `publishHardwareDeployment` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.38 | Offline Access Validation | Ticketing Sales | CONTRACTED | `getOfflinePackage` |
| 3.1.5 | Access control devices shall validate dynamic QR codes using secure offline cryptographic validation without requiring continuous connectivity to the central platform. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.1.10 | System shall support embedding entitlement information within secure QR, RFID, NFC, mobile wallet, and digital credential tokens. Embedded information may include ticket type, seat assignment, event … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.49 | The validity check logic allows offline validity check. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.75 | The access control can be operated in offline mode. Turnstiles can perform access control in absence of database access (database unavailable or not reachable). Key access control criteria can be … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.3.30 | Distributed Policy Evaluation - System shall support local policy evaluation when offline. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 18.1.3 | Offline Mode - System shall support offline operation. | Employee Mobile App & AI Assistant | CONTRACTED | `getOfflinePackage` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-207` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-207`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 6: Works in Edge Package & Data Distribution → Define what configuration and operational data is securely distributed to edge devices.
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (403, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-207?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: What publishing changes.
- [ ] Every transition is wired: `BO-204`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `ACCESS_VALIDATE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-208` Offline Credential & Revocation Cache

**Manage the local information required to reject credentials that should no longer be usable. This is especially important because Board 3 requires refunded, cancelled, transferred, exchanged, upgraded and reissued credentials to be invalidated.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`, `TENANT_CONFIGURE` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/offline-credential-revocation-cache-bo-208` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Form: Save offline policy** (modal, opened by *Save offline policy*; *Save offline policy* calls `setOfflinePolicy`, *Cancel* sends nothing)

**Collects what `setOfflinePolicy` sends before it is called.** Required: `scopePath`. Optional: `id`, `maxOfflineHours`, `allowedOffline`, `offlineValueCeiling`, `offlineTransactionCeiling`, `onCeilingBreach`, `requiresManagerToExtend`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scope path `scopePath` | text field | required | — | pattern `^[a-z0-9_]+(\.[a-z0-9_]+)*$` | — | The node this policy is for, and the key `setOfflinePolicy` upserts on. The body names its target here, because the path does not. | `setOfflinePolicy` body |
| Max offline hours `maxOfflineHours` | stepper or slider (hours) | optional | 24 | min 1; max 72 | — | After which the workstation refuses to sell rather than keep journalling. A till three days offline holding 900 unsynced sales is a reconciliation nobody can do and a fraud nobody … | `setOfflinePolicy` body |
| Allowed offline `allowedOffline` | multi-select chips | optional | — | Sale · Refund · Exchange · Entitlement issue · Entitlement validate · Loyalty accrual · Loyalty redemption · Wallet spend · Price override · Discount · Void line · No sale; Selling from a cached catalogue is safe; issuing a refund is not, because the original … | — | What may happen with no network, by data class. Selling from a cached catalogue is safe; issuing a refund is not, because the original sale cannot be verified. | `setOfflinePolicy` body |
| Offline value ceiling `offlineValueCeiling` | money field | optional | — | Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129). | AED, 2 decimals shown (up to 4 accepted), currency from the … | Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129). | `setOfflinePolicy` body |
| Offline transaction ceiling `offlineTransactionCeiling` | number field | optional | — | min 1; max 5000 | — | A ceiling on count as well as value. Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only the second. | `setOfflinePolicy` body |
| On ceiling breach `onCeilingBreach` | segmented control | optional | Block new sales | Warn · Block new sales · Block all | — | — | `setOfflinePolicy` body |
| Requires manager to extend `requiresManagerToExtend` | toggle | optional | on | — | — | — | `setOfflinePolicy` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save offline policy (primary button) | `setOfflinePolicy` PUT `/offline-policy` | OfflinePolicy | OfflinePolicy | 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `TENANT_CONFIGURE`; opens modal first |

**Data it reads**: `listOfflineCredentialRevocation` (onLoad, Offline Credential & Revocation Cache)

**Where the user goes next**

- → `BO-204` Offline & Edge Operations Command Center: *Returns to the board's landing screen*; calls `listOfflineCredentialRevocation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline credential revocation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline credential revocation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline credential revocation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the offline credential revocation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 The edge threshold is shorter than the central one. |

#### Permissions

- `setGateOfflinePolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `listOfflineCredentialRevocation` → `SCOPE_VIEW` (read) · staff
- `setOfflinePolicy` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-208` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-208`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 8: Works in Offline Credential & Revocation Cache → Manage the local information required to reject credentials that should no longer be usable. This is especially important because Board 3 requires refunded, cancelled, transferred, exchanged …
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-208?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save offline policy.
- [ ] Every transition is wired: `BO-204`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`, `TENANT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-209` Offline Entitlement & Usage Ledger

**Track entitlement consumption while the central system is unavailable. This is necessary for tickets such as: 3 Fast Pass uses 1 park entry 1 meal 1 re-entry where usage can occur during an outage.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/offline-entitlement-usage-ledger-bo-209` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listOfflineEntitlementUsage` (onLoad, Offline Entitlement & Usage Ledger)

**Where the user goes next**

- → `BO-204` Offline & Edge Operations Command Center: *Returns to the board's landing screen*; calls `listOfflineEntitlementUsage`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline entitlement usage list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline entitlement usage untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline entitlement usage yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the offline entitlement usage are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listOfflineEntitlementUsage` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-209` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-209`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 10: Works in Offline Entitlement & Usage Ledger → Track entitlement consumption while the central system is unavailable. This is necessary for tickets such as: 3 Fast Pass uses 1 park entry 1 meal 1 re-entry where usage can occur during an outage.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-209?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-204`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-210` Connectivity Failure & Degraded Mode Policy

**Configure how devices transition from normal online operation to offline/degraded operation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`, `TENANT_CONFIGURE` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/connectivity-failure-degraded-mode-policy-bo-210` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save offline policy (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listConnectivityFailureDegraded` (onLoad, Connectivity Failure & Degraded Mode Policy)

**Where the user goes next**

- → `BO-204` Offline & Edge Operations Command Center: *Returns to the board's landing screen*; calls `listConnectivityFailureDegraded`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The connectivity failure degraded list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the connectivity failure degraded untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No connectivity failure degraded yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the connectivity failure degraded are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 The edge threshold is shorter than the central one. |

#### Permissions

- `setGateOfflinePolicy` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `listConnectivityFailureDegraded` → `SCOPE_VIEW` (read) · staff
- `setOfflinePolicy` → `TENANT_CONFIGURE` (configure) · staff
- `setConnectivityThresholds` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-210` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-210`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 12: Works in Connectivity Failure & Degraded Mode Policy → Configure how devices transition from normal online operation to offline/degraded operation.
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-210?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save offline policy, Cancel.
- [ ] Every transition is wired: `BO-204`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_VIEW`, `TENANT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-211` Reconnection, Synchronization & Conflict Resolution

**Synchronize everything that occurred offline when connectivity returns.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/reconnection-synchronization-conflict-resolution-bo-211` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every reconnection synchronization conflict** (data table, from `listReconnectionSynchronizationConflict`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Conflict | text | Conflict identifier |
| Central remaining balance before outage | 1,234 | Entitlement uses remaining centrally before the outage (a count, not money) |
| Resolution policy | chip: Preserve both and flag, Earliest transaction wins, Configured business rule … | How this conflict is resolved |
| Credential | text | Credential involved |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Pending scans | 1,234 | Pending scans |
| Entitlement events | 1,234 | Entitlement events |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Overrides | 1,234 | Overrides |
| Security events | 1,234 | Security events |

**The selected reconnection synchronization conflict** (detail panel): The pack groups this record's detail under its own headings: “Connectivity Restored”, “Authenticate”, “Upload Offline Transactions”, “Sequence Events”, “Reconcile Credential State”, “Reconcile Entitlements”.

**Data it reads**: `listReconnectionSynchronizationConflict` (onLoad, Reconnection, Synchronization & Conflict Resolution)

**Where the user goes next**

- → `BO-204` Offline & Edge Operations Command Center: *Returns to the board's landing screen*; calls `listReconnectionSynchronizationConflict`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reconnection synchronization conflict list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reconnection synchronization conflict untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reconnection synchronization conflict yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reconnection synchronization conflict are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listReconnectionSynchronizationConflict` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Handheld scanners read QR, RFID or other supported media. Offline, devices validate locally from data embedded in the credential, queue the transactions and auto-sync when connectivity returns. *(agreed · MoM 2 Sep 2026, 4.13 / 4.14 Handheld Scanners & Offline Mode · DI-646)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-211` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-211`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 14: Works in Reconnection, Synchronization & Conflict Resolution → Synchronize everything that occurred offline when connectivity returns.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-211?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-204`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-212` Offline Simulation & Resilience Testing

**Allow venues to prove that their access environment will survive outages before opening to guests.**

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
| Route | `/access-venue/offline-simulation-resilience-testing-bo-212` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run simulation (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-204` Offline & Edge Operations Command Center: *Returns to the board's landing screen*; calls `simulateOfflineResilienceTesting`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline simulation resilience list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline simulation resilience untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline simulation resilience yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the offline simulation resilience are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `simulateOfflineResilienceTesting` → `ACCESS_POINT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-212` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-212`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 16: Works in Offline Simulation & Resilience Testing → Allow venues to prove that their access environment will survive outages before opening to guests.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-212?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run simulation, Cancel.
- [ ] Every transition is wired: `BO-204`.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-213` Edge Security, Audit & Deployment

**Govern the complete offline/edge environment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `INCIDENT_MANAGE`, `SCOPE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `alertId` (navigation) |
| Route | `/access-venue/edge-security-audit-deployment-bo-213` |

#### Inputs: what the user enters or picks

**Form: Save security alert** (modal, opened by *Save security alert*; *Save security alert* calls `updateSecurityAlert`, *Cancel* sends nothing)

**Collects what `updateSecurityAlert` sends before it is called.** Required: `status`. Optional: `note`, `securityInvestigationId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | segmented control | required | — | Acknowledged · Resolved · Dismissed | — | — | `updateSecurityAlert` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `updateSecurityAlert` body |
| Security investigation `securityInvestigationId` | picker: choose a security investigation | optional | — | — | shows names, sends the id | — | `updateSecurityAlert` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The alert is already resolved or dismissed.

#### Outputs: what the screen shows and produces

**Shown**

**Package signatures** (metric tile, from `listEdgeSecurityDeployment`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy version | text | Edge policy version identifier |
| Deployment scope | chip: Tenant, Venue, Park, Edge cluster, Gate group, Device group… | Where this edge policy version deploys |
| Stage | chip: Draft, Validated, Security tested, Offline simulated, Approved, Pilot… | Release stage |
| Is production | yes / no (icon or chip) | Currently in production |
| Scheduled at | 1 Oct 2026, 14:30 | Scheduled deployment time |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Edge certificates | 1,234 | Edge certificates |
| Edge credentials | 1,234 | Edge credentials |
| Package signatures | 1,234 | Package signatures |
| Authorized devices | 1,234 | Authorized devices |
| Revoked devices | 1,234 | Revoked devices |
| Failed package validation | 1,234 | Failed package validation |
| Unauthorized connection attempts | 1,234 | unauthorized connection attempts |
| Configuration changes | 1,234 | configuration changes |
| Offline override activity | 1,234 | offline override activity |

**Authorized devices** (metric tile, from `listEdgeSecurityDeployment`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy version | text | Edge policy version identifier |
| Deployment scope | chip: Tenant, Venue, Park, Edge cluster, Gate group, Device group… | Where this edge policy version deploys |
| Stage | chip: Draft, Validated, Security tested, Offline simulated, Approved, Pilot… | Release stage |
| Is production | yes / no (icon or chip) | Currently in production |
| Scheduled at | 1 Oct 2026, 14:30 | Scheduled deployment time |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Edge certificates | 1,234 | Edge certificates |
| Edge credentials | 1,234 | Edge credentials |
| Package signatures | 1,234 | Package signatures |
| Authorized devices | 1,234 | Authorized devices |
| Revoked devices | 1,234 | Revoked devices |
| Failed package validation | 1,234 | Failed package validation |
| Unauthorized connection attempts | 1,234 | unauthorized connection attempts |
| Configuration changes | 1,234 | configuration changes |
| Offline override activity | 1,234 | offline override activity |

**Revoked devices** (metric tile, from `listEdgeSecurityDeployment`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy version | text | Edge policy version identifier |
| Deployment scope | chip: Tenant, Venue, Park, Edge cluster, Gate group, Device group… | Where this edge policy version deploys |
| Stage | chip: Draft, Validated, Security tested, Offline simulated, Approved, Pilot… | Release stage |
| Is production | yes / no (icon or chip) | Currently in production |
| Scheduled at | 1 Oct 2026, 14:30 | Scheduled deployment time |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Edge certificates | 1,234 | Edge certificates |
| Edge credentials | 1,234 | Edge credentials |
| Package signatures | 1,234 | Package signatures |
| Authorized devices | 1,234 | Authorized devices |
| Revoked devices | 1,234 | Revoked devices |
| Failed package validation | 1,234 | Failed package validation |
| Unauthorized connection attempts | 1,234 | unauthorized connection attempts |
| Configuration changes | 1,234 | configuration changes |
| Offline override activity | 1,234 | offline override activity |

**Failed package validation** (metric tile, from `listEdgeSecurityDeployment`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy version | text | Edge policy version identifier |
| Deployment scope | chip: Tenant, Venue, Park, Edge cluster, Gate group, Device group… | Where this edge policy version deploys |
| Stage | chip: Draft, Validated, Security tested, Offline simulated, Approved, Pilot… | Release stage |
| Is production | yes / no (icon or chip) | Currently in production |
| Scheduled at | 1 Oct 2026, 14:30 | Scheduled deployment time |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Edge certificates | 1,234 | Edge certificates |
| Edge credentials | 1,234 | Edge credentials |
| Package signatures | 1,234 | Package signatures |
| Authorized devices | 1,234 | Authorized devices |
| Revoked devices | 1,234 | Revoked devices |
| Failed package validation | 1,234 | Failed package validation |
| Unauthorized connection attempts | 1,234 | unauthorized connection attempts |
| Configuration changes | 1,234 | configuration changes |
| Offline override activity | 1,234 | offline override activity |

**unauthorized connection attempts** (metric tile, from `listEdgeSecurityDeployment`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy version | text | Edge policy version identifier |
| Deployment scope | chip: Tenant, Venue, Park, Edge cluster, Gate group, Device group… | Where this edge policy version deploys |
| Stage | chip: Draft, Validated, Security tested, Offline simulated, Approved, Pilot… | Release stage |
| Is production | yes / no (icon or chip) | Currently in production |
| Scheduled at | 1 Oct 2026, 14:30 | Scheduled deployment time |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Edge certificates | 1,234 | Edge certificates |
| Edge credentials | 1,234 | Edge credentials |
| Package signatures | 1,234 | Package signatures |
| Authorized devices | 1,234 | Authorized devices |
| Revoked devices | 1,234 | Revoked devices |
| Failed package validation | 1,234 | Failed package validation |
| Unauthorized connection attempts | 1,234 | unauthorized connection attempts |
| Configuration changes | 1,234 | configuration changes |
| Offline override activity | 1,234 | offline override activity |

**configuration changes** (metric tile, from `listEdgeSecurityDeployment`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Policy version | text | Edge policy version identifier |
| Deployment scope | chip: Tenant, Venue, Park, Edge cluster, Gate group, Device group… | Where this edge policy version deploys |
| Stage | chip: Draft, Validated, Security tested, Offline simulated, Approved, Pilot… | Release stage |
| Is production | yes / no (icon or chip) | Currently in production |
| Scheduled at | 1 Oct 2026, 14:30 | Scheduled deployment time |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Edge certificates | 1,234 | Edge certificates |
| Edge credentials | 1,234 | Edge credentials |
| Package signatures | 1,234 | Package signatures |
| Authorized devices | 1,234 | Authorized devices |
| Revoked devices | 1,234 | Revoked devices |
| Failed package validation | 1,234 | Failed package validation |
| Unauthorized connection attempts | 1,234 | unauthorized connection attempts |
| Configuration changes | 1,234 | configuration changes |
| Offline override activity | 1,234 | offline override activity |

**Every edge security audit** (data table, from `listEdgeSecurityDeployment`)

| Shows | Format | Notes |
|---|---|---|
| Edge certificates/credentials | text | not in the schema: `Edge certificates/credentials` |

**The selected edge security audit** (detail panel): The pack groups this record's detail under its own headings: “Draft”, “Deployment Scope”, “Current Production”, “Scheduled”, “Rollback”, “FORCE ONLINE-ONLY”.

| Shows | Format | Notes |
|---|---|---|
| Edge certificates/credentials | text | not in the schema: `Edge certificates/credentials` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save security alert (primary button) | `updateSecurityAlert` POST `/security-alerts/{alertId}/status` | inline | AccessSecurityAlert | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `INCIDENT_MANAGE`; opens modal first |

**Data it reads**: `listEdgeSecurityDeployment` (onLoad, Edge Security, Audit & Deployment)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The edge security audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the edge security audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No edge security audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the edge security audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The alert is already resolved or dismissed. |

#### Permissions

- `listEdgeSecurityDeployment` → `SCOPE_VIEW` (read) · staff
- `updateSecurityAlert` → `INCIDENT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-213` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS24 Access Control Board 7.dc.html#bo-213`
- Workshop pack: Access Control Module_Reference.pdf board 7
- Flow F117 *Access Control board 7: Offline & Edge Operations Command Center*, step 18: Works in Edge Security, Audit & Deployment → Govern the complete offline/edge environment.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (110 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-213?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save security alert.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `INCIDENT_MANAGE`, `SCOPE_VIEW`.
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

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getOfflinePackage": {"method":"GET","path":"/access/offline-package","contract":"access","summary":"Entitlement and rule set for offline validation","permission":"ACCESS_VALIDATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":"sinceVersion","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":"validFrom","in":"query","required":true},{"name":"validTo","in":"query","required":true},{"name":"If-None-Match","in":"header","required":null}],"requestBody":null,"responds":"OfflinePackage"},
"listConnectivityFailureDegraded": {"method":"GET","path":"/connectivity-failure-degraded","contract":"access","summary":"Connectivity Failure & Degraded Mode Policy","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConnectivityFailureDegradedModePolicyView"},
"listEdgePackageData": {"method":"GET","path":"/edge-package-data","contract":"access","summary":"Edge Package & Data Distribution","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listEdgeSecurityDeployment": {"method":"GET","path":"/edge-security-deployment","contract":"access","summary":"Edge Security, Audit & Deployment","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOfflineCredentialRevocation": {"method":"GET","path":"/offline-credential-revocation","contract":"access","summary":"Offline Credential & Revocation Cache","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OfflineCredentialRevocationCacheView"},
"listOfflineEdge": {"method":"GET","path":"/offline-edge","contract":"access","summary":"Offline & Edge Operations Command Center","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOfflineEntitlementUsage": {"method":"GET","path":"/offline-entitlement-usage","contract":"access","summary":"Offline Entitlement & Usage Ledger","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listReconnectionSynchronizationConflict": {"method":"GET","path":"/reconnection-synchronization-conflict","contract":"access","summary":"Reconnection, Synchronization & Conflict Resolution","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"publishHardwareDeployment": {"method":"POST","path":"/hardware-deployments","contract":"access","summary":"Deploy a gate configuration version","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"HardwareDeploymentInput","responds":"HardwareDeploymentView"},
"setConnectivityThresholds": {"method":"PUT","path":"/connectivity-policy","contract":"tenancy","summary":"When a workstation decides it is offline, and when it is back","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ConnectivityPolicy","responds":"ConnectivityPolicy"},
"setEdgeNodeLocal": {"method":"PUT","path":"/edge-node-local","contract":"access","summary":"Edge Node & Local Processing Configuration","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"EdgeNodeLocalProcessingConfigurationInput","responds":"EdgeNodeLocalProcessingConfigurationView"},
"setGateOfflinePolicy": {"method":"PUT","path":"/offline-policies","contract":"access","summary":"Set the offline policy of a venue","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessOfflinePolicy","responds":"AccessOfflinePolicy"},
"setOfflinePolicy": {"method":"PUT","path":"/offline-policy","contract":"tenancy","summary":"What a workstation may do with no network, and for how long","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OfflinePolicy","responds":"OfflinePolicy"},
"simulateOfflineResilienceTesting": {"method":"PUT","path":"/offline-resilience-testing","contract":"access","summary":"Offline Simulation & Resilience Testing","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OfflineSimulationResilienceTestingInput","responds":"OfflineSimulationResilienceTestingView"},
"updateSecurityAlert": {"method":"POST","path":"/security-alerts/{alertId}/status","contract":"access","summary":"Acknowledge, resolve or dismiss a security alert","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessSecurityAlert"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessAccreditationCredential": {"type":"object","x-ticvai-persistence":"access.accreditation_credential","x-ticvai-agreed":"29 September: build pass (group OWN, from group RA's handoff; BL-181); the events accreditation.credentialIssued and accreditation.holderStatusChanged name access as their critical consumer","description":"**What a gate needs to admit an accredited person, kept by `access`** (29 September, build). Written only by the consumers of `accreditation.credentialIssued` (a row per credential; a replacement sets the replaced row's `admits` false) and `accreditation.holderStatusChanged` (every credential of the holder: `admits` false unless the holder is `active`, validity taken from the event). Read by `validateAccess` and shipped in the offline package. The record of truth stays in `accreditation`; this is a copy shaped for the gate, never edited by a person.","required":["id","holderId","encodedIdentifier","admits","scopePath"],"properties":{"id":{"type":"string","format":"uuid","description":"The accreditation credential's id (`credentialId` on the events)."},"holderId":{"type":"string","format":"uuid"},"programmeId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","description":"printedBadge, mobileCredential, qr, nfcCard, rfidCard or wristband, as issued."},"encodedIdentifier":{"type":"string","x-ticvai-unique":"tenant","description":"What the gate reads from the credential. Never sent to webhook subscribers."},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"zoneIds":{"type":"array","description":"The holder's effective zones, from the event (`effectiveZones`).","items":{"type":"string","format":"uuid"}},"holderStatus":{"type":"string","enum":["active","suspended","revoked","expired","archived"],"description":"The holder's status as last published; only `active` admits."},"admits":{"type":"boolean","description":"False once the credential is replaced or the holder is not active."},"sourceChangedAt":{"type":"string","format":"date-time","description":"The `issuedAt` or `changedAt` of the event last applied; an older event arriving late is ignored."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005), the accreditation programme's scope."}}},
"AccessDynamicPolicy": {"type":"object","x-ticvai-persistence":"access.dynamic_policy","description":"One guest-admission dynamic (attribute-based) policy with its current content - type, context or identity it tests, condition expression, result, priority, zones, validity, status and current version. Not identity.authorisation_policy, which is staff permission (declared 29 September, data-model close-out DM1).\n\n**Guest admission lives here and nowhere else** (ADR-0068, accepted 1 October). `validateAccess` online and the gate offline evaluate the same active version: `getOfflinePackage` carries it, and every `scan_event` records the policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`) and the set it was decided under (`policySetVersion`). The condition is `conditionRule`, a closed JSON format (`AdmissionRule`), not free text. Identity's staff-permission engine was renamed `AuthorisationPolicy` on the same day, so \"access policy\" means this.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). **This one governs who may pass which gate**: admission of a guest, pass holder, accreditation holder or employee at an access point, decided in validation with results a gate acts on (allow, deny, review, requireId, requireBiometric, requireCompanion, requireSupervisor). **identity `AuthorisationPolicy` governs who may do what in the software**: a principal's permissions on operations and screens, decided by identity `evaluateAccess`. An employee's badge opening a staff door is decided here; the same employee approving a refund is decided in identity. Effectiveness is reported per engine: `listDynamicPolicyEffectiveness` here, `listAuthorisationPolicyEffectiveness` in identity.","required":["id","scopePath","name","policyType","conditionRule","result","status","currentVersion"],"properties":{"id":{"type":"string","format":"uuid","description":"The policyId"},"venueId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node; where it applies further is access.policy_scope_assignment"},"name":{"type":"string","maxLength":200},"policyType":{"type":"string","enum":["guestAttribute","accreditation","occupancy","employee","risk","membership","timeEvent"]},"contextType":{"type":"string","enum":["date","day","time","season","event","performance","specialEvent","holiday","operatingCalendar","occupancy","attractionStatus"],"nullable":true,"description":"Context/time/event policies (setContextTimeEvent)"},"identityType":{"type":"string","enum":["guest","member","annualPassHolder","employee","contractor","vendor","performer","media","vip","security","emergencyServices","eventStaff"],"nullable":true,"description":"Identity-based policies (listIdentityMembershipAccreditation)"},"conditionRule":{"$ref":"#/components/schemas/AdmissionRule","description":"The condition, in the closed JSON rule format evaluated the same way online and at the gate (ADR-0068; replaces the free-text `conditionExpression`)."},"result":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"]},"priority":{"type":"integer","nullable":true},"allowedZoneIds":{"type":"array","items":{"type":"string","format":"uuid"}},"deniedZoneIds":{"type":"array","items":{"type":"string","format":"uuid"}},"monitorThresholdPercent":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"description":"Occupancy policies. Percent at which the band becomes Monitor"},"restrictThresholdPercent":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"description":"Occupancy policies. Percent at which the band becomes Restrict"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"The grant expires automatically at validTo"},"status":{"type":"string","enum":["draft","pendingApproval","active","inactive","expired"],"default":"draft"},"currentVersion":{"type":"integer","minimum":1,"description":"The version in force (access.dynamic_policy_version)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessOfflinePolicy": {"type":"object","x-ticvai-persistence":"access.offline_policy","description":"The offline policy of one venue: what gates validate locally and for how long, how old the revocation cache may get, and how devices step down through degraded modes. Merges access.offline_validation_profile, access.revocation_cache_policy and access.degraded_mode_policy (declared 29 September, data-model close-out DM1)","required":["id","venueId","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"maxOfflineDurationHours":{"type":"integer","minimum":0,"nullable":true,"description":"Hours a gate may validate offline"},"offlineChecks":{"type":"array","items":{"type":"string","enum":["credentialAuthenticity","digitalSignature","ticketId","venue","park","zone","visitDate","timeWindow","credentialStatusSnapshot","ticketType","guestCategory","seat","timeslot","reservation","entitlements","reEntryPermissions","validityPeriod"]},"description":"What a gate may validate locally"},"afterThresholdBehavior":{"type":"string","enum":["continueRestrictedValidation","operatorWarning","supervisorMode","failClosed","fallback"],"nullable":true},"revocationTriggerEvents":{"type":"array","items":{"type":"string","enum":["fraudLock","refund","cancellation","lostCredential","transfer","reissue","manualInvalidation"]},"description":"Events that push an invalidation into the offline cache"},"revocationMaxAllowedAgeMinutes":{"type":"integer","minimum":0,"nullable":true,"description":"Maximum allowed revocation cache age"},"revocationStalenessAction":{"type":"string","enum":["continue","continueWithWarning","restrictedProductsOnly","supervisorMode","denySelectedCredentialClasses","failClosed"],"nullable":true,"description":"What devices do when the cache is older than the maximum allowed age"},"operatingModes":{"type":"array","items":{"type":"string","enum":["online","degraded","edgeMode","localOffline","unsafeExpired"]},"description":"Operating modes a device moves through as connectivity fails"},"centralUnavailableAfterSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"Seconds without central services before switching to edge mode"},"edgeUnavailableAfterSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"Seconds without the venue edge before switching to local offline"},"automaticSwitch":{"type":"boolean","default":true,"description":"Switch modes automatically without stopping guest flow"},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessSecurityAlert": {"type":"object","x-ticvai-persistence":"access.security_alert","description":"One access security or fraud alert - severity, what was detected, where and on which credential, identity or device - including biometric anomalies and edge security events (certificate, credential or package-signature failures, unauthorised connections, device authorisation and revocation). Merges the proposed access.security_alert and access.edge_security_event (declared 29 September, data-model close-out DM1). Created `open` by the detection jobs (fraud rules, sharing detection, biometric anomaly, edge security events) and moved by updateSecurityAlert; the lifecycle is states/access-security-alert.yaml (decided 29 September, writers pass).","required":["id","scopePath","category","severity","status","detectedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The alertId / anomalyId the lists show"},"venueId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node"},"category":{"type":"string","enum":["fraudSignal","credentialSharing","duplicateAccess","blacklist","biometric","companion","edgeSecurity"]},"alertType":{"type":"string","maxLength":60,"nullable":true,"description":"The kind within the category - for fraudSignal the fraud rule's signal; for biometric one of faceChanged, reEnrollment, repeatedFaceMismatch, multipleFacesOneCredential, oneFaceMultipleCredentials, suspiciousEnrollmentFrequency, unusualVerificationFailures; for edgeSecurity one of certificateFailure, credentialFailure, packageSignatureFailure, unauthorizedConnection, deviceAuthorized, deviceRevoked"},"severity":{"type":"string","enum":["low","medium","high","critical"]},"description":{"type":"string","maxLength":500,"nullable":true,"description":"e.g. Credential attempted simultaneous entry at two gates"},"fraudRuleId":{"type":"string","format":"uuid","nullable":true,"description":"The access fraud rule that raised the alert, if one did"},"entitlementId":{"type":"string","format":"uuid","nullable":true,"description":"The credential (the list's credentialId)"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The identity concerned, where known"},"zoneId":{"type":"string","format":"uuid","nullable":true},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"The gate (the list's gateId)"},"deviceId":{"type":"string","format":"uuid","nullable":true,"description":"The device concerned, for device-sharing and edge events"},"faceReenrolmentAttemptId":{"type":"string","format":"uuid","nullable":true,"description":"Biometric alerts raised on a re-enrolment; the attempt holds the old and new references, operator, reason and review"},"faceProfileReference":{"type":"string","maxLength":200,"nullable":true,"description":"Biometric alerts. Opaque Face Pass reference; never a template"},"securityInvestigationId":{"type":"string","format":"uuid","nullable":true},"status":{"type":"string","enum":["open","acknowledged","resolved","dismissed"],"default":"open"},"detectedAt":{"type":"string","format":"date-time"},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true}}},
"ConnectivityFailureDegradedModePolicyView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Connectivity Failure & Degraded Mode Policy displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venueId":{"type":"string","description":"Venue"},"operatingModes":{"type":"array","items":{"type":"string","enum":["online","degraded","edgeMode","localOffline","unsafeExpired"]},"description":"Operating modes a device moves through as connectivity fails"},"centralUnavailableAfterSeconds":{"type":"integer","description":"Seconds without central services before switching to edge mode"},"edgeUnavailableAfterSeconds":{"type":"integer","description":"Seconds without the venue edge before switching to local offline"},"automaticSwitch":{"type":"boolean","description":"Switch modes automatically without stopping guest flow"},"lastSyncAt":{"type":"string","format":"date-time","description":"Last successful synchronization"}},"required":["venueId"]},
"ConnectivityPolicy": {"type":"object","x-ticvai-persistence":"platform.connectivity_policy","description":"Board 5 of the client's POS set, and the second of the two genuine gaps. **Nothing in the package held a threshold**, so a device that flips offline on one dropped packet and one that waits five minutes were the same product.\n**Going offline and coming back need different thresholds.** Symmetric ones produce a workstation that flaps — offline, online, offline — across a marginal connection, and each flap is a sync.\n**One per scope node, keyed on `scopePath`.** `id` is server-owned and absent where `getConnectivityPolicy` returns the defaults for a node with nothing saved.\n**The `minimum` and `maximum` on each field are proposed, client to correct (decided 28 September, audit R129).** A value outside them, or a broken cross-field rule, is refused `400` with `errors[]` naming the field.\n","required":["scopePath"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$","description":"**The node these thresholds are for, and the key `setConnectivityThresholds` upserts on.** The body names its target here, because the path does not.\n"},"failuresBeforeOffline":{"type":"integer","default":3,"minimum":1,"maximum":10,"description":"**Consecutive, not cumulative.** One dropped request on a busy till is normal; three in a row is a network.\n"},"probeIntervalSeconds":{"type":"integer","default":15,"minimum":5,"maximum":300},"probeTimeoutMs":{"type":"integer","default":2000,"minimum":500,"maximum":30000,"description":"Shorter than `probeIntervalSeconds`, or the body is refused `400` (audit R129)."},"successesBeforeOnline":{"type":"integer","default":5,"minimum":1,"maximum":20,"description":"**Higher than the offline threshold, deliberately.** Coming back is where the cost is — a workstation that returns online and immediately fails has resynced for nothing. **Never below `failuresBeforeOffline`**, or the body is refused `400` (audit R129).\n"},"minimumStableSeconds":{"type":"integer","default":30,"minimum":10,"maximum":600,"description":"How long the connection must hold before the workstation trusts it. **This is what stops the flapping**, and it is the field a venue with poor wifi will actually tune.\n"},"autoSwitch":{"type":"boolean","default":true}}},
"EdgeNodeLocalProcessingConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Edge Node & Local Processing Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"nodeType":{"type":"string","enum":["venueEdgeNode","gateController","turnstileLocalEngine","handheldLocalEngine"],"description":"Which edge component makes local access decisions"},"edgeNodeId":{"type":"string","description":"Edge Node ID"},"tenantId":{"type":"string","description":"Tenant"},"venueId":{"type":"string","description":"Venue"},"network":{"type":"string","description":"Network"},"deviceGroup":{"type":"string","description":"Device Group"},"processingMode":{"type":"string","description":"Processing Mode"},"storageAllocation":{"type":"string","description":"Storage allocation"},"redundancy":{"type":"string","description":"redundancy"},"lastHeartbeat":{"type":"string","format":"date-time","description":"Last heartbeat, set by the node, read only"},"softwareVersion":{"type":"string","description":"software version"},"securityStatus":{"type":"string","description":"security status"}},"required":["edgeNodeId","venueId","nodeType"]},
"EdgeNodeLocalProcessingConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Edge Node & Local Processing Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"nodeType":{"type":"string","enum":["venueEdgeNode","gateController","turnstileLocalEngine","handheldLocalEngine"],"description":"Which edge component makes local access decisions"},"edgeNodeId":{"type":"string","description":"Edge Node ID"},"tenantId":{"type":"string","description":"Tenant"},"venueId":{"type":"string","description":"Venue"},"network":{"type":"string","description":"Network"},"deviceGroup":{"type":"string","description":"Device Group"},"processingMode":{"type":"string","description":"Processing Mode"},"storageAllocation":{"type":"string","description":"Storage allocation"},"redundancy":{"type":"string","description":"redundancy"},"lastHeartbeat":{"type":"string","format":"date-time","description":"Last heartbeat, set by the node, read only"},"softwareVersion":{"type":"string","description":"software version"},"securityStatus":{"type":"string","description":"security status"}},"required":["edgeNodeId","venueId","nodeType"]},
"EdgePackageDataDistributionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Edge Package & Data Distribution displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"packageId":{"type":"string","description":"Edge package identifier"},"contents":{"type":"array","items":{"type":"string","enum":["venues","zones","gates","accessRules","calendars","mediaProfiles","verificationProfiles","entitlementDefinitions","trustedVerificationMaterial","revocationInformation","credentialSecurityParameters","reasonCodes","gateResponses","languages","operatorPermissions"]},"description":"Data sets included in this edge package"},"version":{"type":"string","description":"Version (the pack shows 24.6, 89 | Pag e)"},"devices":{"type":"integer","description":"Devices (the pack shows 84)"},"signatureValid":{"type":"boolean","description":"✓ Signature valid"},"packageComplete":{"type":"boolean","description":"✓ Package complete"},"versionValid":{"type":"boolean","description":"✓ Version valid"},"deviceAuthorized":{"type":"boolean","description":"✓ Device authorized"},"sizeBytes":{"type":"integer","description":"Package size"},"validFrom":{"type":"string","format":"date-time","description":"Valid from"},"validTo":{"type":"string","format":"date-time","description":"Valid to"}},"required":["packageId"]},
"EdgeSecurityAuditDeploymentView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Edge Security, Audit & Deployment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"policyVersionId":{"type":"string","description":"Edge policy version identifier"},"deploymentScope":{"type":"string","enum":["tenant","venue","park","edgeCluster","gateGroup","deviceGroup","individualDevice"],"description":"Where this edge policy version deploys"},"version":{"type":"string","description":"Version label, e.g. V4.8"},"stage":{"type":"string","enum":["draft","validated","securityTested","offlineSimulated","approved","pilot","published"],"description":"Release stage"},"isProduction":{"type":"boolean","description":"Currently in production"},"scheduledAt":{"type":"string","format":"date-time","description":"Scheduled deployment time"}},"required":["policyVersionId"]},
"EdgeSecurityAuditDeploymentViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"edgeCertificates":{"type":"integer","description":"Edge certificates"},"edgeCredentials":{"type":"integer","description":"Edge credentials"},"packageSignatures":{"type":"integer","description":"Package signatures"},"authorizedDevices":{"type":"integer","description":"Authorized devices"},"revokedDevices":{"type":"integer","description":"Revoked devices"},"failedPackageValidation":{"type":"integer","description":"Failed package validation"},"unauthorizedConnectionAttempts":{"type":"integer","description":"unauthorized connection attempts"},"configurationChanges":{"type":"integer","description":"configuration changes"},"offlineOverrideActivity":{"type":"integer","description":"offline override activity"}}},
"HardwareDeploymentInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"Deploy one gate configuration version to a target set (decided 29 September, VM close-out).","required":["id","configurationVersion","targetScope","venueId"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated deployment id"},"configurationVersion":{"type":"string","description":"The access configuration version being deployed"},"targetScope":{"type":"string","enum":["pilot","selectedGates","deviceGroup","venue"]},"venueId":{"type":"string"},"gateIds":{"type":"array","items":{"type":"string"},"description":"Required for pilot and selectedGates"},"deviceGroupId":{"type":"string","description":"Required for deviceGroup"},"runCompatibilityTestFirst":{"type":"boolean","default":true,"description":"Devices that fail the compatibility test are skipped and named in the result"},"scheduledAt":{"type":"string","format":"date-time","description":"Empty deploys now"}}},
"HardwareDeploymentView": {"type":"object","x-ticvai-persistence":"access.hardware_deployment","description":"**One rollout of one gate configuration version to one target set** (decided 29 September, VM close-out). The lifecycle is the one `tenancy.ProfileDeployment` uses for configuration profiles, so a partial failure is visible and retried or rolled back, never an end state.","required":["id","configurationVersion","targetScope","status"],"properties":{"id":{"type":"string","format":"uuid"},"configurationVersion":{"type":"string"},"targetScope":{"type":"string","enum":["pilot","selectedGates","deviceGroup","venue"]},"venueId":{"type":"string"},"gateIds":{"type":"array","items":{"type":"string"}},"deviceGroupId":{"type":"string"},"status":{"type":"string","enum":["queued","inProgress","completed","partiallyFailed","rolledBack"]},"devicesTargeted":{"type":"integer"},"devicesAcknowledged":{"type":"integer"},"failedDeviceIds":{"type":"array","items":{"type":"string"},"description":"Devices that failed the compatibility test or did not acknowledge"},"requestedByPrincipalId":{"type":"string"},"requestedAt":{"type":"string","format":"date-time"},"scheduledAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"The partition key (ADR-0005). Written at venue scope"}}},
"OfflineCredentialRevocationCacheView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Offline Credential & Revocation Cache displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venueId":{"type":"string","description":"Venue"},"triggerEvents":{"type":"array","items":{"type":"string","enum":["fraudLock","refund","cancellation","lostCredential","transfer","reissue","manualInvalidation"]},"description":"Events that push an invalidation into the offline cache"},"stalenessAction":{"type":"string","enum":["continue","continueWithWarning","restrictedProductsOnly","supervisorMode","denySelectedCredentialClasses","failClosed"],"description":"What devices do when the cache is older than the maximum allowed age"},"lastUpdated":{"type":"string","format":"date-time","description":"When the cache was last refreshed"},"ageSeconds":{"type":"integer","description":"Current cache age"},"maxAllowedAgeMinutes":{"type":"integer","description":"Maximum allowed cache age"}},"required":["venueId"]},
"OfflineEdgeOperationsCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Offline & Edge Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venueId":{"type":"string","description":"Venue"},"rulesCached":{"type":"boolean","description":"✓ Rules cached"},"verificationMaterialCurrent":{"type":"boolean","description":"✓ Verification material current"},"revocationDataCurrent":{"type":"boolean","description":"✓ Revocation data current"},"credentialDefinitionsAvailable":{"type":"boolean","description":"✓ Credential definitions available"},"deviceStorageHealthy":{"type":"boolean","description":"✓ Device storage healthy"},"lastSynchronizationSuccessful":{"type":"boolean","description":"✓ Last synchronization successful"},"venueName":{"type":"string","description":"Venue name"},"devices":{"type":"integer","description":"Devices at the venue"},"offlineReady":{"type":"integer","description":"Devices ready to operate offline"},"readinessPercent":{"type":"number","description":"Share of devices offline ready"},"packageStatus":{"type":"string","enum":["current","expiring","expired"],"description":"Edge package status"},"pendingTransactions":{"type":"integer","description":"Offline transactions not yet synchronized"},"readinessStatus":{"type":"string","enum":["ready","warning","notReady"],"description":"Venue readiness"}},"required":["venueId"]},
"OfflineEdgeOperationsCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"offlineReadyDevices":{"type":"integer","description":"Offline-Ready Devices"},"currentlyOnline":{"type":"integer","description":"Currently Online"},"currentlyOffline":{"type":"integer","description":"Currently Offline"},"devicesInDegradedMode":{"type":"integer","description":"Devices in Degraded Mode"},"edgeNodesOnline":{"type":"integer","description":"Edge Nodes Online"},"packagesCurrent":{"type":"integer","description":"Packages Current"},"packagesExpiring":{"type":"integer","description":"Packages Expiring"},"pendingOfflineTransactions":{"type":"integer","description":"Pending Offline Transactions"},"syncConflicts":{"type":"integer","description":"Sync conflicts"},"offlineSecurityAlerts":{"type":"integer","description":"Offline Security Alerts"}}},
"OfflineEntitlementUsageLedgerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Offline Entitlement & Usage Ledger displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ledgerEntryId":{"type":"string","description":"Ledger entry identifier"},"credential":{"type":"string","description":"Credential"},"device":{"type":"string","description":"Device"},"gate":{"type":"string","description":"Gate"},"entitlement":{"type":"string","description":"Entitlement"},"quantity":{"type":"integer","description":"Quantity"},"timestamp":{"type":"string","format":"date-time","description":"Timestamp"},"localSequence":{"type":"integer","description":"Device-local sequence number"},"operator":{"type":"string","description":"operator"},"decision":{"type":"string","description":"decision"},"packageVersion":{"type":"string","description":"package version"}},"required":["ledgerEntryId"]},
"OfflinePackage": {"x-ticvai-persistence":"none — generated artefact in object storage","type":"object","required":["etag","generatedAt","validFrom","validTo","accessPointId","entitlements"],"properties":{"etag":{"type":"string"},"generatedAt":{"type":"string","format":"date-time"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"accessPointId":{"type":"string","format":"uuid"},"entitlementsVersion":{"type":"integer","description":"The highest `access.entitlement` change included (SD-052, 29 September). A refresh sends it as `sinceVersion` and receives only what changed after it, so a 60,000-guest venue is not re-sent whole."},"policySetVersion":{"type":"string","description":"**The active admission policy version the package carries** (ADR-0068, 1 October): a fingerprint of the `(id, currentVersion)` of every policy in `dynamicPolicies`, computed the same way by `validateAccess` online. Every scan the gate records carries it (`ScanEvent.policySetVersion`), so a scan decided offline under a set that has since changed is visible at sync rather than assumed equal."},"dynamicPolicies":{"type":"array","description":"The active guest-admission dynamic policies for this access point's zones (SD-052), each at its active version with its `conditionRule` (ADR-0068), so an offline gate applies the same rules as an online one.","items":{"$ref":"#/components/schemas/AccessDynamicPolicy"}},"entitlements":{"type":"array","description":"Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device removes them.","items":{"type":"object","required":["ticketId","mediaCodes","validFrom","validTo","entriesAllowed","reentryAllowed"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"The `Entitlement.id`."},"mediaCodes":{"type":"array","items":{"type":"string"},"description":"A ticket may carry several media over its life."},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesAllowed":{"type":"integer","nullable":true},"entriesUsed":{"type":"integer"},"reentryAllowed":{"type":"boolean"},"admissionRulesId":{"type":"string","format":"uuid"}}}},"delegatedRights":{"type":"array","description":"Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits when the inter-cell link is down — the same reason locally issued entitlements are included.\n","items":{"type":"object","required":["rightId","ticketId","issuingCellId","validFrom","validTo","entriesAllowed","entriesConsumed"],"properties":{"rightId":{"type":"string"},"ticketId":{"type":"string","format":"uuid","description":"The `Entitlement.id` in the issuing cell."},"issuingCellId":{"type":"string"},"guestLinkId":{"type":"string","nullable":true},"mediaCodes":{"type":"array","items":{"type":"string"}},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"entriesAllowed":{"type":"integer","nullable":true},"entriesConsumed":{"type":"integer"},"admissionRulesId":{"type":"string","format":"uuid"}}}},"blacklist":{"type":"array","items":{"type":"string"},"description":"Media codes to deny outright regardless of entitlement state."},"admissionRules":{"type":"array","items":{"type":"object","required":["id","openMinutesBefore","closeMinutesAfter"],"properties":{"id":{"type":"string","format":"uuid"},"openMinutesBefore":{"type":"integer"},"closeMinutesAfter":{"type":"integer"},"maxDurationMinutes":{"type":"integer","nullable":true},"requiresExitBeforeReentry":{"type":"boolean"}}}},"accreditationCredentials":{"type":"array","description":"Accreditation credentials that admit at this access point, from access.accreditation_credential (29 September, build; BL-181). Only rows that admit are included; a credential dropped from one package to the next no longer admits.","items":{"$ref":"#/components/schemas/AccessAccreditationCredential"}}}},
"OfflinePolicy": {"type":"object","x-ticvai-persistence":"platform.offline_policy","description":"Board 5 of the client's POS set. **ADR-0013 makes the POS local-first and nothing configured the policy** — one of only two things in 36 board screens the package genuinely could not do.\nCF-115 reframed offline into three data classes: catalogue and policy always local, contended inventory leased, transactional facts journalled. **This is where a venue says how far that goes for them.**\n**One per scope node, keyed on `scopePath`** (pull audit R162). `id` is server-owned and absent where `getOfflinePolicy` returns the defaults for a node with nothing saved.\n**The `minimum` and `maximum` on each field are proposed, client to correct (decided 28 September, audit R129).** A value outside them is refused `400`, `errors[]` naming the field.\n","required":["scopePath"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$","description":"**The node this policy is for, and the key `setOfflinePolicy` upserts on.** The body names its target here, because the path does not.\n"},"maxOfflineHours":{"type":"integer","default":24,"minimum":1,"maximum":72,"description":"**After which the workstation refuses to sell rather than keep journalling.** A till three days offline holding 900 unsynced sales is a reconciliation nobody can do and a fraud nobody can detect. Bounds 1 to 72 hours: proposed, client to correct (audit R129).\n"},"allowedOffline":{"type":"array","description":"**What may happen with no network**, by data class. Selling from a cached catalogue is safe; issuing a refund is not, because the original sale cannot be verified.\n","items":{"type":"string","enum":["sale","refund","exchange","entitlementIssue","entitlementValidate","loyaltyAccrual","loyaltyRedemption","walletSpend","priceOverride","discount","voidLine","noSale"]}},"offlineValueCeiling":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Above zero, and in the currency of the venue the policy resolves to; a ceiling in another currency is refused `400` (decided 28 September, audit R129).\n"},"offlineTransactionCeiling":{"type":"integer","nullable":true,"minimum":1,"maximum":5000,"description":"**A ceiling on count as well as value.** Nine hundred small sales and one large one are different risks, and a value ceiling alone catches only the second. Bounds 1 to 5,000: proposed, client to correct (audit R129).\n"},"onCeilingBreach":{"type":"string","enum":["warn","blockNewSales","blockAll"],"default":"blockNewSales"},"requiresManagerToExtend":{"type":"boolean","default":true}}},
"OfflineSimulationResilienceTestingInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Offline Simulation & Resilience Testing submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"scenario":{"type":"string","enum":["centralOutage","edgeOutage","fullOffline"],"description":"Outage scenario to simulate"},"venueId":{"type":"string","description":"Venue under test"},"dynamicQrVerifiedLocally":{"type":"boolean","description":"✓ Dynamic QR verified locally"},"ticketDateVerified":{"type":"boolean","description":"✓ Ticket date verified"},"entryEntitlementVerified":{"type":"boolean","description":"✓ Entry entitlement verified"},"antiPassbackEnforced":{"type":"boolean","description":"✓ Anti-passback enforced"},"gateOpens":{"type":"boolean","description":"✓ Gate opens"},"attendanceStoredLocally":{"type":"boolean","description":"✓ Attendance stored locally"},"transactionQueued":{"type":"boolean","description":"✓ Transaction queued"},"validationCount":{"type":"integer","description":"Number of simulated validations"},"switchedToEdgeMode":{"type":"boolean","description":"Gate switched to edge mode"},"result":{"type":"string","enum":["passed","failed"],"description":"Offline readiness result, read only"}},"required":["venueId","scenario"]},
"OfflineSimulationResilienceTestingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Offline Simulation & Resilience Testing displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"scenario":{"type":"string","enum":["centralOutage","edgeOutage","fullOffline"],"description":"Outage scenario to simulate"},"venueId":{"type":"string","description":"Venue under test"},"dynamicQrVerifiedLocally":{"type":"boolean","description":"✓ Dynamic QR verified locally"},"ticketDateVerified":{"type":"boolean","description":"✓ Ticket date verified"},"entryEntitlementVerified":{"type":"boolean","description":"✓ Entry entitlement verified"},"antiPassbackEnforced":{"type":"boolean","description":"✓ Anti-passback enforced"},"gateOpens":{"type":"boolean","description":"✓ Gate opens"},"attendanceStoredLocally":{"type":"boolean","description":"✓ Attendance stored locally"},"transactionQueued":{"type":"boolean","description":"✓ Transaction queued"},"validationCount":{"type":"integer","description":"Number of simulated validations"},"switchedToEdgeMode":{"type":"boolean","description":"Gate switched to edge mode"},"result":{"type":"string","enum":["passed","failed"],"description":"Offline readiness result, read only"}},"required":["venueId","scenario"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ReconnectionSynchronizationConflictResolutionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Reconnection, Synchronization & Conflict Resolution displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"conflictId":{"type":"string","description":"Conflict identifier"},"centralRemainingBalanceBeforeOutage":{"type":"integer","description":"Entitlement uses remaining centrally before the outage (a count, not money)"},"resolutionPolicy":{"type":"string","enum":["preserveBothAndFlag","earliestTransactionWins","configuredBusinessRule","supervisorReview","securityInvestigation"],"description":"How this conflict is resolved"},"credentialId":{"type":"string","description":"Credential involved"}},"required":["conflictId"]},
"ReconnectionSynchronizationConflictResolutionViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"pendingScans":{"type":"integer","description":"Pending scans"},"entitlementEvents":{"type":"integer","description":"Entitlement events"},"entries":{"type":"integer","description":"Entries"},"exits":{"type":"integer","description":"Exits"},"overrides":{"type":"integer","description":"Overrides"},"securityEvents":{"type":"integer","description":"Security events"}}}
}
```
