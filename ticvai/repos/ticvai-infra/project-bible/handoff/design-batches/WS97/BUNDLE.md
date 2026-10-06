# WS97 — Rental Management board 10

**10 screens · 7 operations · 17 schemas · 5 permissions**

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
  `PRODUCT_VIEW, RENTAL_VIEW, REPORT_VIEW_TENANT, REPORT_VIEW_VENUE, RESOURCE_VIEW`. A control nobody can use must say so,
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

### Ticketing & Guest Commerce, as the venue and TICVAI configure and run it

WHAT THE PROCESS IS. Everything a guest can buy is set up, priced, promoted and serviced here, on Venue Management (P08, the venue's own back office, served inside the venue's cell) and on the TICVAI Console (P09, TICVAI's control plane, outside every cell). End to end: (1) CATALOGUE. A product has one of twelve kinds (admission, timedAdmission, datedAdmission, openDated, seated, membership, bundle, fnb, retail, rental, addOn, giftCard). Its ticket types (adult, child, senior, resident...) are not typed one by one: they are generated from the product's attributes (components) and each value combination becomes a sellable ticket type with no extra setup (DI-164). What a ticket grants (validity, entries, re-entry, days of week, blackout dates, expiry anchor, fast track, transfer) lives on a reusable entitlement template, not on the product. Who may take part (age, height, supervision, certification) is the eligibility rule; what the guest must answer is the data mask and the consent questions; how the guest sees it is guestListing (bookable, infoOnly, hidden), display tags (at most six), media and the booking flow. Group, family and corporate products and every after-sales policy (reschedule, exchange, refund, cancellation, upgrade, transfer) are configured inside the one product configuration, never on separate screens (DI-465, DI-466). (2) LIFECYCLE AND PUBLICATION. A product moves draft, inReview, approved, live, withdrawn, archived. Approval and publication are two acts with two permissions (PRODUCT_APPROVE, PRODUCT_PUBLISH, R091); every product is authorised before it sells online or on site (DI-438). Approved is still not on a till: a till sells only what is in the signed catalogue release it pulled (publishBundle, ADR-0013), so a saved price is a back-office fact until the venue publishes to tills. Changing something that has sold is preceded by an impact check (assessProductChange: orders affected, entitlements issued, future performances, open carts); restoring a version creates a new version, and sold tickets keep the price and terms they were sold under (restoreProductVersion, DI-938, TRACKER Actions row 145). (3) PRICE. Prices live in price lists: per venue, per channel set, with validity dates and a priority, copied for the next season with an uplift (copyPriceList) and repriced in bulk only after a dry run (bulkChangePrices). Currency and decimal scale are never chosen on a form: they resolve from the venue's region (ADR-0008, ADR-0018; AED 2 places, OMR and BHD 3). When several rules apply, the configured hierarchy decides; there is no "lowest price wins" default (DI-595). Tax on the pre-discount price and three-decimal rounding are regional settings (DI-598). Dynamic rules always show their minimum and maximum price guardrails beside the trigger (getDynamicPriceRule). (4) PROMOTE AND BUNDLE. A promotion is a rule (automatic, or gated by a code) created in draft, made live only by Publish, which first analyses stacking; a …
*(source: DI-164; DI-171; DI-438; DI-465; DI-466; DI-595; DI-598; DI-387; DI-039; DI-044; DI-474; DI-671; DI-987; DI-019; DI-080; ADR-0008; ADR-0013; ADR-0018; ADR-0019; ADR-0030; R091; R098; R101; R222; REV3-21; contracts/spine/catalogue.yaml#transitionProductLifecycle …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Product | Anything sellable, of one of the twelve kinds. The record that carries names, channels, listing, media and policies. | Item (except on F&B and retail screens), SKU (for tickets), Offering | contracts/spine/catalogue.yaml#/components/schemas/ProductKind |
| Ticket type | One sellable variant of an admission or event product (Adult, Child, Resident Adult), generated from the product's attributes. For retail and F&B the same record is labelled Variant. | Variant (on ticket screens), Sub-product, Rate (that is a price), Axis value | contracts/spine/catalogue.yaml#updateProductVariant / DI-164 / DI-437 |
| Attribute | A dimension that generates ticket types (Guest category, Residency, Tier, Length). Each has values; adding a value adds ticket types. | Axis, Component (the client's word; use it only in help text), Option | contracts/spine/catalogue.yaml#setProductAttributes / DI-164 / DI-450 |
| Entitlement | What a ticket lets the holder do (validity, entries, re-entry, days, blackout dates, expiry, fast track, transfer), defined once on an entitlement template and shared by several products. | Access rights, Ticket rules, Validity profile | contracts/spine/catalogue.yaml#createEntitlementTemplate / DI-171 / DI-451 |
| Eligibility rule | Who may take part in or buy a product (age, height, supervision, waiver, certification). Distinct from a promotion's eligibility, which decides who gets a discount. | Restriction, Access rule (that is access control) | contracts/spine/catalogue.yaml#setProductEligibilityRule / DI-463 |
| Price list | A set of prices for one venue and a set of channels, valid between two dates, with a priority. Several coexist (B2C, B2B, season). | Price book, Rate card, Tariff | contracts/spine/catalogue.yaml#createPriceList / DI-140 / DI-163 |
| Price category | A standard rate type (Adult, Child, Member) reused across lists so venues do not invent "Adult Standard" and "Normal Adult". | Price band (that is a seat-category band), Fare type (transport) | contracts/spine/catalogue.yaml#setPriceCategoryRateType / … |
| Price band | A priced band on a seat category (code, label, colour, amount, channel, from-date). | Price category, Zone price | contracts/satellite/seating.yaml#/components/schemas/SeatPriceBand |
| Promotion | A rule that changes a price automatically or when a code is entered; draft until published; declares how it stacks. | Offer (except in guest copy), Deal, Discount rule | contracts/satellite/promotions.yaml#createPromotion / DI-173 / DI-174 |
| Coupon code | A code issued from a coupon campaign that applies a promotion-style discount; one shared code or many single-use codes. | Voucher, Promo voucher | contracts/satellite/promotions.yaml#createCouponCampaign / DI-173 |
| Voucher | A code that carries money (face value, balance), sold or issued; a liability until redeemed or expired. | Coupon, Credit note | contracts/satellite/promotions.yaml#listVoucherBatches / … |
| Bundle | A product sold as one line whose price differs from the sum of its components, with a mandatory revenue allocation. "Package" is acceptable in guest copy. | Combo (that is an F&B meal deal), Catalogue bundle | contracts/satellite/promotions.yaml#createBundle / DI-220 / ADR-0019 |
| Catalogue release | The signed snapshot of a venue's catalogue, prices, promotions and sale boards that tills, kiosks and devices pull. Its action label is "Publish to tills". | Bundle, Catalogue bundle, Sync, Deploy | contracts/spine/catalogue.yaml#publishBundle / … |
| Approve / Publish / Save | Save keeps a draft; Approve records that it is authorised (PRODUCT_APPROVE); Publish makes it live for guests and channels (PRODUCT_PUBLISH). Three different buttons, never merged. | Submit, Go live, Activate (except CatalogueConfigStatus active), Deploy | R091 / contracts/spine/catalogue.yaml#transitionProductLifecycle / DI-438 |
| Product states | Draft, In review, Approved, Live, Withdrawn, Archived (ProductLifecycleState), always as coloured badges with these exact labels. | Published (for a product), Pending, Inactive (for a product) | contracts/spine/catalogue.yaml#/components/schemas/ProductLifecycleState |
| Channel | Where something is sold. Labels: pos Point of sale; kiosk Kiosk; web and guestWeb Website; mobile and guestApp App; b2b B2B partners; partner Partner; ota Travel agents (OTA); callCentre Call centre; api API; backOffice Back office. | Touchpoint, Outlet (an outlet is a business inside a venue), raw enum values | contracts/spine/catalogue.yaml#/components/schemas/Channel / … |
| Refund | Money returned after settlement, wholly or for some lines, under the venue's refund policy. | Return (that is retail goods), Reversal, Void | contracts/spine/orders.yaml#createRefund / DI-252 |
| Void | Cancelling a whole order before settlement, within the same shift, with a reason from the void list. After settlement it is a refund. | Cancel order, Delete | contracts/spine/orders.yaml#voidOrder / R222 |
| Exchange / Reschedule | Exchange swaps lines for other products or dates and settles only the difference; Reschedule is the same product moved to another date or time. | Rebook, Date change (acceptable only in guest copy), Refund and resell | contracts/spine/orders.yaml#exchangeOrderLines / … |
| Hold / Capture / Release | A deposit or stored-value amount is held, then partly or fully captured, and the rest released. A held deposit is not a payment. | Charge, Pre-auth (in staff copy), Block funds | contracts/spine/orders.yaml#authoriseStoredValue / … |
| Wallet (TICVAI wallet) | The guest's stored-value balance on TICVAI, spent by hold and capture. Distinct from the tender "Apple Pay / Google Pay", which the contract also calls wallet. | Digital wallet (for stored value), E-wallet, Credit (without a type) | contracts/spine/orders.yaml#/components/schemas/TenderKind / R080 |
| Credit lot | One amount of wallet credit of one credit type (cash, bonus, gift) with its own expiry; lots are spent nearest expiry first and the guest sees the breakdown but cannot choose. | Bucket, Batch, Top-up | TRACKER Actions row 171 / contracts/satellite/wallet.yaml#expireCreditLots |
| Venue map / Seat map | A venue map is the wayfinding map of a park or a floor (points, paths, bookable places); a seat map is the seating layout of an auditorium or stand. Never just "map" where both could be meant. | Layout (alone), Floor plan (unless it is a floor map), Map (alone) | contracts/satellite/venue-map.yaml#createVenueMap / … |
| Point / Bookable place | A point is a place on a venue map (toilet, ride, restaurant, exit). A bookable place is a cabana, lounger, table or pitch placed on the map and sold through its price band. | Pin, POI, Marker, Resource (in staff copy) | contracts/satellite/venue-map.yaml#setVenuePoint / … |
| Station / Route / Timetable / Departure / Fare table / Pass … | A route is an ordered list of stations with offsets; a timetable generates departures up to its release horizon; a fare table prices a route per passenger type; a pass type is a multi-trip or unlimited pass sold as a product. | Stop (except in the stop list), Line (except lineCode), Schedule, Trip (except a guest's journey) | contracts/satellite/transport.yaml / REV3-21 |
| Applies from | The effective date of a change. Every dated change shows it, and sold items keep their old terms. | Effective date (in labels), Start date (for a change) | contracts/satellite/seating.yaml#updateSeatCategory / TRACKER Actions row 194 |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-584` | Rental Executive Command Center | D | 2 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-585` | Rental Revenue & Commercial Analytics | D | 2 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-586` | Utilization & Capacity Analytics | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-587` | Inventory & Equipment Performance Analytics | B | 0 | 12 | 6 | 0 | 1 | 4 | — | notStarted (—) |
| `BO-588` | Rental Duration, Extension & Return Analytics | D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-589` | Damage, Loss, Deposit & Exception Analytics | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-590` | Location & Channel Performance | D | 3 | 16 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-591` | Rental Forecasting & Demand Intelligence | B | 0 | 0 | 6 | 3 | 1 | 6 | — | notStarted (—) |
| `BO-592` | Audit, Governance & Operational Control | D | 0 | 32 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-593` | AI Rental Management Copilot & Action Center | D | 0 | 0 | 6 | 1 | 1 | 6 | — | notStarted (—) |

## Thin screens in this batch

**BO-584, BO-592, BO-593 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-584` Rental Executive Command Center

**Provide senior management with an immediate view of the overall rental business.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-584 |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/rental-executive-command-center-bo-584` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Senior management's rental overview: realised revenue, rentals, utilisation, on-time return rate, damage rate, maintenance trend. Reporting only.

**Known correction pending (do not draw the wrong version)**

- **Only listRentalBookings and a search/filter; no KPI source.** Why: Utilisation and revenue need aggregates the screen does not read. *(source: screens/P08-venue-back-office.yaml#BO-584; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search rental executive | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, rental location, product, category, date range and 2 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRentalBookings` ?status |
| Location | picker: choose a location | — | — | `listRentalBookings` ?locationId |
| From | date and time picker | — | — | `listRentalBookings` ?from |
| To | date and time picker | — | — | `listRentalBookings` ?to |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **KPIs**: Period selector; each KPI with comparison to the previous period. *(source: DI-771)*

**Data it reads**: `listRentalBookings` (onLoad, The commercial picture)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-585` Rental Revenue & Commercial Analytics: *Rental Revenue & Commercial Analytics*
- → `BO-586` Utilization & Capacity Analytics: *Utilization & Capacity Analytics*
- → `BO-587` Inventory & Equipment Performance Analytics: *Inventory & Equipment Performance Analytics*
- → `BO-588` Rental Duration, Extension & Return Analytics: *Rental Duration, Extension & Return Analytics*
- → `BO-589` Damage, Loss, Deposit & Exception Analytics: *Damage, Loss, Deposit & Exception Analytics*
- → `BO-590` Location & Channel Performance: *Location & Channel Performance*
- → `BO-591` Rental Forecasting & Demand Intelligence: *Rental Forecasting & Demand Intelligence*
- → `BO-592` Audit, Governance & Operational Control: *Audit, Governance & Operational Control*
- → `BO-593` AI Rental Management Copilot & Action Center: *AI Rental Management Copilot & Action Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental executive list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental executive untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental executive yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental executive are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis: 'October: AED 186,400 · 4,120 rentals · utilisation 62% · on-time 91% · damage 1.8%'
```

#### Permissions

- `listRentalBookings` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental command centre KPIs: realised revenue, total rentals, average utilisation, on-time return rate, damage rate, maintenance trends; further views for product performance, utilisation, equipment performance, duration/extension, damage/loss/deposit, channel/location and demand forecast. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-771)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-584` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS125 Rental Management Board 10.dc.html#bo-584`
- Workshop pack: Rental_Management.pdf board 10
- Flow F206 *Rental Management board 10: Rental Executive Command Center*, step 1: Opens Rental Executive Command Center → Provide senior management with an immediate view of the overall rental business.
- Flow F206 *Rental Management board 10: Rental Executive Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F206 *Rental Management board 10: Rental Executive Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F206 *Rental Management board 10: Rental Executive Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F206 *Rental Management board 10: Rental Executive Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F206 *Rental Management board 10: Rental Executive Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F206 *Rental Management board 10: Rental Executive Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F206 *Rental Management board 10: Rental Executive Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F206 branch at step 1 (expected): when Nothing has been set up on Rental Executive Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F206 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-584?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-585`, `BO-586`, `BO-587`, `BO-588`, `BO-589`, `BO-590`, `BO-591`, `BO-592`, `BO-593`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-585` Rental Revenue & Commercial Analytics

**Analyze rental commercial performance. The original scope specifically requires reporting on rental revenue.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-585 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/rental-revenue-commercial-analytics-bo-585` |

**What the spec says about it.** **One reporting area, one set of numbers** (decided 2 October 2026, Chinmay; CHG-FIN-006; DI-721, DI-702). This screen is a scoped window onto the reporting area (Analytics, P16): it runs the same seeded report definitions and reads the same seeded KPIs, so its figures equal what Analytics shows for the same scope, period and as-of time. It computes no total of its own and shows the as-of time on every figure.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Rental revenue for the period: gross rental revenue, discounts, refunds, net rental revenue, and the add-on income lines (extensions, late fees, damage charges, forfeited deposits), with average transaction value and revenue per rental hour, filterable by product, category, location and channel.

**Known correction pending (do not draw the wrong version)**

- **The tiles read getKpiValues, which offers no rental measure; only venue-wide takings exists.** Why: Every tile would show the venue's takings. *(source: contracts/satellite/reporting.yaml#/components/schemas/ReportingSystemKpi; Finance, Ledger & Tax · Reporting & Analytics)*
- **"Deposit Captures" is listed among revenue tiles without saying a held deposit is not revenue.** Why: Mixes a liability with income. *(source: screens/P08-venue-back-office.yaml#BO-585; Finance, Ledger & Tax · Reporting & Analytics)*
- **Rental revenue analytics duplicates the reporting area.** Why: DI-721. *(source: DI-721 / screens/P16-venue-analytics.yaml#ANL-002; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search rental revenue commercial | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by product, category, venue, location, channel, day and 2 more — which are present is a decision the pack already made. | — |

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
| Module | select | — | Core · Ticketing · Access · Fnb · Retail · Inventory · Seating · Membership · Marketing · Resources · Queue · Transport … | `getKpiValues` ?module |

#### Outputs: what the screen shows and produces

**Shown**

**Gross Rental Revenue** (metric tile)

**Net Rental Revenue** (metric tile)

**Average Transaction Value** (metric tile)

**Average Revenue per Rental Hour** (metric tile)

**Extension Revenue** (metric tile)

**Late-Fee Revenue** (metric tile)

**Damage Charges** (metric tile)

**Deposit Captures** (metric tile)

**Discount Value** (metric tile)

**Refund Value** (metric tile)

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **tiles**: Net rental revenue = gross minus discounts minus refunds. Deposits held are a liability and are not revenue; only a captured (forfeited) deposit counts, labelled "Deposits forfeited". *(source: contracts/spine/finance.yaml#settleDeposit / DI-771)*

**Data it reads**: `getKpiValues` (onLoad, Rental revenue)

**Where the user goes next**

- → `BO-584` Rental Executive Command Center: *Back to Rental Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental revenue commercial list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental revenue commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental revenue commercial yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental revenue commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Consistency with other screens

- Match `P16 ANL-002 Sales Revenue & Channel, ANL-005 Cost Margin & Profitability`: Same gross/net wording.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- Ski Dubai rentals · September 2026 · Gross AED 186,420.00 · Discounts 9,320.00 · Refunds 2,150.00 · Net AED 174,950.00
  · 2,214 rentals · ATV AED 84.20 · Extensions 12,600.00 · Late fees 3,480.00 · Damage 1,950.00 · Deposits forfeited
  4,200.00
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental command centre KPIs: realised revenue, total rentals, average utilisation, on-time return rate, damage rate, maintenance trends; further views for product performance, utilisation, equipment performance, duration/extension, damage/loss/deposit, channel/location and demand forecast. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-771)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-585` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS125 Rental Management Board 10.dc.html#bo-585`
- Workshop pack: Rental_Management.pdf board 10
- Flow F206 *Rental Management board 10: Rental Executive Command Center*, step 2: Works in Rental Revenue & Commercial Analytics → Analyze rental commercial performance. The original scope specifically requires reporting on rental revenue.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-585?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-584`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-586` Utilization & Capacity Analytics

**Understand how efficiently rental inventory is being used. The original requirements specifically call for utilization-rate reporting.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-586 |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/utilization-capacity-analytics-bo-586` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Rental utilisation analytics for the rental manager: how much of the rental fleet's available time was used, overall, at peak and off-peak, by product, location, date, time and duration, with a weekday x time-band heatmap and an AI insight. The one thing to get right: utilisation is booked time over available time where available already excludes maintenance and blocks, so the tiles never flatter a fleet that was half in the workshop.

**Known correction pending (do not draw the wrong version)**

- **Sold-out hours, Lost sales due to capacity, Protected inventory utilisation, Peak and Off-peak have no field in any read** Why: The utilisation read returns available, booked and blocked minutes per group only; peak/off-peak need a time-band grouping and lost sales need refused-demand data. *(source: screens/P08-venue-back-office.yaml#BO-586 / contracts/satellite/resources.yaml#getResourceUtilisation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The heatmap and Analyze by Time/Duration cannot be fed** Why: groupBy accepts resource, resourceType, category and venue only; there is no day-of-week x hour grouping. *(source: contracts/satellite/resources.yaml#getResourceUtilisation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What threshold defines "Idle inventory" and "Limited" (pack colours) for rentals?** → Drawn default accepted: Draw idle as under 10% of available hours in the period, editable later from KPI targets (BO-947). *(decided by Chinmay, 2026-10-02; DEC-443 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getResourceUtilisation` ?from |
| To | date and time picker | — | — | `getResourceUtilisation` ?to |
| Group by | radio group | — | Resource · Resource type · Category · Venue | `getResourceUtilisation` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Period and Analyze by**: Period presets (Today, 7 days, 30 days, custom) feeding from/to; Analyze by as tabs Product / Location / Date / Time / Duration from the pack. Only resource, type, category and venue exist as groupings in the read, so Product maps to resource type, Location to venue; Time and Duration greyed. *(source: screens/P08-venue-back-office.yaml#BO-586 / contracts/satellite/resources.yaml#getResourceUtilisation)*

#### Outputs: what the screen shows and produces

**Shown**

**Overall Utilization** (metric tile)

**Peak Utilization** (metric tile)

**Off-Peak Utilization** (metric tile)

**Idle Inventory** (metric tile)

**Sold-Out Hours** (metric tile)

**Lost Sales Due to Capacity** (metric tile)

**Protected Inventory Utilization** (metric tile)

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Seven metric tiles with period-on-period delta: Overall utilisation, Peak utilisation, Off-peak utilisation, Idle inventory (items under 10% in the period, count), Sold-out hours, Lost sales due to capacity (AED), Protected inventory utilisation. Tiles with no source show "Not yet measured" in grey rather than a zero. *(source: screens/P08-venue-back-office.yaml#BO-586 / DI-771)*
- **Utilisation heatmap**: Rows are 3-hour bands (09-12, 12-15, 15-18), columns Mon-Sun; cell shows the percent and is shaded on a single sequential scale; cells at 90% and over get a bold outline as capacity risk. *(source: screens/P08-venue-back-office.yaml#BO-586)*
- **AI insight card**: One sentence finding plus one recommendation, labelled AI, with "Why" showing the two figures compared (e.g. Saturday 15-18 at 97% vs Monday mornings at 31%); no Apply button, it is advice only. *(source: screens/P08-venue-back-office.yaml#BO-586 / DI-772)*
- **Breakdown table**: Label, available hours, booked hours, blocked hours, utilisation %, bookings; sorted by utilisation descending; hours not minutes. *(source: contracts/satellite/resources.yaml#getResourceUtilisation)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Click a heatmap cell or table row**: Opens the resource/equipment calendar (BO-519) on that day and type. *(source: designer default)*
- **Back to Rental Executive Command Center**: Returns to BO-584 keeping the period. *(source: screens/P08-venue-back-office.yaml#BO-586)*

**Data it reads**: `getResourceUtilisation` (onLoad, Utilisation and capacity)

**Where the user goes next**

- → `BO-584` Rental Executive Command Center: *Back to Rental Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The utilization capacity analytics list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the utilization capacity analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No utilization capacity analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the utilization capacity analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Period with no available time (fleet closed for the season)**: Utilisation shows a dash with "No available hours in this period", never 0% or a division error. *(source: contracts/satellite/resources.yaml#/components/schemas/ResourceUtilisation)*
- **Pooled rental stock (towels, life jackets)**: Not counted here (minutes per serialised item); the screen says "Serialised items only" under the title. *(source: contracts/satellite/rental.yaml#setRentalInventoryModel)*

#### Consistency with other screens

- Match `BO-944`: Same utilisation definition, heatmap and colour scale as the resource board's utilisation analytics; one is the rental slice of the other.
- Match `BO-584`: The rental command centre's Average utilisation tile must equal this screen's Overall utilisation for the same period.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
period: 1-30 Sep 2026, Aqua Park
tiles:
  overall: 68%
  peak: 91%
  offPeak: 42%
  idleInventory: 6 items
  soldOutHours: 37 h
  lostSales: Not yet measured
  protected: Not yet measured
heatmap:
- band: 09-12
  mon: 31%
  sat: 78%
  sun: 74%
- band: 15-18
  mon: 62%
  sat: 97%
  sun: 94%
insight: Saturday bike utilisation reaches 97% between 15:00 and 18:00 while Monday mornings average 31%. Consider
  moving non-essential maintenance to Monday mornings.
```

#### Permissions

- `getResourceUtilisation` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental command centre KPIs: realised revenue, total rentals, average utilisation, on-time return rate, damage rate, maintenance trends; further views for product performance, utilisation, equipment performance, duration/extension, damage/loss/deposit, channel/location and demand forecast. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-771)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-586` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS125 Rental Management Board 10.dc.html#bo-586`
- Workshop pack: Rental_Management.pdf board 10
- Flow F206 *Rental Management board 10: Rental Executive Command Center*, step 4: Works in Utilization & Capacity Analytics → Understand how efficiently rental inventory is being used. The original requirements specifically call for utilization-rate reporting.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-586?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-584`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-587` Inventory & Equipment Performance Analytics

**Measure the operational performance of the physical rental fleet. The original requirements call for reporting on inventory availability and equipment performance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block B · ticket #29163 (VM-BO-587) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Fleet KPIs) and a per-row directory (§Identify) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/inventory-equipment-performance-analytics-bo-587` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-001): getAssetHistory is one asset's service history; fleet counts, utilisation and revenue per asset need a rental analytics read that does not exist (contract gap … Contract gap recorded 2 October 2026 (CHG-WIR-004): No rental equipment performance read (utilisation, rentals and revenue per asset).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Fleet performance for rental management: how many items there are and in what state, how hard each works and earns, and which ones cost too much, break repeatedly or sit idle. From the maintenance angle it is where poor performers are spotted and sent to history (BO-580) or retirement (BO-582). The one thing to get right: fleet KPI tiles on top, then a per-asset performance table with a health rating, and the "identify" lists as ranked shortlists - not as table columns.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Health rating has no definition (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Bound to getAssetHistory, a per-asset service history (CHG-WIR-001); The six "Identify" lists are drawn as columns of a table titled "Every inventory equipment performance" (CHG-SBO-016).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How is an asset's Health derived (damage count, downtime, maintenance cost against revenue, last inspection condition)?** → Drawn default accepted: Show the label with a tooltip listing the inputs; draw "Not rated" until defined. *(decided by Chinmay, 2026-10-02; DEC-444 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Analyse by**: Product, location, date range; venue from the top bar. *(source: screens/P08-venue-back-office.yaml#BO-586)*

#### Outputs: what the screen shows and produces

**Shown**

**Total Assets** (metric tile)

**Available** (metric tile)

**Rented** (metric tile)

**Maintenance** (metric tile)

**Out of Service** (metric tile)

**Lost** (metric tile)

**Average Rentals per Asset** (metric tile)

**Average Revenue per Asset** (metric tile)

**Ranked shortlists** (card list): Six ranked shortlists (most and least utilised, highest revenue ...), not the columns of one table; the equipment performance table is asset, rentals, hours, revenue, damage, downtime, health.

| Shows | Format | Notes |
|---|---|---|
| Most utilized assets | text | not in the schema: `Most utilized assets` |
| Least utilized assets | text | not in the schema: `Least utilized assets` |
| Highest revenue assets | text | not in the schema: `Highest revenue assets` |
| Highest maintenance assets | text | not in the schema: `Highest maintenance assets` |
| Repeatedly damaged assets | text | not in the schema: `Repeatedly damaged assets` |
| Excessively idle inventory | text | not in the schema: `Excessively idle inventory` |

**The selected inventory equipment performance** (detail panel): The pack groups this record's detail under its own headings: “Equipment Performance”.

| Shows | Format | Notes |
|---|---|---|
| Most utilized assets | text | not in the schema: `Most utilized assets` |
| Least utilized assets | text | not in the schema: `Least utilized assets` |
| Highest revenue assets | text | not in the schema: `Highest revenue assets` |
| Highest maintenance assets | text | not in the schema: `Highest maintenance assets` |
| Repeatedly damaged assets | text | not in the schema: `Repeatedly damaged assets` |
| Excessively idle inventory | text | not in the schema: `Excessively idle inventory` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Fleet tiles**: Total assets, Available, Rented, Maintenance, Out of service, Lost, Average rentals per asset, Average revenue per asset (AED). *(source: screens/P08-venue-back-office.yaml#BO-586)*
- **Equipment performance table**: Asset, Rentals, Hours, Revenue (AED), Damage count, Downtime (hours or days), Health (Excellent, Good, Fair, Poor) - sortable; a row opens BO-580. *(source: screens/P08-venue-back-office.yaml#BO-588)*
- **Identify shortlists**: Six ranked top-5 lists - Most utilised, Least utilised, Highest revenue, Highest maintenance cost, Repeatedly damaged, Excessively idle - each item linking to the asset. *(source: screens/P08-venue-back-office.yaml#BO-588)*
- **AI recommendation**: "BIKE-031 has high downtime and repair frequency relative to fleet peers - review for replacement" with Start retirement. *(source: screens/P08-venue-back-office.yaml#BO-588)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open asset**: Opens BO-580 (history) for the asset. *(source: screens/P08-venue-back-office.yaml#BO-580)*
- **Export**: CSV of the table for the chosen period. *(source: designer default)*

**Where the user goes next**

- → `BO-584` Rental Executive Command Center: *Back to Rental Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The inventory equipment performance list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the inventory equipment performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No inventory equipment performance yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the inventory equipment performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Pooled products (life jackets, lockers)**: Counted in the fleet tiles by quantity; excluded from the per-asset table with a note. *(source: DI-744)*

#### Consistency with other screens

- Match `BO-584`: Reached from and returns to the Rental Executive Command Center.
- Match `BO-583`: Same health labels and asset links.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  total: 283
  available: 147
  rented: 58
  maintenance: 7
  outOfService: 2
  lost: 1
  avgRentals: 64
  avgRevenue: AED 4,210.00
table:
- asset: BIKE-017
  rentals: 184
  hours: 276
  revenue: AED 11,840.00
  damage: 3
  downtime: 36 h
  health: Good
- asset: BIKE-018
  rentals: 201
  hours: 302
  revenue: AED 13,220.00
  damage: 1
  downtime: 14 h
  health: Excellent
- asset: BIKE-031
  rentals: 96
  hours: 140
  revenue: AED 8,920.00
  damage: 7
  downtime: 18 days
  health: Poor
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental command centre KPIs: realised revenue, total rentals, average utilisation, on-time return rate, damage rate, maintenance trends; further views for product performance, utilisation, equipment performance, duration/extension, damage/loss/deposit, channel/location and demand forecast. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-771)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-587` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS125 Rental Management Board 10.dc.html#bo-587`
- Workshop pack: Rental_Management.pdf board 10
- Flow F206 *Rental Management board 10: Rental Executive Command Center*, step 6: Works in Inventory & Equipment Performance Analytics → Measure the operational performance of the physical rental fleet. The original requirements call for reporting on inventory availability and equipment performance.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-587?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-584`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-588` Rental Duration, Extension & Return Analytics

**Understand customer usage behavior after checkout. The source explicitly requires reporting on rental duration and late returns.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-588 |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/rental-duration-extension-return-analytics-bo-588` |

**From the Food, Beverage & Retail process.** Duration, extension and return behaviour: planned vs actual duration, extension rate, on-time and late returns, critical overdue. Reporting only.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRentalBookings` ?status |
| Location | picker: choose a location | — | — | `listRentalBookings` ?locationId |
| From | date and time picker | — | — | `listRentalBookings` ?from |
| To | date and time picker | — | — | `listRentalBookings` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Average Planned Duration** (metric tile)

**Average Actual Duration** (metric tile)

**Extension Rate** (metric tile)

**Average Extension** (metric tile)

**On-Time Return %** (metric tile)

**Late Return %** (metric tile)

**Average Late Duration** (metric tile)

**Critical Overdue Count** (metric tile)

**Data it reads**: `listRentalBookings` (onLoad, Duration, extension and return)

**Where the user goes next**

- → `BO-584` Rental Executive Command Center: *Back to Rental Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental duration extension list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental duration extension untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental duration extension yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental duration extension are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis: Planned 1 h 42 · actual 1 h 55 · extensions 14% · late 9% · critical overdue 2
```

#### Permissions

- `listRentalBookings` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental command centre KPIs: realised revenue, total rentals, average utilisation, on-time return rate, damage rate, maintenance trends; further views for product performance, utilisation, equipment performance, duration/extension, damage/loss/deposit, channel/location and demand forecast. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-771)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-588` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS125 Rental Management Board 10.dc.html#bo-588`
- Workshop pack: Rental_Management.pdf board 10
- Flow F206 *Rental Management board 10: Rental Executive Command Center*, step 8: Works in Rental Duration, Extension & Return Analytics → Understand customer usage behavior after checkout. The source explicitly requires reporting on rental duration and late returns.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-588?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-584`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-589` Damage, Loss, Deposit & Exception Analytics

**Give management visibility into operational and financial risk. The original scope explicitly requires reporting on damaged items and deposit collection/refund.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-589 |
| Who uses it | venue staff holding `RENTAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/damage-loss-deposit-exception-analytics-bo-589` |

**From the Food, Beverage & Retail process.** Damage, loss, deposit and exceptions: damage cases and rate, lost units, damage charges, deposits held, released, captured, pending, waived fees, overrides. Reporting only.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | text field | — | — | `listRentalBookings` ?status |
| Location | picker: choose a location | — | — | `listRentalBookings` ?locationId |
| From | date and time picker | — | — | `listRentalBookings` ?from |
| To | date and time picker | — | — | `listRentalBookings` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Damage Cases** (metric tile)

**Damage Rate** (metric tile)

**Lost Equipment** (metric tile)

**Total Damage Charges** (metric tile)

**Deposit Collected/Authorized** (metric tile)

**Deposit Released** (metric tile)

**Deposit Captured** (metric tile)

**Deposit Pending** (metric tile)

**Waived Fees** (metric tile)

**Manual Overrides** (metric tile)

**Data it reads**: `listRentalBookings` (onLoad, Damage, loss and deposit exceptions)

**Where the user goes next**

- → `BO-584` Rental Executive Command Center: *Back to Rental Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The damage loss deposit list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the damage loss deposit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No damage loss deposit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the damage loss deposit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis: Damage 22 cases · lost 3 · captured AED 2,340 · released AED 61,800 · waived AED 410
```

#### Permissions

- `listRentalBookings` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental command centre KPIs: realised revenue, total rentals, average utilisation, on-time return rate, damage rate, maintenance trends; further views for product performance, utilisation, equipment performance, duration/extension, damage/loss/deposit, channel/location and demand forecast. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-771)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-589` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS125 Rental Management Board 10.dc.html#bo-589`
- Workshop pack: Rental_Management.pdf board 10
- Flow F206 *Rental Management board 10: Rental Executive Command Center*, step 10: Works in Damage, Loss, Deposit & Exception Analytics → Give management visibility into operational and financial risk. The original scope explicitly requires reporting on damaged items and deposit collection/refund.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-589?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-584`.
- [ ] Every gated control is gated: `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-590` Location & Channel Performance

**Compare rental performance across physical locations and sales channels.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-590 |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/location-channel-performance-bo-590` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Rental performance compared across locations and channels on a stated basis (per visitor, per operating hour, per square metre, per staffed position), so a big location is not "better" just for being big.

**Known correction pending (do not draw the wrong version)**

- **The channel list (B2C, B2B, POS, Walk-In, Mobile App, API/Partner) is not the platform's channel vocabulary; walk-in is a POS sale.** Why: Sales by channel would be bucketed differently from every other board. *(source: MoM 2026-08-18 4.2 Recipes, Operating Hours & Service Channels / MATRIX 1.4.7 / screens/P08-venue-back-office.yaml#BO-590; Finance, Ledger & Tax · Reporting & Analytics)*
- **Location and channel comparison duplicates the reporting area.** Why: DI-721. *(source: DI-721 / screens/P16-venue-analytics.yaml#ANL-020; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is an AI rebalancing recommendation (move stock from Marina A to North Station) inside AI's agreed rental role?** → Drawn default accepted: Show it as a reporting insight only, no action button. *(decided by Chinmay, 2026-10-02; DEC-358 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| KPI | select field | — | — | — | — | Sends `?kpiId=` (required): rentals, revenue, utilisation, availability or damage, one per read. | — |
| Locations | multi select | — | — | — | — | Sends `?scopePaths=`. | — |
| Normalise by | select field | — | — | — | — | Sends `?normaliseBy=`. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpi | picker: choose a kpi | — | — | `getAnalyticsBenchmark` ?kpiId |
| Scope paths | text field | — | — | `getAnalyticsBenchmark` ?scopePaths |
| Normalise by | radio group | — | None · Per visitor · Per operating hour · Per staffed position · Per square metre | `getAnalyticsBenchmark` ?normaliseBy |

#### Outputs: what the screen shows and produces

**Shown**

**Location comparison** (data table, from `getAnalyticsBenchmark`): One KPI per read; the pack's side-by-side Rentals / Revenue / Utilization / Availability / Damage table needs one read per KPI.

| Shows | Format | Notes |
|---|---|---|
| Label | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Normalised value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Normalise by | chip: None, Per visitor, Per operating hour, Per staffed position, Per square metre | The basis a benchmark is compared on. Shared by `getAnalyticsBenchmark` and `BenchmarkRow`. |
| Rank | 1,234 | — |
| Percentile | 12.5% | — |

**Channel comparison** (chart): B2C, B2B, POS, Walk-In, Mobile App, API/Partner. Benchmarks compare scope paths, not sales channels.

| Shows | Format | Notes |
|---|---|---|
| Channel | text | not in the schema: `Channel` |
| Bookings | text | not in the schema: `Bookings` |
| Revenue | text | not in the schema: `Revenue` |
| Average value | text | not in the schema: `Average value` |
| Cancellation | text | not in the schema: `Cancellation` |
| No show | text | not in the schema: `No-show` |
| Utilization contribution | text | not in the schema: `Utilization contribution` |

**AI rebalancing insight** (detail panel): The pack's Marina A to North Station example; no operation returns it.

| Shows | Format | Notes |
|---|---|---|
| Insight | text | not in the schema: `Insight` |
| Recommendation | text | not in the schema: `Recommendation` |
| Linked inventory transfer | text | not in the schema: `Linked inventory transfer` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **location comparison**: Raw value, normalised value with its basis named, rank and percentile. *(source: contracts/satellite/reporting.yaml#/components/schemas/BenchmarkRow)*

**Data it reads**: `getAnalyticsBenchmark` (onLoad, Location and channel performance)

**Where the user goes next**

- → `BO-584` Rental Executive Command Center: *Back to Rental Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The location channel performance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the location channel performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No location channel performance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the location channel performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **a venue manager**: Location comparison needs tenant-wide report access; without it the panel says so. *(source: contracts/satellite/reporting.yaml#getAnalyticsBenchmark)*

#### Consistency with other screens

- Match `P16 ANL-020 Multi-Site & Performance Comparison, ANL-016 Sales & Channel Performance`: Same comparison component and normalisation words.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- Marina A · revenue AED 64,210.00 · per operating hour AED 178.36 · rank 1 · North Station · AED 41,880.00 · AED
  116.33 · rank 3
```

#### Permissions

- `getAnalyticsBenchmark` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental command centre KPIs: realised revenue, total rentals, average utilisation, on-time return rate, damage rate, maintenance trends; further views for product performance, utilisation, equipment performance, duration/extension, damage/loss/deposit, channel/location and demand forecast. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-771)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-590` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS125 Rental Management Board 10.dc.html#bo-590`
- Workshop pack: Rental_Management.pdf board 10
- Flow F206 *Rental Management board 10: Rental Executive Command Center*, step 12: Works in Location & Channel Performance → Compare rental performance across physical locations and sales channels.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-590?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-584`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-591` Rental Forecasting & Demand Intelligence

**Forecast future rental demand and identify capacity problems before they happen. This formally incorporates the AI utilization/demand forecasting recommendation from the source.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block B · ticket #29885 (VM-BO-591) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Forecast KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/rental-forecasting-demand-intelligence-bo-591` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Forecast rental demand by product, location and horizon to see capacity problems before they happen.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listDemandBookingCurve` ?venue |
| Product | text field | — | — | `listDemandBookingCurve` ?product |
| Event | text field | — | — | `listDemandBookingCurve` ?event |
| Performance | text field | — | — | `listDemandBookingCurve` ?performance |
| Channel | select | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | `listDemandBookingCurve` ?channel |
| Horizon | select | — | Intraday · Tomorrow · Days7 · Days30 · Event horizon · Seasonal horizon | `listDemandBookingCurve` ?horizon |
| Date from | date picker | — | — | `listDemandBookingCurve` ?dateFrom |
| Date to | date picker | — | — | `listDemandBookingCurve` ?dateTo |
| Price category | picker: choose a price category | — | — | `listDemandBookingCurve` ?priceCategory |
| Section code | text field | — | — | `listDemandBookingCurve` ?sectionCode |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Expected Rentals** (metric tile)

**Expected Revenue** (metric tile)

**Forecast Utilization** (metric tile)

**Sell-Out Probability** (metric tile)

**Inventory Shortage Risk** (metric tile)

**Maintenance Capacity Impact** (metric tile)

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **forecast**: Booking curve chart (actual vs forecast) per granule with the horizon picker and a confidence band. *(source: contracts/spine/catalogue.yaml#listDemandBookingCurve / DI-771)*

**Data it reads**: `listDemandBookingCurve` (onLoad, Demand forecast)

**Where the user goes next**

- → `BO-584` Rental Executive Command Center: *Back to Rental Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental forecasting demand list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental forecasting demand untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental forecasting demand yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental forecasting demand are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
forecast:
  product: Cabana full day
  horizon: next 14 days
  peak: 'Fri 21 Nov: 118% of capacity'
```

#### Permissions

- `listDemandBookingCurve` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 21.11.2 | Seat Demand Forecasting | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |
| 21.11.3 | Seat Inventory Forecasting | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |
| 21.11.4 | Revenue Forecasting by Section | Seat Management & Venue Mapping | CONTRACTED | `listDemandBookingCurve` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental command centre KPIs: realised revenue, total rentals, average utilisation, on-time return rate, damage rate, maintenance trends; further views for product performance, utilisation, equipment performance, duration/extension, damage/loss/deposit, channel/location and demand forecast. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-771)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-591` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS125 Rental Management Board 10.dc.html#bo-591`
- Workshop pack: Rental_Management.pdf board 10
- Flow F206 *Rental Management board 10: Rental Executive Command Center*, step 14: Works in Rental Forecasting & Demand Intelligence → Forecast future rental demand and identify capacity problems before they happen. This formally incorporates the AI utilization/demand forecasting recommendation from the source.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-591?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-584`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-592` Audit, Governance & Operational Control

**Provide management and administrators with traceability across Rental Management. The source requires role-based permissions and audit logging for rental operations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-592 |
| Who uses it | venue staff holding `RESOURCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | `resourceId` (navigation) |
| Route | `/rentals/audit-governance-operational-control-bo-592` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The rental audit log for managers and administrators: every material rental action (price change, inventory adjustment, deposit override, late-fee waiver, damage assessment, equipment swap, asset status override, retirement) with who, when, before, after and the approval, searchable and exportable, and visible only to the roles allowed to see it. The one thing to get right: before and after values side by side, and an automatic change marked as such ("Auto"), never shown as a person.

**Known correction pending (do not draw the wrong version)**

- **The table and detail panel have no bound columns and are titled "Every audit governance operational"** Why: The pack gives a seven-column audit table; title it "Rental audit log" and bind Date/Time, User, Action, Entity, Before, After, Approval (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-591 / screens/P08-venue-back-office.yaml#BO-592; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The only read is getResourceAuditTrail, which is per resource and opened with a resourceId** Why: The pack's log spans rentals, customers, prices and deposits across the venue; a per-resource trail cannot list price changes, late-fee waivers or deposit captures, which are rental and payment events. *(source: screens/P08-venue-back-office.yaml#BO-591 / contracts/satellite/resources.yaml#getResourceAuditTrail; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The audit entry carries no approval field** Why: The pack's Approval column (Manager, Auto, Approved) has nothing to bind to. *(source: contracts/satellite/resources.yaml#/components/schemas/ResourceAuditEntry; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The 16 pack audit kinds were turned into table columns** Why: They are values of the Action column and a filter, not columns. *(source: screens/P08-venue-back-office.yaml#BO-592; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is there one venue-wide audit search (rentals, resources, payments) or does each module keep its own?** → Drawn default accepted: Draw a single rental-filtered search over the shared audit table, with a greyed "All modules" toggle. *(decided by Chinmay, 2026-10-02; DEC-445 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Search**: Search by Rental ID, Customer, Asset, User, Action, Date as in the pack: one search box (rental id, asset code or customer name) plus Action chips (the 16 audit event kinds) and a date range. *(source: screens/P08-venue-back-office.yaml#BO-591)*

#### Outputs: what the screen shows and produces

**Shown**

**Every audit governance operational** (data table)

| Shows | Format | Notes |
|---|---|---|
| Product configuration change | text | not in the schema: `Product configuration change` |
| Inventory adjustment | text | not in the schema: `Inventory adjustment` |
| Asset status override | text | not in the schema: `Asset status override` |
| Price change | text | not in the schema: `Price change` |
| Deposit override | text | not in the schema: `Deposit override` |
| Booking modification | text | not in the schema: `Booking modification` |
| Cancellation | text | not in the schema: `Cancellation` |
| Equipment assignment | text | not in the schema: `Equipment assignment` |
| Rental extension | text | not in the schema: `Rental extension` |
| Equipment swap | text | not in the schema: `Equipment swap` |
| Late fee waiver | text | not in the schema: `Late-fee waiver` |
| Damage assessment | text | not in the schema: `Damage assessment` |
| Damage fee override | text | not in the schema: `Damage-fee override` |
| Deposit capture | text | not in the schema: `Deposit capture` |
| Maintenance status change | text | not in the schema: `Maintenance status change` |
| Asset retirement | text | not in the schema: `Asset retirement` |

**The selected audit governance operational** (detail panel): The pack groups this record's detail under its own headings: “Audit Table”, “Export”, “Rental Operator”, “Maintenance”, “Finance”, “Manager”.

| Shows | Format | Notes |
|---|---|---|
| Product configuration change | text | not in the schema: `Product configuration change` |
| Inventory adjustment | text | not in the schema: `Inventory adjustment` |
| Asset status override | text | not in the schema: `Asset status override` |
| Price change | text | not in the schema: `Price change` |
| Deposit override | text | not in the schema: `Deposit override` |
| Booking modification | text | not in the schema: `Booking modification` |
| Cancellation | text | not in the schema: `Cancellation` |
| Equipment assignment | text | not in the schema: `Equipment assignment` |
| Rental extension | text | not in the schema: `Rental extension` |
| Equipment swap | text | not in the schema: `Equipment swap` |
| Late fee waiver | text | not in the schema: `Late-fee waiver` |
| Damage assessment | text | not in the schema: `Damage assessment` |
| Damage fee override | text | not in the schema: `Damage-fee override` |
| Deposit capture | text | not in the schema: `Deposit capture` |
| Maintenance status change | text | not in the schema: `Maintenance status change` |
| Asset retirement | text | not in the schema: `Asset retirement` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Audit table**: Columns Date/Time, User (or "System" / "Auto" for automatic transitions), Action (plain words), Entity (RNT-10482, BIKE-017, Kayak), Before, After, Approval (Manager, Auto, Approved, Not required). Newest first, cursor paging (VO-R12). Money in AED (VO-R10). *(source: screens/P08-venue-back-office.yaml#BO-591 / contracts/satellite/resources.yaml#/components/schemas/ResourceAuditEntry)*
- **Detail panel**: The full entry with reason, source channel (POS, Staff App, back office, API) and correlation id; a "View rental" link. *(source: contracts/satellite/resources.yaml#getResourceAuditTrail)*
- **Role-based visibility**: Rental operator sees operational rows only; Maintenance sees asset and maintenance rows; Finance sees commercial and deposit rows; Manager sees location-level rows; Administrator sees all. Hidden kinds are not drawn as empty rows; a note says "Showing operational actions for your role" (per VO-R08). *(source: screens/P08-venue-back-office.yaml#BO-591)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Export**: Excel, CSV or PDF of the current filter; export is itself permission-checked and logged. *(source: screens/P08-venue-back-office.yaml#BO-591)*
- **Back to Rental Executive Command Center**: Returns to BO-584. *(source: screens/P08-venue-back-office.yaml#BO-592)*

**Where the user goes next**

- → `BO-584` Rental Executive Command Center: *Back to Rental Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The audit governance operational list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the audit governance operational untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No audit governance operational yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the audit governance operational are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Entry made offline at a rental desk**: Shows the device time it happened and a small "synced 14:31" note; ordering is by when it happened. *(source: contracts/satellite/resources.yaml#checkOutResource)*
- **Viewer without audit rights**: Empty state "Needs audit access for rentals", not an empty table. *(source: ADR-0002 / DI-387)*

#### Consistency with other screens

- Match `BO-950`: Same audit table component, columns and source-channel labels as the resource decision history; rental is a filtered view of it.
- Match `BO-863`: The per-resource audit timeline on lifecycle uses the same entries.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- at: 08 Oct 2026 14:22
  user: Ahmed Al Mansoori
  action: Late fee waiver
  entity: RNT-10482
  before: AED 80.00
  after: AED 0.00
  approval: Manager
- at: 08 Oct 2026 15:10
  user: Auto
  action: Asset status
  entity: BIKE-017
  before: Rented
  after: Inspection
  approval: Auto
- at: 08 Oct 2026 16:42
  user: Fatima Al Hashimi
  action: Price change
  entity: Double Kayak 2 h
  before: AED 120.00
  after: AED 135.00
  approval: Approved
```

#### Permissions

- `getResourceAuditTrail` → `RESOURCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-592` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS125 Rental Management Board 10.dc.html#bo-592`
- Workshop pack: Rental_Management.pdf board 10
- Flow F206 *Rental Management board 10: Rental Executive Command Center*, step 16: Works in Audit, Governance & Operational Control → Provide management and administrators with traceability across Rental Management. The source requires role-based permissions and audit logging for rental operations.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (32 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-592?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-584`.
- [ ] Every gated control is gated: `RESOURCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-593` AI Rental Management Copilot & Action Center

**Provide a natural-language AI interface across the complete Rental Management module. I strongly recommend this as the final screen because it aligns the rental module with TICVAI's overall AI-first architecture. Instead of management having to manually navigate every report, they should be able to ask TICVAI questions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-593 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPIs & Dashboards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/ai-rental-management-copilot-action-center-bo-593` |

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Ask questions about rentals in plain language and get an answer with how it was interpreted, the figures behind it and a confidence, within the user's own access. AI's role in rentals is reporting and maintenance-scheduling recommendations; it does not run rental operations.

**Known correction pending (do not draw the wrong version)**

- **A metric tile labelled "↓" is declared.** Why: Pack glyph parsed as a label. *(source: screens/P08-venue-back-office.yaml#BO-593; Finance, Ledger & Tax · Reporting & Analytics)*
- **A rental-only assistant duplicates the reporting area's natural-language analytics.** Why: DI-721. *(source: DI-721 / screens/P16-venue-analytics.yaml#ANL-052; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**↓** (metric tile)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **answer**: Interpretation, answer, source figures, confidence, suggested follow-ups; asks a clarifying question when period, location or measure is missing. *(source: MATRIX 8.7.30 / DI-712 / DI-964)*

**Where the user goes next**

- → `BO-584` Rental Executive Command Center: *Back to Rental Executive Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental copilot action list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental copilot action untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental copilot action yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental copilot action are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Question could not be interpreted. (ReportQuestionProblem) |

#### Consistency with other screens

- Match `P16 ANL-052 Ask TICVAI, ANL-009 AI Assistant & Action Center`: Same question box and answer card.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- 'Q: Which items had the most damage at Marina A last month? A: Snowboards 156 cm, 14 damage reports of 312 rentals
  (4.49%); confidence high; follow-up: compare with August?'
```

#### Permissions

- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.7.30 | System shall support natural language reporting. | Unified Operations Dashboard | CONTRACTED | `askReportingQuestion` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- In rentals AI's practical role is reporting and maintenance-scheduling recommendations; day-to-day rental operations stay staff-managed. *(agreed · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-772)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-593` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS125 Rental Management Board 10.dc.html#bo-593`
- Workshop pack: Rental_Management.pdf board 10
- Flow F206 *Rental Management board 10: Rental Executive Command Center*, step 18: Works in AI Rental Management Copilot & Action Center → Provide a natural-language AI interface across the complete Rental Management module. I strongly recommend this as the final screen because it aligns the rental module with TICVAI's overall AI-first …
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)
- ADR-0059 *AI phasing against the six-month plan* (`docs/adr/0059-ai-phasing-against-the-six-month-plan.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-593?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-584`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**9 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"askReportingQuestion": {"method":"POST","path":"/reports/ask","contract":"reporting","summary":"Natural-language reporting query","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"NaturalLanguageAnswer"},
"getAnalyticsBenchmark": {"method":"GET","path":"/analytics-benchmarks","contract":"reporting","summary":"One site against another, on a like-for-like basis","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"kpiId","in":"query","required":true},{"name":"scopePaths","in":"query","required":null},{"name":"normaliseBy","in":"query","required":null}],"requestBody":null,"responds":"BenchmarkRow"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null},{"name":"module","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getResourceAuditTrail": {"method":"GET","path":"/resources/{resourceId}/audit","contract":"resources","summary":"Every material change, with who and why","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ResourceAuditEntry"},
"getResourceUtilisation": {"method":"GET","path":"/resource-utilisation","contract":"resources","summary":"How much of each resource's available time was used","permission":"RESOURCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"ResourceUtilisation"},
"listDemandBookingCurve": {"method":"GET","path":"/demand-booking-curve","contract":"catalogue","summary":"AI Demand Forecasting & Booking Curve Studio","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"performance","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"horizon","in":"query","required":false},{"name":"dateFrom","in":"query","required":false},{"name":"dateTo","in":"query","required":false},{"name":"priceCategory","in":"query","required":false},{"name":"sectionCode","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRentalBookings": {"method":"GET","path":"/rental-bookings","contract":"rental","summary":"Reservations across venues and locations","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"locationId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"RentalBooking"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiDemandForecastingBookingCurveStudioView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What AI Demand Forecasting & Booking Curve Studio displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venue":{"type":"string","description":"Venue id"},"product":{"type":"string","description":"Product id","nullable":true},"event":{"type":"string","description":"Event id","nullable":true},"performance":{"type":"string","description":"Performance id","nullable":true},"date":{"type":"string","description":"Date","format":"date"},"timeslot":{"type":"string","description":"Timeslot","nullable":true},"priceCategory":{"type":"string","description":"Price category","nullable":true},"sectionCode":{"type":"string","nullable":true,"description":"Seat-map section (`seating.Section.code`) the row forecasts; null for a row at price-category or performance level (29 September, build pass, group G2; 21.11.4)"},"channel":{"$ref":"#/components/schemas/Channel","description":"Channel"},"confidence":{"type":"number","description":"Forecast Confidence, percent"},"forecastFinalOccupancy":{"type":"number","description":"Forecast Final Occupancy, percent"},"demand":{"type":"integer","description":"Forecast demand"},"attendance":{"type":"integer","description":"Forecast attendance"},"occupancy":{"type":"number","description":"Forecast occupancy, percent"},"sellThrough":{"type":"number","description":"Forecast sell-through, percent"},"expectedSellOutTime":{"type":"string","description":"Expected Sell-Out Time; empty if no sell-out forecast","format":"date-time","nullable":true},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Forecast revenue"},"conversion":{"type":"number","description":"Forecast conversion, percent"},"remainingInventory":{"type":"integer","description":"Forecast remaining inventory at event"},"mape":{"type":"number","description":"MAPE over closed forecasts at this level, percent"},"forecastBias":{"type":"number","description":"Forecast Bias (positive = over-forecast), percent"},"overForecast":{"type":"number","description":"Share of closed forecasts that over-forecast, percent"},"underForecast":{"type":"number","description":"Share of closed forecasts that under-forecast, percent"},"forecastId":{"type":"string","description":"Forecast id"},"horizon":{"type":"string","description":"Forecast Horizon","enum":["intraday","tomorrow","days7","days30","eventHorizon","seasonalHorizon"]},"bookingCurve":{"type":"array","items":{"type":"object","properties":{"daysBeforeEvent":{"type":"integer","description":"T minus days"},"historicalExpectedPercentSold":{"type":"number","description":"Historical expected curve, percent sold"},"actualPercentSold":{"type":"number","nullable":true,"description":"Current actual curve, percent sold (empty for future points)"},"forecastPercentSold":{"type":"number","description":"AI forecast curve, percent sold"}}},"description":"Booking Curve"},"signalContributions":{"type":"array","items":{"type":"object","properties":{"signal":{"type":"string","enum":["internalSales","bookingVelocity","occupancy","historicalEvents","nearbyEvent","weather","marketTourism","competitor","priceElasticity","other"],"description":"Signal category"},"contributionPercent":{"type":"number","description":"Explanatory share of the forecast"}}},"description":"Model Inputs: which signals contributed"},"confidenceReasons":{"type":"array","items":{"type":"string","enum":["strongHistoricalData","stableBookingPattern","reliableExternalSignals","limitedHistoricalData","volatileBookingPattern","degradedExternalSignals"]},"description":"Reasons behind the forecast confidence"},"modelVersion":{"type":"string","description":"Model version that produced the forecast"},"generatedAt":{"type":"string","description":"When the forecast was produced","format":"date-time"}}},
"BenchmarkNormalisation": {"type":"string","description":"The basis a benchmark is compared on. Shared by `getAnalyticsBenchmark` and `BenchmarkRow`.","enum":["none","perVisitor","perOperatingHour","perStaffedPosition","perSquareMetre"]},
"BenchmarkRow": {"type":"object","description":"BI board 10.4. **The normalisation travels with the comparison.**","properties":{"scopePath":{"type":"string"},"label":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"normalisedValue":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"normaliseBy":{"$ref":"#/components/schemas/BenchmarkNormalisation"},"rank":{"type":"integer"},"percentile":{"type":"number","nullable":true}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"GeneratedQuery": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n","properties":{"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"compiledSql":{"type":"string","nullable":true,"description":"The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"}}},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"NaturalLanguageAnswer": {"x-ticvai-persistence":"none — computed","type":"object","required":["conversationId","question","interpretation","result","reliability"],"properties":{"conversationId":{"type":"string"},"question":{"type":"string"},"interpretation":{"type":"string","description":"What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."},"semanticSpec":{"allOf":[{"$ref":"#/components/schemas/ReportingSemanticQuerySpec"}],"nullable":true,"description":"What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"},"generatedQuery":{"allOf":[{"$ref":"#/components/schemas/GeneratedQuery"}],"nullable":true,"description":"The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"},"result":{"allOf":[{"$ref":"#/components/schemas/ReportResult"}],"nullable":true,"description":"Null when the question is outside the semantic model."},"dataAsOf":{"type":"string","format":"date-time","nullable":true,"description":"Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."},"reliability":{"$ref":"#/components/schemas/ReportingAnswerReliability"},"unavailableReason":{"allOf":[{"$ref":"#/components/schemas/ReportingUnavailableReason"}],"nullable":true,"description":"Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."},"confidence":{"type":"number","minimum":0,"maximum":1,"deprecated":true,"description":"Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."},"suggestedFollowUps":{"type":"array","items":{"type":"string"}},"modelVersion":{"type":"string"},"tokensUsed":{"type":"integer"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RentalBooking": {"type":"object","x-ticvai-persistence":"rental.booking","description":"Board 5. **The booking outlives the order** — an order completes at payment and the rental is still out.\n","required":["id","productId","from","to","status"],"properties":{"id":{"type":"string","format":"uuid"},"reference":{"type":"string"},"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"returnLocationId":{"type":"string","format":"uuid","nullable":true},"customerId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer"},"status":{"type":"string","enum":["draft","confirmed","awaitingArrival","checkedOut","overdue","partiallyReturned","completed","completedWithDamage","notReturned","cancelled","noShow"]},"checkedOutAt":{"type":"string","format":"date-time","nullable":true},"dueBackAt":{"type":"string","format":"date-time","nullable":true},"returnedAt":{"type":"string","format":"date-time","nullable":true},"depositAuthorisationId":{"type":"string","format":"uuid","nullable":true,"description":"The card deposit's terminal pre-authorisation, written by `checkOutRental` (workbook Q304; CHG-CSA-029). The hold is kept whole until every unit is back (workbook Q306)."},"accruedLateFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"readiness":{"type":"array","readOnly":true,"description":"**Computed, not stored** — agreement, requirements, deposit, equipment.","items":{"type":"object","properties":{"check":{"type":"string"},"satisfied":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"participants":{"type":"array","items":{"$ref":"#/components/schemas/RentalParticipant"}},"scopePath":{"type":"string"}}},
"RentalParticipant": {"type":"object","x-ticvai-persistence":"rental.participant","description":"Board 5.5. **A group rental is one booking with participants**, because the agreement, the deposit and the return are handled together.\n","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"isPrimaryRenter":{"type":"boolean","default":false},"dateOfBirth":{"type":"string","format":"date","nullable":true},"idNumber":{"type":"string","nullable":true},"guardianName":{"type":"string","nullable":true},"emergencyContact":{"type":"string","nullable":true},"hasSignedWaiver":{"type":"boolean","readOnly":true},"customFields":{"type":"object","additionalProperties":true}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"ReportingAnswerReliability": {"type":"string","description":"**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},
"ReportingSemanticQuerySpec": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n","required":["metric","period"],"properties":{"metric":{"type":"string","description":"A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."},"dimensions":{"type":"array","maxItems":5,"description":"Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.","items":{"type":"string"}},"filters":{"type":"array","items":{"type":"object","required":["field","operator"],"properties":{"field":{"type":"string","description":"A `SemanticModel` field code."},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","isNull","isNotNull"]},"values":{"type":"array","description":"**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n","items":{}}}}},"period":{"type":"string","description":"ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."},"comparison":{"type":"string","nullable":true,"description":"As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.","enum":["previousPeriod","samePeriodLastYear","target","benchmark"]},"semanticModelVersion":{"type":"integer","readOnly":true,"description":"The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."}}},
"ReportingUnavailableReason": {"type":"string","description":"Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.","enum":["metricNotModelled","dimensionNotModelled","filterNotModelled","comparisonNotAvailable","periodOutsideHistory"]},
"ResourceAuditEntry": {"type":"object","x-ticvai-persistence":"resources.resource_audit","description":"Board 1.10. **Immutable, and it carries the previous value.**","properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"actorId":{"type":"string","format":"uuid","nullable":true},"action":{"type":"string"},"field":{"type":"string","nullable":true},"previousValue":{"nullable":true},"newValue":{"nullable":true},"reason":{"type":"string","nullable":true},"sourceChannel":{"type":"string","nullable":true},"apiOrigin":{"type":"string","nullable":true},"correlationId":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"ResourceUtilisation": {"type":"object","description":"Board 10.02. **Booked time over available time**, where available knows about schedules, blocks, setup and travel.\n","properties":{"key":{"type":"string"},"label":{"type":"string"},"availableMinutes":{"type":"integer"},"bookedMinutes":{"type":"integer"},"blockedMinutes":{"type":"integer"},"utilisationPercent":{"type":"number"},"bookingCount":{"type":"integer"}}}
}
```
