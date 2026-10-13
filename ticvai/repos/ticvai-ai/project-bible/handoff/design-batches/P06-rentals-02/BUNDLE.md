# P06-rentals-02 — P06 · Rentals (2 of 3)

**10 screens · 8 operations · 6 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `RENTAL_OPERATE, RENTAL_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **1 of these operations work offline**: reportRentalIncident
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.
- **How input should be, how output should be.** Each screen's block in `BUNDLE.md` says, field by
  field, the control, whether it is required, its default, its limits and allowed values, its format
  and its error; and, element by element, what is shown and in what format, what each action
  produces and where the user goes next. Draw exactly that.

## The processes these screens belong to

Written by the owner of each process (`handoff/design-notes/`). Read before any screen: it says how the process runs end to end and which words the screens must use.

### Food, Beverage & Retail

Food & beverage, retail, rentals, inventory and procurement across the till (P04), the kitchen display (P15), the staff app (P06), Venue Management (P08), the guest web and app (P01/P02), the kiosk (P05) and the CMS (P13). COUNTER SERVICE (F108): the cashier takes the order on the Food & Drink board from the outlet's menu in force (sections in the outlet's order, option groups attached to the item), sends it to the kitchen, and only then charges — send to kitchen, then charge, for every POS F&B order (R261, upheld against the v2 frame by POSV2-4). The kitchen ticket is on the rail while the card is in the guest's hand; an unpaid sent order is cancelled while ordered or accepted and voided with a reason after (R125(3), R091(5)); the guest gets an order number, and the customer-facing status board (numbers only) is the kitchen display's KIT-007, mirrored on the till's queue (POSV2-7). TABLE SERVICE (F29, F80, F94): a party is seated with its covers, orders across the visit, courses are fired by the pass (DI-333, DI-407), the bill is printed and settled at the end and split by amount, covers, category, item or seat (DI-106); the client's table statuses are Available → Ordered → Table closed → Reserved with no cleaning status (DI-336); moving and merging tables stay on the staff app until after r2 (POSV2-8). GUEST ORDERING (F11, F48): a guest inside the venue orders in the app or web for pickup or delivery to a seat or a scanned location (DI-288, DI-291); F&B and retail are optional licensed modules completed inside TICVAI (DI-505), kept simple (DI-1091); no food without an admission ticket (DI-292); table reservations and the waitlist do not go through the cart and a dining deposit is a venue option, off by default (DI-1048, DI-1049, R077). KITCHEN (P15, F83, F88): TICVAI's own display on commodity screens (19 September, replacing the 31 July "integration point only", DI-077); one kitchen ticket per preparation station from the outlet's routing rules with a fallback display (DI-323); a fired timer counts up and resets per course, not shown for quick service (DI-334); displays are assigned to stations and filter by course, with no station-load tile in r1 (R277). 86 takes an item off sale on every till and guest menu immediately (R110(c)); guests always see "Sold out", never a missing dish. RETAIL (F17, F34, F51): scan and sell through the same cart, charge and payment as tickets and food (DI-795), one cart, one receipt and one QR per guest (DI-293); system stock per venue gates the sale (DI-294); returns by receipt or order number only in r1 (R139(c)), refund to the original tender with a reason code and note (DI-796, DI-797); Shop & Drop is paid online and collected on the way out (R236), a merchandise reservation lasts to the end of the visit day (R169, R215). TILL MONEY (F32, F73, F74, F87): the float is counted by denomination with note images and typed quantities (DI-775, DI-776, R229) while the hardware checks itself (DI-778); the close is a …

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Send to kitchen | Put the order on the kitchen rail. On the till it always comes before Charge. | Fire, Fire order, Submit order, kitchen fires on payment | R261 / POSV2-4 / F108 step 3 |
| Charge | The till's single tender step (Payment, POS-005); the button reads "Charge AED 110.25". | Checkout (on staff screens), Pay now | F108 step 4 / screens/P04-point-of-sale.yaml#POS-021 |
| Fire / Hold (a course) | Kitchen-pass words for releasing or holding the next course of a table, and the "fired" timer. | using "fire" for sending an order from the till | DI-333 / DI-334 / DI-407 |
| Kitchen ticket | The slip on the kitchen display, one per preparation station. | Order (on the kitchen display), KOT | R210 |
| Ready · Served · Collected · Delivered | How an order reaches the guest; a server marks Served, a counter Collected, a runner Delivered (with the location). | Done, Complete, Bumped (as a status) | R125 / contracts/satellite/fnb.yaml#recordOrderHandover |
| Recall (kitchen) / Recall held sale (till) | Bring a mis-bumped kitchen ticket back to the rail; separately, bring a held cart back into a sale. Never "Recall" alone where both could apply. | Undo bump, Restore | contracts/satellite/fnb.yaml#recallKitchenTicket / POSV2-6 |
| Unavailable (86) / Sold out | Staff screens say "Unavailable" and may add "86"; guest screens say "Sold out". Immediate everywhere. | Out of stock (for food), Disabled, Hidden | R110 / contracts/satellite/fnb.yaml#getGuestMenu |
| Order type | Dine-in · Quick service · Takeaway · Delivery, chosen in the cart. | Service mode, Fulfilment source (on the till) | DI-789 / contracts/satellite/fnb.yaml#/components/schemas/ServiceMode |
| Covers | The number of guests at a table, entered when seating; drives split-by-covers. | Pax (except as a small suffix on the floor plan), Heads | DI-104 / contracts/satellite/fnb.yaml#openTableVisit |
| Vacant · Seated · Ordered · Bill requested · Table closed · … | Table statuses on every floor plan (till and staff app); "Table closed" is the client's word for after payment. | Cleaning, Needs clearing, Dirty | DI-336 / DI-792 |
| Till · Cash drawer | Staff copy may say "till" for the workstation; the cash drawer is the deposit box. | Terminal id as a heading, Deposit box (on staff screens) | R156 |
| Float · Count · Blind count · Variance | The opening float; the denomination count; the closing count made without seeing the expected cash; counted minus expected. | Expected in drawer, Discrepancy, Error | R080 / POSV2-3 |
| Cash out · Cash in · Safe drop | Taking cash out of the drawer mid-shift, adding change, and a supervisor moving cash to the safe with the cashier as witness. | Lift, Withdrawal (as button labels) | DI-274 / contracts/spine/shift.yaml#createCashMovement / … |
| Menu item · Merchandise item · Inventory item · SKU | The scoped product words; SKU is a variant's code, Product stays the sellable thing. | SKU as the item's name, Article | R131 |
| Stock on hand · Allocated · Available | Available is on hand minus allocated. | Inventory (as a number), Free stock | R171 / DI-361 |
| Requisition · Purchase order · Goods receipt · Transfer · … | The procurement and stock words, in that flow. | GRN as the only label, Indent | DI-341 / DI-348 / DI-362 / DI-363 |
| Shop & Drop | Bought and paid now, collected on the way out. | Click & collect | R236 |
| Check-out (rental) · Return (rental) | Handing equipment to the guest and taking it back. On the same screens payment is "Charge" or "Pay". | Checkout (for a handover), Check-in (for a return) | DI-758 / DI-765 |
| Deposit hold · Release · Capture | A refundable deposit held, given back in full, or partly kept for damage with the rest released. | Charge deposit, Refund deposit | DI-752 / R127 |
| Extension · Swap · Overdue · Late fee | The active-rental words; a quick swap restarts the clock, a late swap earns a free extension. | Renewal, Exchange (for a swap) | DI-761 / DI-762 / DI-764 |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `EMP-081` | Active Rental Operations Command Center | D | 2 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `EMP-082` | Active Rental Detail & Live Timeline | D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `EMP-083` | Rental Extension Request | D | 2 | 8 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `EMP-084` | Extension Pricing & Confirmation | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `EMP-085` | Equipment Swap / Replacement | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `EMP-086` | Rental Incident & Operational Exception | D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `EMP-087` | Due Soon & Customer Notification Management | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `EMP-088` | Overdue Rental Management | D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `EMP-089` | Active Group Rental Management | D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `EMP-090` | Active Rental Intelligence & Operational Alerts | D | 0 | 9 | 6 | 0 | 1 | 6 | — | notStarted (generated) |

## Thin screens in this batch

**EMP-082, EMP-084, EMP-085, EMP-086, EMP-087, EMP-088, EMP-089, EMP-090 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `EMP-081` Active Rental Operations Command Center

**Provide operators and supervisors with a real-time view of every rental currently in progress.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task APP-STAFF-EMP-081 |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | commandCentre (comfortable density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/active-rental-operations-command-center-emp-081` |

**What the spec says about it.** The staff-app form of `BO-554`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**From the Food, Beverage & Retail process.** Everything currently out, for the attendant and the station supervisor: who has what, when it is due back, and what is late. One list with chips for Due soon and Overdue (the contract makes them one query at two thresholds), replacing the separate due-soon, overdue and group screens.

**Known correction pending (do not draw the wrong version)**

- **Board 7 is ten screens around one list and one rental. Consolidate to two per platform: Active rentals (EMP-081 with EMP-087 Due soon and EMP-088 Overdue as filters and EMP-090's alerts as a strip) and Rental detail (EMP-082 with EMP-089 - a group is one booking with participants), with Extend …** Why: listOverdueRentals is explicitly one query at two thresholds; a group rental is one booking; DI-671 asks for consolidation. *(source: contracts/satellite/rental.yaml#listOverdueRentals / contracts/satellite/rental.yaml#/components/schemas/RentalParticipant / DI-671; Food, Beverage & Retail)*
- **Tiles "Extensions Requested", "Equipment Swap Required" and "Active Incidents" have no data source; the Venue filter is meaningless on a venue-scoped handheld.** Why: An extension is applied immediately (no request state), no booking field flags a needed swap, and there is no operation listing incidents. *(source: contracts/satellite/rental.yaml#extendRental / contracts/satellite/rental.yaml#reportRentalIncident / contracts/satellite/rental.yaml#/components/schemas/RentalBooking; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search active rental operations | search field | — | — | — | — | — | — |
| Filter by | text field | optional | — | — | — | Sends `?status=` to `listRentalBookings` (the rental status; location goes as `locationId`) (CHG-RFM-012). The pack filters this screen by venue, location, product, customer, rental status, expected … | `listRentalBookings` ?status |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Location | picker: choose a location | — | — | `listRentalBookings` ?locationId |
| From | date and time picker | — | — | `listRentalBookings` ?from |
| To | date and time picker | — | — | `listRentalBookings` ?to |
| Due within minutes | number field (minutes) | — | — | `listOverdueRentals` ?dueWithinMinutes |
| Location | picker: choose a location | — | — | `listOverdueRentals` ?locationId |

#### Outputs: what the screen shows and produces

**Shown**

**Active Rentals** (metric tile)

**Due Within 30 Minutes** (metric tile)

**Overdue** (metric tile)

**Extensions Requested** (metric tile)

**Equipment Swap Required** (metric tile)

**Active Incidents** (metric tile)

**Group Rentals Active** (metric tile)

**Expected Returns Next Hour** (metric tile)

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Active rental row**: Guest, units (tags), due back time and a live countdown ("due in 12 min"), turning amber inside the due-soon threshold and red when overdue with the accruing late fee ("57 min late - AED 35.00 so far"). Sort: overdue first, then due soonest. *(source: contracts/satellite/rental.yaml#listOverdueRentals / DI-761 / DI-764)*
- **Counters**: Active rentals · Due within 30 min · Overdue · Group rentals out · Expected back next hour. Tap filters the list. *(source: contracts/satellite/rental.yaml#listRentalBookings / contracts/satellite/rental.yaml#listOverdueRentals)*

**Data it reads**: `listRentalBookings` (onLoad, Rentals out right now); `listOverdueRentals` (onLoad, Due soon and late)

**Where the user goes next**

- → `EMP-003` Home — on duty: *Back to Home — on duty*
- → `EMP-082` Active Rental Detail & Live Timeline: *Active Rental Detail & Live Timeline*; carries `bookingId`
- → `EMP-083` Rental Extension Request: *Rental Extension Request*
- → `EMP-084` Extension Pricing & Confirmation: *Extension Pricing & Confirmation*; carries `bookingId`
- → `EMP-085` Equipment Swap / Replacement: *Equipment Swap / Replacement*; carries `bookingId`
- → `EMP-086` Rental Incident & Operational Exception: *Rental Incident & Operational Exception*
- → `EMP-087` Due Soon & Customer Notification Management: *Due Soon & Customer Notification Management*
- → `EMP-088` Overdue Rental Management: *Overdue Rental Management*
- → `EMP-089` Active Group Rental Management: *Active Group Rental Management*; carries `bookingId`
- → `EMP-090` Active Rental Intelligence & Operational Alerts: *Active Rental Intelligence & Operational Alerts*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No active rental operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the active rental operations are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the active rental operations untouched. |
| Loading (`?state=loading`) | The active rental operations list; the counts above it resolve separately. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Consistency with other screens

- Match `EMP-071`: Same row component.
- Match `BO-554`: Shared design; the desk adds the venue-wide view.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
counters:
  active: 64
  dueWithin30Min: 9
  overdue: 3
  groupsOut: 2
  expectedNextHour: 21
rows:
- guest: Daniel Brooks
  units:
  - SUP-011
  due: '10:30'
  state: 57 min late - AED 35.00 so far
- guest: Priya Nair
  units:
  - STR-P (pooled stroller)
  due: '13:00'
  state: due in 2 h 05 min
```

#### Permissions

- `listRentalBookings` → `RENTAL_VIEW` (read) · staff
- `listOverdueRentals` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Active operations view tracks all rented items and durations in real time; rental detail timeline shows booking time, handover time and expected return time per item, with extension requests and extension pricing. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-761)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-081` · status **notStarted** · provenance generated
- Workshop pack:  board 7

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-081?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `EMP-003`, `EMP-082`, `EMP-083`, `EMP-084`, `EMP-085`, `EMP-086`, `EMP-087`, `EMP-088`, `EMP-089`, `EMP-090`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-082` Active Rental Detail & Live Timeline

**Provide the complete operational view of one active rental.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task APP-STAFF-EMP-082 |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/active-rental-detail-live-timeline-emp-082` |

**What the spec says about it.** The staff-app form of `BO-555`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** One rental while it is out: who, which units, when it went out, when it is due, what it is accruing, and the actions the attendant may take (Extend, Swap, Report incident, Start return). A timeline per item, as the client asked.

**Known correction pending (do not draw the wrong version)**

- **The booking read carries no equipment assignments and no events, so the per-item timeline (DI-761) and the per-unit states of a group cannot be drawn; there is also no booking creation time.** Why: getRentalBooking's summary promises "its timeline" but the schema has only checkedOutAt, dueBackAt and returnedAt. *(source: contracts/satellite/rental.yaml#getRentalBooking / contracts/satellite/rental.yaml#/components/schemas/RentalBooking / DI-761; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Timeline**: Booked at · Checked out at (by whom) · Extended to · Swapped (old/new unit) · Incident · Due back - each with the GST time; per item for a group. *(source: DI-761 / contracts/satellite/rental.yaml#/components/schemas/RentalBooking)*

**Where the user goes next**

- → `EMP-081` Active Rental Operations Command Center: *Back to Active Rental Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No active rental detail yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the active rental detail are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the active rental detail untouched. |
| Loading (`?state=loading`) | The active rental detail list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Consistency with other screens

- Match `BO-543`: The reservation detail before check-out; the same header and timeline component continue here.
- Match `BO-555`: Shared design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
booking: RNT-10482, Aisha Rahman
timeline:
- Booked 14 Oct 19:22 (guest app)
- Checked out 10:04 by Priya Nair
- Extended to 11:30 (+30 min, AED 25.00)
- Due back 11:30
```

#### Permissions

- `getRentalBooking` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Active operations view tracks all rented items and durations in real time; rental detail timeline shows booking time, handover time and expected return time per item, with extension requests and extension pricing. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-761)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-082` · status **notStarted** · provenance generated
- Workshop pack:  board 7

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-082?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `EMP-081`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-083` Rental Extension Request

**Allow the customer or operator to request additional rental time. This is one of the important capabilities I recommend formally adding to the rental scope.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task APP-STAFF-EMP-083 |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/rental-extension-request-emp-083` |

**What the spec says about it.** The staff-app form of `BO-556`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** "Can I keep it another hour?" - first check that the units are free for the longer window, then price it. Opened from the rental detail as a sheet that continues straight into pricing (EMP-084). Get right: check availability before showing any price.

**Known correction pending (do not draw the wrong version)**

- **The "Extension check" table's columns are schema paths (RentalAvailability.windows[].availableQuantity, blockedWindows[].reason ...), and the screen has no bookingId entry parameter although it acts on one rental.** Why: Plumbing on a user screen; and for a serialised rental the check must be for the units already assigned, not the product in general. *(source: screens/P06-staff-app.yaml#EMP-083; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Additional duration | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?to=` to `getRentalAvailability` (the expected return plus the added time) (CHG-RFM-012). +30, +60, +90 min or Custom; sets the `to` sent to `getRentalAvailability`. | `getRentalAvailability` ?to |
| Requested new return | text field | — | — | — | — | Computed from expected return plus the added duration; read-only. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `getRentalAvailability` ?productId |
| Location | picker: choose a location | — | — | `getRentalAvailability` ?locationId |
| From | date and time picker | — | — | `getRentalAvailability` ?from |
| Quantity | number field | 1 | — | `getRentalAvailability` ?quantity |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Additional time**: Chips in the venue's extension increment (default 30 min - +30, +60, +90) plus Custom; the new return time is computed and shown, not typed. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalFeePolicy / screens/P06-staff-app.yaml#EMP-083)*

#### Outputs: what the screen shows and produces

**Shown**

**Current rental** (detail panel): No rental read is bound; these are the pack's labels.

| Shows | Format | Notes |
|---|---|---|
| Start | text | not in the schema: `Start` |
| Expected return | text | not in the schema: `Expected return` |
| Current duration | text | not in the schema: `Current duration` |

**Extension check** (data table, from `getRentalAvailability`): EXTENSION AVAILABLE when the window stays open; otherwise the first blocking window's reason. The pack names the blocking asset (BIKE-017); no field does.

| Shows | Format | Notes |
|---|---|---|
| Available quantity | 1,234 | — |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| Reason | chip: Booked, Turnaround, Maintenance, Blackout, Closed, Buffer… | — |
| Blocking asset | text | not in the schema: `Blocking asset` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Check availability (secondary button) | `getRentalAvailability` GET `/rental-availability` | — | RentalAvailability | — | — |
| Continue to pricing (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Availability answer**: "Extension available until 12:00" in green, or "BIKE-014 is booked from 11:45" with the longest possible extension offered ("Extend to 11:30 instead"). *(source: contracts/satellite/rental.yaml#extendRental / contracts/satellite/rental.yaml#getRentalAvailability)*

**Data it reads**: `getRentalAvailability` (onLoad, Can it be extended)

**Where the user goes next**

- → `EMP-081` Active Rental Operations Command Center: *Back to Active Rental Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No rental extension request yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental extension request are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental extension request untouched. |
| Loading (`?state=loading`) | The rental extension request list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Consistency with other screens

- Match `BO-556`: Shared design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
current:
  start: '10:00'
  due: '11:00'
request: +60 min
answer: Available until 12:00
```

#### Permissions

- `getRentalAvailability` → `RENTAL_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Active operations view tracks all rented items and durations in real time; rental detail timeline shows booking time, handover time and expected return time per item, with extension requests and extension pricing. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-761)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-083` · status **notStarted** · provenance generated
- Workshop pack:  board 7

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-083?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: Check availability, Continue to pricing.
- [ ] Every transition is wired: `EMP-081`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-084` Extension Pricing & Confirmation

**Calculate the commercial impact of an approved extension. Once Board 3 confirms availability, Board 4 calculates the extension charge.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task APP-STAFF-EMP-084 |
| Who uses it | venue staff holding `RENTAL_OPERATE`, `RENTAL_VIEW` (1 operate, 1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/extension-pricing-confirmation-emp-084` |

**What the spec says about it.** The staff-app form of `BO-557`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Price the extension, get the guest's yes and payment, then extend. The price is the venue's extension price per increment, deliberately cheaper than paying late; show that comparison so the attendant can sell it.

**Known correction pending (do not draw the wrong version)**

- **The extension is priced with quoteRentalPrice, which prices a new rental from the pricing profile and returns a deposit, while the fee policy defines the extension price per increment; and no payment step exists between quote and extend.** Why: The extension charge would come out at the base rental rate with a second deposit; the contract text itself says "take acceptance, take payment". *(source: contracts/satellite/rental.yaml#quoteRentalPrice / contracts/satellite/rental.yaml#/components/schemas/RentalFeePolicy / contracts/satellite/rental.yaml#extendRental; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Price**: "+60 min - AED 50.00 (2 x 25.00)" with, beneath it, "If returned late instead: AED 70.00". No deposit line - the deposit already held does not change. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalFeePolicy / DI-753)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Charge and extend**: Takes payment through the usual Charge step, then extends with the accepted quote. Quote expired -> re-price with a note; conflict -> back to the availability answer. *(source: contracts/satellite/rental.yaml#extendRental)*
- **Extend free**: Only as an extension-fee waiver override (reason required); this is also how a late swap's compensation is given (DI-762). *(source: contracts/satellite/rental.yaml#/components/schemas/RentalOverride / DI-762)*

**Where the user goes next**

- → `EMP-081` Active Rental Operations Command Center: *Back to Active Rental Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No extension pricing confirmation yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the extension pricing confirmation are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the extension pricing confirmation untouched. |
| Loading (`?state=loading`) | The extension pricing confirmation list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The equipment is reserved for a later booking. The conflicting booking's window is named, so the counter can offer a shorter extension instead of a refusal.; 422 `quoteExpired` or `quoteMismatch` on `acceptedQuoteId`. |

#### Consistency with other screens

- Match `BO-557`: Shared design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
extension:
  from: '11:00'
  to: '12:00'
  price: AED 50.00
  vatIncluded: AED 2.38
  lateAlternative: AED 70.00
```

#### Permissions

- `quoteRentalPrice` → `RENTAL_VIEW` (read) · staff, guest
- `extendRental` → `RENTAL_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Active operations view tracks all rented items and durations in real time; rental detail timeline shows booking time, handover time and expected return time per item, with extension requests and extension pricing. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-761)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-084` · status **notStarted** · provenance generated
- Workshop pack:  board 7

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-084?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `EMP-081`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`, `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-085` Equipment Swap / Replacement

**Replace equipment during an active rental without terminating and recreating the rental. This is another capability I strongly recommend adding.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task APP-STAFF-EMP-085 |
| Who uses it | venue staff holding `RENTAL_OPERATE` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/equipment-swap-replacement-emp-085` |

**What the spec says about it.** The staff-app form of `BO-558`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** A unit fails mid-rental: take it back, give a replacement, keep the rental going. The client's rule decides the time: a quick swap restarts the clock from the replacement, a later one keeps the clock and lets the attendant give that booking a free extension. The faulty unit goes to maintenance, not back to the pool.

**Known correction pending (do not draw the wrong version)**

- **The swap operation says "the deposit, the agreement and the clock stay where they are" and has no field to restart the clock or grant free time; the quick-swap threshold is not a venue setting anywhere.** Why: Contradicts the agreed swap rule (DI-762); the threshold is a configured limit that should be a venue setting with a tenant default (R094). *(source: contracts/satellite/rental.yaml#swapRentalEquipment / DI-762 / R094; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Reason**: A short list (Brake fault, Puncture, Leak, Comfort/size, Other); "Other" needs a note. *(source: R222 / contracts/satellite/rental.yaml#swapRentalEquipment)*
- **Replacement unit**: Scanned like the equipment step; may be left empty only to end that unit early. *(source: contracts/satellite/rental.yaml#swapRentalEquipment / DI-762)*
- **Time**: Within the quick-swap threshold (e.g. 5 min since check-out) show "Clock restarts at 10:07". After it, show "Clock unchanged - due 11:00" with an optional "Add free time" (e.g. +15 min). *(source: DI-762 / MoM 2026-09-09 4.8 / TRACKER Workshops/Actions row 267)*
- **Raise maintenance job**: On by default for the outgoing unit. *(source: contracts/satellite/rental.yaml#swapRentalEquipment)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `EMP-081` Active Rental Operations Command Center: *Back to Active Rental Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No equipment swap replacement yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the equipment swap replacement are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the equipment swap replacement untouched. |
| Loading (`?state=loading`) | The equipment swap replacement list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Consistency with other screens

- Match `BO-558`: Shared design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
out:
  unit: BIKE-014
  reason: Brake fault
in: BIKE-031
checkedOutAt: '10:04'
swappedAt: '10:21'
timeRule: Clock unchanged - due 12:15; free time +15 min granted
```

#### Permissions

- `swapRentalEquipment` → `RENTAL_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Equipment swap assigns the replacement to the booking. Swap within a short threshold (e.g. 5 minutes) restarts the timer; a later swap (e.g. 15 minutes into 30) lets the operator grant that booking only a free time extension/buffer. *(agreed · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-762)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-085` · status **notStarted** · provenance generated
- Workshop pack:  board 7

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-085?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `EMP-081`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-086` Rental Incident & Operational Exception

**Capture incidents occurring while equipment is in customer possession.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task APP-STAFF-EMP-086 |
| Who uses it | venue staff holding `RENTAL_OPERATE` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/rental-incident-operational-exception-emp-086` |

**What the spec says about it.** The staff-app form of `BO-559`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Log something that happened during a rental - injury, loss, theft, complaint, equipment failure, safety breach - against the booking and the unit. Distinct from damage at return: an incident may carry no charge and still be the most important event of the day.

**Known correction pending (do not draw the wrong version)**

- **The screen has no bookingId or assetId entry parameter, although it is opened for one rental and one unit.** Why: Without them the attendant would have to identify the booking again; pre-fill both from the rental detail. *(source: screens/P06-staff-app.yaml#EMP-086 / contracts/satellite/rental.yaml#reportRentalIncident; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Kind**: Large tiles; "Other" needs a note. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalIncident / R222)*
- **Severity**: Low / Medium / High / Critical; High and Critical show "Authorities notified?" and the supervisor's call button. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalIncident)*
- **Photos**: Optional. *(source: DI-766)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `EMP-081` Active Rental Operations Command Center: *Back to Active Rental Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No rental incident operational yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental incident operational are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental incident operational untouched. |
| Loading (`?state=loading`) | The rental incident operational list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Consistency with other screens

- Match `BO-559`: Shared design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
incident:
  booking: RNT-10487
  unit: BIKE-022
  kind: Equipment failure
  severity: Medium
  description: Guest reports front brake slipping on the hill path; bike walked back to hub
```

#### Permissions

- `reportRentalIncident` → `RENTAL_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Incidents (e.g. reported brake malfunction) are logged against the booking; automatic SMS/app return reminders to the customer. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-763)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-086` · status **notStarted** · provenance generated
- Workshop pack:  board 7

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-086?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `EMP-081`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-087` Due Soon & Customer Notification Management

**Proactively communicate with customers before their rental becomes overdue. The original matrix requires overdue rental notifications.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task APP-STAFF-EMP-087 |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/due-soon-customer-notification-management-emp-087` |

**What the spec says about it.** The staff-app form of `BO-560`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Rentals due back soon, so the guest can be reminded before they are late. After consolidation this is the "Due soon" filter of the active list with a "Send reminder" action per row; reminders are also sent automatically.

**Known correction pending (do not draw the wrong version)**

- **The screen has no action at all, while the client asked for return reminders by SMS/app.** Why: A due-soon list nobody can act on; merge into EMP-081 with Send reminder (see EMP-088 for the message operation's own problem). *(source: screens/P06-staff-app.yaml#EMP-087 / DI-763; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Due within minutes | number field (minutes) | — | — | `listOverdueRentals` ?dueWithinMinutes |
| Location | picker: choose a location | — | — | `listOverdueRentals` ?locationId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Due-soon row**: Guest, units, due time, minutes left, last reminder sent ("SMS 10:30"). *(source: contracts/satellite/rental.yaml#listOverdueRentals / DI-763)*

**Data it reads**: `listOverdueRentals` (onLoad, Due soon)

**Where the user goes next**

- → `EMP-081` Active Rental Operations Command Center: *Back to Active Rental Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No due soon customer yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the due soon customer are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the due soon customer untouched. |
| Loading (`?state=loading`) | The due soon customer list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Consistency with other screens

- Match `EMP-081`: Same list, Due soon filter.
- Match `BO-560`: Shared design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- guest: Omar Ziad
  unit: KAY-007
  due: '11:00'
  left: 18 min
  reminder: SMS sent 10:45
```

#### Permissions

- `listOverdueRentals` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Incidents (e.g. reported brake malfunction) are logged against the booking; automatic SMS/app return reminders to the customer. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-763)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-087` · status **notStarted** · provenance generated
- Workshop pack:  board 7

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-087?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `EMP-081`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-088` Overdue Rental Management

**Provide operators with a dedicated workflow for rentals that have exceeded their expected return time. The original requirement calls for automatic late-fee calculation, configurable grace periods and overdue notifications.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task APP-STAFF-EMP-088 |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/overdue-rental-management-emp-088` |

**What the spec says about it.** The staff-app form of `BO-561`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-008): sendTransactionalMessage declares the service and partner audiences, not staff, so a staff device cannot call it as declared (design-notes correction fnb-retail …

**From the Food, Beverage & Retail process.** Rentals past due: how late, what it is accruing, and contact with the guest. After consolidation this is the "Overdue" filter of the active list. Show the point at which a late rental becomes "Not returned" (the deposit is then captured in full).

**Fixed on main** (the package already carries these; draw what it says): The message operation bound here (sendTransactionalMessage) declares the service and partner audiences, not staff, and asks for template … (CHG-WIR-008).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Due within minutes | number field (minutes) | — | — | `listOverdueRentals` ?dueWithinMinutes |
| Location | picker: choose a location | — | — | `listOverdueRentals` ?locationId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Overdue row**: "57 min late - AED 35.00 so far" (grace already applied), guest mobile with Call, and "Becomes Not returned at 18:00" when the venue sets that threshold. *(source: contracts/satellite/rental.yaml#listOverdueRentals / contracts/satellite/rental.yaml#/components/schemas/RentalFeePolicy / DI-764)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Send reminder**: Picks the venue's overdue template by name and the channel (SMS / WhatsApp / App); queued result shown on the row; "No mobile on file" when the guest has none. *(source: contracts/satellite/marketing-crm.yaml#sendTransactionalMessage)*

**Data it reads**: `listOverdueRentals` (onLoad, Late, and what it is accruing)

**Where the user goes next**

- → `EMP-081` Active Rental Operations Command Center: *Back to Active Rental Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No overdue rental yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the overdue rental are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the overdue rental untouched. |
| Loading (`?state=loading`) | The overdue rental list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Consistency with other screens

- Match `BO-561`: Shared design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- guest: Daniel Brooks
  unit: SUP-011
  due: '10:30'
  late: 57 min
  accrued: AED 35.00
  mobile: +971 50 412 8836
```

#### Permissions

- `listOverdueRentals` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Overdue tracking flags bookings past expected return and applies configured overdue pricing; a group / multi-item active-rental view and an intelligence panel (utilisation, incident trends) complete the board. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-764)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-088` · status **notStarted** · provenance generated
- Workshop pack:  board 7

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-088?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `EMP-081`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-089` Active Group Rental Management

**Manage group rentals where multiple pieces of equipment may have different operational states.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task APP-STAFF-EMP-089 |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/active-group-rental-management-emp-089` |

**What the spec says about it.** The staff-app form of `BO-562`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** A group rental while out - one booking, many units, each possibly in a different state (out, swapped, returned early, late). After consolidation this is the rental detail with one row per participant/unit.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Group rows**: Participant, unit, state (Out / Returned / Swapped / Late), due time; header shows "8 of 10 out, 2 back". *(source: contracts/satellite/rental.yaml#/components/schemas/RentalParticipant / DI-764 / DI-767)*

**Where the user goes next**

- → `EMP-081` Active Rental Operations Command Center: *Back to Active Rental Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No active group rental yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the active group rental are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the active group rental untouched. |
| Loading (`?state=loading`) | The active group rental list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Consistency with other screens

- Match `EMP-082`: Same screen after consolidation; the assignments gap noted there blocks this view too.
- Match `BO-562`: Shared design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
group: RNT-10487, 10 x Mountain bike M
summary: 8 out, 2 returned early (Omar Ziad BIKE-014, Fatima Al Suwaidi BIKE-022)
```

#### Permissions

- `getRentalBooking` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Overdue tracking flags bookings past expected return and applies configured overdue pricing; a group / multi-item active-rental view and an intelligence panel (utilisation, incident trends) complete the board. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-764)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-089` · status **notStarted** · provenance generated
- Workshop pack:  board 7

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-089?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `EMP-081`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-090` Active Rental Intelligence & Operational Alerts

**Use AI and real-time operational data to identify risks before they become operational problems.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task APP-STAFF-EMP-090 |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/active-rental-intelligence-operational-alerts-emp-090` |

**What the spec says about it.** The staff-app form of `BO-563`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Food, Beverage & Retail process.** Operational alerts for the station. On the handheld keep only what an attendant acts on now - rentals due in the next hour and late ones - as a strip on the active list. Predictions and trends belong to the back office's rental analytics.

**Known correction pending (do not draw the wrong version)**

- **The table is titled "Every active rental intelligence", the detail panel's headings are sample values ("RNT-10482", "Confirmed", "Ready for Checkout"), and five of seven columns (predicted late returns, future conflicts, extension demand, return pressure, inventory shortage) have no operation …** Why: Generated plumbing and unbound predictions; and the client agreed AI's role in rentals is reporting and maintenance recommendations, with day-to-day operations staff-managed. *(source: screens/P06-staff-app.yaml#EMP-090 / DI-772 / DI-764; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Due within minutes | number field (minutes) | — | — | `listOverdueRentals` ?dueWithinMinutes |
| Location | picker: choose a location | — | — | `listOverdueRentals` ?locationId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every active rental intelligence** (data table)

| Shows | Format | Notes |
|---|---|---|
| Rentals due next hour | text | not in the schema: `Rentals due next hour` |
| Predicted late returns | text | not in the schema: `Predicted late returns` |
| Future reservation conflicts | text | not in the schema: `Future reservation conflicts` |
| Extension demand | text | not in the schema: `Extension demand` |

**The selected active rental intelligence** (detail panel): The pack groups this record's detail under its own headings: “RNT-10482”, “Confirmed”, “Ready for Checkout”, “Active”, “Incident”, “Overdue”.

| Shows | Format | Notes |
|---|---|---|
| Rentals due next hour | text | not in the schema: `Rentals due next hour` |
| Predicted late returns | text | not in the schema: `Predicted late returns` |
| Future reservation conflicts | text | not in the schema: `Future reservation conflicts` |
| Extension demand | text | not in the schema: `Extension demand` |
| Equipment incident trends | text | not in the schema: `Equipment incident trends` |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Alert strip**: "9 due back in the next hour · 3 overdue" with tap-through. *(source: contracts/satellite/rental.yaml#listOverdueRentals / DI-772)*

**Data it reads**: `listOverdueRentals` (onLoad, Operational alerts)

**Where the user goes next**

- → `EMP-081` Active Rental Operations Command Center: *Back to Active Rental Operations Command Center*

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No active rental intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the active rental intelligence are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the active rental intelligence untouched. |
| Loading (`?state=loading`) | The active rental intelligence list. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Consistency with other screens

- Match `BO-563`: The desk version may keep the intelligence panel.
- Match `BO-584`: Rental executive analytics own utilisation and incident trends.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
strip: 9 due back in the next hour - 3 overdue
```

#### Permissions

- `listOverdueRentals` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Overdue tracking flags bookings past expected return and applies configured overdue pricing; a group / multi-item active-rental view and an intelligence panel (utilisation, incident trends) complete the board. *(client request · MoM 9 Sep 2026, 4.8 Active Rental Operations, Swaps & Exceptions · DI-764)*

Also apply: 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-090` · status **notStarted** · provenance generated
- Workshop pack:  board 7

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-090?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `EMP-081`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**10 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"extendRental": {"method":"POST","path":"/rental-bookings/{bookingId}/extend","contract":"rental","summary":"Keep it longer, if it is free and the guest accepts the price","permission":"RENTAL_OPERATE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RentalBooking"},
"getRentalAvailability": {"method":"GET","path":"/rental-availability","contract":"rental","summary":"What can be rented, when, with turnaround already subtracted","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":true},{"name":"locationId","in":"query","required":null},{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"quantity","in":"query","required":null}],"requestBody":null,"responds":"RentalAvailability"},
"getRentalBooking": {"method":"GET","path":"/rental-bookings/{bookingId}","contract":"rental","summary":"One booking, its timeline and its readiness","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RentalBooking"},
"listOverdueRentals": {"method":"GET","path":"/rental-bookings/overdue","contract":"rental","summary":"What is late, by how long, and what it is accruing","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"dueWithinMinutes","in":"query","required":null},{"name":"locationId","in":"query","required":null}],"requestBody":null,"responds":"RentalBooking"},
"listRentalBookings": {"method":"GET","path":"/rental-bookings","contract":"rental","summary":"Reservations across venues and locations","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"locationId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"RentalBooking"},
"quoteRentalPrice": {"method":"POST","path":"/rental-price","contract":"rental","summary":"What this rental would cost, and the deposit it would hold","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalQuoteRequest","responds":"RentalQuote"},
"reportRentalIncident": {"method":"POST","path":"/rental-incidents","contract":"rental","summary":"Something happened during a rental","permission":"RENTAL_OPERATE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalIncident","responds":"RentalIncident"},
"swapRentalEquipment": {"method":"POST","path":"/rental-bookings/{bookingId}/swap","contract":"rental","summary":"Replace a faulty item mid-rental","permission":"RENTAL_OPERATE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RentalBooking"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"RentalAvailability": {"type":"object","description":"Board 3. **A pooled product answers with a count, a serialised one with assets.**","properties":{"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid","nullable":true},"windows":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"availableQuantity":{"type":"integer"},"availableAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"blockedWindows":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"reason":{"type":"string","enum":["booked","turnaround","maintenance","blackout","closed","buffer","held"]}}}}}},
"RentalBooking": {"type":"object","x-ticvai-persistence":"rental.booking","description":"Board 5. **The booking outlives the order** — an order completes at payment and the rental is still out.\n","required":["id","productId","from","to","status"],"properties":{"id":{"type":"string","format":"uuid"},"reference":{"type":"string"},"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"returnLocationId":{"type":"string","format":"uuid","nullable":true},"customerId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer"},"status":{"type":"string","enum":["draft","confirmed","awaitingArrival","checkedOut","overdue","partiallyReturned","completed","completedWithDamage","notReturned","cancelled","noShow"]},"checkedOutAt":{"type":"string","format":"date-time","nullable":true},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"returnedAt":{"type":"string","format":"date-time","nullable":true},"depositAuthorisationId":{"type":"string","format":"uuid","nullable":true,"description":"The card deposit's terminal pre-authorisation, written by `checkOutRental` (workbook Q304; CHG-CSA-029). The hold is kept whole until every unit is back (workbook Q306)."},"accruedLateFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"readiness":{"type":"array","readOnly":true,"description":"**Computed, not stored** — agreement, requirements, deposit, equipment.","items":{"type":"object","properties":{"check":{"type":"string"},"satisfied":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"participants":{"type":"array","items":{"$ref":"#/components/schemas/RentalParticipant"}},"scopePath":{"type":"string"}}},
"RentalIncident": {"type":"object","x-ticvai-persistence":"rental.incident","description":"Board 7.6. **Distinct from damage** — an incident may carry no charge and still be the most important thing that happened.\n","required":["kind","description"],"properties":{"id":{"type":"string","format":"uuid"},"bookingId":{"type":"string","format":"uuid","nullable":true},"assetId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["injury","loss","theft","complaint","equipmentFailure","safetyBreach","other"]},"description":{"type":"string"},"severity":{"type":"string","enum":["low","medium","high","critical"]},"reportedBy":{"type":"string","format":"uuid"},"reportedAt":{"type":"string","format":"date-time"},"photoAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"workOrderId":{"type":"string","format":"uuid","nullable":true},"authorityNotified":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"RentalParticipant": {"type":"object","x-ticvai-persistence":"rental.participant","description":"Board 5.5. **A group rental is one booking with participants**, because the agreement, the deposit and the return are handled together.\n","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"isPrimaryRenter":{"type":"boolean","default":false},"dateOfBirth":{"type":"string","format":"date","nullable":true},"idNumber":{"type":"string","nullable":true},"guardianName":{"type":"string","nullable":true},"emergencyContact":{"type":"string","nullable":true},"hasSignedWaiver":{"type":"boolean","readOnly":true},"customFields":{"type":"object","additionalProperties":true}}},
"RentalQuote": {"type":"object","x-ticvai-persistence":"rental.quote","description":"Board 4.10. **Rental amount and deposit are returned apart, because the deposit is not revenue.**\n**A quote `quoteRentalPrice` issues is stored until `expiresAt`**, with what was asked, so the figures it gave can be held to and checked later. `explainRentalPrice` and `simulateRentalPricing` return the same shape and store nothing (decided 29 September, data model DM4).\n**Consumed by `acceptedQuoteId`** on `createRentalBooking` and the extension. A quote is not deleted when it is used or expires: a nightly job removes quotes 30 days past `expiresAt` that no booking references, so a booking can always show the quote it was priced at (decided 29 September, writers pass; DM4).\n","required":["quoteId","productId","from","to","rentalAmount","depositAmount"],"properties":{"quoteId":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid","description":"The request's product; with `locationId`, `from`, `to` and `quantity`, what was quoted."},"locationId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer","default":1},"customerId":{"type":"string","format":"uuid","nullable":true},"rentalAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"addOnAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalPayable":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"depositInstrument":{"type":"string","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005), written at `venue` scope."}}},
"RentalQuoteRequest": {"type":"object","required":["productId","from","to"],"properties":{"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer","default":1},"salesChannel":{"type":"string","nullable":true},"customerId":{"type":"string","format":"uuid","nullable":true},"promotionCode":{"type":"string","nullable":true}}}
}
```
