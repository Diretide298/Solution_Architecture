# P04-not-in-v2-01 — P04 · Screens the v2 build does not draw

**7 screens · 18 operations · 37 schemas · 12 permissions**

Platform P04 Venue POS · ships as **venue-pos** ·
staff audience · posTerminal ·
offline-capable

## Why this batch is drawn

No view in the POS v2 build or the approved build. The frames on disk were drawn in Claude Design on 29 September in the approved build's style; draw them again in v2's look (handoff/design-batches/apps/2-pos/README.md). POS-009 and POS-015 build on v2's shift panel, without 'Expected in drawer' (POS v2 decision POSV2-3). The look to match is `sources/designs/TICVAI_POS_Terminal_v2.html` (its shift panel: `wireframes/incoming/P04-pos-v2/img/v2-shift.jpg`), not the approved build below.

## Who this is for

**staff on posTerminal.** Everything below is how you know what is
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
  `ASSET_LIBRARY_VIEW, ATTENDANCE_RECORD, CASH_LIFT, ORDER_CREATE, ORDER_EXCHANGE, ORDER_VIEW, PRODUCT_CONFIGURE, REPORT_VIEW_WORKSTATION, SCOPE_VIEW, SHIFT_OPEN, WORKFORCE_VIEW, WORKSTATION_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **11 of these operations work offline**: createCashMovement, getMediaAsset, getMediaEntitlements, getTableMap, getTillShiftPolicy, listCashMovements, listDepositBoxes, listRotaAssignments
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `POS-009` | Staff Roster | A | 8 | 24 | 6 | 18 | 1 | 0 | — | notStarted (designed) |
| `POS-010` | Add to Existing Ticket | A | 37 | 39 | 5 | 44 | 3 | 0 | — | notStarted (designed) |
| `POS-015` | Cash Operations Dashboard | A | 0 | 54 | 6 | 0 | 2 | 6 | — | notStarted (designed) |
| `POS-017` | Cash In / Cash Out Operations | A | 21 | 0 | 5 | 0 | 2 | 6 | — | notStarted (designed) |
| `POS-018` | Safe Drop & Cash Transfer Management | A | 24 | 20 | 6 | 1 | 1 | 6 | — | notStarted (designed) |
| `POS-019` | Shift Templates & Policies | A | 10 | 32 | 6 | 1 | 1 | 6 | — | notStarted (designed) |
| `POS-024` | Outlet Setup | A | 20 | 18 | 6 | 3 | 0 | 0 | — | notStarted (designed) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `POS-009` Staff Roster

**See who is on duty and on which terminal.**

| | |
|---|---|
| App · platform | TICVAI POS · P04 Venue POS (terminal) |
| Module | Shift · wave 2 · needs the `core` module |
| Block | Block A · ticket #18136 (APP-POS-POS-009) |
| Who uses it | venue staff holding `ATTENDANCE_RECORD`, `REPORT_VIEW_WORKSTATION`, `WORKFORCE_VIEW` (2 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is a touch terminal, 1366 x 768 landscape; the kitchen display is a wall screen at 1920 x 1080. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (touchLarge density): `approveShiftOpen` decides items that `listShifts` queues — every row is waiting for a person, so the empty state is success |
| Offline | Last known roster, with its age shown |
| Opens with | `shiftId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/sell/staff-roster` |

**What the spec says about it.** Close (POS-007) counts each foreign currency separately (`foreignHoldings`). **A variance collapsed into a base-currency total cannot be attributed to the currency that caused it.** **createCashMovement removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class). **Improved 20 August against the client design board**, answering 2 board screen(s): Shift & Operator Dashboard; Operator & Workstation Assignment. **Owns POS board frame(s) POS-3A** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Blind close** (decided 2 October 2026, Chinmay; CHG-FIN-003): closing from here submits the cashier's blind count with `submitShiftCount` (no expected cash, no variance shown; the supervisor is alerted beyond the threshold); `closeShift`, which returns the expected figure, is the supervisor's path on BO-039 and BO-040. Foreign-currency counting belongs to the close (POS-007), not the roster (design-notes correction fnb-retail POS-009; CHG-SPO-015).

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): A roster is a read plus attendance; twelve shift and money operations, the workstation and alert tables and rota planning (createRotaAssignment, a back-office … Removed 2 October 2026 (CHG-WIR-008): A roster is a read plus attendance; twelve shift and money operations, the workstation and alert tables and rota planning (createRotaAssignment, a back-office … Removed 2 October 2026 (CHG-WIR-008): A roster is a read plus attendance; twelve shift and money operations, the workstation and alert tables and rota planning (createRotaAssignment, a back-office …

**From the Food, Beverage & Retail process.** Who is on duty right now, on which till, and their own clock: a supervisor sees the venue's staff on shift (role, till, shift times, status), and any staff member clocks in or out and starts or ends a break here — the v2 shift panel's Clock Out and Start Break moved here (POSV2-3). The one thing to get right: attendance (clock) and the cash shift are separate — clocking out does not close a drawer.

**Fixed on main** (the package already carries these; draw what it says): Twelve shift operations (open, close, accept variance, approve open, reopen, resume, suspend, no-sale, cash movements) are attached with … (CHG-WIR-008); The screen notes describe foreign-currency counting at close ("Close counts each foreign currency separately"). (CHG-SPO-015); createRotaAssignment ("Create rota assignment") is on the till. (CHG-WIR-008).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Opened from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedFrom=` to `listShifts`. | `listShifts` ?openedFrom |
| Opened to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedTo=` to `listShifts`. | `listShifts` ?openedTo |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listShifts` ?workstationId |
| Status | select | — | Pending approval · Open · Suspended · Pending variance · Pending closure · Closed · Auto closed | `listShifts` ?status |
| From | date picker | — | — | `listRotaAssignments` ?from |
| To | date picker | — | — | `listRotaAssignments` ?to |
| Principal | picker: choose a principal | — | — | `listRotaAssignments` ?principalId |
| Department | picker: choose a department | — | — | `listRotaAssignments` ?departmentId |

**Form: Clock in, clock out, start or end a break** (modal, opened by *Clock in, clock out, start or end a break*; *Record* calls `recordAttendance`, *Cancel* sends nothing)

**Collects what `recordAttendance` sends before it is called.** Required: `kind` (clockIn, clockOut, breakStart, breakEnd) and `occurredAt`, the device time. Optional: `assignmentId`, `accessPointId`. An out-of-sequence clock (a clock-out with no clock-in) is refused 409 and reported, never corrected. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Clock in · Clock out · Break start · Break end | — | — | `recordAttendance` body |
| Occurred at `occurredAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time. The server records both this and when it arrived. | `recordAttendance` body |
| Assignment `assignmentId` | picker: choose an assignment | optional | — | — | shows names, sends the id | — | `recordAttendance` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | — | `recordAttendance` body |
| Latitude `latitude` | number field | optional | — | — | — | — | `recordAttendance` body |
| Longitude `longitude` | number field | optional | — | — | — | — | `recordAttendance` body |

Errors to draw in the form: 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported rather than silently corrected.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Clock in / out, Start / End break**: One tap each; device time recorded and queued offline; at a venue that requires it, the access point or location is captured. *(source: contracts/satellite/workforce.yaml#recordAttendance / POSV2-3)*

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listShifts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |

**Every rota assignment** (data table, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Rest period before | 1,234 | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and … |
| Breaches working hour limit | yes / no (icon or chip) | Flagged at assignment, not discovered at payroll. A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a … |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Display name | text | — |
| Venue | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Position | text | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota … |
| Required role | the name it points at, never the id | Checked on assignment. A rota naming someone unqualified is a rota that gets overridden. |
| Workstation | the name it points at, never the id | Where the position needs a till. The link between a rota and a cash session, without merging the two. |

**Data table** (data table): Staff, role and terminal, shift, sales, status — the columns in the design

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Clock in, clock out, start or end a break (secondary button) | `recordAttendance` POST `/attendance/clock` | inline | AttendanceRecord | 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported rather than silently corrected. | works offline; gated `ATTENDANCE_RECORD`; opens modal first |
| Export roster (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Roster**: Rows: staff name, role, till, rota time, attendance (on duty / on break / not clocked in), shift status (Open, Suspended, Waiting for supervisor). Sorted by till. A cashier without the view permission sees only themselves. *(source: contracts/satellite/workforce.yaml#listRotaAssignments / contracts/spine/shift.yaml#listShifts)*
- **My shift**: Start time, elapsed time and breaks taken today. No takings and no expected cash. *(source: POSV2-3 / DI-806)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Clock out**: Records attendance only; "Clocking out pauses selling but keeps the cash shift open — close the shift to count the drawer." *(source: POSV2-3 / contracts/satellite/workforce.yaml#recordAttendance)*

**Data it reads**: `listShifts` (onLoad, Open shifts at this venue); `listRotaAssignments` (onLoad, The rota)

**Where the user goes next**

- → `POS-001` Begin Shift: *Begin Shift*; carries `shiftId`
- → `POS-007` Close Shift: *Close Shift*
- → `BO-043` Daily Reconciliation: *The daily cash reconciliation lists every shift of the day and resolves the ones still under review, one by…*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staff roster list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staff roster untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on workstationId, status, openedFrom, openedTo and the staff roster are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Last known roster, with its age shown |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported rather than silently corrected. |

#### Edge cases to draw

- **Clock-out with no clock-in, or a second clock-in**: Refused and reported as out of sequence, not silently corrected. *(source: contracts/satellite/workforce.yaml#recordAttendance)*
- **Offline**: Last known roster with its age; clock actions queue with device time. *(source: screens/P04-point-of-sale.yaml#POS-009)*

#### Consistency with other screens

- Match `POS-025`: The On shift pill opens this panel; it carries no Expected in drawer (POSV2-3).
- Match `EMP-003`: Clock in/out uses the same attendance record as the staff app.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
roster:
- name: J. Smith
  role: Senior Cashier
  till: Gate A · Till 14
  rota: 09:30–18:00
  status: On duty · shift open since 09:42
- name: Fatima Al Suwaidi
  role: Cashier
  till: Bite & Go · Till 3
  rota: 11:00–19:30
  status: On break since 14:05
- name: Omar Ziad
  role: Supervisor
  till: —
  rota: 10:00–22:00
  status: On duty
```

#### Permissions

- `listShifts` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listRotaAssignments` → `WORKFORCE_VIEW` (read) · staff
- `recordAttendance` → `ATTENDANCE_RECORD` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.11 | The system should be able to generate operational rosters for staff resources. The rosters should provide information on the staff resources associated with an attraction, their availability, booked … | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.32 | System shall support staff scheduling and assignment. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.33 | System shall manage employee shifts. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.60 | Employees shall receive assignments on mobile devices. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.61 | Employees shall check into assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.62 | Employees shall check out assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.63 | Employees shall view schedules via mobile app. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 18.1.1 | iOS Mobile Application - System shall provide a native iOS application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 18.1.2 | Android Mobile Application - System shall provide a native Android application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 1.2.81 | System shall record planned shifts, actual check-in times, actual check-out times, attendance status, lateness, early departures, no-shows, overtime hours, attendance exceptions, and workforce … | Ticketing Catalogue | CONTRACTED | `recordAttendance` |
| 18.9.1 | Attendance Management - Users shall clock in and clock out. | Employee Mobile App & AI Assistant | CONTRACTED | `recordAttendance` |
| 18.9.2 | Shift Management - Users shall view assigned shifts. | Employee Mobile App & AI Assistant | CONTRACTED | `recordAttendance` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Shift management: assignment and scheduling by cashier/department, templates and policies, opening/closing, exceptions/alerts. Allam: explore merging shift-closing and till-closing screens to reduce dashboard count. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-309)*

Also apply: 41 for all of P04, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P04 Venue POS.dc.html#pos-009` · status **notStarted** · provenance designed · **Drawn by Claude Design on `POS Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Prototype (TICVAI OS 4.2.1, build 2026.08.14, verified —, match none): `sources/designs/TICVAI_POS_Terminal_client_approved.html`, view **
- Derived from `wireframes/reference/POS Board 3.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 3.dc.html#pos-3a`
- Flow F74 *A shift closes and the day is reported*, step 3: Staffing against takings is read. → **Takings per staffed hour is the number a venue manager actually wants**, and it needs both sides.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (403, 409).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#POS-009?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Clock in, clock out, start or end a …, Export roster.
- [ ] Every transition is wired: `POS-001`, `POS-007`, `BO-043`.
- [ ] Every gated control is gated: `ATTENDANCE_RECORD`, `REPORT_VIEW_WORKSTATION`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `POS-010` Add to Existing Ticket

**Sell something onto media the guest is already carrying.**

| | |
|---|---|
| App · platform | TICVAI POS · P04 Venue POS (terminal) |
| Module | Sell · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #18001 (APP-POS-POS-010) |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW`, `ORDER_CREATE`, `ORDER_EXCHANGE`, `ORDER_VIEW` (2 read, 2 operate); in the flows as cashier |
| Device and orientation | This is a touch terminal, 1366 x 768 landscape; the kitchen display is a wall screen at 1920 x 1080. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (touchLarge density): `getMediaEntitlements` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Not available.** The entitlement set must be read live; appending to a stale picture double-sells a locker |
| Opens with | `mediaCode` (deepLink), `mediaId` (deepLink), `cartId` (session), `orderId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/sell/add-to-existing-ticket` |

**What the spec says about it.** CF-58, from the 14 August MoM. Not in the delivered mockups. **9 assets operations removed 18 August (CF-114).** The whole media contract was attached to this screen. **A till adding an item to a ticket does not manage a media library** — it reads the asset it needs and nothing else. Same shape as CF-87, one level up: that attached sibling operations, this attached a whole contract. **Wired 24 August from review**: getCart, exchangeOrderLines. **The operations existed and this screen could not call them** — reviewers reported them as missing APIs, which is what an unreachable operation looks like from a wireframe.

**From the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process.** Add something (a locker, Fast Track, a meal) to a ticket the guest already holds, by scanning it. Block A. The add-on joins the existing QR, never a new one; surrendered, expired or blocked media is refused before money is taken.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No prototype frame (match none). (CHG-SPO-020)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
|  | scan target | — | — | — | — | Scan the guest QR, wristband or card first. The media is the join, not the order | — |

**Form: Append entitlement to media** (modal, opened by *Append entitlement to media*; *Append entitlement to media* calls `appendEntitlementToMedia`, *Cancel* sends nothing)

**Collects what `appendEntitlementToMedia` sends before it is called.** Required: `id`, `lines`, `recordedAt`. Optional: `paymentMethod`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the new order this creates, and its idempotency key — it must equal the `Idempotency-Key` header. | `appendEntitlementToMedia` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `appendEntitlementToMedia` body |
| Variant `lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `appendEntitlementToMedia` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `appendEntitlementToMedia` body |
| Performance `lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `appendEntitlementToMedia` body |
| Payment method `paymentMethod` | radio group | optional | — | Card · Cash · Wallet · Gift card · Charge to account | — | — | `appendEntitlementToMedia` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `appendEntitlementToMedia` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `appendEntitlementToMedia` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Media expired (`mediaExpired`), blocked (`mediaBlocked`), already surrendered at exit (`mediaSurrendered`), or the entitlement cannot share media … (AppendRefusedProblem)

**Form: Exchange order lines** (modal, opened by *Exchange order lines*; *Exchange order lines* calls `exchangeOrderLines`, *Cancel* sends nothing)

**Collects what `exchangeOrderLines` sends before it is called.** Required: `id`, `outgoingLineIds`, `incomingLines`, `recordedAt`. Optional: `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header. | `exchangeOrderLines` body |
| Outgoing lines `outgoingLineIds` | multi-picker: choose outgoing lines | required | — | at least 1 | — | — | `exchangeOrderLines` body |
| Incoming lines `incomingLines` | repeatable rows | required | — | at least 1 | — | — | `exchangeOrderLines` body |
| ID `incomingLines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `exchangeOrderLines` body |
| Variant `incomingLines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `exchangeOrderLines` body |
| Recommendation `incomingLines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `exchangeOrderLines` body |
| Performance `incomingLines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `exchangeOrderLines` body |
| Booked window `incomingLines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `exchangeOrderLines` body |
| Starts at `incomingLines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `exchangeOrderLines` body |
| Ends at `incomingLines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `exchangeOrderLines` body |
| Inventory hold `incomingLines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `exchangeOrderLines` body |
| Seats `incomingLines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `exchangeOrderLines` body |
| Resource hold `incomingLines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `exchangeOrderLines` body |
| Attributes `incomingLines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `exchangeOrderLines` body |
| Transport `incomingLines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `exchangeOrderLines` body |
| Quantity `incomingLines[].quantity` | number field | required | — | min 1 | — | — | `exchangeOrderLines` body |
| Eligibility declaration `incomingLines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `exchangeOrderLines` body |
| Age band `incomingLines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `exchangeOrderLines` body |
| Age years `incomingLines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `exchangeOrderLines` body |
| Height band index `incomingLines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `exchangeOrderLines` body |
| Confident swimmer `incomingLines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `exchangeOrderLines` body |
| Guardian signed `incomingLines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `exchangeOrderLines` body |
| Quoted unit price `incomingLines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `exchangeOrderLines` body |
| Holder name `incomingLines[].holderName` | text field | optional | — | — | — | — | `exchangeOrderLines` body |
| Data mask values `incomingLines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `exchangeOrderLines` body |
| Waive fee `waiveFee` | toggle | optional | off | — | — | — | `exchangeOrderLines` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `exchangeOrderLines` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `exchangeOrderLines` body |

Errors to draw in the form: 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem)

**Rules for these inputs** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **ticket scan**: Scan or type the ticket's code; shows what it already includes and what can be added. *(source: DI-295; F58 step 7)*

#### Outputs: what the screen shows and produces

**Shown**

**The media entitlements** (detail panel, from `getMediaEntitlements`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Media kind | chip: QR, Wristband, Card, NFC, Mobile pass | — |
| Subject | the name it points at, never the id | — |
| Is valid | yes / no (icon or chip) | — |
| Invalid reason | text | — |
| Can accept more | yes / no (icon or chip) | False where the media has been surrendered, expired or blocked. A cashier should know before taking money, not after. |
| Entitlements | list or chips (count when long) | — |

**The media asset** (detail panel, from `getMediaAsset`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Image, Video, Audio, Document, Vector, Font… | — |
| Status | chip: Processing, Ready, Quarantined, Failed, Archived | — |
| Filename | text | — |
| Content type | text | — |
| Size bytes | 1,234 | — |
| Title | in the reader's language | — |
| Description | in the reader's language | Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored. |
| Alt text | in the reader's language | Required before use in a guest-facing surface. WCAG 2.2 AA. |
| Width | 1,234 | — |
| Height | 1,234 | — |
| Duration seconds | 1,234.5 | — |
| Custom metadata | grouped details | BL-178. `assets` is a strong contract and its metadata was fixed — kind, title, alt text, dimensions, rights. |
| Shared with tenants | list or chips (count when long) | BL-178. Cross-tenant sharing, and it is refused by default for a reason. |
| Tags | list or chips (count when long) | — |
| Venue | the name it points at, never the id | — |

**The cart** (detail panel, from `getCart`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Token | text | How an anonymous guest returns to their cart, including from a recovery email. Rotated on claim, so a link shared before signing in does … |
| Venue | the name it points at, never the id | — |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing … |
| Subject | the name it points at, never the id | Null while anonymous. Set by `claimCart`. |
| Status | chip: Active, Expiring, Expired, Abandoned, Checked out | — |
| Lines | list or chips (count when long) | — |
| Conflicts | list or chips (count when long) | — |
| Subtotal | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Discount total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied promotions | list or chips (count when long) | Re-evaluated on every read. A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became … |
| Expires at | 1 Oct 2026, 14:30 | The earliest lease expiry in the cart, or the cart's own window where it holds none. |
| Extensions used | 1,234 | — |
| Max extensions | 1,234 | — |

**Detail panel** (detail panel): What they already hold — so a cashier does not sell a locker to someone who has one

**Banner** (banner): Surrendered, expired or blocked media is refused before money is taken, not after

**Sale board** (sale board): Only variants whose template allows canShareMedia

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Append entitlement to media (primary button) | `appendEntitlementToMedia` POST `/media/{mediaCode}/entitlements` | AppendEntitlementRequest | AppendEntitlementResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Media expired (`mediaExpired`), blocked (`mediaBlocked`), already surrendered at exit (`mediaSurrendered`), or … | opens modal first; produces a document or message: Add something to a ticket the guest already holds |
| Exchange order lines (secondary button) | `exchangeOrderLines` POST `/orders/{orderId}/exchanges` | ExchangeOrderRequest | OrderExchangeResult | 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem) | opens modal first |
| Add and pay (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce (guest web, guest app, kiosk, partner portal, POS ticket sale) process; these refine the tables above and win where they differ)

- **upgrade price**: Upgrades show the difference to pay (e.g. a better section the same day), within the product's upgrade window. *(source: DI-603)*

**Data it reads**: `getMediaAsset` (onLoad, Read an asset with derivatives and usage); `getCart` (onLoad, The cart, priced and checked, right now)

**Where the user goes next**

- → `POS-002` Sell — Ticket Catalogue: *Sell — Ticket Catalogue*; carries `orderId`, `promotionId`
- → `POS-003` Sell — Timed Entry: *Sell — Timed Entry*
- → `POS-004` Sell — Seat Map: *Sell — Seat Map*; carries `performanceId`
- → `POS-005` Payment: *Payment*; carries `paymentId`
- → `POS-011` Returns, Refunds & Exchanges: *They change their mind about the locker*; carries `orderId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The add existing ticket, read by `getMediaEntitlements`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the add existing ticket untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No add existing ticket yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getMediaEntitlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Not available.** The entitlement set must be read live; appending to a stale picture double-sells a locker |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Media expired (`mediaExpired`), blocked (`mediaBlocked`), already surrendered at exit (`mediaSurrendered`), or the entitlement cannot share media … (AppendRefusedProblem); 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem) |

#### Edge cases to draw

- **Offline**: Not available; the entitlements must be read live. *(source: screens/P04-point-of-sale.yaml#POS-010 states.offline)*

#### Consistency with other screens

- Match `POS-005`: Pays as a normal sale.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
ticket: YAS1-000123-02 · Aqua Park Day Pass · Adult
addOn: Locker · Large · AED 45
```

#### Permissions

- `getMediaEntitlements` → `ORDER_VIEW` (read) · staff
- `appendEntitlementToMedia` → `ORDER_CREATE` (operate) · staff
- `getMediaAsset` → `ASSET_LIBRARY_VIEW` (read) · staff
- `getCart` → no permission · guest, partner, staff
- `exchangeOrderLines` → `ORDER_EXCHANGE` (operate) · staff, partner

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getMediaEntitlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

44 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.11 | Ticket Storage - System shall store digital tickets. | Guest Mobile App & Branding | CONTRACTED | `getMediaEntitlements` |
| 2.6.18 | - Dynamic QR code | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.7.24 | The BtoB Customer can also receive simple QR Codes, vouchers or packaged PLUs. | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.13.3 | Tickets can be issued and sent either by email (PDF or M-ticket, E-ticket). | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.14.16 | Generate digital cards with QR/NFC/barcode. | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.16.2 | The system should support multiple media types for a ticket. Expected formats: - Paper/thermal tickets with QR, Barcode, RFID - Print at home tickets with QR, Barcode - Smartphones: NFC (near-field … | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 2.16.17 | The system shall allow multiple media types to be linked to the same guest account and entitlement simultaneously, including QR tickets, RFID wristbands, membership cards, and mobile wallets. | Ticketing Sales | CONTRACTED | `getMediaEntitlements` |
| 3.1.1 | Dynamic QR Code Supports: 1. Registration: Customers select "Digital Ticket" via the confirmation page, email, or ticket PDF to begin the enrollment process. 2.Activation: After registration, the … | Admission and Access | CONTRACTED | `getMediaEntitlements` |
| 3.1.2 | Unique Code per Ticket: Generate a unique QR code for every issued ticket or pass. | Admission and Access | CONTRACTED | `getMediaEntitlements` |
| 3.1.7 | Dynamic QR technology shall support memberships, annual passes, loyalty accounts, wallets, and other digital credentials in addition to standard tickets. | Admission and Access | CONTRACTED | `getMediaEntitlements` |
| 3.2.63 | It is expected that the access code created by the system is unique and randomized to improve fraud prevention. | Admission and Access | CONTRACTED | `getMediaEntitlements` |
| 5.4.18 | Provide digital loyalty card in app. | F&B & Guest Management | CONTRACTED | `getMediaEntitlements` |
| … 32 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Upgrade eligibility checks validity/usage. Cases: seated ticket to a better section same day, paying the difference at the counter; general admission to season pass with the amount paid credited. Windows: before use, after use within a window, or until a cutoff (event ticket until the guest exits). *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-603)*
- The till can add an item to an existing ticket (e.g. a locker) after the sale; not in the delivered mockups. *(agreed · MoM 14 Aug 2026, (cited as CF-58 in POS-010 notes) · DI-314)*
- Add-on entitlements (e.g. a locker) are linked to the existing ticket QR by scanning it, not issued as a new QR. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-295)*

Also apply: 5 for P04 · Sell, 41 for all of P04, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P04 Venue POS.dc.html#pos-010` · status **notStarted** · provenance designed
- Prototype (TICVAI OS 4.2.1, build 2026.08.14, verified —, match none): `sources/designs/TICVAI_POS_Terminal_client_approved.html`, view **
- Flow F58 *A ticket is sold at a till, added to, and refunded*, step 7: The guest asks to add a locker to the ticket they just bought. → **Appended to the existing media rather than issued as a second ticket.** A guest carrying two cards for one visit is a guest who will present the wrong one at a gate.

#### Acceptance for the design

- [ ] Every input above is drawn (37), with its required mark, default, format and its error state (404, 409, 410).
- [ ] Every output is drawn (39 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#POS-010?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Append entitlement to media, Exchange order lines, Add and pay.
- [ ] Every transition is wired: `POS-002`, `POS-003`, `POS-004`, `POS-005`, `POS-011`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`, `ORDER_CREATE`, `ORDER_EXCHANGE`, `ORDER_VIEW`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `POS-015` Cash Operations Dashboard

**See the live cash position of every till, for a supervisor.**

| | |
|---|---|
| App · platform | TICVAI POS · P04 Venue POS (terminal) |
| Module | Sell · wave 1 · needs the `core` module |
| Block | Block A · ticket #17886 (APP-POS-POS-015) |
| Who uses it | venue staff holding `REPORT_VIEW_WORKSTATION`, `SHIFT_OPEN` (2 operate); in the flows as venue manager |
| Device and orientation | This is a touch terminal, 1366 x 768 landscape; the kitchen display is a wall screen at 1920 x 1080. · LTR and RTL · light, dark theme |
| Pattern | listDetail (touchLarge density): `listCashMovements` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Working from the local journal.** The till keeps taking money; this reconciles on sync. |
| Opens with | `workstationId` (session), `shiftId` (deepLink) · cold entry: **Resolves from the session, which carries the workstation** — a till is signed into, not navigated to. |
| Route | `/sell/cash-operations-dashboard` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them.

**From the Food, Beverage & Retail process.** A supervisor's live view of cash on this till and outlet: the opening float, cash in and out, safe drops, and which cash drawers are open and who holds them. The one thing to get right: it is a supervisor view — a cashier must never see the expected cash in their own drawer here (R080(e), POSV2-3).

**Fixed on main** (the package already carries these; draw what it says): The purpose reads "Cash Operations Dashboard — from the client design board, 20 August" and the layout is two raw tables and a Confirm … (CHG-WIR-010); DI-273 asks for expected cash per till on a screen of the till app, while the blind count forbids showing a cashier the expected cash. (CHG-SPO-014); F73 step 3 says "cash limits and the drawer ceiling are set" here; no operation or setting holds a drawer limit. (CHG-SPO-014).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Open only | toggle | — | — | `listDepositBoxes` ?openOnly |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every cash movement** (data table, from `listCashMovements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. |
| Kind | chip: Opening float, Lift, Add | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Denominations | list or chips (count when long) | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. |
| Reference | text | Safe drop reference or bag number. |
| Reason | text | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Shift | the name it points at, never the id | — |
| Authorised by principal | the name it points at, never the id | The principal who authorised the movement, recorded for audit. |
| Sequence | 1,234 | Monotonic within the shift. Preserves order across an offline batch. |
| Synced at | 1 Oct 2026, 14:30 | — |

**Every deposit box** (data table, from `listDepositBoxes`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Cashier principal | the name it points at, never the id | — |
| Cashier name | text | — |
| Venue | the name it points at, never the id | — |
| Workstation | the name it points at, never the id | Where it is being used now. Changes during a shift; the box does not. |
| Shift | the name it points at, never the id | The shift trading from this box. A UUIDv7, as `Shift.id` is. |
| Status | chip: Allocated, Open, Suspended, Closing, Closed, Reconciled | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Opening denominations | list or chips (count when long) | 5.8.3. Either this or a total — a supervisor handing over a counted bag should not have to re-count it into fields. |
| Withdrawn total | AED 1,234.50 | Reduces the expected close figure. Cash skimmed for banking is not a shortfall, and a system that treats it as one makes every busy cashier … |
| Foreign holdings | list or chips (count when long) | 4.6.11 and 6.1.10. Foreign cash accepted at this till, counted separately by currency. |
| Expected total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Drawers over their limit** (banner, from `listDepositBoxes`): The supervisor's view (DEC-179; CHG-CSP-016): boxes over the drawer limit, with a lift to offer. **Expected cash per till is a supervisor figure**: shown only to a holder of OVERSHORT_ACCEPT or SHIFT_CLOSE_OTHER, never on a cashier's screen (DI-273, audit R080, POSV2-3).

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Cashier principal | the name it points at, never the id | — |
| Cashier name | text | — |
| Venue | the name it points at, never the id | — |
| Workstation | the name it points at, never the id | Where it is being used now. Changes during a shift; the box does not. |
| Shift | the name it points at, never the id | The shift trading from this box. A UUIDv7, as `Shift.id` is. |
| Status | chip: Allocated, Open, Suspended, Closing, Closed, Reconciled | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Opening denominations | list or chips (count when long) | 5.8.3. Either this or a total — a supervisor handing over a counted bag should not have to re-count it into fields. |
| Denomination | the name it points at, never the id | References `platform.denomination`, as `CashCountLine.denominationId` does. Until 26 September this was `denomination: number` — a face … |
| Count | 1,234 | — |
| Withdrawn total | AED 1,234.50 | Reduces the expected close figure. Cash skimmed for banking is not a shortfall, and a system that treats it as one makes every busy cashier … |
| Over drawer limit | yes / no (icon or chip) | The box holds more than its till's drawer limit (decided 2 October 2026, Chinmay, BO-042; DEC-179; CHG-CSP-016): computed on read from the … |
| Foreign holdings | list or chips (count when long) | 4.6.11 and 6.1.10. Foreign cash accepted at this till, counted separately by currency. |
| Currency | text | Stored, because it is the one thing that is not the region's. A foreign holding is by definition cash in a currency the till does not trade … |
| Expected amount | AED 1,234.50 | The sum of tenders taken in this currency during the shift. |
| Counted amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Variance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Base equivalent | AED 1,234.50 | At the rates on the payments, not today's. A shift closed on Friday and reviewed on Monday is reviewed at Friday's rates (CF-37). |

**The selected cash movement** (detail panel, from `listCashMovements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. |
| Kind | chip: Opening float, Lift, Add | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Denominations | list or chips (count when long) | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. |
| Reference | text | Safe drop reference or bag number. |
| Reason | text | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Shift | the name it points at, never the id | — |
| Authorised by principal | the name it points at, never the id | The principal who authorised the movement, recorded for audit. |
| Sequence | 1,234 | Monotonic within the shift. Preserves order across an offline batch. |
| Synced at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Cash movements**: Time, kind (Opening float · Cash out · Cash in · Safe drop), amount, who authorised, reference/bag number, reason. Newest first. *(source: contracts/spine/shift.yaml#listCashMovements / DI-308)*
- **Cash drawers**: Each drawer's holder, till, status (Open · Suspended · Closing · Closed · Reconciled). A drawer belongs to a cashier, not a till. *(source: contracts/spine/shift.yaml#listDepositBoxes)*
- **Totals**: Cash and card totals and variance tracking per till, for supervisors only. *(source: DI-273 / DI-308)*

**Data it reads**: `listCashMovements` (onLoad, Lifts, adds and the opening float); `listDepositBoxes` (onLoad, Cash boxes and who holds them)

**Where the user goes next**

- → `POS-001` Begin Shift: *Begin Shift*; carries `shiftId`
- → `POS-018` Safe Drop & Cash Transfer Management: *Safe drop destinations are allocated*; carries `shiftId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cash operations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cash operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cash operations yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCashMovements` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listCashMovements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Working from the local journal.** The till keeps taking money; this reconciles on sync. |

#### Edge cases to draw

- **A cashier opens the screen**: Their own movements only, with no expected cash and no variance. *(source: POSV2-3 / R080)*
- **Offline**: Shown from the local journal with "as of" time; reconciles on sync. *(source: screens/P04-point-of-sale.yaml#POS-015)*

#### Consistency with other screens

- Match `POS-017`: Cash in and cash out recorded there appear here immediately.
- Match `POS-018`: Safe drops appear here with the witness.
- Match `BO-041`: The back-office cash movements list shows the same rows venue-wide.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
movements:
- time: 09:42
  kind: Opening float
  amount: AED 1,000.00
  by: J. Smith
- time: '13:15'
  kind: Safe drop
  amount: AED 3,000.00
  by: Omar Ziad (witness J. Smith)
  bag: SD-0412
- time: '15:40'
  kind: Cash in
  amount: AED 200.00
  reason: Change order
```

#### Permissions

- `listCashMovements` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listDepositBoxes` → `SHIFT_OPEN` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listCashMovements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Till/cash management shows total cash and card transactions and variance tracking, and supports cash-in/cash-out for mid-shift cash pickups. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-308)*
- Shift/session view shows open and closed sessions per workstation with expected cash and card totals; a live till monitor shows real-time cash status per workstation and open/close codes. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-273)*

Also apply: 5 for P04 · Sell, 41 for all of P04, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P04 Venue POS.dc.html#pos-015` · status **notStarted** · provenance designed
- Prototype (TICVAI OS 4.2.1, build 2026.08.14, verified —, match none): `sources/designs/TICVAI_POS_Terminal_client_approved.html`, view **
- Flow F73 *A till is configured and its cash rules set*, step 3: Cash limits and the drawer limit are set, and the till watches the drawer against it. → **A limit on the drawer is a security control, and a warning, never a block** (decided 2 October 2026, Chinmay, BO-042: "Add drawer limit setting (warn + offer cash lift)"; DEC-179, CHG-CSP-016 …
- Flow F73 branch at step 3 (recoverable): when The drawer goes over its limit during the shift., **The till warns and offers a cash lift; it never refuses a sale** (DEC-179, CHG-CSP-016). The lift is a `createCashMovement` of kind `lift` on POS-018, witnessed with the cashier's PIN on the same …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (54 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#POS-015?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm.
- [ ] Every transition is wired: `POS-001`, `POS-018`.
- [ ] Every gated control is gated: `REPORT_VIEW_WORKSTATION`, `SHIFT_OPEN`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `POS-017` Cash In / Cash Out Operations

**Cash In / Cash Out Operations — from the client design board, 20 August.**

| | |
|---|---|
| App · platform | TICVAI POS · P04 Venue POS (terminal) |
| Module | Sell · wave 1 · needs the `core` module |
| Block | Block A · ticket #17888 (APP-POS-POS-017) |
| Who uses it | venue staff holding `CASH_LIFT` (1 operate) |
| Device and orientation | This is a touch terminal, 1366 x 768 landscape; the kitchen display is a wall screen at 1920 x 1080. · LTR and RTL · light, dark theme |
| Pattern | configEditor (touchLarge density): the screen declares only writes (`createCashMovement`) and no read of a population — it is settings, not a list |
| Offline | **Working from the local journal.** The till keeps taking money; this reconciles on sync. |
| Opens with | `workstationId` (session), `shiftId` (deepLink) · cold entry: **Resolves from the session, which carries the workstation** — a till is signed into, not navigated to. |
| Route | `/sell/cash-in-cash-out-operations` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Drawn 31 August** — `POS Frontline Board 2.dc.html` frame `pos-2d`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Cash In / Cash Out Operations* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**From the Food, Beverage & Retail process.** Mid-shift cash in and cash out on this till: a cashier or supervisor records cash taken out of the drawer (a pickup when the drawer is heavy) or added (change). Both adjust the expected figure used at close, so a busy cashier does not end the day apparently short. The one thing to get right: two quick forms with the denomination breakdown and a reason — not a raw data form.

**Fixed on main** (the package already carries these; draw what it says): The layout is text fields bound to the raw request (id, kind, amount, denominations, reference, reason, recordedAt). (CHG-SPO-014); The configurable drawer limit the client asked for has no setting in any contract. (CHG-SPO-014).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Cash in or cash out | segmented control | optional | — | Opening float · Lift · Add | — | A two-way choice (lift or add); never typed. | `CreateCashMovementRequest.kind` |
| Counted by denomination | repeatable rows | optional | — | at least 1 | — | The amount is the sum of the notes and coins counted, not typed separately. | `CreateCashMovementRequest.denominations` |
| Reason | text area | optional | — | max length 500 | — | From the venue's reasons, with a reference where one applies. `id` and `recordedAt` are set by the till. | `CreateCashMovementRequest.reason` |

**Sent by *Create cash movement*** (`createCashMovement`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. | `createCashMovement` body |
| Kind `kind` | segmented control | required | — | Opening float · Lift · Add | — | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one cashier's box; `add` by `createCashMovement`. | `createCashMovement` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createCashMovement` body |
| Denominations `denominations` | repeatable rows | optional | — | at least 1 | — | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. | `createCashMovement` body |
| ID `denominations[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Shift `denominations[].shiftId` | picker: choose a shift | required | — | — | shows names, sends the id | A UUIDv7, as `Shift.id` and `orders.pos_shift.id` are. | `createCashMovement` body |
| Deposit box `denominations[].depositBoxId` | picker: choose a deposit box | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Count kind `denominations[].countKind` | segmented control | optional | — | Opening float · Close · Movement | — | Which count this line belongs to — the opening float (`openShift`), the close (`closeShift`) or a lift or add (`createCashMovement`). | `createCashMovement` body |
| Cash movement `denominations[].cashMovementId` | picker: choose a cash movement | optional | — | — | shows names, sends the id | The movement this line counts, where `countKind` is `movement`. How `listCashMovements` rebuilds each movement's `denominations`. | `createCashMovement` body |
| Denomination `denominations[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` — face value, kind and sort order live there. | `createCashMovement` body |
| Counted quantity `denominations[].countedQuantity` | number field | required | — | min 0 | — | How many of this note or coin were in the drawer. | `createCashMovement` body |
| Counted value `denominations[].countedValue` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Quantity times face value, stored. Derivable, and stored anyway: a denomination revalued or deactivated later would silently rewrite a historical count. | `createCashMovement` body |
| Counted by `denominations[].countedBy` | picker: choose a counted by | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Counted at `denominations[].countedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCashMovement` body |
| Recount of `denominations[].recountOf` | picker: choose a recount of | optional | — | — | shows names, sends the id | A recount points at what it replaces rather than overwriting it. `requestRecount` exists because a variance is a question before it is a fact. | `createCashMovement` body |
| Reference `reference` | text field | optional | — | max length 64 | — | Safe drop reference or bag number. | `createCashMovement` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `createCashMovement` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCashMovement` body |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Direction**: Cash out or Cash in (lift / add). Opening float is never chosen here. *(source: contracts/spine/shift.yaml#createCashMovement)*
- **Amount by denomination**: Same counter as the float; the amount is the counted total. Cash out cannot exceed the float counted at the last count less what has been lifted since. *(source: contracts/spine/shift.yaml#createCashMovement / R123)*
- **Reference**: Safe-drop reference or bag number, up to 64 characters. *(source: contracts/spine/shift.yaml#createCashMovement)*
- **Reason**: Free text up to 500 characters. *(source: contracts/spine/shift.yaml#createCashMovement)*

#### Outputs: what the screen shows and produces

**Shown**

**The drawer is over its limit** (banner): **Warn and offer a cash lift; never block, never a figure to the cashier** (decided 2 October 2026, Chinmay, batch 6, BO-042: "Add drawer limit setting (warn + offer cash lift)"; DEC-179; DI-274; CHG-CSP-016). The limit is `VenueSettings.cashDrawerLimit` with a till override (`Workstation.cashDrawerLimit`).

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Create cash movement (primary button) | `createCashMovement` POST `/shifts/{shiftId}/cash-movements` | CreateCashMovementRequest | CashMovement | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since … | works offline |

**Where the user goes next**

- → `POS-001` Begin Shift: *Begin Shift*; carries `shiftId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved cash cash out. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cash cash out untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cash cash out configured. The form opens empty and `createCashMovement` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `CASH_LIFT`, which `createCashMovement` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Working from the local journal.** The till keeps taking money; this reconciles on sync. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since (`lift-exceeds-float`, audit R123 … |

#### Edge cases to draw

- **Cash out larger than the drawer can hold**: Refused with the reason in plain words ("More than the drawer holds since the last count"). *(source: contracts/spine/shift.yaml#createCashMovement / R123)*
- **Offline**: Recorded locally with device time and synced; shown as pending. *(source: contracts/spine/shift.yaml#createCashMovement)*

#### Consistency with other screens

- Match `POS-018`: A supervisor's safe drop with a witness (POS-018) and a cash out here both record a cash out; draw them as one cash screen with two tabs if the client agrees (DI-309 asks to reduce screen count).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cashOut: AED 2,000.00 · AED 500 × 2, AED 200 × 5 · bag SD-0413 · 'drawer heavy before lunch peak'
cashIn: AED 200.00 · AED 5 × 20, AED 1 × 100 · 'change order'
```

#### Permissions

- `createCashMovement` → `CASH_LIFT` (operate) · staff

**A refused user sees:** Shown when the caller lacks `CASH_LIFT`, which `createCashMovement` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Till/cash management shows total cash and card transactions and variance tracking, and supports cash-in/cash-out for mid-shift cash pickups. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-308)*
- Configurable cash-drawer limit: on a busy day the cashier unloads excess cash mid-shift; the unloaded amount is held separately (partial hold) and reconciled at final close. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-274)*

Also apply: 5 for P04 · Sell, 41 for all of P04, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P04 Venue POS.dc.html#pos-017` · status **notStarted** · provenance designed · **Drawn by Claude Design on `POS Frontline Board 2.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been …
- Prototype (TICVAI OS 4.2.1, build 2026.08.14, verified —, match none): `sources/designs/TICVAI_POS_Terminal_client_approved.html`, view **
- Derived from `wireframes/reference/POS Frontline Board 2.dc.html`
- Client design-board frames: `POS Frontline Board 2.dc.html#pos-2d`

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#POS-017?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create cash movement.
- [ ] Every transition is wired: `POS-001`.
- [ ] Every gated control is gated: `CASH_LIFT`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `POS-018` Safe Drop & Cash Transfer Management

**Drop cash from a drawer to the safe when it passes the ceiling.**

| | |
|---|---|
| App · platform | TICVAI POS · P04 Venue POS (terminal) |
| Module | Sell · wave 1 · needs the `core` module |
| Block | Block A · ticket #17889 (APP-POS-POS-018) |
| Who uses it | venue staff holding `CASH_LIFT`, `SHIFT_OPEN` (2 operate); in the flows as cashier, venue manager |
| Device and orientation | This is a touch terminal, 1366 x 768 landscape; the kitchen display is a wall screen at 1920 x 1080. · LTR and RTL · light, dark theme |
| Pattern | listDetail (touchLarge density): `listPrincipals` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Working from the local journal.** The till keeps taking money; this reconciles on sync. |
| Opens with | `workstationId` (session), `boxId` (deepLink), `shiftId` (deepLink) · cold entry: **Resolves from the session, which carries the workstation** — a till is signed into, not navigated to. |
| Route | `/sell/safe-drop-cash-transfer-management` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Owns POS board frame(s) POS-3B** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): listPrincipals (needs USER_MANAGE), the principal and rota tables and Create rota assignment are unrelated to a safe drop, which needs the open drawers … Removed 2 October 2026 (CHG-WIR-008): listPrincipals (needs USER_MANAGE), the principal and rota tables and Create rota assignment are unrelated to a safe drop, which needs the open drawers … Removed 2 October 2026 (CHG-WIR-008): listPrincipals (needs USER_MANAGE), the principal and rota tables and Create rota assignment are unrelated to a safe drop, which needs the open drawers …

**From the Food, Beverage & Retail process.** A supervisor takes cash out of a cashier's drawer for the safe or banking (a safe drop), with the cashier as witness; it reduces the expected close figure and is not a variance. The one thing to get right: two people sign on one device — the supervisor taking it and the cashier it came from.

**Fixed on main** (the package already carries these; draw what it says): Attached operations and tables are unrelated: listPrincipals (needs USER_MANAGE), "Every principal" with a "Scope path" filter, "Every rota … (CHG-WIR-008); The purpose is "Safe Drop & Cash Transfer Management — from the client design board, 20 August". (CHG-WIR-010).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Open only | toggle | — | — | `listDepositBoxes` ?openOnly |

**Form: Withdraw from deposit box** (confirmDialog, opened by *Withdraw from deposit box*; *Withdraw* calls `withdrawFromDepositBox`, *Cancel* sends nothing)

**Names what `withdrawFromDepositBox` changes and what it leaves alone**, in the consequence rather than the verb. A safe drop cash this affects should be identified in the dialog, not just counted. **Collects what `withdrawFromDepositBox` sends before it is called.** Required: `id`, `amount`, `witnessPrincipalId`, `recordedAt`. Optional: `reason`, `note`.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the `CashMovement` this records. | `withdrawFromDepositBox` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `withdrawFromDepositBox` body |
| Witness principal `witnessPrincipalId` | picker: choose a witness principal | required | — | — | shows names, sends the id | The cashier the cash came from. Kept as `CashMovement.witnessPrincipalId`. | `withdrawFromDepositBox` body |
| Reason `reason` | radio group | optional | — | Banking · Safe drop · Change order · Other | — | Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records. | `withdrawFromDepositBox` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `withdrawFromDepositBox` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `withdrawFromDepositBox` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 The box is being counted or has been counted — `closing`, `closed` or `reconciled` (problem type `deposit-box-not-open`).

**Form: Create cash movement** (modal, opened by *Create cash movement*; *Create cash movement* calls `createCashMovement`, *Cancel* sends nothing)

**Collects what `createCashMovement` sends before it is called.** Required: `id`, `kind`, `amount`, `recordedAt`. Optional: `denominations`, `reference`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. | `createCashMovement` body |
| Kind `kind` | segmented control | required | — | Opening float · Lift · Add | — | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one cashier's box; `add` by `createCashMovement`. | `createCashMovement` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createCashMovement` body |
| Denominations `denominations` | repeatable rows | optional | — | at least 1 | — | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. | `createCashMovement` body |
| ID `denominations[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Shift `denominations[].shiftId` | picker: choose a shift | required | — | — | shows names, sends the id | A UUIDv7, as `Shift.id` and `orders.pos_shift.id` are. | `createCashMovement` body |
| Deposit box `denominations[].depositBoxId` | picker: choose a deposit box | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Count kind `denominations[].countKind` | segmented control | optional | — | Opening float · Close · Movement | — | Which count this line belongs to — the opening float (`openShift`), the close (`closeShift`) or a lift or add (`createCashMovement`). | `createCashMovement` body |
| Cash movement `denominations[].cashMovementId` | picker: choose a cash movement | optional | — | — | shows names, sends the id | The movement this line counts, where `countKind` is `movement`. How `listCashMovements` rebuilds each movement's `denominations`. | `createCashMovement` body |
| Denomination `denominations[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` — face value, kind and sort order live there. | `createCashMovement` body |
| Counted quantity `denominations[].countedQuantity` | number field | required | — | min 0 | — | How many of this note or coin were in the drawer. | `createCashMovement` body |
| Counted value `denominations[].countedValue` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Quantity times face value, stored. Derivable, and stored anyway: a denomination revalued or deactivated later would silently rewrite a historical count. | `createCashMovement` body |
| Counted by `denominations[].countedBy` | picker: choose a counted by | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Counted at `denominations[].countedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCashMovement` body |
| Recount of `denominations[].recountOf` | picker: choose a recount of | optional | — | — | shows names, sends the id | A recount points at what it replaces rather than overwriting it. `requestRecount` exists because a variance is a question before it is a fact. | `createCashMovement` body |
| Reference `reference` | text field | optional | — | max length 64 | — | Safe drop reference or bag number. | `createCashMovement` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `createCashMovement` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCashMovement` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since (`lift-exceeds-float`, audit R123 …

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Drawer**: Pick the open cash drawer (by cashier and till); drawers being counted or closed are not offered. *(source: contracts/spine/shift.yaml#listDepositBoxes / contracts/spine/shift.yaml#withdrawFromDepositBox)*
- **Amount**: Counted by denomination where the venue counts drops; otherwise an amount. *(source: contracts/spine/shift.yaml#withdrawFromDepositBox)*
- **Reason**: Banking · Safe drop · Change order · Other (Other needs a note). *(source: contracts/spine/shift.yaml#withdrawFromDepositBox / R222)*
- **Witness**: The cashier whose drawer it is confirms on the same device. *(source: contracts/spine/shift.yaml#withdrawFromDepositBox)*

#### Outputs: what the screen shows and produces

**Shown**

**Open drawers** (data table, from `listDepositBoxes`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Cashier principal | the name it points at, never the id | — |
| Cashier name | text | — |
| Venue | the name it points at, never the id | — |
| Workstation | the name it points at, never the id | Where it is being used now. Changes during a shift; the box does not. |
| Shift | the name it points at, never the id | The shift trading from this box. A UUIDv7, as `Shift.id` is. |
| Status | chip: Allocated, Open, Suspended, Closing, Closed, Reconciled | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Opening denominations | list or chips (count when long) | 5.8.3. Either this or a total — a supervisor handing over a counted bag should not have to re-count it into fields. |
| Denomination | the name it points at, never the id | References `platform.denomination`, as `CashCountLine.denominationId` does. Until 26 September this was `denomination: number` — a face … |
| Count | 1,234 | — |
| Withdrawn total | AED 1,234.50 | Reduces the expected close figure. Cash skimmed for banking is not a shortfall, and a system that treats it as one makes every busy cashier … |
| Over drawer limit | yes / no (icon or chip) | The box holds more than its till's drawer limit (decided 2 October 2026, Chinmay, BO-042; DEC-179; CHG-CSP-016): computed on read from the … |
| Foreign holdings | list or chips (count when long) | 4.6.11 and 6.1.10. Foreign cash accepted at this till, counted separately by currency. |
| Currency | text | Stored, because it is the one thing that is not the region's. A foreign holding is by definition cash in a currency the till does not trade … |
| Expected amount | AED 1,234.50 | The sum of tenders taken in this currency during the shift. |
| Counted amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Variance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Base equivalent | AED 1,234.50 | At the rates on the payments, not today's. A shift closed on Friday and reviewed on Monday is reviewed at Friday's rates (CF-37). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Create cash movement (primary button) | `createCashMovement` POST `/shifts/{shiftId}/cash-movements` | CreateCashMovementRequest | CashMovement | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since … | works offline; opens modal first |
| Withdraw from deposit box (destructive button) | `withdrawFromDepositBox` POST `/deposit-boxes/{boxId}/withdraw` | inline | DepositBox | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 The box is being counted or has been counted — `closing`, `closed` or `reconciled` (problem type `deposit-box-not-open`). | step-up: pin (The cashier the cash came from countersigns the withdrawal with their own PIN on the same device (DEC-178; CHG-CSP-015).); works offline; opens confirmDialog first |

**Data it reads**: `listDepositBoxes` (onLoad, The open drawers and boxes to drop from)

**Where the user goes next**

- → `POS-001` Begin Shift: *Begin Shift*; carries `shiftId`
- → `POS-020` Shift Exceptions & Alerts: *A no-sale is recorded*; carries `shiftId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The safe drop cash list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the safe drop cash untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No safe drop cash yet. Offers Create cash movement (`createCashMovement`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on scopePath, isActive and the safe drop cash are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SHIFT_OPEN`, which `listDepositBoxes` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Working from the local journal.** The till keeps taking money; this reconciles on sync. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since (`lift-exceeds-float`, audit R123 …; 409 The box is being counted or has been counted — `closing`, `closed` or `reconciled` (problem type `deposit-box-not-open`). |

#### Edge cases to draw

- **The drawer is being counted or is closed**: Refused ("This drawer is being counted — nothing can go in or out"). *(source: contracts/spine/shift.yaml#withdrawFromDepositBox)*

#### Consistency with other screens

- Match `POS-017`: Same denomination counter; see the merge suggestion there.
- Match `BO-042`: The back office's banking and safe view receives these drops.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
drop: Omar Ziad takes AED 3,000.00 from J. Smith's drawer (Till 14) · Safe drop · bag SD-0412 · 13:15
```

#### Permissions

- `createCashMovement` → `CASH_LIFT` (operate) · staff
- `withdrawFromDepositBox` → `CASH_LIFT` (operate) · staff · step-up pin
- `listDepositBoxes` → `SHIFT_OPEN` (operate) · staff

**A refused user sees:** Shown when the caller lacks `SHIFT_OPEN`, which `listDepositBoxes` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.8.8 | The system should allow the supervisor to withdraw some cash during the day from an cashier’s cash float and trace it in the system. | F&B & Guest Management | CONTRACTED | `withdrawFromDepositBox` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Configurable cash-drawer limit: on a busy day the cashier unloads excess cash mid-shift; the unloaded amount is held separately (partial hold) and reconciled at final close. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-274)*

Also apply: 5 for P04 · Sell, 41 for all of P04, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P04 Venue POS.dc.html#pos-018` · status **notStarted** · provenance designed · **Drawn by Claude Design on `POS Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Prototype (TICVAI OS 4.2.1, build 2026.08.14, verified —, match none): `sources/designs/TICVAI_POS_Terminal_client_approved.html`, view **
- Derived from `wireframes/reference/POS Board 3.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 3.dc.html#pos-3b`
- Flow F32 *A till opens, trades and settles*, step 4: A guest wants cash back and the drawer is heavy. A safe drop is recorded. → **The drawer never holds more than the venue's ceiling.** A safe drop mid-shift is a security control, not bookkeeping, and it is recorded as a movement so the settlement adds up.
- Flow F73 *A till is configured and its cash rules set*, step 4: Safe drop destinations are allocated. → **A box per till per shift.** Two tills sharing a box is two cashiers answering for one variance.

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#POS-018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create cash movement, Withdraw from deposit box.
- [ ] Every transition is wired: `POS-001`, `POS-020`.
- [ ] Every gated control is gated: `CASH_LIFT`, `SHIFT_OPEN`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `POS-019` Shift Templates & Policies

**See this till's shifts and the opening and closing rules they run under.**

| | |
|---|---|
| App · platform | TICVAI POS · P04 Venue POS (terminal) |
| Module | Sell · wave 1 · needs the `core` module |
| Block | Block A · ticket #17915 (APP-POS-POS-019) |
| Who uses it | venue staff holding `REPORT_VIEW_WORKSTATION`, `SCOPE_VIEW`, `WORKSTATION_CONFIGURE` (1 operate, 1 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is a touch terminal, 1366 x 768 landscape; the kitchen display is a wall screen at 1920 x 1080. · LTR and RTL · light, dark theme |
| Pattern | listDetail (touchLarge density): `listShifts` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | **Working from the local journal.** The till keeps taking money; this reconciles on sync. |
| Opens with | `workstationId` (session), `venueId` (session) · cold entry: **Resolves from the session, which carries the workstation** — a till is signed into, not navigated to. |
| Route | `/sell/shift-templates-policies` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Named in the board contents and not written up in it.** **Owns POS board frame(s) POS-3C** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): Venue-wide settings (setVenueSettings, TENANT_CONFIGURE) were edited and read from a till; venue configuration belongs in Venue Management (BO-1063), and a till … Removed 2 October 2026 (CHG-WIR-021): Venue-wide settings (setVenueSettings, TENANT_CONFIGURE) were edited and read from a till; venue configuration belongs in Venue Management (BO-1063), and a till … Contract gap recorded 2 October 2026 (CHG-WIR-024): No operation reads or writes a till shift policy (opening and closing rules, exceptions and alerts) for F73 step 2.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Meant to set the rules every till in the venue closes to (shift templates and policies), from the till by a manager. As wired it lists shifts and edits the venue's general settings (support hours, quiet hours, biometrics, alerting), which is not the job. The rule to keep: shift policy is venue scope, never per workstation, or the variance report compares nothing.

**Fixed on main** (the package already carries these; draw what it says): The screen's only write is setVenueSettings (support hours, quiet hours, biometrics, segregated access, alerting); nothing reads or writes … (CHG-WIR-021); Venue settings are edited from a till. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every shift' drop id, workstationId, venueId, scopePath, principalId. (CHG-SPO-015).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should the cashier ever see expected sales during or at close?** → The cashier never sees expected sales during or at close (blind close). *(decided by Chinmay, 2026-10-02; DEC-098 / CHG-FIN-003 / CHG-NOTE-005)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Opened from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedFrom=` to `listShifts`. | `listShifts` ?openedFrom |
| Opened to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedTo=` to `listShifts`. | `listShifts` ?openedTo |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listShifts` ?workstationId |
| Status | select | — | Pending approval · Open · Suspended · Pending variance · Pending closure · Closed · Auto closed | `listShifts` ?status |

**Form: Edit the till rules** (modal, opened by *Edit the till rules*; *Save the till rules* calls `setTillShiftPolicy`, *Cancel* sends nothing)

**Collects the whole policy** (`setTillShiftPolicy` replaces it; a field left out returns to its default), prefilled from `getTillShiftPolicy`. Says it applies to shifts opened after it. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setTillShiftPolicy` body |
| Require open approval `requireOpenApproval` | toggle | optional | off | — | — | Every shift opens `pendingApproval` and waits for `approveShiftOpen` (SHIFT_APPROVE_OPEN). | `setTillShiftPolicy` body |
| Opening float tolerance `openingFloatTolerance` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | How far a declared opening float may differ from the box's allocated float before the shift waits for approval (`states/shift.yaml`, pendingApproval). | `setTillShiftPolicy` body |
| Deposit box required `depositBoxRequired` | toggle | optional | on | — | — | A shift cannot open without a deposit box (`OpenShiftRequest.depositBoxCode`); refused `400` otherwise. | `setTillShiftPolicy` body |
| Bag number required `bagNumberRequired` | toggle | optional | off | — | — | A shift cannot open without a bag number (`OpenShiftRequest.bagNumber`). | `setTillShiftPolicy` body |
| Require close approval `requireCloseApproval` | toggle | optional | off | — | — | Every counted shift waits in `pendingClosure` for `approveShiftClose` (SHIFT_APPROVE_CLOSE), even within the variance threshold. | `setTillShiftPolicy` body |
| Auto close after hours `autoCloseAfterHours` | stepper or slider (hours) | optional | 14 | min 1; max 48 | — | Hours after which an open or suspended shift nobody closed is closed by the inactivity job as `autoClosed` and the supervisors are told (`states/shift.yaml`). | `setTillShiftPolicy` body |
| No sale alert count `noSaleAlertCount` | number field | optional | 10 | min 1 | — | No-sales in one shift (`recordNoSale`) at which the supervisors are alerted on the venue's alerting channel; the count is on POS-020. | `setTillShiftPolicy` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setVenueSettings: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/tenancy.yaml#setVenueSettings)*

#### Outputs: what the screen shows and produces

**Shown**

**Every shift** (data table, from `listShifts`): Who, when and the state; names rather than ids (design-notes correction platform-foundation POS-019).

| Shows | Format | Notes |
|---|---|---|
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |

**The selected shift** (detail panel, from `listShifts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sales total | AED 1,234.50 | What the till took in sales, as the guest paid it — tax included: the shift's takings, not Gross sales (CHG-FIN-002, CHG-FIN-010). |
| Refunds total | AED 1,234.50 | What the till paid back, as the guest was refunded it — tax included. |
| Lifts total | AED 1,234.50 | Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net. |

**The rules this till opens and closes to** (detail panel, from `getTillShiftPolicy`): The rules: open approval, deposit box and bag number, the abandoned-shift limit and the exception alerts, set for the whole venue (CHG-CSP-020). The variance threshold and drawer limit are venue settings shown beside them.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Require open approval | yes / no (icon or chip) | Every shift opens `pendingApproval` and waits for `approveShiftOpen` (SHIFT_APPROVE_OPEN). |
| Opening float tolerance | AED 1,234.50 | How far a declared opening float may differ from the box's allocated float before the shift waits for approval (`states/shift.yaml` … |
| Deposit box required | yes / no (icon or chip) | A shift cannot open without a deposit box (`OpenShiftRequest.depositBoxCode`); refused `400` otherwise. |
| Bag number required | yes / no (icon or chip) | A shift cannot open without a bag number (`OpenShiftRequest.bagNumber`). |
| Require close approval | yes / no (icon or chip) | Every counted shift waits in `pendingClosure` for `approveShiftClose` (SHIFT_APPROVE_CLOSE), even within the variance threshold. |
| Auto close after hours | 1,234 | Hours after which an open or suspended shift nobody closed is closed by the inactivity job as `autoClosed` and the supervisors are told … |
| No sale alert count | 1,234 | No-sales in one shift (`recordNoSale`) at which the supervisors are alerted on the venue's alerting channel; the count is on POS-020. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (primary button) | navigation or local | — | — | — | — |
| Edit the till rules (secondary button) | `setTillShiftPolicy` PUT `/venues/{venueId}/till-shift-policy` | TillShiftPolicy | TillShiftPolicy | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `WORKSTATION_CONFIGURE`; opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Shifts list**: This till's shifts by default, newest first: cashier name, opened/closed times in the venue's time zone, status and box code. No expected or counted totals: the close is blind. *(source: contracts/spine/shift.yaml#listShifts; POSV2-3)*
- **Money columns (liftsTotal, refundsTotal, salesTotal)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `listShifts` (onLoad, List shifts); `getTillShiftPolicy` (onLoad, The venue's till opening, closing and exception rules that …)

**Where the user goes next**

- → `POS-001` Begin Shift: *Begin Shift*; carries `shiftId`
- → `POS-015` Cash Operations Dashboard: *Cash limits and the drawer limit are set, and the till watches the drawer against it*; carries `shiftId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The shift templates policies list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the shift templates policies untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No shift templates policies yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on workstationId, status, openedFrom, openedTo and the shift templates policies are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Working from the local journal.** The till keeps taking money; this reconciles on sync. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **A manager tries to change a policy for this till only**: Not possible; the screen says the policy applies to every till at AquaCove Abu Dhabi. *(source: F73 step 2; ADR-0018)*
- **Can read but not change (holds REPORT_VIEW_WORKSTATION, TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: TENANT_CONFIGURE for Save venue settings. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/tenancy.yaml#setVenueSettings)*
- **setVenueSettings answers 422**: Show it as something the person can act on, not a failure: **An enable the venue cannot evidence.** Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender verification where no device in the venue reports `genderClassification`. `errors[]` names each missing field or the missing capability. *(source: contracts/spine/tenancy.yaml#setVenueSettings)*

#### Consistency with other screens

- Match `POS-007`: The close rules set here are what POS-007's blind close enforces.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
shifts:
- cashier: Rahul Menon
  opened: 01/10/2026 08:55
  status: open
  box: BOX-AUH-07
- cashier: Mariam Saeed
  opened: 30/09/2026 14:01
  closed: 30/09/2026 22:12
  status: closed
  box: BOX-AUH-03
```

#### Permissions

- `listShifts` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `getTillShiftPolicy` → `SCOPE_VIEW` (read) · staff
- `setTillShiftPolicy` → `WORKSTATION_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.44 | Incident & Exception Logging | Ticketing Sales | CONTRACTED | data `Shift` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Shift management: assignment and scheduling by cashier/department, templates and policies, opening/closing, exceptions/alerts. Allam: explore merging shift-closing and till-closing screens to reduce dashboard count. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-309)*

Also apply: 5 for P04 · Sell, 41 for all of P04, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P04 Venue POS.dc.html#pos-019` · status **notStarted** · provenance designed · **Drawn by Claude Design on `POS Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Prototype (TICVAI OS 4.2.1, build 2026.08.14, verified —, match none): `sources/designs/TICVAI_POS_Terminal_client_approved.html`, view **
- Derived from `wireframes/reference/POS Board 3.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 3.dc.html#pos-3c`
- Flow F73 *A till is configured and its cash rules set*, step 2: Shift policy is set. → **Venue scope, not workstation.** Every till in a venue closes to the same rules or the variance report compares nothing.
- Flow F73 branch at step 2 (high): when A shift is open on the till., **Refused.** Changing the rules under an open shift means it closes against rules it did not open under.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (32 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#POS-019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Edit the till rules.
- [ ] Every transition is wired: `POS-001`, `POS-015`.
- [ ] Every gated control is gated: `REPORT_VIEW_WORKSTATION`, `SCOPE_VIEW`, `WORKSTATION_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `POS-024` Outlet Setup

**A manager configures this outlet from the floor.**

| | |
|---|---|
| App · platform | TICVAI POS · P04 Venue POS (terminal) |
| Module | Sell · wave 1 · needs the `fnb` module |
| Block | Block A · ticket #17952 (APP-POS-POS-024) |
| Who uses it | venue staff holding `ORDER_VIEW`, `PRODUCT_CONFIGURE` (1 read, 1 configure) |
| Device and orientation | This is a touch terminal, 1366 x 768 landscape; the kitchen display is a wall screen at 1920 x 1080. · LTR and RTL · light, dark theme |
| Pattern | listDetail (touchLarge density): `listOutlets` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | **Configuration is refused offline.** A table layout edited on two disconnected tablets is two layouts, and the room only has one. |
| Opens with | `workstationId` (session), `outletId` (session), `itemId` (deepLink) · cold entry: **Resolves from the session, which carries the workstation and its outlet.** A till is signed into, not navigated to — and the outlet is a property of where … |
| Route | `/sell/outlet-setup` |

**What the spec says about it.** **Configuration on the till, gated by permission rather than by device.** P04 is *Terminal and Tablet* (`reactNativeTablet`) and ADR-0002 makes authorisation user-driven — **a manager signs into the same till a cashier uses and sees screens the cashier does not.** **A table layout is decided standing in the room.** A manager at a desk cannot see whether two four-tops push together, which is why `setTableLayout` and `setTableCombinations` belong within reach of the floor and not only in the back office.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): The outlet is the till's and the menu is not edited here (86 needs only the items); the outlet and menu tables were plumbing on a manager's screen (R254 … Removed 2 October 2026 (CHG-WIR-008): The outlet is the till's and the menu is not edited here (86 needs only the items); the outlet and menu tables were plumbing on a manager's screen (R254 …

**From the Food, Beverage & Retail process.** Outlet configuration from the floor, for a manager signed in on the same till a cashier uses: the table layout (halls, tables, shapes, capacity, position), which tables combine, and taking items off sale. The one thing to get right: it is a visual editor of the same floor POS-028 shows, and it is clearly a manager mode — a cashier sees why they cannot enter, not an empty screen.

**Fixed on main** (the package already carries these; draw what it says): Text fields "Venue id" and "Kind", tables "Every outlet" and "Every menu", and listMenus are on the screen. (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **setTableLayout matches tables by id (update or add). How is a table removed from the layout?** → 'Remove table' marks the table Out of service (setTableLayout never deletes). *(decided by Chinmay, 2026-10-02; DEC-067 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| 86 an item | multi select | — | — | — | — | — | — |

**Form: Save table layout** (modal, opened by *Save table layout*; *Save table layout* calls `setTableLayout`, *Cancel* sends nothing)

**Collects what `setTableLayout` sends before it is called.** Required: `tables`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tables `tables` | repeatable rows | required | — | — | — | — | `setTableLayout` body |
| ID `tables[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setTableLayout` body |
| Label `tables[].label` | text field | required | — | max length 32 | — | The table code, unique per venue (decided 28 September, audit R108). Two tables in one venue never share a label, across all its outlets, so *T12* names one table wherever it is … | `setTableLayout` body |
| Capacity `tables[].capacity` | number field | required | — | min 1 | — | — | `setTableLayout` body |
| Zone `tables[].zone` | text field | optional | — | — | — | — | `setTableLayout` body |
| Position `tables[].position` | group | optional | — | — | — | — | `setTableLayout` body |
| X `tables[].position.x` | number field | optional | — | — | — | — | `setTableLayout` body |
| Y `tables[].position.y` | number field | optional | — | — | — | — | `setTableLayout` body |
| Shape `tables[].shape` | radio group | optional | — | Round · Square · Rectangle · Booth · Bar | — | — | `setTableLayout` body |
| Is out of service `tables[].isOutOfService` | toggle | optional | off | `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`. | — | Damaged, or its section closed. `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`. | `setTableLayout` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Save table combinations** (modal, opened by *Save table combinations*; *Save table combinations* calls `setTableCombinations`, *Cancel* sends nothing)

**Collects what `setTableCombinations` sends before it is called.** Required: `combinations`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Combinations `combinations` | repeatable rows | required | — | — | — | — | `setTableCombinations` body |
| Tables `combinations[].tableIds` | multi-picker: choose tables | required | — | at least 2 | — | — | `setTableCombinations` body |
| Combined covers `combinations[].combinedCovers` | number field | required | — | min 1 | — | — | `setTableCombinations` body |
| Setup minutes `combinations[].setupMinutes` | number field (minutes) | optional | 5 | — | — | — | `setTableCombinations` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Save item availability** (modal, opened by *Save item availability*; *Save item availability* calls `setItemAvailability`, *Cancel* sends nothing)

**Collects what `setItemAvailability` sends before it is called.** Required: `isAvailable`, `recordedAt`. Optional: `reason`, `restoreAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Is available `isAvailable` | toggle | required | — | — | — | — | `setItemAvailability` body |
| Reason `reason` | radio group | optional | — | Sold out · Ingredient unavailable · Equipment down · Seasonal · Other; A reason of `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | `other` is allowed only with a `note`, which it then requires (decided 28 September, audit R222). | `setItemAvailability` body |
| Note `note` | text area | optional | — | max length 500 | — | Free text. Required where the reason is `other` (audit R222). | `setItemAvailability` body |
| Restore at `restoreAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Automatic restore, typically at next service. Kept as `MenuItem.restoreAt`. | `setItemAvailability` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the act (offline-capable; replayed in this order). | `setItemAvailability` body |

Errors to draw in the form: 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Table**: Label (unique within the venue), capacity, shape (round, square, rectangle, booth, bar), hall, position by dragging on the plan, and Out of service. Capacity cannot change while a party is seated at the table. *(source: contracts/satellite/fnb.yaml#setTableLayout / contracts/satellite/fnb.yaml#/components/schemas/TableDefinition / R108 / R194)*
- **Combination**: Pick two or more tables on the plan and enter what they seat together and the set-up minutes; declared by a person, never inferred from adjacency. *(source: contracts/satellite/fnb.yaml#setTableCombinations)*
- **Take off sale (86)**: Pick items, a reason (Other needs a note) and an optional "back at" time; immediate on every till and guest menu. *(source: contracts/satellite/fnb.yaml#setItemAvailability / R110 / R222)*

#### Outputs: what the screen shows and produces

**Shown**

**Floor** (card list): Each table has Remove (marks it Out of service, DEC-067) rather than Delete.

**Combinations** (detail panel): **Declared, not inferred.** Two adjacent tables do not always combine — a pillar, a step, a service run. A host knows which pairs work and a floor plan does not.

**Floor** (detail panel, from `getTableMap`)

| Shows | Format | Notes |
|---|---|---|
| Outlet | the name it points at, never the id | — |
| Zones | list or chips (count when long) | — |
| Tables | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Label | text | The table code, unique per venue (decided 28 September, audit R108). Two tables in one venue never share a label, across all its outlets … |
| Capacity | 1,234 | — |
| Zone | text | — |
| Position | grouped details | — |
| X | 1,234.5 | — |
| Y | 1,234.5 | — |
| Shape | chip: Round, Square, Rectangle, Booth, Bar | — |
| Is out of service | yes / no (icon or chip) | Damaged, or its section closed. `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`. |
| Status | chip: Free, Seated, Ordered, Bill requested, Needs clearing, Reserved… | — |
| Visit | the name it points at, never the id | — |
| Covers | 1,234 | — |
| Seated at | 1 Oct 2026, 14:30 | — |
| Server principal | the name it points at, never the id | — |
| Bill total | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Apply (primary button) | navigation or local | — | — | — | — |
| Save table layout (primary button) | `setTableLayout` PUT `/outlets/{outletId}/tables` | inline | TableMap | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Save table combinations (secondary button) | `setTableCombinations` PUT `/outlets/{outletId}/table-combinations` | inline | inline | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Save item availability (secondary button) | `setItemAvailability` PUT `/menu-items/{itemId}/availability` | inline | MenuItem | 400 Validation failed; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | works offline; opens modal first |

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Save layout**: Saves the hall's whole layout in one go; refused if someone else changed it meanwhile ("Reload to see the latest layout"). *(source: contracts/satellite/fnb.yaml#setTableLayout)*

**Data it reads**: `getTableMap` (onLoad, The outlet's floor as it is laid out)

**Where the user goes next**

- → `POS-002` Sell — Ticket Catalogue: *Sell — Ticket Catalogue*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | This outlet, its tables and its menu. |
| Error (`?state=error`) | Could not load configuration. **Selling is unaffected.** |
| Empty, first run (`?state=emptyFirstRun`) | **A new outlet with no layout.** The one action that draws the first table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches. |
| Permission denied (`?state=emptyNoAccess`) | **You are signed in as a cashier.** Configuration needs a manager role — ADR-0002 makes that the person, not the device, so signing in again on this same till is the way through. |
| Offline (`?state=offline`) | **Configuration is refused offline.** A table layout edited on two disconnected tablets is two layouts, and the room only has one. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Offline**: Editing is refused offline with the reason (two disconnected tablets would make two layouts); 86 still works offline. *(source: screens/P04-point-of-sale.yaml#POS-024 / contracts/satellite/fnb.yaml#setItemAvailability)*
- **A cashier opens the screen**: "You are signed in as a cashier. Sign in as a manager on this till to change the outlet." *(source: screens/P04-point-of-sale.yaml#POS-024)*

#### Consistency with other screens

- Match `POS-028`: The same plan component in edit mode.
- Match `EMP-053`: Table and seating configuration on the staff app edits the same layout; the two must not diverge.
- Match `BO-729`: The outlet itself (type, hours, channels) is set in Venue Management; the till edits only the floor and availability.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
hall: Terrace · 5 tables
tables:
- T12 round · 2 · (x 2.0, y 1.5)
- T14 rectangle · 6
- T15 booth · 4 · out of service
combination: T6 + T7 = 9 covers · 5 min set-up
```

#### Permissions

- `setTableLayout` → `PRODUCT_CONFIGURE` (configure) · staff
- `setTableCombinations` → `PRODUCT_CONFIGURE` (configure) · staff
- `setItemAvailability` → `PRODUCT_CONFIGURE` (configure) · staff
- `getTableMap` → `ORDER_VIEW` (read) · staff

**A refused user sees:** **You are signed in as a cashier.** Configuration needs a manager role — ADR-0002 makes that the person, not the device, so signing in again on this same till is the way through.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.9.6 | The system should be able to create, modify, delete a restaurant floor plan. | Bundles and Promotions | CONTRACTED | `setTableLayout` |
| 4.6.9 | The system should be able to allow the back office to limit the sale of a particular item per day or per timeslot.(example: Happy hour time slot based sales). | Bundles and Promotions | CONTRACTED | `setItemAvailability` |
| 5.1.1 | The system should be able to allow table reservations view for the available tables in real-time, for the guests to choose/request. | F&B & Guest Management | CONTRACTED | `getTableMap` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P04 · Sell, 41 for all of P04, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P04 Venue POS.dc.html#pos-024` · status **notStarted** · provenance designed
- Prototype (TICVAI OS 4.2.1, build 2026.08.14, verified —, match none): `sources/designs/TICVAI_POS_Terminal_client_approved.html`, view **
- ADR-0002 *Authorisation is user-driven, not workstation-driven* (`docs/adr/0002-authorisation-is-user-driven-not-workstation-driven.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (400, 404, 412).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#POS-024?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Apply, Save table layout, Save table combinations, Save item availability.
- [ ] Every transition is wired: `POS-002`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P04 reference designs** (from `handoff/design-batches/apps/2-pos/README.md`)

- `sources/designs/TICVAI_POS_Terminal_v2.html`: **the POS reference from 1 October.** Our improved build of the client-approved terminal (`TICVAI POS Terminal (3).html`). It is a **candidate, not client-approved**: the 14 screens captured from it are `designed`, in `review`, with a `wireframe.candidate` block, never client-verified (tools/applied/pos-v2-1-october.py). The file is 9.7 MB and **kept out of git**: it is on Chinmay's disk at that path, and the captures in `wireframes/incoming/P04-pos-v2/` are the record.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the build the client signed off (10 September). It stays as it is; each screen's `wireframe.prototype` block still cites its view. When the client approves v2, v2 takes its place.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-026, DI-027, DI-029, DI-032, DI-033, DI-034, DI-035, DI-036, DI-037, DI-038, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P04 as a whole** (21: 0 open, 21 closed). Open first; a closed row says where it went on 30 September.

- **A17** Design the offline POS and handheld-validation architecture *(Softlabs Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A19** Prepare case study: online-first vs offline-first POS architecture (pros/cons) *(Chinmay Parab · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A23** Review and preserve the POS prototype for UI/UX reference *(Softlabs Team · Low · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A24** Propose an enhanced POS user experience (redesign, not a copy) *(Softlabs Team · High · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A26** Recommend a UX approach combining quick-access 'hot function' buttons with search-driven POS functionality *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · 9 Sep 2026 · workshop tracker)*
- **A37** Complete and share mockups for the food ordering / POS counter app *(Aishwarya More · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A51** Design ticket + F&B combo redemption flow: single QR encodes admission + meal entitlement, redeemable once at the F&B counter after entry; support both a shared group QR (redeemed together) and individually … *(Softlabs Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker)*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker)*
- **A79** Complete outstanding finance/infrastructure due diligence: review the ticketing system's manuals for additional revenue-recognition rules, finalize chart-of-accounts/ERP mapping due diligence, confirm the … *(Chinmay Parab / Qossai / Allam · Medium · Ongoing → 30 Sep: Closed, Rolled into S7 (HLD/LLD) · 12 Aug 2026 · workshop tracker)*
- **A83** Design the Menu & Product Command Center and Menu Builder (recipe/product mapping alerts, drag-and-drop POS layout, chargeable/free modifiers with min/max rules, combo meals with upgrade options) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker)*
- **A173** Expose wallet APIs for both patterns (external systems consuming the API directly, and third-party F&B/retail POS such as Micros or Symphony verifying and deducting balance) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker)*
- **A267** Revise POS prototype with 09-Sep feedback and share *(Pradnya Yeram · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Sep 2026 · workshop tracker)*
- … 7 more in `handoff/design-inputs/task-tracker-index.json`

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

### Across P04 Venue POS

- No driver is ever installed on the workstation OS: drivers are built into the TICVAI app; staff only connect the device and test print/scan from within the app; new models are supported by a back-end driver update, not a code release. *(agreed · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-897)*
- Qossai: dim/fade the background ("foggy") when a side panel or modal opens so the cashier's attention stays on the active task. *(client request · MoM 9 Sep 2026, 4.13 POS Prototype Review - Home Screen, Ticketing Cart & Link-to-Sale UX · DI-785)*
- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*
- Funding approval rules: a top-up above a configured threshold requires supervisor or finance approval via supervisor login. Top-up reversal (full or partial, back to the original payment method) requires manual verification/authorisation before processing. *(agreed · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-520)*
- Top-up rules set minimum and maximum amounts per transaction; channel/funding-source mapping restricts which payment methods each channel offers (e.g. cash top-up on-site only, not online), so each channel's top-up screen offers only its allowed methods. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-517)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*
- Staff-facing POS and tablet UIs always carry TICVAI branding, not client branding. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-296)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- Each device gets a unique workstation ID, but what a user sees is set by their role, not the device: e.g. a cashier sees the full park ticket range at a main-gate POS but only the F&B menu at a restaurant POS. Applies to the roaming "flying" POS too. *(agreed · MoM 12 Aug 2026, 2. Flying POS Setup and Permission Configuration · DI-246)*
- Built-in help menu with step-by-step tutorials with screenshots for common tasks (e.g. how to sell a ticket at the POS). *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-160)*
- In-system task assignment between staff (e.g. a cashier flagging something for a supervisor) without email or messaging apps. *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-159)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- F&B is reached from the same top-level navigation as other experiences (tours, guides); table management only appears for venues with a restaurant configuration. *(client request · MoM 3 Aug 2026, 5. Table Management & Dining Service Models · DI-107)*
- Allam: the cashier design must work consistently across all cashier device types: POS terminals, tablets, iPads and kiosks. *(agreed · MoM 3 Aug 2026, 3. UX Design Approach Discussion · DI-101)*
- Prefer the demoed cleaner, better-spaced layout over the cluttered PDF: adequate spacing and large touch targets to prevent mis-taps on touchscreens and tablets. *(agreed · MoM 3 Aug 2026, 3. UX Design Approach Discussion · DI-100)*
- Shift-level settings: light/dark mode, currency selection (displayed pricing follows the cashier's location), language selection, screen brightness, and manual online/offline toggling. *(agreed · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-098)*
- Notification system with ticket alerts (cancellations, capacity nearing or at its limit) and system alerts (printer offline, POS offline). *(client request · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-093)*
- Embedded AI assistant the cashier can query directly, e.g. to find today's promo code, process a refund, or switch between light/night themes. *(agreed · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-092)*
- Header metrics show tickets sold and revenue for the current shift. *(client request · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-090)*
- **Open question.** Allam: alongside search, provide always-visible "hot function" buttons for high-frequency actions (refund, check transaction, print last receipt). Softlabs to recommend the right balance of hot buttons and search. *(open · MoM 3 Aug 2026, 3. UX Design Approach Discussion · DI-088)*
- A prominent search ("magic banner") lets the cashier reach functionality such as refunds or resending a ticket by searching, rather than through static menus or sidebars. *(client request · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-087)*
- Qossai's demoed cashier interface is the primary reference/baseline, to be enhanced and redesigned enough that it does not look like a copy while keeping its UX ideas; the earlier AI-generated PDF is secondary colour/theme inspiration only. *(agreed · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-086)*
- The POS/tablet application carries TICVAI's own branding and UI direction; the B2C and B2B mobile applications are white-label by design. *(agreed · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-084)*
- POS product names and menus may be Arabic-only for certain regions. *(client request · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-082)*
- Selling a capacity-based product (e.g. seat-assigned tickets) while offline is blocked with a clear notification, never allowed through or silently failing; non-capacity products stay sellable offline. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-074)*
- Qossai: the POS raises an alert when a venue goes offline. *(client request · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-073)*
- Offline state must be clearly visible in the UI, e.g. a visible mode indicator or greyed-out unavailable functions; exact visual treatment to be settled in the UI/UX session. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-072)*
- Allam: the app detects loss of connectivity and switches to offline mode automatically, without cashier action, then restores online mode and syncs pending transactions automatically. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-071)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Full card numbers are never stored or shown; only a masked representation (e.g. last four digits) so the user can identify which card was used. *(agreed · MoM 31 Jul 2026, 10. Compliance & Data Protection · DI-069)*
- Allam: the platform is device-agnostic (Android, iOS and web) so sales can continue on any available device. *(agreed · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-068)*
- **Open question.** Qossai asked whether a cashier on a tablet could use the POS via a browser URL. A lightweight web POS will be considered; it would have no offline support (installed thick client required for offline). *(open · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-067)*
- **Open question.** POS catalogue: Chinmay's middle ground is an online real-time catalogue that falls back automatically to the last-synced catalogue if connectivity is lost; local-first vs online-first still to be compared (case study). *(open · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-066)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- POS: sell tickets, memberships, F&B, retail and services from one unified cashier experience. Access Control: real-time entry validation, occupancy monitoring, offline mode and gate management. *(agreed · Design Vision Book 29 Jul 2026, 07 Modules Overview (p7) - 04 Point of Sale; 03 Access Control · DI-035)*
- Selling reference layout: clean top navigation; category tabs with counts (All Events 32, Exhibitions, Guided Tours ...); sort and type chips (Price, Rating, Popular; General, Seated, Multipass, Scheduled, Rental); content cards with large image, type badge, rating, tags (LIMITED, NEW, BESTSELLER), availability ("180 available", "11 left") and "from" price; persistent cart on the right with member discount, totals and "Checkout Securely". *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, items 2-5 · DI-026)*
- POS must keep selling general admission tickets during an internet outage, and access-control apps must keep scanning and validating tickets during a connectivity failure. *(agreed · MoM 28 Jul 2026, 15. Offline POS and Access-Control Operations · DI-012)*

### In P04 · Sell

- A guest is not repeatedly re-offered something already declined (e.g. a fast pass rejected three times), and an offer ignored online is not re-presented on another channel, e.g. at POS after the guest bought it there. *(agreed · MoM 21 Sep 2026, 4.6 Personalized Offer Delivery & Omni-Channel Orchestration · DI-962)*
- Navigation depends on ticket type: admission has no date/time and goes straight to quantity/cart; dated asks date only; timed asks date then time; seated asks date, then time, then seat. *(agreed · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-116)*
- Add-to-cart offers upsell add-ons, including an AI-generated upsell prompt (e.g. suggesting the cashier add two more items to unlock a bundle discount). *(client request · MoM 3 Aug 2026, 2. Point-of-Sale (Cashier) UI Walkthrough · DI-096)*
- A "Build Your Experience" workflow helps cashiers sell bundled experiences without searching through hundreds of ticket types. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-010)*
- POS allows notes to be added against individual tickets in the cart. *(client request · MoM 28 Jul 2026, 1. POS Design Reference and Functional Walkthrough · DI-005)*

**10 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"appendEntitlementToMedia": {"method":"POST","path":"/media/{mediaCode}/entitlements","contract":"orders","summary":"Add something to a ticket the guest already holds","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AppendEntitlementRequest","responds":"AppendEntitlementResult"},
"createCashMovement": {"method":"POST","path":"/shifts/{shiftId}/cash-movements","contract":"shift","summary":"Record a cash lift or add","permission":"CASH_LIFT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCashMovementRequest","responds":"CashMovement"},
"exchangeOrderLines": {"method":"POST","path":"/orders/{orderId}/exchanges","contract":"orders","summary":"Exchange lines for different products or dates","permission":"ORDER_EXCHANGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ExchangeOrderRequest","responds":"OrderExchangeResult"},
"getCart": {"method":"GET","path":"/carts/{cartId}","contract":"orders","summary":"The cart, priced and checked, right now","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Cart"},
"getMediaAsset": {"method":"GET","path":"/media/{mediaId}","contract":"assets","summary":"Read an asset with derivatives and usage","permission":"ASSET_LIBRARY_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaAssetDetail"},
"getMediaEntitlements": {"method":"GET","path":"/media/{mediaCode}/entitlements","contract":"orders","summary":"What is already on this media","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaEntitlements"},
"getTableMap": {"method":"GET","path":"/outlets/{outletId}/tables","contract":"fnb","summary":"Table map with live state","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"TableMap"},
"getTillShiftPolicy": {"method":"GET","path":"/venues/{venueId}/till-shift-policy","contract":"shift","summary":"The rules every till in the venue opens and closes to","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"TillShiftPolicy"},
"listCashMovements": {"method":"GET","path":"/shifts/{shiftId}/cash-movements","contract":"shift","summary":"Lifts, adds and the opening float","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDepositBoxes": {"method":"GET","path":"/deposit-boxes","contract":"shift","summary":"Cash boxes and who holds them","permission":"SHIFT_OPEN","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"openOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRotaAssignments": {"method":"GET","path":"/rota-assignments","contract":"workforce","summary":"The rota","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"departmentId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listShifts": {"method":"GET","path":"/shifts","contract":"shift","summary":"List shifts","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"openedFrom","in":"query","required":null},{"name":"openedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"recordAttendance": {"method":"POST","path":"/attendance/clock","contract":"workforce","summary":"Clock in, clock out, or take a break","permission":"ATTENDANCE_RECORD","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"setItemAvailability": {"method":"PUT","path":"/menu-items/{itemId}/availability","contract":"fnb","summary":"Mark an item available or eighty-sixed","permission":"PRODUCT_CONFIGURE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MenuItem"},
"setTableCombinations": {"method":"PUT","path":"/outlets/{outletId}/table-combinations","contract":"fnb","summary":"Which tables can be pushed together, and to what capacity","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setTableLayout": {"method":"PUT","path":"/outlets/{outletId}/tables","contract":"fnb","summary":"Configure the table layout","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableMap"},
"setTillShiftPolicy": {"method":"PUT","path":"/venues/{venueId}/till-shift-policy","contract":"shift","summary":"Set the rules every till in the venue opens and closes to","permission":"WORKSTATION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TillShiftPolicy","responds":"TillShiftPolicy"},
"withdrawFromDepositBox": {"method":"POST","path":"/deposit-boxes/{boxId}/withdraw","contract":"shift","summary":"A supervisor takes cash out mid-shift","permission":"CASH_LIFT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DepositBox"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AllergenCode": {"type":"string","description":"**The fourteen declarable allergens, as one closed list.** Every allergen field in this contract uses it — the menu claim, the ticket line, a substitution's delta, a modifier option, the label on a bag — so a declared set and an actual set compare without anybody normalising case or synonyms. It was the `Allergen.contains` enum; the other fields were free text.\n","enum":["gluten","crustaceans","eggs","fish","peanuts","soybeans","milk","nuts","celery","mustard","sesame","sulphites","lupin","molluscs"]},
"AppendEntitlementRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the new order this creates, and its idempotency key — it must equal the `Idempotency-Key` header."},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["variantId","quantity"],"properties":{"variantId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid","nullable":true}}}},"paymentMethod":{"type":"string","enum":["card","cash","wallet","giftCard","chargeToAccount"]},"note":{"type":"string","maxLength":300},"recordedAt":{"type":"string","format":"date-time"}}},
"AppendEntitlementResult": {"type":"object","x-ticvai-persistence":"none — computed","required":["order","media"],"properties":{"order":{"allOf":[{"$ref":"#/components/schemas/Order"}],"description":"A **new** order. The original is untouched — it was paid, receipted and possibly reported on, and editing it would move yesterday's revenue.\n"},"media":{"allOf":[{"$ref":"#/components/schemas/MediaEntitlements"}],"description":"The full set now on the media, so the cashier can say what the QR does."},"addedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"AttendanceAmendment": {"type":"object","x-ticvai-persistence":"workforce.attendance_amendment","description":"One correction to an attendance record, appended by `amendAttendance` and never updated (decided 28 September, audit R129 (7)).\n","required":["id","attendanceRecordId","amendedByPrincipalId","amendedAt","occurredAtBefore","occurredAtAfter","reason"],"properties":{"id":{"type":"string","format":"uuid"},"attendanceRecordId":{"type":"string","format":"uuid"},"amendedByPrincipalId":{"type":"string","format":"uuid"},"amendedAt":{"type":"string","format":"date-time"},"occurredAtBefore":{"type":"string","format":"date-time","description":"The record's time before this correction."},"occurredAtAfter":{"type":"string","format":"date-time","description":"The time this correction set (`correctedAt` on the request)."},"reason":{"type":"string","maxLength":300}}},
"AttendanceRecord": {"type":"object","x-ticvai-persistence":"workforce.attendance","required":["id","principalId","kind","occurredAt"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"assignmentId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["clockIn","clockOut","breakStart","breakEnd"]},"occurredAt":{"type":"string","format":"date-time","description":"Device time — when it happened."},"recordedAt":{"type":"string","format":"date-time","description":"When the server received it. **Both are kept**: a steward clocking in offline at a gate is not late because the sync was.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true},"latitude":{"type":"number","nullable":true},"longitude":{"type":"number","nullable":true},"isAmended":{"type":"boolean","readOnly":true},"amendedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who made the latest amendment. The full history is `amendments` (audit R129 (7))."},"amendmentReason":{"type":"string","nullable":true,"readOnly":true,"description":"The latest amendment's reason. The full history is `amendments` (audit R129 (7))."},"originalOccurredAt":{"type":"string","format":"date-time","nullable":true,"description":"**The original is never overwritten.** Attendance feeds pay, and a record that can be quietly rewritten is not evidence.\n"},"amendments":{"type":"array","readOnly":true,"description":"**Every correction, oldest first, one row each** (decided 28 September, audit R129 (7)). A single set of amendment columns holds only the last one, and the second correction to a record would erase the evidence of the first.\n","items":{"$ref":"#/components/schemas/AttendanceAmendment"}},"exception":{"type":"string","nullable":true,"enum":["late","earlyLeave","missingClockOut","noShow","outOfGeofence","unscheduled"],"description":"Computed against the rota. Null where the record matches what was expected."}}},
"Cart": {"type":"object","x-ticvai-persistence":"orders.cart","required":["id","venueId","channel","status","lines"],"properties":{"id":{"type":"string","format":"uuid"},"token":{"type":"string","readOnly":true,"description":"**How an anonymous guest returns to their cart**, including from a recovery email. Rotated on claim, so a link shared before signing in does not reach the account after.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null while anonymous. Set by `claimCart`."},"status":{"$ref":"#/components/schemas/CartStatus"},"lines":{"type":"array","items":{"$ref":"#/components/schemas/CartLine"}},"conflicts":{"type":"array","items":{"$ref":"#/components/schemas/CartConflict"}},"consentQuestions":{"type":"array","readOnly":true,"description":"**The consent questions this cart's products and flow ask** (decided 29 September, rev 3 REV3-26), computed on read at their current version as **the union of each line's published booking flow's `white-label.BookingFlow.settings.consentQuestionIds`** (the flow `getPublishedBookingFlow` resolves for the line's product: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig`, 29 September W12) **and every line's `catalogue.Product.consentQuestionIds`, each question once**: the flow's first, in its order, then each product's in cart-line order, a question already listed not repeated (its `lineIds` gain the line). The client asks them, in the order given, and sends the answers to `marketing.recordConsentAnswers`; `answered` then turns true. One or several, as the venue chose. `checkoutCart` refuses while a required one is unanswered.\n","items":{"allOf":[{"$ref":"../satellite/marketing-crm.yaml#/components/schemas/ConsentQuestion"},{"type":"object","properties":{"lineIds":{"type":"array","description":"The cart lines that ask it. Empty for a question the flow asks.","items":{"type":"string","format":"uuid"}},"answered":{"type":"boolean","description":"Every person (for `perPerson`) or the booking (for `perBooking`) has an answer."}}}]}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"discountTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPromotionIds":{"type":"array","description":"**Re-evaluated on every read.** A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became applicable should be.\n","items":{"type":"string","format":"uuid"}},"couponCodes":{"type":"array","readOnly":true,"description":"The promo codes the guest entered through `applyCartPromoCode` (decided 28 September, audit R073 (e)). **Sent as `couponCodes` on every promotions evaluation of this cart**, so a code is re-checked on each read like any promotion; a code that stops qualifying stays listed here and its promotion drops out of `appliedPromotionIds`.\n","items":{"type":"string","maxLength":100}},"expiresAt":{"type":"string","format":"date-time","description":"The earliest lease expiry in the cart, or the cart's own window where it holds none."},"extensionsUsed":{"type":"integer","readOnly":true},"maxExtensions":{"type":"integer","readOnly":true},"locale":{"type":"string"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time"}}},
"CartConflict": {"type":"object","x-ticvai-persistence":"none — computed on read","description":"2.9.5. Golf at 13:00 and karting at 13:00 for the same guest. **A prompt, not a refusal** — a party of four may legitimately split, and refusing would be wrong more often than right.\n","properties":{"kind":{"type":"string","enum":["overlappingTime","sameSessionDifferentVenue","exceedsPartySize","requiresPrerequisite","consentBlocksBooking"]},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"message":{"type":"string"},"isBlocking":{"type":"boolean","description":"Most are not. `requiresPrerequisite` is — an add-on with no ticket to attach to cannot be sold. So is `consentBlocksBooking`: a consent question answered with the answer the venue set to block the booking (decided 29 September, rev 3 REV3-26).\n"}}},
"CartLine": {"type":"object","x-ticvai-persistence":"orders.cart_line","required":["id","variantId","quantity"],"properties":{"id":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"productName":{"type":"string","readOnly":true},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid","nullable":true},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Set from `addCartLine`; checkout copies it to the order line.\n"},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"Set on a table deposit line only (decided 29 September, rev 3 REV3-8b): the `fnb.TableReservation` this line secures. Priced from the deposit the booking snapshotted, not from the variant. Becomes an `orders.deposit` row at checkout, not revenue. A table booking with no deposit never has a line (rev 3 REV3-8).\n"},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"}},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"The `resources.ResourceHold` this line buys (decided 29 September, rev 3 REV3-15). While set, `leaseExpiresAt` is the hold's `expiresAt` and `inventoryHoldId` is null."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"parentLineId":{"type":"string","format":"uuid","nullable":true,"description":"The line this add-on is attached to, from `AddCartLineRequest.parentLineId`. Kept on the line because **removing the parent removes the child**, and `removeCartLine` has to be able to find the children.\n"},"overridePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"overrideReason":{"type":"string","nullable":true,"enum":["priceMatch","serviceRecovery","negotiated","damagedGoods","staffSale","error"],"description":"BL-085. **An operator could apply an approved discount and not enter a price.** A price match against a competitor and a service-recovery gesture are not discounts off a list — they are a number somebody decided.\n**Escalated above a configured threshold, and the reason is a closed set**: a free-text override reason is an override nobody can report on, and this is the field an auditor reads first.\n"},"feeKind":{"type":"string","nullable":true,"enum":["booking","transaction","service","delivery","convenience","cancellation"],"description":"**A fee is a line, not an adjustment.** `orders` already separates a service charge from a tip for the reason that applies here: **a guest is entitled to see what they are being charged for**, and a fee folded into the ticket price is a fee nobody can question.\nItemised at checkout, taxed on its own code, and refundable separately — **a cancellation fee is usually the one thing not refunded**, which only works if it is its own line.\n"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lineTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"inventoryHoldId":{"type":"string","nullable":true,"description":"The capacity held for this line — a `catalogue.InventoryHold.id`, typed as that id is. **Null for a product with no capacity** — a t-shirt needs stock, not a lease.\n"},"leaseExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"Shown to the guest. *\"Your seats are held for 6 minutes\"* is better than discovering it at checkout.\n"},"isAvailable":{"type":"boolean","readOnly":true,"description":"Re-checked on every read. **A line can become unavailable while the cart sits** — a lease expiring is not the same as the product selling out, and both land here.\n"}}},
"CartStatus": {"type":"string","enum":["active","expiring","expired","abandoned","checkedOut"]},
"CashMovement": {"x-ticvai-persistence":"orders.cash_movement","allOf":[{"$ref":"#/components/schemas/CreateCashMovementRequest"},{"type":"object","required":["shiftId","authorisedByPrincipalId","sequence"],"properties":{"shiftId":{"type":"string","format":"uuid"},"depositBoxId":{"type":"string","format":"uuid","nullable":true,"description":"The box the cash moved in or out of. Set on every lift `withdrawFromDepositBox` records (26 September, pull audit R099).\n"},"witnessPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The cashier who countersigned a withdrawal. Null on other movements."},"withdrawalReason":{"allOf":[{"$ref":"#/components/schemas/WithdrawalReason"}],"nullable":true},"authorisedByPrincipalId":{"type":"string","format":"uuid","description":"The principal who authorised the movement, recorded for audit."},"sequence":{"type":"integer","description":"Monotonic within the shift. Preserves order across an offline batch."},"syncedAt":{"type":"string","format":"date-time","nullable":true}}}]},
"CashMovementKind": {"type":"string","enum":["openingFloat","lift","add"],"description":"`openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one cashier's box; `add` by `createCashMovement`.\n"},
"CreateCashMovementRequest": {"type":"object","required":["id","kind","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7."},"kind":{"$ref":"#/components/schemas/CashMovementKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"denominations":{"$ref":"#/components/schemas/DenominationCount","x-ticvai-persisted":false,"description":"**Stored as `orders.cash_count_line` rows** with `countKind: movement` and this movement's `cashMovementId`, not as a column. The jsonb blob this used to land in is what `Denomination` was created to replace (26 September, pull audit R099).\n"},"reference":{"type":"string","maxLength":64,"description":"Safe drop reference or bag number."},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","variantId","quantity","quotedUnitPrice"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these."},"variantId":{"type":"string","format":"uuid"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"inventoryHoldId":{"type":"string","nullable":true,"description":"Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"},"description":"Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"quantity":{"type":"integer","minimum":1},"eligibilityDeclaration":{"type":"array","nullable":true,"x-ticvai-note":"One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n","items":{"type":"object","properties":{"ageBand":{"type":"string","enum":["infant","child","junior","adult","senior"],"description":"Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."},"ageYears":{"type":"integer","nullable":true},"heightBandIndex":{"type":"integer","nullable":true},"confidentSwimmer":{"type":"boolean","nullable":true,"description":"**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"},"guardianSigned":{"type":"boolean"}}},"description":"What was declared for each guest on this line, kept as the record staff check at the gate."},"quotedUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the client charged, from its local bundle."},"holderName":{"type":"string","nullable":true},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"}}},
"DenominationCount": {"type":"array","description":"**A count is a list of lines and the line is the row.** Until 24 August this array carried the persistence hint itself, so `orders.cash_count_line` derived a single column — `shift_id` — and a count line had no denomination, no quantity and no variance.\n**The array is the transport; `CashCountLine` is the row.**\n","items":{"$ref":"#/components/schemas/CashCountLine"},"minItems":1},
"DepositBox": {"type":"object","x-ticvai-persistence":"orders.deposit_box + orders.deposit_box_opening_denomination + orders.deposit_box_foreign_holding","description":"5.8. **Allocated to a cashier, not to a workstation.** A cashier moving between tills takes their float with them, which is what makes a variance attributable to a person.\n**`openingDenominations` and `foreignHoldings` are child rows** (26 September, pull audit R099): `orders.deposit_box_opening_denomination` and `orders.deposit_box_foreign_holding`, one row per item, keyed to the box. Until then the contract carried both and the table had nowhere to put either.\n","required":["cashierPrincipalId","venueId","openingFloat"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"cashierPrincipalId":{"type":"string","format":"uuid"},"cashierName":{"type":"string","readOnly":true},"venueId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Where it is being used now. **Changes during a shift; the box does not.**"},"shiftId":{"type":"string","format":"uuid","nullable":true,"description":"The shift trading from this box. A UUIDv7, as `Shift.id` is."},"status":{"$ref":"#/components/schemas/DepositBoxStatus"},"openingFloat":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"openingDenominations":{"type":"array","description":"5.8.3. **Either this or a total** — a supervisor handing over a counted bag should not have to re-count it into fields. POS-001 offered only denominations until 14 August.\n","items":{"type":"object","required":["denominationId","count"],"properties":{"denominationId":{"type":"string","format":"uuid","description":"References `platform.denomination`, as `CashCountLine.denominationId` does. Until 26 September this was `denomination: number` — a face value as a JSON float, which naming-and-style 5.1 forbids and which could disagree with the note it named (pull audit R122).\n"},"count":{"type":"integer","minimum":0}}}},"withdrawnTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"**Reduces the expected close figure.** Cash skimmed for banking is not a shortfall, and a system that treats it as one makes every busy cashier look short.\n"},"overDrawerLimit":{"type":"boolean","readOnly":true,"default":false,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"**The box holds more than its till's drawer limit** (decided 2 October 2026, Chinmay, BO-042; DEC-179; CHG-CSP-016): computed on read from the box's expected cash against `tenancy.Workstation.cashDrawerLimit` or the venue's `cashDrawerLimit`. BO-042 flags the box and offers a lift; false where no limit is set. A flag, not a figure: it tells the cashier nothing about the expected cash (CHG-FIN-003).\n"},"foreignHoldings":{"type":"array","description":"4.6.11 and 6.1.10. **Foreign cash accepted at this till, counted separately by currency.** A till taking USD and EUR alongside AED has three counts and three variances — collapsing them into a base-currency total makes a variance unattributable to the currency that caused it.\n**No opening float in a foreign currency and no change given in one.** Foreign cash only ever comes in, which is what keeps this to one number per currency rather than a full reconciliation each.\n","items":{"type":"object","required":["currency","countedAmount"],"properties":{"currency":{"type":"string","pattern":"^[A-Z]{3}$","description":"**Stored, because it is the one thing that is not the region's.** A foreign holding is by definition cash in a currency the till does not trade in, so it cannot resolve from the region (ADR-0018) the way the box's own amounts do; it is the key of the row, one per currency per box. The amounts on this item are in this currency.\n"},"expectedAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The sum of tenders taken in this currency during the shift."},"countedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"baseEquivalent":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**At the rates on the payments, not today's.** A shift closed on Friday and reviewed on Monday is reviewed at Friday's rates (CF-37).\n"}}}},"expectedTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"countedTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**Flagged where it is not the holder.** A box closed without its holder present is allowed — the cash is counted by somebody, and who counted it is the record.\n"},"allocatedAt":{"type":"string","format":"date-time","description":"When the device recorded the allocation. `allocateDepositBox` is offline-capable, so for a box allocated offline this differs from the server's receipt time.\n"},"closedAt":{"type":"string","format":"date-time","nullable":true}}},
"DepositBoxStatus": {"type":"string","enum":["allocated","open","suspended","closing","closed","reconciled"]},
"EntitlementStatus": {"type":"string","description":"**What the storage layer holds, and what a guest is shown.** `MediaEntitlements` carried only `isValid` and a reason string — a boolean cannot distinguish a ticket that was used from one that expired, was refunded, or was transferred to somebody else, and those are four different conversations at a gate.\nAdded 17 August. `states/entitlement.yaml` had modelled these six since 14 August and the contract had no enum behind it, which the state checker reported correctly for three days.\n\n**The client's 13 Virtual Ticket statuses map onto these six** (decided 2 October 2026, Chinmay, critical set 2, BO-336: \"Map the pack's 13 names onto the model; add any missing states\"; DEC-266; CHG-CSP-033). Every name maps, so no value is added (one would be a breaking change against r1): Active is `issued`, Partially used `partiallyConsumed`, Used `fullyConsumed`, Expired `expired`, Transferred `surrendered`, Suspended and Blocked are `issued` with the suspended flag or an identity lock, and Cancelled, Voided, Refunded and Reissued / superseded are `cancelled` told apart by access `Entitlement.cancellationKind`. Created and Pending fulfilment (DI-670's Reserved) are the order before an entitlement exists. The table is `states/entitlement-status.yaml` (`pack_status_map`); access `Entitlement.lifecycleLabel` carries the name.\n","enum":["issued","partiallyConsumed","fullyConsumed","expired","cancelled","surrendered"]},
"ExchangeOrderRequest": {"type":"object","required":["id","outgoingLineIds","incomingLines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header."},"outgoingLineIds":{"type":"array","minItems":1,"items":{"type":"string","format":"uuid"}},"incomingLines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"waiveFee":{"type":"boolean","default":false},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"MediaAsset": {"x-ticvai-persistence":"assets.media_asset","type":"object","required":["id","kind","status","filename","contentType","sizeBytes","referenceCount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MediaKind"},"status":{"$ref":"#/components/schemas/MediaStatus"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"title":{"$ref":"#/components/schemas/LocalisedText"},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Required before use in a guest-facing surface. WCAG 2.2 AA."},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"durationSeconds":{"type":"number","nullable":true},"customMetadata":{"type":"object","nullable":true,"additionalProperties":true,"description":"BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"},"sharedWithTenantIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"},"tags":{"type":"array","items":{"type":"string"}},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"url":{"type":"string","description":"Signed and expiring for private assets; stable CDN URL for public ones."},"thumbnailUrl":{"type":"string","nullable":true},"referenceCount":{"type":"integer","description":"How many surfaces reference this asset. Non-zero refuses deletion.\n"},"rights":{"$ref":"#/components/schemas/MediaRights"},"isRightsExpired":{"type":"boolean"},"version":{"type":"integer"},"uploadedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"MediaAssetDetail": {"x-ticvai-persistence":"assets.media_asset","allOf":[{"$ref":"#/components/schemas/MediaAsset"},{"type":"object","properties":{"derivatives":{"type":"array","description":"Generated from the original, never uploaded separately. A new breakpoint is a re-render rather than a re-upload of everything.\n","items":{"type":"object","properties":{"label":{"type":"string"},"width":{"type":"integer"},"height":{"type":"integer"},"sizeBytes":{"type":"integer"},"url":{"type":"string"}}}},"usage":{"type":"array","description":"Every place this asset is referenced.","items":{"$ref":"#/components/schemas/MediaUsage"}},"collections":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"}}}},"previousVersions":{"type":"array","items":{"type":"object","properties":{"version":{"type":"integer"},"replacedAt":{"type":"string","format":"date-time"},"replacedByPrincipalId":{"type":"string","format":"uuid"}}}}}}]},
"MediaEntitlements": {"type":"object","x-ticvai-persistence":"none — projection over entitlement and scan history","required":["mediaCode","isValid","entitlements"],"properties":{"mediaCode":{"type":"string"},"mediaKind":{"type":"string","enum":["qr","wristband","card","nfc","mobilePass"]},"subjectId":{"type":"string","format":"uuid","nullable":true},"isValid":{"type":"boolean"},"invalidReason":{"type":"string","nullable":true},"canAcceptMore":{"type":"boolean","description":"False where the media has been surrendered, expired or blocked. A cashier should know before taking money, not after.\n"},"entitlements":{"type":"array","items":{"type":"object","properties":{"entitlementId":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","enum":["admission","locker","fnb","retail","parking","rental","experience","membership"]},"orderId":{"type":"string","format":"uuid"},"addedAt":{"type":"string","format":"date-time"},"status":{"allOf":[{"$ref":"#/components/schemas/EntitlementStatus"}],"description":"**Replaced `isRedeemed` on 17 August.** A boolean could not distinguish a ticket that was used from one that expired, was refunded, or was transferred — four different conversations at a gate, and the steward could see only \"not valid\".\n"},"entriesUsed":{"type":"integer"},"entriesAllowed":{"type":"integer","nullable":true},"redeemedAt":{"type":"string","format":"date-time","nullable":true},"transferredToSubjectId":{"type":"string","format":"uuid","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true}}}}}},
"MediaUsage": {"x-ticvai-persistence":"assets.media_usage","type":"object","description":"One place an asset is used. **`surface: product` is written by catalogue** for each item of `Product.media` (decided 29 September, rev 3 23SEP-4): `referenceId` is the product id and `isLive` is true while the product is listed to guests, which is what stops an asset in use on a ticket card being archived from under it.\n","required":["surface","referenceId"],"properties":{"extractedText":{"type":"string","description":"**Text pulled out of an uploaded document**, after extraction. The generic retrieval path for anything a tenant uploads — a PDF nobody can search is a PDF nobody reads.\n"},"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"surface":{"type":"string","enum":["tenantBranding","homepageBanner","promoBlock","contentPage","product","event","menuItem","merchandise","workOrder","incident","inspection","campaign"]},"referenceId":{"type":"string"},"label":{"type":"string"},"isLive":{"type":"boolean","description":"True where the referencing surface is published to guests."}}},
"MenuItem": {"x-ticvai-persistence":"fnb.menu_item","type":"object","required":["id","productVariantId","name","price","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"productVariantId":{"type":"string","format":"uuid","description":"**The catalogue variant this item links to, for reporting, stock and tax class only. It is not where the price comes from** (Chinmay, 2 October, workbook Q34; CHG-CSA-009). F&B owns its own catalogue: F&B prices were migrated into the F&B service so ticketing scales as an isolated service (ADR-0028), and the price an outlet sells at is `price` on this item. The central catalogue prices tickets and single-price booths; it never reprices a dish. A menu belongs to one outlet, so `price` is that outlet's price, and an outlet may set its own; it changes through `updateMenu`, `setMenuSections` or `applyMenuActions` (`reprice`). Tax is computed on the order line by the tax engine. (Replaces the earlier text \"pricing and tax come from there — a menu is a presentation of the catalogue\", which was stale.)\n"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"dailyCount":{"type":"integer","minimum":0,"nullable":true,"readOnly":true,"description":"**How many portions the kitchen set for today** (`setMenuItemDailyCount`; Chinmay, 2 October, workbook Q194; CHG-CSA-017). Null means the item is not counted. Reset at the venue day start.\n"},"remainingCount":{"type":"integer","minimum":0,"nullable":true,"readOnly":true,"description":"**What is left of `dailyCount`** (\"6 left\" on the till and the guest menu). Each sale takes from it; **at zero the item is marked unavailable automatically**, with an `EightySixEvent` whose `source` is `dailyCount`. Null where the item is not counted.\n"},"sortOrder":{"type":"integer"},"modifierGroupIds":{"type":"array","items":{"type":"string","format":"uuid"}},"stationId":{"type":"string","format":"uuid","nullable":true},"menuSectionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The section the item sits in, set by `setMenuSections` and `applyMenuActions` (`moveSection`)."},"isStockTracked":{"type":"boolean","description":"True where a recipe exists. Stock-tracked items cannot be sold offline."},"isAvailable":{"type":"boolean"},"unavailableReason":{"type":"string","nullable":true},"restoreAt":{"type":"string","format":"date-time","nullable":true,"description":"When an unavailable item comes back on its own (`setItemAvailability`). Null means by hand."},"preparationMinutes":{"type":"integer","nullable":true},"allergens":{"type":"array","items":{"$ref":"#/components/schemas/AllergenCode"}}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**The currency the guest selected and is charged in** (CHG-FIN-001, 2 October 2026). Null or equal to `currency` for a sale in the base currency. Everything else on the order, and every ledger posting, stays in the base currency `currency`."},"chargeFxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`), stored on the order so the payment, the receipt, the tax invoice and any refund use the same rate (CHG-FIN-001)."},"chargeFxRateId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `finance.FxRate` row the rate was taken from, for audit."},"chargeTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"`grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to the provider asks for (CHG-FIN-001)."},"chargeRateLockedUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms the new amount (CHG-FIN-001)."},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderExchangeResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["orderId","outgoingValue","incomingValue","difference"],"properties":{"orderId":{"type":"string","format":"uuid"},"outgoingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incomingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"exchangeFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Only the difference settles. The replacement is held before the original is released, never the other way round.\n"},"newLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RotaAssignment": {"type":"object","x-ticvai-persistence":"workforce.rota_assignment","required":["principalId","venueId","startsAt","endsAt","position"],"properties":{"overtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"description":"BL-044, 1.2.83. **UAE labour law limits working hours and mandates rest periods**, and nothing in the package counted either. Derived from attendance against the shift.\n"},"restPeriodBefore":{"type":"integer","nullable":true,"description":"Minutes since the previous shift ended. **The check that stops a closing shift followed by an opening one**, which is legal in most places and unsafe in all of them.\n"},"breachesWorkingHourLimit":{"type":"boolean","default":false,"readOnly":true,"description":"**Flagged at assignment, not discovered at payroll.** A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a month later means it was worked.\n"},"labourCost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**Cost at the point of scheduling.** A manager building a rota without seeing its cost is a manager who finds out from finance.\n"},"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string","readOnly":true},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"position":{"type":"string","description":"What they are rostered to do — gate steward, cashier, lifeguard, technician. **Most positions never touch a till**, which is why a rota assignment is not a shift.\n**A position code, not a label.** It is the same value as `StaffingRules.minimumCover[].positionCode`, `OpenShift.positionCode` and `StaffingCoverage.positionCode`: coverage counts rostered people per position, so an assignment spelled differently from the rule it fills is counted against nothing and the gap stays open. Tenant-defined, which is why it is not an enum here.\n"},"requiredRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Checked on assignment. A rota naming someone unqualified is a rota that gets overridden."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Where the position needs a till. **The link between a rota and a cash session**, without merging the two.\n"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"status":{"$ref":"#/components/schemas/RotaStatus"},"breakMinutes":{"type":"integer","nullable":true},"note":{"type":"string","nullable":true}}},
"RotaStatus": {"type":"string","enum":["planned","published","confirmed","swapPending","cancelled","completed","noShow"]},
"Shift": {"x-ticvai-persistence":"orders.pos_shift + orders.pos_shift_approval + orders.pos_shift_incident","description":"**`approvals` and `incidents` are child rows** (26 September, pull audit R099): `orders.pos_shift_approval` and `orders.pos_shift_incident`, one row per item, keyed to the shift. Until then the contract carried both and `orders.pos_shift` had nowhere to put either.\n","type":"object","required":["id","workstationId","venueId","scopePath","principalId","status","currency","currencyScale","openedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key."},"workstationId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"principalId":{"type":"string","format":"uuid","description":"Who opened it. Cash reconciles to a person and a drawer."},"principalDisplayName":{"type":"string"},"incidents":{"type":"array","description":"BL-097. **A till has exceptions and there was nowhere to write them** — a no-sale, a drawer opened without a transaction, a manager override, a guest dispute.\n**This is the log a cash-up investigation starts from**, and a shift that balances with four unexplained no-sales is not a shift that balanced.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["noSale","drawerOpen","override","voidAfterPayment","guestDispute","tillJam","priceQuery","other"]},"at":{"type":"string","format":"date-time"},"principalId":{"type":"string","format":"uuid"},"note":{"type":"string","nullable":true}}}},"status":{"$ref":"#/components/schemas/ShiftStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"depositBoxCode":{"type":"string","nullable":true},"bagNumber":{"type":"string","nullable":true},"openingFloat":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"salesTotal":{"x-ticvai-column":"gross_sales_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till took in sales, as the guest paid it — tax included: the shift's takings, not Gross sales (CHG-FIN-002, CHG-FIN-010). **Never shown to the shift's own cashier before the count is in** (CHG-FIN-003): with the float and the lifts it gives away the expected cash.\n"},"refundsTotal":{"x-ticvai-column":"gross_refunded_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till paid back, as the guest was refunded it — tax included."},"liftsTotal":{"x-ticvai-column":"lifted_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net."},"expectedCash":{"x-ticvai-column":"expected_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"26 September, pull audit R207. **The figure the blind count was measured against**, revealed once the count is in — null until then. Until this date only `ShiftCloseResult` carried it, returned once by `closeShift`, so BO-040 could not show the over/short it exists to accept. **Null to the shift's own cashier on every read** (CHG-FIN-003, 2 October): returned only to a caller holding OVERSHORT_ACCEPT or SHIFT_CLOSE_OTHER at the venue.\n"},"countedCash":{"x-ticvai-column":"counted_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"What the close count found. Null until the shift is counted."},"variance":{"x-ticvai-column":"variance_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"Counted minus expected, as `ShiftCloseResult.variance`. Negative is short. Null to the shift's own cashier, as `expectedCash` (CHG-FIN-003)."},"cashierReason":{"type":"string","nullable":true,"readOnly":true,"enum":["tillError","unrecordedRefund","miscount","other"],"description":"What the cashier said went wrong, given with the blind count (`CloseShiftRequest.cashierReason`, DI-803) without seeing the variance; the supervisor reads it beside the variance on BO-040 (CHG-FIN-003).\n"},"cashierNote":{"type":"string","nullable":true,"readOnly":true,"maxLength":1000,"description":"The cashier's note with the count (`CloseShiftRequest.notes`; CHG-FIN-003)."},"heldLeaseCount":{"type":"integer","description":"Inventory leases currently held by this workstation. Surfaced so an operator closing a shift can see what will be returned.\n"},"openedAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time","description":"When the device recorded the open. `openedAt` is the server's time."},"suspendedAt":{"type":"string","format":"date-time","nullable":true},"suspendReason":{"type":"string","maxLength":200,"nullable":true,"description":"The `reason` given to `suspendShift`. Cleared on resume."},"closedAt":{"type":"string","format":"date-time","nullable":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who submitted the close count. `reopenShift` refuses an approver who is this principal, and until 26 September there was nothing to compare against (pull audit R099).\n"},"recountRequestedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `rejectShiftVariance`, cleared by the cashier's recount** (decided 2 October 2026, Chinmay; DEC-175; CHG-CSP-013; DI-804). While set, the shift is `pendingVariance` waiting for the cashier rather than the supervisor: the cashier's view says \"Recount requested\" instead of \"Under review\".\n"},"recountRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The supervisor who sent the count back (CHG-CSP-013)."},"recountReason":{"type":"string","nullable":true,"readOnly":true,"maxLength":500,"description":"The supervisor's reason, shown to the cashier; never an amount (CHG-CSP-013, CHG-FIN-003)."},"countNumber":{"type":"integer","minimum":0,"readOnly":true,"description":"How many close counts the shift has had: 0 before the first, 1 after it, 2 after a recount (CHG-CSP-013). The latest is the one measured.\n"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while the shift has unsynced operations."},"approvals":{"type":"array","items":{"type":"object","required":["kind","principalId","at"],"properties":{"kind":{"type":"string","enum":["open","close","variance"],"description":"`open` from `approveShiftOpen`, `close` from `approveShiftClose`, `variance` from `acceptShiftVariance`.\n"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"reason":{"type":"string"}}}}}},
"ShiftStatus": {"type":"string","enum":["pendingApproval","open","suspended","pendingVariance","pendingClosure","closed","autoClosed"]},
"TableCombination": {"type":"object","x-ticvai-persistence":"fnb.table_combination","description":"**Tables that can be pushed together, and what they seat together.** Declared by a host rather than inferred from a floor plan — a pillar, a step or a service run stops two adjacent tables combining. `setTableCombinations` writes the outlet's set.\n","required":["tableIds","combinedCovers"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"outletId":{"type":"string","format":"uuid","readOnly":true,"description":"The outlet in the path."},"tableIds":{"type":"array","minItems":2,"items":{"type":"string","format":"uuid"}},"combinedCovers":{"type":"integer","minimum":1},"setupMinutes":{"type":"integer","default":5},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `outlet` scope."}}},
"TableDefinition": {"x-ticvai-persistence":"fnb.dining_table","type":"object","description":"A restaurant (dining) table, reserved with `createTableReservation`. Not a map-bookable `resources` table, which is a non-dining spot sold like a cabana (decided 29 September, rev 3 GAP-C2).","required":["id","label","capacity"],"properties":{"id":{"type":"string","format":"uuid"},"label":{"type":"string","maxLength":32,"x-ticvai-unique":"venue","description":"**The table code, unique per venue** (decided 28 September, audit R108). Two tables in one venue never share a label, across all its outlets, so *T12* names one table wherever it is read. `createTable` and `updateTable` refuse a duplicate with `409` `duplicate-code`.\n"},"capacity":{"type":"integer","minimum":1},"zone":{"type":"string","nullable":true},"position":{"type":"object","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"shape":{"type":"string","enum":["round","square","rectangle","booth","bar"]},"isOutOfService":{"type":"boolean","default":false,"description":"**Damaged, or its section closed.** `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`."}}},
"TableMap": {"x-ticvai-persistence":"none — projection","type":"object","required":["outletId","tables"],"properties":{"outletId":{"type":"string","format":"uuid"},"zones":{"type":"array","items":{"type":"string"}},"tables":{"type":"array","items":{"$ref":"#/components/schemas/TableState"}}}},
"TableState": {"x-ticvai-persistence":"none — projection over table and visit","allOf":[{"$ref":"#/components/schemas/TableDefinition"},{"type":"object","required":["status"],"properties":{"status":{"$ref":"#/components/schemas/TableStatus"},"visitId":{"type":"string","format":"uuid","nullable":true},"covers":{"type":"integer","nullable":true},"seatedAt":{"type":"string","format":"date-time","nullable":true},"serverPrincipalId":{"type":"string","format":"uuid","nullable":true},"billTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}]},
"TillShiftPolicy": {"x-ticvai-persistence":"orders.till_shift_policy","type":"object","description":"**The venue's opening, closing and exception rules for every till** (CHG-CSP-020; POS-019; DI-309). One per venue. Proposed defaults are ours, client to correct.\n","required":["venueId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","readOnly":true},"requireOpenApproval":{"type":"boolean","default":false,"description":"Every shift opens `pendingApproval` and waits for `approveShiftOpen` (SHIFT_APPROVE_OPEN). Off by default: only a float outside `openingFloatTolerance` waits.\n"},"openingFloatTolerance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"How far a declared opening float may differ from the box's allocated float before the shift waits for approval (`states/shift.yaml`, pendingApproval). Null: any difference waits.\n"},"depositBoxRequired":{"type":"boolean","default":true,"description":"A shift cannot open without a deposit box (`OpenShiftRequest.depositBoxCode`); refused `400` otherwise."},"bagNumberRequired":{"type":"boolean","default":false,"description":"A shift cannot open without a bag number (`OpenShiftRequest.bagNumber`)."},"requireCloseApproval":{"type":"boolean","default":false,"description":"Every counted shift waits in `pendingClosure` for `approveShiftClose` (SHIFT_APPROVE_CLOSE), even within the variance threshold.\n"},"autoCloseAfterHours":{"type":"integer","nullable":true,"minimum":1,"maximum":48,"default":14,"description":"Hours after which an open or suspended shift nobody closed is closed by the inactivity job as `autoClosed` and the supervisors are told (`states/shift.yaml`). Null never auto-closes.\n"},"noSaleAlertCount":{"type":"integer","nullable":true,"minimum":1,"default":10,"description":"No-sales in one shift (`recordNoSale`) at which the supervisors are alerted on the venue's alerting channel; the count is on POS-020. Null sends no alert.\n"},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"WithdrawalReason": {"type":"string","description":"Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records.","enum":["banking","safeDrop","changeOrder","other"]}
}
```
