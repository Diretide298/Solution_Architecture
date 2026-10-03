# P08-venue-operations-01 — P08 · Venue Operations (1 of 2)

**10 screens · 73 operations · 107 schemas · 28 permissions**

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

- **Every control that can be refused must be gated.** 28 permissions apply here:
  `ACCESS_OVERRIDE, ACCESS_POINT_CONFIGURE, ACCESS_VALIDATE, ASSET_VIEW, DEVELOPER_MANAGE, DEVELOPER_VIEW, DEVICE_CONFIGURE, DEVICE_MANAGE, DEVICE_VIEW, INCIDENT_MANAGE, INCIDENT_VIEW, MAINTENANCE_APPROVE`…. A control nobody can use must say so,
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

### Finance, Ledger & Tax · Reporting & Analytics

Finance and insights run underneath every sale. A sale at a till (P04), kiosk, web storefront (P01) or guest app (P02) is priced and taxed per line at the moment of sale, recorded in the venue's base currency (AED in the UAE; 2 decimals, or 3 for BHD, KWD and OMR, never rounded away), and posted to an append-only dual ledger through account mappings per money event; anything unmapped lands in suspense. Tax follows the jurisdiction's tax profile: inclusive or exclusive, compound where a tax applies on another, zero-rated or exempt with verified evidence, and computed on the discounted price by default or on the price before discount where the region requires it (Egypt). A guest may select a currency the venue charges and pay in it: the rate is locked on the order, the payment partner is asked in that currency, the ledger keeps the base amount with the rate, and a refund goes back in the currency paid (decided 2 October 2026, Chinmay); a currency shown but not charged is an approximate price. Foreign cash at a till is recorded at its base equivalent and change is given in base currency. A paid order can carry a VAT receipt (simplified tax invoice), a full tax invoice with the buyer's TRN, or a consolidated invoice for a company, each numbered without gaps and never edited; corrections are credit memos. Revenue is recognised by rule: POS-style immediate, tickets on the visit, gift cards and wallet on use, annual passes straight-line or per visit, breakage on expiry; deferred revenue is a balance that ages. Each venue's day is reconciled (POS cash, gateways, bank, wallet against the ledger, provider files matched automatically, only genuine mismatches to a person); chargebacks are defended against the bank's deadline; month end runs seven close checks and goes to a finance approver. Nothing posted is deleted: a correction is a reversal, an approver is never the preparer, and ledger approval needs a second factor. Back-office finance lives in Venue Management (P08: chart of accounts, mapping, FX, journals, recognition, reconciliation, period close, chargebacks); tax profiles, calculation validation and platform reconciliation in the TICVAI Console (P09); partner settlement in P10. Reporting is one consolidated, permission-based area (Analytics, P16): seeded standard dashboards and reports plus no-code builders over a governed business catalogue; the P08 report screens, the POS terminal day view and the kitchen performance view are scoped windows onto the same definitions and must show the same numbers. Every figure is read from a lag-tolerant reporting copy and shows its "as of" time; scope comes from the person's rights, never from a filter; AI explains and recommends but never acts, answers only within the person's role, labels forecasts, and is phase two for finance ledgers.

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Base currency | The venue's region currency; the currency every record and ledger posting is in. A guest may pay in a currency they select (where the venue charges it); the books still hold the base amount and the rate. | Home currency, Local price, Default currency | DI-211 / DI-282 / contracts/spine/orders.yaml#/components/schemas/Order |
| Pay in USD (a currency the venue charges) | The guest's selected payment currency; the card is charged in it at the rate locked on the order, and refunds go back in it. | Converted price, Approx. (for a charged currency) | contracts/spine/orders.yaml#checkoutCart / … |
| ≈ (approx.) price in USD / SAR / … | A conversion of a base-currency price for a currency the venue shows but does not charge, always next to the base price. | Converted price, USD price | DI-211 / screens/P02-guest-mobile-app.yaml#GST-044 |
| Takings | Money received in the period less refunds (cash-basis); the seeded KPI on hubs. | Revenue, Sales, Income | contracts/satellite/reporting.yaml#/components/schemas/ReportingSystemKpi / R283 |
| Gross sales | Issued sales before discounts and refunds; whether tax is included must be stated on the tile. | Revenue, Turnover | MATRIX 6.1.78 |
| Net revenue | Gross sales less discounts less refunds, adjusted per finance policy. | Net sales, Revenue, Income | MATRIX 6.1.78 |
| Recognised revenue / Deferred revenue | Earned under the recognition rules / paid for but not yet earned. Kept distinct from sales. | Realised revenue, Unearned income, Wallet revenue | MATRIX 5.12.6 / DI-260 / contracts/spine/finance.yaml#getDeferredRevenue |
| VAT receipt | The simplified tax invoice issued on a paid order. | Receipt (when it is a tax document), Bill | contracts/spine/finance.yaml#issueTaxInvoice |
| Tax invoice / Combined tax invoice | A full invoice with the buyer's details / one invoice for several paid orders of one buyer. | Bill, Statement | contracts/spine/finance.yaml#/components/schemas/FinTaxInvoiceType |
| Credit memo | The document that corrects an issued invoice after a refund; the invoice itself is never edited. | Credit note (until the client's tax adviser chooses "Tax credit note"), Edit invoice | contracts/spine/finance.yaml#/components/schemas/FinTaxInvoice |
| VAT (or the jurisdiction's tax name) | Use the tax profile's own name on every surface; "Tax" only where several kinds are summed. | GST in UAE, Service charge for a tax | contracts/spine/catalogue.yaml#setTaxProfileJurisdiction |
| Price before discount | The taxable base where the jurisdiction taxes the undiscounted price. | Gross price, List tax | DI-598 |
| Post / Reverse | A journal reaches the ledger when approved and posted; a correction is a reversal, never an edit or delete. | Edit entry, Delete entry, Undo | contracts/spine/finance.yaml#reverseJournalEntry |
| Period (Open / Closing / Closed) | A fiscal period's state; closing stops postings, closed locks them. | Month locked, Frozen | contracts/spine/finance.yaml#/components/schemas/PeriodStatus |
| Variance (Over / Short) | The difference between expected and counted or recorded, always saying between which two figures. | Discrepancy, Error, Loss | DI-275 / contracts/spine/finance.yaml#/components/schemas/UnifiedReconciliation |
| Settlement / Exception / Resolve | A provider's file for a day / a line that did not match / the recorded explanation. | Payout file, Error, Close | contracts/spine/finance.yaml#/components/schemas/SettlementException |
| Chargeback | A bank-initiated reversal with an evidence deadline; not a refund. | Dispute refund, Reversal | contracts/spine/orders.yaml#/components/schemas/Chargeback |
| Report / Dashboard / Tile / KPI | A runnable, exportable, schedulable definition / a page of tiles / one visual bound to a report / a company-wide measure defined once. | Widget (outside the builder's library), Board (for a user-facing dashboard) | contracts/satellite/reporting.yaml#/components/schemas/DashboardTile / … |
| Warning / Critical | KPI status bands set by a target's amber and red thresholds; always words plus colour. | Amber, Red (alone), Bad | contracts/satellite/reporting.yaml#/components/schemas/KpiTarget |
| As of HH:MM / Updated N sec ago | The freshness of every figure read from the reporting copy; stale shows a warning. | Live (unless refreshed), Real-time | MATRIX 8.7.22 |
| Forecast | Any projected figure, with its range; never shown as a fact. | Expected, Will be | DI-973 |
| Outlet / Workstation (till) | A sales point / the device; staff copy may say "till" for the workstation. | Store, POS (in copy), Drawer (for the device) | R156 |
| Channel | POS, Web, App, Kiosk, B2B, OTA, from one closed list. | Source, Platform | MoM 2026-08-18 4.2 Recipes, Operating Hours & Service Channels / MATRIX 1.4.7 |

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
| `BO-036` | Device Registry | B–D | 32 | 41 | 6 | 66 | 10 | 0 | — | notStarted (generated) |
| `BO-044` | F&B Outlets | A | 72 | 38 | 6 | 2 | 0 | 0 | — | notStarted (generated) |
| `BO-058` | Reporting Home | B–D | 91 | 26 | 6 | 100 | 2 | 0 | — | notStarted (generated) |
| `BO-060` | Attendance & Footfall | B–D | 111 | 38 | 6 | 153 | 1 | 0 | — | notStarted (generated) |
| `BO-064` | Zones & Areas | A | 32 | 27 | 6 | 27 | 0 | 0 | — | notStarted (generated) |
| `BO-067` | Integrations | B–D | 5 | 40 | 6 | 27 | 1 | 0 | — | notStarted (generated) |
| `BO-070` | Work Orders | B–D | 61 | 31 | 6 | 17 | 6 | 2 | — | notStarted (generated) |
| `BO-100` | Venue Home | B–D | 4 | 29 | 6 | 18 | 2 | 0 | — | notStarted (generated) |
| `BO-108` | Venue Operations | B–D | 6 | 32 | 6 | 17 | 0 | 0 | — | notStarted (generated) |
| `BO-128` | Live Workstation Health Monitor | B–D | 3 | 12 | 6 | 0 | 9 | 6 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-036` Device Registry

**Know which handheld is where, and whether it has synced.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE`, `DEVICE_MANAGE`, `DEVICE_VIEW`, `REPORT_VIEW_VENUE`, `SCOPE_VIEW`, `WORKSTATION_CONFIGURE` (3 configure, 2 read, 1 operate); in the flows as technician |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listDevices` reads the population and `getWorkstation` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `workstationId` (deepLink), `deviceId` (deepLink) · cold entry: A workstation opened from the registry or an alert. A device opened from the registry. A profile opened from the list. |
| Route | `/venue-operations/device-registry` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board**, answering 4 board screen(s): Workstation Overview Dashboard; Workstation Registry; Workstation Details & Configuration and 1 more. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Owns POS board frame(s) POS-1A, POS-1B, POS-1C** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none. **Guest CRM operations removed 28 September (audit R254)** — `searchGuests`, `getGuestProfile`, `updateGuestProfile`, `mergeGuestProfiles`, `getGuestConsents`, `getConsentHistory`, `getGuestLoyalty`, `adjustLoyaltyPoints`, `getWishlist` and `listGuestDevices` were attached by module resemblance and have nothing to do with a device registry; the ones no other screen called moved to BO-735 Guest Directory. **Absorbed BO-127 on 28 September (audit R276)**: Hardware & Peripherals Management carried `listDevices`, `registerDevice` and `recordDeviceHeartbeat`, all already here, so nothing new came with it; BO-127 is retired and its entry from BO-108 lands here.

**Known gaps.** **`getWorkstationHealth` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape. Removed 2 October 2026 (CHG-WIR-021): recordDeviceHeartbeat is a device-audience operation the device sends itself; a back-office browser is not the device (device operations on staff screens are … Removed 2 October 2026 (CHG-WIR-021): The device register carried profile deployment (deployConfigurationProfile) and the audit log (listAuditRecords); deployment is BO-126's and the audit log …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Every device the venue owns (tills, handhelds, scanners, printers, terminals): where it is, who holds it, whether it answers and when it last synced, with registration, credential issue and revoke. The job is "which handheld is where"; configuring workstations and deploying profiles have their own screens.

**Fixed on main** (the package already carries these; draw what it says): Twelve operations including configureWorkstation, deployConfigurationProfile, listAlerts and listAuditRecords on the device register. (CHG-WIR-021); Shows a button or form for recordDeviceHeartbeat, whose only audience is device. (CHG-WIR-021); formRegisterDevice asks the person for id. (CHG-SBO-004); formDeployConfigurationProfile asks the person for status, id. (CHG-WIR-021); formRecordDeviceHeartbeat asks the person for status. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every registered device' drop id, driver, workstationId, pushToken, pushPlatform … (CHG-SBO-004).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are BO-036 and BO-127 the same screen?** → BO-127 is merged into BO-036 as one device register. *(decided by Chinmay, 2026-10-02; DEC-166 / CHG-NOTE-005)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listDevices`. | `listDevices` ?workstationId |
| Kind | select | optional | — | Receipt printer · Ticket printer · Label printer · Cash drawer · Barcode scanner · RFID reader · NFC reader · Card reader · ID reader · Biometric reader · Access reader · Payment terminal … | — | Sends `?kind=` to `listDevices`. | `listDevices` ?kind |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Sale board kind | radio group | — | Ticketing · Fnb · Retail · Mixed | `listWorkstations` ?saleBoardKind |
| Status | radio group | — | Raised · Acknowledged · Resolved · Expired | `listAlerts` ?status |
| Severity | segmented control | — | Info · Warning · Critical | `listAlerts` ?severity |
| Workstation | picker: choose a workstation | — | — | `listAlerts` ?workstationId |
| Shift | picker: choose a shift | — | — | `listAlerts` ?shiftId |
| Item | picker: choose an item | — | — | `listAlerts` ?itemId |

**Form: Register device** (modal, opened by *Register device*; *Register device* calls `registerDevice`, *Cancel* sends nothing)

**Collects what `registerDevice` sends before it is called.** Required: `kind`, `driver`, `workstationId`. Optional: `identifier`, `model`, `pushToken`, `pushPlatform`, `offlineScope`, `isRequired` and 5 more. **Not asked:** is a client UUIDv7 generated silently (design-note correction, 2 October 2026). Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `batteryPercent`, `capabilities`, `firmwareVersion`, `health`, `id`, `lastCheckedAt`, `lastHeartbeatAt`, `pushFailureCount`, `status` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Receipt printer · Ticket printer · Label printer · Cash drawer · Barcode scanner · RFID reader · NFC reader · Card reader · ID reader · Biometric reader · Access reader · Payment terminal … | — | `mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation. | `registerDevice` body |
| Driver `driver` | text field | required | — | — | — | Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change (ADR-0015). | `registerDevice` body |
| Identifier `identifier` | text field | optional | — | — | — | — | `registerDevice` body |
| Workstation `workstationId` | picker: choose a workstation | optional | — | — | shows names, sends the id | Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control device (one with a `hardwareType`), which is … | `registerDevice` body |
| Model `model` | text field | optional | — | — | — | — | `registerDevice` body |
| Hardware type `hardwareType` | select | optional | — | Standard turnstile · Full height turnstile · Tripod turnstile · Speed gate · Wide lane · Accessible pod gate · Buggy gate · Vip gate · Staff gate · Android handheld · Ios device · Tablet … | — | The specific hardware under `kind` (ADR-0067, 1 October): Access's hardware types (a speed gate, a tripod turnstile, a podium) merged into the one register. | `registerDevice` body |
| Hardware model `hardwareModelId` | picker: choose a hardware model | optional | — | — | shows names, sends the id | The model in the hardware library (access `setHardwareModel`; ADR-0067). Access owns the library; this names a model in it. | `registerDevice` body |
| Serial number `serialNumber` | text field | optional | — | max length 100; A serial already registered in the tenant is refused `409` by `registerDevice`. | — | The manufacturer's serial (ADR-0067: was on the access-control device row, now `access.device_placement`). | `registerDevice` body |
| Ip network reference `ipNetworkReference` | text field | optional | — | — | — | Network address or reference the device is reached at (ADR-0067). | `registerDevice` body |
| Push token `pushToken` | text field | optional | — | Guest devices register for push and staff devices did not — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has … | — | BL-163. Guest devices register for push and staff devices did not — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told … | `registerDevice` body |
| Push platform `pushPlatform` | radio group | optional | — | Ios · Android · Web · Windows | — | — | `registerDevice` body |
| Offline scope `offlineScope` | radio group | optional | — | None · Read only · Sell and scan · Full venue | — | BL-163. What this device may do with no connection, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it settled. | `registerDevice` body |
| Is required `isRequired` | toggle | optional | — | — | — | True blocks shift open when the device is unreachable. | `registerDevice` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Identifier already bound to another workstation, or `serialNumber` already registered in the tenant (`duplicate-serial`, moved here from access with the …; 422 `workstationId` missing for a kind other than `mobileHandset`, or given for a `mobileHandset` (18.1.5).

**Form: Configure workstation** (modal, opened by *Configure workstation*; *Configure workstation* calls `configureWorkstation`, *Cancel* sends nothing)

**Collects what `configureWorkstation` sends before it is called.** Required: `name`, `saleBoardId`. Optional: `cashierInputMode`, `guestDisplayContent`, `loadedMediaStockId`, `departmentId`, `accessPointId`, `devices`, `deploymentProfile`, `edgeNodeId`, `isActive`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets it (readOnly in the contract): `mediaStockRemaining` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Cashier input mode `cashierInputMode` | radio group | optional | Hybrid | Keyboard · Touch · Scanner · Hybrid | — | BL-061. A till operator who touch-types is slower on a touchscreen and a new starter is faster. | `configureWorkstation` body |
| Guest display content `guestDisplayContent` | multi-select chips | optional | — | Line items · Total · Loyalty balance · Promotions · Branding · Upsell · Queue position | — | What the guest-facing screen shows while a sale is in progress. Line items always; the rest is the venue's choice — and a second screen showing nothing is a second screen the … | `configureWorkstation` body |
| Loaded media stock `loadedMediaStockId` | picker: choose a loaded media stock | optional | — | — | shows names, sends the id | BL-095. Neither which stock a printer is loaded with nor how much is left. | `configureWorkstation` body |
| Name `name` | text field | required | — | max length 200 | — | — | `configureWorkstation` body |
| Sale board `saleBoardId` | picker: choose a sale board | optional | — | — | shows names, sends the id | This till's own layout, overriding its outlet's (DEC-183; CHG-CSP-006). Optional since 2 October 2026: absent or null, the till uses `Outlet.saleBoardId`. | `configureWorkstation` body |
| Outlet `outletId` | picker: choose an outlet | optional | — | — | shows names, sends the id | The outlet this till stands in (CHG-CSP-006). | `configureWorkstation` body |
| Cash drawer limit `cashDrawerLimit` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | This till's drawer limit; null inherits `VenueSettings.cashDrawerLimit` (DEC-179; CHG-CSP-016). | `configureWorkstation` body |
| Department `departmentId` | picker: choose a department | optional | — | — | shows names, sends the id | — | `configureWorkstation` body |
| Access point `accessPointId` | picker: choose an access point | optional | — | — | shows names, sends the id | — | `configureWorkstation` body |
| Devices `devices` | repeatable rows | optional | — | — | — | — | `configureWorkstation` body |
| Kind `devices[].kind` | select | required | — | Receipt printer · Ticket printer · Label printer · Cash drawer · Barcode scanner · RFID reader · NFC reader · Card reader · ID reader · Biometric reader · Access reader · Payment terminal … | — | `mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation. | `configureWorkstation` body |
| Driver `devices[].driver` | text field | required | — | — | — | Driver identifier. Adding a vendor is a driver plus configuration, never a core change — every venue arrives with hardware not previously seen. | `configureWorkstation` body |
| Identifier `devices[].identifier` | text field | optional | — | — | — | Serial | `configureWorkstation` body |
| Is required `devices[].isRequired` | toggle | optional | off | — | — | When true, the workstation refuses to open a shift if the device is absent. | `configureWorkstation` body |
| Deployment profile `deploymentProfile` | segmented control | optional | — | Terminal local · Venue edge · Thin | — | How this workstation obtains catalogue and inventory (ADR-0013). - `terminalLocal` — own SQLite, leases direct from the cell. | `configureWorkstation` body |
| Edge node `edgeNodeId` | picker: choose an edge node | optional | — | — | shows names, sends the id | — | `configureWorkstation` body |
| Is active `isActive` | toggle | optional | on | — | — | — | `configureWorkstation` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 A shift is open on this workstation. The change is not applied; it can be made once the shift has closed.; 422 No board would apply: the request sends no `saleBoardId` and the workstation's outlet has none (`sale-board-required`; CHG-CSP-006).

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: configureWorkstation: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/tenancy.yaml#configureWorkstation)*

#### Outputs: what the screen shows and produces

**Shown**

**Every registered device** (data table, from `listDevices`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Receipt printer, Ticket printer, Label printer, Cash drawer, Barcode scanner, RFID … | `mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no … |
| Identifier | text | — |
| Model | text | — |
| Offline scope | chip: None, Read only, Sell and scan, Full venue | BL-163. What this device may do with no connection, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it … |
| Firmware version | text | As the device last reported it on its heartbeat. |
| Is required | yes / no (icon or chip) | True blocks shift open when the device is unreachable. |

**Every workstation** (data table, from `listWorkstations`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Sale board | grouped details | Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. |
| Devices | list or chips (count when long) | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |

**Every alert** (data table, from `listAlerts`)

| Shows | Format | Notes |
|---|---|---|
| Rule name | text | `AlertRule.name` as it stood when the alert was raised. The line a person reads — a list of rule ids is not an alert panel, and a screen … |
| Metric | chip: Occupancy, Capacity utilisation, Admission rate, No show rate, Conversion, Sales by … | The rule's metric, carried so the alert says what went out of range. |
| Raised at | 1 Oct 2026, 14:30 | — |
| Severity | chip: Info, Warning, Critical | How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter. |
| Status | chip: Raised, Acknowledged, Resolved, Expired | Where a raised alert is. Shared by `Alert` and the `listAlerts` filter. |
| Observed value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Threshold | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |

**The selected registered device** (detail panel, from `listDevices`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Receipt printer, Ticket printer, Label printer, Cash drawer, Barcode scanner, RFID … | `mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no … |
| Driver | text | Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change … |
| Identifier | text | — |
| Push failure count | 1,234 | Consecutive failures. A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a … |
| Status | chip: Online, Offline, Error, Consumable low, Needs attention, Local mode… | What the device last said on its heartbeat; `unknown` until it has. `localMode` is an access-control device validating from its offline … |
| Battery percent | 1,234 | Board 1 of the client's POS design set, 20 August. A wristband encoder at 8% is a gate that stops working in an hour, and nothing in the … |
| Last checked at | 1 Oct 2026, 14:30 | Distinct from `lastHeartbeatAt`. A heartbeat is the workstation saying the device is attached; a check is the device answering. |
| Health | chip: Healthy, Warning, Degraded, Offline, Unknown | Derived, not reported. Computed from heartbeat age, battery, firmware currency and error rate — a device does not know whether it is … |

**The workstation** (detail panel, from `getWorkstation`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Sale board | grouped details | Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. |
| Devices | list or chips (count when long) | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Time zone | text | — |
| Health score | 1,234 | Board 1 of the client's POS set. A number a manager can sort by — the package held `lastHeartbeatAt` and a heartbeat timestamp is not a … |

**Workstation health** (detail panel, from `getWorkstationHealth`): Shows `score`, `status`, `contributors` from `getWorkstationHealth`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.

| Shows | Format | Notes |
|---|---|---|
| Score | 1,234 | — |
| Status | chip: Healthy, Warning, Degraded, Offline | — |
| Contributors | list or chips (count when long) | — |
| Factor | chip: Heartbeat age, Device offline, Device battery, Firmware outdated, Sync backlog … | — |
| Detail | text | — |
| Weight | 1,234 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Register device (primary button) | `registerDevice` POST `/devices` | RegisteredDevice | RegisteredDevice | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Identifier already bound to another workstation, or `serialNumber` already registered in the tenant (`duplicate-serial`, moved here … | opens modal first |
| Configure workstation (secondary button) | `configureWorkstation` PUT `/workstations/{workstationId}` | ConfigureWorkstationRequest | Workstation | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Device rows**: Asset tag, kind, model, assigned workstation name, custodian, last seen location and time, sync state; missing or silent devices first. *(source: contracts/spine/tenancy.yaml#listDevices; contracts/spine/tenancy.yaml#/components/schemas/DeviceAssignment)*
- **Money columns (observedValue)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. *(source: ADR-0008; ADR-0011; DI-306)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Revoke device credential**: The device stops authenticating at once; confirmation names the device and its custodian ("lost handheld" flow). *(source: contracts/spine/tenancy.yaml#revokeDeviceCredential)*
- **Deploy configuration profile**: Separate from Save. The publish gate names what goes live, where and from when before it happens; blocked names what is wrong and how to fix it; an override past a warning is recorded with who authorised it. *(source: screens/_components.yaml#publishGate; contracts/spine/tenancy.yaml#deployConfigurationProfile)*

**Data it reads**: `listDevices` (onLoad, List registered devices); `listWorkstations` (onLoad, List workstations); `listAlerts` (onLoad, What is currently raised)

**Where the user goes next**

- → `BO-124` Layout & Journey Builder: *Layout & Journey Builder*; carries `deviceId`
- → `BO-070` Work Orders: *A work order is raised to fix it*
- → `BO-129` Software, Configuration & Version Management: *A configuration profile is set for it*; carries `workstationId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The device registry list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the device registry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No device registry yet. Offers Register device (`registerDevice`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on workstationId, kind and the device registry are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `DEVICE_VIEW`, which `listDevices` requires to show this screen, and names that permission (the screen's other reads need `REPORT_VIEW_VENUE`, `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `DEVICE_CONFIGURE` for `registerDevice` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A shift is open on this workstation. The change is not applied; it can be made once the shift has closed.; 409 Identifier already bound to another workstation, or `serialNumber` already registered in the tenant (`duplicate-serial`, moved here from access with the …; 422 No board would apply: the request sends no `saleBoardId` and the workstation's outlet has none … |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds AUDIT_VIEW, DEVICE_VIEW, REPORT_VIEW_VENUE, SCOPE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: DEVICE_CONFIGURE for Register device; WORKSTATION_CONFIGURE for Configure workstation; TENANT_CONFIGURE for Deploy configuration profile; DEVICE_MANAGE for issueDeviceCredential, revokeDeviceCredential. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/tenancy.yaml#registerDevice)*
- **registerDevice answers 409**: Show it as something the person can act on, not a failure: Identifier already bound to another workstation, or `serialNumber` already registered in the tenant (`duplicate-serial`, moved here from access with the register, ADR-0067). *(source: contracts/spine/tenancy.yaml#registerDevice)*
- **registerDevice answers 422**: Show it as something the person can act on, not a failure: `workstationId` missing for a kind other than `mobileHandset`, or given for a `mobileHandset` (18.1.5). *(source: contracts/spine/tenancy.yaml#registerDevice)*
- **configureWorkstation answers 409**: Show it as something the person can act on, not a failure: **A shift is open on this workstation.** The change is not applied; it can be made once the shift has closed. Names the open shift. *(source: contracts/spine/tenancy.yaml#configureWorkstation)*
- **deployConfigurationProfile answers 409**: Show it as something the person can act on, not a failure: **The named version is not deployable** — it is still a `draft`, or this profile has no such version. Names the version and its status. *(source: contracts/spine/tenancy.yaml#deployConfigurationProfile)*

#### Consistency with other screens

- Match `BO-128`: Live health is there; this is the register.
- Match `ADM-582`: The Console's terminal assignment is the payment-terminal view of the same register (ADR-0067 one device register).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
devices:
- assetTag: AQC-AUH-0341
  kind: handheld
  model: Zebra TC52
  workstation: Main Gate Handheld 14
  custodian: Yusuf Rahman
  lastSeen: 01/10/2026 09:02
  sync: synced
- assetTag: AQC-AUH-0118
  kind: receiptPrinter
  model: Epson TM-m30III
  workstation: Main Gate Till 3
  lastSeen: 01/10/2026 09:05
- assetTag: AQC-DXB-0072
  kind: scanner
  model: Honeywell CT40
  custodian: unassigned
  lastSeen: 26/09/2026 18:11
  sync: 4 days behind
```

#### Permissions

- `listDevices` → `DEVICE_VIEW` (read) · staff
- `registerDevice` → `DEVICE_CONFIGURE` (configure) · staff
- `configureWorkstation` → `WORKSTATION_CONFIGURE` (configure) · staff
- `getWorkstation` → `SCOPE_VIEW` (read) · staff
- `getWorkstationHealth` → `DEVICE_VIEW` (read) · staff
- `listWorkstations` → `SCOPE_VIEW` (read) · staff
- `listAlerts` → `REPORT_VIEW_VENUE` (operate) · staff
- `issueDeviceCredential` → `DEVICE_MANAGE` (configure) · staff
- `revokeDeviceCredential` → `DEVICE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `DEVICE_VIEW`, which `listDevices` requires to show this screen, and names that permission (the screen's other reads need `REPORT_VIEW_VENUE`, `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `DEVICE_CONFIGURE` for `registerDevice` …

#### Requirements it meets

66 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.18 | POS and kiosk devices shall be linked to the Device Management module so administrators can monitor device status, location, software version, connectivity, errors, paper levels, and assigned … | Ticketing Sales | CONTRACTED | `listDevices` |
| 2.1.26 | System shall provide centralized monitoring of kiosk health including online status, stock levels, payment devices, printers, connectivity, and alerts. | Ticketing Sales | CONTRACTED | `listDevices` |
| 8.9.6 | System shall monitor scanners, POS devices, kiosks, handhelds, printers, gates, network connectivity, and infrastructure health. | Unified Operations Dashboard | CONTRACTED | `listDevices` |
| 16.2.7 | Device Inventory Management - System shall maintain device inventories. | Device Management | CONTRACTED | `listDevices` |
| 16.2.8 | Device Classification - System shall support device categorization. | Device Management | CONTRACTED | `listDevices` |
| 16.2.12 | Device Asset Tracking - System shall maintain device asset records. | Device Management | CONTRACTED | `listDevices` |
| 16.9.55 | Device APIs - System shall expose device management APIs. | Device Management | CONTRACTED | `listDevices` |
| 2.1.14 | The system should be able to identify each ticketing kiosk individually by an ID, locate it geographically and administer it remotely. The kiosks should include a supervision interface and alert … | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.6 | It is expected that front gate sales can be performed by the operators using a POS having a touch screen. | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.7 | The POS can be connected to a keyboard for which the function touches can be setup by the system administrator. | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.8 | The POS can be connected to a cash drawer | Ticketing Sales | CONTRACTED | `registerDevice` |
| 2.13.9 | The POS can be connected to a BOCA printer (it is expected to have the list of ticket printing hardware compatible) | Ticketing Sales | CONTRACTED | `registerDevice` |
| … 54 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Asset record: purchase date, warranty status/expiry, supplier, serial, manufacturer; ownership and responsibility shown separately (venue owns, operations responsible); a visual map shows installation location. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-895)*
- Inventory counts by status (assigned, under maintenance, in stock) - e.g. 15 receipt printers broken down by ticketing, retail, F&B and in store. *(client request · MoM 15 Sep 2026, 4.4 Device Inventory, Configuration Templates & Driver Management · DI-894)*
- 360 device view shows status and workstation; reassign to another workstation or deactivate with a logged reason; lifecycle view tracks registration -> enrolment -> assignment -> reassignment. *(client request · MoM 15 Sep 2026, 4.3 Device Management - Registration, Enrollment & Workstation Assignment · DI-893)*
- Device directory: search and add devices (printers, scanners, customer displays, cash drawers, turnstiles, handhelds, mobile POS) capturing serial number, type and model; adding generates a secure enrolment code; devices are assigned to workstations (e.g. A has ticket printer, receipt printer and cash drawer). *(client request · MoM 15 Sep 2026, 4.3 Device Management - Registration, Enrollment & Workstation Assignment · DI-892)*
- Hardware and peripherals list nine device kinds, each with status, battery and last check. *(agreed · client-design-boards-audit 20 Aug 2026, What the boards give us - 1D Hardware & Peripherals · DI-402)*
- Workstation details: six tabs, a health score, a current-operator card with role and shift, IP address, configuration profile with version and deployment date, and a today's summary (transactions, refunds, cash collected). *(agreed · client-design-boards-audit 20 Aug 2026, What the boards give us - 1C Workstation Details · DI-401)*
- Hardware & peripheral management per workstation (receipt printer, cash drawer, payment terminal, barcode/ticket scanner, ticket printer) with device-level status. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-303)*
- New workstation form: name, auto-generated ID, department, mode; workstation detail: ID, department, IP address, configuration, linked devices, operator/shift activity and sales totals. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-302)*
- Workstation overview dashboard: all workstations for a venue (or across venues), grouped by department and sub-department, with online/offline/health status and type (mobile POS, kiosk, on-site POS). *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-301)*
- Each workstation records its connected devices (receipt printer, barcode scanner, ticket printer) so a cashier signing in there gets the right hardware automatically; every workstation has its own activity log and rights. *(agreed · MoM 7 Aug 2026, 3. Operating Areas, Workstations & Permissions Hierarchy · DI-150)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-036` · status **notStarted** · provenance generated · **Drawn by Claude Design on `POS Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/POS Board 1.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 1.dc.html#pos-1a`, `POS Board 1.dc.html#pos-1b`, `POS Board 1.dc.html#pos-1c`
- Flow F79 *A workstation is registered, configured and rolled out*, step 1: The new device is registered and its workstation configured. → **Known before it is used.** A till nobody registered is a till whose sales belong to nobody.
- Flow F95 *A fleet is watched, a fault is found, and a station is fixed*, step 2: The failing till is found, with its alerts. → Which device, where, and what it last said.
- Flow F95 *A fleet is watched, a fault is found, and a station is fixed*, step 4: The till is confirmed healthy again. → Reporting again, and the alert clears.
- Flow F79 branch at step 1 (medium): when A step in the chain is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` on each screen decides — a tenant without the retail licence does not see the retail half, and the journey is shorter rather than broken.
- ADR-0067 *One device register; Access keeps only where a device is placed* (`docs/adr/0067-one-device-register.md`)
- ADR-0015 *Standards-First Device Drivers* (`docs/adr/0015-standards-first-device-drivers.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (32), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (41 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-036?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Register device, Configure workstation, What publishing changes.
- [ ] Every transition is wired: `BO-124`, `BO-070`, `BO-129`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`, `DEVICE_MANAGE`, `DEVICE_VIEW`, `REPORT_VIEW_VENUE`, `SCOPE_VIEW`, `WORKSTATION_CONFIGURE`.
- [ ] The 10 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 6 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-044` F&B Outlets

**See every outlet and whether it is trading.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 1 · needs the `fnb` module |
| Block | Block A · task APP-SETUP-BO-044 |
| Who uses it | venue staff holding `INCIDENT_MANAGE`, `INCIDENT_VIEW`, `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `REGION_CONFIGURE`… (3 configure, 4 read); in the flows as storekeeper |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listOutlets` reads the population and `getGuestMenu` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `outletId` (deepLink), `actionId` (deepLink), `venueId` (session) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/f-b-outlets` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Improved 20 August against the client design board**, answering 9 board screen(s): F&B Command Center; Outlet Management; Create / Edit Outlet and 6 more. **The id, flows and navigation are unchanged** — a board specifies a screen further; it does not replace it. **Food-safety operations wired 20 August** — boards 5G and 5J of the client F&B pack, and **HACCP is a regulatory obligation nothing in the package touched.** **This screen owns 18 board frames — the whole of F&B board 1 and the whole of Retail board 1.** No flow could be derived from it because **a chain of nine frames that all resolve to one screen is not a journey**, it is one screen the client drew nine views of. **That is the module system working**: a venue configuring an outlet and a venue configuring a store are the same screen with a different licence, and `requiresModule` is what makes them look different. **Worth stating rather than papering over with a single-step flow.** **Five of the 74 board chains collapse to this one screen and no others do.** The client drew nine F&B views and nine retail views of one outlet configuration surface — **which is what makes it the strongest evidence in the package that the module system is the right shape.** Nine frames per domain, one screen, and `requiresModule` is the only …

**Known gaps.** **`getHaccpStatus` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape. Removed 2 October 2026 (CHG-WIR-008): Reserve merchandise (a guest or till act), Record waste (a stock act), the F&B order and merchandise tables, and the outlet stock and guest menu panels were … Removed 2 October 2026 (CHG-WIR-008): Reserve merchandise (a guest or till act), Record waste (a stock act), the F&B order and merchandise tables, and the outlet stock and guest menu panels were …

**From the Food, Beverage & Retail process.** The outlet register: every F&B outlet (and, under the retail licence, every shop) at the venue, whether it is trading now, and the outlet's own configuration — name, code, kind, zone, stock location, cost centre, opening hours, active; ordering and delivery rules; floor plan for table-service outlets; return policy for shops; food-safety status. One thing to get right: configuration is per outlet, and the outlet's type decides which panels it has (a quick-service counter has no floor plan; a fine-dining room does).

**Fixed on main** (the package already carries these; draw what it says): Reserve merchandise (reserveMerchandise), Record waste (recordWaste), the "Every F&B order" and "Every merchandise" tables, the outlet … (CHG-WIR-008); Text fields "Venue id" and "Kind"; columns id, venueId, stockLocationId, costCenterId. (CHG-SBO-008); The outlet has no type/service model or department link: OutletKind is restaurant/bar/cafe/kiosk/…, while DI-319 types outlets (fine … (CHG-SBO-008); No-access state is keyed to PRODUCT_VIEW (getFnbDeliveryPolicy) although the list is listOutlets (SCOPE_VIEW). (CHG-SBO-008); BO-044 duplicates the client pack's BO-728 Outlet Management and BO-729 Create / Edit Outlet; R276 did not decide this pair. (CHG-SBO-021).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Are outlet names bilingual (English and Arabic)?** → Outlet names: English, plus the local language where the country requires it. *(decided by Chinmay, 2026-10-02; DEC-031 / CHG-NOTE-004)*
- **Can an outlet be deactivated while it has live orders?** → Drawn default stands (answer: "Default / recommended accepted"): Allow with a warning naming the live orders. *(decided by Chinmay, 2026-10-02; DEC-032 / CHG-NOTE-004)*
- **Homogeneous venue-owned outlets set up once centrally — via templates or a bulk edit?** → Drawn default stands (answer: "Default / recommended accepted"): Via outlet templates (BO-730). *(decided by Chinmay, 2026-10-02; DEC-033 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Kind | select | optional | — | Shop · Restaurant · Bar · Cafe · Kiosk · Game floor · Ticket office · Mobile | — | Outlet kinds in words (restaurant, bar, cafe, kiosk ...); the venue comes from the session. | `Outlet.kind` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Outlet | picker: choose an outlet | — | — | `getFnbDeliveryPolicy` ?outletId |
| Kind | select | — | Shop · Restaurant · Bar · Cafe · Kiosk · Game floor · Ticket office · Mobile | `listOutlets` ?kind |

**Form: Save F&B delivery policy** (modal, opened by *Save F&B delivery policy*; *Save F&B delivery policy* calls `setFnbDeliveryPolicy`, *Cancel* sends nothing)

**Collects what `setFnbDeliveryPolicy` sends before it is called.** Required: `outletId`. Optional: `collectionEnabled`, `deliveryEnabled`, `collectionPoint`, `collectionHoldMinutes`, `asapCollectionMinutes`, `asapDeliveryMinutes`, `slotMinutes`, `minimumOrder`, `deliveryFee`, `freeDeliveryAbove`, `radiusKm` and 3 more. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `setFnbDeliveryPolicy` body |
| Collection enabled `collectionEnabled` | toggle | optional | on | — | — | — | `setFnbDeliveryPolicy` body |
| Delivery enabled `deliveryEnabled` | toggle | optional | off | — | — | — | `setFnbDeliveryPolicy` body |
| Collection point `collectionPoint` | text field | optional | — | max length 200 | — | — | `setFnbDeliveryPolicy` body |
| Collection hold minutes `collectionHoldMinutes` | number field (minutes) | optional | 20 | — | — | — | `setFnbDeliveryPolicy` body |
| Asap collection minutes `asapCollectionMinutes` | number field (minutes) | optional | 25 | — | — | — | `setFnbDeliveryPolicy` body |
| Asap delivery minutes `asapDeliveryMinutes` | number field (minutes) | optional | 45 | — | — | — | `setFnbDeliveryPolicy` body |
| Slot minutes `slotMinutes` | number field (minutes) | optional | 30 | — | — | — | `setFnbDeliveryPolicy` body |
| Minimum order `minimumOrder` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setFnbDeliveryPolicy` body |
| Delivery fee `deliveryFee` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setFnbDeliveryPolicy` body |
| Free delivery above `freeDeliveryAbove` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setFnbDeliveryPolicy` body |
| Radius km `radiusKm` | number field | optional | — | min 0 | — | — | `setFnbDeliveryPolicy` body |
| Emirates served `emiratesServed` | list of values (chips) | optional | — | — | — | — | `setFnbDeliveryPolicy` body |
| Cutlery opt in `cutleryOptIn` | toggle | optional | on | Cutlery only when asked for, as in the design. | — | Cutlery only when asked for, as in the design. | `setFnbDeliveryPolicy` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Save return policy** (modal, opened by *Save return policy*; *Save return policy* calls `setReturnPolicy`, *Cancel* sends nothing)

**Collects what `setReturnPolicy` sends before it is called.** Required: `outletId`, `defaultWindowDays`, `requiresReceipt`. Optional: `allowCashRefundOnCardSale`, `selfAuthoriseLimit`, `requiresSecondUserAbove`, `requiresApprovalAbove`, `restockableConditions`, `nonReturnableCategoryIds`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets it (readOnly in the contract): `id` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `setReturnPolicy` body |
| Default window days `defaultWindowDays` | number field (days) | required | — | min 0 | — | — | `setReturnPolicy` body |
| Requires receipt `requiresReceipt` | toggle | required | on | — | — | — | `setReturnPolicy` body |
| Allow cash refund on card sale `allowCashRefundOnCardSale` | toggle | optional | off | — | — | — | `setReturnPolicy` body |
| Self authorise limit `selfAuthoriseLimit` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Up to this, one cashier may accept a return alone. | `setReturnPolicy` body |
| Requires second user above `requiresSecondUserAbove` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setReturnPolicy` body |
| Requires approval above `requiresApprovalAbove` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setReturnPolicy` body |
| Restockable conditions `restockableConditions` | multi-select chips | optional | — | Resaleable · Opened · Damaged · Faulty · Missing parts | — | Conditions that return stock to sale. Everything else is written off. | `setReturnPolicy` body |
| Non returnable categorys `nonReturnableCategoryIds` | multi-picker: choose non returnable categorys | optional | — | — | — | — | `setReturnPolicy` body |

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

**Form: Sign corrective action** (modal, opened by *Sign corrective action*; *Sign corrective action* calls `signCorrectiveAction`, *Cancel* sends nothing)

**Collects what `signCorrectiveAction` sends before it is called.** Required: `actionTaken`. Optional: `disposal`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action taken `actionTaken` | text field | required | — | — | — | — | `signCorrectiveAction` body |
| Disposal `disposal` | radio group | optional | — | None · Discarded · Reworked · Quarantined · Returned | — | — | `signCorrectiveAction` body |

Errors to draw in the form: 409 A critical finding signed by the principal who raised it (`CorrectiveAction.raisedByPrincipalId`).

**Form: Create outlet** (modal, opened by *Create outlet*; *Create outlet* calls `createOutlet`, *Cancel* sends nothing)

**Collects what `createOutlet` sends before it is called.** Required: `code`, `name`, `venueId`, `kind`. Optional: `nameTranslations`, `outletType`, `departmentId`, `zone`, `stockLocationId`, `costCenterId`, `paymentTiming`, `admissionContext`, `producesForOutletIds`, `saleBoardId`, `openingHours`, `isActive`. `venueId` comes from the session, never typed. **Name** in English, plus each locale the region lists in `localLanguageNameLocales` (DEC-031). **Payment timing**: Send first, then pay (the default, R261) or Pay first (DEC-064). **Admission context**: Inside the venue (a guest order needs an admission ticket) or Standalone (no ticket; DEC-070). **Outlet type** and **department** …

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createOutlet` body |
| Name `name` | text field | required | — | max length 200 | — | The outlet's name in English. Other languages are `nameTranslations` (CHG-CSP-005). | `createOutlet` body |
| Name translations `nameTranslations` | key and value settings | optional | — | localLanguageNameLocales`, Arabic in the UAE), creating or amending an outlet without it is refused `422 local-name-required`. | — | The outlet's name in other languages, keyed by ISO 639-1 code (decided 2 October 2026, Chinmay, batch 2 #26, BO-044: "Yes, where a country needs it: the local language plus … | `createOutlet` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createOutlet` body |
| Kind `kind` | select | required | — | Shop · Restaurant · Bar · Cafe · Kiosk · Game floor · Ticket office · Mobile | — | — | `createOutlet` body |
| Outlet type `outletType` | select | optional | — | Fine dining · Casual dining · Quick service · Coffee shop · Bar lounge · Food court · Buffet · Commissary · Retail | — | The service model (DI-319; DEC-196; CHG-CSP-005). Null on an outlet that is not F&B or retail. | `createOutlet` body |
| Department `departmentId` | picker: choose a department | optional | — | — | shows names, sends the id | The department the outlet belongs to (DI-319: department, sub-department, cost centre and status; DEC-196; CHG-CSP-005): an `OrgUnit` of kind department, as … | `createOutlet` body |
| Zone `zone` | text field | optional | — | — | — | — | `createOutlet` body |
| Stock location `stockLocationId` | picker: choose a stock location | optional | — | — | shows names, sends the id | Where this outlet draws stock from. A shop and its stockroom are one location; a bar drawing from a central cellar is not. | `createOutlet` body |
| Cost center `costCenterId` | picker: choose a cost center | optional | — | — | shows names, sends the id | Revenue and cost attribution. Outlet is the natural grain for both. | `createOutlet` body |
| Payment timing `paymentTiming` | segmented control | optional | Send first | Send first · Pay first | — | Pay first, or send to the kitchen first then pay (DEC-064; CHG-CSP-004). | `createOutlet` body |
| Admission context `admissionContext` | segmented control | optional | Inside venue | Inside venue · Standalone | — | Inside the venue (needs an admission ticket) or standalone (no ticket) (DEC-070; CHG-CSP-004). | `createOutlet` body |
| Produces for outlets `producesForOutletIds` | multi-picker: choose produces for outlets | optional | — | — | — | One kitchen serving several outlets is a producing outlet (decided 2 October 2026, Chinmay, batch 6 set 5, BO-134: "Yes: via a producing outlet (one kitchen outlet produces for … | `createOutlet` body |
| Sale board `saleBoardId` | picker: choose a sale board | optional | — | — | shows names, sends the id | The till layout every till in this outlet uses, unless a till overrides it (decided 2 October 2026, Chinmay, batch 6 set 4, BO-109: "Per outlet, with a till override"; DEC-183 … | `createOutlet` body |
| Opening hours `openingHours` | repeatable rows | optional | — | — | — | The weekly pattern, one entry per window. Several windows on a day are allowed. | `createOutlet` body |
| Day `openingHours[].day` | select | required | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `createOutlet` body |
| From `openingHours[].from` | time picker | required | — | — | HH:mm, 24-hour | Local time, 24-hour `HH:MM`, when the outlet opens. | `createOutlet` body |
| To `openingHours[].to` | time picker | required | — | — | HH:mm, 24-hour | Local time, 24-hour `HH:MM`, when the outlet closes. | `createOutlet` body |
| Ends next day `openingHours[].endsNextDay` | toggle | optional | off | With `endsNextDay` false, `to` must be later than `from` (`422 window-ends-before-start`); with it true, `to` must be earlier than or equal to `from`, so a window never spans more than 24 hours. | — | A late-night window is one window past midnight (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-731; DEC-197; CHG-CSP-007). | `createOutlet` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `createOutlet` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Code already in use in this venue; 422 The region requires a local-language name and `nameTranslations` lacks it (`local-name-required`), an opening window ends before it starts …

**Form: Save outlet** (modal, opened by *Save outlet*; *Save outlet* calls `updateOutlet`, *Cancel* sends nothing)

**Collects what `updateOutlet` sends before it is called.** Nothing in the body is required. Optional: `name`, `nameTranslations`, `stockLocationId`, `costCenterId`, `departmentId`, `outletType`, `paymentTiming`, `admissionContext`, `producesForOutletIds`, `saleBoardId`, `openingHours`, `isActive`. `venueId` comes from the session, never typed. **Name** in English, plus each locale the region lists in `localLanguageNameLocales` (DEC-031). **Payment timing**: Send first, then pay (the default, R261) or Pay first (DEC-064). **Admission context**: Inside the venue (a guest order needs an admission ticket) or Standalone (no ticket; DEC-070). **Outlet type** and **department** (DEC-196, DI-319). …

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateOutlet` body |
| Name translations `nameTranslations` | key and value settings | optional | — | localLanguageNameLocales`, Arabic in the UAE), creating or amending an outlet without it is refused `422 local-name-required`. | — | The outlet's name in other languages, keyed by ISO 639-1 code (decided 2 October 2026, Chinmay, batch 2 #26, BO-044: "Yes, where a country needs it: the local language plus … | `updateOutlet` body |
| Stock location `stockLocationId` | picker: choose a stock location | optional | — | — | shows names, sends the id | — | `updateOutlet` body |
| Cost center `costCenterId` | picker: choose a cost center | optional | — | — | shows names, sends the id | — | `updateOutlet` body |
| Department `departmentId` | picker: choose a department | optional | — | — | shows names, sends the id | — | `updateOutlet` body |
| Outlet type `outletType` | select | optional | — | Fine dining · Casual dining · Quick service · Coffee shop · Bar lounge · Food court · Buffet · Commissary · Retail | — | How an F&B or retail outlet trades, which switches features on or off (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-729: "Add both fields: outlet type and department … | `updateOutlet` body |
| Payment timing `paymentTiming` | segmented control | optional | Send first | Send first · Pay first | — | When an F&B order is paid, set per outlet (Chinmay, 2 October, workbook Q64; refines audit R261 per outlet; CHG-CSA-010). | `updateOutlet` body |
| Admission context `admissionContext` | segmented control | optional | — | Inside venue · Standalone | — | Whether an outlet sits behind the admission gate (decided 2 October 2026, Chinmay, batch 1, WEB-036: "Inside the venue, a ticket is needed. | `updateOutlet` body |
| Produces for outlets `producesForOutletIds` | multi-picker: choose produces for outlets | optional | — | — | — | Replaces the whole list of outlets this one produces for (CHG-CSP-005). | `updateOutlet` body |
| Sale board `saleBoardId` | picker: choose a sale board | optional | — | — | shows names, sends the id | — | `updateOutlet` body |
| Opening hours `openingHours` | repeatable rows | optional | — | — | — | Replaces the whole weekly pattern. An empty array clears it. | `updateOutlet` body |
| Day `openingHours[].day` | select | required | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `updateOutlet` body |
| From `openingHours[].from` | time picker | required | — | — | HH:mm, 24-hour | Local time, 24-hour `HH:MM`, when the outlet opens. | `updateOutlet` body |
| To `openingHours[].to` | time picker | required | — | — | HH:mm, 24-hour | Local time, 24-hour `HH:MM`, when the outlet closes. | `updateOutlet` body |
| Ends next day `openingHours[].endsNextDay` | toggle | optional | off | With `endsNextDay` false, `to` must be later than `from` (`422 window-ends-before-start`); with it true, `to` must be earlier than or equal to `from`, so a window never spans more than 24 hours. | — | A late-night window is one window past midnight (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-731; DEC-197; CHG-CSP-007). | `updateOutlet` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateOutlet` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 As `createOutlet`: a missing required local-language name (`local-name-required`), a window that ends before it starts (`window-ends-before-start`), or a …

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Code and name**: Code unique within the venue (max 64; 409 "Code already in use"); name max 200. Kind is fixed after creation (no edit field). The name is in English, plus the local-language name where the country requires it (Arabic in the UAE). *(source: contracts/spine/tenancy.yaml#createOutlet / contracts/spine/tenancy.yaml#updateOutlet / decided 2 October 2026 by Chinmay (CHG-NOTE-004))*
- **Kind**: Under F&B: Restaurant, Bar, Café, Kiosk, Mobile. Under retail: Shop. Game floor and ticket office are not offered here. *(source: contracts/spine/tenancy.yaml#/components/schemas/OutletKind / DI-350)*
- **Stock location and cost centre**: Pickers by name; a bar drawing from a central cellar points at the cellar. *(source: contracts/spine/tenancy.yaml#/components/schemas/Outlet / DI-319)*
- **Opening hours**: Weekly grid, several windows per day (lunch and dinner), local HH:MM in the region's time zone. Saving an empty grid clears the hours — confirm before saving. *(source: contracts/spine/tenancy.yaml#/components/schemas/OpeningHoursWindow / contracts/spine/tenancy.yaml#updateOutlet)*
- **Ordering and delivery**: Collection on and delivery off by default; collection hold 20 min, ASAP collection 25 min, ASAP delivery 45 min, slot 30 min; minimum order, delivery fee and free-delivery threshold in AED; radius km and emirates served appear only when delivery is on; cutlery only on request (default on). *(source: contracts/satellite/fnb.yaml#setFnbDeliveryPolicy)*
- **Floor plan**: Only for outlets offering table service. Table labels unique across the venue (T12 names one table); a capacity change is refused while a party is seated at that table. *(source: contracts/satellite/fnb.yaml#setTableLayout / R108 / DI-319)*

#### Outputs: what the screen shows and produces

**Shown**

**Outlets** (data table, from `listOutlets`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | The outlet's name in English. Other languages are `nameTranslations` (CHG-CSP-005). |
| Kind | chip: Shop, Restaurant, Bar, Cafe, Kiosk, Game floor… | — |
| Outlet type | chip: Fine dining, Casual dining, Quick service, Coffee shop, Bar lounge, Food court… | The service model (DI-319; DEC-196; CHG-CSP-005). Null on an outlet that is not F&B or retail. |
| Zone | text | — |
| Payment timing | chip: Send first, Pay first | Pay first, or send to the kitchen first then pay (DEC-064; CHG-CSP-004). |

**The selected outlet** (detail panel, from `listOutlets`): Stock location, cost centre and department show their names; the ids stay for the copy action only. **Decided 2 October 2026 by Chinmay:** the name in English plus the local language where the region requires it (`nameTranslations`, `RegionSettings.localLanguageNameLocales`; DEC-031), the payment timing (pay first, or send to the kitchen first then pay; DEC-064), inside the venue (needs an …

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | The outlet's name in English. Other languages are `nameTranslations` (CHG-CSP-005). |
| Name translations | grouped details | The outlet's name in other languages, keyed by ISO 639-1 code (decided 2 October 2026, Chinmay, batch 2 #26, BO-044: "Yes, where a country … |
| Kind | chip: Shop, Restaurant, Bar, Cafe, Kiosk, Game floor… | — |
| Outlet type | chip: Fine dining, Casual dining, Quick service, Coffee shop, Bar lounge, Food court… | The service model (DI-319; DEC-196; CHG-CSP-005). Null on an outlet that is not F&B or retail. |
| Zone | text | — |
| Produces for outlets | list or chips (count when long) | One kitchen serving several outlets is a producing outlet (decided 2 October 2026, Chinmay, batch 6 set 5, BO-134: "Yes: via a producing … |
| Sale board | the name it points at, never the id | The till layout every till in this outlet uses, unless a till overrides it (decided 2 October 2026, Chinmay, batch 6 set 4, BO-109: "Per … |

**The F&B delivery policy** (detail panel, from `getFnbDeliveryPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Collection enabled | yes / no (icon or chip) | — |
| Delivery enabled | yes / no (icon or chip) | — |
| Collection hold minutes | 1,234 | — |
| Asap collection minutes | 1,234 | — |
| Asap delivery minutes | 1,234 | — |
| Slot minutes | 1,234 | — |
| Delivery fee | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Emirates served | list or chips (count when long) | — |

**The return policy** (detail panel, from `getReturnPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Default window days | 1,234 | — |
| Requires receipt | yes / no (icon or chip) | — |
| Allow cash refund on card sale | yes / no (icon or chip) | — |
| Self authorise limit | AED 1,234.50 | Up to this, one cashier may accept a return alone. |
| Requires second user above | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Requires approval above | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Restockable conditions | list or chips (count when long) | Conditions that return stock to sale. Everything else is written off. |

**The table map** (detail panel, from `getTableMap`)

| Shows | Format | Notes |
|---|---|---|
| Outlet | the name it points at, never the id | — |
| Zones | list or chips (count when long) | — |
| Tables | list or chips (count when long) | — |

**Haccp status** (detail panel, from `getHaccpStatus`): Shows `checksDue`, `checksMissed`, `openActions`, `unsignedActions`, `oldestOpenActionAgeHours`, `lastInspectionAt` from `getHaccpStatus`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.

| Shows | Format | Notes |
|---|---|---|
| Checks due | 1,234 | — |
| Checks missed | 1,234 | — |
| Open actions | 1,234 | — |
| Unsigned actions | 1,234 | — |
| Oldest open action age hours | 1,234 | — |
| Last inspection at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create outlet (primary button) | `createOutlet` POST `/outlets` | Outlet | Outlet | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Code already in use in this venue | opens modal first |
| Save return policy (secondary button) | `setReturnPolicy` PUT `/outlets/{outletId}/return-policy` | ReturnPolicy | ReturnPolicy | — | opens modal first |
| Save table layout (secondary button) | `setTableLayout` PUT `/outlets/{outletId}/tables` | inline | TableMap | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |
| Save outlet (secondary button) | `updateOutlet` PATCH `/outlets/{outletId}` | inline | Outlet | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Sign corrective action (secondary button) | `signCorrectiveAction` POST `/food-safety/corrective-actions/{actionId}/sign` | inline | CorrectiveAction | 409 A critical finding signed by the principal who raised it (`CorrectiveAction.raisedByPrincipalId`). | opens modal first |
| Save F&B delivery policy (secondary button) | `setFnbDeliveryPolicy` PUT `/fnb-delivery-policy` | FnbDeliveryPolicy | FnbDeliveryPolicy | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Outlet list**: Name, code, kind, zone, Trading now (from opening hours against now in GST), Active, and for F&B the unsigned food-safety actions count — the number that matters before service. *(source: F28 step 6 / contracts/spine/tenancy.yaml#listOutlets)*
- **Outlet detail**: Sections Overview, Opening hours, Ordering & delivery, Floor plan (table service), Returns (shops), Food safety. *(source: DI-330 / screens/P08-venue-back-office.yaml#BO-044)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Create outlet**: Adds the outlet (venue from the session); 409 names the duplicate code. *(source: contracts/spine/tenancy.yaml#createOutlet)*
- **Save delivery policy**: Replaces the outlet's policy; 412 when someone else saved first — re-read and show the difference. *(source: contracts/satellite/fnb.yaml#setFnbDeliveryPolicy)*
- **Sign corrective action**: Requires what was done (and disposal where food was discarded); the unsigned count drops. *(source: contracts/satellite/fnb.yaml#signCorrectiveAction / F28 step 6)*

**Data it reads**: `getFnbDeliveryPolicy` (onLoad, Takeaway and delivery rules); `listOutlets` (onLoad, List outlets); `getHaccpStatus` (onLoad, getHaccpStatus)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The outlets list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the outlets untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No outlets yet. Offers Create outlet (`createOutlet`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, kind and the outlets are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | You don't have access to outlets — ask your venue manager. Permission keys are never shown to the user; the screen names the access in words. **Never an empty table** — that reads as *there is no data*. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A critical finding signed by the principal who raised it (`CorrectiveAction.raisedByPrincipalId`).; 409 Code already in use in this venue; 409 The venue has no food-safety lead named in `fnb.foodSafetyLeadPrincipalId` (audit R096 (9)). |

#### Edge cases to draw

- **Outlet made inactive while orders are live**: Allowed, with a warning that names the live orders; the guest dining list stops showing the outlet. *(source: contracts/satellite/fnb.yaml#listDiningOutlets / decided 2 October 2026 by Chinmay (CHG-NOTE-004))*
- **Food-safety escalation with no food-safety lead set**: Refused "no food-safety lead"; link to Venue Configuration where the lead is set. *(source: contracts/spine/tenancy.yaml#getVenueSettings / R096)*

#### Consistency with other screens

- Match `BO-728`: The client pack's Outlet Management is the same register; one design, not two.
- Match `BO-729`: Create / Edit Outlet in the pack is this screen's form.
- Match `BO-065`: Delivery locations and which outlets serve them are venue-level there.
- Match `POS-028`: The till's floor plan reads the layout drawn here.
- Match `WEB-036`: Guests see the delivery rules set here (minimum order, fee, ASAP times).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
outlets:
- name: Oasis Bistro
  code: OAS-BIS
  kind: Restaurant
  zone: Lagoon
  trading_now: Open — dinner service 18:00–23:00
  unsigned_food_safety: 0
- name: Bite & Go
  code: BTG-01
  kind: Kiosk
  zone: Aqua Park
  trading_now: Open
  unsigned_food_safety: 2
- name: Pool Bar
  code: PLB-01
  kind: Bar
  zone: Wave Pool
  delivery: Cabanas 1–24, ASAP 15 min
- name: Marina Bay retail store
  code: MBR-01
  kind: Shop
  returns: 14 days, receipt required
```

#### Permissions

- `getFnbDeliveryPolicy` → `PRODUCT_VIEW` (read) · staff, guest
- `setFnbDeliveryPolicy` → `PRODUCT_CONFIGURE` (configure) · staff
- `listOutlets` → `SCOPE_VIEW` (read) · staff
- `createOutlet` → `REGION_CONFIGURE` (configure) · staff
- `getReturnPolicy` → `ORDER_VIEW` (read) · staff
- `getTableMap` → `ORDER_VIEW` (read) · staff
- `setReturnPolicy` → `REGION_CONFIGURE` (configure) · staff
- `setTableLayout` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateOutlet` → `REGION_CONFIGURE` (configure) · staff
- `getHaccpStatus` → `INCIDENT_VIEW` (read) · staff
- `signCorrectiveAction` → `INCIDENT_MANAGE` (configure) · staff
- `recordCorrectiveAction` → `INCIDENT_MANAGE` (configure) · staff
- `escalateCorrectiveAction` → `INCIDENT_MANAGE` (configure) · staff
- `closeCorrectiveAction` → `INCIDENT_MANAGE` (configure) · staff
- `setDeliveryLocationOutletMapping` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** You don't have access to outlets — ask your venue manager. Permission keys are never shown to the user; the screen names the access in words. **Never an empty table** — that reads as *there is no data*.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.1.1 | The system should be able to allow table reservations view for the available tables in real-time, for the guests to choose/request. | F&B & Guest Management | CONTRACTED | `getTableMap` |
| 4.9.6 | The system should be able to create, modify, delete a restaurant floor plan. | Bundles and Promotions | CONTRACTED | `setTableLayout` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-044` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 1.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 1.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `FnB Board 1.dc.html#fnb-1b`, `FnB Board 1.dc.html#fnb-1c`, `FnB Board 1.dc.html#fnb-1d`, `FnB Board 1.dc.html#fnb-1e`, `FnB Board 1.dc.html#fnb-1f`, `FnB Board 1.dc.html#fnb-1g`
- Flow F28 *A temperature excursion is caught and signed off*, step 6: The venue manager reviews open and unsigned findings before service. → **Unsigned actions are the number that matters on this screen.** A year of unsigned entries is what an inspection finds, and nobody notices until then.

#### Acceptance for the design

- [ ] Every input above is drawn (72), with its required mark, default, format and its error state (400, 403, 404, 409, 412, 422).
- [ ] Every output is drawn (38 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-044?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create outlet, Save return policy, Save table layout, Save outlet, Sign corrective action, Save F&B delivery policy.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `INCIDENT_MANAGE`, `INCIDENT_VIEW`, `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `REGION_CONFIGURE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-058` Reporting Home

**Find the report rather than build it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 1 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_SCHEDULE`, `REPORT_VIEW_VENUE` (1 configure, 2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listReports` reads the population and `getFinancialReport` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `conversationId` (deepLink), `reportId` (deepLink) · cold entry: A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. |
| Route | `/venue-operations/reporting-home` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Retail board operations wired 24 August.** **Cross-platform navigation removed 24 August**: EMP-020. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **One reporting area, one set of numbers** (decided 2 October 2026, Chinmay; CHG-FIN-006; DI-721, DI-702). This screen is a scoped window onto the reporting area (Analytics, P16): it runs the same seeded report definitions and reads the same seeded KPIs, so its figures equal what Analytics shows for the same scope, period and as-of time. It computes no total of its own and shows the as-of time on every figure.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The report library: find the report rather than build it, run it with its prompts, see recent runs, and schedule it to people. The standard reports (end-of-day, sales by channel, payment summary, shift, refunds, voids and discounts, attendance) come seeded; custom ones appear beside them. The one thing to get right: a person only sees reports they may run, and a report never shows data outside their scope whatever its filters say.

**Known correction pending (do not draw the wrong version)**

- **BO-058 and BO-059 declare almost the same operations, including authoring and P&L.** Why: The 28 September duplicate-screens decision listed this pair but settled others only; the library and the sales report need distinct jobs. *(source: R276 / screens/P08-venue-back-office.yaml#BO-059; Finance, Ledger & Tax · Reporting & Analytics)*
- **The report library loads a P&L.** Why: Statutory statements are one report in the library, not part of it on load. *(source: screens/P08-venue-back-office.yaml#BO-058; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Category | select | optional | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | — | Sends `?category=` to `listReports`. | `listReports` ?category |
| Search | text field | optional | — | — | — | Sends `?search=` to `listReports`. | `listReports` ?search |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Report | select | — | Profit and loss · Balance sheet · Cash flow · Revenue by venue · Revenue by product · Tax summary | `getFinancialReport` ?report |
| Fiscal period | picker: choose a fiscal period | — | — | `getFinancialReport` ?fiscalPeriodId |
| Legal entity | picker: choose a legal entity | — | — | `getFinancialReport` ?legalEntityId |
| Cost center | picker: choose a cost center | — | — | `getFinancialReport` ?costCenterId |
| Report | picker: choose a report | — | — | `listReportExecutions` ?reportId |
| Status | select | — | Queued · Running · Completed · Failed · Cancelled · Expired | `listReportExecutions` ?status |
| Mine only | toggle | on | — | `listReportExecutions` ?mineOnly |

**Form: Run report** (modal, opened by *Run report*; *Run report* calls `runReport`, *Cancel* sends nothing)

**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Parameters `parameters` | key and value settings | optional | — | — | — | Open on purpose; its shape is the report's. Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. | `runReport` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | `runReport` body |
| Date from `dateFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158). | `runReport` body |
| Date to `dateTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (audit R158). | `runReport` body |
| Force async `forceAsync` | toggle | optional | off | — | — | Queue regardless of size, for a result to be collected later. | `runReport` body |

Errors to draw in the form: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope

**Form: Ask reporting question** (modal, opened by *Ask reporting question*; *Ask reporting question* calls `askReportingQuestion`, *Cancel* sends nothing)

**Collects what `askReportingQuestion` sends before it is called.** Required: `question`. Optional: `conversationId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Question `question` | text area | required | — | min length 3; max length 1000 | — | — | `askReportingQuestion` body |
| Conversation `conversationId` | text field | optional | — | — | — | Continue a prior exchange for follow-up questions. | `askReportingQuestion` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows the answer to one venue. Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | `askReportingQuestion` body |

Errors to draw in the form: 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope

**Form: Create report** (modal, opened by *Create report*; *Create report* calls `createReport`, *Cancel* sends nothing)

**Collects what `createReport` sends before it is called.** Required: `name`, `category`, `dataSource`, `columns`, `requiredPermission`. Optional: `description`, `filters`, `groupBy`, `parameters`, `maxDateRangeDays`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createReport` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `createReport` body |
| Category `category` | select | required | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | — | — | `createReport` body |
| Data source `dataSource` | select | required | — | Orders · Order lines · Payments · Refunds · Shifts · Scan events · Entitlements · Products · Inventory · Stock movements · Stock counts · Waste … | — | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over data nobody maintains. | `createReport` body |
| Columns `columns` | repeatable rows | required | — | at least 1 | — | — | `createReport` body |
| Field `columns[].field` | text field | required | — | — | — | — | `createReport` body |
| Label `columns[].label` | text field | optional | — | — | — | — | `createReport` body |
| Aggregation `columns[].aggregation` | select | optional | None | None · Count · Count distinct · Sum · Average · Min · Max | — | — | `createReport` body |
| Sort order `columns[].sortOrder` | number field | optional | — | — | — | — | `createReport` body |
| Sort direction `columns[].sortDirection` | segmented control | optional | — | Asc · Desc | — | — | `createReport` body |
| Format `columns[].format` | text field | optional | — | — | — | — | `createReport` body |
| Role `columns[].role` | segmented control | optional | — | Dimension · Measure | — | What the column is to a chart (decided 2 October 2026, Chinmay; CHG-FIN-007). A `dimension` groups (date, venue, channel, product); a `measure` is aggregated (sum of net revenue … | `createReport` body |
| Encoding `columns[].encoding` | select | optional | — | Category · X · Y · Series · Value · Size · Colour · Location · Stage · Source · Target · Row … | — | Which field well the column fills (CHG-FIN-007), the binding the twenty marks of `DashboardTile.visualisation` need. | `createReport` body |
| Axis `columns[].axis` | segmented control | optional | — | Primary · Secondary | — | For a measure on a `combo`, the axis it is drawn against. A secondary axis needs its own `unitLabel` (CHG-FIN-007). | `createReport` body |
| Series type `columns[].seriesType` | segmented control | optional | — | Bar · Line · Area | — | For a measure on a `combo`, how that series is drawn (CHG-FIN-007). | `createReport` body |
| Hierarchy level `columns[].hierarchyLevel` | number field | optional | — | min 1 | — | For `matrix` rows and columns, `treemap` nesting and `decompositionTree` levels, the depth of this dimension, 1 outermost. | `createReport` body |
| Unit label `columns[].unitLabel` | text field | optional | — | max length 40 | — | The unit an axis states, for example "AED" or "Admissions". Required on a secondary axis (CHG-FIN-007). | `createReport` body |
| Filters `filters` | repeatable rows | optional | — | — | — | — | `createReport` body |
| Field `filters[].field` | text field | required | — | — | — | — | `createReport` body |
| Operator `filters[].operator` | select | required | — | Equals · Not equals · Greater than · Less than · Between · In · Not in · Contains · Is null · Is not null | — | — | `createReport` body |
| Value `filters[].value` | field | optional | — | — | — | Open on purpose; its type is the field's. One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a … | `createReport` body |
| Values `filters[].values` | list of values (chips) | optional | — | — | — | The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`. | `createReport` body |
| Is parameter `filters[].isParameter` | toggle | optional | off | — | — | Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope. | `createReport` body |
| Group by `groupBy` | list of values (chips) | optional | — | — | — | — | `createReport` body |
| Parameters `parameters` | repeatable rows | optional | — | — | — | — | `createReport` body |
| Key `parameters[].key` | text field | required | — | — | — | — | `createReport` body |
| Label `parameters[].label` | text field | required | — | — | — | — | `createReport` body |
| Type `parameters[].type` | select | required | — | String · Integer · Decimal · Money · Boolean · Date · Date time · Uuid · Enum | — | — | `createReport` body |
| Is required `parameters[].isRequired` | toggle | required | — | — | — | — | `createReport` body |
| Default value `parameters[].defaultValue` | field | optional | — | — | — | Open on purpose. A value of this parameter's `type`, used when a run supplies none. | `createReport` body |
| Required permission `requiredPermission` | select | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE … | — | Permission needed to run this report, from the shared `Permission` vocabulary. The author cannot assign one they do not hold — otherwise a venue user could build themselves a … | `createReport` body |
| Max date range days `maxDateRangeDays` | number field (days) | optional | 366 | min 1 | — | Guards against a query spanning years of scan events. When a report sets none, 366 days applies (decided 28 September, audit R158), so `runReport`'s date-range 400 always has a … | `createReport` body |

Errors to draw in the form: 400 Unknown field, invalid filter, or estimated cost beyond the limit; 403 Author does not hold the permission they assigned to the report

**Form: Save natural language query** (modal, opened by *Save natural language query*; *Save natural language query* calls `saveNaturalLanguageQuery`, *Cancel* sends nothing)

**Collects what `saveNaturalLanguageQuery` sends before it is called.** Required: `name`. Optional: `category`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `saveNaturalLanguageQuery` body |
| Category `category` | select | optional | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | — | — | `saveNaturalLanguageQuery` body |

**Form: Save report** (modal, opened by *Save report*; *Save report* calls `updateReport`, *Cancel* sends nothing)

**Collects what `updateReport` sends before it is called.** Required: `name`, `category`, `dataSource`, `columns`, `requiredPermission`. Optional: `description`, `filters`, `groupBy`, `parameters`, `maxDateRangeDays`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `updateReport` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `updateReport` body |
| Category `category` | select | required | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | — | — | `updateReport` body |
| Data source `dataSource` | select | required | — | Orders · Order lines · Payments · Refunds · Shifts · Scan events · Entitlements · Products · Inventory · Stock movements · Stock counts · Waste … | — | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over data nobody maintains. | `updateReport` body |
| Columns `columns` | repeatable rows | required | — | at least 1 | — | — | `updateReport` body |
| Field `columns[].field` | text field | required | — | — | — | — | `updateReport` body |
| Label `columns[].label` | text field | optional | — | — | — | — | `updateReport` body |
| Aggregation `columns[].aggregation` | select | optional | None | None · Count · Count distinct · Sum · Average · Min · Max | — | — | `updateReport` body |
| Sort order `columns[].sortOrder` | number field | optional | — | — | — | — | `updateReport` body |
| Sort direction `columns[].sortDirection` | segmented control | optional | — | Asc · Desc | — | — | `updateReport` body |
| Format `columns[].format` | text field | optional | — | — | — | — | `updateReport` body |
| Role `columns[].role` | segmented control | optional | — | Dimension · Measure | — | What the column is to a chart (decided 2 October 2026, Chinmay; CHG-FIN-007). A `dimension` groups (date, venue, channel, product); a `measure` is aggregated (sum of net revenue … | `updateReport` body |
| Encoding `columns[].encoding` | select | optional | — | Category · X · Y · Series · Value · Size · Colour · Location · Stage · Source · Target · Row … | — | Which field well the column fills (CHG-FIN-007), the binding the twenty marks of `DashboardTile.visualisation` need. | `updateReport` body |
| Axis `columns[].axis` | segmented control | optional | — | Primary · Secondary | — | For a measure on a `combo`, the axis it is drawn against. A secondary axis needs its own `unitLabel` (CHG-FIN-007). | `updateReport` body |
| Series type `columns[].seriesType` | segmented control | optional | — | Bar · Line · Area | — | For a measure on a `combo`, how that series is drawn (CHG-FIN-007). | `updateReport` body |
| Hierarchy level `columns[].hierarchyLevel` | number field | optional | — | min 1 | — | For `matrix` rows and columns, `treemap` nesting and `decompositionTree` levels, the depth of this dimension, 1 outermost. | `updateReport` body |
| Unit label `columns[].unitLabel` | text field | optional | — | max length 40 | — | The unit an axis states, for example "AED" or "Admissions". Required on a secondary axis (CHG-FIN-007). | `updateReport` body |
| Filters `filters` | repeatable rows | optional | — | — | — | — | `updateReport` body |
| Field `filters[].field` | text field | required | — | — | — | — | `updateReport` body |
| Operator `filters[].operator` | select | required | — | Equals · Not equals · Greater than · Less than · Between · In · Not in · Contains · Is null · Is not null | — | — | `updateReport` body |
| Value `filters[].value` | field | optional | — | — | — | Open on purpose; its type is the field's. One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a … | `updateReport` body |
| Values `filters[].values` | list of values (chips) | optional | — | — | — | The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`. | `updateReport` body |
| Is parameter `filters[].isParameter` | toggle | optional | off | — | — | Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope. | `updateReport` body |
| Group by `groupBy` | list of values (chips) | optional | — | — | — | — | `updateReport` body |
| Parameters `parameters` | repeatable rows | optional | — | — | — | — | `updateReport` body |
| Key `parameters[].key` | text field | required | — | — | — | — | `updateReport` body |
| Label `parameters[].label` | text field | required | — | — | — | — | `updateReport` body |
| Type `parameters[].type` | select | required | — | String · Integer · Decimal · Money · Boolean · Date · Date time · Uuid · Enum | — | — | `updateReport` body |
| Is required `parameters[].isRequired` | toggle | required | — | — | — | — | `updateReport` body |
| Default value `parameters[].defaultValue` | field | optional | — | — | — | Open on purpose. A value of this parameter's `type`, used when a run supplies none. | `updateReport` body |
| Required permission `requiredPermission` | select | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE … | — | Permission needed to run this report, from the shared `Permission` vocabulary. The author cannot assign one they do not hold — otherwise a venue user could build themselves a … | `updateReport` body |
| Max date range days `maxDateRangeDays` | number field (days) | optional | 366 | min 1 | — | Guards against a query spanning years of scan events. When a report sets none, 366 days applies (decided 28 September, audit R158), so `runReport`'s date-range 400 always has a … | `updateReport` body |

Errors to draw in the form: 409 The report is a system report, which is clone-only (audit R096).

**Form: Create report schedule** (modal, opened by *Create report schedule*; *Create report schedule* calls `createReportSchedule`, *Cancel* sends nothing)

**Collects what `createReportSchedule` sends before it is called.** Required: `reportId`, `cadence`, `recipients`, `format`. Optional: `name`, `parameters`, `includePersonalData`, `skipIfEmpty`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Report `reportId` | picker: choose a report | required | — | — | shows names, sends the id | — | `createReportSchedule` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `createReportSchedule` body |
| Cadence `cadence` | group | required | — | — | — | What each frequency needs (decided 28 September, audit R158). `daily`: `timeOfDay`. | `createReportSchedule` body |
| Frequency `cadence.frequency` | select | required | — | Daily · Weekly · Monthly · Quarterly · On shift close · On period close | — | — | `createReportSchedule` body |
| Day of week `cadence.dayOfWeek` | stepper or slider | optional | — | min 0; max 6 | — | — | `createReportSchedule` body |
| Day of month `cadence.dayOfMonth` | stepper or slider | optional | — | min 1; max 31 | — | — | `createReportSchedule` body |
| Time of day `cadence.timeOfDay` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | — | `createReportSchedule` body |
| Parameters `parameters` | key and value settings | optional | — | — | — | As `RunReportRequest.parameters` — keyed by the report's `ReportParameter.key`, applied to every run. | `createReportSchedule` body |
| Recipients `recipients` | repeatable rows | required | — | at least 1 | — | — | `createReportSchedule` body |
| Kind `recipients[].kind` | radio group | required | — | Principal · Email · Sftp · Webhook | — | — | `createReportSchedule` body |
| Address `recipients[].address` | text field | required | — | — | — | — | `createReportSchedule` body |
| Principal `recipients[].principalId` | picker: choose a principal | optional | — | — | shows names, sends the id | — | `createReportSchedule` body |
| Format `format` | radio group | required | — | Csv · Xlsx · Pdf · Json | — | — | `createReportSchedule` body |
| Include personal data `includePersonalData` | toggle | optional | off | — | — | — | `createReportSchedule` body |
| Skip if empty `skipIfEmpty` | toggle | optional | on | — | — | An empty report every morning trains people to ignore the report. | `createReportSchedule` body |

Errors to draw in the form: 400 Invalid cadence (a field its frequency needs is missing, or one it does not take is sent, audit R158), or no recipients

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Search and category**: Category is a pick list of report categories, not free text. *(source: contracts/satellite/reporting.yaml#/components/schemas/ReportCategory)*
- **Run prompts**: Date range within the report's maximum, and the report's own prompts: site, operating area, sales channel, workstation, user. *(source: DI-183 / DI-151 / MATRIX 6.1.19)*
- **Schedule**: Cadence (e.g. daily 07:00 region time), recipients or recipient groups, format (PDF, Excel, CSV), include personal data (only for holders of the personal-data export right), skip if empty. The schedule runs with the owner's permissions. *(source: contracts/satellite/reporting.yaml#createReportSchedule / DI-714 / contracts/shared/permissions.yaml#/components/schemas/Permission)*

#### Outputs: what the screen shows and produces

**Shown**

**Every report definition** (data table, from `listReports`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Category | chip: Sales, Admission, Financial, Inventory, Guest, Operations… | — |
| Max date range days | 1,234 | Guards against a query spanning years of scan events. When a report sets none, 366 days applies (decided 28 September, audit R158), so … |
| Is system | yes / no (icon or chip) | Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). Clone-only (decided 28 September, audit R096): `updateReport` … |

**Every report execution** (data table, from `listReportExecutions`)

| Shows | Format | Notes |
|---|---|---|
| Report name | text | — |
| Definition version | text | The version this ran against. With the parameters and scope below, it is everything needed to reproduce the result. |
| Status | chip: Queued, Running, Completed, Failed, Cancelled, Expired | — |
| Row count | 1,234 | — |
| Duration ms | 1,234 | — |
| Error | text | — |

**The selected report definition** (detail panel, from `getReport`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Category | chip: Sales, Admission, Financial, Inventory, Guest, Operations… | — |
| Data source | chip: Orders, Order lines, Payments, Refunds, Shifts, Scan events… | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over … |
| Columns | list or chips (count when long) | — |
| Filters | list or chips (count when long) | — |
| Estimated cost | chip: Low, Medium, High | Informs whether it may run inline or must be queued. |
| Last run at | 1 Oct 2026, 14:30 | — |

**The financial report** (detail panel, from `getFinancialReport`)

| Shows | Format | Notes |
|---|---|---|
| Report | chip: Profit and loss, Balance sheet, Cash flow, Revenue by venue, Revenue by product … | The report `getFinancialReport` returns. One vocabulary for the query and the response. |
| Fiscal period | the name it points at, never the id | — |
| Legal entity | the name it points at, never the id | — |
| Currency | text | — |
| Currency scale | 1,234 | — |
| Generated at | 1 Oct 2026, 14:30 | — |
| Sections | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Run report (primary button) | `runReport` POST `/reports/{reportId}/run` | RunReportRequest | ReportResult | 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope | opens modal first |
| Ask reporting question (secondary button) | `askReportingQuestion` POST `/reports/ask` | inline | NaturalLanguageAnswer | 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope | opens modal first |
| Create report (secondary button) | `createReport` POST `/reports` | CreateReportRequest | ReportDefinition | 400 Unknown field, invalid filter, or estimated cost beyond the limit; 403 Author does not hold the permission they assigned to the report | opens modal first |
| Delete report (destructive button) | `deleteReport` DELETE `/reports/{reportId}` | — | — | 409 Active schedules reference this report (`report-scheduled`), or it is a system report, which is clone-only (`system-report`, audit R096) | — |
| Save natural language query (secondary button) | `saveNaturalLanguageQuery` POST `/reports/ask/{conversationId}/save` | inline | ReportDefinition | — | opens modal first |
| Save report (secondary button) | `updateReport` PUT `/reports/{reportId}` | CreateReportRequest | ReportDefinition | 409 The report is a system report, which is clone-only (audit R096). | opens modal first |
| Create report schedule (secondary button) | `createReportSchedule` POST `/report-schedules` | CreateReportScheduleRequest | ReportSchedule | 400 Invalid cadence (a field its frequency needs is missing, or one it does not take is sent, audit R158), or no recipients | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Library**: Seeded reports marked "Standard"; each row shows what it answers, last run and its owner. *(source: R282 / contracts/satellite/reporting.yaml#listSeededReports)*
- **Recent runs**: Status (queued, running, done, failed), parameters used, who ran it, file links; large runs finish in the background. *(source: contracts/satellite/reporting.yaml#listReportExecutions)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Run**: Opens the result; very large results run in the background and notify. *(source: contracts/satellite/reporting.yaml#runReport / DI-710)*
- **Schedule**: Creates the schedule; the first delivery time is shown. *(source: contracts/satellite/reporting.yaml#createReportSchedule)*
- **Ask**: A plain-language answer with its sources; "Save as report" adds it to the library. *(source: F20 step 1 / F20 step 3)*

**Data it reads**: `listReports` (onLoad, List available report definitions); `getFinancialReport` (onLoad, P&L, balance sheet or cash flow); `listReportExecutions` (onLoad, List executions)

**Where the user goes next**

- → `BO-061` Scheduled Reports: *It is scheduled to the people who need it*; carries `reportId`, `scheduleId`
- → `EMP-020` AI assistant — answer: *The answer arrives with its sources*; carries `conversationId`

**What opens over it**

- confirmDialog *Delete report*: **Names what `deleteReport` changes and what it leaves alone**, in the consequence rather than the verb. A reporting home this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reporting home list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reporting home untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reporting home yet. Offers Create report (`createReport`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on category, search and the reporting home are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listReports` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `REPORT_MANAGE` for `createReport`, `deleteReport`, `saveNaturalLanguageQuery`, `updateReport`; `REPORT_SCHEDULE` for `createReportSchedule`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Invalid cadence (a field its frequency needs is missing, or one it does not take is sent, audit R158), or no recipients; 400 Question could not be interpreted. (ReportQuestionProblem); 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 400 Unknown field, invalid filter, or estimated cost beyond the limit |

#### Edge cases to draw

- **Reports older than the live window**: Archived transactions are still retrievable; a run over them may take longer and says so. *(source: DI-018)*
- **Arabic users**: Reports render right-to-left in Arabic with the same numbers. *(source: DI-019 / MATRIX 6.1.78)*

#### Consistency with other screens

- Match `ANL-031`: One report catalogue; this is the venue view of the same library (DI-721).
- Match `BO-059`: Sales reports open from here filtered; they are not a second library.
- Match `BO-061`: Scheduled reports are managed there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
reports:
- Standard · End of day consolidated · last run today 06:00 by schedule
- Standard · Payment summary by cashier
- Standard · Sales by channel
- Custom · Cabana bookings by weekday · owner Omar Haddad
schedule: Daily closing summary · every day 07:00 · PDF · Finance team, Operations managers
```

#### Permissions

- `listReports` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `createReport` → `REPORT_MANAGE` (configure) · staff, partner
- `deleteReport` → `REPORT_MANAGE` (configure) · staff, partner
- `getFinancialReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `getReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `saveNaturalLanguageQuery` → `REPORT_MANAGE` (configure) · staff, partner
- `updateReport` → `REPORT_MANAGE` (configure) · staff, partner
- `createReportSchedule` → `REPORT_SCHEDULE` (operate) · staff
- `listReportExecutions` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listReports` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `REPORT_MANAGE` for `createReport`, `deleteReport`, `saveNaturalLanguageQuery`, `updateReport`; `REPORT_SCHEDULE` for `createReportSchedule`.

#### Requirements it meets

100 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 13.3.14 | APIs shall expose operational, financial, attendance, membership and sales reporting data. | Developer & API Management | CONTRACTED | `runReport` |
| 8.7.30 | System shall support natural language reporting. | Unified Operations Dashboard | CONTRACTED | `askReportingQuestion` |
| 1.1.40 | System shall provide analytics and dashboards covering ticket sales, attendance, utilization, conversion rates, capacity utilization and revenue performance. | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.104 | Membership analytics | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.135 | Required Reports Operational Reports Donations by Campaign. Donations by Site. Donations by Product. Donations by Sales Channel. Donations by Date. Donations by User/Cashier. Donations by Payment … | Ticketing Catalogue | CONTRACTED | `createReport` |
| 3.2.65 | An Entry or Exit report is expected presenting the readings per outcome (ok/ko), per time and per access point. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.66 | The in park report showing the difference between the Entries and the Exits. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.68 | The length of stay report shall present the difference between the time in scan and the time out scan. | Admission and Access | CONTRACTED | `createReport` |
| … 88 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Report library filterable by site, operating area, sales channel, workstation or user; e.g. Sales Report (payment-method breakdown, totals, voids, deposits, itemised ticket sales) and Payment Summary (per-cashier breakdown). *(agreed · MoM 7 Aug 2026, 21. Dashboards & Reporting · DI-183)*
- Sales reporting can be scoped to an operating area, showing all transactions from its workstations. *(agreed · MoM 7 Aug 2026, 3. Operating Areas, Workstations & Permissions Hierarchy · DI-151)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-058` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 6.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 6.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 6.dc.html#ret-6h`
- Flow F107 *A report is defined, scheduled and delivered*, step 1: The report is defined. → Built once and run to check it shows the right numbers.
- Flow F20 *A manager asks a question and gets an answer*, step 1: Asks in plain language → Grounded in the tenant’s own data
- Flow F20 *A manager asks a question and gets an answer*, step 3: Saves it as a report → A one-off question becomes schedulable
- Flow F82 *A month is analysed from incrementality to a scheduled report*, step 5: Reporting Home. → **Drawn by the client as RET-6H.** 7 operations on this step.
- Flow F107 branch at step 1 (medium): when The acting principal lacks the permission at this scope., **Refused at the first step, not the last.** ADR-0002 makes authorisation user-driven — a person who gets three steps in and then cannot finish has been told the wrong thing.
- Flow F20 branch at step 1 (recoverable): when The question needs data the manager may not see, **Retrieval runs as the caller.** The assistant sees exactly what that person could read directly, so the answer is narrower rather than refused.
- Flow F20 branch at step 1 (recoverable): when The question contains guest personal data, Masked before the prompt leaves the platform. **The masking list fails closed** — an unset list sends nothing rather than everything.
- Flow F20 branch at step 3 (recoverable): when The saved report returns different numbers tomorrow, Expected. It runs against the analytical replica and the data moved. **The generated query is saved, not the answer**, which is why the query is returned in the first place.
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)
- ADR-0059 *AI phasing against the six-month plan* (`docs/adr/0059-ai-phasing-against-the-six-month-plan.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (91), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-058?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Run report, Ask reporting question, Create report, Delete report, Save natural language query, Save report, Create report schedule.
- [ ] Every transition is wired: `BO-061`, `EMP-020`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_SCHEDULE`, `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-060` Attendance & Footfall

**See how many people actually came in.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 2 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_MANAGE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP` (4 operate, 1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listScans` reads the population and `getFinancialReport` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `conversationId` (deepLink), `reportId` (deepLink) · cold entry: A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. |
| Route | `/venue-operations/attendance-footfall` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **One reporting area, one set of numbers** (decided 2 October 2026, Chinmay; CHG-FIN-006; DI-721, DI-702). This screen is a scoped window onto the reporting area (Analytics, P16): it runs the same seeded report definitions and reads the same seeded KPIs, so its figures equal what Analytics shows for the same scope, period and as-of time. It computes no total of its own and shows the as-of time on every figure.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** How many people actually came in: admissions by hour and by entry point against capacity, a live headcount of who is inside, and the group breakdown (general admission, group, re-entry). The one thing to get right: this is a report screen; it admits nobody and changes no gate.

**Known correction pending (do not draw the wrong version)**

- **Gate operations (validate access, group admit, override, sync scans, offline package) and a scan target are on this report screen.** Why: Admitting or overriding a guest is a scanner's job (P07); a back-office report must not admit anyone. *(source: screens/P08-venue-back-office.yaml#BO-060; Finance, Ledger & Tax · Reporting & Analytics)*
- **Report authoring and a P&L load are on this screen.** Why: Same as BO-059. *(source: screens/P08-venue-back-office.yaml#BO-060; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Access point id | picker: choose an access point (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?accessPointId=` to `listScans`. | `listScans` ?accessPointId |
| Ticket id | picker: choose a ticket (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?ticketId=` to `listScans`. | `listScans` ?ticketId |
| Outcome | segmented control | optional | — | Admitted · Denied · Overridden | — | Sends `?outcome=` to `listScans`. | `listScans` ?outcome |
| Recorded from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedFrom=` to `listScans`. | `listScans` ?recordedFrom |
| Recorded to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedTo=` to `listScans`. | `listScans` ?recordedTo |
|  | scan target | — | — | — | — | **A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or … | — |
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Report | select | — | Profit and loss · Balance sheet · Cash flow · Revenue by venue · Revenue by product · Tax summary | `getFinancialReport` ?report |
| Fiscal period | picker: choose a fiscal period | — | — | `getFinancialReport` ?fiscalPeriodId |
| Legal entity | picker: choose a legal entity | — | — | `getFinancialReport` ?legalEntityId |
| Cost center | picker: choose a cost center | — | — | `getFinancialReport` ?costCenterId |
| Since version | number field | — | — | `getOfflinePackage` ?sinceVersion |
| Valid from | date and time picker | — | — | `getOfflinePackage` ?validFrom |
| Valid to | date and time picker | — | — | `getOfflinePackage` ?validTo |
| Category | select | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | `listReports` ?category |
| Search | text field | — | — | `listReports` ?search |

**Form: Run report** (modal, opened by *Run report*; *Run report* calls `runReport`, *Cancel* sends nothing)

**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Parameters `parameters` | key and value settings | optional | — | — | — | Open on purpose; its shape is the report's. Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. | `runReport` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | `runReport` body |
| Date from `dateFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158). | `runReport` body |
| Date to `dateTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (audit R158). | `runReport` body |
| Force async `forceAsync` | toggle | optional | off | — | — | Queue regardless of size, for a result to be collected later. | `runReport` body |

Errors to draw in the form: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope

**Form: Ask reporting question** (modal, opened by *Ask reporting question*; *Ask reporting question* calls `askReportingQuestion`, *Cancel* sends nothing)

**Collects what `askReportingQuestion` sends before it is called.** Required: `question`. Optional: `conversationId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Question `question` | text area | required | — | min length 3; max length 1000 | — | — | `askReportingQuestion` body |
| Conversation `conversationId` | text field | optional | — | — | — | Continue a prior exchange for follow-up questions. | `askReportingQuestion` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows the answer to one venue. Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | `askReportingQuestion` body |

Errors to draw in the form: 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope

**Form: Create report** (modal, opened by *Create report*; *Create report* calls `createReport`, *Cancel* sends nothing)

**Collects what `createReport` sends before it is called.** Required: `name`, `category`, `dataSource`, `columns`, `requiredPermission`. Optional: `description`, `filters`, `groupBy`, `parameters`, `maxDateRangeDays`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createReport` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `createReport` body |
| Category `category` | select | required | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | — | — | `createReport` body |
| Data source `dataSource` | select | required | — | Orders · Order lines · Payments · Refunds · Shifts · Scan events · Entitlements · Products · Inventory · Stock movements · Stock counts · Waste … | — | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over data nobody maintains. | `createReport` body |
| Columns `columns` | repeatable rows | required | — | at least 1 | — | — | `createReport` body |
| Field `columns[].field` | text field | required | — | — | — | — | `createReport` body |
| Label `columns[].label` | text field | optional | — | — | — | — | `createReport` body |
| Aggregation `columns[].aggregation` | select | optional | None | None · Count · Count distinct · Sum · Average · Min · Max | — | — | `createReport` body |
| Sort order `columns[].sortOrder` | number field | optional | — | — | — | — | `createReport` body |
| Sort direction `columns[].sortDirection` | segmented control | optional | — | Asc · Desc | — | — | `createReport` body |
| Format `columns[].format` | text field | optional | — | — | — | — | `createReport` body |
| Role `columns[].role` | segmented control | optional | — | Dimension · Measure | — | What the column is to a chart (decided 2 October 2026, Chinmay; CHG-FIN-007). A `dimension` groups (date, venue, channel, product); a `measure` is aggregated (sum of net revenue … | `createReport` body |
| Encoding `columns[].encoding` | select | optional | — | Category · X · Y · Series · Value · Size · Colour · Location · Stage · Source · Target · Row … | — | Which field well the column fills (CHG-FIN-007), the binding the twenty marks of `DashboardTile.visualisation` need. | `createReport` body |
| Axis `columns[].axis` | segmented control | optional | — | Primary · Secondary | — | For a measure on a `combo`, the axis it is drawn against. A secondary axis needs its own `unitLabel` (CHG-FIN-007). | `createReport` body |
| Series type `columns[].seriesType` | segmented control | optional | — | Bar · Line · Area | — | For a measure on a `combo`, how that series is drawn (CHG-FIN-007). | `createReport` body |
| Hierarchy level `columns[].hierarchyLevel` | number field | optional | — | min 1 | — | For `matrix` rows and columns, `treemap` nesting and `decompositionTree` levels, the depth of this dimension, 1 outermost. | `createReport` body |
| Unit label `columns[].unitLabel` | text field | optional | — | max length 40 | — | The unit an axis states, for example "AED" or "Admissions". Required on a secondary axis (CHG-FIN-007). | `createReport` body |
| Filters `filters` | repeatable rows | optional | — | — | — | — | `createReport` body |
| Field `filters[].field` | text field | required | — | — | — | — | `createReport` body |
| Operator `filters[].operator` | select | required | — | Equals · Not equals · Greater than · Less than · Between · In · Not in · Contains · Is null · Is not null | — | — | `createReport` body |
| Value `filters[].value` | field | optional | — | — | — | Open on purpose; its type is the field's. One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a … | `createReport` body |
| Values `filters[].values` | list of values (chips) | optional | — | — | — | The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`. | `createReport` body |
| Is parameter `filters[].isParameter` | toggle | optional | off | — | — | Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope. | `createReport` body |
| Group by `groupBy` | list of values (chips) | optional | — | — | — | — | `createReport` body |
| Parameters `parameters` | repeatable rows | optional | — | — | — | — | `createReport` body |
| Key `parameters[].key` | text field | required | — | — | — | — | `createReport` body |
| Label `parameters[].label` | text field | required | — | — | — | — | `createReport` body |
| Type `parameters[].type` | select | required | — | String · Integer · Decimal · Money · Boolean · Date · Date time · Uuid · Enum | — | — | `createReport` body |
| Is required `parameters[].isRequired` | toggle | required | — | — | — | — | `createReport` body |
| Default value `parameters[].defaultValue` | field | optional | — | — | — | Open on purpose. A value of this parameter's `type`, used when a run supplies none. | `createReport` body |
| Required permission `requiredPermission` | select | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE … | — | Permission needed to run this report, from the shared `Permission` vocabulary. The author cannot assign one they do not hold — otherwise a venue user could build themselves a … | `createReport` body |
| Max date range days `maxDateRangeDays` | number field (days) | optional | 366 | min 1 | — | Guards against a query spanning years of scan events. When a report sets none, 366 days applies (decided 28 September, audit R158), so `runReport`'s date-range 400 always has a … | `createReport` body |

Errors to draw in the form: 400 Unknown field, invalid filter, or estimated cost beyond the limit; 403 Author does not hold the permission they assigned to the report

**Form: Save natural language query** (modal, opened by *Save natural language query*; *Save natural language query* calls `saveNaturalLanguageQuery`, *Cancel* sends nothing)

**Collects what `saveNaturalLanguageQuery` sends before it is called.** Required: `name`. Optional: `category`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `saveNaturalLanguageQuery` body |
| Category `category` | select | optional | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | — | — | `saveNaturalLanguageQuery` body |

**Form: Sync scans** (modal, opened by *Sync scans*; *Sync scans* calls `syncScans`, *Cancel* sends nothing)

**Collects what `syncScans` sends before it is called.** Required: `deviceId`, `scans`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | Sequence numbers are monotonic per device, not globally. | `syncScans` body |
| Scans `scans` | repeatable rows | required | — | at least 1; at most 500 | — | — | `syncScans` body |
| ID `scans[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key and dedupe key. | `syncScans` body |
| Media code `scans[].mediaCode` | text area | required | — | max length 256 | — | What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life. | `syncScans` body |
| Media kind `scans[].mediaKind` | select | required | — | Image · Video · Audio · Document · Vector · Font · Archive | — | — | `syncScans` body |
| Direction `scans[].direction` | radio group | required | — | Entry · Exit · Reentry · Crossover | — | — | `syncScans` body |
| Group size `scans[].groupSize` | number field | optional | — | min 1 | — | For group media admitting several holders on one read. | `syncScans` body |
| Proximity token `scans[].proximityToken` | text field | optional | — | — | — | BLE proximity assertion where the venue requires the operator to be physically at the gate. | `syncScans` body |
| Recorded at `scans[].recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the read. Authoritative for ordering, not for validity. | `syncScans` body |
| Sequence `scans[].sequence` | number field | required | — | min 1 | — | Monotonic per device. The server processes in this order. | `syncScans` body |
| Local outcome `scans[].localOutcome` | segmented control | required | — | Admitted · Denied · Overridden | — | What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded. | `syncScans` body |
| Local deny reason `scans[].localDenyReason` | select | optional | — | Not found · Not yet valid · Expired · Already used · Reentry limit reached · Exit required before reentry · Wrong access point · Wrong performance · Outside admission window · Entitlement suspended · Blacklisted · Capacity reached … | — | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean. | `syncScans` body |
| Overridden by principal `scans[].overriddenByPrincipalId` | picker: choose an overridden by principal | optional | — | — | shows names, sends the id | — | `syncScans` body |
| Override reason `scans[].overrideReason` | text field | optional | — | — | — | — | `syncScans` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Save report** (modal, opened by *Save report*; *Save report* calls `updateReport`, *Cancel* sends nothing)

**Collects what `updateReport` sends before it is called.** Required: `name`, `category`, `dataSource`, `columns`, `requiredPermission`. Optional: `description`, `filters`, `groupBy`, `parameters`, `maxDateRangeDays`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `updateReport` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `updateReport` body |
| Category `category` | select | required | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | — | — | `updateReport` body |
| Data source `dataSource` | select | required | — | Orders · Order lines · Payments · Refunds · Shifts · Scan events · Entitlements · Products · Inventory · Stock movements · Stock counts · Waste … | — | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over data nobody maintains. | `updateReport` body |
| Columns `columns` | repeatable rows | required | — | at least 1 | — | — | `updateReport` body |
| Field `columns[].field` | text field | required | — | — | — | — | `updateReport` body |
| Label `columns[].label` | text field | optional | — | — | — | — | `updateReport` body |
| Aggregation `columns[].aggregation` | select | optional | None | None · Count · Count distinct · Sum · Average · Min · Max | — | — | `updateReport` body |
| Sort order `columns[].sortOrder` | number field | optional | — | — | — | — | `updateReport` body |
| Sort direction `columns[].sortDirection` | segmented control | optional | — | Asc · Desc | — | — | `updateReport` body |
| Format `columns[].format` | text field | optional | — | — | — | — | `updateReport` body |
| Role `columns[].role` | segmented control | optional | — | Dimension · Measure | — | What the column is to a chart (decided 2 October 2026, Chinmay; CHG-FIN-007). A `dimension` groups (date, venue, channel, product); a `measure` is aggregated (sum of net revenue … | `updateReport` body |
| Encoding `columns[].encoding` | select | optional | — | Category · X · Y · Series · Value · Size · Colour · Location · Stage · Source · Target · Row … | — | Which field well the column fills (CHG-FIN-007), the binding the twenty marks of `DashboardTile.visualisation` need. | `updateReport` body |
| Axis `columns[].axis` | segmented control | optional | — | Primary · Secondary | — | For a measure on a `combo`, the axis it is drawn against. A secondary axis needs its own `unitLabel` (CHG-FIN-007). | `updateReport` body |
| Series type `columns[].seriesType` | segmented control | optional | — | Bar · Line · Area | — | For a measure on a `combo`, how that series is drawn (CHG-FIN-007). | `updateReport` body |
| Hierarchy level `columns[].hierarchyLevel` | number field | optional | — | min 1 | — | For `matrix` rows and columns, `treemap` nesting and `decompositionTree` levels, the depth of this dimension, 1 outermost. | `updateReport` body |
| Unit label `columns[].unitLabel` | text field | optional | — | max length 40 | — | The unit an axis states, for example "AED" or "Admissions". Required on a secondary axis (CHG-FIN-007). | `updateReport` body |
| Filters `filters` | repeatable rows | optional | — | — | — | — | `updateReport` body |
| Field `filters[].field` | text field | required | — | — | — | — | `updateReport` body |
| Operator `filters[].operator` | select | required | — | Equals · Not equals · Greater than · Less than · Between · In · Not in · Contains · Is null · Is not null | — | — | `updateReport` body |
| Value `filters[].value` | field | optional | — | — | — | Open on purpose; its type is the field's. One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a … | `updateReport` body |
| Values `filters[].values` | list of values (chips) | optional | — | — | — | The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`. | `updateReport` body |
| Is parameter `filters[].isParameter` | toggle | optional | off | — | — | Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope. | `updateReport` body |
| Group by `groupBy` | list of values (chips) | optional | — | — | — | — | `updateReport` body |
| Parameters `parameters` | repeatable rows | optional | — | — | — | — | `updateReport` body |
| Key `parameters[].key` | text field | required | — | — | — | — | `updateReport` body |
| Label `parameters[].label` | text field | required | — | — | — | — | `updateReport` body |
| Type `parameters[].type` | select | required | — | String · Integer · Decimal · Money · Boolean · Date · Date time · Uuid · Enum | — | — | `updateReport` body |
| Is required `parameters[].isRequired` | toggle | required | — | — | — | — | `updateReport` body |
| Default value `parameters[].defaultValue` | field | optional | — | — | — | Open on purpose. A value of this parameter's `type`, used when a run supplies none. | `updateReport` body |
| Required permission `requiredPermission` | select | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE … | — | Permission needed to run this report, from the shared `Permission` vocabulary. The author cannot assign one they do not hold — otherwise a venue user could build themselves a … | `updateReport` body |
| Max date range days `maxDateRangeDays` | number field (days) | optional | 366 | min 1 | — | Guards against a query spanning years of scan events. When a report sets none, 366 days applies (decided 28 September, audit R158), so `runReport`'s date-range 400 always has a … | `updateReport` body |

Errors to draw in the form: 409 The report is a system report, which is clone-only (audit R096).

**Form: Validate access** (modal, opened by *Validate access*; *Validate access* calls `validateAccess`, *Cancel* sends nothing)

**Collects what `validateAccess` sends before it is called.** Required: `id`, `mediaCode`, `mediaKind`, `direction`, `recordedAt`. Optional: `groupSize`, `proximityToken`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key and dedupe key. | `validateAccess` body |
| Media code `mediaCode` | text area | required | — | max length 256 | — | What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life. | `validateAccess` body |
| Media kind `mediaKind` | select | required | — | Image · Video · Audio · Document · Vector · Font · Archive | — | — | `validateAccess` body |
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

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Period and gates**: Today (live) or a past range; entry points from the venue's list; by hour or day. *(source: R282 / DI-182)*

#### Outputs: what the screen shows and produces

**Shown**

**Every scan event** (data table, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |

**Every report definition** (data table, from `listReports`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Category | chip: Sales, Admission, Financial, Inventory, Guest, Operations… | — |
| Max date range days | 1,234 | Guards against a query spanning years of scan events. When a report sets none, 366 days applies (decided 28 September, audit R158), so … |
| Is system | yes / no (icon or chip) | Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). Clone-only (decided 28 September, audit R096): `updateReport` … |

**The selected scan event** (detail panel, from `listScans`): **An override is its own row** (decided 28 September, audit R228): outcome `overridden`, `operatorPrincipalId` is the supervisor who overrode, and `overridesScanId` links it to the denied scan, which is never updated. Selecting either row shows the other.

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |
| Deny reason | chip: Not found, Not yet valid, Expired, Already used, Reentry limit reached, Exit … | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a … |
| Direction | chip: Entry, Exit, Reentry, Crossover | — |
| Operator principal | the name it points at, never the id | — |
| Overrides scan | the name it points at, never the id | Set only on an override row, naming the denied scan it admits against (decided 28 September, audit R228). |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Synced at | 1 Oct 2026, 14:30 | Null while pending. Differs from recordedAt for offline scans. |

**The offline package** (detail panel, from `getOfflinePackage`)

| Shows | Format | Notes |
|---|---|---|
| Generated at | 1 Oct 2026, 14:30 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Access point | the name it points at, never the id | — |
| Entitlements | list or chips (count when long) | Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device … |
| Delegated rights | list or chips (count when long) | Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits … |
| Blacklist | list or chips (count when long) | Media codes to deny outright regardless of entitlement state. |
| Admission rules | list or chips (count when long) | — |

**The report definition** (detail panel, from `getReport`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Category | chip: Sales, Admission, Financial, Inventory, Guest, Operations… | — |
| Data source | chip: Orders, Order lines, Payments, Refunds, Shifts, Scan events… | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over … |
| Columns | list or chips (count when long) | — |
| Filters | list or chips (count when long) | — |
| Estimated cost | chip: Low, Medium, High | Informs whether it may run inline or must be queued. |
| Last run at | 1 Oct 2026, 14:30 | — |

**The financial report** (detail panel, from `getFinancialReport`)

| Shows | Format | Notes |
|---|---|---|
| Report | chip: Profit and loss, Balance sheet, Cash flow, Revenue by venue, Revenue by product … | The report `getFinancialReport` returns. One vocabulary for the query and the response. |
| Fiscal period | the name it points at, never the id | — |
| Legal entity | the name it points at, never the id | — |
| Currency | text | — |
| Currency scale | 1,234 | — |
| Generated at | 1 Oct 2026, 14:30 | — |
| Sections | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Run report (primary button) | `runReport` POST `/reports/{reportId}/run` | RunReportRequest | ReportResult | 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope | opens modal first |
| Ask reporting question (secondary button) | `askReportingQuestion` POST `/reports/ask` | inline | NaturalLanguageAnswer | 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope | opens modal first |
| Create report (secondary button) | `createReport` POST `/reports` | CreateReportRequest | ReportDefinition | 400 Unknown field, invalid filter, or estimated cost beyond the limit; 403 Author does not hold the permission they assigned to the report | opens modal first |
| Delete report (destructive button) | `deleteReport` DELETE `/reports/{reportId}` | — | — | 409 Active schedules reference this report (`report-scheduled`), or it is a system report, which is clone-only (`system-report`, audit R096) | — |
| Lookup ticket (secondary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | produces a document or message: Read-only validity check without admitting |
| Override access (destructive button) | `overrideAccess` POST `/access/override` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 The scan was not a denial, or has already been overridden | — |
| Save natural language query (secondary button) | `saveNaturalLanguageQuery` POST `/reports/ask/{conversationId}/save` | inline | ReportDefinition | — | opens modal first |
| Sync scans (secondary button) | `syncScans` POST `/access/scans` | inline | ScanSyncResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Save report (secondary button) | `updateReport` PUT `/reports/{reportId}` | CreateReportRequest | ReportDefinition | 409 The report is a system report, which is clone-only (audit R096). | opens modal first |
| Validate access (secondary button) | `validateAccess` POST `/access/validate` | ValidateRequest | ValidationResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell | opens modal first |
| Validate group access (secondary button) | `validateGroupAccess` POST `/access/group-validate` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Inside now**: Admitted minus exited, refreshed at least every 30 seconds with "Updated 40 sec ago"; capacity percentage beside it. *(source: DI-182 / contracts/satellite/reporting.yaml#/components/schemas/DashboardTile)*
- **Admissions by hour and gate**: Heat map of hour against gate, values readable without colour; bars per gate. *(source: R282 / MATRIX 6.1.69)*
- **Category breakdown**: General admission, group, re-entry, crossover; schools and groups listed by booking. *(source: DI-647)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Run report**: Runs the seeded attendance and footfall report for the range. *(source: R282)*

**Data it reads**: `listScans` (onLoad, List scan events); `getFinancialReport` (onLoad, P&L, balance sheet or cash flow); `getOfflinePackage` (onLoad, Entitlement and rule set for offline validation); `listReports` (onLoad, List available report definitions)

**What opens over it**

- confirmDialog *Delete report*: **Names what `deleteReport` changes and what it leaves alone**, in the consequence rather than the verb. A attendance footfall this affects should be identified in the dialog, not just counted.
- confirmDialog *Override access*: **Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A attendance footfall this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason` …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attendance footfall list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attendance footfall untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attendance footfall yet. Offers Create report (`createReport`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the attendance footfall are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires to show this screen, and names that permission (the screen's other reads need `ACCESS_VALIDATE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCESS_OVERRIDE` for `overrideAccess`; `REPORT_MANAGE` for … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 Question could not be interpreted. (ReportQuestionProblem); 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 400 Unknown field, invalid filter, or estimated cost beyond the limit |

#### Edge cases to draw

- **A gate offline**: Its scans arrive late when it syncs; the hour shows "incomplete: Gate 3 offline" until then. *(source: DI-625)*

#### Consistency with other screens

- Match `ANL-014`: The analytics attendance board uses the same admission definition (admitted, in-direction scans).
- Match `BO-100`: The admissions tile is the same figure.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
now: Inside now 6,214 · capacity 8,500 · 73% · Updated 40 sec ago
hourly: 10:00 1,842 · 11:00 2,310 · 12:00 1,166 · Main Gate 62% · North Gate 38%
```

#### Permissions

- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `createReport` → `REPORT_MANAGE` (configure) · staff, partner
- `deleteReport` → `REPORT_MANAGE` (configure) · staff, partner
- `getFinancialReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `getReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `listReports` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff
- `saveNaturalLanguageQuery` → `REPORT_MANAGE` (configure) · staff, partner
- `syncScans` → `ACCESS_VALIDATE` (operate) · staff
- `updateReport` → `REPORT_MANAGE` (configure) · staff, partner
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff
- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires to show this screen, and names that permission (the screen's other reads need `ACCESS_VALIDATE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCESS_OVERRIDE` for `overrideAccess`; `REPORT_MANAGE` for …

#### Requirements it meets

153 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 13.3.14 | APIs shall expose operational, financial, attendance, membership and sales reporting data. | Developer & API Management | CONTRACTED | `runReport` |
| 1.1.63 | Entitlement audit reporting | Ticketing Catalogue | CONTRACTED | `listScans` |
| 3.1.6 | The system shall maintain complete scan history including gate, location, timestamp, device ID, operator, validation result, and entry attempts. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.21 | The system should keep track of the count of people passing through an access control device. Multiple Access Control System can be grouped together to give the capacity count of a specific … | Admission and Access | CONTRACTED | `listScans` |
| 3.2.54 | If access control reading is valid, the attendance counter is increased by the number or Guests associated to the ticket. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.55 | All Guests are invited use the turnstiles when leaving the park. It is expected that the system counts the number of exits. Scan can be required at exit. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.58 | In park attendance figure per ticket time is calculated in real time. | Admission and Access | CONTRACTED | `listScans` |
| 5.3.28 | Maintain detailed access validation history including gate entries, exits, attraction validations, RFID scans, QR scans, and turnstile events. | F&B & Guest Management | CONTRACTED | `listScans` |
| … 141 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Admission Summary dashboard: real-time headcount of guests inside the venue from ticket scans. *(agreed · MoM 7 Aug 2026, 21. Dashboards & Reporting · DI-182)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-060` · status **notStarted** · provenance generated
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)
- ADR-0059 *AI phasing against the six-month plan* (`docs/adr/0059-ai-phasing-against-the-six-month-plan.md`)
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (111), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (38 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-060?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Run report, Ask reporting question, Create report, Delete report, Lookup ticket, Override access, Save natural language query, Sync scans, Save report, Validate access, Validate group access.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_MANAGE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-064` Zones & Areas

**Divide the venue into the things gates control.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 1 · needs the `access` module |
| Block | Block A · task APP-SETUP-BO-064 |
| Who uses it | venue staff holding `ACCESS_POINT_CONFIGURE`, `SCOPE_MANAGE`, `SCOPE_VIEW` (2 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listOrgUnits` reads the population and `getAccessPoint` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `accessPointId` (deepLink), `orgUnitId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/zones-areas` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Direction is set only here (decided 28 September, audit R221)** — `createAccessPoint` and `updateAccessPoint` carry an access point's fixed direction; `setTurnstileMode` sets the operating mode (with an optional turnstile mode) and never the direction. The scanner shows direction read-only.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): The operating mode is a live podium action (R221) that belongs on BO-201 and SCN-016; on this configuration screen it invites changing a gate's live state from a …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Builds the venue's access topology: the organisational nodes (venue, departments) on the left and the access points that gates enforce under them, each with a fixed direction, anti-passback, exit-before-re-entry, controller driver and optional geofence. This is the only place direction is set. The one thing to get right: draw it as a tree of places with access points as leaves, not two unrelated tables.

**Fixed on main** (the package already carries these; draw what it says): Save turnstile mode (setTurnstileMode) on this configuration screen (CHG-WIR-001); Filter text fields "Under" and "Level" for org units (CHG-SBO-009); venueId is a required create field (CHG-SBO-009).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Level | select | optional | — | Tenant · Brand · Region · Venue · Department · Sub department · Workstation · Outlet · Subject | — | Level in words (brand, region, venue, department ...); the units are a tree, not ids typed by hand. | `OrgUnit.level` |
| Include inactive | toggle | optional | off | — | — | Sends `?includeInactive=` to `listOrgUnits`. | `listOrgUnits` ?includeInactive |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Under | text field | — | — | `listOrgUnits` ?under |
| Level | select | — | Tenant · Brand · Region · Venue · Department · Sub department · Workstation · Outlet · Subject | `listOrgUnits` ?level |

**Form: Create org unit** (modal, opened by *Create org unit*; *Create org unit* calls `createOrgUnit`, *Cancel* sends nothing)

**Collects what `createOrgUnit` sends before it is called.** Required: `level`, `parentId`, `code`, `name`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Level `level` | select | required | — | Tenant · Brand · Region · Venue · Department · Sub department · Workstation · Outlet · Subject | — | The eight organisational levels, plus `subject`. Restored 24 August. | `createOrgUnit` body |
| Parent `parentId` | picker: choose a parent | required | — | — | shows names, sends the id | Required for every level except tenant, which the cell creates at provisioning. | `createOrgUnit` body |
| Code `code` | text field | required | — | max length 64; pattern `^[a-z0-9_]+$` | — | Becomes the final ltree segment. Immutable once created. | `createOrgUnit` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createOrgUnit` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types.

**Form: Save access point geofence** (modal, opened by *Save access point geofence*; *Save access point geofence* calls `setAccessPointGeofence`, *Cancel* sends nothing)

**Collects what `setAccessPointGeofence` sends before it is called.** Required: `enforcement`. Optional: `latitude`, `longitude`, `radiusMetres`, `allowProximityBeacon`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Latitude `latitude` | number field | optional | — | — | — | — | `setAccessPointGeofence` body |
| Longitude `longitude` | number field | optional | — | — | — | — | `setAccessPointGeofence` body |
| Radius metres `radiusMetres` | number field | optional | — | min 5; max 5000 | — | — | `setAccessPointGeofence` body |
| Enforcement `enforcement` | segmented control | required | — | Off · Warn · Deny | — | `off` keeps the fence on record and checks nothing; `warn` lets a validation from outside the fence through with a warning; `deny` refuses it. | `setAccessPointGeofence` body |
| Allow proximity beacon `allowProximityBeacon` | toggle | optional | — | — | — | Accept a BLE proximity assertion in place of GPS. Better indoors. | `setAccessPointGeofence` body |

Errors to draw in the form: 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Save access point** (modal, opened by *Save access point*; *Save access point* calls `updateAccessPoint`, *Cancel* sends nothing)

**Collects what `updateAccessPoint` sends before it is called.** Nothing in the body is required. Optional: `name`, `direction`, `antiPassbackEnabled`, `requiresExitBeforeReentry`, `isActive`, `driver`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateAccessPoint` body |
| Direction `direction` | radio group | optional | — | Entry · Exit · Reentry · Crossover | — | — | `updateAccessPoint` body |
| Anti passback enabled `antiPassbackEnabled` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Requires exit before reentry `requiresExitBeforeReentry` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Driver `driver` | text field | optional | — | — | — | Driver identifier for the controller behind this access point. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific. | `updateAccessPoint` body |
| Temporary closure `temporaryClosure` | group | optional | — | — | — | Close or reopen the access point's attraction for a while (`AccessPoint.temporaryClosure`; DEC-228; CHG-CSP-026). | `updateAccessPoint` body |
| Is closed `temporaryClosure.isClosed` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Reason `temporaryClosure.reason` | text area | optional | — | max length 200 | — | — | `updateAccessPoint` body |
| Reopens at `temporaryClosure.reopensAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAccessPoint` body |
| Offer virtual queue return `temporaryClosure.offerVirtualQueueReturn` | toggle | optional | — | — | — | — | `updateAccessPoint` body |
| Queue `temporaryClosure.queueId` | picker: choose a queue | optional | — | — | shows names, sends the id | — | `updateAccessPoint` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Save org unit** (modal, opened by *Save org unit*; *Save org unit* calls `updateOrgUnit`, *Cancel* sends nothing)

**Collects what `updateOrgUnit` sends before it is called.** Nothing in the body is required. Optional: `name`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateOrgUnit` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateOrgUnit` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types.

**Form: Create access point** (modal, opened by *Create access point*; *Create access point* calls `createAccessPoint`, *Cancel* sends nothing)

**Collects what `createAccessPoint` sends before it is called.** Required: `code`, `name`, `direction`. Optional: `antiPassbackEnabled`, `requiresExitBeforeReentry`, `driver`. `venueId` comes from the session (VO-R03, VO-R09), never asked. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createAccessPoint` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createAccessPoint` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createAccessPoint` body |
| Direction `direction` | radio group | required | — | Entry · Exit · Reentry · Crossover | — | — | `createAccessPoint` body |
| Anti passback enabled `antiPassbackEnabled` | toggle | optional | off | — | — | — | `createAccessPoint` body |
| Requires exit before reentry `requiresExitBeforeReentry` | toggle | optional | off | — | — | — | `createAccessPoint` body |
| Driver `driver` | text field | optional | — | — | — | — | `createAccessPoint` body |

Errors to draw in the form: 400 Validation failed

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Access point - direction**: Entry / Exit / Re-entry / Crossover as a segmented control, set here only; changing it on an active point asks for confirmation because gates reverse what they admit. *(source: contracts/spine/access.yaml#createAccessPoint / R221)*
- **Access point - code, name**: Code max 64 unique in the venue; name as staff see it on scanners ("Main Plaza Gate 2"). *(source: contracts/spine/access.yaml#createAccessPoint)*
- **Anti-passback / Exit required before re-entry**: Two toggles with one-line explanations; exit-before-re-entry only makes sense on entry or re-entry points. *(source: contracts/spine/access.yaml#createAccessPoint / MATRIX 1.1.60)*
- **Geofence**: Map with a pin and radius (5-5000 m) and enforcement Off / Warn / Deny, plus "Accept a beacon instead of GPS (better indoors)". Default Warn; Deny shows a caution about indoor GPS. *(source: contracts/spine/access.yaml#setAccessPointGeofence)*
- **Org unit - code**: Lower-case letters, digits and underscore only; immutable after creation (show locked with the reason). *(source: contracts/spine/tenancy.yaml#createOrgUnit)*

#### Outputs: what the screen shows and produces

**Shown**

**Zones and areas** (tree nav, from `listOrgUnits`)

| Shows | Format | Notes |
|---|---|---|
| Level | chip: Tenant, Brand, Region, Venue, Department, Sub department… | The eight organisational levels, plus `subject`. Restored 24 August. |
| Code | text | — |
| Name | text | — |
| Is active | yes / no (icon or chip) | False causes every permission query at or beneath this node to resolve to DENY. |
| Child count | 1,234 | — |

**Every access point** (data table, from `listAccessPoints`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| External credential sources | list or chips (count when long) | BL-108. A hotel room card admitting a guest to a water park — externally issued, and the platform validates it without having sold it. |
| Operating mode | chip: Normal, Free flow, Drop arm, Closed, Podium, Maintenance | Set by the podium with `setTurnstileMode`, and it wins (audit R221). BL-107 and BL-109. |
| Mode | chip: Free rotation, Closed | Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates … |
| Direction | chip: Entry, Exit, Reentry, Crossover | Fixed per access point (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium. |

**The selected org unit** (detail panel, from `getOrgUnit`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Level | chip: Tenant, Brand, Region, Venue, Department, Sub department… | The eight organisational levels, plus `subject`. Restored 24 August. |
| Parent | the name it points at, never the id | — |
| Path | text | Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`. |
| Code | text | — |
| Name | text | — |
| Is active | yes / no (icon or chip) | False causes every permission query at or beneath this node to resolve to DENY. |
| Child count | 1,234 | — |

**The access point** (detail panel, from `getAccessPoint`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| External credential sources | list or chips (count when long) | BL-108. A hotel room card admitting a guest to a water park — externally issued, and the platform validates it without having sold it. |
| Scan anomaly rules | list or chips (count when long) | BL-104. Rule-based scan anomalies, separated from the parked model-based engine — device sharing, simultaneous entries at two gates, an … |
| Operating mode | chip: Normal, Free flow, Drop arm, Closed, Podium, Maintenance | Set by the podium with `setTurnstileMode`, and it wins (audit R221). BL-107 and BL-109. |
| Vehicle location capture | yes / no (icon or chip) | BL-023. Nothing helped a guest find their vehicle. |
| Mode | chip: Free rotation, Closed | Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates … |
| Direction | chip: Entry, Exit, Reentry, Crossover | Fixed per access point (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create access point (primary button) | `createAccessPoint` POST `/access-points` | CreateAccessPointRequest | AccessPoint | 400 Validation failed | opens modal first |
| Create org unit (secondary button) | `createOrgUnit` POST `/org-units` | CreateScopeNodeRequest | OrgUnit | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types. | opens modal first |
| Save access point geofence (secondary button) | `setAccessPointGeofence` PUT `/access-points/{accessPointId}/geofence` | AccessPointGeofence | AccessPoint | 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save access point (secondary button) | `updateAccessPoint` PATCH `/access-points/{accessPointId}` | inline | AccessPoint | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save org unit (secondary button) | `updateOrgUnit` PATCH `/org-units/{orgUnitId}` | inline | OrgUnit | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Topology tree**: Venue > department/park nodes > access points with direction icon, active state and last heartbeat ("seen 2 min ago"). *(source: contracts/spine/access.yaml#/components/schemas/AccessPoint / contracts/spine/tenancy.yaml#listOrgUnits)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Add access point**: Creates under the selected node; venue from the session (VO-R03). *(source: contracts/spine/access.yaml#createAccessPoint)*
- **Deactivate node**: Confirm "Every permission at or below this node will be denied; no data is deleted". *(source: contracts/spine/tenancy.yaml#updateOrgUnit)*

**Data it reads**: `listOrgUnits` (onLoad, List scope nodes visible to the session); `listAccessPoints` (onLoad, List access points)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The zones areas list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the zones areas untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No zones areas yet. Offers Create access point (`createAccessPoint`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on under, level, includeInactive and the zones areas are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SCOPE_VIEW`, which `listOrgUnits` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCESS_POINT_CONFIGURE` for `createAccessPoint`, `setAccessPointGeofence`, `updateAccessPoint`; `SCOPE_MANAGE` for `createOrgUnit`, `updateOrgUnit`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types. |

#### Edge cases to draw

- **Deactivating an access point that has scans today**: Allowed; confirm shows today's scan count and that the gate will stop validating. *(source: contracts/spine/access.yaml#updateAccessPoint)*

#### Consistency with other screens

- Match `BO-201`: Live gate mode (normal, free flow, drop arm, closed, podium, maintenance) is changed on BO-201 and SCN-016, not here.
- Match `BO-146`: Access areas and zones from the access board must show in the same tree (cross-check with BO-145/BO-146).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tree: Aqua Park > Main Plaza > Main Plaza Gate 1 (Entry), Gate 2 (Entry), Gate 3 (Exit); North Entry (Re-entry);
  Car Park Barrier A (Entry)
```

#### Permissions

- `listOrgUnits` → `SCOPE_VIEW` (read) · staff
- `listAccessPoints` → `SCOPE_VIEW` (read) · staff
- `createAccessPoint` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `createOrgUnit` → `SCOPE_MANAGE` (configure) · staff
- `getAccessPoint` → `SCOPE_VIEW` (read) · staff
- `getOrgUnit` → `SCOPE_VIEW` (read) · staff
- `setAccessPointGeofence` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `updateAccessPoint` → `ACCESS_POINT_CONFIGURE` (configure) · staff
- `updateOrgUnit` → `SCOPE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `SCOPE_VIEW`, which `listOrgUnits` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCESS_POINT_CONFIGURE` for `createAccessPoint`, `setAccessPointGeofence`, `updateAccessPoint`; `SCOPE_MANAGE` for `createOrgUnit`, `updateOrgUnit`.

#### Requirements it meets

27 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.41 | Venue-Specific Policies - System shall support venue-specific access policies. | Admission and Access | CONTRACTED | `listOrgUnits` |
| 3.3.43 | Policy Inheritance - System shall support inheritance of policies across organizational structures. | Admission and Access | CONTRACTED | `listOrgUnits` |
| 7.1.13 | The system shall support permission assignment at company, department, venue, park, attraction, facility, event, sales channel, POS terminal, and product levels. | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.27 | The system shall support management of companies, business units, departments, parks, venues, attractions, facilities, cost centers, and reporting structures. | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.37 | Allow administrators to restrict access by venue, park, facility, attraction, sales channel, POS terminal, country, region, IP address and network range. Policies should support allow/deny logic and … | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.52 | Support policies spanning multiple parks, venues, attractions, departments and business units while maintaining centralized governance. | F&B POS | CONTRACTED | `listOrgUnits` |
| 1.1.60 | Check-in / Check-out entitlement control | Ticketing Catalogue | CONTRACTED | `createAccessPoint` |
| 3.2.11 | The system should be able to define and configure all access control rules, all gates (entrances of access-control areas), access points and locations (a group of areas). | Admission and Access | CONTRACTED | `createAccessPoint` |
| 7.1.14 | The system shall isolate users, permissions, configurations, and data between tenants. Users shall only access data belonging to their assigned tenant unless explicitly authorized. | F&B POS | CONTRACTED | `getOrgUnit` |
| 7.1.53 | Allow separate authorization policies for each tenant in a multi-tenant environment without impacting other tenants. | F&B POS | CONTRACTED | `getOrgUnit` |
| 7.3.1 | The sales system shall be able to manage the data transactions for Multi Tenants Sites | F&B POS | CONTRACTED | `getOrgUnit` |
| 13.1.46 | Multi-Tenant API Access - System shall support tenant-specific API access. | Developer & API Management | CONTRACTED | `getOrgUnit` |
| … 15 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-064` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (32), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (27 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-064?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create access point, Create org unit, Save access point geofence, Save access point, Save org unit.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ACCESS_POINT_CONFIGURE`, `SCOPE_MANAGE`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-067` Integrations

**Connect the venue to the systems around it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVELOPER_MANAGE`, `DEVELOPER_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): 3 independent reads and no read of one record — the screen watches a population rather than working one |
| Offline | online only |
| Opens with | `subscriptionId` (navigation) · cold entry: **Deliveries belong to a subscription**, so the list is reached from the subscription that owns them. Opened without one the screen shows the subscriptions and … |
| Route | `/venue-operations/integrations` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Drawn 31 August** — `Seat Platform Board 13.dc.html` frame `seatp-13d`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Integrations* matched at 1.0. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): createApiClient on the tenant's integrations screen; production clients are issued by TICVAI on an approved request and sandbox clients belong to developers …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The venue's integrations at a glance: API clients acting for the tenant and webhook subscriptions with their recent deliveries. A tenant sees and suspends the clients that act for it; developers create their own clients in the developer portal.

**Fixed on main** (the package already carries these; draw what it says): createApiClient on the tenant's screen. (CHG-WIR-021); formCreateApiClient asks the person for status, id. (CHG-WIR-021); formCreateWebhookSubscription asks the person for status, id. (CHG-SBO-004); Tables show every schema field, plumbing included: 'Every API client' drop id, developerId, clientId, allowedTenantIds. (CHG-SBO-004).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Client | picker: choose a client | — | — | `listWebhookSubscriptions` ?clientId |

**Form: Create webhook subscription** (modal, opened by *Create webhook subscription*; *Create webhook subscription* calls `createWebhookSubscription`, *Cancel* sends nothing)

**Collects what `createWebhookSubscription` sends before it is called.** Required: `clientId`, `endpointUrl`, `eventTypes`. Optional: `filters`, `signingSecret`. **Not asked:** is a client UUIDv7 generated silently; is set by the server (design-note correction, 2 October 2026). Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `consecutiveFailures`, `disabledReason`, `id`, `status` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Client `clientId` | picker: choose a client | required | — | — | shows names, sends the id | — | `createWebhookSubscription` body |
| Endpoint URL `endpointUrl` | text field | required | — | — | — | — | `createWebhookSubscription` body |
| Event types `eventTypes` | multi-select chips | required | — | Access.validated · Accreditation.application decided · Accreditation.credential issued · Accreditation.holder status changed · Accreditation.renewal due · Ai.ceiling approaching · API client.anomaly detected · Approval.escalated · Approval.expired · … | — | Filtered at subscription, not at delivery. A subscriber taking every event and discarding 99% is a subscriber the platform pays to talk to. | `createWebhookSubscription` body |
| Filters `filters` | key and value settings | optional | — | — | — | 13.3.22. Tenant, venue, or a business condition on the payload. | `createWebhookSubscription` body |
| Signing secret `signingSecret` | text field | optional | — | — | — | How the receiver knows it was TICVAI. Without a signature an endpoint accepts a ticket-sale event from anybody who learns the URL. | `createWebhookSubscription` body |

Errors to draw in the form: 422 An entry in `eventTypes` is not in the webhook event catalogue.

#### Outputs: what the screen shows and produces

**Shown**

**Api clients** (metric tile, from `listApiClients`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Developer | the name it points at, never the id | — |
| Name | text | — |
| Client | text | — |
| Environment | chip: Sandbox, Production | Bound to one, stated on the object rather than by naming convention. A key that works in both is a key somebody will use in the wrong one. |
| Scopes | list or chips (count when long) | Resolved against the tenant's licence at token issue (13.3.24). A scope granted here and not licensed there produces no token — and the … |
| Issued by | chip: Partner, Ticvai | Who generated the key (M17-06): a developer for a sandbox key, TICVAI for a production key issued on an approved `requestProductionAccess`. |
| Certification listing | the name it points at, never the id | For a production client, the certified integration it was issued against. |
| Credential ttl days | 1,234 | Key lifetime. Default 365 for production, 90 for sandbox (M17-06, configurable expiry). |
| Expires at | 1 Oct 2026, 14:30 | When the key stops working unless rotated. No token is issued after it. |
| Allowed tenants | list or chips (count when long) | 13.1.46. Which tenants this client may act for. |
| Ip allow list | list or chips (count when long) | 13.1.38. Required on a production client (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the … |
| Status | chip: Active, Suspended, Revoked | — |
| Last used at | 1 Oct 2026, 14:30 | A credential unused for a year is a credential nobody will notice being stolen. |

**Webhook subscriptions** (metric tile, from `listWebhookSubscriptions`): Every webhook subscription in the tenant; selecting an API client passes `?clientId=` to narrow it (decided 28 September, audit R214 (4)).

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Client | the name it points at, never the id | — |
| Endpoint URL | text | — |
| Event types | list or chips (count when long) | Filtered at subscription, not at delivery. A subscriber taking every event and discarding 99% is a subscriber the platform pays to talk to. |
| Filters | grouped details | 13.3.22. Tenant, venue, or a business condition on the payload. |
| Signing secret | text | How the receiver knows it was TICVAI. Without a signature an endpoint accepts a ticket-sale event from anybody who learns the URL. |
| Status | chip: Pending verification, Active, Paused, Failing, Disabled | — |
| Consecutive failures | 1,234 | — |
| Disabled reason | text | 13.1.29. An endpoint failing for days is disabled rather than retried forever, and the developer is told — a queue growing against a dead … |

**Webhook deliveries** (metric tile, from `listWebhookDeliveries`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Subscription | the name it points at, never the id | — |
| Event | the name it points at, never the id | — |
| Event type | text | — |
| Status | chip: Pending, Delivered, Failed, Retrying, Abandoned | — |
| Attempt count | 1,234 | — |
| Response code | 1,234 | — |
| Response body excerpt | text | Truncated, and it is what makes the log useful — a 500 with the receiver's own error message in it answers the question without a … |
| Is replay | yes / no (icon or chip) | — |
| Is test | yes / no (icon or chip) | Sent by `testWebhookSubscription` (VM close-out, 29 September). Marked in the payload so a receiver never books it, and never counted … |
| Delivered at | 1 Oct 2026, 14:30 | — |

**Every API client** (data table, from `listApiClients`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Environment | chip: Sandbox, Production | Bound to one, stated on the object rather than by naming convention. A key that works in both is a key somebody will use in the wrong one. |
| Scopes | list or chips (count when long) | Resolved against the tenant's licence at token issue (13.3.24). A scope granted here and not licensed there produces no token — and the … |
| Ip allow list | list or chips (count when long) | 13.1.38. Required on a production client (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the … |
| Status | chip: Active, Suspended, Revoked | — |
| Last used at | 1 Oct 2026, 14:30 | A credential unused for a year is a credential nobody will notice being stolen. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create webhook subscription (secondary button) | `createWebhookSubscription` POST `/webhook-subscriptions` | WebhookSubscription | WebhookSubscription | 422 An entry in `eventTypes` is not in the webhook event catalogue. | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Webhook deliveries**: Last deliveries per subscription with status code, attempts and next retry; failures first. *(source: contracts/satellite/public-api.yaml#listWebhookDeliveries)*

**Data it reads**: `listApiClients` (onLoad, API clients this tenant has issued); `listWebhookSubscriptions` (onLoad, Subscriptions and their targets)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Detail loads |
| Error (`?state=error`) | Could not load |
| Empty, first run (`?state=emptyFirstRun`) | Not found — it may have been deleted or moved out of scope |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listApiClients` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `DEVELOPER_VIEW`, which `listApiClients` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `DEVELOPER_MANAGE` for `createWebhookSubscription`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 An entry in `eventTypes` is not in the webhook event catalogue. |

#### Edge cases to draw

- **Can read but not change (holds DEVELOPER_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: DEVELOPER_MANAGE for Create API client, Create webhook subscription. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/public-api.yaml#createApiClient)*
- **createApiClient answers 409**: Show it as something the person can act on, not a failure: A `production` client without a current certification, or asked for by a developer rather than issued by TICVAI (`certification-required`, M17-06). Use `requestProductionAccess`. *(source: contracts/satellite/public-api.yaml#createApiClient)*
- **createApiClient answers 422**: Show it as something the person can act on, not a failure: A `production` client with an empty `ipAllowList` (`ip-allow-list-required`, M17-07), or a scope that is not in the scope catalogue (`unknown-scope`, M17-05). *(source: contracts/satellite/public-api.yaml#createApiClient)*
- **createWebhookSubscription answers 422**: Show it as something the person can act on, not a failure: An entry in `eventTypes` is not in the webhook event catalogue. *(source: contracts/satellite/public-api.yaml#createWebhookSubscription)*

#### Consistency with other screens

- Match `DEV-003`: Clients created by a developer appear here for the tenant they may act for.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Api clients: 128
  Webhook subscriptions: 46
  Webhook deliveries: 312
Every API client:
- name: Kiosk connector (sandbox)
  status: active
  lastUsedAt: 01/10/2026 09:14
- name: OTA availability feed
  status: pending
  lastUsedAt: 30/09/2026 18:02
- name: Wallet sync
  status: suspended
  lastUsedAt: 28/09/2026 11:45
```

#### Permissions

- `listApiClients` → `DEVELOPER_VIEW` (read) · staff, partner
- `listWebhookSubscriptions` → `DEVELOPER_VIEW` (read) · staff, partner
- `listWebhookDeliveries` → `DEVELOPER_VIEW` (read) · staff, partner
- `createWebhookSubscription` → `DEVELOPER_MANAGE` (configure) · staff, partner

**A refused user sees:** Shown when the caller lacks `DEVELOPER_VIEW`, which `listApiClients` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `DEVELOPER_MANAGE` for `createWebhookSubscription`.

#### Requirements it meets

27 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.7.52 | System shall allow approved B2B partners to request, generate, manage, rotate, and revoke API credentials. Access shall be restricted by partner permissions, products, quotas, rate limits, IP … | Ticketing Sales | CONTRACTED | data `ApiClient` |
| 7.1.25 | The system shall support dedicated API users, integration users, service accounts, API keys, credential rotation, expiry controls, IP restrictions, and audit logging. | F&B POS | CONTRACTED | data `ApiClient` |
| 13.1.11 | API Key Management - System shall support API key generation and management. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.13 | OAuth Support - System shall support OAuth authentication. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.14 | Token Management - System shall support access token management. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.15 | Credential Revocation - System shall support credential revocation. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.21 | API Explorer - System shall provide interactive API testing tools. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.22 | SDK Availability - System shall provide SDKs for supported platforms. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.23 | Code Samples - System shall provide implementation examples. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.24 | Postman Collections - System shall provide Postman collections. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.38 | IP Whitelisting - System shall support IP whitelisting. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.40 | Security Monitoring - System shall monitor API security events. | Developer & API Management | CONTRACTED | data `ApiClient` |
| … 15 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Financial year/period setup varies by country (UAE Jan–Dec, India Apr–Mar); closing a period locks further postings. An ERP integration centre manages external connections. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-263)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-067` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Seat Platform Board 13.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been …
- Derived from `wireframes/reference/Seat Platform Board 13.dc.html`
- Client design-board frames: `Seat Platform Board 13.dc.html#seatp-13d`

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-067?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create webhook subscription.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `DEVELOPER_MANAGE`, `DEVELOPER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-070` Work Orders

**Get something fixed, and know it was.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 2 · needs the `maintenance` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MAINTENANCE_APPROVE`, `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VIEW` (2 operate, 1 configure, 1 read); in the flows as technician |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listWorkOrders` reads the population and `getWorkOrder` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `workOrderId` (deepLink), `vendorServiceRequestId` (navigation) · cold entry: **Without `workOrderId` the list opens** — the ordinary arrival from BO-108 Venue Operations (decided 29 September, VM close-out). **A staff link opened cold … |
| Route | `/venue-operations/work-orders` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **createRefund removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class). **Rebound 28 September to maintenance work orders (audit R254)** — the screen carried thirteen sales-order operations (`listOrders`, `voidOrder`, `holdOrder` and ten more) because *order* resembled *work order*. It now lists, raises, pauses, rejects, completes, closes and cancels maintenance work orders from `maintenance.yaml`; the sales-order work stays on the POS and order screens.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The work order desk for supervisors: raise, prioritise, assign, follow and close maintenance work. Priority is shown with where it came from (scored by venue policy, asset override, or manual); smart assignment ranks technicians by skill, shift and load but assigns nothing until a person presses Assign; outside vendors are tracked on the work order. The one thing to get right: the lifecycle Created > Assigned > Accepted > In progress > Completed > Verified > Closed is visible on every row, with a running timer.

**Known correction pending (do not draw the wrong version)**

- **Accept, Start and Resume are not bound although the lifecycle needs them (only pause, reject, complete, close, cancel)** Why: Matrix 18.2.1-18.2.4 and the screen's own lifecycle include accept and start; bind them or state they live only on the Staff App. *(source: MATRIX 18.2.2 / MATRIX 18.2.4 / contracts/satellite/maintenance.yaml#acceptWorkOrder; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No calendar view although listWorkOrders was given from/to/categoryId for calendars (M17-03)** Why: Every calendar in the platform needs day/week/month (VO-R01). *(source: contracts/satellite/maintenance.yaml#listWorkOrders / DI-919; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Parts reservation (DI-925) not bound** Why: Parts are reserved in the general inventory from the work order. *(source: DI-925; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select | optional | — | Open · Assigned · In progress · Paused · Awaiting parts · Completed · Verified · Closed · Cancelled | — | Sends `?status=` to `listWorkOrders`. | `listWorkOrders` ?status |
| Priority | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | Sends `?priority=` to `listWorkOrders`. | `listWorkOrders` ?priority |
| Assigned to | picker: choose an assigned to principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?assignedToPrincipalId=` to `listWorkOrders`. | `listWorkOrders` ?assignedToPrincipalId |
| Asset id | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | Sends `?assetId=` to `listWorkOrders`. | `listWorkOrders` ?assetId |
| Overdue only | toggle | — | — | — | — | Sends `?overdueOnly=true` to `listWorkOrders`. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Overdue only | toggle | off | — | `listWorkOrders` ?overdueOnly |
| From | date and time picker | — | — | `listWorkOrders` ?from |
| To | date and time picker | — | — | `listWorkOrders` ?to |
| Category | picker: choose a category | — | — | `listWorkOrders` ?categoryId |

**Form: Raise work order** (modal, opened by *Raise work order*; *Raise work order* calls `createWorkOrder`, *Cancel* sends nothing)

**Collects what `createWorkOrder` sends before it is called.** Required: `id`, `title`, `venueId`, `recordedAt`. Optional: `description`, `assetId`, `locationDescription`, `kind`, `priority`, `categoryId`, `assignedToPrincipalId`, `dueAt`, `attachmentRefs`, `faultAssessment` and `requiredQualificationCodes`. **Priority is left empty to be scored** (M17-01): the asset's override, else the venue policy's score of the fault assessment; choosing one makes it manual. Dismissing sends nothing; the screen behind is unchanged.

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

**Form: Save work order** (modal, opened by *Save work order*; *Save work order* calls `updateWorkOrder`, *Cancel* sends nothing)

**Collects what `updateWorkOrder` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | How the maintenance head confirms a `suggestWorkOrderAssignee` candidate (M17-13). | `updateWorkOrder` body |
| Priority `priority` | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | — | `updateWorkOrder` body |
| Required qualification codes `requiredQualificationCodes` | list of values (chips) | optional | — | at most 10 | — | — | `updateWorkOrder` body |
| Due at `dueAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateWorkOrder` body |
| Description `description` | text area | optional | — | max length 5000 | — | — | `updateWorkOrder` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateWorkOrder` body |

**Form: Pause work order** (modal, opened by *Pause work order*; *Pause work order* calls `pauseWorkOrder`, *Cancel* sends nothing)

**Collects what `pauseWorkOrder` sends before it is called.** Required: `reason` (awaitingParts, awaitingPermit, awaitingOutageWindow, awaitingSpecialist, endOfShift, safetyConcern, other). Optional: `note`, **required when the reason is Other** — the form will not confirm without it and the server refuses 400 (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Awaiting parts · Awaiting permit · Awaiting outage window · Awaiting specialist · End of shift · Safety concern · Other | — | — | `pauseWorkOrder` body |
| Note `note` | text area | optional | — | max length 300; Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real … | `pauseWorkOrder` body |
| Requisition `requisitionId` | picker: choose a requisition | optional | — | — | shows names, sends the id | Where a part was ordered, so the two are linked. | `pauseWorkOrder` body |

Errors to draw in the form: 400 Validation failed

**Form: Reject work order** (modal, opened by *Reject work order*; *Reject work order* calls `rejectWorkOrder`, *Cancel* sends nothing)

**Collects what `rejectWorkOrder` sends before it is called.** Required: `reason` (wrongSkill, notOnShift, wrongVenue, alreadyInHand, unsafe, other). Optional: `note`, **required when the reason is Other** — the form will not confirm without it and the server refuses 400 (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Wrong skill · Not on shift · Wrong venue · Already in hand · Unsafe · Other | — | — | `rejectWorkOrder` body |
| Note `note` | text area | optional | — | max length 300; Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real … | `rejectWorkOrder` body |

Errors to draw in the form: 400 Validation failed

**Form: Complete work order** (modal, opened by *Complete work order*; *Complete work order* calls `completeWorkOrder`, *Cancel* sends nothing)

**Collects what `completeWorkOrder` sends before it is called.** Required: `resolution`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Resolution `resolution` | text area | required | — | min length 3; max length 5000 | — | — | `completeWorkOrder` body |
| Resolution code `resolutionCode` | select | optional | — | Repaired · Part replaced · Adjusted · Cleaned · No fault found · Referred external · Replaced · Deferred | — | — | `completeWorkOrder` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `completeWorkOrder` body |
| Follow up required `followUpRequired` | toggle | optional | off | — | — | — | `completeWorkOrder` body |
| Follow up note `followUpNote` | text area | optional | — | max length 1000 | — | — | `completeWorkOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `completeWorkOrder` body |

Errors to draw in the form: 400 Completion photographs required for this category and none supplied

**Form: Close work order** (modal, opened by *Close work order*; *Close work order* calls `closeWorkOrder`, *Cancel* sends nothing)

**Collects what `closeWorkOrder` sends before it is called.** Required: `outcome` (completedAndVerified, notReproducible, supersededByReplacement, noLongerApplicable, duplicate). Optional: `note`, `duplicateOfWorkOrderId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | radio group | required | — | Completed and verified · Not reproducible · Superseded by replacement · No longer applicable · Duplicate | — | — | `closeWorkOrder` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `closeWorkOrder` body |
| Duplicate of work order `duplicateOfWorkOrderId` | picker: choose a duplicate of work order | optional | — | — | shows names, sends the id | — | `closeWorkOrder` body |

**Sent by *Cancel work order*** (`cancelWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | radio group | required | — | Raised in error · Duplicate · Superseded · No longer required | — | — | `cancelWorkOrder` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `cancelWorkOrder` body |
| Superseded by work order `supersededByWorkOrderId` | picker: choose a superseded by work order | optional | — | — | shows names, sends the id | — | `cancelWorkOrder` body |

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

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Raise work order**: Photo-first: photos at the top, then title, asset (scan or pick), location, fault assessment (what is affected - safety, guest operations, revenue), required skills, due date; Priority left empty by default with "Will be scored"; choosing one marks it Manual. "Take the asset out of service now" toggle for faults on a live ride. *(source: contracts/satellite/maintenance.yaml#createWorkOrder / DI-923 / DI-232)*
- **Pause / Reject reasons**: Closed lists (Awaiting parts, permit, outage window, specialist, end of shift, safety concern, other / Wrong skill, not on shift, wrong venue, already in hand, unsafe, other); Other requires a note. *(source: contracts/satellite/maintenance.yaml#pauseWorkOrder / contracts/satellite/maintenance.yaml#rejectWorkOrder)*
- **Cancel reason**: Raised in error / Duplicate / Superseded (pick the superseding work order) / No longer required; not offered once work has started. *(source: contracts/satellite/maintenance.yaml#cancelWorkOrder)*
- **Close outcome**: Completed and verified / Not reproducible / Superseded by replacement / No longer applicable / Duplicate. *(source: contracts/satellite/maintenance.yaml#closeWorkOrder)*

#### Outputs: what the screen shows and produces

**Shown**

**Every work order** (data table, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Elapsed minutes | 1,234 | Labour minutes accumulated up to the last pause or stop. Maintained on write by `recordWorkOrderTime`, `pauseWorkOrder` and … |

**The selected work order** (detail panel, from `getWorkOrder`)

| Shows | Format | Notes |
|---|---|---|
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Description | text | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Location description | text | Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor. |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |
| Resolution code | chip: Repaired, Part replaced, Adjusted, Cleaned, No fault found, Referred external… | — |

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Raise work order (primary button) | `createWorkOrder` POST `/work-orders` | CreateWorkOrderRequest | WorkOrder | 400 Validation failed | opens modal first |
| Save work order (secondary button) | `updateWorkOrder` PATCH `/work-orders/{workOrderId}` | inline | WorkOrder | — | opens modal first |
| Pause work order (secondary button) | `pauseWorkOrder` POST `/work-orders/{workOrderId}/pause` | inline | WorkOrder | 400 Validation failed | opens modal first |
| Reject work order (secondary button) | `rejectWorkOrder` POST `/work-orders/{workOrderId}/reject` | inline | WorkOrder | 400 Validation failed | opens modal first |
| Complete work order (secondary button) | `completeWorkOrder` POST `/work-orders/{workOrderId}/complete` | inline | WorkOrder | 400 Completion photographs required for this category and none supplied | opens modal first |
| Close work order (secondary button) | `closeWorkOrder` POST `/work-orders/{workOrderId}/close` | inline | WorkOrder | — | opens modal first |
| Cancel work order (destructive button) | `cancelWorkOrder` POST `/work-orders/{workOrderId}/cancel` | inline | WorkOrder | 409 Labour time or a part is already recorded against it (`work-recorded`; CHG-RUL-010). | — |
| Assign suggested technician (secondary button) | `updateWorkOrder` PATCH `/work-orders/{workOrderId}` | inline | WorkOrder | — | opens modal first |
| Request a vendor (secondary button) | `createVendorServiceRequest` POST `/vendor-service-requests` | VendorServiceRequest | VendorServiceRequest | 400 Validation failed; 409 The work order is closed or cancelled. | — |
| Update vendor request (secondary button) | `updateVendorServiceRequest` PATCH `/vendor-service-requests/{vendorServiceRequestId}` | inline | VendorServiceRequest | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The request is already `completed` or `cancelled`. | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **List and calendar**: List (default) with a Calendar toggle - Day (hours from the venue day start), Week, Month, Agenda - filtered by asset category for the team. *(source: DI-908 / contracts/satellite/maintenance.yaml#listWorkOrders)*
- **Row**: Number, title, asset, kind, priority badge plus source tag (Scored 78 / Asset override / Manual), status step, assignee name, due and overdue flag, elapsed timer. *(source: DI-923 / DI-231 / contracts/satellite/maintenance.yaml#listWorkOrders)*
- **Suggested technicians**: Ranked list with all-skills tick or missing skills named, on-shift, open jobs; an Assign button per row; no auto-assign. *(source: DI-924 / contracts/satellite/maintenance.yaml#suggestWorkOrderAssignee)*
- **Vendor requests**: Supplier, scope, status, vendor reference, quoted cost (AED), visit time. *(source: contracts/satellite/maintenance.yaml#listVendorServiceRequests)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Assign**: Sets the assignee; the job shows "Assigned - not yet accepted" until the technician accepts on the Staff App. *(source: contracts/satellite/maintenance.yaml#updateWorkOrder / contracts/satellite/maintenance.yaml#acceptWorkOrder)*
- **Complete**: Requires a resolution and, where the category demands, completion photos; does not return the asset to service. *(source: contracts/satellite/maintenance.yaml#completeWorkOrder)*

**Data it reads**: `listWorkOrders` (onLoad, Maintenance work orders at the venue (rebound 28 September …)

**Where the user goes next**

- → `BO-036` Device Registry: *The till is confirmed healthy again*
- → `BO-108` Venue Operations: *Venue Operations*
- → `BO-030` Work Order Verification: *Verify the completed work*; carries `workOrderId`; calls `completeWorkOrder`
- → `BO-071` Planned Maintenance: *Planned maintenance*
- → `BO-072` Incident Log: *Incident log*
- → `BO-069` Asset Register: *Open the asset*; carries `assetId`

**What opens over it**

- confirmDialog *Cancel work order*: **Names what `cancelWorkOrder` changes and what it leaves alone.** Required: `reason` (raisedInError, duplicate, superseded, noLongerRequired).

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The work orders list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the work orders untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No work orders yet. Offers Raise work order (`createWorkOrder`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on status, priority, assignedToPrincipalId, assetId and overdueOnly; the work orders are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORK_ORDER_VIEW`, which `listWorkOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MAINTENANCE_APPROVE` for `closeWorkOrder`; `MAINTENANCE_EXECUTE` for `pauseWorkOrder`, `rejectWorkOrder`; `WORK_ORDER_MANAGE` for … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Completion photographs required for this category and none supplied; 400 Validation failed; 409 Labour time or a part is already recorded against it (`work-recorded`; CHG-RUL-010).; 409 The request is already `completed` or `cancelled`. |

#### Edge cases to draw

- **Parts needed**: Parts are reserved from the general inventory; when short, the refusal names the part; reserve is hidden offline. *(source: DI-925 / TRACKER Actions row 304)*
- **Raised offline from the Staff App**: Appears with "Recorded offline 10:12, synced 10:40". *(source: contracts/satellite/maintenance.yaml#createWorkOrder)*

#### Consistency with other screens

- Match `EMP-004`: Technician task list on the Staff App shows the same statuses and timer.
- Match `BO-030`: Completed jobs needing verification flow to BO-030.
- Match `BO-069`: Priority override comes from the asset.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
workOrders:
- wo: WO-2026-01482
  title: Restraint bar R3 not locking
  asset: Falcon Coaster
  priority: Emergency - Asset override
  status: In progress
  assignee: Rahul Menon
  elapsed: 1 h 12 min
- wo: WO-2026-01490
  title: Gate 2 reader intermittent
  asset: Main Plaza Gate 2 turnstile
  priority: High - Scored 78
  status: Assigned - not accepted
  assignee: Omar Haddad
  due: 1 Oct 2026 14:00
- wo: WO-2026-01491
  title: Chiller 2 noise
  asset: Plant room chiller 2
  priority: Normal - Manual
  status: Awaiting parts
  vendor: Gulf Cooling LLC, quote AED 4,200
```

#### Permissions

- `suggestWorkOrderAssignee` → `WORK_ORDER_VIEW` (read) · staff
- `listVendorServiceRequests` → `WORK_ORDER_VIEW` (read) · staff
- `createVendorServiceRequest` → `WORK_ORDER_MANAGE` (configure) · staff
- `updateVendorServiceRequest` → `WORK_ORDER_MANAGE` (configure) · staff
- `listWorkOrders` → `WORK_ORDER_VIEW` (read) · staff
- `getWorkOrder` → `WORK_ORDER_VIEW` (read) · staff
- `createWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `updateWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `pauseWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `rejectWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `completeWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `closeWorkOrder` → `MAINTENANCE_APPROVE` (operate) · staff
- `cancelWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `WORK_ORDER_VIEW`, which `listWorkOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `MAINTENANCE_APPROVE` for `closeWorkOrder`; `MAINTENANCE_EXECUTE` for `pauseWorkOrder`, `rejectWorkOrder`; `WORK_ORDER_MANAGE` for …

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| 17.3.4 | Root Cause Analysis - System shall support root cause analysis. | Maintenance & Safety Management | CONTRACTED | data `WorkOrder` |
| 17.3.5 | Maintenance Escalation - System shall support maintenance escalation workflows. | Maintenance & Safety Management | CONTRACTED | data `WorkOrder` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Smart assignment (confirmed by the maintenance head): technicians ranked by skill, shift and load; the ranking assigns nothing and Assign on a row does; outside vendor requests listed on the work order. *(agreed · MoM 17 Sep 2026, M17-13 · DI-924)*
- Work-order priority is shown with its source side by side (scored by venue policy, asset override, or manual); an asset carries a "fault priority override"; a new work order leaves priority empty to be scored; the venue sets weights and bands (safety, guest operations, revenue, asset criticality, summing to 100). *(agreed · MoM 17 Sep 2026, M17-01 · DI-923)*
- Work orders assigned to a technician must be visible on a technician-facing mobile app so field staff see assigned tasks and act directly from their device; execution shows a repair checklist, spare parts/tools consumed, a timeline (assigned, started, part requests) and a functional-test checklist before completion. *(client request · MoM 17 Sep 2026, 4.4 Work Order Management & Execution · DI-911)*
- Corrective-maintenance priority combines a configurable weighted scoring model (e.g. P1 emergency when guest operations are affected) with a direct per-asset priority override field: "if this specific device goes down, raise this priority level". *(agreed · MoM 17 Sep 2026, 4.3 Corrective & Emergency Maintenance · DI-909)*
- Calendars must support filtering by asset category so a team only sees maintenance relevant to them, e.g. an IT team sees turnstiles, printers and POS terminals, not unrelated categories. *(agreed · MoM 17 Sep 2026, 4.2 Preventive Maintenance Planning · DI-908)*
- Device maintenance: preventive cycles (quarterly, half-yearly, seasonal) on a calendar by device type; staff log faulty devices which raise work orders; diagnostic workspace for the engineer; warranty and maintenance history; return to service. *(client request · MoM 15 Sep 2026, 4.6 Device Maintenance & Lifecycle Servicing · DI-902)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A297** Build asset registry and preventive maintenance planning *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'preventive maintenance')*
- **A299** Build work orders, safety inspections and incident management *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'work order')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-070` · status **notStarted** · provenance generated
- Flow F95 *A fleet is watched, a fault is found, and a station is fixed*, step 3: A work order is raised to fix it. → **Fixed, and known to be fixed.** A printer swapped without a work order is a repair nobody can count.

#### Acceptance for the design

- [ ] Every input above is drawn (61), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (31 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-070?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Raise work order, Save work order, Pause work order, Reject work order, Complete work order, Close work order, Cancel work order, Assign suggested technician, Request a vendor, Update vendor request.
- [ ] Every transition is wired: `BO-036`, `BO-108`, `BO-030`, `BO-071`, `BO-072`, `BO-069`.
- [ ] Every gated control is gated: `MAINTENANCE_APPROVE`, `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VIEW`.
- [ ] The 6 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-100` Venue Home

**The screen a venue manager opens in the morning, and the only way into everything else.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE`, `REPORT_VIEW_WORKSTATION`, `TENANT_VIEW` (2 operate, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listShifts` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: **Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more … |
| Route | `/home` |

**What the spec says about it.** **Built 20 August because P08 had none.** `BO-001 Queue Directory` was the declared entry point to a 99-screen back office — it exits to four queue screens, and **93 screens hung off nothing.** A back office entered through a queue list. **The module was also one bucket holding 72 of 99 screens**, so there was nothing for a home screen to point at; sections were derived from the contract each screen principally calls. **Takings, defined** (decided 2 October 2026, Chinmay; CHG-FIN-010; resolves the contradiction "gross value of payments" against "payments less refunds"). Takings is the money taken through the tills and channels less the money paid back, by tender, VAT included: a cash-control figure, not revenue. It is what a drawer and a settlement are reconciled against, and for a till shift it is the hidden half of the blind count: float plus cash takings is the expected cash, which the cashier never sees (CHG-FIN-003; MoM 9 Sep 2026 4.18). On this hub the tile reads "Takings today" from the seeded `takings` KPI and is never labelled revenue.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The screen a venue manager opens every morning and the way into everything else: today's takings and admissions, open shifts, alerts, and the sections they may use. The one thing to get right: the tiles show only what the platform computes (takings and admissions), with their freshness; the Vision Book's other cards wait for a source rather than showing invented numbers.

**Fixed on main** (the package already carries these; draw what it says): The takings definition says both "gross value of payments" and "payments less refunds". (CHG-FIN-010).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **The Vision Book shows net profit, average order value, live visitors with capacity, AI insights and sales by channel on this screen. Which come back, and from what?** → Drawn default accepted: Takings and admissions only (R283); the others as an open placeholder list. *(decided by Chinmay, 2026-10-02; DEC-355 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

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
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Venue**: Asked first for someone with more than one venue; remembered. *(source: screens/P08-venue-back-office.yaml#BO-100)*

#### Outputs: what the screen shows and produces

**Shown**

**Every shift** (data table, from `listShifts`)

| Shows | Format | Notes |
|---|---|---|
| Principal display name | text | — |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |

**Takings and admissions today** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=takings,admissions`. Takings: money taken less money paid back, VAT included, a cash-control figure and not revenue (CHG-FIN-010).

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Period | text | — |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Open shifts** (metric tile): Open shifts today, from `listShifts`. **Items needing attention are dropped until a summary operation exists** (decided 28 September, audit R283).

**Card list** (card list): One card per section. **No attention counts** until a summary operation exists to supply them (decided 28 September, audit R283); a count nothing computes would be a guess.

**Banner** (banner): Alerts that crossed a threshold, from VenueSettings.alerting. **On-platform and markable as read** (CF-134).

**The selected shift** (detail panel, from `listShifts`)

| Shows | Format | Notes |
|---|---|---|
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Deposit box code | text | — |
| Bag number | text | — |
| Sales total | AED 1,234.50 | What the till took in sales, as the guest paid it — tax included: the shift's takings, not Gross sales (CHG-FIN-002, CHG-FIN-010). |
| Refunds total | AED 1,234.50 | What the till paid back, as the guest was refunded it — tax included. |
| Lifts total | AED 1,234.50 | Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net. |

**The venue settings** (detail panel, from `getVenueSettings`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | From the path of `setVenueSettings`. |
| Currency code | text | `readOnly` is the freeze. `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the … |
| Currency scale | 1,234 | Scale travels with currency (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency … |
| Support hours | grouped details | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. |
| Quiet hours | grouped details | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. |
| Biometrics | grouped details | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. |
| Segregated access | grouped details | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a … |
| Alerting | grouped details | CF-134. On-platform notification, marked as read. |

**Tree nav** (tree nav): The eight sections. **Persistent — a back office is a place somebody works all day**, and a nav that disappears on every detail screen makes them use the browser back button as navigation.

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Greeting and date**: "Good morning, Ahmed" with the venue and today's date in the venue's time zone. *(source: DI-028)*
- **Takings tile**: "Takings today" (money received less refunds), never "Revenue"; comparison with the same weekday last week, the target status where a target exists, and "as of" with a stale warning. *(source: contracts/satellite/reporting.yaml#/components/schemas/ReportingSystemKpi / contracts/satellite/reporting.yaml#/components/schemas/KpiValue / R283)*
- **Admissions tile**: Admitted today; same comparison and freshness. *(source: R283)*
- **Open shifts**: Count of shifts open now, from the shift list. *(source: screens/P08-venue-back-office.yaml#BO-100)*
- **Sections**: Only sections the person may open; no attention counts. *(source: R283 / DI-387)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Open a tile**: Takings opens the sales report; admissions opens attendance. *(source: DI-709)*

**Data it reads**: `getKpiValues` (onLoad, Today's takings and admissions tiles — …); `getVenueSettings` (onLoad, What this venue is configured to do); `listShifts` (onLoad, Who is on and what has been taken)

**Where the user goes next**

- → `BO-364` Approval Command Center Dashboard: *Approval Command Center Dashboard*
- → `BO-374` Approval Decision Workspace: *Approval Decision Workspace*
- → `BO-384` Delegation & Escalation Command Center: *Delegation & Escalation Command Center*
- → `BO-101` Orders & Money: *Orders & Money*
- → `BO-102` Sell: *Sell*
- → `BO-103` Access & Venue: *Access & Venue*
- → `BO-104` Food & Beverage: *Food & Beverage*
- → `BO-105` Stock & Supply: *Stock & Supply*
- → `BO-106` People & Access Rights: *People & Access Rights*
- → `BO-107` Guests & Marketing: *Guests & Marketing*
- → `BO-108` Venue Operations: *Venue Operations*
- → `BO-394` Game & Ride Operations Dashboard: *Game & Ride Operations Dashboard*
- → `BO-484` Self-Service Experience Command Center: *Self-Service Experience Command Center*
- → `BO-404` Reader Management Dashboard: *Reader Management Dashboard*
- → `BO-414` Wallet & Credit Management Dashboard: *Wallet & Credit Management Dashboard*
- → `BO-424` Gameplay Validation Command Center: *Gameplay Validation Command Center*
- → `BO-434` Game & Ride Pricing Command Center: *Game & Ride Pricing Command Center*
- → `BO-444` Redemption Operations Dashboard: *Redemption Operations Dashboard*
- → `BO-454` Card Lifecycle Command Center: *Card Lifecycle Command Center*
- → `BO-464` Game & Ride Operations Control Center: *Game & Ride Operations Control Center*
- → `BO-474` Reader Integration Command Center: *Reader Integration Command Center*
- → `BO-494` Rental Product Command Center: *Rental Product Command Center*
- → `BO-584` Rental Executive Command Center: *Rental Executive Command Center*
- → `BO-504` Rental Inventory Command Center: *Rental Inventory Command Center*
- → `BO-514` Availability Command Center: *Availability Command Center*
- → `BO-524` Rental Pricing Command Center: *Rental Pricing Command Center*
- → `BO-534` Rental Booking Command Center: *Rental Booking Command Center*
- → `BO-544` Rental Checkout Command Center: *Rental Checkout Command Center*
- → `BO-554` Active Rental Operations Command Center: *Active Rental Operations Command Center*
- → `BO-564` Rental Return Command Center: *Rental Return Command Center*
- → `BO-574` Maintenance Command Center: *Maintenance Command Center*
- → `BO-595` AI Setup Command Center: *AI Setup Command Center*
- → `BO-605` Go-Live Readiness Command Center: *Go-Live Readiness Command Center*
- → `BO-594` Environment Ready & Handoff to AI Setup: *Environment Ready & Handoff to AI Setup*
- → `BO-615` Accreditation Command Center: *Accreditation Command Center*
- → `BO-625` Accreditation Holder Directory: *Accreditation Holder Directory*
- → `BO-635` Accreditation Review Queue: *Accreditation Review Queue*
- → `BO-644` Credential Issuance Command Center: *Credential Issuance Command Center*
- → `BO-654` Accreditation Access Command Center: *Accreditation Access Command Center*
- → `BO-664` Accreditation Lifecycle Command Center: *Accreditation Lifecycle Command Center*
- → `BO-674` Accreditation Communications Command Center: *Accreditation Communications Command Center*
- → `BO-684` Accreditation Executive Dashboard: *Accreditation Executive Dashboard*
- → `BO-694` Event Catalogue Command Center: *Event Catalogue Command Center*
- → `BO-697` Event Schedule Command Center: *Event Schedule Command Center*
- → `BO-700` Venue & Space Command Center: *Venue & Space Command Center*
- → `BO-703` Seating & Capacity Command Center: *Seating & Capacity Command Center*
- → `BO-706` Registration & Attendance Command Center: *Registration & Attendance Command Center*
- → `BO-710` Event Resource Command Center: *Event Resource Command Center*
- → `BO-716` Event Lifecycle & Change Command Center: *Event Lifecycle & Change Command Center*
- → `BO-721` Activity Performance & Slot Template Configuration: *Activity Performance & Slot Template Configuration*
- → `BO-725` Performance Operations Command Center: *Performance Operations Command Center*
- → `BO-727` F&B Command Center: *F&B Command Center*
- → `BO-734` CRM Command Center: *CRM Command Center*
- → `BO-824` Gamification Command Center: *Gamification Command Center*
- → `BO-834` Digital Experience Center: *Digital Experience Center*
- → `BO-844` Waiver Command Center: *Waiver Command Center*
- → `BO-744` Data Governance Center: *Data Governance Center*
- → `BO-754` Audience Intelligence: *Audience Intelligence*
- → `BO-764` Campaign Command Center: *Campaign Command Center*
- → `BO-774` Journey Automation Center: *Journey Automation Center*
- → `BO-784` Communications Center: *Communications Center*
- → `BO-794` Omnichannel Command Center: *Omnichannel Command Center*
- → `BO-804` Case Command Center: *Case Command Center*
- → `BO-814` Voice of Customer Center: *Voice of Customer Center*
- → `BO-854` Resource Management Command Center: *Resource Management Command Center*
- → `BO-943` Resource Analytics Command Center: *Resource Analytics Command Center*
- → `BO-864` Resource Calendar Command Center: *Resource Calendar Command Center*
- → `BO-873` Staff Resource Directory: *Staff Resource Directory*
- → `BO-883` Workforce Roster Command Center: *Workforce Roster Command Center*
- → `BO-893` Experience Resource Requirement Builder: *Experience Resource Requirement Builder*
- → `BO-903` Equipment & Asset Command Center: *Equipment & Asset Command Center*
- → `BO-913` Event Resource Planning Command Center: *Event Resource Planning Command Center*
- → `BO-923` AI Resource Intelligence Command Center: *AI Resource Intelligence Command Center*
- → `BO-933` My Resource Operations Home: *My Resource Operations Home*
- → `BO-953` Seat Map Command Center: *Seat Map Command Center*
- → `BO-1043` Revenue Command Center: *Revenue Command Center*
- → `BO-1051` Seat Analytics Command Center: *Seat Analytics Command Center*
- → `BO-1061` Platform Command Center: *Platform Command Center*
- → `BO-1071` Integration Command Center: *Integration Command Center*
- → `BO-963` Import Command Center: *Import Command Center*
- → `BO-973` Layout Command Center: *Layout Command Center*
- → `BO-983` Inventory Command Center: *Inventory Command Center*
- → `BO-993` Experience Command Center: *Experience Command Center*
- → `BO-1003` Hold Command Center: *Hold Command Center*
- → `BO-1013` Rules Command Center: *Rules Command Center*
- → `BO-1023` Group Reservation Center: *Group Reservation Center*
- → `BO-1033` Recommendation Command Center: *Recommendation Command Center*
- → `BO-1081` Finance Dashboard: *Finance Dashboard*
- → `BO-1082` Admissions Revenue: *Admissions Revenue*
- → `BO-1083` Wallet Command Center: *Wallet Command Center*
- → `BO-1173` Wallet Integration Command Center: *Wallet Integration Command Center*
- → `BO-1093` Funding Command Center: *Funding Command Center*
- → `BO-1103` Stored Value & Credit Command Center: *Stored Value & Credit Command Center*
- → `BO-1113` Shared Wallet Command Center: *Shared Wallet Command Center*
- → `BO-1123` Gift Card & Digital Benefit Command Center: *Gift Card & Digital Benefit Command Center*
- → `BO-1133` Wallet Usage & Channel Command Center: *Wallet Usage & Channel Command Center*
- → `BO-1143` Wallet Operations Command Center: *Wallet Operations Command Center*
- → `BO-1153` Wallet Security & Risk Command Center: *Wallet Security & Risk Command Center*
- → `BO-1163` Wallet Finance & Liability Command Center: *Wallet Finance & Liability Command Center*
- → `BO-144` Access Control Command Center: *Access Control Command Center*
- → `BO-154` Access Rule Command Center: *Access Rule Command Center*
- → `BO-164` Digital Credential Security Command Center: *Digital Credential Security Command Center*
- → `BO-174` Media & Credential Command Center: *Media & Credential Command Center*
- → `BO-184` Biometric Access Command Center: *Biometric Access Command Center*
- → `BO-194` Device & Gate Command Center: *Device & Gate Command Center*
- → `BO-204` Offline & Edge Operations Command Center: *Offline & Edge Operations Command Center*
- → `BO-214` Guest Journey Command Center: *Guest Journey Command Center*
- → `BO-224` Live Access Operations Command Center: *Live Access Operations Command Center*
- → `BO-234` Dynamic Access Policy Command Center: *Dynamic Access Policy Command Center*
- → `BO-244` Access Security & Fraud Command Center: *Access Security & Fraud Command Center*
- → `BO-254` Access Monitoring & Analytics Command Center: *Access Monitoring & Analytics Command Center*
- → `BO-264` Group Sales Command Center: *Group Sales Command Center*
- → `BO-274` Group Booking Operations Command Center: *Group Booking Operations Command Center*
- → `BO-284` Membership & Annual Pass Command Center: *Membership & Annual Pass Command Center*
- → `BO-294` Member Operations Command Center: *Member Operations Command Center*
- → `BO-304` Order & Reservation Command Center: *Order & Reservation Command Center*
- → `BO-314` Amendment & After-Sales Command Center: *Amendment & After-Sales Command Center*
- → `BO-324` Payment & Order Financial Command Center: *Payment & Order Financial Command Center*
- → `BO-334` Virtual Ticket Command Center: *Virtual Ticket Command Center*
- → `BO-344` Media Design Studio Command Center: *Media Design Studio Command Center*
- → `BO-354` Credential Operations Command Center: *Credential Operations Command Center*
- → `ADM-048` Commercial Pricing Command Center: *Commercial Pricing Command Center*
- → `ADM-058` Pricing Rule Command Center: *Pricing Rule Command Center*
- → `ADM-078` Pricing Governance Command Center: *Pricing Governance Command Center*
- → `ADM-088` Dynamic Pricing Strategy Command Center: *Dynamic Pricing Strategy Command Center*
- → `ADM-098` AI Pricing Intelligence Command Center: *AI Pricing Intelligence Command Center*
- → `ADM-108` Revenue Optimization Command Center: *Revenue Optimization Command Center*
- → `ADM-118` Product Lifecycle Command Center: *Product Lifecycle Command Center*
- → `ADM-128` Product Governance Command Center: *Product Governance Command Center*
- → `ADM-138` Promotion Command Center Dashboard: *Promotion Command Center Dashboard*
- → `ADM-148` Promotion Rule Builder: *Promotion Rule Builder*
- → `ADM-158` Coupon & Promo Code Command Center: *Coupon & Promo Code Command Center*
- → `ADM-168` Advanced Offer Command Center: *Advanced Offer Command Center*
- → `ADM-178` Bundle & Combo Command Center: *Bundle & Combo Command Center*
- → `ADM-188` Dynamic Bundle Operations Command Center: *Dynamic Bundle Operations Command Center*
- → `ADM-198` Targeting & Eligibility Command Center: *Targeting & Eligibility Command Center*
- → `ADM-208` Stacking & Conflict Command Center: *Stacking & Conflict Command Center*
- → `ADM-218` Campaign Governance & Budget Command Center: *Campaign Governance & Budget Command Center*
- → `ADM-228` Promotion Performance Command Center: *Promotion Performance Command Center*
- → `ADM-238` Rules & Workflow Command Center: *Rules & Workflow Command Center*
- → `ADM-248` Workflow Operations Command Center: *Workflow Operations Command Center*
- → `ADM-258` Sales Channel Command Center: *Sales Channel Command Center*
- → `ADM-268` Channel Operations Command Center: *Channel Operations Command Center*
- → `ADM-278` Resale Marketplace Command Center: *Resale Marketplace Command Center*
- → `ADM-288` Resale Operations Command Center: *Resale Operations Command Center*
- → `ADM-298` My Tickets & Resale Marketplace Entry: *My Tickets & Resale Marketplace Entry*
- → `ADM-308` Upgrade & Conversion Command Center: *Upgrade & Conversion Command Center*
- → `ADM-559` Payment Command Center: *Payment Command Center*
- → `ADM-569` Payment Orchestration Command Center: *Payment Orchestration Command Center*
- → `ADM-579` Terminal & Card-Present Command Center: *Terminal & Card-Present Command Center*
- → `ADM-589` Digital Payments Command Center: *Digital Payments Command Center*
- → `ADM-599` Mixed Tender & Credit Command Center: *Mixed Tender & Credit Command Center*
- → `ADM-609` Refund & Payment Adjustment Command Center: *Refund & Payment Adjustment Command Center*
- → `ADM-629` Payment Risk & Fraud Command Center: *Payment Risk & Fraud Command Center*
- → `ADM-639` Recommendation Command Center: *Recommendation Command Center*
- → `ADM-649` Upsell & Upgrade Command Center: *Upsell & Upgrade Command Center*
- → `ADM-659` Cross-Sell Command Center: *Cross-Sell Command Center*
- → `ADM-669` Journey & Context Command Center: *Journey & Context Command Center*
- → `ADM-679` Personalization & NBO Command Center: *Personalization & NBO Command Center*
- → `ADM-689` Recommendation Performance Command Center: *Recommendation Performance Command Center*
- → `ADM-069` Tax Profile & Jurisdiction Configuration: *Tax Profile & Jurisdiction Configuration*
- → `ADM-070` Tax Rule & Treatment Builder: *Tax Rule & Treatment Builder*
- → `ADM-071` Fee & Surcharge Library: *Fee & Surcharge Library*
- → `ADM-072` Fee Applicability & Charging Rule Builder: *Fee Applicability & Charging Rule Builder*
- → `ADM-073` Fee Waiver, Tax Exemption & Exception Rules: *Fee Waiver, Tax Exemption & Exception Rules*
- → `ADM-074` Price Calculation Sequence & Formula Engine: *Price Calculation Sequence & Formula Engine*
- → `ADM-075` Currency Precision, Rounding & Monetary Rules: *Currency Precision, Rounding & Monetary Rules*
- → `ADM-076` Price Breakdown, Calculation Simulation & Explainability: *Price Breakdown, Calculation Simulation & Explainability*
- → `ADM-077` Calculation Validation, Reconciliation & Service Interface: *Calculation Validation, Reconciliation & Service Interface*
- → `ADM-620` Reconciliation Source & Import Manager: *Reconciliation Source & Import Manager*
- → `ADM-621` Transaction Matching & Reconciliation Engine: *Transaction Matching & Reconciliation Engine*
- → `ADM-622` Reconciliation Exception & Investigation Center: *Reconciliation Exception & Investigation Center*
- → `ADM-623` Settlement & Payout Manager: *Settlement & Payout Manager*
- → `ADM-624` Fees, Commission, FX & Settlement Economics: *Fees, Commission, FX & Settlement Economics*
- → `ADM-625` Merchant Account & Settlement Calendar Manager: *Merchant Account & Settlement Calendar Manager*
- → `ADM-626` Settlement Posting, Finance Handoff & Close Manager: *Settlement Posting, Finance Handoff & Close Manager*
- → `ADM-627` Reconciliation Audit, Trace & Evidence Center: *Reconciliation Audit, Trace & Evidence Center*
- → `ADM-628` Reconciliation Simulator, Forecast & AI Operations Advisor: *Reconciliation Simulator, Forecast & AI Operations Advisor*
- → `ADM-038` Communication Service Command Center: *Communication Service Command Center*
- → `ADM-319` Approval Workflow Library: *Approval Workflow Library*
- → `ADM-329` Approval Matrix Command Center: *Approval Matrix Command Center*
- → `ADM-339` Governance & Compliance Command Center: *Governance & Compliance Command Center*
- → `ADM-349` Approval Integration Command Center: *Approval Integration Command Center*
- → `ADM-359` Approval Executive KPI Dashboard: *Approval Executive KPI Dashboard*
- → `PTR-026` Territory, Market & Distribution Rights: *Territory, Market & Distribution Rights*
- → `PTR-029` Partner Access, Roles & Permission Profile: *Partner Access, Roles & Permission Profile*
- → `PTR-035` Commission, Margin & Incentive Management: *Commission, Margin & Incentive Management*
- → `PTR-036` Credit Limit & Exposure Management: *Credit Limit & Exposure Management*
- → `PTR-037` Deposit, Guarantee & Financial Security Management: *Deposit, Guarantee & Financial Security Management*
- → `PTR-039` Commercial Allocation, Quota & Commitment Management: *Commercial Allocation, Quota & Commitment Management*
- → `PTR-047` Partner Reconciliation & Exception Management: *Partner Reconciliation & Exception Management*
- → `PTR-048` Commission Calculation & Settlement Management: *Commission Calculation & Settlement Management*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tiles render in place; each resolves on its own so one slow source does not hold the page. |
| Error (`?state=error`) | Could not load the summary. **Every section is still reachable** — this screen is a landing page, and a failed tile must not block navigation. |
| Empty, first run (`?state=emptyFirstRun`) | **A venue on its first morning.** No shifts, no orders, no stock. The state links to the opening checklist rather than showing eight empty tiles — **a dashboard of zeroes teaches a new manager nothing.** |
| Empty, no results (`?state=emptyNoResults`) | Nothing happened in the window selected. Yesterday and today are the useful defaults. |
| Permission denied (`?state=emptyNoAccess`) | **Sections you cannot open are not shown.** A manager with no finance permission sees seven sections, not eight greyed out — a menu that lists what you may not do is a menu that invites a support ticket. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **First morning of a new venue**: The opening checklist instead of zero tiles. *(source: screens/P08-venue-back-office.yaml#BO-100 / DI-038)*
- **A manager without finance rights**: The takings tile and the finance section are absent, not greyed. *(source: DI-387 / DI-248)*

#### Consistency with other screens

- Match `ANL-001`: The executive board carries the wider KPI set; the same takings figure appears there.
- Match `BO-106`: Hubs reuse these two tiles.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
greeting: Good morning, Ahmed · Aquaventure Waterpark · Thursday 1 October 2026
tiles:
- Takings today AED 142,880.00 · +6.4% vs last Thursday · as of 11:42
- Admissions 6,214 · +3.1%
- Open shifts 14
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `getVenueSettings` → `TENANT_VIEW` (read) · staff
- `listShifts` → `REPORT_VIEW_WORKSTATION` (operate) · staff

**A refused user sees:** **Sections you cannot open are not shown.** A manager with no finance permission sees seven sections, not eight greyed out — a menu that lists what you may not do is a menu that invites a support ticket.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.44 | Incident & Exception Logging | Ticketing Sales | CONTRACTED | data `Shift` |
| 3.2.45 | Face Pass and Face Tag should support automatic gender recognition and reject customers who do not match the designated gender segment. | Admission and Access | CONTRACTED_PARTIAL | data `VenueSettings` |
| 3.2.46 | Face Pass shouldt restrict male guests attempting to enter during Friday Ladies Night, which needs to be validated with rule-based facial recognition validation. | Admission and Access | CONTRACTED | data `VenueSettings` |
| 8.9.3 | System shall display queue lengths, estimated wait times, queue utilization, queue alerts, and queue prediction metrics. | Unified Operations Dashboard | CONTRACTED | data `VenueSettings` |
| 11.1.15 | Approval Breach Alerts - System shall notify users when approval SLA thresholds are exceeded. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.17 | Approval Notifications - System shall notify approvers when new approval requests are assigned. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.18 | Approval Reminder Notifications - System shall send reminder notifications for pending approvals. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.19 | Approval Outcome Notifications - System shall notify requestors when approvals are approved, rejected or escalated. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 15.1.32 | Overstock Alerts - System shall generate overstock alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 15.1.33 | Stock Shortage Alerts - System shall generate stock shortage alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 15.1.34 | Expiry Alerts - System shall generate expiry alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 16.4.23 | Device Alerts - System shall generate device alerts. | Device Management | CONTRACTED | data `VenueSettings` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Offline policies and a venue-level Operations Summary dashboard aggregating department-level views into one venue overview. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-311)*
- The dashboard is the venue command centre: KPI cards (Total Revenue, Tickets Sold, Net Profit, Avg. Order Value, each with delta vs last 7 days); Live Visitors with capacity % and "Updated just now"; Revenue Overview (Day/Week/Month/Year); AI Insights (e.g. "Increase VIP ticket price by 8%"); Sales by Channel; Operational Status per area (Operational/Attention); Activity Feed; Top Events; At a Glance strip. *(agreed · Design Vision Book 29 Jul 2026, 04 Dashboard Vision (p4) - dashboard content · DI-031)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-100` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (29 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-100?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-364`, `BO-374`, `BO-384`, `BO-101`, `BO-102`, `BO-103`, `BO-104`, `BO-105`, `BO-106`, `BO-107`, `BO-108`, `BO-394`, `BO-484`, `BO-404`, `BO-414`, `BO-424`, `BO-434`, `BO-444`, `BO-454`, `BO-464`, `BO-474`, `BO-494`, `BO-584`, `BO-504`, `BO-514`, `BO-524`, `BO-534`, `BO-544`, `BO-554`, `BO-564`, `BO-574`, `BO-595`, `BO-605`, `BO-594`, `BO-615`, `BO-625`, `BO-635`, `BO-644`, `BO-654`, `BO-664`, `BO-674`, `BO-684`, `BO-694`, `BO-697`, `BO-700`, `BO-703`, `BO-706`, `BO-710`, `BO-716`, `BO-721`, `BO-725`, `BO-727`, `BO-734`, `BO-824`, `BO-834`, `BO-844`, `BO-744`, `BO-754`, `BO-764`, `BO-774`, `BO-784`, `BO-794`, `BO-804`, `BO-814`, `BO-854`, `BO-943`, `BO-864`, `BO-873`, `BO-883`, `BO-893`, `BO-903`, `BO-913`, `BO-923`, `BO-933`, `BO-953`, `BO-1043`, `BO-1051`, `BO-1061`, `BO-1071`, `BO-963`, `BO-973`, `BO-983`, `BO-993`, `BO-1003`, `BO-1013`, `BO-1023`, `BO-1033`, `BO-1081`, `BO-1082`, `BO-1083`, `BO-1173`, `BO-1093`, `BO-1103`, `BO-1113`, `BO-1123`, `BO-1133`, `BO-1143`, `BO-1153`, `BO-1163`, `BO-144`, `BO-154`, `BO-164`, `BO-174`, `BO-184`, `BO-194`, `BO-204`, `BO-214`, `BO-224`, `BO-234`, `BO-244`, `BO-254`, `BO-264`, `BO-274`, `BO-284`, `BO-294`, `BO-304`, `BO-314`, `BO-324`, `BO-334`, `BO-344`, `BO-354`, `ADM-048`, `ADM-058`, `ADM-078`, `ADM-088`, `ADM-098`, `ADM-108`, `ADM-118`, `ADM-128`, `ADM-138`, `ADM-148`, `ADM-158`, `ADM-168`, `ADM-178`, `ADM-188`, `ADM-198`, `ADM-208`, `ADM-218`, `ADM-228`, `ADM-238`, `ADM-248`, `ADM-258`, `ADM-268`, `ADM-278`, `ADM-288`, `ADM-298`, `ADM-308`, `ADM-559`, `ADM-569`, `ADM-579`, `ADM-589`, `ADM-599`, `ADM-609`, `ADM-629`, `ADM-639`, `ADM-649`, `ADM-659`, `ADM-669`, `ADM-679`, `ADM-689`, `ADM-069`, `ADM-070`, `ADM-071`, `ADM-072`, `ADM-073`, `ADM-074`, `ADM-075`, `ADM-076`, `ADM-077`, `ADM-620`, `ADM-621`, `ADM-622`, `ADM-623`, `ADM-624`, `ADM-625`, `ADM-626`, `ADM-627`, `ADM-628`, `ADM-038`, `ADM-319`, `ADM-329`, `ADM-339`, `ADM-349`, `ADM-359`, `PTR-026`, `PTR-029`, `PTR-035`, `PTR-036`, `PTR-037`, `PTR-039`, `PTR-047`, `PTR-048`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`, `REPORT_VIEW_WORKSTATION`, `TENANT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-108` Venue Operations

**Everything in venue operations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_VIEW`, `INCIDENT_VIEW`, `REPORT_VIEW_VENUE`, `WORK_ORDER_VIEW` (3 read, 1 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listWorkOrders` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: **Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more … |
| Route | `/venue-operations` |

**What the spec says about it.** Section landing. **6 screens reach the entry point through here** — before 20 August they reached it through nothing. **Given its section's own operations on 4 September.** It sat on `getVenueSettings` alone, which made it identical to every other section landing page — a hub that shows nothing of its section is a menu item, not a screen.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): A hub shows state and links; the venue settings panel does not belong on it and getVenueSettings carries no module enablement (R279) (design-notes correction …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The Venue Operations section landing: today's admissions and takings, open work orders by priority, open incidents (reportable ones first), assets out of service, and tiles into the section's screens (devices, F&B outlets, reporting, attendance, zones, integrations, work orders). The one thing to get right: what needs action now (emergency work orders, reportable incidents near deadline, rides out of service) comes before the menu.

**Fixed on main** (the package already carries these; draw what it says): Work-order filters as id text fields and the venue settings panel on a hub (CHG-WIR-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Assigned to principal id | picker: choose an assigned to principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?assignedToPrincipalId=` to `listWorkOrders`. | `listWorkOrders` ?assignedToPrincipalId |
| Status | select | optional | — | Open · Assigned · In progress · Paused · Awaiting parts · Completed · Verified · Closed · Cancelled | — | Sends `?status=` to `listWorkOrders`. | `listWorkOrders` ?status |
| Priority | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | Sends `?priority=` to `listWorkOrders`. | `listWorkOrders` ?priority |
| Asset id | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | Sends `?assetId=` to `listWorkOrders`. | `listWorkOrders` ?assetId |
| Overdue only | toggle | optional | off | — | — | Sends `?overdueOnly=` to `listWorkOrders`. | `listWorkOrders` ?overdueOnly |
| Search venue operations | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |
| From | date and time picker | — | — | `listWorkOrders` ?from |
| To | date and time picker | — | — | `listWorkOrders` ?to |
| Category | picker: choose a category | — | — | `listWorkOrders` ?categoryId |
| Severity | radio group | — | Near miss · Minor · Moderate · Major · Critical | `listIncidents` ?severity |
| Status | radio group | — | Reported · Under investigation · Action required · Closed | `listIncidents` ?status |
| Is reportable | toggle | — | — | `listIncidents` ?isReportable |
| Category | picker: choose a category | — | — | `listAssets` ?categoryId |
| Status | select | — | In service · Out of service · Under maintenance · Awaiting parts · Retired · Disposed | `listAssets` ?status |
| … 1 more | | | | `operations.json` |

#### Outputs: what the screen shows and produces

**Shown**

**Every work order** (data table, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |

**Every incident** (data table, from `listIncidents`)

| Shows | Format | Notes |
|---|---|---|
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Location description | text | — |
| Notification due at | 1 Oct 2026, 14:30 | — |
| Notified at | 1 Oct 2026, 14:30 | The earliest `notifiedAt` among this incident's authority notifications. Maintained on write by `recordAuthorityNotification`; each … |

**Every asset** (data table, from `listAssets`)

| Shows | Format | Notes |
|---|---|---|
| Asset tag | text | Unique per venue (decided 28 September, audit R108). Two assets in one venue never share a tag; `createAsset` refuses a duplicate with … |
| Name | text | — |
| Location description | text | — |
| Serial number | text | — |
| Commissioned at | 1 Oct 2026 | — |
| Warranty expires at | 1 Oct 2026 | — |

**Takings and admissions today** (metric tile, from `getKpiValues`): **Takings and admissions**, from `getKpiValues?kpiCodes=takings,admissions`; with no `period` the period is today in the venue's time zone (decided 28 September, audit R283).

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Period | text | — |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Card list** (card list): 6 screens. **No attention counts** until a summary operation exists to supply them (decided 28 September, audit R283).

**The selected work order** (detail panel, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |
| Kind | chip: Corrective, Planned, Inspection follow up, Incident corrective, Improvement | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Attention strip**: Emergency/urgent work orders open, reportable incidents awaiting notification with the nearest deadline, assets out of service. *(source: contracts/satellite/maintenance.yaml#listWorkOrders / contracts/satellite/maintenance.yaml#listIncidents / contracts/satellite/maintenance.yaml#listAssets)*
- **KPI tiles**: Admissions and takings today (VO-R10). *(source: contracts/satellite/reporting.yaml#getKpiValues / R283)*

**Data it reads**: `getKpiValues` (onLoad, Today's takings and admissions tiles — …); `listWorkOrders` (onLoad, Work raised and its state); `listIncidents` (onLoad, Incidents open in the venue); `listAssets` (onLoad, Assets and their condition)

**Where the user goes next**

- → `BO-036` Device Registry: *Device Registry*
- → `BO-044` F&B Outlets: *F&B Outlets*
- → `BO-058` Reporting Home: *Reporting Home*
- → `BO-060` Attendance & Footfall: *Attendance & Footfall*
- → `BO-064` Zones & Areas: *Zones & Areas*
- → `BO-067` Integrations: *Integrations*
- → `BO-100` Venue Home: *Venue Home*
- → `BO-128` Live Workstation Health Monitor: *Live Workstation Health Monitor*
- → `BO-129` Software, Configuration & Version Management: *Software, Configuration & Version Management*
- → `BO-130` Offline Policy & Rules Configuration: *Offline Policy & Rules Configuration*
- → `BO-131` Connectivity & Auto-Switch Settings: *Connectivity & Auto-Switch Settings*
- → `BO-132` Offline Transaction Monitor & Sync Queue: *Offline Transaction Monitor & Sync Queue*
- → `BO-133` Offline Alerts, Limits & Audit: *Offline Alerts, Limits & Audit*
- → `BO-1184` Transport Routes & Stops: *Transport routes*
- → `BO-1183` Transport Stations: *Transport stations*
- → `BO-070` Work Orders: *Work Orders*; carries `workOrderId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list, with counts. |
| Error (`?state=error`) | Could not load. Venue Home is still reachable. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing configured in venue operations yet.** The action is the first thing to set up, not a blank list. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter. |
| Permission denied (`?state=emptyNoAccess`) | You do not have permission for venue operations. **Said plainly** — an empty section reads as broken. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Consistency with other screens

- Match `BO-103`: Same hub layout as the Access & Venue landing.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
attention:
  emergencyWOs: 1
  reportableIncidents: 1 (notify by 14:05)
  outOfService: Falcon Coaster, Gate 2 turnstile
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `listWorkOrders` → `WORK_ORDER_VIEW` (read) · staff
- `listIncidents` → `INCIDENT_VIEW` (read) · staff
- `listAssets` → `ASSET_VIEW` (read) · staff

**A refused user sees:** You do not have permission for venue operations. **Said plainly** — an empty section reads as broken.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.9.5 | System shall provide real-time visibility of incidents, hazards, complaints, emergencies, and operational disruptions. | Unified Operations Dashboard | CONTRACTED | `listIncidents` |
| 1.2.40 | System shall allocate equipment to activities and events. | Ticketing Catalogue | CONTRACTED | data `Asset` |
| 1.2.41 | System shall track asset availability. | Ticketing Catalogue | CONTRACTED | data `Asset` |
| 1.2.42 | System shall block resources under maintenance. | Ticketing Catalogue | CONTRACTED | data `Asset` |
| 1.2.43 | System shall manage inspections and compliance checks. | Ticketing Catalogue | CONTRACTED | data `Asset` |
| 1.2.44 | System shall track resource lifecycle status. | Ticketing Catalogue | CONTRACTED | data `Asset` |
| 1.2.45 | System shall support asset depreciation tracking. | Ticketing Catalogue | CONTRACTED | data `Asset` |
| 1.2.46 | System shall support retirement of resources. | Ticketing Catalogue | CONTRACTED | data `Asset` |
| 8.9.4 | System shall display operational status of attractions, rides, facilities, equipment, and service locations including open, closed, maintenance, and restricted states. | Unified Operations Dashboard | CONTRACTED | data `Asset` |
| 17.1.4 | Asset Lifecycle Management - System shall support asset lifecycle tracking. | Maintenance & Safety Management | CONTRACTED | data `Asset` |
| 17.3.4 | Root Cause Analysis - System shall support root cause analysis. | Maintenance & Safety Management | CONTRACTED | data `WorkOrder` |
| 17.3.5 | Maintenance Escalation - System shall support maintenance escalation workflows. | Maintenance & Safety Management | CONTRACTED | data `WorkOrder` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-108` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (32 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-108?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-036`, `BO-044`, `BO-058`, `BO-060`, `BO-064`, `BO-067`, `BO-100`, `BO-128`, `BO-129`, `BO-130`, `BO-131`, `BO-132`, `BO-133`, `BO-1184`, `BO-1183`, `BO-070`.
- [ ] Every gated control is gated: `ASSET_VIEW`, `INCIDENT_VIEW`, `REPORT_VIEW_VENUE`, `WORK_ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-128` Live Workstation Health Monitor

**Watch every workstation's health live and open the worst first.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_VIEW`, `SCOPE_VIEW` (2 read); in the flows as technician |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listWorkstations` reads the population and `getWorkstationHealth` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `workstationId` (deepLink) · cold entry: Resolves from the session. A principal with more than one venue is asked which first. |
| Route | `/venue-operations/live-workstation-health-monitor` |

**What the spec says about it.** **Added 20 August from the client design board.** The operations existed and no screen called them. **Owns POS board frame(s) POS-5B** (client pack, 24 August). **Assigned by board purpose rather than by operation overlap** — three attempts at deriving that mapping produced plausible nonsense, and a reader who trusts a bad table is worse off than one who has none.

**Known gaps.** **`getWorkstationHealth` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape. Removed 2 October 2026 (CHG-WIR-021): Save offline policy (setOfflinePolicy) on a live monitor; offline policy is configuration, set on BO-130 and BO-206, and the monitor links there (design-notes …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The live state of every workstation in the venue: online, offline (and for how long), pending sync, peripheral failures; refreshed live. A supervisor finds the till that stopped syncing before the cashier notices.

**Fixed on main** (the package already carries these; draw what it says): Save offline policy on a monitor. (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every workstation' drop id, venueId, regionId, departmentId, scopePath, accessPointId. (CHG-SBO-004).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listWorkstations`. | `listWorkstations` ?venueId |
| Sale board kind | radio group | optional | — | Ticketing · Fnb · Retail · Mixed | — | Sends `?saleBoardKind=` to `listWorkstations`. | `listWorkstations` ?saleBoardKind |
| Search live workstation health monitor | search field | — | — | — | — | — | — |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setOfflinePolicy: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/tenancy.yaml#setOfflinePolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Every workstation** (data table, from `listWorkstations`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Sale board | grouped details | Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. |
| Devices | list or chips (count when long) | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |

**Workstation health** (detail panel, from `getWorkstationHealth`): Shows `score`, `status`, `contributors` from `getWorkstationHealth`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.

| Shows | Format | Notes |
|---|---|---|
| Score | 1,234 | — |
| Status | chip: Healthy, Warning, Degraded, Offline | — |
| Contributors | list or chips (count when long) | — |
| Factor | chip: Heartbeat age, Device offline, Device battery, Firmware outdated, Sync backlog … | — |
| Detail | text | — |
| Weight | 1,234 | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Workstation rows**: Name, sale board, connection state with duration, pending sync count, failing peripheral named; offline and failing first. *(source: contracts/spine/tenancy.yaml#getWorkstationHealth)*

**Data it reads**: `listWorkstations` (onLoad, List workstations)

**Where the user goes next**

- → `BO-108` Venue Operations: *Venue Operations*
- → `BO-129` Software, Configuration & Version Management: *Software, Configuration & Version Management*; carries `workstationId`
- → `BO-037` Offline Package Status: *What the tills did offline is reconciled*
- → `BO-036` Device Registry: *The failing till is found, with its alerts*; carries `workstationId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The live workstation health list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the live workstation health untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No live workstation health yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, saleBoardKind and the live workstation health are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SCOPE_VIEW`, which `listWorkstations` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `DEVICE_VIEW` for `getWorkstationHealth`. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds DEVICE_VIEW, SCOPE_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: TENANT_CONFIGURE for Save offline policy. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/tenancy.yaml#setOfflinePolicy)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
workstations:
- name: Main Gate Till 5
  state: offline 12 min
  pendingSync: 37
  failing: card terminal
- name: Main Gate Till 3
  state: online
  pendingSync: 0
```

#### Permissions

- `getWorkstationHealth` → `DEVICE_VIEW` (read) · staff
- `listWorkstations` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `SCOPE_VIEW`, which `listWorkstations` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `DEVICE_VIEW` for `getWorkstationHealth`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Performance monitoring shows successful vs failed validations and scan response time; configurable alert rules (e.g. low battery, device offline) with escalation for unresolved alerts. *(client request · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-901)*
- **Open question.** Open: can health metrics such as handheld battery be read via the manufacturer's SDK in-app rather than by physical inspection? Depends on each vendor SDK; to confirm during integration. *(open · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-900)*
- One screen shows live online/offline status of every workstation and device (printers, turnstiles, handheld scanners); a 360 health view shows connectivity, CPU/memory, storage and temperature. *(client request · MoM 15 Sep 2026, 4.5 Device Monitoring, Health & Alerts · DI-899)*
- Workstation health is shown as a percentage score a manager can sort by, not only a last-heartbeat timestamp. *(agreed · client-design-boards-audit 20 Aug 2026, Genuine functional gaps - workstation health score · DI-403)*
- Workstation details: six tabs, a health score, a current-operator card with role and shift, IP address, configuration profile with version and deployment date, and a today's summary (transactions, refunds, cash collected). *(agreed · client-design-boards-audit 20 Aug 2026, What the boards give us - 1C Workstation Details · DI-401)*
- Offline policies and a venue-level Operations Summary dashboard aggregating department-level views into one venue overview. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-311)*
- **Open question.** Live workstation monitor with department-level health; proposed graphical park-map view of workstation locations and live status, depending on venue zone metadata, with manual drag-and-drop placement as fallback. *(open · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-304)*
- Hardware & peripheral management per workstation (receipt printer, cash drawer, payment terminal, barcode/ticket scanner, ticket printer) with device-level status. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-303)*
- Workstation overview dashboard: all workstations for a venue (or across venues), grouped by department and sub-department, with online/offline/health status and type (mobile POS, kiosk, on-site POS). *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-301)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'station')*
- **C28** Share clean input format (schema/metadata) for park maps — including zones, regions, and category tagging — needed to drive AI-assisted map and workstation-location auto-configuration *(Allam / Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'station')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'station')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'station')*
- **A84** Design kitchen station routing and KDS/printer rules (with fallback device logic), including course-wise ordering and a live "fired" ticket timer *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'station')*
- **A265** Check if a booth/station config module exists that links to the live map builder *(Chinmay Parab · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'station')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-128` · status **notStarted** · provenance generated · **Drawn by Claude Design on `POS Board 5.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once …
- Derived from `wireframes/reference/POS Board 5.dc.html`
- Drawn by: Claude Design POS pack, 24 August
- Client design-board frames: `POS Board 5.dc.html#pos-5b`
- Flow F89 *Offline policy is set, cached, monitored and reconciled*, step 4: The fleet is monitored. → Which tills are offline, and since when.
- Flow F95 *A fleet is watched, a fault is found, and a station is fixed*, step 1: The fleet is watched. → **A workstation that stops reporting is itself the signal.**
- Flow F95 branch at step 1 (medium): when A step is not licensed for this tenant., **The chain stops at the module boundary.** `requiresModule` decides — the journey is shorter, not broken.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-128?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-108`, `BO-129`, `BO-037`, `BO-036`.
- [ ] Every gated control is gated: `DEVICE_VIEW`, `SCOPE_VIEW`.
- [ ] The 9 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
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

### In P08 · Venue Operations

- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*

**31 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"askReportingQuestion": {"method":"POST","path":"/reports/ask","contract":"reporting","summary":"Natural-language reporting query","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"NaturalLanguageAnswer"},
"cancelWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/cancel","contract":"maintenance","summary":"Cancel a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"closeCorrectiveAction": {"method":"POST","path":"/food-safety/corrective-actions/{actionId}/close","contract":"fnb","summary":"Close a signed finding","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CorrectiveAction"},
"closeWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/close","contract":"maintenance","summary":"Administratively closed","permission":"MAINTENANCE_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"completeWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/complete","contract":"maintenance","summary":"Complete a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"configureWorkstation": {"method":"PUT","path":"/workstations/{workstationId}","contract":"tenancy","summary":"Configure a workstation","permission":"WORKSTATION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ConfigureWorkstationRequest","responds":"Workstation"},
"createAccessPoint": {"method":"POST","path":"/access-points","contract":"access","summary":"Create an access point","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateAccessPointRequest","responds":"AccessPoint"},
"createOrgUnit": {"method":"POST","path":"/org-units","contract":"tenancy","summary":"Create a scope node","permission":"SCOPE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"brand","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateScopeNodeRequest","responds":"OrgUnit"},
"createOutlet": {"method":"POST","path":"/outlets","contract":"tenancy","summary":"Create an outlet","permission":"REGION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Outlet","responds":"Outlet"},
"createReport": {"method":"POST","path":"/reports","contract":"reporting","summary":"Create a custom report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportRequest","responds":"ReportDefinition"},
"createReportSchedule": {"method":"POST","path":"/report-schedules","contract":"reporting","summary":"Schedule a report","permission":"REPORT_SCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportScheduleRequest","responds":"ReportSchedule"},
"createVendorServiceRequest": {"method":"POST","path":"/vendor-service-requests","contract":"maintenance","summary":"Engage an outside vendor on a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VendorServiceRequest","responds":"VendorServiceRequest"},
"createWebhookSubscription": {"method":"POST","path":"/webhook-subscriptions","contract":"public-api","summary":"Subscribe to business events","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WebhookSubscription","responds":"WebhookSubscription"},
"createWorkOrder": {"method":"POST","path":"/work-orders","contract":"maintenance","summary":"Raise a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateWorkOrderRequest","responds":"WorkOrder"},
"deleteReport": {"method":"DELETE","path":"/reports/{reportId}","contract":"reporting","summary":"Retire a report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"escalateCorrectiveAction": {"method":"POST","path":"/food-safety/corrective-actions/{actionId}/escalate","contract":"fnb","summary":"Escalate a finding","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CorrectiveAction"},
"getAccessPoint": {"method":"GET","path":"/access-points/{accessPointId}","contract":"access","summary":"Read an access point","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AccessPoint"},
"getFinancialReport": {"method":"GET","path":"/reports/financial","contract":"finance","summary":"Financial statements, revenue and tax summaries","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"report","in":"query","required":true},{"name":"fiscalPeriodId","in":"query","required":true},{"name":"legalEntityId","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"costCenterId","in":"query","required":null}],"requestBody":null,"responds":"FinancialReport"},
"getFnbDeliveryPolicy": {"method":"GET","path":"/fnb-delivery-policy","contract":"fnb","summary":"How an outlet does takeaway and delivery","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":true}],"requestBody":null,"responds":"FnbDeliveryPolicy"},
"getHaccpStatus": {"method":"GET","path":"/food-safety/status","contract":"fnb","summary":"Where this venue stands, right now","permission":"INCIDENT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":null},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null},{"name":"module","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getOfflinePackage": {"method":"GET","path":"/access/offline-package","contract":"access","summary":"Entitlement and rule set for offline validation","permission":"ACCESS_VALIDATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":"sinceVersion","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":"validFrom","in":"query","required":true},{"name":"validTo","in":"query","required":true},{"name":"If-None-Match","in":"header","required":null}],"requestBody":null,"responds":"OfflinePackage"},
"getOrgUnit": {"method":"GET","path":"/org-units/{orgUnitId}","contract":"tenancy","summary":"Read a scope node","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"OrgUnit"},
"getReport": {"method":"GET","path":"/reports/{reportId}","contract":"reporting","summary":"Read a report definition","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ReportDefinition"},
"getReturnPolicy": {"method":"GET","path":"/outlets/{outletId}/return-policy","contract":"retail","summary":"Read the retail return policy","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ReturnPolicy"},
"getTableMap": {"method":"GET","path":"/outlets/{outletId}/tables","contract":"fnb","summary":"Table map with live state","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"TableMap"},
"getVenueSettings": {"method":"GET","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Operational settings for this venue","permission":"TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"getWorkOrder": {"method":"GET","path":"/work-orders/{workOrderId}","contract":"maintenance","summary":"Read a work order","permission":"WORK_ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WorkOrderDetail"},
"getWorkstation": {"method":"GET","path":"/workstations/{workstationId}","contract":"tenancy","summary":"Read a workstation","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[],"requestBody":null,"responds":"Workstation"},
"getWorkstationHealth": {"method":"GET","path":"/workstations/{workstationId}/health","contract":"tenancy","summary":"A score a manager can sort by, and what is dragging it down","permission":"DEVICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":null},
"issueDeviceCredential": {"method":"POST","path":"/devices/{deviceId}/credentials","contract":"tenancy","summary":"Give the device an identity it can prove","permission":"DEVICE_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DeviceCredential"},
"listAccessPoints": {"method":"GET","path":"/access-points","contract":"access","summary":"List access points","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAlerts": {"method":"GET","path":"/alerts","contract":"reporting","summary":"What is currently wrong","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"severity","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"itemId","in":"query","required":null}],"requestBody":null,"responds":"Alert"},
"listApiClients": {"method":"GET","path":"/api-clients","contract":"public-api","summary":"Registered clients for this developer","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ApiClient"},
"listAssets": {"method":"GET","path":"/assets","contract":"maintenance","summary":"List assets","permission":"ASSET_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"maintenanceDue","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDevices": {"method":"GET","path":"/devices","contract":"tenancy","summary":"List registered devices","permission":"DEVICE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listIncidents": {"method":"GET","path":"/incidents","contract":"maintenance","summary":"List incidents","permission":"INCIDENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"severity","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"isReportable","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrgUnits": {"method":"GET","path":"/org-units","contract":"tenancy","summary":"List scope nodes visible to the session","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"under","in":"query","required":null},{"name":"level","in":"query","required":null},{"name":"includeInactive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOutlets": {"method":"GET","path":"/outlets","contract":"tenancy","summary":"List outlets","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"Outlet"},
"listReportExecutions": {"method":"GET","path":"/report-executions","contract":"reporting","summary":"List executions","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"reportId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"mineOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listReports": {"method":"GET","path":"/reports","contract":"reporting","summary":"List available report definitions","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"category","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listScans": {"method":"GET","path":"/access/scans","contract":"access","summary":"List scan events","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"accessPointId","in":"query","required":null},{"name":"ticketId","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"recordedFrom","in":"query","required":null},{"name":"recordedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listShifts": {"method":"GET","path":"/shifts","contract":"shift","summary":"List shifts","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"openedFrom","in":"query","required":null},{"name":"openedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVendorServiceRequests": {"method":"GET","path":"/vendor-service-requests","contract":"maintenance","summary":"Requests sent to outside vendors","permission":"WORK_ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workOrderId","in":"query","required":null},{"name":"supplierId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWebhookDeliveries": {"method":"GET","path":"/webhook-subscriptions/{subscriptionId}/deliveries","contract":"public-api","summary":"What was sent, what failed, and why","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"WebhookDelivery"},
"listWebhookSubscriptions": {"method":"GET","path":"/webhook-subscriptions","contract":"public-api","summary":"The tenant's webhook subscriptions, filterable by API client","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"clientId","in":"query","required":false}],"requestBody":null,"responds":"WebhookSubscription"},
"listWorkOrders": {"method":"GET","path":"/work-orders","contract":"maintenance","summary":"List work orders","permission":"WORK_ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assignedToPrincipalId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"assetId","in":"query","required":null},{"name":"overdueOnly","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkstations": {"method":"GET","path":"/workstations","contract":"tenancy","summary":"List workstations","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"saleBoardKind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"lookupTicket": {"method":"GET","path":"/access/lookup","contract":"access","summary":"Read-only validity check without admitting","permission":"TICKET_LOOKUP","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"mediaCode","in":"query","required":null},{"name":"ticketId","in":"query","required":null}],"requestBody":null,"responds":"TicketStatus"},
"overrideAccess": {"method":"POST","path":"/access/override","contract":"access","summary":"Admit against a failed validation","permission":"ACCESS_OVERRIDE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationResult"},
"pauseWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/pause","contract":"maintenance","summary":"Stopped, and why","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"recordCorrectiveAction": {"method":"POST","path":"/food-safety/corrective-actions/{actionId}/action","contract":"fnb","summary":"Record what was done about a finding","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CorrectiveAction"},
"registerDevice": {"method":"POST","path":"/devices","contract":"tenancy","summary":"Register a device","permission":"DEVICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RegisteredDevice","responds":"RegisteredDevice"},
"rejectWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/reject","contract":"maintenance","summary":"The assignee declines, with a reason","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"revokeDeviceCredential": {"method":"DELETE","path":"/devices/{deviceId}/credentials","contract":"tenancy","summary":"Cut a device off now","permission":"DEVICE_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"reason","in":"query","required":true}],"requestBody":null,"responds":null},
"runReport": {"method":"POST","path":"/reports/{reportId}/run","contract":"reporting","summary":"Run a report","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RunReportRequest","responds":"ReportResult"},
"saveNaturalLanguageQuery": {"method":"POST","path":"/reports/ask/{conversationId}/save","contract":"reporting","summary":"Save a natural-language answer as a report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReportDefinition"},
"setAccessPointGeofence": {"method":"PUT","path":"/access-points/{accessPointId}/geofence","contract":"access","summary":"Set a geofence for handheld validation","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AccessPointGeofence","responds":"AccessPoint"},
"setDeliveryLocationOutletMapping": {"method":"PUT","path":"/venues/{venueId}/delivery-location-outlets","contract":"fnb","summary":"Set which outlets deliver to which delivery locations","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DeliveryLocation"},
"setFnbDeliveryPolicy": {"method":"PUT","path":"/fnb-delivery-policy","contract":"fnb","summary":"Set takeaway and delivery rules","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"FnbDeliveryPolicy","responds":"FnbDeliveryPolicy"},
"setReturnPolicy": {"method":"PUT","path":"/outlets/{outletId}/return-policy","contract":"retail","summary":"Set the retail return policy","permission":"REGION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ReturnPolicy","responds":"ReturnPolicy"},
"setTableLayout": {"method":"PUT","path":"/outlets/{outletId}/tables","contract":"fnb","summary":"Configure the table layout","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TableMap"},
"signCorrectiveAction": {"method":"POST","path":"/food-safety/corrective-actions/{actionId}/sign","contract":"fnb","summary":"Say what was done, and put a name to it","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CorrectiveAction"},
"suggestWorkOrderAssignee": {"method":"GET","path":"/work-orders/{workOrderId}/assignee-suggestions","contract":"maintenance","summary":"Who should take this work order, ranked","permission":"WORK_ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"syncScans": {"method":"POST","path":"/access/scans","contract":"access","summary":"Replay scans recorded offline","permission":"ACCESS_VALIDATE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ScanSyncResult"},
"updateAccessPoint": {"method":"PATCH","path":"/access-points/{accessPointId}","contract":"access","summary":"Update an access point","permission":"ACCESS_POINT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessPoint"},
"updateOrgUnit": {"method":"PATCH","path":"/org-units/{orgUnitId}","contract":"tenancy","summary":"Rename or deactivate a scope node","permission":"SCOPE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"brand","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrgUnit"},
"updateOutlet": {"method":"PATCH","path":"/outlets/{outletId}","contract":"tenancy","summary":"Amend an outlet","permission":"REGION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Outlet"},
"updateReport": {"method":"PUT","path":"/reports/{reportId}","contract":"reporting","summary":"Publish a new version of a definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportRequest","responds":"ReportDefinition"},
"updateVendorServiceRequest": {"method":"PATCH","path":"/vendor-service-requests/{vendorServiceRequestId}","contract":"maintenance","summary":"Move a vendor request along","permission":"WORK_ORDER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"VendorServiceRequest"},
"updateWorkOrder": {"method":"PATCH","path":"/work-orders/{workOrderId}","contract":"maintenance","summary":"Assign, reprioritise or amend","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"validateAccess": {"method":"POST","path":"/access/validate","contract":"access","summary":"Validate media at an access point and admit or deny","permission":"ACCESS_VALIDATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ValidateRequest","responds":"ValidationResult"},
"validateGroupAccess": {"method":"POST","path":"/access/group-validate","contract":"access","summary":"Admit a group on one read","permission":"ACCESS_VALIDATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationResult"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessAccreditationCredential": {"type":"object","x-ticvai-persistence":"access.accreditation_credential","x-ticvai-agreed":"29 September: build pass (group OWN, from group RA's handoff; BL-181); the events accreditation.credentialIssued and accreditation.holderStatusChanged name access as their critical consumer","description":"**What a gate needs to admit an accredited person, kept by `access`** (29 September, build). Written only by the consumers of `accreditation.credentialIssued` (a row per credential; a replacement sets the replaced row's `admits` false) and `accreditation.holderStatusChanged` (every credential of the holder: `admits` false unless the holder is `active`, validity taken from the event). Read by `validateAccess` and shipped in the offline package. The record of truth stays in `accreditation`; this is a copy shaped for the gate, never edited by a person.","required":["id","holderId","encodedIdentifier","admits","scopePath"],"properties":{"id":{"type":"string","format":"uuid","description":"The accreditation credential's id (`credentialId` on the events)."},"holderId":{"type":"string","format":"uuid"},"programmeId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","description":"printedBadge, mobileCredential, qr, nfcCard, rfidCard or wristband, as issued."},"encodedIdentifier":{"type":"string","x-ticvai-unique":"tenant","description":"What the gate reads from the credential. Never sent to webhook subscribers."},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"zoneIds":{"type":"array","description":"The holder's effective zones, from the event (`effectiveZones`).","items":{"type":"string","format":"uuid"}},"holderStatus":{"type":"string","enum":["active","suspended","revoked","expired","archived"],"description":"The holder's status as last published; only `active` admits."},"admits":{"type":"boolean","description":"False once the credential is replaced or the holder is not active."},"sourceChangedAt":{"type":"string","format":"date-time","description":"The `issuedAt` or `changedAt` of the event last applied; an older event arriving late is ignored."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005), the accreditation programme's scope."}}},
"AccessDynamicPolicy": {"type":"object","x-ticvai-persistence":"access.dynamic_policy","description":"One guest-admission dynamic (attribute-based) policy with its current content - type, context or identity it tests, condition expression, result, priority, zones, validity, status and current version. Not identity.authorisation_policy, which is staff permission (declared 29 September, data-model close-out DM1).\n\n**Guest admission lives here and nowhere else** (ADR-0068, accepted 1 October). `validateAccess` online and the gate offline evaluate the same active version: `getOfflinePackage` carries it, and every `scan_event` records the policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`) and the set it was decided under (`policySetVersion`). The condition is `conditionRule`, a closed JSON format (`AdmissionRule`), not free text. Identity's staff-permission engine was renamed `AuthorisationPolicy` on the same day, so \"access policy\" means this.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). **This one governs who may pass which gate**: admission of a guest, pass holder, accreditation holder or employee at an access point, decided in validation with results a gate acts on (allow, deny, review, requireId, requireBiometric, requireCompanion, requireSupervisor). **identity `AuthorisationPolicy` governs who may do what in the software**: a principal's permissions on operations and screens, decided by identity `evaluateAccess`. An employee's badge opening a staff door is decided here; the same employee approving a refund is decided in identity. Effectiveness is reported per engine: `listDynamicPolicyEffectiveness` here, `listAuthorisationPolicyEffectiveness` in identity.","required":["id","scopePath","name","policyType","conditionRule","result","status","currentVersion"],"properties":{"id":{"type":"string","format":"uuid","description":"The policyId"},"venueId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node; where it applies further is access.policy_scope_assignment"},"name":{"type":"string","maxLength":200},"policyType":{"type":"string","enum":["guestAttribute","accreditation","occupancy","employee","risk","membership","timeEvent"]},"contextType":{"type":"string","enum":["date","day","time","season","event","performance","specialEvent","holiday","operatingCalendar","occupancy","attractionStatus"],"nullable":true,"description":"Context/time/event policies (setContextTimeEvent)"},"identityType":{"type":"string","enum":["guest","member","annualPassHolder","employee","contractor","vendor","performer","media","vip","security","emergencyServices","eventStaff"],"nullable":true,"description":"Identity-based policies (listIdentityMembershipAccreditation)"},"conditionRule":{"$ref":"#/components/schemas/AdmissionRule","description":"The condition, in the closed JSON rule format evaluated the same way online and at the gate (ADR-0068; replaces the free-text `conditionExpression`)."},"result":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"]},"priority":{"type":"integer","nullable":true},"allowedZoneIds":{"type":"array","items":{"type":"string","format":"uuid"}},"deniedZoneIds":{"type":"array","items":{"type":"string","format":"uuid"}},"monitorThresholdPercent":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"description":"Occupancy policies. Percent at which the band becomes Monitor"},"restrictThresholdPercent":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"description":"Occupancy policies. Percent at which the band becomes Restrict"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"The grant expires automatically at validTo"},"status":{"type":"string","enum":["draft","pendingApproval","active","inactive","expired"],"default":"draft"},"currentVersion":{"type":"integer","minimum":1,"description":"The version in force (access.dynamic_policy_version)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessPoint": {"x-ticvai-persistence":"access.access_point","type":"object","required":["id","code","name","venueId","operatingMode","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"externalCredentialSources":{"allOf":[{"$ref":"#/components/schemas/ExternalCredentialSourceList"}],"description":"BL-108. **A hotel room card admitting a guest to a water park** — externally issued, and the platform validates it without having sold it.\n**The entitlement is created on first use, not on check-in.** A hotel with 400 rooms does not want 400 entitlements a night for guests who never visit.\n"},"scanAnomalyRules":{"allOf":[{"$ref":"#/components/schemas/ScanAnomalyRuleList"}],"description":"BL-104. **Rule-based scan anomalies, separated from the parked model-based engine** — device sharing, simultaneous entries at two gates, an impossible walking time between them.\n**These are deterministic and need no model**, which is why they are here and not in `ai`: two entries eight seconds apart at gates four hundred metres apart is arithmetic.\n"},"operatingMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}],"default":"normal","description":"**Set by the podium with `setTurnstileMode`, and it wins** (audit R221). BL-107 and BL-109. **A closed turnstile and one in emergency drop-arm mode look the same in the model and are opposite in meaning.** Closed refuses everybody; drop-arm lets everybody through, and it is the state that exists for an evacuation.\n**`podium` is a supervised validation position** — a member of staff directing a group through a lane, validating by eye against a list. It scans nothing and it is how school parties actually enter.\n**`freeFlow` counts without validating.** Useful at a free event, and a mode that must be visibly distinct from a broken reader.\n"},"vehicleLocationCapture":{"type":"boolean","default":false,"description":"BL-023. **Nothing helped a guest find their vehicle.** Where the access point is a car park entry, the level and zone are captured against the visit so the app can answer it — **the guest who cannot find their car at 11pm is the last impression of the day.**\n"},"mode":{"allOf":[{"$ref":"#/components/schemas/TurnstileMode"}],"nullable":true,"description":"Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates in its fixed `direction` (audit R221).\n"},"direction":{"allOf":[{"$ref":"#/components/schemas/Direction"}],"description":"**Fixed per access point** (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium.\n\n**R221 amended 2 October 2026: a gate's direction can be switched live** (Chinmay, critical set 1, BO-230: \"Live direction switch with permission, logged\"; DEC-255; CHG-CSP-032; DI-648: more entry gates in the morning, more exit gates in the evening). `setAccessPointDirection` switches it from Live Gate Mode & Lane Control (BO-230) or the scanner's gate mode screen (SCN-016) for a holder of the configuration right, logged; the podium's `setTurnstileMode` still never touches it.\n"},"temporaryClosure":{"type":"object","nullable":true,"description":"**What the access point does while its attraction is temporarily closed** (decided 2 October 2026, Chinmay, batch 6 set 9, BO-147: \"Deny + reopening time + a virtual-queue return window where enabled\"; DEC-228; CHG-CSP-026). While `isClosed`, every scan is denied (`ValidationResult.denyCause` `attractionTemporarilyClosed`) with the reopening time when it is known; where the venue offers it and the attraction has a virtual queue, the guest is offered a return window (`queue.joinQueue`) instead of being turned away empty-handed. Set with `updateAccessPoint`; null when open. Travels in the offline package, so an offline gate denies the same way.","properties":{"isClosed":{"type":"boolean","default":false},"reason":{"type":"string","maxLength":200,"nullable":true,"description":"Shown to staff; the guest sees \"Attraction temporarily closed\"."},"reopensAt":{"type":"string","format":"date-time","nullable":true,"description":"When it is expected to reopen; shown to the guest when known."},"offerVirtualQueueReturn":{"type":"boolean","default":false,"description":"Offer a virtual-queue return window at the denied scan, where the attraction has a queue."},"queueId":{"type":"string","format":"uuid","nullable":true,"description":"The virtual queue the return window is taken in."}}},"antiPassbackEnabled":{"type":"boolean"},"requiresExitBeforeReentry":{"type":"boolean","default":false,"description":"Written by `createAccessPoint` and `updateAccessPoint`, and returned so the edit form reads back what it wrote."},"driver":{"type":"string","nullable":true,"description":"Driver identifier for the controller behind this access point, as written by `createAccessPoint` and `updateAccessPoint`. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific.\n"},"geofence":{"allOf":[{"$ref":"#/components/schemas/AccessPointGeofence"}],"nullable":true,"description":"Written by `setAccessPointGeofence`; null until one is set. **One `jsonb` column on the access point row** (`access.access_point.geofence`), read with the point when a handheld validates against it.\n"},"isActive":{"type":"boolean"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true}}},
"AccessPointGeofence": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"Where a handheld may validate for one access point, and what happens outside it. The body of `setAccessPointGeofence` and the value of `AccessPoint.geofence`.\n","required":["enforcement"],"properties":{"latitude":{"type":"number"},"longitude":{"type":"number"},"radiusMetres":{"type":"integer","minimum":5,"maximum":5000},"enforcement":{"type":"string","enum":["off","warn","deny"],"description":"`off` keeps the fence on record and checks nothing; `warn` lets a validation from outside the fence through with a warning; `deny` refuses it.\n"},"allowProximityBeacon":{"type":"boolean","description":"Accept a BLE proximity assertion in place of GPS. Better indoors."}}},
"AccessPointOperatingMode": {"type":"string","description":"BL-107 and BL-109. **What the gate does, and what the podium sets** (`setTurnstileMode`, decided 28 September, audit R221). `closed` refuses everybody; `dropArm` lets everybody through and exists for an evacuation; `podium` is supervised validation by eye; `freeFlow` counts without validating; `maintenance` takes the lane out of use.\n","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"]},
"Alert": {"type":"object","x-ticvai-persistence":"reporting.alert","description":"A raised alert. **Acknowledged rather than dismissed** — CF-134 asked for it markable, and the difference is that an acknowledgement records who saw it.\n","required":["id","ruleId","raisedAt","severity","status"],"properties":{"id":{"type":"string","format":"uuid"},"ruleId":{"type":"string","format":"uuid"},"ruleName":{"type":"string","description":"`AlertRule.name` as it stood when the alert was raised. **The line a person reads** — a list of rule ids is not an alert panel, and a screen should not need `listAlertRules` to label one.\n"},"metric":{"allOf":[{"$ref":"#/components/schemas/MetricSource"}],"description":"The rule's metric, carried so the alert says what went out of range."},"raisedAt":{"type":"string","format":"date-time"},"severity":{"$ref":"#/components/schemas/AlertSeverity"},"status":{"$ref":"#/components/schemas/AlertStatus"},"observedValue":{"$ref":"#/components/schemas/MetricValue"},"threshold":{"$ref":"#/components/schemas/MetricValue"},"scopePath":{"type":"string"},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation the reading was taken for, where the metric is measured per workstation (`salesByWorkstation`). Null otherwise. `listAlerts` filters on it."},"shiftId":{"type":"string","format":"uuid","nullable":true,"description":"The till shift (`orders.pos_shift`) the reading belongs to, where it was taken for a workstation with a shift open. Null otherwise. `listAlerts` filters on it."},"itemId":{"type":"string","format":"uuid","nullable":true,"description":"The inventory item the reading is about, where the metric is measured per item (`stockAgeing`, `stockTurnover`, `wastageRate`, `inventoryValuation`). Null otherwise. **What a replenishment screen prefills a requisition from.**\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true},"acknowledgementNote":{"type":"string","maxLength":300,"nullable":true,"description":"The `note` given to `acknowledgeAlert`. Kept, because an acknowledgement that says what is being done about it is the one escalation can skip."},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"description":"**Set when the metric returns to range, automatically.** An alert that only a person can close is an alert list that only grows.\n"},"escalatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. **A critical alert nobody acknowledged is the case escalation exists for.**\n"}}},
"AlertSeverity": {"type":"string","description":"How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter.","enum":["info","warning","critical"]},
"AlertStatus": {"type":"string","description":"Where a raised alert is. Shared by `Alert` and the `listAlerts` filter.","enum":["raised","acknowledged","resolved","expired"]},
"ApiClient": {"type":"object","x-ticvai-persistence":"control.api_client","description":"CF-135a. **The one credential model.** 2.7.52, 7.1.25 and 7.1.30 each asserted their own, so a partner API key, a POS integration credential and a webstore credential were three unrelated things with three lifecycles.\n","required":["id","developerId","name","environment","scopes","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"developerId":{"type":"string","format":"uuid"},"name":{"type":"string"},"clientId":{"type":"string","readOnly":true},"environment":{"type":"string","enum":["sandbox","production"],"description":"**Bound to one, stated on the object rather than by naming convention.** A key that works in both is a key somebody will use in the wrong one.\n"},"scopes":{"type":"array","description":"**Resolved against the tenant's licence at token issue** (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call time, so an integrator finds out in testing. **Module scopes** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, one of `listApiScopes`.\n","items":{"type":"string","pattern":"^[a-zA-Z]+\\.(read|write)$"}},"issuedBy":{"type":"string","enum":["partner","ticvai"],"readOnly":true,"description":"Who generated the key (M17-06): a developer for a sandbox key, TICVAI for a production key issued on an approved `requestProductionAccess`.\n"},"certificationListingId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"control.integration_listing","description":"For a production client, the certified integration it was issued against."},"credentialTtlDays":{"type":"integer","minimum":1,"maximum":730,"nullable":true,"description":"Key lifetime. Default 365 for production, 90 for sandbox (M17-06, configurable expiry)."},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the key stops working unless rotated. No token is issued after it."},"allowedTenantIds":{"type":"array","description":"13.1.46. **Which tenants this client may act for.** A developer integrating for one venue must not reach another, and a client with an empty list reaches none.\n","items":{"type":"string","format":"uuid"}},"ipAllowList":{"type":"array","description":"13.1.38. **Required on a production client** (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the internet); optional in the sandbox. CIDR ranges. Checked at token issue and on every call.\n","items":{"type":"string"}},"status":{"type":"string","enum":["active","suspended","revoked"],"readOnly":true},"lastUsedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**A credential unused for a year is a credential nobody will notice being stolen.**\n"}}},
"Asset": {"x-ticvai-persistence":"maintenance.asset","allOf":[{"$ref":"#/components/schemas/CreateAssetRequest"},{"type":"object","x-ticvai-retired-columns":["is_maintenance_overdue","document_refs"],"required":["id","status"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid","nullable":true,"description":"1.2.x. **Where this asset is also bookable.** An AV rig is an asset to maintain and a resource to allocate, and they are the same object seen from two sides.\n**`resources` owns the calendar and this owns the condition.** An asset out of service makes its resource unbookable, which is one link rather than two models of availability.\n"},"deviceId":{"type":"string","format":"uuid","nullable":true,"description":"BL-160. **Where this asset is also a registered device.** A turnstile is an asset to maintain and a device to operate, and — exactly as with `resourceId` above — they are the same object seen from two sides.\n**Nothing joined them before this.** A turnstile controller reporting `needsAttention` could not raise a work order against itself, and an engineer closing one had no way back to the device whose firmware caused it.\n**Null for most assets and for most devices.** A chiller is not a device and a signature pad is not on the asset register; the link is sparse, and it lives here rather than on `platform.device` because `platform` is the foundation tier and a foreign key pointing from it into `maintenance` would invert the tiers — every cell running a spine would carry a column for a satellite it may not deploy.\n"},"acquisitionCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"acquiredOn":{"type":"string","format":"date","nullable":true},"depreciation":{"type":"object","nullable":true,"description":"**Recorded here and posted by `finance`.** Depreciation is an accounting act and the asset register is where the useful life is actually known — an engineer knows a chiller lasts fifteen years and an accountant knows what to do about it.\n","properties":{"method":{"type":"string","enum":["straightLine","reducingBalance","unitsOfProduction","none"]},"usefulLifeMonths":{"type":"integer"},"residualValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accumulatedDepreciation":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"retiredOn":{"type":"string","format":"date","nullable":true,"description":"**Retirement is not deletion.** A work order from three years ago still names this asset, and an inspection record with no asset is an inspection of nothing.\n"},"disposalProceeds":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"$ref":"#/components/schemas/AssetStatus"},"statusReason":{"type":"string","nullable":true},"openWorkOrderCount":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Work orders on this asset whose status is `open`, `assigned`, `inProgress`, `paused` or `awaitingParts` — the same set `AssetDetail.openWorkOrders` returns. **Maintained on write**: `createWorkOrder` and every transition into or out of that set (complete, cancel, close, reject back to open) adjust it in the same transaction as the work-order row.\n"},"nextMaintenanceDueAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The earliest `nextDueAt` among this asset's active maintenance plans; null when none has one. **Maintained on write**: recomputed whenever one of those plans is created, amended, suspended or has its `nextDueAt` moved by a completed work order. `listAssets?maintenanceDue` filters on this column against the clock.\n"},"isMaintenanceOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`nextMaintenanceDueAt` is in the past at the moment of the read. **Computed on read and not stored** — it depends on the clock, so a stored copy is stale the minute after it is written.\n"},"lastInspectionAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`performedAt` of the latest inspection submitted against this asset. **Maintained on write** by `submitInspection`, in the same transaction as the inspection row; an inspection synced late with an earlier `performedAt` does not move it back.\n"},"usageCounter":{"type":"number","nullable":true,"description":"Cycles, hours or kilometres. Drives usage-based maintenance."}}}]},
"AssetStatus": {"type":"string","enum":["inService","outOfService","underMaintenance","awaitingParts","retired","disposed"]},
"Cadence": {"x-ticvai-persistence":"none — embedded in schedule","type":"object","description":"**What each frequency needs (decided 28 September, audit R158).** `daily`: `timeOfDay`. `weekly`: `dayOfWeek` and `timeOfDay`. `monthly`: `dayOfMonth` and `timeOfDay`, a day past the month's end running on its last day. `quarterly`: `dayOfMonth` and `timeOfDay`, in the first month of each quarter. `onShiftClose` and `onPeriodClose`: nothing else, they run on the event. A field a frequency needs and does not have, or one it does not take, is the 400 on `createReportSchedule`. **Times are in the venue's time zone.**\n","required":["frequency"],"properties":{"frequency":{"type":"string","enum":["daily","weekly","monthly","quarterly","onShiftClose","onPeriodClose"]},"dayOfWeek":{"type":"integer","minimum":0,"maximum":6},"dayOfMonth":{"type":"integer","minimum":1,"maximum":31},"timeOfDay":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$"},"timeZone":{"type":"string","readOnly":true,"description":"Always the venue's time zone (decided 28 September, audit R158), returned so a reader knows which. Not taken on a write."}}},
"CatalogueState": {"x-ticvai-persistence":"none — computed from workstation bundle_version","type":"object","description":"The workstation's local catalogue position. A terminal beyond `staleAfter` must refuse to trade rather than transact against stale prices.\n","required":["appliedBundleVersion","appliedAt","staleAfter","isStale"],"properties":{"appliedBundleVersion":{"type":"string"},"appliedAt":{"type":"string","format":"date-time"},"staleAfter":{"type":"string","format":"date-time","description":"Beyond this the terminal refuses to trade."},"isStale":{"type":"boolean"},"pendingBundleVersion":{"type":"string","nullable":true,"description":"Published but not yet applied."}}},
"ConfigureWorkstationRequest": {"type":"object","required":["name"],"properties":{"cashierInputMode":{"type":"string","enum":["keyboard","touch","scanner","hybrid"],"default":"hybrid","description":"BL-061. **A till operator who touch-types is slower on a touchscreen and a new starter is faster.** The mode is per workstation because the operator is.\n"},"guestDisplayContent":{"type":"array","description":"**What the guest-facing screen shows while a sale is in progress.** Line items always; the rest is the venue's choice — and **a second screen showing nothing is a second screen the guest ignores when it does show something that matters.**\n","items":{"type":"string","enum":["lineItems","total","loyaltyBalance","promotions","branding","upsell","queuePosition"]}},"loadedMediaStockId":{"type":"string","format":"uuid","nullable":true,"description":"BL-095. **Neither which stock a printer is loaded with nor how much is left.** A till that runs out of wristbands mid-queue is an outage nobody predicted, and the stock is inventory like anything else — this names which.\n"},"mediaStockRemaining":{"type":"integer","nullable":true,"readOnly":true,"description":"Decremented on issue. **The number that turns a surprise into a reorder**, and it is read-only because the count comes from what was printed rather than from somebody's estimate.\n"},"name":{"type":"string","maxLength":200},"saleBoardId":{"type":"string","format":"uuid","nullable":true,"description":"**This till's own layout, overriding its outlet's** (DEC-183; CHG-CSP-006). Optional since 2 October 2026: absent or null, the till uses `Outlet.saleBoardId`.\n"},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"The outlet this till stands in (CHG-CSP-006)."},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"This till's drawer limit; null inherits `VenueSettings.cashDrawerLimit` (DEC-179; CHG-CSP-016)."},"departmentId":{"type":"string","format":"uuid","nullable":true},"accessPointId":{"type":"string","format":"uuid","nullable":true},"devices":{"type":"array","items":{"$ref":"#/components/schemas/DeviceBinding"}},"deploymentProfile":{"$ref":"#/components/schemas/DeploymentProfile"},"edgeNodeId":{"type":"string","format":"uuid","nullable":true},"isActive":{"type":"boolean","default":true}}},
"CorrectiveAction": {"type":"object","x-ticvai-persistence":"fnb.corrective_action","description":"What was done about a finding, and who signed it. **Opened automatically by an out-of-range reading or a cold-chain breach**, because an action that depends on somebody remembering to raise it is an action that is not raised.\n**Signed by a named principal, and the signature is the record.** *Discarded and reset* with nobody against it is not a corrective action.\n","required":["id","raisedAt","source","status"],"properties":{"id":{"type":"string","format":"uuid"},"raisedAt":{"type":"string","format":"date-time"},"raisedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who raised it, which is who may not sign it when it is critical** (`signCorrectiveAction`). Null where the action was opened automatically by a reading or a cold-chain breach."},"source":{"type":"string","enum":["temperatureExcursion","coldChainBreach","expiredStock","contamination","pestSighting","equipmentFailure","missedCheck","manual"],"description":"`missedCheck` is raised by the server when a checkpoint goes past its `checkFrequencyMinutes` with no reading (audit R125 (5))."},"sourceRef":{"type":"string","format":"uuid","nullable":true},"severity":{"type":"string","enum":["observation","minor","major","critical"],"description":"**Set by the source when the platform opens it** (decided 28 September, audit R125 (5)): an out-of-range reading or a cold-chain breach opens at `major`, a missed check at `minor`. `critical` is a person's escalation, not a default."},"actionTaken":{"type":"string","nullable":true},"disposal":{"type":"string","enum":["none","discarded","reworked","quarantined","returned"],"nullable":true},"status":{"type":"string","enum":["open","actioned","signed","escalated","closed"]},"signedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"signedAt":{"type":"string","format":"date-time","nullable":true},"escalatedToPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**A critical finding a shift cannot close.** Escalation exists so a supervisor signs what a cook should not. Always the venue's food-safety lead at the time of escalation (`fnb.foodSafetyLeadPrincipalId`, audit R096 (9)).\n"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"CreateAccessPointRequest": {"type":"object","required":["code","name","venueId","direction"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"direction":{"$ref":"#/components/schemas/Direction"},"antiPassbackEnabled":{"type":"boolean","default":false},"requiresExitBeforeReentry":{"type":"boolean","default":false},"driver":{"type":"string"}}},
"CreateAssetRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["assetTag","name","venueId","criticality"],"properties":{"assetTag":{"type":"string","maxLength":64,"x-ticvai-unique":"venue","description":"**Unique per venue** (decided 28 September, audit R108). Two assets in one venue never share a tag; `createAsset` refuses a duplicate with `409` `duplicate-code`. Two venues may each have an `A-001`.\n"},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"criticality":{"$ref":"#/components/schemas/AssetCriticality"},"priorityOverride":{"allOf":[{"$ref":"#/components/schemas/WorkOrderPriority"}],"nullable":true,"description":"**\"If this device goes down, raise this priority\"** (decided 17 September, M17-01). A corrective work order raised on this asset takes this priority instead of the score. Null means the score decides.\n"},"manufacturer":{"type":"string","maxLength":200},"model":{"type":"string","maxLength":200},"serialNumber":{"type":"string","maxLength":128},"commissionedAt":{"type":"string","format":"date"},"warrantyExpiresAt":{"type":"string","format":"date"},"supplierId":{"type":"string","format":"uuid"},"linkedProductIds":{"type":"array","description":"Products this asset delivers. A fault here can stop them selling.\n","items":{"type":"string","format":"uuid"}},"linkedAccessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Access point this asset controls. Out of service blocks it."},"requiresInspectionToReturn":{"type":"boolean","default":false,"description":"True means a completed inspection is required before return to service. A technician cannot simply declare a ride safe.\n"},"documents":{"type":"array","description":"Manuals, procedures, certificates, each with its name and kind. Stored one row per document in `maintenance.asset_document`, which is where `AssetDetail.documents` reads them from.\n","items":{"$ref":"#/components/schemas/AssetDocumentInput"}},"documentRefs":{"type":"array","x-ticvai-persisted":false,"description":"**The refs alone, kept for callers that predate `documents`.** Each ref sent here is stored as an `asset_document` row with no name and no kind. Returned as the refs of `documents`, computed on read — there is no second copy to fall out of step.\n","items":{"type":"string"}}}},
"CreateReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","category","dataSource","columns","requiredPermission"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"category":{"$ref":"#/components/schemas/ReportCategory"},"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"parameters":{"type":"array","items":{"$ref":"#/components/schemas/ReportParameter"}},"requiredPermission":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission","description":"Permission needed to run this report, from the shared `Permission` vocabulary. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"},"maxDateRangeDays":{"type":"integer","nullable":true,"minimum":1,"default":366,"description":"Guards against a query spanning years of scan events. **When a report sets none, 366 days applies (decided 28 September, audit R158)**, so `runReport`'s date-range 400 always has a limit."}}},
"CreateReportScheduleRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["reportId","cadence","recipients","format"],"properties":{"reportId":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":200},"cadence":{"$ref":"#/components/schemas/Cadence"},"parameters":{"type":"object","additionalProperties":true,"description":"As `RunReportRequest.parameters` — keyed by the report's `ReportParameter.key`, applied to every run."},"recipients":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/Recipient"}},"format":{"$ref":"#/components/schemas/ExportFormat"},"includePersonalData":{"type":"boolean","default":false},"skipIfEmpty":{"type":"boolean","default":true,"description":"An empty report every morning trains people to ignore the report."}}},
"CreateScopeNodeRequest": {"type":"object","required":["level","parentId","code","name"],"properties":{"level":{"$ref":"#/components/schemas/ScopeLevel"},"parentId":{"type":"string","format":"uuid","description":"Required for every level except tenant, which the cell creates at provisioning."},"code":{"type":"string","maxLength":64,"pattern":"^[a-z0-9_]+$","description":"Becomes the final ltree segment. Immutable once created."},"name":{"type":"string","maxLength":200}}},
"CreateWorkOrderRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","title","venueId","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"title":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":5000},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"kind":{"allOf":[{"$ref":"#/components/schemas/WorkOrderKind"}],"default":"corrective"},"priority":{"allOf":[{"$ref":"#/components/schemas/WorkOrderPriority"}],"description":"**Optional since 29 September** (M17-01). Sent, it is `manual` and wins. Absent, the asset's `priorityOverride` applies, and failing that the venue's `WorkOrderPriorityPolicy` scores the fault.\n"},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","maxItems":10,"items":{"type":"string"},"description":"Skills the job needs, as qualification codes; `suggestWorkOrderAssignee` ranks by them (M17-13)."},"categoryId":{"type":"string","format":"uuid"},"assignedToPrincipalId":{"type":"string","format":"uuid"},"dueAt":{"type":"string","format":"date-time"},"attachmentRefs":{"type":"array","description":"Photo-first. Expected at creation, not added later from memory.","items":{"type":"string"}},"takeAssetOutOfService":{"type":"boolean","default":false,"description":"Raise and immediately suspend the asset. For a fault found on a live ride, the two are one action.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"DataSource": {"type":"string","description":"What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n\n**`forecastPoints` added 29 September** (8.2.55, build pass, group G2): the points of published AI forecast versions; see `x-ticvai-forecast-points`.\n\n**Three accreditation sources added 29 September** (12.1.50, build pass): `accreditationApplications`, `accreditationHolders` and `accreditationCredentials`, over `accreditation.application`, `accreditation.holder` and `accreditation.credential`. They are what the accreditation KPIs and any accreditation report or export (`exportReportResult`, csv or xlsx) are built over. **All three name a person**, and `REPORT_EXPORT_PII` gates them as it gates `guests`.\n","enum":["orders","orderLines","payments","refunds","shifts","scanEvents","entitlements","products","inventory","stockMovements","stockCounts","waste","workstations","devices","principals","loyalty","reviews","queueEntries","guests","campaigns","cases","ledgerEntries","workOrders","approvals","purchaseOrders","receipts","requisitions","stockBatches","resourceBookings","delegations","forms","challenges","wallets","resaleListings","accreditationApplications","accreditationHolders","accreditationCredentials","forecastPoints"],"x-ticvai-forecast-points":"**`forecastPoints` added 29 September (build pass, group G2; 8.2.55)**: one row per forecast point (`ai.forecast_point`) of a **published** forecast version (`ai.forecast_version` status `published`), with the definition it belongs to (`ai.forecast_definition`: subject, grain, unit), the period, the dimension key and the p10, p50 and p90 values. Draft, awaiting-approval and superseded versions are not reachable, and scenario points (`scenarioId` set) only with the scenario named as a filter: **a forecast leaves the platform as the one somebody published**. It is how a forecast is exported (`runReport` then `exportReportResult`, csv or xlsx), scheduled or put on a dashboard. Names no person, so `REPORT_EXPORT` is enough. Read from the reporting replica of the AI log database (design 2.4), never from the model service.\n"},
"DeliveryLocation": {"type":"object","x-ticvai-persistence":"fnb.delivery_location","required":["id","venueId","kind","label","isServiceable"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/DeliveryLocationKind"},"label":{"type":"string","description":"What a runner is told. \"Cabana 12\", \"Row H Seat 4\", \"Lawn — north gate\"."},"zone":{"type":"string","nullable":true},"tableId":{"type":"string","format":"uuid","nullable":true,"description":"Set where the location is a restaurant table, so it shares table state."},"seatId":{"type":"string","nullable":true,"description":"Set where the seat is the address. References the seat map."},"servingOutletIds":{"type":"array","description":"Which outlets deliver here. A cabana served by the pool bar and not the restaurant is normal, and a location nothing serves is not an address.\n","items":{"type":"string","format":"uuid"}},"isServiceable":{"type":"boolean","description":"False where the location exists but is not currently taking delivery — closed section, weather, no runner on shift.\n"},"unserviceableReason":{"type":"string","nullable":true},"walkTimeMinutes":{"type":"integer","nullable":true,"description":"From the serving outlet. Feeds the guest's estimate — a cabana eight minutes away is not the same promise as a table by the kitchen.\n"}}},
"DeliveryLocationKind": {"type":"string","description":"4.6.26. One concept, because a runner needs one instruction.","enum":["table","seat","cabana","sunbed","poolside","box","suite","lawn","collectionPoint","namedLocation"]},
"DenyReason": {"type":"string","description":"Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n","enum":["notFound","notYetValid","expired","alreadyUsed","reentryLimitReached","exitRequiredBeforeReentry","wrongAccessPoint","wrongPerformance","outsideAdmissionWindow","entitlementSuspended","blacklisted","capacityReached","waiverRequired","accompanimentRequired","mediaDeactivated","unpaid","delegatedRightExhausted","delegatedRightRevoked","journeyNotCovered"]},
"DeploymentProfile": {"type":"string","description":"How this workstation obtains catalogue and inventory (ADR-0013).\n- `terminalLocal` — own SQLite, leases direct from the cell. Small venues, 4G sites - `venueEdge` — own SQLite, distributed via the venue edge node which holds the\n  venue lease and sub-leases to terminals. Mid and large venues, stadium gates\n- `thin` — no local catalogue, server reads. Non-transactional surfaces only\n","enum":["terminalLocal","venueEdge","thin"]},
"DeviceApprovalStatus": {"type":"string","description":"Whether a registered device may go into production (DEC-241, DEC-245; CHG-CSP-011). The model is `states/registered-device-approval.yaml`.\n","enum":["pendingApproval","approved","rejected"]},
"DeviceBinding": {"x-ticvai-persistence":"platform.device","type":"object","required":["kind","driver"],"properties":{"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Driver identifier. Adding a vendor is a driver plus configuration, never a core change — every venue arrives with hardware not previously seen.\n"},"identifier":{"type":"string","description":"Serial","port or network address.":null},"isRequired":{"type":"boolean","default":false,"description":"When true, the workstation refuses to open a shift if the device is absent.\n"}}},
"DeviceCapability": {"type":"string","description":"BL-179. **Something a driver reports, not something the platform provides.** The list grows as vendors are added, which is ADR-0015's whole position: adding a vendor is a driver plus configuration rather than a core change.\n**`genderClassification` is here because `VenueSettings.segregatedAccess. genderVerification` already offers `deviceAssisted` and nothing answered it** — a switch with no driver behind it. Where a venue's access hardware performs the check and the venue chooses to use it, the result is **advisory to the steward and never decisive at the turnstile** (`ValidationResult.advisory`). 3.2.45 asks for rejection; the package deviates deliberately and CF-130 records why.\n**Access's capabilities merged in** (ADR-0067, 1 October): `dynamicQr`, `rfid`, `nfc`, `facePass`, `offline` and `heightCheck` were the access register's own list, from the compatibility matrix.\n","enum":["genderClassification","dynamicQr","rfid","nfc","facePass","offline","heightCheck"]},
"DeviceCredential": {"type":"object","x-ticvai-persistence":"tenancy.device_credential","description":"16.7.35 to 16.7.37. **Per device, with an expiry**, which is what makes retirement and revocation mean anything.\n","properties":{"id":{"type":"string","format":"uuid"},"deviceId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["clientCertificate","deviceToken","mutualTls"]},"fingerprint":{"type":"string","description":"**The identifier, never the secret.** The credential material is returned once at issue and is not readable afterwards.\n"},"issuedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"},"revokedAt":{"type":"string","format":"date-time","nullable":true},"revocationReason":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"DeviceKind": {"type":"string","enum":["receiptPrinter","ticketPrinter","labelPrinter","cashDrawer","barcodeScanner","rfidReader","nfcReader","cardReader","idReader","biometricReader","accessReader","paymentTerminal","customerDisplay","signageDisplay","kitchenDisplay","turnstileController","wristbandEncoder","signaturePad","scale","camera","mobileHandset","handheldScanner","accessPodium","bleBeacon"],"description":"`mobileHandset` (18.1.5, added 29 September): a staff phone or tablet running the staff app, registered for push and bound to no workstation.\n**One kind vocabulary for every device** (ADR-0067, 1 October). `handheldScanner`, `accessPodium` and `bleBeacon` came from Access's register; the finer hardware type (a speed gate under `turnstileController`, a tablet under `handheldScanner`) is `RegisteredDevice.hardwareType` (common `DeviceHardwareType`).\n"},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"ExecutionStatus": {"type":"string","enum":["queued","running","completed","failed","cancelled","expired"]},
"ExportFormat": {"type":"string","enum":["csv","xlsx","pdf","json"]},
"ExternalCredentialSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.external_credential_sources`). Read with the access point when a credential is presented; a source is never queried on its own.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["hotelRoomCard","corporateBadge","cityPass","transitCard","partnerToken"]},"providerName":{"type":"string"},"endpoint":{"type":"string"},"credentialRef":{"type":"string"},"grantsProductId":{"type":"string","format":"uuid"}}}},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"FinancialReport": {"x-ticvai-persistence":"none — computed from replica","type":"object","required":["report","fiscalPeriodId","currency","generatedAt","sections"],"properties":{"report":{"$ref":"#/components/schemas/FinancialReportKind"},"fiscalPeriodId":{"type":"string","format":"uuid"},"legalEntityId":{"type":"string","format":"uuid","nullable":true},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer"},"generatedAt":{"type":"string","format":"date-time"},"sections":{"type":"array","items":{"type":"object","required":["name","lines","total"],"properties":{"name":{"type":"string"},"lines":{"type":"array","items":{"type":"object","properties":{"label":{"type":"string"},"accountCode":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"priorPeriodAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The same line for **the same period last year** (decided 28 September, audit R127 (3)). Absent where that period did not exist."}}}},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"FinancialReportKind": {"type":"string","description":"The report `getFinancialReport` returns. One vocabulary for the query and the response.","enum":["profitAndLoss","balanceSheet","cashFlow","revenueByVenue","revenueByProduct","taxSummary"]},
"FnbDeliveryPolicy": {"type":"object","x-ticvai-persistence":"fnb.delivery_policy","required":["outletId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"outletId":{"type":"string","format":"uuid"},"collectionEnabled":{"type":"boolean","default":true},"deliveryEnabled":{"type":"boolean","default":false},"collectionPoint":{"type":"string","maxLength":200,"nullable":true},"collectionHoldMinutes":{"type":"integer","default":20},"asapCollectionMinutes":{"type":"integer","default":25},"asapDeliveryMinutes":{"type":"integer","default":45},"slotMinutes":{"type":"integer","default":30},"minimumOrder":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"deliveryFee":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"freeDeliveryAbove":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"radiusKm":{"type":"number","minimum":0,"nullable":true},"emiratesServed":{"type":"array","items":{"type":"string"}},"cutleryOptIn":{"type":"boolean","default":true,"description":"Cutlery only when asked for, as in the design."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"GeneratedQuery": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n","properties":{"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"compiledSql":{"type":"string","nullable":true,"description":"The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"}}},
"Incident": {"x-ticvai-persistence":"maintenance.incident","type":"object","required":["id","incidentNumber","kind","severity","status","venueId","occurredAt","reportedByPrincipalId"],"properties":{"id":{"type":"string","format":"uuid"},"incidentNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"kind":{"$ref":"#/components/schemas/IncidentKind"},"severity":{"$ref":"#/components/schemas/IncidentSeverity"},"status":{"$ref":"#/components/schemas/IncidentStatus"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"locationDescription":{"type":"string","nullable":true},"isReportable":{"type":"boolean","description":"Requires notification to an external authority within a statutory window."},"notificationDueAt":{"type":"string","format":"date-time","nullable":true},"notifiedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The earliest `notifiedAt` among this incident's authority notifications. **Maintained on write** by `recordAuthorityNotification`; each notification itself is a row of `maintenance.incident_authority_notification`.\n"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"reportedByPrincipalId":{"type":"string","format":"uuid"},"correctiveWorkOrderId":{"type":"string","format":"uuid","nullable":true},"escalation":{"type":"object","nullable":true,"readOnly":true,"description":"**Set while the incident is escalated** (the optional Escalated step of the 3 October flow; CHG-RUL-011). Screens show \"Escalated\" when `status` is `underInvestigation` and this is set. Cleared when the incident closes.\n","properties":{"toPrincipalId":{"type":"string","format":"uuid"},"byPrincipalId":{"type":"string","format":"uuid"},"reason":{"type":"string"},"escalatedAt":{"type":"string","format":"date-time"}}},"reopenCount":{"type":"integer","minimum":0,"readOnly":true,"description":"How many times the incident was reopened (CHG-RUL-011). Each reopen is a logged row."},"occurredAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"IncidentKind": {"type":"string","enum":["guestInjury","staffInjury","nearMiss","propertyDamage","equipmentFailure","securityIncident","fireOrEvacuation","foodSafety","environmental","other"]},
"IncidentSeverity": {"type":"string","enum":["nearMiss","minor","moderate","major","critical"]},
"IncidentStatus": {"type":"string","enum":["reported","underInvestigation","actionRequired","closed"]},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"MediaKind": {"type":"string","enum":["image","video","audio","document","vector","font","archive"]},
"MetricSource": {"type":"string","description":"**A named metric with a verified source.** BL-053, 75 requirement rows.\n`reporting` is a generic builder, and **a generic builder makes every reporting requirement look covered** — it will happily assemble a report over data nobody produces. That is the shape to watch across the whole walk, and this enum is the answer to it: each value below was checked against the schema before being named.\n| Metric | Source | |---|---| | `occupancy` | `catalogue.channel_capacity.sold` and `leased` against `capacity` | | `capacityUtilisation` | `catalogue.channel_capacity.remaining` over the same window | | `admissionRate` | `access.scan_event.outcome`, in-direction | | `noShowRate` | Entitlements issued against scans that never arrived | | `conversion` | `orders.cart` against `orders.sales_order` | | `salesByOperator` | `orders.sales_order.principal_id` | | `salesByWorkstation` | The workstation on the shift that took it | | `waitTime` | `queue.waiting_guest.estimated_call_at` against `called_at` | | `throughput` | `queue.waiting_guest` completions per hour | | `abandonmentRate` | Queue entries that left before being called |\n**`salesByInstructor` was deliberately absent from the first cut** because it needed the staff-assignment link CL-01 covers. It was added on 18 August once `resources.Resource` produced it — see `x-ticvai-extension-note` below. Naming a metric with no source is still the defect this enum exists to prevent.\n**Money-valued metrics are listed in `x-ticvai-money-valued`.** A reading or threshold on one of them is a `Money`, never a float (`MetricValue`).\n","enum":["occupancy","capacityUtilisation","admissionRate","noShowRate","conversion","salesByOperator","salesByWorkstation","waitTime","throughput","abandonmentRate","inventoryValuation","stockTurnover","stockAgeing","wastageRate","resaleVolume","resaleCommission","salesByInstructor","resourceUtilisation","allocationUtilisation","channelAllocationBurn","membershipChurn","membershipRenewalRate","supplierDeliveryPerformance","revenuePerEntitlement","revenuePerVisitor","assetDowntime","meanTimeToRepair","challengeCompletionRate","attributedRevenue","loyaltyActiveMembers","loyaltyTierDistribution","loyaltyPointsLiability","loyaltyBreakageRate","loyaltyMemberRetention","challengeParticipationRate","gamificationLoyaltyImpact","gamificationMembershipImpact","gamificationRetention","accreditationApplications","accreditationTimeToDecision","accreditationCredentialsIssued","accreditationActiveHolders","accreditationRenewalsDue","staffingShortfall","grossSales","discounts","refunds","netRevenue","recognisedRevenue","deferredRevenue","taxCollected","takings"],"x-ticvai-money-valued":["grossSales","discounts","refunds","netRevenue","recognisedRevenue","deferredRevenue","taxCollected","takings","inventoryValuation","resaleCommission","revenuePerEntitlement","revenuePerVisitor","attributedRevenue","loyaltyPointsLiability"],"x-ticvai-extended-29-september":"**Fourteen metrics added 29 September (build pass)**, each checked against the schema of the contract that produces it.\n\n| Metric | Source | Requirement | |---|---|---| | `loyaltyActiveMembers` | `marketing.loyalty_position` members with a `marketing.loyalty_points` movement in the period | 5.4.27 | | `loyaltyTierDistribution` | `marketing.loyalty_position.tier_id` against `marketing.programme_tier`, members per tier | 5.4.27 | | `loyaltyPointsLiability` | the balance of `ledger.journal_line` on each programme's `pointsLiabilityAccountId`, where points post on accrual and release on redemption or expiry | 5.4.27 | | `loyaltyBreakageRate` | `marketing.loyalty_points` expiry movements over points earned, in the period | 5.4.27 | | `loyaltyMemberRetention` | members with a movement in the previous period who also have one in this period | 5.4.27 | | `challengeParticipationRate` | distinct `marketing.challenge_progress.subject_id` over active loyalty members | 22.6.20 | | `gamificationLoyaltyImpact` | points earned per member, challenge participants against non-participants (`marketing.loyalty_points` split by `marketing.challenge_progress`) | 22.6.20 | | `gamificationMembershipImpact` | joins and renewals in `identity.customer_membership`, participants against non-participants | 22.6.20 | | `gamificationRetention` | return visits (`access.scan_event`, in-direction) of participants against non-participants | 22.6.20 | | `accreditationApplications` | `accreditation.application` by `status` | 12.1.50 | | `accreditationTimeToDecision` | `accreditation.application.decided_at` minus `submitted_at` | 12.1.50 | | `accreditationCredentialsIssued` | `accreditation.credential.issued_at` | 12.1.50 | | `accreditationActiveHolders` | `accreditation.holder` `active`, by `category_code` | 12.1.50 | | `accreditationRenewalsDue` | `accreditation.holder.valid_to` inside `accreditation.validity.renewal_window_days` | 12.1.50 |\n\n**`staffingShortfall` added the same evening (build pass, group G2; 8.2.49)**: the largest gap in the window between the staff rostered and the staff the forecast requires, per venue and position, from `workforce.forecast_requirement` (the handed-over AI staff requirement) against `workforce.rota_assignment` and `workforce.open_shift`, computed as `workforce.getStaffingCoverage` with `basis` `forecastRequirement`. An `AlertRule` on it with `comparator` `above` and `threshold` 0 is the staffing shortage alert; `windowMinutes` looks ahead rather than back for this metric (the rota for the coming window), and `cooldownMinutes` stops one short shift alerting every quarter hour.\n\n**Points issued, points redeemed, campaign performance and reward redemption were already served** by the `loyalty` and `campaigns` sources, and challenge completion and revenue attribution by `challengeCompletionRate` and `attributedRevenue`.\n","x-ticvai-extended-2-october":"**Eight finance measures added 2 October 2026** (Chinmay; CHG-FIN-007, CHG-FIN-010), each with the source and formula of the seeded KPI of the same code in `ReportingSystemKpi`: `grossSales`, `discounts`, `refunds`, `netRevenue`, `recognisedRevenue`, `deferredRevenue`, `taxCollected` and `takings`, so an alert rule can watch them (a refund spike, takings below a target). Formulas are the D-185 default; client finance sign-off is pending.","x-ticvai-money-valued-note":"**`salesByOperator`, `salesByWorkstation` and `resaleVolume` are not listed because the package does not say whether they count sales or sum their value.** Until that is decided, a rule on them carries a plain number.\n","x-ticvai-extended":"18 August 2026","x-ticvai-extension-note":"**Nineteen metrics added when their upstream models landed**, which is how BL-053 was always going to close — not by changing `reporting` but by building the things it wanted to report on.\n`inventoryValuation`, `stockTurnover`, `stockAgeing` and `wastageRate` came from `inventory.StockBatch`; `resaleVolume` and `resaleCommission` from `orders.ResaleListing`; **`salesByInstructor` from `resources.Resource`, which was the one metric this enum deliberately refused to name in the morning** because nothing produced it. `allocationUtilisation` from `PartnerUser` and `ChannelListing`, `membershipChurn` from `Journey`, `supplierDeliveryPerformance` from `ProductionRun`, `assetDowntime` and `meanTimeToRepair` from `WorkOrder.downtimeMinutes`, `challengeCompletionRate` from `ChallengeProgress`, `attributedRevenue` from `AttributionTouch`.\n**Each was checked against the schema before being named.** That rule has not changed — naming a metric with no source is the defect this enum exists to prevent.\n"},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"NaturalLanguageAnswer": {"x-ticvai-persistence":"none — computed","type":"object","required":["conversationId","question","interpretation","result","reliability"],"properties":{"conversationId":{"type":"string"},"question":{"type":"string"},"interpretation":{"type":"string","description":"What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."},"semanticSpec":{"allOf":[{"$ref":"#/components/schemas/ReportingSemanticQuerySpec"}],"nullable":true,"description":"What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"},"generatedQuery":{"allOf":[{"$ref":"#/components/schemas/GeneratedQuery"}],"nullable":true,"description":"The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"},"result":{"allOf":[{"$ref":"#/components/schemas/ReportResult"}],"nullable":true,"description":"Null when the question is outside the semantic model."},"dataAsOf":{"type":"string","format":"date-time","nullable":true,"description":"Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."},"reliability":{"$ref":"#/components/schemas/ReportingAnswerReliability"},"unavailableReason":{"allOf":[{"$ref":"#/components/schemas/ReportingUnavailableReason"}],"nullable":true,"description":"Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."},"confidence":{"type":"number","minimum":0,"maximum":1,"deprecated":true,"description":"Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."},"suggestedFollowUps":{"type":"array","items":{"type":"string"}},"modelVersion":{"type":"string"},"tokensUsed":{"type":"integer"}}},
"OfflinePackage": {"x-ticvai-persistence":"none — generated artefact in object storage","type":"object","required":["etag","generatedAt","validFrom","validTo","accessPointId","entitlements"],"properties":{"etag":{"type":"string"},"generatedAt":{"type":"string","format":"date-time"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"accessPointId":{"type":"string","format":"uuid"},"entitlementsVersion":{"type":"integer","description":"The highest `access.entitlement` change included (SD-052, 29 September). A refresh sends it as `sinceVersion` and receives only what changed after it, so a 60,000-guest venue is not re-sent whole."},"policySetVersion":{"type":"string","description":"**The active admission policy version the package carries** (ADR-0068, 1 October): a fingerprint of the `(id, currentVersion)` of every policy in `dynamicPolicies`, computed the same way by `validateAccess` online. Every scan the gate records carries it (`ScanEvent.policySetVersion`), so a scan decided offline under a set that has since changed is visible at sync rather than assumed equal."},"dynamicPolicies":{"type":"array","description":"The active guest-admission dynamic policies for this access point's zones (SD-052), each at its active version with its `conditionRule` (ADR-0068), so an offline gate applies the same rules as an online one.","items":{"$ref":"#/components/schemas/AccessDynamicPolicy"}},"entitlements":{"type":"array","description":"Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device removes them.","items":{"type":"object","required":["ticketId","mediaCodes","validFrom","validTo","entriesAllowed","reentryAllowed"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"The `Entitlement.id`."},"mediaCodes":{"type":"array","items":{"type":"string"},"description":"A ticket may carry several media over its life."},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesAllowed":{"type":"integer","nullable":true},"entriesUsed":{"type":"integer"},"reentryAllowed":{"type":"boolean"},"admissionRulesId":{"type":"string","format":"uuid"}}}},"delegatedRights":{"type":"array","description":"Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits when the inter-cell link is down — the same reason locally issued entitlements are included.\n","items":{"type":"object","required":["rightId","ticketId","issuingCellId","validFrom","validTo","entriesAllowed","entriesConsumed"],"properties":{"rightId":{"type":"string"},"ticketId":{"type":"string","format":"uuid","description":"The `Entitlement.id` in the issuing cell."},"issuingCellId":{"type":"string"},"guestLinkId":{"type":"string","nullable":true},"mediaCodes":{"type":"array","items":{"type":"string"}},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"entriesAllowed":{"type":"integer","nullable":true},"entriesConsumed":{"type":"integer"},"admissionRulesId":{"type":"string","format":"uuid"}}}},"blacklist":{"type":"array","items":{"type":"string"},"description":"Media codes to deny outright regardless of entitlement state."},"admissionRules":{"type":"array","items":{"type":"object","required":["id","openMinutesBefore","closeMinutesAfter"],"properties":{"id":{"type":"string","format":"uuid"},"openMinutesBefore":{"type":"integer"},"closeMinutesAfter":{"type":"integer"},"maxDurationMinutes":{"type":"integer","nullable":true},"requiresExitBeforeReentry":{"type":"boolean"}}}},"accreditationCredentials":{"type":"array","description":"Accreditation credentials that admit at this access point, from access.accreditation_credential (29 September, build; BL-181). Only rows that admit are included; a credential dropped from one package to the next no longer admits.","items":{"$ref":"#/components/schemas/AccessAccreditationCredential"}}}},
"OfflineScan": {"x-ticvai-persistence":"none — client-side journal","allOf":[{"$ref":"#/components/schemas/ValidateRequest"},{"type":"object","required":["sequence","localOutcome"],"properties":{"sequence":{"type":"integer","minimum":1,"description":"Monotonic per device. The server processes in this order."},"localOutcome":{"allOf":[{"$ref":"#/components/schemas/ScanOutcome"}],"description":"What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded.\n"},"localDenyReason":{"$ref":"#/components/schemas/DenyReason"},"overriddenByPrincipalId":{"type":"string","format":"uuid","nullable":true},"overrideReason":{"type":"string","nullable":true}}}]},
"OpeningHoursWindow": {"type":"object","description":"26 September, pull audit R088. **One weekly window an outlet is open.** `Outlet.openingHours` was an array of untyped objects. The shape is the one `supportHours.windows` already uses — a day and a from/to — with the times as local `HH:MM` in the region's time zone. Several windows on one day are a split shift, such as lunch and dinner.\n","required":["day","from","to"],"properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet opens."},"to":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet closes."},"endsNextDay":{"type":"boolean","default":false,"description":"**A late-night window is one window past midnight** (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-731; DEC-197; CHG-CSP-007). A bar open 23:00 to 01:00 on Friday is `day: fri`, `from: '23:00'`, `to: '01:00'`, `endsNextDay: true`: one service period, and its takings belong to Friday's trading day, not split across two days. With `endsNextDay` false, `to` must be later than `from` (`422 window-ends-before-start`); with it true, `to` must be earlier than or equal to `from`, so a window never spans more than 24 hours.\n"}}},
"OrgUnit": {"x-ticvai-persistence":"platform.scope","type":"object","required":["id","level","path","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"level":{"$ref":"#/components/schemas/ScopeLevel"},"parentId":{"type":"string","format":"uuid","nullable":true},"path":{"type":"string","description":"Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`.","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"isActive":{"type":"boolean","description":"False causes every permission query at or beneath this node to resolve to DENY.\n"},"childCount":{"type":"integer","minimum":0}}},
"Outlet": {"type":"object","x-ticvai-persistence":"platform.outlet","required":["id","code","name","venueId","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200,"description":"The outlet's name in English. Other languages are `nameTranslations` (CHG-CSP-005)."},"nameTranslations":{"$ref":"#/components/schemas/OutletNameTranslations"},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/OutletKind"},"outletType":{"allOf":[{"$ref":"#/components/schemas/OutletType"}],"nullable":true,"description":"The service model (DI-319; DEC-196; CHG-CSP-005). Null on an outlet that is not F&B or retail."},"departmentId":{"type":"string","format":"uuid","nullable":true,"description":"**The department the outlet belongs to** (DI-319: department, sub-department, cost centre and status; DEC-196; CHG-CSP-005): an `OrgUnit` of kind department, as `Workstation.departmentId`. The outlet itself is the sub-department, so it needs no second field.\n"},"zone":{"type":"string","nullable":true},"stockLocationId":{"type":"string","format":"uuid","nullable":true,"description":"Where this outlet draws stock from. A shop and its stockroom are one location; a bar drawing from a central cellar is not.\n"},"costCenterId":{"type":"string","format":"uuid","nullable":true,"description":"Revenue and cost attribution. Outlet is the natural grain for both."},"paymentTiming":{"allOf":[{"$ref":"#/components/schemas/OutletPaymentTiming"}],"default":"sendFirst","description":"Pay first, or send to the kitchen first then pay (DEC-064; CHG-CSP-004)."},"admissionContext":{"allOf":[{"$ref":"#/components/schemas/OutletAdmissionContext"}],"default":"insideVenue","description":"Inside the venue (needs an admission ticket) or standalone (no ticket) (DEC-070; CHG-CSP-004)."},"producesForOutletIds":{"type":"array","default":[],"description":"**One kitchen serving several outlets is a producing outlet** (decided 2 October 2026, Chinmay, batch 6 set 5, BO-134: \"Yes: via a producing outlet (one kitchen outlet produces for several)\"; DEC-188; CHG-CSP-005). The outlets this one prepares food for, in the same venue. The model stays per outlet (DI-330): each outlet keeps its own menu and stations, and an order at a listed outlet may route to this outlet's kitchen stations (fnb `KitchenStation`). Empty on an outlet that only produces for itself. An outlet may not list itself, an outlet of another venue (`422 outlet-not-in-venue`), or one that lists it back.\n","items":{"type":"string","format":"uuid"}},"saleBoardId":{"type":"string","format":"uuid","nullable":true,"description":"**The till layout every till in this outlet uses, unless a till overrides it** (decided 2 October 2026, Chinmay, batch 6 set 4, BO-109: \"Per outlet, with a till override\"; DEC-183; CHG-CSP-006). DI-326 puts the layout at the outlet; MATRIX 2.1.9 binds a board to a workstation. Both hold: a workstation with no board of its own (`ConfigureWorkstationRequest.saleBoardId` absent or null) uses this one, and `Workstation.saleBoardSource` says which applied.\n"},"openingHours":{"type":"array","description":"The weekly pattern, one entry per window. Several windows on a day are allowed.","items":{"$ref":"#/components/schemas/OpeningHoursWindow"}},"isActive":{"type":"boolean"}}},
"OutletAdmissionContext": {"type":"string","description":"**Whether an outlet sits behind the admission gate** (decided 2 October 2026, Chinmay, batch 1, WEB-036: \"Inside the venue, a ticket is needed. A restaurant outside the venue (standalone) can sell without one\"; DEC-070; CHG-CSP-004). `insideVenue` (the default): a guest ordering food needs an admission ticket or a place inside, as DI-292 (14 August) decided. `standalone`: a restaurant outside the gate, which may sell takeaway and delivery (DI-1039) with no ticket. DI-292 is amended for standalone outlets only. The admission check itself stays in Access (ADR-0068). F&B keeps its own payment and its own receipt either way. **The canonical name** (2 October 2026, CHG-CLN-008): the field is `admissionContext` on the outlet and on F&B's guest `DiningOutlet`; common `OutletSiting` and the word \"siting\" are deprecated aliases of this.\n","enum":["insideVenue","standalone"]},
"OutletKind": {"type":"string","enum":["shop","restaurant","bar","cafe","kiosk","gameFloor","ticketOffice","mobile"]},
"OutletNameTranslations": {"type":"object","x-ticvai-persistence":"none — jsonb column on platform.outlet","description":"**The outlet's name in other languages, keyed by ISO 639-1 code** (decided 2 October 2026, Chinmay, batch 2 #26, BO-044: \"Yes, where a country needs it: the local language plus English\"; DEC-031; CHG-CSP-005). `Outlet.name` stays the English name. Where the region requires a local name (`RegionSettings.localLanguageNameLocales`, Arabic in the UAE), creating or amending an outlet without it is refused `422 local-name-required`. The same shape as catalogue's `LocalisedText` (DI-210).\n","additionalProperties":{"type":"string","maxLength":200}},
"OutletPaymentTiming": {"type":"string","description":"**When an F&B order is paid, set per outlet** (Chinmay, 2 October, workbook Q64; refines audit R261 per outlet; CHG-CSA-010). `sendFirst`, the default and R261's rule: the order goes to the kitchen, then the till charges (table service, and quick service where the venue wants the kitchen started while the guest pays). `payFirst`: the till charges before anything reaches the kitchen; an unpaid order at a `payFirst` outlet is never sent (`fnb.createFnbOrder`, `fnb.fireCourse`). Shared because the outlet (tenancy `Outlet`) holds it and F&B enforces it.\n","enum":["sendFirst","payFirst"],"default":"sendFirst"},
"OutletType": {"type":"string","description":"**How an F&B or retail outlet trades, which switches features on or off** (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-729: \"Add both fields: outlet type and department (DI-319)\"; DEC-196; CHG-CSP-005). DI-319: a quick-service outlet needs no table booking, a fine-dining outlet needs a table layout. `kind` stays the physical place (a shop, a restaurant, a kiosk); this is the service model inside it. `commissary` is a producing kitchen (DEC-186, DEC-188).\n","enum":["fineDining","casualDining","quickService","coffeeShop","barLounge","foodCourt","buffet","commissary","retail"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Recipient": {"x-ticvai-persistence":"reporting.schedule_recipient","type":"object","description":"One recipient of a schedule. **A row of `reporting.schedule_recipient`, a child of `reporting.schedule`** — `ReportSchedule` declares the pair, which is what gives the table its `schedule_id`. Pull audit 26 September: declared on its own, the table had no column tying a recipient to its schedule.\n","required":["kind","address"],"properties":{"kind":{"type":"string","enum":["principal","email","sftp","webhook"]},"address":{"type":"string"},"principalId":{"type":"string","format":"uuid"}}},
"RegisteredDevice": {"x-ticvai-persistence":"platform.device","type":"object","description":"**The only device register** (ADR-0067, accepted 1 October; the register of record since 29 September). Identity (kind, hardware type, model, serial), every version (firmware, configuration, rule package, credential package), health, heartbeat and one lifecycle (`enrolmentState`: registered, enrolled, provisioned, active, deactivated, retired) for every device in the estate live on this row. The access-control device row, which repeated serial, versions, health and lifecycle, is now `access.device_placement` and holds only where an access-control device is placed. Tenancy owns and migrates this table; Access reads it only through this contract.\n","required":["id","kind","driver"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Built to an open standard where one exists — ESC/POS, UnifiedPOS, OSDP. Adding a vendor is a driver plus configuration, not a core change (ADR-0015).\n"},"identifier":{"type":"string","nullable":true},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Required for every kind except `mobileHandset`, which is bound to no workstation (18.1.5, 29 September), and except an access-control device (one with a `hardwareType`), which is placed in the gate topology by access `placeAccessDevice` rather than bound to a workstation (ADR-0067); `registerDevice` refuses either mistake with `422`.\n"},"model":{"type":"string","nullable":true},"hardwareType":{"$ref":"../shared/common.yaml#/components/schemas/DeviceHardwareType","nullable":true,"description":"**The specific hardware under `kind`** (ADR-0067, 1 October): Access's hardware types (a speed gate, a tripod turnstile, a podium) merged into the one register. Null for a device with no finer type than its kind.\n"},"hardwareModelId":{"type":"string","format":"uuid","nullable":true,"description":"The model in the hardware library (access `setHardwareModel`; ADR-0067). Access owns the library; this names a model in it.\n"},"serialNumber":{"type":"string","nullable":true,"maxLength":100,"description":"The manufacturer's serial (ADR-0067: was on the access-control device row, now `access.device_placement`). A serial already registered in the tenant is refused `409` by `registerDevice`.\n"},"ipNetworkReference":{"type":"string","nullable":true,"description":"Network address or reference the device is reached at (ADR-0067)."},"configurationVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Access configuration version the device reports running (ADR-0067)."},"localRuleVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Admission rule package the device reports running (ADR-0067)."},"credentialSecurityPackageVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Credential security package the device reports running (ADR-0067)."},"scannerHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Component health as the device or vendor reports it on its heartbeat (ADR-0067)."},"controllerHealth":{"type":"string","nullable":true,"readOnly":true},"cameraHealth":{"type":"string","nullable":true,"readOnly":true,"description":"Where the device has a camera."},"connectivity":{"type":"string","nullable":true,"readOnly":true,"description":"Reported connectivity."},"pushToken":{"type":"string","format":"password","nullable":true,"writeOnly":true,"description":"BL-163. **Guest devices register for push and staff devices did not** — `registerGuestDevice` exists with a token, platform and failure count, and a scanner that cannot be told anything is a scanner somebody has to walk to.\nWrite-only, and marked `writeOnly`: accepted by `registerDevice` and never returned by `listDevices` or `getDevice`. **A push token is a credential**, and the rule that no surface holds a provider key applies here too.\n"},"pushPlatform":{"type":"string","nullable":true,"enum":["ios","android","web","windows"]},"pushFailureCount":{"type":"integer","default":0,"readOnly":true,"description":"**Consecutive failures.** A token that has failed repeatedly is a device that was wiped or reassigned, and continuing to push to it is how a notification queue fills with nothing.\n"},"offlineScope":{"type":"string","nullable":true,"enum":["none","readOnly","sellAndScan","fullVenue"],"description":"BL-163. **What this device may do with no connection**, which was unstated for the staff app while `venue-pos` and `venue-scanner` had it settled.\n**`fullVenue` on a personal handset is a decision, not a default** — a device that can do everything offline is a device that carries the whole venue's data in somebody's pocket.\n"},"firmwareVersion":{"type":"string","nullable":true,"readOnly":true,"description":"As the device last reported it on its heartbeat."},"isRequired":{"type":"boolean","description":"True blocks shift open when the device is unreachable."},"status":{"type":"string","readOnly":true,"enum":["online","offline","error","consumableLow","needsAttention","localMode","unknown"],"description":"What the device last said on its heartbeat; `unknown` until it has. `localMode` is an access-control device validating from its offline package with its link down (ADR-0067).\n"},"batteryPercent":{"type":"integer","nullable":true,"readOnly":true,"minimum":0,"maximum":100,"description":"Board 1 of the client's POS design set, 20 August. **A wristband encoder at 8% is a gate that stops working in an hour**, and nothing in the package carried it.\n**Null where the device has no battery**, which is most of them — a receipt printer reporting 100% forever is worse than one reporting nothing.\n"},"lastCheckedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Distinct from `lastHeartbeatAt`.** A heartbeat is the workstation saying the device is attached; a check is the device answering. **A printer with no paper heartbeats perfectly**, which is why the client's board shows both columns.\n"},"health":{"type":"string","enum":["healthy","warning","degraded","offline","unknown"],"default":"unknown","readOnly":true,"description":"**Derived, not reported.** Computed from heartbeat age, battery, firmware currency and error rate — a device does not know whether it is healthy, and asking it produces a fleet that is 100% healthy and 12% broken.\n"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"capabilities":{"type":"array","readOnly":true,"items":{"$ref":"#/components/schemas/DeviceCapability"},"description":"BL-179. **What this driver reports it can do, beyond reading media.** ADR-0015 is standards-first — the device does what the device does — and until now a venue could switch on a feature that depended on hardware without anything being able to say whether the hardware was there.\n**A capability absent is a capability unavailable**, not a capability assumed. A venue setting that requires one is refused where no device in scope reports it, rather than silently doing nothing at the gate.\n"},"enrolmentState":{"type":"string","enum":["registered","enrolled","provisioned","active","deactivated","retired"],"default":"registered","readOnly":true,"description":"BL-160. **Where the device is in its life, which is not the same question as whether it is answering.** `enrolDevice` has taken the whole matrix — registered, enrolled, provisioned, active, deactivated, retired — since 16.1.2, and until now there was no column for it to land in, so the operation read this table and wrote nothing.\n**Distinct from `status` and from `health`.** `status` is what the device last said and `health` is what we computed from it; a decommissioned turnstile still sitting on the network is `online` and `retired` at once, and neither column contradicts the other. **A device that is `retired` is refused at the gate whatever its status says.**\nThe transition itself — who moved it, from what, and why — is a `tenancy.device_audit` record. It is not repeated here, because the latest transition stored in two places is one place to go stale.\n"},"retiredAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set when `enrolmentState` reaches `retired`, and null otherwise.** Derivable from `tenancy.device_audit`, and kept as a column for the same reason `maintenance.asset.retired_on` is one: a retirement date you reconstruct from an audit log is a date nobody filters a fleet by.\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**The profile this device was provisioned with.** `enrolDevice` has accepted one since 16.1.3 and there was nowhere to keep it, so the answer to *\"what is this reader configured as\"* lived only in the request that set it.\n"},"approvalStatus":{"allOf":[{"$ref":"#/components/schemas/DeviceApprovalStatus"}],"default":"pendingApproval","readOnly":true,"description":"**A new device waits for approval before it may go live** (decided 2 October 2026, Chinmay, critical set 1, BO-196: \"Secure enrolment code + pending approval\"; DEC-241; CHG-CSP-011; MoM 15 September, DI-892, DI-906). Every device registers `pendingApproval`. It may enrol and be provisioned and tested, but `enrolDevice` refuses `active` until `approveDevice` approves it (`409 device-approval-required`). A separate axis from `enrolmentState`, which keeps its r1 values; the model is `states/registered-device-approval.yaml`.\n"},"enrolmentCode":{"type":"string","nullable":true,"readOnly":true,"maxLength":12,"description":"**A one-time code the device must present to enrol** (DEC-241; CHG-CSP-011). Issued by `registerDevice` and returned once, in its response only; every later read returns null. The installer enters it on the device, and `enrolDevice` to `enrolled` must carry the same code before `enrolmentCodeExpiresAt` (`422 enrolment-code-invalid`). A device that never presents it never gets an identity, so a box plugged into the venue network cannot claim to be a reader.\n"},"enrolmentCodeExpiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the enrolment code stops working (24 hours after registration, proposed; client to correct)."},"testedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who recorded the device's acceptance test (`DeviceEnrolment.testResult` on the move to `provisioned`). The approver must be someone else (DEC-245).\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who approved the device into production, never the person who tested it** (decided 2 October 2026, Chinmay, critical set 1, BO-203: \"Approver must differ from the tester\"; DEC-245; CHG-CSP-011). `approveDevice` refuses the tester with `403 approver-is-tester`.\n"},"approvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"ReportCategory": {"type":"string","enum":["sales","admission","financial","inventory","guest","operations","marketing","workforce","compliance","custom"]},
"ReportColumn": {"x-ticvai-persistence":"reporting.report_column","type":"object","required":["field"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"field":{"type":"string"},"label":{"type":"string"},"aggregation":{"allOf":[{"$ref":"#/components/schemas/Aggregation"}],"default":"none"},"sortOrder":{"type":"integer"},"sortDirection":{"type":"string","enum":["asc","desc"]},"format":{"type":"string","nullable":true},"role":{"type":"string","nullable":true,"enum":["dimension","measure"],"description":"**What the column is to a chart** (decided 2 October 2026, Chinmay; CHG-FIN-007). A `dimension` groups (date, venue, channel, product); a `measure` is aggregated (sum of net revenue, count of admissions). Null on a column only a table shows."},"encoding":{"type":"string","nullable":true,"enum":["category","x","y","series","value","size","colour","location","stage","source","target","row","column","hierarchyLevel","label","tooltip"],"description":"**Which field well the column fills** (CHG-FIN-007), the binding the twenty marks of `DashboardTile.visualisation` need. The per-mark rule is on that field."},"axis":{"type":"string","nullable":true,"enum":["primary","secondary"],"description":"For a measure on a `combo`, the axis it is drawn against. A secondary axis needs its own `unitLabel` (CHG-FIN-007)."},"seriesType":{"type":"string","nullable":true,"enum":["bar","line","area"],"description":"For a measure on a `combo`, how that series is drawn (CHG-FIN-007)."},"hierarchyLevel":{"type":"integer","nullable":true,"minimum":1,"description":"For `matrix` rows and columns, `treemap` nesting and `decompositionTree` levels, the depth of this dimension, 1 outermost. Levels must follow a real hierarchy (DI-709), for example year, month, day, or region, venue, outlet (CHG-FIN-007)."},"unitLabel":{"type":"string","nullable":true,"maxLength":40,"description":"The unit an axis states, for example \"AED\" or \"Admissions\". Required on a secondary axis (CHG-FIN-007)."}}},
"ReportDefinition": {"x-ticvai-persistence":"reporting.report_definition + reporting.report_column + reporting.report_filter","allOf":[{"$ref":"#/components/schemas/CreateReportRequest"},{"type":"object","required":["id","version","isSystem","isRetired","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"version":{"type":"string","description":"The current version. Assigned by the server on each publish; earlier ones are kept as `ReportDefinitionVersion`."},"isSystem":{"type":"boolean","description":"Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). **Clone-only (decided 28 September, audit R096)**: `updateReport` and `deleteReport` refuse it with 409 `system-report`; a venue changes a copy made with `createReport`.\n"},"isRetired":{"type":"boolean"},"estimatedCost":{"type":"string","enum":["low","medium","high"],"description":"Informs whether it may run inline or must be queued."},"createdByPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}}]},
"ReportExecution": {"x-ticvai-persistence":"reporting.execution","type":"object","required":["id","reportId","definitionVersion","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"reportId":{"type":"string","format":"uuid"},"reportName":{"type":"string"},"definitionVersion":{"type":"string","description":"The version this ran against. With the parameters and scope below, it is everything needed to reproduce the result.\n"},"status":{"$ref":"#/components/schemas/ExecutionStatus"},"parameters":{"type":"object","additionalProperties":true,"description":"The parameters it ran with, keyed by `ReportParameter.key` of `definitionVersion` — defaults filled in, so the record is complete."},"scopeApplied":{"type":"array","description":"Scope paths the caller held. What constrained the result.","items":{"type":"string"}},"rowCount":{"type":"integer","nullable":true},"durationMs":{"type":"integer","nullable":true},"error":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"scheduleId":{"type":"string","format":"uuid","nullable":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true,"description":"Results are retained for a limited period, then discarded."}}},
"ReportFilter": {"x-ticvai-persistence":"reporting.report_filter","type":"object","required":["field","operator"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"field":{"type":"string"},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","contains","isNull","isNotNull"]},"value":{"description":"**Open on purpose; its type is the field's.** One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a string. Absent for `in`, `notIn`, `between`, `isNull` and `isNotNull`.\n"},"values":{"type":"array","description":"The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`.","items":{}},"isParameter":{"type":"boolean","default":false,"description":"Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope.\n"}}},
"ReportParameter": {"x-ticvai-persistence":"reporting.report_parameter","type":"object","required":["key","label","type","isRequired"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"},"isRequired":{"type":"boolean"},"defaultValue":{"description":"Open on purpose. A value of this parameter's `type`, used when a run supplies none."}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"ReportSchedule": {"x-ticvai-persistence":"reporting.schedule + reporting.schedule_recipient","allOf":[{"$ref":"#/components/schemas/CreateReportScheduleRequest"},{"type":"object","required":["id","ownerPrincipalId","isPaused","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid","description":"The schedule runs under this principal's permissions, not the recipients'. A standing grant of whatever the owner can see.\n"},"isPaused":{"type":"boolean"},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"lastRunStatus":{"$ref":"#/components/schemas/ExecutionStatus"},"nextRunAt":{"type":"string","format":"date-time","nullable":true},"consecutiveFailures":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"}}}]},
"ReportingAnswerReliability": {"type":"string","description":"**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},
"ReportingSemanticQuerySpec": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n","required":["metric","period"],"properties":{"metric":{"type":"string","description":"A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."},"dimensions":{"type":"array","maxItems":5,"description":"Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.","items":{"type":"string"}},"filters":{"type":"array","items":{"type":"object","required":["field","operator"],"properties":{"field":{"type":"string","description":"A `SemanticModel` field code."},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","isNull","isNotNull"]},"values":{"type":"array","description":"**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n","items":{}}}}},"period":{"type":"string","description":"ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."},"comparison":{"type":"string","nullable":true,"description":"As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.","enum":["previousPeriod","samePeriodLastYear","target","benchmark"]},"semanticModelVersion":{"type":"integer","readOnly":true,"description":"The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."}}},
"ReportingUnavailableReason": {"type":"string","description":"Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.","enum":["metricNotModelled","dimensionNotModelled","filterNotModelled","comparisonNotAvailable","periodOutsideHistory"]},
"ResolutionCode": {"type":"string","enum":["repaired","partReplaced","adjusted","cleaned","noFaultFound","referredExternal","replaced","deferred"]},
"ReturnCondition": {"type":"string","description":"Determines whether stock is restored or written off.","enum":["resaleable","opened","damaged","faulty","missingParts"]},
"ReturnPolicy": {"x-ticvai-persistence":"retail.return_policy","type":"object","required":["outletId","defaultWindowDays","requiresReceipt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"outletId":{"type":"string","format":"uuid"},"defaultWindowDays":{"type":"integer","minimum":0},"requiresReceipt":{"type":"boolean","default":true},"allowCashRefundOnCardSale":{"type":"boolean","default":false},"selfAuthoriseLimit":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Up to this, one cashier may accept a return alone."},"requiresSecondUserAbove":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"requiresApprovalAbove":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"restockableConditions":{"type":"array","description":"Conditions that return stock to sale. Everything else is written off.\n\nStored as a `text[]` column on `retail.return_policy`, like `nonReturnableCategoryIds`. The items wrap the enum in `allOf` so the schema derivation reads a list of values rather than a child table.\n","items":{"allOf":[{"$ref":"#/components/schemas/ReturnCondition"}]}},"nonReturnableCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"RunReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","properties":{"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"},"venueId":{"type":"string","format":"uuid","description":"Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"},"dateFrom":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."},"dateTo":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (audit R158)."},"forceAsync":{"type":"boolean","default":false,"description":"Queue regardless of size, for a result to be collected later."}}},
"SaleBoardKind": {"type":"string","enum":["ticketing","fnb","retail","mixed"]},
"ScanAnomalyRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.scan_anomaly_rules`). Read with the access point at validation, and a rule is never queried on its own.\n","items":{"type":"object","properties":{"rule":{"type":"string","enum":["simultaneousEntry","impossibleTravelTime","rapidReentry","sharedDevice","velocityBreach"]},"action":{"type":"string","enum":["log","flag","requireSupervisor","deny"]},"thresholdSeconds":{"type":"integer","nullable":true}}}},
"ScanEvent": {"x-ticvai-append-only":"recordedAt","x-ticvai-persistence":"access.scan_event","type":"object","required":["id","accessPointId","venueId","outcome","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The scan's client-generated UUIDv7, the key offline replay deduplicates on."},"accessPointId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"ticketId":{"type":"string","format":"uuid","nullable":true,"description":"The `Entitlement.id` scanned; null where the media resolved to nothing."},"mediaCode":{"type":"string","nullable":true},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"direction":{"$ref":"#/components/schemas/Direction"},"operatorPrincipalId":{"type":"string","format":"uuid","nullable":true},"deviceId":{"type":"string","format":"uuid","nullable":true},"overridesScanId":{"type":"string","format":"uuid","nullable":true,"description":"**Set only on an override row**, naming the denied scan it admits against (decided 28 September, audit R228). The denied scan itself is never updated: the denial and the override are two rows, and at most one override row names any scan. Null on every other scan.\n"},"overrideReason":{"type":"string","nullable":true,"description":"The supervisor's justification, on the override row only. The overriding principal is that row's `operatorPrincipalId`."},"dynamicPolicyId":{"type":"string","format":"uuid","nullable":true,"description":"The dynamic access policy (`access.dynamic_policy`) whose result decided this scan; null when no dynamic policy matched and the entitlement alone decided (added 29 September, build pass, 3.3.48). `listDynamicPolicyEffectiveness` counts from it."},"dynamicPolicyVersion":{"type":"integer","minimum":1,"nullable":true,"description":"The version of that policy in force at the scan, so a report spanning a change counts each version apart."},"dynamicPolicyResult":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"],"nullable":true,"description":"What the policy decided, which for a step-up is not the same as the scan's outcome."},"quantity":{"type":"integer","minimum":1,"default":1,"description":"Admissions this scan counted. More than one only for a group wave (`validateGroupAccess`) or a quantity entitlement consumed in one pass (added 29 September, data-model close-out DM1)."},"localSequence":{"type":"integer","nullable":true,"description":"The device-local sequence number of a scan recorded offline; null for an online scan (added 29 September, data-model close-out DM1)."},"policySetVersion":{"type":"string","nullable":true,"description":"The admission policy set the scan was decided under (`OfflinePackage.policySetVersion`, or the same fingerprint computed online by `validateAccess`), beside the one policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`). ADR-0068, 1 October."},"packageVersion":{"type":"string","nullable":true,"description":"The offline package (`access.edge_package`) the device validated against; null for an online scan (added 29 September, data-model close-out DM1)."},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while pending. Differs from recordedAt for offline scans."}}},
"ScanOutcome": {"type":"string","enum":["admitted","denied","overridden"]},
"ScanSyncResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["accepted","results"],"properties":{"accepted":{"type":"integer","description":"Entries processed before any stop."},"stoppedAtSequence":{"type":"integer","nullable":true,"description":"Sequence of the first entry that could not be processed. Null when the whole batch succeeded. The client retries from here — never past it.\n"},"results":{"type":"array","items":{"type":"object","required":["id","sequence","status"],"properties":{"id":{"type":"string"},"sequence":{"type":"integer"},"status":{"type":"string","enum":["accepted","duplicate","reconciled","rejected"]},"serverOutcome":{"$ref":"#/components/schemas/ScanOutcome"},"divergence":{"type":"string","nullable":true,"description":"Present when `reconciled` — the device admitted and the server would have denied, or vice versa. Surfaced to the operator, not swallowed.\n"},"error":{"$ref":"../shared/common.yaml#/components/schemas/Problem"}}}}}},
"ScopeLevel": {"type":"string","description":"**The eight organisational levels, plus `subject`.** Restored 24 August.\n`tenancy.yaml` holds the authoritative definition of the eight levels and this mirrors them so a contract can reference a level without depending on the whole tenancy surface. **Seven organisational levels plus `outlet`** — a commercial branch beside the organisational one (CF-138, ADR-0018). **A department has requisitions and rotas; an outlet has a menu and stock**, and modelling a restaurant as a department would put it in the staffing tree.\n\n**`subject` is the one value tenancy does not have, and it is not a level.** It is here because `check-package` reads this enum as the closed vocabulary for `x-ticvai-scope-level`, and some operations act on one guest's own resources, which sit in no node of the venue hierarchy. So `subject` is valid as an operation's scope level and never as a `ScopeRef.level`: every `ScopeRef` is a row of `platform.scope`, and those carry one of the eight.\n","enum":["tenant","brand","region","venue","department","subDepartment","workstation","outlet","subject"]},
"Shift": {"x-ticvai-persistence":"orders.pos_shift + orders.pos_shift_approval + orders.pos_shift_incident","description":"**`approvals` and `incidents` are child rows** (26 September, pull audit R099): `orders.pos_shift_approval` and `orders.pos_shift_incident`, one row per item, keyed to the shift. Until then the contract carried both and `orders.pos_shift` had nowhere to put either.\n","type":"object","required":["id","workstationId","venueId","scopePath","principalId","status","currency","currencyScale","openedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key."},"workstationId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"principalId":{"type":"string","format":"uuid","description":"Who opened it. Cash reconciles to a person and a drawer."},"principalDisplayName":{"type":"string"},"incidents":{"type":"array","description":"BL-097. **A till has exceptions and there was nowhere to write them** — a no-sale, a drawer opened without a transaction, a manager override, a guest dispute.\n**This is the log a cash-up investigation starts from**, and a shift that balances with four unexplained no-sales is not a shift that balanced.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["noSale","drawerOpen","override","voidAfterPayment","guestDispute","tillJam","priceQuery","other"]},"at":{"type":"string","format":"date-time"},"principalId":{"type":"string","format":"uuid"},"note":{"type":"string","nullable":true}}}},"status":{"$ref":"#/components/schemas/ShiftStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"depositBoxCode":{"type":"string","nullable":true},"bagNumber":{"type":"string","nullable":true},"openingFloat":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"salesTotal":{"x-ticvai-column":"gross_sales_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till took in sales, as the guest paid it — tax included: the shift's takings, not Gross sales (CHG-FIN-002, CHG-FIN-010). **Never shown to the shift's own cashier before the count is in** (CHG-FIN-003): with the float and the lifts it gives away the expected cash.\n"},"refundsTotal":{"x-ticvai-column":"gross_refunded_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till paid back, as the guest was refunded it — tax included."},"liftsTotal":{"x-ticvai-column":"lifted_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net."},"expectedCash":{"x-ticvai-column":"expected_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"26 September, pull audit R207. **The figure the blind count was measured against**, revealed once the count is in — null until then. Until this date only `ShiftCloseResult` carried it, returned once by `closeShift`, so BO-040 could not show the over/short it exists to accept. **Null to the shift's own cashier on every read** (CHG-FIN-003, 2 October): returned only to a caller holding OVERSHORT_ACCEPT or SHIFT_CLOSE_OTHER at the venue.\n"},"countedCash":{"x-ticvai-column":"counted_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"What the close count found. Null until the shift is counted."},"variance":{"x-ticvai-column":"variance_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"Counted minus expected, as `ShiftCloseResult.variance`. Negative is short. Null to the shift's own cashier, as `expectedCash` (CHG-FIN-003)."},"cashierReason":{"type":"string","nullable":true,"readOnly":true,"enum":["tillError","unrecordedRefund","miscount","other"],"description":"What the cashier said went wrong, given with the blind count (`CloseShiftRequest.cashierReason`, DI-803) without seeing the variance; the supervisor reads it beside the variance on BO-040 (CHG-FIN-003).\n"},"cashierNote":{"type":"string","nullable":true,"readOnly":true,"maxLength":1000,"description":"The cashier's note with the count (`CloseShiftRequest.notes`; CHG-FIN-003)."},"heldLeaseCount":{"type":"integer","description":"Inventory leases currently held by this workstation. Surfaced so an operator closing a shift can see what will be returned.\n"},"openedAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time","description":"When the device recorded the open. `openedAt` is the server's time."},"suspendedAt":{"type":"string","format":"date-time","nullable":true},"suspendReason":{"type":"string","maxLength":200,"nullable":true,"description":"The `reason` given to `suspendShift`. Cleared on resume."},"closedAt":{"type":"string","format":"date-time","nullable":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who submitted the close count. `reopenShift` refuses an approver who is this principal, and until 26 September there was nothing to compare against (pull audit R099).\n"},"recountRequestedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `rejectShiftVariance`, cleared by the cashier's recount** (decided 2 October 2026, Chinmay; DEC-175; CHG-CSP-013; DI-804). While set, the shift is `pendingVariance` waiting for the cashier rather than the supervisor: the cashier's view says \"Recount requested\" instead of \"Under review\".\n"},"recountRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The supervisor who sent the count back (CHG-CSP-013)."},"recountReason":{"type":"string","nullable":true,"readOnly":true,"maxLength":500,"description":"The supervisor's reason, shown to the cashier; never an amount (CHG-CSP-013, CHG-FIN-003)."},"countNumber":{"type":"integer","minimum":0,"readOnly":true,"description":"How many close counts the shift has had: 0 before the first, 1 after it, 2 after a recount (CHG-CSP-013). The latest is the one measured.\n"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while the shift has unsynced operations."},"approvals":{"type":"array","items":{"type":"object","required":["kind","principalId","at"],"properties":{"kind":{"type":"string","enum":["open","close","variance"],"description":"`open` from `approveShiftOpen`, `close` from `approveShiftClose`, `variance` from `acceptShiftVariance`.\n"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"reason":{"type":"string"}}}}}},
"ShiftStatus": {"type":"string","enum":["pendingApproval","open","suspended","pendingVariance","pendingClosure","closed","autoClosed"]},
"TableDefinition": {"x-ticvai-persistence":"fnb.dining_table","type":"object","description":"A restaurant (dining) table, reserved with `createTableReservation`. Not a map-bookable `resources` table, which is a non-dining spot sold like a cabana (decided 29 September, rev 3 GAP-C2).","required":["id","label","capacity"],"properties":{"id":{"type":"string","format":"uuid"},"label":{"type":"string","maxLength":32,"x-ticvai-unique":"venue","description":"**The table code, unique per venue** (decided 28 September, audit R108). Two tables in one venue never share a label, across all its outlets, so *T12* names one table wherever it is read. `createTable` and `updateTable` refuse a duplicate with `409` `duplicate-code`.\n"},"capacity":{"type":"integer","minimum":1},"zone":{"type":"string","nullable":true},"position":{"type":"object","properties":{"x":{"type":"number"},"y":{"type":"number"}}},"shape":{"type":"string","enum":["round","square","rectangle","booth","bar"]},"isOutOfService":{"type":"boolean","default":false,"description":"**Damaged, or its section closed.** `getTableMap` shows it as `outOfService` and a claim on it is refused with `tableOutOfService`."}}},
"TableMap": {"x-ticvai-persistence":"none — projection","type":"object","required":["outletId","tables"],"properties":{"outletId":{"type":"string","format":"uuid"},"zones":{"type":"array","items":{"type":"string"}},"tables":{"type":"array","items":{"$ref":"#/components/schemas/TableState"}}}},
"TableState": {"x-ticvai-persistence":"none — projection over table and visit","allOf":[{"$ref":"#/components/schemas/TableDefinition"},{"type":"object","required":["status"],"properties":{"status":{"$ref":"#/components/schemas/TableStatus"},"visitId":{"type":"string","format":"uuid","nullable":true},"covers":{"type":"integer","nullable":true},"seatedAt":{"type":"string","format":"date-time","nullable":true},"serverPrincipalId":{"type":"string","format":"uuid","nullable":true},"billTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}]},
"TicketStatus": {"x-ticvai-persistence":"none — computed from entitlement and scans","description":"**A validation result, not a lifecycle**, despite the name. Computed at scan time from the entitlement and its scan history — `isValid`, `entriesUsed`, `isInsideVenue`.\n**The name misled a state model into anchoring on it** (`states/entitlement.yaml`, removed 18 August): six lifecycle states were checked against an object with no values, and `check-states` warned about it for a day before anyone read the schema.\nThe entitlement's lifecycle is `orders.EntitlementStatus`. **This is what a gate learns when it scans**, which is a different question with a similar name.\n","type":"object","required":["ticketId","isValid"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"Stable for the life of the ticket, independent of the media carrying it."},"mediaCode":{"type":"string","nullable":true},"productName":{"type":"string"},"holderName":{"type":"string","nullable":true,"description":"Present only where the entitlement is name-bound. Identity and entitlement are separate concerns; most entitlements carry no holder.\n"},"isValid":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesUsed":{"type":"integer"},"entriesAllowed":{"type":"integer","nullable":true,"description":"Null means unlimited."},"reentryAllowed":{"type":"boolean"},"isInsideVenue":{"type":"boolean","description":"Derived from the last scan. Drives anti-passback evaluation."},"issuingCellId":{"type":"string","nullable":true,"description":"Present when this entitlement was issued in a different cell and is being redeemed here as a delegated right (ADR-0010). Null for locally issued tickets.\n"},"guestLinkId":{"type":"string","nullable":true,"description":"Pseudonymous cross-region guest reference. Present only on delegated rights. Carries no personal data.\n"},"admissionRulesId":{"type":"string","format":"uuid"},"denyReason":{"$ref":"#/components/schemas/DenyReason"}}},
"TurnstileMode": {"type":"string","description":"**Reduced to two values — decided 28 September, audit R221.** Entry, exit, re-entry and crossover were the access point's `Direction` under another name, and two fields that could disagree left the gate to guess. Direction is fixed per access point; within `normal` or `podium` operation the turnstile may only be let spin free or held closed.\n","enum":["freeRotation","closed"]},
"ValidateRequest": {"type":"object","required":["id","mediaCode","mediaKind","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key and dedupe key."},"mediaCode":{"type":"string","maxLength":256,"description":"What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life.\n"},"mediaKind":{"$ref":"#/components/schemas/MediaKind"},"direction":{"$ref":"#/components/schemas/Direction"},"groupSize":{"type":"integer","minimum":1,"description":"For group media admitting several holders on one read."},"proximityToken":{"type":"string","description":"BLE proximity assertion where the venue requires the operator to be physically at the gate. Absent where not configured.\n"},"recordedAt":{"type":"string","format":"date-time","description":"Device time of the read. Authoritative for ordering, not for validity."}}},
"ValidationResult": {"x-ticvai-persistence":"none — computed, persisted as scan_event","type":"object","required":["scanId","outcome","accessPointId","recordedAt"],"properties":{"scanId":{"type":"string","format":"uuid"},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"denyDetail":{"type":"string","description":"Human-readable, localised. For operator display, never for logic."},"denyCause":{"type":"string","nullable":true,"enum":["attractionTemporarilyClosed","timeBoundWindowElapsed","offlineLimitExceeded"],"description":"**The finer cause of three denials decided on 2 October 2026**, beside the r1 `denyReason` a client already switches on (a new `DenyReason` value would be a breaking change against r1; CHG-CSP-026, CHG-CSP-030, CHG-CSP-035). `attractionTemporarilyClosed` (DEC-228): `denyReason` `outsideAdmissionWindow`, with `reopensAt` and `queueReturnOffer`. `timeBoundWindowElapsed` (DEC-232): a time-bound entitlement scanned after its window from first scan, `denyReason` `expired`. `offlineLimitExceeded` (DEC-426): a reader offline longer than the venue's `AccessOfflinePolicy.maxOfflineDurationHours` refusing a tap it cannot check, `denyReason` `outsideAdmissionWindow`. Null for every other denial."},"reopensAt":{"type":"string","format":"date-time","nullable":true,"description":"When a temporarily closed attraction expects to reopen, where known (DEC-228; CHG-CSP-026)."},"queueReturnOffer":{"type":"object","nullable":true,"description":"A virtual-queue return window offered at a denied scan of a temporarily closed attraction, where the venue enables it (DEC-228; CHG-CSP-026). Taking it is `queue.joinQueue`.","properties":{"queueId":{"type":"string","format":"uuid"},"returnWindowStart":{"type":"string","format":"date-time"},"returnWindowEnd":{"type":"string","format":"date-time"}}},"accessPointId":{"type":"string","format":"uuid"},"ticket":{"$ref":"#/components/schemas/TicketStatus"},"admittedCount":{"type":"integer","description":"Holders admitted on this read. Differs from groupSize on partial admission."},"recordedAt":{"type":"string","format":"date-time"},"serverEvaluatedAt":{"type":"string","format":"date-time"},"advisory":{"type":"object","nullable":true,"description":"BL-179, CF-130. **What a device observed, for the steward, never for the gate.** Present only where an access point's device reports the matching `DeviceCapability` and the venue has turned the corresponding setting on.\n**Never persisted.** This schema is computed and stored as `access.scan_event`, and the advisory is deliberately not part of what is stored: an inferred classification kept against a guest is sensitive personal data with no consent behind it. **A guest agreed to be admitted, not to be classified** — Face Pass and Face Tag carry `consent_purpose_id` and `consent_given_at` because somebody enrolled, and nobody enrols in being looked at by a turnstile. `scan_event` records that an override happened and never what the device thought, which keeps `overrideRateAlertThreshold` working without building a register nobody agreed to.\n**It cannot reach `outcome` or `denyReason`.** Those are decisive and `entitlementGated` is `true` and read-only: the gate admits on the entitlement, and everything here sits on top of that without replacing any of it.\n","properties":{"genderClassification":{"type":"string","enum":["women","men","undetermined"],"description":"**`undetermined` is a real answer and the most common one to design for.** A classifier that never returns it is one that has been tuned to look confident.\n"},"confidence":{"type":"number","minimum":0,"maximum":1,"description":"**Required reading for the steward, not decoration.** An advisory with no confidence is read as a fact, and `overrideRateAlertThreshold` exists to catch exactly the failure that produces — *an override rate near zero means the steward has stopped deciding.* That number only means anything if the steward could see how sure the device was.\n"},"reportedByDeviceId":{"type":"string","format":"uuid","description":"**Which device said it.** A classifier that degrades is one camera, not a venue, and an advisory nobody can trace to hardware cannot be investigated or switched off alone.\n"}}}}},
"VendorServiceRequest": {"x-ticvai-persistence":"maintenance.vendor_service_request","type":"object","description":"**An outside vendor engaged on a work order** (decided 17 September, M17-13). The supplier is an `inventory.supplier`.\n","required":["workOrderId","supplierId","scope"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","readOnly":true},"workOrderId":{"type":"string","format":"uuid"},"supplierId":{"type":"string","format":"uuid"},"scope":{"type":"string","maxLength":2000,"description":"What the vendor is asked to do."},"status":{"allOf":[{"$ref":"#/components/schemas/VendorServiceRequestStatus"}],"default":"draft"},"vendorReference":{"type":"string","maxLength":100,"nullable":true},"quotedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"finalCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scheduledVisitAt":{"type":"string","format":"date-time","nullable":true},"note":{"type":"string","maxLength":1000,"nullable":true},"raisedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"VendorServiceRequestStatus": {"type":"string","enum":["draft","sent","accepted","scheduled","completed","cancelled"]},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"},"consentFormId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's own consent form, which every biometric capture is taken on** (decided 2 October 2026, Chinmay, batch 4, BO-188: \"Consent first, on the venue's consent form\"; DEC-128, DEC-549; CHG-CSP-018). A form from the venue's consent-form builder in Venue Management (the one builder Face Pass, Face Tag, marketing and waivers share; marketing-crm `setDigitalWaiverForm`). Turning `isEnabled` on without one is refused `422 consent-form-required`, as a missing DPIA is; each Face Pass and Face Tag capture records the form and its version it was consented on (access `enrolFacePass`, `enrolFaceTag`).\n"},"templatesHeldByTicvai":{"type":"boolean","readOnly":true,"description":"**True where TICVAI's platform stores this venue's biometric templates** (rather than the venue's own on-premises reader estate). Derived from the venue's access deployment. While true, Venue Management shows the venue a standing warning that every guest must accept the venue's consent form before capture, because the data sits with TICVAI as the venue's processor (decided 2 October 2026, Chinmay, batch 4, BO-188: \"If we store the data, highlight or notify the venue that the client must accept a consent form\"; DEC-128; CHG-CSP-018).\n"},"allowMinors":{"type":"boolean","default":true,"description":"**Whether this venue enrols minors at all** (decided 2 October 2026, Chinmay, critical set 1, BO-187 and CMS-029: \"Guardian consent on the venue's form; minor age per country; the venue can switch minors off\"; supersedes the GST-069 default; DEC-237; CHG-CSP-019). On: a minor (below `RegionSettings.minorAgeThreshold`) is enrolled only with a guardian's consent on the venue's consent form. Off: a minor's enrolment is refused (`422 minors-not-enrolled`) and the guest uses another verification method.\n"},"accreditationFaceMatching":{"type":"object","nullable":true,"description":"**Face matching to find duplicate accreditation applicants, off unless the venue enables it** (decided 2 October 2026, Chinmay, critical set 3, BO-631: \"Only where the venue enables it, with applicant consent and the venue's legal sign-off; off by default\"; DEC-461; CHG-CSP-022). Enabling it is refused without `legalSignOffReference` (`422 legal-sign-off-required`); each applicant matched must have consented on the application (accreditation's own record). Null is off.\n","properties":{"isEnabled":{"type":"boolean","default":false},"legalSignOffReference":{"type":"string","nullable":true,"maxLength":200,"description":"The venue's own reference for its legal sign-off; the platform records that one was named, by whom and when."},"signedOffByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"signedOffAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"chargeCurrencies":{"type":"array","nullable":true,"description":"**Which currencies a guest may select and pay in** (decided 2 October 2026, Chinmay; CHG-FIN-001; MoM 10 Aug 2026 4.7 option (b), DI-211). A subset of `displayCurrencies`: each code must also be one the venue's payment provider can charge (`orders.PaymentProvider.presentmentCurrencies`) and one the region holds a `tender` rate for; anything else is refused `400`. Null or empty: guests pay in the trading (base) currency only and the other display currencies stay approximate. The ledger is always in the base currency, with the rate recorded on every payment and refund.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**The most cash a till drawer should hold before some is lifted to the safe** (decided 2 October 2026, Chinmay, batch 6 set 3, BO-042: \"Add drawer limit setting (warn + offer cash lift)\"; DEC-179; CHG-CSP-016; DI-274: on a busy day the cashier unloads excess cash mid-shift and it is reconciled at close). The venue default; a till may set its own (`Workstation.cashDrawerLimit`). When the cash a till has taken since its last count takes the drawer over it, the till warns and offers a cash lift (`shift.createCashMovement` kind `lift`) and BO-042 flags the box (`shift.DepositBox.overDrawerLimit`). A warning, never a block: a sale is not refused because the drawer is full. Null sets no limit. **No proposed default: the client's finance team sets it.**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"tableReservedLeadMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":240,"default":30,"deprecated":true,"description":"**Deprecated (2 October 2026, CHG-CLN-009): `fnb.FnbReservationPolicy.reservedLeadMinutes` is canonical.** The table state model reads the reservation policy (`states/table.yaml`); this venue setting is kept for compatibility, never read, and not drawn. Its former meaning: **How long before a pre-allocated booking its table shows Reserved** (decided 2 October 2026, Chinmay, batch 6 set 6b, EMP-052: \"Reserved when a booking names the table, or N minutes (venue-set) before a pre-allocated booking\"; DEC-202; CHG-CSP-017; DI-689, DI-336). A booking that names its table holds it as Reserved for the booking's whole slot; a booking the host pre-allocated shows its table Reserved from this many minutes before it. Zero shows Reserved only once the booking is due. The fnb table state model applies it (`states/table.yaml`, owned by fnb). Proposed default 30 minutes, client to correct.\n"},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}},
"WebhookDelivery": {"type":"object","x-ticvai-persistence":"control.webhook_delivery","description":"13.1.30. **The log a developer needs most**, and without it every question becomes a support ticket.\n","required":["id","subscriptionId","eventType","status"],"properties":{"id":{"type":"string","format":"uuid"},"subscriptionId":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid"},"eventType":{"type":"string"},"status":{"type":"string","enum":["pending","delivered","failed","retrying","abandoned"]},"attemptCount":{"type":"integer"},"responseCode":{"type":"integer","nullable":true},"responseBodyExcerpt":{"type":"string","nullable":true,"description":"**Truncated, and it is what makes the log useful** — a 500 with the receiver's own error message in it answers the question without a conversation.\n"},"isReplay":{"type":"boolean","default":false},"isTest":{"type":"boolean","default":false,"description":"Sent by `testWebhookSubscription` (VM close-out, 29 September). Marked in the payload so a receiver never books it, and never counted towards `consecutiveFailures`.\n"},"deliveredAt":{"type":"string","format":"date-time","nullable":true}}},
"WebhookEventType": {"type":"string","description":"**The webhook event catalogue: every event a subscription may name** (29 September, build pass). Each value is the `name` of an event in `events/` — `aggregate.pastTenseFact`, published through `platform.outbox` by exactly one context. A name is added here in the same change that adds its event file, and never before.\n**Added 29 September**, each closing a requirement that had the webhook mechanism and nothing to subscribe to:\n| Events | Publisher | Requirement | |---|---|---| | `device.statusChanged`, `device.tamperDetected`, `device.enrolmentChanged`, `device.firmwareReleased`, `device.firmwareRolloutCompleted` | tenancy | 16.9.56 | | `accreditation.applicationDecided`, `accreditation.holderStatusChanged`, `accreditation.credentialIssued`, `accreditation.renewalDue` | accreditation | 12.1.53 | | `approval.requested`, `approval.escalated`, `approval.stepCompleted`, `approval.expired` | approvals | 11.1.64, 11.1.66 | | `seat.held`, `seat.released`, `seat.blocked`, `seatMap.published` | seating | 21.13.4 | | `consent.deviceConsentRecorded`, `consent.deviceConsentClaimed` | marketing | 2.6.65 | | `order.chargebackRecorded` | orders | 8.3.11 to 8.3.15 (a tenant's own finance or fraud tooling) | | `entitlement.expiringSoon` | access | 5.5.30 (a tenant's own CRM) | | `apiClient.anomalyDetected` | public-api | 17 September minutes M17-07 (added 30 September with its event file) |\n**Deprecated** (1 October, ADR-0067 amendment): `device.enrolmentChanged` is still offered but nothing inside the platform consumes it any more; it is removed at the next major version of this API. Subscribers are told in the release note.\n**Published and deliberately not offered** (29 September, build pass, group G2): `identity.credentialResetRequested` and `identity.loginRecorded` are security signals, and a stream of them to an outside receiver is a map of which accounts are under attack; `storefront.sessionEvent` is high-volume fraud telemetry, not a business fact a receiver acts on.\n","x-ticvai-deprecated-values":["device.enrolmentChanged"],"enum":["access.validated","accreditation.applicationDecided","accreditation.credentialIssued","accreditation.holderStatusChanged","accreditation.renewalDue","ai.ceilingApproaching","apiClient.anomalyDetected","approval.escalated","approval.expired","approval.granted","approval.rejected","approval.requested","approval.stepCompleted","assets.documentIndexed","cart.abandoned","catalogue.productPublished","consent.deviceConsentClaimed","consent.deviceConsentRecorded","conversation.handedOver","device.enrolmentChanged","device.firmwareReleased","device.firmwareRolloutCompleted","device.statusChanged","device.tamperDetected","entitlement.expiringSoon","entitlement.issued","entitlement.statusChanged","fnb.menuPublished","fnb.orderReady","inventory.purchaseOrderReceived","ledger.journalPosted","ledger.periodClosed","maintenance.assetReturnedToService","maintenance.templatePublished","maintenance.workOrderCompleted","marketing.caseClosed","order.chargebackRecorded","order.completed","order.paid","order.refunded","performance.cancelled","reporting.definitionPublished","retail.merchandisePublished","seat.blocked","seat.held","seat.released","seat.sold","seatMap.published","shift.closed","stock.depleted","tenant.suspended","whitelabel.contentPublished"]},
"WebhookSubscription": {"type":"object","x-ticvai-persistence":"control.webhook_subscription","description":"13.1.26, 13.3.18 and 13.3.22. **The 29 events already exist and nothing outside could receive one.**\n","required":["id","clientId","endpointUrl","eventTypes","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"clientId":{"type":"string","format":"uuid"},"endpointUrl":{"type":"string"},"eventTypes":{"type":"array","description":"**Filtered at subscription, not at delivery.** A subscriber taking every event and discarding 99% is a subscriber the platform pays to talk to. Each entry is a name from the webhook event catalogue (`WebhookEventType`).\n","items":{"$ref":"#/components/schemas/WebhookEventType"}},"filters":{"type":"object","nullable":true,"description":"13.3.22. Tenant, venue, or a business condition on the payload.","additionalProperties":true},"signingSecret":{"type":"string","format":"password","writeOnly":true,"description":"**How the receiver knows it was TICVAI.** Without a signature an endpoint accepts a ticket-sale event from anybody who learns the URL.\n**Write-only: accepted on create, never returned.** The same rule as `clientSecret` — a system that can show you a secret later is a system that hands it to whoever reads the subscription.\n"},"status":{"type":"string","enum":["pendingVerification","active","paused","failing","disabled"],"readOnly":true},"consecutiveFailures":{"type":"integer","readOnly":true},"disabledReason":{"type":"string","nullable":true,"readOnly":true,"description":"13.1.29. **An endpoint failing for days is disabled rather than retried forever**, and the developer is told — a queue growing against a dead endpoint is a cost the platform carries silently.\n"}}},
"WorkOrder": {"x-ticvai-persistence":"maintenance.work_order","x-ticvai-retired-columns":["is_overdue"],"type":"object","required":["id","workOrderNumber","title","venueId","status","priority","kind","createdAt"],"properties":{"downtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"},"rootCause":{"type":"string","nullable":true,"enum":["wearAndTear","operatorError","guestDamage","manufacturingDefect","environmental","softwareFault","powerFailure","deferredMaintenance","unknown"],"description":"**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"},"rootCauseNote":{"type":"string","nullable":true},"escalatedAt":{"type":"string","format":"date-time","nullable":true},"escalationLevel":{"type":"integer","default":0,"description":"**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"},"id":{"type":"string","format":"uuid"},"workOrderNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"title":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"assetName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"},"status":{"$ref":"#/components/schemas/WorkOrderStatus"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"priorityScore":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"readOnly":true,"description":"The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."},"prioritySource":{"type":"string","enum":["scored","assetOverride","manual"],"readOnly":true,"description":"Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","items":{"type":"string"},"description":"Skills the job needs (M17-13)."},"kind":{"$ref":"#/components/schemas/WorkOrderKind"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"raisedByPrincipalId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"},"locationDescription":{"type":"string","maxLength":500,"nullable":true,"description":"Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"},"elapsedMinutes":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"},"isTimerRunning":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"},"dueAt":{"type":"string","format":"date-time","nullable":true},"isOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"},"requiresVerification":{"type":"boolean"},"sourcePlanId":{"type":"string","format":"uuid","nullable":true},"sourceInspectionId":{"type":"string","format":"uuid","nullable":true},"sourceIncidentId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrderAssigneeSuggestion": {"x-ticvai-persistence":"none — computed on read","type":"object","required":["principalId","rank"],"properties":{"principalId":{"type":"string","format":"uuid"},"name":{"type":"string"},"rank":{"type":"integer","minimum":1},"hasAllQualifications":{"type":"boolean"},"missingQualificationCodes":{"type":"array","items":{"type":"string"}},"onShift":{"type":"boolean","description":"On shift now or before the work order is due."},"openWorkOrderCount":{"type":"integer"}}},
"WorkOrderDetail": {"x-ticvai-persistence":"maintenance.work_order","allOf":[{"$ref":"#/components/schemas/WorkOrder"},{"type":"object","properties":{"description":{"type":"string","nullable":true},"resolution":{"type":"string","nullable":true},"resolutionCode":{"$ref":"#/components/schemas/ResolutionCode"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"timeEntries":{"type":"array","items":{"type":"object","properties":{"action":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"pauseReason":{"type":"string","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}}},"parts":{"type":"array","items":{"type":"object","properties":{"inventoryItemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"quantity":{"type":"number"},"reservedQuantity":{"type":"number","description":"Still reserved for this work order and not yet issued (M17-02)."},"cost":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"labourCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"partsCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","x-ticvai-column":"net_cost_amount"},"completedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who called `completeWorkOrder`. **What `verifyWorkOrder` compares against** — the verifier may not be the technician who completed the work, and the assignee is not necessarily that person.\n"},"followUpRequired":{"type":"boolean","default":false},"followUpNote":{"type":"string","maxLength":1000,"nullable":true},"verificationOutcome":{"type":"string","enum":["verified","rejected"],"nullable":true,"description":"The latest `verifyWorkOrder` outcome."},"verificationNote":{"type":"string","maxLength":1000,"nullable":true},"verifiedAt":{"type":"string","format":"date-time","nullable":true},"verifiedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"cancelReason":{"type":"string","enum":["raisedInError","duplicate","superseded","noLongerRequired"],"nullable":true},"cancelNote":{"type":"string","maxLength":300,"nullable":true},"supersededByWorkOrderId":{"type":"string","format":"uuid","nullable":true,"description":"Set by `cancelWorkOrder` where the reason is `superseded`."},"cancelledAt":{"type":"string","format":"date-time","nullable":true},"closeOutcome":{"type":"string","enum":["completedAndVerified","notReproducible","supersededByReplacement","noLongerApplicable","duplicate"],"nullable":true},"closeNote":{"type":"string","maxLength":500,"nullable":true},"duplicateOfWorkOrderId":{"type":"string","format":"uuid","nullable":true,"description":"Set by `closeWorkOrder` where the outcome is `duplicate`."},"closedAt":{"type":"string","format":"date-time","nullable":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true}}}]},
"WorkOrderFaultAssessment": {"x-ticvai-persistence":"none — columns on maintenance.work_order","type":"object","description":"What the person raising a fault says about it, which the priority score reads (M17-01).","properties":{"safetyRisk":{"type":"boolean","default":false},"guestImpact":{"type":"string","enum":["none","degraded","closed"],"default":"none"}}},
"WorkOrderKind": {"type":"string","enum":["corrective","planned","inspectionFollowUp","incidentCorrective","improvement"]},
"WorkOrderPriority": {"type":"string","enum":["low","normal","high","urgent","emergency"]},
"WorkOrderStatus": {"type":"string","enum":["open","assigned","inProgress","paused","awaitingParts","completed","verified","closed","cancelled"]},
"Workstation": {"x-ticvai-persistence":"platform.workstation","type":"object","required":["id","code","name","venueId","regionId","scopePath","saleBoard","currency","currencyScale","timeZone"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"**The outlet this till stands in** (CHG-CSP-006). Its board is the till's board unless the till overrides it. Null on a workstation that belongs to no outlet (a ticket office counter set up before outlets), which must then carry its own board.\n"},"scopePath":{"type":"string"},"saleBoard":{"type":"object","description":"Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. What the operator may then DO within it is governed by their permissions.\n**The effective board** since 2 October 2026 (DEC-183; CHG-CSP-006): the till's own when it overrides the outlet, otherwise the outlet's (`saleBoardSource`).\n","required":["id","kind"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SaleBoardKind"},"name":{"type":"string"}}},"saleBoardSource":{"type":"string","enum":["outlet","workstation"],"readOnly":true,"description":"**Where `saleBoard` came from** (decided 2 October 2026, Chinmay, BO-109: \"Per outlet, with a till override\"; DEC-183; CHG-CSP-006): `outlet` when the till uses its outlet's layout, `workstation` when this till overrides it. BO-109 shows which tills differ from their outlet.\n"},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**This till's drawer limit, overriding the venue's** (`VenueSettings.cashDrawerLimit`; DEC-179; CHG-CSP-016). Null inherits the venue's. Above it the till warns and offers a cash lift.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point.\n"},"devices":{"type":"array","items":{"$ref":"#/components/schemas/DeviceBinding"}},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"timeZone":{"type":"string"},"deploymentProfile":{"$ref":"#/components/schemas/DeploymentProfile"},"edgeNodeId":{"type":"string","format":"uuid","nullable":true,"description":"Present when `deploymentProfile` is `venueEdge`."},"healthScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"readOnly":true,"description":"Board 1 of the client's POS set. **A number a manager can sort by** — the package held `lastHeartbeatAt` and a heartbeat timestamp is not a score.\nThe client's board shows 1,248 workstations at 96% healthy, and **the value of that figure is that it ranks**: a fleet dashboard exists so somebody can open the worst one first.\n**Derived from its devices, its heartbeat age, its firmware currency and its error rate.** Read-only, because a workstation that could set its own score would.\n**The formula, proposed, client to correct (audit R096 (2)):** score = 40% device online share (the share of its devices reporting online) + 25% heartbeat freshness (100 at one minute old or less, 0 at 15 minutes or more, linear between) + 20% firmware and profile currency (100 on the latest, 50 one version behind, 0 older) + 15% error rate (100 at 0 errors an hour, 0 at 10 or more, linear between), rounded to a whole number. **Below 80 is a warning and below 60 a failure.**\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"description":"Which profile this workstation runs, and at which version. **The client's board shows a fleet split four ways — 72% latest, 18.8% one behind, 6.1% outdated** — and the package had a firmware version field and no profile.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks*.\n"},"catalogueState":{"$ref":"#/components/schemas/CatalogueState"},"offlineCapable":{"type":"boolean","description":"Derived from `deploymentProfile`. False only for `thin`. Under local-first, catalogue READS are always local on transactional surfaces; this flag governs whether WRITES can be queued.\n"},"isActive":{"type":"boolean"}}}
}
```
