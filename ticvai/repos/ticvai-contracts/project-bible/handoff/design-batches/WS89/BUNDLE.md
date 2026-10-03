# WS89 — Rental Management board 2

**10 screens · 13 operations · 24 schemas · 5 permissions**

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
  `ASSET_MANAGE, ASSET_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, RENTAL_VIEW`. A control nobody can use must say so,
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
| `BO-504` | Rental Inventory Command Center | D | 2 | 40 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-505` | Serialized Equipment Registry | D | 10 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-506` | Equipment / Asset Profile | D | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `BO-507` | Pooled Inventory Management | D | 0 | 0 | 6 | 31 | 1 | 4 | — | notStarted (—) |
| `BO-508` | Equipment Status & Condition Management | D | 0 | 0 | 6 | 2 | 2 | 0 | — | notStarted (—) |
| `BO-509` | QR / Barcode Equipment Identification | D | 1 | 0 | 6 | 3 | 1 | 0 | — | notStarted (—) |
| `BO-510` | Inventory Location Allocation | D | 0 | 0 | 6 | 3 | 1 | 4 | — | notStarted (—) |
| `BO-511` | Inventory Transfer Management | D | 0 | 8 | 6 | 8 | 1 | 4 | — | notStarted (—) |
| `BO-512` | Inventory Adjustment & Exception Management | D | 0 | 0 | 6 | 12 | 1 | 4 | — | notStarted (—) |
| `BO-513` | Inventory Intelligence & Rebalancing | D | 0 | 16 | 6 | 19 | 1 | 4 | — | notStarted (—) |

## Thin screens in this batch

**BO-506, BO-508, BO-509, BO-510, BO-512, BO-513 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-504` Rental Inventory Command Center

**Provide a real-time operational overview of all rental inventory across venues and locations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-504 |
| Who uses it | venue staff holding `ASSET_VIEW`, `RENTAL_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/rental-inventory-command-center-bo-504` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): General inventory positions have no rented, reserved or maintenance state; rental unit status lives with rental bookings and assets (DI-744; design-notes … Removed 2 October 2026 (CHG-WIR-008): General inventory positions have no rented, reserved or maintenance state; rental unit status lives with rental bookings and assets (DI-744; design-notes …

**From the Food, Beverage & Retail process.** Rental inventory across stations: how many units are available, reserved, rented, in maintenance, damaged, lost or out of service, per product and location. The one thing to get right: the simplified states agreed with the client, and a click from a number to the units behind it.

**Fixed on main** (the package already carries these; draw what it says): Reads general inventory (listInventoryItems, getStockPositions) whose positions have no rented, reserved or maintenance state. (CHG-WIR-008).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search rental inventory | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, location, product, category, tracking model and 3 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRentalBookings` ?status |
| Location | picker: choose a location | — | — | `listRentalBookings` ?locationId |
| From | date and time picker | — | — | `listRentalBookings` ?from |
| To | date and time picker | — | — | `listRentalBookings` ?to |
| Category | picker: choose a category | — | — | `listAssets` ?categoryId |
| Status | select | — | In service · Out of service · Under maintenance · Awaiting parts · Retired · Disposed | `listAssets` ?status |
| Maintenance due | toggle | — | — | `listAssets` ?maintenanceDue |

#### Outputs: what the screen shows and produces

**Shown**

**Rentals** (data table, from `listRentalBookings`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Reference | text | — |
| Product | the name it points at, never the id | — |
| Location | the name it points at, never the id | — |
| Return location | the name it points at, never the id | — |
| Customer | the name it points at, never the id | — |
| Order | the name it points at, never the id | — |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | — |
| Quantity | 1,234 | — |
| Status | chip: Draft, Confirmed, Awaiting arrival, Checked out, Overdue, Partially returned… | — |
| Checked out at | 1 Oct 2026, 14:30 | — |
| Due back at | 1 Oct 2026, 14:30 | — |
| Returned at | 1 Oct 2026, 14:30 | — |
| Deposit authorisation | the name it points at, never the id | The card deposit's terminal pre-authorisation, written by `checkOutRental` (workbook Q304; CHG-CSA-029). |
| Accrued late fee | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Readiness | list or chips (count when long) | Computed, not stored — agreement, requirements, deposit, equipment. |
| Check | text | — |
| Satisfied | yes / no (icon or chip) | — |
| Detail | text | — |

**Units** (data table, from `listAssets`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Asset tag | text | Unique per venue (decided 28 September, audit R108). Two assets in one venue never share a tag; `createAsset` refuses a duplicate with … |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Category | the name it points at, never the id | — |
| Location description | text | — |
| Criticality | chip: Safety critical, Revenue critical, Standard, Low | — |
| Priority override | chip: Low, Normal, High, Urgent, Emergency | "If this device goes down, raise this priority" (decided 17 September, M17-01). A corrective work order raised on this asset takes this … |
| Manufacturer | text | — |
| Model | text | — |
| Serial number | text | — |
| Commissioned at | 1 Oct 2026 | — |
| Warranty expires at | 1 Oct 2026 | — |
| Supplier | the name it points at, never the id | — |
| Linked products | list or chips (count when long) | Products this asset delivers. A fault here can stop them selling. |
| Linked access point | the name it points at, never the id | Access point this asset controls. Out of service blocks it. |
| Requires inspection to return | yes / no (icon or chip) | True means a completed inspection is required before return to service. A technician cannot simply declare a ride safe. |
| Documents | list or chips (count when long) | Manuals, procedures, certificates, each with its name and kind. Stored one row per document in `maintenance.asset_document`, which is where … |
| Ref | text | The document in the media store. |
| Name | text | — |

**Total Inventory** (metric tile)

**Available Now** (metric tile)

**Reserved** (metric tile)

**Rented** (metric tile)

**Under Maintenance** (metric tile)

**Damaged** (metric tile)

**Lost** (metric tile)

**Out of Service** (metric tile)

**Inventory Utilization %** (metric tile)

**Inventory Alerts** (metric tile)

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Status totals**: Available · Reserved · Rented · Faulty / in maintenance (excluded from available until resolved) · Lost; per product and per station. *(source: DI-744 / DI-500)*

**Data it reads**: `listRentalBookings` (onLoad, Units out); `listAssets` (onLoad, Rental units and their condition)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-505` Serialized Equipment Registry: *Serialized Equipment Registry*
- → `BO-506` Equipment / Asset Profile: *Equipment / Asset Profile*; carries `assetId`
- → `BO-507` Pooled Inventory Management: *Pooled Inventory Management*
- → `BO-508` Equipment Status & Condition Management: *Equipment Status & Condition Management*; carries `assetId`
- → `BO-509` QR / Barcode Equipment Identification: *QR / Barcode Equipment Identification*
- → `BO-510` Inventory Location Allocation: *Inventory Location Allocation*
- → `BO-511` Inventory Transfer Management: *Inventory Transfer Management*
- → `BO-512` Inventory Adjustment & Exception Management: *Inventory Adjustment & Exception Management*
- → `BO-513` Inventory Intelligence & Rebalancing: *Inventory Intelligence & Rebalancing*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental inventory list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental inventory untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental inventory yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental inventory are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
totals: 'City Bicycle: 40 total · 22 available · 6 reserved · 9 rented · 3 in maintenance'
```

#### Permissions

- `listRentalBookings` → `RENTAL_VIEW` (read) · staff
- `listAssets` → `ASSET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Inventory overview shows totals by status - available, reserved, rented, in maintenance, out of service - per product. Serialized items show condition (good, in repair, in maintenance) and lifecycle history (purchase date, servicing, rental activity); pooled items show aggregate quantity only. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-744)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-504` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS117 Rental Management Board 2.dc.html#bo-504`
- Workshop pack: Rental_Management.pdf board 2
- Flow F198 *Rental Management board 2: Rental Inventory Command Center*, step 1: Opens Rental Inventory Command Center → Provide a real-time operational overview of all rental inventory across venues and locations.
- Flow F198 *Rental Management board 2: Rental Inventory Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F198 *Rental Management board 2: Rental Inventory Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F198 *Rental Management board 2: Rental Inventory Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F198 *Rental Management board 2: Rental Inventory Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F198 *Rental Management board 2: Rental Inventory Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F198 *Rental Management board 2: Rental Inventory Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F198 *Rental Management board 2: Rental Inventory Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F198 branch at step 1 (expected): when Nothing has been set up on Rental Inventory Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F198 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-504?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-505`, `BO-506`, `BO-507`, `BO-508`, `BO-509`, `BO-510`, `BO-511`, `BO-512`, `BO-513`.
- [ ] Every gated control is gated: `ASSET_VIEW`, `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-505` Serialized Equipment Registry

**Manage individually identifiable rental assets.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-505 |
| Who uses it | venue staff holding `ASSET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Fields) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/serialized-equipment-registry-bo-505` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): listSerialisedItems is retail serials (in stock, sold, returned); rental units are assets with rental states (listAssets, declared) (design-notes correction …

**From the Food, Beverage & Retail process.** The register of individually numbered rental units: serial, asset code, product, station, purchase and warranty, condition and status, with each unit's history. The one thing to get right: search by serial or scan, and condition and history on one page.

**Fixed on main** (the package already carries these; draw what it says): listSerialisedItems (retail serials, statuses in stock / sold / returned) is the main read, and the layout is a form of select fields. (CHG-WIR-008).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Serial Number | select field | — | — | — | — | — | — |
| Asset Code | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Manufacturer Serial Number | select field | — | — | — | — | — | — |
| Location | select field | — | — | — | — | — | — |
| Acquisition Date | select field | — | — | — | — | — | — |
| Purchase Cost | select field | — | — | — | — | — | — |
| Warranty Expiry | select field | — | — | — | — | — | — |
| Condition | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `listAssets` ?categoryId |
| Status | select | — | In service · Out of service · Under maintenance · Awaiting parts · Retired · Disposed | `listAssets` ?status |
| Maintenance due | toggle | — | — | `listAssets` ?maintenanceDue |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Unit record**: Serial, asset code, product, station, purchase date and cost, warranty expiry, condition (Good · In repair · In maintenance), status, rentals and servicing history. *(source: DI-744 / DI-745)*

**Data it reads**: `listAssets` (onLoad, The asset register behind them)

**Where the user goes next**

- → `BO-504` Rental Inventory Command Center: *Back to Rental Inventory Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The serialized equipment registry configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the serialized equipment registry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No serialized equipment registry configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
unit: BIKE-121 · City Bicycle · Beach Hut · bought 12 Mar 2026 · warranty to Mar 2028 · Good · 214 rentals
```

#### Permissions

- `listAssets` → `ASSET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Inventory overview shows totals by status - available, reserved, rented, in maintenance, out of service - per product. Serialized items show condition (good, in repair, in maintenance) and lifecycle history (purchase date, servicing, rental activity); pooled items show aggregate quantity only. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-744)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-505` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS117 Rental Management Board 2.dc.html#bo-505`
- Workshop pack: Rental_Management.pdf board 2
- Flow F198 *Rental Management board 2: Rental Inventory Command Center*, step 2: Works in Serialized Equipment Registry → Manage individually identifiable rental assets.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-505?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-504`.
- [ ] Every gated control is gated: `ASSET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-506` Equipment / Asset Profile

**Provide a complete digital record for every serialized rental asset.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-506 |
| Who uses it | venue staff holding `ASSET_MANAGE`, `ASSET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/rentals/equipment-asset-profile-bo-506` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The rental lens of an asset's record: one serialised rental item (a mountain bike, a kayak, a wheelchair) with its identity, where it is, its state and condition, its rental use and its maintenance, on one page with tabs. It is the same physical asset as the venue asset register; rental adds use counters and rental history. The one thing to get right: status (can it be rented now) and condition (what shape it is in) sit side by side in the header, with the next maintenance stated in the unit that matters for rentals ("in 6 rentals or 18 rental hours").

**Known correction pending (do not draw the wrong version)**

- **Gap note "the pack gives this screen nothing that can be drawn"** Why: Pack pages 19-20 list the creation fields, the profile's fifteen facts, seven tabs and the lifecycle timeline. *(source: screens/P08-venue-back-office.yaml#BO-506 / screens/P08-venue-back-office.yaml#BO-507; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Save asset" button bound to no operation, and an unlabelled detail panel** Why: getAsset reads it and updateAsset saves it; both are declared for this screen but not bound to components. *(source: screens/P08-venue-back-office.yaml#BO-506 / contracts/satellite/maintenance.yaml#updateAsset; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Condition is shown by the pack but the asset has no condition field** Why: rental.yaml says "maintenance.Asset already carries serial, acquisition, warranty, condition and history", but Asset has no condition; only rental inspection items record one. *(source: contracts/satellite/rental.yaml#recordRentalInspection / contracts/satellite/maintenance.yaml#/components/schemas/Asset; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Total rentals, rental hours and last rental have no source on the asset** Why: Asset carries a single usageCounter; rental counts come from rental agreements, and no read joins them to the asset. *(source: screens/P08-venue-back-office.yaml#BO-506 / contracts/satellite/maintenance.yaml#/components/schemas/Asset; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **A wrong serial number or acquisition cost cannot be corrected** Why: updateAsset accepts name, location, category, warranty, supplier, override and documents only. *(source: contracts/satellite/maintenance.yaml#updateAsset; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which record owns condition - the asset (maintenance) or the latest rental inspection?** → Drawn default accepted: Show condition from the latest inspection with its date ("Good - inspected 30 Sep 17:10"). *(decided by Chinmay, 2026-10-02; DEC-432 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Editable details**: Name, location, category, warranty expiry, supplier and fault-priority override are editable here; serial number, asset code, manufacturer and acquisition date and cost are shown read-only (they are set at creation). Documents upload with a name and a kind. *(source: screens/P08-venue-back-office.yaml#BO-506 / contracts/satellite/maintenance.yaml#updateAsset)*
- **Asset code and serial number**: Asset code (tag) unique per venue; a duplicate serial is refused with the existing asset named - shown on creation and on import. *(source: screens/P08-venue-back-office.yaml#BO-506 / contracts/satellite/maintenance.yaml#createAsset)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save asset (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Header**: BIKE-017, Mountain Bike - Adult, status chip and condition chip side by side, location (North Station, Summit Peaks), QR icon that shows the label. *(source: screens/P08-venue-back-office.yaml#BO-506 / screens/P08-venue-back-office.yaml#BO-507)*
- **Overview facts**: Product, category, purchase date, warranty (amber within 60 days), total rentals, total rental hours, last rental, last inspection, last maintenance, next maintenance - each a labelled value, not a table. *(source: screens/P08-venue-back-office.yaml#BO-506 / contracts/satellite/maintenance.yaml#getAsset)*
- **Tabs**: Overview, Rental history, Inspections, Damage, Maintenance, Transfers, Audit - in the pack's order. *(source: screens/P08-venue-back-office.yaml#BO-507)*
- **Lifecycle strip**: A horizontal timeline Purchased > Activated > Rented x184 > Repaired > Returned to service, with dates on hover. *(source: screens/P08-venue-back-office.yaml#BO-507 / contracts/satellite/maintenance.yaml#getAssetHistory)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save asset**: Sends only the changed fields; documents replace the list as a whole, so the confirm lists documents added and removed. *(source: contracts/satellite/maintenance.yaml#updateAsset)*
- **Change status**: Opens BO-508 for this asset. *(source: screens/P08-venue-back-office.yaml#BO-508)*
- **Raise a repair**: Opens the maintenance work order (BO-577) pre-filled with this asset. *(source: screens/P08-venue-back-office.yaml#BO-577)*

**Where the user goes next**

- → `BO-504` Rental Inventory Command Center: *Back to Rental Inventory Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The equipment asset profile list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the equipment asset profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No equipment asset profile yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the equipment asset profile are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Asset currently rented**: Header shows "Rented - due back 16:30" with the booking reference; status changes warn that a guest has it. *(source: contracts/satellite/rental.yaml#assignRentalEquipment / designer default)*
- **Asset retired**: Read-only with a grey Retired banner and the retirement date; history stays visible. *(source: contracts/satellite/maintenance.yaml#/components/schemas/Asset)*

#### Consistency with other screens

- Match `BO-069`: Same Asset 360 component as the venue asset register; rental adds the rental counters and the Rental history tab. One component, not two designs (per VO-R14).
- Match `BO-580`: The Maintenance tab is the maintenance history and lifecycle screen in short form.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
asset:
  code: BIKE-017
  name: Mountain Bike - Adult
  serial: TRK-MB-22-004417
  status: Available
  condition: Good
  location: North Station, Summit Peaks
  purchased: 12 Jan 2026
  warranty: 12 Jan 2028
  rentals: 184
  rentalHours: 276
  lastRental: 30 Sep 2026
  lastInspection: 30 Sep 2026 17:10
  lastMaintenance: 8 Sep 2026 (brake repair)
  nextMaintenance: In 6 rentals or 18 rental hours
```

#### Permissions

- `getAsset` → `ASSET_VIEW` (read) · staff
- `updateAsset` → `ASSET_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.1.6 | Asset Documentation - System shall maintain manuals and technical documents. | Maintenance & Safety Management | CONTRACTED | `getAsset` |
| 17.5.10 | Safety Documentation - System shall support safety document management. | Maintenance & Safety Management | CONTRACTED | `getAsset` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Inventory overview shows totals by status - available, reserved, rented, in maintenance, out of service - per product. Serialized items show condition (good, in repair, in maintenance) and lifecycle history (purchase date, servicing, rental activity); pooled items show aggregate quantity only. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-744)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-506` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS117 Rental Management Board 2.dc.html#bo-506`
- Workshop pack: Rental_Management.pdf board 2
- Flow F198 *Rental Management board 2: Rental Inventory Command Center*, step 4: Works in Equipment / Asset Profile → Provide a complete digital record for every serialized rental asset.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-506?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save asset, Cancel.
- [ ] Every transition is wired: `BO-504`.
- [ ] Every gated control is gated: `ASSET_MANAGE`, `ASSET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 5 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-507` Pooled Inventory Management

**Manage products where individual physical items do not require serial-level tracking.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-507 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/pooled-inventory-management-bo-507` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Quantity-only rental stock (life jackets, paddles, towels) per station: increase, decrease, adjust with a reason, transfer, or mark units out of service. The one thing to get right: every change carries a reason.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Location | picker: choose a location | — | — | `getStockPositions` ?locationId |
| Item | picker: choose an item | — | — | `getStockPositions` ?itemId |
| Include zero | toggle | off | — | `getStockPositions` ?includeZero |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Adjustment**: Quantity and reason (Damaged · Lost · Stolen · Found · Other with a note). *(source: DI-746 / R222)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Increase Quantity (primary button) | navigation or local | — | — | — | — |
| Decrease Quantity (secondary button) | navigation or local | — | — | — | — |
| Adjust Inventory (secondary button) | navigation or local | — | — | — | — |
| Transfer Quantity (secondary button) | navigation or local | — | — | — | — |
| Mark Out of Service (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getStockPositions` (onLoad, Pooled quantities)

**Where the user goes next**

- → `BO-504` Rental Inventory Command Center: *Back to Rental Inventory Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pooled inventory list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pooled inventory untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pooled inventory yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pooled inventory are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed, including an `adjustmentIn`, `adjustmentOut` or `waste` movement with no `reason` (audit R171).; 409 Insufficient stock at the source; 409 Insufficient stock, and the item does not permit negative balances |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
position: Life Jacket (adult) · Beach Hut 50 · Kayak Jetty 100 · 4 out of service
```

#### Permissions

- `getStockPositions` → `PRODUCT_VIEW` (read) · staff
- `createStockMovement` → `PRODUCT_CONFIGURE` (configure) · staff
- `createStockTransfer` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

31 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.4.9 | The system should allow multi-store retailing where the stores are connected with the inventory information of other stores. This should allow the guests to order items which are out of stock in the … | Bundles and Promotions | CONTRACTED | `getStockPositions` |
| 4.4.14 | Support multiple warehouses, stores, kiosks, stock rooms, and inventory locations with centralized visibility. | Bundles and Promotions | CONTRACTED | `getStockPositions` |
| 4.4.25 | Maintain one inventory source across POS, B2C, B2B, Mobile App, Kiosks, APIs, and future channels with real-time synchronization. | Bundles and Promotions | CONTRACTED | `getStockPositions` |
| 15.1.9 | Real-Time Inventory Tracking - System shall track inventory levels in real time. | Inventory Management | CONTRACTED | `getStockPositions` |
| 15.1.10 | Multi-Location Inventory - System shall support inventory across multiple locations. | Inventory Management | CONTRACTED | `getStockPositions` |
| 15.1.11 | Multi-Warehouse Inventory - System shall support multiple warehouses. | Inventory Management | CONTRACTED | `getStockPositions` |
| 15.1.12 | Available Stock Tracking - System shall track available stock. | Inventory Management | CONTRACTED | `getStockPositions` |
| 15.1.13 | Reserved Stock Tracking - System shall track reserved inventory. | Inventory Management | CONTRACTED | `getStockPositions` |
| 18.7.1 | Inventory Lookup - Users shall view inventory availability. | Employee Mobile App & AI Assistant | CONTRACTED | `getStockPositions` |
| 18.7.2 | Stock Count - Users shall perform stock counts. | Employee Mobile App & AI Assistant | CONTRACTED | `getStockPositions` |
| 18.7.3 | Inventory Transfers - Users shall execute inventory transfers. | Employee Mobile App & AI Assistant | CONTRACTED | `getStockPositions` |
| 18.7.4 | Goods Receipt - Users shall record goods receipt transactions. | Employee Mobile App & AI Assistant | CONTRACTED | `getStockPositions` |
| … 19 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Inventory overview shows totals by status - available, reserved, rented, in maintenance, out of service - per product. Serialized items show condition (good, in repair, in maintenance) and lifecycle history (purchase date, servicing, rental activity); pooled items show aggregate quantity only. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-744)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-507` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS117 Rental Management Board 2.dc.html#bo-507`
- Workshop pack: Rental_Management.pdf board 2
- Flow F198 *Rental Management board 2: Rental Inventory Command Center*, step 6: Works in Pooled Inventory Management → Manage products where individual physical items do not require serial-level tracking.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-507?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Increase Quantity, Decrease Quantity, Adjust Inventory, Transfer Quantity, Mark Out of Service.
- [ ] Every transition is wired: `BO-504`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-508` Equipment Status & Condition Management

**Separate operational status from physical condition. This distinction is important.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-508 |
| Who uses it | venue staff holding `ASSET_MANAGE`, `ASSET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/rentals/equipment-status-condition-management-bo-508` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Where staff change a rental item's state - send it for repair, mark it out of service, return it - with a reason and an expected return date, keeping operational status (can it be rented) separate from physical condition (what shape it is in). The system enforces which moves are allowed, so a damaged or unsafe item cannot slip back into rentable stock. The one thing to get right: Available is never chosen by hand from a damaged or unsafe state - it is reached only through an inspection.

**Known correction pending (do not draw the wrong version)**

- **The rental statuses (Available, Reserved, Rented, Inspection required, Cleaning, Lost) do not exist in AssetStatus** Why: AssetStatus is inService, outOfService, underMaintenance, awaitingParts, retired, disposed; rental availability is derived from bookings. The screen must show the derived rental state and set only the maintenance status. *(source: screens/P08-venue-back-office.yaml#BO-509 / contracts/satellite/maintenance.yaml#/components/schemas/AssetStatus; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **DI-500 agreed simplified states (available, rented, faulty) but the pack lists nine statuses and six conditions** Why: The two client inputs disagree; the lead should confirm which set the screen offers. *(source: screens/P08-venue-back-office.yaml#BO-509 / DI-500; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No expected return-to-service date and no condition on the status change** Why: DI-745 asks for an estimated return date with the reason; SetAssetStatusRequest has neither, so availability cannot be restored on time. *(source: DI-745 / contracts/satellite/maintenance.yaml#/components/schemas/SetAssetStatusRequest; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Allowed transitions are not enforced by the contract** Why: The pack requires TICVAI to control valid transitions; setAssetStatus accepts any status except return without inspection. *(source: screens/P08-venue-back-office.yaml#BO-509 / contracts/satellite/maintenance.yaml#setAssetStatus; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Gap note "nothing that can be drawn"; Save asset status bound to no operation** Why: The pack lists both vocabularies and the transition rules; setAssetStatus is the save. *(source: screens/P08-venue-back-office.yaml#BO-509 / screens/P08-venue-back-office.yaml#BO-508; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is Cleaning a status (item unavailable while cleaned) or part of the return inspection?** → Drawn default accepted: Draw Cleaning as part of the return inspection, not a status. *(decided by Chinmay, 2026-10-02; DEC-433 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **New status**: Only the moves allowed from the current state are offered (for example from Rented: Returned > Inspection required; from Inspection required: Available after a passed inspection, or Under maintenance). Rented and Reserved are never offered - they come from bookings. *(source: screens/P08-venue-back-office.yaml#BO-509 / contracts/satellite/maintenance.yaml#setAssetStatus)*
- **Condition**: Excellent, Good, Fair, Damaged, Major damage, Unsafe as colour chips; Damaged, Major damage and Unsafe force the status to Under maintenance or Out of service. *(source: screens/P08-venue-back-office.yaml#BO-509)*
- **Reason**: Required, at least 3 characters (max 1000); short presets (Damage on return, Failed inspection, Preventive service due, Lost) plus free text. *(source: contracts/satellite/maintenance.yaml#/components/schemas/SetAssetStatusRequest / DI-745)*
- **Expected back in service**: Date and time picker, required when taking an item out; feeds rental availability for future bookings. *(source: screens/P08-venue-back-office.yaml#BO-583 / DI-745)*
- **Raise a work order**: A tick, on by default when moving to Under maintenance; opens the work order with this asset. *(source: contracts/satellite/maintenance.yaml#/components/schemas/SetAssetStatusRequest)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save asset status (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Current state**: Status chip and condition chip side by side, with when and by whom each was last changed. *(source: screens/P08-venue-back-office.yaml#BO-509 / contracts/satellite/maintenance.yaml#/components/schemas/AssetStatusChange)*
- **Downstream effect**: After saving, "BIKE-031 removed from rentable stock until 3 Oct 10:00 - 2 future bookings affected" with a link to the bookings. *(source: screens/P08-venue-back-office.yaml#BO-583 / contracts/satellite/maintenance.yaml#/components/schemas/AssetStatusResult)*
- **Status history**: The sequence of changes (from, to, reason, who, when), newest first. *(source: contracts/satellite/maintenance.yaml#/components/schemas/AssetStatusChange)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save status**: Sets the status with the reason; a return to service without the required inspection is refused 409 with "Complete the return-to-service inspection" and a link to BO-581. *(source: contracts/satellite/maintenance.yaml#setAssetStatus / screens/P08-venue-back-office.yaml#BO-581)*
- **Scan**: Scanning the item's QR opens it here directly. *(source: DI-745 / contracts/satellite/maintenance.yaml#lookupAsset)*

**Where the user goes next**

- → `BO-504` Rental Inventory Command Center: *Back to Rental Inventory Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The equipment status condition list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the equipment status condition untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No equipment status condition yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the equipment status condition are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Return to service attempted without the inspection this asset category requires. |

#### Edge cases to draw

- **Taking out an item that is booked for later today**: Confirm lists the bookings affected and offers to swap them to another item before saving (per VO-R16). *(source: screens/P08-venue-back-office.yaml#BO-583)*
- **Item marked lost**: Lost needs a reason and the last known booking; it leaves available stock and is flagged for the damage/loss process. *(source: screens/P08-venue-back-office.yaml#BO-509)*

#### Consistency with other screens

- Match `BO-069`: The same status change control and consequence wording as Take out of service on the asset register.
- Match `BO-581`: The only path back to Available from a damaged or unsafe state.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
item:
  code: BIKE-028
  status: Inspection required
  condition: Fair
  change:
    to: Under maintenance
    reason: Rear derailleur bent on return
    backBy: 3 Oct 2026 10:00
    workOrder: raised
```

#### Permissions

- `setAssetStatus` → `ASSET_MANAGE` (configure) · staff
- `getAsset` → `ASSET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.1.6 | Asset Documentation - System shall maintain manuals and technical documents. | Maintenance & Safety Management | CONTRACTED | `getAsset` |
| 17.5.10 | Safety Documentation - System shall support safety document management. | Maintenance & Safety Management | CONTRACTED | `getAsset` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staff change an item's status (maintenance/repair) with a reason and an estimated return-to-service date; scanning an item's QR code pulls up its full details instantly. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-745)*
- Rental/equipment items use simplified states — available, rented, faulty/out-of-maintenance (excluded from available inventory until resolved) — not granular custom attributes. Clients supply item data at onboarding; a screen lets them update inventory and item details afterwards. *(agreed · MoM 26 Aug 2026, 4.8 Equipment, Assets & Rental Management; 5. Key Decisions · DI-500)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-508` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS117 Rental Management Board 2.dc.html#bo-508`
- Workshop pack: Rental_Management.pdf board 2
- Flow F198 *Rental Management board 2: Rental Inventory Command Center*, step 8: Works in Equipment Status & Condition Management → Separate operational status from physical condition. This distinction is important.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-508?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save asset status, Cancel.
- [ ] Every transition is wired: `BO-504`.
- [ ] Every gated control is gated: `ASSET_MANAGE`, `ASSET_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 5 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-509` QR / Barcode Equipment Identification

**Give every physical serialized rental item a scannable digital identity. This incorporates the equipment-assignment scanning recommendation from the source.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-509 |
| Who uses it | venue staff holding `ASSET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/qr-barcode-equipment-identification-bo-509` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No operation generates or prints asset labels.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Every serialised rental item gets a scannable identity: generate and print its label, and scan it to see what it is, where it should be, its state and condition, and when it next needs maintenance, with the next actions. The one thing to get right: scanning is the fast path everywhere (works offline at a rental station), and the label carries only the code - details appear after a signed-in scan.

**Known correction pending (do not draw the wrong version)**

- **Search field bound to no operation; gap note says nothing is drawable** Why: lookupAsset (by tag or serial) is the search; the pack gives the label, the result card and its actions. *(source: screens/P08-venue-back-office.yaml#BO-510 / screens/P08-venue-back-office.yaml#BO-509; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No operation generates or prints asset labels** Why: The pack requires single and bulk label printing; nothing in the maintenance contract produces a label. *(source: screens/P08-venue-back-office.yaml#BO-509 / screens/P08-venue-back-office.yaml#BO-510; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **NFC and RFID lookups have no parameter** Why: lookupAsset takes assetTag or serialNumber only; an RFID or NFC tag id needs a field on the asset or the lookup. *(source: contracts/satellite/maintenance.yaml#lookupAsset / MATRIX 18.3.2; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should the QR encode a URL (opens the asset after sign-in) or only the code?** → Drawn default accepted: Encode the code only; the label prints the code in text as well. *(decided by Chinmay, 2026-10-02; DEC-434 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Scan or type**: Camera scan of QR or barcode, NFC or RFID tap where the device supports it, or typing the asset code or serial number. Never a database id. *(source: screens/P08-venue-back-office.yaml#BO-509 / contracts/satellite/maintenance.yaml#lookupAsset)*
- **Label printing**: Single label or bulk (pick a product and location); label shows the venue's TICVAI rental asset label, the code in text and the QR; template chosen once per venue. *(source: screens/P08-venue-back-office.yaml#BO-509 / screens/P08-venue-back-office.yaml#BO-510)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Scan result card**: "BIKE-001 - Mountain Bike", Location North Station, Status Available, Condition Good, Next maintenance "82 rental hours", with the asset's photo; wrong-location scans say "Expected at Marina Station". *(source: screens/P08-venue-back-office.yaml#BO-510 / contracts/satellite/maintenance.yaml#lookupAsset)*
- **Actions on the card**: Inspect, Transfer, Maintenance (raise a repair), View history; Assign is shown only in checkout (rental board 6), here as a link. *(source: screens/P08-venue-back-office.yaml#BO-510)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Scan**: Opens the card in under a second; offline it uses the cached register and says "Offline - details from 09:40". *(source: contracts/satellite/maintenance.yaml#lookupAsset)*
- **Maintenance**: Opens the maintenance work order (BO-577) with the asset filled in. *(source: screens/P08-venue-back-office.yaml#BO-577)*
- **Print labels**: Produces a print sheet for the selected items; reprinting a label does not change the code. *(source: screens/P08-venue-back-office.yaml#BO-509)*

**Where the user goes next**

- → `BO-504` Rental Inventory Command Center: *Back to Rental Inventory Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The barcode equipment identification list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the barcode equipment identification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No barcode equipment identification yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the barcode equipment identification are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Code not found**: "No item with this code at Summit Peaks" with "Search all venues" for those allowed (per VO-R09). *(source: contracts/satellite/maintenance.yaml#lookupAsset)*
- **Scan of an item that belongs to another venue**: Shown read-only with "Belongs to Aqua Park" and a Transfer action; the venue is not switched. *(source: ADR-0030)*
- **Damaged label**: Type the serial number; "Reprint label" offered on the result. *(source: contracts/satellite/maintenance.yaml#lookupAsset)*

#### Consistency with other screens

- Match `EMP-075`: The Staff App equipment scan uses the same lookup and the same result card.
- Match `BO-069`: Asset labels for venue assets and rental items use one label template component.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
scan:
  code: BIKE-001
  product: Mountain Bike - Adult
  location: North Station, Summit Peaks
  status: Available
  condition: Good
  nextMaintenance: 82 rental hours
```

#### Permissions

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

- Staff change an item's status (maintenance/repair) with a reason and an estimated return-to-service date; scanning an item's QR code pulls up its full details instantly. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-745)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-509` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS117 Rental Management Board 2.dc.html#bo-509`
- Workshop pack: Rental_Management.pdf board 2
- Flow F198 *Rental Management board 2: Rental Inventory Command Center*, step 10: Works in QR / Barcode Equipment Identification → Give every physical serialized rental item a scannable digital identity. This incorporates the equipment-assignment scanning recommendation from the source.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-509?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-504`.
- [ ] Every gated control is gated: `ASSET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-510` Inventory Location Allocation

**Manage how inventory is distributed among rental locations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-510 |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/inventory-location-allocation-bo-510` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-008): Creating a stock location is warehouse set-up, not allocation of rental units to stations (R254; design-notes correction fnb-retail BO-510).

**From the Food, Beverage & Retail process.** How rental units are spread across pick-up stations (50 life jackets at A, 100 at B), with the target per station. The one thing to get right: a station × product grid with current and target quantities.

**Fixed on main** (the package already carries these; draw what it says): Bound to generic stock locations (list/create stock location). (CHG-WIR-008).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Allocation grid**: Rows products, columns stations; current units, target, shortfall. *(source: DI-746)*

**Data it reads**: `listStockLocations` (onLoad, Where stock may sit)

**Where the user goes next**

- → `BO-504` Rental Inventory Command Center: *Back to Rental Inventory Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The inventory location allocation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the inventory location allocation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No inventory location allocation yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the inventory location allocation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
grid: 'Life Jacket: Beach Hut 50 / target 60 · Kayak Jetty 100 / target 90'
```

#### Permissions

- `listStockLocations` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.5.4 | The system should have the ability to record the local /in store inventory (stock management system: used for in-store stock view/management reporting) | Bundles and Promotions | CONTRACTED | `listStockLocations` |
| 4.5.13 | Manage inventory across multiple warehouses and locations. | Bundles and Promotions | CONTRACTED | `listStockLocations` |
| 10.1.5 | The system should have the ability to record the local /in store inventory( for in store stock view/management). | Games & F&B Integration | CONTRACTED | `listStockLocations` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Stock is allocated per pickup location (e.g. 50 life jackets at A, 100 at B) with inter-location transfer; adjustments record damaged/lost/stolen with a reason; rebalancing view shows availability and shortages by station. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-746)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-510` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS117 Rental Management Board 2.dc.html#bo-510`
- Workshop pack: Rental_Management.pdf board 2
- Flow F198 *Rental Management board 2: Rental Inventory Command Center*, step 12: Works in Inventory Location Allocation → Manage how inventory is distributed among rental locations.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-510?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-504`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-511` Inventory Transfer Management

**Control physical inventory movement between locations. The original requirements explicitly include inventory transfers between locations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-511 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `transferId` (navigation) |
| Route | `/rentals/inventory-transfer-management-bo-511` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Moving rental units between stations: a serialised unit by scan, or a pooled quantity, sent and received. The one thing to get right: in transit units are not available at either end.

**Known correction pending (do not draw the wrong version)**

- **Buttons for "Scheduled transfer" and "Emergency transfer".** Why: No operation or field distinguishes them. *(source: screens/P08-venue-back-office.yaml#BO-511; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Dispatched · In transit · Received · Partially received · Cancelled | `listStockTransfers` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Inbound and outbound transfers** (data table, from `listStockTransfers`): **Every transfer whose source or destination is this venue**, marked inbound or outbound (decided 28 September, audit R183).

| Shows | Format | Notes |
|---|---|---|
| Transfer number | text | — |
| From location | the name it points at, never the id | — |
| To location | the name it points at, never the id | — |
| From venue | the name it points at, never the id | The venue of `fromLocationId`. Set by the server (audit R183). |
| To venue | the name it points at, never the id | The venue of `toLocationId`. Set by the server (audit R183). |
| Status | chip: Dispatched, In transit, Received, Partially received, Cancelled | — |
| Dispatched at | 1 Oct 2026, 14:30 | — |
| Received at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Serialized asset transfer (primary button) | navigation or local | — | — | — | — |
| Pooled quantity transfer (secondary button) | navigation or local | — | — | — | — |
| Bulk transfer (secondary button) | navigation or local | — | — | — | — |
| Scheduled transfer (secondary button) | navigation or local | — | — | — | — |
| Emergency transfer (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Transfers**: From, to, items or quantity, sent and received times, status. *(source: DI-746 / contracts/satellite/inventory.yaml#listStockTransfers)*

**Data it reads**: `listStockTransfers` (onLoad, Transfers in flight, inbound and outbound for this venue …)

**Where the user goes next**

- → `BO-504` Rental Inventory Command Center: *Back to Rental Inventory Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The inventory transfer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the inventory transfer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No inventory transfer yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the inventory transfer are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Insufficient stock at the source; 409 The transfer is not `inTransit` or `partiallyReceived` — it has already been received in full, or closed short |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
transfer: 20 × Life Jacket · Kayak Jetty → Beach Hut · sent 09:10 · received 09:35
```

#### Permissions

- `listStockTransfers` → `PRODUCT_VIEW` (read) · staff
- `createStockTransfer` → `PRODUCT_CONFIGURE` (configure) · staff
- `receiveStockTransfer` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.4.15 | Support stock transfers between stores and warehouses including approval workflows, shipment tracking, receiving confirmation, and audit logs. | Bundles and Promotions | CONTRACTED | `createStockTransfer` |
| 4.5.5 | The system should provide ability to transfer stocks to another store with a approval level | Bundles and Promotions | CONTRACTED | `createStockTransfer` |
| 4.5.14 | Transfer inventory between locations with approval workflows. | Bundles and Promotions | CONTRACTED | `createStockTransfer` |
| 15.1.15 | In-Transit Inventory Tracking - System shall track inventory in transit. | Inventory Management | CONTRACTED | `createStockTransfer` |
| 15.2.16 | Internal Transfers - System shall support internal transfers. | Inventory Management | CONTRACTED | `createStockTransfer` |
| 15.2.17 | Replenishment Management - System shall support warehouse replenishment. | Inventory Management | CONTRACTED | `createStockTransfer` |
| 15.5.3 | Inter-Venue Transfers - System shall support inter-venue transfers. | Inventory Management | CONTRACTED | `createStockTransfer` |
| 15.2.15 | Shipment Tracking - System shall support shipment tracking. | Inventory Management | CONTRACTED | `receiveStockTransfer` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Stock is allocated per pickup location (e.g. 50 life jackets at A, 100 at B) with inter-location transfer; adjustments record damaged/lost/stolen with a reason; rebalancing view shows availability and shortages by station. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-746)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-511` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS117 Rental Management Board 2.dc.html#bo-511`
- Workshop pack: Rental_Management.pdf board 2
- Flow F198 *Rental Management board 2: Rental Inventory Command Center*, step 14: Works in Inventory Transfer Management → Control physical inventory movement between locations. The original requirements explicitly include inventory transfers between locations.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-511?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Serialized asset transfer, Pooled quantity transfer, Bulk transfer, Scheduled transfer, Emergency transfer.
- [ ] Every transition is wired: `BO-504`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-512` Inventory Adjustment & Exception Management

**Handle physical inventory discrepancies and exceptional conditions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-512 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/inventory-adjustment-exception-management-bo-512` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Recording damaged, lost or stolen rental units and other discrepancies with a reason, and the history of such adjustments. The one thing to get right: reason and person on every adjustment.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Item | picker: choose an item | — | — | `listStockMovements` ?itemId |
| Location | picker: choose a location | — | — | `listStockMovements` ?locationId |
| Kind | select | — | Receipt · Issue · Sale depletion · Waste · Adjustment in · Adjustment out · Transfer out · Transfer in · Count gain · Count loss · Supplier return · Production | `listStockMovements` ?kind |
| Recorded from | date and time picker | — | — | `listStockMovements` ?recordedFrom |
| Recorded to | date and time picker | — | — | `listStockMovements` ?recordedTo |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Reason**: Damaged · Lost · Stolen · Count difference · Other (note required). *(source: DI-746 / R222)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create stock movement (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listStockMovements` (onLoad, Adjustments so far)

**Where the user goes next**

- → `BO-504` Rental Inventory Command Center: *Back to Rental Inventory Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The inventory adjustment exception list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the inventory adjustment exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No inventory adjustment exception yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the inventory adjustment exception are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed, including an `adjustmentIn`, `adjustmentOut` or `waste` movement with no `reason` (audit R171).; 409 Insufficient stock, and the item does not permit negative balances |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
adjustment: −2 × Paddle · Kayak Jetty · Lost · Omar Ziad · 14:20
```

#### Permissions

- `createStockMovement` → `PRODUCT_CONFIGURE` (configure) · staff
- `listStockMovements` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.4.13 | Maintain real-time inventory balances and automatically update stock after sales, returns, transfers, adjustments, and goods receipt transactions. | Bundles and Promotions | CONTRACTED | `createStockMovement` |
| 4.5.1 | The system should be able to sync all the products and associated information from the inventory management on real-time or timed intervals, to be able to scan/search for the product and complete the … | Bundles and Promotions | CONTRACTED | `createStockMovement` |
| 4.5.2 | The system should be able to sync all the product sale and return products between POS and inventory in order to push data back to inventory management tools to manage re-order levels. | Bundles and Promotions | CONTRACTED | `createStockMovement` |
| 15.1.16 | Damaged Inventory Tracking - System shall track damaged inventory. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.17 | Goods Receipt - System shall support inventory receipt transactions. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.18 | Inventory Adjustments - System shall support stock adjustments. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.19 | Stock Consumption - System shall record stock consumption. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.20 | Return to Stock - System shall support stock returns. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.21 | Write-Off Management - System shall support inventory write-offs. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.22 | Inventory Movement History - System shall maintain inventory movement history. | Inventory Management | CONTRACTED | `createStockMovement` |
| 15.1.23 | Inventory Audit Trail - System shall maintain inventory audit logs. | Inventory Management | CONTRACTED | `createStockMovement` |
| 17.6.4 | Maintenance Inventory Integration - System shall integrate with inventory management. | Maintenance & Safety Management | CONTRACTED | `createStockMovement` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Stock is allocated per pickup location (e.g. 50 life jackets at A, 100 at B) with inter-location transfer; adjustments record damaged/lost/stolen with a reason; rebalancing view shows availability and shortages by station. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-746)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-512` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS117 Rental Management Board 2.dc.html#bo-512`
- Workshop pack: Rental_Management.pdf board 2
- Flow F198 *Rental Management board 2: Rental Inventory Command Center*, step 16: Works in Inventory Adjustment & Exception Management → Handle physical inventory discrepancies and exceptional conditions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-512?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create stock movement, Cancel.
- [ ] Every transition is wired: `BO-504`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-513` Inventory Intelligence & Rebalancing

**Use operational data and AI to improve rental inventory distribution and utilization. This is one of the areas where TICVAI should go beyond the original matrix.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-513 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/inventory-intelligence-rebalancing-bo-513` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-008): Reorder suggestions buy stock; rebalancing moves rental units between stations (R254; design-notes correction fnb-retail BO-513).

**From the Food, Beverage & Retail process.** Where rental units are short or idle across stations, and suggested transfers to rebalance. The one thing to get right: suggestions are advisory — a person creates the transfer.

**Fixed on main** (the package already carries these; draw what it says): getSuggestedRequisitions (procurement reorder suggestions) is bound for rebalancing. (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is AI rebalancing in scope, given the client limited rental AI to reporting and maintenance recommendations?** → Drawn default accepted: Show shortfalls as a report; no AI recommendation panel. *(decided by Chinmay, 2026-10-02; DEC-299 / CHG-NOTE-004)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Location | picker: choose a location | — | — | `getStockPositions` ?locationId |
| Item | picker: choose an item | — | — | `getStockPositions` ?itemId |
| Include zero | toggle | off | — | `getStockPositions` ?includeZero |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every inventory intelligence rebalancing** (data table)

| Shows | Format | Notes |
|---|---|---|
| Utilization by product | text | not in the schema: `Utilization by product` |
| Utilization by location | text | not in the schema: `Utilization by location` |
| Idle equipment | text | not in the schema: `Idle equipment` |
| Shortage risk | text | not in the schema: `Shortage risk` |
| Excess inventory | text | not in the schema: `Excess inventory` |
| Maintenance impact | text | not in the schema: `Maintenance impact` |
| Unavailable inventory | text | not in the schema: `Unavailable inventory` |
| Inventory turnover | text | not in the schema: `Inventory turnover` |

**The selected inventory intelligence rebalancing** (detail panel): The pack groups this record's detail under its own headings: “North Station”, “Marina Station”, “The board should visually demonstrate”, “Serialized Asset”, “Pooled Inventory”, “Integration Boundaries”.

| Shows | Format | Notes |
|---|---|---|
| Utilization by product | text | not in the schema: `Utilization by product` |
| Utilization by location | text | not in the schema: `Utilization by location` |
| Idle equipment | text | not in the schema: `Idle equipment` |
| Shortage risk | text | not in the schema: `Shortage risk` |
| Excess inventory | text | not in the schema: `Excess inventory` |
| Maintenance impact | text | not in the schema: `Maintenance impact` |
| Unavailable inventory | text | not in the schema: `Unavailable inventory` |
| Inventory turnover | text | not in the schema: `Inventory turnover` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Review Recommendation / Create Transfer / Dismiss (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Shortfalls**: Per station and product, available vs expected demand; suggested moves with quantities. *(source: DI-746)*

**Data it reads**: `getStockPositions` (onLoad, Imbalance across locations)

**Where the user goes next**

- → `BO-504` Rental Inventory Command Center: *Back to Rental Inventory Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The inventory intelligence rebalancing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the inventory intelligence rebalancing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No inventory intelligence rebalancing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the inventory intelligence rebalancing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Insufficient stock at the source |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
suggestion: Move 10 City Bicycles Marina Gate → Beach Hut before 15:00 (Beach Hut sold out 2 of last 3 Fridays)
```

#### Permissions

- `getStockPositions` → `PRODUCT_VIEW` (read) · staff
- `createStockTransfer` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

19 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.4.9 | The system should allow multi-store retailing where the stores are connected with the inventory information of other stores. This should allow the guests to order items which are out of stock in the … | Bundles and Promotions | CONTRACTED | `getStockPositions` |
| 4.4.14 | Support multiple warehouses, stores, kiosks, stock rooms, and inventory locations with centralized visibility. | Bundles and Promotions | CONTRACTED | `getStockPositions` |
| 4.4.25 | Maintain one inventory source across POS, B2C, B2B, Mobile App, Kiosks, APIs, and future channels with real-time synchronization. | Bundles and Promotions | CONTRACTED | `getStockPositions` |
| 15.1.9 | Real-Time Inventory Tracking - System shall track inventory levels in real time. | Inventory Management | CONTRACTED | `getStockPositions` |
| 15.1.10 | Multi-Location Inventory - System shall support inventory across multiple locations. | Inventory Management | CONTRACTED | `getStockPositions` |
| 15.1.11 | Multi-Warehouse Inventory - System shall support multiple warehouses. | Inventory Management | CONTRACTED | `getStockPositions` |
| 15.1.12 | Available Stock Tracking - System shall track available stock. | Inventory Management | CONTRACTED | `getStockPositions` |
| 15.1.13 | Reserved Stock Tracking - System shall track reserved inventory. | Inventory Management | CONTRACTED | `getStockPositions` |
| 18.7.1 | Inventory Lookup - Users shall view inventory availability. | Employee Mobile App & AI Assistant | CONTRACTED | `getStockPositions` |
| 18.7.2 | Stock Count - Users shall perform stock counts. | Employee Mobile App & AI Assistant | CONTRACTED | `getStockPositions` |
| 18.7.3 | Inventory Transfers - Users shall execute inventory transfers. | Employee Mobile App & AI Assistant | CONTRACTED | `getStockPositions` |
| 18.7.4 | Goods Receipt - Users shall record goods receipt transactions. | Employee Mobile App & AI Assistant | CONTRACTED | `getStockPositions` |
| … 7 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Stock is allocated per pickup location (e.g. 50 life jackets at A, 100 at B) with inter-location transfer; adjustments record damaged/lost/stolen with a reason; rebalancing view shows availability and shortages by station. *(client request · MoM 9 Sep 2026, 4.3 Rental Inventory & Equipment Management · DI-746)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-513` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS117 Rental Management Board 2.dc.html#bo-513`
- Workshop pack: Rental_Management.pdf board 2
- Flow F198 *Rental Management board 2: Rental Inventory Command Center*, step 18: Works in Inventory Intelligence & Rebalancing → Use operational data and AI to improve rental inventory distribution and utilization. This is one of the areas where TICVAI should go beyond the original matrix.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-513?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Review Recommendation / Create Transfer ….
- [ ] Every transition is wired: `BO-504`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
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
"createStockMovement": {"method":"POST","path":"/stock-movements","contract":"inventory","summary":"Record an issue, return or adjustment","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateStockMovementRequest","responds":"StockMovement"},
"createStockTransfer": {"method":"POST","path":"/stock-transfers","contract":"inventory","summary":"Send stock to another location","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateStockTransferRequest","responds":"StockTransfer"},
"getAsset": {"method":"GET","path":"/assets/{assetId}","contract":"maintenance","summary":"Read an asset with history and documents","permission":"ASSET_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AssetDetail"},
"getStockPositions": {"method":"GET","path":"/stock","contract":"inventory","summary":"Stock on hand by item and location","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"locationId","in":"query","required":null},{"name":"itemId","in":"query","required":null},{"name":"includeZero","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAssets": {"method":"GET","path":"/assets","contract":"maintenance","summary":"List assets","permission":"ASSET_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"maintenanceDue","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRentalBookings": {"method":"GET","path":"/rental-bookings","contract":"rental","summary":"Reservations across venues and locations","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"locationId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"RentalBooking"},
"listStockLocations": {"method":"GET","path":"/stock-locations","contract":"inventory","summary":"List stock locations","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listStockMovements": {"method":"GET","path":"/stock-movements","contract":"inventory","summary":"The movement ledger","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"itemId","in":"query","required":null},{"name":"locationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"recordedFrom","in":"query","required":null},{"name":"recordedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listStockTransfers": {"method":"GET","path":"/stock-transfers","contract":"inventory","summary":"List transfers","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"lookupAsset": {"method":"GET","path":"/assets/lookup","contract":"maintenance","summary":"Find an asset by tag or QR","permission":"ASSET_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assetTag","in":"query","required":null},{"name":"serialNumber","in":"query","required":null}],"requestBody":null,"responds":"AssetDetail"},
"receiveStockTransfer": {"method":"POST","path":"/stock-transfers/{transferId}/receive","contract":"inventory","summary":"Receive a transfer","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"StockTransfer"},
"setAssetStatus": {"method":"PUT","path":"/assets/{assetId}/status","contract":"maintenance","summary":"Take an asset out of service or return it","permission":"ASSET_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetAssetStatusRequest","responds":"AssetStatusResult"},
"updateAsset": {"method":"PATCH","path":"/assets/{assetId}","contract":"maintenance","summary":"Amend an asset","permission":"ASSET_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Asset"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Asset": {"x-ticvai-persistence":"maintenance.asset","allOf":[{"$ref":"#/components/schemas/CreateAssetRequest"},{"type":"object","x-ticvai-retired-columns":["is_maintenance_overdue","document_refs"],"required":["id","status"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid","nullable":true,"description":"1.2.x. **Where this asset is also bookable.** An AV rig is an asset to maintain and a resource to allocate, and they are the same object seen from two sides.\n**`resources` owns the calendar and this owns the condition.** An asset out of service makes its resource unbookable, which is one link rather than two models of availability.\n"},"deviceId":{"type":"string","format":"uuid","nullable":true,"description":"BL-160. **Where this asset is also a registered device.** A turnstile is an asset to maintain and a device to operate, and — exactly as with `resourceId` above — they are the same object seen from two sides.\n**Nothing joined them before this.** A turnstile controller reporting `needsAttention` could not raise a work order against itself, and an engineer closing one had no way back to the device whose firmware caused it.\n**Null for most assets and for most devices.** A chiller is not a device and a signature pad is not on the asset register; the link is sparse, and it lives here rather than on `platform.device` because `platform` is the foundation tier and a foreign key pointing from it into `maintenance` would invert the tiers — every cell running a spine would carry a column for a satellite it may not deploy.\n"},"acquisitionCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"acquiredOn":{"type":"string","format":"date","nullable":true},"depreciation":{"type":"object","nullable":true,"description":"**Recorded here and posted by `finance`.** Depreciation is an accounting act and the asset register is where the useful life is actually known — an engineer knows a chiller lasts fifteen years and an accountant knows what to do about it.\n","properties":{"method":{"type":"string","enum":["straightLine","reducingBalance","unitsOfProduction","none"]},"usefulLifeMonths":{"type":"integer"},"residualValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accumulatedDepreciation":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"retiredOn":{"type":"string","format":"date","nullable":true,"description":"**Retirement is not deletion.** A work order from three years ago still names this asset, and an inspection record with no asset is an inspection of nothing.\n"},"disposalProceeds":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"$ref":"#/components/schemas/AssetStatus"},"statusReason":{"type":"string","nullable":true},"openWorkOrderCount":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Work orders on this asset whose status is `open`, `assigned`, `inProgress`, `paused` or `awaitingParts` — the same set `AssetDetail.openWorkOrders` returns. **Maintained on write**: `createWorkOrder` and every transition into or out of that set (complete, cancel, close, reject back to open) adjust it in the same transaction as the work-order row.\n"},"nextMaintenanceDueAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The earliest `nextDueAt` among this asset's active maintenance plans; null when none has one. **Maintained on write**: recomputed whenever one of those plans is created, amended, suspended or has its `nextDueAt` moved by a completed work order. `listAssets?maintenanceDue` filters on this column against the clock.\n"},"isMaintenanceOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`nextMaintenanceDueAt` is in the past at the moment of the read. **Computed on read and not stored** — it depends on the clock, so a stored copy is stale the minute after it is written.\n"},"lastInspectionAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`performedAt` of the latest inspection submitted against this asset. **Maintained on write** by `submitInspection`, in the same transaction as the inspection row; an inspection synced late with an earlier `performedAt` does not move it back.\n"},"usageCounter":{"type":"number","nullable":true,"description":"Cycles, hours or kilometres. Drives usage-based maintenance."}}}]},
"AssetDetail": {"x-ticvai-persistence":"maintenance.asset","allOf":[{"$ref":"#/components/schemas/Asset"},{"type":"object","properties":{"openWorkOrders":{"type":"array","items":{"$ref":"#/components/schemas/WorkOrder"}},"maintenancePlans":{"type":"array","items":{"$ref":"#/components/schemas/MaintenancePlan"}},"documents":{"type":"array","description":"Manuals, procedures, certificates. What a technician needs on site. Read from `maintenance.asset_document`.\n","items":{"$ref":"#/components/schemas/AssetDocument"}}}}]},
"AssetDocument": {"x-ticvai-persistence":"maintenance.asset_document","type":"object","description":"A document attached to an asset — manual, procedure, certificate — with the name and kind a technician needs on site. **One row per document**, because `AssetDetail.documents` returns a name and a kind for each and a `text[]` of refs has nowhere to hold either.\n","required":["id","assetId","ref"],"properties":{"id":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"ref":{"type":"string","description":"The document in the media store."},"name":{"type":"string","maxLength":200,"nullable":true},"kind":{"allOf":[{"$ref":"#/components/schemas/AssetDocumentKind"}],"nullable":true,"description":"Null where the document arrived as a bare ref in `documentRefs`."}}},
"AssetDocumentInput": {"x-ticvai-persistence":"none — request only","type":"object","required":["ref","kind"],"properties":{"ref":{"type":"string","description":"The document in the media store."},"name":{"type":"string","maxLength":200},"kind":{"$ref":"#/components/schemas/AssetDocumentKind"}}},
"AssetDocumentKind": {"type":"string","enum":["manual","sop","certificate","warranty","drawing","riskAssessment"]},
"AssetStatus": {"type":"string","enum":["inService","outOfService","underMaintenance","awaitingParts","retired","disposed"]},
"AssetStatusResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["asset","downstreamEffects"],"properties":{"asset":{"$ref":"#/components/schemas/Asset"},"downstreamEffects":{"type":"object","description":"What else changed. Surfaced so the person taking a ride out of service sees the commercial consequence at the moment they do it.\n","properties":{"productsSuspended":{"type":"array","items":{"type":"string","format":"uuid"}},"accessPointBlocked":{"type":"boolean"},"performancesAffected":{"type":"integer"},"workOrderId":{"type":"string","format":"uuid","nullable":true}}}}},
"CreateAssetRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["assetTag","name","venueId","criticality"],"properties":{"assetTag":{"type":"string","maxLength":64,"x-ticvai-unique":"venue","description":"**Unique per venue** (decided 28 September, audit R108). Two assets in one venue never share a tag; `createAsset` refuses a duplicate with `409` `duplicate-code`. Two venues may each have an `A-001`.\n"},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"criticality":{"$ref":"#/components/schemas/AssetCriticality"},"priorityOverride":{"allOf":[{"$ref":"#/components/schemas/WorkOrderPriority"}],"nullable":true,"description":"**\"If this device goes down, raise this priority\"** (decided 17 September, M17-01). A corrective work order raised on this asset takes this priority instead of the score. Null means the score decides.\n"},"manufacturer":{"type":"string","maxLength":200},"model":{"type":"string","maxLength":200},"serialNumber":{"type":"string","maxLength":128},"commissionedAt":{"type":"string","format":"date"},"warrantyExpiresAt":{"type":"string","format":"date"},"supplierId":{"type":"string","format":"uuid"},"linkedProductIds":{"type":"array","description":"Products this asset delivers. A fault here can stop them selling.\n","items":{"type":"string","format":"uuid"}},"linkedAccessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Access point this asset controls. Out of service blocks it."},"requiresInspectionToReturn":{"type":"boolean","default":false,"description":"True means a completed inspection is required before return to service. A technician cannot simply declare a ride safe.\n"},"documents":{"type":"array","description":"Manuals, procedures, certificates, each with its name and kind. Stored one row per document in `maintenance.asset_document`, which is where `AssetDetail.documents` reads them from.\n","items":{"$ref":"#/components/schemas/AssetDocumentInput"}},"documentRefs":{"type":"array","x-ticvai-persisted":false,"description":"**The refs alone, kept for callers that predate `documents`.** Each ref sent here is stored as an `asset_document` row with no name and no kind. Returned as the refs of `documents`, computed on read — there is no second copy to fall out of step.\n","items":{"type":"string"}}}},
"CreateStockMovementRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","itemId","locationId","kind","quantity","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"itemId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MovementKind"},"quantity":{"type":"number","exclusiveMinimum":0,"description":"Always positive. **The `kind` decides whether it adds or removes stock**, not the sign (decided 28 September, audit R171).\n"},"unit":{"type":"string"},"reason":{"type":"string","maxLength":500,"description":"**Required for `adjustmentIn`, `adjustmentOut` and `waste`** (decided 28 September, audit R171); adjustments are reported separately.\n"},"costCenterId":{"type":"string","format":"uuid"},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateStockTransferRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","fromLocationId","toLocationId","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"fromLocationId":{"type":"string","format":"uuid"},"toLocationId":{"type":"string","format":"uuid"},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["itemId","quantity"],"properties":{"itemId":{"type":"string","format":"uuid"},"quantity":{"type":"number","minimum":0},"unit":{"type":"string"}}}},"note":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"LocationKind": {"type":"string","enum":["mainStore","subStore","kitchen","bar","retailFloor","cellar","transit"]},
"MaintenancePlan": {"x-ticvai-persistence":"maintenance.preventive_plan","type":"object","required":["id","name","assetId","taskTemplate"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":200},"assetId":{"type":"string","format":"uuid"},"assetCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"Applies to every asset in the category rather than one."},"intervalDays":{"type":"integer","nullable":true,"description":"Elapsed-time trigger."},"usageInterval":{"type":"number","nullable":true,"description":"Usage trigger — cycles, hours, kilometres. **Whichever comes first** when both are set. A ride serviced every three months or ten thousand cycles is one plan.\n"},"leadTimeDays":{"type":"integer","default":7,"description":"How far ahead the work order is generated, so parts can be ordered before the job is already late.\n"},"taskTemplate":{"type":"object","required":["title","priority"],"properties":{"title":{"type":"string"},"description":{"type":"string"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"estimatedMinutes":{"type":"integer"},"inspectionTemplateId":{"type":"string","format":"uuid"},"requiredPartIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},"lastCompletedAt":{"type":"string","format":"date-time","nullable":true},"nextDueAt":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"}}},
"MovementKind": {"type":"string","description":"**The kind decides the direction** (decided 28 September, audit R171). In: `receipt`, `transferIn`, `adjustmentIn`, `countGain`, `production` (the finished item entering stock; the ingredients leave as `issue`). Out: `issue`, `saleDepletion`, `waste`, `adjustmentOut`, `transferOut`, `countLoss`, `supplierReturn`. `adjustment` and `countAdjustment` were split into an in and an out kind so that no kind has two directions.\n","enum":["receipt","issue","saleDepletion","waste","adjustmentIn","adjustmentOut","transferOut","transferIn","countGain","countLoss","supplierReturn","production"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RentalBooking": {"type":"object","x-ticvai-persistence":"rental.booking","description":"Board 5. **The booking outlives the order** — an order completes at payment and the rental is still out.\n","required":["id","productId","from","to","status"],"properties":{"id":{"type":"string","format":"uuid"},"reference":{"type":"string"},"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"returnLocationId":{"type":"string","format":"uuid","nullable":true},"customerId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer"},"status":{"type":"string","enum":["draft","confirmed","awaitingArrival","checkedOut","overdue","partiallyReturned","completed","completedWithDamage","notReturned","cancelled","noShow"]},"checkedOutAt":{"type":"string","format":"date-time","nullable":true},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"returnedAt":{"type":"string","format":"date-time","nullable":true},"depositAuthorisationId":{"type":"string","format":"uuid","nullable":true,"description":"The card deposit's terminal pre-authorisation, written by `checkOutRental` (workbook Q304; CHG-CSA-029). The hold is kept whole until every unit is back (workbook Q306)."},"accruedLateFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"readiness":{"type":"array","readOnly":true,"description":"**Computed, not stored** — agreement, requirements, deposit, equipment.","items":{"type":"object","properties":{"check":{"type":"string"},"satisfied":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"participants":{"type":"array","items":{"$ref":"#/components/schemas/RentalParticipant"}},"scopePath":{"type":"string"}}},
"RentalParticipant": {"type":"object","x-ticvai-persistence":"rental.participant","description":"Board 5.5. **A group rental is one booking with participants**, because the agreement, the deposit and the return are handled together.\n","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"isPrimaryRenter":{"type":"boolean","default":false},"dateOfBirth":{"type":"string","format":"date","nullable":true},"idNumber":{"type":"string","nullable":true},"guardianName":{"type":"string","nullable":true},"emergencyContact":{"type":"string","nullable":true},"hasSignedWaiver":{"type":"boolean","readOnly":true},"customFields":{"type":"object","additionalProperties":true}}},
"SetAssetStatusRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["status","reason","recordedAt"],"properties":{"status":{"$ref":"#/components/schemas/AssetStatus"},"reason":{"type":"string","minLength":3,"maxLength":1000},"inspectionId":{"type":"string","format":"uuid","nullable":true,"description":"Required for return to service where the asset demands it."},"raiseWorkOrder":{"type":"boolean","default":false},"recordedAt":{"type":"string","format":"date-time"}}},
"StockLocation": {"x-ticvai-persistence":"inventory.location","type":"object","required":["id","code","name","venueId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/LocationKind"},"parentLocationId":{"type":"string","format":"uuid","nullable":true},"isActive":{"type":"boolean"}}},
"StockMovement": {"x-ticvai-persistence":"inventory.movement","allOf":[{"$ref":"#/components/schemas/CreateStockMovementRequest"},{"type":"object","required":["balanceAfter","principalId","createdAt"],"properties":{"balanceAfter":{"type":"number"},"unitCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCost":{"x-ticvai-column":"net_cost_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"principalId":{"type":"string","format":"uuid"},"sourceType":{"type":"string","nullable":true,"description":"What generated it — an order, a count, a transfer."},"sourceId":{"type":"string","nullable":true},"journalEntryId":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time"}}}]},
"StockPosition": {"x-ticvai-persistence":"none — derived from movements","type":"object","required":["itemId","locationId","onHand","unit"],"properties":{"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"sku":{"type":"string"},"locationId":{"type":"string","format":"uuid"},"locationName":{"type":"string"},"onHand":{"type":"number"},"allocated":{"type":"number","description":"**Reserved for orders**: the quantity under an active stock reservation for an order (decided 28 September, audit R171). A transfer is not allocation: dispatched stock has already left on-hand and sits in transit.\n"},"available":{"type":"number","description":"**On-hand minus allocated** (decided 28 September, audit R171). What can still be sold or issued.\n"},"unit":{"type":"string"},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lastCountedAt":{"type":"string","format":"date-time","nullable":true},"lastMovementAt":{"type":"string","format":"date-time","nullable":true}}},
"StockTransfer": {"x-ticvai-persistence":"inventory.transfer + inventory.transfer_line","type":"object","required":["id","fromLocationId","toLocationId","status","lines","dispatchedAt"],"properties":{"id":{"type":"string","format":"uuid"},"transferNumber":{"type":"string"},"fromLocationId":{"type":"string","format":"uuid"},"toLocationId":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/TransferStatus"},"lines":{"type":"array","items":{"type":"object","properties":{"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"dispatchedQuantity":{"type":"number"},"receivedQuantity":{"type":"number","nullable":true},"discrepancy":{"type":"number","nullable":true},"discrepancyReason":{"type":"string","nullable":true}}}},"dispatchedByPrincipalId":{"type":"string","format":"uuid"},"receivedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"dispatchedAt":{"type":"string","format":"date-time"},"receivedAt":{"type":"string","format":"date-time","nullable":true},"closeShortReason":{"type":"string","nullable":true,"description":"Why the balance was written off, from `closeTransferShort`."},"closeShortSignedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The supervisor whose step-up closed the transfer short (audit R144)."},"fromVenueId":{"type":"string","format":"uuid","readOnly":true,"description":"The venue of `fromLocationId`. Set by the server (audit R183)."},"toVenueId":{"type":"string","format":"uuid","readOnly":true,"description":"The venue of `toLocationId`. Set by the server (audit R183)."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). `fromLocationId` and `toLocationId` give the endpoints; **this gives the owner**, the source venue's scope.\n\n**Both venues see a transfer between them** (decided 28 September, audit R183). It used to sit at the tenant above both, where neither venue could see it. The row is owned at the source venue and `toScopePath` admits the destination venue too."},"toScopePath":{"type":"string","readOnly":true,"description":"The destination venue's scope. Row-level security admits a caller whose scope matches `scopePath` or `toScopePath`, so both venues read the transfer (decided 28 September, audit R183).\n"}}},
"TransferStatus": {"type":"string","enum":["dispatched","inTransit","received","partiallyReceived","cancelled"]},
"WorkOrder": {"x-ticvai-persistence":"maintenance.work_order","x-ticvai-retired-columns":["is_overdue"],"type":"object","required":["id","workOrderNumber","title","venueId","status","priority","kind","createdAt"],"properties":{"downtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"},"rootCause":{"type":"string","nullable":true,"enum":["wearAndTear","operatorError","guestDamage","manufacturingDefect","environmental","softwareFault","powerFailure","deferredMaintenance","unknown"],"description":"**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"},"rootCauseNote":{"type":"string","nullable":true},"escalatedAt":{"type":"string","format":"date-time","nullable":true},"escalationLevel":{"type":"integer","default":0,"description":"**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"},"id":{"type":"string","format":"uuid"},"workOrderNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"title":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"assetName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"},"status":{"$ref":"#/components/schemas/WorkOrderStatus"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"priorityScore":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"readOnly":true,"description":"The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."},"prioritySource":{"type":"string","enum":["scored","assetOverride","manual"],"readOnly":true,"description":"Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","items":{"type":"string"},"description":"Skills the job needs (M17-13)."},"kind":{"$ref":"#/components/schemas/WorkOrderKind"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"raisedByPrincipalId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"},"locationDescription":{"type":"string","maxLength":500,"nullable":true,"description":"Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"},"elapsedMinutes":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"},"isTimerRunning":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"},"dueAt":{"type":"string","format":"date-time","nullable":true},"isOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"},"requiresVerification":{"type":"boolean"},"sourcePlanId":{"type":"string","format":"uuid","nullable":true},"sourceInspectionId":{"type":"string","format":"uuid","nullable":true},"sourceIncidentId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrderPriority": {"type":"string","enum":["low","normal","high","urgent","emergency"]}
}
```
