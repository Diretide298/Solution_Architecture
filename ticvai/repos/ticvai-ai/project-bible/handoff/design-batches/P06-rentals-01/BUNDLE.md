# P06-rentals-01 — P06 · Rentals (1 of 3)

**10 screens · 7 operations · 11 schemas · 3 permissions**

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
| `EMP-071` | Rental Checkout Command Center | C | 2 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `EMP-072` | Voucher Scan & Reservation Retrieval | C | 0 | 0 | 6 | 0 | 1 | 2 | — | notStarted (generated) |
| `EMP-073` | Checkout Readiness Validation | C | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `EMP-074` | Equipment Assignment Workspace | C | 0 | 11 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `EMP-075` | Equipment Scan & Validation | C | 1 | 0 | 6 | 3 | 1 | 0 | — | notStarted (generated) |
| `EMP-076` | Pre-Rental Condition Inspection | C | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `EMP-077` | Safety & Handover Checklist | C | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `EMP-078` | Deposit & Financial Handover Validation | C | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `EMP-079` | Group & Multi-Item Checkout | C | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `EMP-080` | Checkout Confirmation & Rental Activation | C | 2 | 0 | 6 | 0 | 0 | 6 | — | notStarted (generated) |

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
| Block | Block C · task APP-STAFF-EMP-071 |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | commandCentre (comfortable density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/rental-checkout-command-center-emp-071` |

**What the spec says about it.** The staff-app form of `BO-544`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**From the Food, Beverage & Retail process.** The rental attendant's start point at the counter (Kayak station, Beach Hut, Bike hub): who is arriving for a rental and what each booking still lacks before the equipment can go out. It must be a working queue of today's bookings with a big "Scan voucher" action (DI-758), not eight KPI tiles over nothing. The one thing to get right is that each row shows its readiness at a glance, so the attendant fetches a signature or a supervisor before the guest reaches the counter, not after.

**Known correction pending (do not draw the wrong version)**

- **The thirty staff-app screens EMP-071..EMP-100 are field-for-field copies of BO-544..BO-573 (same operations, layout, states, gaps and entry parameters; only id, route, density and navigation differ). Pairs: EMP-071/BO-544, EMP-072/BO-545, EMP-073/BO-546, EMP-074/BO-547, EMP-075/BO-548 …** Why: DI-671 asks to minimise separate screens rather than mirror every workshop board; DI-474 and DI-987 ask the same for back-office screens. Duplicated definitions will drift and double the design and build work. *(source: screens/P06-staff-app.yaml#EMP-071 / DI-671 / DI-474 / DI-987; Food, Beverage & Retail)*
- **Board 6 is ten screens for one act at the counter. Consolidate to two per platform: (1) Check-out queue (EMP-071, with EMP-072's scan as its main action) and (2) Check-out for one booking, a stepped flow Readiness (EMP-073) -> Equipment (EMP-074 + EMP-075 + EMP-079, one screen with one row per …** Why: checkOutRental is consumed by three screens (EMP-077, EMP-078, EMP-080) each with its own submit button, and assignRentalEquipment by three (EMP-074, EMP-075, EMP-079). A handover is one act; three submit buttons for it means the handover can be "completed" from the safety screen with no deposit step seen. DI-760 asks for a group's items to go out in a single action. *(source: contracts/satellite/rental.yaml#checkOutRental / contracts/satellite/rental.yaml#assignRentalEquipment / DI-671 / DI-760; Food, Beverage & Retail)*
- **Labels use "Checkout" for the rental handover: screen names (Rental Checkout Command Center, Checkout Readiness Validation, Group & Multi-Item Checkout, Checkout Confirmation & Rental Activation) and tiles (Awaiting Checkout, Ready for Checkout, Checkout in Progress). Use "Check-out" for the …** Why: The process vocabulary keeps the rental handover distinct from payment on the same screens. *(source: designer default / MoM 2026-09-09 4.7; Food, Beverage & Retail)*
- **Tiles "Checkout in Progress" and "Equipment Issues" have no data behind them.** Why: RentalBooking.status goes from awaitingArrival straight to checkedOut (no in-progress state) and no booking field records an equipment issue before handover. Drop both, or add a status the contract can count. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalBooking; Food, Beverage & Retail)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What does the handheld do offline at the rental counter? All 30 staff-app rental screens have the offline state as TODO. check-out, equipment assignment, inspection, return and incident are offline-capable in the contract, but the reads they depend on (the booking list and one booking) are not, and …** → Drawn default stands (answer: "Offline: check-out of bookings already loaded, with a cash deposit or supervisor approval; returns queue"): Draw an offline banner; allow check-out only for a booking already loaded, with a cash deposit or a supervisor override; queue the call and show "Will sync". Returns may be recorded offline with the statement marked "Settles when back online". *(decided by Chinmay, 2026-10-02; DEC-302 / CHG-NOTE-004)*
- **How long does an uncollected booking hold its equipment before it becomes a no-show? R169 sets hold lengths for seats, carts and merchandise but none for a rental.** → Drawn default accepted: Show "Late arrival +N min" in amber from the booked start; offer "Mark no-show" only to a supervisor (it goes through the booking modification screen BO-542). *(decided by Chinmay, 2026-10-02; DEC-303 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search rental checkout | search field | — | — | — | — | — | — |
| Filter by | text field | optional | — | — | — | Sends `?status=` to `listRentalBookings` (the booking status; location goes as `locationId`) (CHG-RFM-012). The pack filters this screen by location, product, start time, booking type … | `listRentalBookings` ?status |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Location | picker: choose a location | — | — | `listRentalBookings` ?locationId |
| From | date and time picker | — | — | `listRentalBookings` ?from |
| To | date and time picker | — | — | `listRentalBookings` ?to |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Scan voucher / Search**: Primary entry is the camera scan of the booking QR the guest received on confirmation (DI-757, DI-758); the search box takes the booking reference or the guest's name or mobile. A scan that matches opens the check-out for that booking directly (EMP-072 is not a separate stop on the handheld; see the consolidation correction). *(source: DI-758 / DI-757 / MoM 2026-09-09 4.7)*
- **Filters**: Keep Location (defaults to the attendant's own station), Product, Start time window, Group/Individual and Readiness. Drop "Venue" on the handheld: a staff session is already scoped to one venue. Status is a chip row (Awaiting arrival · Late arrival · Checked out today), not a multi-select. *(source: contracts/satellite/rental.yaml#listRentalBookings / screens/P06-staff-app.yaml#EMP-071)*

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

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Booking row**: Reference, guest name, product x quantity (e.g. "Single kayak x2"), booked window in GST, location, group badge when the booking has more than one participant, and a readiness strip of four dots (Agreement · Requirements · Deposit · Equipment) from the computed readiness array, each green or amber. Sort by start time ascending; late arrivals pinned to the top in amber. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalBooking / DI-758)*
- **Counters above the queue**: Only counters the data can produce: Arriving next 30 min (awaitingArrival, from within 30 min), Ready for check-out (awaitingArrival with every readiness item satisfied), Missing requirements (any readiness item unsatisfied), Late arrivals (awaitingArrival, from in the past), Checked out today (checkedOut, checkedOutAt today). Each counter is a tap-to-filter chip, not a dashboard card. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalBooking / DI-758)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Scan voucher**: Opens the camera; a recognised booking opens its check-out at the first unsatisfied step. Unknown code: "No rental booking found for this code" with Search as the fallback. A booking for another location: show it with "Booked at Beach Hut" and let the attendant continue (no silent refusal). *(source: DI-758 / contracts/satellite/rental.yaml#getRentalBooking)*
- **Tap a row**: Opens the check-out for that booking (readiness first). *(source: F202 step 2)*

**Data it reads**: `listRentalBookings` (onLoad, Awaiting arrival)

**Where the user goes next**

- → `EMP-003` Home — on duty: *Back to Home — on duty*
- → `EMP-072` Voucher Scan & Reservation Retrieval: *Voucher Scan & Reservation Retrieval*; carries `bookingId`
- → `EMP-073` Checkout Readiness Validation: *Checkout Readiness Validation*; carries `bookingId`
- → `EMP-074` Equipment Assignment Workspace: *Equipment Assignment Workspace*; carries `bookingId`
- → `EMP-075` Equipment Scan & Validation: *Equipment Scan & Validation*; carries `bookingId`
- → `EMP-076` Pre-Rental Condition Inspection: *Pre-Rental Condition Inspection*; carries `bookingId`
- → `EMP-077` Safety & Handover Checklist: *Safety & Handover Checklist*; carries `bookingId`
- → `EMP-078` Deposit & Financial Handover Validation: *Deposit & Financial Handover Validation*; carries `bookingId`
- → `EMP-079` Group & Multi-Item Checkout: *Group & Multi-Item Checkout*; carries `bookingId`
- → `EMP-080` Checkout Confirmation & Rental Activation: *Checkout Confirmation & Rental Activation*; carries `bookingId`

#### States

| State | What it shows |
|---|---|
| Empty, first run (`?state=emptyFirstRun`) | No rental checkout yet. Carries the create action; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental checkout are still there. Names the active filter and offers to clear it. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental checkout untouched. |
| Loading (`?state=loading`) | The rental checkout list; the counts above it resolve separately. |
| Offline (`?state=offline`) | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |

#### Edge cases to draw

- **Guest arrives with a booking that was cancelled or marked no-show**: Row shows the status in grey with no check-out action; the attendant is told to sell a new rental instead. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalBooking / contracts/satellite/rental.yaml#updateRentalBooking)*
- **Device offline**: Banner "Offline - showing the queue as of 10:42", rows loaded before the drop stay openable, scan of an unloaded booking says it cannot be found offline. *(source: DI-071 / DI-072 / screens/P06-staff-app.yaml#EMP-071)*

#### Consistency with other screens

- Match `BO-544`: Same queue, same row anatomy and counters; the desk version adds the Venue filter and denser rows.
- Match `BO-534`: The booking board counts the same statuses (awaiting arrival, checked out); use the same status labels and colours.
- Match `EMP-081`: Same row component as the active-rentals list, with the readiness strip replaced by the due-back time.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
station: Kayak station, Aqua Park Marina
date: Sat 17 Oct 2026
counters:
  arrivingNext30Min: 6
  readyForCheckOut: 4
  missingRequirements: 3
  lateArrivals: 1
  checkedOutToday: 27
rows:
- reference: RNT-10482
  guest: Aisha Rahman
  product: Single kayak x2
  window: 10:00-11:00
  readiness:
  - agreement ok
  - requirements ok
  - deposit missing
  - equipment ok
- reference: RNT-10487
  guest: Khalid Al Mansoori (school group
  10 participants): null
  product: Mountain bike M x10
  window: 10:15-12:15
  readiness:
  - agreement 7 of 10 signed
  - requirements ok
  - deposit ok
  - equipment ok
- reference: RNT-10479
  guest: Daniel Brooks
  product: Stand-up paddleboard x1
  window: 09:30-10:30
  status: Late arrival (+14 min)
```

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
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-072` Voucher Scan & Reservation Retrieval

**Quickly identify the customer reservation when they arrive. The original requirement specifically requires scanning and validating the customer's voucher/ticket.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block C · task APP-STAFF-EMP-072 |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/voucher-scan-reservation-retrieval-emp-072` |

**What the spec says about it.** The staff-app form of `BO-545`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Finding the guest's booking from the QR voucher they show. On the handheld this is the scan action of the check-out queue and a result card, not a destination of its own; the card confirms the guest and booking before the attendant starts the handover. Get right: a failed scan must say why (not found, wrong venue, cancelled, already checked out) in one line.

**Known correction pending (do not draw the wrong version)**

- **The scan cannot resolve a booking. The screen's only operation, getRentalBooking, needs the booking id, and the entry state requires bookingId from navigation on the very screen that exists to find it. listRentalBookings has no reference, code or guest search parameter.** Why: DI-758 requires staff to scan a QR code to pull up a reservation. Needs a lookup by voucher code or reference (and by guest name or mobile for search). *(source: contracts/satellite/rental.yaml#getRentalBooking / contracts/satellite/rental.yaml#listRentalBookings / screens/P06-staff-app.yaml#EMP-072 / DI-758; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Scanned code**: Camera scan of the booking QR (DI-757 sends it by email or another channel); manual entry of the reference as fallback. The guest name and mobile search lives on the queue. *(source: DI-757 / DI-758)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Result card**: Guest name, reference, product x quantity, booked window, location, status badge, readiness strip and "Paid AED 240.00 · Deposit AED 600.00 to hold". Primary button "Start check-out"; it is disabled for cancelled, no-show or already checked out, with the reason. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalBooking / DI-757)*

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

#### Edge cases to draw

- **Voucher already used (status checkedOut)**: Card says "Already checked out at 10:04 by Priya Nair" and offers Open rental (EMP-082). *(source: contracts/satellite/rental.yaml#/components/schemas/RentalBooking)*

#### Consistency with other screens

- Match `EMP-092`: The return scan uses the same scanner component and the same not-found wording.
- Match `BO-545`: Shared design; at a desk the scanner is a USB/keyboard-wedge reader feeding the same field.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
scanned: RNT-10482
card:
  guest: Aisha Rahman
  product: Single kayak x2
  window: Sat 17 Oct 2026, 10:00-11:00
  location: Kayak station
  paid: AED 240.00
  deposit: AED 600.00 (2 x 300.00)
```

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
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-073` Checkout Readiness Validation

**Prevent equipment from being handed over until mandatory requirements are satisfied.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block C · task APP-STAFF-EMP-073 |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/checkout-readiness-validation-emp-073` |

**What the spec says about it.** The staff-app form of `BO-546`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Step 1 of the check-out for one booking: what must be true before anything is handed over, with a fix for each failure. Five rows, each green or amber with the action that clears it. The server enforces the same gate at check-out, so this step is a guide, never the only check.

**Known correction pending (do not draw the wrong version)**

- **Readiness items are free strings (readiness[].check), and the contract's set (agreement, requirements, deposit, equipment) omits payment, which DI-759 lists first.** Why: The designer and the build need a fixed list to draw and test; make check an enum including payment/confirmation. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalBooking / DI-759; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Readiness rows**: Booking paid and confirmed (from status) · Agreement signed (for a group, "7 of 10 signed" with the missing names) · Requirements captured (age, ID, guardian, height/weight per the product's rules) · Deposit (amount and method due) · Equipment available. Each amber row names its fix: "Sign agreement", "Capture ID", "Take deposit" (jumps to the deposit step), "Choose another unit". Rules marked "not applicable" for the product are not shown at all; "optional" ones are shown grey and never block. *(source: contracts/satellite/rental.yaml#getRentalBooking / contracts/satellite/rental.yaml#/components/schemas/RentalOperationalRules / DI-759)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Continue to equipment**: Enabled when every required row is green, or when a supervisor override is attached (see the deposit step for who can grant it on the handheld). *(source: contracts/satellite/rental.yaml#/components/schemas/RentalCheckOut)*
- **Sign agreement**: Opens the waiver capture (signRentalAgreement, the BO-539 component); the signature-pad hardware is still open (DI-756). *(source: contracts/satellite/rental.yaml#signRentalAgreement / DI-756)*

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

#### Consistency with other screens

- Match `BO-543`: The back office's reservation detail shows the same readiness rows; one component.
- Match `BO-546`: Shared design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
booking: RNT-10487, Khalid Al Mansoori, Mountain bike M x10
rows:
- check: Booking paid and confirmed
  state: ok
- check: Agreement signed
  state: 7 of 10 - missing Omar Ziad, Fatima Al Suwaidi, Daniel Brooks
- check: 'Requirements: minimum age 12'
  state: ok
- check: Deposit
  state: AED 1,500.00 card hold to take
- check: Equipment
  state: 10 available at Bike hub
```

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
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-074` Equipment Assignment Workspace

**Assign the actual physical equipment to the reservation.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block C · task APP-STAFF-EMP-074 |
| Who uses it | venue staff holding `RENTAL_OPERATE`, `RENTAL_VIEW` (1 operate, 1 read) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/equipment-assignment-workspace-emp-074` |

**What the spec says about it.** The staff-app form of `BO-547`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Step 2: bind the physical units to the booking. One screen for one unit or a group of ten (EMP-074, EMP-075 and EMP-079 are the same job): one row per unit the booking needs, each filled by scanning the unit's tag, or by picking from the available units where the product allows it. Pooled items (towels, life jackets in a hybrid kit) are counted, not scanned.

**Fixed on main** (the package already carries these; draw what it says): The manual pick from available units (DI-760) has no operation behind it on this screen; getRentalAvailability (which returns available … (CHG-WIR-008).

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

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Unit rows**: Number of rows = booking quantity for serialised products. Scan fills the row with the tag and model; "Pick from available" lists only free units for the window (turnaround already subtracted). If the product's check-out scan rule is "required", manual pick is hidden. Substitution with another product is offered only if the product allows it. *(source: contracts/satellite/rental.yaml#assignRentalEquipment / contracts/satellite/rental.yaml#/components/schemas/RentalOperationalRules / DI-760 / DI-740)*
- **Pooled accessories (hybrid kits)**: "Paddle x2, Life jacket x2" shown as counted lines with a stepper; no scan. *(source: contracts/satellite/rental.yaml#setRentalInventoryModel)*

#### Outputs: what the screen shows and produces

**Shown**

**Available units** (detail panel, from `getRentalAvailability`)

| Shows | Format | Notes |
|---|---|---|
| Product | the name it points at, never the id | — |
| Location | the name it points at, never the id | — |
| Windows | list or chips (count when long) | — |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| Available quantity | 1,234 | — |
| Available assets | list or chips (count when long) | — |
| Blocked windows | list or chips (count when long) | — |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| Reason | chip: Booked, Turnaround, Maintenance, Blackout, Closed, Buffer… | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Assign rental equipment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Assigned unit**: Tag, name and last inspection date, e.g. "BIKE-014 · Mountain bike M · inspected 16 Oct". A unit picked manually carries a small "picked, not scanned" mark, because the record keeps that fact. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalEquipmentAssignment)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Continue to condition**: Saves all rows in one assignment call. A refused unit (already out, under maintenance, wrong product) turns its row red with that reason and keeps the others. *(source: contracts/satellite/rental.yaml#assignRentalEquipment)*

**Data it reads**: `getRentalAvailability` (onLoad, Units available to assign)

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

#### Consistency with other screens

- Match `EMP-085`: The swap's "incoming unit" uses this same scan row.
- Match `BO-547`: Shared design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
booking: RNT-10487 (10 x Mountain bike M)
rows:
- BIKE-014 scanned
- BIKE-022 scanned
- BIKE-031 scanned
- BIKE-040 picked
- 6 to assign
```

#### Permissions

- `assignRentalEquipment` → `RENTAL_OPERATE` (operate) · staff
- `getRentalAvailability` → `RENTAL_VIEW` (read) · staff, guest

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
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-074?state=<state>`: emptyFirstRun, emptyNoAccess, emptyNoResults, error, loading, offline.
- [ ] Every action is wired with its success and its failure: Assign rental equipment, Cancel.
- [ ] Every transition is wired: `EMP-071`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`, `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-075` Equipment Scan & Validation

**Ensure the operator cannot accidentally assign the wrong, unavailable or unsafe equipment.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block C · task APP-STAFF-EMP-075 |
| Who uses it | venue staff holding `ASSET_VIEW`, `RENTAL_OPERATE` (1 read, 1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/equipment-scan-validation-emp-075` |

**What the spec says about it.** The staff-app form of `BO-548`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** The scan-and-validate behaviour of the equipment step (merge into EMP-074). Each scan resolves the tag and is checked before it is accepted: right product, free, in service, not overdue for maintenance. The point is that the wrong, unavailable or unsafe unit cannot be assigned by accident.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search | text field | optional | — | — | — | Sends `?assetTag=` to `lookupAsset` (the tag typed or scanned on the equipment) (CHG-RFM-012). A search that returns nothing must say so differently from a search not yet run. | `lookupAsset` ?assetTag |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Assign rental equipment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Scan result**: Green: tag, name, "In service". Red with the reason in words: "Under maintenance", "Already out on RNT-10466", "This is a Junior bike - booking is for Mountain bike M", "Maintenance overdue since 12 Oct". Show the asset's status in the simplified words available / rented / faulty, not the six maintenance statuses. *(source: contracts/satellite/maintenance.yaml#lookupAsset / contracts/satellite/rental.yaml#assignRentalEquipment / DI-500)*

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

#### Consistency with other screens

- Match `EMP-074`: Same screen after consolidation.
- Match `BO-548`: Shared design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
scans:
- tag: BIKE-014
  result: ok
- tag: BIKE-019
  result: Under maintenance (brake pads)
- tag: KAY-003
  result: Wrong product
```

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
| Block | Block C · task APP-STAFF-EMP-076 |
| Who uses it | venue staff holding `RENTAL_OPERATE` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/pre-rental-condition-inspection-emp-076` |

**What the spec says about it.** The staff-app form of `BO-549`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Step 3: record the condition of each unit before it goes out - the only defence in a dispute at return. A short condition choice per unit, the product's checklist, an optional note and optional photos.

**Known correction pending (do not draw the wrong version)**

- **The action bar has buttons "Asset", "Reservation" and "Checkout inspection" - these are values the operation sends (asset id, booking id, phase), not user actions.** Why: Plumbing leaking onto a user screen; the unit and booking are context, the phase is implicit in the step. *(source: screens/P06-staff-app.yaml#EMP-076; Food, Beverage & Retail)*
- **The condition before handover is captured twice - as a pre-rental inspection (recordRentalInspection) and again as conditionNote/photos on the check-out call.** Why: The attendant must record it once; decide which record is the evidence and drop the other from the screen. *(source: contracts/satellite/rental.yaml#recordRentalInspection / contracts/satellite/rental.yaml#/components/schemas/RentalCheckOut; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Condition**: Good · Minor damage · Major damage · Faulty. "Not returned" is a return-only value and must not appear here. Faulty or Major damage blocks the unit: offer "Choose another unit" back in the equipment step. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalInspection / DI-500)*
- **Photos**: Optional by default (the client said photos are optional, not mandatory); required only where the product's photo-at-check-out rule says required. *(source: DI-766 / contracts/satellite/rental.yaml#/components/schemas/RentalOperationalRules)*
- **Checklist**: Pass/fail per item with a note on fail (e.g. Brakes, Tyres, Chain, Seat clamp). Items come from the product configuration. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalInspection / DI-759)*

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

#### Consistency with other screens

- Match `EMP-094`: Same component with phase "after return"; the comparison (EMP-095) relies on identical layout.
- Match `BO-549`: Shared design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
unit: BIKE-014
checklist:
- item: Brakes
  passed: true
- item: Tyres
  passed: true
- item: Chain
  passed: true
- item: Bell
  passed: false
  note: missing
condition: Minor damage
note: Scratch on top tube, bell missing
```

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
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-077` Safety & Handover Checklist

**Ensure mandatory operational and safety steps are completed before starting the rental. Example — Kayak ✓ Life jacket provided ✓ Paddle provided ✓ Safety briefing completed ✓ Emergency procedure explained ✓ Restricted areas explained ✓ Customer confirms swimming ability Example — Bicycle ✓ Helmet provided ✓ Brake check completed ✓ Seat adjusted ✓ Safety briefing completed The checklist should be configurable by rental product/category from Board 1.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block C · task APP-STAFF-EMP-077 |
| Who uses it | venue staff holding `RENTAL_OPERATE` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/safety-handover-checklist-emp-077` |

**What the spec says about it.** The staff-app form of `BO-550`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Step 4: the safety handover - what the guest is given and told, ticked off with the guest present. The list depends on the product (kayak: life jacket, paddle, briefing, emergency procedure, restricted areas, swimming ability; bike: helmet, brake check, seat adjusted, briefing).

**Known correction pending (do not draw the wrong version)**

- **The safety checklist items are not stored - the check-out request carries one boolean (safetyBriefingGiven) - and no product or category field holds the configurable list the screen's purpose says comes from Board 1.** Why: Ticks that are not recorded are no defence after an incident; the list needs a configuration field and a place in the check-out record. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalCheckOut / contracts/satellite/rental.yaml#/components/schemas/RentalOperationalRules / screens/P06-staff-app.yaml#EMP-077; Food, Beverage & Retail)*
- **This step submits the check-out (primary button bound to checkOutRental) although deposit and confirmation follow it.** Why: See the board 6 consolidation correction on EMP-071; only the final Confirm step submits. *(source: screens/P06-staff-app.yaml#EMP-077; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Checklist items**: Large tick rows; every item required unless configured optional. "Customer confirms swimming ability" is a guest confirmation, so it reads as a question to the guest. *(source: screens/P06-staff-app.yaml#EMP-077 / DI-759)*
- **Safety briefing given**: Required where the product's safety-briefing rule is required; the check-out is refused without it. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalOperationalRules / contracts/satellite/rental.yaml#checkOutRental)*

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

#### Consistency with other screens

- Match `BO-550`: Shared design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
product: Single kayak
items:
- Life jacket provided
- Paddle provided
- Safety briefing completed
- Emergency procedure explained
- Restricted areas explained (swim zone buoys)
- Customer confirms swimming ability
```

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
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-078` Deposit & Financial Handover Validation

**Give the rental operator a clear commercial status without requiring them to enter the Finance module.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block C · task APP-STAFF-EMP-078 |
| Who uses it | venue staff holding `RENTAL_OPERATE` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/deposit-financial-handover-validation-emp-078` |

**What the spec says about it.** The staff-app form of `BO-551`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step. **The card hold is a pre-authorisation on the payment terminal** (decided 2 October 2026, Chinmay, batch 6, EMP-078; DEC-304; CHG-CSA-029). The terminal returns the authorisation reference, the check-out carries it (`RentalCheckOut.depositAuthorisationId`) and the booking stores it; **check-out is blocked until the pre-authorisation succeeds** (`checkOutRental` answers 409 `deposit-not-authorised`), and the screen says so rather than offering to continue.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Step 5: take the deposit hold and show the attendant the money position without opening Finance: what was paid for the rental, the deposit to hold, how, and anything outstanding. The deposit is held, not charged, and is never added into the rental price.

**Known correction pending (do not draw the wrong version)**

- **depositInstrument on the check-out is a free string while the deposit policy defines the instrument list (cardPreAuthorisation, cardCharge, cash, wallet).** Why: The method buttons need the enum; a free string invites values the settlement cannot release. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalCheckOut / contracts/satellite/rental.yaml#/components/schemas/RentalDepositPolicy; Food, Beverage & Retail)*
- **The staff-app role grants RENTAL_OPERATE but not RENTAL_OVERRIDE, so a deposit waiver or reduction, and any override of a failed readiness check, cannot be requested from the handheld.** Why: Either a supervisor step-up on the same device or a hand-off to the back office must be drawn; today neither is possible. *(source: contracts/satellite/rental.yaml#requestRentalCommercialOverride; Food, Beverage & Retail)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How is the card hold taken and linked? The check-out carries the amount and method but no authorisation reference; the booking has depositAuthorisationId with no writer named.** → Rental card hold: pre-authorisation on the payment terminal; the reference is stored on the booking; check-out is blocked until it succeeds. *(decided by Chinmay, 2026-10-02; DEC-304 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Deposit method**: Only the methods the deposit policy allows, as buttons: Card hold (pre-authorisation), Card charge, Cash, Wallet. Cash goes into the till drawer like any other cash taken at the station. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalDepositPolicy / DI-752)*
- **Deposit amount**: Pre-filled from the booking's quote (fixed or percentage per policy, within its minimum and maximum); read-only for the attendant. Waiving or reducing it is an override with the original and adjusted amounts and a reason ("Other" needs a note). *(source: contracts/satellite/rental.yaml#/components/schemas/RentalQuote / contracts/satellite/rental.yaml#/components/schemas/RentalOverride / DI-752 / R222)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Money panel**: Two separate blocks, never summed: "Rental - paid AED 240.00 (order AQP-104582)" and "Deposit hold - AED 600.00 to hold, released on return". Outstanding rental balance, if any, in red with "Charge". *(source: contracts/satellite/rental.yaml#quoteRentalPrice / DI-757)*

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

#### Consistency with other screens

- Match `EMP-099`: Same two-block layout at return, with Captured and Released added.
- Match `BO-551`: Shared design; the desk adds the override approval.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rental:
  paid: AED 240.00
  order: AQP-104582
deposit:
  amount: AED 600.00
  basis: fixed 2 x 300.00
  method: Card hold
  card: Visa ending 4417
```

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
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-079` Group & Multi-Item Checkout

**Provide an efficient checkout workflow for group rentals and reservations containing multiple equipment units. This is particularly important because the original requirements support group reservations.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block C · task APP-STAFF-EMP-079 |
| Who uses it | venue staff holding `RENTAL_OPERATE` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/group-multi-item-checkout-emp-079` |

**What the spec says about it.** The staff-app form of `BO-552`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** The group case of the equipment step (merge into EMP-074): ten bikes for a school group go out in one action, one row per participant with the unit assigned to each.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Assign rental equipment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Group table**: Participant name, waiver signed (yes/no), unit tag. The group can leave only when every participant has a unit and a signature, or a supervisor overrides. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalParticipant / DI-755 / DI-760)*

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

#### Consistency with other screens

- Match `EMP-089`: The active group view uses the same participant/unit rows.
- Match `BO-552`: Shared design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
group: RNT-10487, Al Mansoori school trip
rows:
- participant: Omar Ziad
  waiver: signed
  unit: BIKE-014
- participant: Fatima Al Suwaidi
  waiver: not signed
  unit: BIKE-022
```

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
| Block | Block C · task APP-STAFF-EMP-080 |
| Who uses it | venue staff holding `RENTAL_OPERATE` (1 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | configEditor (comfortable density): the pack gives this screen a configuration directory (§Options; Select Equipment) and no display directory — it is settings, not a population |
| Offline | TODO — not decided. Rental Management does not say what a staff device does here without a connection, and no minute has decided it. |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/checkout-confirmation-rental-activation-emp-080` |

**What the spec says about it.** The staff-app form of `BO-553`, for the attendant at the rental counter. Decided 11 September 2026 that Rental boards 6–8 live on both platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step.

**From the Food, Beverage & Retail process.** Final step: confirm and start the rental. A review of what is going out (units, condition, safety done, deposit held, due back time) and one "Check out" button that makes the booking active and starts the clock. The server re-checks every precondition here and names the one that failed.

**Known correction pending (do not draw the wrong version)**

- **The layout has a text field labelled "Email / SMS / App Notification", a select labelled with an arrow glyph, and pattern configEditor.** Why: Pack artefacts read literally - the first is a channel choice, the second has no meaning, and an activation step is not a configuration editor. No operation sends the confirmation either. *(source: screens/P06-staff-app.yaml#EMP-080; Food, Beverage & Retail)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does the rental clock start at the booked start or at handover? A guest who arrives 15 minutes late for a 1-hour kayak - due back at the booked end or one hour after handover?** → Drawn default accepted: Due back = booked end time; the attendant may set dueBackAt later only with a supervisor. *(decided by Chinmay, 2026-10-02; DEC-305 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Email / SMS / App Notification | text field | — | — | — | — | — | — |
| ↓ | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Due back**: Pre-filled with the booked end time; shown large. Changing it is not a check-out edit - use Extend once the rental is active. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalCheckOut / DI-761)*
- **Send confirmation by**: A segmented choice Email / SMS / App (pre-selected from the guest's contact details). *(source: screens/P06-staff-app.yaml#EMP-080)*

#### Outputs: what the screen shows and produces

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Check out**: Success: booking becomes "Out", the guest sees the due-back time, the queue counter moves. Refusal (409) names the missing precondition and jumps to that step ("Agreement not signed by Daniel Brooks"). *(source: contracts/satellite/rental.yaml#checkOutRental)*

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

#### Consistency with other screens

- Match `BO-553`: Shared design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
review:
  booking: RNT-10482
  units:
  - KAY-003
  - KAY-007
  kit: Paddle x2
  Life jacket x2: null
  deposit: AED 600.00 held
  dueBack: Sat 17 Oct 2026 11:00
```

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
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
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
"getRentalAvailability": {"method":"GET","path":"/rental-availability","contract":"rental","summary":"What can be rented, when, with turnaround already subtracted","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":true},{"name":"locationId","in":"query","required":null},{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"quantity","in":"query","required":null}],"requestBody":null,"responds":"RentalAvailability"},
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
"RentalAvailability": {"type":"object","description":"Board 3. **A pooled product answers with a count, a serialised one with assets.**","properties":{"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid","nullable":true},"windows":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"availableQuantity":{"type":"integer"},"availableAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"blockedWindows":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"reason":{"type":"string","enum":["booked","turnaround","maintenance","blackout","closed","buffer","held"]}}}}}},
"RentalBooking": {"type":"object","x-ticvai-persistence":"rental.booking","description":"Board 5. **The booking outlives the order** — an order completes at payment and the rental is still out.\n","required":["id","productId","from","to","status"],"properties":{"id":{"type":"string","format":"uuid"},"reference":{"type":"string"},"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"returnLocationId":{"type":"string","format":"uuid","nullable":true},"customerId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer"},"status":{"type":"string","enum":["draft","confirmed","awaitingArrival","checkedOut","overdue","partiallyReturned","completed","completedWithDamage","notReturned","cancelled","noShow"]},"checkedOutAt":{"type":"string","format":"date-time","nullable":true},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"returnedAt":{"type":"string","format":"date-time","nullable":true},"depositAuthorisationId":{"type":"string","format":"uuid","nullable":true,"description":"The card deposit's terminal pre-authorisation, written by `checkOutRental` (workbook Q304; CHG-CSA-029). The hold is kept whole until every unit is back (workbook Q306)."},"accruedLateFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"readiness":{"type":"array","readOnly":true,"description":"**Computed, not stored** — agreement, requirements, deposit, equipment.","items":{"type":"object","properties":{"check":{"type":"string"},"satisfied":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"participants":{"type":"array","items":{"$ref":"#/components/schemas/RentalParticipant"}},"scopePath":{"type":"string"}}},
"RentalCheckOut": {"type":"object","description":"Board 6. **The readiness gate is enforced server-side.**","properties":{"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"depositInstrument":{"type":"string","nullable":true},"depositAuthorisationId":{"type":"string","format":"uuid","nullable":true,"description":"**The terminal pre-authorisation of a card deposit** (workbook Q304; CHG-CSA-029), as the payments terminal returned it. Required where the deposit is on a card; stored on the booking."},"conditionNote":{"type":"string","nullable":true},"photoAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"safetyBriefingGiven":{"type":"boolean","default":false},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"overrideId":{"type":"string","format":"uuid","nullable":true,"description":"**A supervisor override for a failed precondition**, which is recorded rather than allowed silently.\n"}}},
"RentalEquipmentAssignment": {"type":"object","x-ticvai-persistence":"rental.equipment_assignment","description":"Board 6.4. **The moment a serialised rental stops being a quantity.**","required":["assetId"],"properties":{"id":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","description":"A `maintenance.Asset`, which is also a `resources` resource where the product is schedule-controlled."},"serialNumber":{"type":"string","nullable":true},"scannedCode":{"type":"string","nullable":true},"assignedManually":{"type":"boolean","default":false},"assignedAt":{"type":"string","format":"date-time"},"returnedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"RentalInspection": {"type":"object","x-ticvai-persistence":"rental.inspection","description":"Boards 6.5 and 8.4. **Before and after are one record shape with a phase**, which is what makes the comparison view possible.\n","required":["phase","condition"],"properties":{"id":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"phase":{"type":"string","enum":["preRental","postRental"]},"condition":{"type":"string","enum":["good","minorDamage","majorDamage","faulty","notReturned"],"description":"**26 August: simplified state attributes.** *\"rental/equipment items can be tracked with simplified state attributes (e.g., available, rented, faulty) rather than requiring granular custom attributes for this category — agreed by Allam.\"* So the condition is a short enum, and anything finer belongs in the note or the photographs.\n"},"checklist":{"type":"array","items":{"type":"object","properties":{"item":{"type":"string"},"passed":{"type":"boolean"},"note":{"type":"string","nullable":true}}}},"note":{"type":"string","nullable":true},"photoAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"inspectedBy":{"type":"string","format":"uuid"},"inspectedAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string"}}},
"RentalParticipant": {"type":"object","x-ticvai-persistence":"rental.participant","description":"Board 5.5. **A group rental is one booking with participants**, because the agreement, the deposit and the return are handled together.\n","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"isPrimaryRenter":{"type":"boolean","default":false},"dateOfBirth":{"type":"string","format":"date","nullable":true},"idNumber":{"type":"string","nullable":true},"guardianName":{"type":"string","nullable":true},"emergencyContact":{"type":"string","nullable":true},"hasSignedWaiver":{"type":"boolean","readOnly":true},"customFields":{"type":"object","additionalProperties":true}}},
"WorkOrder": {"x-ticvai-persistence":"maintenance.work_order","x-ticvai-retired-columns":["is_overdue"],"type":"object","required":["id","workOrderNumber","title","venueId","status","priority","kind","createdAt"],"properties":{"downtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"},"rootCause":{"type":"string","nullable":true,"enum":["wearAndTear","operatorError","guestDamage","manufacturingDefect","environmental","softwareFault","powerFailure","deferredMaintenance","unknown"],"description":"**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"},"rootCauseNote":{"type":"string","nullable":true},"escalatedAt":{"type":"string","format":"date-time","nullable":true},"escalationLevel":{"type":"integer","default":0,"description":"**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"},"id":{"type":"string","format":"uuid"},"workOrderNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"title":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"assetName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"},"status":{"$ref":"#/components/schemas/WorkOrderStatus"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"priorityScore":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"readOnly":true,"description":"The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."},"prioritySource":{"type":"string","enum":["scored","assetOverride","manual"],"readOnly":true,"description":"Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","items":{"type":"string"},"description":"Skills the job needs (M17-13)."},"kind":{"$ref":"#/components/schemas/WorkOrderKind"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"raisedByPrincipalId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"},"locationDescription":{"type":"string","maxLength":500,"nullable":true,"description":"Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"},"elapsedMinutes":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"},"isTimerRunning":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"},"dueAt":{"type":"string","format":"date-time","nullable":true},"isOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"},"requiresVerification":{"type":"boolean"},"sourcePlanId":{"type":"string","format":"uuid","nullable":true},"sourceInspectionId":{"type":"string","format":"uuid","nullable":true},"sourceIncidentId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}}
}
```
