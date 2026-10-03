# P01-in-venue-services-01 — P01 · In-venue Services

**6 screens · 23 operations · 51 schemas · 5 permissions**

Platform P01 Guest Web · ships as **guest** ·
guest audience · web ·
online only

## Who this is for

**guest on web.** Everything below is how you know what is
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
  `ORDER_MODIFY, PARKING_CONFIGURE, PRODUCT_VIEW, QUEUE_VIEW, VENUE_MAP_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store. Offline, a screen shows what was already loaded, under the banner below.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
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

### Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale)

A guest finds something to do, picks when and how many, holds capacity, pays, and receives a ticket they can show at the gate, transfer or resell. The same booking engine serves the guest website (P01, WEB-), the guest app (P02, GST-) and, through the same catalogue, cart and order operations, the kiosk (P05), the cashier at the till (P04) and the staff handheld (P06); partners book on credit through the partner portal (P10). Guest surfaces are white-label (venue logo, colours, fonts, card layouts, step indicator style, cart placement) with "Powered by TICVAI" kept; the till and handheld stay TICVAI-branded. The booking runs in a fixed order that the client set on 29 September and confirmed on 30 September: for a dated product, the date first, then the time (hidden until a date), then the tickets (hidden until a time); undated products go straight to the tickets; product-first flows (workshops) pick the product, then the date; seated events with one performance open on the seat map, sections first, zoom into a section, pinch out to compare. Choosing a date, time or session commits nothing; capacity is held only when a quantity is set (a 15-minute basket window, 8 minutes for seats and cabanas, one extension). The guest counters (adult, child, senior, infant, person of determination) belong to the chosen ticket and take its prices, so a basket line is "<ticket> · <guest type> × <n>"; group and school products start from group ticket cards and a typed headcount (minus, plus, and +10 on the app), supervisors free. Help me choose filters the catalogue on the server (never a consent step) with Show everything; consent questions such as "Are you able to swim?" are asked once after the session is picked and never again where the page already asked. Sign-in or the six-digit guest code is asked when the guest leaves Add-ons (or at payment, per venue), only the fields the venue configured; after the code, only the T&Cs tick remains (W1). Payment creates the order first and treats an unknown outcome as "checking with your bank", never a second charge; tickets issue on payment, go to Apple or Google Wallet, and a dynamic-QR event's ticket lives in the app. The guest app is deliberately not a copy of the website (30 September): its structure is Home, Explore, Plan and Tickets tabs with a persistent Buy tickets button, item pages that propose the right product (a restaurant's meal combo that includes admission), ride videos that play with no loader, a visit planner that plans each day at one park from that park's rides, dining and shops only, and in-park walking navigation; the booking flow inside it is functionally identical to the web. Vocabulary in guest copy follows the glossary's recorded exceptions (Booking, Session, QR). source: [F01, F02, F03, F07, F49, F52, F55, F57, F58, F59, MoM 29 Sep 1 (W1-W12), MoM 29 Sep 2, MoM 29 Sep 3, MoM 30 Sep 4.4-4.8, CLIENT-RESPONSE-30SEP 1-6, CLIENT-RESPONSE-REV3-25SEP, REV3-1, REV3-2, REV3-3, REV3-4, REV3-26, DI-1086 …

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Booking | An order or reservation as the guest reads it (Booking Confirmation, Group Booking, My bookings). Code says Order or Reservation. | Order (in guest copy), Purchase record, Transaction | docs/glossary.md (Recorded exceptions, Booking, audit R145) |
| Session | A dated, timed performance as the guest reads it (Pick a session, Surf sessions). Staff screens (POS, back office) keep Performance. | Slot, Showtime, Performance (in guest copy) | docs/glossary.md (Recorded exceptions, Session, rev 3 CFG-10); DI-1064 |
| Basket | The guest's unpaid selection with its held capacity (Add to basket, Your basket). Never a paid order. The till and staff screens say Cart. | Cart (in guest copy), Bag, Order (for an unpaid selection) | CLIENT-RESPONSE-REV3-25SEP (Basket, 10) … |
| Ticket | The issued instrument a guest shows at the gate. Product names from the catalogue keep their own words (Day Pass, Annual pass, 2 park ticket); the interface around them says ticket. | Admission, Voucher (for a ticket), Pass (in interface copy) | docs/glossary.md (Ticket) |
| Adult, Child, Senior, Infant, Person of determination | The guest types of a ticket, each with its age or height band shown under it (Child 3-12, Under 1.20 m). A companion of a person of determination is its own free type where the product has one. | Disabled, Handicapped, Kid, Pax | DI-686; screens/P01-guest-web-storefront.yaml#WEB-049 (Passengers notes) … |
| Held for | The countdown on held capacity ("Your seats are held for 7:42"); the release is Release hold. | Lease, Reserved for (a reservation is a different thing), Locked | contracts/spine/orders.yaml#/components/schemas/CartLine (leaseExpiresAt) … |
| Reservation | Booked and not yet paid; holds capacity and expires (My Reservations). Paid tickets are in Tickets or My Tickets. | Booking (for an unpaid hold in lists), Pending order | docs/glossary.md (Reservation); DI-199 |
| Help me choose | The venue's questions whose answers filter the products; Show everything clears them. | Quiz, Wizard, Experience builder, Consent | MoM 29 Sep W4; REV3-11 |
| Info only / Not bookable online | A product listed with full details that cannot be booked online; it shows Contact sales to book with Call sales and Email sales. | Unavailable, Sold out, Coming soon | REV3-14; MoM 29 Sep W3 |
| Guest code | The six-digit code sent to the guest's email or mobile to prove the contact at guest checkout; the copy says six digits. | OTP, PIN, Token, Verification key | DI-1034; MoM 29 Sep W1 |
| How many people | The typed headcount of a group or school booking (number box with minus and plus; +10 on the app), with Supervisors listed separately and free. | Group size (the removed dropdown), Pax | DI-1104; DI-1105; CLIENT-RESPONSE-30SEP 1 |
| Waiting room | The on-sale queue in front of a high-demand performance's sale (WEB-015, GST-046). | Virtual queue (that is the ride queue), Lobby | screens/P01-guest-web-storefront.yaml#WEB-015 notes (ADR-0066) |
| QR | The code a guest shows, in guest copy only (Dynamic QR). Staff screens say Media code. | Barcode, Serial, Media code (in guest copy) | docs/glossary.md (Recorded exceptions, QR, audit R210) |
| Not at this park | The planner's per-day notice that the day's park cannot meet a preference, naming the park that can. | Unavailable, No results | DI-1113 |
| Book this plan | Turns the whole visit plan (tickets, Fast Track, meal combos) into basket lines. | Checkout plan, Buy itinerary | screens/P02-guest-mobile-app.yaml#GST-053 (Book this plan) |

### Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue)

Venue operations is everything that happens after a sale and inside the gates. A guest's ticket is one virtual ticket with interchangeable media (QR, dynamic QR, RFID wristband, NFC, Face Pass or Face Tag); at an access point a scanner (P07, or the scan function inside the Staff App P06) validates the media against the admission profile and the guest admission policy, offline if it must, and every deny carries a reason and a next action. The back office (Venue Management P08) configures that estate: the venue topology (venue, park, zone, attraction, access point, gate and lane, device placement), admission profiles and rules (entry, exit, re-entry, anti-passback, validity, crossover, companions), credential security (dynamic QR, device binding, beacons), biometrics, gate modes, and the live operations, fraud and monitoring views. Accreditation (P08 setup and review, P11 web portal for applicants, web first) takes an applicant from a configurable form through document checks, OCR, duplicate blocking and multi-level approval to a credential with zone rights. Resources and capacity manage bookable resources (rooms, vehicles, equipment, cabanas, instructors) that are booked as a consequence of selling a product, never sold directly. Workforce covers shift templates, rosters, attendance, swaps and breaks, mirrored on the Staff App. Maintenance and safety cover the asset register, preventive calendars, work orders with scored priority, inspections and incidents, with technicians working from the Staff App. Games and rides configure readers, credit types and consumption priority, play entitlements, game pricing, retry pricing, redemption and the card lifecycle. The virtual queue (Q1) gives a guest a live wait time and a return window for a ride; it is not the on-sale waiting room (Q2). Every calendar has day, week and month views. Configuration resolves tenant, region, venue (outlet only for F&B and retail), and a user's permissions, never the device, decide what they may do. The guest apps (P01, P02) show the guest's side of this: My Tickets, the scan code, Face Pass, wait times, the virtual queue, map booking of cabanas and the visit planner.
*(source: F06 step 1 / F112 step 1 / F111 step 1 / ADR-0002 / ADR-0012 / ADR-0018 / ADR-0041 / ADR-0066 / ADR-0067 / ADR-0068 / DI-652 / DI-627 / DI-640 / DI-654 / DI-666 / DI-482 / DI-483 / DI-907 / DI-919 / DI-923 / DI-865 / DI-678 / TRACKER Actions row 160 / MoM 2026-09-02 AccessControl / MoM 2026-09-07 …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Ticket | The one virtual record a guest owns (ticket number, product, validity, entries). Its number never changes, whatever media carries it or whoever it is transferred or resold to. | Pass (unless the product is a pass), Booking, Order line | DI-652 / DI-620 / contracts/spine/access.yaml#/components/schemas/TicketStatus |
| Media | What the ticket is presented by at a gate (QR code, dynamic QR, wristband/RFID card, NFC, Face Pass, Face Tag). One ticket can carry several media as fallbacks; a media code can also cover several tickets scanned as one group. Show one … | Credential (for guest media; keep Credential for accreditation badges and staff), Ticket code | DI-180 / DI-608 / DI-652 |
| Access point | A place where a scan is judged, with a fixed direction (entry, exit, re-entry, crossover). Hierarchy shown to users is Venue > Park > Zone > Attraction > Access point > Gate/lane > Device. | Scanner (that is the device), Door | screens/P08-venue-back-office.yaml#BO-144 / … |
| Admission profile | The named set of rules an access point enforces (opening window, entries, exit scan, re-entry, validity, crossover). Products point at a profile; tiers such as Bronze/Silver/Gold are profiles with gate allow and deny lists. | Admission rules (as a screen title), Access rule set | DI-185 / contracts/spine/access.yaml#/components/schemas/AdmissionRules |
| Admitted / Denied / Overridden | The three scan outcomes. A denial is always shown with its reason in plain words and a next action; an override is a supervisor admitting despite a denial, and is always attributed and reasoned. | Valid/Invalid, Success/Fail, Error | contracts/spine/access.yaml#/components/schemas/ScanOutcome / … |
| Used | A ticket entry is used the moment a scan succeeds, whether or not the guest physically passed. Mistakes are resolved from the scan history, not by un-scanning. | Redeemed (for admission), Checked in (that is group check-in, a different step) | DI-627 / TRACKER Actions row 221 / TRACKER Actions row 189 |
| Gate mode | What a lane is doing now, set live by the podium or supervisor - Normal, Free flow (counts, does not validate), Drop arm (everybody through, evacuation), Closed (nobody through), Podium (staff validating by eye), Maintenance. Direction is … | Turnstile mode (as a label for direction), Open/Locked | contracts/spine/access.yaml#/components/schemas/AccessPointOperatingMode / R221 |
| Offline package | What a scanner holds to validate with no network - entitlements, blacklist, admission profiles and the active guest admission policy version - with its age always visible. | Cache, Local DB | F06 step 3 / ADR-0068 |
| Sync and reconciliation | Sending the offline scan journal to the server, and the duty manager's review of scans the server rejected after the device had already admitted the guest. | Upload, Retry | F06 step 6 / DI-065 |
| Face Pass / Face Tag | Face Pass is the long-lived face credential for members and season-pass holders (renewable); Face Tag is short-lived, for one day or event. Retention is set per tier by the venue. | Face ID, Biometric login | DI-640 / ADR-0063 |
| Accreditation / Credential (accreditation) | Accreditation is the application and approval of a person (media, contractor, corporate, staff of a partner) for an event or season; the credential is what is issued after approval (photo badge, QR or RFID) with zone access rights. | Registration (for the whole process), Ticket | DI-654 / DI-662 |
| Resource | A bookable thing or person a product needs (room, vehicle, cabana, equipment set, instructor). Guests buy products; resources are assigned to the booking, pre-assigned or dynamically. | Asset (that is maintenance), Inventory (that is stock) | DI-475 / DI-482 / TRACKER Actions row 160 |
| Asset | A physical item maintained by the venue (ride, turnstile, printer, pump) with a register record, documents, warranty and maintenance history. | Resource, Device (unless it is an IT device in the device register) | DI-910 / ADR-0067 |
| Work order | A unit of maintenance work, lifecycle Created > Assigned > In progress > Review > Closed, with a resolution timer. | Ticket (reserved for guest tickets), Job card | DI-231 |
| Game / attraction (games module) | In the games and rides module an attraction is an individual game or ride (roller coaster, racing game, bumper cars), not a venue. | Venue, Park | DI-863 |
| Virtual queue / Return window | A guest's place in a ride's queue held without standing in line, with a return window (for example 4:50 to 5:00 PM) that recalculates live. Distinct from the walk-in line and the VIP/express lane, and from the on-sale waiting room. | Waiting room, Fast pass (that is the express product), Booking | DI-675 / DI-678 / DI-679 / ADR-0066 |
| Wait time source | Where a ride's wait time comes from - Sensor, Throughput, Manual, or Unavailable - always shown beside the number. | Live (when the source is manual) | contracts/satellite/queue.yaml#/components/schemas/WaitTimeSource / DI-315 |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `WEB-036` | F&B – Browse & Order | A | 70 | 43 | 6 | 22 | 11 | 0 | guest | review (client-verified) |
| `WEB-037` | Menu Item Detail | A | 0 | 7 | 5 | 1 | 2 | 2 | guest | review (client-verified) |
| `WEB-038` | F&B – Order Tracking | A | 0 | 14 | 5 | 0 | 0 | 0 | guest | review (client-verified) |
| `WEB-039` | Venue Map & Wait Times | A | 0 | 18 | 6 | 5 | 4 | 6 | guest | review (client-verified) |
| `WEB-040` | Virtual Queue | A | 8 | 15 | 6 | 11 | 3 | 6 | guest | review (client-verified) |
| `WEB-041` | Parking – Reserve & Pay | A | 22 | 2 | 7 | 7 | 2 | 2 | guest | review (client-verified) |

## Thin screens in this batch

**WEB-037, WEB-038 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `WEB-036` F&B – Browse & Order

**Order food from a table, a lounger or a seat.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | In-venue Services · wave 1 · needs the `fnb` module |
| Block | Block A · task APP-WEB-WEB-036 |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): Location, menu, basket, pay: the guest picks an outlet, then orders from its menu (CHG-SGU-018) |
| Offline | **The offline banner shows.** The menu already loaded stays with its age. Ordering, claiming a table and booking wait for the connection — an order placed offline is food nobody is making. |
| Opens with | `outletId` (deepLink), `venueId` (session), `orderId` (deepLink), `entryId` (deepLink), `cartId` (session), `reservationId` (navigation) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a … |
| Route | `/fandb--browse-and-order` |

**What the spec says about it.** **A guest scans a QR on a table and lands in a browser.** That is the single most common F&B ordering pattern anywhere, and until 24 August it was the one thing this surface could not do — `claimTableSession` and `claimLocationSession` were app-only. **Nobody installs an app to order a coffee.** **Renamed 31 August** from *F&B — Browse & Order*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest. **Cross-surface parity, 31 August**: added getGuestOrderStatus. **The same screen on web and app was calling different operations** — one side could do something the other could not, and nothing recorded the difference as deliberate. **Rev 3 (decided 29 September).** **Table reservation and waitlist stay out of the basket (REV3-8):** `createTableReservation` and `joinRestaurantWaitlist` confirm straight away with a *No card needed* confirmation; the prototype's basket line is prototype-only. **Deposit (REV3-8b, superseding audit R077 (a)):** where the venue has enabled a dining deposit, `createTableReservation` answers `awaitingDeposit`; the screen shows `deposit.amount` and basis, adds the deposit to the cart (`addCartLine` with `deposit.variantId` and `tableReservationId`), pays it through checkout, and shows `refundableUntil` and the late-cancel and no-show terms. Off by default; amount and basis are venue configuration, never a fixed AED 100. **Modifiers (REV3-9):** Add opens the modifier side panel of WEB-037 when the item has groups attached. Delivery fee, minimum order …

**From the Food, Beverage & Retail process.** The guest web's food screen for someone already inside the venue. They scan the QR on a table, lounger, cabana or seat and land here in the browser, with no app needed. For outlets that offer it, the same screen also handles takeaway and delivery with a time slot, and booking a restaurant table or joining its waitlist (in the app those two live on GST-070). The one thing to get right: the guest learns where the food is going and whether it can come there before building a basket, and every refusal arrives before payment, never after.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- WEB-036 can book a table but cannot change or cancel one (no updateTableReservation), while GST-070 can. And no guest-callable read of one's own table bookings or waitlist place exists (listTableReservations is … (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): The layout puts plumbing on a guest screen: data tables "Every browse order", "Every fulfilment slots", "Every modifier group" (with … (CHG-SGU-018); claimTableSession is declared, as a button and a modal. (CHG-SGU-018); listModifierGroups is declared to draw the modifier panel. (CHG-SGU-018); The rev 3 prototype's "At the venue → Order food" sends the order with "Send to the kitchen" and no payment step. (CHG-SGU-018); The table booking has no field for a seating-area preference or an occasion, though the client's dining flow asks for both and the rev 3 … (CHG-SGU-018).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Takeaway and delivery to an address (DG-5, DI-1039, 29 September) let someone buy food without an admission ticket, which DI-292 (14 August) put out of scope. Which stands?** → Outlet property: 'Inside the venue (needs an admission ticket)' or 'Standalone (no ticket)'. Inside-venue outlets need admission for guest ordering; a standalone restaurant sells takeaway/delivery without a ticket. *(decided by Chinmay, 2026-10-02; DEC-070 / CHG-NOTE-004 / CHG-SGU-001)*
- **Does a guest F&B order go through the one shared cart and checkout (one receipt, DI-293), or does it keep its own pay step after createGuestFnbOrder (F11 step 4 on GST-009)?** → The guest F&B order keeps its own payment step and receipt; DI-293's one cart/one receipt does not apply to F&B. *(decided by Chinmay, 2026-10-02; DEC-071 / CHG-NOTE-004 / CHG-SGU-001)*
- **When is room charge (paymentMethod roomCharge) offered to a guest, if ever?** → Not answered: the workbook cell repeats the sibling WEB-036 answer. Room charge is not shown to guests (drawn default). *(decided by Chinmay, 2026-10-02; DEC-072 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Lounger, table or seat number | text field | optional | — | — | — | A scanned code arrives with the link and is claimed at once; this short box is the fallback when the QR is damaged ("Lounger B-14", "Table 12"). Party size is asked only at a table. | `LocationSession.label` |
| How you get it | radio group | optional | — | Table service · App to table · App to collect · Counter only · Not available | — | Only what the outlet supports: to my table, seat or lounger; collect from the counter; delivery to an address. Sends `mode`. | `DiningOutlet.orderingMethod` |
| When | repeatable rows | optional | — | — | — | ASAP first ("About 25 min"), then the open slots; a date only for advance takeaway or delivery. | `FulfilmentSlots.slots` |
| Deliver to | text field | optional | — | — | — | The delivery area check before the menu; an address outside it never reaches a basket. Building, unit, emirate (from the outlet's emirates) and directions. | `DeliveryLocation.label` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Outlet | picker: choose an outlet | — | — | `getFnbDeliveryPolicy` ?outletId |
| Mode | segmented control | — | Collection · Delivery | `listFulfilmentSlots` ?mode |
| Date | date picker | — | — | `listFulfilmentSlots` ?date |
| At | date and time picker | — | — | `getGuestMenu` ?at |
| Language | language picker | — | — | `getGuestMenu` ?language |
| Open now | toggle | on | — | `listDiningOutlets` ?openNow |
| Ordering method | radio group | — | Table service · App to table · App to collect · Counter only · Not available | `listDiningOutlets` ?orderingMethod |
| Kind | select | — | Table · Seat · Cabana · Sunbed · Poolside · Box · Suite · Lawn · Collection point · Named location | `listDeliveryLocations` ?kind |
| Serving outlet | picker: choose a serving outlet | — | — | `listDeliveryLocations` ?servingOutletId |

**Form: Book a table** (modal, opened by *Book a table*; *Book a table* calls `createTableReservation`, *Cancel* sends nothing)

Restaurant, date, time and party size on one screen, an optional note for allergies or requests, and optional seating preference (`seatingPreference`) and occasion (`occasion`: birthday, anniversary, business, celebration, other; DEC-204). Name and contact are prefilled from the profile. No table picking, no duration, and nothing the server sets (id, status, tables, group, visit). Confirmed at once with "No card needed", unless the venue enabled a deposit (`awaitingDeposit`).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `createTableReservation` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `createTableReservation` body |
| Guest name `guestName` | text field | optional | — | — | — | — | `createTableReservation` body |
| Contact point `contactPoint` | text field | optional | — | — | — | — | `createTableReservation` body |
| Party size `partySize` | number field | required | — | min 1 | — | — | `createTableReservation` body |
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createTableReservation` body |
| Duration minutes `durationMinutes` | number field (minutes) | optional | — | An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. | — | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. | `createTableReservation` body |
| Tables `tables` | repeatable rows | optional | — | — | — | The dining tables assigned to this reservation, one row each. Usually empty until seating. | `createTableReservation` body |
| Reservation `tables[].reservationId` | picker: choose a reservation | required | — | — | shows names, sends the id | — | `createTableReservation` body |
| Table `tables[].tableId` | picker: choose a table | required | — | — | shows names, sends the id | — | `createTableReservation` body |
| Created at `tables[].createdAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createTableReservation` body |
| Status `status` | select | optional | — | Awaiting deposit · Booked · Confirmed · Seated · Completed · Cancelled · No show; `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`. | — | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`. | `createTableReservation` body |
| Group `groupId` | picker: choose a group | optional | — | — | shows names, sends the id | 5.1.2. Several bookings managed as one party across adjacent tables. | `createTableReservation` body |
| Notes `notes` | text area | optional | — | — | — | Allergies, accessibility needs and other requests, as the guest wrote them. | `createTableReservation` body |
| Seating preference `seatingPreference` | text field | optional | — | max length 64 | — | The seating area the guest asked for, e.g. indoor, terrace, majlis (Chinmay, 2 October, workbook Q204; DI-791; CHG-CSA-018). | `createTableReservation` body |
| Occasion `occasion` | radio group | optional | — | Birthday · Anniversary · Business · Celebration · Other | — | The occasion the guest named (workbook Q204, DI-337; CHG-CSA-018). Shown to the host and the server; never a price. | `createTableReservation` body |

Errors to draw in the form: 409 No cover available for that party size at that time. The reason names the constraint — a party of eight refused when a party of two would fit …

**Form: Change or cancel booking** (modal, opened by *Change or cancel booking*; *Change or cancel booking* calls `updateTableReservation`, *Cancel* sends nothing)

Party size and time only; the restaurant is fixed. Cancelling says the consequence first: free, deposit released, or deposit kept.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `updateTableReservation` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `updateTableReservation` body |
| Guest name `guestName` | text field | optional | — | — | — | — | `updateTableReservation` body |
| Contact point `contactPoint` | text field | optional | — | — | — | — | `updateTableReservation` body |
| Party size `partySize` | number field | required | — | min 1 | — | — | `updateTableReservation` body |
| Starts at `startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateTableReservation` body |
| Duration minutes `durationMinutes` | number field (minutes) | optional | — | An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. | — | How long the cover is held. An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked. | `updateTableReservation` body |
| Tables `tables` | repeatable rows | optional | — | — | — | The dining tables assigned to this reservation, one row each. Usually empty until seating. | `updateTableReservation` body |
| Reservation `tables[].reservationId` | picker: choose a reservation | required | — | — | shows names, sends the id | — | `updateTableReservation` body |
| Table `tables[].tableId` | picker: choose a table | required | — | — | shows names, sends the id | — | `updateTableReservation` body |
| Created at `tables[].createdAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateTableReservation` body |
| Status `status` | select | optional | — | Awaiting deposit · Booked · Confirmed · Seated · Completed · Cancelled · No show; `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`. | — | `awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`. | `updateTableReservation` body |
| Group `groupId` | picker: choose a group | optional | — | — | shows names, sends the id | 5.1.2. Several bookings managed as one party across adjacent tables. | `updateTableReservation` body |
| Notes `notes` | text area | optional | — | — | — | Allergies, accessibility needs and other requests, as the guest wrote them. | `updateTableReservation` body |
| Seating preference `seatingPreference` | text field | optional | — | max length 64 | — | The seating area the guest asked for, e.g. indoor, terrace, majlis (Chinmay, 2 October, workbook Q204; DI-791; CHG-CSA-018). | `updateTableReservation` body |
| Occasion `occasion` | radio group | optional | — | Birthday · Anniversary · Business · Celebration · Other | — | The occasion the guest named (workbook Q204, DI-337; CHG-CSA-018). Shown to the host and the server; never a price. | `updateTableReservation` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Join the waitlist** (modal, opened by *Join the waitlist*; *Join the waitlist* calls `joinRestaurantWaitlist`, *Cancel* sends nothing)

Party size and seating (Any, Indoor, Outdoor, Bar, Booth, High chair needed). Name and contact come from the profile; nothing the server sets is asked.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `joinRestaurantWaitlist` body |
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `joinRestaurantWaitlist` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | — | `joinRestaurantWaitlist` body |
| Party size `partySize` | number field | required | — | — | — | — | `joinRestaurantWaitlist` body |
| Quoted wait minutes `quotedWaitMinutes` | number field (minutes) | optional | — | — | — | — | `joinRestaurantWaitlist` body |
| Seating preference `seatingPreference` | select | optional | — | Any · Indoor · Outdoor · Bar · Booth · High chair | — | — | `joinRestaurantWaitlist` body |
| Status `status` | select | required | — | Waiting · Notified · Seated · Walked away · No show · Cancelled | — | — | `joinRestaurantWaitlist` body |
| Notified at `notifiedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `joinRestaurantWaitlist` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the party joined, on the device. The wait a party had is measured from here to `notifiedAt` or to seating, which is the report `walkedAway` exists for. | `joinRestaurantWaitlist` body |
| Hold expires at `holdExpiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | How long a table waits for somebody who was called. Too short and a guest returning from the bathroom loses it; too long and the table sits empty at peak — which is why it is a … | `joinRestaurantWaitlist` body |

**Sent by *Pay*** (`createGuestFnbOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createGuestFnbOrder` body |
| Location session `locationSessionId` | picker: choose a location session | optional | — | — | shows names, sends the id | From `claimLocationSession`. Where the order is going. | `createGuestFnbOrder` body |
| Outlet `outletId` | picker: choose an outlet | optional | — | — | shows names, sends the id | Required for collection. Ignored where a location session is supplied — the session names its outlet. | `createGuestFnbOrder` body |
| Fulfilment `fulfilment` | group | optional | — | — | — | Required for takeaway and address delivery; refused with 422 when it breaks the outlet's `FnbDeliveryPolicy`. | `createGuestFnbOrder` body |
| Mode `fulfilment.mode` | segmented control | required | — | Collection · Delivery · In venue | — | `collection` from a counter, `delivery` to an address outside the venue, `inVenue` to a table, seat, cabana or named location (the location session). | `createGuestFnbOrder` body |
| Collection at `fulfilment.collectionAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createGuestFnbOrder` body |
| Window start `fulfilment.windowStart` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createGuestFnbOrder` body |
| Window end `fulfilment.windowEnd` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createGuestFnbOrder` body |
| Delivery address `fulfilment.deliveryAddress` | group | optional | — | — | — | — | `createGuestFnbOrder` body |
| Building `fulfilment.deliveryAddress.building` | text field | optional | — | max length 200 | — | — | `createGuestFnbOrder` body |
| Unit `fulfilment.deliveryAddress.unit` | text field | optional | — | max length 60 | — | — | `createGuestFnbOrder` body |
| Emirate `fulfilment.deliveryAddress.emirate` | text field | optional | — | max length 60 | — | — | `createGuestFnbOrder` body |
| Directions `fulfilment.deliveryAddress.directions` | text area | optional | — | max length 500 | — | — | `createGuestFnbOrder` body |
| Cutlery `fulfilment.cutlery` | toggle | optional | off | — | — | — | `createGuestFnbOrder` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createGuestFnbOrder` body |
| ID `lines[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createGuestFnbOrder` body |
| Menu item `lines[].menuItemId` | picker: choose a menu item | required | — | — | shows names, sends the id | — | `createGuestFnbOrder` body |
| Quantity `lines[].quantity` | stepper or slider | required | — | min 1; max 20 | — | — | `createGuestFnbOrder` body |
| Modifier options `lines[].modifierOptionIds` | multi-picker: choose modifier options | optional | — | — | — | — | `createGuestFnbOrder` body |
| Note `lines[].note` | text area | optional | — | max length 200 | — | Free text to the kitchen. Allergy notes belong here and are surfaced prominently on the ticket. | `createGuestFnbOrder` body |
| Quoted total `quotedTotal` | money field | required | — | Checked against the server's recomputation — a guest is never trusted with a price, and a mismatch is refused rather than silently corrected in either direction. | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the guest was shown. Checked against the server's recomputation — a guest is never trusted with a price, and a mismatch is refused rather than silently corrected in either … | `createGuestFnbOrder` body |
| Payment method `paymentMethod` | radio group | optional | — | Card · Wallet · Room charge · Add to tab | — | — | `createGuestFnbOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createGuestFnbOrder` body |

**Sent by *Leave restaurant waitlist*** (`leaveRestaurantWaitlist`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Note `note` | text area | optional | — | max length 300 | — | Why, where the guest or host gave a reason. Optional. | `leaveRestaurantWaitlist` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Where you are (location)**: First step for in-venue ordering. A scanned code arrives with the link and is claimed at once; the guest is never shown the code. Fallback when the QR is damaged: a short text box for the human-readable location code ("Lounger B-14", "Table 12"), never a list of every location. At a seated event the seat comes from the guest's ticket and is offered prefilled ("Deliver to Row H, Seat 4?"), not typed. Where several outlets serve the location, the guest picks the outlet next. *(source: contracts/satellite/fnb.yaml#claimLocationSession / F11 step 1 / DI-288 / DI-291 / TRACKER Workshops/Actions row 56)*
- **Party size (at a table)**: Asked only when the scanned location is a table (optional, minimum 1). Not asked at a lounger, cabana or seat, which have no table visit. *(source: contracts/satellite/fnb.yaml#/components/schemas/LocationSession / DI-1000)*
- **How you get it (order type)**: Offer only what the chosen outlet supports. To my table, seat or lounger (orderingMethod appToTable, needs the location step). Collect from the counter (appToCollect, with collectionEnabled). Delivery to an address (deliveryEnabled). An outlet whose method is counterOnly or notAvailable shows its menu to read, with no Add buttons and the line "Order at the counter". The guest never sees the words "mode", "fulfilment" or "ordering method". *(source: contracts/satellite/fnb.yaml#/components/schemas/GuestOrderingMethod / contracts/satellite/fnb.yaml#/components/schemas/FnbDeliveryPolicy / DI-205)*
- **When (collection time or delivery window)**: ASAP first, labelled with the policy's minutes ("About 25 min"; delivery "About 45 min"), then fixed slots of slotMinutes. Times are in the venue's time zone. Only open slots are listed, because a slot closes when the kitchen cannot make it. No date picker for same-day in-venue orders; a date appears only for advance takeaway or delivery. Up to three quick choices share one screen. *(source: contracts/satellite/fnb.yaml#listFulfilmentSlots / contracts/satellite/fnb.yaml#/components/schemas/FnbDeliveryPolicy / DI-1001)*
- **Delivery address**: Building (required), unit, emirate and directions (500 characters at most). Emirate is a choice from the outlet's emiratesServed, not free text. Checked before the menu, so an address outside the area never reaches a basket. *(source: contracts/satellite/fnb.yaml#/components/schemas/GuestOrderFulfilment / DI-1039)*
- **Cutlery**: A checkbox "Add cutlery", off by default. Shown only where the outlet's cutleryOptIn is on. *(source: contracts/satellite/fnb.yaml#/components/schemas/GuestOrderFulfilment / contracts/satellite/fnb.yaml#/components/schemas/FnbDeliveryPolicy)*
- **Quantity per dish**: 1 to 20 per line. The stepper stops at 20 and says why; a quantity of 0 removes the line. *(source: contracts/satellite/fnb.yaml#/components/schemas/CreateGuestOrderLine)*
- **Note for the kitchen**: Optional, 200 characters at most, one per dish, placeholder "Allergies or requests". Allergy notes belong here, and the kitchen ticket shows them prominently. *(source: contracts/satellite/fnb.yaml#/components/schemas/CreateGuestOrderLine)*
- **Payment**: Card or digital wallet only on the guest web. "Add to my table's bill" appears only where the location session joined an open table visit and the outlet runs a tab. Room charge is not offered. *(source: contracts/spine/orders.yaml#createPayment / R080 / contracts/satellite/fnb.yaml#createGuestFnbOrder / decided 2 October 2026 by Chinmay (CHG-NOTE-004))*
- **Book a table (date, time, party size)**: One screen: restaurant, date, time and party size, plus an optional note for allergies or requests. No table picking (a host seats the party on the night) and no duration field (the venue sets it). Name and contact are prefilled from the signed-in profile. *(source: contracts/satellite/fnb.yaml#createTableReservation / REV3-8 / DI-1001 / DI-1048 / DI-688)*
- **Join the waitlist (party size, seating)**: Party size and a seating preference: Any (default), Indoor, Outdoor, Bar, Booth, High chair needed. Two screens at most. *(source: contracts/satellite/fnb.yaml#joinRestaurantWaitlist / DI-1001)*
- **Where the outlet is (an outlet property)**: Inside the venue (needs an admission ticket) or Standalone (no ticket). Ordering from an inside-the-venue outlet needs admission (a ticket or a claimed location in the venue); a standalone restaurant outside the venue sells takeaway and delivery without a ticket. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

#### Outputs: what the screen shows and produces

**Shown**

**Where you can eat now** (card list, from `listDiningOutlets`): Outlets open now: photo, name, zone, cuisine, how to order ("Order to your seat", "Collect", "Counter only") and closing time; a wait only when the outlet reports one. No ids.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Zone | text | — |
| Cuisine | list or chips (count when long) | — |
| Ordering method | chip: Table service, App to table, App to collect, Counter only, Not available | How a guest may order at this outlet. Varies within one venue, so it is per outlet rather than a venue setting. |
| Closes at | 1 Oct 2026, 14:30 | — |
| Estimated wait minutes | 1,234 | From current kitchen ticket volume, not a fixed figure. Null where the outlet has no kitchen display reporting ticket status — an invented … |
| Image | the image or video | — |

**Menu** (detail panel, from `getGuestMenu`): Sections in the outlet's order, "Lunch menu until 16:00" from `inForceUntil`; each dish with photo, price and allergens; a dish's modifier groups come inside the menu (no venue-wide modifier list). Sold out stays in place, greyed.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| In force until | 1 Oct 2026, 14:30 | When this menu stops applying. The client shows it, because a guest browsing breakfast at 10:55 should know. |
| Sections | list or chips (count when long) | — |

**Your order** (cart panel, from `getFnbDeliveryPolicy`): Lines with choices and a 1-20 stepper, the kitchen note per dish; for delivery the fee, the free-delivery threshold and the minimum order.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Outlet | the name it points at, never the id | — |
| Collection enabled | yes / no (icon or chip) | — |
| Delivery enabled | yes / no (icon or chip) | — |
| Collection point | text | — |
| Collection hold minutes | 1,234 | — |
| Asap collection minutes | 1,234 | — |
| Asap delivery minutes | 1,234 | — |
| Slot minutes | 1,234 | — |
| Minimum order | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Delivery fee | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Free delivery above | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Radius km | 1,234.5 | — |
| Emirates served | list or chips (count when long) | — |
| Cutlery opt in | yes / no (icon or chip) | Cutlery only when asked for, as in the design. |

**Order placed** (banner, from `getGuestOrderStatus`): The order number large, where it is going, the ready time as a clock time; then tracking (WEB-038 / GST-025).

| Shows | Format | Notes |
|---|---|---|
| Order | text | — |
| Order number | text | — |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Estimated ready at | 1 Oct 2026, 14:30 | — |
| Is ready for collection | yes / no (icon or chip) | — |
| Lines | list or chips (count when long) | Per-line status. A guest waiting on one dish should see which. |
| Name | text | — |
| Quantity | 1,234 | — |
| Status | chip: Received, Preparing, Ready, Served, Recalled, Cancelled | — |

**Needs an admission ticket** (banner, from `createGuestFnbOrder`): **Where the outlet is (decided by Chinmay, 2 October 2026; DEC-070, DEC-206).** An outlet is *Inside the venue (needs an admission ticket)* or *Standalone (no ticket)* (`Outlet.admissionContext`). Ordering from an inside-the-venue outlet needs admission: a ticket, or a location claimed inside the venue; `createGuestFnbOrder` refuses 403 `entry-ticket-required` otherwise, and the screen says so …

| Shows | Format | Notes |
|---|---|---|
| Order | text | — |
| Order number | text | Short and readable. It gets called out across a counter. |
| Fulfilment | chip: Collect, Deliver to location, Table service, Deliver to address | How the order reaches the guest, in the request's terms: `collect` is `GuestOrderFulfilment.mode` `collection`; `deliverToAddress` is … |
| Delivery label | text | Where it is going, as a runner would read it. |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Estimated ready at | 1 Oct 2026, 14:30 | — |
| Collection point | text | — |
| Table label | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Pay (primary button) | `createGuestFnbOrder` POST `/guest-orders` | CreateGuestOrderRequest | GuestOrderResult | 402 Payment required or declined; 403 The outlet is inside the venue (`tenancy.Outlet.admissionContext` `insideVenue`) and the guest holds no valid admission ticket for the venue today …; 409 An item became unavailable … | emits `fnb.kitchenTicketCreated` |
| Book a table (secondary button) | `createTableReservation` POST `/table-reservations` | TableReservation | TableReservation | 409 No cover available for that party size at that time. The reason names the constraint — a party of eight refused when a party of two would fit … | opens modal first |
| Change or cancel booking (secondary button) | `updateTableReservation` PATCH `/table-reservations/{reservationId}` | TableReservation | TableReservation | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Join the waitlist (secondary button) | `joinRestaurantWaitlist` POST `/waitlist` | RestaurantWaitlist | RestaurantWaitlist | — | opens modal first |
| Leave restaurant waitlist (destructive button) | `leaveRestaurantWaitlist` POST `/waitlist/{entryId}/leave` | inline | RestaurantWaitlist | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The party is already `seated`, `walkedAway` or `noShow`. Names the entry's current status. | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Outlet list**: Only outlets open now, so a guest is never sent to a restaurant that closed an hour ago. Each card shows photo, name, zone, cuisine, how to order ("Order to your seat", "Collect", "Counter only") and the closing time. A wait estimate ("About 12 min") appears only when the outlet reports one; with none, show nothing and never invent a figure. *(source: contracts/satellite/fnb.yaml#listDiningOutlets / contracts/satellite/fnb.yaml#/components/schemas/DiningOutlet)*
- **Menu**: Sections in the outlet's own order. Below the menu name, a small line from inForceUntil ("Lunch menu until 16:00"), because a guest browsing breakfast at 10:55 should know. Each dish shows photo, name as written (dish names are not translated), description, price and its allergens, always visible on the card. A dish with no allergens says "No allergens declared"; the list is never left out. *(source: contracts/satellite/fnb.yaml#getGuestMenu / contracts/satellite/fnb.yaml#/components/schemas/GuestMenu / F11 step 2 / DI-975)*
- **Sold out**: A dish with isAvailable false stays in its place, greyed, with a "Sold out" badge, its reason when given ("Back at 15:00"), and Add disabled. It is never hidden or filtered out by default. On guest screens the word is "Sold out", never "86" or "Out of stock". *(source: contracts/satellite/fnb.yaml#getGuestMenu / R110)*
- **Prices**: Prices are formatted with the menu's currency and currencyScale: AED with 2 decimals, and BHD or KWD with 3, the third decimal never rounded. *(source: contracts/satellite/fnb.yaml#/components/schemas/GuestMenu / DI-306)*
- **Basket**: Each line lists its choices ("Hot, Burnt butter rice"), with a quantity stepper and the line price. For delivery the basket adds the delivery fee, "Add AED 46.00 more for free delivery" while below freeDeliveryAbove, and the minimum order. The total shown is the quotedTotal sent with the order. *(source: DI-1039 / DI-1050 / contracts/satellite/fnb.yaml#/components/schemas/CreateGuestOrderRequest)*
- **Order placed**: The order number is large, because it gets called out across a counter. Below it: where the order is going ("Lounger B-14 · Pool deck") or the collection point, and the ready time as a clock time. The guest goes straight on to tracking (WEB-038). *(source: contracts/satellite/fnb.yaml#/components/schemas/GuestOrderResult / R152)*
- **Table booked**: Confirmed at once, with no basket: "Table for 4 · Thu 15 Oct · 19:30 · Oasis Bistro", then "No card needed", "Change" and "Cancel booking". Cancelling is free. *(source: REV3-8 / DI-1048 / contracts/satellite/fnb.yaml#updateTableReservation)*
- **Deposit (only when the venue enabled it)**: Shown only when the booking comes back awaitingDeposit. Show the amount and how it was worked out ("AED 100.00 per guest × 6 = AED 600.00"), whether the card is only authorised or charged now, "Free to cancel until Wed 14 Oct, 19:30" (refundableUntil), and what happens on a late cancel or a no-show. The deposit goes to the cart as its own line, and a countdown shows the 15-minute hold. Never draw a fixed AED 100: amount and basis are venue settings. *(source: REV3-8b / DI-1049 / contracts/satellite/fnb.yaml#/components/schemas/TableReservationDeposit / contracts/spine/orders.yaml#/components/schemas/DiningDepositPolicy / R169)*
- **On the waitlist**: The quoted wait ("About 25 min") and the status in plain words ("You're on the list", then "Your table is ready, come to the host stand by 19:42" when notified). "Leave the waitlist" is always visible. *(source: contracts/satellite/fnb.yaml#/components/schemas/RestaurantWaitlist / R073)*
- **Receipt**: The F&B order has its own payment step and its own receipt; it does not join the guest's ticket receipt (DI-293's one receipt does not apply to F&B). *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Scan the code / Enter lounger or table number**: Claims the location. Success shows "Ordering to Lounger B-14". Where an open table visit exists, the guest joins it ("You've joined Table 12, one bill for the table"). A refusal names one cause: code expired ("This code has expired, scan the code on your lounger again"), location out of service, or nothing delivers here, which offers counter collection instead. *(source: contracts/satellite/fnb.yaml#claimLocationSession / F11 step 1 / F48 step 4)*
- **Add**: A dish with no modifier groups goes straight into the basket. A dish with groups opens the modifier side panel (WEB-037). The panel appears whenever groups are attached; there is no venue on/off setting. *(source: REV3-9 / DI-1050)*
- **Place order and pay**: The order and the total the guest saw go to the server, which recomputes the price; then payment by card or wallet. The kitchen sees the order only once payment succeeds, unless it goes on an open table tab. The button reads "Pay AED 86.00", never "Send to the kitchen" (see corrections). While payment is unresolved the screen says "Checking your payment", and the kitchen is not told. *(source: contracts/satellite/fnb.yaml#createGuestFnbOrder / F11 step 3 / F11 step 4)*
- **Reserve**: Books the table. With no deposit the confirmation shows straight away, with nothing in the basket. With a deposit, the deposit line goes into the cart and the guest pays through the normal checkout; the booking is confirmed once the payment is authorised. *(source: contracts/satellite/fnb.yaml#createTableReservation / contracts/spine/orders.yaml#addCartLine / REV3-8 / REV3-8b)*
- **Join waitlist / Leave waitlist**: Joining confirms at once, with no payment and no basket. Leaving asks "Give up your place? The next party moves up.", names the restaurant and party size, and cannot be undone; joining again puts the party at the back. *(source: contracts/satellite/fnb.yaml#leaveRestaurantWaitlist / R073 / REV3-8)*

**Data it reads**: `getFnbDeliveryPolicy` (onLoad, Minimum order, delivery fee and area); `listFulfilmentSlots` (onLoad, Collection times or delivery windows still open); `getGuestMenu` (onLoad, The menu a guest sees); `listDiningOutlets` (onLoad, Where a guest can eat, right now); `listDeliveryLocations` (onLoad, Where an order can be delivered); `getGuestOrderStatus` (onLoad, Track an order Only when signed in (decided 2 October 2026 …)

**Where the user goes next**

- → `WEB-037` Menu Item Detail: *Menu Item Detail*; carries `outletId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Content resolves in place. |
| Error (`?state=error`) | Could not load. **The rest of the site is unaffected.** |
| Empty, first run (`?state=emptyFirstRun`) | No outlet takes orders here now. Names when the next one opens; a counter-only outlet's menu can still be read. |
| Empty, no results (`?state=emptyNoResults`) | No outlet open now matches: says so, with the next opening time. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **The offline banner shows.** The menu already loaded stays with its age. Ordering, claiming a table and booking wait for the connection — an order placed offline is food nobody is making. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither a location code nor a seat reference supplied; 409 An item became unavailable, the quoted total no longer matches, the location session expired, or the outlet stopped taking orders.; 409 Code expired or unknown, the location is out of service, or no outlet currently delivers to it — a cabana is useless as an address if nothing serves it.; 409 No capacity, or the product is not … |

#### Edge cases to draw

- **A dish sells out between browsing and paying**: The order is refused (itemUnavailable) with the dishes named. Mark those basket lines "Sold out" and offer to remove them; the rest of the basket stays. Never drop a line silently. *(source: contracts/satellite/fnb.yaml#createGuestFnbOrder)*
- **The price changed (menu switch, promotion expired)**: The order is refused (priceChanged). Show the new total and ask the guest to confirm it. The order is never placed silently at a different price. *(source: contracts/satellite/fnb.yaml#/components/schemas/CreateGuestOrderRequest)*
- **The menu changes over while the guest browses (breakfast to lunch at inForceUntil)**: Reload the new menu and flag basket lines that are no longer on it. The guest removes them before paying. *(source: contracts/satellite/fnb.yaml#/components/schemas/GuestMenu)*
- **The location session expired (the guest moved, or came back the next day)**: "Scan the code where you're sitting again." The basket is kept. *(source: F11 step 1 / contracts/satellite/fnb.yaml#/components/schemas/LocationSession)*
- **Delivery rule broken**: Below the minimum: checkout stays off with "Minimum order AED 90.00, add AED 12.50". Outside the area: "We don't deliver to this address" with Change address and Switch to takeaway. Slot just closed: "That time just filled, pick another". Delivery or collection switched off: that option disappears. *(source: DI-1039 / contracts/satellite/fnb.yaml#createGuestFnbOrder)*
- **The outlet refuses the order after payment (past last orders, out of an ingredient)**: Tracking shows "Cancelled, refunded to your card" straight away, not after ten minutes. If one dish fails after the order was accepted, only that line is cancelled and refunded. *(source: F11 step 5)*
- **The scanned code belongs to a different venue from the one the guest picked**: Offer to switch to that venue ("You're at Aqua Park, switch?"). The venue choice is the guest's, remembered on the device and changeable. *(source: R267 / designer default)*
- **The guest is somewhere nothing delivers**: Delivery to their spot is not offered at all. Offer counter collection instead. The failure comes before the order, not after the payment. *(source: F48 step 4 / contracts/satellite/fnb.yaml#/components/schemas/DeliveryLocation)*
- **Table not available**: The two refusals read differently. noTableForPartySize: "No table for 8 at 19:30, try a smaller party or another time". outletFullAtTime: "Fully booked at 19:30". Both offer other times. *(source: contracts/satellite/fnb.yaml#createTableReservation)*
- **The deposit is not paid within the hold**: After 15 minutes the table is released. Say so, and offer to book again. *(source: contracts/satellite/fnb.yaml#/components/schemas/TableReservationDeposit / R169)*
- **Leaving a waitlist after being seated**: Refused, with the current status named ("You've already been seated"). *(source: contracts/satellite/fnb.yaml#leaveRestaurantWaitlist)*
- **Offline**: The menu already loaded stays, with its age. The pay button reads "Offline, ordering is paused". Claiming a location and booking wait for the connection. *(source: screens/P01-guest-web-storefront.yaml#WEB-036 / F11 step 1)*

#### Consistency with other screens

- Match `GST-024`: Must be functionally identical (DI-970, DI-1084): the same order types, sold-out and allergen display, delivery rules, refusals and wording. Mobile layout may differ (DI-1086). In the app, table booking and the waitlist are on GST-070; on the web they are here.
- Match `GST-070`: The table booking, deposit and waitlist wording must match word for word ("No card needed", the deposit terms, "Leave the waitlist").
- Match `WEB-037`: The modifier side panel opened by Add is WEB-037's panel; the basket line format comes from it.
- Match `WEB-038`: Order placed leads to WEB-038, carrying the order; the order number shows the same way on both.
- Match `POS-021`: The till shows the same menu in force (getGuestMenu, staff audience since 1 October). A dish sold out at the till is sold out here immediately.
- Match `KIT-007`: The guest status board shows the same order number a guest sees here.
- Match `WEB-010`: The deposit line shows in the shared cart with the reservation date (23SEP-9). Table bookings with no deposit never appear in the cart.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Aqua Park (order prefix AQP), Dubai, times in GST
outlets:
- name: Bite & Go
  zone: Wave Pool
  cuisine:
  - Grill
  - Wraps
  howToOrder: Collect
  wait: About 12 min
  closes: '18:00'
- name: Pool Bar
  zone: Pool deck
  howToOrder: Order to your lounger
  wait: null
  closes: '19:00'
- name: Oasis Bistro
  zone: Marina side
  howToOrder: Table service and bookings
  closes: '23:00'
location: Lounger B-14 · Pool deck (served by Pool Bar)
menu: Lunch menu · until 16:00
items:
- name: Chicken shawarma wrap
  price: AED 38.00
  allergens:
  - gluten
  - sesame
  - milk
- name: Halloumi fries
  price: AED 29.00
  allergens:
  - milk
- name: Fattoush salad
  price: AED 32.00
  allergens:
  - gluten
  soldOut: true
  reason: Back at 15:00
- name: Burnt butter rice
  price: AED 18.00
  allergens:
  - milk
- name: Mango lassi
  price: AED 22.00
  allergens:
  - milk
- name: Fresh lemon mint
  price: AED 19.00
  allergens: []
basketLine: Chicken shawarma wrap ×2 · Hot, Extra garlic sauce · AED 88.00
deliveryPolicy:
  fee: AED 15.00
  freeFrom: AED 200.00
  minimum: AED 90.00
  emirates:
  - Dubai
  collectionHold: 20 min
  asapCollection: 25 min
  asapDelivery: 45 min
order:
  number: AQP-104582
  guest: Aisha Rahman
  to: Lounger B-14 · Pool deck
  readyAbout: '13:25'
  total: AED 86.00
reservation:
  outlet: Oasis Bistro
  party: 4
  when: Thu 15 Oct 2026, 19:30
  note: One guest has a sesame allergy
  status: Booked
  card: No card needed
depositExample:
  enabled: true
  basis: per guest
  amount: AED 100.00
  fromPartySize: 6
  party: 6
  total: AED 600.00
  freeToCancelUntil: Wed 14 Oct 2026, 19:30
  lateCancelOrNoShow: Deposit kept
waitlist:
  outlet: Oasis Bistro
  party: 3
  seating: Outdoor
  quotedWait: About 25 min
```

#### Permissions

- `getFnbDeliveryPolicy` → `PRODUCT_VIEW` (read) · staff, guest
- `listFulfilmentSlots` → no permission · guest
- `getGuestMenu` → no permission · guest, staff
- `listDiningOutlets` → no permission · guest
- `claimLocationSession` → no permission · guest
- `createGuestFnbOrder` → no permission · guest
- `listDeliveryLocations` → no permission · guest, staff
- `getGuestOrderStatus` → no permission · guest
- `createTableReservation` → no permission · guest
- `joinRestaurantWaitlist` → `ORDER_MODIFY` (operate) · staff, guest
- `leaveRestaurantWaitlist` → `ORDER_MODIFY` (operate) · staff, guest
- `addCartLine` → no permission · guest, partner, staff
- `updateTableReservation` → no permission · guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

22 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.9 | APIs shall support menu retrieval, order creation, order status, kitchen status, inventory updates and promotions. | Developer & API Management | CONTRACTED | `getGuestMenu` |
| 19.2.50 | Location Delivery - System shall support delivery to guest location. | Guest Mobile App & Branding | CONTRACTED | `claimLocationSession` |
| 4.6.23 | Allow guests to place orders through mobile applications. | Bundles and Promotions | CONTRACTED | `claimLocationSession` |
| 4.6.24 | Allow guests to order by scanning QR codes. | Bundles and Promotions | CONTRACTED | `claimLocationSession` |
| 4.6.25 | Allow ordering directly from guest seats. | Bundles and Promotions | CONTRACTED | `claimLocationSession` |
| 4.6.26 | Deliver orders to tables, seats, cabanas or designated locations. | Bundles and Promotions | CONTRACTED | `claimLocationSession` |
| 19.2.47 | Mobile Food Ordering - System shall support mobile food ordering. | Guest Mobile App & Branding | CONTRACTED | `createGuestFnbOrder` |
| 4.9.10 | The system should be able to create,modify and delete new/existing reservations | Bundles and Promotions | CONTRACTED | `createTableReservation` |
| 4.9.13 | The system should be able to allow table reservations in advance according to the requirements. | Bundles and Promotions | CONTRACTED | `createTableReservation` |
| 7.5.1 | Event scheduled services such as table booking or meal delivery can be managed by the system (sales only) | F&B POS | CONTRACTED | `createTableReservation` |
| 13.3.11 | APIs shall support reservation creation, modification, cancellation, waitlists and availability checks. | Developer & API Management | CONTRACTED | `createTableReservation` |
| 19.2.19 | Add-On Purchases - System shall support add-on purchases. | Guest Mobile App & Branding | CONTRACTED | `addCartLine` |
| … 10 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- In takeaway, delivery and café menus, Add opens a side panel for the dish: choose-one options (spice level, drink size, ice), optional priced add-ons (sides, dips, toppings, leave-outs) and quantity; total updates live and the basket line lists the choices. Shown whenever the item has modifier groups (no toggle). *(agreed · rev 3 design review 29 Sep 2026, REV3-9 · 9. Add-ons and modifiers for F&B menu items · DI-1050)*
- Dining deposit hold is a venue option, off unless enabled in Venue Management; amount and basis (per guest, per table, percentage) are venue configuration, never a hard-coded AED 100. Show the deposit step only when enabled. *(agreed · rev 3 design review 29 Sep 2026, REV3-8b · 8. deposit hold flow · DI-1049)*
- Table reservations and the waitlist do not go into the cart: after date, time and party size the guest gets a confirmation straight away ("no card needed"). *(agreed · rev 3 design review 29 Sep 2026, REV3-8 · 8. Unable to complete the table booking flow · DI-1048)*
- Delivery basket shows the fee (AED 15, free from AED 200) and "Add AED X more for free delivery"; below AED 90 checkout is refused; outside Dubai shows "We don't deliver to this address" with Change address / Switch to takeaway. A slot can close mid-flow: "That time just filled". *(agreed · design review 29 Sep 2026, 5. Takeaway and delivery (WEB-036) · DI-1039)*
- On the one-decision-per-screen layout, information blocks (notes, "what happens next", "what's included") stay on the screen before them and up to three quick choices share one screen. Table reservation and deposit hold become 1 screen; waitlist, takeaway, delivery, private dining enquiry 2; dinner deals 2 (party size with date/time). *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): Steps with nothing to decide · DI-1001)*
- **Open question.** Resources: meeting-room booking (headcount, duration, time slot, room, add-ons tea/coffee/snacks), modelled on House of Wisdom. Merchandise: browse, cart with add/remove quantity, pickup or doorstep delivery. F&B: outlet/menu browsing; collect at counter, curbside, doorstep or priority delivery. *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Resources, Merchandise, F&B) · DI-690)*
- **Open question.** Dining has two flows: book a table (date, time, group size, seating-area preference, occasion, allergy/special-request notes) and order food (delivery or pickup location, items, checkout). *(open · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Dining) · DI-688)*
- Decision (raised by Aishwarya): F&B and retail/merchandise online sale are optional back-office-enabled modules; where enabled, the whole purchase (browse, cart, checkout, pickup-at-venue or ship-to-guest) completes inside TICVAI — guests are never sent to download a separate app. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-505)*
- Out of scope: buying F&B with no admission ticket (entering only to buy food). *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-292)*
- Seated events: guest chooses pickup or delivery to seat (seat known from the booking). Open venues (beach, water park): a physical QR at each seat/location is scanned to say where food is delivered. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-288)*
- F&B: browse outlets and order; pickup location shown automatically per outlet, with delivery as an extra option (needs guest location) when the venue uses the platform's F&B module. Retail follows the same pickup/delivery model. *(client request · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-205)*

Also apply: 1 for P01 · In-venue Services, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-036` · status **review** · provenance client-verified
- Prototype (rev 3 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Summit Peaks → header 'At the venue' → Order food (table ordering)*. Differences: Prototype splits in-venue table ordering (At the venue) from takeaway/delivery ordering (a booking flow with a delivery-area and slot check). Table reservation and waitlist (in YAML apis) are booking flows at Saffron Table. **The prototype sends the order with "Send to the kitchen" and no payment step: wrong here.** The contract takes payment before the kitchen sees a guest order unless the outlet runs a tab, and F11 puts the pay step (4) before the kitchen (5); the design shows the pay step …
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0066 *The on-sale waiting room sits at the edge, apart from the ride queue* (`docs/adr/0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (70), with its required mark, default, format and its error state (400, 402, 403, 404, 409, 412, 422).
- [ ] Every output is drawn (43 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-036?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Pay, Book a table, Change or cancel booking, Join the waitlist, Leave restaurant waitlist.
- [ ] Every transition is wired: `WEB-037`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 11 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 12 edge case(s) from the process notes are drawn.
- [ ] The 3 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-037` Menu Item Detail

**What is in it, and what may be changed.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | In-venue Services · wave 1 · needs the `fnb` module |
| Block | Block A · task APP-WEB-WEB-037 |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): One dish from the outlet's guest menu, with its modifiers and allergens (CHG-SGU-018) |
| Offline | **The offline banner shows.** The dish already loaded stays, with a note that it may be out of date and its allergens in full. Ordering is refused — availability changes by the minute. |
| Opens with | `outletId` (deepLink), `menuItemId` (deepLink) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a … |
| Route | `/menu-item-detail` |

**What the spec says about it.** **Allergens are read here more often than anywhere else in the platform**, and a guest checking one on a phone browser is the ordinary case rather than the exception. **Rev 3 (decided 29 September, rev 3 REV3-9).** The modifier side panel is drawn here (no api change); the *F&B add-ons & modifiers (on/off)* toggle is dropped: modifiers show when the item has attached groups.

**From the Food, Beverage & Retail process.** One dish: what is in it, what may be changed, and the side panel where the guest chooses before adding. Allergens are read here more often than anywhere else in the platform, usually on a phone browser. In-venue ordering shows it as a dialog and takeaway or delivery as a side panel (the same thing rendered twice). The one thing to get right: allergens are complete and visible, and they update as options are chosen.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The guest menu carries a dish's allergens as one flat list. The package's own Allergen model separates "contains" from "may contain" and carries vegetarian, vegan and halal flags, and the rev 3 prototype dish dialog … (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): The screen takes only outletId on entry, with no dish identifier, so a shared or deep link cannot open a particular dish. (CHG-SGU-018); listModifierGroups drives the screen (a "Every modifier group" table with scopePath, the pattern "list, select, act"), and the empty state … (CHG-SGU-018).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| At | date and time picker | — | — | `getGuestMenu` ?at |
| Language | language picker | — | — | `getGuestMenu` ?language |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Choose-one groups (spice level, drink size, ice)**: A group whose minimum is above 0 is required and labelled "Required · choose 1". A group with a maximum of 1 renders as radio choices. The default option (isDefault) is preselected. Add to order stays off until every required group has a choice, and says which one is missing. *(source: contracts/satellite/fnb.yaml#/components/schemas/ModifierGroup / DI-1050 / TRACKER Workshops/Actions row 87)*
- **Optional add-ons and leave-outs (sides, dips, toppings, "No onions")**: Checkboxes, with "Choose up to 3" from the group's maximum; further boxes disable at the limit. A priced option shows "+ AED 6.00"; a zero-priced one shows no price. An option that is unavailable stays visible, greyed, marked "Sold out", never hidden. *(source: contracts/satellite/fnb.yaml#/components/schemas/ModifierGroup / DI-1050)*
- **Quantity**: 1 to 20; the stepper sits at the foot of the panel beside the live total. *(source: contracts/satellite/fnb.yaml#/components/schemas/CreateGuestOrderLine)*
- **Note for the kitchen**: Optional, 200 characters, placeholder "Allergies or requests"; printed prominently on the kitchen ticket. *(source: contracts/satellite/fnb.yaml#/components/schemas/CreateGuestOrderLine / DI-688)*

#### Outputs: what the screen shows and produces

**Shown**

**The dish** (detail panel, from `getGuestMenu`): The dish `menuItemId` resolved inside the outlet's `getGuestMenu`: photo, name, description, price, its modifier groups (min and max per group) and allergens. Until the guest menu carries the Allergen object, "Contains" is drawn from the current list and "May contain" and the diet badges (vegetarian, vegan, halal) are drawn as pending (CHG-SGU-024).

| Shows | Format | Notes |
|---|---|---|
| Outlet | the name it points at, never the id | — |
| Menu | the name it points at, never the id | — |
| Name | text | — |
| In force until | 1 Oct 2026, 14:30 | When this menu stops applying. The client shows it, because a guest browsing breakfast at 10:55 should know. |
| Currency | text | — |
| Currency scale | 1,234 | — |
| Sections | list or chips (count when long) | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Allergens**: The dish's allergens as icon plus word from the fourteen declarable allergens, in the guest's language, and never collapsed behind a tap. When a chosen option adds an allergen, it joins the list live, marked with its source ("Eggs, from Extra garlic sauce"). A dish with none says "No allergens declared". *(source: contracts/satellite/fnb.yaml#/components/schemas/AllergenCode / contracts/satellite/fnb.yaml#/components/schemas/ModifierGroup / F11 step 2)*
- **Live total**: Dish price plus the chosen options' price changes, times quantity, at the menu's currency scale. It updates on every tap. *(source: DI-1050 / contracts/satellite/fnb.yaml#/components/schemas/GuestMenu)*
- **Basket line it produces**: The dish name, then the choices in group order separated by commas ("Hot, Burnt butter rice"), then quantity and price. *(source: DI-1050 / REV3-9)*
- **Sold-out dish**: Still opens, so the guest can read the allergens. Add is disabled, and the reason is shown when given. *(source: contracts/satellite/fnb.yaml#getGuestMenu)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Add to order**: Adds the line with its choices and closes the panel. The basket count in the header updates. Nothing goes to the server until the order is placed (on WEB-036). *(source: screens/P01-guest-web-storefront.yaml#WEB-037 / DI-1050)*
- **Cancel / close**: Discards the choices; the basket is unchanged. *(source: screens/P01-guest-web-storefront.yaml#WEB-037)*

**Data it reads**: `getGuestMenu` (onLoad, The menu a guest sees)

**What opens over it**

- drawer *Add, on an item with modifier groups attached*: **A side panel of choices**: choose-one groups, priced optional add-ons within their limits, and quantity; the basket line lists the choices. Shown whenever the item has groups attached (`listModifierGroups`); there is no tenant on/off toggle (decided 29 September, rev 3 REV3-9).

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Content resolves in place. |
| Error (`?state=error`) | Could not load. **The rest of the site is unaffected.** |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing here yet for this venue.** Names what turns it on rather than showing an empty panel. |
| Permission denied (`?state=emptyNoAccess`) | Never shown: a menu is public and browsing a dish needs no sign-in. |
| Offline (`?state=offline`) | **The offline banner shows.** The dish already loaded stays, with a note that it may be out of date and its allergens in full. Ordering is refused — availability changes by the minute. |

#### Edge cases to draw

- **A required group has every option sold out**: The dish cannot be ordered. Show it as "Sold out" with Add disabled, rather than a panel the guest cannot complete. *(source: contracts/satellite/fnb.yaml#/components/schemas/ModifierGroup / designer default)*
- **The server refuses the choices (modifierConstraintUnmet) at order time**: Reopen the panel for that line with the group highlighted. *(source: contracts/satellite/fnb.yaml#/components/schemas/GuestOrderProblem)*
- **Offline**: The dish stays, with "May be out of date" and its allergens in full. Add is disabled. *(source: screens/P01-guest-web-storefront.yaml#WEB-037)*

#### Consistency with other screens

- Match `GST-061`: Functionally identical: same panel, rules, allergen display and basket-line format (DI-970, REV3-9).
- Match `KSK-016`: The same allergen rendering on the kiosk card.
- Match `POS-021`: The same modifier groups and limits the till applies. A guest-built line and a till-built line read the same on the kitchen ticket.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
dish: Chicken shawarma wrap · AED 38.00 · allergens gluten, sesame, milk
groups:
- name: Spice level
  rule: Required · choose 1
  options:
  - Mild (default)
  - Medium
  - Hot
- name: Add-ons
  rule: Choose up to 3
  options:
  - Extra garlic sauce + AED 6.00 (adds eggs)
  - Burnt butter rice + AED 18.00
  - Gluten-free wrap + AED 10.00
  - Halloumi + AED 9.00 (Sold out)
- name: Leave out
  rule: Optional
  options:
  - No onions
  - No pickles
quantity: 2
note: No sesame please, allergy
liveTotal: AED 88.00
basketLine: Chicken shawarma wrap ×2 · Hot, Extra garlic sauce · AED 88.00
```

#### Permissions

- `getGuestMenu` → no permission · guest, staff

**A refused user sees:** Never shown: a menu is public and browsing a dish needs no sign-in.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.9 | APIs shall support menu retrieval, order creation, order status, kitchen status, inventory updates and promotions. | Developer & API Management | CONTRACTED | `getGuestMenu` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- In takeaway, delivery and café menus, Add opens a side panel for the dish: choose-one options (spice level, drink size, ice), optional priced add-ons (sides, dips, toppings, leave-outs) and quantity; total updates live and the basket line lists the choices. Shown whenever the item has modifier groups (no toggle). *(agreed · rev 3 design review 29 Sep 2026, REV3-9 · 9. Add-ons and modifiers for F&B menu items · DI-1050)*
- Modifiers can be free or chargeable with minimum/maximum selection rules; combo meals support component selection with upgrade options at additional cost. *(client request · MoM 18 Aug 2026, 4.4 Menu, Product & Recipe Management · DI-328)*

Also apply: 1 for P01 · In-venue Services, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A82** Design the F&B Command Center suite: a real-time cross-outlet sales/operations dashboard, the F&B Stock Command Center (stock value, low-stock alerts, recipe-based consumption, batch/wastage tracking, replenishment … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'recipe')*
- **A83** Design the Menu & Product Command Center and Menu Builder (recipe/product mapping alerts, drag-and-drop POS layout, chargeable/free modifiers with min/max rules, combo meals with upgrade options) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'menu & product')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-037` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *At the venue → Order food → tap a dish; Takeaway/Delivery → 'Add' opens the modifier side panel*. Differences: Two renderings of the same thing (dialog in-venue, side panel in takeaway/delivery).

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-037?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-038` F&B – Order Tracking

**Watch it being made, and see the table bill; it is paid at the table.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | In-venue Services · wave 1 · needs the `fnb` module |
| Block | Block A · task APP-WEB-WEB-038 |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | statusTracker (compact density): `getGuestOrderStatus` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **The offline banner shows.** The last status stays with its age ("Preparing, 2 min ago"); nothing refreshes until the connection returns. |
| Opens with | `subjectId` (session), `orderId` (deepLink), `sessionId` (deepLink), `venueId` (session) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a … |
| Route | `/fandb--order-tracking` |

**What the spec says about it.** **Order to ready is the kitchen's number; ready to collected is the counter's.** A guest watching a status that never changes walks to the counter. **Renamed 31 August** from *F&B — Order Tracking*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest.

**From the Food, Beverage & Retail process.** Order tracking on the web: the guest watches the order the kitchen is actually making, and at a table sees the one bill for the sitting. Order to ready is the kitchen's time; ready to collected is the counter's. The one thing to get right: the status always moves with the kitchen. No timer counts down against nothing, and when it is ready the guest knows exactly where to go or that it is on its way.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table bill (getGuestBill) is read through a TableSession id (/table-sessions/{sessionId}/bill), but guests now claim with claimLocationSession and hold a LocationSession with a visitId. (CHG-SGU-024)

**Fixed on main** (the package already carries these; draw what it says): "Claim table session" is the primary action of a tracking screen, on WEB-038 and GST-025. (CHG-SGU-018); The purpose says "settle the bill", but no payment operation is declared, and orders put on a table tab need a way to be paid. (CHG-SGU-018).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Can a guest pay the table's bill from the web or app, or is the bill view read-only?** → Drawn default accepted: Read-only bill with "Ask your server to pay"; no pay button. *(decided by Chinmay, 2026-10-02; DEC-073 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**The guest order status** (detail panel, from `getGuestOrderStatus`)

| Shows | Format | Notes |
|---|---|---|
| Order | text | — |
| Order number | text | — |
| Status | chip: Ordered, Accepted, In preparation, Ready, Served, Collected… | The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or … |
| Estimated ready at | 1 Oct 2026, 14:30 | — |
| Is ready for collection | yes / no (icon or chip) | — |
| Lines | list or chips (count when long) | Per-line status. A guest waiting on one dish should see which. |

**The bill** (detail panel, from `getGuestBill`): The table bill, read through the table session the guest holds. A guest who claimed with `claimLocationSession` holds a visit, not a table session, and cannot read it yet (CHG-SGU-024); "Pay at the table" until a guest payment of the visit's bill exists.

| Shows | Format | Notes |
|---|---|---|
| Visit | text | — |
| Covers | 1,234 | — |
| Lines | list or chips (count when long) | — |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Service charge | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Discount amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Status steps**: The steps adapt to how the order reaches the guest. Collection: Ordered → Being made → Ready to collect → Collected. To a seat, lounger or cabana: Ordered → Being made → On its way → Delivered. At a table: Ordered → Being made → Served. "Ordered" reads "Waiting for the kitchen to accept" until the order is accepted. Cancelled and Refunded replace the steps with one plain message. *(source: contracts/satellite/fnb.yaml#/components/schemas/FnbOrderStatus / contracts/satellite/fnb.yaml#/components/schemas/GuestOrderResult / F11 step 6)*
- **Ready to collect**: When ready for collection, the screen turns into a pickup card: the order number very large, the collection point ("Hatch 3, Bite & Go") and how long it is held ("Held for 20 minutes"). *(source: contracts/satellite/fnb.yaml#/components/schemas/GuestOrderStatus / contracts/satellite/fnb.yaml#/components/schemas/FnbDeliveryPolicy)*
- **Ready time**: A clock time in the venue's time zone ("Ready about 13:25"), from the kitchen's estimate. With no estimate, show nothing rather than a guess. *(source: contracts/satellite/fnb.yaml#getGuestOrderStatus / contracts/satellite/fnb.yaml#/components/schemas/DiningOutlet)*
- **Per-dish status**: Each dish with its own state (Received, Being made, Ready, Served; Cancelled struck through with "refunded"), so a guest waiting on one dish sees which. A dish recalled by the kitchen reads "Being made". *(source: contracts/satellite/fnb.yaml#/components/schemas/GuestOrderStatus / contracts/satellite/fnb.yaml#/components/schemas/KitchenTicketStatus)*
- **Table bill**: Only where the order is on a table visit. Every line ordered at the table this sitting, by app or by a server, as one bill: covers, lines, service charge, VAT, discounts and total. *(source: contracts/satellite/fnb.yaml#getGuestBill)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **(automatic) refresh**: The status is polled while the screen is open; no refresh button is needed. Changes also go to the in-venue notifications feed (WEB-046). *(source: screens/P01-guest-web-storefront.yaml#WEB-038)*
- **Order more**: Back to WEB-036 with the same location, so the next order goes to the same place. *(source: F11 step 1 / designer default)*

**Data it reads**: `getGuestOrderStatus` (onInterval, The order's status (ordered, accepted, in preparation …); `getGuestBill` (onLoad, The bill for the guest's table)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Loading the order. |
| Error (`?state=error`) | Could not load. **The rest of the site is unaffected.** |
| Empty, first run (`?state=emptyFirstRun`) | The order is not found or was refunded (a cold link): says which, with the way back to ordering. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **The offline banner shows.** The last status stays with its age ("Preparing, 2 min ago"); nothing refreshes until the connection returns. |

#### Edge cases to draw

- **The runner cannot find the guest**: The order is held at the outlet and the guest is told to collect it: "We couldn't find you at Lounger B-14, collect it at Pool Bar." It is not thrown away. *(source: F11 step 7)*
- **The outlet refused the order before accepting it**: "The kitchen couldn't take your order, refunded to your card", shown at once. *(source: F11 step 5)*
- **One dish became unavailable after acceptance**: That dish shows "Cancelled, AED 29.00 refunded"; the rest carries on. *(source: F11 step 5)*
- **Signal lost**: The last status stays, with its age ("Updated 3 min ago"), and is never presented as current. *(source: F11 step 6 / screens/P01-guest-web-storefront.yaml#WEB-038)*
- **The link is opened days later**: The final state is shown (Collected, Delivered or Refunded) with one way on (order food again). Never a 404. *(source: screens/P01-guest-web-storefront.yaml#WEB-038)*

#### Consistency with other screens

- Match `GST-025`: Functionally identical, with the same step labels and messages (DI-970).
- Match `KIT-007`: Same order number and the same moment of "Ready" as the guest status board. The guest screen never runs ahead of the kitchen.
- Match `WEB-036`: Entered from Order placed.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
order:
  number: AQP-104582
  outlet: Bite & Go
  collect: Hatch 3
  readyAbout: '13:25'
  held: 20 min
lines:
- name: Chicken shawarma wrap ×2
  status: Being made
- name: Mango lassi
  status: Ready
- name: Halloumi fries
  status: Cancelled · AED 29.00 refunded
tableBill:
  outlet: Oasis Bistro
  table: Table 12
  covers: 4
  subtotal: AED 412.00
  serviceCharge: AED 41.20
  vat: AED 22.66
  total: AED 475.86
```

#### Permissions

- `getGuestOrderStatus` → no permission · guest
- `getGuestBill` → no permission · guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P01 · In-venue Services, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-038` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *At the venue → Order food → 'Send to the kitchen'*. Differences: No bill or settle-the-bill view (YAML getGuestBill, 'settle the bill').
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-038?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 5 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-039` Venue Map & Wait Times

**Where things are, and how long they take.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | In-venue Services · wave 1 · needs the `queue` module |
| Block | Block A · task APP-WEB-WEB-039 |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listQueues` reads the population and `getVenueMap` reads one of them — list, select, act |
| Offline | **The offline banner shows.** A map and route graph already loaded stay usable, so directions do not need a signal. Wait times show their last reading marked out of date, never as live — a queue length from an hour ago sends a guest to the wrong ride. With no map loaded yet, the screen asks the … |
| Opens with | `mapId` (deepLink), `venueId` (session) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a … |
| Route | `/venue-map-and-wait-times` |

**What the spec says about it.** **`getVenueMap` was already `guest` audience and offline-capable and no web screen drew it.** A map in a browser is a map. **Drawn 26 August** — `Seat Board 3.dc.html` frame `seat-3c`. **The frame names this screen on its own face**, which is the first pack to do that: the earlier F&B, POS and Retail boards had to be hand-assigned by purpose after three derivation attempts produced nonsense. **A board that says what it draws removes the guess entirely.**

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** The venue map with live wait times, for a guest at the venue without the app. Block A. The 30 September build draws a 3D view with the 2D plan one tap away and walking directions; the screen must keep a stale wait time visible but marked, never hidden and never shown as live.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No map3dUnavailable or weak-GPS state is drawn. (CHG-SGU-026)

**Fixed on main** (the package already carries these; draw what it says): "Venue id" text field, "Open only" toggle and an "Every queue" table. (CHG-GST-003).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Version | number field | — | — | `getVenueMap` ?version |
| Draft | toggle | off | Staff only, and it needs `VENUE_MAP_MANAGE`, because the draft is unfinished work that must never reach a guest. | `getVenueMap` ?draft |
| Draft | toggle | off | Staff only, and it needs `VENUE_MAP_MANAGE`, as on `getVenueMap`. | `getVenueMapGraph` ?draft |
| Step free only | toggle | off | — | `getVenueMapGraph` ?stepFreeOnly |
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |
| Open only | toggle | off | — | `listQueues` ?openOnly |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Waits** (card list, from `listQueues`): Wait times by category (rides, dining). The venue is the one the guest picked on Home (`venueId` from the session, audit R267), never typed. Was the generated table 'Every queue'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Name | in the reader's language | — |
| Kind | chip: Standby, Single rider, Fast pass, Virtual, Accessible, Group only… | 5.6.x. A ride has several queues and the model had one. |
| Operating windows | list or chips (count when long) | When the queue runs, which is not when the venue is open. A ride closing an hour early for maintenance leaves a queue accepting guests for … |

**Venue Map & Wait Times** (card list)

**Detail** (detail panel)

**The venue map graph** (detail panel, from `getVenueMapGraph`)

| Shows | Format | Notes |
|---|---|---|
| Map | the name it points at, never the id | — |
| Generated at | 1 Oct 2026, 14:30 | — |
| Nodes | list or chips (count when long) | — |
| Edges | list or chips (count when long) | — |
| Components | 1,234 | How many disconnected parts. One is the answer for a park. |

**The wait time** (detail panel, from `getWaitTimes`): **A stale wait time is shown with a caveat, never hidden** (decided 28 September, audit R080 (b)): where `WaitTime.isStale` is true the minutes stay on screen marked out of date with their `asOf` time, as queue.yaml says.

| Shows | Format | Notes |
|---|---|---|
| Queue name | in the reader's language | — |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**The venue map** (detail panel, from `getVenueMap`)

| Shows | Format | Notes |
|---|---|---|
| Map | grouped details | A park map, or a floor plan. Several per venue — a guest on the second floor should not be shown the ground floor's toilets. |
| Points | list or chips (count when long) | — |
| Paths | list or chips (count when long) | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **wait time**: Per ride on its map pin and in the list ("41 min"); a stale reading keeps its minutes greyed with "as of 14:05". A closed ride says Closed, not 0 min. Long waits are coloured against nearby shorter ones so the guest can choose. *(source: contracts/satellite/queue.yaml#getWaitTimes; screens/P01-guest-web-storefront.yaml#WEB-039 (wait time notes, R080 b); DI-204; DI-682)*
- **map**: 3D view by default where the venue supplied a model, 2D plan one tap away ("Same plan, drawn two ways"); points for rides, dining, shops, restrooms, first aid and gates with category filters. *(source: screens/P01-guest-web-storefront.yaml#WEB-039 wireframe.prototype; DI-891; DI-203)*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Directions**: From the chosen gate or "you are here" (with location permission) to a point, as a route on the map and a step list; the route graph works offline once loaded. *(source: screens/P01-guest-web-storefront.yaml#WEB-039 states.offline; AUDIT-29SEP (turn-by-turn banner))*

**Data it reads**: `getVenueMap` (onLoad, A map with its points and paths); `getVenueMapGraph` (onLoad, The navigation graph, ready to route over); `getWaitTimes` (onLoad, Wait times across a venue); `listQueues` (onLoad, List queues)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Content resolves in place. |
| Error (`?state=error`) | Could not load. **The rest of the site is unaffected.** |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing here yet for this venue.** Names what turns it on rather than showing an empty panel. |
| Empty, no results (`?state=emptyNoResults`) | No attraction of the category picked; the other categories stay. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **The offline banner shows.** A map and route graph already loaded stay usable, so directions do not need a signal. Wait times show their last reading marked out of date, never as live — a queue length from an hour ago sends a guest to the wrong ride. With no map loaded yet, the screen asks the guest to reconnect. |

#### Edge cases to draw

- **The venue has no 3D model, or the device cannot render it**: Opens on the 2D plan with no error. *(source: DI-1103 (our reading adds a 2D fallback))*
- **Location is denied or weak**: Directions start from a chosen gate; no blue dot. *(source: DI-1103 (weak-GPS state))*

#### Consistency with other screens

- Match `GST-021`: Same pins, categories and wait-time treatment; the app adds live walking navigation.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
waits:
- The Drop · 41 min
- Vortex · 25 min
- Lazy River · 5 min
- Falcon Coaster · Closed
staleNote: as of 14:05
```

#### Permissions

- `getVenueMap` → `VENUE_MAP_VIEW` (read) · staff, guest
- `getVenueMapGraph` → `VENUE_MAP_VIEW` (read) · staff, guest
- `getWaitTimes` → no permission · guest, public
- `listQueues` → `QUEUE_VIEW` (read) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.55 | Interactive Venue Map - System shall provide interactive venue maps. | Guest Mobile App & Branding | CONTRACTED | `getVenueMap` |
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A visual venue map highlights long-queue rides vs low-queue alternatives so operations can redirect guests, e.g. a notification suggesting a nearby ride with a shorter wait. *(client request · MoM 7 Sep 2026, 4.17 AI guest flow optimization · DI-682)*
- In the app a guest with a valid ticket browses rides, sees the current wait (e.g. 60 minutes), joins the virtual queue for their party and gets a return window (e.g. 4:50-5:00 PM). Missing the window can auto-release the slot. *(client request · MoM 7 Sep 2026, 4.13 Virtual Queue - Mobile Journey & Configuration · DI-675)*
- Live wait time per ride/attraction shown in the app (e.g. "41 minutes"), fed by the venue's third-party camera/sensor system through a TICVAI API. *(agreed · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-204)*
- **Open question.** Customisable venue map showing attractions, dining, retail and restrooms. Qossai: define image/format guidance for tenant map uploads; benchmark is the Kidzania app's interactive 3D-style map. Final guidance still open. *(open · MoM 10 Aug 2026, 4.4 Venue Map, Queueing, F&B, Retail & Parking · DI-203)*

Also apply: 1 for P01 · In-venue Services, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-039` · status **review** · provenance client-verified · **Drawn by Claude Design on `Seat Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Prototype (rev 3 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Summit Peaks → header 'At the venue' → Map & waits (3D view, with the 2D plan one tap away)*. Differences: Prototype adds turn-by-turn walking directions and navigation mode. The map has a 3D view / 2D plan switch ("Same plan, drawn two ways"); no map3dUnavailable or weakGps state is drawn.
- Derived from `wireframes/reference/Seat Board 3.dc.html`
- Client design-board frames: `Seat Board 3.dc.html#seat-3c`
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-039?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-040` Virtual Queue

**Hold a place without standing in one.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | In-venue Services · wave 1 · needs the `queue` module |
| Block | Block A · task APP-WEB-WEB-040 |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | statusTracker (compact density): `getWaitingGuest` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **The offline banner shows.** The guest's place stays on screen with its age, so they can see they hold it. Joining and leaving need the connection — a place taken offline is a place nobody else can see. |
| Opens with | `subjectId` (session), `entryId` (deepLink) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a … |
| Route | `/virtual-queue` |

**What the spec says about it.** **The point of a virtual queue is that the guest walks away** — which works the same in a browser tab as in an app. **Rev 3 (decided 29 September, rev 3 GAP-D2).** The web and app waves of this capability differ; they are aligned to one wave once the client picks it (open, client to choose).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The browser version of the ride virtual queue: the guest sees each ride's wait, joins for their party, and then watches their place - position, parties ahead, estimated call time, then the call and the return window - and can leave. It is the ride queue (Q1), never the on-sale waiting room. The one thing to get right: the return window is honest and recalculates live, and the "called" state is unmissable.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Web and app waves of the virtual queue differ (open, client to choose) (CHG-SGU-025)

**Fixed on main** (the package already carries these; draw what it says): Join waitlist / Leave waitlist (catalogue sold-out waitlist) sit on the virtual queue screen with purpose "Join a virtual queue" (CHG-SGU-021).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which wave ships the virtual queue on web and app (they currently differ)?** → Drawn default accepted: Draw both identical; label nothing as wave-specific. *(decided by Chinmay, 2026-10-02; DEC-142 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `getWaitTimes` ?category |

**Form: Join queue** (modal, opened by *Join queue*; *Join queue* calls `joinQueue`, *Cancel* sends nothing)

**Collects what `joinQueue` sends before it is called.** Required: `id`, `queueId`, `partySize`, `recordedAt`. Optional: `entitlementId`, `partyHeightsCm`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `joinQueue` body |
| Queue `queueId` | picker: choose a queue | required | — | — | shows names, sends the id | — | `joinQueue` body |
| Party size `partySize` | number field | required | — | min 1 | — | — | `joinQueue` body |
| Entitlement `entitlementId` | text field | optional | — | — | — | Fast Pass or priority entitlement. Owned by Product & Entitlement — this contract references it and never defines it. | `joinQueue` body |
| Party heights cm `partyHeightsCm` | list of values (chips) | optional | — | — | — | Where the queue has a height requirement. Refusing here is far better than refusing at the ride, in front of a child who has already waited. | `joinQueue` body |
| Accessibility need declared `accessibilityNeedDeclared` | toggle | optional | off | — | — | The party declares an accessibility need (5.6.7; decided 29 September, build pass). | `joinQueue` body |
| Promotion code `promotionCode` | text field | optional | — | max length 64 | — | A promotion code the guest holds, checked against the lane's `QueueFastPass.promotionIds` (5.6.34). | `joinQueue` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `joinQueue` body |

Errors to draw in the form: 409 Already in this queue, at the cross-queue limit, party exceeds the maximum, queue is paused or closed, or a party member does not meet the height requirement. (QueueJoinProblem)

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Join (party size, heights, accessibility, promotion code)**: Party size stepper (max per the queue); heights per child only where the ride has a height rule, so the refusal happens here and not at the ride; "Someone in our party has an accessibility need" checkbox; promotion code field only where a lane grants privilege by promotion. *(source: contracts/satellite/queue.yaml#joinQueue / contracts/satellite/queue.yaml#/components/schemas/QueueFastPass)*

#### Outputs: what the screen shows and produces

**Shown**

**The waiting guest** (detail panel, from `getWaitingGuest`)

| Shows | Format | Notes |
|---|---|---|
| Queue name | in the reader's language | — |
| Party number | 1,234 | What the guest sees and what appears on signage. |
| Status | chip: Waiting, Called, Redeemed, Expired, No show, Cancelled… | — |
| Estimated call at | 1 Oct 2026, 14:30 | — |
| Called at | 1 Oct 2026, 14:30 | — |
| Return window ends at | 1 Oct 2026, 14:30 | — |
| Redeemed at | 1 Oct 2026, 14:30 | — |
| Admitted count | 1,234 | — |

**The wait time** (detail panel, from `getWaitTimes`)

| Shows | Format | Notes |
|---|---|---|
| Queue name | in the reader's language | — |
| Status | chip: Open, Paused, Closed, At capacity | — |
| Wait minutes | 1,234 | Null where the queue is closed or no estimate is available. |
| Is stale | yes / no (icon or chip) | The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as … |
| Height requirement cm | 1,234 | — |
| Zone | text | — |
| As of | 1 Oct 2026, 14:30 | When the figure was produced — the queue's `waitTimeAsOf`. |

**Virtual Queue** (card list)

**Detail** (detail panel)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Join queue (primary button) | `joinQueue` POST `/waiting-guests` | JoinQueueRequest | WaitingGuest | 409 Already in this queue, at the cross-queue limit, party exceeds the maximum, queue is paused or closed, or a party member does not meet the height requirement. (QueueJoinProblem) | opens modal first |
| Leave queue (secondary button) | `leaveQueue` DELETE `/waiting-guests/{entryId}` | — | — | 409 Already called or redeemed | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Place in queue**: "Party 214 - 18 parties ahead - expected around 16:50" with the time the estimate was updated; when called: full-width "Your turn - return by 17:05 to Falcon Coaster entrance" with a countdown. *(source: contracts/satellite/queue.yaml#getWaitingGuest / DI-675 / DI-679)*
- **Wait times list**: Ride, wait minutes, source label (Live sensor / Estimated / Set by staff) and "updated 3 min ago"; stale readings shown with a caveat, never hidden. *(source: contracts/satellite/queue.yaml#getWaitTimes / screens/P02-guest-mobile-app.yaml#GST-022)*
- **Express upsell**: On a long wait, an offer to buy an express/fast-lane ticket with its price; not re-offered once declined. *(source: DI-683 / DI-962)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Join queue**: Returns position and party number; one active entry per guest per queue (a second join on the same ride is refused with "You are already in this queue"). *(source: contracts/satellite/queue.yaml#joinQueue)*
- **Leave queue**: Confirm "Give up your place in the Falcon Coaster queue?"; frees the place. *(source: contracts/satellite/queue.yaml#leaveQueue)*

**Data it reads**: `getWaitingGuest` (onInterval, The guest's place and the call to come forward, read on …); `getWaitTimes` (onLoad, Wait times across a venue)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Content resolves in place. |
| Error (`?state=error`) | Could not load. **The rest of the site is unaffected.** |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing here yet for this venue.** Names what turns it on rather than showing an empty panel. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **The offline banner shows.** The guest's place stays on screen with its age, so they can see they hold it. Joining and leaving need the connection — a place taken offline is a place nobody else can see. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already called or redeemed; 409 Already in this queue, at the cross-queue limit, party exceeds the maximum, queue is paused or closed, or a party member does not meet the height requirement. (QueueJoinProblem) |

#### Edge cases to draw

- **Missed return window**: Shows "Your place has been released" with Join again where the queue is open. *(source: DI-675 / contracts/satellite/queue.yaml#/components/schemas/QueueEntryStatus)*
- **Queue paused or closed (ride stopped)**: Paused keeps the place with "Ride paused - your place is kept"; closed releases everyone with the venue's message and expected reopening. *(source: contracts/satellite/queue.yaml#setQueueStatus)*
- **Ride is sold out for a performance-based attraction**: The waitlist (join/leave) is a different thing - "tell me if a place frees up" - and must be labelled so, not as a queue. *(source: contracts/spine/catalogue.yaml#joinWaitlist)*

#### Consistency with other screens

- Match `GST-023`: Same states, wording and countdown on the app.
- Match `SCN-003`: At the ride the VQ guest is scanned within their window in a VQ lane, never merged into the VIP line.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
entry:
  ride: Falcon Coaster
  party: 4
  partyNumber: 214
  ahead: 18
  expected: '16:50'
  window: 16:50-17:05
waits:
- ride: Falcon Coaster
  wait: 60 min
  source: Live sensor
- ride: Wave Rider
  wait: 25 min
  source: Set by staff
  updated: 12 min ago
```

#### Permissions

- `joinQueue` → no permission · guest
- `getWaitingGuest` → no permission · guest
- `leaveQueue` → no permission · guest
- `getWaitTimes` → no permission · guest, public

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.35 | Virtual Queue Management - System shall support virtual queues. | Guest Mobile App & Branding | CONTRACTED | `joinQueue` |
| 2.13.31 | Queue Management Integration | Ticketing Sales | CONTRACTED | `joinQueue` |
| 5.6.10 | Support eligibility validation based on ticket type, membership, age, height restrictions, package entitlement, waiver status, or loyalty tier. | F&B & Guest Management | CONTRACTED | `joinQueue` |
| 5.6.30 | Expose APIs for third-party systems, kiosks, apps, CRM, and partners. | F&B & Guest Management | CONTRACTED | `joinQueue` |
| 5.6.32 | Allow self-service kiosks to support queue reservation, lookup, cancellation, and status viewing. | F&B & Guest Management | CONTRACTED | `joinQueue` |
| 19.2.36 | Queue Status Tracking - System shall provide queue status tracking. | Guest Mobile App & Branding | CONTRACTED | `getWaitingGuest` |
| 5.6.23 | Allow guests and staff to cancel reservations according to policy. | F&B & Guest Management | CONTRACTED | `leaveQueue` |
| 19.2.37 | Estimated Waiting Time - System shall provide estimated waiting times. | Guest Mobile App & Branding | CONTRACTED | `getWaitTimes` |
| 5.6.3 | Display queue lengths, wait times, throughput, capacity utilization, occupancy, and customer flow metrics. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.15 | Continuously calculate and display estimated waiting times. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |
| 5.6.16 | Allow guests to view their live queue position and estimated service time. | F&B & Guest Management | CONTRACTED | `getWaitTimes` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Proactively upsell an express/fast-lane ticket to a guest facing a long wait (e.g. "buy express ticket for [amount]"). *(agreed · MoM 7 Sep 2026, 4.17 Revenue lever / 5. Key Decisions · DI-683)*
- The return time shown to a VQ guest must be genuinely accurate and recalculate dynamically from real-time conditions across all three tiers, not a static estimate given at booking. *(agreed · MoM 7 Sep 2026, 4.15 Waiting-time honesty & recalculation · DI-679)*
- In the app a guest with a valid ticket browses rides, sees the current wait (e.g. 60 minutes), joins the virtual queue for their party and gets a return window (e.g. 4:50-5:00 PM). Missing the window can auto-release the slot. *(client request · MoM 7 Sep 2026, 4.13 Virtual Queue - Mobile Journey & Configuration · DI-675)*

Also apply: 1 for P01 · In-venue Services, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-040` · status **review** · provenance client-verified
- Prototype (rev 3 (30 September build), verified 2026-10-01, match exact): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Summit Peaks → header 'At the venue' → Virtual queue*
- ADR-0066 *The on-sale waiting room sits at the edge, apart from the ride queue* (`docs/adr/0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-040?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Join queue, Leave queue.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-041` Parking – Reserve & Pay

**Reserve a facility before arriving.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | In-venue Services · wave 1 · needs the `access` module |
| Block | Block A · task APP-WEB-WEB-041 |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · the venue's theme |
| Pattern | listDetail (compact density): `listParkingFacilities` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **The offline banner shows.** A reservation already confirmed stays on screen with its plate and car park. Reserving, paying and changing the plate need the connection. |
| Opens with | `entitlementId` (deepLink), `venueId` (session), `cartId` (session) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared link, a scanned code and a … |
| Route | `/parking--reserve-and-pay` |

**What the spec says about it.** **A guest reserves parking on the drive, from whatever is open on their phone.** Requiring an install for a car park is requiring an install to arrive. **Renamed 31 August** from *Parking — Reserve & Pay*. **A guest surface is one product with two renderings** — a screen named differently on web and app is two screens to a developer and one journey to a guest. **Rebound 28 September** (decided 28 September, audit R166): parking is sold through the normal cart and checkout (`addCartLine`, `checkoutCart`, `createPayment`), so the entitlement gets its `orderId`; the guest no longer calls `createParkingEntitlement`, which the order service issues at payment. No live availability; a full car park is the `soldOutForDay` refusal. **Rev 3 (decided 29 September, rev 3 GAP-D2).** The web and app waves of this capability differ; they are aligned to one wave once the client picks it (open, client to choose).

**Known gaps.** Parking goes through the basket (R166); checkout is the basket's. Payment is the basket's, after checkout (R166).

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Reserve and pay for parking before arriving, through the normal basket. Block A. There is no live space count in the first release: never show free bays; a full car park is the "full for that day" refusal when the guest tries.

**Fixed on main** (the package already carries these; draw what it says): The prototype shows live free-bay counts and pays with "Reserve and pay" directly. (CHG-SGU-020); Separate "Check out" and "Pay" buttons and a "Save parking entitlement" form exposing status. (CHG-GST-003).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which wave do web and app parking ship in?** → Drawn default accepted: Draw both now; the wave is the client's pick. *(decided by Chinmay, 2026-10-02; DEC-122 / CHG-NOTE-007)*

#### Inputs: what the user enters or picks

**Form: Add parking to my cart** (modal, opened by *Add parking to my cart*; *Add to cart* calls `addCartLine`, *Cancel* sends nothing)

**Collects what `addCartLine` sends before it is called.** Required: `variantId` (the car park's parking product), `quantity`. Optional: `performanceId`, `attributes` (the plate). A 409 `soldOutForDay` is shown as **the car park is full** for that day — capacity reached, not a live count (decided 28 September, audit R166). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Variant `variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `addCartLine` body |
| Quantity `quantity` | number field | required | — | min 1 | — | — | `addCartLine` body |
| Performance `performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `addCartLine` body |
| Booked window `bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `addCartLine` body |
| Starts at `bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `addCartLine` body |
| Ends at `bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `addCartLine` body |
| Recommendation `recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `addCartLine` body |
| Table reservation `tableReservationId` | picker: choose a table reservation | optional | — | A booking that is not awaiting a deposit is refused 422 `depositNotDue`. | shows names, sends the id | A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's … | `addCartLine` body |
| Seats `seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). | — | At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on … | `addCartLine` body |
| Resource hold `resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and … | `addCartLine` body |
| Parent line `parentLineId` | picker: choose a parent line | optional | — | — | shows names, sends the id | For an add-on attaching to a ticket already in the cart. Removing the parent removes the child — a locker with no admission is not a sale. | `addCartLine` body |
| Attributes `attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `addCartLine` body |
| Transport `attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `addCartLine` body |
| Route `attributes.transport.routeId` | picker: choose a route | required | — | — | shows names, sends the id | The `transport.TransportRoute`. | `addCartLine` body |
| From station `attributes.transport.fromStationId` | picker: choose a from station | required | — | — | shows names, sends the id | Boarding station, a stop of the route. | `addCartLine` body |
| To station `attributes.transport.toStationId` | picker: choose a to station | required | — | — | shows names, sends the id | Alighting station, a later stop of the route. | `addCartLine` body |
| Passenger type code `attributes.transport.passengerTypeCode` | text field | optional | — | pattern `^[a-z][a-zA-Z0-9]{0,31}$` | — | The fare table's passenger type (`adult`, `child`, ...). Required on a one-way trip. | `addCartLine` body |
| Pass type `attributes.transport.passTypeId` | picker: choose a pass type | optional | — | — | shows names, sends the id | Pass purchase only. The `transport.PassType` bought for this station pair. | `addCartLine` body |
| Pass entitlement `attributes.transport.passEntitlementId` | picker: choose a pass entitlement | optional | — | — | shows names, sends the id | A seat reserved with a pass already owned. The line is zero-priced and validated against the pass (stations covered, an entry left, within validity). | `addCartLine` body |

Errors to draw in the form: 403 The performance's on-sale waiting room is on and the request has no valid admission token (ADR-0066).; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The booked window is missing, not allowed or the wrong length for the variant (`windowRequired`, `windowNotAllowed`, `windowLengthMismatch`; rev 3 REV3-13), or … (CartProblem)

**Form: Change plate** (modal, opened by *Change plate*; *Save* calls `updateParkingEntitlement`, *Cancel* sends nothing)

**The plate only.** `updateParkingEntitlement` with the new plate; a guest never sets a status.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Plate number `plateNumber` | text field | optional | — | — | — | Personal data, under the same rules as `ParkingEntitlement.plateNumber`. | `updateParkingEntitlement` body |
| Plate country `plateCountry` | text field | optional | — | — | — | — | `updateParkingEntitlement` body |
| Status `status` | segmented control | optional | — | Revoked | — | The only status a caller may set. Every other move is the server's. | `updateParkingEntitlement` body |

Errors to draw in the form: 400 Validation failed

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **car park**: Cards per car park with its price and walking time (Premium by the gate, Standard East, Accessible bays, Coach and minibus). *(source: sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html (parking options); contracts/spine/access.yaml#listParkingFacilities)*
- **plate number**: Asked only for a car park on the ANPR model (plate pushed to the barrier whitelist), with the emirate or country; changeable later until entry. Not asked where security checks the QR. *(source: DI-300; DI-316; contracts/spine/access.yaml#updateParkingEntitlement)*
- **date**: The visit date, prefilled from tickets already in the basket. *(source: designer default)*

#### Outputs: what the screen shows and produces

**Shown**

**Car parks** (card list, from `listParkingFacilities`): The venue's car parks by name; no live free-bay count in the first release. The venue is the one the guest picked on Home (`venueId` from the session, audit R267), never typed. Was the generated table 'Every parking facility'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |

**Parking — Reserve & Pay** (card list)

**Detail** (detail panel)

**The selected parking facility** (detail panel, from `listParkingFacilities`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add parking to my cart (primary button) | `addCartLine` POST `/carts/{cartId}/lines` | AddCartLineRequest | Cart | 403 The performance's on-sale waiting room is on and the request has no valid admission token (ADR-0066).; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The … | opens modal first |
| Change plate (secondary button) | `updateParkingEntitlement` PATCH `/parking-entitlements/{entitlementId}` | UpdateParkingEntitlementRequest | ParkingEntitlement | 400 Validation failed | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **parking pass**: After payment, the pass with car park, date, plate (if any) and the QR the barrier or security reads. *(source: contracts/spine/orders.yaml#addCartLine ("the parking entitlement is issued at payment"))*

**What each action does** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **Add to basket**: Adds the car park's parking product as a basket line; paid with the tickets in one checkout. *(source: contracts/spine/orders.yaml#addCartLine; R166)*

**Data it reads**: `listParkingFacilities` (onLoad, Car parks at a venue, and how each integrates)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Content resolves in place. |
| Error (`?state=error`) | Could not load. **The rest of the site is unaffected.** |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing here yet for this venue.** Names what turns it on rather than showing an empty panel. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: the car parks are the venue's, with no filter a guest sets. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that … |
| Offline (`?state=offline`) | **The offline banner shows.** A reservation already confirmed stays on screen with its plate and car park. Reserving, paying and changing the plate need the connection. |
| Sold out for day (`?state=soldOutForDay`) | **The car park is full.** `addCartLine` refused the parking line with `soldOutForDay`: issued entitlements have reached the facility's capacity for that day. Shown only then — there is no live space count in the first release, so the screen never promises spaces before the guest tries (decided 28 September, audit R166). |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 No capacity, or the product is not sellable on this channel (`notSellableOnChannel`). (CartProblem); 422 The booked window is missing, not allowed or the wrong length for the variant (`windowRequired`, `windowNotAllowed`, `windowLengthMismatch`; rev 3 REV3-13), or … (CartProblem) |

#### Edge cases to draw

- **The car park is full for the day**: "Premium is full on Fri 2 Oct" with the other car parks; shown only after trying. *(source: screens/P01-guest-web-storefront.yaml#WEB-041 states.soldOutForDay)*

#### Consistency with other screens

- Match `GST-027`: Same car parks and the same full-for-the-day message.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
carParks:
- name: Premium · by the gate
  sub: Under cover · 2 minutes on foot
  price: AED 80
- name: Standard · East
  sub: Open air · 7 minutes on foot
  price: AED 40
- name: Accessible bays
  sub: Beside the accessible entrance
  price: Free
plate: Dubai · K 48213
```

#### Permissions

- `listParkingFacilities` → `PARKING_CONFIGURE` (configure) · staff, guest
- `addCartLine` → no permission · guest, partner, staff
- `updateParkingEntitlement` → no permission · guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data; decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-4)). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that …

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.19 | Add-On Purchases - System shall support add-on purchases. | Guest Mobile App & Branding | CONTRACTED | `addCartLine` |
| 1.1.130 | The solution shall support donation solicitation during the customer checkout process. Functional Requirements Donation prompt at checkout. Optional donation acceptance. Multiple donation campaign … | Ticketing Catalogue | CONTRACTED | `addCartLine` |
| 2.12.1 | The system should have the ability for order entry: - Select an item to place on an order. - Indicate quantity of item selected - Apply a name to an order (e.g. Smith Party). Each admission on the … | Ticketing Sales | CONTRACTED | `addCartLine` |
| 2.12.29 | In order to improve Guest experience, it shall be possible to pre-order as many product or services as possible, including multi-park pass. | Ticketing Sales | CONTRACTED | `addCartLine` |
| 3.4.1 | The payment can be done upfront or at exit. | Admission and Access | PARKED | data `ParkingFacility` |
| 7.4.12 | The system can manage Parking | F&B POS | PARKED | data `ParkingFacility` |
| 7.4.30 | For each PLU, it is possible to manage Parking tickets which can have a fixed rate per day or per hour. | F&B POS | PARKED | data `ParkingFacility` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Parking is barrier integration, not space counting: one configuration screen chooses a model - no integration (TICVAI QR checked by security), ANPR (guest enters a plate at checkout, pushed to the barrier whitelist) or QR handoff to the barrier. Pay-per-hour parking is out of scope. *(agreed · MoM 14 Aug 2026, 10 · DI-316)*
- Parking supports three models: (1) no integration — TICVAI QR verified manually by security; (2) plate number at checkout pushed to the parking system's ANPR whitelist; (3) TICVAI QR passed to the barrier. Hourly pay-on-exit parking stays on the parking system's own POS. *(agreed · MoM 14 Aug 2026, 10. Parking Integrations · DI-300)*

Also apply: 1 for P01 · In-venue Services, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A41** Analyse the integration effort for third-party systems (parking, ride/queue-timing sensors, etc.) to consume TAIS's own standardised API as the default integration model *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'parking')*
- **A42** Design the parking module to support both native QR-based validation (own solution) and a plate-number capture field for future ANPR/third-party parking integrations *(Softlabs Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'parking')*

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the *Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has no dark or light mode: the venue's theme applies on every device setting. Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (11, CMS-002, CMS-004, CMS-104); Theme (27, CMS-005, ADM-016); Fonts (5, CMS-003); Header (5, CMS-009); Navigation (17, CMS-009); Footer (website) (15, CMS-009); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001, ADM-424); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-041` · status **review** · provenance client-verified
- Prototype (rev 3 (30 September build), verified 2026-10-01, match partial): `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, view *Summit Peaks → header 'At the venue' → Parking*. Differences: Shows live free-bay counts, which the YAML says it does not have (no live availability; full = soldOutForDay). Pays directly with 'Reserve and pay' rather than through cart and checkout (R166). Also a plate field in the cabana/party flows. **Do not draw live free-bay counts or "Reserve and pay"**: no live count in the first release, and parking goes through the basket (R166) (CHG-SGU-020).
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0037 *A lock holds one statement, not a transaction* (`docs/adr/0037-what-may-be-inside-a-lock.md`)
- ADR-0066 *The on-sale waiting room sits at the edge, apart from the ride queue* (`docs/adr/0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (22), with its required mark, default, format and its error state (400, 403, 409, 422).
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-041?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline, soldOutForDay.
- [ ] Every action is wired with its success and its failure: Add parking to my cart, Change plate.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

## Tenant configuration on every guest screen

Every guest screen in this batch is white-label. These elements are set by the tenant in the CMS and apply to every screen of the guest app (each screen's block lists the ones particular to it). **Draw with the default theme; on the key screens add one alternate tenant theme** (below), so a reviewer sees the brand is configuration, not paint. The full map, with the input-to-output examples: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Element | Configured in | Allowed values | Default | What it changes |
|---|---|---|---|---|
| Logo (`brand.logoAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo in the header or nav bar, the splash and the footer |
| Logo dark image (`brand.logoDarkAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo on dark backgrounds (falls back to the primary logo) |
| Logo variant (`brand.logoVariant`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | Light · Dark · Duotone | Light | which logo lockup sits in the nav bar, and whose colours drive the theme |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Splash image (`brand.splashImageAssetRefs`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG, JPG, SVG or MP4 from the media library | — | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). |
| Splash duration seconds (`brand.splashDurationSeconds`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | min 0; max 10 | 3 | — |
| Splash background colour (`brand.splashBackgroundColour`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | #RRGGBB | — | — |
| Show loading indicator (`brand.showLoadingIndicator`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | — | on | — |
| Intro video (`brand.introVideoAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode (`brand.introVideoMode`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | When GST-001 plays it full screen. "Skip introduction" is always shown. |
| Powered by TICVAI credit (`brand.showPoweredBy`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | — | on | the *Powered by TICVAI* credit on the launch screen, at the foot of Account and in the web footer; on by default, and switching it off needs the licence add-on (403 … |
| Primary colour (`theme.primaryColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings |
| Secondary colour (`theme.secondaryColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | secondary buttons and secondary emphasis: unselected chips, secondary tabs |
| Accent colour (`theme.accentColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | highlights: badges (LIMITED, NEW, BESTSELLER), availability counts, sale prices |
| Background colour (`theme.backgroundColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | the page background behind every screen (the `ground` token) |
| Text colour (`theme.textColour`) | `CMS-005`, `ADM-016` | #RRGGBB | — | body text on the background |
| Corner radius (`theme.cornerRadius`) | `CMS-005`, `ADM-016` | min 0; max 32 | — | the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest) |
| Surface style (`theme.surfaceStyle`) | `CMS-005`, `ADM-016` | Glass · Solid | Glass | cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token) |
| Button style (`theme.buttonStyle`) | `CMS-005`, `ADM-016` | Solid · Outline · Pill | Solid | every button's shape: solid fill, outline, or pill |
| Component colours (`theme.componentColours`) | `CMS-005`, `ADM-016` | — | — | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |
| Primary latin (`fonts.primaryLatin`) | `CMS-003` | — | — | headings and body text in English |
| Primary arabic (`fonts.primaryArabic`) | `CMS-003` | Required when `ar` is among the tenant's languages (audit R163). | — | headings and body text in Arabic |
| Secondary latin (`fonts.secondaryLatin`) | `CMS-003` | — | — | the secondary face (eyebrows, numbers) in English |
| Secondary arabic (`fonts.secondaryArabic`) | `CMS-003` | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | — | the secondary face in Arabic |
| Custom font images (`fonts.customFontAssetRefs`) | `CMS-003` | PNG, JPG, SVG or MP4 from the media library | — | Uploaded font files, as `MediaAsset` ids. |
| Header layout (`header.layout`) | `CMS-009` | Logo left · Logo centre · Logo with menu | — | the header: logo left, logo centred, or logo with the menu |
| Show logo (`header.showLogo`) | `CMS-009` | — | on | — |
| Show menu (`header.showMenu`) | `CMS-009` | — | on | — |
| Show notifications (`header.showNotifications`) | `CMS-009` | — | on | — |
| Background colour (`header.backgroundColour`) | `CMS-009` | #RRGGBB | — | — |
| Navigation kind (`navigation.kind`) | `CMS-009` | Bottom navigation · Drawer · Tabs | — | the main navigation: bottom tab bar, drawer, or tabs |
| Navigation items (`navigation.items`) | `CMS-009` | at most 12 | — | — |
| Buy button (`navigation.buyButton`) | `CMS-009` | — | — | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps; it opens GST-003. |
| Footer columns (`footer.columns`) | `CMS-009` | — | — | — |
| Legal links (`footer.legalLinks`) | `CMS-009` | — | — | Required links, held separately from the free-form columns — a tenant reorganising their footer must not be able to remove the privacy notice by accident. |
| Copyright text (`footer.copyrightText`) | `CMS-009` | — | — | — |
| Social links (`footer.socialLinks`) | `CMS-009` | — | — | — |
| Languages (`languages.languages`) | `CMS-011`, `ADM-018` | at least 1 | — | the language button in the header; Arabic flips every screen right to left |
| Default language (`languages.defaultLanguage`) | `CMS-011`, `ADM-018` | ISO 639-1 code, shown as the language name | — | the language a first visit opens in |
| Modules (`modules.modules`) | `CMS-001`, `ADM-424` | — | — | — |
| Features (`features.features`) | `CMS-001` | — | — | — |
| Custom domain hostname (`domains.hostname`) | `CMS-017`, `ADM-017` | — | — | — |
| Custom domain kind (`domains.kind`) | `CMS-017`, `ADM-017` | Guest web · Guest app · Partner portal · Developer portal | — | — |
| Verification method (`domains.verificationMethod`) | `CMS-017`, `ADM-017` | Dns txt · Cname · Http file | Dns txt | — |
| Entity kind (`seo.entityKind`) | `CMS-013` | Content page · Product · Event · Performance · Membership · Promotion · Venue | — | — |
| Entity (`seo.entityId`) | `CMS-013` | shows names, sends the id | — | — |
| Locale (`seo.locale`) | `CMS-013` | — | — | — |
| SEO metadata title (`seo.title`) | `CMS-013` | — | — | — |
| Meta description (`seo.metaDescription`) | `CMS-013` | — | — | — |
| Keywords (`seo.keywords`) | `CMS-013` | — | — | — |
| Canonical URL (`seo.canonicalUrl`) | `CMS-013` | — | — | — |
| Slug (`seo.slug`) | `CMS-013` | — | — | 22.11.6. Human-readable, and changing one is a redirect rather than an edit — a slug that changes without a 301 is a page that was ranking and now is not. |
| Hreflang (`seo.hreflang`) | `CMS-013` | — | — | 22.11.11. Which URL serves which language, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page. |
| Schema org type (`seo.schemaOrgType`) | `CMS-013` | — | — | — |
| Open graph (`seo.openGraph`) | `CMS-013` | — | — | — |
| Is auto generated (`seo.isAutoGenerated`) | `CMS-013` | — | on | 22.11.2. Generated by default and overridable. |
| No index (`seo.noIndex`) | `CMS-013` | — | off | — |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `CMS-104`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Component colours: primary CTA (`theme.componentColours.primaryCta`) | `CMS-005`, `ADM-016` | — | — | the one main call to action on each screen, when it should differ from the brand colour |
| Component colours: pay button (`theme.componentColours.payButton`) | `CMS-005`, `ADM-016` | — | — | the Pay button at checkout |
| Buy button: style (`navigation.buyButton.style`) | `CMS-009` | Raised · Floating · Flat · Hidden | Raised | the Buy tickets button in the tab bar: raised (default), floating, flat, or hidden |

**The alternate tenant theme (Coastal Aqua)**: Primary colour #0077B6; Secondary colour #023E8A; Accent colour #FFB703; Background colour #F5FAFC; Text colour #0B1324; Corner radius 18; Surface style Solid; Button style Pill; Logo variant Duotone; Header layout Logo centre; Step indicator Dots; Card layout Cards across; Card size Standard; Cart layout Floating icon; Fonts Poppins / Tajawal.
**Key screens to show in it:** `WEB-001`, `WEB-005`, `WEB-006`, `WEB-010`, `WEB-012`, `GST-001`, `GST-007`, `GST-041`, `KSK-002`, `KSK-003`.

**Decided for every guest screen:** **No dark or light mode.** The venue's chosen theme applies on every device setting; `Theme.darkMode` is deprecated and ignored, never drawn, and the guest app has no Light/Dark switch (Chinmay, 2 October, Q150; CHG-CSA-035). ***Powered by TICVAI* is a tenant toggle, on by default** (`brand.showPoweredBy`): shown on the launch screen, at the foot of Account and in the web footer; switching it off needs the licence add-on, or 403 `powered-by-locked` (Chinmay, 2 October, Q160; DI-297; CHG-CSA-036). **Each homepage section sets its card count and its scroll animation** (`maxItems`; `scrollAnimation` rise, scale, slide, blur or none, default rise): every customisation option of the approved wireframe (Chinmay, 2 October, Q152 and Q153; DI-1088; CHG-CSA-040). **Landing-page templates.** A tenant with no landing page of its own starts from a TICVAI template (`listLandingPageTemplates`, kept as `HomepageLayout.templateKey`); one with its own site links in with deep links (`landingSource` ownSite) (Chinmay, 2 October, batch 2 #41; CHG-CSA-037).

**Never configurable:** A dark or light mode: the guest surfaces have one theme, the venue's (Chinmay, 2 October; CHG-CSA-035). Semantic colour pairs (success, warning, danger, neutral) are not overridable: a tenant who recolours danger to their brand green has made a destructive confirmation look like a success (`screens/_design-tokens.yaml` whiteLabel). Site structure and the navigation flow are fixed and adapt to the product configuration (MoM 3 Aug, DI-119); a guest always books a product or package, never a resource (DI-502). A colour pair that fails 4.5:1 contrast is refused by the CMS, not warned (setTheme 400 ContrastProblem, audit R139).

## Reference designs and the trackers for this platform

**P01 reference designs** (from `handoff/design-batches/apps/1-guest-app/README.md`)

- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the website. Rev 3 with the 29 September fixes and the 30 September feedback (group booking with a headcount, multi-park counters, surf session tickets, the swim-ability answer, transport stations and departures, popular route cards; `CLIENT-RESPONSE-30SEP.md` beside it). The client approved it for development once W1 to W10 are in.
- `sources/designs/guest-rev3-30-september/TICVAI Visit Planner.dc.html`: the visit planner. WEB-050 Plan Your Visit is this file.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-026, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-038, DI-040, DI-042, DI-044, DI-045, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P01 as a whole** (23: 3 open, 20 closed). Open first; a closed row says where it went on 30 September.

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker)*
- **S9** Final UI/UX for the website and the mobile app *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **T1** Feedback on the revised website and mobile wireframes *(Allam / Qossai · Open · due 1 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A28** Review the 'Viva Ticket' website as a reference for ticket-flow variations *(Softlabs Design Team · Low · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A29** Collate design references/inspiration and share with TICVAI, organized by mobile app, website, and admin/back-office pages *(Softlabs (Sahil & Aishwarya) · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A55** Implement per-tenant module visibility toggles (e.g., hide Dining, Retail, or other services) configurable independently for the guest website and mobile app *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker)*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker)*
- **A115** Apply HA selectively to revenue-critical components (ticketing, POS, B2C) same-region, with multi-region DR as an optional add-on *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Aug 2026 · workshop tracker)*
- **A118** Commission the third-party penetration test before go-live (ticketing, B2C, B2B, mobile apps) and resolve all severities *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 24 Aug 2026 · workshop tracker)*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker)*
- **A174** Cross-check the six previously-scoped wallet types against Allam's documentation and deliver the three wireframe flows (ticketing, F&B, retail) plus the revised B2C flow *(Chinmay Parab / Pradnya Yeram / Allam · High · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker)*
- … 9 more in `handoff/design-inputs/task-tracker-index.json`

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

### Across P01 Guest Web

- Step-indicator style is configurable, the same as on the web: bars, dots, counters or step names. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1093)*
- **Open question.** Real venue photos, clips and logos are still to come from the client; designs use stand-ins. Slots expected: a photo per ticket card and clip per card, a square shot per extra/shop item, one landscape poster per venue for the single-event page. Photos ≥1600 px, clips mp4 6–12 s, no audio. *(open · design review 29 Sep 2026, Asset list — TICVAI Guest Booking · DI-1080)*
- The tenant picks which logo lockup sits in the nav bar and a logo variant (Light, Dark, Duotone) whose colours drive the theme. *(agreed · design review 29 Sep 2026, CFG-4 · Brand logo + Logo palette (Light/Dark/Duotone) · DI-1068)*
- Theme settings: surface style Glass (default) or Solid cards; button style Solid (default), Outline or Pill. *(agreed · design review 29 Sep 2026, CFG-3 · Surfaces (Glass/Solid) and Buttons (Solid/Outline/Pill) · DI-1067)*
- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Guest-facing copy may say "session" (surf sessions, timed sessions) as a glossary exception, like "Booking". *(agreed · design review 29 Sep 2026, CFG-10 · 'Sessions can be added, edited or closed from Config -> Sessions' · DI-1064)*
- Never ask the same thing twice: table zone is picked on the table map (no zone step before it); height is asked once (height bands on the water-park day pass are the eligibility check); party/school summaries prefill headcount, child's name and age from the earlier form. *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): repeated steps removed · DI-1000)*
- Confirmed final: cart sliding in from the right or bottom, card size options, and cart-sidebar placement left or right; Qossai specifically liked the compact card size. No further changes requested. *(agreed · MoM 24 Sep 2026, 4.10 Guest Web App — Card Layout & Cart Configuration Confirmed · DI-991)*
- Headers are reserved for standard elements only (venue image, category tabs, language bar, profile icon), applied consistently; date/availability selection belongs in the main content below the header, never in the header. Header/layout patterns must be adapted for mobile, which looks and behaves differently. *(agreed · MoM 24 Sep 2026, 4.9 Guest Web App — Specific UX Feedback (Header/Date Placement Standardization) · DI-990)*
- A language button (EN / العربية) sits in the header next to the profile icon, web and mobile. Arabic flips the whole layout right-to-left and switches interface text (navigation, buttons, booking steps, ticket names and tags, cart, seat map, checkout, account). Venue, show and dish names stay as written. *(client request · design review 23 Sep 2026, Header 2. Language icon in the header · DI-975)*
- Replace "Sign in / Create account" in the header with a single profile icon. It opens one screen with Log in and Register tabs; signed-in guests get their account menu from the same icon. *(client request · design review 23 Sep 2026, Header 1. One profile icon in the header that opens login / register · DI-974)*
- Allam's model reference: a simple card-based family-entertainment-centre site with minimal clicks, a right-side cart drawer, "help me choose", clear categories, video that autoplays when a guest taps "read more", adapting seamlessly between desktop and mobile. Allam and Qossai want this simplicity to guide the guest experience. *(client request · MoM 18 Sep 2026, 4.14 Guest Website UX Review — Upsell/Cross-Sell Placement & Reference Sites · DI-952)*
- **Open question.** Allam expects a large volume of feedback on the guest web/mobile prototype; detailed feedback goes to a separate dedicated session with Qossai and Allam. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-888)*
- The reviewed prototype is the actual guest-facing B2C site customers browse and book from, not a CMS tool. A separate, more limited white-label interface lets a client adjust colours, fonts and layout from a menu of options; not yet built in the prototype. *(agreed · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-887)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*
- Qossai is dissatisfied with the current B2C guest platform build and wants a separate vision session; references: the "Little Explorer" site and Six Flags. Six Flags cues: single-page flow. *(client request · MoM 8 Sep 2026, 4.20 Planning & Next Steps · DI-736)*
- Allam: most guests book from a smartphone, so the mobile version of the booking flows is the higher priority to validate (only desktop shown). *(client request · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough · DI-684)*
- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*
- Configurable cookie consent banner (accept/reject) per website; some cookies flagged mandatory (non-rejectable), others optional; templated and configurable in the system. *(client request · MoM 1 Sep 2026, 4.13 Privacy Consent & Cookie Policy · DI-617)*
- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Six Flags Kidiya reference: fixed header with configurable navigation (logo, Explore/Tickets/Passes, sub-menus), every item toggleable via the CMS. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-424)*
- Allam: the venue's main website is fully venue-managed; after "Book Now" the white-label B2C flow keeps the venue's header/footer branding while product selection, cart and checkout are TICVAI-managed. Header/footer links to non-checkout pages redirect to the main venue site. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-397)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- Qossai: the TICVAI name must always remain visible to end users of a client-branded guest app (e.g. a "Made by TICVAI" credit) and cannot be removed by the client. *(agreed · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-250)*
- Qossai: present products with video rather than static images (as Talabat-style apps do); see benchmark app "222" for further inspiration. *(client request · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-222)*
- Qossai shared reference apps (Al Qadiya / Six Flags Saudi Arabia, and "The District" by Zomato) and cited their use of video over static images as design inspiration. *(client request · MoM 5 Aug 2026, 13. Mobile / POS App Design References · DI-146)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- Base ticket-booking UX (web and mobile) on current market best practice rather than the demoed references as-is; Allam recommends the "Viva Ticket" website as a reference for the flow variations. *(agreed · MoM 3 Aug 2026, 10. Reference Material & Design Research · DI-125)*
- A multi-language toggle switches the entire site's content. *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-120)*
- Allam: banner, header, footer and background color are CMS-configurable per client, but site structure and navigation flow are fixed and adapt automatically to product configuration (dated, non-dated, seated, membership products surface the right fields). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-119)*
- All sites are fully mobile-responsive; e.g. the desktop calendar view collapses into a mobile-optimized layout. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-113)*
- A "powered by [platform]" footer credit is fixed and not client-editable. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-111)*
- One client can run multiple branded sites from the same setup, e.g. two brands sharing a footer but with distinct headers and hero banners. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-110)*
- White-label sites share one platform/template but each is configured independently: header, footer, logo, colors, fonts and hero banner are client-editable from the backend. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-108)*
- Selling reference layout: clean top navigation; category tabs with counts (All Events 32, Exhibitions, Guided Tours ...); sort and type chips (Price, Rating, Popular; General, Seated, Multipass, Scheduled, Rental); content cards with large image, type badge, rating, tags (LIMITED, NEW, BESTSELLER), availability ("180 available", "11 left") and "from" price; persistent cart on the right with member discount, totals and "Checkout Securely". *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, items 2-5 · DI-026)*
- Preliminary perceived-performance targets: web pages load in under about 3 seconds, mobile app loads in under about 2 seconds, ticket validation responds in under 500 milliseconds. *(agreed · MoM 28 Jul 2026, 18. Performance and Scalability · DI-015)*

### In P01 · In-venue Services

- **Open question.** Web "at the venue" section gives guests without the app on-site features in the browser: interactive maps, wait times, 3D venue maps, food ordering, virtual queue status, parking, basic directions (main gate, first aid). In progress; client review pending. *(open · MoM 15 Sep 2026, 4.2 Guest Web App - 3D Stadium Seat View & At-Venue Wayfinding · DI-891)*

**22 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addCartLine": {"method":"POST","path":"/carts/{cartId}/lines","contract":"orders","summary":"Add something","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"AddCartLineRequest","responds":"Cart"},
"claimLocationSession": {"method":"POST","path":"/location-sessions","contract":"fnb","summary":"Tell the platform where the guest is","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LocationSession"},
"createGuestFnbOrder": {"method":"POST","path":"/guest-orders","contract":"fnb","summary":"A guest orders food","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateGuestOrderRequest","responds":"GuestOrderResult"},
"createTableReservation": {"method":"POST","path":"/table-reservations","contract":"fnb","summary":"Book a table in advance","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TableReservation","responds":"TableReservation"},
"getFnbDeliveryPolicy": {"method":"GET","path":"/fnb-delivery-policy","contract":"fnb","summary":"How an outlet does takeaway and delivery","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":true}],"requestBody":null,"responds":"FnbDeliveryPolicy"},
"getGuestBill": {"method":"GET","path":"/table-sessions/{sessionId}/bill","contract":"fnb","summary":"The bill for the guest's table","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Bill"},
"getGuestMenu": {"method":"GET","path":"/outlets/{outletId}/guest-menu","contract":"fnb","summary":"The menu a guest sees","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"at","in":"query","required":null},{"name":"language","in":"query","required":null}],"requestBody":null,"responds":"GuestMenu"},
"getGuestOrderStatus": {"method":"GET","path":"/guest-orders/{orderId}","contract":"fnb","summary":"Track an order","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuestOrderStatus"},
"getVenueMap": {"method":"GET","path":"/venue-maps/{mapId}","contract":"venue-map","summary":"A map with its points and paths","permission":"VENUE_MAP_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"version","in":"query","required":null},{"name":"draft","in":"query","required":null}],"requestBody":null,"responds":"VenueMapDetail"},
"getVenueMapGraph": {"method":"GET","path":"/venue-maps/{mapId}/graph","contract":"venue-map","summary":"The navigation graph, ready to route over","permission":"VENUE_MAP_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"draft","in":"query","required":null},{"name":"stepFreeOnly","in":"query","required":null}],"requestBody":null,"responds":"VenueMapGraph"},
"getWaitTimes": {"method":"GET","path":"/queues/wait-times","contract":"queue","summary":"Wait times across a venue","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":true},{"name":"category","in":"query","required":null}],"requestBody":null,"responds":"WaitTime"},
"getWaitingGuest": {"method":"GET","path":"/waiting-guests/{entryId}","contract":"queue","summary":"Read a queue entry","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WaitingGuest"},
"joinQueue": {"method":"POST","path":"/waiting-guests","contract":"queue","summary":"Join a virtual queue","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"JoinQueueRequest","responds":"WaitingGuest"},
"joinRestaurantWaitlist": {"method":"POST","path":"/waitlist","contract":"fnb","summary":"Add a party to an outlet's waitlist","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RestaurantWaitlist","responds":"RestaurantWaitlist"},
"leaveQueue": {"method":"DELETE","path":"/waiting-guests/{entryId}","contract":"queue","summary":"Leave a queue","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"leaveRestaurantWaitlist": {"method":"POST","path":"/waitlist/{entryId}/leave","contract":"fnb","summary":"Take a party off an outlet's waitlist","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RestaurantWaitlist"},
"listDeliveryLocations": {"method":"GET","path":"/venues/{venueId}/delivery-locations","contract":"fnb","summary":"Where an order can be delivered","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"servingOutletId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDiningOutlets": {"method":"GET","path":"/venues/{venueId}/dining","contract":"fnb","summary":"Where a guest can eat, right now","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"openNow","in":"query","required":null},{"name":"orderingMethod","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFulfilmentSlots": {"method":"GET","path":"/outlets/{outletId}/fulfilment-slots","contract":"fnb","summary":"Collection times or delivery windows still open","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"path","required":true},{"name":"mode","in":"query","required":true},{"name":"date","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listParkingFacilities": {"method":"GET","path":"/parking-facilities","contract":"access","summary":"Car parks at a venue, and how each integrates","permission":"PARKING_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listQueues": {"method":"GET","path":"/queues","contract":"queue","summary":"List queues","permission":"QUEUE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"openOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"updateParkingEntitlement": {"method":"PATCH","path":"/parking-entitlements/{entitlementId}","contract":"access","summary":"Change the plate, or revoke","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"UpdateParkingEntitlementRequest","responds":"ParkingEntitlement"},
"updateTableReservation": {"method":"PATCH","path":"/table-reservations/{reservationId}","contract":"fnb","summary":"Change or cancel a booking","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"TableReservation","responds":"TableReservation"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AddCartLineRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["variantId","quantity"],"properties":{"variantId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Optional; sent by a page or till that shows the engine's recommendations. Not validated against the engine: an unknown id only fails to attribute.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"A table deposit line (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` in `awaitingDeposit` this pays for, sent with `variantId` set to the booking's `deposit.variantId` and `quantity` 1. The price is the booking's `deposit.amount`. A booking that is not awaiting a deposit is refused 422 `depositNotDue`.\n"},"seatIds":{"type":"array","maxItems":50,"description":"At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)). Over the limit is 422 `seatLimitExceeded`.","items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant and `quantity` is 1. The hold is the line's capacity; no inventory lease is taken."},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"For an add-on attaching to a ticket already in the cart. **Removing the parent removes the child** — a locker with no admission is not a sale.\n"},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"}}},
"AllergenCode": {"type":"string","description":"**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n","enum":["gluten","crustaceans","eggs","fish","peanuts","soybeans","milk","nuts","celery","mustard","sesame","sulphites","lupin","molluscs"]},
"Bill": {"x-ticvai-persistence":"none — computed from visit orders","type":"object","required":["visitId","lines","subtotal","taxAmount","total"],"properties":{"visitId":{"type":"string"},"covers":{"type":"integer"},"lines":{"type":"array","items":{"type":"object","required":["lineId","name","quantity","lineTotal"],"properties":{"lineId":{"type":"string"},"orderId":{"type":"string"},"name":{"type":"string"},"quantity":{"type":"integer"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"categoryCode":{"type":"string","nullable":true},"seatNumber":{"type":"integer","nullable":true}}}},"subtotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"serviceCharge":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"BookedWindow": {"type":"object","nullable":true,"x-ticvai-persistence":"none — embedded as window_starts_at and window_ends_at on orders.cart_line and orders.order_line","description":"**The booked time window of an hourly product, such as a meeting room** (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). The guest picks a date, a length and a start time from `resources.listProductStartTimes`; the length is the product's `length` variant (1 hour, 2 hours, half day, full day), priced per variant, so the price is the variant's. **`endsAt` minus `startsAt` must equal the chosen variant's length** (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. Required on a product with `catalogue.Product.requiresTimeWindow` true and refused on any other (`windowRequired`, `windowNotAllowed`). The room itself is not named here: the window holds capacity of the room type, and `resources.allocateResources` picks the room at checkout (26 August minute: a guest books a meeting room product, never a raw room).\n","required":["startsAt","endsAt"],"properties":{"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time","description":"After `startsAt`, on the same venue day."}}},
"Cart": {"type":"object","x-ticvai-persistence":"orders.cart","required":["id","venueId","channel","status","lines"],"properties":{"id":{"type":"string","format":"uuid"},"token":{"type":"string","readOnly":true,"description":"**How an anonymous guest returns to their cart**, including from a recovery email. Rotated on claim, so a link shared before signing in does not reach the account after.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null while anonymous. Set by `claimCart`."},"status":{"$ref":"#/components/schemas/CartStatus"},"lines":{"type":"array","items":{"$ref":"#/components/schemas/CartLine"}},"conflicts":{"type":"array","items":{"$ref":"#/components/schemas/CartConflict"}},"consentQuestions":{"type":"array","readOnly":true,"description":"**The consent questions this cart's products and flow ask** (decided 29 September, rev 3 REV3-26), computed on read at their current version as **the union of each line's published booking flow's `white-label.BookingFlow.settings.consentQuestionIds`** (the flow `getPublishedBookingFlow` resolves for the line's product: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig`, 29 September W12) **and every line's `catalogue.Product.consentQuestionIds`, each question once**: the flow's first, in its order, then each product's in cart-line order, a question already listed not repeated (its `lineIds` gain the line). The client asks them, in the order given, and sends the answers to `marketing.recordConsentAnswers`; `answered` then turns true. One or several, as the venue chose. `checkoutCart` refuses while a required one is unanswered.\n","items":{"allOf":[{"$ref":"../satellite/marketing-crm.yaml#/components/schemas/ConsentQuestion"},{"type":"object","properties":{"lineIds":{"type":"array","description":"The cart lines that ask it. Empty for a question the flow asks.","items":{"type":"string","format":"uuid"}},"answered":{"type":"boolean","description":"Every person (for `perPerson`) or the booking (for `perBooking`) has an answer."}}}]}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"discountTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPromotionIds":{"type":"array","description":"**Re-evaluated on every read.** A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became applicable should be.\n","items":{"type":"string","format":"uuid"}},"couponCodes":{"type":"array","readOnly":true,"description":"The promo codes the guest entered through `applyCartPromoCode` (decided 28 September, audit R073 (e)). **Sent as `couponCodes` on every promotions evaluation of this cart**, so a code is re-checked on each read like any promotion; a code that stops qualifying stays listed here and its promotion drops out of `appliedPromotionIds`.\n","items":{"type":"string","maxLength":100}},"expiresAt":{"type":"string","format":"date-time","description":"The earliest lease expiry in the cart, or the cart's own window where it holds none."},"extensionsUsed":{"type":"integer","readOnly":true},"maxExtensions":{"type":"integer","readOnly":true},"locale":{"type":"string"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time"}}},
"CartConflict": {"type":"object","x-ticvai-persistence":"none — computed on read","description":"2.9.5. Golf at 13:00 and karting at 13:00 for the same guest. **A prompt, not a refusal** — a party of four may legitimately split, and refusing would be wrong more often than right.\n","properties":{"kind":{"type":"string","enum":["overlappingTime","sameSessionDifferentVenue","exceedsPartySize","requiresPrerequisite","consentBlocksBooking"]},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"message":{"type":"string"},"isBlocking":{"type":"boolean","description":"Most are not. `requiresPrerequisite` is — an add-on with no ticket to attach to cannot be sold. So is `consentBlocksBooking`: a consent question answered with the answer the venue set to block the booking (decided 29 September, rev 3 REV3-26).\n"}}},
"CartLine": {"type":"object","x-ticvai-persistence":"orders.cart_line","required":["id","variantId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"productName":{"type":"string","readOnly":true},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid","nullable":true},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Set from `addCartLine`; checkout copies it to the order line.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"Set on a table deposit line only (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` this line secures. Priced from the deposit the booking snapshotted, not from the variant. Becomes an `orders.deposit` row at checkout, not revenue. A table booking with no deposit never has a line (rev 3 REV3-8).\n"},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"The `resources.ResourceHold` this line buys (decided 29 September, rev 3 REV3-15). While set, `leaseExpiresAt` is the hold's `expiresAt` and `inventoryHoldId` is null."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"The line this add-on is attached to, from `AddCartLineRequest.parentLineId`. Kept on the line because **removing the parent removes the child**, and `removeCartLine` has to be able to find the children.\n"},"overridePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"overrideReason":{"type":"string","nullable":true,"enum":["priceMatch","serviceRecovery","negotiated","damagedGoods","staffSale","error"],"description":"BL-085. **An operator could apply an approved discount and not enter a price.** A price match against a competitor and a service-recovery gesture are not discounts off a list — they are a number somebody decided.\n**Escalated above a configured threshold, and the reason is a closed set**: a free-text override reason is an override nobody can report on, and this is the field an auditor reads first.\n"},"feeKind":{"type":"string","nullable":true,"enum":["booking","transaction","service","delivery","convenience","cancellation"],"description":"**A fee is a line, not an adjustment.** `orders` already separates a service charge from a tip for the reason that applies here: **a guest is entitled to see what they are being charged for**, and a fee folded into the ticket price is a fee nobody can question.\nItemised at checkout, taxed on its own code, and refundable separately — **a cancellation fee is usually the one thing not refunded**, which only works if it is its own line.\n"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"inventoryHoldId":{"type":"string","nullable":true,"description":"The capacity held for this line — a `catalogue.InventoryHold.id`, typed as that id is. **Null for a product with no capacity** — a t-shirt needs stock, not a lease.\n"},"leaseExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"Shown to the guest. *\"Your seats are held for 6 minutes\"* is better than discovering it at checkout.\n"},"isAvailable":{"type":"boolean","readOnly":true,"description":"Re-checked on every read. **A line can become unavailable while the cart sits** — a lease expiring is not the same as the product selling out, and both land here.\n"}}},
"CartStatus": {"type":"string","enum":["active","expiring","expired","abandoned","checkedOut"]},
"CreateGuestOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","menuItemId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"menuItemId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1,"maximum":20},"modifierOptionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"note":{"type":"string","maxLength":200,"description":"Free text to the kitchen. Allergy notes belong here and are surfaced prominently on the ticket.\n"}}},
"CreateGuestOrderRequest": {"type":"object","required":["id","lines","quotedTotal","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"locationSessionId":{"type":"string","format":"uuid","nullable":true,"description":"From `claimLocationSession`. Where the order is going. Required for delivery to a table, seat, cabana or named location. Absent for collection, where the outlet is named instead.\n"},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"Required for collection. Ignored where a location session is supplied — the session names its outlet."},"fulfilment":{"allOf":[{"$ref":"#/components/schemas/GuestOrderFulfilment"}],"nullable":true,"description":"Required for takeaway and address delivery; refused with 422 when it breaks the outlet's `FnbDeliveryPolicy`."},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateGuestOrderLine"}},"quotedTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the guest was shown. Checked against the server's recomputation — a guest is never trusted with a price, and a mismatch is refused rather than silently corrected in either direction.\n"},"paymentMethod":{"type":"string","enum":["card","wallet","roomCharge","addToTab"]},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateQueueRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","venueId","capacityPerCycle","cycleMinutes"],"properties":{"code":{"type":"string","maxLength":64},"name":{"$ref":"#/components/schemas/LocalisedText"},"venueId":{"type":"string","format":"uuid"},"attractionProductId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"The ride. Taking it out of service closes this queue rather than leaving guests holding positions for something that is not running.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["standby","singleRider","fastPass","virtual","accessible","groupOnly","staffOnly"],"default":"standby","description":"5.6.x. **A ride has several queues and the model had one.** A single-rider line and a standby line at the same attraction draw from one capacity and fill at different rates, and modelling them as one queue makes both wait estimates wrong.\n**`accessible` is not a courtesy lane.** It has its own capacity because a guest who cannot stand in a switchback needs a place to wait, not priority.\n"},"operatingWindows":{"type":"array","description":"**When the queue runs, which is not when the venue is open.** A ride closing an hour early for maintenance leaves a queue accepting guests for a cycle that will not happen.\nStored one row per window in `queue.queue_operating_window` (see `Queue`), not as a column on the queue.\n","items":{"type":"object","required":["day","from","to"],"properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Venue local time, 24-hour `HH:MM`, when the queue starts running."},"to":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Venue local time, 24-hour `HH:MM`, when the queue stops running."},"lastEntryMinutesBefore":{"type":"integer","default":0,"description":"**When the queue stops accepting, which is before it stops running.** A guest joining two minutes before close waits twenty and is turned away at the front.\n"}}}},"parentQueueId":{"type":"string","format":"uuid","nullable":true,"description":"Where several queues share one capacity. **The standby and single-rider lines at one ride draw from the same cycles**, and a parent is how that is expressed without either queue owning the other.\n"},"loadBalanceWithQueueIds":{"type":"array","description":"BL-137. **Two rides with the same theme and different waits**, and nothing directed a guest to the shorter one. Load balancing is an offer, not an assignment — **a guest sent to a ride they did not choose is a guest who feels managed.**\n","items":{"type":"string","format":"uuid"}},"inQueueOfferEnabled":{"type":"boolean","default":false,"description":"**A guest with twenty minutes to wait is a guest with twenty minutes to buy something.** Offers surface in the wait screen and are the only reason a virtual queue earns its infrastructure.\n"},"notifyBeforeCallMinutes":{"type":"integer","default":5,"description":"BL-017, 19.2.61. **A guest was not told their turn was approaching**, which makes a virtual queue worse than a physical one — at least a line is visible.\n"},"capacityPerCycle":{"type":"integer","minimum":1},"cycleMinutes":{"type":"number","minimum":0},"maxPartySize":{"type":"integer","default":6},"returnWindowMinutes":{"type":"integer","default":15,"description":"How long a called party has to arrive before the entry expires."},"heightRequirementCm":{"type":"integer","nullable":true},"fastPassAllocationPercent":{"type":"number","minimum":0,"maximum":100,"default":0,"description":"Share of each cycle reserved for Fast Pass holders."},"zone":{"type":"string","nullable":true},"fastPass":{"allOf":[{"$ref":"#/components/schemas/QueueFastPass"}],"nullable":true,"description":"The lane's Fast Pass block (decided 29 September, VM close-out). Null on a queue that takes no Fast Pass.\n"}}},
"DeliveryLocation": {"type":"object","x-ticvai-persistence":"fnb.delivery_location","required":["id","venueId","kind","label","isServiceable"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/DeliveryLocationKind"},"label":{"type":"string","description":"What a runner is told. \"Cabana 12\", \"Row H Seat 4\", \"Lawn — north gate\"."},"zone":{"type":"string","nullable":true},"tableId":{"type":"string","format":"uuid","nullable":true,"description":"Set where the location is a restaurant table, so it shares table state."},"seatId":{"type":"string","nullable":true,"description":"Set where the seat is the address. References the seat map."},"servingOutletIds":{"type":"array","description":"Which outlets deliver here. A cabana served by the pool bar and not the restaurant is normal, and a location nothing serves is not an address.\n","items":{"type":"string","format":"uuid"}},"isServiceable":{"type":"boolean","description":"False where the location exists but is not currently taking delivery — closed section, weather, no runner on shift.\n"},"unserviceableReason":{"type":"string","nullable":true},"walkTimeMinutes":{"type":"integer","nullable":true,"description":"From the serving outlet. Feeds the guest's estimate — a cabana eight minutes away is not the same promise as a table by the kitchen.\n"}}},
"DeliveryLocationKind": {"type":"string","description":"4.6.26. One concept, because a runner needs one instruction.","enum":["table","seat","cabana","sunbed","poolside","box","suite","lawn","collectionPoint","namedLocation"]},
"DiningOutlet": {"type":"object","x-ticvai-persistence":"none — projection over outlet, menu and table state","required":["outletId","name","kind","isOpenNow","orderingMethod"],"properties":{"outletId":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string"},"zone":{"type":"string","nullable":true},"cuisine":{"type":"array","items":{"type":"string"}},"isOpenNow":{"type":"boolean"},"opensAt":{"type":"string","format":"date-time","nullable":true},"closesAt":{"type":"string","format":"date-time","nullable":true},"orderingMethod":{"$ref":"#/components/schemas/GuestOrderingMethod"},"estimatedWaitMinutes":{"type":"integer","nullable":true,"description":"From current kitchen ticket volume, not a fixed figure. Null where the outlet has no kitchen display reporting ticket status — an invented wait time is worse than none.\n"},"imageAssetRef":{"type":"string","nullable":true},"menuId":{"type":"string","format":"uuid","nullable":true},"admissionContext":{"allOf":[{"$ref":"../spine/tenancy.yaml#/components/schemas/OutletAdmissionContext"}],"description":"**Inside the venue or standalone** (decided 2 October 2026, Chinmay: DEC-070, workbook Q70; CHG-CLN-008): the outlet's `tenancy.Outlet.admissionContext`, so the guest sees before ordering whether an admission ticket for today is needed (`insideVenue`, refused `403 entry-ticket-required` without one) or not (`standalone`, takeaway and delivery). The canonical name; \"siting\" is its deprecated alias."}}},
"FnbDeliveryPolicy": {"type":"object","x-ticvai-persistence":"fnb.delivery_policy","required":["outletId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"outletId":{"type":"string","format":"uuid"},"collectionEnabled":{"type":"boolean","default":true},"deliveryEnabled":{"type":"boolean","default":false},"collectionPoint":{"type":"string","maxLength":200,"nullable":true},"collectionHoldMinutes":{"type":"integer","default":20},"asapCollectionMinutes":{"type":"integer","default":25},"asapDeliveryMinutes":{"type":"integer","default":45},"slotMinutes":{"type":"integer","default":30},"minimumOrder":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"deliveryFee":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"freeDeliveryAbove":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"radiusKm":{"type":"number","minimum":0,"nullable":true},"emiratesServed":{"type":"array","items":{"type":"string"}},"cutleryOptIn":{"type":"boolean","default":true,"description":"Cutlery only when asked for, as in the design."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"FnbOrderStatus": {"type":"string","description":"The full lifecycle from 4.6.35. Nine states, not six — the earlier enum collapsed `accepted` into `placed` and had no `collected` or `delivered` at all, which made collection and delivery indistinguishable from a server putting a plate down.\n`accepted` matters because an outlet may refuse: past last orders, out of a key ingredient, or simply too far behind. A guest whose order sat in `placed` for ten minutes and was then rejected has a worse experience than one refused immediately.\n","enum":["ordered","accepted","inPreparation","ready","served","collected","delivered","cancelled","refunded"]},
"FnbReservationTable": {"type":"object","x-ticvai-persistence":"fnb.reservation_table","description":"**Taken from the backend workbook, 20 September.** Maps one or more dining tables assigned to a reservation.","required":["reservationId","tableId","createdAt"],"properties":{"reservationId":{"type":"string","format":"uuid"},"tableId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"FulfilmentSlots": {"type":"object","x-ticvai-persistence":"none — computed per request","properties":{"slots":{"type":"array","items":{"type":"object","properties":{"start":{"type":"string","format":"date-time"},"end":{"type":"string","format":"date-time","nullable":true},"isAsap":{"type":"boolean"}}}}}},
"GuestMenu": {"type":"object","x-ticvai-persistence":"none — projection over menu, item and availability","required":["outletId","menuId","name","inForceUntil","sections"],"properties":{"outletId":{"type":"string","format":"uuid"},"menuId":{"type":"string","format":"uuid"},"name":{"type":"string"},"inForceUntil":{"type":"string","format":"date-time","nullable":true,"description":"When this menu stops applying. The client shows it, because a guest browsing breakfast at 10:55 should know.\n"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer"},"sections":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"sortOrder":{"type":"integer"},"items":{"type":"array","items":{"type":"object","required":["menuItemId","name","price","isAvailable","allergens"],"properties":{"menuItemId":{"type":"string","format":"uuid"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"imageAssetRef":{"type":"string","nullable":true},"isAvailable":{"type":"boolean","description":"Marked, not removed. A guest who saw a dish yesterday and cannot find it today assumes the app is broken; \"sold out\" is an answer.\n"},"unavailableReason":{"type":"string","nullable":true},"allergens":{"type":"array","description":"Always present. Not a field a tenant may choose to omit.","items":{"$ref":"#/components/schemas/AllergenCode"}},"preparationMinutes":{"type":"integer","nullable":true},"modifierGroups":{"type":"array","items":{"$ref":"#/components/schemas/ModifierGroup"}}}}}}}}}},
"GuestOrderFulfilment": {"type":"object","x-ticvai-persistence":"fnb.order_fulfilment","description":"How a guest's order leaves the kitchen: collected, delivered to an address, or taken to a place in the venue.","required":["mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"orderId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-column":"service_order_id","description":"The guest order this fulfils (`FnbOrder.id`). Set by the server from the order it arrives with."},"mode":{"type":"string","enum":["collection","delivery","inVenue"],"description":"`collection` from a counter, `delivery` to an address outside the venue, `inVenue` to a table, seat, cabana or named location (the location session). `GuestOrderResult.fulfilment` reports the same choice."},"collectionAt":{"type":"string","format":"date-time","nullable":true},"windowStart":{"type":"string","format":"date-time","nullable":true},"windowEnd":{"type":"string","format":"date-time","nullable":true},"deliveryAddress":{"type":"object","nullable":true,"properties":{"building":{"type":"string","maxLength":200},"unit":{"type":"string","maxLength":60,"nullable":true},"emirate":{"type":"string","maxLength":60},"directions":{"type":"string","maxLength":500,"nullable":true}}},"deliveryFee":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true},"cutlery":{"type":"boolean","default":false},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"GuestOrderResult": {"type":"object","x-ticvai-persistence":"none — projection over fnb_order","required":["orderId","orderNumber","status","total"],"properties":{"orderId":{"type":"string"},"orderNumber":{"type":"string","description":"Short and readable. It gets called out across a counter."},"fulfilment":{"type":"string","enum":["collect","deliverToLocation","tableService","deliverToAddress"],"description":"How the order reaches the guest, in the request's terms: `collect` is `GuestOrderFulfilment.mode` `collection`; `deliverToAddress` is `delivery`; `inVenue` is `tableService` where the location session is a table and `deliverToLocation` for a seat, cabana or named location. `KitchenTicket.serviceMode` is the kitchen's view and uses `ServiceMode`."},"deliveryLabel":{"type":"string","nullable":true,"description":"Where it is going, as a runner would read it."},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"collectionPoint":{"type":"string","nullable":true},"tableLabel":{"type":"string","nullable":true}}},
"GuestOrderStatus": {"type":"object","x-ticvai-persistence":"none — projection over kitchen_ticket","required":["orderId","status","lines"],"properties":{"orderId":{"type":"string"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/FnbOrderStatus"},"estimatedReadyAt":{"type":"string","format":"date-time","nullable":true},"isReadyForCollection":{"type":"boolean"},"lines":{"type":"array","description":"Per-line status. A guest waiting on one dish should see which.","items":{"type":"object","properties":{"name":{"type":"string"},"quantity":{"type":"integer"},"status":{"$ref":"#/components/schemas/KitchenTicketStatus"}}}}}},
"GuestOrderingMethod": {"x-ticvai-persistence":"none — enum","type":"string","description":"How a guest may order at this outlet. Varies within one venue, so it is per outlet rather than a venue setting.\n","enum":["tableService","appToTable","appToCollect","counterOnly","notAvailable"]},
"JoinQueueRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","queueId","partySize","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"queueId":{"type":"string","format":"uuid"},"partySize":{"type":"integer","minimum":1},"entitlementId":{"type":"string","nullable":true,"description":"Fast Pass or priority entitlement. Owned by Product & Entitlement — this contract references it and never defines it.\n"},"partyHeightsCm":{"type":"array","description":"Where the queue has a height requirement. Refusing here is far better than refusing at the ride, in front of a child who has already waited.\n","items":{"type":"integer"}},"accessibilityNeedDeclared":{"type":"boolean","default":false,"description":"The party declares an accessibility need (5.6.7; decided 29 September, build pass). Grants priority only on a lane whose `QueueFastPass.accessibilityPriority` is on, and is recorded on the entry either way.\n"},"promotionCode":{"type":"string","maxLength":64,"nullable":true,"description":"A promotion code the guest holds, checked against the lane's `QueueFastPass.promotionIds` (5.6.34). A code for a promotion the lane does not list grants nothing and is not an error.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"KitchenTicketStatus": {"type":"string","enum":["received","preparing","ready","served","recalled","cancelled"]},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"LocationSession": {"type":"object","x-ticvai-persistence":"fnb.location_session","required":["id","locationId","kind","label","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/DeliveryLocationKind"},"label":{"type":"string"},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"The outlet serving this location. Where several serve it, the guest chooses and this is set on the first order.\n"},"visitId":{"type":"string","format":"uuid","nullable":true,"description":"The table visit this session orders onto, where the location is a table. Absent for a cabana or a seat, which have no visit concept — the order stands alone.\n"},"joinedExistingVisit":{"type":"boolean"},"subjectId":{"type":"string","format":"uuid"},"expiresAt":{"type":"string","format":"date-time","description":"Sessions expire so a guest who leaves cannot order to a lounger now occupied by someone else.\n"}}},
"ModifierGroup": {"x-ticvai-persistence":"fnb.modifier_group + fnb.modifier_option","type":"object","description":"**An F&B modifier is a choice added to a dish at the moment of ordering** — *no onions*, *extra cheese*, *cooked medium*. **It is not an Attribute**, the axis that generates catalogue variants (naming-and-style §3 lists *Modifier* as a banned synonym for that), and the two must not be merged: a variant is a different product with its own stock, a modifier is an instruction on a line with at most a price delta.\n","required":["id","code","name","minSelections","maxSelections","options"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"minSelections":{"type":"integer","minimum":0,"description":"Greater than zero makes the group required."},"maxSelections":{"type":"integer","minimum":1},"options":{"type":"array","minItems":1,"items":{"type":"object","required":["id","name","priceDelta"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"priceDelta":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isDefault":{"type":"boolean"},"isAvailable":{"type":"boolean"},"allergens":{"type":"array","description":"What choosing this option adds to the dish. `attachModifierGroup` refuses a group that adds one the item does not declare, and `verifyAllergens` reports it as `via` `modifier`.","items":{"$ref":"#/components/schemas/AllergenCode"}}}}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"OrderLineAttributes": {"type":"object","nullable":true,"additionalProperties":true,"x-ticvai-persistence":"none — embedded as attributes (jsonb) on orders.cart_line and orders.order_line","description":"Open attributes of a line, kept from the cart to the order line. **`transport` is the one with a defined shape** (decided 29 September, rev 3 REV3-21); other keys are free.\n","properties":{"transport":{"$ref":"#/components/schemas/TransportLineAttributes"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ParkingEntitlement": {"type":"object","x-ticvai-persistence":"access.parking_entitlement","description":"**Issued at payment of an order that contains a parking product** (decided 28 September, audit R166). Parking is sold through the normal cart and checkout (`orders.addCartLine`, `orders.checkoutCart`), so every entitlement carries that order's `orderId`. The guest pays for the parking right with their order; the facility's own system is never paid through the app (`ParkingFacility.takesPayment`). **No live availability in the first release**: the sale is refused as full only when the facility's issued entitlements reach its `capacity`.\n","required":["facilityId","orderId","validFrom","validTo"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"facilityId":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","description":"The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`)."},"subjectId":{"type":"string","format":"uuid","nullable":true},"plateNumber":{"type":"string","nullable":true,"description":"Required in `plateWhitelist` mode, meaningless in the others. **Personal data** — a plate identifies a person, so it lives under the same rules as a contact point.\n"},"plateCountry":{"type":"string","nullable":true},"mediaCode":{"type":"string","nullable":true,"description":"The code presented in `none` and `qrHandoff` modes."},"status":{"allOf":[{"$ref":"#/components/schemas/ParkingEntitlementStatus"}],"readOnly":true,"description":"Server-owned. Moves as `states/parking-entitlement.yaml` says; a create body does not send it."},"pushedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"pushFailureReason":{"type":"string","nullable":true,"readOnly":true},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"}}},
"ParkingEntitlementStatus": {"type":"string","enum":["pending","pushed","pushFailed","active","used","expired","revoked"]},
"ParkingFacility": {"type":"object","x-ticvai-persistence":"access.parking_facility","required":["name","venueId","mode"],"properties":{"id":{"type":"string","format":"uuid","description":"**Server-assigned, and the upsert key of `setParkingFacility`.** Absent in a body, it creates; present, it names the facility being replaced. A client never mints one.\n"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"mode":{"$ref":"#/components/schemas/ParkingIntegrationMode"},"capacity":{"type":"integer","nullable":true,"description":"**What \"full\" means in the first release** (decided 28 September, audit R166): the facility is full when the issued `ParkingEntitlement`s valid for a time reach this number. There is no live space count from the car park; a guest sees *full* only when capacity is reached, never an availability figure. Null means no limit is enforced.\n"},"takesPayment":{"type":"boolean","readOnly":true,"default":false,"description":"**Always false, and stated rather than assumed** (19.2.78, CF-124). The requirement asks the guest app to take parking payments; the client decided on 14 August that it does not.\nAll three integration models are entitlement-based — the ticket carries the parking right and the platform pushes a plate or a code. **Pay-per-hour parking unrelated to a ticket runs on the parking system's own POS**, because taking that money here would make the venue an acquirer for parking, with a settlement path and a tax treatment nobody has designed.\nThe field exists so that a future reversal is a value change with a visible blast radius, rather than a silent gap somebody rediscovers.\n"},"vendorSwapTargetDays":{"type":"integer","readOnly":true,"default":5,"description":"**A new parking vendor should take days, not weeks** — Qossai, 14 August. The team has integrated parking APIs before and the architecture is expected to make the next one cheap.\nRecorded as a design constraint rather than a runtime value: **everything vendor-specific lives in `vendorName`, `endpoint` and `credentialRef`**, and the three modes are the adaptor surface (ADR-0012). A vendor needing a fourth mode is the signal this has been violated.\n"},"vendorName":{"type":"string","nullable":true,"description":"Staff only — omitted from a guest's `listParkingFacilities` response."},"endpoint":{"type":"string","nullable":true,"description":"Staff only — omitted from a guest's `listParkingFacilities` response."},"credentialRef":{"type":"string","nullable":true,"description":"A vault reference, never the credential. Staff only — omitted from a guest's `listParkingFacilities` response."},"pushLeadMinutes":{"type":"integer","nullable":true,"description":"Staff only — omitted from a guest's `listParkingFacilities` response. How far ahead of the visit a plate is pushed. **Too early and the whitelist fills with cars that will not arrive; too late and the guest is at the barrier.**\n"},"accessPointIds":{"type":"array","description":"Where the platform validates its own code, in `none` and `qrHandoff` modes.","items":{"type":"string","format":"uuid"}},"isActive":{"type":"boolean"}}},
"ParkingIntegrationMode": {"type":"string","description":"CF-52, settled 14 August. **Not variations of one thing** — each decides what happens at sale and what a guest presents at the barrier.\n","enum":["none","plateWhitelist","qrHandoff"]},
"PlacedResource": {"type":"object","x-ticvai-persistence":"venuemap.placed_resource","description":"**A bookable resource where it stands on the map** (decided 29 September, rev 3 REV3-15 and GAP-C2): cabana B09 on the Beach, 15 guests, Large. The resource itself, its bookings and its holds live in `resources`; this row says where it is drawn and what the guest sees. Written into the working draft by `importVenueGeometry` or `setPlacedResource`, copied into the `VenueMapVersion` snapshot at publish. A guest picks one on the published map, holds it with `resources.createResourceHold` and buys it. **Supersedes audit R073 (c) and the 26 August minute for resources on an ingested map.**\n","required":["id","mapId","resourceId","label","kind","zone","capacity","priceBandCode","position"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes it."},"resourceId":{"type":"string","format":"uuid","x-ticvai-references":"resources.Resource","description":"The `resources.Resource` this is. **Availability, holds and bookings are keyed by this**, so a republished map with the cabana moved keeps its bookings.\n"},"label":{"type":"string","maxLength":40,"x-ticvai-unique":"map","description":"What the guest sees and taps, e.g. `B09`. **Unique on the map**, compared without case after digit normalisation; normally the resource's `code`.\n"},"kind":{"type":"string","enum":["cabana","lounger","table","pitch","other"],"description":"A subset of `resources.ResourceKind`, the kinds a guest books from a map. A `table` here is a non-dining spot (a beach or event table) sold like a cabana; restaurant tables stay `fnb` table reservations (decided 29 September, rev 3 GAP-C2)."},"zone":{"type":"string","maxLength":80,"description":"The area the guest reads it by, e.g. `Beach`, `River`, `Terrace`."},"capacity":{"type":"integer","minimum":1,"maximum":500,"description":"Guests it takes, e.g. 15. Shown on the map and checked against the party at hold."},"priceBandCode":{"type":"string","maxLength":40,"description":"The band it sells in, e.g. `Large`, one of the `priceBands` given at import. The band's `variantId` prices it; the map holds no price.\n"},"variantId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"catalogue.ProductVariant","description":"Resolved from the price band. What a cart line for this resource names."},"position":{"type":"object","required":["x","y"],"description":"Drawing coordinates of its label anchor, as on `VenuePoint`.","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"boundary":{"type":"array","nullable":true,"description":"The shape drawn, as a polygon in drawing coordinates. Null for a pin.","items":{"type":"object","properties":{"x":{"type":"number"},"y":{"type":"number"}}}},"isBookable":{"type":"boolean","default":true,"description":"False keeps it on the map and off sale, e.g. a cabana kept for staff use. Shown greyed.\n"}}},
"Queue": {"x-ticvai-persistence":"queue.queue + queue.queue_operating_window","allOf":[{"$ref":"#/components/schemas/CreateQueueRequest"},{"type":"object","required":["id","status","waitingPartyCount"],"properties":{"id":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/QueueStatus"},"statusReason":{"type":"string","nullable":true},"waitingPartyCount":{"type":"integer"},"waitingGuestCount":{"type":"integer"},"currentWaitMinutes":{"type":"integer","nullable":true},"waitTimeSource":{"$ref":"#/components/schemas/WaitTimeSource"},"waitTimeAsOf":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When `currentWaitMinutes` was last set, by whichever source set it. `WaitTime.asOf` reads this.\n"},"manualWaitExpiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"Set by `setWaitTime` as now plus `expiresInMinutes`. Past it, the manual figure is dropped and the queue reverts to its sensor or throughput estimate. Null when the current figure is not manual.\n"},"manualWaitNote":{"type":"string","maxLength":200,"nullable":true,"readOnly":true,"description":"The `note` given with the current manual figure. Cleared when it expires."},"expectedReopenAt":{"type":"string","format":"date-time","nullable":true}}}]},
"QueueEntryStatus": {"type":"string","enum":["waiting","called","redeemed","expired","noShow","cancelled","released"]},
"QueueStatus": {"type":"string","enum":["open","paused","closed","atCapacity"]},
"RestaurantWaitlist": {"type":"object","x-ticvai-persistence":"fnb.waitlist_entry","description":"BL-130. **Distinct from `queue`, which is for rides.** A restaurant waitlist has a party size, a table preference and a walk-away point, and a guest who leaves is not the same as a guest who was served.\n","required":["id","outletId","partySize","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"outletId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"partySize":{"type":"integer"},"quotedWaitMinutes":{"type":"integer","nullable":true},"seatingPreference":{"type":"string","enum":["any","indoor","outdoor","bar","booth","highChair"],"nullable":true},"status":{"type":"string","enum":["waiting","notified","seated","walkedAway","noShow","cancelled"]},"notifiedAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time","description":"**When the party joined, on the device.** The wait a party had is measured from here to `notifiedAt` or to seating, which is the report `walkedAway` exists for. Required on a join — the operation is offline-capable."},"syncedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"holdExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**How long a table waits for somebody who was called.** Too short and a guest returning from the bathroom loses it; too long and the table sits empty at peak — which is why it is a setting rather than a constant.\n"}}},
"TableReservation": {"type":"object","x-ticvai-persistence":"fnb.table_reservation","x-ticvai-retired-columns":["table_ids"],"required":["outletId","startsAt","partySize"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"outletId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"guestName":{"type":"string"},"contactPoint":{"type":"string"},"partySize":{"type":"integer","minimum":1},"startsAt":{"type":"string","format":"date-time"},"durationMinutes":{"type":"integer","description":"**How long the cover is held.** An outlet turning tables twice an evening needs this to be real, or the second sitting cannot be booked.\n"},"tables":{"type":"array","description":"The dining tables assigned to this reservation, one row each.\n**Usually empty until seating.** Committing a specific table at booking time refuses later bookings against a constraint that did not need to exist — that was true of the `tableIds` array this replaces and it is still true, because it is about *when* a table is assigned rather than how the assignment is stored.\n**Replaces `tableIds`, retired 20 September.** An array cannot carry per-row state, which is the same reason this merge took `entry_rule_point`, `menu_item_modifier`, `seat_block_item`, `plan_benefit`, `payment_method_config` and `tier_module` from the backend workbook. A party seated across three tables that releases one early has nowhere to say so in an array, and *\"which reservations are on table 7 tonight\"* is a GIN scan over every reservation instead of an index seek.\n","items":{"$ref":"#/components/schemas/FnbReservationTable"}},"status":{"$ref":"#/components/schemas/TableReservationStatus"},"groupId":{"type":"string","format":"uuid","nullable":true,"description":"5.1.2. Several bookings managed as one party across adjacent tables."},"notes":{"type":"string","description":"Allergies, accessibility needs and other requests, as the guest wrote them."},"seatingPreference":{"type":"string","maxLength":64,"nullable":true,"description":"**The seating area the guest asked for**, e.g. indoor, terrace, majlis (Chinmay, 2 October, workbook Q204; DI-791; CHG-CSA-018). The outlet's own area names, as the waitlist's `RestaurantWaitlist.seatingPreference` takes them. A preference, not a table: the host seats the party on the night."},"occasion":{"type":"string","nullable":true,"enum":["birthday","anniversary","business","celebration","other"],"description":"The occasion the guest named (workbook Q204, DI-337; CHG-CSA-018). Shown to the host and the server; never a price."},"takenByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The staff member who took the booking (`createTableReservationForGuest`); null for a guest's own booking (CHG-CSA-045)."},"actualPartySize":{"type":"integer","nullable":true,"readOnly":true},"tableVisitId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"deposit":{"$ref":"#/components/schemas/TableReservationDeposit"},"createdAt":{"type":"string","format":"date-time","readOnly":true}}},
"TableReservationDeposit": {"type":"object","nullable":true,"readOnly":true,"x-ticvai-persistence":"fnb.table_reservation","description":"**The deposit this booking holds, snapshotted from `orders.DepositPolicy.dining` when it was made** (decided 29 September, rev 3 REV3-8b). Null where no deposit applied, which is every booking while the venue leaves `dining.enabled` false (the default). A later change to the policy does not re-price a booking already made.\n","required":["amount","basis"],"properties":{"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"basis":{"type":"string","enum":["fixedPerGuest","fixedPerTable","percentOfMinimumSpend"]},"holdExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"While `awaitingDeposit`, when the held cover is released if the deposit has not been authorised. The cart lease of the deposit line (15 minutes, audit R169)."},"refundableUntil":{"type":"string","format":"date-time","nullable":true,"description":"`startsAt` less `dining.refundableUntilHours`. Cancelling before it releases the deposit in full."},"variantId":{"type":"string","format":"uuid","description":"The venue's table-deposit variant, `DepositPolicy.dining.depositVariantId`, which the client sends to `addCartLine` with this booking's id."},"cartLineId":{"type":"string","format":"uuid","nullable":true,"description":"The `orders.CartLine` carrying the deposit, once added."},"depositId":{"type":"string","format":"uuid","nullable":true,"description":"The `orders.deposit` row, once the payment is authorised."}}},
"TableReservationStatus": {"type":"string","description":"`awaitingDeposit` only where the venue's dining deposit applies (decided 29 September, rev 3 REV3-8b); a booking with no deposit starts `booked`.","enum":["awaitingDeposit","booked","confirmed","seated","completed","cancelled","noShow"]},
"UpdateParkingEntitlementRequest": {"type":"object","x-ticvai-persistence":"none — request only; applied to access.parking_entitlement","description":"**The body of `updateParkingEntitlement`: only what changes.** A partial update, so a field left out keeps its stored value. Two changes are possible, one per call:\n- **A plate change** — `plateNumber`, and `plateCountry` where it differs. The new plate is re-pushed and the old one leaves the whitelist. Resending the current plate is how a failed push is retried.\n- **A revoke** — `status: revoked`. The plate leaves the whitelist and the entitlement is terminal.\nA body carrying both, or neither, is a `400`. Which states allow each change is `states/parking-entitlement.yaml`'s to say.\n","minProperties":1,"properties":{"plateNumber":{"type":"string","description":"Personal data, under the same rules as `ParkingEntitlement.plateNumber`."},"plateCountry":{"type":"string","nullable":true},"status":{"type":"string","enum":["revoked"],"description":"The only status a caller may set. Every other move is the server's."}}},
"VenueMap": {"type":"object","x-ticvai-persistence":"venuemap.map","description":"A park map, or a floor plan. **Several per venue** — a guest on the second floor should not be shown the ground floor's toilets.\n","required":["id","name","venueId","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","readOnly":true,"description":"Derived from `venueId`. Not sent by a client."},"kind":{"type":"string","enum":["park","floor","zone","parking"]},"floorLevel":{"type":"integer","nullable":true},"status":{"type":"string","enum":["draft","published","archived"],"readOnly":true,"description":"`draft` on create. Moves through `publishVenueMap` (`states/venue-map.yaml`), never by sending a value.\n"},"publishedVersion":{"type":"integer","nullable":true,"readOnly":true,"description":"The `VenueMapVersion.version` guests are served. Null until the first publish.\n"},"graphVersion":{"type":"integer","readOnly":true,"description":"**Bumped by a publish or a closure**, and returned as `VenueMapGraph.version`. Separate from `publishedVersion` because a closure changes the routes without creating a map version, and a closure that looked like a publish would lie about what changed.\n"},"isGeoreferenced":{"type":"boolean","readOnly":true,"description":"**Whether a guest can be located on it.** Without a georeference the map is a picture — useful, and not navigable.\n"},"baseAssetId":{"type":"string","format":"uuid","nullable":true,"description":"**The illustrated map a guest actually sees**, held in `assets` like any other media.\n**This is not the CAD drawing.** The drawing gives geometry — where things are, and how they connect. The base image is a designed illustration with the venue's own styling, and the two are different artefacts that happen to describe the same place. A park hands you an architect's plan and a beautiful painted map, and **the guest wants the second while the platform needs the first.**\nNull is valid. A map with geometry and no illustration renders as shapes — plain, and navigable.\n","x-ticvai-references":"assets.MediaAsset"},"baseImageAlignment":{"type":"object","nullable":true,"description":"**How the illustration lines up with the geometry.** They are drawn at different scales by different people, and a point placed on the plan lands in the wrong place on the painting unless something reconciles them.\nTwo known points is enough. **Without this the illustration is a picture behind the map rather than the map itself.**\n","properties":{"imageWidthPx":{"type":"integer"},"imageHeightPx":{"type":"integer"},"anchors":{"type":"array","minItems":2,"maxItems":4,"items":{"type":"object","properties":{"planX":{"type":"number"},"planY":{"type":"number"},"imageX":{"type":"number"},"imageY":{"type":"number"}}}}}},"tileSetRef":{"type":"string","nullable":true,"readOnly":true,"description":"Where a base image is large enough to need zoom levels. **A 12,000-pixel park map is not something a phone downloads on arrival**, and a guest opening the map on venue wifi at the gate is the worst moment to send twenty megabytes.\nGenerated from the base asset. Null means the image is small enough to serve whole.\n"},"boundsGeoJson":{"type":"string","nullable":true},"graphStatus":{"type":"string","readOnly":true,"enum":["notBuilt","connected","disconnected","partial"],"description":"**Whether every public point can actually be reached.** Computed at publish.\n`disconnected` means a point has no path to it at all — a toilet nobody can walk to is a toilet that does not exist. `partial` means every point is reachable and at least one only by steps, which is a different and quieter failure: **the map works until a wheelchair user opens it.**\n"}}},
"VenueMapDetail": {"type":"object","description":"19.2.55. **The whole map in one call**, so a client caches it and filters locally.","properties":{"version":{"type":"integer","nullable":true,"readOnly":true,"description":"**The published version these points and paths belong to**, which is the number a client caches and sends back as `version`. It can differ from `map.publishedVersion` when an older version was asked for. Null when the draft was read.\n"},"map":{"$ref":"#/components/schemas/VenueMap"},"points":{"type":"array","items":{"$ref":"#/components/schemas/VenuePoint"}},"paths":{"type":"array","items":{"$ref":"#/components/schemas/VenuePath"}},"resources":{"type":"array","description":"The bookable resources placed on this version of the map (rev 3 REV3-15). Empty on a map that carries none.\n","items":{"$ref":"#/components/schemas/PlacedResource"}}}},
"VenueMapGraph": {"type":"object","description":"19.2.56. **What a client needs to route, and nothing more.** Small enough to cache, versioned so a stale route is detectable.\n","required":["mapId","version","nodes","edges"],"properties":{"mapId":{"type":"string","format":"uuid"},"version":{"type":"integer","description":"**Bumped by a publish or a closure**, and stored as `VenueMap.graphVersion`. A client holding an older version knows its route may cross something that closed, and asking for the graph is cheaper than asking whether the graph changed.\n"},"generatedAt":{"type":"string","format":"date-time"},"nodes":{"type":"array","items":{"type":"object","properties":{"pointId":{"type":"string","format":"uuid"},"x":{"type":"number"},"y":{"type":"number"},"kind":{"type":"string"},"isStepFree":{"type":"boolean"}}}},"edges":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"uuid"},"to":{"type":"string","format":"uuid"},"distanceMetres":{"type":"number"},"isStepFree":{"type":"boolean"},"throughPointId":{"type":"string","nullable":true,"description":"Where an access point restricts this edge. **The direction lives on that point**, not here, so a gate reconfigured to bidirectional changes routing without a map edit.\n"},"isClosed":{"type":"boolean"}}}},"components":{"type":"integer","description":"How many disconnected parts. **One is the answer for a park.** More than one on a map that should be a single site means something is unreachable and the client can say so without walking the graph.\n"}}},
"VenuePath": {"type":"object","x-ticvai-persistence":"venuemap.path","description":"19.2.56. **The navigation graph.** The map supplies it; routing over it is a client concern, because a phone with the map cached routes offline and a server round-trip per step does not.\n","required":["id","mapId","fromPointId","toPointId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes the path."},"fromPointId":{"type":"string","format":"uuid"},"toPointId":{"type":"string","format":"uuid"},"geometry":{"type":"string","nullable":true,"description":"The centreline this edge follows, as an encoded polyline. **A walkway in a drawing is a polygon and a route is a line down the middle of it**, so extraction thins the polygon to a centreline and splits it at every fork.\nNull where the path was drawn on screen as a straight connection, which is normal for a venue with no walkway layer.\n"},"distanceMetres":{"type":"number","nullable":true,"readOnly":true,"description":"Computed by the server from `geometry` and the georeference. **Along the centreline, not point to point.** A path that curves round a lake is longer than the distance between its ends, and a guest told 80 metres who walks 200 stops trusting the map.\nRequires a georeference for real units; without one, distances are in drawing units and routing still works because **only the ratios matter to a shortest path.**\n"},"isStepFree":{"type":"boolean","default":true,"description":"**The single most important attribute on this object.** A wheelchair user routed up a staircase has been failed by the map, not by the venue.\n"},"isIndoor":{"type":"boolean","default":false},"restrictedByPointId":{"type":"string","format":"uuid","nullable":true,"description":"**Where a path is one-way, it is because of a thing on it — not because of the path.** Removed `isOneWay` on 18 August: a pedestrian walkway has no direction, and the three cases that look one-way are all a gate or a queue.\nA turnstile is one-way and `access.AccessPoint.direction` already says so. A queue line is one-way and `queue` owns it. **Putting the restriction on the path duplicated both and would have drifted from them** — a gate reconfigured to bidirectional would leave a path still marked one-way, and nothing would have noticed.\nSet where a path passes through an access point. The router reads the direction from the point.\n"},"closedReason":{"type":"string","nullable":true,"readOnly":true,"description":"Set by `setPathClosure` during works or an incident, never by sending it here. **A closed path removes routes rather than hiding the path**, so a guest sees why rather than wondering where it went.\n"}}},
"VenuePoint": {"type":"object","x-ticvai-persistence":"venuemap.point","description":"19.2.57 to 19.2.60. **What a venue places on the map**, and what a guest taps.\n","required":["id","mapId","kind","name","position"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"mapId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of the operation that writes the point."},"kind":{"type":"string","enum":["ride","attraction","show","restaurant","cafe","shop","kiosk","toilet","babyCare","prayerRoom","firstAid","atm","lockers","entrance","exit","emergencyExit","assemblyPoint","parking","guestServices","smokingArea","waterFountain","chargingPoint","photoSpot","junction","other"],"description":"**A closed set, and `emergencyExit` is separate from `exit` on purpose.** An exit is where a guest leaves; an emergency exit is where they are sent, and a map that cannot tell them apart is a map that routes a normal departure through a fire door.\n**`junction` is the one that is not a point of interest.** A path connects two points, so a fork in a walkway with nothing at it still needs a node — otherwise every bend has to be named as a destination, and a guest browsing the map sees forty entries called *Path junction 12*.\n**Junctions are hidden from guests and present in the graph.** Generated by extraction where paths meet; a venue never places one by hand.\n"},"name":{"type":"string","x-ticvai-unique":"venue","description":"**Unique per venue** (decided 28 September, audit R108). Two points on a venue's maps never share a name, compared without case, so *Toilets North* names one place; `setVenuePoint` refuses a duplicate with `409` `duplicate-code`. Junctions are named by extraction and are exempt.\n"},"nameLocalised":{"type":"object","nullable":true,"additionalProperties":{"type":"string"}},"position":{"type":"object","required":["x","y"],"description":"Drawing coordinates. **Latitude and longitude are derived from the georeference**, not stored, so a map that is re-georeferenced does not need every point moved.\n","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"For a restaurant, cafe, shop or kiosk. **Tapping it should open the menu**, and that only works if the map knows which outlet it is.\n"},"productId":{"type":"string","format":"uuid","nullable":true,"description":"For a ride or show — links to wait times and to booking. **What a guest is offered from any point, including a restaurant or a shop, is `featuredOffer`** (29 September, MOB-4); this link stays for wait times.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"For an entrance or exit. **This is what makes 3.2.64 work** — live admission statistics drawn on the point they came from.\n"},"isStepFree":{"type":"boolean","default":true,"description":"Whether the point itself can be reached without steps. **The same name as `VenuePath.isStepFree`, because it is the same concept** (it was `isAccessible` until the 26 September audit). **Placed on the point rather than inferred from the path**, because a step-free route to a building with steps at the door is not a step-free route.\n"},"openingHours":{"type":"string","nullable":true},"iconRef":{"type":"string","nullable":true},"isActive":{"type":"boolean","default":true},"isNavigable":{"type":"boolean","default":true,"description":"Whether a route may pass through it. **False for a point that marks a place without being reachable** — a stage a guest cannot walk onto, a zone label.\n"},"isDestination":{"type":"boolean","default":true,"description":"**Whether a guest may be routed *to* it, and whether it appears in a list of places.** False for a `junction`, which exists in the graph and nowhere else.\nSeparate from `isNavigable` because the two differ: a junction is navigable and not a destination, and a fenced landmark is a destination you can be shown but not walked into.\n"},"description":{"type":"object","nullable":true,"additionalProperties":{"type":"string","maxLength":1000},"description":"**What the guest reads on Item Detail** (29 September, MOB-4). Keyed by locale, like `nameLocalised`. One screen now serves rides, shows, restaurants and shops (GST-004 and GST-006 merged), and it opens from the map pin, so the point carries the words rather than each kind borrowing them from a different module. Set on BO-094.\n"},"media":{"type":"array","maxItems":12,"description":"**The gallery on Item Detail** (29 September, MOB-4): images and short clips from the asset library, first `isPrimary` shown on the map card. Assets are referenced, never copied, so a replaced photo changes everywhere.\n","items":{"type":"object","required":["assetId","kind"],"properties":{"assetId":{"type":"string","format":"uuid","x-ticvai-references":"assets.media_asset"},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false},"altText":{"type":"string","nullable":true,"maxLength":200}}}},"featuredOffer":{"type":"object","nullable":true,"required":["kind","id"],"description":"**The product card on Item Detail, for every kind of point** (29 September, MOB-4). `productId` above links a ride or show to its wait times; this is what the guest is offered from the point, and it may be a bundle: a restaurant offers *meal combo with admission* (`promotions` bundle with an admission and a meal component), which checks out in about three steps (GST-004 → GST-056 → GST-041). A point with none shows no card. **Referenced, not priced here**: the card reads `catalogue.getProduct` or `promotions.getBundle` for the live price and availability.\n","properties":{"kind":{"type":"string","enum":["product","bundle"]},"id":{"type":"string","format":"uuid","description":"The `catalogue.product` id or the `promotions.bundle` id, by `kind`."},"label":{"type":"string","nullable":true,"maxLength":40,"description":"The button text, e.g. *Buy meal combo*. Null uses the product's own call to action."}}},"typicalDurationMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":600,"description":"**How long a visit to this point usually takes**, ride time and queue excluded (29 September, MOB-6). The visit planner lays out a day with it; the queue comes from `queue.getWaitTimes` on the day. Null for a point the planner never places (a toilet).\n"},"interestTags":{"type":"array","maxItems":12,"description":"**What a guest who says they like this would like here** (29 September, MOB-6): the planner matches the guest's interests against these. A closed list so that the Plan tab's interest chips and the venue's tags are the same words.\n","items":{"type":"string","enum":["thrill","family","kids","water","animals","shows","culture","shopping","dining","relaxing","photo","adventure","sport","nightlife","indoor"]}},"cuisineTags":{"type":"array","maxItems":8,"description":"**For dining points** (restaurant, cafe, kiosk; 29 September, MOB-6). The planner places meals at points whose cuisine the party chose, at meal times. Free text codes such as `arabic`, `indian`, `italian`, `fastFood`, `vegetarian`, `halal` — cuisines are too many to close, and a wrong enum is worse than an unmatched tag. **Read per venue**: the planner matches a guest's cuisine only against the points of the venue that day is at (30 September, MoM 4.7).\n","items":{"type":"string","maxLength":30}},"retailTags":{"type":"array","maxItems":8,"description":"**For retail points** (shop, and a kiosk that sells goods rather than food; 30 September client meeting, MoM 4.7: retail and kiosk shops join F&B as venue-linked planner options). The planner places a shop stop at points whose tags the party chose, on the day of this point's venue only. Free text codes such as `souvenirs`, `toys`, `apparel`, `photo`, `essentials`, for the same reason as `cuisineTags`. A kiosk may carry both lists.\n","items":{"type":"string","maxLength":30}}}},
"WaitTime": {"x-ticvai-persistence":"none — computed from readings and throughput","type":"object","required":["queueId","waitMinutes","source","asOf","isStale"],"properties":{"queueId":{"type":"string","format":"uuid"},"queueName":{"$ref":"#/components/schemas/LocalisedText"},"attractionProductId":{"type":"string","format":"uuid","nullable":true},"attractionCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"The catalogue `ProductCategory` the attraction product is filed under — the value the `category` filter on `getWaitTimes` matches. Read from catalogue, not stored here.\n"},"status":{"$ref":"#/components/schemas/QueueStatus"},"waitMinutes":{"type":"integer","nullable":true,"description":"Null where the queue is closed or no estimate is available."},"source":{"$ref":"#/components/schemas/WaitTimeSource"},"isStale":{"type":"boolean","description":"The underlying feed has gone quiet past its expected interval. The figure is shown with a caveat rather than frozen and presented as current, and it is not hidden (decided 28 September, audit R080 (b)): the screen shows `waitMinutes` with its `asOf` and a stale marker.\n"},"heightRequirementCm":{"type":"integer","nullable":true},"zone":{"type":"string","nullable":true},"asOf":{"type":"string","format":"date-time","description":"When the figure was produced — the queue's `waitTimeAsOf`."}}},
"WaitTimeSource": {"type":"string","description":"Where the estimate came from. Surfaced so an operator knows whether a figure is measured or guessed.\n","enum":["sensor","throughput","manual","unavailable"]},
"WaitingGuest": {"x-ticvai-persistence":"queue.entry","type":"object","required":["id","queueId","partyNumber","partySize","status","joinedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client-generated UUIDv7 from `JoinQueueRequest.id`, and the `entryId` every entry path takes. `listMyWaitingGuests` gives it back to a guest who has lost it.\n"},"queueId":{"type":"string","format":"uuid"},"queueName":{"$ref":"#/components/schemas/LocalisedText"},"subjectId":{"type":"string","format":"uuid","nullable":true},"partyNumber":{"type":"integer","description":"What the guest sees and what appears on signage."},"partySize":{"type":"integer"},"status":{"$ref":"#/components/schemas/QueueEntryStatus"},"positionInQueue":{"type":"integer","nullable":true},"partiesAhead":{"type":"integer","nullable":true},"estimatedCallAt":{"type":"string","format":"date-time","nullable":true},"isFastPass":{"type":"boolean"},"priorityBasis":{"type":"string","enum":["none","entitlement","loyaltyTier","promotion","accessibility"],"default":"none","description":"Why this party is priority, when it is (decided 29 September, build pass; 5.6.7, 5.6.34): the first `QueueFastPass` criterion met at join, in the order entitlement, loyalty tier, promotion, accessibility. `isFastPass` is true whenever this is not `none`. Kept on the entry so a disputed priority can be explained afterwards.\n"},"priorityTierId":{"type":"string","format":"uuid","nullable":true,"description":"The loyalty tier that granted priority, where `priorityBasis` is `loyaltyTier`."},"priorityPromotionId":{"type":"string","format":"uuid","nullable":true,"description":"The promotion that granted priority, where `priorityBasis` is `promotion`."},"accessibilityNeedDeclared":{"type":"boolean","default":false,"description":"What the party declared at join, shown to the operator at the front."},"entitlementId":{"type":"string","nullable":true},"calledAt":{"type":"string","format":"date-time","nullable":true},"returnWindowEndsAt":{"type":"string","format":"date-time","nullable":true},"redeemedAt":{"type":"string","format":"date-time","nullable":true},"admittedCount":{"type":"integer","nullable":true},"joinedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}}
}
```
