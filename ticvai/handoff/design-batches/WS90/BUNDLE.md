# WS90 — Rental Management board 3

**10 screens · 7 operations · 7 schemas · 5 permissions**

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
  `PRICE_VIEW, RENTAL_CONFIGURE, RENTAL_MANAGE, RENTAL_VIEW, RESOURCE_VIEW`. A control nobody can use must say so,
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
| `BO-514` | Availability Command Center | B–D | 2 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-515` | Availability Rule Configuration | B–D | 10 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-516` | Operating Hours & Rental Windows | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-517` | Timeslot & Duration Availability Setup | B–D | 7 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-518` | Real-Time Availability Calendar | B–D | 0 | 3 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-519` | Resource / Equipment Calendar | B–D | 5 | 25 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-520` | Blackout, Closure & Capacity Blocking | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-521` | Overlap & Conflict Engine | B–D | 5 | 14 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-522` | Inventory Holds, Buffers & Release Rules | B–D | 0 | 0 | 6 | 0 | 1 | 4 | — | notStarted (—) |
| `BO-523` | Availability Intelligence & AI Forecasting | B–D | 0 | 16 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-516, BO-518, BO-520, BO-522, BO-523 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-514` Availability Command Center

**Provide management and operators with a real-time overview of rental availability across all locations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/availability-command-center-bo-514` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search availability | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, rental location, product, category, date and 2 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `getRentalAvailability` ?productId |
| Location | picker: choose a location | — | — | `getRentalAvailability` ?locationId |
| From | date and time picker | — | — | `getRentalAvailability` ?from |
| To | date and time picker | — | — | `getRentalAvailability` ?to |
| Quantity | number field | 1 | — | `getRentalAvailability` ?quantity |

#### Outputs: what the screen shows and produces

**Shown**

**Total Rentable Inventory** (metric tile)

**Available Now** (metric tile)

**Reserved** (metric tile)

**Currently Rented** (metric tile)

**Maintenance Blocked** (metric tile)

**Operationally Blocked** (metric tile)

**Next 2 Hours Demand** (metric tile)

**Availability Risk** (metric tile)

**Data it reads**: `getRentalAvailability` (onLoad, What is free, across products)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-515` Availability Rule Configuration: *Availability Rule Configuration*; carries `productId`
- → `BO-516` Operating Hours & Rental Windows: *Operating Hours & Rental Windows*; carries `productId`
- → `BO-517` Timeslot & Duration Availability Setup: *Timeslot & Duration Availability Setup*; carries `productId`
- → `BO-518` Real-Time Availability Calendar: *Real-Time Availability Calendar*
- → `BO-519` Resource / Equipment Calendar: *Resource / Equipment Calendar*
- → `BO-520` Blackout, Closure & Capacity Blocking: *Blackout, Closure & Capacity Blocking*; carries `productId`
- → `BO-521` Overlap & Conflict Engine: *Overlap & Conflict Engine*
- → `BO-522` Inventory Holds, Buffers & Release Rules: *Inventory Holds, Buffers & Release Rules*; carries `productId`
- → `BO-523` Availability Intelligence & AI Forecasting: *Availability Intelligence & AI Forecasting*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The availability list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the availability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No availability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the availability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getRentalAvailability` → `RENTAL_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Real-time availability view shows total, available, rented and returned inventory per item and per location, alongside revenue generated. *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-747)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-514` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS118 Rental Management Board 3.dc.html#bo-514`
- Workshop pack: Rental_Management.pdf board 3
- Flow F199 *Rental Management board 3: Availability Command Center*, step 1: Opens Availability Command Center → Provide management and operators with a real-time overview of rental availability across all locations.
- Flow F199 *Rental Management board 3: Availability Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F199 *Rental Management board 3: Availability Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F199 *Rental Management board 3: Availability Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F199 *Rental Management board 3: Availability Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F199 *Rental Management board 3: Availability Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F199 *Rental Management board 3: Availability Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F199 *Rental Management board 3: Availability Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F199 branch at step 1 (expected): when Nothing has been set up on Availability Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F199 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-514?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-515`, `BO-516`, `BO-517`, `BO-518`, `BO-519`, `BO-520`, `BO-521`, `BO-522`, `BO-523`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-515` Availability Rule Configuration

**Define the fundamental rules used by the availability engine for each rental product.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure availability according to; Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/rentals/availability-rule-configuration-bo-515` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Physical inventory | select field | — | — | — | — | — | — |
| Location allocation | select field | — | — | — | — | — | — |
| Existing reservations | select field | — | — | — | — | — | — |
| Active rentals | select field | — | — | — | — | — | — |
| Maintenance blocks | select field | — | — | — | — | — | — |
| Out-of-service assets | select field | — | — | — | — | — | — |
| Inventory buffer | select field | — | — | — | — | — | — |
| Turnaround time | select field | — | — | — | — | — | — |
| Operating hours | select field | — | — | — | — | — | — |
| Booking Availability: ON | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-514` Availability Command Center: *Back to Availability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The availability rule configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the availability rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No availability rule configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setRentalAvailabilityRules` → `RENTAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Per-item availability rules: minimum advance booking time, maximum advance window, last-minute cutoff, same-day booking allowed, min/max booking quantity. Operating hours per station; slot inventory per window (e.g. 10 kayaks 10-11 and 11-12, then 5 at 12-1). *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-748)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-515` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS118 Rental Management Board 3.dc.html#bo-515`
- Workshop pack: Rental_Management.pdf board 3
- Flow F199 *Rental Management board 3: Availability Command Center*, step 2: Works in Availability Rule Configuration → Define the fundamental rules used by the availability engine for each rental product.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-515?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-514`.
- [ ] Every gated control is gated: `RENTAL_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-516` Operating Hours & Rental Windows

**Control when rental products can actually be booked and used. The source specifically requires inventory allocation according to operating hours.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/rentals/operating-hours-rental-windows-bo-516` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-514` Availability Command Center: *Back to Availability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operating hours rental list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operating hours rental untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operating hours rental yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the operating hours rental are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setRentalAvailabilityRules` → `RENTAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Per-item availability rules: minimum advance booking time, maximum advance window, last-minute cutoff, same-day booking allowed, min/max booking quantity. Operating hours per station; slot inventory per window (e.g. 10 kayaks 10-11 and 11-12, then 5 at 12-1). *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-748)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-516` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS118 Rental Management Board 3.dc.html#bo-516`
- Workshop pack: Rental_Management.pdf board 3
- Flow F199 *Rental Management board 3: Availability Command Center*, step 4: Works in Operating Hours & Rental Windows → Control when rental products can actually be booked and used. The source specifically requires inventory allocation according to operating hours.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-516?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-514`.
- [ ] Every gated control is gated: `RENTAL_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-517` Timeslot & Duration Availability Setup

**Configure how rental availability is presented to customers. The source supports both fixed and customer-defined rental periods.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Duration options; Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/rentals/timeslot-duration-availability-setup-bo-517` |

**Known gaps.** **Timeslot & Duration Availability Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Slot Interval | select field | — | — | — | — | — | — |
| Fixed/Flexible Start | select field | — | — | — | — | — | — |
| Allowed Durations | select field | — | — | — | — | — | — |
| Minimum Duration | select field | — | — | — | — | — | — |
| Maximum Duration | select field | — | — | — | — | — | — |
| Turnaround Time | select field | — | — | — | — | — | — |
| Booking Cutoff | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-514` Availability Command Center: *Back to Availability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The timeslot duration availability configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the timeslot duration availability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No timeslot duration availability configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setRentalDurationRules` → `RENTAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Per-item availability rules: minimum advance booking time, maximum advance window, last-minute cutoff, same-day booking allowed, min/max booking quantity. Operating hours per station; slot inventory per window (e.g. 10 kayaks 10-11 and 11-12, then 5 at 12-1). *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-748)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-517` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS118 Rental Management Board 3.dc.html#bo-517`
- Workshop pack: Rental_Management.pdf board 3
- Flow F199 *Rental Management board 3: Availability Command Center*, step 6: Works in Timeslot & Duration Availability Setup → Configure how rental availability is presented to customers. The source supports both fixed and customer-defined rental periods.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-517?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-514`.
- [ ] Every gated control is gated: `RENTAL_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-518` Real-Time Availability Calendar

**Provide the operational calendar explicitly required by the source.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW`, `RENTAL_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/real-time-availability-calendar-bo-518` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `getRentalAvailability` ?productId |
| Location | picker: choose a location | — | — | `getRentalAvailability` ?locationId |
| From | date and time picker | — | — | `getRentalAvailability` ?from |
| To | date and time picker | — | — | `getRentalAvailability` ?to |
| Quantity | number field | 1 | — | `getRentalAvailability` ?quantity |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Calendar** (calendar view, from `listRealTimeAvailability`): Rental availability by day and hour. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Filters the category on what it read.

| Shows | Format | Notes |
|---|---|---|
| Failed checks | list or chips (count when long) | Checkout validations that failed; empty means the bundle is sellable. |
| Bundle | text | Bundle ID |
| Sellable | yes / no (icon or chip) | Whether the bundle can be sold now |

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listRealTimeAvailability` (onLoad, Real-Time Availability & Checkout Validation); `getRentalAvailability` (onLoad, Live availability)

**Where the user goes next**

- → `BO-514` Availability Command Center: *Back to Availability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The real-time availability calendar list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the real-time availability calendar untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No real-time availability calendar yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the real-time availability calendar are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listRealTimeAvailability` → `PRICE_VIEW` (read) · staff
- `getRentalAvailability` → `RENTAL_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Real-time availability view shows total, available, rented and returned inventory per item and per location, alongside revenue generated. *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-747)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-518` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS118 Rental Management Board 3.dc.html#bo-518`
- Workshop pack: Rental_Management.pdf board 3
- Flow F199 *Rental Management board 3: Availability Command Center*, step 8: Works in Real-Time Availability Calendar → Provide the operational calendar explicitly required by the source.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (3 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-518?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-514`.
- [ ] Every gated control is gated: `PRICE_VIEW`, `RENTAL_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-519` Resource / Equipment Calendar

**Provide asset-level availability for serialized inventory.**

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
| Route | `/rentals/resource-equipment-calendar-bo-519` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | — | — | — | — | Sends `?from=` (required). | — |
| To | date picker | — | — | — | — | Sends `?to=` (required). | — |
| Resource type | select field | — | — | — | — | Sends `?resourceTypeId=` (bikes, kayaks, watercraft, wheelchairs, cabanas). | — |
| Category | select field | — | — | — | — | Sends `?categoryId=`. | — |
| View | select field | — | — | — | — | Sends `?granularity=` (day, week, month, agenda). | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceCalendar` ?from |
| To | date and time picker | — | — | `getResourceCalendar` ?to |
| Resource type | picker: choose a resource type | — | — | `getResourceCalendar` ?resourceTypeId |
| Category | picker: choose a category | — | — | `getResourceCalendar` ?categoryId |
| Granularity | radio group | — | Day · Week · Month · Agenda | `getResourceCalendar` ?granularity |

#### Outputs: what the screen shows and produces

**Shown**

**Calendar** (calendar view, from `getResourceCalendar`): Resource and equipment bookings by hour. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Filters the category on what it read.

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

**Equipment timeline** (data table, from `getResourceCalendar`): One row per serialised resource; `segments` drawn as coloured blocks across the hours, as in the pack's BIKE-001 to BIKE-004 grid.

| Shows | Format | Notes |
|---|---|---|
| Resource name | text | — |
| Resource type | the name it points at, never the id | — |
| Utilisation percent | 1,234.5 | — |
| Segments | list or chips (count when long) | — |

**The selected block** (detail panel, from `getResourceCalendar`): The pack's block drill-down; only the reservation reference (`bookingId`) and state are bound.

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| State | chip: Available, Reserved, Assigned, Partially utilised, Fully utilised, Unavailable… | — |
| Booking | the name it points at, never the id | — |
| Conflicts with | list or chips (count when long) | — |
| Customer | text | not in the schema: `Customer` |
| Expected checkout | text | not in the schema: `Expected checkout` |
| Expected return | text | not in the schema: `Expected return` |
| Turnaround | text | not in the schema: `Turnaround` |
| Equipment status | text | not in the schema: `Equipment status` |
| Related maintenance | text | not in the schema: `Related maintenance` |

**Data it reads**: `getResourceCalendar` (onLoad, Equipment against time)

**Where the user goes next**

- → `BO-514` Availability Command Center: *Back to Availability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource equipment calendar list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource equipment calendar untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource equipment calendar yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the resource equipment calendar are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getResourceCalendar` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Resource/equipment calendar shows a visual booking timeline per item across the day; blockout dates; overlap/conflict validation prevents double-booking before publish; holds/buffers per channel (online, POS, B2B) with release rules; demand forecast visual. *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-749)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-519` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS118 Rental Management Board 3.dc.html#bo-519`
- Workshop pack: Rental_Management.pdf board 3
- Flow F199 *Rental Management board 3: Availability Command Center*, step 10: Works in Resource / Equipment Calendar → Provide asset-level availability for serialized inventory.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-519?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-514`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-520` Blackout, Closure & Capacity Blocking

**Allow authorized users to deliberately remove inventory from sale. The original scope requires seasonal availability, blackout dates and maintenance periods.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_CONFIGURE`, `RENTAL_MANAGE`, `RENTAL_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/rentals/blackout-closure-capacity-blocking-bo-520` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Location | picker: choose a location | — | — | `listRentalProducts` ?locationId |
| Category | picker: choose a category | — | — | `listRentalProducts` ?categoryId |
| Tracking model | segmented control | — | Pooled · Serialised · Hybrid | `listRentalProducts` ?trackingModel |
| Status | text field | — | — | `listRentalProducts` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Selected weekdays (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listRentalProducts` (onLoad, The rental products whose availability is blocked)

**Where the user goes next**

- → `BO-514` Availability Command Center: *Back to Availability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The blackout closure capacity list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the blackout closure capacity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No blackout closure capacity yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the blackout closure capacity are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Bookings exist in the window; they are listed |

#### Permissions

- `createRentalBlackout` → `RENTAL_MANAGE` (configure) · staff
- `setRentalAvailabilityRules` → `RENTAL_CONFIGURE` (configure) · staff
- `listRentalProducts` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resource/equipment calendar shows a visual booking timeline per item across the day; blockout dates; overlap/conflict validation prevents double-booking before publish; holds/buffers per channel (online, POS, B2B) with release rules; demand forecast visual. *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-749)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-520` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS118 Rental Management Board 3.dc.html#bo-520`
- Workshop pack: Rental_Management.pdf board 3
- Flow F199 *Rental Management board 3: Availability Command Center*, step 12: Works in Blackout, Closure & Capacity Blocking → Allow authorized users to deliberately remove inventory from sale. The original scope requires seasonal availability, blackout dates and maintenance periods.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-520?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Selected weekdays, Cancel.
- [ ] Every transition is wired: `BO-514`.
- [ ] Every gated control is gated: `RENTAL_CONFIGURE`, `RENTAL_MANAGE`, `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-521` Overlap & Conflict Engine

**Provide transparency into one of the most important calculations in the rental system. The original requirement explicitly states: Calculate overlapping rentals and prevent inventory conflicts.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/overlap-conflict-engine-bo-521` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Rental product | select field | — | — | — | — | Sends `?productId=` (required). | — |
| Location | select field | — | — | — | — | Sends `?locationId=`. | — |
| From | date picker | — | — | — | — | Sends `?from=` (required). | — |
| To | date picker | — | — | — | — | Sends `?to=` (required). | — |
| Quantity requested | number field | — | — | — | — | Sends `?quantity=`. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `getRentalAvailability` ?productId |
| Location | picker: choose a location | — | — | `getRentalAvailability` ?locationId |
| From | date and time picker | — | — | `getRentalAvailability` ?from |
| To | date and time picker | — | — | `getRentalAvailability` ?to |
| Quantity | number field | 1 | — | `getRentalAvailability` ?quantity |

#### Outputs: what the screen shows and produces

**Shown**

**Sellable inventory** (metric tile, from `getRentalAvailability`): The lowest `availableQuantity` across the requested period.

| Shows | Format | Notes |
|---|---|---|
| Available quantity | 1,234 | — |

**Physical allocation** (metric tile): The pack asks for physical allocation; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Physical allocation | text | not in the schema: `Physical allocation` |

**Overlapping active rentals** (metric tile): The pack asks for overlapping active rentals; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Overlapping active rentals | text | not in the schema: `Overlapping active rentals` |

**Safety buffer** (metric tile): The pack asks for safety buffer; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Safety buffer | text | not in the schema: `Safety buffer` |

**Blocking windows (conflict types)** (data table, from `getRentalAvailability`): `reason` covers booked, turnaround, maintenance, blackout, closed, buffer and held; the pack's rental-extension and location conflicts have no value.

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| Reason | chip: Booked, Turnaround, Maintenance, Blackout, Closed, Buffer… | — |

**Available windows** (data table, from `getRentalAvailability`): The alternative times ("14:30 - 10 available") come from here.

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| Available quantity | 1,234 | — |
| Available assets | list or chips (count when long) | — |

**Alternative recommendation** (detail panel): Alternative locations need a second read per location; the pack's Marina Station example is not returned by one call.

| Shows | Format | Notes |
|---|---|---|
| Alternative location | text | not in the schema: `Alternative location` |
| Available quantity there | text | not in the schema: `Available quantity there` |
| Alternative start time | text | not in the schema: `Alternative start time` |

**Data it reads**: `getRentalAvailability` (onLoad, Where bookings overlap)

**Where the user goes next**

- → `BO-514` Availability Command Center: *Back to Availability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The overlap conflict list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the overlap conflict untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No overlap conflict yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the overlap conflict are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getRentalAvailability` → `RENTAL_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resource/equipment calendar shows a visual booking timeline per item across the day; blockout dates; overlap/conflict validation prevents double-booking before publish; holds/buffers per channel (online, POS, B2B) with release rules; demand forecast visual. *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-749)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-521` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS118 Rental Management Board 3.dc.html#bo-521`
- Workshop pack: Rental_Management.pdf board 3
- Flow F199 *Rental Management board 3: Availability Command Center*, step 14: Works in Overlap & Conflict Engine → Provide transparency into one of the most important calculations in the rental system. The original requirement explicitly states: Calculate overlapping rentals and prevent inventory conflicts.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-521?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-514`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-522` Inventory Holds, Buffers & Release Rules

**Control inventory that should temporarily or permanently be withheld from normal sales. The source explicitly requires configurable inventory buffers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/rentals/inventory-holds-buffers-release-rules-bo-522` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-514` Availability Command Center: *Back to Availability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The inventory holds buffers list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the inventory holds buffers untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No inventory holds buffers yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the inventory holds buffers are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setRentalAvailabilityRules` → `RENTAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resource/equipment calendar shows a visual booking timeline per item across the day; blockout dates; overlap/conflict validation prevents double-booking before publish; holds/buffers per channel (online, POS, B2B) with release rules; demand forecast visual. *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-749)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-522` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS118 Rental Management Board 3.dc.html#bo-522`
- Workshop pack: Rental_Management.pdf board 3
- Flow F199 *Rental Management board 3: Availability Command Center*, step 16: Works in Inventory Holds, Buffers & Release Rules → Control inventory that should temporarily or permanently be withheld from normal sales. The source explicitly requires configurable inventory buffers.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-522?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-514`.
- [ ] Every gated control is gated: `RENTAL_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-523` Availability Intelligence & AI Forecasting

**Use AI to forecast demand and proactively optimize rental availability. The source recommends AI-based utilization and demand forecasting.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/availability-intelligence-ai-forecasting-bo-523` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `getRentalAvailability` ?productId |
| Location | picker: choose a location | — | — | `getRentalAvailability` ?locationId |
| From | date and time picker | — | — | `getRentalAvailability` ?from |
| To | date and time picker | — | — | `getRentalAvailability` ?to |
| Quantity | number field | 1 | — | `getRentalAvailability` ?quantity |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every availability intelligence forecasting** (data table)

| Shows | Format | Notes |
|---|---|---|
| Forecast demand | text | not in the schema: `Forecast Demand` |
| Forecast utilization | text | not in the schema: `Forecast Utilization` |
| Sell out probability | text | not in the schema: `Sell-Out Probability` |
| Inventory shortage risk | text | not in the schema: `Inventory Shortage Risk` |
| Excess inventory | text | not in the schema: `Excess Inventory` |
| Location imbalance | text | not in the schema: `Location Imbalance` |
| Expected cancellations | text | not in the schema: `Expected Cancellations` |
| Expected late returns | text | not in the schema: `Expected Late Returns` |

**The selected availability intelligence forecasting** (detail panel): The pack groups this record's detail under its own headings: “North Station”, “Important Availability Formula”, “Allocated Physical Inventory”.

| Shows | Format | Notes |
|---|---|---|
| Forecast demand | text | not in the schema: `Forecast Demand` |
| Forecast utilization | text | not in the schema: `Forecast Utilization` |
| Sell out probability | text | not in the schema: `Sell-Out Probability` |
| Inventory shortage risk | text | not in the schema: `Inventory Shortage Risk` |
| Excess inventory | text | not in the schema: `Excess Inventory` |
| Location imbalance | text | not in the schema: `Location Imbalance` |
| Expected cancellations | text | not in the schema: `Expected Cancellations` |
| Expected late returns | text | not in the schema: `Expected Late Returns` |

**Data it reads**: `getRentalAvailability` (onLoad, Availability forecast)

**Where the user goes next**

- → `BO-514` Availability Command Center: *Back to Availability Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The availability intelligence forecasting list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the availability intelligence forecasting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No availability intelligence forecasting yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the availability intelligence forecasting are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getRentalAvailability` → `RENTAL_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Resource/equipment calendar shows a visual booking timeline per item across the day; blockout dates; overlap/conflict validation prevents double-booking before publish; holds/buffers per channel (online, POS, B2B) with release rules; demand forecast visual. *(client request · MoM 9 Sep 2026, 4.4 Rental Availability, Scheduling & Channel Allocation · DI-749)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-523` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS118 Rental Management Board 3.dc.html#bo-523`
- Workshop pack: Rental_Management.pdf board 3
- Flow F199 *Rental Management board 3: Availability Command Center*, step 18: Works in Availability Intelligence & AI Forecasting → Use AI to forecast demand and proactively optimize rental availability. The source recommends AI-based utilization and demand forecasting.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-523?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-514`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
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

**12 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createRentalBlackout": {"method":"POST","path":"/rental-blackouts","contract":"rental","summary":"Close a product, location or window","permission":"RENTAL_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalBlackout","responds":"RentalBlackout"},
"getRentalAvailability": {"method":"GET","path":"/rental-availability","contract":"rental","summary":"What can be rented, when, with turnaround already subtracted","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":true},{"name":"locationId","in":"query","required":null},{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"quantity","in":"query","required":null}],"requestBody":null,"responds":"RentalAvailability"},
"getResourceCalendar": {"method":"GET","path":"/resource-calendar","contract":"resources","summary":"Every resource against time, with conflicts already marked","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"resourceTypeId","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"granularity","in":"query","required":null}],"requestBody":null,"responds":"ResourceCalendarRow"},
"listRealTimeAvailability": {"method":"GET","path":"/real-time-availability","contract":"promotions","summary":"Real-Time Availability & Checkout Validation","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RealTimeAvailabilityCheckoutValidationView"},
"listRentalProducts": {"method":"GET","path":"/rental-products","contract":"rental","summary":"Rental products across venues and locations","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"locationId","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"trackingModel","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"RentalProduct"},
"setRentalAvailabilityRules": {"method":"PUT","path":"/rental-products/{productId}/availability-rules","contract":"rental","summary":"Operating hours, rental windows, buffers and release rules","permission":"RENTAL_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalAvailabilityRules","responds":"RentalAvailabilityRules"},
"setRentalDurationRules": {"method":"PUT","path":"/rental-products/{productId}/duration","contract":"rental","summary":"Minimum, maximum, increment, extension and turnaround","permission":"RENTAL_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalDurationRules","responds":"RentalDurationRules"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"RealTimeAvailabilityCheckoutValidationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Real-Time Availability & Checkout Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"failedChecks":{"type":"array","items":{"type":"string","enum":["productInactive","inventoryUnavailable","capacityUnavailable","timeslotUnavailable","resourceUnavailable","priceInvalid","promotionInvalid","partnerComponentInvalid","componentMappingInvalid"]},"description":"Checkout validations that failed; empty means the bundle is sellable."},"bundleId":{"type":"string","description":"Bundle ID"},"sellable":{"type":"boolean","description":"Whether the bundle can be sold now"}}},
"RentalAvailability": {"type":"object","description":"Board 3. **A pooled product answers with a count, a serialised one with assets.**","properties":{"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid","nullable":true},"windows":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"availableQuantity":{"type":"integer"},"availableAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"blockedWindows":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"reason":{"type":"string","enum":["booked","turnaround","maintenance","blackout","closed","buffer","held"]}}}}}},
"RentalAvailabilityRules": {"type":"object","x-ticvai-persistence":"rental.availability_rules","description":"Boards 3.2, 3.3 and 3.9. **The hold-release rule is the one that quietly loses stock.**\n","properties":{"operatingWindows":{"type":"array","items":{"type":"object","properties":{"daysOfWeek":{"type":"array","items":{"type":"string"}},"from":{"type":"string"},"to":{"type":"string"}}}},"slotMinutes":{"type":"integer","nullable":true},"holdMinutes":{"type":"integer","default":15,"description":"**How long an unconfirmed basket keeps stock.** A hold that never expires removes inventory from sale after every abandoned checkout.\n"},"releaseOnPaymentFailure":{"type":"boolean","default":true},"overbookPercent":{"type":"number","default":0},"scopePath":{"type":"string"}}},
"RentalBlackout": {"type":"object","x-ticvai-persistence":"rental.blackout","description":"Board 3.7. **Closure and capacity reduction are one act at different strengths.**","required":["from","to","reason"],"properties":{"id":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"reason":{"type":"string"},"capacityPercent":{"type":"integer","default":0,"description":"Zero closes it; fifty halves it."},"scopePath":{"type":"string"}}},
"RentalDurationRules": {"type":"object","x-ticvai-persistence":"rental.duration_rules","description":"Board 1.7. **Turnaround feeds availability automatically.** *10:00–11:00 rental, 11:00–11:15 turnaround, next available 11:15.*\n","properties":{"minimumMinutes":{"type":"integer"},"maximumMinutes":{"type":"integer"},"incrementMinutes":{"type":"integer","default":15},"defaultMinutes":{"type":"integer"},"turnaroundMinutes":{"type":"integer","default":0},"extensionAllowed":{"type":"boolean","default":true},"maximumExtensionMinutes":{"type":"integer","nullable":true},"sameDayReturnRequired":{"type":"boolean","default":false},"overnightAllowed":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"RentalProduct": {"type":"object","x-ticvai-persistence":"rental.product","description":"Board 1.3. **The master reference every later board resolves against.**","required":["code","name","venueId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"internalName":{"type":"string","nullable":true},"description":{"type":"string","nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"imageAssetId":{"type":"string","format":"uuid","nullable":true},"tags":{"type":"array","items":{"type":"string"}},"tenantId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"trackingModel":{"type":"string","enum":["pooled","serialised","hybrid"]},"catalogueProductId":{"type":"string","format":"uuid","nullable":true,"description":"**The thing the guest actually buys.** `catalogue` sells it and this configures how it behaves once sold; the link is here so a rental is never sold twice through two different product records.\n"},"resourceTypeId":{"type":"string","format":"uuid","nullable":true,"description":"**For serialised products, the `resources` type its assets belong to.** The individual bikes are resources and maintenance assets — this contract does not keep a third register of them.\n"},"status":{"type":"string","enum":["draft","configurationReview","approved","active","suspended","archived"]},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"version":{"type":"integer","default":1},"isActive":{"type":"boolean","default":true}}},
"ResourceCalendarRow": {"type":"object","description":"Board 2.01. **One resource across the window, with its states already computed** — including conflict, which a client cannot derive from a booking list.\n","properties":{"resourceId":{"type":"string","format":"uuid"},"resourceName":{"type":"string"},"resourceTypeId":{"type":"string","format":"uuid"},"utilisationPercent":{"type":"number"},"segments":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"state":{"type":"string","enum":["available","reserved","assigned","partiallyUtilised","fullyUtilised","unavailable","onBreak","onLeave","underMaintenance","operationallyBlocked","pendingApproval","conflict"]},"bookingId":{"type":"string","format":"uuid","nullable":true},"conflictsWith":{"type":"array","items":{"type":"string","format":"uuid"}}}}}}}
}
```
