# P06-rentals-01 — P06 · Rentals (1 of 3)

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
  `ASSET_VIEW, RENTAL_OPERATE, RENTAL_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **4 of these operations work offline**: assignRentalEquipment, checkOutRental, lookupAsset, recordRentalInspection
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
| `EMP-071` | Rental Checkout Command Center | B–D | 2 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `EMP-072` | Voucher Scan & Reservation Retrieval | B–D | 0 | 0 | 6 | 0 | 1 | 2 | — | notStarted (generated) |
| `EMP-073` | Checkout Readiness Validation | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `EMP-074` | Equipment Assignment Workspace | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `EMP-075` | Equipment Scan & Validation | B–D | 1 | 0 | 6 | 3 | 1 | 0 | — | notStarted (generated) |
| `EMP-076` | Pre-Rental Condition Inspection | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `EMP-077` | Safety & Handover Checklist | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `EMP-078` | Deposit & Financial Handover Validation | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `EMP-079` | Group & Multi-Item Checkout | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `EMP-080` | Checkout Confirmation & Rental Activation | B–D | 2 | 0 | 6 | 0 | 0 | 6 | — | notStarted (generated) |

## Thin screens in this batch

**EMP-072, EMP-073, EMP-074, EMP-075, EMP-076, EMP-077, EMP-078, EMP-079, EMP-080 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `EMP-071` Rental Checkout Command Center

**Provide rental operators with a real-time operational queue of customers requiring equipment checkout.**

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
| Route | `/rentals/rental-checkout-command-center-emp-071` |

**What the spec says about it.** The staff-app form of `BO-544`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search rental checkout | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by location, product, start time, booking type, group/individual, readiness and 1 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRentalBookings` ?status |
| Location | picker: choose a location | — | — | `listRentalBookings` ?locationId |
| From | date and time picker | — | — | `listRentalBookings` ?from |
| To | date and time picker | — | — | `listRentalBookings` ?to |

#### Outputs: what the screen shows and produces

**Shown**

**Arriving Next 30 Min** (metric tile)

**Awaiting Checkout** (metric tile)

**Ready for Checkout** (metric tile)

**Checkout in Progress** (metric tile)

**Checked Out Today** (metric tile)

**Missing Requirements** (metric tile)

**Equipment Issues** (metric tile)

**Late Arrivals** (metric tile)

**Data it reads**: `listRentalBookings` (onLoad, Awaiting arrival)

**Where the user goes next**

- → `EMP-003` Home — on duty: *Back to Home — on duty*
- → `EMP-072` Voucher Scan & Reservation Retrieval: *Voucher Scan & Reservation Retrieval*
- → `EMP-073` Checkout Readiness Validation: *Checkout Readiness Validation*
- → `EMP-074` Equipment Assignment Workspace: *Equipment Assignment Workspace*
- → `EMP-075` Equipment Scan & Validation: *Equipment Scan & Validation*
- → `EMP-076` Pre-Rental Condition Inspection: *Pre-Rental Condition Inspection*
- → `EMP-077` Safety & Handover Checklist: *Safety & Handover Checklist*
- → `EMP-078` Deposit & Financial Handover Validation: *Deposit & Financial Handover Validation*
- → `EMP-079` Group & Multi-Item Checkout: *Group & Multi-Item Checkout*
- → `EMP-080` Checkout Confirmation & Rental Activation: *Checkout Confirmation & Rental Activation*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No rental checkout yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental checkout are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental checkout untouched. |
| Loading (`?state=loading`) | The rental checkout list; the counts above it resolve separately. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Permissions

- `listRentalBookings` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Checkout screen shows bookings by status (in progress, checked out) and lets staff scan a QR code to pull up a reservation. *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-758)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-071` · status **notStarted** · provenance generated
- Workshop pack:  board 6

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-071?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `EMP-003`, `EMP-072`, `EMP-073`, `EMP-074`, `EMP-075`, `EMP-076`, `EMP-077`, `EMP-078`, `EMP-079`, `EMP-080`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-072` Voucher Scan & Reservation Retrieval

**Quickly identify the customer reservation when they arrive. The original requirement specifically requires scanning and validating the customer's voucher/ticket.**

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
| Route | `/rentals/voucher-scan-reservation-retrieval-emp-072` |

**What the spec says about it.** The staff-app form of `BO-545`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Where the user goes next**

- → `EMP-071` Rental Checkout Command Center: *Back to Rental Checkout Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No voucher scan reservation yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the voucher scan reservation are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the voucher scan reservation untouched. |
| Loading (`?state=loading`) | The voucher scan reservation list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Permissions

- `getRentalBooking` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Checkout screen shows bookings by status (in progress, checked out) and lets staff scan a QR code to pull up a reservation. *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-758)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-072` · status **notStarted** · provenance generated
- Workshop pack:  board 6

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-072?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `EMP-071`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-073` Checkout Readiness Validation

**Prevent equipment from being handed over until mandatory requirements are satisfied.**

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
| Route | `/rentals/checkout-readiness-validation-emp-073` |

**What the spec says about it.** The staff-app form of `BO-546`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Where the user goes next**

- → `EMP-071` Rental Checkout Command Center: *Back to Rental Checkout Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No checkout readiness validation yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the checkout readiness validation are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the checkout readiness validation untouched. |
| Loading (`?state=loading`) | The checkout readiness validation list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Permissions

- `getRentalBooking` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Before handover: readiness validation (reservation, payment, inventory), a pre-rental condition checklist (e.g. bicycle brakes and tyres working) and a safety handover checklist (e.g. helmet with a bicycle). *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-759)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-073` · status **notStarted** · provenance generated
- Workshop pack:  board 6

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-073?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `EMP-071`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-074` Equipment Assignment Workspace

**Assign the actual physical equipment to the reservation.**

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
| Route | `/rentals/equipment-assignment-workspace-emp-074` |

**What the spec says about it.** The staff-app form of `BO-547`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Assign rental equipment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `EMP-071` Rental Checkout Command Center: *Back to Rental Checkout Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No equipment yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the equipment are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the equipment untouched. |
| Loading (`?state=loading`) | The equipment list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Asset already out, under maintenance, or of the wrong product |

#### Permissions

- `assignRentalEquipment` → `RENTAL_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Serialized items: staff assign the specific unit (e.g. bicycle #121) at checkout by scanning its QR code or selecting it manually from available units. Multi-item checkout hands a whole group's items (e.g. 10 bicycles) out in a single action. *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-760)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-074` · status **notStarted** · provenance generated
- Workshop pack:  board 6

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-074?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: Assign rental equipment, Cancel.
- [ ] Every transition is wired: `EMP-071`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-075` Equipment Scan & Validation

**Ensure the operator cannot accidentally assign the wrong, unavailable or unsafe equipment.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_VIEW`, `RENTAL_OPERATE` (1 read, 1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/equipment-scan-validation-emp-075` |

**What the spec says about it.** The staff-app form of `BO-548`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Assign rental equipment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `EMP-071` Rental Checkout Command Center: *Back to Rental Checkout Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No equipment scan validation yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the equipment scan validation are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the equipment scan validation untouched. |
| Loading (`?state=loading`) | The equipment scan validation list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Asset already out, under maintenance, or of the wrong product |

#### Permissions

- `assignRentalEquipment` → `RENTAL_OPERATE` (operate) · staff
- `lookupAsset` → `ASSET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 18.3.1 | QR Asset Scanning - Users shall scan asset QR codes. | Employee Mobile App & AI Assistant | CONTRACTED | `lookupAsset` |
| 18.3.2 | NFC Asset Scanning - Users shall scan NFC asset tags. | Employee Mobile App & AI Assistant | CONTRACTED | `lookupAsset` |
| 18.3.3 | Asset Lookup - Users shall view asset details. | Employee Mobile App & AI Assistant | CONTRACTED | `lookupAsset` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Serialized items: staff assign the specific unit (e.g. bicycle #121) at checkout by scanning its QR code or selecting it manually from available units. Multi-item checkout hands a whole group's items (e.g. 10 bicycles) out in a single action. *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-760)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-075` · status **notStarted** · provenance generated
- Workshop pack:  board 6

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-075?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: Assign rental equipment, Cancel.
- [ ] Every transition is wired: `EMP-071`.
- [ ] Every gated control is gated: `ASSET_VIEW`, `RENTAL_OPERATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-076` Pre-Rental Condition Inspection

**Document the equipment condition before handover. Photo capture at checkout is specifically recommended in the source.**

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
| Route | `/rentals/pre-rental-condition-inspection-emp-076` |

**What the spec says about it.** The staff-app form of `BO-549`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Asset (primary button) | navigation or local | — | — | — | — |
| Reservation (secondary button) | navigation or local | — | — | — | — |
| Checkout inspection (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `EMP-071` Rental Checkout Command Center: *Back to Rental Checkout Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No pre-rental condition inspection yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pre-rental condition inspection are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pre-rental condition inspection untouched. |
| Loading (`?state=loading`) | The pre-rental condition inspection list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Permissions

- `recordRentalInspection` → `RENTAL_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Before handover: readiness validation (reservation, payment, inventory), a pre-rental condition checklist (e.g. bicycle brakes and tyres working) and a safety handover checklist (e.g. helmet with a bicycle). *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-759)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-076` · status **notStarted** · provenance generated
- Workshop pack:  board 6

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-076?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: Asset, Reservation, Checkout inspection.
- [ ] Every transition is wired: `EMP-071`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-077` Safety & Handover Checklist

**Ensure mandatory operational and safety steps are completed before starting the rental. Example — Kayak ✓ Life jacket provided ✓ Paddle provided ✓ Safety briefing completed ✓ Emergency procedure explained ✓ Restricted areas explained ✓ Customer confirms swimming ability Example — Bicycle ✓ Helmet provided ✓ Brake check completed ✓ Seat adjusted ✓ Safety briefing completed The checklist should be configurable by rental product/category from Board 1.**

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
| Route | `/rentals/safety-handover-checklist-emp-077` |

**What the spec says about it.** The staff-app form of `BO-550`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

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

- → `EMP-071` Rental Checkout Command Center: *Back to Rental Checkout Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No safety handover checklist yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the safety handover checklist are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the safety handover checklist untouched. |
| Loading (`?state=loading`) | The safety handover checklist list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A required precondition is not met, and the response names which — the counter needs to know whether to fetch a signature or a supervisor. |

#### Permissions

- `checkOutRental` → `RENTAL_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Before handover: readiness validation (reservation, payment, inventory), a pre-rental condition checklist (e.g. bicycle brakes and tyres working) and a safety handover checklist (e.g. helmet with a bicycle). *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-759)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-077` · status **notStarted** · provenance generated
- Workshop pack:  board 6

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-077?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `EMP-071`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-078` Deposit & Financial Handover Validation

**Give the rental operator a clear commercial status without requiring them to enter the Finance module.**

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
| Route | `/rentals/deposit-financial-handover-validation-emp-078` |

**What the spec says about it.** The staff-app form of `BO-551`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

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

- → `EMP-071` Rental Checkout Command Center: *Back to Rental Checkout Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No deposit financial handover yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the deposit financial handover are still there. The pack's own statuses are ✓ AUTHORIZED — the state names which is selected. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the deposit financial handover untouched. |
| Loading (`?state=loading`) | The deposit financial handover list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A required precondition is not met, and the response names which — the counter needs to know whether to fetch a signature or a supervisor. |

#### Permissions

- `checkOutRental` → `RENTAL_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental items (e.g. strollers, wheelchairs, towels): inventory and quantity per day, check-out and check-in, with inventory updated automatically on return; a refundable deposit (with guest details) is captured at rental and refunded on return. *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-498)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-078` · status **notStarted** · provenance generated
- Workshop pack:  board 6

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-078?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `EMP-071`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-079` Group & Multi-Item Checkout

**Provide an efficient checkout workflow for group rentals and reservations containing multiple equipment units. This is particularly important because the original requirements support group reservations.**

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
| Route | `/rentals/group-multi-item-checkout-emp-079` |

**What the spec says about it.** The staff-app form of `BO-552`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Assign rental equipment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `EMP-071` Rental Checkout Command Center: *Back to Rental Checkout Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No group multi-item checkout yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group multi-item checkout are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group multi-item checkout untouched. |
| Loading (`?state=loading`) | The group multi-item checkout list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Asset already out, under maintenance, or of the wrong product |

#### Permissions

- `assignRentalEquipment` → `RENTAL_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Serialized items: staff assign the specific unit (e.g. bicycle #121) at checkout by scanning its QR code or selecting it manually from available units. Multi-item checkout hands a whole group's items (e.g. 10 bicycles) out in a single action. *(client request · MoM 9 Sep 2026, 4.7 Rental Checkout & Fulfillment · DI-760)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-079` · status **notStarted** · provenance generated
- Workshop pack:  board 6

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-079?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: Assign rental equipment, Cancel.
- [ ] Every transition is wired: `EMP-071`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-080` Checkout Confirmation & Rental Activation

**Officially start the rental and transition the reservation into an active rental.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_OPERATE` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | configEditor (comfortable density): the pack gives this screen a configuration directory (§Options; Select Equipment) and no display directory — it is settings, not a population |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/checkout-confirmation-rental-activation-emp-080` |

**What the spec says about it.** The staff-app form of `BO-553`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Email / SMS / App Notification | text field | — | — | — | — | — | — |
| ↓ | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `EMP-071` Rental Checkout Command Center: *Back to Rental Checkout Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No checkout confirmation rental configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the checkout confirmation rental untouched. |
| Loading (`?state=loading`) | The checkout confirmation rental configuration as saved. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A required precondition is not met, and the response names which — the counter needs to know whether to fetch a signature or a supervisor. |

#### Permissions

- `checkOutRental` → `RENTAL_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-080` · status **notStarted** · provenance generated
- Workshop pack:  board 6

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-080?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `EMP-071`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`.
- [ ] The module and platform inputs below are applied.
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

**9 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"assignRentalEquipment": {"method":"POST","path":"/rental-bookings/{bookingId}/equipment","contract":"rental","summary":"Bind specific assets to the booking, by scan where required","permission":"RENTAL_OPERATE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RentalEquipmentAssignment"},
"checkOutRental": {"method":"POST","path":"/rental-bookings/{bookingId}/check-out","contract":"rental","summary":"Hand it over, with the deposit held and the condition recorded","permission":"RENTAL_OPERATE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalCheckOut","responds":"RentalBooking"},
"getRentalBooking": {"method":"GET","path":"/rental-bookings/{bookingId}","contract":"rental","summary":"One booking, its timeline and its readiness","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RentalBooking"},
"listRentalBookings": {"method":"GET","path":"/rental-bookings","contract":"rental","summary":"Reservations across venues and locations","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"locationId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"RentalBooking"},
"lookupAsset": {"method":"GET","path":"/assets/lookup","contract":"maintenance","summary":"Find an asset by tag or QR","permission":"ASSET_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assetTag","in":"query","required":null},{"name":"serialNumber","in":"query","required":null}],"requestBody":null,"responds":"AssetDetail"},
"recordRentalInspection": {"method":"POST","path":"/rental-bookings/{bookingId}/inspection","contract":"rental","summary":"Condition before or after, with evidence","permission":"RENTAL_OPERATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalInspection","responds":"RentalInspection"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Asset": {"x-ticvai-persistence":"maintenance.asset","allOf":[{"$ref":"#/components/schemas/CreateAssetRequest"},{"type":"object","x-ticvai-retired-columns":["is_maintenance_overdue","document_refs"],"required":["id","status"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid","nullable":true,"description":"1.2.x. **Where this asset is also bookable.** An AV rig is an asset to maintain and a resource to allocate, and they are the same object seen from two sides.\n**`resources` owns the calendar and this owns the condition.** An asset out of service makes its resource unbookable, which is one link rather than two models of availability.\n"},"deviceId":{"type":"string","format":"uuid","nullable":true,"description":"BL-160. **Where this asset is also a registered device.** A turnstile is an asset to maintain and a device to operate, and — exactly as with `resourceId` above — they are the same object seen from two sides.\n**Nothing joined them before this.** A turnstile controller reporting `needsAttention` could not raise a work order against itself, and an engineer closing one had no way back to the device whose firmware caused it.\n**Null for most assets and for most devices.** A chiller is not a device and a signature pad is not on the asset register; the link is sparse, and it lives here rather than on `platform.device` because `platform` is the foundation tier and a foreign key pointing from it into `maintenance` would invert the tiers — every cell running a spine would carry a column for a satellite it may not deploy.\n"},"acquisitionCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"acquiredOn":{"type":"string","format":"date","nullable":true},"depreciation":{"type":"object","nullable":true,"description":"**Recorded here and posted by `finance`.** Depreciation is an accounting act and the asset register is where the useful life is actually known — an engineer knows a chiller lasts fifteen years and an accountant knows what to do about it.\n","properties":{"method":{"type":"string","enum":["straightLine","reducingBalance","unitsOfProduction","none"]},"usefulLifeMonths":{"type":"integer"},"residualValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accumulatedDepreciation":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"retiredOn":{"type":"string","format":"date","nullable":true,"description":"**Retirement is not deletion.** A work order from three years ago still names this asset, and an inspection record with no asset is an inspection of nothing.\n"},"disposalProceeds":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"$ref":"#/components/schemas/AssetStatus"},"statusReason":{"type":"string","nullable":true},"openWorkOrderCount":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Work orders on this asset whose status is `open`, `assigned`, `inProgress`, `paused` or `awaitingParts` — the same set `AssetDetail.openWorkOrders` returns. **Maintained on write**: `createWorkOrder` and every transition into or out of that set (complete, cancel, close, reject back to open) adjust it in the same transaction as the work-order row.\n"},"nextMaintenanceDueAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The earliest `nextDueAt` among this asset's active maintenance plans; null when none has one. **Maintained on write**: recomputed whenever one of those plans is created, amended, suspended or has its `nextDueAt` moved by a completed work order. `listAssets?maintenanceDue` filters on this column against the clock.\n"},"isMaintenanceOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`nextMaintenanceDueAt` is in the past at the moment of the read. **Computed on read and not stored** — it depends on the clock, so a stored copy is stale the minute after it is written.\n"},"lastInspectionAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`performedAt` of the latest inspection submitted against this asset. **Maintained on write** by `submitInspection`, in the same transaction as the inspection row; an inspection synced late with an earlier `performedAt` does not move it back.\n"},"usageCounter":{"type":"number","nullable":true,"description":"Cycles, hours or kilometres. Drives usage-based maintenance."}}}]},
"AssetDetail": {"x-ticvai-persistence":"maintenance.asset","allOf":[{"$ref":"#/components/schemas/Asset"},{"type":"object","properties":{"openWorkOrders":{"type":"array","items":{"$ref":"#/components/schemas/WorkOrder"}},"maintenancePlans":{"type":"array","items":{"$ref":"#/components/schemas/MaintenancePlan"}},"documents":{"type":"array","description":"Manuals, procedures, certificates. What a technician needs on site. Read from `maintenance.asset_document`.\n","items":{"$ref":"#/components/schemas/AssetDocument"}}}}]},
"AssetDocument": {"x-ticvai-persistence":"maintenance.asset_document","type":"object","description":"A document attached to an asset — manual, procedure, certificate — with the name and kind a technician needs on site. **One row per document**, because `AssetDetail.documents` returns a name and a kind for each and a `text[]` of refs has nowhere to hold either.\n","required":["id","assetId","ref"],"properties":{"id":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"ref":{"type":"string","description":"The document in the media store."},"name":{"type":"string","maxLength":200,"nullable":true},"kind":{"allOf":[{"$ref":"#/components/schemas/AssetDocumentKind"}],"nullable":true,"description":"Null where the document arrived as a bare ref in `documentRefs`."}}},
"MaintenancePlan": {"x-ticvai-persistence":"maintenance.preventive_plan","type":"object","required":["id","name","assetId","taskTemplate"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":200},"assetId":{"type":"string","format":"uuid"},"assetCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"Applies to every asset in the category rather than one."},"intervalDays":{"type":"integer","nullable":true,"description":"Elapsed-time trigger."},"usageInterval":{"type":"number","nullable":true,"description":"Usage trigger — cycles, hours, kilometres. **Whichever comes first** when both are set. A ride serviced every three months or ten thousand cycles is one plan.\n"},"leadTimeDays":{"type":"integer","default":7,"description":"How far ahead the work order is generated, so parts can be ordered before the job is already late.\n"},"taskTemplate":{"type":"object","required":["title","priority"],"properties":{"title":{"type":"string"},"description":{"type":"string"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"estimatedMinutes":{"type":"integer"},"inspectionTemplateId":{"type":"string","format":"uuid"},"requiredPartIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},"lastCompletedAt":{"type":"string","format":"date-time","nullable":true},"nextDueAt":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"}}},
"RentalBooking": {"type":"object","x-ticvai-persistence":"rental.booking","description":"Board 5. **The booking outlives the order** — an order completes at payment and the rental is still out.\n","required":["id","productId","from","to","status"],"properties":{"id":{"type":"string","format":"uuid"},"reference":{"type":"string"},"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"returnLocationId":{"type":"string","format":"uuid","nullable":true},"customerId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer"},"status":{"type":"string","enum":["draft","confirmed","awaitingArrival","checkedOut","overdue","partiallyReturned","completed","completedWithDamage","notReturned","cancelled","noShow"]},"checkedOutAt":{"type":"string","format":"date-time","nullable":true},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"returnedAt":{"type":"string","format":"date-time","nullable":true},"depositAuthorisationId":{"type":"string","format":"uuid","nullable":true},"accruedLateFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"readiness":{"type":"array","readOnly":true,"description":"**Computed, not stored** — agreement, requirements, deposit, equipment.","items":{"type":"object","properties":{"check":{"type":"string"},"satisfied":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"participants":{"type":"array","items":{"$ref":"#/components/schemas/RentalParticipant"}},"scopePath":{"type":"string"}}},
"RentalCheckOut": {"type":"object","description":"Board 6. **The readiness gate is enforced server-side.**","properties":{"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"depositInstrument":{"type":"string","nullable":true},"conditionNote":{"type":"string","nullable":true},"photoAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"safetyBriefingGiven":{"type":"boolean","default":false},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"overrideId":{"type":"string","format":"uuid","nullable":true,"description":"**A supervisor override for a failed precondition**, which is recorded rather than allowed silently.\n"}}},
"RentalEquipmentAssignment": {"type":"object","x-ticvai-persistence":"rental.equipment_assignment","description":"Board 6.4. **The moment a serialised rental stops being a quantity.**","required":["assetId"],"properties":{"id":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","description":"A `maintenance.Asset`, which is also a `resources` resource where the product is schedule-controlled."},"serialNumber":{"type":"string","nullable":true},"scannedCode":{"type":"string","nullable":true},"assignedManually":{"type":"boolean","default":false},"assignedAt":{"type":"string","format":"date-time"},"returnedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"RentalInspection": {"type":"object","x-ticvai-persistence":"rental.inspection","description":"Boards 6.5 and 8.4. **Before and after are one record shape with a phase**, which is what makes the comparison view possible.\n","required":["phase","condition"],"properties":{"id":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"phase":{"type":"string","enum":["preRental","postRental"]},"condition":{"type":"string","enum":["good","minorDamage","majorDamage","faulty","notReturned"],"description":"**26 August: simplified state attributes.** *\"rental/equipment items can be tracked with simplified state attributes (e.g., available, rented, faulty) rather than requiring granular custom attributes for this category — agreed by Allam.\"* So the condition is a short enum, and anything finer belongs in the note or the photographs.\n"},"checklist":{"type":"array","items":{"type":"object","properties":{"item":{"type":"string"},"passed":{"type":"boolean"},"note":{"type":"string","nullable":true}}}},"note":{"type":"string","nullable":true},"photoAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"inspectedBy":{"type":"string","format":"uuid"},"inspectedAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string"}}},
"RentalParticipant": {"type":"object","x-ticvai-persistence":"rental.participant","description":"Board 5.5. **A group rental is one booking with participants**, because the agreement, the deposit and the return are handled together.\n","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"isPrimaryRenter":{"type":"boolean","default":false},"dateOfBirth":{"type":"string","format":"date","nullable":true},"idNumber":{"type":"string","nullable":true},"guardianName":{"type":"string","nullable":true},"emergencyContact":{"type":"string","nullable":true},"hasSignedWaiver":{"type":"boolean","readOnly":true},"customFields":{"type":"object","additionalProperties":true}}},
"WorkOrder": {"x-ticvai-persistence":"maintenance.work_order","x-ticvai-retired-columns":["is_overdue"],"type":"object","required":["id","workOrderNumber","title","venueId","status","priority","kind","createdAt"],"properties":{"downtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"},"rootCause":{"type":"string","nullable":true,"enum":["wearAndTear","operatorError","guestDamage","manufacturingDefect","environmental","softwareFault","powerFailure","deferredMaintenance","unknown"],"description":"**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"},"rootCauseNote":{"type":"string","nullable":true},"escalatedAt":{"type":"string","format":"date-time","nullable":true},"escalationLevel":{"type":"integer","default":0,"description":"**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"},"id":{"type":"string","format":"uuid"},"workOrderNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"title":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"assetName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"},"status":{"$ref":"#/components/schemas/WorkOrderStatus"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"priorityScore":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"readOnly":true,"description":"The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."},"prioritySource":{"type":"string","enum":["scored","assetOverride","manual"],"readOnly":true,"description":"Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","items":{"type":"string"},"description":"Skills the job needs (M17-13)."},"kind":{"$ref":"#/components/schemas/WorkOrderKind"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"raisedByPrincipalId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"},"locationDescription":{"type":"string","maxLength":500,"nullable":true,"description":"Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"},"elapsedMinutes":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"},"isTimerRunning":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"},"dueAt":{"type":"string","format":"date-time","nullable":true},"isOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"},"requiresVerification":{"type":"boolean"},"sourcePlanId":{"type":"string","format":"uuid","nullable":true},"sourceInspectionId":{"type":"string","format":"uuid","nullable":true},"sourceIncidentId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}}
}
```
