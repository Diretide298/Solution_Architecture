# WS160 — Resource Management Configuration board 6

**10 screens · 26 operations · 44 schemas · 12 permissions**

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

- **Every control that can be refused must be gated.** 12 permissions apply here:
  `ASSET_VIEW, INSPECTION_MANAGE, INSPECTION_SUBMIT, INSPECTION_VIEW, RENTAL_CONFIGURE, RENTAL_OPERATE, RENTAL_PRICE, RENTAL_VIEW, RESOURCE_BOOK, RESOURCE_MANAGE, RESOURCE_VIEW, WORK_ORDER_MANAGE`. A control nobody can use must say so,
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
| `BO-903` | Equipment & Asset Command Center | B–D | 0 | 26 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-904` | Rental Resource Configuration | B–D | 29 | 0 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-905` | Rental Inventory & Availability Control | B–D | 5 | 0 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-906` | Resource Checkout Workspace | B–D | 12 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-907` | Guest & Resource Assignment | B–D | 0 | 26 | 6 | 25 | 0 | 0 | — | notStarted (—) |
| `BO-908` | Rental Duration, Extension & Return Management | B–D | 0 | 32 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-909` | Deposit & Rental Financial Control | B–D | 0 | 16 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-910` | Maintenance & Resource Blocking | B–D | 19 | 0 | 6 | 10 | 1 | 2 | — | notStarted (—) |
| `BO-911` | Inspection, Condition & Compliance Management | A | 31 | 25 | 6 | 4 | 0 | 0 | — | notStarted (—) |
| `BO-912` | Asset Lifecycle, Depreciation & Retirement | B–D | 11 | 38 | 6 | 5 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-903, BO-907, BO-908, BO-909 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-903` Equipment & Asset Command Center

**Provide operations teams with a real-time overview of all physical resources across the organization.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_VIEW`, `RESOURCE_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/equipment-asset-command-center-bo-903` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-001): A resource cost table and a primary "Create resource cost" button sat on the command centre; cost entry belongs on cost analytics (BO-945, which declares both) … Removed 2 October 2026 (CHG-WIR-001): A resource cost table and a primary "Create resource cost" button sat on the command centre; cost entry belongs on cost analytics (BO-945, which declares both) …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The physical estate at a glance for operations: how many items exist, how many are available, out with guests, due back, overdue, in maintenance, due inspection, damaged, lost or retired, what they are worth (for those allowed to see money), and the alerts that need someone now. The one thing to get right: every number is a tile that opens the filtered list, and the alerts name the item and the place ("Towel inventory at Waterpark Zone B below threshold").

**Known correction pending (do not draw the wrong version)**

- **The twelve KPIs and Asset Value Indicators are drawn as columns of a table titled "Every equipment asset"** Why: KPIs are tiles on a command centre (VO-R02). *(source: screens/P08-venue-back-office.yaml#BO-903; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Twelve item states (reserved, in use, due, overdue, inspection due, damaged, lost...) against the agreed simplified states** Why: 26 August agreed rental/equipment items use available, rented, faulty/out of maintenance; due and overdue are booking conditions, not item states. Count them from bookings, keep item state simple. *(source: DI-500 / TRACKER Actions row 158; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No read returns asset values (replacement, depreciated) or inspection due** Why: Neither the resource nor the maintenance asset carries value fields. *(source: contracts/satellite/resources.yaml#/components/schemas/Resource / contracts/satellite/maintenance.yaml#listAssets; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): A resource cost table (id, resourceId, scopePath, raw ids) with a "Resource id" text filter and a primary "Create resource cost" button sit … (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Cabana · Lounger · Locker · Wheelchair · Stroller · Equipment · Room · Auditorium · Vehicle · Instructor · Staff · Table … | `listResources` ?kind |
| Available from | date and time picker | — | — | `listResources` ?availableFrom |
| Available to | date and time picker | — | — | `listResources` ?availableTo |
| Category | picker: choose a category | — | — | `listAssets` ?categoryId |
| Status | select | — | In service · Out of service · Under maintenance · Awaiting parts · Retired · Disposed | `listAssets` ?status |
| Maintenance due | toggle | — | — | `listAssets` ?maintenanceDue |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Breakdown**: View by resource type, category, venue, location, operational status, condition, ownership, rental status - as a segmented control over the status chart. *(source: screens/P08-venue-back-office.yaml#BO-903 / screens/P08-venue-back-office.yaml#BO-904)*

#### Outputs: what the screen shows and produces

**Shown**

**Every equipment asset** (data table)

| Shows | Format | Notes |
|---|---|---|
| Total assets | text | not in the schema: `Total assets` |
| Available | text | not in the schema: `Available` |
| Reserved | text | not in the schema: `Reserved` |
| Checked out | text | not in the schema: `Checked out` |
| In use | text | not in the schema: `In use` |
| Due for return | text | not in the schema: `Due for return` |
| Overdue | text | not in the schema: `Overdue` |
| Under maintenance | text | not in the schema: `Under maintenance` |
| Inspection due | text | not in the schema: `Inspection due` |
| Damaged | text | not in the schema: `Damaged` |
| Lost | text | not in the schema: `Lost` |
| Retired | text | not in the schema: `Retired` |
| Asset value indicators | text | not in the schema: `Asset Value Indicators` |

**The selected equipment asset** (detail panel): The pack groups this record's detail under its own headings: “Users shall view resources by”, “Users may initiate”.

| Shows | Format | Notes |
|---|---|---|
| Total assets | text | not in the schema: `Total assets` |
| Available | text | not in the schema: `Available` |
| Reserved | text | not in the schema: `Reserved` |
| Checked out | text | not in the schema: `Checked out` |
| In use | text | not in the schema: `In use` |
| Due for return | text | not in the schema: `Due for return` |
| Overdue | text | not in the schema: `Overdue` |
| Under maintenance | text | not in the schema: `Under maintenance` |
| Inspection due | text | not in the schema: `Inspection due` |
| Damaged | text | not in the schema: `Damaged` |
| Lost | text | not in the schema: `Lost` |
| Retired | text | not in the schema: `Retired` |
| Asset value indicators | text | not in the schema: `Asset Value Indicators` |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Total asset value, Replacement value, Depreciated value, Maintenance cost, Lost/damaged value. Each needs attaching to the control it gates, or the screen needs the control.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Total assets, Available, Reserved, Checked out, In use, Due for return, Overdue, Under maintenance, Inspection due, Damaged, Lost, Retired - metric tiles with deltas (VO-R02), Overdue and Damaged in alert colour when above zero. *(source: screens/P08-venue-back-office.yaml#BO-903)*
- **Asset value**: Total value, Replacement value, Depreciated value, Maintenance cost (YTD), Lost/damaged value in AED - shown only with financial permission, otherwise the row is absent and a note says why (VO-R08). *(source: screens/P08-venue-back-office.yaml#BO-903)*
- **Smart alerts**: Count-and-place sentences with a link each (18 rental items overdue; 7 assets need inspection this week; Projector P-17 repeated maintenance; towels low at Waterpark Zone B). *(source: screens/P08-venue-back-office.yaml#BO-904)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Quick actions**: Add asset, Checkout, Return, Transfer, Block for maintenance (BO-910), Record inspection, Report damage, Retire asset (BO-912); each opens its screen with the item preselected when one is selected. *(source: screens/P08-venue-back-office.yaml#BO-904)*
- **Board tiles**: Rental configuration, inventory, checkout, assignment, returns, deposits, maintenance, inspection, lifecycle (BO-904 to BO-912). *(source: screens/P08-venue-back-office.yaml#BO-903)*

**Data it reads**: `listResources` (onLoad, Equipment and assets); `listAssets` (onLoad, The asset register)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-904` Rental Resource Configuration: *Rental Resource Configuration*
- → `BO-905` Rental Inventory & Availability Control: *Rental Inventory & Availability Control*
- → `BO-906` Resource Checkout Workspace: *Resource Checkout Workspace*
- → `BO-907` Guest & Resource Assignment: *Guest & Resource Assignment*
- → `BO-908` Rental Duration, Extension & Return Management: *Rental Duration, Extension & Return Management*
- → `BO-909` Deposit & Rental Financial Control: *Deposit & Rental Financial Control*
- → `BO-910` Maintenance & Resource Blocking: *Maintenance & Resource Blocking*
- → `BO-911` Inspection, Condition & Compliance Management: *Inspection, Condition & Compliance Management*
- → `BO-912` Asset Lifecycle, Depreciation & Retirement: *Asset Lifecycle, Depreciation & Retirement*; carries `assetId`, `resourceId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The equipment asset list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the equipment asset untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No equipment asset yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: nothing on this screen filters its list. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **An item checked out at POS**: Never also counted as available on another channel; counts are one platform state. *(source: screens/P08-venue-back-office.yaml#BO-912)*

#### Consistency with other screens

- Match `BO-069`: An asset is maintenance's record; this board counts resources and links to the asset register for maintenance detail.
- Match `BO-584`: Rental command centre KPIs (overdue, damage) must match for the same scope.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  total: 2,568
  available: 1,124
  checkedOut: '684'
  reserved: '210'
  underMaintenance: '98'
  inspectionDue: '132'
  damaged: '48'
  lost: '22'
value:
  total: AED 3,245,600.00
  replacement: AED 4,812,300.00
  depreciated: AED 2,106,750.00
  maintenanceYtd: AED 186,500.00
alerts:
- 18 rental items overdue
- 7 assets require inspection this week
- Projector P-17 has repeated maintenance
- Towels at Aqua Park Zone B below 50
```

#### Permissions

- `listResources` → `RESOURCE_VIEW` (read) · staff
- `listAssets` → `ASSET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-903` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-903`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 6
- Flow F269 *Resource Management Configuration board 6: Equipment & Asset Command Center*, step 1: Opens Equipment & Asset Command Center → Provide operations teams with a real-time overview of all physical resources across the organization.
- Flow F269 *Resource Management Configuration board 6: Equipment & Asset Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F269 *Resource Management Configuration board 6: Equipment & Asset Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F269 *Resource Management Configuration board 6: Equipment & Asset Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F269 *Resource Management Configuration board 6: Equipment & Asset Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F269 *Resource Management Configuration board 6: Equipment & Asset Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F269 *Resource Management Configuration board 6: Equipment & Asset Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F269 *Resource Management Configuration board 6: Equipment & Asset Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F269 branch at step 1 (expected): when Nothing has been set up on Equipment & Asset Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F269 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-903?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-904`, `BO-905`, `BO-906`, `BO-907`, `BO-908`, `BO-909`, `BO-910`, `BO-911`, `BO-912`.
- [ ] Every gated control is gated: `ASSET_VIEW`, `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-904` Rental Resource Configuration

**Define how a physical resource behaves when offered as a customer-rental resource.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_CONFIGURE`, `RENTAL_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/rentals/rental-resource-configuration-bo-904` |

**From the Food, Beverage & Retail process.** Rental behaviour of a physical resource from the resource-management board (strollers, wheelchairs, towels): rental enabled, durations, extensions, walk-in and advance, eligibility, quantity model.

**Known correction pending (do not draw the wrong version)**

- **This board (BO-904 to BO-909, F269) repeats the rental boards: configuration (BO-494–BO-503), availability (BO-514), check-out (BO-544/EMP-071), return and extension (BO-554, BO-564) and deposits (BO-529/530), on the same rental operations.** Why: Two sets of screens for one capability; make the rental boards canonical and keep this board only as an entry from resource management (DI-671, DI-474). *(source: DI-671 / DI-474 / DI-498 / DI-500; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Rental enabled | select field | — | — | — | — | — | — |
| Rental item/resource type | select field | — | — | — | — | — | — |
| Rental duration | select field | — | — | — | — | — | — |
| Minimum duration | select field | — | — | — | — | — | — |
| Maximum duration | select field | — | — | — | — | — | — |
| Rental increments | select field | — | — | — | — | — | — |
| Same-day return required | select field | — | — | — | — | — | — |
| Overnight rental permitted | select field | — | — | — | — | — | — |
| Extension permitted | select field | — | — | — | — | — | — |
| Maximum extension | select field | — | — | — | — | — | — |
| Advance reservation permitted | select field | — | — | — | — | — | — |
| Walk-in rental permitted | select field | — | — | — | — | — | — |
| Customer eligibility | select field | — | — | — | — | — | — |
| Venue availability | select field | — | — | — | — | — | — |
| Quantity Model | select field | — | — | — | — | — | — |
| Expected return time | select field | — | — | — | — | — | — |
| Grace period | select field | — | — | — | — | — | — |
| Late-return policy | select field | — | — | — | — | — | — |
| Automatic overdue status | select field | — | — | — | — | — | — |
| Return venue | select field | — | — | — | — | — | — |
| Cross-venue return allowed | select field | — | — | — | — | — | — |
| Inspection required | select field | — | — | — | — | — | — |
| Channel Rules | select field | — | — | — | — | — | — |
| POS | select field | — | — | — | — | — | — |
| B2C | select field | — | — | — | — | — | — |
| Mobile App | select field | — | — | — | — | — | — |
| Kiosk | select field | — | — | — | — | — | — |
| Employee App | select field | — | — | — | — | — | — |
| API | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-903` Equipment & Asset Command Center: *Back to Equipment & Asset Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental resource configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental resource configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Bookings exist under the current model |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
resource: Stroller · rental enabled · 1–8 h · walk-in and advance · quantity model pooled
```

#### Permissions

- `getRentalProduct` → `RENTAL_VIEW` (read) · staff
- `setRentalInventoryModel` → `RENTAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental/equipment items use simplified states — available, rented, faulty/out-of-maintenance (excluded from available inventory until resolved) — not granular custom attributes. Clients supply item data at onboarding; a screen lets them update inventory and item details afterwards. *(agreed · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management; 5. Key Decisions · DI-500)*
- Rental items (e.g. strollers, wheelchairs, towels): inventory and quantity per day, check-out and check-in, with inventory updated automatically on return; a refundable deposit (with guest details) is captured at rental and refunded on return. *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-498)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-904` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-904`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 6
- Flow F269 *Resource Management Configuration board 6: Equipment & Asset Command Center*, step 2: Works in Rental Resource Configuration → Define how a physical resource behaves when offered as a customer-rental resource.

#### Acceptance for the design

- [ ] Every input above is drawn (29), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-904?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-903`.
- [ ] Every gated control is gated: `RENTAL_CONFIGURE`, `RENTAL_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-905` Rental Inventory & Availability Control

**Provide real-time inventory visibility for rental and operational resources.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_CONFIGURE`, `RENTAL_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/rentals/rental-inventory-availability-control-bo-905` |

**From the Food, Beverage & Retail process.** Rental quantity thresholds per resource: minimum available, transfer threshold, critical threshold, alerts.

**Known correction pending (do not draw the wrong version)**

- **Thresholds have no field in the availability rules it writes.** Why: Fields without data. *(source: screens/P08-venue-back-office.yaml#BO-905; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Minimum available quantity | select field | — | — | — | — | — | — |
| Reorder/transfer threshold | select field | — | — | — | — | — | — |
| Critical threshold | select field | — | — | — | — | — | — |
| Maximum quantity | select field | — | — | — | — | — | — |
| Smart Alerts | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `getRentalAvailability` ?productId |
| Location | picker: choose a location | — | — | `getRentalAvailability` ?locationId |
| From | date and time picker | — | — | `getRentalAvailability` ?from |
| To | date and time picker | — | — | `getRentalAvailability` ?to |
| Quantity | number field | 1 | — | `getRentalAvailability` ?quantity |

#### Outputs: what the screen shows and produces

**Data it reads**: `getRentalAvailability` (onLoad, What is free, with turnaround subtracted)

**Where the user goes next**

- → `BO-903` Equipment & Asset Command Center: *Back to Equipment & Asset Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental inventory availability configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental inventory availability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental inventory availability configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
thresholds: Wheelchair · min 4 available · alert at 2 · critical 1
```

#### Permissions

- `getRentalAvailability` → `RENTAL_VIEW` (read) · staff, guest
- `setRentalAvailabilityRules` → `RENTAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental/equipment items use simplified states — available, rented, faulty/out-of-maintenance (excluded from available inventory until resolved) — not granular custom attributes. Clients supply item data at onboarding; a screen lets them update inventory and item details afterwards. *(agreed · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management; 5. Key Decisions · DI-500)*
- Rental items (e.g. strollers, wheelchairs, towels): inventory and quantity per day, check-out and check-in, with inventory updated automatically on return; a refundable deposit (with guest details) is captured at rental and refunded on return. *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-498)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-905` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-905`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 6
- Flow F269 *Resource Management Configuration board 6: Equipment & Asset Command Center*, step 4: Works in Rental Inventory & Availability Control → Provide real-time inventory visibility for rental and operational resources.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-905?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-903`.
- [ ] Every gated control is gated: `RENTAL_CONFIGURE`, `RENTAL_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-906` Resource Checkout Workspace

**Provide frontline employees with a fast digital interface for issuing physical resources to guests.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_OPERATE`, `RENTAL_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/resource-checkout-workspace-bo-906` |

**From the Food, Beverage & Retail process.** Frontline check-out of a resource to a guest (see BO-904 for the overlap with the rental check-out screens).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Resource | select field | — | — | — | — | — | — |
| Guest | select field | — | — | — | — | — | — |
| Checkout time | select field | — | — | — | — | — | — |
| Expected return | select field | — | — | — | — | — | — |
| Rental duration | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Rental station | select field | — | — | — | — | — | — |
| Employee | select field | — | — | — | — | — | — |
| Condition at checkout | select field | — | — | — | — | — | — |
| Deposit | select field | — | — | — | — | — | — |
| Notes | select field | — | — | — | — | — | — |
| Fast Checkout | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-903` Equipment & Asset Command Center: *Back to Equipment & Asset Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The resource checkout configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the resource checkout untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No resource checkout configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A required precondition is not met, and the response names which — the counter needs to know whether to fetch a signature or a supervisor. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
checkout: Stroller S-14 → Daniel Brooks · 10:20 · due 14:20 · deposit AED 100 cash
```

#### Permissions

- `checkOutRental` → `RENTAL_OPERATE` (operate) · staff
- `getRentalBooking` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental items (e.g. strollers, wheelchairs, towels): inventory and quantity per day, check-out and check-in, with inventory updated automatically on return; a refundable deposit (with guest details) is captured at rental and refunded on return. *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-498)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-906` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-906`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 6
- Flow F269 *Resource Management Configuration board 6: Equipment & Asset Command Center*, step 6: Works in Resource Checkout Workspace → Provide frontline employees with a fast digital interface for issuing physical resources to guests.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-906?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-903`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`, `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-907` Guest & Resource Assignment

**Maintain a live relationship between every checked-out physical resource and the guest responsible for it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_OPERATE`, `RESOURCE_BOOK` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/guest-resource-assignment-bo-907` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Food, Beverage & Retail process.** Which guest holds which resource right now.

**Known correction pending (do not draw the wrong version)**

- **checkOutResource (resources) and assignRentalEquipment (rentals) both attached.** Why: Two models for one hand-out. *(source: screens/P08-venue-back-office.yaml#BO-907; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every guest resource** (data table)

| Shows | Format | Notes |
|---|---|---|
| Guest | text | not in the schema: `Guest` |
| Photograph where available | text | not in the schema: `Photograph where available` |
| Ticket/booking | text | not in the schema: `Ticket/booking` |
| Membership | text | not in the schema: `Membership` |
| Resource | text | not in the schema: `Resource` |
| Resource ID | text | not in the schema: `Resource ID` |
| Checkout time | text | not in the schema: `Checkout time` |
| Expected return | text | not in the schema: `Expected return` |
| Current status | text | not in the schema: `Current status` |
| Deposit | text | not in the schema: `Deposit` |
| Venue | text | not in the schema: `Venue` |
| Responsible employee | text | not in the schema: `Responsible employee` |
| Guest resource timeline | text | not in the schema: `Guest Resource Timeline` |

**The selected guest resource** (detail panel): The pack groups this record's detail under its own headings: “Expected returns”.

| Shows | Format | Notes |
|---|---|---|
| Guest | text | not in the schema: `Guest` |
| Photograph where available | text | not in the schema: `Photograph where available` |
| Ticket/booking | text | not in the schema: `Ticket/booking` |
| Membership | text | not in the schema: `Membership` |
| Resource | text | not in the schema: `Resource` |
| Resource ID | text | not in the schema: `Resource ID` |
| Checkout time | text | not in the schema: `Checkout time` |
| Expected return | text | not in the schema: `Expected return` |
| Current status | text | not in the schema: `Current status` |
| Deposit | text | not in the schema: `Deposit` |
| Venue | text | not in the schema: `Venue` |
| Responsible employee | text | not in the schema: `Responsible employee` |
| Guest resource timeline | text | not in the schema: `Guest Resource Timeline` |

**Where the user goes next**

- → `BO-903` Equipment & Asset Command Center: *Back to Equipment & Asset Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest resource list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest resource untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest resource yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guest resource are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Asset already out, under maintenance, or of the wrong product |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
row: Wheelchair W-03 · Fatima Al Suwaidi · since 09:45 · Main Gate
```

#### Permissions

- `assignRentalEquipment` → `RENTAL_OPERATE` (operate) · staff
- `checkOutResource` → `RESOURCE_BOOK` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

25 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.8 | The system should allow check out & check in feature for rental resources. For example, towels in the water park. Inventory management of these resources should be handled in the system. | Ticketing Catalogue | CONTRACTED | `checkOutResource` |
| 1.2.9 | The system should allow configuration of deposit requirement for rental resources. The collection and return of the deposit at the time of check-in and check-out should be handled within the system. | Ticketing Catalogue | CONTRACTED | `checkOutResource` |
| 1.2.10 | The system should allow linking of a checked-out resource object to a guest profile. Specification of a rental time period for a checked-out resource object should be supported. | Ticketing Catalogue | CONTRACTED | `checkOutResource` |
| 7.4.10 | The system can manage Cabins rental | F&B POS | CONTRACTED | `checkOutResource` |
| 7.4.36 | Lockers can be managed by the system (sales and inventory) | F&B POS | CONTRACTED | `checkOutResource` |
| 7.4.37 | Wheelchairs can be managed by the system (sales and inventory) | F&B POS | CONTRACTED | `checkOutResource` |
| 7.4.38 | Strollers can be managed by the system (sales and inventory) | F&B POS | CONTRACTED | `checkOutResource` |
| 7.4.51 | Track serial numbers for RFID wristbands, devices, lockers, tablets and rental assets. Record assignment, location, status and movement history. | F&B POS | CONTRACTED | `checkOutResource` |
| 7.4.52 | Manage deposits for rented assets such as lockers, strollers, wheelchairs and equipment. Support collection, refund, partial refund and forfeiture workflows. | F&B POS | CONTRACTED | `checkOutResource` |
| 7.6.1 | Functional Requirements Ability to create and manage rental products (Bike, Kayak, Watercraft, Stroller, Cabana, Locker, Wheelchair, etc.). Configure: - Product Code - Product Name - Description - … | F&B POS | CONTRACTED | `checkOutResource` |
| 7.6.2 | Serial Number Management Support unique serial number assignment for each rental item. Ability to: - Create serial numbers - Activate/Deactivate serial numbers Mark item as: - Available - Rented - … | F&B POS | CONTRACTED | `checkOutResource` |
| 7.6.3 | Functional Requirements Real-time inventory tracking. Maintain available inventory by: - Product - Date - Time Slot - Location Automatically reduce inventory upon reservation. Automatically restore … | F&B POS | CONTRACTED | `checkOutResource` |
| … 13 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-907` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-907`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 6
- Flow F269 *Resource Management Configuration board 6: Equipment & Asset Command Center*, step 8: Works in Guest & Resource Assignment → Maintain a live relationship between every checked-out physical resource and the guest responsible for it.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-907?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-903`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`, `RESOURCE_BOOK`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-908` Rental Duration, Extension & Return Management

**Control rental periods and manage extensions, overdue items, and returns.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_OPERATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `bookingId` (navigation) |
| Route | `/rentals/rental-duration-extension-return-management-bo-908` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Food, Beverage & Retail process.** Extensions, overdue items and returns for resources, with usage-based charging at return (paid 1 h, used 3 h → 2 extra hours).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every rental duration extension** (data table)

| Shows | Format | Notes |
|---|---|---|
| Resource | text | not in the schema: `Resource` |
| Guest | text | not in the schema: `Guest` |
| Checkout | text | not in the schema: `Checkout` |
| Due time | text | not in the schema: `Due time` |
| Remaining time | text | not in the schema: `Remaining time` |
| Status | text | not in the schema: `Status` |
| Deposit | text | not in the schema: `Deposit` |
| Extension eligibility | text | not in the schema: `Extension eligibility` |
| Status indicators | text | not in the schema: `Status Indicators` |
| Active | text | not in the schema: `Active` |
| Due soon | text | not in the schema: `Due Soon` |
| Overdue | text | not in the schema: `Overdue` |
| Extended | text | not in the schema: `Extended` |
| Return pending | text | not in the schema: `Return Pending` |
| Returned | text | not in the schema: `Returned` |
| Extension | text | not in the schema: `Extension` |

**The selected rental duration extension** (detail panel): The pack groups this record's detail under its own headings: “Extend Rental”, “On return”, “Possible next status”, “Overdue Management”.

| Shows | Format | Notes |
|---|---|---|
| Resource | text | not in the schema: `Resource` |
| Guest | text | not in the schema: `Guest` |
| Checkout | text | not in the schema: `Checkout` |
| Due time | text | not in the schema: `Due time` |
| Remaining time | text | not in the schema: `Remaining time` |
| Status | text | not in the schema: `Status` |
| Deposit | text | not in the schema: `Deposit` |
| Extension eligibility | text | not in the schema: `Extension eligibility` |
| Status indicators | text | not in the schema: `Status Indicators` |
| Active | text | not in the schema: `Active` |
| Due soon | text | not in the schema: `Due Soon` |
| Overdue | text | not in the schema: `Overdue` |
| Extended | text | not in the schema: `Extended` |
| Return pending | text | not in the schema: `Return Pending` |
| Returned | text | not in the schema: `Returned` |
| Extension | text | not in the schema: `Extension` |

**Where the user goes next**

- → `BO-903` Equipment & Asset Command Center: *Back to Equipment & Asset Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental duration extension list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental duration extension untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental duration extension yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental duration extension are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The equipment is reserved for a later booking. The conflicting booking's window is named, so the counter can offer a shorter extension instead of a refusal.; 422 `quoteExpired` or `quoteMismatch` on `acceptedQuoteId`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
return: Wheelchair W-03 · paid 1 h · used 3 h · extra 2 h AED 40
```

#### Permissions

- `extendRental` → `RENTAL_OPERATE` (operate) · staff
- `returnRental` → `RENTAL_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Usage-based billing at return: excess charged on actual vs. paid duration (e.g. a wheelchair paid for one hour but used for three is charged two extra hours at return). *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-499)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-908` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-908`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 6
- Flow F269 *Resource Management Configuration board 6: Equipment & Asset Command Center*, step 10: Works in Rental Duration, Extension & Return Management → Control rental periods and manage extensions, overdue items, and returns.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (32 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-908?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-903`.
- [ ] Every gated control is gated: `RENTAL_OPERATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-909` Deposit & Rental Financial Control

**Configure and manage deposits associated with rental resources.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_PRICE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/deposit-rental-financial-control-bo-909` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Food, Beverage & Retail process.** Deposit and fee policy for resources (see BO-529/BO-531, which write the same policies).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every deposit rental financial** (data table)

| Shows | Format | Notes |
|---|---|---|
| Required | text | not in the schema: `Required` |
| Collected | text | not in the schema: `Collected` |
| Authorized | text | not in the schema: `Authorized` |
| Held | text | not in the schema: `Held` |
| Partially retained | text | not in the schema: `Partially retained` |
| Returned | text | not in the schema: `Returned` |
| Forfeited | text | not in the schema: `Forfeited` |
| Return decision | text | not in the schema: `Return Decision` |

**The selected deposit rental financial** (detail panel): The pack groups this record's detail under its own headings: “Stroller”, “Premium Camera”, “Collection Methods”, “Upon resource return”, “Governance”, “Finance Integration”.

| Shows | Format | Notes |
|---|---|---|
| Required | text | not in the schema: `Required` |
| Collected | text | not in the schema: `Collected` |
| Authorized | text | not in the schema: `Authorized` |
| Held | text | not in the schema: `Held` |
| Partially retained | text | not in the schema: `Partially retained` |
| Returned | text | not in the schema: `Returned` |
| Forfeited | text | not in the schema: `Forfeited` |
| Return decision | text | not in the schema: `Return Decision` |

**Where the user goes next**

- → `BO-903` Equipment & Asset Command Center: *Back to Equipment & Asset Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The deposit rental financial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the deposit rental financial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No deposit rental financial yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the deposit rental financial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy: Strollers · deposit AED 100 cash or card · late AED 10/h
```

#### Permissions

- `setRentalDepositPolicy` → `RENTAL_PRICE` (operate) · staff
- `setRentalFeePolicy` → `RENTAL_PRICE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental items (e.g. strollers, wheelchairs, towels): inventory and quantity per day, check-out and check-in, with inventory updated automatically on return; a refundable deposit (with guest details) is captured at rental and refunded on return. *(client request · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management · DI-498)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-909` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-909`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 6
- Flow F269 *Resource Management Configuration board 6: Equipment & Asset Command Center*, step 12: Works in Deposit & Rental Financial Control → Configure and manage deposits associated with rental resources.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-909?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-903`.
- [ ] Every gated control is gated: `RENTAL_PRICE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-910` Maintenance & Resource Blocking

**Prevent unavailable or unsafe resources from being assigned, rented, or reserved.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_VIEW`, `RESOURCE_MANAGE`, `WORK_ORDER_MANAGE` (1 read, 2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `blockId` (navigation) |
| Route | `/rentals/maintenance-resource-blocking-bo-910` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Takes an unsafe or broken resource out of use: a maintenance record (type, issue, severity, start, expected and actual completion, technician or vendor, cost, attachments) that immediately blocks new reservations, checkout, assignment and event allocation, lists the future bookings it hits, and hands them to the replacement engine. The one thing to get right: one action blocks and raises the repair, and the affected bookings are shown before the user leaves the screen.

**Known correction pending (do not draw the wrong version)**

- **"Manufacturer service" is the primary button and "Automatic Blocking" a selectField** Why: Manufacturer service is a maintenance type; automatic blocking is behaviour, not a field. The primary action is Start maintenance. *(source: screens/P08-venue-back-office.yaml#BO-910; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **A resource has no link to its maintenance asset** Why: Blocking the resource and raising the asset's work order are two unconnected acts; the work order cannot name the resource it blocks. *(source: contracts/satellite/resources.yaml#/components/schemas/Resource / contracts/satellite/maintenance.yaml#createWorkOrder; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's maintenance calendar has no calendar component** Why: Every calendar has Day, Week and Month views (VO-R01). *(source: screens/P08-venue-back-office.yaml#BO-910; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): releaseResourceBlock is not bound (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Resource | select field | — | — | — | — | — | — |
| Maintenance type | select field | — | — | — | — | — | — |
| Issue | select field | — | — | — | — | — | — |
| Severity | select field | — | — | — | — | — | — |
| Start date/time | select field | — | — | — | — | — | — |
| Expected completion | select field | — | — | — | — | — | — |
| Actual completion | select field | — | — | — | — | — | — |
| Technician/vendor | select field | — | — | — | — | — | — |
| Cost | select field | — | — | — | — | — | — |
| Attachments | select field | — | — | — | — | — | — |
| Notes | select field | — | — | — | — | — | — |
| Automatic Blocking | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Within days | number field (days) | 14 | — | `getDueMaintenance` ?withinDays |
| From | date and time picker | — | — | `getDueMaintenance` ?from |
| To | date and time picker | — | — | `getDueMaintenance` ?to |
| Category | picker: choose a category | — | — | `getDueMaintenance` ?categoryId |

**Form: Create resource cost** (modal, opened by *Create resource cost*; *Create resource cost* calls `createResourceCost`, *Cancel* sends nothing)

**Collects what `createResourceCost` sends before it is called.** Required: `resourceId`, `kind`, `amount`, `incurredOn`. Optional: `fromVenueId`, `toVenueId`, `note`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

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

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Resource and maintenance type**: Resource picker (or scan); type as chips Preventive, Corrective, Emergency, Scheduled, Inspection-triggered, Manufacturer service. *(source: screens/P08-venue-back-office.yaml#BO-910)*
- **Issue and severity**: Issue text with photos (photo-first); severity Low / Medium / High / Critical feeding the work order's fault assessment. *(source: screens/P08-venue-back-office.yaml#BO-910 / contracts/satellite/maintenance.yaml#createWorkOrder)*
- **Window**: Start date-time (default now) and expected completion; these are the block's from and to. Actual completion is set when the block is released, not typed up front. *(source: contracts/satellite/resources.yaml#createResourceBlock)*
- **Technician / vendor, cost**: Technician from the work-order assignee suggestion or a vendor; cost recorded as an operating cost entry in AED. *(source: contracts/satellite/maintenance.yaml#suggestWorkOrderAssignee / contracts/satellite/resources.yaml#createResourceCost)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Manufacturer service (primary button) | navigation or local | — | — | — | — |
| Create resource cost (secondary button) | `createResourceCost` POST `/resource-costs` | ResourceCostEntry | ResourceCostEntry | 422 Unknown resource at this venue; a `transfer` without both venues or with the same venue twice; a non-positive amount. | gated `RESOURCE_MANAGE`; opens modal first |
| Release block (secondary button) | `releaseResourceBlock` DELETE `/resource-blocks/{blockId}` | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Future booking impact**: "Projector P-01 blocked for maintenance - 3 future assignments affected" with the list and a "Find replacements" button (BO-902). *(source: screens/P08-venue-back-office.yaml#BO-910)*
- **Tabs**: Active maintenance (resource, issue, severity, start, expected completion, status), Maintenance calendar (Day/Week/Month, VO-R01), History. *(source: screens/P08-venue-back-office.yaml#BO-910)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Start maintenance**: Creates the maintenance block (reason maintenance) and raises the work order; refused if the window overlaps a confirmed booking unless the person may override - the clash is named. *(source: contracts/satellite/resources.yaml#createResourceBlock / contracts/satellite/maintenance.yaml#createWorkOrder / DI-484)*
- **Complete / return to service**: Releases the block with actual completion; where the asset category requires inspection, return waits for it. *(source: contracts/satellite/resources.yaml#releaseResourceBlock / contracts/satellite/maintenance.yaml#setAssetStatus)*
- **Add cost**: Books an operating cost against the resource. *(source: contracts/satellite/resources.yaml#createResourceCost)*

**Data it reads**: `getDueMaintenance` (onLoad, What is due)

**Where the user goes next**

- → `BO-903` Equipment & Asset Command Center: *Back to Equipment & Asset Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The maintenance resource blocking configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the maintenance resource blocking untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No maintenance resource blocking configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Bookings already exist in the window. They are listed, because blocking over a booked resource is sometimes right and must never be silent. (ResourceConflictProblem); 422 Unknown resource at this venue; a `transfer` without both venues or with the same venue twice; a non-positive amount. |

#### Edge cases to draw

- **Emergency on an item currently checked out to a guest**: Block starts at return; the screen shows "Out with Sara Al Nuaimi until 16:00 - recall?". *(source: designer default)*
- **Expected completion passes with the block still open**: Overdue badge; future bookings beyond the original date flagged again. *(source: designer default)*

#### Consistency with other screens

- Match `BO-870`: The lead's operational blocking uses the same blocks; this is its maintenance-specific entry.
- Match `BO-576`: Due preventive tasks from the maintenance calendar appear here and on the same calendar component.
- Match `BO-902`: Affected bookings go to recovery with trigger Maintenance.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
record:
  resource: Projector P-17
  type: Corrective
  issue: Lamp failure - no image
  severity: High
  start: Sat 10 Oct 2026 09:00
  expected: Sat 10 Oct 2026 15:00
  technician: Rahul Menon
  cost: AED 450.00
impact: 3 future assignments affected - Corporate Conference 13:00, Product Launch 15:00, Training 17:00
```

#### Permissions

- `createResourceBlock` → `RESOURCE_MANAGE` (configure) · staff
- `createWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `getDueMaintenance` → `ASSET_VIEW` (read) · staff
- `createResourceCost` → `RESOURCE_MANAGE` (configure) · staff
- `releaseResourceBlock` → `RESOURCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 16.5.25 | Corrective Maintenance - System shall support corrective maintenance tracking. | Device Management | CONTRACTED | `createWorkOrder` |
| 16.5.26 | Maintenance Work Orders - System shall support device maintenance work orders. | Device Management | CONTRACTED | `createWorkOrder` |
| 17.3.1 | Maintenance Requests - System shall support maintenance requests. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.3.2 | Breakdown Management - System shall support equipment breakdown management. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.3.3 | Emergency Maintenance - System shall support emergency maintenance requests. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.1 | Work Order Creation - System shall support work order creation. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.2 | Work Order Assignment - System shall support work order assignment. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.3 | Work Order Prioritization - System shall support work order prioritization. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.4 | Work Order Status Management - System shall support work order lifecycle management. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.2.4 | Automated Work Order Generation - System shall automatically generate preventive maintenance work orders. | Maintenance & Safety Management | CONTRACTED | `getDueMaintenance` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental/equipment items use simplified states — available, rented, faulty/out-of-maintenance (excluded from available inventory until resolved) — not granular custom attributes. Clients supply item data at onboarding; a screen lets them update inventory and item details afterwards. *(agreed · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management; 5. Key Decisions · DI-500)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-910` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-910`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 6
- Flow F269 *Resource Management Configuration board 6: Equipment & Asset Command Center*, step 14: Works in Maintenance & Resource Blocking → Prevent unavailable or unsafe resources from being assigned, rented, or reserved.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (400, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-910?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Manufacturer service, Create resource cost, Release block.
- [ ] Every transition is wired: `BO-903`.
- [ ] Every gated control is gated: `ASSET_VIEW`, `RESOURCE_MANAGE`, `WORK_ORDER_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-911` Inspection, Condition & Compliance Management

**Ensure physical resources remain safe, compliant, and operationally fit for use.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 1 · needs the `resources` module |
| Block | Block A · task APP-SETUP-BO-911 |
| Who uses it | venue staff holding `INSPECTION_MANAGE`, `INSPECTION_SUBMIT`, `INSPECTION_VIEW` (1 configure, 1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/inspection-condition-compliance-management-bo-911` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): recordRentalInspection records a rental booking's pre- or post-rental condition; a compliance inspection of a resource is not tied to a booking. submitInspection …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Inspection and compliance for physical resources (strollers, AV kits, wheelchairs, cabanas): checklists by resource type, inspection results with evidence, and a compliance schedule that says when each item was last and is next inspected, who is responsible, and whether it is compliant. A failed or unsafe result blocks the resource automatically and can raise a maintenance request. The one thing to get right: the compliance schedule is the list (what is due, overdue, non-compliant), and the result vocabulary leads straight to the blocking consequence.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The six-value result does not exist (CHG-SBO-005)
- Next inspection, frequency per resource, responsible person and compliance status have no source (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Bound to recordRentalInspection with entry parameter bookingId (CHG-WIR-001); Result values used as action-bar buttons ("Passed with Observation", "Failed", "Evidence") (CHG-SBO-009).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Do resource inspections use the maintenance inspection model (asset register) for every bookable resource, which needs each resource to have an asset record?** → Drawn default accepted: Assume every inspected resource is also an asset (Asset.resourceId); draw resources without one as "Not on the asset register". *(decided by Chinmay, 2026-10-02; DEC-513 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Template | picker: choose a template | — | — | `listInspections` ?templateId |
| Asset | upload, or pick from the media library | — | — | `listInspections` ?assetId |
| Outcome | segmented control | — | Passed · Passed with observations · Failed | `listInspections` ?outcome |
| Performed from | date picker | — | — | `listInspections` ?performedFrom |
| Performed to | date picker | — | — | `listInspections` ?performedTo |

**Form: New template** (modal, opened by *New template*; *New template* calls `createInspectionTemplate`, *Cancel* sends nothing)

**Collects what `createInspectionTemplate` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Instructions `instructions` | text field | optional | — | — | — | The procedure itself. A technician asking how to isolate a chiller is asking a safety question, and the answer has to come from the template rather than from its title. | `createInspectionTemplate` body |
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createInspectionTemplate` body |
| Code `code` | text field | required | — | max length 64 | — | — | `createInspectionTemplate` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createInspectionTemplate` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createInspectionTemplate` body |
| Applies to asset category `appliesToAssetCategoryId` | picker: choose an applies to asset category | optional | — | — | shows names, sends the id | — | `createInspectionTemplate` body |
| Frequency `frequency` | select | optional | — | Pre opening · Post closing · Daily · Weekly · Monthly · Annual · Ad hoc | — | — | `createInspectionTemplate` body |
| Items `items` | repeatable rows | required | — | at least 1 | — | — | `createInspectionTemplate` body |
| Key `items[].key` | text field | required | — | — | — | — | `createInspectionTemplate` body |
| Label `items[].label` | text field | required | — | — | — | — | `createInspectionTemplate` body |
| Kind `items[].kind` | select | required | — | Pass fail · Yes no · Numeric · Text · Photo · Signature | — | — | `createInspectionTemplate` body |
| Is required `items[].isRequired` | toggle | required | — | — | — | — | `createInspectionTemplate` body |
| Is safety critical `items[].isSafetyCritical` | toggle | optional | off | A failed safety-critical item blocks the inspection from passing and cannot be overridden by completing the rest. | — | A failed safety-critical item blocks the inspection from passing and cannot be overridden by completing the rest. | `createInspectionTemplate` body |
| Requires photo on fail `items[].requiresPhotoOnFail` | toggle | optional | on | — | — | — | `createInspectionTemplate` body |
| Min value `items[].minValue` | number field | optional | — | — | — | — | `createInspectionTemplate` body |
| Max value `items[].maxValue` | number field | optional | — | — | — | — | `createInspectionTemplate` body |
| Guidance `items[].guidance` | text field | optional | — | — | — | — | `createInspectionTemplate` body |
| Retention years `retentionYears` | number field | optional | 7 | — | — | Compliance inspections are retained alongside the financial trail. | `createInspectionTemplate` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `createInspectionTemplate` body |

**Form: Record inspection** (modal, opened by *Record inspection*; *Record inspection* calls `submitInspection`, *Cancel* sends nothing)

**Collects what `submitInspection` sends before it is called.** Required: `templateId`, `venueId`, `responses`, `recordedAt`. Optional: `assetId`, `signatureRef`. `id` is a client UUIDv7 generated silently, never asked. The result (passed, passed with observations, failed) is a choice inside the inspection; evidence is a section of it, not a button. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `submitInspection` body |
| Template `templateId` | picker: choose a template | required | — | — | shows names, sends the id | — | `submitInspection` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `submitInspection` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `submitInspection` body |
| Responses `responses` | repeatable rows | required | — | at least 1 | — | — | `submitInspection` body |
| Key `responses[].key` | text field | required | — | — | — | — | `submitInspection` body |
| Value `responses[].value` | field | required | — | — | — | — | `submitInspection` body |
| Passed `responses[].passed` | toggle | optional | — | — | — | — | `submitInspection` body |
| Note `responses[].note` | text area | optional | — | max length 1000 | — | — | `submitInspection` body |
| Attachment refs `responses[].attachmentRefs` | list of values (chips) | optional | — | — | — | — | `submitInspection` body |
| Signature ref `signatureRef` | text field | optional | — | — | — | — | `submitInspection` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `submitInspection` body |

Errors to draw in the form: 400 A required item was not answered

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Inspection template**: Built per resource type - items (pass/fail, yes/no, number with range, text, photo, signature), safety-critical flag, photo on fail; reuses the maintenance template builder, not a second one. *(source: screens/P08-venue-back-office.yaml#BO-911 / contracts/satellite/maintenance.yaml#createInspectionTemplate)*
- **Result**: Passed, Passed with observation, Cleaning required, Maintenance required, Failed, Unsafe - one choice, in that order, with colours from green to red. Maintenance required, Failed and Unsafe show what will happen ("Stroller S-114 will be blocked; raise a maintenance request?"). *(source: screens/P08-venue-back-office.yaml#BO-911 / screens/P08-venue-back-office.yaml#BO-912)*
- **Evidence**: Photos, documents, notes, signature; signature required to submit. *(source: screens/P08-venue-back-office.yaml#BO-911 / contracts/satellite/maintenance.yaml#submitInspection)*

#### Outputs: what the screen shows and produces

**Shown**

**Inspections** (data table, from `listInspections`)

| Shows | Format | Notes |
|---|---|---|
| Template name | text | — |
| Asset | the image or video | — |
| Outcome | chip: Passed, Passed with observations, Failed | — |
| Failed item count | 1,234 | — |
| Failed safety critical count | 1,234 | — |
| Performed at | 1 Oct 2026, 14:30 | — |

**Inspection templates** (data table, from `listInspectionTemplates`)

| Shows | Format | Notes |
|---|---|---|
| Instructions | text | The procedure itself. A technician asking how to isolate a chiller is asking a safety question, and the answer has to come from the … |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Applies to asset category | the name it points at, never the id | — |
| Frequency | chip: Pre opening, Post closing, Daily, Weekly, Monthly, Annual… | — |
| Items | list or chips (count when long) | — |
| Key | text | — |
| Label | text | — |
| Kind | chip: Pass fail, Yes no, Numeric, Text, Photo, Signature | — |
| Is required | yes / no (icon or chip) | — |
| Is safety critical | yes / no (icon or chip) | A failed safety-critical item blocks the inspection from passing and cannot be overridden by completing the rest. |
| Requires photo on fail | yes / no (icon or chip) | — |
| Min value | 1,234.5 | — |
| Max value | 1,234.5 | — |
| Guidance | text | — |
| Retention years | 1,234 | Compliance inspections are retained alongside the financial trail. |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| New template (secondary button) | `createInspectionTemplate` POST `/inspection-templates` | InspectionTemplate | InspectionTemplate | — | opens modal first |
| Record inspection (primary button) | `submitInspection` POST `/inspections` | SubmitInspectionRequest | InspectionResult | 400 A required item was not answered | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Compliance schedule**: Columns Resource, Type, Last inspection, Next inspection, Frequency, Responsible person, Compliance status (Compliant, Due soon, Overdue, Non-compliant), Automatic status (Available or Blocked). Overdue and non-compliant first. *(source: screens/P08-venue-back-office.yaml#BO-911)*
- **Inspection history**: Per resource, inspections with result, inspector and time, retained for seven years. *(source: contracts/satellite/maintenance.yaml#listInspections)*
- **AI pattern note**: "Projector P-17 failed three power-related inspections in 60 days - consider replacement assessment", advisory. *(source: screens/P08-venue-back-office.yaml#BO-912)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Start inspection**: Opens the resource's template; submitting records the result and, for Failed or Unsafe, blocks the resource and offers a maintenance request. *(source: screens/P08-venue-back-office.yaml#BO-912 / contracts/satellite/maintenance.yaml#submitInspection)*
- **Create maintenance request**: Raises a work order on the resource's asset pre-filled with the failed items. *(source: screens/P08-venue-back-office.yaml#BO-912 / contracts/satellite/maintenance.yaml#createWorkOrder)*

**Data it reads**: `listInspections` (onLoad, Inspections so far); `listInspectionTemplates` (onLoad, The compliance inspection templates)

**Where the user goes next**

- → `BO-903` Equipment & Asset Command Center: *Back to Equipment & Asset Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The inspection condition compliance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the inspection condition compliance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No inspection condition compliance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the inspection condition compliance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A required item was not answered |

#### Edge cases to draw

- **Resource booked when it fails inspection**: Blocking lists the future assignments affected and triggers the replacement flow of the resource board. *(source: screens/P08-venue-back-office.yaml#BO-910)*
- **Inspection done offline**: Queues; the block applies on the device that did it at once and on the server at sync. *(source: contracts/satellite/maintenance.yaml#submitInspection)*

#### Consistency with other screens

- Match `BO-903`: Reached from and returns to the Equipment & Asset Command Center.
- Match `EMP-048`: Same inspection item component on the Staff App.
- Match `BO-910`: Blocking and the maintenance calendar of resources live there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
schedule:
- resource: Stroller S-114
  type: Stroller
  last: 28 Sep 2026
  next: 5 Oct 2026
  frequency: Weekly
  responsible: Maria Santos
  compliance: Compliant
  status: Available
- resource: Projector P-17
  type: AV equipment
  last: 30 Sep 2026 - Failed
  next: '-'
  frequency: Monthly
  responsible: Omar Haddad
  compliance: Non-compliant
  status: Blocked
- resource: Wheelchair WC-014
  type: Mobility
  last: 1 Sep 2026
  next: 1 Oct 2026
  frequency: Monthly
  responsible: Maria Santos
  compliance: Overdue
  status: Available
```

#### Permissions

- `submitInspection` → `INSPECTION_SUBMIT` (operate) · staff
- `listInspections` → `INSPECTION_VIEW` (read) · staff
- `listInspectionTemplates` → `INSPECTION_VIEW` (read) · staff
- `createInspectionTemplate` → `INSPECTION_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.5.7 | Safety Audits - System shall support safety audits. | Maintenance & Safety Management | CONTRACTED | `submitInspection` |
| 17.5.9 | Safety Compliance Tracking - System shall support safety compliance tracking. | Maintenance & Safety Management | CONTRACTED | `listInspections` |
| 17.5.1 | Safety Inspections - System shall support safety inspections. | Maintenance & Safety Management | CONTRACTED | `createInspectionTemplate` |
| 17.5.2 | Safety Checklists - System shall support configurable safety checklists. | Maintenance & Safety Management | CONTRACTED | `createInspectionTemplate` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-911` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-911`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 6
- Flow F269 *Resource Management Configuration board 6: Equipment & Asset Command Center*, step 16: Works in Inspection, Condition & Compliance Management → Ensure physical resources remain safe, compliant, and operationally fit for use.

#### Acceptance for the design

- [ ] Every input above is drawn (31), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-911?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: New template, Record inspection.
- [ ] Every transition is wired: `BO-903`.
- [ ] Every gated control is gated: `INSPECTION_MANAGE`, `INSPECTION_SUBMIT`, `INSPECTION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-912` Asset Lifecycle, Depreciation & Retirement

**Manage the physical resource from acquisition through operational use to final retirement.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_VIEW`, `RESOURCE_MANAGE`, `RESOURCE_VIEW` (2 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | `assetId` (navigation), `resourceId` (navigation) |
| Route | `/rentals/asset-lifecycle-depreciation-retirement-bo-912` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The life of a physical item from order to disposal: lifecycle timeline, acquisition and warranty facts, depreciation reference (method, useful life, accumulated, net book value), maintenance and utilisation history, a retirement assessment with a replacement recommendation, and the retirement workflow with approvals and disposal details. The one thing to get right: Finance owns the accounting; this screen holds operational references and makes sure a retired item never appears available again.

**Known correction pending (do not draw the wrong version)**

- **No field anywhere holds purchase cost, useful life, depreciation method, accumulated depreciation or book value** Why: Neither Resource nor the maintenance Asset carries them; the depreciation tab has no source. *(source: contracts/satellite/resources.yaml#/components/schemas/Resource / contracts/satellite/maintenance.yaml#createAsset; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Three different lifecycles meet on this screen (the pack's nine, ResourceLifecycleState, AssetStatus)** Why: Ordered, Received, In use, End of life and Disposed exist in none of the resource states; the asset has inService, outOfService, underMaintenance, awaitingParts, retired, disposed. *(source: screens/P08-venue-back-office.yaml#BO-912 / contracts/satellite/resources.yaml#/components/schemas/ResourceLifecycleState / contracts/satellite/maintenance.yaml#setAssetStatus; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The purpose text includes board 7's objective; a "-> End of Life" button and a raw resource cost table (id, scopePath) are on the screen (CHG-WIR-003).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Resource id | picker: choose a resource (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?resourceId=` to `listResourceCosts`. | `listResourceCosts` ?resourceId |
| Kind | segmented control | optional | — | Transfer · Operating · Replacement | — | Sends `?kind=` to `listResourceCosts`. | `listResourceCosts` ?kind |
| From | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?from=` to `listResourceCosts`. | `listResourceCosts` ?from |
| To | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?to=` to `listResourceCosts`. | `listResourceCosts` ?to |

**Form: Create resource cost** (modal, opened by *Create resource cost*; *Create resource cost* calls `createResourceCost`, *Cancel* sends nothing)

**Collects what `createResourceCost` sends before it is called.** Required: `resourceId`, `kind`, `amount`, `incurredOn`. Optional: `fromVenueId`, `toVenueId`, `note`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

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

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Asset information**: Acquisition date, purchase cost (AED), supplier, warranty to-date, expected useful life (years), replacement value, depreciation method (Straight-line or configured) and period. *(source: screens/P08-venue-back-office.yaml#BO-912)*
- **Retirement**: Reason, retirement date, disposal method (Sale, Scrap, Donation, Return to supplier), disposal value, replacement resource; approvals by Operations, Finance and Asset manager as required. *(source: screens/P08-venue-back-office.yaml#BO-912 / contracts/satellite/resources.yaml#setResourceLifecycleState)*

#### Outputs: what the screen shows and produces

**Shown**

**Every asset lifecycle depreciation** (data table)

| Shows | Format | Notes |
|---|---|---|
| Acquisition date | text | not in the schema: `Acquisition date` |
| Purchase cost | text | not in the schema: `Purchase cost` |
| Supplier | text | not in the schema: `Supplier` |
| Warranty | text | not in the schema: `Warranty` |
| Expected useful life | text | not in the schema: `Expected useful life` |
| Replacement value | text | not in the schema: `Replacement value` |
| Current book/reference value | text | not in the schema: `Current book/reference value` |
| Depreciation method | text | not in the schema: `Depreciation method` |
| Depreciation period | text | not in the schema: `Depreciation period` |
| Maintenance history | text | not in the schema: `Maintenance history` |
| Utilization | text | not in the schema: `Utilization` |
| Condition | text | not in the schema: `Condition` |
| Depreciation | text | not in the schema: `Depreciation` |
| Straight line depreciation | text | not in the schema: `Straight-line depreciation` |
| Configurable financial method | text | not in the schema: `Configurable financial method` |
| Accumulated depreciation | text | not in the schema: `Accumulated depreciation` |
| Current value | text | not in the schema: `Current value` |

**Every resource cost entry** (data table, from `listResourceCosts`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Transfer, Operating, Replacement | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Incurred on | 1 Oct 2026 | — |
| Note | text | — |

**The selected asset lifecycle depreciation** (detail panel): The pack groups this record's detail under its own headings: “Retirement Assessment”, “Projector P-17”, “Retirement may require”, “Stroller S-084”, “Typical operational states include”, “Board 6 shall integrate with”.

| Shows | Format | Notes |
|---|---|---|
| Acquisition date | text | not in the schema: `Acquisition date` |
| Purchase cost | text | not in the schema: `Purchase cost` |
| Supplier | text | not in the schema: `Supplier` |
| Warranty | text | not in the schema: `Warranty` |
| Expected useful life | text | not in the schema: `Expected useful life` |
| Replacement value | text | not in the schema: `Replacement value` |
| Current book/reference value | text | not in the schema: `Current book/reference value` |
| Depreciation method | text | not in the schema: `Depreciation method` |
| Depreciation period | text | not in the schema: `Depreciation period` |
| Maintenance history | text | not in the schema: `Maintenance history` |
| Utilization | text | not in the schema: `Utilization` |
| Condition | text | not in the schema: `Condition` |
| Depreciation | text | not in the schema: `Depreciation` |
| Straight line depreciation | text | not in the schema: `Straight-line depreciation` |
| Configurable financial method | text | not in the schema: `Configurable financial method` |
| Accumulated depreciation | text | not in the schema: `Accumulated depreciation` |
| Current value | text | not in the schema: `Current value` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| → End of Life (primary button) | navigation or local | — | — | — | — |
| Asset Information (secondary button) | navigation or local | — | — | — | — |
| Create resource cost (secondary button) | `createResourceCost` POST `/resource-costs` | ResourceCostEntry | ResourceCostEntry | 422 Unknown resource at this venue; a `transfer` without both venues or with the same venue twice; a non-positive amount. | gated `RESOURCE_MANAGE`; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Lifecycle timeline**: Ordered, Received, Active, In use, Maintenance, Suspended, End of life, Retired, Disposed with dates; current state highlighted. *(source: screens/P08-venue-back-office.yaml#BO-912)*
- **Depreciation summary**: Method, useful life, purchase cost, accumulated depreciation, net book value, labelled "Reference - accounting in Finance". *(source: screens/P08-venue-back-office.yaml#BO-912)*
- **Retirement assessment**: Age, condition, utilisation, maintenance cost YTD, downtime, failure frequency, current value, and an AI recommendation with its reason (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-912)*
- **History**: Work orders, inspections, incidents and status changes in sequence; cost entries (operating, replacement) beneath. *(source: contracts/satellite/maintenance.yaml#getAssetHistory / contracts/satellite/resources.yaml#listResourceCosts)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Start retirement**: Submits the retire transition with disposal and replacement; goes to approval where required; once retired the resource leaves every availability read. *(source: screens/P08-venue-back-office.yaml#BO-912 / contracts/satellite/resources.yaml#setResourceLifecycleState)*
- **Add replacement cost**: Books the cost of the replacing item against the resource. *(source: contracts/satellite/resources.yaml#createResourceCost)*

**Data it reads**: `listResourceCosts` (onLoad, Cost entries booked against resources)

**Where the user goes next**

- → `BO-903` Equipment & Asset Command Center: *Back to Equipment & Asset Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset lifecycle depreciation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset lifecycle depreciation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No asset lifecycle depreciation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the asset lifecycle depreciation are still there. The pack's own statuses are deliver this event? — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The transition is not allowed from the current state, or an approval the configuration requires has not been given. (ResourceTransitionProblem); 422 Unknown resource at this venue; a `transfer` without both venues or with the same venue twice; a non-positive amount. |

#### Edge cases to draw

- **Retiring an item with future bookings**: Refused until the bookings are moved, listing them with a link to recovery. *(source: screens/P08-venue-back-office.yaml#BO-912 / contracts/satellite/resources.yaml#/components/schemas/ResourceTransitionProblem)*

#### Consistency with other screens

- Match `BO-863`: The lifecycle states here must reconcile with the nine resource states of the governance screen.
- Match `BO-582`: Rental write-off and retirement (DI-770) record the same retirement and write-off value.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
asset:
  name: Projector P-17
  tag: P17-AV-00023
  acquired: 15 Jan 2020
  purchase: AED 7,500.00
  usefulLife: 5 years
  accumulated: AED 4,500.00
  netBook: AED 3,000.00
assessment:
  age: 6.7 years
  maintenanceYtd: AED 4,800.00
  downtime: 14 days
  utilisation: 71%
  recommendation: Consider replacement - maintenance cost above the lifecycle threshold
```

#### Permissions

- `setResourceLifecycleState` → `RESOURCE_MANAGE` (configure) · staff
- `getAssetHistory` → `ASSET_VIEW` (read) · staff
- `listResourceCosts` → `RESOURCE_VIEW` (read) · staff
- `createResourceCost` → `RESOURCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 16.5.27 | Maintenance History - System shall maintain maintenance history. | Device Management | CONTRACTED | `getAssetHistory` |
| 17.1.8 | Asset History - System shall maintain complete asset history. | Maintenance & Safety Management | CONTRACTED | `getAssetHistory` |
| 17.3.7 | Service History - System shall maintain service history. | Maintenance & Safety Management | CONTRACTED | `getAssetHistory` |
| 18.3.4 | Asset History - Users shall view maintenance history. | Employee Mobile App & AI Assistant | CONTRACTED | `getAssetHistory` |
| 18.3.5 | Asset Documentation - Users shall access manuals and documents. | Employee Mobile App & AI Assistant | CONTRACTED | `getAssetHistory` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-912` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS131 Resource Management Configuration Board 6.dc.html#bo-912`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 6
- Flow F269 *Resource Management Configuration board 6: Equipment & Asset Command Center*, step 18: Works in Asset Lifecycle, Depreciation & Retirement → Manage the physical resource from acquisition through operational use to final retirement.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (38 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-912?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: → End of Life, Asset Information, Create resource cost.
- [ ] Every transition is wired: `BO-903`.
- [ ] Every gated control is gated: `ASSET_VIEW`, `RESOURCE_MANAGE`, `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"assignRentalEquipment": {"method":"POST","path":"/rental-bookings/{bookingId}/equipment","contract":"rental","summary":"Bind specific assets to the booking, by scan where required","permission":"RENTAL_OPERATE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RentalEquipmentAssignment"},
"checkOutRental": {"method":"POST","path":"/rental-bookings/{bookingId}/check-out","contract":"rental","summary":"Hand it over, with the deposit held and the condition recorded","permission":"RENTAL_OPERATE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalCheckOut","responds":"RentalBooking"},
"checkOutResource": {"method":"POST","path":"/resource-bookings/{bookingId}/check-out","contract":"resources","summary":"Hand it over, with a deposit against it","permission":"RESOURCE_BOOK","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ResourceBooking"},
"createInspectionTemplate": {"method":"POST","path":"/inspection-templates","contract":"maintenance","summary":"Create an inspection template","permission":"INSPECTION_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"InspectionTemplate","responds":"InspectionTemplate"},
"createResourceBlock": {"method":"POST","path":"/resource-blocks","contract":"resources","summary":"Take a resource out of service for a window, with a reason","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceBlock","responds":"ResourceBlock"},
"createResourceCost": {"method":"POST","path":"/resource-costs","contract":"resources","summary":"Book a transfer, operating or replacement cost against a resource","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ResourceCostEntry","responds":"ResourceCostEntry"},
"createWorkOrder": {"method":"POST","path":"/work-orders","contract":"maintenance","summary":"Raise a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateWorkOrderRequest","responds":"WorkOrder"},
"extendRental": {"method":"POST","path":"/rental-bookings/{bookingId}/extend","contract":"rental","summary":"Keep it longer, if it is free and the guest accepts the price","permission":"RENTAL_OPERATE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RentalBooking"},
"getAssetHistory": {"method":"GET","path":"/assets/{assetId}/history","contract":"maintenance","summary":"Service history","permission":"ASSET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getDueMaintenance": {"method":"GET","path":"/maintenance-plans/due","contract":"maintenance","summary":"Planned tasks due or overdue","permission":"ASSET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"withinDays","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null}],"requestBody":null,"responds":"DueMaintenanceTask"},
"getRentalAvailability": {"method":"GET","path":"/rental-availability","contract":"rental","summary":"What can be rented, when, with turnaround already subtracted","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":true},{"name":"locationId","in":"query","required":null},{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"quantity","in":"query","required":null}],"requestBody":null,"responds":"RentalAvailability"},
"getRentalBooking": {"method":"GET","path":"/rental-bookings/{bookingId}","contract":"rental","summary":"One booking, its timeline and its readiness","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RentalBooking"},
"getRentalProduct": {"method":"GET","path":"/rental-products/{productId}","contract":"rental","summary":"The master configuration of one rental product","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RentalProduct"},
"listAssets": {"method":"GET","path":"/assets","contract":"maintenance","summary":"List assets","permission":"ASSET_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"maintenanceDue","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listInspectionTemplates": {"method":"GET","path":"/inspection-templates","contract":"maintenance","summary":"List inspection templates","permission":"INSPECTION_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"InspectionTemplate"},
"listInspections": {"method":"GET","path":"/inspections","contract":"maintenance","summary":"List completed inspections","permission":"INSPECTION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"templateId","in":"query","required":null},{"name":"assetId","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"performedFrom","in":"query","required":null},{"name":"performedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listResourceCosts": {"method":"GET","path":"/resource-costs","contract":"resources","summary":"Cost entries booked against resources","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"resourceId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listResources": {"method":"GET","path":"/resources","contract":"resources","summary":"Resources at this venue","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"availableFrom","in":"query","required":null},{"name":"availableTo","in":"query","required":null}],"requestBody":null,"responds":"Resource"},
"releaseResourceBlock": {"method":"DELETE","path":"/resource-blocks/{blockId}","contract":"resources","summary":"Put it back into service","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"returnRental": {"method":"POST","path":"/rental-bookings/{bookingId}/return","contract":"rental","summary":"Take it back, inspect it, and settle everything at once","permission":"RENTAL_OPERATE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalReturn","responds":"RentalSettlement"},
"setRentalAvailabilityRules": {"method":"PUT","path":"/rental-products/{productId}/availability-rules","contract":"rental","summary":"Operating hours, rental windows, buffers and release rules","permission":"RENTAL_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalAvailabilityRules","responds":"RentalAvailabilityRules"},
"setRentalDepositPolicy": {"method":"PUT","path":"/rental-deposit-policies","contract":"rental","summary":"How much is held, how, and what happens to it","permission":"RENTAL_PRICE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalDepositPolicy","responds":"RentalDepositPolicy"},
"setRentalFeePolicy": {"method":"PUT","path":"/rental-fee-policies","contract":"rental","summary":"Grace period, late fees and extension pricing","permission":"RENTAL_PRICE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalFeePolicy","responds":"RentalFeePolicy"},
"setRentalInventoryModel": {"method":"PUT","path":"/rental-products/{productId}/inventory-model","contract":"rental","summary":"Pooled, serialised or hybrid","permission":"RENTAL_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalInventoryModel","responds":"RentalInventoryModel"},
"setResourceLifecycleState": {"method":"POST","path":"/resources/{resourceId}/state","contract":"resources","summary":"Move a resource through its lifecycle, with a reason","permission":"RESOURCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Resource"},
"submitInspection": {"method":"POST","path":"/inspections","contract":"maintenance","summary":"Submit a completed inspection","permission":"INSPECTION_SUBMIT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SubmitInspectionRequest","responds":"InspectionResult"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Asset": {"x-ticvai-persistence":"maintenance.asset","allOf":[{"$ref":"#/components/schemas/CreateAssetRequest"},{"type":"object","x-ticvai-retired-columns":["is_maintenance_overdue","document_refs"],"required":["id","status"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid","nullable":true,"description":"1.2.x. **Where this asset is also bookable.** An AV rig is an asset to maintain and a resource to allocate, and they are the same object seen from two sides.\n**`resources` owns the calendar and this owns the condition.** An asset out of service makes its resource unbookable, which is one link rather than two models of availability.\n"},"deviceId":{"type":"string","format":"uuid","nullable":true,"description":"BL-160. **Where this asset is also a registered device.** A turnstile is an asset to maintain and a device to operate, and — exactly as with `resourceId` above — they are the same object seen from two sides.\n**Nothing joined them before this.** A turnstile controller reporting `needsAttention` could not raise a work order against itself, and an engineer closing one had no way back to the device whose firmware caused it.\n**Null for most assets and for most devices.** A chiller is not a device and a signature pad is not on the asset register; the link is sparse, and it lives here rather than on `platform.device` because `platform` is the foundation tier and a foreign key pointing from it into `maintenance` would invert the tiers — every cell running a spine would carry a column for a satellite it may not deploy.\n"},"acquisitionCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"acquiredOn":{"type":"string","format":"date","nullable":true},"depreciation":{"type":"object","nullable":true,"description":"**Recorded here and posted by `finance`.** Depreciation is an accounting act and the asset register is where the useful life is actually known — an engineer knows a chiller lasts fifteen years and an accountant knows what to do about it.\n","properties":{"method":{"type":"string","enum":["straightLine","reducingBalance","unitsOfProduction","none"]},"usefulLifeMonths":{"type":"integer"},"residualValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accumulatedDepreciation":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"retiredOn":{"type":"string","format":"date","nullable":true,"description":"**Retirement is not deletion.** A work order from three years ago still names this asset, and an inspection record with no asset is an inspection of nothing.\n"},"disposalProceeds":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"$ref":"#/components/schemas/AssetStatus"},"statusReason":{"type":"string","nullable":true},"openWorkOrderCount":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Work orders on this asset whose status is `open`, `assigned`, `inProgress`, `paused` or `awaitingParts` — the same set `AssetDetail.openWorkOrders` returns. **Maintained on write**: `createWorkOrder` and every transition into or out of that set (complete, cancel, close, reject back to open) adjust it in the same transaction as the work-order row.\n"},"nextMaintenanceDueAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The earliest `nextDueAt` among this asset's active maintenance plans; null when none has one. **Maintained on write**: recomputed whenever one of those plans is created, amended, suspended or has its `nextDueAt` moved by a completed work order. `listAssets?maintenanceDue` filters on this column against the clock.\n"},"isMaintenanceOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`nextMaintenanceDueAt` is in the past at the moment of the read. **Computed on read and not stored** — it depends on the clock, so a stored copy is stale the minute after it is written.\n"},"lastInspectionAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`performedAt` of the latest inspection submitted against this asset. **Maintained on write** by `submitInspection`, in the same transaction as the inspection row; an inspection synced late with an earlier `performedAt` does not move it back.\n"},"usageCounter":{"type":"number","nullable":true,"description":"Cycles, hours or kilometres. Drives usage-based maintenance."}}}]},
"AssetCriticality": {"type":"string","enum":["safetyCritical","revenueCritical","standard","low"]},
"AssetHistoryEntry": {"x-ticvai-persistence":"none — union view over work orders, inspections, incidents and asset status changes","type":"object","description":"**Every kind has a source.** `workOrder` is a work-order row, `inspection` an inspection, `incident` an incident, `statusChange` a `maintenance.asset_status_change` row. `partReplaced` is a completed work order whose `resolutionCode` is `partReplaced`, and `planCompleted` a completed work order with a `sourcePlanId` — both read from `maintenance.work_order`, not stored twice.\n","required":["kind","occurredAt","summary"],"properties":{"kind":{"type":"string","enum":["workOrder","inspection","incident","statusChange","partReplaced","planCompleted"]},"referenceId":{"type":"string","format":"uuid","nullable":true,"description":"The source row's id: a work order, inspection or incident, or an `asset_status_change` id. A uuid, as every id is (ADR-0056).\n"},"summary":{"type":"string"},"principalId":{"type":"string","format":"uuid","nullable":true},"occurredAt":{"type":"string","format":"date-time"}}},
"AssetStatus": {"type":"string","enum":["inService","outOfService","underMaintenance","awaitingParts","retired","disposed"]},
"CreateAssetRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["assetTag","name","venueId","criticality"],"properties":{"assetTag":{"type":"string","maxLength":64,"x-ticvai-unique":"venue","description":"**Unique per venue** (decided 28 September, audit R108). Two assets in one venue never share a tag; `createAsset` refuses a duplicate with `409` `duplicate-code`. Two venues may each have an `A-001`.\n"},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"criticality":{"$ref":"#/components/schemas/AssetCriticality"},"priorityOverride":{"allOf":[{"$ref":"#/components/schemas/WorkOrderPriority"}],"nullable":true,"description":"**\"If this device goes down, raise this priority\"** (decided 17 September, M17-01). A corrective work order raised on this asset takes this priority instead of the score. Null means the score decides.\n"},"manufacturer":{"type":"string","maxLength":200},"model":{"type":"string","maxLength":200},"serialNumber":{"type":"string","maxLength":128},"commissionedAt":{"type":"string","format":"date"},"warrantyExpiresAt":{"type":"string","format":"date"},"supplierId":{"type":"string","format":"uuid"},"linkedProductIds":{"type":"array","description":"Products this asset delivers. A fault here can stop them selling.\n","items":{"type":"string","format":"uuid"}},"linkedAccessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Access point this asset controls. Out of service blocks it."},"requiresInspectionToReturn":{"type":"boolean","default":false,"description":"True means a completed inspection is required before return to service. A technician cannot simply declare a ride safe.\n"},"documents":{"type":"array","description":"Manuals, procedures, certificates, each with its name and kind. Stored one row per document in `maintenance.asset_document`, which is where `AssetDetail.documents` reads them from.\n","items":{"$ref":"#/components/schemas/AssetDocumentInput"}},"documentRefs":{"type":"array","x-ticvai-persisted":false,"description":"**The refs alone, kept for callers that predate `documents`.** Each ref sent here is stored as an `asset_document` row with no name and no kind. Returned as the refs of `documents`, computed on read — there is no second copy to fall out of step.\n","items":{"type":"string"}}}},
"CreateWorkOrderRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","title","venueId","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"title":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":5000},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"kind":{"allOf":[{"$ref":"#/components/schemas/WorkOrderKind"}],"default":"corrective"},"priority":{"allOf":[{"$ref":"#/components/schemas/WorkOrderPriority"}],"description":"**Optional since 29 September** (M17-01). Sent, it is `manual` and wins. Absent, the asset's `priorityOverride` applies, and failing that the venue's `WorkOrderPriorityPolicy` scores the fault.\n"},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","maxItems":10,"items":{"type":"string"},"description":"Skills the job needs, as qualification codes; `suggestWorkOrderAssignee` ranks by them (M17-13)."},"categoryId":{"type":"string","format":"uuid"},"assignedToPrincipalId":{"type":"string","format":"uuid"},"dueAt":{"type":"string","format":"date-time"},"attachmentRefs":{"type":"array","description":"Photo-first. Expected at creation, not added later from memory.","items":{"type":"string"}},"takeAssetOutOfService":{"type":"boolean","default":false,"description":"Raise and immediately suspend the asset. For a fault found on a live ride, the two are one action.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"DueMaintenanceTask": {"x-ticvai-persistence":"none — computed","type":"object","required":["planId","assetId","assetName","dueAt","isOverdue","criticality"],"properties":{"planId":{"type":"string","format":"uuid"},"planName":{"type":"string"},"assetId":{"type":"string","format":"uuid"},"assetName":{"type":"string"},"criticality":{"$ref":"#/components/schemas/AssetCriticality"},"dueAt":{"type":"string","format":"date-time"},"isOverdue":{"type":"boolean"},"daysOverdue":{"type":"integer"},"triggeredBy":{"type":"string","enum":["interval","usage"]},"workOrderId":{"type":"string","format":"uuid","nullable":true}}},
"Inspection": {"x-ticvai-persistence":"maintenance.inspection","type":"object","required":["id","templateId","venueId","outcome","performedByPrincipalId","performedAt"],"properties":{"id":{"type":"string","format":"uuid"},"templateId":{"type":"string","format":"uuid"},"templateName":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"outcome":{"$ref":"#/components/schemas/InspectionOutcome"},"failedItemCount":{"type":"integer"},"failedSafetyCriticalCount":{"type":"integer"},"performedByPrincipalId":{"type":"string","format":"uuid","description":"An inspection nobody signed is not an inspection."},"performedAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true},"retainUntil":{"type":"string","format":"date","nullable":true}}},
"InspectionItem": {"x-ticvai-persistence":"maintenance.inspection_item","type":"object","description":"**One answer to one question, which the API has always accepted and never stored.** `SubmitInspectionRequest.responses[]` takes a key, a value, a pass flag, a note and attachments; the only persistence ever claimed for them was `maintenance.inspection_response`, a table that does not exist.\nSo `maintenance.inspection_template_item` held the questions, `maintenance.inspection` held `failedItemCount` and `failedSafetyCriticalCount`, and **which check failed was accepted over the wire and dropped** — on a record that takes an asset out of service.\nReturned on `InspectionResult`, not on `Inspection`: `listInspections` returns the latter in a list, and twenty item rows per inspection on a list screen is the wrong trade. The counts stay for exactly that reason.\n","required":["id","inspectionId","itemKey"],"properties":{"id":{"type":"string","format":"uuid"},"inspectionId":{"type":"string","format":"uuid"},"templateItemId":{"type":"string","format":"uuid","nullable":true,"description":"**Nullable because a template changes and an inspection does not.** An answer recorded against an item that was later removed still has to be readable, so the key below is the durable record and this is the live link.\n"},"itemKey":{"type":"string","maxLength":120,"description":"The template item's `key`, copied at submission and never updated."},"label":{"type":"string","nullable":true,"description":"The question as it was asked, copied at submission. **A template reworded next season must not silently reword last season's inspection.**\n"},"value":{"nullable":true,"description":"Whatever the item's `kind` calls for — a boolean, a number, a string."},"passed":{"type":"boolean","nullable":true,"description":"Null where the item is informational rather than pass or fail."},"isSafetyCritical":{"type":"boolean","default":false,"description":"Copied from the template item at submission, for the same reason as `label`: it is what makes `failedSafetyCriticalCount` reproducible, and the template can change.\n"},"note":{"type":"string","maxLength":1000,"nullable":true},"attachmentAssetIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"**A deliberate array, and the same exception as `workforce.sync_conflict.affectedAssignmentIds`**: evidence attached to this answer at the moment it was recorded. It is never queried from the other end — nobody asks which inspection items reference a photograph — and it must not change when an asset library is reorganised.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"InspectionItemKind": {"type":"string","enum":["passFail","yesNo","numeric","text","photo","signature"]},
"InspectionOutcome": {"type":"string","enum":["passed","passedWithObservations","failed"]},
"InspectionResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["inspection","consequences"],"properties":{"inspection":{"$ref":"#/components/schemas/Inspection"},"items":{"type":"array","description":"**The answers, which had nowhere to live until 20 September.** A failed safety-critical item takes an asset out of service and `consequences` below says it happened; this says which check caused it.\n","items":{"$ref":"#/components/schemas/InspectionItem"}},"consequences":{"type":"object","description":"What the submission triggered. A failed safety-critical item takes the asset out of service without waiting for anyone to decide.\n","properties":{"assetTakenOutOfService":{"type":"boolean"},"workOrdersRaised":{"type":"array","items":{"type":"string","format":"uuid"}},"productsSuspended":{"type":"array","items":{"type":"string","format":"uuid"}},"escalatedToPrincipalId":{"type":"string","format":"uuid","nullable":true}}}}},
"InspectionTemplate": {"x-ticvai-persistence":"maintenance.inspection_template + maintenance.inspection_template_item","type":"object","required":["id","code","name","items"],"properties":{"instructions":{"type":"string","description":"**The procedure itself.** A technician asking how to isolate a chiller is asking a safety question, and the answer has to come from the template rather than from its title.\n"},"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid","nullable":true},"appliesToAssetCategoryId":{"type":"string","format":"uuid","nullable":true},"frequency":{"type":"string","enum":["preOpening","postClosing","daily","weekly","monthly","annual","adHoc"]},"items":{"type":"array","minItems":1,"items":{"type":"object","required":["key","label","kind","isRequired"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"kind":{"$ref":"#/components/schemas/InspectionItemKind"},"isRequired":{"type":"boolean"},"isSafetyCritical":{"type":"boolean","default":false,"description":"A failed safety-critical item **blocks the inspection from passing** and cannot be overridden by completing the rest.\n"},"requiresPhotoOnFail":{"type":"boolean","default":true},"minValue":{"type":"number","nullable":true},"maxValue":{"type":"number","nullable":true},"guidance":{"type":"string","nullable":true}}}},"retentionYears":{"type":"integer","default":7,"description":"Compliance inspections are retained alongside the financial trail."},"isActive":{"type":"boolean"}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RentalAvailability": {"type":"object","description":"Board 3. **A pooled product answers with a count, a serialised one with assets.**","properties":{"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid","nullable":true},"windows":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"availableQuantity":{"type":"integer"},"availableAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}},"blockedWindows":{"type":"array","items":{"type":"object","properties":{"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"reason":{"type":"string","enum":["booked","turnaround","maintenance","blackout","closed","buffer","held"]}}}}}},
"RentalAvailabilityRules": {"type":"object","x-ticvai-persistence":"rental.availability_rules","description":"Boards 3.2, 3.3 and 3.9. **The hold-release rule is the one that quietly loses stock.**\n","properties":{"operatingWindows":{"type":"array","items":{"type":"object","properties":{"daysOfWeek":{"type":"array","items":{"type":"string"}},"from":{"type":"string"},"to":{"type":"string"}}}},"slotMinutes":{"type":"integer","nullable":true},"holdMinutes":{"type":"integer","default":15,"description":"**How long an unconfirmed basket keeps stock.** A hold that never expires removes inventory from sale after every abandoned checkout.\n"},"releaseOnPaymentFailure":{"type":"boolean","default":true},"overbookPercent":{"type":"number","default":0},"scopePath":{"type":"string"}}},
"RentalBooking": {"type":"object","x-ticvai-persistence":"rental.booking","description":"Board 5. **The booking outlives the order** — an order completes at payment and the rental is still out.\n","required":["id","productId","from","to","status"],"properties":{"id":{"type":"string","format":"uuid"},"reference":{"type":"string"},"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"returnLocationId":{"type":"string","format":"uuid","nullable":true},"customerId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer"},"status":{"type":"string","enum":["draft","confirmed","awaitingArrival","checkedOut","overdue","partiallyReturned","completed","completedWithDamage","notReturned","cancelled","noShow"]},"checkedOutAt":{"type":"string","format":"date-time","nullable":true},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"returnedAt":{"type":"string","format":"date-time","nullable":true},"depositAuthorisationId":{"type":"string","format":"uuid","nullable":true,"description":"The card deposit's terminal pre-authorisation, written by `checkOutRental` (workbook Q304; CHG-CSA-029). The hold is kept whole until every unit is back (workbook Q306)."},"accruedLateFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"readiness":{"type":"array","readOnly":true,"description":"**Computed, not stored** — agreement, requirements, deposit, equipment.","items":{"type":"object","properties":{"check":{"type":"string"},"satisfied":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"participants":{"type":"array","items":{"$ref":"#/components/schemas/RentalParticipant"}},"scopePath":{"type":"string"}}},
"RentalCheckOut": {"type":"object","description":"Board 6. **The readiness gate is enforced server-side.**","properties":{"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"depositInstrument":{"type":"string","nullable":true},"depositAuthorisationId":{"type":"string","format":"uuid","nullable":true,"description":"**The terminal pre-authorisation of a card deposit** (workbook Q304; CHG-CSA-029), as the payments terminal returned it. Required where the deposit is on a card; stored on the booking."},"conditionNote":{"type":"string","nullable":true},"photoAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"safetyBriefingGiven":{"type":"boolean","default":false},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"overrideId":{"type":"string","format":"uuid","nullable":true,"description":"**A supervisor override for a failed precondition**, which is recorded rather than allowed silently.\n"}}},
"RentalDamageAssessment": {"type":"object","x-ticvai-persistence":"rental.damage_assessment","description":"Board 8.6. **A dispute is a state, not a deletion.**","required":["amount","description"],"properties":{"id":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"description":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"inspectionId":{"type":"string","format":"uuid","nullable":true},"assessedBy":{"type":"string","format":"uuid"},"approvedBy":{"type":"string","format":"uuid","nullable":true},"customerAcknowledgement":{"type":"string","enum":["accepted","disputed","notPresented"],"default":"notPresented"},"workOrderId":{"type":"string","format":"uuid","nullable":true,"description":"Raised in `maintenance`, so the repair is tracked where every other repair is."},"scopePath":{"type":"string"}}},
"RentalDepositPolicy": {"type":"object","x-ticvai-persistence":"rental.deposit_policy","description":"Boards 4.6 and 4.7. **Held, not taken**, and settled against an inspection.","properties":{"id":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid","nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"required":{"type":"boolean","default":true},"basis":{"type":"string","enum":["fixed","percentage","riskBased"]},"fixedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"percentage":{"type":"number","nullable":true},"minimumAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"instruments":{"type":"array","items":{"type":"string","enum":["cardPreAuthorisation","cardCharge","cash","wallet"]}},"autoRelease":{"type":"boolean","default":true},"inspectionRequiredBeforeRelease":{"type":"boolean","default":false},"autoReleaseDelayHours":{"type":"integer","default":0},"partialCapturePermitted":{"type":"boolean","default":true},"supervisorApprovalThreshold":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"waiverEligible":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"RentalEquipmentAssignment": {"type":"object","x-ticvai-persistence":"rental.equipment_assignment","description":"Board 6.4. **The moment a serialised rental stops being a quantity.**","required":["assetId"],"properties":{"id":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","description":"A `maintenance.Asset`, which is also a `resources` resource where the product is schedule-controlled."},"serialNumber":{"type":"string","nullable":true},"scannedCode":{"type":"string","nullable":true},"assignedManually":{"type":"boolean","default":false},"assignedAt":{"type":"string","format":"date-time"},"returnedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"RentalFeePolicy": {"type":"object","x-ticvai-persistence":"rental.fee_policy","description":"Board 4.8. **Extension is priced below late return on purpose** — *\"this encourages customers to extend properly rather than returning late.\"*\n","properties":{"id":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid","nullable":true},"gracePeriodMinutes":{"type":"integer","default":0},"lateFeeBasis":{"type":"string","enum":["fixed","perMinute","per15Minutes","per30Minutes","perHour","tiered"]},"lateFeeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lateFeeTiers":{"type":"array","items":{"type":"object","properties":{"afterMinutes":{"type":"integer"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"maximumDailyCharge":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"extensionPricePerIncrement":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"extensionIncrementMinutes":{"type":"integer","default":30},"notReturnedAfterHours":{"type":"integer","nullable":true,"description":"**When a late rental becomes a lost one.** The deposit is captured in full and the asset retired; without a threshold the fee accrues forever and nobody decides.\n"},"damageFeeMaximum":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"**A ceiling, not a rate.** Added 22 September: `rental.settlement.damage_fee` was stored with nothing bounding it. **A dent is assessed, not tabulated** — the amount is entered per incident against the actual damage, so the control is how high an operator may go, the same shape `maximumDailyCharge` already gives the late fee.\n"},"damageFeeApprovalAbove":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"**Above this, a second person signs it off.** A damage fee is the one charge on a settlement that a single operator decides alone, and the one a guest is most likely to dispute. The shape is `orders.RefundPolicy.requiresApprovalAbove`, applied to the other direction of money.\n"},"missingItemFeeBasis":{"type":"string","enum":["replacementCost","fixedAmount"],"description":"**What an unreturned item costs.** `replacementCost` reads the item's own replacement value, which is what the fee usually is; `fixedAmount` uses `missingItemFeeAmount`. Added 22 September — `rental.settlement.missing_item_fee` was stored with no source.\n"},"missingItemFeeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Used when `missingItemFeeBasis` is `fixedAmount`."},"scopePath":{"type":"string"}}},
"RentalInspection": {"type":"object","x-ticvai-persistence":"rental.inspection","description":"Boards 6.5 and 8.4. **Before and after are one record shape with a phase**, which is what makes the comparison view possible.\n","required":["phase","condition"],"properties":{"id":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"phase":{"type":"string","enum":["preRental","postRental"]},"condition":{"type":"string","enum":["good","minorDamage","majorDamage","faulty","notReturned"],"description":"**26 August: simplified state attributes.** *\"rental/equipment items can be tracked with simplified state attributes (e.g., available, rented, faulty) rather than requiring granular custom attributes for this category — agreed by Allam.\"* So the condition is a short enum, and anything finer belongs in the note or the photographs.\n"},"checklist":{"type":"array","items":{"type":"object","properties":{"item":{"type":"string"},"passed":{"type":"boolean"},"note":{"type":"string","nullable":true}}}},"note":{"type":"string","nullable":true},"photoAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"inspectedBy":{"type":"string","format":"uuid"},"inspectedAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string"}}},
"RentalInventoryModel": {"type":"object","x-ticvai-persistence":"rental.inventory_model","description":"Board 1.5. **Pooled, serialised or hybrid**, and the switches the counter obeys.","required":["trackingModel"],"properties":{"trackingModel":{"type":"string","enum":["pooled","serialised","hybrid"]},"inventoryUnit":{"type":"string","nullable":true},"totalQuantity":{"type":"integer","nullable":true,"description":"Pooled only. *150 lockers.*"},"components":{"type":"array","description":"**Hybrid only** — *one serialised kayak, two pooled paddles, two pooled life jackets.* One booking, two mechanisms.\n","items":{"type":"object","properties":{"resourceTypeId":{"type":"string","format":"uuid","nullable":true},"label":{"type":"string"},"quantity":{"type":"integer"},"serialised":{"type":"boolean"}}}},"assignmentRequiredAtCheckout":{"type":"boolean","default":false},"scanRequired":{"type":"boolean","default":false},"allowManualAssignment":{"type":"boolean","default":true},"allowSubstitution":{"type":"boolean","default":true},"allowEquipmentSwap":{"type":"boolean","default":true},"scopePath":{"type":"string"}}},
"RentalParticipant": {"type":"object","x-ticvai-persistence":"rental.participant","description":"Board 5.5. **A group rental is one booking with participants**, because the agreement, the deposit and the return are handled together.\n","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"isPrimaryRenter":{"type":"boolean","default":false},"dateOfBirth":{"type":"string","format":"date","nullable":true},"idNumber":{"type":"string","nullable":true},"guardianName":{"type":"string","nullable":true},"emergencyContact":{"type":"string","nullable":true},"hasSignedWaiver":{"type":"boolean","readOnly":true},"customFields":{"type":"object","additionalProperties":true}}},
"RentalProduct": {"type":"object","x-ticvai-persistence":"rental.product","description":"Board 1.3. **The master reference every later board resolves against.**","required":["code","name","venueId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"internalName":{"type":"string","nullable":true},"description":{"type":"string","nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"imageAssetId":{"type":"string","format":"uuid","nullable":true},"tags":{"type":"array","items":{"type":"string"}},"tenantId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"trackingModel":{"type":"string","enum":["pooled","serialised","hybrid"]},"catalogueProductId":{"type":"string","format":"uuid","nullable":true,"description":"**The thing the guest actually buys.** `catalogue` sells it and this configures how it behaves once sold; the link is here so a rental is never sold twice through two different product records.\n"},"resourceTypeId":{"type":"string","format":"uuid","nullable":true,"description":"**For serialised products, the `resources` type its assets belong to.** The individual bikes are resources and maintenance assets — this contract does not keep a third register of them.\n"},"status":{"type":"string","enum":["draft","configurationReview","approved","active","suspended","archived"]},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"version":{"type":"integer","default":1},"isActive":{"type":"boolean","default":true}}},
"RentalReturn": {"type":"object","description":"Board 8. **Late fee, damage and partial return all land on one deposit.**","required":["returnedAt"],"properties":{"returnedAt":{"type":"string","format":"date-time"},"returnLocationId":{"type":"string","format":"uuid","nullable":true},"returnedAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"missingAssetIds":{"type":"array","items":{"type":"string","format":"uuid"}},"inspection":{"$ref":"#/components/schemas/RentalInspection"},"damage":{"type":"array","items":{"$ref":"#/components/schemas/RentalDamageAssessment"}},"waiveLateFee":{"type":"boolean","default":false},"overrideId":{"type":"string","format":"uuid","nullable":true}}},
"RentalSettlement": {"type":"object","x-ticvai-persistence":"rental.settlement","description":"Board 8.8. **One statement, because there is one deposit.** *Capture AED 120, release AED 380.*\n","properties":{"bookingId":{"type":"string","format":"uuid"},"expectedReturnAt":{"type":"string","format":"date-time"},"actualReturnAt":{"type":"string","format":"date-time"},"gracePeriodMinutes":{"type":"integer"},"chargeableLateMinutes":{"type":"integer"},"lateFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"damageFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"missingItemFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCharged":{"x-ticvai-column":"gross_charged_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"depositCaptured":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"depositReleased":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceDue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"**Where the charges exceed the deposit.** A bike written off against a AED 200 hold leaves a real debt, and netting it to zero hides it.\n"},"outcome":{"type":"string","enum":["completed","completedWithDamage","partiallyReturned","notReturned"]},"scopePath":{"type":"string"}}},
"Resource": {"type":"object","x-ticvai-persistence":"resources.resource","description":"**A specific object, not a quantity of interchangeable ones.** A venue with forty identical strollers has forty resources, because guest number twelve returned stroller number twelve.\n","required":["id","code","name","kind","venueId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"$ref":"#/components/schemas/ResourceKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentResourceId":{"type":"string","format":"uuid","nullable":true,"description":"**A pool cabana belongs to the pool area; a seat belongs to an auditorium.** Booking a parent takes its children with it, which is the behaviour a venue expects and would otherwise have to enforce by hand.\n"},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"For a resource of kind `instructor` or `staff`. **`workforce` still owns their rota** — this says whether they are qualified and whether they are already committed.\n"},"attributes":{"type":"object","additionalProperties":true,"description":"Configurable per kind — capacity, size, shade, power, poolside."},"setupMinutes":{"type":"integer","default":0,"description":"**Before the booking, not inside it.** An auditorium booked 14:00–16:00 is unavailable from 13:30 with a 30-minute setup, and a calendar that cannot express that double-books every time.\n"},"teardownMinutes":{"type":"integer","default":0,"description":"After the booking. **Kept as it is** (decided 29 September, W10): with a `cleaningPolicy` of `afterEveryBooking` the cleaning buffer is added after the teardown, so a room with no teardown and a 15-minute clean is free 15 minutes after each booking ends.\n"},"cleaningPolicy":{"allOf":[{"$ref":"#/components/schemas/ResourceCleaningPolicy"}],"nullable":true,"description":"How the resource is cleaned between uses (decided 29 September, W10). Null means no cleaning is scheduled beyond `teardownMinutes`."},"requiresQualification":{"type":"array","items":{"type":"string"},"description":"Qualification codes a person must hold to be assigned to this."},"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["available","booked","checkedOut","maintenance","retired"]},"isActive":{"type":"boolean","default":true}}},
"ResourceBlock": {"type":"object","x-ticvai-persistence":"resources.resource_block","description":"Board 2.07. **A block is not a booking**, and the reason travels with it so an operator knows whether to wait or to look elsewhere.\n","required":["resourceId","from","to","reason"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid"},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"reason":{"type":"string","enum":["setup","teardown","maintenance","blackout","closed","operational","training"]},"note":{"type":"string","nullable":true},"createdBy":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"ResourceBooking": {"type":"object","x-ticvai-persistence":"resources.booking","required":["id","resourceId","from","to","status"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"status":{"$ref":"#/components/schemas/ResourceBookingStatus"},"holdId":{"type":"string","format":"uuid","nullable":true,"description":"The `ResourceHold` this booking was converted from, where a guest picked the resource on a venue map (rev 3 REV3-15). Null for a staff booking or an allocation.\n"},"recurrenceGroupId":{"type":"string","format":"uuid","nullable":true,"description":"Ties the occurrences of a recurring booking. **Cancelling one week does not cancel the series**, and cancelling the series is a separate act with a separate confirmation.\n"},"depositAuthorisationId":{"type":"string","format":"uuid","nullable":true,"description":"The hold, through `orders.authoriseStoredValue` (CF-126). **A deposit taken and refunded is two transactions and a fee; held and released is neither.**\n"},"checkedOutAt":{"type":"string","format":"date-time","nullable":true},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"returnedAt":{"type":"string","format":"date-time","nullable":true},"conditionOut":{"type":"string","nullable":true},"conditionIn":{"type":"string","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the latest offline check-out or check-in write reached the server. **The device times are `checkedOutAt` and `returnedAt`**, taken from each write's `recordedAt`; this is the server's half of the pair naming-and-style 5.2 requires. Null while pending.\n"}}},
"ResourceBookingStatus": {"type":"string","enum":["reserved","checkedOut","returned","overdue","cancelled","noShow"]},
"ResourceCleaningPolicy": {"x-ticvai-persistence":"none — columns on resources.resource","type":"object","description":"**When the resource is cleaned, and what that takes out of availability** (decided 29 September, W10; the meeting-room case from the 29 September website review).\n- `afterEveryBooking` (option A): `bufferMinutes` blocked after every booking, after its teardown. - `timesPerDay` (option B): `cleaningsPerDay` cleanings of `bufferMinutes` each, between `windowStart` and `windowEnd`, **placed by the system**. The targets are spread evenly across the window; each is put in the free gap nearest its target that is long enough, and never on a booking, a hold or a block. **A confirmed booking is never moved for a cleaning.** Placement is computed on read from the day's bookings, so it moves when bookings change, and a start time is offered only if every cleaning of that day can still be placed after it is booked.\n`createResource` and `updateResource` refuse a policy with `timesPerDay` and no `cleaningsPerDay`, or a window that ends before it starts, with `422`.\n","required":["mode","bufferMinutes"],"properties":{"mode":{"type":"string","enum":["afterEveryBooking","timesPerDay"]},"bufferMinutes":{"type":"integer","minimum":5,"maximum":240,"description":"Minutes one cleaning takes. The prototype uses 15 (proposed default, client to correct)."},"cleaningsPerDay":{"type":"integer","minimum":1,"maximum":24,"nullable":true,"description":"Required for `timesPerDay`; ignored for `afterEveryBooking`."},"windowStart":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window opens. Null means the resource's opening time."},"windowEnd":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","nullable":true,"description":"Venue-local time the cleaning window closes. Null means the resource's closing time."}}},
"ResourceCostEntry": {"type":"object","x-ticvai-persistence":"resources.resource_cost","description":"**One cost booked against a resource**: a transfer between locations, an operating cost or a replacement. `getResourceCostAnalytics` sums these per group and window (decided 29 September, data model DM4).\n","required":["id","resourceId","kind","amount","incurredOn"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"resourceId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["transfer","operating","replacement"]},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incurredOn":{"type":"string","format":"date"},"fromVenueId":{"type":"string","format":"uuid","nullable":true,"description":"A `transfer` only, with `toVenueId`."},"toVenueId":{"type":"string","format":"uuid","nullable":true},"note":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005), written at `venue` scope."}}},
"ResourceKind": {"type":"string","description":"BL-135. **`locker` was an entitlement kind in `orders` and nothing issued, assigned or released one.** A locker is a specific object checked out to a named guest and returned — which is this context exactly, and modelling it as an entitlement would have needed a second check-out mechanism.\nA seed for `ResourceType` rather than the law (board 1.02): a customer adding a class does it with `createResourceType`, not by waiting for this list to grow.\n**`table` is a non-dining spot** (decided 29 September, rev 3 GAP-C2, confirmed by Chinmay): a beach or event table placed on a venue map, picked and sold like a cabana (`createResourceHold`, then the order). **A dining table is not this**: restaurant tables stay `fnb` tables, booked with `fnb.createTableReservation` and the waitlist (audit R073 (d)).\n","enum":["cabana","lounger","locker","wheelchair","stroller","equipment","room","auditorium","vehicle","instructor","staff","table","pitch","studio","other"],"x-ticvai-refuses":{"mealPlan":"**Listed by 5.5.8b and deliberately not a kind.** 5.5.8b groups meal plans with lockers and parking, but a meal plan is a balance rather than an object. It resolves to `retail.Wallet` with a `mealPlan` credit kind (CF-126), not to a resource — so it is not offered here, and a form built from this enum cannot offer it either."}},
"ResourceLifecycleState": {"type":"string","description":"Board 1.10. **States of one machine**, whose allowed transitions are configuration.","enum":["draft","pendingApproval","approved","active","temporarilyUnavailable","underMaintenance","suspended","retired","archived"]},
"StoredValueKind": {"type":"string","description":"**Six things in this package hold a balance and behave the same way** — a wallet, a gift card, a game card, a voucher, a loyalty position and a prepaid entitlement. They were built separately across three sessions and each grew its own balance, bonus balance, status, blocked reason and expiry (CF-126).\n**The concern is not tidiness. Only one of the six could hold an authorisation.** `authoriseWalletSpend` / `captureWalletAuthorisation` / `relinquishWalletAuthorisation` gave two-phase spend to the retail wallet alone, so **a guest with 200 game credits starting a play the machine then failed had no held balance** — the credits were either taken or not, with no third state.\nThe entities stay distinct because their lifecycles genuinely differ — a gift card activates at a till, a loyalty position never expires the same way. **What is shared is the spend mechanism**, and this enum is what lets it be shared.\n","enum":["wallet","giftCard","gameCard","voucher","loyalty","prepaidEntitlement"]},
"SubmitInspectionRequest": {"x-ticvai-persistence":"maintenance.inspection + maintenance.inspection_item","type":"object","required":["id","templateId","venueId","responses","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"templateId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"responses":{"type":"array","minItems":1,"items":{"type":"object","required":["key","value"],"properties":{"key":{"type":"string"},"value":{},"passed":{"type":"boolean","nullable":true},"note":{"type":"string","maxLength":1000},"attachmentRefs":{"type":"array","items":{"type":"string"}}}}},"signatureRef":{"type":"string","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"WorkOrder": {"x-ticvai-persistence":"maintenance.work_order","x-ticvai-retired-columns":["is_overdue"],"type":"object","required":["id","workOrderNumber","title","venueId","status","priority","kind","createdAt"],"properties":{"downtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"},"rootCause":{"type":"string","nullable":true,"enum":["wearAndTear","operatorError","guestDamage","manufacturingDefect","environmental","softwareFault","powerFailure","deferredMaintenance","unknown"],"description":"**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"},"rootCauseNote":{"type":"string","nullable":true},"escalatedAt":{"type":"string","format":"date-time","nullable":true},"escalationLevel":{"type":"integer","default":0,"description":"**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"},"id":{"type":"string","format":"uuid"},"workOrderNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"title":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"assetName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"},"status":{"$ref":"#/components/schemas/WorkOrderStatus"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"priorityScore":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"readOnly":true,"description":"The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."},"prioritySource":{"type":"string","enum":["scored","assetOverride","manual"],"readOnly":true,"description":"Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","items":{"type":"string"},"description":"Skills the job needs (M17-13)."},"kind":{"$ref":"#/components/schemas/WorkOrderKind"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"raisedByPrincipalId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"},"locationDescription":{"type":"string","maxLength":500,"nullable":true,"description":"Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"},"elapsedMinutes":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"},"isTimerRunning":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"},"dueAt":{"type":"string","format":"date-time","nullable":true},"isOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"},"requiresVerification":{"type":"boolean"},"sourcePlanId":{"type":"string","format":"uuid","nullable":true},"sourceInspectionId":{"type":"string","format":"uuid","nullable":true},"sourceIncidentId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrderFaultAssessment": {"x-ticvai-persistence":"none — columns on maintenance.work_order","type":"object","description":"What the person raising a fault says about it, which the priority score reads (M17-01).","properties":{"safetyRisk":{"type":"boolean","default":false},"guestImpact":{"type":"string","enum":["none","degraded","closed"],"default":"none"}}},
"WorkOrderKind": {"type":"string","enum":["corrective","planned","inspectionFollowUp","incidentCorrective","improvement"]},
"WorkOrderPriority": {"type":"string","enum":["low","normal","high","urgent","emergency"]},
"WorkOrderStatus": {"type":"string","enum":["open","assigned","inProgress","paused","awaitingParts","completed","verified","closed","cancelled"]}
}
```
