# P06-rentals-03 — P06 · Rentals (3 of 3)

**10 screens · 6 operations · 10 schemas · 3 permissions**

Platform P06 Venue Staff App · ships as **venue-staff-mobile** ·
staff audience · mobileApp ·
offline-capable

## Who this is for

**staff on mobileApp.** Everything below is how you know what is
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
  `ASSET_MANAGE, RENTAL_OPERATE, RENTAL_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **3 of these operations work offline**: recordRentalInspection, returnRental, setAssetStatus
  — and the rest do not. A surface that looks the same online and off is lying.
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
| `EMP-091` | Rental Return Command Center | B–D | 2 | 0 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `EMP-092` | Return Scan & Rental Retrieval | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `EMP-093` | Return Summary & Actual Return Time | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `EMP-094` | Post-Rental Condition Inspection | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `EMP-095` | Before vs After Condition Comparison | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `EMP-096` | Damage Assessment & Charge Workflow | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `EMP-097` | Partial Return & Missing Equipment | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `EMP-098` | Late Fees, Damage Fees & Final Settlement | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `EMP-099` | Deposit Release, Capture & Customer Confirmation | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `EMP-100` | Return Completion & Equipment Disposition | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**EMP-092, EMP-093, EMP-094, EMP-095, EMP-096, EMP-097, EMP-098, EMP-099, EMP-100 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `EMP-091` Rental Return Command Center

**Provide operators with a live operational view of all expected, in-progress, partial, overdue and completed returns.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | commandCentre (comfortable density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/rental-return-command-center-emp-091` |

**What the spec says about it.** The staff-app form of `BO-564`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search rental return | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, return location, product, expected return, rental status, damage status and 2 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRentalBookings` ?status |
| Location | picker: choose a location | — | — | `listRentalBookings` ?locationId |
| From | date and time picker | — | — | `listRentalBookings` ?from |
| To | date and time picker | — | — | `listRentalBookings` ?to |

#### Outputs: what the screen shows and produces

**Shown**

**Expected Returns Today** (metric tile)

**Due Next 30 Minutes** (metric tile)

**Return in Progress** (metric tile)

**Overdue** (metric tile)

**Partial Returns** (metric tile)

**Damage Cases** (metric tile)

**Maintenance Required** (metric tile)

**Returns Completed Today** (metric tile)

**Deposits Pending Settlement** (metric tile)

**Equipment Awaiting Inspection** (metric tile)

**Data it reads**: `listRentalBookings` (onLoad, Expected back)

**Where the user goes next**

- → `EMP-003` Home — on duty: *Back to Home — on duty*
- → `EMP-092` Return Scan & Rental Retrieval: *Return Scan & Rental Retrieval*
- → `EMP-093` Return Summary & Actual Return Time: *Return Summary & Actual Return Time*
- → `EMP-094` Post-Rental Condition Inspection: *Post-Rental Condition Inspection*
- → `EMP-095` Before vs After Condition Comparison: *Before vs After Condition Comparison*
- → `EMP-096` Damage Assessment & Charge Workflow: *Damage Assessment & Charge Workflow*
- → `EMP-097` Partial Return & Missing Equipment: *Partial Return & Missing Equipment*
- → `EMP-098` Late Fees, Damage Fees & Final Settlement: *Late Fees, Damage Fees & Final Settlement*
- → `EMP-099` Deposit Release, Capture & Customer Confirmation: *Deposit Release, Capture & Customer Confirmation*
- → `EMP-100` Return Completion & Equipment Disposition: *Return Completion & Equipment Disposition*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No rental return yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental return are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental return untouched. |
| Loading (`?state=loading`) | The rental return list; the counts above it resolve separately. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Permissions

- `listRentalBookings` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-091` · status **notStarted** · provenance generated
- Workshop pack:  board 8

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-091?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `EMP-003`, `EMP-092`, `EMP-093`, `EMP-094`, `EMP-095`, `EMP-096`, `EMP-097`, `EMP-098`, `EMP-099`, `EMP-100`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-092` Return Scan & Rental Retrieval

**Quickly identify which active rental the returned equipment belongs to. The original requirements specifically require scanning the rented item and retrieving its reservation.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/return-scan-rental-retrieval-emp-092` |

**What the spec says about it.** The staff-app form of `BO-565`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Where the user goes next**

- → `EMP-091` Rental Return Command Center: *Back to Rental Return Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No return scan rental yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the return scan rental are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the return scan rental untouched. |
| Loading (`?state=loading`) | The return scan rental list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Permissions

- `getRentalBooking` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Return: staff scan or search a booking; late fee is calculated automatically from actual vs booked duration. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-765)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-092` · status **notStarted** · provenance generated
- Workshop pack:  board 8

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-092?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `EMP-091`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-093` Return Summary & Actual Return Time

**Establish the operational return event before inspection and financial settlement.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_OPERATE` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/return-summary-actual-return-time-emp-093` |

**What the spec says about it.** The staff-app form of `BO-566`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

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

- → `EMP-091` Rental Return Command Center: *Back to Rental Return Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No return summary actual yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the return summary actual are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the return summary actual untouched. |
| Loading (`?state=loading`) | The return summary actual list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Permissions

- `returnRental` → `RENTAL_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Return: staff scan or search a booking; late fee is calculated automatically from actual vs booked duration. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-765)*
- Usage-based billing at return: excess charged on actual vs. paid duration (e.g. a wheelchair paid for one hour but used for three is charged two extra hours at return). *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-499)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-093` · status **notStarted** · provenance generated
- Workshop pack:  board 8

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-093?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `EMP-091`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-094` Post-Rental Condition Inspection

**Perform a structured inspection of returned equipment.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_OPERATE` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/post-rental-condition-inspection-emp-094` |

**What the spec says about it.** The staff-app form of `BO-567`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

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

- → `EMP-091` Rental Return Command Center: *Back to Rental Return Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No post-rental condition inspection yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the post-rental condition inspection are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the post-rental condition inspection untouched. |
| Loading (`?state=loading`) | The post-rental condition inspection list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Permissions

- `recordRentalInspection` → `RENTAL_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Post-rental condition inspection, with before/after photo capture that is optional, not mandatory. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-766)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-094` · status **notStarted** · provenance generated
- Workshop pack:  board 8

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-094?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `EMP-091`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-095` Before vs After Condition Comparison

**Use the evidence captured during Board 6 checkout to establish whether damage existed before the rental or occurred during it. This is one of the important capabilities I recommended adding.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_OPERATE` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/before-vs-after-condition-comparison-emp-095` |

**What the spec says about it.** The staff-app form of `BO-568`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

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

- → `EMP-091` Rental Return Command Center: *Back to Rental Return Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No before after condition yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the before after condition are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the before after condition untouched. |
| Loading (`?state=loading`) | The before after condition list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Permissions

- `recordRentalInspection` → `RENTAL_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Post-rental condition inspection, with before/after photo capture that is optional, not mandatory. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-766)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-095` · status **notStarted** · provenance generated
- Workshop pack:  board 8

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-095?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `EMP-091`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-096` Damage Assessment & Charge Workflow

**Convert confirmed equipment damage into a controlled operational and commercial case. The source specifically recommends a formal damage assessment workflow.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_OPERATE` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/damage-assessment-charge-workflow-emp-096` |

**What the spec says about it.** The staff-app form of `BO-569`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

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

- → `EMP-091` Rental Return Command Center: *Back to Rental Return Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No damage assessment charge yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the damage assessment charge are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the damage assessment charge untouched. |
| Loading (`?state=loading`) | The damage assessment charge list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Permissions

- `assessRentalDamage` → `RENTAL_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Damage assessment; partial group returns (e.g. 8 of 10 bicycles back, 2 outstanding); late fees, damage fees and final settlement calculated together before deposit release (individual or group); ends with a rental completion report. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-767)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-096` · status **notStarted** · provenance generated
- Workshop pack:  board 8

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-096?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `EMP-091`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-097` Partial Return & Missing Equipment

**Handle multi-item and group rentals where equipment is returned at different times. This implements the partial-return capability we added in Board 7.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_OPERATE` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/partial-return-missing-equipment-emp-097` |

**What the spec says about it.** The staff-app form of `BO-570`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

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

- → `EMP-091` Rental Return Command Center: *Back to Rental Return Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No partial return missing yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partial return missing are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partial return missing untouched. |
| Loading (`?state=loading`) | The partial return missing list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Permissions

- `returnRental` → `RENTAL_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Damage assessment; partial group returns (e.g. 8 of 10 bicycles back, 2 outstanding); late fees, damage fees and final settlement calculated together before deposit release (individual or group); ends with a rental completion report. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-767)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-097` · status **notStarted** · provenance generated
- Workshop pack:  board 8

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-097?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `EMP-091`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-098` Late Fees, Damage Fees & Final Settlement

**Calculate the customer's final rental financial position. Board 8 should consume, not recreate, the commercial policies configured in Board 4.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_OPERATE` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/late-fees-damage-fees-final-settlement-emp-098` |

**What the spec says about it.** The staff-app form of `BO-571`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

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

- → `EMP-091` Rental Return Command Center: *Back to Rental Return Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No late fees damage yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the late fees damage are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the late fees damage untouched. |
| Loading (`?state=loading`) | The late fees damage list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Permissions

- `returnRental` → `RENTAL_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Damage assessment; partial group returns (e.g. 8 of 10 bicycles back, 2 outstanding); late fees, damage fees and final settlement calculated together before deposit release (individual or group); ends with a rental completion report. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-767)*
- Usage-based billing at return: excess charged on actual vs. paid duration (e.g. a wheelchair paid for one hour but used for three is charged two extra hours at return). *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-499)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-098` · status **notStarted** · provenance generated
- Workshop pack:  board 8

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-098?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `EMP-091`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-099` Deposit Release, Capture & Customer Confirmation

**Complete the deposit lifecycle and provide the customer with a transparent final statement. The source requires full refund/release, partial refund and deposit forfeiture, together with transaction history.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_OPERATE` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/deposit-release-capture-customer-confirmation-emp-099` |

**What the spec says about it.** The staff-app form of `BO-572`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

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

- → `EMP-091` Rental Return Command Center: *Back to Rental Return Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No deposit release capture yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the deposit release capture are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the deposit release capture untouched. |
| Loading (`?state=loading`) | The deposit release capture list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Permissions

- `returnRental` → `RENTAL_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Damage assessment; partial group returns (e.g. 8 of 10 bicycles back, 2 outstanding); late fees, damage fees and final settlement calculated together before deposit release (individual or group); ends with a rental completion report. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-767)*
- Rental items (e.g. strollers, wheelchairs, towels): inventory and quantity per day, check-out and check-in, with inventory updated automatically on return; a refundable deposit (with guest details) is captured at rental and refunded on return. *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-498)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-099` · status **notStarted** · provenance generated
- Workshop pack:  board 8

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-099?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `EMP-091`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-100` Return Completion & Equipment Disposition

**Complete the rental while determining exactly what happens to every returned physical asset. This is extremely important because returning an item does not necessarily mean it becomes immediately available again.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_MANAGE`, `RENTAL_OPERATE` (1 configure, 1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `assetId` (navigation), `bookingId` (navigation) |
| Route | `/rentals/return-completion-equipment-disposition-emp-100` |

**What the spec says about it.** The staff-app form of `BO-573`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

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

- → `EMP-091` Rental Return Command Center: *Back to Rental Return Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No return completion equipment yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the return completion equipment are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the return completion equipment untouched. |
| Loading (`?state=loading`) | The return completion equipment list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Return to service attempted without the inspection this asset category requires. |

#### Permissions

- `returnRental` → `RENTAL_OPERATE` (operate) · staff
- `setAssetStatus` → `ASSET_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Damage assessment; partial group returns (e.g. 8 of 10 bicycles back, 2 outstanding); late fees, damage fees and final settlement calculated together before deposit release (individual or group); ends with a rental completion report. *(client request · MoM 9 Sep 2026, 4.9 Rental Returns, Damage Assessment & Deposit Settlement · DI-767)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-100` · status **notStarted** · provenance generated
- Workshop pack:  board 8

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-100?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `EMP-091`.
- [ ] Every gated control is gated: `ASSET_MANAGE`, `RENTAL_OPERATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P06 reference designs** (from `handoff/design-batches/apps/4-staff-app/README.md`)

- `sources/designs/TICVAI_Employee_App_UI_Reference_1.pdf`: the client's employee app reference: dark theme, Home, Tasks, Scan, AI, More.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P06 as a whole** (3: 0 open, 3 closed). Open first; a closed row says where it went on 30 September.

- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A49** Confirm scope: deliver a lightweight standalone ticket-validation app for dedicated scanner devices, in addition to the scan/validate function embedded in the full Staff Operations App *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A71** Design an offline-first, native ticket-scanning/access-control capability (local scan storage with sync-on-reconnect) for both the dedicated scanner app and the scanning function embedded in the Employee App *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 10 Aug 2026 · workshop tracker)*

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

### Across P06 Venue Staff App

- From the case screen agents act on the customer's bookings/tickets (date change, reschedule, resend tickets), initiate refunds/compensation, route for internal approval, or escalate to another department, which sees it on that department's mobile app. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-542)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Staff-facing POS and tablet UIs always carry TICVAI branding, not client branding. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-296)*
- Approval screens offer Approve, Reject, Return and Request More Information, show an AI-generated approval summary beside the request, and a visible trail of who approved at each stage (e.g. IT → Ops Manager → Finance → CEO → IT publishes). *(client request · MoM 10 Aug 2026, 5.5 Multi-Stage Approval Workflow · DI-235)*
- Two separate apps: an access-control app (handhelds or fixed terminals) scoped purely to entry validation/scanning, and an employee app (approvals, alerts/messages, matrix features) that may include a basic ticket-validity lookup but not full scanning. *(agreed · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-128)*
- Offline state must be clearly visible in the UI, e.g. a visible mode indicator or greyed-out unavailable functions; exact visual treatment to be settled in the UI/UX session. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-072)*
- Allam: the app detects loss of connectivity and switches to offline mode automatically, without cashier action, then restores online mode and syncs pending transactions automatically. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-071)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Allam: the platform is device-agnostic (Android, iOS and web) so sales can continue on any available device. *(agreed · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-068)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

**12 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"assessRentalDamage": {"method":"POST","path":"/rental-bookings/{bookingId}/damage","contract":"rental","summary":"Price the damage, and say who approved it","permission":"RENTAL_OPERATE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalDamageAssessment","responds":"RentalDamageAssessment"},
"getRentalBooking": {"method":"GET","path":"/rental-bookings/{bookingId}","contract":"rental","summary":"One booking, its timeline and its readiness","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RentalBooking"},
"listRentalBookings": {"method":"GET","path":"/rental-bookings","contract":"rental","summary":"Reservations across venues and locations","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"locationId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"RentalBooking"},
"recordRentalInspection": {"method":"POST","path":"/rental-bookings/{bookingId}/inspection","contract":"rental","summary":"Condition before or after, with evidence","permission":"RENTAL_OPERATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalInspection","responds":"RentalInspection"},
"returnRental": {"method":"POST","path":"/rental-bookings/{bookingId}/return","contract":"rental","summary":"Take it back, inspect it, and settle everything at once","permission":"RENTAL_OPERATE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalReturn","responds":"RentalSettlement"},
"setAssetStatus": {"method":"PUT","path":"/assets/{assetId}/status","contract":"maintenance","summary":"Take an asset out of service or return it","permission":"ASSET_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetAssetStatusRequest","responds":"AssetStatusResult"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Asset": {"x-ticvai-persistence":"maintenance.asset","allOf":[{"$ref":"#/components/schemas/CreateAssetRequest"},{"type":"object","x-ticvai-retired-columns":["is_maintenance_overdue","document_refs"],"required":["id","status"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid","nullable":true,"description":"1.2.x. **Where this asset is also bookable.** An AV rig is an asset to maintain and a resource to allocate, and they are the same object seen from two sides.\n**`resources` owns the calendar and this owns the condition.** An asset out of service makes its resource unbookable, which is one link rather than two models of availability.\n"},"deviceId":{"type":"string","format":"uuid","nullable":true,"description":"BL-160. **Where this asset is also a registered device.** A turnstile is an asset to maintain and a device to operate, and — exactly as with `resourceId` above — they are the same object seen from two sides.\n**Nothing joined them before this.** A turnstile controller reporting `needsAttention` could not raise a work order against itself, and an engineer closing one had no way back to the device whose firmware caused it.\n**Null for most assets and for most devices.** A chiller is not a device and a signature pad is not on the asset register; the link is sparse, and it lives here rather than on `platform.device` because `platform` is the foundation tier and a foreign key pointing from it into `maintenance` would invert the tiers — every cell running a spine would carry a column for a satellite it may not deploy.\n"},"acquisitionCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"acquiredOn":{"type":"string","format":"date","nullable":true},"depreciation":{"type":"object","nullable":true,"description":"**Recorded here and posted by `finance`.** Depreciation is an accounting act and the asset register is where the useful life is actually known — an engineer knows a chiller lasts fifteen years and an accountant knows what to do about it.\n","properties":{"method":{"type":"string","enum":["straightLine","reducingBalance","unitsOfProduction","none"]},"usefulLifeMonths":{"type":"integer"},"residualValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accumulatedDepreciation":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"retiredOn":{"type":"string","format":"date","nullable":true,"description":"**Retirement is not deletion.** A work order from three years ago still names this asset, and an inspection record with no asset is an inspection of nothing.\n"},"disposalProceeds":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"$ref":"#/components/schemas/AssetStatus"},"statusReason":{"type":"string","nullable":true},"openWorkOrderCount":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Work orders on this asset whose status is `open`, `assigned`, `inProgress`, `paused` or `awaitingParts` — the same set `AssetDetail.openWorkOrders` returns. **Maintained on write**: `createWorkOrder` and every transition into or out of that set (complete, cancel, close, reject back to open) adjust it in the same transaction as the work-order row.\n"},"nextMaintenanceDueAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The earliest `nextDueAt` among this asset's active maintenance plans; null when none has one. **Maintained on write**: recomputed whenever one of those plans is created, amended, suspended or has its `nextDueAt` moved by a completed work order. `listAssets?maintenanceDue` filters on this column against the clock.\n"},"isMaintenanceOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`nextMaintenanceDueAt` is in the past at the moment of the read. **Computed on read and not stored** — it depends on the clock, so a stored copy is stale the minute after it is written.\n"},"lastInspectionAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`performedAt` of the latest inspection submitted against this asset. **Maintained on write** by `submitInspection`, in the same transaction as the inspection row; an inspection synced late with an earlier `performedAt` does not move it back.\n"},"usageCounter":{"type":"number","nullable":true,"description":"Cycles, hours or kilometres. Drives usage-based maintenance."}}}]},
"AssetStatus": {"type":"string","enum":["inService","outOfService","underMaintenance","awaitingParts","retired","disposed"]},
"AssetStatusResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["asset","downstreamEffects"],"properties":{"asset":{"$ref":"#/components/schemas/Asset"},"downstreamEffects":{"type":"object","description":"What else changed. Surfaced so the person taking a ride out of service sees the commercial consequence at the moment they do it.\n","properties":{"productsSuspended":{"type":"array","items":{"type":"string","format":"uuid"}},"accessPointBlocked":{"type":"boolean"},"performancesAffected":{"type":"integer"},"workOrderId":{"type":"string","format":"uuid","nullable":true}}}}},
"RentalBooking": {"type":"object","x-ticvai-persistence":"rental.booking","description":"Board 5. **The booking outlives the order** — an order completes at payment and the rental is still out.\n","required":["id","productId","from","to","status"],"properties":{"id":{"type":"string","format":"uuid"},"reference":{"type":"string"},"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"returnLocationId":{"type":"string","format":"uuid","nullable":true},"customerId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer"},"status":{"type":"string","enum":["draft","confirmed","awaitingArrival","checkedOut","overdue","partiallyReturned","completed","completedWithDamage","notReturned","cancelled","noShow"]},"checkedOutAt":{"type":"string","format":"date-time","nullable":true},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"returnedAt":{"type":"string","format":"date-time","nullable":true},"depositAuthorisationId":{"type":"string","format":"uuid","nullable":true},"accruedLateFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"readiness":{"type":"array","readOnly":true,"description":"**Computed, not stored** — agreement, requirements, deposit, equipment.","items":{"type":"object","properties":{"check":{"type":"string"},"satisfied":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"participants":{"type":"array","items":{"$ref":"#/components/schemas/RentalParticipant"}},"scopePath":{"type":"string"}}},
"RentalDamageAssessment": {"type":"object","x-ticvai-persistence":"rental.damage_assessment","description":"Board 8.6. **A dispute is a state, not a deletion.**","required":["amount","description"],"properties":{"id":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"description":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"inspectionId":{"type":"string","format":"uuid","nullable":true},"assessedBy":{"type":"string","format":"uuid"},"approvedBy":{"type":"string","format":"uuid","nullable":true},"customerAcknowledgement":{"type":"string","enum":["accepted","disputed","notPresented"],"default":"notPresented"},"workOrderId":{"type":"string","format":"uuid","nullable":true,"description":"Raised in `maintenance`, so the repair is tracked where every other repair is."},"scopePath":{"type":"string"}}},
"RentalInspection": {"type":"object","x-ticvai-persistence":"rental.inspection","description":"Boards 6.5 and 8.4. **Before and after are one record shape with a phase**, which is what makes the comparison view possible.\n","required":["phase","condition"],"properties":{"id":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"phase":{"type":"string","enum":["preRental","postRental"]},"condition":{"type":"string","enum":["good","minorDamage","majorDamage","faulty","notReturned"],"description":"**26 August: simplified state attributes.** *\"rental/equipment items can be tracked with simplified state attributes (e.g., available, rented, faulty) rather than requiring granular custom attributes for this category — agreed by Allam.\"* So the condition is a short enum, and anything finer belongs in the note or the photographs.\n"},"checklist":{"type":"array","items":{"type":"object","properties":{"item":{"type":"string"},"passed":{"type":"boolean"},"note":{"type":"string","nullable":true}}}},"note":{"type":"string","nullable":true},"photoAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"inspectedBy":{"type":"string","format":"uuid"},"inspectedAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string"}}},
"RentalParticipant": {"type":"object","x-ticvai-persistence":"rental.participant","description":"Board 5.5. **A group rental is one booking with participants**, because the agreement, the deposit and the return are handled together.\n","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"isPrimaryRenter":{"type":"boolean","default":false},"dateOfBirth":{"type":"string","format":"date","nullable":true},"idNumber":{"type":"string","nullable":true},"guardianName":{"type":"string","nullable":true},"emergencyContact":{"type":"string","nullable":true},"hasSignedWaiver":{"type":"boolean","readOnly":true},"customFields":{"type":"object","additionalProperties":true}}},
"RentalReturn": {"type":"object","description":"Board 8. **Late fee, damage and partial return all land on one deposit.**","required":["returnedAt"],"properties":{"returnedAt":{"type":"string","format":"date-time"},"returnLocationId":{"type":"string","format":"uuid","nullable":true},"returnedAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"missingAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"inspection":{"$ref":"#/components/schemas/RentalInspection"},"damage":{"type":"array","items":{"$ref":"#/components/schemas/RentalDamageAssessment"}},"waiveLateFee":{"type":"boolean","default":false},"overrideId":{"type":"string","format":"uuid","nullable":true}}},
"RentalSettlement": {"type":"object","x-ticvai-persistence":"rental.settlement","description":"Board 8.8. **One statement, because there is one deposit.** *Capture AED 120, release AED 380.*\n","properties":{"bookingId":{"type":"string","format":"uuid"},"expectedReturnAt":{"type":"string","format":"date-time"},"actualReturnAt":{"type":"string","format":"date-time"},"gracePeriodMinutes":{"type":"integer"},"chargeableLateMinutes":{"type":"integer"},"lateFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"damageFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"missingItemFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCharged":{"x-ticvai-column":"gross_charged_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"depositCaptured":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"depositReleased":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceDue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"**Where the charges exceed the deposit.** A bike written off against a AED 200 hold leaves a real debt, and netting it to zero hides it.\n"},"outcome":{"type":"string","enum":["completed","completedWithDamage","partiallyReturned","notReturned"]},"scopePath":{"type":"string"}}},
"SetAssetStatusRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["status","reason","recordedAt"],"properties":{"status":{"$ref":"#/components/schemas/AssetStatus"},"reason":{"type":"string","minLength":3,"maxLength":1000},"inspectionId":{"type":"string","format":"uuid","nullable":true,"description":"Required for return to service where the asset demands it."},"raiseWorkOrder":{"type":"boolean","default":false},"recordedAt":{"type":"string","format":"date-time"}}}
}
```
