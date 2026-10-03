# WS83 — Game and Ride board 6

**10 screens · 13 operations · 14 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `DEVICE_VIEW, ORDER_CREATE, PRICE_CONFIGURE, PRODUCT_CONFIGURE, PRODUCT_VIEW, WALLET_VIEW`. A control nobody can use must say so,
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
| `BO-444` | Redemption Operations Dashboard | B | 2 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-445` | Redemption Credit Rule Configuration | D | 7 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-446` | Ticket-Based Redemption / Ticket-Eater Integration | D | 0 | 2 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-447` | Ticketless Redemption Game Integration | D | 0 | 17 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-448` | Redemption Wallet & Balance View | C | 0 | 0 | 6 | 16 | 0 | 6 | — | notStarted (—) |
| `BO-449` | Redemption Counter / Prize Checkout | D | 0 | 4 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-450` | Prize Catalogue & Credit Cost Configuration | D | 19 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-451` | Prize Inventory Integration | D | 0 | 15 | 6 | 12 | 0 | 4 | — | notStarted (—) |
| `BO-452` | Direct-Pay / Crane & Prize Machine Configuration | D | 23 | 56 | 6 | 13 | 0 | 0 | — | notStarted (—) |
| `BO-453` | Redemption Transaction Ledger, Reconciliation & Audit | D | 0 | 41 | 6 | 3 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-446, BO-447, BO-448, BO-450, BO-451 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-444` Redemption Operations Dashboard

**Provide a central operational view of redemption activity across venues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block B · task VM-BO-444 |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/redemption-operations-dashboard-bo-444` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-025): listRedemption is coupon redemption analytics (promotions); the games redemption dashboard is about prize redemption (DI-878), two meanings of redemption … Contract gap recorded 2 October 2026 (CHG-WIR-027): A read of prize redemptions (redeemPrize records them; nothing lists them) for the redemption operations dashboard.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Redemption activity across venues: coupon and promo-code redemptions and their performance.

**Fixed on main** (the package already carries these; draw what it says): The screen sits in Games & Rides (redemption of game points for prizes) but reads coupon redemption analytics. (CHG-WIR-025); List operation(s) listRedemption return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listRedemption … (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search redemption operations | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, zone, source type, game, prize, date and 1 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Redemption Credits Earned Today** (metric tile)

**Redemption Credits Redeemed** (metric tile)

**Active Redemption Wallets** (metric tile)

**Prize Redemptions Today** (metric tile)

**Ticket-Eater Transactions** (metric tile)

**Ticketless Redemption Transactions** (metric tile)

**Low-Stock Prize Items** (metric tile)

**Failed Redemption Transactions** (metric tile)

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **redemption analytics**: Redemptions, discount given and conversion by campaign and channel. *(source: contracts/satellite/promotions.yaml#listRedemption)*

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-445` Redemption Credit Rule Configuration: *Redemption Credit Rule Configuration*
- → `BO-446` Ticket-Based Redemption / Ticket-Eater Integration: *Ticket-Based Redemption / Ticket-Eater Integration*
- → `BO-447` Ticketless Redemption Game Integration: *Ticketless Redemption Game Integration*
- → `BO-448` Redemption Wallet & Balance View: *Redemption Wallet & Balance View*
- → `BO-449` Redemption Counter / Prize Checkout: *Redemption Counter / Prize Checkout*
- → `BO-450` Prize Catalogue & Credit Cost Configuration: *Prize Catalogue & Credit Cost Configuration*
- → `BO-451` Prize Inventory Integration: *Prize Inventory Integration*
- → `BO-452` Direct-Pay / Crane & Prize Machine Configuration: *Direct-Pay / Crane & Prize Machine Configuration*
- → `BO-453` Redemption Transaction Ledger, Reconciliation & Audit: *Redemption Transaction Ledger, Reconciliation & Audit*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The redemption operations list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the redemption operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No redemption operations yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the redemption operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
redemptions:
- campaign: INSTA-DUNE
  redeemed: 412
  discount: AED 12,360.00
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Redemption points earned per game (score or level) are redeemed for prizes at a counter; per-game config of points granted or required (e.g. 200 points to play using redemption credit). *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-878)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-444` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS63 Game and Ride Board 6.dc.html#bo-444`
- Workshop pack: Game_and_Ride_Module.pdf board 6
- Flow F192 *Game and Ride board 6: Redemption Operations Dashboard*, step 1: Opens Redemption Operations Dashboard → Provide a central operational view of redemption activity across venues.
- Flow F192 *Game and Ride board 6: Redemption Operations Dashboard*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F192 *Game and Ride board 6: Redemption Operations Dashboard*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F192 *Game and Ride board 6: Redemption Operations Dashboard*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F192 *Game and Ride board 6: Redemption Operations Dashboard*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F192 *Game and Ride board 6: Redemption Operations Dashboard*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F192 *Game and Ride board 6: Redemption Operations Dashboard*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F192 *Game and Ride board 6: Redemption Operations Dashboard*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F192 branch at step 1 (expected): when Nothing has been set up on Redemption Operations Dashboard yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F192 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-444?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-445`, `BO-446`, `BO-447`, `BO-448`, `BO-449`, `BO-450`, `BO-451`, `BO-452`, `BO-453`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-445` Redemption Credit Rule Configuration

**Configure how games generate redemption credits.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-445 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/redemption-credit-rule-configuration-bo-445` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-001): The prize catalogue has nothing to do with how games earn credits; it belongs to BO-449 and BO-450 (design-notes correction venue-operations BO-445). Contract gap recorded 2 October 2026 (CHG-WIR-004): No read of redemption rules (setRedemptionRules has no get).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Where the venue decides how many redemption credits a game awards for a play: fixed per play, by score, by score band, or as reported by the machine. Redemption credits are the "prize currency" a guest earns by playing and spends at the prize counter; they are never the paid game credit. The one thing to get right: this, ticket-eater integration (BO-446) and ticketless games (BO-447) all write one redemption rules record, so draw one editor with sections and a single Save.

**Known correction pending (do not draw the wrong version)**

- **"External Game Value" and "Machine-Reported Value" are drawn as action-bar buttons** Why: They are two of the five calculation methods in the pack, options of one choice, not actions. *(source: screens/P08-venue-back-office.yaml#BO-445; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Rule Name, Effective Dates and Status are select fields; Game / Game Group is free text** Why: Generated control types; a name is text, dates are a range picker, status is a toggle and the game is a picker. *(source: screens/P08-venue-back-office.yaml#BO-445; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The record cannot hold score bands, minimum, multiplier, rounding, bonus or promotional multiplier, rule name, status or dates** Why: earnRules carries only ticketsPerPlay, ticketsPerScorePoint and maximumPerPlay; the pack's Tier-based method and its six controls have nowhere to go. *(source: screens/P08-venue-back-office.yaml#BO-446 / contracts/satellite/games.yaml#/components/schemas/RedemptionRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The same currency is called tickets, points and redemption credits** Why: RedemptionRules says tickets, GameCard says points, the pack says redemption credits. Use "Redemption credits" on every screen of boards 6, 7 and 10. *(source: screens/P08-venue-back-office.yaml#BO-444 / contracts/satellite/games.yaml#/components/schemas/GameCard / contracts/satellite/games.yaml#/components/schemas/RedemptionRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The write has no read (CHG-WIR-004)

**Fixed on main** (the package already carries these; draw what it says): listPrizes is bound on load (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should one earn rule be shareable by a game group, or is it always per game?** → Drawn default accepted: Per game, with "Apply to several games" as a copy action. *(decided by Chinmay, 2026-10-02; DEC-412 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Rule Name | select field | — | — | — | — | — | — |
| Game / Game Group | text field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Redemption Enabled | select field | — | — | — | — | — | — |
| Credit Calculation Method | select field | — | — | — | — | — | — |
| Effective Dates | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Rule name, Status, Effective dates**: The pack asks for a named rule with Active / Inactive status and an effective date range. The record holds per-game earn rules with no name, status or dates; draw them greyed (per VO-R13) and show the rule as "Basketball Pro earn rule" until the record carries a name. *(source: screens/P08-venue-back-office.yaml#BO-445 / contracts/satellite/games.yaml#/components/schemas/RedemptionRules)*
- **Game / Game group (earnRules.gameId)**: A game picker, one rule per game; a game appears once. "Game group" (several games sharing one rule) is not in the record: offer "Apply to several games" which copies the rule to each selected game. *(source: screens/P08-venue-back-office.yaml#BO-445 / contracts/satellite/games.yaml#/components/schemas/RedemptionRules)*
- **Credit calculation method**: A single choice of the pack's five: Fixed per play, Score-based, Tier-based (score bands), External game value, Machine-reported value. Fixed shows "credits per play" (ticketsPerPlay); Score-based shows "credits per score point" (ticketsPerScorePoint). Tier-based shows a band table (Score from, Score to, Credits), the pack's Basketball example pre-filled as a hint. External and Machine-reported take the number the game sends, capped by the maximum. *(source: screens/P08-venue-back-office.yaml#BO-445 / screens/P08-venue-back-office.yaml#BO-446 / contracts/satellite/games.yaml#/components/schemas/RedemptionRules)*
- **Controls (minimum, maximum, multiplier, rounding, bonus credits, promotional multiplier)**: Group under "Limits and boosts". Maximum per play maps to maximumPerPlay; the other five have no field and are drawn greyed. Rounding is a closed set (Round down, Round to nearest, Round up), never free text. *(source: screens/P08-venue-back-office.yaml#BO-446 / contracts/satellite/games.yaml#/components/schemas/RedemptionRules)*
- **Venue**: From the top-bar venue switcher, not a field (per VO-R03 and VO-R09). *(source: contracts/spine/access.yaml#setJourneySequenceRule / ADR-0030)*
- **Where credits are held, expiry and counter approval**: A "Redemption credit settings" section shared with BO-446/447/449: the credit type that holds them (ticketCreditTypeId), Ticketless games on (default on), Ticket-eaters on (default off), Credits expire (default off) with validity in days shown only when on, and "A prize above [ ] credits needs a second person" (counterApprovalAboveTickets, empty = never). *(source: contracts/satellite/games.yaml#setRedemptionRules)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| External Game Value (primary button) | navigation or local | — | — | — | — |
| Machine-Reported Value (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Earn calculator**: Beside the form, a "Try a score" box: enter a score, see the credits awarded with the steps (band matched, cap applied). Example "Basketball Pro, score 26: band 21-30, 200 credits". *(source: screens/P08-venue-back-office.yaml#BO-446 / screens/P08-venue-back-office.yaml#BO-448)*
- **Rules list**: Columns Game, Method ("Score bands, 4 bands"), Maximum per play, Status. One row per game, sorted by game name. *(source: designer default)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save redemption rules**: Sends the whole record, every game's rule and the shared settings, in one PUT (per VO-R04). Confirm names the games affected ("Changes earn rules for 3 games; readers apply them after their next configuration deployment"). *(source: contracts/satellite/games.yaml#setRedemptionRules / contracts/satellite/games.yaml#deployReaderConfiguration)*
- **Validate**: Checks band overlaps and gaps (score 10 in two bands; no band covering 31+) and shows them against the rows before Save. *(source: screens/P08-venue-back-office.yaml#BO-442 / designer default)*

**Where the user goes next**

- → `BO-444` Redemption Operations Dashboard: *Back to Redemption Operations Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The redemption credit rule configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the redemption credit rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No redemption credit rule configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **The machine reports more credits than the configured maximum**: The award is capped and the play is flagged for the reconciliation on BO-453 ("Machine reported 500, credited 300"). *(source: screens/P08-venue-back-office.yaml#BO-453 / contracts/satellite/games.yaml#setRedemptionRules)*
- **Turning ticketless games off while games still award credits**: Warn before save that the listed games will stop crediting cards after the next deployment. *(source: contracts/satellite/games.yaml#/components/schemas/RedemptionRules)*
- **A game with both a game-level points range and an earn rule maximum**: Show the stricter of the two and say which one limits ("Capped at 300 by the game profile"). *(source: contracts/satellite/games.yaml#/components/schemas/Game / contracts/satellite/games.yaml#/components/schemas/RedemptionRules)*

#### Consistency with other screens

- Match `BO-446`: Same record, section "Ticket-eaters"; one Save across BO-445, BO-446 and BO-447 (per VO-R14).
- Match `BO-399`: DI-878's "200 points to play using redemption credit" is the spend side, set as an accepted credit type on the game; this screen is only the earn side.
- Match `BO-449`: The second-person threshold set here is what the counter enforces.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
earnRules:
- game: Basketball Pro
  method: Score bands
  bands: '0-10: 50, 11-20: 100, 21-30: 200, 31+: 300'
  maxPerPlay: 300
- game: Prize Crane
  method: Fixed per play
  perPlay: 10
- game: Laser Arena
  method: Score-based
  perScorePoint: 0.5
  maxPerPlay: 400
settings:
  ticketless: 'On'
  ticketEaters: 'On'
  expire: 'Off'
  secondPersonAbove: 10000
```

#### Permissions

- `setRedemptionRules` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Redemption points earned per game (score or level) are redeemed for prizes at a counter; per-game config of points granted or required (e.g. 200 points to play using redemption credit). *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-878)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-445` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS63 Game and Ride Board 6.dc.html#bo-445`
- Workshop pack: Game_and_Ride_Module.pdf board 6
- Flow F192 *Game and Ride board 6: Redemption Operations Dashboard*, step 2: Works in Redemption Credit Rule Configuration → Configure how games generate redemption credits.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-445?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: External Game Value, Machine-Reported Value.
- [ ] Every transition is wired: `BO-444`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-446` Ticket-Based Redemption / Ticket-Eater Integration

**Configure the integration with ticket-eater machines that convert physical redemption tickets into digital wallet credits.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-446 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Customer identifies wallet/card) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/ticket-based-redemption-ticket-eater-integration-bo-446` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Configures the ticket-eater machines that count paper redemption tickets and post the count as digital redemption credits to the guest's card. Staff need the machine list, the conversion rule, and what happens when a machine jams, sees a fake ticket or cannot identify the card. The one thing to get right: the pack asks for this flow to be drawn visually and kept distinct from ticketless games: Physical tickets, then Ticket-eater, then TICVAI, then Wallet.

**Known correction pending (do not draw the wrong version)**

- **The machine list and detail have no source (generated "Every ticket-based redemption ticket-eater")** Why: No operation lists ticket-eaters or holds their configuration; they are devices (ADR-0067) and the list must read the device register. *(source: ADR-0067 / contracts/spine/tenancy.yaml#listDevices; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No field for the conversion rule** Why: The pack makes "N tickets = M credits" configurable; RedemptionRules has only the ticketEaterEnabled switch. *(source: screens/P08-venue-back-office.yaml#BO-446 / contracts/satellite/games.yaml#/components/schemas/RedemptionRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No write path posts a ticket-eater count** Why: recordGamePlay needs creditsUsed of at least 1, so a machine that takes no payment cannot report a count through it; the integration needs its own posting operation. *(source: contracts/satellite/games.yaml#/components/schemas/RecordPlayRequest; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **When tickets are fed in and the card identification fails, are the counted tickets lost, held on the machine, or printed as a claim slip?** → Drawn default accepted: Draw "Count held on the machine, tap your card to claim" and flag it for client confirmation. *(decided by Chinmay, 2026-10-02; DEC-413 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Ticket-eater machine (ID, name, zone, IP / device ID, status, reader)**: Not typed in here. A ticket-eater is a device in the platform device register; pick a registered device of the ticket-eater kind and show its name, zone, address and status read-only, with a link to the device record. *(source: screens/P08-venue-back-office.yaml#BO-446 / ADR-0067 / ADR-0015)*
- **Conversion rule**: "[1] physical ticket = [1] redemption credit", two whole numbers, default 1 to 1, with a preview line ("850 tickets inserted = 850 credits"). One rule per machine, or venue default when empty. *(source: screens/P08-venue-back-office.yaml#BO-446 / screens/P08-venue-back-office.yaml#BO-447)*
- **Ticket-eaters enabled**: The venue switch (ticketEaterEnabled, default off) heads the section; with it off the machine list shows but every machine reads "Not accepting tickets". *(source: contracts/satellite/games.yaml#/components/schemas/RedemptionRules)*

#### Outputs: what the screen shows and produces

**Shown**

**Every ticket-based redemption ticket-eater** (data table)

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**The selected ticket-based redemption ticket-eater** (detail panel): The pack groups this record's detail under its own headings: “The source specifically requires”, “Physical tickets inserted”, “Ticket-Eater counts tickets”, “Machine sends count to TICVAI”, “Credits added to wallet”, “Transaction Result”.

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Flow diagram**: A horizontal flow at the top: Card identified, Tickets inserted, Machine counts, Count sent to TICVAI, TICVAI validates, Credits added, Balance shown. Mirror it on BO-447 with the ticketless flow so the two read as a pair. *(source: screens/P08-venue-back-office.yaml#BO-446 / screens/P08-venue-back-office.yaml#BO-447 / screens/P08-venue-back-office.yaml#BO-453)*
- **Machine list**: Columns Machine, Zone, Status (Online / Offline / Jammed), Conversion, Tickets today, Last count. Offline machines first. *(source: screens/P08-venue-back-office.yaml#BO-446)*
- **Last transaction panel**: "Tickets inserted 850 / Credits added 850 / New redemption balance 2,450", card masked (****4321). *(source: screens/P08-venue-back-office.yaml#BO-447)*
- **Exception handling**: A fixed list with what the guest and the attendant see for each: Ticket jam (count kept, call attendant), Invalid ticket (rejected, not counted), Duplicate transaction (ignored, not credited twice), Machine offline (counts held on the machine until it reconnects), Wallet identification failed (tap card first; count not posted). *(source: screens/P08-venue-back-office.yaml#BO-447)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Saves the shared redemption rules record (per VO-R14 with BO-445 and BO-447); a machine-level conversion has no field yet and is greyed. *(source: contracts/satellite/games.yaml#setRedemptionRules)*
- **Test machine**: Runs the device test (connectivity, card read) and shows each check passed or failed. *(source: contracts/satellite/games.yaml#testReader)*

**Where the user goes next**

- → `BO-444` Redemption Operations Dashboard: *Back to Redemption Operations Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ticket-based redemption ticket-eater list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ticket-based redemption ticket-eater untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ticket-based redemption ticket-eater yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the ticket-based redemption ticket-eater are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **The same count arrives twice after a network retry**: Credited once; the duplicate appears on BO-453 as "Duplicate ignored" with both arrival times. *(source: screens/P08-venue-back-office.yaml#BO-447 / screens/P08-venue-back-office.yaml#BO-453)*
- **Tickets inserted with no card tapped**: The machine prompts "Tap your card first"; nothing posts. A count already taken is held on the machine: "Tap your card to claim" (for the client to confirm). *(source: screens/P08-venue-back-office.yaml#BO-447 / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*
- **The card tapped is blocked or expired**: Credits are not posted to a blocked or expired card; the machine shows the card status reason. *(source: contracts/satellite/games.yaml#/components/schemas/GameCard)*

#### Consistency with other screens

- Match `BO-447`: Twin screen; same layout, the flow differs only in its first two steps.
- Match `BO-404`: Ticket-eaters are devices in the same device register as readers; status words match the reader health monitor (BO-466).
- Match `BO-453`: The machine count versus credits posted is one of the reconciliation columns there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
machines:
- machine: TE-01 Ticket Eater
  zone: Summit Peaks Arcade
  status: Online
  conversion: 1 ticket = 1 credit
  ticketsToday: 18420
  lastCount: '10:40'
- machine: TE-02 Ticket Eater
  zone: Family Zone
  status: Offline since 09:55
  conversion: 1 ticket = 1 credit
  ticketsToday: 6110
  lastCount: 09:52
lastTransaction:
  card: '****4321'
  guest: Khalid Al Zaabi
  inserted: 850
  added: 850
  newBalance: 2450
```

#### Permissions

- `setRedemptionRules` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Physical-ticket redemption: some games dispense paper tickets by score, redeemed at a counter or ticket-counting machine. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-879)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-446` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS63 Game and Ride Board 6.dc.html#bo-446`
- Workshop pack: Game_and_Ride_Module.pdf board 6
- Flow F192 *Game and Ride board 6: Redemption Operations Dashboard*, step 4: Works in Ticket-Based Redemption / Ticket-Eater Integration → Configure the integration with ticket-eater machines that convert physical redemption tickets into digital wallet credits.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-446?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-444`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-447` Ticketless Redemption Game Integration

**Configure games that automatically send redemption-credit results to TICVAI after gameplay. The source requires integration with redemption games to digitally load credits after the guest completes a game.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-447 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Guest taps card) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/ticketless-redemption-game-integration-bo-447` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Configures the ticketless redemption games: after a game ends the machine sends its score or award to TICVAI, which validates it against the authorised play and credits the guest's card with no paper. The one thing to get right: a result is accepted only for a play TICVAI authorised (correct game, correct play id, not already credited), so the screen must show that validation chain, not just a game list.

**Known correction pending (do not draw the wrong version)**

- **Two maxima for the same award** Why: Game carries minPointsAwarded and maxPointsAwarded while the earn rule carries maximumPerPlay; the contract must say which wins (draw the stricter, per BO-445). *(source: contracts/satellite/games.yaml#/components/schemas/Game / contracts/satellite/games.yaml#/components/schemas/RedemptionRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The games list is unbound (generated "Every ticketless redemption game") (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is "Redemption enabled" a per-game switch (the pack) or implied by the game having an earn rule (the contract)?** → Drawn default accepted: Per-game toggle that adds or removes the game's earn rule. *(decided by Chinmay, 2026-10-02; DEC-414 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | In service · Out of service · Maintenance · Retired | `listGames` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Game, Game ID, Reader, Device / game controller**: Pick a game; its code, mapped reader and controller come from the game and reader records and are shown read-only here, with links to BO-396 and BO-400. Only games whose type pays out tickets are offered. *(source: screens/P08-venue-back-office.yaml#BO-447 / contracts/satellite/games.yaml#/components/schemas/Game / contracts/satellite/games.yaml#/components/schemas/AttractionType)*
- **Integration protocol**: Read-only, from the reader model's protocol (BO-476); not set per game. *(source: screens/P08-venue-back-office.yaml#BO-447 / screens/P08-venue-back-office.yaml#BO-476)*
- **Redemption enabled, Credit source, Status**: Redemption enabled is a toggle per game; Credit source is the earn method chosen on BO-445 (shown, with a link, not chosen again here). Status is the game's status. *(source: screens/P08-venue-back-office.yaml#BO-447 / screens/P08-venue-back-office.yaml#BO-445)*

#### Outputs: what the screen shows and produces

**Shown**

**Every ticketless redemption game** (data table)

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**Redemption games** (data table, from `listGames`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Zone | text | — |
| Asset | the image or video | The machine. Taken out of service by maintenance, the game stops accepting play rather than swallowing credits. |
| Reader | the name it points at, never the id | — |
| Credit cost | 1,234 | — |
| Min points awarded | 1,234 | — |
| Max points awarded | 1,234 | — |
| Height requirement cm | 1,234 | — |
| Status | chip: In service, Out of service, Maintenance, Retired | — |
| Plays today | 1,234 | — |
| Credits taken today | 1,234 | — |
| Points awarded today | 1,234 | — |

**The selected ticketless redemption game** (detail panel): The pack groups this record's detail under its own headings: “Game Integration”, “Gameplay authorized”, “Game starts”, “Game completes”, “Game calculates win/score”, “Game sends redemption result”.

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Flow diagram**: Guest taps card, Play authorised, Game starts, Game completes, Game sends score, TICVAI validates, Credits added. Same visual language as BO-446's ticket flow. *(source: screens/P08-venue-back-office.yaml#BO-447 / screens/P08-venue-back-office.yaml#BO-448 / screens/P08-venue-back-office.yaml#BO-453)*
- **Validation checklist**: Five checks shown for the last result received: Authorised play, Correct game and play id, Not a duplicate, Card valid, Earn rule valid. Each green or red with the reason. *(source: screens/P08-venue-back-office.yaml#BO-448)*
- **Games list**: Columns Game, Reader, Credit source ("Score bands"), Results today, Credits awarded today, Last result. Games with redemption off are greyed, not hidden. *(source: contracts/satellite/games.yaml#/components/schemas/Game)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save**: Saves the shared redemption rules record (per VO-R14); ticketless games on/off is the venue switch at the top. *(source: contracts/satellite/games.yaml#setRedemptionRules)*
- **Send a test result**: Runs the reader test including the game-complete signal and shows whether a result would be accepted. *(source: contracts/satellite/games.yaml#testReader / contracts/satellite/games.yaml#/components/schemas/ReaderTestResult)*

**Data it reads**: `listGames` (onLoad, Redemption games and the points they award)

**Where the user goes next**

- → `BO-444` Redemption Operations Dashboard: *Back to Redemption Operations Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ticketless redemption game list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ticketless redemption game untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ticketless redemption game yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the ticketless redemption game are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A score arrives for a play TICVAI never authorised**: Rejected and listed on BO-453 as an exception ("Result without an authorised play"); no credits posted. *(source: screens/P08-venue-back-office.yaml#BO-448 / screens/P08-venue-back-office.yaml#BO-453)*
- **The same result is sent twice**: The play id is the idempotency key; the second is ignored and shown as a duplicate. *(source: contracts/satellite/games.yaml#/components/schemas/RecordPlayRequest)*
- **Result arrives after the reader was offline**: Credited with the original play time; shown as "Synced later" in the ledger. *(source: contracts/satellite/games.yaml#syncGamePlays / DI-065)*

#### Consistency with other screens

- Match `BO-446`: Twin screen; same layout and flow component.
- Match `BO-477`: The score arrives as the standard SCORE_RECEIVED event; the mapping from the vendor's event is set there.
- Match `BO-465`: The live feed shows credits earned on the play row (ticketsEarned).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
games:
- game: Basketball Pro
  reader: R-023
  source: Score bands
  resultsToday: 612
  creditsToday: 96400
- game: Laser Arena
  reader: R-040
  source: Score-based
  resultsToday: 288
  creditsToday: 51200
lastResult:
  game: Basketball Pro
  card: '****4321'
  score: 26
  credits: 200
  checks: All 5 passed
```

#### Permissions

- `setRedemptionRules` → `PRODUCT_CONFIGURE` (configure) · staff
- `listGames` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-447` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS63 Game and Ride Board 6.dc.html#bo-447`
- Workshop pack: Game_and_Ride_Module.pdf board 6
- Flow F192 *Game and Ride board 6: Redemption Operations Dashboard*, step 6: Works in Ticketless Redemption Game Integration → Configure games that automatically send redemption-credit results to TICVAI after gameplay. The source requires integration with redemption games to digitally load credits after the guest completes a …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-447?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-444`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-448` Redemption Wallet & Balance View

**Allow operators and systems to view the redemption-credit balance stored within a customer wallet. The source requires redemption credits stored in the wallet to be viewable from operator kiosks and self-service kiosks.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block C · task VM-BO-448 |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `subjectId` (navigation) |
| Route | `/games-rides/redemption-wallet-balance-view-bo-448` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The redemption-credit (prize points) balance in a guest wallet, for operators.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **redemption balance**: Points separate from money balances, never shown in AED. *(source: contracts/satellite/wallet.yaml#getWallet / DI-878)*

**Where the user goes next**

- → `BO-444` Redemption Operations Dashboard: *Back to Redemption Operations Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The redemption wallet balance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the redemption wallet balance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No redemption wallet balance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the redemption wallet balance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
wallet:
  holder: Omar Haddad
  redemptionPoints: 1240
```

#### Permissions

- `getWallet` → `WALLET_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.9 | Digital Wallet - System shall provide a digital wallet. | Guest Mobile App & Branding | CONTRACTED | `getWallet` |
| 1.1.105 | Stored value card management | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 1.1.108 | Balance enquiry | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 1.1.111 | Expiry management | Ticketing Catalogue | CONTRACTED | `getWallet` |
| 2.6.48 | System shall provide one unified wallet experience across website, mobile app, POS, kiosk, and membership channels. The wallet shall show stored value, vouchers, loyalty points, membership benefits … | Ticketing Sales | CONTRACTED | `getWallet` |
| 2.13.34 | Digital Wallet Integration | Ticketing Sales | CONTRACTED | `getWallet` |
| 4.3.7 | The system should allow guests to use their digital wallet to make online and in-app purchases (through API integrations), buy tickets of all type or purchase any service within venue such as retail … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.8 | The system should provide a digital wallet that allows: - multiple channels for payments, including but not limited to the Mobile app and wearable (which is linked to the digital wallet). - multiple … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.13 | The system should allow guests to make in-store and attraction payments using digital wallets via contactless methods as RFID, NFC and QR-code. | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.20 | The system should enable usage of wallet by other systems through integration. All functionalities of the wallet such as credit redemption, balance check and wallet funding should be available … | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.22 | Support cashless stored-value balances. | Bundles and Promotions | CONTRACTED | `getWallet` |
| 4.3.23 | Support gift card balances. | Bundles and Promotions | CONTRACTED | `getWallet` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-448` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS63 Game and Ride Board 6.dc.html#bo-448`
- Workshop pack: Game_and_Ride_Module.pdf board 6
- Flow F192 *Game and Ride board 6: Redemption Operations Dashboard*, step 8: Works in Redemption Wallet & Balance View → Allow operators and systems to view the redemption-credit balance stored within a customer wallet. The source requires redemption credits stored in the wallet to be viewable from operator kiosks and …
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-448?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-444`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-449` Redemption Counter / Prize Checkout

**Provide the operator interface used when a customer exchanges redemption credits for prizes. The source explicitly requires redemption-credit usage at a redemption counter for prizes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-449 |
| Who uses it | venue staff holding `ORDER_CREATE`, `PRODUCT_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Scan / Tap Customer Card; Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/redemption-counter-prize-checkout-bo-449` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-001): A counter attendant does not change earn rules; the binding gave a till a configuration write (design-notes correction venue-operations BO-449).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The prize counter: an attendant identifies the guest's card, builds a basket of prizes by scanning or searching, and completes the redemption, which deducts redemption credits and takes the prizes out of stock in one step. It is an operator till, used standing at a counter with children waiting, not a back-office table. The one thing to get right: nothing is handed over unless the server confirmed the deduction; the counter cannot complete offline.

**Known correction pending (do not draw the wrong version)**

- **Table and detail titled "Every redemption counter prize", with the sample "Redemption Balance 2,450" as a column** Why: Generated labels and a sample value used as a label; the screen is a counter basket (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-449; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No way to record the second approver** Why: RedemptionRules sets counterApprovalAboveTickets, but redeemPrize carries no approver, so the threshold cannot be enforced or audited. *(source: contracts/satellite/games.yaml#redeemPrize / contracts/satellite/games.yaml#/components/schemas/RedemptionRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Confirmation dialog on Remove Item** Why: Removing a basket line changes nothing on the server; an undo is faster at a busy counter (VO-R16 reserves confirmations for live, destructive actions). *(source: screens/P08-venue-back-office.yaml#BO-033; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): setRedemptionRules is bound to the counter (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should the counter be a P08 screen at all, or a till mode on the POS or Staff App where the counter workstation actually runs?** → Drawn default accepted: Draw it as a full-screen counter mode at tablet size inside P08, flagged for the lead. *(decided by Chinmay, 2026-10-02; DEC-415 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Card (cardCode)**: First step, full width: "Tap or scan the guest's card". Manual entry of the card number as fallback. Once read, the header shows masked card, guest first name, card status and Redemption balance "2,450 credits" in large type. *(source: screens/P08-venue-back-office.yaml#BO-449 / contracts/satellite/games.yaml#getGameCard)*
- **Prize (scan barcode)**: Scan adds one unit; matched on the prize's own barcode first, then the linked retail item's barcode or SKU. Scanning the same prize again increases its quantity rather than adding a line. *(source: contracts/satellite/games.yaml#lookupPrize)*
- **Prize (search)**: Search opens the prize wall grouped by tier (Small, Medium, Large, Jackpot) with image and credit cost; prizes the card can afford come first. Out-of-stock prizes stay visible, greyed, with "Out of stock". *(source: contracts/satellite/games.yaml#listPrizes / contracts/satellite/games.yaml#/components/schemas/Prize)*
- **Quantity**: Stepper per line, minimum 1; cannot exceed stock on hand (shown "8 in stock"). *(source: contracts/satellite/games.yaml#redeemPrize / contracts/satellite/games.yaml#/components/schemas/Prize)*

#### Outputs: what the screen shows and produces

**Shown**

**Every redemption counter prize** (data table)

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |
| Redemption balance: 2,450 | text | not in the schema: `Redemption Balance: 2,450` |

**The selected redemption counter prize** (detail panel): The pack groups this record's detail under its own headings: “Football 1 1,000”, “Before completing”, “REDEMPTION APPROVED”.

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |
| Redemption balance: 2,450 | text | not in the schema: `Redemption Balance: 2,450` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Scan Prize Barcode (primary button) | `lookupPrize` GET `/prizes/lookup` | — | Prize | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Search Prize (secondary button) | `lookupPrize` GET `/prizes/lookup` | — | Prize | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Change Quantity (secondary button) | navigation or local | — | — | — | — |
| Remove Item (destructive button) | navigation or local | — | — | — | — |
| Complete Redemption (secondary button) | navigation or local | — | — | — | — |
| Cancel Transaction (destructive button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Basket**: Columns Prize, Qty, Credit cost, Line total; footer "Total 1,800 credits / Remaining 650". When the total exceeds the balance the footer turns red with "Short by 350 credits" and Complete is disabled. *(source: screens/P08-venue-back-office.yaml#BO-449)*
- **Pre-completion checks**: The pack's six checks as a compact checklist above Complete: Card active, Enough credits, In stock, Prize active, This venue, Rule valid. All green enables Complete. *(source: screens/P08-venue-back-office.yaml#BO-450)*
- **Result**: "REDEMPTION APPROVED / Credits deducted 1,800 / Remaining balance 650" with the redemption number, then the card clears for the next guest. *(source: screens/P08-venue-back-office.yaml#BO-450 / contracts/satellite/games.yaml#/components/schemas/PrizeRedemption)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Complete redemption**: Sends the basket once with an id generated when the basket was started; a retry after a timeout reuses the same id so credits are never deducted twice. On 409 the problem names the shortfall or the out-of-stock lines, which are highlighted in the basket for the attendant to fix. *(source: contracts/satellite/games.yaml#redeemPrize / contracts/satellite/games.yaml#/components/schemas/PrizeConflictProblem)*
- **Remove item**: Removes the line immediately with an Undo for a few seconds; nothing has been sent, so no confirmation dialog. *(source: designer default)*
- **Cancel transaction**: Clears card and basket; confirms only when the basket has lines ("Discard 2 prizes?"). Nothing is deducted. *(source: screens/P08-venue-back-office.yaml#BO-450)*

**Where the user goes next**

- → `BO-444` Redemption Operations Dashboard: *Back to Redemption Operations Dashboard*

**What opens over it**

- confirmDialog *Remove Item*: **Remove Item on a redemption counter prize is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.
- confirmDialog *Cancel Transaction*: **Cancel Transaction on a redemption counter prize is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The redemption counter prize list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the redemption counter prize untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No redemption counter prize yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the redemption counter prize are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Insufficient points, or a prize is out of stock (PrizeConflictProblem) |

#### Edge cases to draw

- **No connection**: Card read and prize lookup still work (offline-capable), Complete is disabled with "Redemption needs a connection; stock changes in real time". Never hand over on an offline basket. *(source: contracts/satellite/games.yaml#redeemPrize / contracts/satellite/games.yaml#lookupPrize)*
- **Basket total above the second-person threshold**: Complete asks for a second staff member to sign in and approve, naming the threshold ("Prizes above 10,000 credits need a supervisor"). *(source: contracts/satellite/games.yaml#/components/schemas/RedemptionRules)*
- **Another counter takes the last unit while this basket is open**: The 409 marks the line "Only 0 left"; the attendant removes it or swaps the prize. *(source: contracts/satellite/games.yaml#/components/schemas/PrizeConflictProblem)*
- **Card blocked, expired or replaced**: Stop at the card step with the status and next action ("This card was replaced by ****9875; tap the new card"). *(source: contracts/satellite/games.yaml#/components/schemas/GameCard)*

#### Consistency with other screens

- Match `BO-491`: The guest's prize discovery shows the same prizes, tiers and stock indicators; the counter is where they are actually redeemed.
- Match `BO-445`: The second-person threshold comes from the redemption settings there.
- Match `BO-453`: Every completed basket appears in the redemption ledger with its inventory movement ids.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
card:
  card: '****4321'
  guest: Sara Al Nuaimi
  balance: 2450
basket:
- prize: Teddy Bear
  qty: 1
  cost: 800
- prize: Football
  qty: 1
  cost: 1000
totals:
  total: 1800
  remaining: 650
  redemptionNumber: RED-0220
```

#### Permissions

- `listPrizes` → `PRODUCT_VIEW` (read) · staff
- `redeemPrize` → `ORDER_CREATE` (operate) · staff
- `lookupPrize` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Redemption points earned per game (score or level) are redeemed for prizes at a counter; per-game config of points granted or required (e.g. 200 points to play using redemption credit). *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-878)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-449` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS63 Game and Ride Board 6.dc.html#bo-449`
- Workshop pack: Game_and_Ride_Module.pdf board 6
- Flow F192 *Game and Ride board 6: Redemption Operations Dashboard*, step 10: Works in Redemption Counter / Prize Checkout → Provide the operator interface used when a customer exchanges redemption credits for prizes. The source explicitly requires redemption-credit usage at a redemption counter for prizes.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-449?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Scan Prize Barcode, Search Prize, Change Quantity, Remove Item, Complete Redemption, Cancel Transaction.
- [ ] Every transition is wired: `BO-444`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-450` Prize Catalogue & Credit Cost Configuration

**Configure the prize catalogue and how many redemption credits each prize requires.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-450 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `prizeId` (navigation) |
| Route | `/games-rides/prize-catalogue-credit-cost-configuration-bo-450` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): The catalogue configures prizes; handing one over (redeemPrize) belongs to the counter BO-449. The catalogue's writes are createPrize and setPrizeCost …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The prize catalogue: what prizes exist, what they cost in redemption credits, what they cost the venue, and whether they are active. The prize manager adds prizes, sets their credit cost and links each one to the stock item it draws from. The one thing to get right: credit cost and unit cost sit side by side with the margin, because the ratio between them is the only control on a redemption arcade's margin.

**Known correction pending (do not draw the wrong version)**

- **A primary button and a data table with empty labels** Why: Generated placeholders; the screen needs "Prize catalogue" and "Add prize". *(source: screens/P08-venue-back-office.yaml#BO-450; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Two credit costs and two stock sources** Why: Prize.pointCost and PrizeCost.ticketPrice both hold the credit cost; Prize.onHand holds a stock count while PrizeCost says stock comes from inventory. Each needs one owner. *(source: contracts/satellite/games.yaml#/components/schemas/Prize / contracts/satellite/games.yaml#/components/schemas/PrizeCost; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): redeemPrize is bound to the catalogue (CHG-WIR-001); No update, activate or deactivate operation (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the minimum customer level a membership tier, a loyalty level or an age?** → Drawn default accepted: Greyed select labelled "Minimum level (optional)". *(decided by Chinmay, 2026-10-02; DEC-416 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Max points | number field | — | — | `listPrizes` ?maxPoints |

**Form: Add prize** (modal, opened by *Add prize*; *Add prize* calls `createPrize`, *Cancel* sends nothing)

**Collects what `createPrize` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createPrize` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createPrize` body |
| Description `description` | text area | optional | — | — | — | — | `createPrize` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createPrize` body |
| Merchandise `merchandiseId` | picker: choose a merchandise | optional | — | — | shows names, sends the id | Links to retail. Redemption depletes stock through the inventory ledger — a prize wall running out is a stock problem and should look like one. | `createPrize` body |
| Point cost `pointCost` | number field | required | — | min 1 | — | — | `createPrize` body |
| On hand `onHand` | number field | required | — | — | — | — | `createPrize` body |
| Is available `isAvailable` | toggle | optional | — | — | — | — | `createPrize` body |
| Tier `tier` | text field | optional | — | — | — | Small, medium, large, jackpot. Drives prize-wall layout. | `createPrize` body |
| Image `imageAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `createPrize` body |
| Barcode `barcode` | text field | optional | — | max length 64 | — | The prize's own barcode, read by `lookupPrize` before the linked retail item's barcode or SKU. | `createPrize` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `createPrize` body |

**Form: Set credit cost** (modal, opened by *Set credit cost*; *Set credit cost* calls `setPrizeCost`, *Cancel* sends nothing)

**Collects what `setPrizeCost` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Prize `prizeId` | picker: choose a prize | optional | — | — | shows names, sends the id | — | `setPrizeCost` body |
| Ticket price `ticketPrice` | number field | optional | — | — | — | — | `setPrizeCost` body |
| Unit cost `unitCost` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setPrizeCost` body |
| Inventory item `inventoryItemId` | picker: choose an inventory item | optional | — | — | shows names, sends the id | Stock comes from `inventory`. A prize catalogue with its own count is one that disagrees with the stockroom. | `setPrizeCost` body |
| Direct pay price `directPayPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setPrizeCost` body |
| Display tier `displayTier` | text field | optional | — | — | — | — | `setPrizeCost` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setPrizeCost` body |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Prize name, description, category, image**: Name required (max 200, Arabic variant per VO-R10); category is the tier (Small, Medium, Large, Jackpot) that lays out the prize wall, a select not free text; image from the asset library. *(source: contracts/satellite/games.yaml#/components/schemas/Prize)*
- **Prize ID**: Not an input (per VO-R03); shown read-only after creation. *(source: contracts/spine/access.yaml#setJourneySequenceRule)*
- **SKU, barcode, inventory location**: Barcode is the prize's own (max 64, unique in the venue; duplicate shown against the field). SKU and inventory location come from the linked stock item and are shown read-only once linked. *(source: contracts/satellite/games.yaml#/components/schemas/Prize / contracts/satellite/games.yaml#/components/schemas/PrizeCost)*
- **Credit cost, unit cost**: Credit cost is a whole number of redemption credits, minimum 1. Unit cost is AED with two decimals. Margin is calculated and read-only ("Margin 38%"). *(source: contracts/satellite/games.yaml#/components/schemas/PrizeCost)*
- **Promotional cost, effective dates, venue-specific cost, minimum customer level**: Draw greyed under "Promotions and limits" (per VO-R13); the records hold none of them. *(source: screens/P08-venue-back-office.yaml#BO-451)*
- **Direct-pay price**: Shown only when the prize is dispensed by a crane or prize machine (BO-452); AED. *(source: contracts/satellite/games.yaml#/components/schemas/PrizeCost)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add prize (secondary button) | `createPrize` POST `/prizes` | Prize | Prize | — | opens modal first |
| Set credit cost (secondary button) | `setPrizeCost` PUT `/prizes/{prizeId}/cost` | PrizeCost | PrizeCost | — | opens modal first; produces a document or message: What a prize costs in tickets, and what it costs the venue |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Catalogue table**: Columns Image, Prize, Category, Credit cost, Unit cost, Margin, In stock, Status. Sort by credit cost. Inactive prizes shown greyed; out-of-stock prizes keep their row. *(source: screens/P08-venue-back-office.yaml#BO-450 / contracts/satellite/games.yaml#listPrizes)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Add prize**: Opens the editor empty; Save creates the prize then its cost record. The venue is the one in the top bar. *(source: contracts/satellite/games.yaml#createPrize / contracts/satellite/games.yaml#setPrizeCost)*
- **Edit, Clone, Activate, Deactivate**: Clone opens a new prize pre-filled with "(copy)" and no barcode. Deactivate confirms with the effect ("Teddy Bear disappears from the counter search and the guest prize wall"). *(source: screens/P08-venue-back-office.yaml#BO-451)*

**Data it reads**: `listPrizes` (onLoad, The prize catalogue)

**Where the user goes next**

- → `BO-444` Redemption Operations Dashboard: *Back to Redemption Operations Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The prize catalogue credit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the prize catalogue credit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No prize catalogue credit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the prize catalogue credit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Deactivating a prize that sits in an open counter basket**: The counter's completion fails the "Prize active" check and the attendant removes it. *(source: screens/P08-venue-back-office.yaml#BO-450)*
- **Credit cost raised**: Applies to the next basket; baskets already completed keep the cost they were redeemed at. *(source: contracts/satellite/games.yaml#/components/schemas/PrizeRedemption)*

#### Consistency with other screens

- Match `BO-451`: The stock link and stock figures are the same on both screens.
- Match `BO-491`: Image, name, category and cost are what the guest sees on the kiosk prize wall.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
prizes:
- prize: Keychain
  category: Small
  credits: 150
  unitCost: AED 2.50
  stock: 240
- prize: Plush Toy
  category: Medium
  credits: 800
  unitCost: AED 12.00
  stock: 25
- prize: Football
  category: Medium
  credits: 1000
  unitCost: AED 18.00
  stock: 8
- prize: Headphones
  category: Large
  credits: 3500
  unitCost: AED 65.00
  stock: 0
- prize: Gaming Console
  category: Jackpot
  credits: 25000
  unitCost: AED 1,450.00
  stock: 2
```

#### Permissions

- `listPrizes` → `PRODUCT_VIEW` (read) · staff
- `createPrize` → `PRODUCT_CONFIGURE` (configure) · staff
- `setPrizeCost` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Redemption points earned per game (score or level) are redeemed for prizes at a counter; per-game config of points granted or required (e.g. 200 points to play using redemption credit). *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-878)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-450` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS63 Game and Ride Board 6.dc.html#bo-450`
- Workshop pack: Game_and_Ride_Module.pdf board 6
- Flow F192 *Game and Ride board 6: Redemption Operations Dashboard*, step 12: Works in Prize Catalogue & Credit Cost Configuration → Configure the prize catalogue and how many redemption credits each prize requires.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-450?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add prize, Set credit cost.
- [ ] Every transition is wired: `BO-444`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-451` Prize Inventory Integration

**Connect prize redemption directly with TICVAI inventory so redemption transactions reduce stock in real time. The source explicitly requires prizes at the redemption counter, skill games and direct-pay machines such as cranes to be integrated with the inventory system.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-451 |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `prizeId` (navigation) |
| Route | `/games-rides/prize-inventory-integration-bo-451` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Shows that every prize redeemed or dispensed takes a unit out of stock, and where stock is getting low, across the counter, skill-game prizes, direct-pay machines and cranes. Stock lives in inventory; this screen links prizes to stock items and shows the stock position, it does not keep its own count. The one thing to get right: low and out-of-stock prizes are obvious at a glance, and the policy for "inventory unavailable" is explicit.

**Known correction pending (do not draw the wrong version)**

- **Two links from a prize to stock** Why: Prize.merchandiseId links to a retail item and PrizeCost.inventoryItemId links to an inventory item; one prize needs one stock link. *(source: contracts/satellite/games.yaml#/components/schemas/Prize / contracts/satellite/games.yaml#/components/schemas/PrizeCost; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Entry parameter prizeId with no carrier** Why: The screen is reached from the redemption dashboard, which carries nothing; it is a list, not a single prize. *(source: screens/P08-venue-back-office.yaml#BO-451; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): The screen has only a "Redemption Counter" button and Cancel (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **If inventory is unreachable, does the counter block redemption or allow it and reconcile later?** → Drawn default accepted: Block, as drawn above. *(decided by Chinmay, 2026-10-02; DEC-417 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Location | picker: choose a location | — | — | `getStockPositions` ?locationId |
| Item | picker: choose an item | — | — | `getStockPositions` ?itemId |
| Include zero | toggle | off | — | `getStockPositions` ?includeZero |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Linked stock item**: Per prize, a picker of inventory items (name, SKU, location); one stock item per prize. *(source: contracts/satellite/games.yaml#/components/schemas/PrizeCost)*
- **Reorder level**: Shown from the stock item, not edited here; links to the inventory screen that owns it. *(source: screens/P08-venue-back-office.yaml#BO-451)*
- **When inventory is unavailable**: A closed choice the pack leaves to policy: Block redemption, or Allow and reconcile later. Draw greyed with Block selected until a field exists. *(source: screens/P08-venue-back-office.yaml#BO-452)*

#### Outputs: what the screen shows and produces

**Shown**

**Prize stock** (data table, from `getStockPositions`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Item | the name it points at, never the id | — |
| Item name | text | — |
| SKU | text | — |
| Location | the name it points at, never the id | — |
| Location name | text | — |
| On hand | 1,234.5 | — |
| Allocated | 1,234.5 | Reserved for orders: the quantity under an active stock reservation for an order (decided 28 September, audit R171). |
| Available | 1,234.5 | On-hand minus allocated (decided 28 September, audit R171). What can still be sold or issued. |
| Unit | text | — |
| Value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Last counted at | 1 Oct 2026, 14:30 | — |
| Last movement at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Redemption Counter (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Stock table**: Columns Prize, Available, Reserved, Reorder level, Status, Dispensed by (Counter / Crane / Skill game / Direct pay). Status words Healthy (green), Low (amber, at or below reorder level), Out of stock (red). Out-of-stock and low first. *(source: screens/P08-venue-back-office.yaml#BO-451 / screens/P08-venue-back-office.yaml#BO-452)*
- **Integration rule strip**: Prize redeemed, Stock minus 1, Stock updated, Low-stock check, Alert or reorder. Drawn as a small flow above the table. *(source: screens/P08-venue-back-office.yaml#BO-451)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Link stock item**: Saves the prize's stock link with its cost record (whole record, per VO-R04). *(source: contracts/satellite/games.yaml#setPrizeCost)*
- **View stock movements**: Opens the inventory movement history for the linked item, filtered to redemptions. *(source: contracts/satellite/inventory.yaml#listStockMovements)*

**Data it reads**: `getStockPositions` (onLoad, Prize stock on hand by item and location)

**Where the user goes next**

- → `BO-444` Redemption Operations Dashboard: *Back to Redemption Operations Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The prize inventory integration list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the prize inventory integration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No prize inventory integration yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the prize inventory integration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A crane dispenses a prize while its stock shows zero**: The machine already gave the prize; the movement posts and the stock shows negative with a red "Count needed" flag, never silently zero. *(source: screens/P08-venue-back-office.yaml#BO-452 / designer default)*
- **A prize not linked to any stock item**: Row shows "Not linked; stock not tracked" in amber, and the counter treats it per the unavailable-inventory policy. *(source: contracts/satellite/games.yaml#/components/schemas/PrizeCost)*

#### Consistency with other screens

- Match `BO-141`: Low-stock alerts for prizes surface in the operational alerts centre that absorbed the games alert board (BO-472, R276).
- Match `BO-450`: Same prize identity and stock link.
- Match `BO-452`: Crane and prize machines name their linked prize there; their dispenses reduce the same stock.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
stock:
- prize: Plush Toy
  available: 25
  reserved: 2
  reorder: 10
  status: Healthy
  dispensedBy: Counter, Premium Crane 01
- prize: Football
  available: 8
  reserved: 0
  reorder: 10
  status: Low
  dispensedBy: Counter
- prize: Headphones
  available: 0
  reserved: 0
  reorder: 5
  status: Out of stock
  dispensedBy: Counter
```

#### Permissions

- `setPrizeCost` → `PRODUCT_CONFIGURE` (configure) · staff
- `createPrize` → `PRODUCT_CONFIGURE` (configure) · staff
- `getStockPositions` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-451` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS63 Game and Ride Board 6.dc.html#bo-451`
- Workshop pack: Game_and_Ride_Module.pdf board 6
- Flow F192 *Game and Ride board 6: Redemption Operations Dashboard*, step 14: Works in Prize Inventory Integration → Connect prize redemption directly with TICVAI inventory so redemption transactions reduce stock in real time. The source explicitly requires prizes at the redemption counter, skill games and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-451?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Redemption Counter, Cancel.
- [ ] Every transition is wired: `BO-444`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-452` Direct-Pay / Crane & Prize Machine Configuration

**Configure prize machines such as cranes or other direct-pay devices that may consume wallet value and dispense inventory items. The matrix specifically references skill games and direct pay machines (e.g., cranes) as part of the inventory integration requirement.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-452 |
| Who uses it | venue staff holding `DEVICE_VIEW`, `PRICE_CONFIGURE`, `PRODUCT_VIEW` (2 read, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/direct-pay-crane-prize-machine-configuration-bo-452` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Configuration of direct-pay prize machines (cranes and similar), which take wallet value and dispense prizes from stock. It belongs to Games & Rides (route, module and entry from the Redemption Operations Dashboard all say so). Its only inventory part is the prize stock at the machine. The one thing to get right is that a machine whose prize is at zero must not complete a play.

**Known correction pending (do not draw the wrong version)**

- **The screen is grouped under Inventory & Procurement in the handoff. Its own definition is module Games & Rides, route /games-rides, entered from the Redemption Operations Dashboard (BO-444).** Why: The placement in Inventory is wrong. Inventory supplies only the prize stock. Machine setup, wallet price and reader are games configuration. *(source: screens/P08-venue-back-office.yaml#BO-452; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): The only operation is the stock read. Machine id, name, type, play price and reader are labels with no data behind them. (CHG-WIR-008).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Inventory location | select field | — | — | — | — | Sends `?locationId=`; the machine's prize location. | — |
| Linked prize / SKU | select field | — | — | — | — | Sends `?itemId=`. | — |
| Include out-of-stock prizes | toggle | — | — | — | — | Sends `?includeZero=true`; a machine whose prize is at zero must not complete redemption. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Location | picker: choose a location | — | — | `getStockPositions` ?locationId |
| Item | picker: choose an item | — | — | `getStockPositions` ?itemId |
| Include zero | toggle | off | — | `getStockPositions` ?includeZero |
| Status | radio group | — | In service · Out of service · Maintenance · Retired | `listGames` ?status |
| Status | radio group | — | Unconfigured · Active · Offline · Maintenance · Disabled | `listReaders` ?status |

**Form: Save play price** (modal, opened by *Save play price*; *Save play price* calls `setGamePricing`, *Cancel* sends nothing)

**Collects what `setGamePricing` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Game `gameId` | picker: choose a game | optional | — | — | shows names, sends the id | — | `setGamePricing` body |
| Standard price `standardPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setGamePricing` body |
| Vip price `vipPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setGamePricing` body |
| Group pricing `groupPricing` | repeatable rows | optional | — | — | — | — | `setGamePricing` body |
| Minimum players `groupPricing[].minimumPlayers` | number field | optional | — | — | — | — | `setGamePricing` body |
| Price per player `groupPricing[].pricePerPlayer` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setGamePricing` body |
| Peak pricing `peakPricing` | repeatable rows | optional | — | — | — | — | `setGamePricing` body |
| Days of week `peakPricing[].daysOfWeek` | list of values (chips) | optional | — | — | — | — | `setGamePricing` body |
| From `peakPricing[].from` | text field | optional | — | — | — | — | `setGamePricing` body |
| To `peakPricing[].to` | text field | optional | — | — | — | — | `setGamePricing` body |
| Price `peakPricing[].price` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setGamePricing` body |
| Calendar exceptions `calendarExceptions` | repeatable rows | optional | — | — | — | — | `setGamePricing` body |
| Date `calendarExceptions[].date` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setGamePricing` body |
| Price `calendarExceptions[].price` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setGamePricing` body |
| Closed `calendarExceptions[].closed` | toggle | optional | off | — | — | — | `setGamePricing` body |
| Retry price `retryPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setGamePricing` body |
| Retry window seconds `retryWindowSeconds` | number field (seconds) | optional | — | — | — | How long after the game ends the retry offer stays open. | `setGamePricing` body |
| Retry offer lead seconds `retryOfferLeadSeconds` | number field (seconds) | optional | — | min 0 | — | When the retry offer appears (Chinmay, 2 October, workbook Q410, default accepted; DI-877; CHG-CSA-028): this many seconds before the game ends, and it stays open … | `setGamePricing` body |
| Priority `priority` | multi-select chips | optional | — | Calendar exception · Peak · Group · Vip · Retry · Standard | — | — | `setGamePricing` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setGamePricing` body |

#### Outputs: what the screen shows and produces

**Shown**

**Prize machines and their stock** (data table, from `getStockPositions`): Only stock is bound. No operation lists machines, so the machine columns are pack labels.

| Shows | Format | Notes |
|---|---|---|
| Machine ID | text | not in the schema: `Machine ID` |
| Machine name | text | not in the schema: `Machine name` |
| Machine type | text | not in the schema: `Machine type` |
| Item name | text | — |
| SKU | text | — |
| Location name | text | — |
| Available | 1,234.5 | On-hand minus allocated (decided 28 September, audit R171). What can still be sold or issued. |
| On hand | 1,234.5 | — |
| Allocated | 1,234.5 | Reserved for orders: the quantity under an active stock reservation for an order (decided 28 September, audit R171). |
| Last movement at | 1 Oct 2026, 14:30 | — |
| Play price | text | not in the schema: `Play price` |
| Machine status | text | not in the schema: `Machine status` |

**Machines** (data table, from `listGames`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Zone | text | — |
| Asset | the image or video | The machine. Taken out of service by maintenance, the game stops accepting play rather than swallowing credits. |
| Reader | the name it points at, never the id | — |
| Credit cost | 1,234 | — |
| Min points awarded | 1,234 | — |
| Max points awarded | 1,234 | — |
| Height requirement cm | 1,234 | — |
| Status | chip: In service, Out of service, Maintenance, Retired | — |
| Plays today | 1,234 | — |
| Credits taken today | 1,234 | — |
| Points awarded today | 1,234 | — |

**Readers** (data table, from `listReaders`)

| Shows | Format | Notes |
|---|---|---|
| Device | the name it points at, never the id | `tenancy.RegisteredDevice`. Enrolment, firmware and tamper state live there. |
| Game | the name it points at, never the id | — |
| Reader profile | the name it points at, never the id | — |
| Accepted credit types | list or chips (count when long) | — |
| Accepts direct pay | yes / no (icon or chip) | — |
| Retap delay seconds | 1,234 | The setting that stops a guest paying twice for one go. A wristband held against a reader for a second and a half is two taps to the … |
| Display rules | grouped details | — |
| Free game glow | yes / no (icon or chip) | What tells a guest their entitlement was used rather than their money. Without it the complaint arrives at the desk. |
| Show balance | yes / no (icon or chip) | — |
| Show price | yes / no (icon or chip) | — |
| Theme code | text | — |
| Languages | list or chips (count when long) | — |
| Io mapping | grouped details | Board 9.6. Which output starts the game, which input reports it finished. |
| Status | chip: Unconfigured, Active, Offline, Maintenance, Disabled | — |

**The selected machine profile** (detail panel, from `getStockPositions`): The pack's Machine Profile; current stock is `available`.

| Shows | Format | Notes |
|---|---|---|
| Machine ID | text | not in the schema: `Machine ID` |
| Machine name | text | not in the schema: `Machine name` |
| Machine type | text | not in the schema: `Machine type` |
| Venue | text | not in the schema: `Venue` |
| Zone | text | not in the schema: `Zone` |
| Reader | text | not in the schema: `Reader` |
| Item name | text | — |
| SKU | text | — |
| Location name | text | — |
| Available | 1,234.5 | On-hand minus allocated (decided 28 September, audit R171). What can still be sold or issued. |
| Unit | text | — |
| Value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Last counted at | 1 Oct 2026, 14:30 | — |
| Play price | text | not in the schema: `Play price` |
| Machine status | text | not in the schema: `Machine status` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save play price (secondary button) | `setGamePricing` PUT `/game-pricing` | GamePricing | GamePricing | — | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Machines with their prize stock**: Machine name, type, zone, play price (AED), linked prize, prize available at the machine's location, status. *(source: screens/P08-venue-back-office.yaml#BO-452 / contracts/satellite/inventory.yaml#getStockPositions)*

**Data it reads**: `getStockPositions` (onLoad, Prize stock); `listGames` (onLoad, The prize machines); `listReaders` (onLoad, The readers on each machine)

**Where the user goes next**

- → `BO-444` Redemption Operations Dashboard: *Back to Redemption Operations Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The direct-pay crane prize list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the direct-pay crane prize untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No direct-pay crane prize yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the direct-pay crane prize are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- machine: Crane 03 – Plush Party
  zone: Arcade Hall
  playPrice: AED 10.00
  prize: Plush dolphin 30 cm
  available: 41
  status: Active
```

#### Permissions

- `getStockPositions` → `PRODUCT_VIEW` (read) · staff
- `listGames` → `PRODUCT_VIEW` (read) · staff
- `listReaders` → `DEVICE_VIEW` (read) · staff
- `setGamePricing` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

13 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 1 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-452` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS63 Game and Ride Board 6.dc.html#bo-452`
- Workshop pack: Game_and_Ride_Module.pdf board 6
- Flow F192 *Game and Ride board 6: Redemption Operations Dashboard*, step 16: Works in Direct-Pay / Crane & Prize Machine Configuration → Configure prize machines such as cranes or other direct-pay devices that may consume wallet value and dispense inventory items. The matrix specifically references skill games and direct pay machines …

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state.
- [ ] Every output is drawn (56 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-452?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save play price.
- [ ] Every transition is wired: `BO-444`.
- [ ] Every gated control is gated: `DEVICE_VIEW`, `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-453` Redemption Transaction Ledger, Reconciliation & Audit

**Provide complete traceability of redemption credits earned, redeemed, adjusted and associated inventory movements.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block D · task VM-BO-453 |
| Who uses it | venue staff holding `PRODUCT_VIEW`, `WALLET_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Compare; Redemption Counter / Prize Machine) and no metric row |
| Offline | online only |
| Opens with | `subjectId` (navigation) |
| Route | `/games-rides/redemption-transaction-ledger-reconciliation-audit-bo-453` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-001): A ledger needs reads of plays with credits earned and of card movements; setPrizeCost is a configuration write, and the ledger is entered from the dashboard with … Contract gap recorded 2 October 2026 (CHG-WIR-004): No read lists prize redemptions.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The redemption ledger: every credit earned (ticket-eater, ticketless game), every credit spent at the counter, every adjustment, with the stock movement it caused, and a reconciliation of what machines reported against what TICVAI posted. Finance and the arcade manager use it to answer "where did these credits come from" and "why do the numbers disagree". The one thing to get right: reconciliation is a comparison with a variance you can click, not one more table of columns.

**Known correction pending (do not draw the wrong version)**

- **The table's columns are the reconciliation sources plus "versus"** Why: The generator turned the pack's comparison list into columns; ledger and reconciliation are two different parts. *(source: screens/P08-venue-back-office.yaml#BO-453; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): setPrizeCost is the only operation bound (CHG-WIR-001); Entry parameter prizeId (CHG-WIR-001).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listGameplayTransactions` ?from |
| Reader | picker: choose a reader | — | — | `listGameplayTransactions` ?readerId |
| Outcome | segmented control | — | Allowed · Refused · Reversed | `listGameplayTransactions` ?outcome |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Filters**: Card, Source (Ticket-eater, Ticketless game, Prize counter, Adjustment), Game or machine, Date range (default today), Status. Card filter accepts a masked or full card number. *(source: screens/P08-venue-back-office.yaml#BO-453)*

#### Outputs: what the screen shows and produces

**Shown**

**Every redemption transaction ledger** (data table)

| Shows | Format | Notes |
|---|---|---|
| Game reported credits | text | not in the schema: `Game-reported credits` |
| TICVAI posted credits | text | not in the schema: `TICVAI-posted credits` |
| Ticket eater counts | text | not in the schema: `Ticket-eater counts` |
| Wallet balance movements | text | not in the schema: `Wallet balance movements` |
| Prize transactions | text | not in the schema: `Prize transactions` |
| Inventory deductions | text | not in the schema: `Inventory deductions` |
| Versus | text | not in the schema: `versus` |

**Credits earned** (data table, from `listGameplayTransactions`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Reader | the name it points at, never the id | — |
| Game | the name it points at, never the id | — |
| Card | the name it points at, never the id | — |
| At | 1 Oct 2026, 14:30 | — |
| Outcome | chip: Allowed, Refused, Reversed | — |
| Reason | text | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Charged from | text | — |
| Entitlement | the name it points at, never the id | — |
| Tickets earned | 1,234 | — |
| Decided offline | yes / no (icon or chip) | — |
| Synced at | 1 Oct 2026, 14:30 | — |

**Card movements** (data table, from `listWalletTransactions`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | text | — |
| Wallet | the name it points at, never the id | The wallet this movement is on (SD-027, 29 September). A shared wallet has many subjects, so the subject alone cannot say which balance … |
| Wallet hold | the name it points at, never the id | The hold a spend settled, where it came through `holdWalletFunds`. |
| Kind | chip: Top up, Spend, Refund, Adjustment, Bonus, Expiry… | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Balance after | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Order | text | — |
| Venue | the name it points at, never the id | — |
| Reason | text | — |
| Principal | the name it points at, never the id | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**The selected redemption transaction ledger** (detail panel): The pack groups this record's detail under its own headings: “Transaction Ledger”, “Transaction Details”, “Exceptions”, “Page 62 of 105”, “Critical architecture for Board 6”, “Ticket-Eater”.

| Shows | Format | Notes |
|---|---|---|
| Game reported credits | text | not in the schema: `Game-reported credits` |
| TICVAI posted credits | text | not in the schema: `TICVAI-posted credits` |
| Ticket eater counts | text | not in the schema: `Ticket-eater counts` |
| Wallet balance movements | text | not in the schema: `Wallet balance movements` |
| Prize transactions | text | not in the schema: `Prize transactions` |
| Inventory deductions | text | not in the schema: `Inventory deductions` |
| Versus | text | not in the schema: `versus` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Ledger**: Columns Time, Transaction, Source, Earned, Redeemed, Status; the running Balance column appears only when one card is filtered (a running balance across cards means nothing). Earned in green "+1,200", redeemed "-800". Cursor paging (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-453)*
- **Transaction detail**: The pack's fields: transaction id, card (masked), game or machine, credits before, earned or spent, after, prize, inventory transaction id (link), device, operator, time, status. *(source: screens/P08-venue-back-office.yaml#BO-453)*
- **Reconciliation**: Three comparison strips for the chosen day: Game-reported vs Posted credits, Ticket-eater counts vs Posted credits, Prizes redeemed vs Inventory deductions. Each shows both totals and a variance chip; clicking the variance lists the exceptions behind it. *(source: screens/P08-venue-back-office.yaml#BO-453)*
- **Exceptions**: Closed list with counts - Duplicate credit award, Missing wallet posting, Inventory mismatch, Machine count mismatch, Failed redemption, Reversed transaction. *(source: screens/P08-venue-back-office.yaml#BO-453)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Investigate**: Opens the transaction with its device events and the matching wallet and stock movements side by side. *(source: screens/P08-venue-back-office.yaml#BO-453)*
- **Reconcile**: Marks an exception reviewed with a reason; any credit correction is made as a card adjustment by a person, never automatically. *(source: contracts/satellite/wallet.yaml#adjustGameCard)*
- **Export**: CSV of the filtered ledger with the same columns. *(source: screens/P08-venue-back-office.yaml#BO-453)*
- **View wallet, View inventory transaction**: Deep links to the card profile (BO-455) and the stock movement. *(source: screens/P08-venue-back-office.yaml#BO-453)*

**Data it reads**: `listGameplayTransactions` (onLoad, Plays and the redemption credits they earned)

**Where the user goes next**

- → `BO-444` Redemption Operations Dashboard: *Back to Redemption Operations Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The redemption transaction ledger list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the redemption transaction ledger untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No redemption transaction ledger yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the redemption transaction ledger are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Plays recorded offline arrive hours later**: They appear at their original time with a "Synced 14:05" tag, so yesterday's reconciliation can change; the strip says "Includes 12 late records". *(source: DI-065 / contracts/satellite/games.yaml#syncGamePlays)*
- **Anomaly detection flags a machine paying out above its rule**: Shown as a suggestion with its reason; a person decides (per VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-453)*

#### Consistency with other screens

- Match `BO-473`: Same reconciliation strip component as the gameplay reconciliation (authorised vs deducted vs started).
- Match `BO-423`: The wallet credit ledger shows money; this ledger shows redemption credits. Keep the two units visibly different (AED vs credits).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
ledger:
- time: '10:00'
  tx: TKT-001
  source: Ticket Eater TE-01
  earned: 1200
  redeemed: null
  balance: 1200
- time: '10:30'
  tx: GAME-101
  source: Basketball Pro
  earned: 200
  redeemed: null
  balance: 1400
- time: '11:15'
  tx: RED-220
  source: Prize Counter (Maria Santos)
  earned: null
  redeemed: 800
  balance: 600
reconciliation:
  gameReported: 96600
  posted: 96400
  variance: 200
  cause: 1 award above the rule maximum, capped
```

#### Permissions

- `listGameplayTransactions` → `PRODUCT_VIEW` (read) · staff
- `listWalletTransactions` → `WALLET_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.112 | Transaction history | Ticketing Catalogue | CONTRACTED | `listWalletTransactions` |
| 5.3.17 | Maintain guest wallet balances, top-ups, spending history, refunds, transfers, expirations, and transaction history. | F&B & Guest Management | CONTRACTED | `listWalletTransactions` |
| 22.2.14 | Wallet History | Marketing & CRM | CONTRACTED | `listWalletTransactions` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-453` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS63 Game and Ride Board 6.dc.html#bo-453`
- Workshop pack: Game_and_Ride_Module.pdf board 6
- Flow F192 *Game and Ride board 6: Redemption Operations Dashboard*, step 18: Works in Redemption Transaction Ledger, Reconciliation & Audit → Provide complete traceability of redemption credits earned, redeemed, adjusted and associated inventory movements.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (41 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-453?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-444`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`, `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
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

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createPrize": {"method":"POST","path":"/prizes","contract":"games","summary":"Add a prize","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Prize","responds":"Prize"},
"getStockPositions": {"method":"GET","path":"/stock","contract":"inventory","summary":"Stock on hand by item and location","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"locationId","in":"query","required":null},{"name":"itemId","in":"query","required":null},{"name":"includeZero","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getWallet": {"method":"GET","path":"/wallets/{subjectId}","contract":"wallet","summary":"Read a guest wallet","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Wallet"},
"listGameplayTransactions": {"method":"GET","path":"/gameplay-transactions","contract":"games","summary":"Taps, decisions and what they cost","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"readerId","in":"query","required":null},{"name":"outcome","in":"query","required":null}],"requestBody":null,"responds":"GameplayTransaction"},
"listGames": {"method":"GET","path":"/games","contract":"games","summary":"List games","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"Game"},
"listPrizes": {"method":"GET","path":"/prizes","contract":"games","summary":"The prize catalogue","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"maxPoints","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listReaders": {"method":"GET","path":"/readers","contract":"games","summary":"Readers, their attractions and their health","permission":"DEVICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"Reader"},
"listWalletTransactions": {"method":"GET","path":"/wallets/{subjectId}/transactions","contract":"wallet","summary":"Wallet transaction history","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"lookupPrize": {"method":"GET","path":"/prizes/lookup","contract":"games","summary":"Look up a prize by barcode or SKU","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"code","in":"query","required":true},{"name":"venueId","in":"query","required":true}],"requestBody":null,"responds":"Prize"},
"redeemPrize": {"method":"POST","path":"/prize-redemptions","contract":"games","summary":"Redeem points for a prize","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PrizeRedemption"},
"setGamePricing": {"method":"PUT","path":"/game-pricing","contract":"games","summary":"Standard, group, peak, VIP, retry and calendar prices","permission":"PRICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GamePricing","responds":"GamePricing"},
"setPrizeCost": {"method":"PUT","path":"/prizes/{prizeId}/cost","contract":"games","summary":"What a prize costs in tickets, and what it costs the venue","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PrizeCost","responds":"PrizeCost"},
"setRedemptionRules": {"method":"PUT","path":"/redemption-rules","contract":"games","summary":"How tickets are earned, held and spent","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RedemptionRules","responds":"RedemptionRules"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Game": {"x-ticvai-persistence":"games.game","type":"object","required":["id","code","name","venueId","creditCost","status"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"zone":{"type":"string","nullable":true},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"The machine. Taken out of service by maintenance, the game stops accepting play rather than swallowing credits.\n"},"readerId":{"type":"string","format":"uuid","nullable":true},"creditCost":{"type":"integer","minimum":1},"minPointsAwarded":{"type":"integer"},"maxPointsAwarded":{"type":"integer"},"heightRequirementCm":{"type":"integer","nullable":true},"status":{"$ref":"#/components/schemas/GameStatus"},"playsToday":{"type":"integer"},"creditsTakenToday":{"type":"integer"},"pointsAwardedToday":{"type":"integer"}}},
"GamePricing": {"type":"object","x-ticvai-persistence":"games.pricing","description":"Board 5. **Priority is explicit**, because evaluation order is not a decision anybody made.\n`groupPricing`, `peakPricing` and `calendarExceptions` are stored one row per entry in `games.pricing_exception` (`GamePricingException`); the rest of this shape is `games.pricing`.\n","properties":{"gameId":{"type":"string","format":"uuid"},"standardPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"vipPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"groupPricing":{"type":"array","items":{"type":"object","properties":{"minimumPlayers":{"type":"integer"},"pricePerPlayer":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"peakPricing":{"type":"array","items":{"type":"object","properties":{"daysOfWeek":{"type":"array","items":{"type":"string"}},"from":{"type":"string"},"to":{"type":"string"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"calendarExceptions":{"type":"array","items":{"type":"object","properties":{"date":{"type":"string","format":"date"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"closed":{"type":"boolean","default":false}}}},"retryPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"retryWindowSeconds":{"type":"integer","nullable":true,"description":"How long after the game ends the retry offer stays open."},"retryOfferLeadSeconds":{"type":"integer","minimum":0,"nullable":true,"description":"**When the retry offer appears** (Chinmay, 2 October, workbook Q410, default accepted; DI-877; CHG-CSA-028): this many seconds before the game ends, and it stays open `retryWindowSeconds` after. A retry is charged in money at `retryPrice`, never from an entitlement; a retry after a machine fault is the reader's `retryPricing`, not this."},"priority":{"type":"array","items":{"type":"string","enum":["calendarException","peak","group","vip","retry","standard"]}},"scopePath":{"type":"string"}}},
"GameStatus": {"type":"string","enum":["inService","outOfService","maintenance","retired"]},
"GameplayTransaction": {"type":"object","x-ticvai-persistence":"games.gameplay_transaction","description":"Boards 8.2 and 8.5. **The refused ones are the valuable half.**","properties":{"id":{"type":"string","format":"uuid"},"readerId":{"type":"string","format":"uuid"},"gameId":{"type":"string","format":"uuid","nullable":true},"cardId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time"},"outcome":{"type":"string","enum":["allowed","refused","reversed"]},"reason":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargedFrom":{"type":"string","nullable":true},"entitlementId":{"type":"string","format":"uuid","nullable":true},"ticketsEarned":{"type":"integer","nullable":true},"decidedOffline":{"type":"boolean","default":false},"syncedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Prize": {"x-ticvai-persistence":"games.prize","type":"object","required":["id","name","venueId","pointCost","onHand"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":200},"description":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid"},"merchandiseId":{"type":"string","format":"uuid","nullable":true,"description":"Links to retail. Redemption depletes stock through the inventory ledger — a prize wall running out is a stock problem and should look like one.\n"},"pointCost":{"type":"integer","minimum":1},"onHand":{"type":"integer"},"isAvailable":{"type":"boolean"},"tier":{"type":"string","nullable":true,"description":"Small, medium, large, jackpot. Drives prize-wall layout."},"imageAssetRef":{"type":"string","nullable":true},"barcode":{"type":"string","maxLength":64,"nullable":true,"description":"The prize's own barcode, read by `lookupPrize` before the linked retail item's barcode or SKU. Unique within the venue (VM close-out, 29 September)."},"isActive":{"type":"boolean"}}},
"PrizeCost": {"type":"object","x-ticvai-persistence":"games.prize_cost","description":"Boards 6.7 and 6.8. **Two numbers, one of them on the shelf.**","properties":{"prizeId":{"type":"string","format":"uuid"},"ticketPrice":{"type":"integer"},"unitCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"marginPercent":{"type":"number","readOnly":true},"inventoryItemId":{"type":"string","format":"uuid","nullable":true,"description":"**Stock comes from `inventory`.** A prize catalogue with its own count is one that disagrees with the stockroom.\n"},"directPayPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"displayTier":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"PrizeRedemption": {"x-ticvai-persistence":"games.redemption + games.redemption_line","type":"object","required":["id","cardCode","lines","pointsUsed","pointsRemaining","recordedAt"],"properties":{"id":{"type":"string"},"redemptionNumber":{"type":"string"},"cardCode":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"lines":{"type":"array","items":{"type":"object","properties":{"prizeId":{"type":"string","format":"uuid"},"name":{"type":"string"},"quantity":{"type":"integer"},"pointCost":{"type":"integer"}}}},"pointsUsed":{"type":"integer"},"pointsRemaining":{"type":"integer"},"stockMovementIds":{"type":"array","description":"Movements raised in the inventory ledger.","items":{"type":"string"}},"issuedByPrincipalId":{"type":"string","format":"uuid"},"recordedAt":{"type":"string","format":"date-time"}}},
"Reader": {"type":"object","x-ticvai-persistence":"games.reader","description":"Board 2. **A `tenancy` device with a game configuration on it.**","required":["deviceId"],"properties":{"deviceId":{"type":"string","format":"uuid","description":"`tenancy.RegisteredDevice`. **Enrolment, firmware and tamper state live there.**\n"},"gameId":{"type":"string","format":"uuid","nullable":true},"readerProfileId":{"type":"string","format":"uuid","nullable":true},"acceptedCreditTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"acceptsDirectPay":{"type":"boolean","default":false},"retapDelaySeconds":{"type":"integer","default":3,"description":"**The setting that stops a guest paying twice for one go.** A wristband held against a reader for a second and a half is two taps to the hardware and one intention to the guest.\n"},"displayRules":{"type":"object","properties":{"freeGameGlow":{"type":"boolean","default":true,"description":"**What tells a guest their entitlement was used rather than their money.** Without it the complaint arrives at the desk.\n"},"showBalance":{"type":"boolean","default":true},"showPrice":{"type":"boolean","default":true},"themeCode":{"type":"string","nullable":true},"languages":{"type":"array","items":{"type":"string"}}}},"ioMapping":{"type":"object","additionalProperties":true,"description":"Board 9.6. Which output starts the game, which input reports it finished. **Deliberately open.** The keys are the reader model's own I/O lines, so the shape belongs to the vendor adaptor for that model (game readers are a driver, not a build — ADR-0012, ADR-0015), not to this contract.\n"},"status":{"type":"string","enum":["unconfigured","active","offline","maintenance","disabled"]},"scopePath":{"type":"string"}}},
"RedemptionRules": {"type":"object","x-ticvai-persistence":"games.redemption_rules","description":"Board 6. **Ticket-based and ticketless are one currency arriving two ways.**","properties":{"ticketCreditTypeId":{"type":"string","format":"uuid","nullable":true},"earnRules":{"type":"array","items":{"type":"object","properties":{"gameId":{"type":"string","format":"uuid"},"ticketsPerPlay":{"type":"integer","nullable":true},"ticketsPerScorePoint":{"type":"number","nullable":true},"maximumPerPlay":{"type":"integer","nullable":true}}}},"ticketEaterEnabled":{"type":"boolean","default":false},"ticketlessEnabled":{"type":"boolean","default":true},"ticketsExpire":{"type":"boolean","default":false},"ticketValidityDays":{"type":"integer","nullable":true},"counterApprovalAboveTickets":{"type":"integer","nullable":true,"description":"**A prize above a threshold needs a second person.** The alternative is a counter that can hand out the top shelf.\n"},"scopePath":{"type":"string"}}},
"StockPosition": {"x-ticvai-persistence":"none — derived from movements","type":"object","required":["itemId","locationId","onHand","unit"],"properties":{"itemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"sku":{"type":"string"},"locationId":{"type":"string","format":"uuid"},"locationName":{"type":"string"},"onHand":{"type":"number"},"allocated":{"type":"number","description":"**Reserved for orders**: the quantity under an active stock reservation for an order (decided 28 September, audit R171). A transfer is not allocation: dispatched stock has already left on-hand and sits in transit.\n"},"available":{"type":"number","description":"**On-hand minus allocated** (decided 28 September, audit R171). What can still be sold or issued.\n"},"unit":{"type":"string"},"value":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lastCountedAt":{"type":"string","format":"date-time","nullable":true},"lastMovementAt":{"type":"string","format":"date-time","nullable":true}}},
"Wallet": {"x-ticvai-persistence":"wallet.wallet + wallet.credit_lot","type":"object","required":["subjectId","balance","currency","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"credits":{"type":"array","description":"4.3.5 and 4.3.19. **One balance and one bonus balance with one expiry could not express what the requirement asks for** — cash, bonus and redemption credit, each with its own expiry.\n**The expiries are the reason this is a list.** Cash a guest paid for should outlive a promotional credit they were given, and a single `expiresAt` either expires the money they paid or never expires the promotion.\n**Consumed first-expiry-first-out across all three** (4.3.19), which is also the order that is fairest to the guest — spend what is about to die before what is not.\n**One entry per `active` lot in `wallet.credit_lot`** for this wallet: `amount` is the lot's `remaining_amount`, `expiresAt` its `expires_at`, `sourceRef` its `source_reference`. `kind` and `isRefundable` are not stored on the lot; they come from the lot's credit type (`listCreditLots` returns the lots themselves).\n","items":{"type":"object","required":["kind","amount"],"properties":{"kind":{"type":"string","enum":["cash","bonus","redemption","refund","goodwill"],"description":"**`cash` is money the guest paid and the others are not.** That distinction decides what is refundable, what expires, and what shows as a liability.\n","x-ticvai-persisted":false},"amount":{"x-ticvai-column":"remaining_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"sourceRef":{"type":"string","nullable":true,"x-ticvai-column":"source_reference"},"isRefundable":{"type":"boolean","default":false,"x-ticvai-persisted":false,"description":"**True only for `cash`.** A guest cannot cash out a promotional credit, and a wallet that lets them has given away the promotion twice.\n"}}}},"bonusBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Promotional value. Typically non-refundable and spent first."},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"status":{"type":"string","enum":["active","suspended","closed"]},"homeCellName":{"type":"string","nullable":true,"description":"Where the authoritative balance lives. Present when the guest is linked across cells.\n"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"lastActivityAt":{"type":"string","format":"date-time","nullable":true}}},
"WalletTransaction": {"x-ticvai-persistence":"wallet.wallet_transaction","type":"object","required":["id","kind","amount","balanceAfter","recordedAt"],"properties":{"id":{"type":"string"},"walletId":{"type":"string","format":"uuid","x-ticvai-references":"wallet.wallet","description":"The wallet this movement is on (SD-027, 29 September). A shared wallet has many subjects, so the subject alone cannot say which balance moved."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"wallet.hold","description":"The hold a spend settled, where it came through `holdWalletFunds`."},"kind":{"$ref":"#/components/schemas/WalletTransactionKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceAfter":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"orderId":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"WalletTransactionKind": {"type":"string","enum":["topUp","spend","refund","adjustment","bonus","expiry","transfer"]}
}
```
