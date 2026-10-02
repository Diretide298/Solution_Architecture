# WS96 — Rental Management board 9

**10 screens · 28 operations · 29 schemas · 9 permissions**

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

- **Every control that can be refused must be gated.** 9 permissions apply here:
  `ASSET_MANAGE, ASSET_VIEW, INSPECTION_SUBMIT, MAINTENANCE_EXECUTE, PROCUREMENT_REQUEST, PRODUCT_VIEW, WORK_ORDER_MANAGE, WORK_ORDER_VERIFY, WORK_ORDER_VIEW`. A control nobody can use must say so,
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
| `BO-574` | Maintenance Command Center | B–D | 2 | 0 | 6 | 1 | 0 | 2 | — | notStarted (—) |
| `BO-575` | Maintenance Rule & Service Plan Configuration | B–D | 8 | 0 | 6 | 4 | 1 | 2 | — | notStarted (—) |
| `BO-576` | Maintenance Calendar & Scheduling | B–D | 7 | 30 | 6 | 10 | 3 | 2 | — | notStarted (—) |
| `BO-577` | Maintenance Work Order | B–D | 29 | 20 | 6 | 22 | 3 | 2 | — | notStarted (—) |
| `BO-578` | Technician Repair Workspace | B–D | 8 | 0 | 6 | 5 | 1 | 0 | — | notStarted (—) |
| `BO-579` | Parts, Cost & Maintenance Expense Tracking | B–D | 9 | 5 | 6 | 2 | 2 | 2 | — | notStarted (—) |
| `BO-580` | Asset Maintenance History & Lifecycle | B–D | 0 | 0 | 6 | 5 | 1 | 2 | — | notStarted (—) |
| `BO-581` | Return-to-Service Inspection & Approval | B–D | 5 | 0 | 6 | 3 | 1 | 3 | — | notStarted (—) |
| `BO-582` | Asset Retirement, Write-Off & Replacement Recommendation | B–D | 0 | 0 | 6 | 5 | 1 | 0 | — | notStarted (—) |
| `BO-583` | Maintenance Intelligence & Predictive AI | B–D | 0 | 18 | 6 | 1 | 2 | 2 | — | notStarted (—) |

## Thin screens in this batch

**BO-580, BO-581, BO-582, BO-583 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-574` Maintenance Command Center

**Provide maintenance teams and rental management with a real-time view of rental asset health and maintenance workload.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_VIEW`, `WORK_ORDER_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/maintenance-command-center-bo-574` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No maintenance KPI read (counts by state, average downtime).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The rental board's maintenance command centre: how healthy the rental fleet is and how much maintenance work is in hand - assets under maintenance, inspections waiting, preventive work due or overdue, repairs awaiting parts, items ready to return to service, average downtime - plus the maintenance queue and AI alerts, with tiles opening the board's nine screens. The one thing to get right: it is the shared command-centre pattern with metric tiles and a short queue (per VO-R02), filtered to the rental fleet, not a second maintenance system beside the venue's.

**Known correction pending (do not draw the wrong version)**

- **Ten metric tiles bound to no operation** Why: listWorkOrders and getDueMaintenance (declared) can give counts by status and due, but there is no count or KPI read: Inspection required, Ready for return to service and Average downtime need an aggregate (downtimeMinutes is per work order). *(source: screens/P08-venue-back-office.yaml#BO-574 / contracts/satellite/maintenance.yaml#listWorkOrders; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Damage repair is a maintenance type the work order cannot carry** Why: WorkOrderKind is corrective, planned, inspectionFollowUp, incidentCorrective, improvement; the pack's type (Preventive, Corrective, Damage) and its source list (return inspection, damage case, customer complaint, recall) have no field. *(source: screens/P08-venue-back-office.yaml#BO-583 / contracts/satellite/maintenance.yaml#/components/schemas/WorkOrderKind; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Filter "Product" has no parameter on listWorkOrders** Why: Work orders filter by asset, category, status, priority and dates; product would need the asset's linked product. *(source: screens/P08-venue-back-office.yaml#BO-575 / contracts/satellite/maintenance.yaml#listWorkOrders; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should the rental maintenance command centre be a saved view of the venue maintenance dashboard (rental categories pre-filtered) rather than its own screen?** → Drawn default accepted: Draw it once as the shared command-centre pattern with the rental filter applied (per VO-R02). *(decided by Chinmay, 2026-10-02; DEC-436 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search maintenance | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, location, product, asset, maintenance type, priority and 3 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Assigned to principal | picker: choose an assigned to principal | — | — | `listWorkOrders` ?assignedToPrincipalId |
| Status | select | — | Open · Assigned · In progress · Paused · Awaiting parts · Completed · Verified · Closed · Cancelled | `listWorkOrders` ?status |
| Priority | radio group | — | Low · Normal · High · Urgent · Emergency | `listWorkOrders` ?priority |
| Asset | upload, or pick from the media library | — | — | `listWorkOrders` ?assetId |
| Overdue only | toggle | off | — | `listWorkOrders` ?overdueOnly |
| From | date and time picker | — | — | `listWorkOrders` ?from |
| To | date and time picker | — | — | `listWorkOrders` ?to |
| Category | picker: choose a category | — | — | `listWorkOrders` ?categoryId |
| Within days | number field (days) | 14 | — | `getDueMaintenance` ?withinDays |
| From | date and time picker | — | — | `getDueMaintenance` ?from |
| To | date and time picker | — | — | `getDueMaintenance` ?to |
| Category | picker: choose a category | — | — | `getDueMaintenance` ?categoryId |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Venue comes from the top bar; the filter row offers Location (rental station), Product, Maintenance type (Preventive, Corrective, Damage repair), Priority, Technician, Status and Due date as pickers. Asset is a scan/search box, not a filter list. *(source: screens/P08-venue-back-office.yaml#BO-575)*

#### Outputs: what the screen shows and produces

**Shown**

**Assets Under Maintenance** (metric tile)

**Inspection Required** (metric tile)

**Preventive Maintenance Due** (metric tile)

**Overdue Maintenance** (metric tile)

**Corrective Repairs** (metric tile)

**Damage Repairs** (metric tile)

**Awaiting Parts** (metric tile)

**Ready for Return to Service** (metric tile)

**Average Downtime** (metric tile)

**Maintenance Alerts** (metric tile)

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Ten tiles in the pack's order - Assets under maintenance, Inspection required, Preventive maintenance due, Overdue maintenance (red when above 0), Corrective repairs, Damage repairs, Awaiting parts, Ready for return to service (green, opens BO-581), Average downtime (hours, with the change against last week), Maintenance alerts. Each tile opens the filtered list. *(source: screens/P08-venue-back-office.yaml#BO-574 / screens/P08-venue-back-office.yaml#BO-575)*
- **Maintenance queue**: Work order, asset, product, type, priority, due ("Today", "10 Sep"), status - top ten by priority and due, "See all" to BO-577. Statuses read Open, Assigned, In progress, Awaiting parts, Repair complete, Inspection, Closed (the work order's states in the rental board's words). *(source: screens/P08-venue-back-office.yaml#BO-575 / contracts/satellite/maintenance.yaml#listWorkOrders)*
- **AI alert**: A suggestion card - "6 mountain bikes forecast to need scheduled maintenance during next weekend's peak" - with "See which" and "Plan on Monday instead" opening the calendar; nothing is scheduled until a person confirms. *(source: screens/P08-venue-back-office.yaml#BO-575 / DI-772)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open a board screen**: Tiles for Service plans (BO-575), Calendar (BO-576), Work orders (BO-577), Repair workspace (BO-578), Parts and cost (BO-579), History (BO-580), Return to service (BO-581), Retirement (BO-582), Intelligence (BO-583); each returns here. *(source: F205 step 1 / F205 step 3)*
- **Open a queue row**: Opens the work order in BO-577 with its id. *(source: screens/P08-venue-back-office.yaml#BO-574)*

**Data it reads**: `listWorkOrders` (onLoad, Open work orders); `getDueMaintenance` (onLoad, What is due)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-575` Maintenance Rule & Service Plan Configuration: *Maintenance Rule & Service Plan Configuration*; carries `planId`
- → `BO-576` Maintenance Calendar & Scheduling: *Maintenance Calendar & Scheduling*
- → `BO-577` Maintenance Work Order: *Maintenance Work Order*; carries `workOrderId`
- → `BO-578` Technician Repair Workspace: *Technician Repair Workspace*; carries `workOrderId`
- → `BO-579` Parts, Cost & Maintenance Expense Tracking: *Parts, Cost & Maintenance Expense Tracking*; carries `workOrderId`
- → `BO-580` Asset Maintenance History & Lifecycle: *Asset Maintenance History & Lifecycle*; carries `assetId`
- → `BO-581` Return-to-Service Inspection & Approval: *Return-to-Service Inspection & Approval*; carries `workOrderId`
- → `BO-582` Asset Retirement, Write-Off & Replacement Recommendation: *Asset Retirement, Write-Off & Replacement Recommendation*; carries `assetId`
- → `BO-583` Maintenance Intelligence & Predictive AI: *Maintenance Intelligence & Predictive AI*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The maintenance list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the maintenance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No maintenance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the maintenance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **No rental assets on the asset register yet**: An empty state "No serialised rental items registered - add them in the equipment registry" instead of zero tiles. *(source: designer default)*
- **A tile's figure cannot be read**: The tile shows "Not available" with the reason; the other tiles still load. *(source: designer default)*

#### Consistency with other screens

- Match `BO-070`: The queue rows are the same work orders as the venue work order desk, filtered to rental categories; one row component.
- Match `BO-108`: The venue-wide maintenance attention strip and these tiles count the same records; the rental fleet is one asset category among others.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  underMaintenance: 7
  inspectionRequired: 4
  preventiveDue: 12
  overdue: 2
  corrective: 3
  damage: 5
  awaitingParts: 2
  readyForReturn: 3
  averageDowntime: 18 h (down 4 h)
  alerts: 1
queue:
- wo: WO-2026-01501
  asset: BIKE-017
  product: Mountain Bike
  type: Damage repair
  priority: High
  due: Today
  status: In progress
- wo: WO-2026-01503
  asset: KAY-022
  product: Double Kayak
  type: Preventive
  priority: Normal
  due: 10 Oct
  status: Scheduled
- wo: WO-2026-01504
  asset: BIKE-031
  product: Mountain Bike
  type: Corrective
  priority: Emergency
  due: Today
  status: Awaiting parts
```

#### Permissions

- `listWorkOrders` → `WORK_ORDER_VIEW` (read) · staff
- `getDueMaintenance` → `ASSET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.2.4 | Automated Work Order Generation - System shall automatically generate preventive maintenance work orders. | Maintenance & Safety Management | CONTRACTED | `getDueMaintenance` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-574` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-574`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 1: Opens Maintenance Command Center → Provide maintenance teams and rental management with a real-time view of rental asset health and maintenance workload.
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F205 branch at step 1 (expected): when Nothing has been set up on Maintenance Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F205 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-574?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-575`, `BO-576`, `BO-577`, `BO-578`, `BO-579`, `BO-580`, `BO-581`, `BO-582`, `BO-583`.
- [ ] Every gated control is gated: `ASSET_VIEW`, `WORK_ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-575` Maintenance Rule & Service Plan Configuration

**Define when different rental products/assets require preventive maintenance. This is important because maintenance should not depend only on staff manually noticing a problem.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_MANAGE`, `ASSET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `planId` (navigation) |
| Route | `/rentals/maintenance-rule-service-plan-configuration-bo-575` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Where a rental manager defines when each rental product needs preventive service, so maintenance does not depend on someone noticing: every 30 days, every 50 rentals, every 100 rental hours, when condition drops to Fair, or after a safety incident - whichever happens first - with the checklist, duration, skill, approval and post-service inspection. The one thing to get right: several triggers on one plan, combined with "whichever happens first", shown as one readable sentence.

**Known correction pending (do not draw the wrong version)**

- **Eight select fields bound to no operation** Why: listMaintenancePlans, createMaintenancePlan and updateMaintenancePlan are declared but not bound; Estimated duration should be a number, Service checklist an inspection-template picker. *(source: screens/P08-venue-back-office.yaml#BO-575 / contracts/satellite/maintenance.yaml#createMaintenancePlan; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Rental-count, condition-based and incident-based triggers are not in the plan** Why: MaintenancePlan has intervalDays and one usageInterval (one unit) only; "every 50 rentals OR 100 rental hours" needs two usage meters, and condition and incident triggers have no field. *(source: screens/P08-venue-back-office.yaml#BO-576 / screens/P08-venue-back-office.yaml#BO-583 / contracts/satellite/maintenance.yaml#/components/schemas/MaintenancePlan; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Required skill, required approval and post-maintenance inspection have no field on the plan** Why: The task template carries title, priority, minutes, inspection template and parts only; skills live on the work order, verification on the category. *(source: contracts/satellite/maintenance.yaml#/components/schemas/MaintenancePlan; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **A plan for a product (all bikes) must name one asset** Why: MaintenancePlan requires assetId; a product-wide plan needs the category scope without a single asset. *(source: contracts/satellite/maintenance.yaml#/components/schemas/MaintenancePlan; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is "product" (rental product) a valid plan scope, or must every rental product map one-to-one to an asset category?** → Drawn default accepted: Draw the product picker and resolve it to the product's asset category. *(decided by Chinmay, 2026-10-02; DEC-437 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Product / Category | select field | — | — | — | — | — | — |
| Maintenance Type | select field | — | — | — | — | — | — |
| Trigger | select field | — | — | — | — | — | — |
| Service Checklist | select field | — | — | — | — | — | — |
| Estimated Duration | select field | — | — | — | — | — | — |
| Required Technician Skill | select field | — | — | — | — | — | — |
| Required Approval | select field | — | — | — | — | — | — |
| Post-Maintenance Inspection | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Product / category**: Picker of rental products and categories (Mountain Bike - Adult, Double Kayak); the plan covers every serialised item of that product. *(source: screens/P08-venue-back-office.yaml#BO-576 / contracts/satellite/maintenance.yaml#/components/schemas/MaintenancePlan)*
- **Maintenance type**: Preventive service, Inspection, Cleaning, Safety check - a select, which becomes the work order's title prefix. *(source: screens/P08-venue-back-office.yaml#BO-576)*
- **Triggers**: A list of trigger rows, each removable - Every [30] days; Every [50] rentals; Every [100] rental hours; When condition becomes [Fair]; After a safety-related incident. A line under the list reads "Every 50 rentals or 100 rental hours or 30 days - whichever happens first". *(source: screens/P08-venue-back-office.yaml#BO-576 / screens/P08-venue-back-office.yaml#BO-583)*
- **Service checklist**: Picker of inspection templates for the product's category, with "Create checklist"; not a free-text select. *(source: screens/P08-venue-back-office.yaml#BO-576 / contracts/satellite/maintenance.yaml#listInspectionTemplates)*
- **Estimated duration**: A number in minutes (e.g. 45), not a select. *(source: contracts/satellite/maintenance.yaml#/components/schemas/MaintenancePlan)*
- **Required technician skill**: Multi-select of qualification codes (Bike mechanic, Marine hull); these feed smart assignment. *(source: contracts/satellite/maintenance.yaml#createWorkOrder / DI-924)*
- **Required approval / Post-maintenance inspection**: Two switches - "Supervisor must verify the work" and "Return-to-service inspection required" (default on for safety equipment such as bikes, kayaks, life jackets). *(source: screens/P08-venue-back-office.yaml#BO-576 / screens/P08-venue-back-office.yaml#BO-581)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Plans for this product**: Each plan as its sentence, with next due item ("BIKE-018 in 6 rental hours") and the count of items covered. *(source: contracts/satellite/maintenance.yaml#listMaintenancePlans)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save plan**: Creates or amends the plan (PATCH for an existing one); the confirm says how many items will fall due in the next 7 days as a result. *(source: contracts/satellite/maintenance.yaml#createMaintenancePlan / contracts/satellite/maintenance.yaml#updateMaintenancePlan)*
- **Suspend**: Stops raising work for the plan, with a reason; existing work orders stay. *(source: contracts/satellite/maintenance.yaml#updateMaintenancePlan)*

**Data it reads**: `listMaintenancePlans` (onLoad, Service plans)

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The maintenance rule service configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the maintenance rule service untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No maintenance rule service configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither an interval nor a usage trigger supplied |

#### Edge cases to draw

- **No trigger set**: Save disabled with "Add at least one trigger". *(source: contracts/satellite/maintenance.yaml#/components/schemas/MaintenancePlan)*
- **Peak period**: An AI suggestion may propose moving due work to a quieter day (BO-583); the plan itself is not changed by it. *(source: screens/P08-venue-back-office.yaml#BO-583)*

#### Consistency with other screens

- Match `BO-071`: Same MaintenancePlan record and editor; this is the rental entry into it (per VO-R14).
- Match `BO-576`: Plans produce the due items on the rental maintenance calendar.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
plan:
  product: Mountain Bike - Adult (48 items)
  type: Preventive service
  triggers: Every 50 rentals or 100 rental hours or 30 days - whichever happens first
  checklist: Bike preventive service (12 checks)
  duration: 45 min
  skills:
  - Bike mechanic
  verify: true
  returnInspection: true
```

#### Permissions

- `listMaintenancePlans` → `ASSET_VIEW` (read) · staff
- `createMaintenancePlan` → `ASSET_MANAGE` (configure) · staff
- `updateMaintenancePlan` → `ASSET_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 16.5.24 | Preventive Maintenance - System shall support preventive maintenance schedules. | Device Management | CONTRACTED | `createMaintenancePlan` |
| 17.2.1 | Maintenance Plans - System shall support preventive maintenance plans. | Maintenance & Safety Management | CONTRACTED | `createMaintenancePlan` |
| 17.2.2 | Maintenance Schedules - System shall support maintenance scheduling. | Maintenance & Safety Management | CONTRACTED | `createMaintenancePlan` |
| 17.2.3 | Maintenance Frequencies - System shall support daily, weekly, monthly and annual schedules. | Maintenance & Safety Management | CONTRACTED | `createMaintenancePlan` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Preventive maintenance schedules (e.g. every 30 or 60 days) and periodic counts that flag shortages (e.g. 500 life jackets last month vs 495 this month). *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-768)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-575` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-575`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 2: Works in Maintenance Rule & Service Plan Configuration → Define when different rental products/assets require preventive maintenance. This is important because maintenance should not depend only on staff manually noticing a problem.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-575?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `ASSET_MANAGE`, `ASSET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-576` Maintenance Calendar & Scheduling

**Plan preventive and corrective maintenance while understanding its effect on rental capacity. The original requirement specifically calls for scheduled maintenance periods.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_VIEW`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VIEW` (2 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/maintenance-calendar-scheduling-bo-576` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The rental maintenance calendar: preventive and corrective jobs placed in time against the fleet, so a planner sees what is out when, schedules a job on a free technician and workshop, and is warned before the job takes away items that guests have already booked. The one thing to get right: scheduling a job removes the item from sellable availability for that window, and a clash with existing reservations is shown before confirming, not after.

**Known correction pending (do not draw the wrong version)**

- **Pattern configEditor and template form for a calendar** Why: The pack page is a calendar with Day, Week, Month and Resource views and a scheduling form; draw a calendar screen with a side panel. *(source: screens/P08-venue-back-office.yaml#BO-577 / screens/P08-venue-back-office.yaml#BO-576; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Planned start, expected completion and workshop have no field on the work order** Why: createWorkOrder carries dueAt only; a job cannot be placed on a calendar from 09:00 to 11:00. *(source: screens/P08-venue-back-office.yaml#BO-577 / contracts/satellite/maintenance.yaml#/components/schemas/CreateWorkOrderRequest; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Nothing removes the item from rental availability or reports reservation conflicts** Why: The pack's critical integration (board 9 to board 3) has no operation; createRentalBlackout closes a product or location window, not one serialised item. *(source: screens/P08-venue-back-office.yaml#BO-577 / contracts/satellite/rental.yaml#createRentalBlackout; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The calendar reads only getDueMaintenance, so scheduled corrective jobs never appear (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How long is the turnaround added after a maintenance window before the item is rentable again?** → Drawn default accepted: Show "+ turnaround (product setting)" on the card; value from the rental product. *(decided by Chinmay, 2026-10-02; DEC-438 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Asset | select field | — | — | — | — | — | — |
| Maintenance Type | select field | — | — | — | — | — | — |
| Start Date/Time | select field | — | — | — | — | — | — |
| Expected Completion | select field | — | — | — | — | — | — |
| Technician | select field | — | — | — | — | — | — |
| Workshop/Location | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Within days | number field (days) | 14 | — | `getDueMaintenance` ?withinDays |
| From | date and time picker | — | — | `getDueMaintenance` ?from |
| To | date and time picker | — | — | `getDueMaintenance` ?to |
| Category | picker: choose a category | — | — | `getDueMaintenance` ?categoryId |
| Assigned to principal | picker: choose an assigned to principal | — | — | `listWorkOrders` ?assignedToPrincipalId |
| Status | select | — | Open · Assigned · In progress · Paused · Awaiting parts · Completed · Verified · Closed · Cancelled | `listWorkOrders` ?status |
| Priority | radio group | — | Low · Normal · High · Urgent · Emergency | `listWorkOrders` ?priority |
| Asset | upload, or pick from the media library | — | — | `listWorkOrders` ?assetId |
| Overdue only | toggle | off | — | `listWorkOrders` ?overdueOnly |
| From | date and time picker | — | — | `listWorkOrders` ?from |
| To | date and time picker | — | — | `listWorkOrders` ?to |
| Category | picker: choose a category | — | — | `listWorkOrders` ?categoryId |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Schedule maintenance**: Asset (scan or search), maintenance type, start date and time, expected completion (after start), technician (ranked suggestions shown, nobody pre-assigned), workshop or location, priority. Start and completion are date-time pickers, not selects. *(source: screens/P08-venue-back-office.yaml#BO-577 / DI-924)*
- **Drag to reschedule**: Dragging a job shows the old and new time and whether it now clashes with bookings before it is dropped. *(source: screens/P08-venue-back-office.yaml#BO-576 / designer default)*

#### Outputs: what the screen shows and produces

**Shown**

**Calendar** (calendar view, from `getDueMaintenance`): Maintenance falling due, by day, week or month; a task opens a work order. Day, week, month and agenda views; the day starts at the venue's `calendarDayStartHour`. Sends the visible window as `from`/`to` and the category filter as `categoryId`.

| Shows | Format | Notes |
|---|---|---|
| Plan | the name it points at, never the id | — |
| Plan name | text | — |
| Asset | the image or video | — |
| Asset name | text | — |
| Criticality | chip: Safety critical, Revenue critical, Standard, Low | — |
| Due at | 1 Oct 2026, 14:30 | — |
| Is overdue | yes / no (icon or chip) | — |
| Days overdue | 1,234 | — |
| Triggered by | chip: Interval, Usage | — |
| Work order | the name it points at, never the id | — |

**Scheduled jobs** (data table, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Root cause | chip: Wear and tear, Operator error, Guest damage, Manufacturing defect, Environmental … | Structured, because free text cannot be counted. *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault … |
| Root cause note | text | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| ID | the name it points at, never the id | — |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |
| Priority score | 1,234 | The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01). |
| Priority source | chip: Scored, Asset override, Manual | Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`. |
| Fault assessment | grouped details | What the person raising a fault says about it, which the priority score reads (M17-01). |
| Safety risk | yes / no (icon or chip) | — |
| Guest impact | chip: None, Degraded, Closed | — |
| Required qualification codes | list or chips (count when long) | Skills the job needs (M17-13). |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Calendar**: Views Day, Week, Month, Agenda and Resource (one row per technician or workshop). Day view in hours from the venue's day start; filter by asset category and product; each card "BIKE-017 - Brake repair 09:00-11:00", coloured by type, with due-from-plan items shown dashed until scheduled. *(source: screens/P08-venue-back-office.yaml#BO-577 / DI-919 / DI-908)*
- **Capacity effect**: A strip above the calendar per product - "Mountain bikes available Sat 12 Oct 10:00-14:00 - 41 of 48 (7 in maintenance)". *(source: screens/P08-venue-back-office.yaml#BO-576 / screens/P08-venue-back-office.yaml#BO-583)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Confirm schedule**: Raises (or updates) the work order and blocks the item for the window plus turnaround. If future reservations are affected, a "Reservation conflict" dialog lists them first, with Swap item, Move job or Confirm anyway. *(source: screens/P08-venue-back-office.yaml#BO-577 / screens/P08-venue-back-office.yaml#BO-583)*
- **Open job**: Opens BO-577 with the work order. *(source: screens/P08-venue-back-office.yaml#BO-577)*

**Data it reads**: `getDueMaintenance` (onLoad, The maintenance calendar); `listWorkOrders` (onLoad, Scheduled work orders in the calendar window)

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The maintenance calendar scheduling configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the maintenance calendar scheduling untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No maintenance calendar scheduling configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Job finishes early**: Availability returns from the approved return-to-service time, not the planned end. *(source: screens/P08-venue-back-office.yaml#BO-583)*
- **Job overruns**: Changing the expected completion re-checks bookings and lists any newly affected reservation. *(source: screens/P08-venue-back-office.yaml#BO-583)*

#### Consistency with other screens

- Match `BO-070`: The venue work order desk's calendar toggle is the same component and views.
- Match `BO-071`: Due items from plans appear on both calendars identically.
- Match `BO-520`: Maintenance blocks and rental blackouts show on the rental availability calendar with distinct styles.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
day: 12 Oct 2026
jobs:
- 09:00-11:00 BIKE-017 - Brake repair - Rahul Menon - North Station workshop
- 10:00-12:00 BIKE-031 - Preventive service - Omar Haddad
- 13:00-16:00 KAY-022 - Hull inspection - Aqua Park marina
conflict: BIKE-031 is booked 11:30-13:30 (booking RB-2026-00871, Priya Nair) - swap to BIKE-044?
```

#### Permissions

- `getDueMaintenance` → `ASSET_VIEW` (read) · staff
- `createWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `listWorkOrders` → `WORK_ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.2.4 | Automated Work Order Generation - System shall automatically generate preventive maintenance work orders. | Maintenance & Safety Management | CONTRACTED | `getDueMaintenance` |
| 16.5.25 | Corrective Maintenance - System shall support corrective maintenance tracking. | Device Management | CONTRACTED | `createWorkOrder` |
| 16.5.26 | Maintenance Work Orders - System shall support device maintenance work orders. | Device Management | CONTRACTED | `createWorkOrder` |
| 17.3.1 | Maintenance Requests - System shall support maintenance requests. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.3.2 | Breakdown Management - System shall support equipment breakdown management. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.3.3 | Emergency Maintenance - System shall support emergency maintenance requests. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.1 | Work Order Creation - System shall support work order creation. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.2 | Work Order Assignment - System shall support work order assignment. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.3 | Work Order Prioritization - System shall support work order prioritization. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.4 | Work Order Status Management - System shall support work order lifecycle management. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Every calendar has day, week and month (and agenda) views, and the day view is broken into hours from the venue's day start hour (calendarDayStartHour). *(agreed · MoM 17 Sep 2026, M17-03 · DI-919)*
- Calendars must support filtering by asset category so a team only sees maintenance relevant to them, e.g. an IT team sees turnstiles, printers and POS terminals, not unrelated categories. *(agreed · MoM 17 Sep 2026, 4.2 Preventive Maintenance Planning · DI-908)*
- Preventive maintenance schedules (e.g. every 30 or 60 days) and periodic counts that flag shortages (e.g. 500 life jackets last month vs 495 this month). *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-768)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-576` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-576`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 4: Works in Maintenance Calendar & Scheduling → Plan preventive and corrective maintenance while understanding its effect on rental capacity. The original requirement specifically calls for scheduled maintenance periods.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-576?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `ASSET_VIEW`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-577` Maintenance Work Order

**Create and manage the actual repair/service job.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VIEW` (1 operate, 1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `workOrderId` (navigation), `vendorServiceRequestId` (navigation) |
| Route | `/rentals/maintenance-work-order-bo-577` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The rental board's maintenance work order: one repair or service job on one rental item, from its source (a return damage case, a preventive plan, an inspection) through assignment, repair, return-to-service inspection and closure. Priority shows its score and where it came from; smart assignment ranks technicians but assigns nobody; outside vendors are tracked on the job. The one thing to get right: this is the same work order as the venue's (BO-070) seen through the rental board, so it uses the same row, priority-with-source and lifecycle - plus the rental fields (product, source case, estimated cost).

**Known correction pending (do not draw the wrong version)**

- **Gap note "nothing that can be drawn"; an unlabelled table and detail panel; Create bound to no operation** Why: Pack page 113 lists the work order fields, statuses and attachment groups; createWorkOrder and listWorkOrders are declared. *(source: screens/P08-venue-back-office.yaml#BO-578 / screens/P08-venue-back-office.yaml#BO-577; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Source (return damage case), planned start, expected completion, workshop and estimated cost have no field on the work order** Why: WorkOrder links a plan, inspection or incident only, and carries dueAt and actual costs; the rental source case and planning fields are lost. *(source: screens/P08-venue-back-office.yaml#BO-578 / screens/P08-venue-back-office.yaml#BO-583 / contracts/satellite/maintenance.yaml#/components/schemas/WorkOrder; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Save priority scoring" (the venue-wide weights and bands) is edited from a single work order** Why: The policy is venue configuration (WORK_ORDER_MANAGE, applies to all later work); show it read-only here with a link to maintenance settings. *(source: contracts/satellite/maintenance.yaml#setWorkOrderPriorityPolicy / DI-923; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Priority words differ across sources** Why: Contract low, normal, high, urgent, emergency; maintenance pack P1 Emergency, P2 Critical, P3 High, P4 Normal, P5 Low; rental pack High, Medium, Critical. One display vocabulary is needed. *(source: screens/P08-venue-back-office.yaml#BO-577 / screens/P08-venue-back-office.yaml#BO-575 / contracts/satellite/maintenance.yaml#/components/schemas/WorkOrderPriority; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Duplicate of BO-070** Why: Same work order operations and panels; the rental board entry should open BO-070's component with rental fields shown (per VO-R14). *(source: screens/P08-venue-back-office.yaml#BO-070; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Display priorities as "P1 Emergency ... P5 Low" (the workshop's words) with Urgent as P2, or keep the contract words?** → Drawn default accepted: Draw "P1 Emergency, P2 Urgent, P3 High, P4 Normal, P5 Low". *(decided by Chinmay, 2026-10-02; DEC-439 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Assigned to principal | picker: choose an assigned to principal | — | — | `listWorkOrders` ?assignedToPrincipalId |
| Status | select | — | Open · Assigned · In progress · Paused · Awaiting parts · Completed · Verified · Closed · Cancelled | `listWorkOrders` ?status |
| Priority | radio group | — | Low · Normal · High · Urgent · Emergency | `listWorkOrders` ?priority |
| Asset | upload, or pick from the media library | — | — | `listWorkOrders` ?assetId |
| Overdue only | toggle | off | — | `listWorkOrders` ?overdueOnly |
| From | date and time picker | — | — | `listWorkOrders` ?from |
| To | date and time picker | — | — | `listWorkOrders` ?to |
| Category | picker: choose a category | — | — | `listWorkOrders` ?categoryId |

**Sent by *Assign suggested technician*** (`updateWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | How the maintenance head confirms a `suggestWorkOrderAssignee` candidate (M17-13). | `updateWorkOrder` body |
| Priority `priority` | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | — | `updateWorkOrder` body |
| Required qualification codes `requiredQualificationCodes` | list of values (chips) | optional | — | at most 10 | — | — | `updateWorkOrder` body |
| Due at `dueAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateWorkOrder` body |
| Description `description` | text area | optional | — | max length 5000 | — | — | `updateWorkOrder` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateWorkOrder` body |

**Sent by *Request a vendor*** (`createVendorServiceRequest`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Work order `workOrderId` | picker: choose a work order | required | — | — | shows names, sends the id | — | `createVendorServiceRequest` body |
| Supplier `supplierId` | picker: choose a supplier | required | — | — | shows names, sends the id | — | `createVendorServiceRequest` body |
| Scope `scope` | text area | required | — | max length 2000 | — | What the vendor is asked to do. | `createVendorServiceRequest` body |
| Status `status` | select | optional | Draft | Draft · Sent · Accepted · Scheduled · Completed · Cancelled | — | — | `createVendorServiceRequest` body |
| Vendor reference `vendorReference` | text field | optional | — | max length 100 | — | — | `createVendorServiceRequest` body |
| Quoted cost `quotedCost` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createVendorServiceRequest` body |
| Final cost `finalCost` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createVendorServiceRequest` body |
| Scheduled visit at `scheduledVisitAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createVendorServiceRequest` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `createVendorServiceRequest` body |

**Sent by *Update vendor request*** (`updateVendorServiceRequest`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | optional | — | Draft · Sent · Accepted · Scheduled · Completed · Cancelled | — | — | `updateVendorServiceRequest` body |
| Vendor reference `vendorReference` | text field | optional | — | max length 100 | — | — | `updateVendorServiceRequest` body |
| Quoted cost `quotedCost` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `updateVendorServiceRequest` body |
| Final cost `finalCost` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `updateVendorServiceRequest` body |
| Scheduled visit at `scheduledVisitAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateVendorServiceRequest` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `updateVendorServiceRequest` body |

**Sent by *Save priority scoring*** (`setWorkOrderPriorityPolicy`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Weights `weights` | group | required | — | — | — | — | `setWorkOrderPriorityPolicy` body |
| Safety `weights.safety` | stepper or slider | required | — | min 0; max 100 | — | — | `setWorkOrderPriorityPolicy` body |
| Guest operations `weights.guestOperations` | stepper or slider | required | — | min 0; max 100 | — | — | `setWorkOrderPriorityPolicy` body |
| Revenue `weights.revenue` | stepper or slider | required | — | min 0; max 100 | — | — | `setWorkOrderPriorityPolicy` body |
| Criticality `weights.criticality` | stepper or slider | required | — | min 0; max 100 | — | — | `setWorkOrderPriorityPolicy` body |
| Bands `bands` | repeatable rows | required | — | at least 1; at most 5 | — | Highest first. A score at or above `minScore` takes `priority`. | `setWorkOrderPriorityPolicy` body |
| Min score `bands[].minScore` | stepper or slider | required | — | min 0; max 100 | — | — | `setWorkOrderPriorityPolicy` body |
| Priority `bands[].priority` | radio group | required | — | Low · Normal · High · Urgent · Emergency | — | — | `setWorkOrderPriorityPolicy` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Raise a work order**: Asset (scan or search; product filled from it), maintenance type, source (Return damage case with its case number, Preventive plan, Return inspection, Staff inspection, Customer complaint, AI recommendation, Manufacturer recall), issue text, photos first, fault assessment (anyone at risk; guest impact None / Degraded / Closed), required skills, planned start, expected completion, workshop, estimated cost in AED. Priority empty by default with "Will be scored". *(source: screens/P08-venue-back-office.yaml#BO-578 / screens/P08-venue-back-office.yaml#BO-583 / DI-923 / contracts/satellite/maintenance.yaml#createWorkOrder)*
- **Priority override**: Choosing a priority marks it Manual and asks for a reason; the scored value stays visible beside it. *(source: screens/P08-venue-back-office.yaml#BO-577 / DI-923)*
- **Vendor request**: Supplier picker, scope (required, max 2000), vendor reference, quoted cost and final cost in AED, visit date and time; status steps Draft > Sent > Accepted > Scheduled > Completed or Cancelled. *(source: contracts/satellite/maintenance.yaml#createVendorServiceRequest / contracts/satellite/maintenance.yaml#updateVendorServiceRequest)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Detail panel** (detail panel): One record, read-only.

**Priority and how it was set** (detail panel, from `getWorkOrder`): **The score and its source side by side** (decided 17 September, M17-01): *scored* (the venue policy), *asset override* or *manual*, so a supervisor sees why a fault is urgent.

| Shows | Format | Notes |
|---|---|---|
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |
| Priority score | 1,234 | The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01). |
| Priority source | chip: Scored, Asset override, Manual | Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`. |
| Fault assessment | grouped details | What the person raising a fault says about it, which the priority score reads (M17-01). |
| Required qualification codes | list or chips (count when long) | Skills the job needs (M17-13). |

**Suggested technicians** (data table, from `suggestWorkOrderAssignee`): **Smart assignment, confirmed by the maintenance head** (decided 17 September, M17-13). The ranking assigns nothing; *Assign* on a row sends its principal with `updateWorkOrder`.

| Shows | Format | Notes |
|---|---|---|
| Rank | 1,234 | — |
| Name | text | — |
| Has all qualifications | yes / no (icon or chip) | — |
| Missing qualification codes | list or chips (count when long) | — |
| On shift | yes / no (icon or chip) | On shift now or before the work order is due. |
| Open work order count | 1,234 | — |

**Vendor requests** (data table, from `listVendorServiceRequests`): Outside vendors engaged on this work order (decided 17 September, M17-13).

| Shows | Format | Notes |
|---|---|---|
| Supplier | the name it points at, never the id | — |
| Scope | text | What the vendor is asked to do. |
| Status | chip: Draft, Sent, Accepted, Scheduled, Completed, Cancelled | — |
| Vendor reference | text | — |
| Quoted cost | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Scheduled visit at | 1 Oct 2026, 14:30 | — |

**How fault priority is scored** (detail panel, from `getWorkOrderPriorityPolicy`): **The venue's weights and bands** (decided 17 September, M17-01): safety, guest operations, revenue and asset criticality, summing to 100.

| Shows | Format | Notes |
|---|---|---|
| Weights | grouped details | — |
| Bands | list or chips (count when long) | Highest first. A score at or above `minScore` takes `priority`. |
| Updated at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create work order (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Assign suggested technician (secondary button) | `updateWorkOrder` PATCH `/work-orders/{workOrderId}` | inline | WorkOrder | — | — |
| Request a vendor (secondary button) | `createVendorServiceRequest` POST `/vendor-service-requests` | VendorServiceRequest | VendorServiceRequest | 400 Validation failed; 409 The work order is closed or cancelled. | — |
| Update vendor request (secondary button) | `updateVendorServiceRequest` PATCH `/vendor-service-requests/{vendorServiceRequestId}` | inline | VendorServiceRequest | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The request is already `completed` or `cancelled`. | — |
| Save priority scoring (secondary button) | `setWorkOrderPriorityPolicy` PUT `/work-order-priority-policy` | WorkOrderPriorityPolicy | WorkOrderPriorityPolicy | 400 Weights that do not sum to 100, or bands that do not descend. | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Header**: Work order number, asset, product, source with a link ("Return damage case DMG-20261001-0021"), type, priority badge with source, status step bar. *(source: screens/P08-venue-back-office.yaml#BO-577 / DI-923)*
- **Priority and how it was set**: "High - scored 52 (safety 40 + guest operations 5 + revenue 0 + criticality 7)" or "Emergency - asset override" or "Normal - manual, by Fatima Al Hashimi: parts on site"; the score and its source always side by side. *(source: contracts/satellite/maintenance.yaml#getWorkOrderPriorityPolicy / DI-923)*
- **Suggested technicians**: Ranked rows - name, all skills (tick) or missing skills named, on shift now or before due, open jobs; an Assign button per row; no row is pre-selected. *(source: contracts/satellite/maintenance.yaml#suggestWorkOrderAssignee / DI-924)*
- **Attachments**: Grouped as the pack lists - Return photos, Damage photos, Incident records, Technician photos, Documents - each with its evidence stage. *(source: screens/P08-venue-back-office.yaml#BO-578 / contracts/satellite/maintenance.yaml#attachWorkOrderEvidence)*
- **Status bar**: Open > Assigned > In progress > Awaiting parts > Repair complete > Inspection > Closed, mapped to the work order's states (Repair complete is Completed, Inspection is awaiting the return-to-service inspection). *(source: screens/P08-venue-back-office.yaml#BO-578 / contracts/satellite/maintenance.yaml#/components/schemas/WorkOrderStatus)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Create work order**: Raises it with photos; priority scored unless set; returns the number and score. *(source: contracts/satellite/maintenance.yaml#createWorkOrder)*
- **Assign (on a suggested row)**: Sets the assignee; the job reads "Assigned - not yet accepted" until the technician accepts on the Staff App. *(source: contracts/satellite/maintenance.yaml#updateWorkOrder / DI-924)*
- **Request a vendor / Update vendor request**: Adds or moves a vendor request; a closed or cancelled work order refuses a new one (409) and completed or cancelled requests are final. *(source: contracts/satellite/maintenance.yaml#createVendorServiceRequest / contracts/satellite/maintenance.yaml#updateVendorServiceRequest)*
- **Send to return-to-service inspection**: After Repair complete, opens BO-581 for this asset and job. *(source: screens/P08-venue-back-office.yaml#BO-581)*

**Data it reads**: `listWorkOrders` (onLoad, List work orders)

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The maintenance work order list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the maintenance work order untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No maintenance work order yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the maintenance work order are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 400 Weights that do not sum to 100, or bands that do not descend.; 409 The request is already `completed` or `cancelled`.; 409 The work order is closed or cancelled. |

#### Edge cases to draw

- **Item still rented when the job is raised (damage found mid-rental)**: The job is raised; the item shows "With guest until 16:30" and the planned start cannot be before return. *(source: screens/P08-venue-back-office.yaml#BO-583 / designer default)*
- **Venue scoring weights changed after the job was raised**: The job keeps its original score; the panel says "Scored under the policy of 14 Sep". *(source: contracts/satellite/maintenance.yaml#setWorkOrderPriorityPolicy)*
- **No technician has all required skills**: The list still ranks, with missing skills in red; "Request a vendor" is highlighted. *(source: contracts/satellite/maintenance.yaml#suggestWorkOrderAssignee / DI-924)*

#### Consistency with other screens

- Match `BO-070`: Same work order, row, priority badge with source, suggestion list and vendor panel; one component set (per VO-R14).
- Match `BO-578`: The technician's execution of this job.
- Match `BO-581`: Return to service is a separate step after Repair complete.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
workOrder:
  wo: WO-2026-01501
  asset: BIKE-017
  product: Mountain Bike - Adult
  source: Return damage case DMG-20261001-0021
  type: Damage repair
  issue: Front brake lever bent during rental.
  priority: High - scored 52
  status: Assigned - not yet accepted
  assignee: Rahul Menon
  plannedStart: 1 Oct 2026 09:00
  expectedCompletion: 1 Oct 2026 11:00
  workshop: North Station workshop
  estimatedCost: AED 130.00
suggestions:
- rank: 1
  name: Rahul Menon
  skills: All
  onShift: 'Yes'
  openJobs: 2
- rank: 2
  name: Omar Haddad
  skills: Missing Bike mechanic L2
  onShift: 'Yes'
  openJobs: 1
vendor:
  supplier: Gulf Cycles LLC
  scope: Replace hydraulic brake set
  status: Sent
  quoted: AED 420.00
```

#### Permissions

- `getWorkOrderPriorityPolicy` → `WORK_ORDER_VIEW` (read) · staff
- `setWorkOrderPriorityPolicy` → `WORK_ORDER_MANAGE` (configure) · staff
- `suggestWorkOrderAssignee` → `WORK_ORDER_VIEW` (read) · staff
- `listVendorServiceRequests` → `WORK_ORDER_VIEW` (read) · staff
- `createVendorServiceRequest` → `WORK_ORDER_MANAGE` (configure) · staff
- `updateVendorServiceRequest` → `WORK_ORDER_MANAGE` (configure) · staff
- `listWorkOrders` → `WORK_ORDER_VIEW` (read) · staff
- `getWorkOrder` → `WORK_ORDER_VIEW` (read) · staff
- `createWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `updateWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `attachWorkOrderEvidence` → `MAINTENANCE_EXECUTE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

22 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.4.8 | Work Order Audit Trail - System shall maintain work order audit logs. | Maintenance & Safety Management | CONTRACTED | `getWorkOrder` |
| 16.5.25 | Corrective Maintenance - System shall support corrective maintenance tracking. | Device Management | CONTRACTED | `createWorkOrder` |
| 16.5.26 | Maintenance Work Orders - System shall support device maintenance work orders. | Device Management | CONTRACTED | `createWorkOrder` |
| 17.3.1 | Maintenance Requests - System shall support maintenance requests. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.3.2 | Breakdown Management - System shall support equipment breakdown management. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.3.3 | Emergency Maintenance - System shall support emergency maintenance requests. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.1 | Work Order Creation - System shall support work order creation. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.2 | Work Order Assignment - System shall support work order assignment. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.3 | Work Order Prioritization - System shall support work order prioritization. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.4 | Work Order Status Management - System shall support work order lifecycle management. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 18.5.1 | Photo Capture - Users shall capture photos. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.2 | Video Capture - Users shall capture videos. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| … 10 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Smart assignment (confirmed by the maintenance head): technicians ranked by skill, shift and load; the ranking assigns nothing and Assign on a row does; outside vendor requests listed on the work order. *(agreed · MoM 17 Sep 2026, M17-13 · DI-924)*
- Work-order priority is shown with its source side by side (scored by venue policy, asset override, or manual); an asset carries a "fault priority override"; a new work order leaves priority empty to be scored; the venue sets weights and bands (safety, guest operations, revenue, asset criticality, summing to 100). *(agreed · MoM 17 Sep 2026, M17-01 · DI-923)*
- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-577` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-577`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 6: Works in Maintenance Work Order → Create and manage the actual repair/service job.

#### Acceptance for the design

- [ ] Every input above is drawn (29), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-577?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create work order, Cancel, Assign suggested technician, Request a vendor, Update vendor request, Save priority scoring.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 5 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-578` Technician Repair Workspace

**Provide the technician with a focused operational screen for executing maintenance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE` (1 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `workOrderId` (navigation) |
| Route | `/rentals/technician-repair-workspace-bo-578` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The technician's focused workspace for one repair at a workshop terminal or tablet: the asset and issue, the maintenance checklist to tick, Start / Pause / Awaiting parts / Complete repair, a timestamped work log, notes and evidence. It is the desk-size twin of the Staff App task screen (EMP-005), not a separate design. The one thing to get right: every action is timestamped and attributed automatically, and "Complete repair" does not make the item rentable - it hands over to the return-to-service inspection.

**Known correction pending (do not draw the wrong version)**

- **Gap note "nothing that can be drawn"; one unlabelled primary button and Cancel** Why: Pack pages 113-114 give the checklist, the four technician actions, the work log, notes and evidence. *(source: screens/P08-venue-back-office.yaml#BO-579 / screens/P08-venue-back-office.yaml#BO-578; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No checklist answers and no free-text work-log entries on a work order** Why: timeEntries hold timer actions only; the pack's checklist ticks and "Brake lever confirmed damaged" have nowhere to be stored. *(source: screens/P08-venue-back-office.yaml#BO-579 / contracts/satellite/maintenance.yaml#/components/schemas/WorkOrderDetail; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Duplicate of EMP-005 at desk width** Why: Same operations and states; draw one component (per VO-R14). *(source: screens/P06-staff-app.yaml#EMP-005; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Only start, time and complete are declared; pause, resume and evidence are missing (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Form: Pause** (modal, opened by *Pause*; *Pause* calls `pauseWorkOrder`, *Cancel* sends nothing)

**Collects what `pauseWorkOrder` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Awaiting parts · Awaiting permit · Awaiting outage window · Awaiting specialist · End of shift · Safety concern · Other | — | — | `pauseWorkOrder` body |
| Note `note` | text area | optional | — | max length 300; Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real … | `pauseWorkOrder` body |
| Requisition `requisitionId` | picker: choose a requisition | optional | — | — | shows names, sends the id | Where a part was ordered, so the two are linked. | `pauseWorkOrder` body |

Errors to draw in the form: 400 Validation failed

**Form: Add evidence** (modal, opened by *Add evidence*; *Add evidence* calls `attachWorkOrderEvidence`, *Cancel* sends nothing)

**Collects what `attachWorkOrderEvidence` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Photo · Video · Document · Note · Signature | — | — | `attachWorkOrderEvidence` body |
| Asset ref `assetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | In the media store | `attachWorkOrderEvidence` body |
| Text `text` | text area | optional | — | max length 4000 | — | Where the kind is a note | `attachWorkOrderEvidence` body |
| Captured at `capturedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `attachWorkOrderEvidence` body |
| Stage `stage` | radio group | optional | — | Before · During · After · Sign off | — | — | `attachWorkOrderEvidence` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Checklist**: The plan's or category's checklist (Inspect brake lever, Inspect brake cable, Replace brake lever, Test braking system, Road/safety test, Final inspection) as tick rows with a note per row; failed safety test blocks Complete repair and offers Continue repair, Escalate, Request specialist. *(source: screens/P08-venue-back-office.yaml#BO-578 / screens/P08-venue-back-office.yaml#BO-579)*
- **Pause and Awaiting parts**: Two buttons as the pack shows; both use the one pause reason list (Awaiting parts selected for the second), Other needs a note. *(source: screens/P08-venue-back-office.yaml#BO-579 / contracts/satellite/maintenance.yaml#pauseWorkOrder)*
- **Notes**: Free text added to the work log with time and name (e.g. "Brake cable remains acceptable; lever replacement required"). *(source: screens/P08-venue-back-office.yaml#BO-579 / contracts/satellite/maintenance.yaml#attachWorkOrderEvidence)*
- **Evidence**: Add photo / Add document, each tagged Before, During or After. *(source: screens/P08-venue-back-office.yaml#BO-579 / contracts/satellite/maintenance.yaml#attachWorkOrderEvidence)*
- **Complete repair**: Resolution code chips and resolution text (required), completion photos where the category demands; recordedAt from the clock, never asked. *(source: contracts/satellite/maintenance.yaml#completeWorkOrder)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Pause (secondary button) | `pauseWorkOrder` POST `/work-orders/{workOrderId}/pause` | inline | WorkOrder | 400 Validation failed | opens modal first |
| Resume (secondary button) | `resumeWorkOrder` POST `/work-orders/{workOrderId}/resume` | — | WorkOrder | — | — |
| Add evidence (secondary button) | `attachWorkOrderEvidence` POST `/work-orders/{workOrderId}/attachments` | inline | WorkOrderAttachment | — | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Job header**: Asset BIKE-017, work order number, issue line, priority badge with source, running labour timer and elapsed since raised. *(source: screens/P08-venue-back-office.yaml#BO-578 / DI-231)*
- **Work log**: Rows Time, Technician, Activity - "09:05 Rahul Menon Inspection started", "09:18 Brake lever confirmed damaged", "09:22 Replacement required" - generated from actions and notes, newest last. *(source: screens/P08-venue-back-office.yaml#BO-579 / MATRIX 17.4.8)*
- **Parts and cost so far**: Parts reserved and used with unit cost and line total in AED, labour minutes and cost, total - read-only here; recording parts opens the parts panel (BO-579). *(source: screens/P08-venue-back-office.yaml#BO-579 / contracts/satellite/maintenance.yaml#/components/schemas/WorkOrderDetail / DI-769)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Start work**: Starts the work order and the labour timer; logs "Work started". *(source: contracts/satellite/maintenance.yaml#startWorkOrder)*
- **Pause / Awaiting parts / Resume**: Stops or restarts the timer with the reason in the log; Awaiting parts offers Reserve parts and Request transfer. *(source: contracts/satellite/maintenance.yaml#pauseWorkOrder / contracts/satellite/maintenance.yaml#resumeWorkOrder / DI-925)*
- **Complete repair**: Moves to Repair complete - awaiting inspection; the screen says "Not yet rentable - return-to-service inspection next" and links BO-581. *(source: screens/P08-venue-back-office.yaml#BO-581 / contracts/satellite/maintenance.yaml#completeWorkOrder)*

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The technician repair list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the technician repair untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No technician repair yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the technician repair are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Completion photographs required for this category and none supplied; 400 Validation failed; 409 Action inconsistent with the current timer state |

#### Edge cases to draw

- **Two people open the same job**: The second sees "Rahul Menon is working on this (started 09:05)" and the action buttons are disabled for them. *(source: contracts/satellite/maintenance.yaml#startWorkOrder / designer default)*
- **Required checklist item unticked**: Complete repair disabled with "3 checks left"; skipping a mandatory check needs a reason and a supervisor. *(source: screens/P08-venue-back-office.yaml#BO-578)*

#### Consistency with other screens

- Match `EMP-005`: Same states, buttons, evidence stages, resolution codes and checklist as the Staff App task screen; one design at two widths.
- Match `BO-579`: Parts recorded there show in this screen's cost panel.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
job:
  asset: BIKE-017
  wo: WO-2026-01501
  issue: Front brake lever damaged.
  checklist:
  - Inspect brake lever - done
  - Inspect brake cable - done
  - Replace brake lever - done
  - Test braking system - pending
  - Road/safety test - pending
  - Final inspection - pending
  log:
  - 09:05 Rahul Menon - Inspection started
  - 09:18 Rahul Menon - Brake lever confirmed damaged
  - 09:22 Rahul Menon - Replacement required
  parts:
  - Brake lever x1 AED 55.00
  - Grip x1 AED 15.00
  labour: 45 min, AED 60.00
  total: AED 130.00
```

#### Permissions

- `startWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `recordWorkOrderTime` → `WORK_ORDER_MANAGE` (configure) · staff
- `completeWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `pauseWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `resumeWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `attachWorkOrderEvidence` → `MAINTENANCE_EXECUTE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 18.5.1 | Photo Capture - Users shall capture photos. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.2 | Video Capture - Users shall capture videos. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.3 | Document Upload - Users shall upload documents. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.4 | Notes Management - Users shall record notes. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.5 | Signature Capture - Users shall capture signatures. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-578` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-578`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 8: Works in Technician Repair Workspace → Provide the technician with a focused operational screen for executing maintenance.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-578?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel, Pause, Resume, Add evidence.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-579` Parts, Cost & Maintenance Expense Tracking

**Capture the operational cost associated with maintaining rental equipment. This should integrate with the broader Inventory/Procurement and Finance modules rather than recreate them.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PROCUREMENT_REQUEST`, `PRODUCT_VIEW`, `WORK_ORDER_MANAGE` (1 operate, 1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `workOrderId` (navigation), `stockReservationId` (navigation) |
| Route | `/rentals/parts-cost-maintenance-expense-tracking-bo-579` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Parts and cost for a maintenance work order on rental equipment: parts are reserved from the main inventory (never a separate maintenance stock), issued when used, and released when not needed. Labour and parts cost roll up to the work order. The one thing to get right is that a short-stock refusal names the part, and reserving is hidden offline.

**Known correction pending (do not draw the wrong version)**

- **The primary button has no label and no operation ("The act the screen exists for").** Why: The act is recording parts used against the work order (recordWorkOrderParts). Label it "Record parts used". *(source: screens/P08-venue-back-office.yaml#BO-579 / contracts/satellite/maintenance.yaml#recordWorkOrderParts; Food, Beverage & Retail)*
- **Nothing on the screen selects or reads the work order whose parts are shown, and a requisition for a missing part cannot be linked to it.** Why: The list filters by work order, but the screen has no work-order read. F15's "linked, so the job and the purchase find each other" has no field. *(source: F15 step 2 / DI-925 / TRACKER Workshops/Actions row 304; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**Sent by *Reserve parts*** (`createStockReservation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `createStockReservation` body |
| Item `itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `createStockReservation` body |
| Location `locationId` | picker: choose a location | required | — | — | shows names, sends the id | — | `createStockReservation` body |
| Quantity `quantity` | number field | required | — | more than 0 | — | — | `createStockReservation` body |
| Source type `sourceType` | radio group | required | — | Work order · Rental agreement · Order · Transfer · Other | — | What a stock reservation is for (decided 17 September, M17-02; `rentalAgreement` is the existing use from `rental.agreement_item`). | `createStockReservation` body |
| Source `sourceId` | picker: choose a source | required | — | — | shows names, sends the id | The id of what the stock is reserved for: a work order, a rental agreement or an order. | `createStockReservation` body |
| Expires at `expiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createStockReservation` body |
| Released at `releasedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createStockReservation` body |

**Sent by *Release reservation*** (`releaseStockReservation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 300 | — | — | `releaseStockReservation` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Reserve part**: Item (search or scan), location, quantity. The location defaults to the main store. Hidden when the device is offline. *(source: DI-925 / contracts/satellite/inventory.yaml#createStockReservation)*
- **Record parts used**: Lines with quantity used. Reserved parts are issued first, from the reservation. *(source: contracts/satellite/maintenance.yaml#recordWorkOrderParts)*

#### Outputs: what the screen shows and produces

**Shown**

**Parts reserved for this work order** (data table, from `listStockReservations`): **Reserved in the general inventory, not a maintenance stock** (decided 17 September, M17-02). Sends `?sourceType=workOrder&sourceId=` the work order. Recording parts issues from the reservation first.

| Shows | Format | Notes |
|---|---|---|
| Item | the name it points at, never the id | — |
| Location | the name it points at, never the id | — |
| Quantity | 1,234.5 | — |
| Status | chip: Active, Consumed, Released, Expired | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Reserve parts (secondary button) | `createStockReservation` POST `/stock-reservations` | InventoryStockReservation | InventoryStockReservation | 400 Validation failed; 409 Not enough free stock at the location. | — |
| Release reservation (secondary button) | `releaseStockReservation` POST `/stock-reservations/{stockReservationId}/release` | inline | InventoryStockReservation | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The reservation is not `active`. | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Parts and cost**: Reserved parts (item, location, quantity, status Active / Used / Released / Expired), parts cost, labour cost, total cost (AED). *(source: contracts/satellite/inventory.yaml#listStockReservations / contracts/satellite/maintenance.yaml#recordWorkOrderParts)*

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The parts cost maintenance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the parts cost maintenance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No parts cost maintenance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the parts cost maintenance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Insufficient stock; 409 Not enough free stock at the location.; 409 The reservation is not `active`. |

#### Edge cases to draw

- **Not enough free stock**: Refused, naming the part, e.g. "Not enough free 'Kayak paddle blade, 210 cm' at Main Store (1 free, 2 asked)". *(source: DI-925 / contracts/satellite/inventory.yaml#createStockReservation)*

#### Consistency with other screens

- Match `EMP-005`: The technician reserves and records the same parts on the staff app.
- Match `BO-078`: A part with no stock is requested on a requisition. See the correction there (no work-order link).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
workOrder: 'WO-AQP-003317 · Kayak #12 · cracked paddle'
reserved:
- item: Kayak paddle blade, 210 cm
  location: Main Store
  qty: 2
  status: Active
costs:
  parts: AED 180.00
  labour: AED 95.00
  total: AED 275.00
```

#### Permissions

- `listStockReservations` → `PRODUCT_VIEW` (read) · staff
- `createStockReservation` → `PROCUREMENT_REQUEST` (operate) · staff
- `releaseStockReservation` → `PROCUREMENT_REQUEST` (operate) · staff
- `recordWorkOrderParts` → `WORK_ORDER_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.6.1 | Spare Parts Management - System shall support maintenance spare parts management. | Maintenance & Safety Management | CONTRACTED | `recordWorkOrderParts` |
| 17.6.3 | Spare Parts Consumption - System shall record spare parts consumption. | Maintenance & Safety Management | CONTRACTED | `recordWorkOrderParts` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Work-order parts are reserved in the general inventory; the reserve action is hidden offline, and a refusal for short stock names the part. *(agreed · MoM 17 Sep 2026, M17-02 · DI-925)*
- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-579` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-579`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 10: Works in Parts, Cost & Maintenance Expense Tracking → Capture the operational cost associated with maintaining rental equipment. This should integrate with the broader Inventory/Procurement and Finance modules rather than recreate them.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-579?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel, Reserve parts, Release reservation.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `PROCUREMENT_REQUEST`, `PRODUCT_VIEW`, `WORK_ORDER_MANAGE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-580` Asset Maintenance History & Lifecycle

**Provide the complete maintenance history of an individual serialized rental asset. The original requirement specifically requires maintenance history tracking.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/rentals/asset-maintenance-history-lifecycle-bo-580` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The complete maintenance story of one serialised rental item for a manager or auditor: when it was bought, how much it has earned, how often and why it was repaired, what that cost and how long it was out, in one timeline. It answers whether the item is still worth keeping. The one thing to get right: lifetime revenue against lifetime maintenance cost, side by side, with the timeline as the evidence below.

**Known correction pending (do not draw the wrong version)**

- **Only getAssetHistory is bound; the facts, summary and economics have no source** Why: History entries carry kind, summary and time only - no cost, downtime or revenue. Costs are per work order (WorkOrderDetail), revenue and rental counts are rental data; nothing aggregates them per asset. *(source: contracts/satellite/maintenance.yaml#/components/schemas/AssetHistoryEntry / contracts/satellite/maintenance.yaml#/components/schemas/WorkOrderDetail; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Gap note "nothing that can be drawn"** Why: Pack pages 115-116 give the facts, the maintenance summary, the timeline and the revenue-against-cost view. *(source: screens/P08-venue-back-office.yaml#BO-580 / screens/P08-venue-back-office.yaml#BO-581; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **History entries do not say whether a repair was preventive, corrective or damage** Why: AssetHistoryEntry kinds are workOrder, inspection, incident, statusChange, partReplaced, planCompleted; damage repair is not distinguishable. *(source: screens/P08-venue-back-office.yaml#BO-581 / contracts/satellite/maintenance.yaml#/components/schemas/AssetHistoryEntry; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Period**: Lifetime (default), this year, last 12 months; the annual view shows lifecycle cost per item as the client asked. *(source: DI-769)*
- **Entry filter**: Chips for Preventive, Corrective, Damage repair, Inspection, Status change, Incident. *(source: contracts/satellite/maintenance.yaml#/components/schemas/AssetHistoryEntry)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Asset facts**: Purchased 12 Jan 2026, age 8 months, total rentals 184, rental hours 276, total revenue AED 11,840.00. *(source: screens/P08-venue-back-office.yaml#BO-580)*
- **Maintenance summary**: Preventive services 4, corrective repairs 2, damage repairs 3, total maintenance cost AED 1,480.00, total downtime 36 hours - as metric tiles. *(source: screens/P08-venue-back-office.yaml#BO-580)*
- **Asset economics**: Two bars "Lifetime revenue AED 11,840 vs maintenance cost AED 1,480 (12.5%)"; amber above 50%, red above 80% of acquisition cost (the retirement signal on BO-582). *(source: screens/P08-venue-back-office.yaml#BO-581 / screens/P08-venue-back-office.yaml#BO-582)*
- **Timeline**: Every work order, inspection, incident and status change in date order (12 Jan Activated, 15 Mar Preventive, 4 May Tyre repair, 18 Jul Customer damage, 8 Sep Brake repair), each opening its record; cursor-paged with Load more. *(source: screens/P08-venue-back-office.yaml#BO-581 / contracts/satellite/maintenance.yaml#getAssetHistory)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open an entry**: Opens the work order, inspection or incident it refers to. *(source: contracts/satellite/maintenance.yaml#/components/schemas/AssetHistoryEntry)*
- **Export**: A PDF of the history for an insurer or regulator, with the venue's header. *(source: contracts/satellite/maintenance.yaml#getAssetHistory / designer default)*
- **Consider retirement**: Opens BO-582 for this asset. *(source: screens/P08-venue-back-office.yaml#BO-582)*

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset maintenance history list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset maintenance history untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No asset maintenance history yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the asset maintenance history are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Pooled item (life jackets)**: Not available - pooled items have no individual history; the screen says so and links the product's counts. *(source: DI-744)*
- **Costs recorded in a different currency (vendor invoice in USD)**: Shown in the venue currency with the original amount on hover. *(source: designer default)*

#### Consistency with other screens

- Match `BO-069`: The History tab of the venue asset register is this timeline; same component and entry icons.
- Match `BO-506`: The profile's Maintenance tab is a short form of this screen.
- Match `BO-587`: Fleet analytics rows open here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
asset: BIKE-017
facts:
  purchased: 12 Jan 2026
  age: 8 months
  rentals: 184
  rentalHours: 276
  revenue: AED 11,840.00
summary:
  preventive: 4
  corrective: 2
  damage: 3
  cost: AED 1,480.00
  downtime: 36 h
timeline:
- 12 Jan - Activated
- 15 Mar - Preventive maintenance
- 04 May - Tyre repair
- 18 Jul - Customer damage
- 08 Sep - Brake repair (WO-2026-01501, AED 130.00)
```

#### Permissions

- `getAssetHistory` → `ASSET_VIEW` (read) · staff

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

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-580` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-580`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 12: Works in Asset Maintenance History & Lifecycle → Provide the complete maintenance history of an individual serialized rental asset. The original requirement specifically requires maintenance history tracking.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-580?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `ASSET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-581` Return-to-Service Inspection & Approval

**Ensure repaired equipment does not automatically become rentable when a technician clicks “Repair Complete.” This is one of the most important controls in Board 9.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_MANAGE`, `INSPECTION_SUBMIT`, `WORK_ORDER_VERIFY` (1 configure, 2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `workOrderId` (navigation), `assetId` (navigation) |
| Route | `/rentals/return-to-service-inspection-approval-bo-581` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The control that stops a repaired item becoming rentable just because the technician pressed "Repair complete": a return-to-service inspection against the item's checklist, a result, and a supervisor's approval, after which - and only after which - the item is safe for rental and availability is recalculated. The one thing to get right: two separate people and two separate steps (inspect, then approve and return), with the result in large unmistakable words (SAFE FOR RENTAL / REWORK REQUIRED / UNSAFE).

**Known correction pending (do not draw the wrong version)**

- **The inspection is not linked to the work order it checks** Why: SubmitInspectionRequest has templateId and assetId but no workOrderId; a rework inspection cannot be told from the first. *(source: contracts/satellite/maintenance.yaml#/components/schemas/SubmitInspectionRequest; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Result vocabulary differs** Why: Pack Pass, Rework required, Unsafe, Supervisor review; InspectionOutcome is passed, passedWithObservations, failed. *(source: screens/P08-venue-back-office.yaml#BO-581 / contracts/satellite/maintenance.yaml#/components/schemas/InspectionOutcome; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Gap note "nothing that can be drawn"** Why: Pack pages 116-117 give the checklist, results, approver and the SAFE FOR RENTAL outcome. *(source: screens/P08-venue-back-office.yaml#BO-581 / screens/P08-venue-back-office.yaml#BO-582; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The return to service itself (setAssetStatus inService with the inspection) is not bound (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is supervisor approval required for every rental item, or only where the plan or category says so (pack lists Supervisor review as one result)?** → Drawn default accepted: Required when the product's plan has "Supervisor must verify" on; otherwise the inspector's Pass returns the item. *(decided by Chinmay, 2026-10-02; DEC-440 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Form: Return to service** (modal, opened by *Return to service*; *Return to service* calls `setAssetStatus`, *Cancel* sends nothing)

**Collects what `setAssetStatus` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | select | required | — | In service · Out of service · Under maintenance · Awaiting parts · Retired · Disposed | — | — | `setAssetStatus` body |
| Reason `reason` | text area | required | — | min length 3; max length 1000 | — | — | `setAssetStatus` body |
| Inspection `inspectionId` | picker: choose an inspection | optional | — | — | shows names, sends the id | Required for return to service where the asset demands it. | `setAssetStatus` body |
| Raise work order `raiseWorkOrder` | toggle | optional | off | — | — | — | `setAssetStatus` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setAssetStatus` body |

Errors to draw in the form: 409 Return to service attempted without the inspection this asset category requires.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Inspection checklist**: The item's return-to-service checklist (Brake lever replaced, Brake cable checked, Brake function tested, Tyres checked, Frame inspected, Safety test completed) as pass/fail rows; safety-critical rows marked; a failed row requires a photo and note. *(source: screens/P08-venue-back-office.yaml#BO-581 / contracts/satellite/maintenance.yaml#/components/schemas/InspectionTemplate)*
- **Result**: Pass, Rework required, Unsafe as three large buttons; Rework and Unsafe need a note. Signature of the inspector at the end. *(source: screens/P08-venue-back-office.yaml#BO-581 / contracts/satellite/maintenance.yaml#submitInspection)*
- **Supervisor approval**: Shown after a Pass, for a different person - Approve return to service or Send back, with a note; approver name and time recorded. *(source: screens/P08-venue-back-office.yaml#BO-582 / contracts/satellite/maintenance.yaml#verifyWorkOrder)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Submit inspection (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Return to service (secondary button) | `setAssetStatus` PUT `/assets/{assetId}/status` | SetAssetStatusRequest | AssetStatusResult | 409 Return to service attempted without the inspection this asset category requires. | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Queue**: Items with Repair complete waiting for inspection, and inspected items waiting for approval, oldest first, with how long each has been unrentable. *(source: screens/P08-venue-back-office.yaml#BO-574 / contracts/satellite/maintenance.yaml#listWorkOrders)*
- **Result banner**: "SAFE FOR RENTAL - approved by Fatima Al Hashimi, 1 Oct 2026 11:18" in green; then "Available from 11:18 - Mountain bike availability recalculated". *(source: screens/P08-venue-back-office.yaml#BO-582 / screens/P08-venue-back-office.yaml#BO-583)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Submit inspection**: Records the inspection with the inspector; a failed safety-critical item keeps the item out of service automatically and raises rework. *(source: contracts/satellite/maintenance.yaml#submitInspection)*
- **Approve return to service**: Verifies the work order and returns the asset to service citing the inspection; refused for the person who did the repair. *(source: contracts/satellite/maintenance.yaml#verifyWorkOrder / contracts/satellite/maintenance.yaml#setAssetStatus)*
- **Rework required / Send back**: Reopens the same work order to the technician with the note (same history); the item stays out. *(source: screens/P08-venue-back-office.yaml#BO-581 / contracts/satellite/maintenance.yaml#verifyWorkOrder)*

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The return-to-service inspection approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the return-to-service inspection approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No return-to-service inspection approval yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the return-to-service inspection approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A required item was not answered; 409 Return to service attempted without the inspection this asset category requires. |

#### Edge cases to draw

- **Approver is the technician who did the repair**: Approve disabled with "You repaired this item - another supervisor must approve" (per R106). *(source: contracts/satellite/maintenance.yaml#verifyWorkOrder)*
- **Inspection done offline at the rental station**: The inspection queues and shows "Inspected on device 11:02 - waiting to sync"; approval needs the network. *(source: contracts/satellite/maintenance.yaml#submitInspection / contracts/satellite/maintenance.yaml#verifyWorkOrder)*
- **Item had future bookings during the repair**: After approval, the recalculated availability lists bookings that can now keep this item. *(source: screens/P08-venue-back-office.yaml#BO-583)*

#### Consistency with other screens

- Match `BO-030`: The venue verification queue is the same control; same Verify / Reject wording and evidence panel.
- Match `EMP-048`: Same inspection item component (pass/fail, safety tag, photo on fail, signature).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
item: BIKE-017
checklist:
- Brake lever replaced - Pass
- Brake cable checked - Pass
- Brake function tested - Pass
- Tyres checked - Pass
- Frame inspected - Pass
- Safety test completed - Pass
inspector: Rahul Menon, 11:02
approver: Fatima Al Hashimi, 1 Oct 2026 11:18
result: SAFE FOR RENTAL
```

#### Permissions

- `submitInspection` → `INSPECTION_SUBMIT` (operate) · staff
- `verifyWorkOrder` → `WORK_ORDER_VERIFY` (operate) · staff
- `setAssetStatus` → `ASSET_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.5.7 | Safety Audits - System shall support safety audits. | Maintenance & Safety Management | CONTRACTED | `submitInspection` |
| 17.4.6 | Work Order Approval - System shall support work order approvals. | Maintenance & Safety Management | CONTRACTED | `verifyWorkOrder` |
| 17.4.7 | Work Order Closure - System shall support work order closure workflows. | Maintenance & Safety Management | CONTRACTED | `verifyWorkOrder` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Serviced items return to service; retirement/write-off records the write-off value; maintenance AI view shows at-risk assets, upcoming maintenance cost and total spend. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-770)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-581` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-581`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 14: Works in Return-to-Service Inspection & Approval → Ensure repaired equipment does not automatically become rentable when a technician clicks “Repair Complete.” This is one of the most important controls in Board 9.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-581?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Submit inspection, Cancel, Return to service.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `ASSET_MANAGE`, `INSPECTION_SUBMIT`, `WORK_ORDER_VERIFY`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-582` Asset Retirement, Write-Off & Replacement Recommendation

**Manage assets that should no longer remain in the active rental fleet.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_MANAGE`, `ASSET_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/rentals/asset-retirement-write-off-replacement-recommendation-bo-582` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Taking a rental item out of the fleet for good - end of useful life, excessive maintenance cost, safety concern, repeated failure, total loss, obsolete, lost, management decision - through Recommendation > Review > Approval > Retire, with the economics in front of the approver and the record kept forever. The one thing to get right: retirement is a governed decision that names its consequences (future bookings affected, write-off value to finance) and never deletes the asset.

**Known correction pending (do not draw the wrong version)**

- **Retirement reason, write-off value and disposal proceeds cannot be recorded** Why: setAssetStatus takes status and free-text reason only; Asset has retiredOn and disposalProceeds but no operation writes them, so DI-770's write-off value is lost. *(source: contracts/satellite/maintenance.yaml#setAssetStatus / contracts/satellite/maintenance.yaml#/components/schemas/Asset / DI-770; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No approval step** Why: The pack's workflow is Recommendation > Review > Approval > Retire; setAssetStatus retires immediately for anyone with ASSET_MANAGE. *(source: screens/P08-venue-back-office.yaml#BO-583 / contracts/satellite/maintenance.yaml#setAssetStatus; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Future bookings affected are not reported** Why: AssetStatusResult reports products suspended and performances affected, not rental bookings that held the item. *(source: screens/P08-venue-back-office.yaml#BO-583 / contracts/satellite/maintenance.yaml#/components/schemas/AssetStatusResult; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Save asset status" label and gap note "nothing that can be drawn"** Why: The act is "Submit for retirement" / "Approve and retire"; pack pages 117-118 give reasons, economics and workflow. *(source: screens/P08-venue-back-office.yaml#BO-583 / screens/P08-venue-back-office.yaml#BO-582; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does a retirement need finance approval when the write-off value is above a threshold?** → Drawn default accepted: Draw one approver; show "Finance will be notified" on the confirm. *(decided by Chinmay, 2026-10-02; DEC-441 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Retirement reason**: The pack's eight reasons as a single choice; "Lost / not recovered" asks for the last booking. *(source: screens/P08-venue-back-office.yaml#BO-582)*
- **Write-off value**: Book value (from depreciation where recorded) prefilled; disposal proceeds in AED if sold or scrapped; both passed to finance. *(source: DI-770 / contracts/satellite/maintenance.yaml#/components/schemas/Asset)*
- **Replacement**: Optional "Replace with" - creates a purchase request for the same product; not required to retire. *(source: screens/P08-venue-back-office.yaml#BO-583 / designer default)*
- **Approval**: Submitting sends for approval to a person other than the requester; the approver sees the same case and approves or rejects with a note. *(source: screens/P08-venue-back-office.yaml#BO-583)*

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save asset status (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Case for retiring**: Purchase cost AED 2,500, lifetime revenue AED 8,920, maintenance cost AED 2,180 (87% of purchase), repairs 12, downtime 18 days, condition Poor - tiles, with the repair timeline below. *(source: screens/P08-venue-back-office.yaml#BO-582 / contracts/satellite/maintenance.yaml#getAssetHistory)*
- **AI recommendation**: "Maintenance cost has reached 87% of acquisition cost; failure frequency 3.2 times the fleet average - consider retirement" with the reason shown and an explicit "Start retirement" by a person. *(source: screens/P08-venue-back-office.yaml#BO-582 / DI-772)*
- **Consequences**: Before approval - future bookings that held this item (to be swapped), open work orders on it, and "History kept; removed from availability permanently". *(source: screens/P08-venue-back-office.yaml#BO-583 / contracts/satellite/maintenance.yaml#/components/schemas/AssetStatusResult)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Submit for approval**: Records the recommendation and reason; the item stays as it is until approved. *(source: screens/P08-venue-back-office.yaml#BO-583)*
- **Approve and retire**: Sets the asset to Retired with the reason (Disposed later when it physically leaves); confirm names the bookings and open work orders affected (per VO-R16). *(source: contracts/satellite/maintenance.yaml#setAssetStatus)*

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset retirement write-off list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset retirement write-off untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No asset retirement write-off yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the asset retirement write-off are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Return to service attempted without the inspection this asset category requires. |

#### Edge cases to draw

- **Open work orders on the item**: Listed in the confirm; each must be cancelled or closed (No longer applicable) before retirement completes. *(source: contracts/satellite/maintenance.yaml#closeWorkOrder / screens/P08-venue-back-office.yaml#BO-069)*
- **Item later found (was lost)**: A retired asset can be reinstated by a manager with a reason; its history shows both events. *(source: designer default)*

#### Consistency with other screens

- Match `BO-069`: Retire on the venue asset register uses the same confirm and reason list.
- Match `BO-580`: The economics tiles are the same figures as the history screen.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
asset: BIKE-031
case:
  purchase: AED 2,500.00
  revenue: AED 8,920.00
  maintenance: AED 2,180.00
  repairs: 12
  downtime: 18 days
  condition: Poor
recommendation: Maintenance cost 87% of acquisition cost; failures 3.2 times fleet average
reason: Excessive maintenance cost
writeOff: AED 310.00 book value
requestedBy: Rahul Menon
approver: Ahmed Al Mansoori
```

#### Permissions

- `setAssetStatus` → `ASSET_MANAGE` (configure) · staff
- `getAssetHistory` → `ASSET_VIEW` (read) · staff

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

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Serviced items return to service; retirement/write-off records the write-off value; maintenance AI view shows at-risk assets, upcoming maintenance cost and total spend. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-770)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-582` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-582`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 16: Works in Asset Retirement, Write-Off & Replacement Recommendation → Manage assets that should no longer remain in the active rental fleet.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-582?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save asset status, Cancel.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `ASSET_MANAGE`, `ASSET_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-583` Maintenance Intelligence & Predictive AI

**Use AI to move TICVAI from reactive maintenance toward predictive maintenance. This is where I recommend making the module significantly stronger than the original matrix.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/maintenance-intelligence-predictive-ai-bo-583` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Maintenance intelligence for the rental fleet: a health dashboard (assets at risk, predicted failures, repeat failures, high-cost assets, downtime and its effect on availability, MTBF and MTTR) and a feed of AI recommendations - service this bike within 10 rental hours, move eight services from Saturday to Monday, review this brake supplier, replace rather than repair. The one thing to get right: every recommendation is advisory, shows its evidence, and only a person turns it into a scheduled job or a retirement case.

**Known correction pending (do not draw the wrong version)**

- **The nine dashboard measures are drawn as columns of a data table with a detail panel** Why: They are KPIs and charts (per VO-R02); the pack's "Maintenance Health Dashboard" is tiles. *(source: screens/P08-venue-back-office.yaml#BO-583; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Only getDueMaintenance is bound; no operation returns predictions, MTBF, MTTR or recommendations** Why: Due plans are not predictions. The screen needs a maintenance analytics read and a recommendation feed with accept/dismiss recorded. *(source: contracts/satellite/maintenance.yaml#getDueMaintenance / DI-770 / DI-772; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Detail panel headings taken from unrelated pack text ("Every 30 Days", "Every 50 Rentals")** Why: Those lines are the trigger architecture on the same page, not this record's sections. *(source: screens/P08-venue-back-office.yaml#BO-583; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the capacity-aware scheduling suggestion in the first release (it needs rental demand forecasts), or reporting only (DI-772)?** → Drawn default accepted: Draw the card type; mark it "Needs demand forecast" greyed when unavailable. *(decided by Chinmay, 2026-10-02; DEC-442 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Within days | number field (days) | 14 | — | `getDueMaintenance` ?withinDays |
| From | date and time picker | — | — | `getDueMaintenance` ?from |
| To | date and time picker | — | — | `getDueMaintenance` ?to |
| Category | picker: choose a category | — | — | `getDueMaintenance` ?categoryId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Period and scope**: Last 30 / 90 / 365 days and product filter; venue from the top bar. *(source: screens/P08-venue-back-office.yaml#BO-583)*
- **Dismiss reason**: Dismissing a recommendation asks why (Already planned, Not accurate, Not now) so the suggestions improve; nothing else is typed here. *(source: designer default)*

#### Outputs: what the screen shows and produces

**Shown**

**Every maintenance intelligence predictive** (data table)

| Shows | Format | Notes |
|---|---|---|
| Assets at risk | text | not in the schema: `Assets at Risk` |
| Predicted failures | text | not in the schema: `Predicted Failures` |
| Upcoming preventive maintenance | text | not in the schema: `Upcoming Preventive Maintenance` |
| Repeat failures | text | not in the schema: `Repeat Failures` |
| High maintenance cost assets | text | not in the schema: `High Maintenance Cost Assets` |
| Downtime by product | text | not in the schema: `Downtime by Product` |
| Maintenance impact on availability | text | not in the schema: `Maintenance Impact on Availability` |
| Mean time between failures | text | not in the schema: `Mean Time Between Failures` |
| Mean time to repair | text | not in the schema: `Mean Time to Repair` |

**The selected maintenance intelligence predictive** (detail panel): The pack groups this record's detail under its own headings: “BIKE-018”, “Instead of simply saying”, “Every 30 Days”, “Every 50 Rentals”, “Every 100 Rental Hours”, “Whichever Happens First”.

| Shows | Format | Notes |
|---|---|---|
| Assets at risk | text | not in the schema: `Assets at Risk` |
| Predicted failures | text | not in the schema: `Predicted Failures` |
| Upcoming preventive maintenance | text | not in the schema: `Upcoming Preventive Maintenance` |
| Repeat failures | text | not in the schema: `Repeat Failures` |
| High maintenance cost assets | text | not in the schema: `High Maintenance Cost Assets` |
| Downtime by product | text | not in the schema: `Downtime by Product` |
| Maintenance impact on availability | text | not in the schema: `Maintenance Impact on Availability` |
| Mean time between failures | text | not in the schema: `Mean Time Between Failures` |
| Mean time to repair | text | not in the schema: `Mean Time to Repair` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Health tiles**: Assets at risk, Predicted failures (next 30 days), Upcoming preventive maintenance, Repeat failures, High maintenance cost assets, Mean time between failures (days), Mean time to repair (hours) as metric tiles; Downtime by product and Maintenance impact on availability as small bar charts. Never as columns of one table. *(source: screens/P08-venue-back-office.yaml#BO-583 / DI-770)*
- **Spend tiles**: Upcoming maintenance cost (next 30 days, AED) and total maintenance spend (period), as the client asked. *(source: DI-770)*
- **Recommendation cards**: One card per suggestion with type (Predictive service, Capacity-aware scheduling, Failure pattern, Replace vs repair), the evidence lines ("94 rental hours since last service; inspection scores declining; similar bikes need brake service at 95-110 h"), the recommendation in bold, and the line "Advisory - needs approval". *(source: screens/P08-venue-back-office.yaml#BO-583)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Schedule (on a predictive or capacity card)**: Opens the maintenance calendar (BO-576) with the jobs pre-placed in the suggested window (Monday 09:00-13:00); nothing is saved until the planner confirms there. *(source: screens/P08-venue-back-office.yaml#BO-583 / DI-772 / screens/P08-venue-back-office.yaml#BO-576)*
- **Start retirement (on a replace-vs-repair card)**: Opens BO-582 with the economics filled in. *(source: screens/P08-venue-back-office.yaml#BO-582)*
- **Review (on a failure-pattern card)**: Opens the list of the related repairs and the plan for the product (BO-575) to change its frequency. *(source: screens/P08-venue-back-office.yaml#BO-583 / screens/P08-venue-back-office.yaml#BO-575)*
- **Dismiss**: Hides the card with the reason recorded; dismissed cards are viewable under "Dismissed". *(source: TRACKER Actions row 324 / DI-924)*

**Data it reads**: `getDueMaintenance` (onLoad, Predictive maintenance)

**Where the user goes next**

- → `BO-574` Maintenance Command Center: *Back to Maintenance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The maintenance intelligence predictive list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the maintenance intelligence predictive untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No maintenance intelligence predictive yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the maintenance intelligence predictive are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **AI not configured or not enough history**: Tiles that are plain arithmetic (MTBF, MTTR, spend) still show; the recommendation feed says "Not enough history yet - 3 months of repairs needed" instead of empty cards. *(source: contracts/satellite/maintenance.yaml#suggestWorkOrderAssignee)*
- **A suggestion would break a rule (schedule on a day the workshop is closed)**: Not shown as available (per VO-R11). *(source: TRACKER Actions row 324 / DI-924)*

#### Consistency with other screens

- Match `BO-574`: The command centre's AI alert links into this feed; same card style.
- Match `BO-587`: Repeat-failure and high-cost assets use the same asset health labels (Excellent, Good, Poor).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  atRisk: 6
  predictedFailures: 4
  upcomingPreventive: 12
  repeatFailures: 3
  highCost: 2
  mtbf: 41 days
  mttr: 3.2 h
  upcoming30dCost: AED 4,860.00
  spend90d: AED 18,240.00
cards:
- 'Predictive service - BIKE-018: 94 rental hours since service; schedule within the next 10 rental hours.'
- 'Capacity-aware - Saturday utilisation 94%, Monday 38%: schedule 8 preventive jobs Monday 09:00-13:00.'
- 'Failure pattern - 7 of 12 recent Mountain Bike repairs involved front brakes: review frequency and supplier.'
- 'Replace vs repair - BIKE-031: next repair AED 420, value AED 650, 71% failure risk in 90 days: replace.'
```

#### Permissions

- `getDueMaintenance` → `ASSET_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.2.4 | Automated Work Order Generation - System shall automatically generate preventive maintenance work orders. | Maintenance & Safety Management | CONTRACTED | `getDueMaintenance` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- In rentals AI's practical role is reporting and maintenance-scheduling recommendations; day-to-day rental operations stay staff-managed. *(agreed · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-772)*
- Serviced items return to service; retirement/write-off records the write-off value; maintenance AI view shows at-risk assets, upcoming maintenance cost and total spend. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-770)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-583` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS124 Rental Management Board 9.dc.html#bo-583`
- Workshop pack: Rental_Management.pdf board 9
- Flow F205 *Rental Management board 9: Maintenance Command Center*, step 18: Works in Maintenance Intelligence & Predictive AI → Use AI to move TICVAI from reactive maintenance toward predictive maintenance. This is where I recommend making the module significantly stronger than the original matrix.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-583?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-574`.
- [ ] Every gated control is gated: `ASSET_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**15 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"attachWorkOrderEvidence": {"method":"POST","path":"/work-orders/{workOrderId}/attachments","contract":"maintenance","summary":"Photo, video, document, note or signature","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrderAttachment"},
"completeWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/complete","contract":"maintenance","summary":"Complete a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"createMaintenancePlan": {"method":"POST","path":"/maintenance-plans","contract":"maintenance","summary":"Create a planned maintenance schedule","permission":"ASSET_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MaintenancePlan","responds":"MaintenancePlan"},
"createStockReservation": {"method":"POST","path":"/stock-reservations","contract":"inventory","summary":"Reserve stock for a work order or another need","permission":"PROCUREMENT_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"InventoryStockReservation","responds":"InventoryStockReservation"},
"createVendorServiceRequest": {"method":"POST","path":"/vendor-service-requests","contract":"maintenance","summary":"Engage an outside vendor on a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VendorServiceRequest","responds":"VendorServiceRequest"},
"createWorkOrder": {"method":"POST","path":"/work-orders","contract":"maintenance","summary":"Raise a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateWorkOrderRequest","responds":"WorkOrder"},
"getAssetHistory": {"method":"GET","path":"/assets/{assetId}/history","contract":"maintenance","summary":"Service history","permission":"ASSET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getDueMaintenance": {"method":"GET","path":"/maintenance-plans/due","contract":"maintenance","summary":"Planned tasks due or overdue","permission":"ASSET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"withinDays","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null}],"requestBody":null,"responds":"DueMaintenanceTask"},
"getWorkOrder": {"method":"GET","path":"/work-orders/{workOrderId}","contract":"maintenance","summary":"Read a work order","permission":"WORK_ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WorkOrderDetail"},
"getWorkOrderPriorityPolicy": {"method":"GET","path":"/work-order-priority-policy","contract":"maintenance","summary":"Read how a fault's priority is scored","permission":"WORK_ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WorkOrderPriorityPolicy"},
"listMaintenancePlans": {"method":"GET","path":"/maintenance-plans","contract":"maintenance","summary":"List planned maintenance schedules","permission":"ASSET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listStockReservations": {"method":"GET","path":"/stock-reservations","contract":"inventory","summary":"Soft holds on stock","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"sourceType","in":"query","required":null},{"name":"sourceId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVendorServiceRequests": {"method":"GET","path":"/vendor-service-requests","contract":"maintenance","summary":"Requests sent to outside vendors","permission":"WORK_ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workOrderId","in":"query","required":null},{"name":"supplierId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkOrders": {"method":"GET","path":"/work-orders","contract":"maintenance","summary":"List work orders","permission":"WORK_ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assignedToPrincipalId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"assetId","in":"query","required":null},{"name":"overdueOnly","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"pauseWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/pause","contract":"maintenance","summary":"Stopped, and why","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"recordWorkOrderParts": {"method":"POST","path":"/work-orders/{workOrderId}/parts","contract":"maintenance","summary":"Record parts consumed","permission":"WORK_ORDER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrderDetail"},
"recordWorkOrderTime": {"method":"POST","path":"/work-orders/{workOrderId}/time","contract":"maintenance","summary":"Start, pause or stop work","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"releaseStockReservation": {"method":"POST","path":"/stock-reservations/{stockReservationId}/release","contract":"inventory","summary":"Give reserved stock back","permission":"PROCUREMENT_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"InventoryStockReservation"},
"resumeWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/resume","contract":"maintenance","summary":"Back to work","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"setAssetStatus": {"method":"PUT","path":"/assets/{assetId}/status","contract":"maintenance","summary":"Take an asset out of service or return it","permission":"ASSET_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetAssetStatusRequest","responds":"AssetStatusResult"},
"setWorkOrderPriorityPolicy": {"method":"PUT","path":"/work-order-priority-policy","contract":"maintenance","summary":"Set how a fault's priority is scored","permission":"WORK_ORDER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkOrderPriorityPolicy","responds":"WorkOrderPriorityPolicy"},
"startWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/start","contract":"maintenance","summary":"Work has begun","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"submitInspection": {"method":"POST","path":"/inspections","contract":"maintenance","summary":"Submit a completed inspection","permission":"INSPECTION_SUBMIT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SubmitInspectionRequest","responds":"InspectionResult"},
"suggestWorkOrderAssignee": {"method":"GET","path":"/work-orders/{workOrderId}/assignee-suggestions","contract":"maintenance","summary":"Who should take this work order, ranked","permission":"WORK_ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"updateMaintenancePlan": {"method":"PATCH","path":"/maintenance-plans/{planId}","contract":"maintenance","summary":"Amend or suspend a plan","permission":"ASSET_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MaintenancePlan"},
"updateVendorServiceRequest": {"method":"PATCH","path":"/vendor-service-requests/{vendorServiceRequestId}","contract":"maintenance","summary":"Move a vendor request along","permission":"WORK_ORDER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"VendorServiceRequest"},
"updateWorkOrder": {"method":"PATCH","path":"/work-orders/{workOrderId}","contract":"maintenance","summary":"Assign, reprioritise or amend","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"verifyWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/verify","contract":"maintenance","summary":"Supervisor verification","permission":"WORK_ORDER_VERIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"}
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
"AssetStatusResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["asset","downstreamEffects"],"properties":{"asset":{"$ref":"#/components/schemas/Asset"},"downstreamEffects":{"type":"object","description":"What else changed. Surfaced so the person taking a ride out of service sees the commercial consequence at the moment they do it.\n","properties":{"productsSuspended":{"type":"array","items":{"type":"string","format":"uuid"}},"accessPointBlocked":{"type":"boolean"},"performancesAffected":{"type":"integer"},"workOrderId":{"type":"string","format":"uuid","nullable":true}}}}},
"CreateWorkOrderRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","title","venueId","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"title":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":5000},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"kind":{"allOf":[{"$ref":"#/components/schemas/WorkOrderKind"}],"default":"corrective"},"priority":{"allOf":[{"$ref":"#/components/schemas/WorkOrderPriority"}],"description":"**Optional since 29 September** (M17-01). Sent, it is `manual` and wins. Absent, the asset's `priorityOverride` applies, and failing that the venue's `WorkOrderPriorityPolicy` scores the fault.\n"},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","maxItems":10,"items":{"type":"string"},"description":"Skills the job needs, as qualification codes; `suggestWorkOrderAssignee` ranks by them (M17-13)."},"categoryId":{"type":"string","format":"uuid"},"assignedToPrincipalId":{"type":"string","format":"uuid"},"dueAt":{"type":"string","format":"date-time"},"attachmentRefs":{"type":"array","description":"Photo-first. Expected at creation, not added later from memory.","items":{"type":"string"}},"takeAssetOutOfService":{"type":"boolean","default":false,"description":"Raise and immediately suspend the asset. For a fault found on a live ride, the two are one action.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"DueMaintenanceTask": {"x-ticvai-persistence":"none — computed","type":"object","required":["planId","assetId","assetName","dueAt","isOverdue","criticality"],"properties":{"planId":{"type":"string","format":"uuid"},"planName":{"type":"string"},"assetId":{"type":"string","format":"uuid"},"assetName":{"type":"string"},"criticality":{"$ref":"#/components/schemas/AssetCriticality"},"dueAt":{"type":"string","format":"date-time"},"isOverdue":{"type":"boolean"},"daysOverdue":{"type":"integer"},"triggeredBy":{"type":"string","enum":["interval","usage"]},"workOrderId":{"type":"string","format":"uuid","nullable":true}}},
"Inspection": {"x-ticvai-persistence":"maintenance.inspection","type":"object","required":["id","templateId","venueId","outcome","performedByPrincipalId","performedAt"],"properties":{"id":{"type":"string","format":"uuid"},"templateId":{"type":"string","format":"uuid"},"templateName":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"outcome":{"$ref":"#/components/schemas/InspectionOutcome"},"failedItemCount":{"type":"integer"},"failedSafetyCriticalCount":{"type":"integer"},"performedByPrincipalId":{"type":"string","format":"uuid","description":"An inspection nobody signed is not an inspection."},"performedAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true},"retainUntil":{"type":"string","format":"date","nullable":true}}},
"InspectionItem": {"x-ticvai-persistence":"maintenance.inspection_item","type":"object","description":"**One answer to one question, which the API has always accepted and never stored.** `SubmitInspectionRequest.responses[]` takes a key, a value, a pass flag, a note and attachments; the only persistence ever claimed for them was `maintenance.inspection_response`, a table that does not exist.\nSo `maintenance.inspection_template_item` held the questions, `maintenance.inspection` held `failedItemCount` and `failedSafetyCriticalCount`, and **which check failed was accepted over the wire and dropped** — on a record that takes an asset out of service.\nReturned on `InspectionResult`, not on `Inspection`: `listInspections` returns the latter in a list, and twenty item rows per inspection on a list screen is the wrong trade. The counts stay for exactly that reason.\n","required":["id","inspectionId","itemKey"],"properties":{"id":{"type":"string","format":"uuid"},"inspectionId":{"type":"string","format":"uuid"},"templateItemId":{"type":"string","format":"uuid","nullable":true,"description":"**Nullable because a template changes and an inspection does not.** An answer recorded against an item that was later removed still has to be readable, so the key below is the durable record and this is the live link.\n"},"itemKey":{"type":"string","maxLength":120,"description":"The template item's `key`, copied at submission and never updated."},"label":{"type":"string","nullable":true,"description":"The question as it was asked, copied at submission. **A template reworded next season must not silently reword last season's inspection.**\n"},"value":{"nullable":true,"description":"Whatever the item's `kind` calls for — a boolean, a number, a string."},"passed":{"type":"boolean","nullable":true,"description":"Null where the item is informational rather than pass or fail."},"isSafetyCritical":{"type":"boolean","default":false,"description":"Copied from the template item at submission, for the same reason as `label`: it is what makes `failedSafetyCriticalCount` reproducible, and the template can change.\n"},"note":{"type":"string","maxLength":1000,"nullable":true},"attachmentAssetIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"**A deliberate array, and the same exception as `workforce.sync_conflict.affectedAssignmentIds`**: evidence attached to this answer at the moment it was recorded. It is never queried from the other end — nobody asks which inspection items reference a photograph — and it must not change when an asset library is reorganised.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"InspectionResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["inspection","consequences"],"properties":{"inspection":{"$ref":"#/components/schemas/Inspection"},"items":{"type":"array","description":"**The answers, which had nowhere to live until 20 September.** A failed safety-critical item takes an asset out of service and `consequences` below says it happened; this says which check caused it.\n","items":{"$ref":"#/components/schemas/InspectionItem"}},"consequences":{"type":"object","description":"What the submission triggered. A failed safety-critical item takes the asset out of service without waiting for anyone to decide.\n","properties":{"assetTakenOutOfService":{"type":"boolean"},"workOrdersRaised":{"type":"array","items":{"type":"string","format":"uuid"}},"productsSuspended":{"type":"array","items":{"type":"string","format":"uuid"}},"escalatedToPrincipalId":{"type":"string","format":"uuid","nullable":true}}}}},
"InventoryStockReservation": {"type":"object","x-ticvai-persistence":"inventory.stock_reservation","description":"**Taken from the backend workbook, 20 September.** Temporarily reserves stock for an order or operational requirement so it cannot be allocated elsewhere.","required":["itemId","locationId","quantity","sourceType","sourceId","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"itemId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"quantity":{"type":"number","exclusiveMinimum":0},"sourceType":{"$ref":"#/components/schemas/StockReservationSourceType"},"sourceId":{"type":"string","format":"uuid","description":"The id of what the stock is reserved for: a work order, a rental agreement or an order. A uuid, as every id is (ADR-0056); it was text from 29 September to 30 September because a work order id was then 26-character text (M17-02)."},"status":{"type":"string","enum":["active","consumed","released","expired"],"readOnly":true},"expiresAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"releasedAt":{"type":"string","format":"date-time","nullable":true}}},
"MaintenancePlan": {"x-ticvai-persistence":"maintenance.preventive_plan","type":"object","required":["id","name","assetId","taskTemplate"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":200},"assetId":{"type":"string","format":"uuid"},"assetCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"Applies to every asset in the category rather than one."},"intervalDays":{"type":"integer","nullable":true,"description":"Elapsed-time trigger."},"usageInterval":{"type":"number","nullable":true,"description":"Usage trigger — cycles, hours, kilometres. **Whichever comes first** when both are set. A ride serviced every three months or ten thousand cycles is one plan.\n"},"leadTimeDays":{"type":"integer","default":7,"description":"How far ahead the work order is generated, so parts can be ordered before the job is already late.\n"},"taskTemplate":{"type":"object","required":["title","priority"],"properties":{"title":{"type":"string"},"description":{"type":"string"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"estimatedMinutes":{"type":"integer"},"inspectionTemplateId":{"type":"string","format":"uuid"},"requiredPartIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},"lastCompletedAt":{"type":"string","format":"date-time","nullable":true},"nextDueAt":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ResolutionCode": {"type":"string","enum":["repaired","partReplaced","adjusted","cleaned","noFaultFound","referredExternal","replaced","deferred"]},
"SetAssetStatusRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["status","reason","recordedAt"],"properties":{"status":{"$ref":"#/components/schemas/AssetStatus"},"reason":{"type":"string","minLength":3,"maxLength":1000},"inspectionId":{"type":"string","format":"uuid","nullable":true,"description":"Required for return to service where the asset demands it."},"raiseWorkOrder":{"type":"boolean","default":false},"recordedAt":{"type":"string","format":"date-time"}}},
"StockReservationSourceType": {"type":"string","enum":["workOrder","rentalAgreement","order","transfer","other"],"description":"What a stock reservation is for (decided 17 September, M17-02; `rentalAgreement` is the existing use from `rental.agreement_item`)."},
"SubmitInspectionRequest": {"x-ticvai-persistence":"maintenance.inspection + maintenance.inspection_item","type":"object","required":["id","templateId","venueId","responses","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"templateId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"responses":{"type":"array","minItems":1,"items":{"type":"object","required":["key","value"],"properties":{"key":{"type":"string"},"value":{},"passed":{"type":"boolean","nullable":true},"note":{"type":"string","maxLength":1000},"attachmentRefs":{"type":"array","items":{"type":"string"}}}}},"signatureRef":{"type":"string","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"VendorServiceRequest": {"x-ticvai-persistence":"maintenance.vendor_service_request","type":"object","description":"**An outside vendor engaged on a work order** (decided 17 September, M17-13). The supplier is an `inventory.supplier`.\n","required":["workOrderId","supplierId","scope"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","readOnly":true},"workOrderId":{"type":"string","format":"uuid"},"supplierId":{"type":"string","format":"uuid"},"scope":{"type":"string","maxLength":2000,"description":"What the vendor is asked to do."},"status":{"allOf":[{"$ref":"#/components/schemas/VendorServiceRequestStatus"}],"default":"draft"},"vendorReference":{"type":"string","maxLength":100,"nullable":true},"quotedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"finalCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scheduledVisitAt":{"type":"string","format":"date-time","nullable":true},"note":{"type":"string","maxLength":1000,"nullable":true},"raisedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"VendorServiceRequestStatus": {"type":"string","enum":["draft","sent","accepted","scheduled","completed","cancelled"]},
"WorkOrder": {"x-ticvai-persistence":"maintenance.work_order","x-ticvai-retired-columns":["is_overdue"],"type":"object","required":["id","workOrderNumber","title","venueId","status","priority","kind","createdAt"],"properties":{"downtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"},"rootCause":{"type":"string","nullable":true,"enum":["wearAndTear","operatorError","guestDamage","manufacturingDefect","environmental","softwareFault","powerFailure","deferredMaintenance","unknown"],"description":"**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"},"rootCauseNote":{"type":"string","nullable":true},"escalatedAt":{"type":"string","format":"date-time","nullable":true},"escalationLevel":{"type":"integer","default":0,"description":"**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"},"id":{"type":"string","format":"uuid"},"workOrderNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"title":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"assetName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"},"status":{"$ref":"#/components/schemas/WorkOrderStatus"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"priorityScore":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"readOnly":true,"description":"The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."},"prioritySource":{"type":"string","enum":["scored","assetOverride","manual"],"readOnly":true,"description":"Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","items":{"type":"string"},"description":"Skills the job needs (M17-13)."},"kind":{"$ref":"#/components/schemas/WorkOrderKind"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"raisedByPrincipalId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"},"locationDescription":{"type":"string","maxLength":500,"nullable":true,"description":"Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"},"elapsedMinutes":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"},"isTimerRunning":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"},"dueAt":{"type":"string","format":"date-time","nullable":true},"isOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"},"requiresVerification":{"type":"boolean"},"sourcePlanId":{"type":"string","format":"uuid","nullable":true},"sourceInspectionId":{"type":"string","format":"uuid","nullable":true},"sourceIncidentId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrderAssigneeSuggestion": {"x-ticvai-persistence":"none — computed on read","type":"object","required":["principalId","rank"],"properties":{"principalId":{"type":"string","format":"uuid"},"name":{"type":"string"},"rank":{"type":"integer","minimum":1},"hasAllQualifications":{"type":"boolean"},"missingQualificationCodes":{"type":"array","items":{"type":"string"}},"onShift":{"type":"boolean","description":"On shift now or before the work order is due."},"openWorkOrderCount":{"type":"integer"}}},
"WorkOrderAttachment": {"type":"object","x-ticvai-persistence":"maintenance.work_order_attachment","required":["id","workOrderId","kind","capturedAt"],"properties":{"id":{"type":"string","format":"uuid"},"workOrderId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["photo","video","document","note","signature"]},"assetRef":{"type":"string","format":"uuid","nullable":true},"text":{"type":"string","nullable":true},"stage":{"type":"string","enum":["before","during","after","signOff"],"nullable":true},"capturedByPrincipalId":{"type":"string","format":"uuid"},"capturedAt":{"type":"string","format":"date-time","description":"Device time. **Distinct from when it synced** — a photo taken at 09:14 in a basement and uploaded at 11:40 is evidence of the first, not the second.\n"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrderDetail": {"x-ticvai-persistence":"maintenance.work_order","allOf":[{"$ref":"#/components/schemas/WorkOrder"},{"type":"object","properties":{"description":{"type":"string","nullable":true},"resolution":{"type":"string","nullable":true},"resolutionCode":{"$ref":"#/components/schemas/ResolutionCode"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"timeEntries":{"type":"array","items":{"type":"object","properties":{"action":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"pauseReason":{"type":"string","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}}},"parts":{"type":"array","items":{"type":"object","properties":{"inventoryItemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"quantity":{"type":"number"},"reservedQuantity":{"type":"number","description":"Still reserved for this work order and not yet issued (M17-02)."},"cost":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"labourCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"partsCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","x-ticvai-column":"net_cost_amount"},"completedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who called `completeWorkOrder`. **What `verifyWorkOrder` compares against** — the verifier may not be the technician who completed the work, and the assignee is not necessarily that person.\n"},"followUpRequired":{"type":"boolean","default":false},"followUpNote":{"type":"string","maxLength":1000,"nullable":true},"verificationOutcome":{"type":"string","enum":["verified","rejected"],"nullable":true,"description":"The latest `verifyWorkOrder` outcome."},"verificationNote":{"type":"string","maxLength":1000,"nullable":true},"verifiedAt":{"type":"string","format":"date-time","nullable":true},"verifiedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"cancelReason":{"type":"string","enum":["raisedInError","duplicate","superseded","noLongerRequired"],"nullable":true},"cancelNote":{"type":"string","maxLength":300,"nullable":true},"supersededByWorkOrderId":{"type":"string","format":"uuid","nullable":true,"description":"Set by `cancelWorkOrder` where the reason is `superseded`."},"cancelledAt":{"type":"string","format":"date-time","nullable":true},"closeOutcome":{"type":"string","enum":["completedAndVerified","notReproducible","supersededByReplacement","noLongerApplicable","duplicate"],"nullable":true},"closeNote":{"type":"string","maxLength":500,"nullable":true},"duplicateOfWorkOrderId":{"type":"string","format":"uuid","nullable":true,"description":"Set by `closeWorkOrder` where the outcome is `duplicate`."},"closedAt":{"type":"string","format":"date-time","nullable":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true}}}]},
"WorkOrderFaultAssessment": {"x-ticvai-persistence":"none — columns on maintenance.work_order","type":"object","description":"What the person raising a fault says about it, which the priority score reads (M17-01).","properties":{"safetyRisk":{"type":"boolean","default":false},"guestImpact":{"type":"string","enum":["none","degraded","closed"],"default":"none"}}},
"WorkOrderKind": {"type":"string","enum":["corrective","planned","inspectionFollowUp","incidentCorrective","improvement"]},
"WorkOrderPriority": {"type":"string","enum":["low","normal","high","urgent","emergency"]},
"WorkOrderPriorityPolicy": {"x-ticvai-persistence":"maintenance.priority_scoring_model","type":"object","description":"**How a corrective fault's priority is scored** (decided 17 September, M17-01). One per venue. The score is 0 to 100: each weight times its factor, where safety is the fault's `faultAssessment.safetyRisk`, guest operations is `faultAssessment.guestImpact` (and whether the asset has a linked access point), revenue is whether the asset has linked products, and criticality is the asset's `criticality`. The band the score falls in is the priority. **An asset's `priorityOverride` wins over the score**, and a priority a person sets wins over both.\n","required":["weights","bands"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","readOnly":true},"weights":{"type":"object","required":["safety","guestOperations","revenue","criticality"],"properties":{"safety":{"type":"integer","minimum":0,"maximum":100},"guestOperations":{"type":"integer","minimum":0,"maximum":100},"revenue":{"type":"integer","minimum":0,"maximum":100},"criticality":{"type":"integer","minimum":0,"maximum":100}}},"bands":{"type":"array","minItems":1,"maxItems":5,"description":"Highest first. A score at or above `minScore` takes `priority`.","items":{"type":"object","required":["minScore","priority"],"properties":{"minScore":{"type":"integer","minimum":0,"maximum":100},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"}}}},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"updatedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"nullable":true}}},
"WorkOrderStatus": {"type":"string","enum":["open","assigned","inProgress","paused","awaitingParts","completed","verified","closed","cancelled"]}
}
```
