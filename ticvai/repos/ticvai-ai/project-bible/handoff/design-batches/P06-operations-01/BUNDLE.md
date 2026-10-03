# P06-operations-01 — P06 · Operations (1 of 5)

**10 screens · 47 operations · 49 schemas · 19 permissions**

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

- **Every control that can be refused must be gated.** 19 permissions apply here:
  `ACCESS_OVERRIDE, ACCESS_VALIDATE, INCIDENT_MANAGE, INCIDENT_REPORT, INCIDENT_VIEW, MAINTENANCE_APPROVE, MAINTENANCE_EXECUTE, OVERSHORT_ACCEPT, PROCUREMENT_REQUEST, PRODUCT_VIEW, REPORT_VIEW_OWN, REPORT_VIEW_WORKSTATION`…. A control nobody can use must say so,
  not sit enabled and fail.
- **23 of these operations work offline**: acceptWorkOrder, attachWorkOrderEvidence, completeWorkOrder, createWorkOrder, getCurrentSession, getCurrentShift, getShift, getWorkOrder
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

### Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management)

Platform Foundation is everything the apps stand on. Five apps each have one door: the guest app and website (WEB-016, GST-042: a six-digit code to email or mobile, a password, Apple or Google, UAE Pass; never enterprise SSO), the till (POS-000: employee number and PIN, recent operators as tiles; the kitchen display is the same app), the staff handheld and scanner (EMP-001, SCN-001), Venue Management (SUP-001, the single door for the back office P08, the CMS P13, analytics P16 and the support desk P12) and TICVAI Control (ADM-001 for TICVAI's own platform operators, PTR-001 for partner users; the developer portal P14 and the sign-up P17 belong to this app too). A second factor is required by permission, not by role or device: ROLE_MANAGE, LEDGER_APPROVE and every PLATFORM_* permission, plus any the tenant adds; so a cashier never sees it and a platform operator always does. The factor is an authenticator app with an emailed code as fallback; five wrong codes lock step-up for the lockout minutes, never permanently. Guests get two-step verification only at a venue that switched it on. One person holds one session per workstation: a second sign-in is refused and only a supervisor ends the other session. Several roles mean a role prompt; one role goes straight in. The workstation decides the Sale Board, hardware and till identity, never what a person may do. Sensitive actions (refund approval, journal approval, credential reset, partner credit, commission rules, opening a platform-staff grant and 17 more) demand a fresh step-up on the operation itself, asked in place in the action's confirmation; the tenant may raise the strength, never remove it. Permission outcomes are three, never one word: self-authorised (proceeds, audited), escalated (a supervisor PIN in place), refused (the denied state, naming the permission); a missing permission is never an empty table, and a record outside the person's venues is "not found", indistinguishable from absent. The hierarchy is binding (tenant, brand, region, venue, department, sub-department, workstation; outlet beside department for F&B and retail); region owns currency, decimals, time zone, date format and fiscal year; configuration resolves nearest-ancestor across tenant, region and venue (outlet for F&B and retail), venue is the floor and a workstation is assigned a profile, never configured; every configuration screen says which level it writes and what it inherits. Venue Management is one tenant-level surface filtering across the venues in the session's scope. TICVAI's Console runs outside every cell: a platform operator picks a tenant and opens a time-boxed, audited platform-staff grant (with step-up) before any tenant action, and the tenant sees every action in its audit log (ADM-412 is the reference implementation). Approval workflows record authorisations and never perform the action; the requester cannot approve their own request; a venue may tighten and never loosen a rule from above; in-flight …
*(source: screens/P12-support-agent-console.yaml#SUP-001; R135; R126; R167; DI-1072; ADR-0002; ADR-0003; ADR-0004; R184; contracts/spine/identity.yaml#createMfaChallenge; contracts/spine/approvals.yaml#setStepUpPolicy; ADR-0011; ADR-0018; ADR-0029; R098; contracts/spine/approvals.yaml#decideApprovalRequest …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Sign in / Sign out | Entering and leaving any app, staff or guest. | Login, Log in, Logon, Logout | screens/P04-point-of-sale.yaml#POS-000 … |
| Authentication code | The staff second factor from the authenticator app (or the emailed fallback). | OTP, 2FA code, token | screens/P09-platform-admin-console.yaml#ADM-001 |
| One-time code | The six-digit code a guest receives to sign in or prove a contact. | OTP, PIN, password | DI-1034; R167 |
| Two-step verification | The guest's optional second factor, asked only at venues that switched it on. | MFA, 2FA | DI-1072 |
| Tenant / Brand / Region / Venue / Department / Outlet | The binding hierarchy levels; region owns currency and dates; outlet is F&B or retail inside a venue. | Client, Customer, Org (for tenant), Site, Park, Property (for venue), Area, Territory (for region) | ADR-0011; ADR-0018 |
| Workstation (back office) / till (operator copy) | A configured device; decides Sale Board, hardware and till identity, never authorisation. | Terminal, Station, POS (for the device), till (for the Deposit Box) | ADR-0002; R156 |
| Sale Board | The configured front end a workstation loads (ticketing, F&B or retail). | Screen, Layout, Menu | ADR-0003 |
| Role | A named, fully configurable grouping of permissions; the seeded five are editable starting points. | Group, Profile | R229 |
| Staff member / Partner user / Platform operator | A tenant's staff principal; a partner's user; a TICVAI employee in the Console. | User (alone), Account, Agent (for venue staff) | F104 step 1; F104 step 4; F104 step 5 |
| Platform-staff grant | The time-boxed, audited access a platform operator opens into one tenant before acting in it. | Impersonation, Support login | R098 |
| Escalate / Refused | Escalate is supervisor approval captured in place; Refused is the denied state that names the permission. | Denied (for an action that can be escalated) | R197 |
| Approve / Reject / Return / Request information | The four decisions on an approval request; Withdraw is the requester's own act and never a rejection. | Accept, Decline, Cancel (for withdraw) | contracts/spine/approvals.yaml#decideApprovalRequest … |
| Subscription / Plan / Module / Licence | TICVAI's commercial relationship with a tenant, its plan, the modules it licenses and the limits. | Membership (that is the guest's pass) | R214 |
| Membership / Annual pass | A guest's pass product and its holder (BO-284 to BO-303). | Subscription (that is the tenant's TICVAI plan) | screens/P08-venue-back-office.yaml#BO-284 |
| Sandbox client / Production client | A developer's own test credential; a TICVAI-issued live credential after certification. | Test key, Live key, API key (without environment) | DI-927 |
| Asset (DAM) / Media (ticket) | A digital file in the library; ticket media is a wristband or card carrying entitlements. Never mix them. | Media (for a library asset) | contracts/satellite/assets.yaml#searchMedia … |

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
| `EMP-001` | Sign in | A | 14 | 43 | 9 | 5 | 3 | 0 | — | notStarted (generated) |
| `EMP-002` | Select venue & role | B | 1 | 5 | 6 | 3 | 1 | 5 | — | notStarted (generated) |
| `EMP-003` | Home — on duty | D | 35 | 24 | 6 | 11 | 3 | 0 | — | notStarted (generated) |
| `EMP-009` | End shift | C | 17 | 23 | 6 | 1 | 1 | 6 | — | notStarted (generated) |
| `EMP-010` | Scan — ready | C | 17 | 0 | 6 | 46 | 1 | 0 | — | notStarted (generated) |
| `EMP-004` | Task list | A | 4 | 14 | 6 | 15 | 6 | 0 | — | notStarted (generated) |
| `EMP-005` | Task detail | A | 40 | 17 | 6 | 22 | 4 | 0 | — | notStarted (generated) |
| `EMP-006` | Raise a task | D | 63 | 14 | 6 | 33 | 4 | 0 | — | notStarted (generated) |
| `EMP-007` | Handover notes | D | 0 | 20 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `EMP-008` | Shift summary | C | 4 | 24 | 6 | 1 | 0 | 6 | — | notStarted (generated) |

## Thin screens in this batch

**EMP-002, EMP-007 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `EMP-001` Sign in

**Get an employee onto a shared handheld fast, and resolve the session every other screen of the staff app reads.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | Block A · task APP-STAFF-EMP-001 |
| Who uses it | venue; in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | form (comfortable density): A sign-in on a shared handheld: number and PIN, the venue's SSO where it has one, the code only when a permission demands it - a form, not a list. |
| Offline | Signs in against the cached principal list from the last bundle; the status strip says offline. A steward at a gate at 08:00 still signs in. |
| Opens with | `challengeId` (navigation), `providerId` (deepLink) · cold entry: **The only screen of the staff app that needs nothing.** The handheld's `workstationId` travels in the sign-in request from the device itself, not from a … |
| Route | `/operations/sign-in` |

**What the spec says about it.** **Rebuilt as a sign-in form on 2 October 2026 (CHG-DOOR-002/003; Chinmay, 2 October 2026: fix the Block A blockers now).** It was generated as a list over active sessions, MFA methods and SSO providers with Force logout and Revoke all sessions on the door, which a person who is not yet signed in can never use (platform-foundation process notes). The sequence is the same on every staff and partner door: credentials (or the organisation's SSO) -> the authentication code only when a permission demands it (R135) -> the role prompt when several roles are held (ADR-0003) -> the landing. Managing sessions moved to the staff directory (BO-053); managing MFA methods stays on each app's own security or profile screen. On the handheld the role and venue prompt is EMP-002, which follows when several roles or venues are held; one of each goes straight to EMP-003. Enrolling a method happens on EMP-042, not at a shared device.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The staff app's door on a shared handheld: username and password or PIN, SSO where the venue uses it, the code only where a permission demands it, then the role and venue for the session. Fast enough for a steward at a gate at 08:00; works offline against the cached staff list.

**Fixed on main** (the package already carries these; draw what it says): listDetail pattern with MFA-method and SSO-provider tables; emptyFirstRun "No sign yet". (CHG-DOOR-001); selectRole is not declared though staff hold several roles. (CHG-SPO-018); Tables show every schema field, plumbing included: 'Every MFA method' drop id; 'Every SSO provider' drop id, scopePath. (CHG-DOOR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Employee number or username | text field | — | — | — | — | Goes into `LoginRequest.username`. | — |
| PIN or password | text field | — | — | — | — | Goes into `LoginRequest.credential`, `method: pin` on the handheld (bounded by the device's `workstationId`, which the device sends; CHG-DOOR-001) or `method: password` for a person with no PIN. … | — |
| Authentication code | text field | — | — | — | — | Shown only when the sign-in comes back `requiresMfa`: the person holds a permission in `PasswordPolicy.mfaRequiredForPermissions` (ROLE_MANAGE, LEDGER_APPROVE, every PLATFORM_* permission, or one the … | — |
| New PIN | text field | — | — | — | — | Only when the PIN was reset and is temporary: a new one twice before anything else; the last five cannot be reused (audit R132). | — |

**Sent by *Sign in*** (`login`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Username `username` | text area | required | — | max length 256 | — | — | `login` body |
| Credential `credential` | text area | required | — | max length 512 | — | Password, PIN, card token or RFID token depending on `method`. | `login` body |
| Method `method` | radio group | optional | Password | Password · PIN · Card · RFID · Sso | — | `pin` is how a till is actually used. A cashier signs in at a shared terminal between guests, and a password on a touchscreen with somebody waiting is a password that gets … | `login` body |
| Workstation `workstationId` | picker: choose a workstation | optional | — | — | shows names, sends the id | Identifies the device. Determines Sale Board, connected hardware, till identity and Access Point inheritance. | `login` body |
| Device fingerprint `deviceFingerprint` | text area | optional | — | max length 256 | — | — | `login` body |

**Sent by *Verify*** (`verifyMfaChallenge`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | — | — | — | `verifyMfaChallenge` body |

**Sent by *Email me a code instead*** (`createMfaChallenge`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | text field | required | — | — | — | What the step-up is for. Recorded in the audit trail. | `createMfaChallenge` body |
| Method `methodId` | picker: choose a method | optional | — | — | shows names, sends the id | — | `createMfaChallenge` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | For a guest, the venue whose `VenueSettings.identity.guestTwoStep` applies (sign-in venue, or the venue of the booking being acted on). | `createMfaChallenge` body |

**Sent by *Choose venue and role*** (`selectRole`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Role `roleId` | picker: choose a role | required | — | — | shows names, sends the id | — | `selectRole` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Credential**: PIN on the handheld (bounded by the device's workstation), password where the person has no PIN; SSO button where the tenant configured one. *(source: DI-225; contracts/spine/identity.yaml#/components/schemas/LoginRequest)*

#### Outputs: what the screen shows and produces

**Shown**

**Sign in with your organisation** (card list, from `listSsoProviders`): One button per identity provider the venue configured; **absent, not disabled, when there is none.** Read before sign-in, unauthenticated. When a provider `isEnforced` for this person, the password field is hidden and only this remains.

| Shows | Format | Notes |
|---|---|---|
| Display name | text | — |
| Protocol | chip: Oidc, Saml2 | — |
| Is enforced | yes / no (icon or chip) | True disables password login for principals covered by this provider. |

**Finishing sign-in with your organisation** (progress indicator, from `completeSsoAuthorization`): On the provider's redirect back (`code` and `state` from the redirect, never typed). Returns the same `LoginResponse` as `login`, so the second factor and the role prompt follow exactly as below. 403: the provider proved who this is and no group maps to a role in this tenant, which grants nothing.

| Shows | Format | Notes |
|---|---|---|
| Access token | text | JWT carrying `sid`, validated per request against the session registry. |
| Refresh token | text | — |
| Expires in | 1,234 | Seconds |
| Requires role selection | yes / no (icon or chip) | — |
| Requires MFA | yes / no (icon or chip) | True when the principal holds any permission listed in `PasswordPolicy.mfaRequiredForPermissions` (decided 28 September, audit R135). |
| Has MFA method | yes / no (icon or chip) | Whether the principal has an active MFA method. With `requiresMfa` true and this false, the client must enrol one first (audit R135, R126 … |
| MFA methods | list or chips (count when long) | The principal's active methods, so the client can offer the right one for the `signIn` challenge. |
| ID | the name it points at, never the id | — |
| Kind | chip: Totp, SMS OTP, Email OTP, Biometric, Hardware token | — |
| Label | text | — |
| Masked target | text | Partially masked destination, so a person can tell two methods apart. |
| Is active | yes / no (icon or chip) | — |
| Is primary | yes / no (icon or chip) | — |
| Enrolled at | 1 Oct 2026, 14:30 | — |
| Last used at | 1 Oct 2026, 14:30 | — |
| Available roles | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Is primary | yes / no (icon or chip) | — |

**Signed in as** (banner, from `getCurrentSession`): Read once the sign-in is complete (after the code and the role, where asked): the person's name and role, then straight on. One role and one venue go to EMP-003; several go to EMP-002 first.

| Shows | Format | Notes |
|---|---|---|
| Session | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Role | the name it points at, never the id | — |
| Display name | text | — |
| Scope | list or chips (count when long) | Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. |
| ID | the name it points at, never the id | — |
| Level | chip: Tenant, Brand, Region, Venue, Department, Sub department… | The eight organisational levels, plus `subject`. Restored 24 August. |
| Path | text | Materialised ltree path. Prefix-comparable — `uae.dubai` contains `uae.dubai.marina`. |
| Code | text | — |
| Name | text | — |
| Effective permissions | list or chips (count when long) | Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. |
| Permissions by scope | list or chips (count when long) | Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves. |
| Permissions | list or chips (count when long) | — |
| Sale board | the name it points at, never the id | Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board. |
| Workstation | grouped details | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Venue | the name it points at, never the id | — |
| Region | the name it points at, never the id | — |
| Access point | the name it points at, never the id | Inherited from the workstation, never selected by the operator. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Sign in (primary button) | `login` POST `/auth/login` | LoginRequest | LoginResponse | 400 Validation failed; 409 An active session already exists for this principal on another device. Per §3.1.3 the new login is refused. | — |
| Continue with your organisation (secondary button) | `startSsoAuthorization` GET `/auth/sso/{providerId}/authorize` | — | inline | — | — |
| Verify (primary button) | `verifyMfaChallenge` POST `/auth/mfa/challenge/{challengeId}/verify` | inline | inline | 410 The challenge has expired or was voided (by a fifth wrong code, or a newer challenge for the same purpose).; 422 A wrong code, attempts one to four (CHG-R1S-025; the r1 gate found only the fifth failure specified). | — |
| Email me a code instead (secondary button) | `createMfaChallenge` POST `/auth/mfa/challenge` | inline | inline | — | — |
| Choose venue and role (secondary button) | `selectRole` POST `/auth/select-role` | inline | Session | 403 Authenticated but not permitted at the requested scope | — |

**Data it reads**: `listSsoProviders` (onLoad, Which identity providers this door offers; unauthenticated …); `completeSsoAuthorization` (background, Exchange the provider's code for the same LoginResponse as …)

**Where the user goes next**

- → `EMP-002` Select venue & role: *Selects venue and role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-048` Opening checklist: *Opening checklist*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Checking the credential. The form stays visible and disabled. |
| Empty, first run (`?state=emptyFirstRun`) | **Nobody signed in** - the normal state of a door. A shared handheld between shifts shows nothing until somebody identifies themselves. |
| Error (`?state=error`) | Identity could not be reached. **Says so rather than saying the password is wrong**, and keeps what was typed. |
| Denied (`?state=denied`) | The credential does not match, or the account is locked. One message for both, with the attempts left before the lock; a locked account says when to try again. |
| Permission denied (`?state=emptyNoAccess`) | Signed in, and the person holds no role in this app. Says who at the tenant grants access; distinct from a wrong password. A door has no permission of its own to name, because the person is not signed in until it succeeds. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listSsoProviders` takes no filter; a tenant with no identity provider shows no SSO buttons at all, and the form is the whole door. |
| Session held (`?state=sessionHeld`) | `login` answered 409: this person already holds a session elsewhere (audit R184, ADR-0004). Says where and since when; only a holder of SESSION_FORCE_LOGOUT ends it, on the staff directory (BO-053), and signing in never ends it by itself. |
| MFA required (`?state=mfaRequired`) | **Signed in, not yet through.** The principal holds a permission that requires MFA (ROLE_MANAGE, LEDGER_APPROVE, any PLATFORM_* permission, or one the tenant added), so the screen calls `createMfaChallenge` (`action: signIn`) and asks for the authentication code; `verifyMfaChallenge` completes the sign-in. **Email me a code instead** is the fallback. Five wrong codes lock step-up for the policy's lockout minutes and the screen says until when (audit R135, R126). A person without such a … |
| Offline (`?state=offline`) | Signs in against the cached principal list from the last bundle; the status strip says offline. A steward at a gate at 08:00 still signs in. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 An active session already exists for this principal on another device. Per §3.1.3 the new login is refused.; 422 A wrong code, attempts one to four (CHG-R1S-025; the r1 gate found only the fifth failure specified).; 422 The new credential fails the password policy, or matches the current one or any of the previous `PasswordPolicy.reusePreventionCount` credentials (5 … |

#### Edge cases to draw

- **Offline at sign-in**: Signs in against the cached principal list; the status strip says offline. *(source: screens/P06-staff-app.yaml#EMP-001)*
- **Handheld passed to a colleague at a break**: The colleague signs in afresh; nothing carries over (the person carries the authority, not the device). *(source: F61 step 1; ADR-0002)*

#### Consistency with other screens

- Match `POS-000`: Same keypad, refusal wording and role choice.
- Match `SCN-001`: Same door on the scanner.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
staff:
  name: Yusuf Rahman
  username: '20877'
  role: Steward
  venue: AquaCove Abu Dhabi
  device: Zebra TC52 · AUH-HH-14
```

#### Permissions

- `login` → no permission · anonymous, partner
- `listSsoProviders` → no permission · anonymous, partner
- `startSsoAuthorization` → no permission · anonymous
- `completeSsoAuthorization` → no permission · anonymous
- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest
- `changeOwnCredential` → no permission · staff, partner
- `getCurrentSession` → no permission · staff, partner
- `selectRole` → no permission · staff, partner

**A refused user sees:** Signed in, and the person holds no role in this app. Says who at the tenant grants access; distinct from a wrong password. A door has no permission of its own to name, because the person is not signed in until it succeeds.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.1.5 | The system should have the option to be used by several waiters at the same time. | F&B & Guest Management | CONTRACTED | `login` |
| 5.8.2 | The system should only allow one session per user. | F&B & Guest Management | CONTRACTED | `login` |
| 3.3.28 | Authorization Caching - System shall support caching of authorization decisions. | Admission and Access | CONTRACTED | `getCurrentSession` |
| 7.1.50 | Cache authorization decisions securely to improve performance while ensuring policy changes invalidate outdated cache entries. | F&B POS | CONTRACTED | `getCurrentSession` |
| 7.1.4 | The system should be able to have a login override option for the supervisor level in order to login to the POS if the need arises and the previous user has not logged out. | F&B POS | CONTRACTED | `selectRole` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*
- Employee app login by username/password or SSO. *(client request · MoM 10 Aug 2026, 5.1 Login, Roles & Dashboard · DI-225)*
- A user can hold several roles and switch between them at login (e.g. cashier vs supervisor). *(agreed · MoM 7 Aug 2026, 4. Roles & User Management · DI-152)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-001` · status **notStarted** · provenance generated
- Flow F08 *Steward works a shift on the employee app*, step 1: Signs in → Biometric or SSO
- Flow F64 *A steward signs in and takes a venue and a role*, step 1: They sign in. → **SSO where the venue uses it, MFA where the role demands it.** A gate steward and a finance controller do not need the same ceremony.
- Flow F64 branch at step 1 (high): when MFA is required and the phone is in a locker., **Refused, and the venue has a policy problem rather than a platform one.** A bypass here is a bypass for everybody.
- ADR-0003 *Conditional role selection at login* (`docs/adr/0003-conditional-role-selection-at-login.md`)
- ADR-0004 *Single session per user* (`docs/adr/0004-single-session-per-user.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400, 403, 409, 410, 422).
- [ ] Every output is drawn (43 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-001?state=<state>`: loading, emptyFirstRun, error, denied, emptyNoAccess, emptyNoResults, sessionHeld, mfaRequired, offline.
- [ ] Every action is wired with its success and its failure: Sign in, Continue with your organisation, Verify, Email me a code instead, Choose venue and role.
- [ ] Every transition is wired: `EMP-002`, `EMP-003`, `EMP-048`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-002` Select venue & role

**Confirm which hat this person is wearing today.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | Block B · task APP-STAFF-EMP-002 |
| Who uses it | venue; in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listMfaMethods` reads the population and `getCurrentSession` reads one of them — list, select, act |
| Offline | Cached from the last session |
| Opens with | `sessionId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/operations/select-venue-role` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createRole, forceLogout, listActiveSessions, revokeAllSessions. **Bulk-attach residue** — the 18 August defect that put identical operation sets on unrelated screens. A till does not cancel a performance, a staff app does not create roles, and **a scanner does not run a cash shift.** ** restored** — a role-select screen must read the roles. Over-stripped and caught by F08.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): Venue-and-role selection listed roles with listRoles (ROLE_MANAGE), which a steward never holds, and tables of MFA methods and SSO providers; the roles to choose … Removed 2 October 2026 (CHG-WIR-021): Venue-and-role selection listed roles with listRoles (ROLE_MANAGE), which a steward never holds, and tables of MFA methods and SSO providers; the roles to choose … Removed 2 October 2026 (CHG-WIR-021): Venue-and-role selection listed roles with listRoles (ROLE_MANAGE), which a steward never holds, and tables of MFA methods and SSO providers; the roles to choose …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Right after sign-in on the staff handheld, a person holding several roles or posted at several venues picks which role and venue this session works as. One role and one venue skip the screen. The choice decides navigation and what the session may do; it never changes who the person is.

**Fixed on main** (the package already carries these; draw what it says): Tables of every MFA method and SSO provider, and listRoles (ROLE_MANAGE) for the role list. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every MFA method' drop id; 'Every SSO provider' drop id, scopePath; 'Every role' drop … (CHG-WIR-021); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SPO-018).

#### Inputs: what the user enters or picks

**Form: Select role** (modal, opened by *Select role*; *Select role* calls `selectRole`, *Cancel* sends nothing)

**Collects what `selectRole` sends before it is called.** Required: `roleId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Role `roleId` | picker: choose a role | required | — | — | shows names, sends the id | — | `selectRole` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Role and venue**: Large buttons, one per role the person holds; a venue picker only when the grants cover several venues, listing only those venues. *(source: ADR-0003; contracts/spine/identity.yaml#selectRole; F64 step 1)*

#### Outputs: what the screen shows and produces

**Shown**

**The session** (detail panel, from `getCurrentSession`)

| Shows | Format | Notes |
|---|---|---|
| Display name | text | — |
| Scope | list or chips (count when long) | Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. |
| Effective permissions | list or chips (count when long) | Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Select role (primary button) | `selectRole` POST `/auth/select-role` | inline | Session | 403 Authenticated but not permitted at the requested scope | opens modal first |

**Data it reads**: `getCurrentSession` (onLoad, Current session and effective permissions)

**Where the user goes next**

- → `EMP-048` Opening checklist: *Works the opening checklist*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The select venue role list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the select venue role untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **One venue and one role**: nothing to choose, so the app goes straight on. Shown only when the person holds no role at any venue, and says who at the tenant grants one. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: nothing on this screen filters its list, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks the permission the screen requires, and names it. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Cached from the last session |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
roles:
- Steward
- Supervisor
venues:
- AquaCove Abu Dhabi
- AquaCove Dubai
```

#### Permissions

- `selectRole` → no permission · staff, partner
- `getCurrentSession` → no permission · staff, partner

**A refused user sees:** Shown when the caller lacks the permission the screen requires, and names it. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.1.4 | The system should be able to have a login override option for the supervisor level in order to login to the POS if the need arises and the previous user has not logged out. | F&B POS | CONTRACTED | `selectRole` |
| 3.3.28 | Authorization Caching - System shall support caching of authorization decisions. | Admission and Access | CONTRACTED | `getCurrentSession` |
| 7.1.50 | Cache authorization decisions securely to improve performance while ensuring policy changes invalidate outdated cache entries. | F&B POS | CONTRACTED | `getCurrentSession` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S2** Role-based access control: role and permission matrix *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'permission matrix')*
- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'rbac')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A97** Document the RBAC role-permission matrix (edit/view · view-only · hidden, per role per module, sub-permissions, default templates) *(Chinmay Parab · High · Ongoing → 30 Sep: Closed, Rolled into S2 · 20 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A130** Enforce venue-level admission capacity as superseding event capacity, with a blocking validation and an RBAC-gated override *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 25 Aug 2026 · workshop tracker · keyword 'rbac')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-002` · status **notStarted** · provenance generated
- Flow F08 *Steward works a shift on the employee app*, step 2: Selects venue and role → A person may hold several roles; the shift needs one
- Flow F64 *A steward signs in and takes a venue and a role*, step 2: They pick a venue and a role for the shift. → **One person, several roles, one at a time** (ADR-0002). A supervisor covering a lane takes the steward role and loses the supervisor one until they change back.
- Flow F08 branch at step 2 (requiresStaff): when Emergency declared, EMP-047 emergency mode overrides the home screen entirely. This is the one screen that outranks everything.
- Flow F64 branch at step 2 (medium): when The principal has no role at this venue., Refused at role select, not at first action. **A person who signs in and then cannot do anything has been told the wrong thing.**
- ADR-0003 *Conditional role selection at login* (`docs/adr/0003-conditional-role-selection-at-login.md`)
- ADR-0002 *Authorisation is user-driven, not workstation-driven* (`docs/adr/0002-authorisation-is-user-driven-not-workstation-driven.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-002?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Select role.
- [ ] Every transition is wired: `EMP-048`, `EMP-001`, `EMP-003`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-003` Home — on duty

**The screen the device sits on between tasks.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `maintenance` module |
| Block | Block D · task APP-STAFF-EMP-003 |
| Who uses it | venue staff holding `INCIDENT_MANAGE`, `INCIDENT_REPORT`, `INCIDENT_VIEW`, `REPORT_VIEW_WORKSTATION` (1 configure, 2 operate, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | approvalInbox (comfortable density): `approveShiftOpen` decides items that `listIncidents` queues — every row is waiting for a person, so the empty state is success |
| Offline | Last synced view, with its age. The pending count is always current because it is local |
| Opens with | `incidentId` (deepLink), `shiftId` (session), `workstationId` (session) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/home-on-duty` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **createCashMovement removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class). **Blind close** (decided 2 October 2026, Chinmay; CHG-FIN-003): closing from here submits the cashier's blind count with `submitShiftCount` (no expected cash, no variance shown; the supervisor is alerted beyond the threshold); `closeShift`, which returns the expected figure, is the supervisor's path on BO-039 and BO-040.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): Till and cash-shift writes on the staff-app home are bulk-attach residue; the screen's own notes removed createCashMovement because a screen that does not handle … Removed 2 October 2026 (CHG-WIR-008): Till and cash-shift writes on the staff-app home are bulk-attach residue; the screen's own notes removed createCashMovement because a screen that does not handle … Removed 2 October 2026 (CHG-WIR-008): Till and cash-shift writes on the staff-app home are bulk-attach residue; the screen's own notes removed createCashMovement because a screen that does not handle …

**From the Food, Beverage & Retail process.** The screen a staff handheld sits on between tasks, and for a restaurant host or server it is the start of every service. It must be a role-based home: what this person needs now (open incidents first, then their own work) with the navigation filtered to their role, so a server sees the floor, their tables, reservations and the waitlist and not 50 unrelated destinations. The one thing to get right: it is a home and a launcher, not a till. It reads the current shift and the open incidents and moves no money.

**Known correction pending (do not draw the wrong version)**

- **requiresModule maintenance should be core.** Why: Every staff member's home is gated on the maintenance licence today. A tenant that licenses only F&B would have no home. *(source: screens/P06-staff-app.yaml#EMP-003 / F94 step 1; Food, Beverage & Retail)*
- **Module placement: EMP-003 is the generic staff-app home (module Operations) and belongs to the core staff-app process. The F&B process contributes only the restaurant service strip and the restaurant navigation group, which is how it should be listed.** Why: Its operations are shift and incident operations, and its flows (F08, F64) are steward flows. Placing it under F&B will make the restaurant design own a screen every role uses. *(source: F08 step 4 / F64 step 4 / DI-227; Food, Beverage & Retail)*
- **Filter fields with plumbing labels ("Severity", "Status" as free text fields, an "Is reportable" toggle) should be chips with the incident vocabulary, or removed from the home.** Why: The home shows the open incidents; filtering belongs on the incident list. *(source: screens/P06-staff-app.yaml#EMP-003 / contracts/satellite/maintenance.yaml#listIncidents; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): Remove the till and cash-shift writes from the home: openShift, closeShift, suspendShift, resumeShift, reopenShift, approveShiftOpen … (CHG-WIR-008); The pattern approvalInbox, driven by approveShiftOpen, and the empty state "Nothing is waiting, which is the good outcome" are wrong for a … (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which roles are the restaurant roles on the staff app (host, server, captain or supervisor), and which of the restaurant destinations does each see?** → Drawn default stands (answer: "Host and Server variants; a supervisor sees both"): Draw two variants. The host sees Floor, Reservations, Waitlist and New reservation. The server sees Floor filtered to My tables, the table sheet and the bill. The supervisor sees both, plus Performance and Configuration. *(decided by Chinmay, 2026-10-02; DEC-198 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Severity | radio group | optional | — | Near miss · Minor · Moderate · Major · Critical | — | Sends `?severity=` to `listIncidents`. | `listIncidents` ?severity |
| Status | radio group | optional | — | Reported · Under investigation · Action required · Closed | — | Sends `?status=` to `listIncidents`. | `listIncidents` ?status |
| Is reportable | toggle | optional | — | — | — | Sends `?isReportable=` to `listIncidents`. | `listIncidents` ?isReportable |

**Form: Record authority notification** (modal, opened by *Record authority notification*; *Record authority notification* calls `recordAuthorityNotification`, *Cancel* sends nothing)

**Collects what `recordAuthorityNotification` sends before it is called.** Required: `authority`, `notifiedAt`. Optional: `reference`, `notifiedByPrincipalId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Authority `authority` | text field | required | — | max length 200 | — | — | `recordAuthorityNotification` body |
| Reference `reference` | text field | optional | — | max length 128 | — | — | `recordAuthorityNotification` body |
| Notified at `notifiedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordAuthorityNotification` body |
| Notified by principal `notifiedByPrincipalId` | picker: choose a notified by principal | optional | — | — | shows names, sends the id | — | `recordAuthorityNotification` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `recordAuthorityNotification` body |

Errors to draw in the form: 409 The incident is not reportable (`isReportable` false, audit R106 (6)).

**Form: Report incident** (modal, opened by *Report incident*; *Report incident* calls `reportIncident`, *Cancel* sends nothing)

**Collects what `reportIncident` sends before it is called.** Required: `id`, `kind`, `severity`, `venueId`, `description`, `occurredAt`, `recordedAt`. Optional: `assetId`, `locationDescription`, `involvedSubjectIds`, `involvedStaffPrincipalIds`, `witnessCount`, `firstAidGiven`, `emergencyServicesCalled`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `reportIncident` body |
| Kind `kind` | select | required | — | Guest injury · Staff injury · Near miss · Property damage · Equipment failure · Security incident · Fire or evacuation · Food safety · Environmental · Other | — | — | `reportIncident` body |
| Severity `severity` | radio group | required | — | Near miss · Minor · Moderate · Major · Critical | — | — | `reportIncident` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `reportIncident` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `reportIncident` body |
| Location description `locationDescription` | text area | optional | — | max length 500 | — | — | `reportIncident` body |
| Description `description` | text area | required | — | min length 3; max length 10000 | — | — | `reportIncident` body |
| Involved subjects `involvedSubjectIds` | multi-picker: choose involved subjects | optional | — | — | — | Opaque references. Personal details live in the erasable store, so the incident record survives an erasure request intact. | `reportIncident` body |
| Involved staff principals `involvedStaffPrincipalIds` | multi-picker: choose involved staff principals | optional | — | — | — | — | `reportIncident` body |
| Witness count `witnessCount` | number field | optional | — | — | — | — | `reportIncident` body |
| First aid given `firstAidGiven` | toggle | optional | off | — | — | — | `reportIncident` body |
| Emergency services called `emergencyServicesCalled` | toggle | optional | off | — | — | — | `reportIncident` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `reportIncident` body |
| Occurred at `occurredAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `reportIncident` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `reportIncident` body |

Errors to draw in the form: 400 Validation failed

**Form: Save incident** (modal, opened by *Save incident*; *Save incident* calls `updateIncident`, *Cancel* sends nothing)

**Collects what `updateIncident` sends before it is called.** Nothing in the body is required. Optional: `status`, `severity`, `assignedToPrincipalId`, `investigationNote`, `rootCause`, `correctiveActions`, `correctiveWorkOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | radio group | optional | — | Reported · Under investigation · Action required · Closed | — | — | `updateIncident` body |
| Severity `severity` | radio group | optional | — | Near miss · Minor · Moderate · Major · Critical | — | — | `updateIncident` body |
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | — | `updateIncident` body |
| Investigation note `investigationNote` | text area | optional | — | max length 10000 | — | Appended as a new entry of `IncidentDetail.investigationNotes`, never overwriting the last (audit R106 (5)). | `updateIncident` body |
| Root cause `rootCause` | text area | optional | — | max length 2000 | — | — | `updateIncident` body |
| Corrective actions `correctiveActions` | text area | optional | — | max length 5000 | — | — | `updateIncident` body |
| Corrective work order `correctiveWorkOrderId` | picker: choose a corrective work order | optional | — | — | shows names, sends the id | — | `updateIncident` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `updateIncident` body |
| Escalate `escalate` | group | optional | — | — | — | Escalate an incident under investigation (the optional Escalated step; CHG-RUL-011). | `updateIncident` body |
| To principal `escalate.toPrincipalId` | picker: choose a to principal | required | — | — | shows names, sends the id | — | `updateIncident` body |
| Reason `escalate.reason` | text area | required | — | min length 3; max length 1000 | — | — | `updateIncident` body |
| Reason `reason` | text area | optional | — | min length 3; max length 1000 | — | Why the status changes. Required to reopen a closed incident (back to `underInvestigation`) and to close a `reported` one straight away (CHG-RUL-011). | `updateIncident` body |

Errors to draw in the form: 400 Closure attempted without findings or a corrective action; 403 A critical incident closed by the person who completed its corrective action (`closer-completed-action`; workbook Q530; CHG-CSA-033).; 422 A move outside the incident flow (`incident-transition-not-allowed`; CHG-RUL-011): to `actionRequired`, from `closed` to anything but `underInvestigation`, a …

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Role and venue in force**: Comes from the session (sign-in, then venue and role on EMP-002). Nothing on this screen asks for a workstation, shift or venue id. One person per session on a device: a second person cannot sign in over an active session; they sign out or suspend first. Show the signed-in name and role in the header at all times, because handhelds are shared at a restaurant pass. *(source: F64 step 4 / DI-245 / DI-227 / screens/P06-staff-app.yaml#EMP-003)*

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listIncidents`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |

**The selected incident** (detail panel, from `listIncidents`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Kind | chip: Guest injury, Staff injury, Near miss, Property damage, Equipment failure, Security … | — |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |

**The incident** (detail panel, from `getIncident`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Kind | chip: Guest injury, Staff injury, Near miss, Property damage, Equipment failure, Security … | — |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |

**The shift** (detail panel, from `getShift`)

| Shows | Format | Notes |
|---|---|---|
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Deposit box code | text | — |
| Bag number | text | — |

**The shift** (detail panel, from `getWorkstationShift`)

| Shows | Format | Notes |
|---|---|---|
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Deposit box code | text | — |
| Bag number | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Record authority notification (secondary button) | `recordAuthorityNotification` POST `/incidents/{incidentId}/notify-authority` | inline | Incident | 409 The incident is not reportable (`isReportable` false, audit R106 (6)). | opens modal first |
| Report incident (secondary button) | `reportIncident` POST `/incidents` | ReportIncidentRequest | Incident | 400 Validation failed | works offline; opens modal first |
| Save incident (secondary button) | `updateIncident` PATCH `/incidents/{incidentId}` | inline | Incident | 400 Closure attempted without findings or a corrective action; 403 A critical incident closed by the person who completed its corrective action (`closer-completed-action`; workbook Q530; CHG-CSA-033).; 422 A move … | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Order of the home**: Open incidents surface before anything else (yesterday's unresolved problem before today's first task), then the role's work. For a host or server in an outlet that runs table service, the work block is a compact service strip: my tables by status (Vacant, Occupied, Bill requested, Reserved), the next arrivals, and the waitlist count, each a tap into EMP-052, EMP-054 and EMP-056. For other roles the strip is their tasks and work orders. *(source: F64 step 4 / DI-227 / DI-335 / DI-792)*
- **Navigation set**: Filtered by role and permission, and by the licensed modules (requiresModule fnb on every restaurant screen). A server sees Floor, My tables, Reservations, Waitlist, Notifications, Clock in/out, Venue map, Profile. Restaurant set-up (Table & seating configuration) appears only for a role that holds the configure permission. Group the restaurant destinations under one Restaurant heading rather than ten peer tiles copied from the client board. *(source: DI-227 / DI-228 / DI-400 / contracts/satellite/fnb.yaml#setTableLayout)*
- **Offline strip**: Last synced view with its age; the pending count is always current because it is local. Tapping it opens the sync screen. Restaurant actions that are offline-capable (seat, order, move) stay enabled; the ones that are not (merge, close and settle) are shown disabled with the reason. *(source: screens/P06-staff-app.yaml#EMP-003 / F08 step 4 / DI-072 / F29 step 2)*
- **Kitchen calls**: When the pass calls this server (food ready, guest waiting, bill requested, assistance, allergy query), it lands here as a notification with the table code, not as a broadcast to the room. With no server assigned, the call goes to the outlet's supervisor on duty. *(source: contracts/satellite/fnb.yaml#notifyServer / R125 / F29 step 4)*

**Data it reads**: `getWorkstationShift` (onLoad, The shift on this handheld, read under a view permission so …); `listIncidents` (onLoad, From the flow it appears in); `getShift` (onLoad, Read a shift)

**Where the user goes next**

- → `EMP-004` Task list: *Works the task list*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-051` Restaurant Service Command Center: *Restaurant Service Command Center*
- → `EMP-052` Floor Plan & Table Map: *Floor Plan & Table Map*
- → `EMP-053` Table & Seating Configuration: *Table & Seating Configuration*
- → `EMP-054` Reservation Calendar & Timeline: *Reservation Calendar & Timeline*
- → `EMP-055` Create / Edit Reservation: *Create / Edit Reservation*
- → `EMP-056` Walk-In & Waitlist Management: *Walk-In & Waitlist Management*
- → `EMP-057` Guest Profile & Dining History: *Guest Profile & Dining History*
- → `EMP-058` Live Table & Service Management: *Live Table & Service Management*
- → `EMP-059` Table Order, Bill & Payment Management: *Table Order, Bill & Payment Management*
- → `EMP-060` Reservation & Table Performance: *Reservation & Table Performance*
- → `EMP-061` Retail Inventory Command Center: *Retail Inventory Command Center*
- → `EMP-062` Store Stock & SKU Availability: *Store Stock & SKU Availability*
- → `EMP-063` Requisition & Smart Store Replenishment: *Requisition & Smart Store Replenishment*
- → `EMP-064` Store-to-Store & Warehouse Transfers: *Store-to-Store & Warehouse Transfers*
- → `EMP-065` Receiving: *Receiving & Store Put-Away*
- → `EMP-066` Stock Count & Cycle Count Management: *Stock Count & Cycle Count Management*
- → `EMP-067` Damage, Loss, Shrinkage & Stock Adjustment: *Damage, Loss, Shrinkage & Stock Adjustment*
- → `EMP-068` Reservation, Allocation & Omnichannel Inventory: *Reservation, Allocation & Omnichannel Inventory*
- → `EMP-069` Barcode, RFID, Serialized Stock & Traceability: *Barcode, RFID, Serialized Stock & Traceability*
- → `EMP-070` Inventory Exceptions, AI Replenishment & Action Center: *Inventory Exceptions, AI Replenishment & Action Center*
- → `EMP-071` Rental Checkout Command Center: *Rental Checkout Command Center*
- → `EMP-081` Active Rental Operations Command Center: *Active Rental Operations Command Center*
- → `EMP-091` Rental Return Command Center: *Rental Return Command Center*
- → `EMP-006` Raise a task: *Raise a task*
- → `EMP-014` Ticket lookup: *Ticket lookup*
- → `EMP-019` AI assistant — home: *AI assistant — home*
- → `EMP-021` Roster: *Roster*
- → `EMP-022` My rota: *My rota*
- → `EMP-024` Clock in / out: *Clock in / out*
- → `EMP-025` Break management: *Break management*
- → `EMP-026` Incident report: *Incident report*; carries `incidentId`
- → `EMP-028` Lost & found: *Lost & found*
- → `EMP-029` Guest assistance: *Guest assistance*; carries `incidentId`
- → `EMP-030` Venue map: *Venue map*
- → `EMP-031` Queue monitor: *Queue monitor*
- → `EMP-033` Capacity view: *Capacity view*
- → `EMP-034` Walk-up sale: *Walk-up sale*
- → `EMP-037` Notifications: *Notifications*
- → `EMP-038` Broadcast to team: *Broadcast to team*
- → `EMP-039` Announcements: *Announcements*
- → `EMP-047` Emergency mode: *Emergency mode*
- → `EMP-042` Profile: *Profile*
- → `EMP-032` Manual wait entry: *Opens Manual wait entry*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The home duty list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the home duty untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on severity, status, isReportable and the home duty are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `getWorkstationShift` requires to show this screen, and names that permission (the screen's other reads need `INCIDENT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `INCIDENT_MANAGE` for `recordAuthorityNotification` … |
| Offline (`?state=offline`) | Last synced view, with its age. The pending count is always current because it is local |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Closure attempted without findings or a corrective action; 400 Validation failed; 409 The incident is not reportable (`isReportable` false, audit R106 (6)).; 422 A move outside the incident flow (`incident-transition-not-allowed`; CHG-RUL-011): to `actionRequired`, from `closed` to anything but `underInvestigation`, a … |

#### Edge cases to draw

- **Tenant licenses F&B but not maintenance**: The home must still load: today it is gated on the maintenance module, which would leave a restaurant-only tenant with no home. Draw the home without the incident block when maintenance is not licensed. *(source: screens/P06-staff-app.yaml#EMP-003 / F94 step 1)*
- **Server's shift changes mid-service with tables still open**: The home shows a "You still have 3 open tables" banner before the person clocks out, linking to the table sheet (EMP-058) to change server. *(source: F08 step 8 / F29 step 6 / contracts/satellite/fnb.yaml#reassignServer)*

#### Consistency with other screens

- Match `EMP-002`: The role picked there drives this home; the same role names.
- Match `EMP-052`: The service strip uses the same status names and colours as the floor plan.
- Match `EMP-037`: Kitchen calls (notify server) are the same notification items as the notifications list.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
signedIn: Priya Nair · Server · Oasis Bistro dinner service
incidents:
- INC-2026-0412 · Spill near Terrace bar · Medium · Open
myTables:
  vacant: 2
  occupied: 4
  billRequested: 1
  reserved: 1
nextArrivals:
- 19:30 Daniel Brooks · 2
- 20:00 Fatima Al Suwaidi · 6 · nut allergy
waitlist: 3 parties waiting
kitchenCall: T12 · Food ready · 20:41
pendingSync: 2 waiting to sync · last synced 20:38 GST
```

#### Permissions

- `getWorkstationShift` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listIncidents` → `INCIDENT_VIEW` (read) · staff
- `getIncident` → `INCIDENT_VIEW` (read) · staff
- `getShift` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `recordAuthorityNotification` → `INCIDENT_MANAGE` (configure) · staff
- `reportIncident` → `INCIDENT_REPORT` (operate) · staff
- `updateIncident` → `INCIDENT_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `getWorkstationShift` requires to show this screen, and names that permission (the screen's other reads need `INCIDENT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `INCIDENT_MANAGE` for `recordAuthorityNotification` …

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.9.5 | System shall provide real-time visibility of incidents, hazards, complaints, emergencies, and operational disruptions. | Unified Operations Dashboard | CONTRACTED | `listIncidents` |
| 17.5.3 | Hazard Reporting - System shall support hazard reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 17.5.4 | Incident Reporting - System shall support incident reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 17.5.5 | Near-Miss Reporting - System shall support near-miss reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 18.4.1 | Hazard Reporting - Users shall submit hazard reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.2 | Incident Reporting - Users shall submit incident reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.3 | Near-Miss Reporting - Users shall submit near-miss reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.4 | Safety Inspections - Users shall perform inspections. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.5 | Safety Checklists - Users shall complete safety checklists. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.6 | Corrective Actions - Users shall submit corrective actions. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 2.13.44 | Incident & Exception Logging | Ticketing Sales | CONTRACTED | data `Shift` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*
- Quick-create for maintenance, IT support, cleaning/safety/security, store, purchase and leave requests. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-230)*
- Role-based home shows task counts, work orders and inspections for the employee; the whole navigation set (approvals, inventory, etc.) is filtered by role/permissions. *(client request · MoM 10 Aug 2026, 5.1 Login, Roles & Dashboard · DI-227)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-003` · status **notStarted** · provenance generated
- Flow F08 *Steward works a shift on the employee app*, step 4: Sees the home screen on duty → Today, at a glance
- Flow F64 *A steward signs in and takes a venue and a role*, step 4: They go on duty. → **Open incidents surface before anything else.** A steward starting a shift needs yesterday’s unresolved problem before today’s first task.
- Flow F08 branch at step 4 (recoverable): when Signal lost in a plant room or basement, Queues locally. The status strip shows pending count, and EMP-017 reconciles on return.
- ADR-0023 *— Personal data lives apart from the append-only ledger* (`docs/adr/0023-pii-separation.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (35), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-003?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Record authority notification, Report incident, Save incident.
- [ ] Every transition is wired: `EMP-004`, `EMP-001`, `EMP-002`, `EMP-051`, `EMP-052`, `EMP-053`, `EMP-054`, `EMP-055`, `EMP-056`, `EMP-057`, `EMP-058`, `EMP-059`, `EMP-060`, `EMP-061`, `EMP-062`, `EMP-063`, `EMP-064`, `EMP-065`, `EMP-066`, `EMP-067`, `EMP-068`, `EMP-069`, `EMP-070`, `EMP-071`, `EMP-081`, `EMP-091`, `EMP-006`, `EMP-014`, `EMP-019`, `EMP-021`, `EMP-022`, `EMP-024`, `EMP-025`, `EMP-026`, `EMP-028`, `EMP-029`, `EMP-030`, `EMP-031`, `EMP-033`, `EMP-034`, `EMP-037`, `EMP-038`, `EMP-039`, `EMP-047`, `EMP-042`, `EMP-032`.
- [ ] Every gated control is gated: `INCIDENT_MANAGE`, `INCIDENT_REPORT`, `INCIDENT_VIEW`, `REPORT_VIEW_WORKSTATION`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-009` End shift

**Close out cleanly, including anything unsynced.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | Block C · task APP-STAFF-EMP-009 |
| Who uses it | venue staff holding `OVERSHORT_ACCEPT`, `REPORT_VIEW_WORKSTATION`, `SHIFT_CLOSE`, `SHIFT_OPEN`, `SHIFT_SUSPEND` (5 operate); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | approvalInbox (comfortable density): `approveShiftOpen` decides items that `listCashMovements` queues — every row is waiting for a person, so the empty state is success |
| Offline | **Cannot close.** Closing needs the server total, and a locally computed variance is not a variance |
| Opens with | `shiftId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/operations/end-shift` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Blind close (decided 2 October 2026, Chinmay; CHG-FIN-003).** The cashier never sees the expected cash: not while counting, not after submitting, not as a sales or takings total from which it could be worked out (MoM 12 Aug 2026 section 19, DI-271; MoM 9 Sep 2026 4.18, DI-806: "if a cashier knew they had a small surplus, they could pocket it"). The count is submitted with `submitShiftCount`, which answers only what happens next (closed, with your supervisor, or awaiting close approval); the variance alerts the supervisors on the venue's alerting channel and appears on BO-040. The cashier may add a reason and a note with every count (DI-803). A recount the supervisor asks for is counted blind again (DI-804). Retail practice: docs/active/research-uae-vat-and-blind-close-2-october.md. **No cash count for a server** (decided 2 October 2026, Chinmay; DEC-200; CHG-CSP-039; CHG-SPO-009). A handheld takes no cash, so a server's End shift has no drawer and no count: it closes the service day (unsynced orders, open tables). The blind count and the variance acceptance on this screen are for a cashier whose drawer is on a till.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): An end-of-shift screen does not open a shift, approve an opening float or open the drawer; F72 step 3 needs closeShift, acceptShiftVariance and listCashMovements … Removed 2 October 2026 (CHG-WIR-008): An end-of-shift screen does not open a shift, approve an opening float or open the drawer; F72 step 3 needs closeShift, acceptShiftVariance and listCashMovements … Removed 2 October 2026 (CHG-WIR-008): An end-of-shift screen does not open a shift, approve an opening float or open the drawer; F72 step 3 needs closeShift, acceptShiftVariance and listCashMovements …

**From the Food, Beverage & Retail process.** End the person's shift cleanly: push anything unsynced, hand over what is still open, then close. For a restaurant server, ending a shift means handing their open tables to another server and clocking out. Only a person who holds a till also does the blind cash count. The one thing to get right: the count is blind, and the variance is accepted by a supervisor, never by the cashier whose shift it is.

**Known correction pending (do not draw the wrong version)**

- **Pattern approvalInbox with "Waiting for a decision" over cash movements.** Why: Lifts and adds are not decisions waiting for anybody. The screen is a close-out sequence (sync, hand over, count, result). *(source: screens/P06-staff-app.yaml#EMP-009 / F72 step 3; Food, Beverage & Retail)*
- **No hand-over of open tables and no clock-out on End shift, though F08 says "tasks reassigned, never silently closed" and DI-492 asks for shift closing on the employee app.** Why: For a server, the hand-over of open tables (reassignServer) and clock-out (recordAttendance on EMP-024) are what ending a shift means. *(source: F08 step 8 / DI-492 / contracts/satellite/workforce.yaml#recordAttendance; Food, Beverage & Retail)*
- **Module placement. EMP-009 is a core staff-app or till screen, not F&B.** Why: Its operations are the shift contract. F&B adds only the open-table hand-over step. *(source: TRACKER Workshops/Actions row 63 / F72 step 3; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): Remove openShift, approveShiftOpen, recordNoSale, resumeShift, reopenShift and createCashMovement from End shift. (CHG-WIR-008); acceptShiftVariance has only a reason in its request, with no supervisor step-up field. (CHG-WIR-008); F08 step 8 has the steward end the shift with closeShift, and F72 step 3 has the supervisor close it ("closing and accepting a variance are … (CHG-FIN-003).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does a server on a handheld ever hold cash (a payment taken in cash at the table on EMP-059), and if so, against whose drawer?** → No cash on handhelds: a server's handheld takes no cash payment; cash goes to a till. The server's End shift has no cash count. *(decided by Chinmay, 2026-10-02; DEC-200 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listShifts` ?workstationId |
| Status | select | — | Pending approval · Open · Suspended · Pending variance · Pending closure · Closed · Auto closed | `listShifts` ?status |
| Opened from | date and time picker | — | — | `listShifts` ?openedFrom |
| Opened to | date and time picker | — | — | `listShifts` ?openedTo |

**Form: Close shift** (confirmDialog, opened by *Close shift*; *Submit count* calls `submitShiftCount`, *Not yet* sends nothing)

**Collects what `submitShiftCount` sends.** Required: `countedCash` (by denomination), `recordedAt`. Optional: `cashierReason`, `notes`, `nonCashDeclared`, `releaseHeldLeases`. Says "Your count is final once submitted" and shows no expected figure (CHG-FIN-003).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Counted cash `countedCash` | repeatable rows | required | — | at least 1; A denomination may appear once; a repeat is refused with 422 `duplicate-denomination`. | — | The cashier's blind count, one line per denomination counted (decided 29 September, readiness close-out; our build plan). | `submitShiftCount` body |
| Denomination `countedCash[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` (`Denomination.id`) — face value, kind and counting order live there. | `submitShiftCount` body |
| Count `countedCash[].count` | number field | required | — | min 0; max 100000 | — | How many of this note or coin were counted. Zero is a line, not an omission: a denomination counted and found empty. | `submitShiftCount` body |
| Total `countedCash[].total` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | `count` times the face value, in the denomination's currency. Optional on the way in (the server computes it) and checked when sent. | `submitShiftCount` body |
| Non cash declared `nonCashDeclared` | repeatable rows | optional | — | — | — | Declared totals per non-cash tender, for reconciliation against captured payments. | `submitShiftCount` body |
| Tender `nonCashDeclared[].tender` | text field | required | — | — | — | — | `submitShiftCount` body |
| Amount `nonCashDeclared[].amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `submitShiftCount` body |
| Notes `notes` | text area | optional | — | max length 1000 | — | The cashier's note on the count. Asked of every cashier on a blind count, never only after a variance is shown (CHG-FIN-003, DI-803). | `submitShiftCount` body |
| Cashier reason `cashierReason` | radio group | optional | — | Till error · Unrecorded refund · Miscount · Other | — | Anything the cashier knows went wrong in the shift (DI-803: till error, unrecorded refund, miscount, other). | `submitShiftCount` body |
| Release held leases `releaseHeldLeases` | toggle | optional | on | — | — | Return unsold inventory leases held by this workstation (ADR-0013 C103). Closing without releasing strands capacity until TTL expiry, which is visible at a gate during peak. | `submitShiftCount` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `submitShiftCount` body |

Errors to draw in the form: 403 The shift is not the caller's own (problem type `not-shift-operator`): a supervisor closing somebody else's shift uses `closeShift` (SHIFT_CLOSE_OTHER).; 409 The shift is neither `open`, `suspended` nor `pendingVariance` (problem type `shift-not-countable`).

**Form: Accept shift variance** (modal, opened by *Accept shift variance*; *Accept shift variance* calls `acceptShiftVariance`, *Cancel* sends nothing)

**Collects what `acceptShiftVariance` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | Retained for audit. The accepting principal is recorded. | `acceptShiftVariance` body |
| Supervisor step up `supervisorStepUp` | group | optional | — | — | — | The supervisor accepting, signing on this device (CHG-RUL-019). Refused without it (`403 supervisor-step-up-refused`). | `acceptShiftVariance` body |
| Principal `supervisorStepUp.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | The supervisor signing. Recorded against the act. | `acceptShiftVariance` body |
| Credential `supervisorStepUp.credential` | text area | required | — | max length 512 | — | The supervisor's staff PIN, as they sign in at a till with it. A PIN, never a password (audit R123 (7)). | `acceptShiftVariance` body |

Errors to draw in the form: 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (problem type `approver-is-cashier`) — a cashier signing off their own …; 409 Shift is not `pendingVariance` (problem type `shift-not-pending-variance`) — within tolerance, still open, or already accepted.

**Sent by *Suspend shift*** (`suspendShift`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 200 | — | — | `suspendShift` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `suspendShift` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Counted cash**: One line per denomination, UAE notes 5 to 1000 AED and coins 25 fils, 50 fils and 1 AED, entered as quantities with the line total computed (count times face value). The expected figure is never on screen before submission. A duplicate or inactive denomination is refused, and so is a total that disagrees with the count. *(source: contracts/spine/shift.yaml#closeShift / R229 / R080 / MATRIX 5.9.2)*
- **Open tables to hand over (server)**: Each open table this server holds is listed with a "Change server" picker defaulting to the section's incoming server. Reason "Shift change" is preset. Gratuity split follows the assignment. Nothing closes silently. *(source: F08 step 8 / F29 step 6 / contracts/satellite/fnb.yaml#reassignServer / contracts/satellite/fnb.yaml#transferTableVisit)*
- **Supervisor acceptance**: Shown only when the close result says the variance needs acceptance. A supervisor enters their own PIN on this device and a reason of at least 3 characters. The cashier whose shift it is cannot accept (approver-is-cashier). *(source: contracts/spine/shift.yaml#acceptShiftVariance / R080 / R094)*

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listCashMovements`)

| Shows | Format | Notes |
|---|---|---|
| Reference | text | Safe drop reference or bag number. |
| Reason | text | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Synced at | 1 Oct 2026, 14:30 | — |

**Every shift** (data table, from `listShifts`)

| Shows | Format | Notes |
|---|---|---|
| Principal display name | text | — |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Deposit box code | text | — |
| Bag number | text | — |

**The selected cash movement** (detail panel, from `listCashMovements`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Opening float, Lift, Add | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Reference | text | Safe drop reference or bag number. |
| Reason | text | — |
| Recorded at | 1 Oct 2026, 14:30 | — |

**The shift** (detail panel, from `getShift`)

| Shows | Format | Notes |
|---|---|---|
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Deposit box code | text | — |
| Bag number | text | — |

**The shift** (detail panel, from `getCurrentShift`)

| Shows | Format | Notes |
|---|---|---|
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Deposit box code | text | — |
| Bag number | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Close shift (destructive button) | `submitShiftCount` POST `/shifts/{shiftId}/count` | CloseShiftRequest | ShiftCountReceipt | 403 The shift is not the caller's own (problem type `not-shift-operator`): a supervisor closing somebody else's shift uses `closeShift` (SHIFT_CLOSE_OTHER).; 409 The shift is neither `open`, `suspended` nor … | opens confirmDialog first |
| Accept shift variance (secondary button) | `acceptShiftVariance` POST `/shifts/{shiftId}/accept-variance` | inline | Shift | 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (problem type `approver-is-cashier`) — a cashier signing off their own …; 409 Shift is not `pendingVariance` (problem type … | step-up: pin (A supervisor signs off a cashier's over/short in person, with their own PIN on the device they use (audit R080 (e); any …); gated `OVERSHORT_ACCEPT`; opens modal first |
| Suspend shift (destructive button) | `suspendShift` POST `/shifts/{shiftId}/suspend` | inline | Shift | 403 Authenticated but not permitted at the requested scope; 409 Shift is not `open` (problem type `shift-not-open`) | works offline |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Close result**: After submission, the expected, counted and variance figures, with negative shown as "short" and positive as "over". Within the venue threshold (proposed AED 20.00) the shift is closed. Above it, the shift waits for a supervisor ("Waiting for supervisor") and the screen says so plainly. *(source: contracts/spine/shift.yaml#closeShift / R094)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Close shift**: Online only; offline the button is disabled with "Closing needs a connection; your count is kept". A 409 for open orders lists the open orders or tables that must be settled or handed over first. *(source: contracts/spine/shift.yaml#closeShift / F72 step 2 / screens/P06-staff-app.yaml#EMP-009)*

**Data it reads**: `getCurrentShift` (onLoad, The open or suspended shift on the session's workstation); `getShift` (onLoad, Read a shift); `listCashMovements` (onLoad, Lifts, adds and the opening float); `listShifts` (onLoad, List shifts)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

**What opens over it**

- confirmDialog *Suspend shift*: **Names what `suspendShift` changes and what it leaves alone**, in the consequence rather than the verb. A end shift this affects should be identified in the dialog, not just counted. **Collects what `suspendShift` sends before it is called.** Required: `recordedAt`. Optional: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The end shift list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the end shift untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCashMovements` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SHIFT_OPEN`, which `getCurrentShift` requires to show this screen, and names that permission (the screen's other reads need `REPORT_VIEW_WORKSTATION` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `OVERSHORT_ACCEPT` for `acceptShiftVariance`; `SHIFT_CLOSE` … |
| Offline (`?state=offline`) | **Cannot close.** Closing needs the server total, and a locally computed variance is not a variance |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Shift is not `open` (problem type `shift-not-open`); 409 Shift is not `pendingVariance` (problem type `shift-not-pending-variance`) — within tolerance, still open, or already accepted.; 409 The shift is neither `open`, `suspended` nor `pendingVariance` (problem type `shift-not-countable`). |

#### Edge cases to draw

- **No supervisor present to accept a variance above threshold**: Draw the "Waiting for supervisor" state. Whether the cashier may sign out with it pending is still open (DI-805). *(source: DI-805 / TRACKER 30-Sep/Tracker row 30)*
- **Shift forgotten**: Auto-closed after the venue limit and labelled "Auto-closed (not counted)", not "Closed". *(source: F08 step 8 / MATRIX 5.9.5)*
- **A server on a handheld**: No cash is taken on a handheld; cash goes to a till. The server's End shift has no cash count. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cashier: Omar Ziad · Oasis Bistro bar till 2
count:
  '1000': 0
  '500': 1
  '200': 4
  '100': 6
  '50': 8
  '20': 11
  '10': 9
  '5': 6
  1 AED: 13
  50 fils: 6
  25 fils: 4
countedTotal: AED 2,128.00
result:
  expected: AED 2,140.50
  variance: AED -12.50 short
  status: Closed (within AED 20.00)
handover:
- T12 · 4 covers · AED 620.24 open → Khalid Al Mansoori
- T7 · 2 covers · AED 188.00 open → Khalid Al Mansoori
```

#### Permissions

- `submitShiftCount` → `SHIFT_CLOSE` (operate) · staff
- `acceptShiftVariance` → `OVERSHORT_ACCEPT` (operate) · staff · step-up pin
- `getCurrentShift` → `SHIFT_OPEN` (operate) · staff
- `getShift` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listCashMovements` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listShifts` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `suspendShift` → `SHIFT_SUSPEND` (operate) · staff

**A refused user sees:** Shown when the caller lacks `SHIFT_OPEN`, which `getCurrentShift` requires to show this screen, and names that permission (the screen's other reads need `REPORT_VIEW_WORKSTATION` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `OVERSHORT_ACCEPT` for `acceptShiftVariance`; `SHIFT_CLOSE` …

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.44 | Incident & Exception Logging | Ticketing Sales | CONTRACTED | data `Shift` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-009` · status **notStarted** · provenance generated
- Flow F08 *Steward works a shift on the employee app*, step 8: Ends the shift with a blind count (no expected cash shown; CHG-FIN-003) → Tasks reassigned, notes handed over
- Flow F72 *A shift ends and the summary is read*, step 3: The cashier submits a blind count; beyond the threshold the supervisor accepts the variance (CHG-FIN-003). → **Closing and accepting a variance are supervisor acts** and now live only here. The steward's count is blind (no expected figure, no running variance, no takings; CHG-FIN-003) and takes no PIN; the …
- Flow F08 branch at step 8 (recoverable): when Shift ends with tasks open, Reassigned or carried, never silently closed. An open task at handover is the thing handover exists for.
- Flow F08 branch at step 8 (recoverable): when Steward forgets to end the shift, Auto-closed after the venue limit, and recorded as autoClosed rather than closed — nobody counted it.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (23 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-009?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Close shift, Accept shift variance, Suspend shift.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `OVERSHORT_ACCEPT`, `REPORT_VIEW_WORKSTATION`, `SHIFT_CLOSE`, `SHIFT_OPEN`, `SHIFT_SUSPEND`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-010` Scan — ready

**The raised centre action, and the thing this app is for.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `access` module |
| Block | Block C · task APP-STAFF-EMP-010 |
| Who uses it | venue staff holding `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `TICKET_LOOKUP` (3 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | **Keep working when the network does not.** The screen already had an `offline` state. |
| Opens with | nothing: it opens on its own |
| Route | `/operations/scan-ready` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Absorbed EMP-011, EMP-012, EMP-013, EMP-016 on 18 August.** A scanner is one screen the device sits on all day, and an outcome is a state of it — **routing to `/access/admitted` for something gone in 1.5 seconds is a page load per guest**, and at a gate doing 40 a minute that is the whole problem. Every absorbed screen kept its copy as a named state.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Scan history, sync and offline-package panels on the scan screen; as on SCN-003 the scan screen is idle by design, history is SCN-009's, sync EMP-017's and the … Removed 2 October 2026 (CHG-WIR-001): Scan history, sync and offline-package panels on the scan screen; as on SCN-003 the scan screen is idle by design, history is SCN-009's, sync EMP-017's and the … Removed 2 October 2026 (CHG-WIR-001): Scan history, sync and offline-package panels on the scan screen; as on SCN-003 the scan screen is idle by design, history is SCN-009's, sync EMP-017's and the …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Scanning inside the Staff App for relief cover at a gate: the same outcome states as the scanner (admitted, denied with reason, override required, blocked) on a phone, at lower throughput. The one thing to get right: identical wording and colours to SCN-003 so a steward switching devices sees no difference.

**Fixed on main** (the package already carries these; draw what it says): Scan history table, sync and offline package panels on the scan screen (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

**Form: Validate access** (modal, opened by *Validate access*; *Validate access* calls `validateAccess`, *Cancel* sends nothing)

**Collects what `validateAccess` sends before it is called.** Required: `id`, `mediaCode`, `mediaKind`, `direction`, `recordedAt`. Optional: `groupSize`, `proximityToken`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key and dedupe key. | `validateAccess` body |
| Media code `mediaCode` | text area | required | — | max length 256 | — | What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life. | `validateAccess` body |
| Media kind `mediaKind` | select | required | — | Image · Video · Audio · Document · Vector · Font · Archive · Model3d; glb`) venue model, at most 40 MB. | — | `model3d` added 3 October 2026 (r1 additions; ADR-0069 action item 4): a glTF binary (`model/gltf-binary`, `.glb`) venue model, at most 40 MB. | `validateAccess` body |
| Direction `direction` | radio group | required | — | Entry · Exit · Reentry · Crossover | — | — | `validateAccess` body |
| Group size `groupSize` | number field | optional | — | min 1 | — | For group media admitting several holders on one read. | `validateAccess` body |
| Proximity token `proximityToken` | text field | optional | — | — | — | BLE proximity assertion where the venue requires the operator to be physically at the gate. | `validateAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the read. Authoritative for ordering, not for validity. | `validateAccess` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell

**Form: Validate group access** (modal, opened by *Validate group access*; *Validate group access* calls `validateGroupAccess`, *Cancel* sends nothing)

**Collects what `validateGroupAccess` sends before it is called.** Required: `id`, `mediaCode`, `admitCount`, `recordedAt`. Optional: `direction`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `validateGroupAccess` body |
| Media code `mediaCode` | text area | required | — | max length 256 | — | — | `validateGroupAccess` body |
| Admit count `admitCount` | number field | required | — | min 1 | — | — | `validateGroupAccess` body |
| Direction `direction` | radio group | optional | — | Entry · Exit · Reentry · Crossover | — | — | `validateGroupAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `validateGroupAccess` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance

**Sent by *Override access*** (`overrideAccess`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `overrideAccess` body |
| Scan `scanId` | picker: choose a scan | required | — | — | shows names, sends the id | The denied scan being overridden. | `overrideAccess` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `overrideAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `overrideAccess` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Lookup ticket (secondary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |
| Override access (destructive button) | `overrideAccess` POST `/access/override` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 The scan was not a denial, or has already been overridden | works offline |
| Validate access (secondary button) | `validateAccess` POST `/access/validate` | ValidateRequest | ValidationResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell | works offline; opens modal first |
| Validate group access (secondary button) | `validateGroupAccess` POST `/access/group-validate` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance | works offline; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Outcome states**: As SCN-003, including accreditation verification for service gates. *(source: F08 step 3 / contracts/spine/access.yaml#validateAccess / contracts/satellite/accreditation.yaml#verifyAccreditationCredential)*

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

**What opens over it**

- confirmDialog *Override access*: **Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A scan ready this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason`, `recordedAt`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The scan ready list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the scan ready untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No scan ready yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the scan ready are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TICKET_LOOKUP`, which `lookupTicket` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Keep working when the network does not.** The screen already had an `offline` state. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 No identifier supplied; 400 Validation failed; 409 Requested count exceeds the remaining group allowance |

#### Edge cases to draw

- **Offline**: Same as SCN-003; validation from the bundle, journal kept. *(source: DI-240)*

#### Consistency with other screens

- Match `SCN-003`: One component for both apps.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outcome:
  state: Admitted
  product: Summit Peaks Annual Pass
  holder: Sara Al Nuaimi
```

#### Permissions

- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff
- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff
- `verifyAccreditationCredential` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `TICKET_LOOKUP`, which `lookupTicket` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

46 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.17 | The system should have the ability to scan a ticket into a POS terminal and display record of ticket’s history: transaction time, clerk, payment method, etc. | Admission and Access | CONTRACTED | `lookupTicket` |
| 1.1.61 | Entitlement validity validation | Ticketing Catalogue | CONTRACTED | `validateAccess` |
| 1.1.62 | Entitlement consumption tracking | Ticketing Catalogue | CONTRACTED | `validateAccess` |
| 3.1.3 | Dynamic Refresh: QR codes refresh periodically (e.g., every 30–60 seconds) to prevent screenshots or duplication. | Admission and Access | CONTRACTED | `validateAccess` |
| 3.2.2 | The Ticketing PLUs shall be printed on E-tickets Ticketing PLUs shall be printed on Wristbands (paper and RFID) | Admission and Access | CONTRACTED | `validateAccess` |
| 3.2.3 | The Ticketing PLUs shall be printed on M-tickets | Admission and Access | CONTRACTED | `validateAccess` |
| 3.2.5 | The ticket id can be generated in 2D barcode The ticket id can be generated in QR code The ticket id can be generated in RFID (ISO 15693) The ticket ID number sequence is created by the sales system … | Admission and Access | CONTRACTED | `validateAccess` |
| 3.2.8 | The system should be able to validate different media types in a transparent way, linear barcode, QR code, RFID and NFC. | Admission and Access | CONTRACTED | `validateAccess` |
| 3.2.12 | The system should be able to support child-protection journey in multiple ways such as: - Require scan of an adult ticket as a pair to a child ticket to enable entry/exit from an attraction - Require … | Admission and Access | CONTRACTED | `validateAccess` |
| 3.2.14 | The system should have the ability to recognize and read the ticket format sold by resellers and external partners. | Admission and Access | CONTRACTED | `validateAccess` |
| 3.2.15 | The system should have the ability to display a reason code on the scanner if the ticket is invalid. A ticket can be manually invalidated by an administrator. | Admission and Access | CONTRACTED | `validateAccess` |
| 3.2.16 | The system should have the ability to scan and check-in at self-service turnstile and access control device. | Admission and Access | CONTRACTED | `validateAccess` |
| … 34 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A separate dedicated scanner app for devices used only for scanning (e.g. mounted at turnstiles/gates) shows only scanning functions; the same validation is also embedded in the employee app. *(agreed · MoM 10 Aug 2026, 5.7 Ticket Scanning / Access Control App · DI-239)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-010` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-010?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Lookup ticket, Override access, Validate access, Validate group access.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `TICKET_LOOKUP`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-004` Task list

**See what is assigned, and what is overdue.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `maintenance` module |
| Block | Block A · task APP-STAFF-EMP-004 |
| Who uses it | venue staff holding `MAINTENANCE_EXECUTE`, `WORK_ORDER_VIEW` (1 operate, 1 read); in the flows as supervisor, technician |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listWorkOrders` reads the population and `getWorkOrder` reads one of them — list, select, act |
| Offline | Local queue. Tasks completed offline sync on return |
| Opens with | `workOrderId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/task-list` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createWorkOrder. **Bulk-attach residue** — the 18 August defect that put identical operation sets on unrelated screens. A till does not cancel a performance, a staff app does not create roles, and **a scanner does not run a cash shift.**

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Bulk-attach residue: the task list carried the whole work-order lifecycle. The list needs Accept and Decline only; doing the work is EMP-005, and Verify … Removed 2 October 2026 (CHG-WIR-001): Bulk-attach residue: the task list carried the whole work-order lifecycle. The list needs Accept and Decline only; doing the work is EMP-005, and Verify … Removed 2 October 2026 (CHG-WIR-001): Bulk-attach residue: the task list carried the whole work-order lifecycle. The list needs Accept and Decline only; doing the work is EMP-005, and Verify …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The technician's and steward's queue on the Staff App: what is assigned to me, what is waiting for someone to take it, and what is overdue, worked one-handed on a phone and offline in a plant room. It is a list that opens a task (EMP-005); it is not where work is done. The one thing to get right: an assigned-but-not-accepted job looks different from an accepted one, and urgent work sits on top regardless of when it arrived, with the work-order timer visible on every card.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The work order has no accepted state or acceptedAt (CHG-SPO-019)

**Fixed on main** (the package already carries these; draw what it says): Filters are text fields "Assigned to principal id", "Status", "Priority", "Asset id"; table titled "Every work order" (CHG-SPO-018); Fourteen lifecycle buttons (verify, close, cancel, complete, parts, time, save, start, pause...) on the list screen (CHG-WIR-001); A steward cannot take an unassigned task although F65 says it appears "for whoever is free" and "accepting is the lock" (CHG-WIR-001); Navigation entry only from EMP-006 and inferred exits to Sign in and Select venue (CHG-WIR-002).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **F65 orders the list "by urgency and proximity", but listWorkOrders has no sort or location parameter and staff devices report no position. Is proximity by zone (the steward's assigned zone first) acceptable?** → Drawn default accepted: Sort by priority, overdue, due time; draw a "My zone first" toggle greyed with "Coming later". *(decided by Chinmay, 2026-10-02; DEC-130 / CHG-NOTE-008)*
- **DI-229 asks for search across tasks and incidents; listWorkOrders has no text search. Is search in scope for wave 1?** → Drawn default accepted: Draw a search icon that searches the cached list on the device (title, asset, number). *(decided by Chinmay, 2026-10-02; DEC-131 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status and priority | select | optional | — | Open · Assigned · In progress · Paused · Awaiting parts · Completed · Verified · Closed · Cancelled | — | Chips from the closed sets; my own queue is the default, not a filter (VO-R12; design-notes correction venue-operations EMP-004). No ids are typed. | `WorkOrder.status` |
| Overdue only | toggle | optional | off | — | — | Sends `?overdueOnly=` to `listWorkOrders`. | `listWorkOrders` ?overdueOnly |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Assigned to principal | picker: choose an assigned to principal | — | — | `listWorkOrders` ?assignedToPrincipalId |
| Status | select | — | Open · Assigned · In progress · Paused · Awaiting parts · Completed · Verified · Closed · Cancelled | `listWorkOrders` ?status |
| Priority | radio group | — | Low · Normal · High · Urgent · Emergency | `listWorkOrders` ?priority |
| Asset | upload, or pick from the media library | — | — | `listWorkOrders` ?assetId |
| From | date and time picker | — | — | `listWorkOrders` ?from |
| To | date and time picker | — | — | `listWorkOrders` ?to |
| Category | picker: choose a category | — | — | `listWorkOrders` ?categoryId |

**Sent by *Reject work order*** (`rejectWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Wrong skill · Not on shift · Wrong venue · Already in hand · Unsafe · Other | — | — | `rejectWorkOrder` body |
| Note `note` | text area | optional | — | max length 300; Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real … | `rejectWorkOrder` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **View switch (replaces the id and text filters)**: Three segments at the top - "Mine" (assigned to me, default), "Available" (open, unassigned, my venue), "Overdue". Status and priority are chips under a filter icon (Open, Assigned, In progress, Paused, Awaiting parts, Completed; Emergency to Low), never text boxes. "Assigned to principal id" and "Asset id" are not drawn; the asset is filtered by scanning its tag. *(source: contracts/satellite/maintenance.yaml#listWorkOrders / DI-229)*
- **Scan to filter**: A scan button in the header resolves the asset by tag (works offline) and shows only that asset's open work orders - the way a technician arriving at a pump finds the job for it. *(source: screens/P06-staff-app.yaml#EMP-004 / contracts/satellite/maintenance.yaml#lookupAsset)*

#### Outputs: what the screen shows and produces

**Shown**

**My work orders** (data table, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |

**The selected work order** (detail panel, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |

**The work order** (detail panel, from `getWorkOrder`)

| Shows | Format | Notes |
|---|---|---|
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Accept work order (primary button) | `acceptWorkOrder` POST `/work-orders/{workOrderId}/accept` | — | WorkOrder | 409 Not assigned to this principal, or already accepted | works offline |
| Reject work order (destructive button) | `rejectWorkOrder` POST `/work-orders/{workOrderId}/reject` | inline | WorkOrder | 400 Validation failed | works offline |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Task card**: Priority badge with its source in small text (Emergency - asset override / High - scored 78 / Normal - manual), title, asset name and location, status step, due time with a red Overdue flag, and the running timer. Two timers are different things: "Open 1 h 12 min" (since raised - the resolution duration DI-231 asks for) on every card, and a pulsing "Working 00:42" only while the labour timer runs (isTimerRunning). Safety-critical assets carry a red Safety tag. *(source: DI-231 / DI-923 / contracts/satellite/maintenance.yaml#/components/schemas/WorkOrder)*
- **Assigned but not accepted**: Cards assigned to me that I have not accepted show an outlined style with "New - accept or decline" and the two buttons on the card itself; accepted work is drawn solid. The gap between assigned and accepted is the point of the accept step. *(source: contracts/satellite/maintenance.yaml#acceptWorkOrder / MATRIX 18.2.2)*
- **Sort order**: Emergency and Urgent first, then overdue, then due time; never by arrival. Within equal priority, the work nearest to me where location allows (see decisions). *(source: F65 step 2 / contracts/satellite/maintenance.yaml#getDueMaintenance)*
- **Sync strip**: Offline, a persistent strip "Offline - 3 actions waiting to sync, list from 10:12"; cards changed offline carry a small clock icon until the server confirms them. *(source: screens/P06-staff-app.yaml#EMP-004)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Accept (on card or swipe right)**: Commits me to the job; the card turns solid and moves into "Mine". Works offline and is confirmed on sync; a 409 on sync ("already accepted by Omar Haddad") turns the card grey with that name. *(source: contracts/satellite/maintenance.yaml#acceptWorkOrder / F65 step 3)*
- **Decline (on card or swipe left)**: Opens a bottom sheet with the closed reason list (Wrong skill, Not on shift, Wrong venue, Already being done, Unsafe, Other); Other requires a note (max 300) before Send is enabled. The job returns to Available for someone else - it is never cancelled from here. *(source: contracts/satellite/maintenance.yaml#rejectWorkOrder / DI-231)*
- **Tap a card**: Opens the task (EMP-005) with the work order id; the list keeps its scroll position on return. *(source: screens/P06-staff-app.yaml#EMP-004)*
- **Raise (floating + button)**: Opens Raise a task (EMP-006); the new task appears at the top of Available or Mine on return. *(source: F65 step 1 / DI-230)*

**Data it reads**: `listWorkOrders` (onLoad, List work orders)

**Where the user goes next**

- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-005` Task detail: *Completes a task*; carries `workOrderId`

**What opens over it**

- confirmDialog *Reject work order*: **Names what `rejectWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task list this affects should be identified in the dialog, not just counted. **Collects what `rejectWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The task list list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the task list untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No task list yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on assignedToPrincipalId, status, priority, assetId, overdueOnly and the task list are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORK_ORDER_VIEW`, which `listWorkOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MAINTENANCE_EXECUTE` for `acceptWorkOrder`, `rejectWorkOrder`. |
| Offline (`?state=offline`) | Local queue. Tasks completed offline sync on return |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Not assigned to this principal, or already accepted |

#### Edge cases to draw

- **Offline at shift start**: The cached list is shown with its age; Accept, Decline and opening a task all work offline; the Available segment says "May be out of date - someone else may have taken these". *(source: contracts/satellite/maintenance.yaml#listWorkOrders)*
- **Two people take the same available task**: The second gets "Taken by Maria Santos at 10:14" and the card leaves Available; nothing is lost. *(source: F65 step 3 / contracts/satellite/maintenance.yaml#acceptWorkOrder)*
- **Steward without maintenance rights**: Sees their own raised and assigned tasks; Decline and Accept still work (MAINTENANCE_EXECUTE); supervisor-only actions are absent on this screen rather than disabled. *(source: contracts/satellite/maintenance.yaml#acceptWorkOrder)*
- **Nothing assigned**: Empty state "Nothing assigned to you" with a link to the Available segment and its count. *(source: designer default)*

#### Consistency with other screens

- Match `BO-070`: Same status names, priority badge plus source, and timer as the back-office work order desk; a card here and a row there must read identically.
- Match `EMP-048`: A failed opening-checklist item raises a work order that appears here at the top with the inspection named as source.
- Match `EMP-007`: Open and paused tasks at shift end feed the generated handover (F65 step 5); draw a "Will carry into handover" tag on paused cards.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
mine:
- wo: WO-2026-01482
  title: Restraint bar R3 not locking
  asset: Falcon Coaster
  priority: Emergency - asset override
  status: In progress
  open: 1 h 12 min
  working: 00:42
  safety: true
- wo: WO-2026-01490
  title: Gate 2 reader intermittent
  asset: Main Plaza Gate 2 turnstile
  priority: High - scored 78
  status: Assigned - not accepted
  due: 1 Oct 2026 14:00
available:
- wo: WO-2026-01495
  title: Water on floor by Wave Rider exit stairs
  location: Aqua Park, Wave Rider exit
  priority: Urgent - scored 64
  raisedBy: Maria Santos
  open: 6 min
```

#### Permissions

- `listWorkOrders` → `WORK_ORDER_VIEW` (read) · staff
- `acceptWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `rejectWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `getWorkOrder` → `WORK_ORDER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WORK_ORDER_VIEW`, which `listWorkOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MAINTENANCE_EXECUTE` for `acceptWorkOrder`, `rejectWorkOrder`.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 18.2.1 | Work Order Inbox - Users shall view assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.2 | Work Order Acceptance - Users shall accept assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.3 | Work Order Rejection - Users shall reject assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.4 | Work Order Start - Users shall start work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.5 | Work Order Pause - Users shall pause work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.6 | Work Order Completion - Users shall complete work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.7 | Work Order Closure - Authorized users shall close work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 17.4.8 | Work Order Audit Trail - System shall maintain work order audit logs. | Maintenance & Safety Management | CONTRACTED | `getWorkOrder` |
| 17.3.4 | Root Cause Analysis - System shall support root cause analysis. | Maintenance & Safety Management | CONTRACTED | data `WorkOrder` |
| 17.3.5 | Maintenance Escalation - System shall support maintenance escalation workflows. | Maintenance & Safety Management | CONTRACTED | data `WorkOrder` |
| 17.3.6 | Downtime Tracking - System shall track equipment downtime. | Maintenance & Safety Management | CONTRACTED | data `WorkOrder` |
| 17.4.5 | Work Order Escalation - System shall support work order escalations. | Maintenance & Safety Management | CONTRACTED | data `WorkOrder` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Work orders assigned to a technician must be visible on a technician-facing mobile app so field staff see assigned tasks and act directly from their device; execution shows a repair checklist, spare parts/tools consumed, a timeline (assigned, started, part requests) and a functional-test checklist before completion. *(client request · MoM 17 Sep 2026, 4.4 Work Order Management & Execution · DI-911)*
- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*
- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*
- Tasks are logged with priority and scheduled date/time; work order lifecycle Created → Assigned → In progress → Review → Closed with a timer showing resolution duration. *(client request · MoM 10 Aug 2026, 5.3 Task, Work Order & Asset Management · DI-231)*
- Notifications categorised by type — action-required vs purely informational — and search across tasks and incidents. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-229)*
- In-system task assignment between staff (e.g. a cashier flagging something for a supervisor) without email or messaging apps. *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-159)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-004` · status **notStarted** · provenance generated
- Flow F08 *Steward works a shift on the employee app*, step 5: Works the task list → Assigned and available work
- Flow F12 *Asset fails and closes a queue*, step 2: Technician picks up the work order → Assigned, with the asset history attached
- Flow F65 *A task is raised, worked and handed over*, step 2: It appears on the list for whoever is free. → **Ordered by urgency and proximity**, not by arrival — a spill on the concourse outranks a bulb in a store room raised an hour earlier.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-004?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Accept work order, Reject work order.
- [ ] Every transition is wired: `EMP-003`, `EMP-005`.
- [ ] Every gated control is gated: `MAINTENANCE_EXECUTE`, `WORK_ORDER_VIEW`.
- [ ] The 6 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-005` Task detail

**Do the task and record that it was done.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `maintenance` module |
| Block | Block A · task APP-STAFF-EMP-005 |
| Who uses it | venue staff holding `MAINTENANCE_EXECUTE`, `PROCUREMENT_REQUEST`, `PRODUCT_VIEW`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VIEW` (2 operate, 2 read, 1 configure); in the flows as supervisor, technician |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listWorkOrders` reads the population and `getWorkOrder` reads one of them — list, select, act |
| Offline | Editable offline. Findings and photos queue |
| Opens with | `workOrderId` (deepLink), `stockReservationId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/task-detail` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Cross-platform navigation removed 24 August**: BO-030, BO-078. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Removed 24 August**: createWorkOrder. **Bulk-attach residue** — the 18 August defect that put identical operation sets on unrelated screens. A till does not cancel a performance, a staff app does not create roles, and **a scanner does not run a cash shift.**

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): Verify, Close, Cancel and Save (reassign, reprioritise) are supervisor acts (the verifier may not be the technician); they belong to BO-030 and BO-070, not the … Removed 2 October 2026 (CHG-WIR-001): Verify, Close, Cancel and Save (reassign, reprioritise) are supervisor acts (the verifier may not be the technician); they belong to BO-030 and BO-070, not the … Removed 2 October 2026 (CHG-WIR-001): Verify, Close, Cancel and Save (reassign, reprioritise) are supervisor acts (the verifier may not be the technician); they belong to BO-030 and BO-070, not the …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The task itself on the Staff App: the technician (or steward for a simple task) accepts, starts, works, records what they found, the parts and the time, attaches before and after evidence, and completes - offline if the plant room has no signal. Completion is "work done", never "asset back in service"; a supervisor verifies and returns the asset elsewhere. The one thing to get right: the screen follows the job's state, showing only the next sensible actions (Accept > Start > Pause/Complete), with evidence capture one tap away throughout.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Two ways to pause with two different reason lists (CHG-SPO-019)
- recordWorkOrderTime requires `id` in the body (CHG-SPO-019)
- Complete, Record parts and Record time need WORK_ORDER_MANAGE while Accept/Start/Pause need MAINTENANCE_EXECUTE (CHG-SPO-019)
- No repair checklist or functional-test checklist on a work order (CHG-SPO-019)

**Fixed on main** (the package already carries these; draw what it says): Verify, Close, Cancel and Save (reassign, reprioritise) on the technician's task screen (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **The pack's field actions include Acknowledge, Travelling and Arrived before Start. Are these needed, or is Accept then Start enough?** → Drawn default accepted: Draw Accept and Start only; Travelling/Arrived not drawn. *(decided by Chinmay, 2026-10-02; DEC-132 / CHG-NOTE-008)*
- **Should the functional-test checklist be an inspection template attached to the work order's category?** → Drawn default accepted: Draw a "Checks" section with pass/fail items above Complete, greyed "Not configured for this job" when empty. *(decided by Chinmay, 2026-10-02; DEC-133 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Assigned to principal id | picker: choose an assigned to principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?assignedToPrincipalId=` to `listWorkOrders`. | `listWorkOrders` ?assignedToPrincipalId |
| Status | select | optional | — | Open · Assigned · In progress · Paused · Awaiting parts · Completed · Verified · Closed · Cancelled | — | Sends `?status=` to `listWorkOrders`. | `listWorkOrders` ?status |
| Priority | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | Sends `?priority=` to `listWorkOrders`. | `listWorkOrders` ?priority |
| Asset id | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | Sends `?assetId=` to `listWorkOrders`. | `listWorkOrders` ?assetId |
| Overdue only | toggle | optional | off | — | — | Sends `?overdueOnly=` to `listWorkOrders`. | `listWorkOrders` ?overdueOnly |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listWorkOrders` ?from |
| To | date and time picker | — | — | `listWorkOrders` ?to |
| Category | picker: choose a category | — | — | `listWorkOrders` ?categoryId |

**Form: Start work order** (modal, opened by *Start work order*; *Start work order* calls `startWorkOrder`, *Cancel* sends nothing)

**Collects what `startWorkOrder` sends before it is called.** Nothing in the body is required. Optional: `startedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Started at `startedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time where the job began offline. The server records both. | `startWorkOrder` body |

**Form: Pause work order** (modal, opened by *Pause work order*; *Pause work order* calls `pauseWorkOrder`, *Cancel* sends nothing)

**Collects what `pauseWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`, `requisitionId`. **When the reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Awaiting parts · Awaiting permit · Awaiting outage window · Awaiting specialist · End of shift · Safety concern · Other | — | — | `pauseWorkOrder` body |
| Note `note` | text area | optional | — | max length 300; Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real … | `pauseWorkOrder` body |
| Requisition `requisitionId` | picker: choose a requisition | optional | — | — | shows names, sends the id | Where a part was ordered, so the two are linked. | `pauseWorkOrder` body |

Errors to draw in the form: 400 Validation failed

**Form: Complete work order** (modal, opened by *Complete work order*; *Complete work order* calls `completeWorkOrder`, *Cancel* sends nothing)

**Collects what `completeWorkOrder` sends before it is called.** Required: `resolution`, `recordedAt`. Optional: `resolutionCode`, `attachmentRefs`, `followUpRequired`, `followUpNote`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Resolution `resolution` | text area | required | — | min length 3; max length 5000 | — | — | `completeWorkOrder` body |
| Resolution code `resolutionCode` | select | optional | — | Repaired · Part replaced · Adjusted · Cleaned · No fault found · Referred external · Replaced · Deferred | — | — | `completeWorkOrder` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `completeWorkOrder` body |
| Follow up required `followUpRequired` | toggle | optional | off | — | — | — | `completeWorkOrder` body |
| Follow up note `followUpNote` | text area | optional | — | max length 1000 | — | — | `completeWorkOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `completeWorkOrder` body |

Errors to draw in the form: 400 Completion photographs required for this category and none supplied

**Form: Attach work order evidence** (modal, opened by *Attach work order evidence*; *Attach work order evidence* calls `attachWorkOrderEvidence`, *Cancel* sends nothing)

**Collects what `attachWorkOrderEvidence` sends before it is called.** Required: `kind`. Optional: `assetRef`, `text`, `capturedAt`, `stage`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Photo · Video · Document · Note · Signature | — | — | `attachWorkOrderEvidence` body |
| Asset ref `assetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | In the media store | `attachWorkOrderEvidence` body |
| Text `text` | text area | optional | — | max length 4000 | — | Where the kind is a note | `attachWorkOrderEvidence` body |
| Captured at `capturedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `attachWorkOrderEvidence` body |
| Stage `stage` | radio group | optional | — | Before · During · After · Sign off | — | — | `attachWorkOrderEvidence` body |

**Form: Record work order parts** (modal, opened by *Record work order parts*; *Record work order parts* calls `recordWorkOrderParts`, *Cancel* sends nothing)

**Collects what `recordWorkOrderParts` sends before it is called.** Required: `lines`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `recordWorkOrderParts` body |
| Inventory item `lines[].inventoryItemId` | picker: choose an inventory item | required | — | — | shows names, sends the id | — | `recordWorkOrderParts` body |
| Quantity `lines[].quantity` | number field | required | — | min 0 | — | — | `recordWorkOrderParts` body |
| Location `lines[].locationId` | picker: choose a location | optional | — | — | shows names, sends the id | — | `recordWorkOrderParts` body |

Errors to draw in the form: 409 Insufficient stock

**Form: Record work order time** (modal, opened by *Record work order time*; *Record work order time* calls `recordWorkOrderTime`, *Cancel* sends nothing)

**Collects what `recordWorkOrderTime` sends before it is called.** Required: `id`, `action`, `recordedAt`. Optional: `pauseReason`, `note`. **When the pause reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `recordWorkOrderTime` body |
| Action `action` | radio group | required | — | Start · Pause · Resume · Stop | — | — | `recordWorkOrderTime` body |
| Pause reason `pauseReason` | select | optional | — | Awaiting parts · Awaiting access · Awaiting approval · End of shift · Reassigned · Other | — | — | `recordWorkOrderTime` body |
| Note `note` | text area | optional | — | max length 500; Required where the pause reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the pause reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones … | `recordWorkOrderTime` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordWorkOrderTime` body |

Errors to draw in the form: 400 Validation failed; 409 Action inconsistent with the current timer state

**Sent by *Reject work order*** (`rejectWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Wrong skill · Not on shift · Wrong venue · Already in hand · Unsafe · Other | — | — | `rejectWorkOrder` body |
| Note `note` | text area | optional | — | max length 300; Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real … | `rejectWorkOrder` body |

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

**Sent by *Release reserved parts*** (`releaseStockReservation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 300 | — | — | `releaseStockReservation` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Start**: One big Start button; if the asset has a tag, offer "Scan the asset to confirm" first (pack: correct asset confirmed where many similar assets stand together). startedAt is the device time, sent even when offline; never asked. *(source: screens/P06-staff-app.yaml#EMP-005 / contracts/satellite/maintenance.yaml#startWorkOrder)*
- **Pause reason**: Bottom sheet with the closed list Awaiting parts, Awaiting permit, Awaiting outage window, Awaiting specialist, End of shift, Safety concern, Other (note required, max 300). Awaiting parts moves the job to Awaiting parts and offers "Link the requisition"; all others to Paused. One Pause button only (see corrections on the second timer). *(source: contracts/satellite/maintenance.yaml#pauseWorkOrder / F15 step 1)*
- **Evidence**: Camera opens directly; each capture is tagged Before / During / After / Sign-off by the job state (Before until Start, During while in progress, After at completion) and can be changed. Video, document, note and signature are in a "More" menu. Captures queue offline with a thumbnail and a clock icon. *(source: contracts/satellite/maintenance.yaml#attachWorkOrderEvidence / MATRIX 18.5.1 / DI-232)*
- **Parts used**: Pre-listed from the parts reserved for this job (from the work order's parts with reservedQuantity) with a stepper for quantity used; "Add a part" searches the inventory item list. Hidden offline with "Parts are recorded when you are back online" (stock moves in real time). *(source: contracts/satellite/maintenance.yaml#recordWorkOrderParts / DI-925 / TRACKER Actions row 304)*
- **Complete**: A completion sheet - Resolution code as chips (Repaired, Part replaced, Adjusted, Cleaned, No fault found, Referred to vendor, Replaced, Deferred), resolution text (required, max 5000), completion photos (required where the category demands; the sheet says so before the camera opens), "Follow-up needed" toggle revealing a note (max 1000). recordedAt is the device time, never asked. *(source: contracts/satellite/maintenance.yaml#completeWorkOrder / MATRIX 17.4.6)*

#### Outputs: what the screen shows and produces

**Shown**

**Every work order** (data table, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |

**The selected work order** (detail panel, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |

**The work order** (detail panel, from `getWorkOrder`)

| Shows | Format | Notes |
|---|---|---|
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |

**Parts reserved for this task** (data table, from `listStockReservations`): **Reserved in the general inventory** (decided 17 September, M17-02), `sourceType` workOrder. *Record work order parts* issues from the reservation first. Needs signal: stock depletes in real time, so the reserve action is hidden offline.

| Shows | Format | Notes |
|---|---|---|
| Item | the name it points at, never the id | — |
| Quantity | 1,234.5 | — |
| Status | chip: Active, Consumed, Released, Expired | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Start work order (primary button) | `startWorkOrder` POST `/work-orders/{workOrderId}/start` | inline | WorkOrder | — | works offline; opens modal first |
| Pause work order (secondary button) | `pauseWorkOrder` POST `/work-orders/{workOrderId}/pause` | inline | WorkOrder | 400 Validation failed | works offline; opens modal first |
| Complete work order (secondary button) | `completeWorkOrder` POST `/work-orders/{workOrderId}/complete` | inline | WorkOrder | 400 Completion photographs required for this category and none supplied | works offline; opens modal first |
| Accept work order (secondary button) | `acceptWorkOrder` POST `/work-orders/{workOrderId}/accept` | — | WorkOrder | 409 Not assigned to this principal, or already accepted | works offline |
| Attach work order evidence (secondary button) | `attachWorkOrderEvidence` POST `/work-orders/{workOrderId}/attachments` | inline | WorkOrderAttachment | — | works offline; opens modal first |
| Record work order parts (secondary button) | `recordWorkOrderParts` POST `/work-orders/{workOrderId}/parts` | inline | WorkOrderDetail | 409 Insufficient stock | opens modal first |
| Record work order time (secondary button) | `recordWorkOrderTime` POST `/work-orders/{workOrderId}/time` | inline | WorkOrder | 400 Validation failed; 409 Action inconsistent with the current timer state | works offline; opens modal first |
| Reject work order (destructive button) | `rejectWorkOrder` POST `/work-orders/{workOrderId}/reject` | inline | WorkOrder | 400 Validation failed | works offline |
| Resume work order (secondary button) | `resumeWorkOrder` POST `/work-orders/{workOrderId}/resume` | — | WorkOrder | — | works offline |
| Reserve parts (secondary button) | `createStockReservation` POST `/stock-reservations` | InventoryStockReservation | InventoryStockReservation | 400 Validation failed; 409 Not enough free stock at the location. | — |
| Release reserved parts (secondary button) | `releaseStockReservation` POST `/stock-reservations/{stockReservationId}/release` | inline | InventoryStockReservation | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The reservation is not `active`. | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Header**: Work order number, priority badge with source, asset name and location, status step, the two timers (Open since raised; Working while the labour timer runs) and the due time. Safety instructions from the asset's SOP document pinned under the header for safety-critical assets. *(source: screens/P06-staff-app.yaml#EMP-005 / contracts/satellite/maintenance.yaml#getWorkOrder / DI-231)*
- **Asset panel**: Tap the asset to open its documents (manual, SOP, drawings) and the last five history entries - "Assigned, with the asset history attached". Documents open offline only if cached. *(source: F12 step 2 / contracts/satellite/maintenance.yaml#getAsset)*
- **Timeline**: Raised, Assigned, Accepted, Started, Paused (reason), Part reserved, Part issued, Completed - each with time and name, newest at the bottom; offline entries marked "on device 10:12, synced 10:40". *(source: screens/P06-staff-app.yaml#EMP-005 / DI-911 / MATRIX 17.4.8)*
- **Parts reserved**: Part name, quantity reserved, used so far, status (Reserved, Issued, Released, Expired). Read from the work order so it shows offline; the inventory list is the online refresh. *(source: contracts/satellite/maintenance.yaml#/components/schemas/WorkOrderDetail / DI-925)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Accept / Decline**: Shown only while the job is assigned to me and not accepted; same behaviour as on EMP-004. *(source: contracts/satellite/maintenance.yaml#acceptWorkOrder / contracts/satellite/maintenance.yaml#rejectWorkOrder)*
- **Start / Pause / Resume**: Start begins the labour clock; Pause stops it with a reason; Resume (from Paused or Awaiting parts) restarts it. All offline-capable and timestamped on the device; the server keeps both device and server time. *(source: contracts/satellite/maintenance.yaml#startWorkOrder / contracts/satellite/maintenance.yaml#resumeWorkOrder / MATRIX 18.2.5)*
- **Reserve parts**: Pick part, store and quantity; a 409 names the part and the free quantity ("Seal kit SK-24 - only 0 free at Aqua Park plant store"), with "Request a transfer" and "Raise a requisition". Hidden offline, not greyed - per the 17 September decision. *(source: DI-925 / contracts/satellite/inventory.yaml#createStockReservation / F15 step 1)*
- **Release reserved parts**: Asks for a short reason; offered when the job is completed or paused with reserved parts unused. *(source: contracts/satellite/inventory.yaml#releaseStockReservation)*
- **Complete**: Moves to Completed - awaiting verification; the screen then reads "Done - a supervisor will verify. The asset stays out of service until then." with no button to put it back in service. *(source: contracts/satellite/maintenance.yaml#completeWorkOrder / F12 step 3)*

**Data it reads**: `listWorkOrders` (onLoad, List work orders)

**Where the user goes next**

- → `EMP-007` Handover notes: *Writes handover notes*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `BO-078` Requisitions: *Raises a requisition against the work order*; calls `pauseWorkOrder`
- → `BO-030` Work Order Verification: *Supervisor verifies*; carries `workOrderId`; calls `completeWorkOrder`

**What opens over it**

- confirmDialog *Reject work order*: **Names what `rejectWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task this affects should be identified in the dialog, not just counted. **Collects what `rejectWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The task list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the task untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No task yet. Offers Record work order parts (`recordWorkOrderParts`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on assignedToPrincipalId, status, priority, assetId, overdueOnly and the task are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORK_ORDER_VIEW`, which `listWorkOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MAINTENANCE_EXECUTE` for `startWorkOrder`, `pauseWorkOrder`, `acceptWorkOrder`, `attachWorkOrderEvidence` and 2 more; `PROCUREMENT_REQUEST` for … |
| Offline (`?state=offline`) | Editable offline. Findings and photos queue |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Completion photographs required for this category and none supplied; 400 Validation failed; 409 Action inconsistent with the current timer state; 409 Insufficient stock |

#### Edge cases to draw

- **Completing offline**: Allowed (completion is offline-capable); parts cannot be recorded offline, so the sheet warns "2 parts not yet recorded - they will be asked for when you reconnect" and keeps a reminder on the card. *(source: contracts/satellite/maintenance.yaml#completeWorkOrder / contracts/satellite/maintenance.yaml#recordWorkOrderParts)*
- **Parts recorded on reconnect but stock has gone**: The 409 is shown on the job as "Part not issued - Seal kit SK-24 out of stock" with Request transfer; the completion stands. *(source: contracts/satellite/maintenance.yaml#recordWorkOrderParts)*
- **Safety-critical job completed without after-photos**: Complete is refused before sending with "This job needs completion photos" and the camera opens. *(source: contracts/satellite/maintenance.yaml#completeWorkOrder / MATRIX 17.4.6)*
- **Second fault found during the work**: "Raise a linked task" opens EMP-006 pre-filled with the asset; the original job is not expanded. *(source: F12 step 3)*
- **Supervisor rejected the completion**: The job comes back In progress with a banner showing the verifier's note at the top. *(source: contracts/satellite/maintenance.yaml#verifyWorkOrder)*

#### Consistency with other screens

- Match `BO-578`: The back-office Technician Repair Workspace is this screen at desk width; same states, buttons, evidence stages and checklist.
- Match `BO-030`: The evidence stages, resolution code and parts captured here are exactly what the verifier sees; use the same labels.
- Match `EMP-007`: A job paused with End of shift is listed in the generated handover.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
workOrder:
  wo: WO-2026-01482
  title: Restraint bar R3 not locking
  asset: Falcon Coaster (AP-RIDE-0007), Adventure Zone Bay 3
  priority: Emergency - asset override
  status: In progress
  open: 1 h 12 min
  working: 00:42
  technician: Rahul Menon
  timeline:
  - 09:58 Raised by Ahmed Al Mansoori (from the opening checklist)
  - 10:01 Assigned to Rahul Menon by Fatima Al Hashimi
  - 10:02 Accepted
  - 10:09 Started (asset scanned)
  - 10:31 Part reserved - Restraint latch spring LS-40 x2
  parts:
  - part: Restraint latch spring LS-40
    reserved: 2
    used: 1
    status: Reserved
  resolution: Latch spring fatigued; replaced, lock tested 20 cycles.
  resolutionCode: Part replaced
```

#### Permissions

- `listStockReservations` → `PRODUCT_VIEW` (read) · staff
- `createStockReservation` → `PROCUREMENT_REQUEST` (operate) · staff
- `releaseStockReservation` → `PROCUREMENT_REQUEST` (operate) · staff
- `getWorkOrder` → `WORK_ORDER_VIEW` (read) · staff
- `startWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `pauseWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `completeWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `acceptWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `attachWorkOrderEvidence` → `MAINTENANCE_EXECUTE` (operate) · staff
- `listWorkOrders` → `WORK_ORDER_VIEW` (read) · staff
- `recordWorkOrderParts` → `WORK_ORDER_MANAGE` (configure) · staff
- `recordWorkOrderTime` → `WORK_ORDER_MANAGE` (configure) · staff
- `rejectWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `resumeWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `WORK_ORDER_VIEW`, which `listWorkOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MAINTENANCE_EXECUTE` for `startWorkOrder`, `pauseWorkOrder`, `acceptWorkOrder`, `attachWorkOrderEvidence` and 2 more; `PROCUREMENT_REQUEST` for …

#### Requirements it meets

22 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.4.8 | Work Order Audit Trail - System shall maintain work order audit logs. | Maintenance & Safety Management | CONTRACTED | `getWorkOrder` |
| 18.2.1 | Work Order Inbox - Users shall view assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.2 | Work Order Acceptance - Users shall accept assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.3 | Work Order Rejection - Users shall reject assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.4 | Work Order Start - Users shall start work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.5 | Work Order Pause - Users shall pause work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.6 | Work Order Completion - Users shall complete work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.7 | Work Order Closure - Authorized users shall close work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.5.1 | Photo Capture - Users shall capture photos. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.2 | Video Capture - Users shall capture videos. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.3 | Document Upload - Users shall upload documents. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.4 | Notes Management - Users shall record notes. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| … 10 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Work-order parts are reserved in the general inventory; the reserve action is hidden offline, and a refusal for short stock names the part. *(agreed · MoM 17 Sep 2026, M17-02 · DI-925)*
- Work orders assigned to a technician must be visible on a technician-facing mobile app so field staff see assigned tasks and act directly from their device; execution shows a repair checklist, spare parts/tools consumed, a timeline (assigned, started, part requests) and a functional-test checklist before completion. *(client request · MoM 17 Sep 2026, 4.4 Work Order Management & Execution · DI-911)*
- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*
- Tasks are logged with priority and scheduled date/time; work order lifecycle Created → Assigned → In progress → Review → Closed with a timer showing resolution duration. *(client request · MoM 10 Aug 2026, 5.3 Task, Work Order & Asset Management · DI-231)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-005` · status **notStarted** · provenance generated
- Flow F08 *Steward works a shift on the employee app*, step 6: Completes a task → With findings, not just a tick
- Flow F12 *Asset fails and closes a queue*, step 3: Works and records findings → Parts and time recorded. Completed, not yet in service
- Flow F15 *A part is needed and ordered*, step 1: Pauses the work order, reason: awaiting parts → **The reason decides the state.** awaitingParts is chased by ordering; paused is chased by asking someone
- Flow F15 *A part is needed and ordered*, step 5: The technician resumes → The part is consumed and the movement posts
- Flow F65 *A task is raised, worked and handed over*, step 3: Someone accepts it and works it. → **Accepting is the lock.** Two stewards walking to the same task is the failure the list exists to prevent.
- Flow F65 *A task is raised, worked and handed over*, step 4: It is completed with evidence. → **A photograph closes a spill; a signature closes an inspection.** The evidence kind is the task kind.
- Flow F08 branch at step 6 (requiresStaff): when Task is a safety incident, EMP-026 and EMP-027. A different severity, a different escalation, and it must reach a supervisor rather than sit in a list.
- Flow F08 branch at step 6 (recoverable): when Task needs a part that is not in stock, Blocks on awaitingParts rather than paused. **The distinction matters** — one is a person, the other is supply, and only one is chased by ordering something.
- Flow F12 branch at step 3 (requiresStaff): when Part not in stock, Blocks on awaitingParts, and a requisition is raised. **The queue stays closed** — an asset waiting for a part is not an asset in service.
- Flow F12 branch at step 3 (recoverable): when Technician has no signal in the plant room, Findings queue locally. The work order state moves on sync, and the queue stays closed until it does.
- Flow F12 branch at step 3 (recoverable): when Second fault found during the work, A new work order linked to the first rather than expanding the original. The asset history has to show both.

#### Acceptance for the design

- [ ] Every input above is drawn (40), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-005?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Start work order, Pause work order, Complete work order, Accept work order, Attach work order evidence, Record work order parts, Record work order time, Reject work order, Resume work order, Reserve parts, Release reserved parts.
- [ ] Every transition is wired: `EMP-007`, `EMP-001`, `EMP-002`, `EMP-003`, `BO-078`, `BO-030`.
- [ ] Every gated control is gated: `MAINTENANCE_EXECUTE`, `PROCUREMENT_REQUEST`, `PRODUCT_VIEW`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 5 edge case(s) from the process notes are drawn.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-006` Raise a task

**Report something without finding a manager.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `maintenance` module |
| Block | Block D · task APP-STAFF-EMP-006 |
| Who uses it | venue staff holding `MAINTENANCE_APPROVE`, `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VERIFY`, `WORK_ORDER_VIEW` (3 operate, 1 configure, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listWorkOrders` reads the population and `getWorkOrder` reads one of them — list, select, act |
| Offline | Queues locally. A task raised in a plant room must not need signal |
| Opens with | `workOrderId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/raise-a-task` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Raise a task from where the problem is, in seconds: a steward sees water on the stairs, a cashier sees a dead turnstile, a technician finds a leaking valve. Photo first, then what and where, then send - offline if need be; priority is scored, not guessed. The one thing to get right: it is short enough that people actually use it (scan or photo, pick a fault, one line, Send), and a fault on a live ride can take the ride out of service in the same act.

**Known correction pending (do not draw the wrong version)**

- **Raise screen carries the full list-and-detail (id filters, table of every work order, accept, verify, close, cancel, parts, time)** Why: F65's own note says createWorkOrder sits only on the raise screen and the lifecycle elsewhere; the raise screen needs createWorkOrder, lookupAsset and attachWorkOrderEvidence only. *(source: F65 step 1 / screens/P06-staff-app.yaml#EMP-006; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **createWorkOrder requires WORK_ORDER_MANAGE although "raised by anyone - a cashier who noticed a broken turnstile"** Why: The same permission cancels, reassigns and reprioritises work. Raising needs its own low permission, as incidents have INCIDENT_REPORT. *(source: contracts/satellite/maintenance.yaml#createWorkOrder / contracts/satellite/maintenance.yaml#reportIncident; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **F12 step 1 reports a fault on EMP-026 (Incident report)** Why: A fault is a work order raised here with "take out of service"; an incident is something that happened to a person or place. F12 step 1 should point at EMP-006. *(source: F12 step 1 / contracts/satellite/maintenance.yaml#reportIncident; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Overlay "Create work order" would list id, venueId and recordedAt as required** Why: Device-generated or session values, never inputs (per VO-R03). *(source: contracts/satellite/maintenance.yaml#/components/schemas/CreateWorkOrderRequest; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **DI-230 asks for quick-create of maintenance, IT, cleaning and safety/security requests. Work orders have no trade or team field (WorkOrderKind is corrective/planned/...; categoryId is an asset category). How does a cleaning task reach housekeeping and an IT fault reach IT?** → Drawn default accepted: Draw the kind tiles; route by asset category when an asset is scanned, otherwise to the venue's maintenance queue. *(decided by Chinmay, 2026-10-02; DEC-521 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Assigned to principal id | picker: choose an assigned to principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?assignedToPrincipalId=` to `listWorkOrders`. | `listWorkOrders` ?assignedToPrincipalId |
| Status | select | optional | — | Open · Assigned · In progress · Paused · Awaiting parts · Completed · Verified · Closed · Cancelled | — | Sends `?status=` to `listWorkOrders`. | `listWorkOrders` ?status |
| Priority | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | Sends `?priority=` to `listWorkOrders`. | `listWorkOrders` ?priority |
| Asset id | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | Sends `?assetId=` to `listWorkOrders`. | `listWorkOrders` ?assetId |
| Overdue only | toggle | optional | off | — | — | Sends `?overdueOnly=` to `listWorkOrders`. | `listWorkOrders` ?overdueOnly |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listWorkOrders` ?from |
| To | date and time picker | — | — | `listWorkOrders` ?to |
| Category | picker: choose a category | — | — | `listWorkOrders` ?categoryId |

**Form: Create work order** (modal, opened by *Create work order*; *Create work order* calls `createWorkOrder`, *Cancel* sends nothing)

**Collects what `createWorkOrder` sends before it is called.** Required: `id`, `title`, `venueId`, `priority`, `recordedAt`. Optional: `description`, `assetId`, `locationDescription`, `kind`, `categoryId`, `assignedToPrincipalId`, `dueAt`, `attachmentRefs`, `takeAssetOutOfService`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createWorkOrder` body |
| Title `title` | text field | required | — | max length 200 | — | — | `createWorkOrder` body |
| Description `description` | text area | optional | — | max length 5000 | — | — | `createWorkOrder` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createWorkOrder` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `createWorkOrder` body |
| Location description `locationDescription` | text area | optional | — | max length 500 | — | — | `createWorkOrder` body |
| Kind `kind` | radio group | optional | Corrective | Corrective · Planned · Inspection follow up · Incident corrective · Improvement | — | — | `createWorkOrder` body |
| Priority `priority` | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | Optional since 29 September (M17-01). Sent, it is `manual` and wins. | `createWorkOrder` body |
| Fault assessment `faultAssessment` | group | optional | — | — | — | What the person raising a fault says about it, which the priority score reads (M17-01). | `createWorkOrder` body |
| Safety risk `faultAssessment.safetyRisk` | toggle | optional | off | — | — | — | `createWorkOrder` body |
| Guest impact `faultAssessment.guestImpact` | segmented control | optional | None | None · Degraded · Closed | — | — | `createWorkOrder` body |
| Required qualification codes `requiredQualificationCodes` | list of values (chips) | optional | — | at most 10 | — | Skills the job needs, as qualification codes; `suggestWorkOrderAssignee` ranks by them (M17-13). | `createWorkOrder` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `createWorkOrder` body |
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | — | `createWorkOrder` body |
| Due at `dueAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createWorkOrder` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | Photo-first. Expected at creation, not added later from memory. | `createWorkOrder` body |
| Take asset out of service `takeAssetOutOfService` | toggle | optional | off | — | — | Raise and immediately suspend the asset. For a fault found on a live ride, the two are one action. | `createWorkOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createWorkOrder` body |

Errors to draw in the form: 400 Validation failed

**Form: Attach work order evidence** (modal, opened by *Attach work order evidence*; *Attach work order evidence* calls `attachWorkOrderEvidence`, *Cancel* sends nothing)

**Collects what `attachWorkOrderEvidence` sends before it is called.** Required: `kind`. Optional: `assetRef`, `text`, `capturedAt`, `stage`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Photo · Video · Document · Note · Signature | — | — | `attachWorkOrderEvidence` body |
| Asset ref `assetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | In the media store | `attachWorkOrderEvidence` body |
| Text `text` | text area | optional | — | max length 4000 | — | Where the kind is a note | `attachWorkOrderEvidence` body |
| Captured at `capturedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `attachWorkOrderEvidence` body |
| Stage `stage` | radio group | optional | — | Before · During · After · Sign off | — | — | `attachWorkOrderEvidence` body |

**Form: Complete work order** (modal, opened by *Complete work order*; *Complete work order* calls `completeWorkOrder`, *Cancel* sends nothing)

**Collects what `completeWorkOrder` sends before it is called.** Required: `resolution`, `recordedAt`. Optional: `resolutionCode`, `attachmentRefs`, `followUpRequired`, `followUpNote`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Resolution `resolution` | text area | required | — | min length 3; max length 5000 | — | — | `completeWorkOrder` body |
| Resolution code `resolutionCode` | select | optional | — | Repaired · Part replaced · Adjusted · Cleaned · No fault found · Referred external · Replaced · Deferred | — | — | `completeWorkOrder` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `completeWorkOrder` body |
| Follow up required `followUpRequired` | toggle | optional | off | — | — | — | `completeWorkOrder` body |
| Follow up note `followUpNote` | text area | optional | — | max length 1000 | — | — | `completeWorkOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `completeWorkOrder` body |

Errors to draw in the form: 400 Completion photographs required for this category and none supplied

**Form: Pause work order** (modal, opened by *Pause work order*; *Pause work order* calls `pauseWorkOrder`, *Cancel* sends nothing)

**Collects what `pauseWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`, `requisitionId`. **When the reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Awaiting parts · Awaiting permit · Awaiting outage window · Awaiting specialist · End of shift · Safety concern · Other | — | — | `pauseWorkOrder` body |
| Note `note` | text area | optional | — | max length 300; Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real … | `pauseWorkOrder` body |
| Requisition `requisitionId` | picker: choose a requisition | optional | — | — | shows names, sends the id | Where a part was ordered, so the two are linked. | `pauseWorkOrder` body |

Errors to draw in the form: 400 Validation failed

**Form: Record work order parts** (modal, opened by *Record work order parts*; *Record work order parts* calls `recordWorkOrderParts`, *Cancel* sends nothing)

**Collects what `recordWorkOrderParts` sends before it is called.** Required: `lines`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `recordWorkOrderParts` body |
| Inventory item `lines[].inventoryItemId` | picker: choose an inventory item | required | — | — | shows names, sends the id | — | `recordWorkOrderParts` body |
| Quantity `lines[].quantity` | number field | required | — | min 0 | — | — | `recordWorkOrderParts` body |
| Location `lines[].locationId` | picker: choose a location | optional | — | — | shows names, sends the id | — | `recordWorkOrderParts` body |

Errors to draw in the form: 409 Insufficient stock

**Form: Record work order time** (modal, opened by *Record work order time*; *Record work order time* calls `recordWorkOrderTime`, *Cancel* sends nothing)

**Collects what `recordWorkOrderTime` sends before it is called.** Required: `id`, `action`, `recordedAt`. Optional: `pauseReason`, `note`. **When the pause reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `recordWorkOrderTime` body |
| Action `action` | radio group | required | — | Start · Pause · Resume · Stop | — | — | `recordWorkOrderTime` body |
| Pause reason `pauseReason` | select | optional | — | Awaiting parts · Awaiting access · Awaiting approval · End of shift · Reassigned · Other | — | — | `recordWorkOrderTime` body |
| Note `note` | text area | optional | — | max length 500; Required where the pause reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the pause reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones … | `recordWorkOrderTime` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordWorkOrderTime` body |

Errors to draw in the form: 400 Validation failed; 409 Action inconsistent with the current timer state

**Form: Start work order** (modal, opened by *Start work order*; *Start work order* calls `startWorkOrder`, *Cancel* sends nothing)

**Collects what `startWorkOrder` sends before it is called.** Nothing in the body is required. Optional: `startedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Started at `startedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time where the job began offline. The server records both. | `startWorkOrder` body |

**Form: Save work order** (modal, opened by *Save work order*; *Save work order* calls `updateWorkOrder`, *Cancel* sends nothing)

**Collects what `updateWorkOrder` sends before it is called.** Nothing in the body is required. Optional: `assignedToPrincipalId`, `priority`, `dueAt`, `description`, `categoryId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | How the maintenance head confirms a `suggestWorkOrderAssignee` candidate (M17-13). | `updateWorkOrder` body |
| Priority `priority` | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | — | `updateWorkOrder` body |
| Required qualification codes `requiredQualificationCodes` | list of values (chips) | optional | — | at most 10 | — | — | `updateWorkOrder` body |
| Due at `dueAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateWorkOrder` body |
| Description `description` | text area | optional | — | max length 5000 | — | — | `updateWorkOrder` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateWorkOrder` body |

**Form: Verify work order** (modal, opened by *Verify work order*; *Verify work order* calls `verifyWorkOrder`, *Cancel* sends nothing)

**Collects what `verifyWorkOrder` sends before it is called.** Required: `outcome`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | segmented control | required | — | Verified · Rejected | — | — | `verifyWorkOrder` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `verifyWorkOrder` body |

Errors to draw in the form: 403 Verifier is the technician who completed the work

**Sent by *Cancel work order*** (`cancelWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | radio group | required | — | Raised in error · Duplicate · Superseded · No longer required | — | — | `cancelWorkOrder` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `cancelWorkOrder` body |
| Superseded by work order `supersededByWorkOrderId` | picker: choose a superseded by work order | optional | — | — | shows names, sends the id | — | `cancelWorkOrder` body |

**Sent by *Close work order*** (`closeWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | radio group | required | — | Completed and verified · Not reproducible · Superseded by replacement · No longer applicable · Duplicate | — | — | `closeWorkOrder` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `closeWorkOrder` body |
| Duplicate of work order `duplicateOfWorkOrderId` | picker: choose a duplicate of work order | optional | — | — | shows names, sends the id | — | `closeWorkOrder` body |

**Sent by *Reject work order*** (`rejectWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Wrong skill · Not on shift · Wrong venue · Already in hand · Unsafe · Other | — | — | `rejectWorkOrder` body |
| Note `note` | text area | optional | — | max length 300; Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real … | `rejectWorkOrder` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Photo**: The camera is the first thing on screen; at least one photo is expected (Skip is allowed with a note). Photo is the primary way to log faults on things without tags (pipes, valves, lighting). *(source: DI-232 / contracts/satellite/maintenance.yaml#createWorkOrder)*
- **What is it about**: "Scan the tag" (fills asset and location, works offline) or "No tag - describe where" (location text, max 500). Never an asset id field. *(source: screens/P06-staff-app.yaml#EMP-006 / contracts/satellite/maintenance.yaml#lookupAsset)*
- **Kind of request**: Big tiles for the quick-create types the client listed - Maintenance fault, IT fault, Cleaning, Safety/security concern. A safety concern that hurt or nearly hurt someone is an incident, not a task: that tile offers "Report an incident instead" (EMP-026). Store, purchase and leave requests are not raised here. *(source: DI-230 / contracts/satellite/maintenance.yaml#reportIncident)*
- **Title**: One line, required (max 200), with suggestions from the chosen kind ("Water on floor", "Reader not responding"). *(source: contracts/satellite/maintenance.yaml#createWorkOrder)*
- **Fault assessment**: Two questions only, as large buttons - "Is anyone at risk?" Yes/No, and "Is it affecting guests?" No / Slower than normal / Stopped. These feed the venue's priority score; there is no priority picker for a steward. *(source: contracts/satellite/maintenance.yaml#/components/schemas/WorkOrderFaultAssessment / DI-923)*
- **Take it out of service now**: Shown only when the scanned asset is a ride, gate or other asset with linked products or an access point, and only to a person allowed to change asset status; off by default; on, it warns what stops (ride closed on the map, Gate 2 blocked, queue closed). *(source: contracts/satellite/maintenance.yaml#createWorkOrder / F12 step 1)*
- **Hidden from the form**: id, venueId, recordedAt, assignee and due time are not inputs (device and session supply them; a supervisor assigns later). *(source: contracts/satellite/maintenance.yaml#/components/schemas/CreateWorkOrderRequest)*

#### Outputs: what the screen shows and produces

**Shown**

**Every work order** (data table, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |

**The selected work order** (detail panel, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |

**The work order** (detail panel, from `getWorkOrder`)

| Shows | Format | Notes |
|---|---|---|
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Create work order (primary button) | `createWorkOrder` POST `/work-orders` | CreateWorkOrderRequest | WorkOrder | 400 Validation failed | works offline; opens modal first |
| Accept work order (secondary button) | `acceptWorkOrder` POST `/work-orders/{workOrderId}/accept` | — | WorkOrder | 409 Not assigned to this principal, or already accepted | works offline |
| Attach work order evidence (secondary button) | `attachWorkOrderEvidence` POST `/work-orders/{workOrderId}/attachments` | inline | WorkOrderAttachment | — | works offline; opens modal first |
| Cancel work order (destructive button) | `cancelWorkOrder` POST `/work-orders/{workOrderId}/cancel` | inline | WorkOrder | 409 Labour time or a part is already recorded against it (`work-recorded`; CHG-RUL-010). | — |
| Close work order (destructive button) | `closeWorkOrder` POST `/work-orders/{workOrderId}/close` | inline | WorkOrder | — | — |
| Complete work order (secondary button) | `completeWorkOrder` POST `/work-orders/{workOrderId}/complete` | inline | WorkOrder | 400 Completion photographs required for this category and none supplied | works offline; opens modal first |
| Pause work order (secondary button) | `pauseWorkOrder` POST `/work-orders/{workOrderId}/pause` | inline | WorkOrder | 400 Validation failed | works offline; opens modal first |
| Record work order parts (secondary button) | `recordWorkOrderParts` POST `/work-orders/{workOrderId}/parts` | inline | WorkOrderDetail | 409 Insufficient stock | opens modal first |
| Record work order time (secondary button) | `recordWorkOrderTime` POST `/work-orders/{workOrderId}/time` | inline | WorkOrder | 400 Validation failed; 409 Action inconsistent with the current timer state | works offline; opens modal first |
| Reject work order (destructive button) | `rejectWorkOrder` POST `/work-orders/{workOrderId}/reject` | inline | WorkOrder | 400 Validation failed | works offline |
| Resume work order (secondary button) | `resumeWorkOrder` POST `/work-orders/{workOrderId}/resume` | — | WorkOrder | — | works offline |
| Start work order (secondary button) | `startWorkOrder` POST `/work-orders/{workOrderId}/start` | inline | WorkOrder | — | works offline; opens modal first |
| Save work order (secondary button) | `updateWorkOrder` PATCH `/work-orders/{workOrderId}` | inline | WorkOrder | — | works offline; opens modal first |
| Verify work order (secondary button) | `verifyWorkOrder` POST `/work-orders/{workOrderId}/verify` | inline | WorkOrder | 403 Verifier is the technician who completed the work | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Confirmation**: "Sent - WO-2026-01495, scored Urgent (64)" with "It is on the list for whoever is free"; offline "Saved on this phone - will send when back online" and the number shown once synced. If the asset had an override: "Emergency - this asset is set to Emergency when it fails". *(source: contracts/satellite/maintenance.yaml#createWorkOrder / F65 step 2 / DI-923)*
- **Possible duplicate**: After a scan, the asset's open work orders appear under the tag ("1 open job on this turnstile - raised 08:40 by Omar Haddad") with "Add my photo to it" instead of raising a second. *(source: contracts/satellite/maintenance.yaml#getAsset / designer default)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Send**: Raises the work order with photos; the device scores priority with the policy it last synced and the server re-scores on arrival. Returns to where the person came from (home or task list). *(source: contracts/satellite/maintenance.yaml#createWorkOrder / F65 step 1)*
- **Add my photo to the existing job**: Attaches the photo as Before evidence on that work order instead of raising a new one. *(source: contracts/satellite/maintenance.yaml#attachWorkOrderEvidence)*

**Data it reads**: `listWorkOrders` (onLoad, List work orders)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-004` Task list: *It appears on the list for whoever is free*; carries `workOrderId`; calls `createWorkOrder`

**What opens over it**

- confirmDialog *Cancel work order*: **Names what `cancelWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A raise task this affects should be identified in the dialog, not just counted. **Collects what `cancelWorkOrder` sends before it is called.** Required: `reason`. Optional: `note` …
- confirmDialog *Close work order*: **Names what `closeWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A raise task this affects should be identified in the dialog, not just counted. **Collects what `closeWorkOrder` sends before it is called.** Required: `outcome`. Optional: `note` …
- confirmDialog *Reject work order*: **Names what `rejectWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A raise task this affects should be identified in the dialog, not just counted. **Collects what `rejectWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The raise task list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the raise task untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No raise task yet. Offers Create work order (`createWorkOrder`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on assignedToPrincipalId, status, priority, assetId, overdueOnly and the raise task are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORK_ORDER_VIEW`, which `listWorkOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MAINTENANCE_APPROVE` for `closeWorkOrder`; `MAINTENANCE_EXECUTE` for `acceptWorkOrder`, `attachWorkOrderEvidence`, `pauseWorkOrder` … |
| Offline (`?state=offline`) | Queues locally. A task raised in a plant room must not need signal |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Completion photographs required for this category and none supplied; 400 Validation failed; 409 Action inconsistent with the current timer state; 409 Insufficient stock |

#### Edge cases to draw

- **Offline in a plant room**: Everything works (scan, photo, send); the item waits in the outbox with a count on the home screen. *(source: contracts/satellite/maintenance.yaml#createWorkOrder / screens/P06-staff-app.yaml#EMP-006)*
- **Offline score differs from server score**: The confirmation updates on sync ("Re-scored High by the venue policy"); the person is not asked again. *(source: contracts/satellite/maintenance.yaml#createWorkOrder)*
- **Tag not found**: "Tag not on the register here" with "Describe where instead"; the scanned code is kept in the description. *(source: contracts/satellite/maintenance.yaml#lookupAsset)*
- **Person may not take assets out of service**: The toggle is shown disabled with "Ask a supervisor to close it" and a button that flags the task Urgent (per VO-R08). *(source: contracts/satellite/maintenance.yaml#setAssetStatus)*

#### Consistency with other screens

- Match `EMP-026`: Incident report and Raise a task share the photo-first layout and the scan control; each offers a one-tap switch to the other.
- Match `BO-070`: The raised task appears there with its priority source; the fault-assessment answers are shown on the row's detail.
- Match `BO-069`: The out-of-service toggle has the same consequence wording as Take out of service on the asset register.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
raised:
- kind: Cleaning
  title: Water on floor by Wave Rider exit stairs
  where: Aqua Park, Wave Rider exit
  atRisk: 'Yes'
  guests: Slower than normal
  scored: Urgent (64)
  by: Maria Santos
- kind: Maintenance fault
  title: Gate 2 reader not responding
  asset: Main Plaza Gate 2 turnstile (AP-GATE-0102)
  atRisk: 'No'
  guests: Stopped
  scored: High (78)
  by: Omar Haddad (cashier, Main Plaza ticket office)
```

#### Permissions

- `createWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `acceptWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `attachWorkOrderEvidence` → `MAINTENANCE_EXECUTE` (operate) · staff
- `cancelWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `closeWorkOrder` → `MAINTENANCE_APPROVE` (operate) · staff
- `completeWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `getWorkOrder` → `WORK_ORDER_VIEW` (read) · staff
- `listWorkOrders` → `WORK_ORDER_VIEW` (read) · staff
- `pauseWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `recordWorkOrderParts` → `WORK_ORDER_MANAGE` (configure) · staff
- `recordWorkOrderTime` → `WORK_ORDER_MANAGE` (configure) · staff
- `rejectWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `resumeWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `startWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `updateWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `verifyWorkOrder` → `WORK_ORDER_VERIFY` (operate) · staff

**A refused user sees:** Shown when the caller lacks `WORK_ORDER_VIEW`, which `listWorkOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MAINTENANCE_APPROVE` for `closeWorkOrder`; `MAINTENANCE_EXECUTE` for `acceptWorkOrder`, `attachWorkOrderEvidence`, `pauseWorkOrder` …

#### Requirements it meets

33 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| 18.2.1 | Work Order Inbox - Users shall view assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.2 | Work Order Acceptance - Users shall accept assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.3 | Work Order Rejection - Users shall reject assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| … 21 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Photo capture is the primary way to log faulty assets without barcodes (pipes, valves, lighting); barcode scan is secondary. *(agreed · MoM 10 Aug 2026, 5.3 Task, Work Order & Asset Management · DI-232)*
- Tasks are logged with priority and scheduled date/time; work order lifecycle Created → Assigned → In progress → Review → Closed with a timer showing resolution duration. *(client request · MoM 10 Aug 2026, 5.3 Task, Work Order & Asset Management · DI-231)*
- Quick-create for maintenance, IT support, cleaning/safety/security, store, purchase and leave requests. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-230)*
- In-system task assignment between staff (e.g. a cashier flagging something for a supervisor) without email or messaging apps. *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-159)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-006` · status **notStarted** · provenance generated
- Flow F65 *A task is raised, worked and handed over*, step 1: A steward raises a task. → **Raised in seconds, from where the problem is.** A form that takes a minute is a spill somebody steps around instead.

#### Acceptance for the design

- [ ] Every input above is drawn (63), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-006?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create work order, Accept work order, Attach work order evidence, Cancel work order, Close work order, Complete work order, Pause work order, Record work order parts, Record work order time, Reject work order, Resume work order, Start work order, Save work order, Verify work order.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`, `EMP-004`.
- [ ] Every gated control is gated: `MAINTENANCE_APPROVE`, `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VERIFY`, `WORK_ORDER_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-007` Handover notes

**Tell the next shift what they are walking into.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `core` module |
| Block | Block D · task APP-STAFF-EMP-007 |
| Who uses it | venue staff holding `WORK_ORDER_VIEW` (1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAnnouncements` reads the population and `getAnnouncementReach` reads one of them — list, select, act |
| Offline | Editable offline and synced at end of shift |
| Opens with | nothing: it opens on its own · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/handover-notes` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): A handover is not a staff announcement: publishing needs ANNOUNCEMENT_PUBLISH, which a steward does not hold, and reaches the whole audience, not the next person … Removed 2 October 2026 (CHG-WIR-001): A handover is not a staff announcement: publishing needs ANNOUNCEMENT_PUBLISH, which a steward does not hold, and reaches the whole audience, not the next person … Removed 2 October 2026 (CHG-WIR-001): A handover is not a staff announcement: publishing needs ANNOUNCEMENT_PUBLISH, which a steward does not hold, and reaches the whole audience, not the next person …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Handover notes on the Staff App: what the person ending a shift tells the person starting the next one at the same post (gate, till, ride, plant room). It is opened from the end-of-shift path (EMP-009) and read at the start of the next shift. The one thing to get right: the handover is built from what is still open (paused and unfinished work orders, open incidents, the till shift state) with a short free-text note on top, not a blank text box and not a venue-wide announcement.

**Fixed on main** (the package already carries these; draw what it says): The screen is bound to listAnnouncements, publishAnnouncement, acknowledgeAnnouncement and getAnnouncementReach with an "Every … (CHG-WIR-001); Offline state says "Editable offline and synced at end of shift" while the bound write (publishAnnouncement) is not offline-capable (CHG-WIR-001); entryFrom is empty and the exits to EMP-001, EMP-002 and EMP-003 are inferred (CHG-WIR-002).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is a handover addressed to the next person on the post, to the post itself, or to the supervisor?** → Drawn default accepted: Draw "To the post" with the next rostered person named; supervisor sees all handovers on BO-233. *(decided by Chinmay, 2026-10-02; DEC-522 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

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

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open work carried over**: Pre-filled, not typed: every work order assigned to or accepted by the leaving person that is paused, in progress or awaiting parts, each with its title, location, status and the reason it was paused. The person can untick an item only by reassigning or releasing it (never by deleting it); each carried item stays a link to the work order. *(source: F65 step 5 / F08 step 8 / F65 step 4)*
- **Note to next shift**: Optional free text, max 1,000 characters, Arabic or English (the device language), with quick chips for the common cases ("Gate 3 exit-only from 17:00", "Printer out of paper rolls", "Lost child found, with Guest Services"). Placeholder never used as the label. *(source: F08 step 7 / DI-019 / designer default)*
- **Hand over to**: The incoming person or post, defaulted from the rota (the next assignment on the same position and venue); a picker of colleagues at this venue if nobody is rostered. Not an audience picker of venues, departments and roles; that is broadcast (EMP-038). *(source: contracts/satellite/workforce.yaml#listRotaAssignments / F08 step 7)*
- **id, publishedByPrincipalId, publishedAt**: Never inputs (per VO-R03); the author and time come from the session and the server. *(source: contracts/satellite/workforce.yaml#/components/schemas/Announcement)*

#### Outputs: what the screen shows and produces

**Shown**

**Carried over** (data table, from `listWorkOrders`)

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Incoming handover card (start of shift)**: The newest handover for this post first, headed "From Rahul Menon, Gate steward, 15:02": carried work orders as tappable rows with status pills, then the note. An "I have read this" action closes the card; older handovers for the post sit below, newest first, last 7 days. *(source: F08 step 7 / contracts/satellite/workforce.yaml#acknowledgeAnnouncement)*
- **Outgoing summary (end of shift)**: Counts before the note: "3 work orders carried, 1 incident open, till shift pending closure". A carried count of 0 is shown as "Nothing carried over", not hidden. *(source: F65 step 5 / F08 step 8)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Hand over**: Saves the handover against the post and the shift and returns to EMP-009 to end the shift. Never publishes a staff announcement. Success shows "Handed over to Fatima Al Hashimi". *(source: F08 step 7 / F08 step 8)*
- **Reassign or release a carried item**: Opens the work order with Release (reason required); the item leaves the handover only when released. *(source: F65 step 3 / F65 step 4)*
- **I have read this (incoming)**: Marks the handover read; queued offline like an announcement acknowledgement. *(source: contracts/satellite/workforce.yaml#acknowledgeAnnouncement)*

**Data it reads**: `listWorkOrders` (onLoad, Open work carried into the handover, for the next person on …)

**Where the user goes next**

- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-009` End shift: *Ends the shift with a blind count (no expected cash shown;*; calls `listWorkOrders`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The handover notes list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the handover notes untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No handover notes yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on unacknowledgedOnly and the handover notes are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORK_ORDER_VIEW`, which `listWorkOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Editable offline and synced at end of shift |

#### Edge cases to draw

- **No signal at the end of the shift**: The handover is saved on the device and shows "Saved, will send when online"; the person can still end the shift. The incoming person sees it only after sync, so the card says when it was written, not when it arrived. *(source: F08 step 4)*
- **Nobody rostered on the post next**: Handover goes to the post itself and is shown to whoever next clocks in on that position; the supervisor sees "Unclaimed handover". *(source: contracts/satellite/workforce.yaml#listRotaAssignments / designer default)*
- **A carried work order was closed by someone else meanwhile**: Shown struck through with "Closed by Omar Haddad 15:40", not removed silently. *(source: F65 step 4)*

#### Consistency with other screens

- Match `EMP-009`: End shift opens this screen first when anything is open; the counts here match the end-shift summary.
- Match `EMP-005`: Carried items are the same work orders, same status labels (In progress, Paused, Awaiting parts).
- Match `BO-233`: The back-office shift handover summary reads the same handovers; same wording "Carried over".
- Match `EMP-038`: Broadcast is the one-to-many channel; handover is one post to the next. Do not reuse the broadcast form here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outgoing:
  from: Rahul Menon, Gate steward, Main Plaza Gate 2
  to: Fatima Al Hashimi, Duty supervisor
  carried:
  - WO-1182 Turnstile 4 card reader intermittent - Paused, awaiting parts
  - WO-1190 Spill at Wave Rider queue - In progress
  note: Gate 3 exit-only from 17:00. Lost child (Khalid, 7) reunited at Guest Services 13:20.
  writtenAt: Sat 10 Oct 2026 15:02
```

#### Permissions

- `listWorkOrders` → `WORK_ORDER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WORK_ORDER_VIEW`, which `listWorkOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-007` · status **notStarted** · provenance generated
- Flow F08 *Steward works a shift on the employee app*, step 7: Writes handover notes → What the next shift needs to know
- Flow F65 *A task is raised, worked and handed over*, step 5: Unfinished work is written into the handover. → **The handover is generated from open tasks, not typed.** A note somebody writes at the end of a tiring shift is a note that omits things.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-007?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: What publishing changes.
- [ ] Every transition is wired: `EMP-003`, `EMP-009`.
- [ ] Every gated control is gated: `WORK_ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-008` Shift summary

**See what this person actually did today.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `core` module |
| Block | Block C · task APP-STAFF-EMP-008 |
| Who uses it | venue staff holding `REPORT_VIEW_OWN`, `REPORT_VIEW_WORKSTATION`, `SHIFT_OPEN` (3 operate); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listShifts` reads the population and `getCurrentShift` reads one of them — list, select, act |
| Offline | Local totals, marked as unreconciled |
| Opens with | `shiftId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/operations/shift-summary` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: acceptShiftVariance, approveShiftOpen, closeShift, createCashMovement. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.** **Removed 24 August**: openShift, recordNoSale, reopenShift, resumeShift. **Bulk-attach residue.** A device-settings screen does not merge guest profiles, a rota view does not author the rota, a shift summary does not open a shift, and **authority notification belongs where the incident is raised, not where it is read.** **No figures from which the expected cash could be worked out** (decided 2 October 2026, Chinmay; CHG-FIN-003). The summary shows what the person did (sales count, voids, no-sales, breaks), not sales, refunds or lifts totals, and never expected cash or variance, for their own shift. A supervisor reads those on BO-040.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): F72 step 1 declares the shift summary read-only ("the person being reviewed could sign off their own review"); suspending is the break mechanism and belongs on …

**From the Food, Beverage & Retail process.** A read-only summary of what this person did on their shift, read before the shift is closed by someone else. From the F&B angle the person is a server or a bar cashier. The bar cashier holds a till and has a cash shift. The server mostly does not, and wants covers, tables, sales and tips. The one thing to get right: it never reveals the cash figure that the blind close count is measured against.

**Known correction pending (do not draw the wrong version)**

- **There is no source for a server's own summary (covers served, tables closed, sales by server, gratuity). The Shift record is a till (workstation) shift, so a server with no till sees an empty screen.** Why: Tips and sales attribution follow the server (transferTableVisit, reassignServer), and the matrix asks for waiter assignment for tips. No operation reads them back per person. *(source: contracts/satellite/fnb.yaml#reassignServer / contracts/satellite/fnb.yaml#transferTableVisit / MATRIX 4.9.7; Food, Beverage & Retail)*
- **Module placement: EMP-008 is a core staff-app or till screen (module Operations, requiresModule core), not an F&B screen.** Why: Its data is the cash shift. F&B uses it only for bar and counter staff who hold a till. The tracker already asked to consolidate shift-closing and till-closing screens. *(source: TRACKER Workshops/Actions row 63 / F72 step 1; Food, Beverage & Retail)*
- **Raw data tables "Every shift" and "Every cash movement" with id, scopePath, currencyScale and principalId columns.** Why: Plumbing on a user's screen. The person reads their own shift, in words. *(source: screens/P06-staff-app.yaml#EMP-008; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): Remove "Suspend shift" (suspendShift) from the shift summary. (CHG-WIR-008); The summary shows openingFloat, salesTotal, refundsTotal and liftsTotal while the shift is open, which lets the cashier work out the … (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does a server without a till get a shift summary (covers, sales, tips), and from which source?** → A server without a till gets a service summary: covers, tables, sales, tips. *(decided by Chinmay, 2026-10-02; DEC-199 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listShifts`. | `listShifts` ?workstationId |
| Status | select | optional | — | Pending approval · Open · Suspended · Pending variance · Pending closure · Closed · Auto closed | — | Sends `?status=` to `listShifts`. | `listShifts` ?status |
| Opened from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedFrom=` to `listShifts`. | `listShifts` ?openedFrom |
| Opened to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedTo=` to `listShifts`. | `listShifts` ?openedTo |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Date | date picker | — | — | `getServiceSummary` ?date |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Which shift**: The caller's own current shift from the session by default. Earlier shifts come from a short "My recent shifts" list (date and outlet), not from Workstation id, Status and Opened from/to text fields. *(source: F72 step 1 / contracts/spine/shift.yaml#getCurrentShift / contracts/spine/shift.yaml#listShifts)*

#### Outputs: what the screen shows and produces

**Shown**

**My service today: covers, tables, sales, tips** (metric tile, from `getServiceSummary`): For a server without a till (decided 2 October 2026, Chinmay, batch 6, EMP-008: "Yes: a service summary (covers, tables, sales, tips)"; DEC-199; CHG-CSA-020). Self-scoped under REPORT_VIEW_OWN. A cashier with a drawer sees the shift instead; neither ever sees expected cash (CHG-FIN-003).

| Shows | Format | Notes |
|---|---|---|
| Date | 1 Oct 2026 | — |
| Covers | 1,234 | — |
| Tables | 1,234 | Table visits served. |
| Sales | AED 1,234.50 | Excluding VAT, as `grossSales` (CHG-FIN-007). |
| Tips | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Open tables | 1,234 | Visits still open, with their bills not yet settled. |

**Every shift** (data table, from `listShifts`)

| Shows | Format | Notes |
|---|---|---|
| Principal display name | text | — |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Deposit box code | text | — |
| Bag number | text | — |

**Every cash movement** (data table, from `listCashMovements`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Opening float, Lift, Add | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Reference | text | Safe drop reference or bag number. |
| Recorded at | 1 Oct 2026, 14:30 | — |

**The selected shift** (detail panel, from `getCurrentShift`)

| Shows | Format | Notes |
|---|---|---|
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Deposit box code | text | — |
| Bag number | text | — |

**The shift** (detail panel, from `getShift`)

| Shows | Format | Notes |
|---|---|---|
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Deposit box code | text | — |
| Bag number | text | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Cash figures**: Before the close count has been submitted, show only counts and non-cash facts: number of sales, refunds, no-sales, lifts made and the times. Do not show the opening float plus sales, the lift totals or any total from which the expected cash in the drawer can be worked out. After the count, the expected, counted and variance figures may appear, read-only. *(source: R080 / POSV2-3 / MATRIX 5.9.2 / DI-806 / contracts/spine/shift.yaml#/components/schemas/Shift)*
- **Unreconciled marker**: Offline, local totals are shown and marked "Not yet synced, may change". *(source: screens/P06-staff-app.yaml#EMP-008 / F72 step 2)*
- **Exceptions**: Shift incidents (no-sales, manager overrides) listed with time and reason, so the person sees what a reviewer will see. *(source: contracts/spine/shift.yaml#/components/schemas/Shift)*
- **Service summary (a server without a till)**: Covers, tables, sales and tips for the server's service; no cash figures. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

**Data it reads**: `listShifts` (onLoad, List shifts); `getCurrentShift` (onLoad, The open or suspended shift on the session's workstation); `getShift` (onLoad, Read a shift); `listCashMovements` (onLoad, Lifts, adds and the opening float); `getServiceSummary` (onLoad, A server without a till: my covers, tables, sales and tips …)

**Where the user goes next**

- → `EMP-017` Sync & reconciliation: *Anything unsynced is pushed first*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The shift summary list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the shift summary untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No shift summary yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on workstationId, status, openedFrom, openedTo and the shift summary are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Local totals, marked as unreconciled |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
person: Omar Ziad · Bar cashier · Oasis Bistro bar till 2
shift: Thu 15 Oct 2026 · 16:00 to 23:30 GST · Open
sales: 64 sales · 3 refunds
noSales: 2 (Change for guest 18:12; Till check 21:40)
lifts: 1 safe drop at 20:15 · bag 004417
afterCount:
  expected: AED 2,140.50
  counted: AED 2,128.00
  variance: AED -12.50 short
```

#### Permissions

- `listShifts` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `getCurrentShift` → `SHIFT_OPEN` (operate) · staff
- `getShift` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listCashMovements` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `getServiceSummary` → `REPORT_VIEW_OWN` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.44 | Incident & Exception Logging | Ticketing Sales | CONTRACTED | data `Shift` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-008` · status **notStarted** · provenance generated
- Flow F72 *A shift ends and the summary is read*, step 1: The steward reads their shift summary. → **Read-only.** This screen could close the shift and accept a variance until 24 August — **the person being reviewed could sign off their own review.**

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-008?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `EMP-017`, `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `REPORT_VIEW_OWN`, `REPORT_VIEW_WORKSTATION`, `SHIFT_OPEN`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

### In P06 · Operations

- Employee app navigation: Work Orders, Task & Assets, Inventory/Safety/Inspections, Attendance, Approvals/Requests, Incidents, Communications, Venue Map; plus employee ID/profile and preferences. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-228)*

**23 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"acceptShiftVariance": {"method":"POST","path":"/shifts/{shiftId}/accept-variance","contract":"shift","summary":"Accept an over/short beyond the threshold","permission":"OVERSHORT_ACCEPT","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"acceptWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/accept","contract":"maintenance","summary":"The assignee takes the job","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"attachWorkOrderEvidence": {"method":"POST","path":"/work-orders/{workOrderId}/attachments","contract":"maintenance","summary":"Photo, video, document, note or signature","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrderAttachment"},
"cancelWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/cancel","contract":"maintenance","summary":"Cancel a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"changeOwnCredential": {"method":"POST","path":"/auth/credential","contract":"identity","summary":"Change the caller's own password or PIN","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChangeCredentialRequest","responds":null},
"closeWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/close","contract":"maintenance","summary":"Administratively closed","permission":"MAINTENANCE_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"completeSsoAuthorization": {"method":"POST","path":"/auth/sso/{providerId}/callback","contract":"identity","summary":"Exchange an SSO code for a session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LoginResponse"},
"completeWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/complete","contract":"maintenance","summary":"Complete a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"createMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge","contract":"identity","summary":"Second factor at staff sign-in, and step-up for a sensitive action","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createStockReservation": {"method":"POST","path":"/stock-reservations","contract":"inventory","summary":"Reserve stock for a work order or another need","permission":"PROCUREMENT_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"InventoryStockReservation","responds":"InventoryStockReservation"},
"createWorkOrder": {"method":"POST","path":"/work-orders","contract":"maintenance","summary":"Raise a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateWorkOrderRequest","responds":"WorkOrder"},
"getCurrentSession": {"method":"GET","path":"/auth/session","contract":"identity","summary":"Current session and effective permissions","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[],"requestBody":null,"responds":"Session"},
"getCurrentShift": {"method":"GET","path":"/shifts/current","contract":"shift","summary":"The open or suspended shift on the session's workstation","permission":"SHIFT_OPEN","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[],"requestBody":null,"responds":"Shift"},
"getIncident": {"method":"GET","path":"/incidents/{incidentId}","contract":"maintenance","summary":"Read an incident","permission":"INCIDENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"IncidentDetail"},
"getServiceSummary": {"method":"GET","path":"/service-summary","contract":"reporting","summary":"My service summary (a server without a till)","permission":"REPORT_VIEW_OWN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"date","in":"query","required":null}],"requestBody":null,"responds":"ServiceSummary"},
"getShift": {"method":"GET","path":"/shifts/{shiftId}","contract":"shift","summary":"Read a shift","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Shift"},
"getWorkOrder": {"method":"GET","path":"/work-orders/{workOrderId}","contract":"maintenance","summary":"Read a work order","permission":"WORK_ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WorkOrderDetail"},
"getWorkstationShift": {"method":"GET","path":"/shifts/current/overview","contract":"shift","summary":"Read the open or suspended shift on the session's workstation, without the right to open one","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[],"requestBody":null,"responds":"Shift"},
"listCashMovements": {"method":"GET","path":"/shifts/{shiftId}/cash-movements","contract":"shift","summary":"Lifts, adds and the opening float","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listIncidents": {"method":"GET","path":"/incidents","contract":"maintenance","summary":"List incidents","permission":"INCIDENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"severity","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"isReportable","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listShifts": {"method":"GET","path":"/shifts","contract":"shift","summary":"List shifts","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"openedFrom","in":"query","required":null},{"name":"openedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSsoProviders": {"method":"GET","path":"/auth/sso/providers","contract":"identity","summary":"Identity providers configured for this tenant","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SsoProvider"},
"listStockReservations": {"method":"GET","path":"/stock-reservations","contract":"inventory","summary":"Soft holds on stock","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"sourceType","in":"query","required":null},{"name":"sourceId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkOrders": {"method":"GET","path":"/work-orders","contract":"maintenance","summary":"List work orders","permission":"WORK_ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assignedToPrincipalId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"assetId","in":"query","required":null},{"name":"overdueOnly","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"login": {"method":"POST","path":"/auth/login","contract":"identity","summary":"Authenticate and open a session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LoginRequest","responds":"LoginResponse"},
"lookupTicket": {"method":"GET","path":"/access/lookup","contract":"access","summary":"Read-only validity check without admitting","permission":"TICKET_LOOKUP","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"mediaCode","in":"query","required":null},{"name":"ticketId","in":"query","required":null}],"requestBody":null,"responds":"TicketStatus"},
"overrideAccess": {"method":"POST","path":"/access/override","contract":"access","summary":"Admit against a failed validation","permission":"ACCESS_OVERRIDE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationResult"},
"pauseWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/pause","contract":"maintenance","summary":"Stopped, and why","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"recordAuthorityNotification": {"method":"POST","path":"/incidents/{incidentId}/notify-authority","contract":"maintenance","summary":"Record notification to an external authority","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Incident"},
"recordWorkOrderParts": {"method":"POST","path":"/work-orders/{workOrderId}/parts","contract":"maintenance","summary":"Record parts consumed","permission":"WORK_ORDER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrderDetail"},
"recordWorkOrderTime": {"method":"POST","path":"/work-orders/{workOrderId}/time","contract":"maintenance","summary":"Start, pause or stop work","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"rejectWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/reject","contract":"maintenance","summary":"The assignee declines, with a reason","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"releaseStockReservation": {"method":"POST","path":"/stock-reservations/{stockReservationId}/release","contract":"inventory","summary":"Give reserved stock back","permission":"PROCUREMENT_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"InventoryStockReservation"},
"reportIncident": {"method":"POST","path":"/incidents","contract":"maintenance","summary":"Report an incident","permission":"INCIDENT_REPORT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ReportIncidentRequest","responds":"Incident"},
"resumeWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/resume","contract":"maintenance","summary":"Back to work","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"selectRole": {"method":"POST","path":"/auth/select-role","contract":"identity","summary":"Choose a role for a multi-role session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Session"},
"startSsoAuthorization": {"method":"GET","path":"/auth/sso/{providerId}/authorize","contract":"identity","summary":"Begin an SSO flow","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"redirectUri","in":"query","required":true}],"requestBody":null,"responds":null},
"startWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/start","contract":"maintenance","summary":"Work has begun","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"submitShiftCount": {"method":"POST","path":"/shifts/{shiftId}/count","contract":"shift","summary":"The cashier's blind count, closing their own shift","permission":"SHIFT_CLOSE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CloseShiftRequest","responds":"ShiftCountReceipt"},
"suspendShift": {"method":"POST","path":"/shifts/{shiftId}/suspend","contract":"shift","summary":"Suspend a shift so another user can log in","permission":"SHIFT_SUSPEND","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"updateIncident": {"method":"PATCH","path":"/incidents/{incidentId}","contract":"maintenance","summary":"Investigate, escalate, close or reopen an incident","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Incident"},
"updateWorkOrder": {"method":"PATCH","path":"/work-orders/{workOrderId}","contract":"maintenance","summary":"Assign, reprioritise or amend","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"validateAccess": {"method":"POST","path":"/access/validate","contract":"access","summary":"Validate media at an access point and admit or deny","permission":"ACCESS_VALIDATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ValidateRequest","responds":"ValidationResult"},
"validateGroupAccess": {"method":"POST","path":"/access/group-validate","contract":"access","summary":"Admit a group on one read","permission":"ACCESS_VALIDATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationResult"},
"verifyAccreditationCredential": {"method":"GET","path":"/accreditation-credentials/verify","contract":"accreditation","summary":"Who holds this credential, and where may they go","permission":"ACCESS_VALIDATE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"identifier","in":"query","required":true},{"name":"zoneId","in":"query","required":null}],"requestBody":null,"responds":"AccreditationCredentialVerification"},
"verifyMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge/{challengeId}/verify","contract":"identity","summary":"Complete a sign-in or step-up challenge","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"verifyWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/verify","contract":"maintenance","summary":"Supervisor verification","permission":"WORK_ORDER_VERIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccreditationCredentialVerification": {"type":"object","description":"18.8.3. **What a steward needs to believe the person in front of them**: the face, the name, the category and the zones, and whether any of it is valid now. Returned by `verifyAccreditationCredential`; not stored.\n","required":["outcome"],"properties":{"outcome":{"type":"string","enum":["valid","notYetValid","expired","suspended","revoked","credentialReplaced","credentialLost","credentialInactive"],"description":"`valid` only when the holder is `active`, today is inside the holder's validity, and the credential is `issued` or `active`"},"reason":{"type":"string","nullable":true},"credentialId":{"type":"string","format":"uuid"},"credentialKind":{"type":"string"},"credentialStatus":{"type":"string"},"holderId":{"type":"string","format":"uuid"},"accreditationNumber":{"type":"string"},"fullName":{"type":"string"},"photoAssetId":{"type":"string","format":"uuid","nullable":true},"photoUrl":{"type":"string","nullable":true,"description":"Signed and short-lived, so the scan screen can show the face without a second call"},"organisationName":{"type":"string","nullable":true},"affiliationRole":{"type":"string","nullable":true},"programmeId":{"type":"string","format":"uuid"},"categoryCode":{"type":"string","nullable":true},"categoryName":{"type":"string","nullable":true},"holderStatus":{"type":"string"},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"effectiveZones":{"type":"array","description":"The zones the holder may enter under their profiles and exceptions, today","items":{"type":"object","properties":{"zoneId":{"type":"string","format":"uuid"},"zoneName":{"type":"string"},"allowedNow":{"type":"boolean","description":"Inside the profile schedule (date, day, time, event phase) at this moment"}}}},"escortRequired":{"type":"boolean"},"zoneCheck":{"type":"object","nullable":true,"description":"Present when `zoneId` was given","properties":{"zoneId":{"type":"string","format":"uuid"},"allowed":{"type":"boolean"},"reason":{"type":"string","nullable":true}}},"checkedAt":{"type":"string","format":"date-time"}}},
"CashMovement": {"x-ticvai-persistence":"orders.cash_movement","allOf":[{"$ref":"#/components/schemas/CreateCashMovementRequest"},{"type":"object","required":["shiftId","authorisedByPrincipalId","sequence"],"properties":{"shiftId":{"type":"string","format":"uuid"},"depositBoxId":{"type":"string","format":"uuid","nullable":true,"description":"The box the cash moved in or out of. Set on every lift `withdrawFromDepositBox` records (26 September, pull audit R099).\n"},"witnessPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The cashier who countersigned a withdrawal. Null on other movements."},"withdrawalReason":{"allOf":[{"$ref":"#/components/schemas/WithdrawalReason"}],"nullable":true},"authorisedByPrincipalId":{"type":"string","format":"uuid","description":"The principal who authorised the movement, recorded for audit."},"sequence":{"type":"integer","description":"Monotonic within the shift. Preserves order across an offline batch."},"syncedAt":{"type":"string","format":"date-time","nullable":true}}}]},
"ChangeCredentialRequest": {"type":"object","description":"Request only. The credential itself is stored hashed in `identity.principal_credential` and is never returned by any operation (`handoff/schema-storage-only.md`).\n","required":["method","currentCredential","newCredential"],"properties":{"method":{"type":"string","enum":["password","pin"],"description":"Which credential is being changed. Card, RFID and SSO are not secrets the principal holds, so they are not changed here."},"currentCredential":{"type":"string","maxLength":512,"writeOnly":true},"newCredential":{"type":"string","maxLength":512,"writeOnly":true}}},
"CloseShiftRequest": {"type":"object","required":["countedCash","recordedAt"],"properties":{"countedCash":{"type":"array","minItems":1,"description":"**The cashier's blind count, one line per denomination counted** (decided 29 September, readiness close-out; our build plan). The server writes each line as one `CashCountLine` (`countKind` close) against the shift, taking the face value from `platform.denomination`. A denomination may appear once; a repeat is refused with 422 `duplicate-denomination`.\n","items":{"$ref":"#/components/schemas/CountedDenominationLine"}},"nonCashDeclared":{"type":"array","description":"Declared totals per non-cash tender, for reconciliation against captured payments.\n","items":{"type":"object","required":["tender","amount"],"properties":{"tender":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"notes":{"type":"string","maxLength":1000,"description":"The cashier's note on the count. Asked of every cashier on a blind count, never only after a variance is shown (CHG-FIN-003, DI-803).\n"},"cashierReason":{"type":"string","nullable":true,"enum":["tillError","unrecordedRefund","miscount","other"],"description":"Anything the cashier knows went wrong in the shift (DI-803: till error, unrecorded refund, miscount, other). Optional and given without seeing the variance (CHG-FIN-003); the supervisor reads it beside the variance on BO-040.\n"},"releaseHeldLeases":{"type":"boolean","default":true,"description":"Return unsold inventory leases held by this workstation (ADR-0013 C103). Closing without releasing strands capacity until TTL expiry, which is visible at a gate during peak.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"CountedDenominationLine": {"type":"object","x-ticvai-persistence":"none — request only; lands as `CashCountLine` rows","description":"**One line of a cash count as the cashier types it: which note or coin, how many, and what they come to** (decided 29 September, readiness close-out; our build plan). The shape of the blind count on close (`closeShift`) and of the count columns on the till screens (POS-007, POS-011). It is the request side of `CashCountLine`, which is the stored row and adds the shift, the count kind, who counted and when.\n**`total` is shown to the cashier and checked, not trusted**: the server recomputes `count` times the denomination's face value and refuses a line whose `total` disagrees with 422 `count-total-mismatch`. An inactive or unknown denomination is refused with 422 `unknown-denomination`.\n","required":["denominationId","count"],"properties":{"denominationId":{"type":"string","format":"uuid","description":"References `platform.denomination` (`Denomination.id`) — face value, kind and counting order live there."},"count":{"type":"integer","minimum":0,"maximum":100000,"description":"**How many of this note or coin were counted.** Zero is a line, not an omission: a denomination counted and found empty."},"total":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"`count` times the face value, in the denomination's currency. Optional on the way in (the server computes it) and checked when sent.\n"}}},
"CreateCashMovementRequest": {"type":"object","required":["id","kind","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7."},"kind":{"$ref":"#/components/schemas/CashMovementKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"denominations":{"$ref":"#/components/schemas/DenominationCount","x-ticvai-persisted":false,"description":"**Stored as `orders.cash_count_line` rows** with `countKind: movement` and this movement's `cashMovementId`, not as a column. The jsonb blob this used to land in is what `Denomination` was created to replace (26 September, pull audit R099).\n"},"reference":{"type":"string","maxLength":64,"description":"Safe drop reference or bag number."},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateWorkOrderRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","title","venueId","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"title":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":5000},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"kind":{"allOf":[{"$ref":"#/components/schemas/WorkOrderKind"}],"default":"corrective"},"priority":{"allOf":[{"$ref":"#/components/schemas/WorkOrderPriority"}],"description":"**Optional since 29 September** (M17-01). Sent, it is `manual` and wins. Absent, the asset's `priorityOverride` applies, and failing that the venue's `WorkOrderPriorityPolicy` scores the fault.\n"},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","maxItems":10,"items":{"type":"string"},"description":"Skills the job needs, as qualification codes; `suggestWorkOrderAssignee` ranks by them (M17-13)."},"categoryId":{"type":"string","format":"uuid"},"assignedToPrincipalId":{"type":"string","format":"uuid"},"dueAt":{"type":"string","format":"date-time"},"attachmentRefs":{"type":"array","description":"Photo-first. Expected at creation, not added later from memory.","items":{"type":"string"}},"takeAssetOutOfService":{"type":"boolean","default":false,"description":"Raise and immediately suspend the asset. For a fault found on a live ride, the two are one action.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"DenyReason": {"type":"string","description":"Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n","enum":["notFound","notYetValid","expired","alreadyUsed","reentryLimitReached","exitRequiredBeforeReentry","wrongAccessPoint","wrongPerformance","outsideAdmissionWindow","entitlementSuspended","blacklisted","capacityReached","waiverRequired","accompanimentRequired","mediaDeactivated","unpaid","delegatedRightExhausted","delegatedRightRevoked","journeyNotCovered"]},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"Incident": {"x-ticvai-persistence":"maintenance.incident","type":"object","required":["id","incidentNumber","kind","severity","status","venueId","occurredAt","reportedByPrincipalId"],"properties":{"id":{"type":"string","format":"uuid"},"incidentNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"kind":{"$ref":"#/components/schemas/IncidentKind"},"severity":{"$ref":"#/components/schemas/IncidentSeverity"},"status":{"$ref":"#/components/schemas/IncidentStatus"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"locationDescription":{"type":"string","nullable":true},"isReportable":{"type":"boolean","description":"Requires notification to an external authority within a statutory window."},"notificationDueAt":{"type":"string","format":"date-time","nullable":true},"notifiedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The earliest `notifiedAt` among this incident's authority notifications. **Maintained on write** by `recordAuthorityNotification`; each notification itself is a row of `maintenance.incident_authority_notification`.\n"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"reportedByPrincipalId":{"type":"string","format":"uuid"},"correctiveWorkOrderId":{"type":"string","format":"uuid","nullable":true},"escalation":{"type":"object","nullable":true,"readOnly":true,"description":"**Set while the incident is escalated** (the optional Escalated step of the 3 October flow; CHG-RUL-011). Screens show \"Escalated\" when `status` is `underInvestigation` and this is set. Cleared when the incident closes.\n","properties":{"toPrincipalId":{"type":"string","format":"uuid"},"byPrincipalId":{"type":"string","format":"uuid"},"reason":{"type":"string"},"escalatedAt":{"type":"string","format":"date-time"}}},"reopenCount":{"type":"integer","minimum":0,"readOnly":true,"description":"How many times the incident was reopened (CHG-RUL-011). Each reopen is a logged row."},"occurredAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"IncidentAuthorityNotification": {"x-ticvai-persistence":"maintenance.incident_authority_notification","type":"object","description":"**One notification to an external authority, appended by `recordAuthorityNotification`.** An incident may be reported to more than one authority, or to the same one twice, and each is the evidence that an obligation was met — so each is a row, not an overwrite of `maintenance.incident.notified_at`.\n","required":["id","incidentId","authority","notifiedAt"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"authority":{"type":"string","maxLength":200},"reference":{"type":"string","maxLength":128,"nullable":true},"notifiedAt":{"type":"string","format":"date-time"},"notifiedByPrincipalId":{"type":"string","format":"uuid"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time"}}},
"IncidentDetail": {"x-ticvai-persistence":"maintenance.incident","allOf":[{"$ref":"#/components/schemas/Incident"},{"type":"object","properties":{"description":{"type":"string","description":"The original report. Never edited — investigation adds to the record."},"investigationNote":{"type":"string","nullable":true,"readOnly":true,"description":"The latest entry of `investigationNotes`, kept for readers that show one line."},"investigationNotes":{"type":"array","readOnly":true,"description":"**Every investigation note, oldest first** (decided 28 September, audit R106 (5)). Read from `maintenance.incident_investigation_note`; appended by `updateIncident`.\n","items":{"$ref":"#/components/schemas/IncidentInvestigationNote"}},"rootCause":{"type":"string","nullable":true},"correctiveActions":{"type":"string","nullable":true},"firstAidGiven":{"type":"boolean"},"emergencyServicesCalled":{"type":"boolean"},"witnessCount":{"type":"integer"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"involvedParties":{"type":"array","description":"Who was involved, as given in `ReportIncidentRequest.involvedSubjectIds` and `involvedStaffPrincipalIds`. Read from `maintenance.incident_involved_party`.\n","items":{"$ref":"#/components/schemas/IncidentInvolvedParty"}},"authorityNotifications":{"type":"array","description":"Read from `maintenance.incident_authority_notification`, oldest first.","items":{"$ref":"#/components/schemas/IncidentAuthorityNotification"}}}}]},
"IncidentInvestigationNote": {"x-ticvai-persistence":"maintenance.incident_investigation_note","type":"object","description":"**One investigation note, appended by `updateIncident`** (decided 28 September, audit R106 (5)). A history rather than a field, so what an investigator thought on Tuesday survives what they found on Thursday.\n","required":["id","incidentId","note","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"note":{"type":"string","maxLength":10000},"kind":{"type":"string","enum":["note","statusChange","escalation","reopen"],"default":"note","description":"**Every change is logged here** (CHG-RUL-011): an investigator's note, or a row the server writes for a status change, an escalation or a reopen, with `note` as its reason.\n"},"fromStatus":{"allOf":[{"$ref":"#/components/schemas/IncidentStatus"}],"nullable":true},"toStatus":{"allOf":[{"$ref":"#/components/schemas/IncidentStatus"}],"nullable":true},"writtenByPrincipalId":{"type":"string","format":"uuid"},"recordedAt":{"type":"string","format":"date-time"}}},
"IncidentInvolvedParty": {"x-ticvai-persistence":"maintenance.incident_involved_party","type":"object","description":"**One person involved in an incident, by opaque reference.** A guest or member of the public is a `pii.subject` id — personal details live there, the erasable store of ADR-0023, so the incident record survives an erasure request intact. A member of staff is a principal id. Exactly one of the two is set, as `kind` says.\n","required":["id","incidentId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["subject","staff"]},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"A `pii.subject` id where `kind` is `subject`."},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"The staff principal where `kind` is `staff`."},"role":{"type":"string","nullable":true,"enum":["injured","involved","witness","reporter",null],"description":"The person's part in the incident, from `addIncidentPerson` (CHG-RUL-013)."},"contactStored":{"type":"boolean","readOnly":true,"description":"Whether a contact is held for the person: only with their consent to be contacted (`AddIncidentPersonRequest.contactConsent`; CHG-RUL-013).\n"}}},
"IncidentKind": {"type":"string","enum":["guestInjury","staffInjury","nearMiss","propertyDamage","equipmentFailure","securityIncident","fireOrEvacuation","foodSafety","environmental","other"]},
"IncidentSeverity": {"type":"string","enum":["nearMiss","minor","moderate","major","critical"]},
"IncidentStatus": {"type":"string","enum":["reported","underInvestigation","actionRequired","closed"]},
"InventoryStockReservation": {"type":"object","x-ticvai-persistence":"inventory.stock_reservation","description":"**Taken from the backend workbook, 20 September.** Temporarily reserves stock for an order or operational requirement so it cannot be allocated elsewhere.","required":["itemId","locationId","quantity","sourceType","sourceId","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"itemId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"quantity":{"type":"number","exclusiveMinimum":0},"sourceType":{"$ref":"#/components/schemas/StockReservationSourceType"},"sourceId":{"type":"string","format":"uuid","description":"The id of what the stock is reserved for: a work order, a rental agreement or an order. A uuid, as every id is (ADR-0056); it was text from 29 September to 30 September because a work order id was then 26-character text (M17-02)."},"status":{"type":"string","enum":["active","consumed","released","expired"],"readOnly":true},"expiresAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"releasedAt":{"type":"string","format":"date-time","nullable":true}}},
"LoginRequest": {"type":"object","description":"**`workstationId` is required for a device door and absent from a browser door** (CHG-DOOR-001, 2 October 2026). It was required on every login, so no browser could sign in: the TICVAI Console (ADM-001), Venue Management (SUP-001) and the partner portal (PTR-001) have no workstation. Optional in the schema is additive against r1; the rule moved to where it belongs, the device-bound methods: `pin`, `card` and `rfid` without a `workstationId` are refused 400 (`workstation-required`). A `password` sign-in from a till, handheld or scanner still sends it, because the workstation decides the Sale Board, the hardware and the till identity (never a permission, ADR-0002).\n","required":["username","credential"],"properties":{"username":{"type":"string","maxLength":256},"credential":{"type":"string","description":"Password, PIN, card token or RFID token depending on `method`.\n","maxLength":512,"writeOnly":true},"method":{"type":"string","description":"**`pin` is how a till is actually used.** A cashier signs in at a shared terminal between guests, and a password on a touchscreen with somebody waiting is a password that gets shortened, shared or written on the drawer. The employee number goes in `username` and the PIN in `credential`, so the shape of the request does not change — only what the operator types.\n\n**A PIN is weaker than a password and the difference is bounded by the device, not by the secret.** A `pin` (like `card` and `rfid`) is accepted only with a `workstationId`, refused 400 `workstation-required` without one (CHG-DOOR-001), and the workstation is *NOT a permission source*: it says which till, and the till is on a venue network in a staff area. A PIN is a reasonable credential there and nowhere else, which is why this is an enum value and not a policy flag — a surface that wants it has to ask for it by name.\n\nAdded 10 September 2026 for `POS-000 Sign In`.\n","enum":["password","pin","card","rfid","sso"],"default":"password"},"workstationId":{"type":"string","format":"uuid","description":"Identifies the device. Determines Sale Board, connected hardware, till identity and Access Point inheritance. NOT a permission source.\n\n**Sent by a device door, never by a browser** (CHG-DOOR-001, 2 October 2026). Required in effect for the device-bound methods `pin`, `card` and `rfid` (400 `workstation-required` without it); absent on the TICVAI Console, Venue Management and partner portal sign-ins, which have no workstation.\n"},"deviceFingerprint":{"type":"string","maxLength":256}}},
"LoginResponse": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/TokenPair"},{"type":"object","required":["requiresRoleSelection","requiresMfa"],"properties":{"requiresRoleSelection":{"type":"boolean"},"requiresMfa":{"type":"boolean","description":"True when the principal holds any permission listed in `PasswordPolicy.mfaRequiredForPermissions` (decided 28 September, audit R135). The session is not usable until `verifyMfaChallenge` succeeds on a `signIn` challenge."},"hasMfaMethod":{"type":"boolean","description":"Whether the principal has an active MFA method. With `requiresMfa` true and this false, the client must enrol one first (audit R135, R126 (5))."},"mfaMethods":{"type":"array","description":"The principal's active methods, so the client can offer the right one for the `signIn` challenge. Empty when `requiresMfa` is false.","items":{"$ref":"#/components/schemas/MfaMethod"}},"availableRoles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"session":{"$ref":"#/components/schemas/Session"}}}]},
"MediaKind": {"type":"string","enum":["image","video","audio","document","vector","font","archive","model3d"],"description":"`model3d` added 3 October 2026 (r1 additions; ADR-0069 action item 4): a glTF binary (`model/gltf-binary`, `.glb`) venue model, at most 40 MB. No rendition or derivative is generated for it; the guest app downloads the file as uploaded.\n"},
"MfaMethod": {"x-ticvai-persistence":"identity.mfa_method","type":"object","required":["id","kind","isActive","enrolledAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"label":{"type":"string","nullable":true},"maskedTarget":{"type":"string","nullable":true,"description":"Partially masked destination, so a person can tell two methods apart."},"isActive":{"type":"boolean"},"isPrimary":{"type":"boolean"},"enrolledAt":{"type":"string","format":"date-time"},"lastUsedAt":{"type":"string","format":"date-time","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ReportIncidentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","kind","severity","venueId","description","occurredAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/IncidentKind"},"severity":{"$ref":"#/components/schemas/IncidentSeverity"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"description":{"type":"string","minLength":3,"maxLength":10000},"involvedSubjectIds":{"type":"array","description":"Opaque references. Personal details live in the erasable store, so the incident record survives an erasure request intact.\n","items":{"type":"string","format":"uuid"}},"involvedStaffPrincipalIds":{"type":"array","items":{"type":"string","format":"uuid"}},"witnessCount":{"type":"integer"},"firstAidGiven":{"type":"boolean","default":false},"emergencyServicesCalled":{"type":"boolean","default":false},"attachmentRefs":{"type":"array","items":{"type":"string"}},"occurredAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"}}},
"ResolutionCode": {"type":"string","enum":["repaired","partReplaced","adjusted","cleaned","noFaultFound","referredExternal","replaced","deferred"]},
"RoleSummary": {"x-ticvai-persistence":"none — projection over role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"isPrimary":{"type":"boolean"}}},
"ScanOutcome": {"type":"string","enum":["admitted","denied","overridden"]},
"ServiceSummary": {"x-ticvai-persistence":"none — computed from fnb.table_visit, the orders and payments on it","type":"object","description":"One server's service day (`getServiceSummary`, CHG-CSA-020).","required":["date","covers","tables"],"properties":{"date":{"type":"string","format":"date"},"covers":{"type":"integer"},"tables":{"type":"integer","description":"Table visits served."},"sales":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Excluding VAT, as `grossSales` (CHG-FIN-007)."},"tips":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"openTables":{"type":"integer","description":"Visits still open, with their bills not yet settled."}}},
"Session": {"type":"object","required":["sessionId","principalId","roleId","scope","effectivePermissions"],"properties":{"sessionId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"scope":{"type":"array","description":"Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ScopeRef"}},"effectivePermissions":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/PermissionSet"}],"description":"Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"},"permissionsByScope":{"type":"array","description":"Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/ScopedPermissions"}},"saleBoardId":{"type":"string","format":"uuid","description":"Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n\n**Optional since 2 October 2026: only a till session carries it** (Chinmay, door follow-ups; CHG-CSP-002; breaking change against r1 approved as BC-001 to BC-005 in `docs/active/breaking-changes.yaml`). A browser door (ADM-001, SUP-001, PTR-001) and a staff handheld (EMP-001) sign in with no workstation since CHG-DOOR-001, so they have no board to land on and the field is absent. On a till it is the workstation's effective board: the outlet's board unless the till overrides it (`tenancy.Workstation.saleBoardSource`; CHG-CSP-006). A client reads its landing from this field when present and from its own platform otherwise.\n"},"workstation":{"$ref":"#/components/schemas/WorkstationContext"},"openedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"Shift": {"x-ticvai-persistence":"orders.pos_shift + orders.pos_shift_approval + orders.pos_shift_incident","description":"**`approvals` and `incidents` are child rows** (26 September, pull audit R099): `orders.pos_shift_approval` and `orders.pos_shift_incident`, one row per item, keyed to the shift. Until then the contract carried both and `orders.pos_shift` had nowhere to put either.\n","type":"object","required":["id","workstationId","venueId","scopePath","principalId","status","currency","currencyScale","openedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key."},"workstationId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"principalId":{"type":"string","format":"uuid","description":"Who opened it. Cash reconciles to a person and a drawer."},"principalDisplayName":{"type":"string"},"incidents":{"type":"array","description":"BL-097. **A till has exceptions and there was nowhere to write them** — a no-sale, a drawer opened without a transaction, a manager override, a guest dispute.\n**This is the log a cash-up investigation starts from**, and a shift that balances with four unexplained no-sales is not a shift that balanced.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["noSale","drawerOpen","override","voidAfterPayment","guestDispute","tillJam","priceQuery","other"]},"at":{"type":"string","format":"date-time"},"principalId":{"type":"string","format":"uuid"},"note":{"type":"string","nullable":true}}}},"status":{"$ref":"#/components/schemas/ShiftStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"depositBoxCode":{"type":"string","nullable":true},"bagNumber":{"type":"string","nullable":true},"openingFloat":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"salesTotal":{"x-ticvai-column":"gross_sales_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till took in sales, as the guest paid it — tax included: the shift's takings, not Gross sales (CHG-FIN-002, CHG-FIN-010). **Shown to the shift's own cashier only as one total across every tender** (\"Sales this shift\" on POS-025; the lead, 3 October 2026, CHG-RONEC-002): with no cash share it cannot be turned into the expected cash, so the blind close holds (CHG-FIN-003). The cash share, the tender split, `expectedCash` and `variance` stay with the supervisor.\n"},"refundsTotal":{"x-ticvai-column":"gross_refunded_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till paid back, as the guest was refunded it — tax included."},"liftsTotal":{"x-ticvai-column":"lifted_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net."},"expectedCash":{"x-ticvai-column":"expected_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"26 September, pull audit R207. **The figure the blind count was measured against**, revealed once the count is in — null until then. Until this date only `ShiftCloseResult` carried it, returned once by `closeShift`, so BO-040 could not show the over/short it exists to accept. **Null to the shift's own cashier on every read** (CHG-FIN-003, 2 October): returned only to a caller holding OVERSHORT_ACCEPT or SHIFT_CLOSE_OTHER at the venue.\n"},"countedCash":{"x-ticvai-column":"counted_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"What the close count found. Null until the shift is counted."},"variance":{"x-ticvai-column":"variance_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"Counted minus expected, as `ShiftCloseResult.variance`. Negative is short. Null to the shift's own cashier, as `expectedCash` (CHG-FIN-003)."},"cashierReason":{"type":"string","nullable":true,"readOnly":true,"enum":["tillError","unrecordedRefund","miscount","other"],"description":"What the cashier said went wrong, given with the blind count (`CloseShiftRequest.cashierReason`, DI-803) without seeing the variance; the supervisor reads it beside the variance on BO-040 (CHG-FIN-003).\n"},"cashierNote":{"type":"string","nullable":true,"readOnly":true,"maxLength":1000,"description":"The cashier's note with the count (`CloseShiftRequest.notes`; CHG-FIN-003)."},"heldLeaseCount":{"type":"integer","description":"Inventory leases currently held by this workstation. Surfaced so an operator closing a shift can see what will be returned.\n"},"openedAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time","description":"When the device recorded the open. `openedAt` is the server's time."},"suspendedAt":{"type":"string","format":"date-time","nullable":true},"suspendReason":{"type":"string","maxLength":200,"nullable":true,"description":"The `reason` given to `suspendShift`. Cleared on resume."},"closedAt":{"type":"string","format":"date-time","nullable":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who submitted the close count. `reopenShift` refuses an approver who is this principal, and until 26 September there was nothing to compare against (pull audit R099).\n"},"recountRequestedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `rejectShiftVariance`, cleared by the cashier's recount** (decided 2 October 2026, Chinmay; DEC-175; CHG-CSP-013; DI-804). While set, the shift is `pendingVariance` waiting for the cashier rather than the supervisor: the cashier's view says \"Recount requested\" instead of \"Under review\".\n"},"recountRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The supervisor who sent the count back (CHG-CSP-013)."},"recountReason":{"type":"string","nullable":true,"readOnly":true,"maxLength":500,"description":"The supervisor's reason, shown to the cashier; never an amount (CHG-CSP-013, CHG-FIN-003)."},"countNumber":{"type":"integer","minimum":0,"readOnly":true,"description":"How many close counts the shift has had: 0 before the first, 1 after it, 2 after a recount (CHG-CSP-013). The latest is the one measured.\n"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while the shift has unsynced operations."},"approvals":{"type":"array","items":{"type":"object","required":["kind","principalId","at"],"properties":{"kind":{"type":"string","enum":["open","close","variance"],"description":"`open` from `approveShiftOpen`, `close` from `approveShiftClose`, `variance` from `acceptShiftVariance`.\n"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"reason":{"type":"string"}}}}}},
"ShiftCountReceipt": {"x-ticvai-persistence":"none — computed","type":"object","description":"**What `submitShiftCount` returns to the cashier: what happens next, never the figure** (CHG-FIN-003). No expected cash, no variance, no over or short.\n","required":["shiftId","status","outcome","countedAt"],"properties":{"shiftId":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/ShiftStatus"},"outcome":{"type":"string","enum":["closed","referredToSupervisor","awaitingCloseApproval"],"description":"`closed`: within the venue's threshold, the shift is closed. `referredToSupervisor`: a supervisor reviews the count (`pendingVariance`); the till says \"Your count is with your supervisor\" and nothing about the amount. `awaitingCloseApproval`: the venue supervises every close (`pendingClosure`).\n"},"countedAt":{"type":"string","format":"date-time"},"countNumber":{"type":"integer","minimum":1,"description":"1 for the first count of the close, 2 for a recount the supervisor asked for, and so on."}}},
"ShiftStatus": {"type":"string","enum":["pendingApproval","open","suspended","pendingVariance","pendingClosure","closed","autoClosed"]},
"SsoProtocol": {"type":"string","enum":["oidc","saml2"]},
"SsoProvider": {"x-ticvai-persistence":"identity.sso_provider","type":"object","required":["id","displayName","protocol"],"properties":{"id":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"protocol":{"$ref":"#/components/schemas/SsoProtocol"},"iconAssetRef":{"type":"string","nullable":true},"isEnforced":{"type":"boolean","description":"True disables password login for principals covered by this provider."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope**; the server sets it and ignores it in a request."}}},
"StockReservationSourceType": {"type":"string","enum":["workOrder","rentalAgreement","order","transfer","other"],"description":"What a stock reservation is for (decided 17 September, M17-02; `rentalAgreement` is the existing use from `rental.agreement_item`)."},
"SupervisorStepUp": {"type":"object","description":"**A supervisor signs the act in place, on the device making the call** (decided 28 September, audit R144). Used where the decision is a same-device step-up rather than an approval request: reopening a shift, recounting a stock count, a retail return above the venue threshold, and (proposed by the coordinator, client to confirm) closing a stock transfer short and cancelling a performance.\n\n**The verification rule, the same on every operation that takes it:** the server checks `credential` against `principalId`; that principal must hold the operation's `x-ticvai-permission` at the operation's scope, must be active at that venue, and must not be the person whose act is being reversed where the operation says so. Any failure is a `403` (`supervisor-step-up-refused`) and nothing is written. **No approval request is raised**, and the operation declares `x-ticvai-step-up: pin`.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid","description":"The supervisor signing. Recorded against the act."},"credential":{"type":"string","maxLength":512,"writeOnly":true,"description":"The supervisor's staff PIN, as they sign in at a till with it. **A PIN, never a password** (audit R123 (7)). Never stored or returned."}}},
"TicketStatus": {"x-ticvai-persistence":"none — computed from entitlement and scans","description":"**A validation result, not a lifecycle**, despite the name. Computed at scan time from the entitlement and its scan history — `isValid`, `entriesUsed`, `isInsideVenue`.\n**The name misled a state model into anchoring on it** (`states/entitlement.yaml`, removed 18 August): six lifecycle states were checked against an object with no values, and `check-states` warned about it for a day before anyone read the schema.\nThe entitlement's lifecycle is `orders.EntitlementStatus`. **This is what a gate learns when it scans**, which is a different question with a similar name.\n","type":"object","required":["ticketId","isValid"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"Stable for the life of the ticket, independent of the media carrying it."},"mediaCode":{"type":"string","nullable":true},"productName":{"type":"string"},"holderName":{"type":"string","nullable":true,"description":"Present only where the entitlement is name-bound. Identity and entitlement are separate concerns; most entitlements carry no holder.\n"},"isValid":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesUsed":{"type":"integer"},"entriesAllowed":{"type":"integer","nullable":true,"description":"Null means unlimited."},"reentryAllowed":{"type":"boolean"},"isInsideVenue":{"type":"boolean","description":"Derived from the last scan. Drives anti-passback evaluation."},"issuingCellId":{"type":"string","nullable":true,"description":"Present when this entitlement was issued in a different cell and is being redeemed here as a delegated right (ADR-0010). Null for locally issued tickets.\n"},"guestLinkId":{"type":"string","nullable":true,"description":"Pseudonymous cross-region guest reference. Present only on delegated rights. Carries no personal data.\n"},"admissionRulesId":{"type":"string","format":"uuid"},"denyReason":{"$ref":"#/components/schemas/DenyReason"}}},
"TokenPair": {"x-ticvai-persistence":"none — transient","type":"object","required":["accessToken","refreshToken","expiresIn"],"properties":{"accessToken":{"type":"string","description":"JWT carrying `sid`, validated per request against the session registry."},"refreshToken":{"type":"string"},"expiresIn":{"type":"integer","description":"Seconds"}}},
"ValidateRequest": {"type":"object","required":["id","mediaCode","mediaKind","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key and dedupe key."},"mediaCode":{"type":"string","maxLength":256,"description":"What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life.\n"},"mediaKind":{"$ref":"#/components/schemas/MediaKind"},"direction":{"$ref":"#/components/schemas/Direction"},"groupSize":{"type":"integer","minimum":1,"description":"For group media admitting several holders on one read."},"proximityToken":{"type":"string","description":"BLE proximity assertion where the venue requires the operator to be physically at the gate. Absent where not configured.\n"},"recordedAt":{"type":"string","format":"date-time","description":"Device time of the read. Authoritative for ordering, not for validity."}}},
"ValidationResult": {"x-ticvai-persistence":"none — computed, persisted as scan_event","type":"object","required":["scanId","outcome","accessPointId","recordedAt"],"properties":{"scanId":{"type":"string","format":"uuid"},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"denyDetail":{"type":"string","description":"Human-readable, localised. For operator display, never for logic."},"denyCause":{"type":"string","nullable":true,"enum":["attractionTemporarilyClosed","timeBoundWindowElapsed","offlineLimitExceeded"],"description":"**The finer cause of three denials decided on 2 October 2026**, beside the r1 `denyReason` a client already switches on (a new `DenyReason` value would be a breaking change against r1; CHG-CSP-026, CHG-CSP-030, CHG-CSP-035). `attractionTemporarilyClosed` (DEC-228): `denyReason` `outsideAdmissionWindow`, with `reopensAt` and `queueReturnOffer`. `timeBoundWindowElapsed` (DEC-232): a time-bound entitlement scanned after its window from first scan, `denyReason` `expired`. `offlineLimitExceeded` (DEC-426): a reader offline longer than the venue's `AccessOfflinePolicy.maxOfflineDurationHours` refusing a tap it cannot check, `denyReason` `outsideAdmissionWindow`. Null for every other denial."},"reopensAt":{"type":"string","format":"date-time","nullable":true,"description":"When a temporarily closed attraction expects to reopen, where known (DEC-228; CHG-CSP-026)."},"queueReturnOffer":{"type":"object","nullable":true,"description":"A virtual-queue return window offered at a denied scan of a temporarily closed attraction, where the venue enables it (DEC-228; CHG-CSP-026). Taking it is `queue.joinQueue`.","properties":{"queueId":{"type":"string","format":"uuid"},"returnWindowStart":{"type":"string","format":"date-time"},"returnWindowEnd":{"type":"string","format":"date-time"}}},"accessPointId":{"type":"string","format":"uuid"},"ticket":{"$ref":"#/components/schemas/TicketStatus"},"admittedCount":{"type":"integer","description":"Holders admitted on this read. Differs from groupSize on partial admission."},"recordedAt":{"type":"string","format":"date-time"},"serverEvaluatedAt":{"type":"string","format":"date-time"},"advisory":{"type":"object","nullable":true,"description":"BL-179, CF-130. **What a device observed, for the steward, never for the gate.** Present only where an access point's device reports the matching `DeviceCapability` and the venue has turned the corresponding setting on.\n**Never persisted.** This schema is computed and stored as `access.scan_event`, and the advisory is deliberately not part of what is stored: an inferred classification kept against a guest is sensitive personal data with no consent behind it. **A guest agreed to be admitted, not to be classified** — Face Pass and Face Tag carry `consent_purpose_id` and `consent_given_at` because somebody enrolled, and nobody enrols in being looked at by a turnstile. `scan_event` records that an override happened and never what the device thought, which keeps `overrideRateAlertThreshold` working without building a register nobody agreed to.\n**It cannot reach `outcome` or `denyReason`.** Those are decisive and `entitlementGated` is `true` and read-only: the gate admits on the entitlement, and everything here sits on top of that without replacing any of it.\n","properties":{"genderClassification":{"type":"string","enum":["women","men","undetermined"],"description":"**`undetermined` is a real answer and the most common one to design for.** A classifier that never returns it is one that has been tuned to look confident.\n"},"confidence":{"type":"number","minimum":0,"maximum":1,"description":"**Required reading for the steward, not decoration.** An advisory with no confidence is read as a fact, and `overrideRateAlertThreshold` exists to catch exactly the failure that produces — *an override rate near zero means the steward has stopped deciding.* That number only means anything if the steward could see how sure the device was.\n"},"reportedByDeviceId":{"type":"string","format":"uuid","description":"**Which device said it.** A classifier that degrades is one camera, not a venue, and an advisory nobody can trace to hardware cannot be investigated or switched off alone.\n"}}}}},
"WithdrawalReason": {"type":"string","description":"Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records.","enum":["banking","safeDrop","changeOrder","other"]},
"WorkOrder": {"x-ticvai-persistence":"maintenance.work_order","x-ticvai-retired-columns":["is_overdue"],"type":"object","required":["id","workOrderNumber","title","venueId","status","priority","kind","createdAt"],"properties":{"downtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"},"rootCause":{"type":"string","nullable":true,"enum":["wearAndTear","operatorError","guestDamage","manufacturingDefect","environmental","softwareFault","powerFailure","deferredMaintenance","unknown"],"description":"**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"},"rootCauseNote":{"type":"string","nullable":true},"escalatedAt":{"type":"string","format":"date-time","nullable":true},"escalationLevel":{"type":"integer","default":0,"description":"**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"},"id":{"type":"string","format":"uuid"},"workOrderNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"title":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"assetName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"},"status":{"$ref":"#/components/schemas/WorkOrderStatus"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"priorityScore":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"readOnly":true,"description":"The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."},"prioritySource":{"type":"string","enum":["scored","assetOverride","manual"],"readOnly":true,"description":"Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","items":{"type":"string"},"description":"Skills the job needs (M17-13)."},"kind":{"$ref":"#/components/schemas/WorkOrderKind"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"raisedByPrincipalId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"},"locationDescription":{"type":"string","maxLength":500,"nullable":true,"description":"Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"},"elapsedMinutes":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"},"isTimerRunning":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"},"dueAt":{"type":"string","format":"date-time","nullable":true},"isOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"},"requiresVerification":{"type":"boolean"},"sourcePlanId":{"type":"string","format":"uuid","nullable":true},"sourceInspectionId":{"type":"string","format":"uuid","nullable":true},"sourceIncidentId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrderAttachment": {"type":"object","x-ticvai-persistence":"maintenance.work_order_attachment","required":["id","workOrderId","kind","capturedAt"],"properties":{"id":{"type":"string","format":"uuid"},"workOrderId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["photo","video","document","note","signature"]},"assetRef":{"type":"string","format":"uuid","nullable":true},"text":{"type":"string","nullable":true},"stage":{"type":"string","enum":["before","during","after","signOff"],"nullable":true},"capturedByPrincipalId":{"type":"string","format":"uuid"},"capturedAt":{"type":"string","format":"date-time","description":"Device time. **Distinct from when it synced** — a photo taken at 09:14 in a basement and uploaded at 11:40 is evidence of the first, not the second.\n"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrderDetail": {"x-ticvai-persistence":"maintenance.work_order","allOf":[{"$ref":"#/components/schemas/WorkOrder"},{"type":"object","properties":{"description":{"type":"string","nullable":true},"resolution":{"type":"string","nullable":true},"resolutionCode":{"$ref":"#/components/schemas/ResolutionCode"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"timeEntries":{"type":"array","items":{"type":"object","properties":{"action":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"pauseReason":{"type":"string","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}}},"parts":{"type":"array","items":{"type":"object","properties":{"inventoryItemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"quantity":{"type":"number"},"reservedQuantity":{"type":"number","description":"Still reserved for this work order and not yet issued (M17-02)."},"cost":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"labourCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"partsCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","x-ticvai-column":"net_cost_amount"},"completedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who called `completeWorkOrder`. **What `verifyWorkOrder` compares against** — the verifier may not be the technician who completed the work, and the assignee is not necessarily that person.\n"},"followUpRequired":{"type":"boolean","default":false},"followUpNote":{"type":"string","maxLength":1000,"nullable":true},"verificationOutcome":{"type":"string","enum":["verified","rejected"],"nullable":true,"description":"The latest `verifyWorkOrder` outcome."},"verificationNote":{"type":"string","maxLength":1000,"nullable":true},"verifiedAt":{"type":"string","format":"date-time","nullable":true},"verifiedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"cancelReason":{"type":"string","enum":["raisedInError","duplicate","superseded","noLongerRequired"],"nullable":true},"cancelNote":{"type":"string","maxLength":300,"nullable":true},"supersededByWorkOrderId":{"type":"string","format":"uuid","nullable":true,"description":"Set by `cancelWorkOrder` where the reason is `superseded`."},"cancelledAt":{"type":"string","format":"date-time","nullable":true},"closeOutcome":{"type":"string","enum":["completedAndVerified","notReproducible","supersededByReplacement","noLongerApplicable","duplicate"],"nullable":true},"closeNote":{"type":"string","maxLength":500,"nullable":true},"duplicateOfWorkOrderId":{"type":"string","format":"uuid","nullable":true,"description":"Set by `closeWorkOrder` where the outcome is `duplicate`."},"closedAt":{"type":"string","format":"date-time","nullable":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true}}}]},
"WorkOrderFaultAssessment": {"x-ticvai-persistence":"none — columns on maintenance.work_order","type":"object","description":"What the person raising a fault says about it, which the priority score reads (M17-01).","properties":{"safetyRisk":{"type":"boolean","default":false},"guestImpact":{"type":"string","enum":["none","degraded","closed"],"default":"none"}}},
"WorkOrderKind": {"type":"string","enum":["corrective","planned","inspectionFollowUp","incidentCorrective","improvement"]},
"WorkOrderPriority": {"type":"string","enum":["low","normal","high","urgent","emergency"]},
"WorkOrderStatus": {"type":"string","enum":["open","assigned","inProgress","paused","awaitingParts","completed","verified","closed","cancelled"]},
"WorkstationContext": {"type":"object","required":["id","code","venueId","regionId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid","description":"Inherited from the workstation, never selected by the operator."},"devices":{"type":"array","items":{"type":"object","required":["kind","driver"],"properties":{"kind":{"type":"string","enum":["receiptPrinter","ticketPrinter","cashDrawer","barcodeScanner","rfidReader","paymentTerminal","customerDisplay"]},"driver":{"type":"string"},"identifier":{"type":"string"}}}},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"timezone":{"type":"string"},"cellName":{"type":"string","description":"The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"},"deploymentProfile":{"type":"string","enum":["terminalLocal","venueEdge","thin"],"description":"Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"}}}
}
```
