# WS92 — Rental Management board 5

**10 screens · 7 operations · 7 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `RENTAL_BOOK, RENTAL_VIEW`. A control nobody can use must say so,
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
| `BO-534` | Rental Booking Command Center | B–D | 2 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-535` | New Rental Booking Wizard | B–D | 7 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-536` | Availability Selection & Alternative Options | B–D | 4 | 8 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-537` | Customer & Participant Information | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-538` | Group Rental & Participant Management | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-539` | Rental Agreement & Waiver Completion | B–D | 0 | 14 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-540` | Booking Commercial Summary & Payment | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-541` | Reservation Confirmation & QR Voucher | B–D | 0 | 0 | 6 | 0 | 1 | 2 | — | notStarted (—) |
| `BO-542` | Reservation Modification, Cancellation & No-Show | B–D | 0 | 10 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-543` | Reservation Detail, Timeline & Readiness | B–D | 3 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-537, BO-539, BO-540, BO-541, BO-543 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-534` Rental Booking Command Center

**Provide a single operational view of all rental reservations across venues and locations.**

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
| Route | `/rentals/rental-booking-command-center-bo-534` |

**What the spec says about it.** **Measure names, not "Revenue"** (decided 2 October 2026, Chinmay; CHG-FIN-002; BOARDREQ MOM-2758..2761). Takings (money taken less money paid back, a cash-control figure), Gross sales (before discounts, excluding VAT), Net revenue (gross sales less discounts and refunds), Recognised revenue and Deferred revenue are different numbers and never share a label; a tile takes its label from the seeded KPI it is bound to (`ReportingSystemKpi`).

**From the Food, Beverage & Retail process.** All rental bookings across stations: today's, upcoming, awaiting arrival (online not collected), checked out, completed, cancelled, no-shows, groups. The one thing to get right: tiles filter the list; status words match the check-out and return screens.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search rental booking | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by date, venue, location, product, booking type, channel and 2 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRentalBookings` ?status |
| Location | picker: choose a location | — | — | `listRentalBookings` ?locationId |
| From | date and time picker | — | — | `listRentalBookings` ?from |
| To | date and time picker | — | — | `listRentalBookings` ?to |

#### Outputs: what the screen shows and produces

**Shown**

**Today's Reservations** (metric tile)

**Upcoming Rentals** (metric tile)

**Awaiting Arrival** (metric tile)

**Checked Out** (metric tile)

**Completed** (metric tile)

**Cancelled** (metric tile)

**No-Shows** (metric tile)

**Group Bookings** (metric tile)

**Gross sales today** (metric tile): (CHG-FIN-002: never a bare "Revenue")

**Booking Alerts** (metric tile)

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Bookings**: Reference, guest, product, quantity, station, from–to, status (Confirmed · Awaiting arrival · Checked out · Overdue · Partly returned · Completed · Cancelled · No-show). *(source: DI-754 / contracts/satellite/rental.yaml#/components/schemas/RentalBooking)*

**Data it reads**: `listRentalBookings` (onLoad, Reservations across locations)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-535` New Rental Booking Wizard: *New Rental Booking Wizard*
- → `BO-536` Availability Selection & Alternative Options: *Availability Selection & Alternative Options*
- → `BO-537` Customer & Participant Information: *Customer & Participant Information*
- → `BO-538` Group Rental & Participant Management: *Group Rental & Participant Management*
- → `BO-539` Rental Agreement & Waiver Completion: *Rental Agreement & Waiver Completion*
- → `BO-540` Booking Commercial Summary & Payment: *Booking Commercial Summary & Payment*
- → `BO-541` Reservation Confirmation & QR Voucher: *Reservation Confirmation & QR Voucher*
- → `BO-542` Reservation Modification, Cancellation & No-Show: *Reservation Modification, Cancellation & No-Show*
- → `BO-543` Reservation Detail, Timeline & Readiness: *Reservation Detail, Timeline & Readiness*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental booking list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental booking untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental booking yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental booking are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-544`: Same booking statuses and words as the check-out board.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
booking: RNT-10466 · Aisha Rahman · 2 × City Bicycle · Beach Hut · 14:00–16:00 · Awaiting arrival
```

#### Permissions

- `listRentalBookings` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Bookings made by staff at the rental station or by the customer online use the same flow; booking dashboard shows total reservations, upcoming rentals, items awaiting arrival (online bookings not yet collected) and checked-out items. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-754)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-534` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS120 Rental Management Board 5.dc.html#bo-534`
- Workshop pack: Rental_Management.pdf board 5
- Flow F201 *Rental Management board 5: Rental Booking Command Center*, step 1: Opens Rental Booking Command Center → Provide a single operational view of all rental reservations across venues and locations.
- Flow F201 *Rental Management board 5: Rental Booking Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F201 *Rental Management board 5: Rental Booking Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F201 *Rental Management board 5: Rental Booking Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F201 *Rental Management board 5: Rental Booking Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F201 *Rental Management board 5: Rental Booking Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F201 *Rental Management board 5: Rental Booking Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F201 *Rental Management board 5: Rental Booking Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F201 branch at step 1 (expected): when Nothing has been set up on Rental Booking Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F201 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-534?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-535`, `BO-536`, `BO-537`, `BO-538`, `BO-539`, `BO-540`, `BO-541`, `BO-542`, `BO-543`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-535` New Rental Booking Wizard

**Allow POS/rental operators to create a reservation through a guided workflow.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_BOOK`, `RENTAL_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/new-rental-booking-wizard-bo-535` |

**Known gaps.** **New Rental Booking Wizard declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write …

**From the Food, Beverage & Retail process.** Create a rental booking at the station or the desk; the same steps as the online booking. The one thing to get right: price and deposit quoted live as product, time and quantity change.

**Known correction pending (do not draw the wrong version)**

- **Venue as a field.** Why: The venue is the signed-in scope. *(source: screens/P08-venue-back-office.yaml#BO-535; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue | select field | — | — | — | — | — | — |
| Rental Location | select field | — | — | — | — | — | — |
| Rental Product | select field | — | — | — | — | — | — |
| Quantity | select field | — | — | — | — | — | — |
| Rental Date | select field | — | — | — | — | — | — |
| Start Time | select field | — | — | — | — | — | — |
| Duration | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Booking**: Station, product, quantity, date, start, duration; quote updates live. *(source: DI-754 / contracts/satellite/rental.yaml#quoteRentalPrice / contracts/satellite/rental.yaml#createRentalBooking)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-534` Rental Booking Command Center: *Back to Rental Booking Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The new rental booking configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the new rental booking untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No new rental booking configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not available for that window, quantity or location; 422 `quoteExpired` or `quoteMismatch`: the `acceptedQuoteId` has expired or was given for a different product, location, window or quantity. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
booking: Beach Hut · City Bicycle × 2 · 15 Nov · 14:00 · 2 h → AED 140 + deposit AED 400 held
```

#### Permissions

- `createRentalBooking` → `RENTAL_BOOK` (operate) · staff, guest
- `quoteRentalPrice` → `RENTAL_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Bookings made by staff at the rental station or by the customer online use the same flow; booking dashboard shows total reservations, upcoming rentals, items awaiting arrival (online bookings not yet collected) and checked-out items. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-754)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-535` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS120 Rental Management Board 5.dc.html#bo-535`
- Workshop pack: Rental_Management.pdf board 5
- Flow F201 *Rental Management board 5: Rental Booking Command Center*, step 2: Works in New Rental Booking Wizard → Allow POS/rental operators to create a reservation through a guided workflow.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-535?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-534`.
- [ ] Every gated control is gated: `RENTAL_BOOK`, `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-536` Availability Selection & Alternative Options

**Give the operator/customer a clear booking choice based on Board 3 availability.**

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
| Route | `/rentals/availability-selection-alternative-options-bo-536` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Pick a start time and duration from live availability, with alternatives when the request cannot be met.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Rental product | select field | — | — | — | — | Sends `?productId=` (required). | — |
| Rental location | select field | — | — | — | — | Sends `?locationId=`. | — |
| Rental date and start | date picker | — | — | — | — | Sends `?from=` and `?to=`. | — |
| Quantity | number field | — | — | — | — | Sends `?quantity=`. | — |

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

**Start times by duration** (data table, from `getRentalAvailability`): The pack draws a start-time by duration grid (60 / 90 / 120 min); each duration column is one read with a different `to`. Zero shows Sold Out.

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| Available quantity | 1,234 | — |

**Alternatives when the request cannot be met** (detail panel, from `getRentalAvailability`): Later start times are bound; other locations and the AI note ("Marina B is about 5 minutes away") are not.

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026, 14:30 | — |
| Available quantity | 1,234 | — |
| Alternative location | text | not in the schema: `Alternative location` |
| Distance from requested location | text | not in the schema: `Distance from requested location` |
| AI recommendation | text | not in the schema: `AI recommendation` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Select this slot (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Start times**: Grid of start times by duration with units left; alternatives (other time, other station, similar product). *(source: contracts/satellite/rental.yaml#getRentalAvailability)*

**Data it reads**: `getRentalAvailability` (onLoad, Alternatives when the first choice is gone)

**Where the user goes next**

- → `BO-534` Rental Booking Command Center: *Back to Rental Booking Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The availability selection alternative list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the availability selection alternative untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No availability selection alternative yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the availability selection alternative are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
alternatives: 14:00 full · 14:30 (3 left) · Marina Gate 14:00 (6 left)
```

#### Permissions

- `getRentalAvailability` → `RENTAL_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-536` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS120 Rental Management Board 5.dc.html#bo-536`
- Workshop pack: Rental_Management.pdf board 5
- Flow F201 *Rental Management board 5: Rental Booking Command Center*, step 4: Works in Availability Selection & Alternative Options → Give the operator/customer a clear booking choice based on Board 3 availability.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state.
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-536?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Select this slot.
- [ ] Every transition is wired: `BO-534`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-537` Customer & Participant Information

**Capture the configurable customer information required by the rental product. The original requirements specifically support configurable mandatory fields such as name, mobile, email, nationality, ID number and date of birth.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_BOOK` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/customer-participant-information-bo-537` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Capture the customer and participant details the product requires (from BO-502). The one thing to get right: only the fields this product requires are shown, required ones marked.

**Known correction pending (do not draw the wrong version)**

- **Layout is only Save and Cancel.** Why: Nothing to draw. *(source: screens/P08-venue-back-office.yaml#BO-537; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Customer**: Fields per the product's requirements; ID collected and returned with the item where required. *(source: DI-742 / contracts/satellite/rental.yaml#updateRentalBooking)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save rental booking (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-534` Rental Booking Command Center: *Back to Rental Booking Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer participant information list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer participant information untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer participant information yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer participant information are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
customer: Fatima Al Suwaidi · +971 55 220 8813 · Emirates ID 784-1990-•••••••-1
```

#### Permissions

- `updateRentalBooking` → `RENTAL_BOOK` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group rental (e.g. 10 people on bicycles): capture each member's details and assign an item to each, tracked as one linked group booking, with a group waiver all members sign. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-755)*
- Eligibility rules: required documentation (e.g. Emirates ID collected and returned with the item), age restrictions, and which customer-profile fields must be captured at rental time. *(client request · MoM 9 Sep 2026, 4.2 Rental Location, Duration & Eligibility Rules · DI-742)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-537` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS120 Rental Management Board 5.dc.html#bo-537`
- Workshop pack: Rental_Management.pdf board 5
- Flow F201 *Rental Management board 5: Rental Booking Command Center*, step 6: Works in Customer & Participant Information → Capture the configurable customer information required by the rental product. The original requirements specifically support configurable mandatory fields such as name, mobile, email, nationality, ID …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-537?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save rental booking, Cancel.
- [ ] Every transition is wired: `BO-534`.
- [ ] Every gated control is gated: `RENTAL_BOOK`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-538` Group Rental & Participant Management

**Handle reservations involving multiple participants. The source explicitly requires group reservations, participant demographics and configurable participant forms.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_BOOK` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/group-rental-participant-management-bo-538` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Group rentals (10 people on bicycles): each member's details, an item per member, one linked group booking, a group waiver all sign. The one thing to get right: a participant table with each member's unit and waiver state.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Participants**: Add one by one or bulk upload; copy the primary contact; guardian for minors. *(source: DI-755 / contracts/satellite/rental.yaml#createRentalBooking)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add participant (primary button) | navigation or local | — | — | — | — |
| Bulk upload participants (secondary button) | navigation or local | — | — | — | — |
| Copy primary contact (secondary button) | navigation or local | — | — | — | — |
| Guardian information (secondary button) | navigation or local | — | — | — | — |
| Group waiver where allowed (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-534` Rental Booking Command Center: *Back to Rental Booking Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group rental participant list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group rental participant untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group rental participant yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group rental participant are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not available for that window, quantity or location; 422 `quoteExpired` or `quoteMismatch`: the `acceptedQuoteId` has expired or was given for a different product, location, window or quantity. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
group: Al Mansoori family · 6 bicycles · 6 participants · waiver signed 4/6
```

#### Permissions

- `createRentalBooking` → `RENTAL_BOOK` (operate) · staff, guest
- `signRentalAgreement` → `RENTAL_BOOK` (operate) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group rental (e.g. 10 people on bicycles): capture each member's details and assign an item to each, tracked as one linked group booking, with a group waiver all members sign. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-755)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-538` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS120 Rental Management Board 5.dc.html#bo-538`
- Workshop pack: Rental_Management.pdf board 5
- Flow F201 *Rental Management board 5: Rental Booking Command Center*, step 8: Works in Group Rental & Participant Management → Handle reservations involving multiple participants. The source explicitly requires group reservations, participant demographics and configurable participant forms.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-538?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add participant, Bulk upload participants, Copy primary contact, Guardian information, Group waiver where allowed.
- [ ] Every transition is wired: `BO-534`.
- [ ] Every gated control is gated: `RENTAL_BOOK`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-539` Rental Agreement & Waiver Completion

**Complete all mandatory customer acknowledgments before confirmation or checkout. This implements the digital rental agreement/waiver capability recommended in the source.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_BOOK` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/rental-agreement-waiver-completion-bo-539` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Food, Beverage & Retail process.** Complete the agreement and waiver before confirmation or check-out, against the version in force, individually or as a group. The one thing to get right: who has signed and who has not.

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which signature device is used for group waivers?** → Drawn default accepted: On-screen signature on the tablet. *(decided by Chinmay, 2026-10-02; DEC-300 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Signature**: Per participant or group; recorded against the agreement version. *(source: DI-755 / contracts/satellite/rental.yaml#signRentalAgreement)*

#### Outputs: what the screen shows and produces

**Shown**

**Every rental agreement waiver** (data table)

| Shows | Format | Notes |
|---|---|---|
| Rental terms | text | not in the schema: `Rental Terms` |
| Liability terms | text | not in the schema: `Liability Terms` |
| Safety conditions | text | not in the schema: `Safety Conditions` |
| Damage responsibility | text | not in the schema: `Damage Responsibility` |
| Late return policy | text | not in the schema: `Late Return Policy` |
| Deposit policy | text | not in the schema: `Deposit Policy` |
| Cancellation policy | text | not in the schema: `Cancellation Policy` |

**The selected rental agreement waiver** (detail panel): The pack groups this record's detail under its own headings: “Agreement”, “Completion Methods”, “Customer Signature”.

| Shows | Format | Notes |
|---|---|---|
| Rental terms | text | not in the schema: `Rental Terms` |
| Liability terms | text | not in the schema: `Liability Terms` |
| Safety conditions | text | not in the schema: `Safety Conditions` |
| Damage responsibility | text | not in the schema: `Damage Responsibility` |
| Late return policy | text | not in the schema: `Late Return Policy` |
| Deposit policy | text | not in the schema: `Deposit Policy` |
| Cancellation policy | text | not in the schema: `Cancellation Policy` |

**Where the user goes next**

- → `BO-534` Rental Booking Command Center: *Back to Rental Booking Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental agreement waiver list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental agreement waiver untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental agreement waiver yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental agreement waiver are still there. The pack's own statuses are ✓ Rental Agreement — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
waiver: Waiver v2.1 · signed by Khalid Al Mansoori 13:52 · 2 participants pending
```

#### Permissions

- `signRentalAgreement` → `RENTAL_BOOK` (operate) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Group waivers need a digital signature-capture device (stylus pad); Chinmay says a USB signature pad should integrate. Hardware reference pending from Qossai. *(open · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-756)*
- Group rental (e.g. 10 people on bicycles): capture each member's details and assign an item to each, tracked as one linked group booking, with a group waiver all members sign. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-755)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-539` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS120 Rental Management Board 5.dc.html#bo-539`
- Workshop pack: Rental_Management.pdf board 5
- Flow F201 *Rental Management board 5: Rental Booking Command Center*, step 10: Works in Rental Agreement & Waiver Completion → Complete all mandatory customer acknowledgments before confirmation or checkout. This implements the digital rental agreement/waiver capability recommended in the source.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-539?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-534`.
- [ ] Every gated control is gated: `RENTAL_BOOK`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-540` Booking Commercial Summary & Payment

**Show the complete financial commitment before confirming the reservation.**

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
| Route | `/rentals/booking-commercial-summary-payment-bo-540` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** The full financial commitment before payment: rental price, extras, deposit (held, not charged), taxes, total. The one thing to get right: rental price and deposit are separate blocks, never summed.

**Known correction pending (do not draw the wrong version)**

- **No payment operation is attached; the primary button has no label.** Why: The screen is titled "& Payment". *(source: screens/P08-venue-back-office.yaml#BO-540; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Summary**: Charges, deposit with method and release rule, VAT, total to pay now. *(source: DI-757 / contracts/satellite/rental.yaml#quoteRentalPrice)*

**Data it reads**: `quoteRentalPrice` (onLoad, Rental amount and deposit, apart)

**Where the user goes next**

- → `BO-534` Rental Booking Command Center: *Back to Rental Booking Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The booking commercial summary list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the booking commercial summary untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No booking commercial summary yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the booking commercial summary are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
summary: 2 × City Bicycle 2 h AED 140.00 · VAT AED 7.00 · pay now AED 147.00 · deposit AED 400.00 held on card
```

#### Permissions

- `quoteRentalPrice` → `RENTAL_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Commercial summary shows all charges (including deposit) before payment; once paid the booking is confirmed with a QR code sent by email or other channel; bookings can be amended; reservation timeline shows products, timing, amounts paid and deposit status. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-757)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-540` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS120 Rental Management Board 5.dc.html#bo-540`
- Workshop pack: Rental_Management.pdf board 5
- Flow F201 *Rental Management board 5: Rental Booking Command Center*, step 12: Works in Booking Commercial Summary & Payment → Show the complete financial commitment before confirming the reservation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-540?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-534`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-541` Reservation Confirmation & QR Voucher

**Create the confirmed rental reservation and customer credential. The original voucher flow specifically requires the system to generate a voucher/ticket that is later redeemed at the rental counter.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/reservation-confirmation-qr-voucher-bo-541` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Confirmation of the paid booking and the QR voucher sent by email or another channel, redeemed later at the station.

**Known correction pending (do not draw the wrong version)**

- **No operation sends the voucher.** Why: DI-757 requires sending the QR by email or another channel. *(source: DI-757 / screens/P08-venue-back-office.yaml#BO-541; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Voucher**: QR, reference, product, station, time, what to bring (ID), deposit note; resend option. *(source: DI-757 / contracts/satellite/rental.yaml#getRentalBooking)*

**Where the user goes next**

- → `BO-534` Rental Booking Command Center: *Back to Rental Booking Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reservation confirmation voucher list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reservation confirmation voucher untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reservation confirmation voucher yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reservation confirmation voucher are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
voucher: RNT-10466 · QR · Beach Hut · 15 Nov 14:00 · bring Emirates ID
```

#### Permissions

- `getRentalBooking` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Commercial summary shows all charges (including deposit) before payment; once paid the booking is confirmed with a QR code sent by email or other channel; bookings can be amended; reservation timeline shows products, timing, amounts paid and deposit status. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-757)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-541` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS120 Rental Management Board 5.dc.html#bo-541`
- Workshop pack: Rental_Management.pdf board 5
- Flow F201 *Rental Management board 5: Rental Booking Command Center*, step 14: Works in Reservation Confirmation & QR Voucher → Create the confirmed rental reservation and customer credential. The original voucher flow specifically requires the system to generate a voucher/ticket that is later redeemed at the rental counter.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-541?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-534`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-542` Reservation Modification, Cancellation & No-Show

**Manage the reservation after confirmation but before/during fulfillment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_BOOK` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/reservation-modification-cancellation-no-show-bo-542` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-008): Modifying is updateRentalBooking; a second booking (createRentalBooking) is not a change (R254; design-notes correction fnb-retail BO-542).

**From the Food, Beverage & Retail process.** Change, cancel or mark a no-show on a confirmed booking: quantity, product, time; the price difference shown before saving. The one thing to get right: the effect on price and deposit is shown before saving.

**Fixed on main** (the package already carries these; draw what it says): createRentalBooking attached to a modification screen. (CHG-WIR-008).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every reservation modification cancellation** (data table)

| Shows | Format | Notes |
|---|---|---|
| Cancellation policy | text | not in the schema: `Cancellation policy` |
| Refund amount | text | not in the schema: `Refund amount` |
| Deposit release | text | not in the schema: `Deposit release` |
| Cancellation fee | text | not in the schema: `Cancellation fee` |
| Inventory released | text | not in the schema: `Inventory released` |

**The selected reservation modification cancellation** (detail panel): The pack groups this record's detail under its own headings: “Original”, “Requested”, “Availability”, “Difference”, “No-Show”, “Expected arrival”.

| Shows | Format | Notes |
|---|---|---|
| Cancellation policy | text | not in the schema: `Cancellation policy` |
| Refund amount | text | not in the schema: `Refund amount` |
| Deposit release | text | not in the schema: `Deposit release` |
| Cancellation fee | text | not in the schema: `Cancellation fee` |
| Inventory released | text | not in the schema: `Inventory released` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Quantity (primary button) | navigation or local | — | — | — | — |
| Product (secondary button) | navigation or local | — | — | — | — |

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Modify · Cancel · Mark no-show**: Updates the booking; cancellation shows the refund under the policy. *(source: contracts/satellite/rental.yaml#updateRentalBooking)*

**Where the user goes next**

- → `BO-534` Rental Booking Command Center: *Back to Rental Booking Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reservation modification cancellation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reservation modification cancellation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reservation modification cancellation yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reservation modification cancellation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
change: RNT-10466 · 2 → 3 bicycles · +AED 70.00 · deposit +AED 200
```

#### Permissions

- `updateRentalBooking` → `RENTAL_BOOK` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Commercial summary shows all charges (including deposit) before payment; once paid the booking is confirmed with a QR code sent by email or other channel; bookings can be amended; reservation timeline shows products, timing, amounts paid and deposit status. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-757)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-542` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS120 Rental Management Board 5.dc.html#bo-542`
- Workshop pack: Rental_Management.pdf board 5
- Flow F201 *Rental Management board 5: Rental Booking Command Center*, step 16: Works in Reservation Modification, Cancellation & No-Show → Manage the reservation after confirmation but before/during fulfillment.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-542?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Quantity, Product.
- [ ] Every transition is wired: `BO-534`.
- [ ] Every gated control is gated: `RENTAL_BOOK`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-543` Reservation Detail, Timeline & Readiness

**Provide the complete operational record before handing the reservation to Board 6 for checkout.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select/Scan BIKE-028; Select Product; Capture Customer) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/reservation-detail-timeline-readiness-bo-543` |

**From the Food, Beverage & Retail process.** One booking's full record before check-out: products, timing, amounts paid, deposit status, readiness, timeline.

**Known correction pending (do not draw the wrong version)**

- **Labels "Check Availability — Board 3", "Calculate Price & Deposit — Board 4" and an arrow select.** Why: Pack diagram text used as fields. *(source: screens/P08-venue-back-office.yaml#BO-543; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ↓ | select field | — | — | — | — | — | — |
| Check Availability — Board 3 | text field | — | — | — | — | — | — |
| Calculate Price & Deposit — Board 4 | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Readiness**: Payment, agreement, customer details, inventory — each ready or what is missing. *(source: DI-757 / contracts/satellite/rental.yaml#getRentalBooking)*

**Where the user goes next**

- → `BO-534` Rental Booking Command Center: *Back to Rental Booking Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reservation detail timeline configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reservation detail timeline untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reservation detail timeline configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
readiness: Paid ✓ · Waiver ✓ · ID pending · 2 bicycles available
```

#### Permissions

- `getRentalBooking` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Commercial summary shows all charges (including deposit) before payment; once paid the booking is confirmed with a QR code sent by email or other channel; bookings can be amended; reservation timeline shows products, timing, amounts paid and deposit status. *(client request · MoM 9 Sep 2026, 4.6 Rental Booking, Reservation & Group Management · DI-757)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-543` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS120 Rental Management Board 5.dc.html#bo-543`
- Workshop pack: Rental_Management.pdf board 5
- Flow F201 *Rental Management board 5: Rental Booking Command Center*, step 18: Works in Reservation Detail, Timeline & Readiness → Provide the complete operational record before handing the reservation to Board 6 for checkout.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-543?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-534`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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
"createRentalBooking": {"method":"POST","path":"/rental-bookings","contract":"rental","summary":"Reserve a rental","permission":"RENTAL_BOOK","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalBookingRequest","responds":"RentalBooking"},
"getRentalAvailability": {"method":"GET","path":"/rental-availability","contract":"rental","summary":"What can be rented, when, with turnaround already subtracted","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":true},{"name":"locationId","in":"query","required":null},{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"quantity","in":"query","required":null}],"requestBody":null,"responds":"RentalAvailability"},
"getRentalBooking": {"method":"GET","path":"/rental-bookings/{bookingId}","contract":"rental","summary":"One booking, its timeline and its readiness","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RentalBooking"},
"listRentalBookings": {"method":"GET","path":"/rental-bookings","contract":"rental","summary":"Reservations across venues and locations","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"locationId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"RentalBooking"},
"quoteRentalPrice": {"method":"POST","path":"/rental-price","contract":"rental","summary":"What this rental would cost, and the deposit it would hold","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalQuoteRequest","responds":"RentalQuote"},
"signRentalAgreement": {"method":"POST","path":"/rental-bookings/{bookingId}/agreement","contract":"rental","summary":"Capture the signature, against a version","permission":"RENTAL_BOOK","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalAgreementSignature","responds":"RentalAgreementSignature"},
"updateRentalBooking": {"method":"PATCH","path":"/rental-bookings/{bookingId}","contract":"rental","summary":"Modify, cancel or mark a no-show","permission":"RENTAL_BOOK","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RentalBooking"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"RentalAgreementSignature": {"type":"object","x-ticvai-persistence":"rental.agreement_signature","description":"Boards 1.9 and 5.6. **The version signed travels with the signature.**","required":["agreementVersion"],"properties":{"id":{"type":"string","format":"uuid"},"participantId":{"type":"string","format":"uuid","nullable":true},"agreementVersion":{"type":"string"},"signatoryName":{"type":"string"},"signatoryRole":{"type":"string","enum":["renter","participant","guardian"]},"signatureAssetId":{"type":"string","format":"uuid","nullable":true},"documentAssetId":{"type":"string","format":"uuid","nullable":true},"signedAt":{"type":"string","format":"date-time"},"ipAddress":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"RentalAvailability": {"type":"object","description":"Board 3. **A pooled product answers with a count, a serialised one with assets.**","properties":{"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid","nullable":true},"windows":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"availableQuantity":{"type":"integer"},"availableAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"blockedWindows":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"reason":{"type":"string","enum":["booked","turnaround","maintenance","blackout","closed","buffer","held"]}}}}}},
"RentalBooking": {"type":"object","x-ticvai-persistence":"rental.booking","description":"Board 5. **The booking outlives the order** — an order completes at payment and the rental is still out.\n","required":["id","productId","from","to","status"],"properties":{"id":{"type":"string","format":"uuid"},"reference":{"type":"string"},"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"returnLocationId":{"type":"string","format":"uuid","nullable":true},"customerId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer"},"status":{"type":"string","enum":["draft","confirmed","awaitingArrival","checkedOut","overdue","partiallyReturned","completed","completedWithDamage","notReturned","cancelled","noShow"]},"checkedOutAt":{"type":"string","format":"date-time","nullable":true},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"returnedAt":{"type":"string","format":"date-time","nullable":true},"depositAuthorisationId":{"type":"string","format":"uuid","nullable":true,"description":"The card deposit's terminal pre-authorisation, written by `checkOutRental` (workbook Q304; CHG-CSA-029). The hold is kept whole until every unit is back (workbook Q306)."},"accruedLateFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"readiness":{"type":"array","readOnly":true,"description":"**Computed, not stored** — agreement, requirements, deposit, equipment.","items":{"type":"object","properties":{"check":{"type":"string"},"satisfied":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"participants":{"type":"array","items":{"$ref":"#/components/schemas/RentalParticipant"}},"scopePath":{"type":"string"}}},
"RentalBookingRequest": {"type":"object","required":["productId","from","to"],"properties":{"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"returnLocationId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer","default":1},"customerId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"participants":{"type":"array","items":{"$ref":"#/components/schemas/RentalParticipant"}},"acceptedQuoteId":{"type":"string","format":"uuid","nullable":true,"description":"A `rental.quote` id from `quoteRentalPrice`. **The booking is priced at the quote's `rentalAmount` and `depositAmount`** while the quote is unexpired and its product, location, window and quantity match the request; an expired or mismatched quote is `422` (`quoteExpired`, `quoteMismatch`) rather than silently repriced. Without it the booking is priced now (decided 29 September, writers pass; DM4)."}}},
"RentalParticipant": {"type":"object","x-ticvai-persistence":"rental.participant","description":"Board 5.5. **A group rental is one booking with participants**, because the agreement, the deposit and the return are handled together.\n","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"isPrimaryRenter":{"type":"boolean","default":false},"dateOfBirth":{"type":"string","format":"date","nullable":true},"idNumber":{"type":"string","nullable":true},"guardianName":{"type":"string","nullable":true},"emergencyContact":{"type":"string","nullable":true},"hasSignedWaiver":{"type":"boolean","readOnly":true},"customFields":{"type":"object","additionalProperties":true}}},
"RentalQuote": {"type":"object","x-ticvai-persistence":"rental.quote","description":"Board 4.10. **Rental amount and deposit are returned apart, because the deposit is not revenue.**\n**A quote `quoteRentalPrice` issues is stored until `expiresAt`**, with what was asked, so the figures it gave can be held to and checked later. `explainRentalPrice` and `simulateRentalPricing` return the same shape and store nothing (decided 29 September, data model DM4).\n**Consumed by `acceptedQuoteId`** on `createRentalBooking` and the extension. A quote is not deleted when it is used or expires: a nightly job removes quotes 30 days past `expiresAt` that no booking references, so a booking can always show the quote it was priced at (decided 29 September, writers pass; DM4).\n","required":["quoteId","productId","from","to","rentalAmount","depositAmount"],"properties":{"quoteId":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid","description":"The request's product; with `locationId`, `from`, `to` and `quantity`, what was quoted."},"locationId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer","default":1},"customerId":{"type":"string","format":"uuid","nullable":true},"rentalAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"addOnAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalPayable":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"depositInstrument":{"type":"string","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005), written at `venue` scope."}}},
"RentalQuoteRequest": {"type":"object","required":["productId","from","to"],"properties":{"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer","default":1},"salesChannel":{"type":"string","nullable":true},"customerId":{"type":"string","format":"uuid","nullable":true},"promotionCode":{"type":"string","nullable":true}}}
}
```
