# P08-orders-money-01 — P08 · Orders & Money (1 of 3)

**10 screens · 62 operations · 91 schemas · 21 permissions**

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

- **Every control that can be refused must be gated.** 21 permissions apply here:
  `LEDGER_POST, LEDGER_VIEW, ORDER_CREATE, ORDER_DISCOUNT, ORDER_EXCHANGE, ORDER_MODIFY, ORDER_REFUND, ORDER_REFUND_APPROVE, ORDER_REFUND_BULK, ORDER_REPRINT, ORDER_RESCHEDULE, ORDER_VIEW`…. A control nobody can use must say so,
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
| `BO-022` | Order Detail | B–D | 127 | 53 | 6 | 72 | 1 | 0 | — | notStarted (generated) |
| `BO-023` | Refunds & Exchanges | B–D | 95 | 71 | 6 | 60 | 3 | 6 | — | notStarted (generated) |
| `BO-024` | Payment Exceptions | B–D | 29 | 28 | 5 | 2 | 0 | 0 | — | notStarted (generated) |
| `BO-025` | Chargebacks & Disputes | B–D | 10 | 49 | 6 | 5 | 0 | 0 | — | notStarted (generated) |
| `BO-026` | Group Bookings | B–D | 158 | 69 | 6 | 77 | 2 | 6 | — | notStarted (generated) |
| `BO-027` | Reissue & Media Replacement | B–D | 13 | 7 | 6 | 22 | 0 | 0 | — | notStarted (generated) |
| `BO-028` | Refund Approval Queue | B–D | 2 | 0 | 4 | 1 | 5 | 6 | — | notStarted (generated) |
| `BO-029` | Report Builder | A | 76 | 28 | 6 | 88 | 1 | 0 | — | notStarted (generated) |
| `BO-039` | Shift Directory | B–D | 4 | 35 | 6 | 1 | 2 | 6 | — | notStarted (generated) |
| `BO-040` | Variance Approval | B–D | 17 | 59 | 6 | 5 | 1 | 3 | — | notStarted (generated) |

## Thin screens in this batch

**BO-028 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-022` Order Detail

**See everything about one order in one place.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `LEDGER_POST`, `LEDGER_VIEW`, `ORDER_CREATE`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`… (9 operate, 2 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listOrders` reads the population and `getOrder` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `orderId` (deepLink), `documentId` (navigation), `invoiceId` (navigation) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/venue-operations/order-detail` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Tax documents, as the UAE requires them** (research 2 October 2026, CHG-FIN-011; Executive Regulation Art. 59-60): the document a paid order gets is titled "Tax Invoice" (a simplified tax invoice for a guest, a full one with the buyer's name, address and TRN on request), never "Receipt" or "VAT receipt" as the title, and a correction is a "Tax Credit Note" (the contract calls it a credit memo). A simplified tax invoice is issued automatically when the order is paid; a full one is offered for a VAT-registered buyer and is the only kind above AED 10,000 for them. Amounts and VAT are in AED; a guest who paid in another currency sees the amount paid, the currency and the rate as payment information (CHG-FIN-001). **Refunds** (CHG-FIN-001): a card or wallet payment taken in a guest-selected currency is refunded in that currency at the sale rate (`Refund.tenderCurrency`, `tenderAmount`), shown beside the base amount ("USD 81.72 = AED 300.00 at 3.6710"); foreign cash at a till is refunded in base currency (DI-282).

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Everything about one order in one place: lines, guest, payments, refunds, statement, tax invoice and credit memos, with the after-sales actions of BO-023 available from it.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listOrders`. | `listOrders` ?venueId |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listOrders`. | `listOrders` ?principalId |
| Shift id | picker: choose a shift (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?shiftId=` to `listOrders`. | `listOrders` ?shiftId |
| Status | select | optional | — | Pending · Held · Paid · Partially paid · Completed · Voided · Refunded · Partially refunded · Failed; It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed. | — | Sends `?status=` to `listOrders`. | `listOrders` ?status |
| Created from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?createdFrom=` to `listOrders`. | `listOrders` ?createdFrom |
| Created to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?createdTo=` to `listOrders`. | `listOrders` ?createdTo |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listOrders` ?workstationId |
| Subject | picker: choose a subject | — | — | `listOrders` ?subjectId |
| Tender | select | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | `listOrders` ?tender |
| Order | picker: choose an order | — | — | `listTaxInvoices` ?orderId |
| Legal entity | picker: choose a legal entity | — | — | `listTaxInvoices` ?legalEntityId |
| Invoice type | segmented control | — | Simplified · Full · Consolidated | `listTaxInvoices` ?invoiceType |
| Status | radio group | — | Issued · Partially credited · Fully credited · Superseded | `listTaxInvoices` ?status |
| Issued from | date picker | — | — | `listTaxInvoices` ?issuedFrom |
| Issued to | date picker | — | — | `listTaxInvoices` ?issuedTo |
| Language | text field | — | pattern `^[a-z]{2}(-[A-Z]{2})?$` | `getTaxDocumentRendition` ?language |

**Form: Create order** (modal, opened by *Create order*; *Create order* calls `createOrder`, *Cancel* sends nothing)

**Collects what `createOrder` sends before it is called.** Required: `id`, `venueId`, `channel`, `lines`, `recordedAt`. Optional: `shiftId`, `subjectId`, `guestLinkId`, `catalogueBundleVersion`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. | `createOrder` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createOrder` body |
| Channel `channel` | select | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `createOrder` body |
| Shift `shiftId` | picker: choose a shift | optional | — | — | shows names, sends the id | — | `createOrder` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | Null for an anonymous sale. Identity and entitlement are separate. | `createOrder` body |
| Guest link `guestLinkId` | text field | optional | — | — | — | Present where the guest is linked across cells. | `createOrder` body |
| Catalogue bundle version `catalogueBundleVersion` | text field | optional | — | — | — | The bundle the client priced from. Lets the server explain a variance rather than merely report one. | `createOrder` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createOrder` body |
| ID `lines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `createOrder` body |
| Variant `lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `createOrder` body |
| Recommendation `lines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `createOrder` body |
| Performance `lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `createOrder` body |
| Booked window `lines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `createOrder` body |
| Starts at `lines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createOrder` body |
| Ends at `lines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `createOrder` body |
| Inventory hold `lines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `createOrder` body |
| Seats `lines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `createOrder` body |
| Resource hold `lines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `createOrder` body |
| Attributes `lines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `createOrder` body |
| Transport `lines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `createOrder` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `createOrder` body |
| Eligibility declaration `lines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `createOrder` body |
| Age band `lines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `createOrder` body |
| Age years `lines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `createOrder` body |
| Height band index `lines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `createOrder` body |
| Confident swimmer `lines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `createOrder` body |
| Guardian signed `lines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `createOrder` body |
| Quoted unit price `lines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `createOrder` body |
| Holder name `lines[].holderName` | text field | optional | — | — | — | — | `createOrder` body |
| Data mask values `lines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `createOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createOrder` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the client priced from is beyond its … (OrderRefusedProblem); 422 More seats for one performance than the channel allows (`seatLimitExceeded`, decided 29 September, rev 3 REV3-7). (OrderRefusedProblem)

**Form: Apply manual discount** (modal, opened by *Apply manual discount*; *Apply manual discount* calls `applyManualDiscount`, *Cancel* sends nothing)

**Collects what `applyManualDiscount` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `lineId`, `amount`, `percentage`, `reasonCode`, `approverPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this discount, and its idempotency key — it must equal the `Idempotency-Key` header. | `applyManualDiscount` body |
| Line `lineId` | picker: choose a line | optional | — | — | shows names, sends the id | Omit to discount the order rather than a line. | `applyManualDiscount` body |
| Amount `amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `applyManualDiscount` body |
| Percentage `percentage` | stepper or slider (%) | optional | — | min 0; max 100 | — | — | `applyManualDiscount` body |
| Reason `reason` | text area | required | — | min length 3; max length 300 | — | Required, and free text rather than a code list. A cashier forced to pick the nearest reason picks the first one, and the register stops meaning anything. | `applyManualDiscount` body |
| Reason code `reasonCode` | text field | optional | — | — | — | Optional alongside the free text, where the venue maintains a list. | `applyManualDiscount` body |
| Approver principal `approverPrincipalId` | picker: choose an approver principal | optional | — | — | shows names, sends the id | Required above the venue threshold. May not be the requester. | `applyManualDiscount` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `applyManualDiscount` body |

Errors to draw in the form: 403 Above the cashier's limit and no approver supplied (`approverRequired`), or the approver is the requester (`approverIsRequester`). (OrderRefusedProblem)

**Form: Create refund** (modal, opened by *Create refund*; *Create refund* calls `createRefund`, *Cancel* sends nothing)

**Collects what `createRefund` sends before it is called.** Required: `id`, `amount`, `reason`, `recordedAt`. Optional: `lineIds`, `secondaryAuthorisation`, `refundToOriginalTender`, `alternateTender`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the refund, and its idempotency key — it must equal the `Idempotency-Key` header. | `createRefund` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to refund the whole order. | `createRefund` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createRefund` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `createRefund` body |
| Secondary authorisation `secondaryAuthorisation` | group | optional | — | — | — | Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. | `createRefund` body |
| Principal `secondaryAuthorisation.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | — | `createRefund` body |
| Credential `secondaryAuthorisation.credential` | text area | required | — | max length 512 | — | The second person's staff PIN, as they sign in at a till with it. A PIN, never a password (decided 28 September, audit R123 (7)). | `createRefund` body |
| Refund to original tender `refundToOriginalTender` | toggle | optional | on | — | — | — | `createRefund` body |
| Alternate tender `alternateTender` | select | optional | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 … | `createRefund` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createRefund` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Second authorisation required and absent (`secondAuthorisationRequired`), refund window closed (`refundWindowClosed`), or the amount exceeds what remains … (RefundPolicyProblem)

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

**Form: Hold order** (modal, opened by *Hold order*; *Hold order* calls `holdOrder`, *Cancel* sends nothing)

**Collects what `holdOrder` sends before it is called.** Required: `recordedAt`. Optional: `label`, `holdUntil`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Label `label` | text field | optional | — | max length 60 | — | How the cashier will find it again — a name, a description, a party size. A list of unlabelled parked sales is unusable at a busy counter. | `holdOrder` body |
| Hold until `holdUntil` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `holdOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `holdOrder` body |

Errors to draw in the form: 409 Order is already paid (`alreadyPaid`) or voided (`orderVoided`) — only a `pending` order is parked — or a seated line's lease ends before `holdUntil` … (OrderRefusedProblem)

**Form: Modify order** (modal, opened by *Modify order*; *Modify order* calls `modifyOrder`, *Cancel* sends nothing)

**Collects what `modifyOrder` sends before it is called.** Required: `id`, `recordedAt`. Optional: `addLines`, `removeLineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this modification, not of the order — the order is the path's `orderId`. | `modifyOrder` body |
| Add lines `addLines` | repeatable rows | optional | — | — | — | — | `modifyOrder` body |
| ID `addLines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `modifyOrder` body |
| Variant `addLines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `modifyOrder` body |
| Recommendation `addLines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `modifyOrder` body |
| Performance `addLines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `modifyOrder` body |
| Booked window `addLines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `modifyOrder` body |
| Starts at `addLines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `modifyOrder` body |
| Ends at `addLines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `modifyOrder` body |
| Inventory hold `addLines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `modifyOrder` body |
| Seats `addLines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `modifyOrder` body |
| Resource hold `addLines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `modifyOrder` body |
| Attributes `addLines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `modifyOrder` body |
| Transport `addLines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `modifyOrder` body |
| Quantity `addLines[].quantity` | number field | required | — | min 1 | — | — | `modifyOrder` body |
| Eligibility declaration `addLines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `modifyOrder` body |
| Age band `addLines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `modifyOrder` body |
| Age years `addLines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `modifyOrder` body |
| Height band index `addLines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `modifyOrder` body |
| Confident swimmer `addLines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `modifyOrder` body |
| Guardian signed `addLines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `modifyOrder` body |
| Quoted unit price `addLines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `modifyOrder` body |
| Holder name `addLines[].holderName` | text field | optional | — | — | — | — | `modifyOrder` body |
| Data mask values `addLines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `modifyOrder` body |
| Remove lines `removeLineIds` | multi-picker: choose remove lines | optional | — | — | — | — | `modifyOrder` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `modifyOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `modifyOrder` body |

Errors to draw in the form: 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem)

**Form: Reprint order** (modal, opened by *Reprint order*; *Reprint order* calls `reprintOrder`, *Cancel* sends nothing)

**Collects what `reprintOrder` sends before it is called.** Required: `delivery`, `recordedAt`. Optional: `destination`, `lineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Delivery `delivery` | radio group | required | — | Print · Email · SMS · Whatsapp · Wallet | — | — | `reprintOrder` body |
| Destination `destination` | text field | optional | — | — | — | — | `reprintOrder` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to reprint every line. | `reprintOrder` body |
| Reason `reason` | radio group | optional | — | Printer fault · Guest request · Lost ticket · Not received · Other | — | — | `reprintOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the till reprinted — device time, as for every offline-capable write. | `reprintOrder` body |

Errors to draw in the form: 400 Validation failed

**Form: Reschedule order** (modal, opened by *Reschedule order*; *Reschedule order* calls `rescheduleOrder`, *Cancel* sends nothing)

**Collects what `rescheduleOrder` sends before it is called.** Required: `targetPerformanceId`, `recordedAt`. Optional: `lineIds`, `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target performance `targetPerformanceId` | picker: choose a target performance | required | — | — | shows names, sends the id | — | `rescheduleOrder` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to move the whole order. | `rescheduleOrder` body |
| Waive fee `waiveFee` | toggle | optional | off | — | — | — | `rescheduleOrder` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `rescheduleOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `rescheduleOrder` body |

Errors to draw in the form: 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem)

**Sent by *Void order*** (`voidOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this void, and its idempotency key — it must equal the `Idempotency-Key` header. | `voidOrder` body |
| Reason `reason` | select | required | — | Guest changed mind · Entered in error · Item unavailable · Quality issue · Duplicate · Other | — | The void reason list (decided 28 September, audit R125 (4)): the one list `voidOrder` takes, and the list `fnb.amendFnbOrder` and `fnb.cancelFnbOrder` point to. | `voidOrder` body |
| Note `note` | text area | optional | — | min length 3; max length 500; Required when `reason` is `other` (audit R222); optional otherwise. | — | Required when `reason` is `other` (audit R222); optional otherwise. | `voidOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `voidOrder` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every order** (data table, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |

**Every refund** (data table, from `listOrderRefunds`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | — |
| Batch | the name it points at, never the id | The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own. |
| FX rate | text | The rate on the original payment, not today's (BL-087, CF-118). `Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the … |
| Tax reversal entry | the name it points at, never the id | A refund reverses the tax entry it created, and this is where that is stated rather than implied. |
| Settle to | chip: Original tender, Advance balance, Wire transfer, Store credit | BL-086. A refund could only go back the way it came. |
| FX variance | AED 1,234.50 | Where the sale rate and the current rate differ, the difference is booked as an FX variance rather than hidden in the refund. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied percentage | 1,234.5 | From the venue's time bands, or an approver override. |
| Status | chip: Pending approval, Pending gateway, Completed, Declined, Failed | — |
| Reason | text | — |
| Requested by principal | the name it points at, never the id | — |

**The selected order** (detail panel, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |
| Principal | the name it points at, never the id | The cashier who raised it — what the held-orders list shows. |
| Hold label | text | As `Order.holdLabel`. |
| Held until | 1 Oct 2026, 14:30 | As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse. |

**The order statement** (detail panel, from `getOrderStatement`)

| Shows | Format | Notes |
|---|---|---|
| Order | the name it points at, never the id | — |
| Order number | text | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Entries | list or chips (count when long) | Sequential. What an agent reads to a guest asking about a charge. |
| Total paid | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total refunded | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Current balance | AED 1,234.50 | Positive means the guest owes; negative means a refund is outstanding. |

**The order** (detail panel, from `getOrder`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client UUIDv7 from `CreateOrderRequest.id`. |
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total price variance | AED 1,234.50 | Sum across lines. Zero on a normal order. |
| Lines | list or chips (count when long) | — |
| Payments | list or chips (count when long) | — |
| Principal | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Create order (primary button) | `createOrder` POST `/orders` | CreateOrderRequest | Order | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the … | opens modal first |
| Apply manual discount (secondary button) | `applyManualDiscount` POST `/orders/{orderId}/discounts` | ManualDiscountRequest | Order | 403 Above the cashier's limit and no approver supplied (`approverRequired`), or the approver is the requester (`approverIsRequester`). (OrderRefusedProblem) | opens modal first |
| Create refund (secondary button) | `createRefund` POST `/orders/{orderId}/refunds` | CreateRefundRequest | Refund | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Second authorisation required and absent (`secondAuthorisationRequired`), refund window closed (`refundWindowClosed`), or the amount … | opens modal first |
| Exchange order lines (secondary button) | `exchangeOrderLines` POST `/orders/{orderId}/exchanges` | ExchangeOrderRequest | OrderExchangeResult | 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem) | opens modal first |
| Hold order (secondary button) | `holdOrder` POST `/orders/{orderId}/hold` | inline | Order | 409 Order is already paid (`alreadyPaid`) or voided (`orderVoided`) — only a `pending` order is parked — or a seated line's lease ends before `holdUntil` … (OrderRefusedProblem) | opens modal first |
| Modify order (secondary button) | `modifyOrder` POST `/orders/{orderId}/modify` | ModifyOrderRequest | OrderModificationResult | 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem) | opens modal first |
| Reprint order (secondary button) | `reprintOrder` POST `/orders/{orderId}/reprints` | inline | inline | 400 Validation failed | opens modal first; produces a document or message: Reprint or resend tickets |
| Reschedule order (secondary button) | `rescheduleOrder` POST `/orders/{orderId}/reschedule` | inline | OrderExchangeResult | 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem) | opens modal first |
| Resume order (secondary button) | `resumeOrder` POST `/orders/{orderId}/resume` | — | OrderResumeResult | 409 Held order expired (`holdExpired`), or already resumed at another till (`alreadyResumed`). (OrderRefusedProblem) | — |
| Void order (destructive button) | `voidOrder` POST `/orders/{orderId}/voids` | inline | Order | 409 Settled — a payment on the order has been `captured`, so the money has moved (`alreadySettled`) — or taken in a shift that is now closed (`shiftClosed`). (OrderRefusedProblem) | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **order header and statement**: Order number, channel, status badge, guest, totals; the statement with a running balance; card masked to the last four. *(source: contracts/spine/orders.yaml#getOrderStatement / DI-069)*
- **tax documents**: Tax invoices and credit memos with PDF in English or Arabic; "Issue tax invoice" for a paid order that has none (simplified, full or consolidated). *(source: contracts/spine/finance.yaml#issueTaxInvoice / contracts/spine/finance.yaml#getTaxDocumentRendition)*

**Data it reads**: `listOrders` (onLoad, List orders); `listTaxInvoices` (onLoad, List tax invoices); `getTaxInvoice` (onLoad, Show a tax invoice); `getTaxDocumentRendition` (onLoad, Download the invoice / credit memo PDF)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*; carries `variantId`

**What opens over it**

- confirmDialog *Void order*: **Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A order this affects should be identified in the dialog, not just counted. **Collects what `voidOrder` sends before it is called.** Required: `id`, `reason`, `recordedAt`. `reason` is the void …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order yet. Offers Create order (`createOrder`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the order are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the client priced from is beyond its … (OrderRefusedProblem); 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem); 409 An order is not paid, is … |

#### Consistency with other screens

- Match `BO-023`: Same order header and the same after-sales dialogs.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
order:
  number: DP-2026-104882
  channel: Website
  status: Paid
  guest: Mariam Al Suwaidi
  total: AED 1,180.00
  taxInvoice: TI-AE-2026-008812
```

#### Permissions

- `listOrders` → `ORDER_VIEW` (read) · staff, guest, partner
- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `createOrder` → `ORDER_CREATE` (operate) · staff, guest, partner
- `applyManualDiscount` → `ORDER_DISCOUNT` (operate) · staff, partner
- `createRefund` → `ORDER_REFUND` (operate) · staff, partner
- `exchangeOrderLines` → `ORDER_EXCHANGE` (operate) · staff, partner
- `getOrderStatement` → `ORDER_VIEW` (read) · staff, partner
- `holdOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `listOrderRefunds` → `ORDER_VIEW` (read) · staff, partner
- `modifyOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `reprintOrder` → `ORDER_REPRINT` (operate) · staff, guest, partner
- `rescheduleOrder` → `ORDER_RESCHEDULE` (operate) · staff, partner
- `resumeOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `voidOrder` → `ORDER_VOID` (operate) · staff, partner
- `listTaxInvoices` → `LEDGER_VIEW` (read) · staff, guest
- `issueTaxInvoice` → `LEDGER_POST` (operate) · staff, guest, service
- `getTaxInvoice` → `LEDGER_VIEW` (read) · staff, guest
- `issueCreditMemo` → `LEDGER_POST` (operate) · staff, service
- `getTaxDocumentRendition` → `LEDGER_VIEW` (read) · staff, guest

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

72 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.3.7 | The system should allow access to their purchase history and ongoing orders and preferences. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 5.9.4 | The system should be able to provide a detailed log of transactions for each till. Detailed log of transaction should be always accessible, searchable and printable at back office. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 22.2.11 | Ticketing History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.12 | Membership History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.15 | Reservation History | Marketing & CRM | CONTRACTED | `listOrders` |
| 19.2.12 | Ticket Viewing - System shall display ticket details. | Guest Mobile App & Branding | CONTRACTED | `getOrder` |
| 2.6.2 | Post-order service 1) On the order details page, users can view the order number, amount, time, payment method, user information, refund/change policies, and the QR code of the e-ticket 2) During the … | Ticketing Sales | CONTRACTED | `getOrder` |
| 2.12.27 | All orders can be finalized for payment registration or modified or even cancelled at the Guest Service or any reservation PC. | Ticketing Sales | CONTRACTED | `getOrder` |
| 5.7.8 | The system should be able to use of a unique Order or Reference number (PNR) for each transaction, which can be communicated to the Payment Gateway, Acquiring Bank and the ERP system for … | F&B & Guest Management | CONTRACTED | `getOrder` |
| 2.1.6 | This system should provide a Ticketing POS solution that enables the operator to sell all the tickets defined in the system including multi-day and combo tickets. The POS solution must also support … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.7.29 | The system should be able to offer ticket sales to various outside business entities through the use of the exposed APIs and dedicated modules. Examples of typical clients that would have discounts … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.7.30 | The system should cater to multiple ways of enabling B2B clients, resellers and partner distribution channels to resell tickets and services offered by the client: - Web-based solution for B2B … | Ticketing Sales | CONTRACTED | `createOrder` |
| … 60 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Reservation lookup shows items, customer, payment method, taxes and an optional post-purchase survey, with reprint receipt and regenerate ticket PDF actions. *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-179)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-022` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (127), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (53 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-022?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create order, Apply manual discount, Create refund, Exchange order lines, Hold order, Modify order, Reprint order, Reschedule order, Resume order, Void order.
- [ ] Every transition is wired: `BO-008`.
- [ ] Every gated control is gated: `LEDGER_POST`, `LEDGER_VIEW`, `ORDER_CREATE`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_REFUND`, `ORDER_REPRINT`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-023` Refunds & Exchanges

**Give money back, or move the booking.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `LEDGER_POST`, `LEDGER_VIEW`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_REFUND`… (9 operate, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listOrderRefunds` reads the population and `getOrder` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `orderId` (deepLink), `venueId` (session), `documentId` (navigation), `invoiceId` (navigation) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/venue-operations/refunds-exchanges` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **`getRefundPolicy` wired 24 August.** **A refunds screen that cannot read the refund policy** judges every request by memory — and F09 was reaching it through `BO-003 Queue Integration Setup`, which held the operation only because of the 18 August bulk attach. **Tax documents, as the UAE requires them** (research 2 October 2026, CHG-FIN-011; Executive Regulation Art. 59-60): the document a paid order gets is titled "Tax Invoice" (a simplified tax invoice for a guest, a full one with the buyer's name, address and TRN on request), never "Receipt" or "VAT receipt" as the title, and a correction is a "Tax Credit Note" (the contract calls it a credit memo). A simplified tax invoice is issued automatically when the order is paid; a full one is offered for a VAT-registered buyer and is the only kind above AED 10,000 for them. Amounts and VAT are in AED; a guest who paid in another currency sees the amount paid, the currency and the rate as payment information (CHG-FIN-001). **Refunds** (CHG-FIN-001): a card or wallet payment taken in a guest-selected currency is refunded in that currency at the sale rate (`Refund.tenderCurrency`, `tenderAmount`), shown beside the base amount ("USD 81.72 = AED 300.00 at 3.6710"); foreign cash at a till is refunded in base currency (DI-282).

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-004): No operation lists message dispatches (for F09 step 5, confirming guests of a cancelled performance were notified). Removed 2 October 2026 (CHG-WIR-025): createOrder, holdOrder and resumeOrder are till operations at workstation scope; a refunds desk does not park sales or create orders, they belong to the POS … Removed 2 October 2026 (CHG-WIR-025): createOrder, holdOrder and resumeOrder are till operations at workstation scope; a refunds desk does not park sales or create orders, they belong to the POS …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The staff desk for after-sales on one order: refund (whole or some lines), void, exchange, reschedule, modify, manual discount, reprint, credit memo, all against the order's statement. Used by box office supervisors and the call centre, and at step 3 of an event cancellation to review refund exposure. The thing to get right is choosing the right act: void only before settlement in the same shift, otherwise refund; date change is reschedule, not refund and resell.

**Fixed on main** (the package already carries these; draw what it says): createOrder and holdOrder/resumeOrder (till operations, workstation scope) are on this back-office screen. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Principal | picker: choose a principal | — | — | `listOrders` ?principalId |
| Shift | picker: choose a shift | — | — | `listOrders` ?shiftId |
| Status | select | — | Pending · Held · Paid · Partially paid · Completed · Voided · Refunded · Partially refunded · Failed; It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed. | `listOrders` ?status |
| Created from | date and time picker | — | — | `listOrders` ?createdFrom |
| Created to | date and time picker | — | — | `listOrders` ?createdTo |
| Workstation | picker: choose a workstation | — | — | `listOrders` ?workstationId |
| Subject | picker: choose a subject | — | — | `listOrders` ?subjectId |
| Tender | select | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | `listOrders` ?tender |
| Tax invoice | picker: choose a tax invoice | — | — | `listCreditMemos` ?taxInvoiceId |
| Refund | picker: choose a refund | — | — | `listCreditMemos` ?refundId |
| Legal entity | picker: choose a legal entity | — | — | `listCreditMemos` ?legalEntityId |
| Issued from | date picker | — | — | `listCreditMemos` ?issuedFrom |
| Issued to | date picker | — | — | `listCreditMemos` ?issuedTo |
| Language | text field | — | pattern `^[a-z]{2}(-[A-Z]{2})?$` | `getTaxDocumentRendition` ?language |

**Form: Create refund** (modal, opened by *Create refund*; *Create refund* calls `createRefund`, *Cancel* sends nothing)

**Collects what `createRefund` sends before it is called.** Required: `id`, `amount`, `reason`, `recordedAt`. Optional: `lineIds`, `secondaryAuthorisation`, `refundToOriginalTender`, `alternateTender`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the refund, and its idempotency key — it must equal the `Idempotency-Key` header. | `createRefund` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to refund the whole order. | `createRefund` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createRefund` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `createRefund` body |
| Secondary authorisation `secondaryAuthorisation` | group | optional | — | — | — | Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. | `createRefund` body |
| Principal `secondaryAuthorisation.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | — | `createRefund` body |
| Credential `secondaryAuthorisation.credential` | text area | required | — | max length 512 | — | The second person's staff PIN, as they sign in at a till with it. A PIN, never a password (decided 28 September, audit R123 (7)). | `createRefund` body |
| Refund to original tender `refundToOriginalTender` | toggle | optional | on | — | — | — | `createRefund` body |
| Alternate tender `alternateTender` | select | optional | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 … | `createRefund` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createRefund` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Second authorisation required and absent (`secondAuthorisationRequired`), refund window closed (`refundWindowClosed`), or the amount exceeds what remains … (RefundPolicyProblem)

**Form: Apply manual discount** (modal, opened by *Apply manual discount*; *Apply manual discount* calls `applyManualDiscount`, *Cancel* sends nothing)

**Collects what `applyManualDiscount` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `lineId`, `amount`, `percentage`, `reasonCode`, `approverPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this discount, and its idempotency key — it must equal the `Idempotency-Key` header. | `applyManualDiscount` body |
| Line `lineId` | picker: choose a line | optional | — | — | shows names, sends the id | Omit to discount the order rather than a line. | `applyManualDiscount` body |
| Amount `amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `applyManualDiscount` body |
| Percentage `percentage` | stepper or slider (%) | optional | — | min 0; max 100 | — | — | `applyManualDiscount` body |
| Reason `reason` | text area | required | — | min length 3; max length 300 | — | Required, and free text rather than a code list. A cashier forced to pick the nearest reason picks the first one, and the register stops meaning anything. | `applyManualDiscount` body |
| Reason code `reasonCode` | text field | optional | — | — | — | Optional alongside the free text, where the venue maintains a list. | `applyManualDiscount` body |
| Approver principal `approverPrincipalId` | picker: choose an approver principal | optional | — | — | shows names, sends the id | Required above the venue threshold. May not be the requester. | `applyManualDiscount` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `applyManualDiscount` body |

Errors to draw in the form: 403 Above the cashier's limit and no approver supplied (`approverRequired`), or the approver is the requester (`approverIsRequester`). (OrderRefusedProblem)

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

**Form: Modify order** (modal, opened by *Modify order*; *Modify order* calls `modifyOrder`, *Cancel* sends nothing)

**Collects what `modifyOrder` sends before it is called.** Required: `id`, `recordedAt`. Optional: `addLines`, `removeLineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this modification, not of the order — the order is the path's `orderId`. | `modifyOrder` body |
| Add lines `addLines` | repeatable rows | optional | — | — | — | — | `modifyOrder` body |
| ID `addLines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `modifyOrder` body |
| Variant `addLines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `modifyOrder` body |
| Recommendation `addLines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `modifyOrder` body |
| Performance `addLines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `modifyOrder` body |
| Booked window `addLines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `modifyOrder` body |
| Starts at `addLines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `modifyOrder` body |
| Ends at `addLines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `modifyOrder` body |
| Inventory hold `addLines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `modifyOrder` body |
| Seats `addLines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `modifyOrder` body |
| Resource hold `addLines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `modifyOrder` body |
| Attributes `addLines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `modifyOrder` body |
| Transport `addLines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `modifyOrder` body |
| Quantity `addLines[].quantity` | number field | required | — | min 1 | — | — | `modifyOrder` body |
| Eligibility declaration `addLines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `modifyOrder` body |
| Age band `addLines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `modifyOrder` body |
| Age years `addLines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `modifyOrder` body |
| Height band index `addLines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `modifyOrder` body |
| Confident swimmer `addLines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `modifyOrder` body |
| Guardian signed `addLines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `modifyOrder` body |
| Quoted unit price `addLines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `modifyOrder` body |
| Holder name `addLines[].holderName` | text field | optional | — | — | — | — | `modifyOrder` body |
| Data mask values `addLines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `modifyOrder` body |
| Remove lines `removeLineIds` | multi-picker: choose remove lines | optional | — | — | — | — | `modifyOrder` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `modifyOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `modifyOrder` body |

Errors to draw in the form: 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem)

**Form: Reprint order** (modal, opened by *Reprint order*; *Reprint order* calls `reprintOrder`, *Cancel* sends nothing)

**Collects what `reprintOrder` sends before it is called.** Required: `delivery`, `recordedAt`. Optional: `destination`, `lineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Delivery `delivery` | radio group | required | — | Print · Email · SMS · Whatsapp · Wallet | — | — | `reprintOrder` body |
| Destination `destination` | text field | optional | — | — | — | — | `reprintOrder` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to reprint every line. | `reprintOrder` body |
| Reason `reason` | radio group | optional | — | Printer fault · Guest request · Lost ticket · Not received · Other | — | — | `reprintOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the till reprinted — device time, as for every offline-capable write. | `reprintOrder` body |

Errors to draw in the form: 400 Validation failed

**Form: Reschedule order** (modal, opened by *Reschedule order*; *Reschedule order* calls `rescheduleOrder`, *Cancel* sends nothing)

**Collects what `rescheduleOrder` sends before it is called.** Required: `targetPerformanceId`, `recordedAt`. Optional: `lineIds`, `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target performance `targetPerformanceId` | picker: choose a target performance | required | — | — | shows names, sends the id | — | `rescheduleOrder` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to move the whole order. | `rescheduleOrder` body |
| Waive fee `waiveFee` | toggle | optional | off | — | — | — | `rescheduleOrder` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `rescheduleOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `rescheduleOrder` body |

Errors to draw in the form: 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem)

**Form: Refund every order** (modal, opened by *Refund every order*; *Refund every order* calls `createBulkRefund`, *Cancel* sends nothing)

**Collects what `createBulkRefund` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scope `scope` | group | required | — | — | — | — | `createBulkRefund` body |
| Performance `scope.performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `createBulkRefund` body |
| Event `scope.eventId` | picker: choose an event | optional | — | — | shows names, sends the id | — | `createBulkRefund` body |
| Venue `scope.venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createBulkRefund` body |
| Date from `scope.dateFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createBulkRefund` body |
| Date to `scope.dateTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `createBulkRefund` body |
| Percentage `percentage` | stepper or slider (%) | optional | 100 | min 0; max 100 | — | — | `createBulkRefund` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `createBulkRefund` body |

**Sent by *Void order*** (`voidOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this void, and its idempotency key — it must equal the `Idempotency-Key` header. | `voidOrder` body |
| Reason `reason` | select | required | — | Guest changed mind · Entered in error · Item unavailable · Quality issue · Duplicate · Other | — | The void reason list (decided 28 September, audit R125 (4)): the one list `voidOrder` takes, and the list `fnb.amendFnbOrder` and `fnb.cancelFnbOrder` point to. | `voidOrder` body |
| Note `note` | text area | optional | — | min length 3; max length 500; Required when `reason` is `other` (audit R222); optional otherwise. | — | Required when `reason` is `other` (audit R222); optional otherwise. | `voidOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `voidOrder` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **refund amount and lines**: Pick lines (or the whole order); the amount is proposed from the venue's refund policy time bands ("72 hours or more before: 100%; 24 to 72 hours: 50%; under 24 hours: none") and can be overridden only by an authorised approver with a custom percentage. The policy band that applied is shown beside the amount. *(source: contracts/spine/orders.yaml#getRefundPolicy / DI-252 / TRACKER Actions row 79)*
- **secondaryAuthorisation**: Appears only when the amount is above the venue's "second user above" threshold: a second user (cashier or supervisor) signs in inline and is named on the refund. Above the approval threshold the refund is submitted for approval instead (pendingApproval). *(source: contracts/spine/orders.yaml#createRefund / MATRIX 2.12.3)*
- **refund destination**: Original tender by default; another tender (TICVAI wallet, store credit, bank transfer) only where the refund-to-wallet policy allows, named in the venue's words. *(source: contracts/spine/orders.yaml#createRefund / screens/P08-venue-back-office.yaml#BO-1146 / DI-673)*
- **void reason**: Picked from the void list (Guest changed mind, Entered in error, Item unavailable, Quality issue, Duplicate, Other); Other requires a note (PR-6). *(source: contracts/spine/orders.yaml#/components/schemas/VoidReason / R125 / R222)*
- **manual discount**: Amount or percentage, a free-text reason (at least 3 characters) and, above the venue threshold, an approver who is not the requester. *(source: contracts/spine/orders.yaml#applyManualDiscount / MATRIX 4.2.3)*

#### Outputs: what the screen shows and produces

**Shown**

**Every refund** (data table, from `listOrderRefunds`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | — |
| FX rate | text | The rate on the original payment, not today's (BL-087, CF-118). `Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the … |
| Tax reversal entry | the name it points at, never the id | A refund reverses the tax entry it created, and this is where that is stated rather than implied. |
| Settle to | chip: Original tender, Advance balance, Wire transfer, Store credit | BL-086. A refund could only go back the way it came. |
| FX variance | AED 1,234.50 | Where the sale rate and the current rate differ, the difference is booked as an FX variance rather than hidden in the refund. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied percentage | 1,234.5 | From the venue's time bands, or an approver override. |
| Status | chip: Pending approval, Pending gateway, Completed, Declined, Failed | — |
| Reason | text | — |
| Requested by principal | the name it points at, never the id | — |
| Secondary principal | the name it points at, never the id | — |

**Every order** (data table, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |
| Principal | the name it points at, never the id | The cashier who raised it — what the held-orders list shows. |
| Hold label | text | As `Order.holdLabel`. |
| Held until | 1 Oct 2026, 14:30 | As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse. |

**The selected refund** (detail panel, from `listOrderRefunds`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | — |
| Batch | the name it points at, never the id | The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own. |
| FX rate | text | The rate on the original payment, not today's (BL-087, CF-118). `Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the … |
| Tax reversal entry | the name it points at, never the id | A refund reverses the tax entry it created, and this is where that is stated rather than implied. |
| Settle to | chip: Original tender, Advance balance, Wire transfer, Store credit | BL-086. A refund could only go back the way it came. |
| FX variance | AED 1,234.50 | Where the sale rate and the current rate differ, the difference is booked as an FX variance rather than hidden in the refund. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied percentage | 1,234.5 | From the venue's time bands, or an approver override. |
| Status | chip: Pending approval, Pending gateway, Completed, Declined, Failed | — |
| Reason | text | — |
| Requested by principal | the name it points at, never the id | — |
| Secondary principal | the name it points at, never the id | — |
| Approved by principal | the name it points at, never the id | — |
| Ledger entry | the name it points at, never the id | Written before the gateway is called. |
| Gateway reference | text | — |

**The order statement** (detail panel, from `getOrderStatement`)

| Shows | Format | Notes |
|---|---|---|
| Order | the name it points at, never the id | — |
| Order number | text | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Entries | list or chips (count when long) | Sequential. What an agent reads to a guest asking about a charge. |
| Total paid | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total refunded | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Current balance | AED 1,234.50 | Positive means the guest owes; negative means a refund is outstanding. |

**The refund policy** (detail panel, from `getRefundPolicy`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | The venue in the path. Not taken from a `setRefundPolicy` body. |
| Self authorise limit | AED 1,234.50 | Up to this, a holder of ORDER_REFUND refunds alone. Zero means every refund needs a second authoriser. |
| Requires second user above | AED 1,234.50 | Above this, a second user — cashier OR supervisor — names themselves as audit control. |
| Requires approval above | AED 1,234.50 | Above this, an ORDER_REFUND_APPROVE holder must approve. |
| Time bands | list or chips (count when long) | Refundable percentage by time before the performance. Evaluated most-specific first. |
| Allow partial | yes / no (icon or chip) | — |
| Refund window days | 1,234 | Days after purchase within which a refund may be made. 0 is allowed and means the day of purchase only; null means no window (decided 28 … |
| Variance threshold | AED 1,234.50 | Price variance above this is an exception requiring review rather than a routine posting (CF-38). |

**The order** (detail panel, from `getOrder`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client UUIDv7 from `CreateOrderRequest.id`. |
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total price variance | AED 1,234.50 | Sum across lines. Zero on a normal order. |
| Lines | list or chips (count when long) | — |
| Payments | list or chips (count when long) | — |
| Principal | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Create refund (primary button) | `createRefund` POST `/orders/{orderId}/refunds` | CreateRefundRequest | Refund | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Second authorisation required and absent (`secondAuthorisationRequired`), refund window closed (`refundWindowClosed`), or the amount … | opens modal first |
| Apply manual discount (secondary button) | `applyManualDiscount` POST `/orders/{orderId}/discounts` | ManualDiscountRequest | Order | 403 Above the cashier's limit and no approver supplied (`approverRequired`), or the approver is the requester (`approverIsRequester`). (OrderRefusedProblem) | opens modal first |
| Exchange order lines (secondary button) | `exchangeOrderLines` POST `/orders/{orderId}/exchanges` | ExchangeOrderRequest | OrderExchangeResult | 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem) | opens modal first |
| Modify order (secondary button) | `modifyOrder` POST `/orders/{orderId}/modify` | ModifyOrderRequest | OrderModificationResult | 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem) | opens modal first |
| Reprint order (secondary button) | `reprintOrder` POST `/orders/{orderId}/reprints` | inline | inline | 400 Validation failed | opens modal first; produces a document or message: Reprint or resend tickets |
| Reschedule order (secondary button) | `rescheduleOrder` POST `/orders/{orderId}/reschedule` | inline | OrderExchangeResult | 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem) | opens modal first |
| Void order (destructive button) | `voidOrder` POST `/orders/{orderId}/voids` | inline | Order | 409 Settled — a payment on the order has been `captured`, so the money has moved (`alreadySettled`) — or taken in a shift that is now closed (`shiftClosed`). (OrderRefusedProblem) | — |
| Refund every order (secondary button) | `createBulkRefund` POST `/refunds/bulk` | inline | RefundBatch | — | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **order statement**: Every payment, refund, void, modification and exchange in time order with a running balance; card shown masked to the last four digits only. *(source: contracts/spine/orders.yaml#getOrderStatement / DI-069)*
- **exchange or reschedule result**: Outgoing value, incoming value, fee (waivable with permission) and the difference to pay or refund, before confirming. *(source: contracts/spine/orders.yaml#exchangeOrderLines / contracts/spine/orders.yaml#rescheduleOrder)*
- **credit memos**: Where a tax invoice was issued, the refund produces a credit memo; list them with a PDF link in English or Arabic. *(source: contracts/spine/finance.yaml#issueCreditMemo / contracts/spine/finance.yaml#getTaxDocumentRendition)*

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Refund**: Ledger first, then gateway; status shows Pending gateway until the provider confirms, and the ticket moves to Refunded with the refund linked to it. *(source: contracts/spine/orders.yaml#createRefund / MATRIX 2.12.13)*
- **Void**: Whole order only; refused after settlement or outside the shift with "use Refund"; the dialog names the tickets it revokes. *(source: contracts/spine/orders.yaml#voidOrder)*
- **Reschedule**: The new performance is held before the original is released; if the new date is full nothing changes. *(source: contracts/spine/orders.yaml#exchangeOrderLines)*

**Data it reads**: `listOrders` (onLoad, List orders); `getRefundPolicy` (onLoad, The policy this refund is judged against); `listCreditMemos` (onLoad, List credit memos); `getTaxDocumentRendition` (onLoad, Download the invoice / credit memo PDF)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*; carries `variantId`

**What opens over it**

- confirmDialog *Void order*: **Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A refunds exchanges this affects should be identified in the dialog, not just counted. **Collects what `voidOrder` sends before it is called.** Required: `id`, `reason`, `recordedAt`. `reason` is …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The refunds exchanges list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the refunds exchanges untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No refunds exchanges yet. Offers Create refund (`createRefund`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listOrderRefunds` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listOrderRefunds` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem); 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem); 409 Second authorisation required and … |

#### Edge cases to draw

- **A line whose ticket has already been scanned**: It cannot be removed or refunded through modify; the row says "Used 14 Oct 10:42". *(source: contracts/spine/orders.yaml#modifyOrder)*
- **Bulk refund after an event cancellation**: Refunds for a whole event are authorised on the bulk refund screen (F09 step 4); this screen shows the exposure and links there. *(source: F09 step 3 / DI-269)*
- **Refund window passed or performance in the past**: The refund action explains the policy that blocks it and offers the approver override path where permitted. *(source: contracts/spine/orders.yaml#getRefundPolicy)*

#### Consistency with other screens

- Match `BO-1146`: The destinations offered must match the refund-to-wallet policy configured there.
- Match `ADM-611`: Refund policy rules on the TICVAI Console use the same time-band vocabulary.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
order:
  number: DP-2026-104882
  channel: Website
  guest: Mariam Al Suwaidi / مريم السويدي
  total: AED 1,180.00
  status: Paid
  card: Visa •••• 4417
lines:
- t: Day Pass Adult x2, 14 Nov 2026
  a: AED 590.00
- t: Day Pass Child x2
  a: AED 490.00
- t: Fast Track Express x2
  a: AED 100.00
refundPolicy:
  selfAuthoriseLimit: AED 500.00
  secondUserAbove: AED 500.00
  approvalAbove: AED 2,000.00
  bands:
  - 72 h+ 100%
  - 24-72 h 50%
  - under 24 h 0%
```

#### Permissions

- `listOrderRefunds` → `ORDER_VIEW` (read) · staff, partner
- `createRefund` → `ORDER_REFUND` (operate) · staff, partner
- `applyManualDiscount` → `ORDER_DISCOUNT` (operate) · staff, partner
- `exchangeOrderLines` → `ORDER_EXCHANGE` (operate) · staff, partner
- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `getOrderStatement` → `ORDER_VIEW` (read) · staff, partner
- `listOrders` → `ORDER_VIEW` (read) · staff, guest, partner
- `modifyOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `reprintOrder` → `ORDER_REPRINT` (operate) · staff, guest, partner
- `rescheduleOrder` → `ORDER_RESCHEDULE` (operate) · staff, partner
- `voidOrder` → `ORDER_VOID` (operate) · staff, partner
- `getRefundPolicy` → `ORDER_VIEW` (read) · staff
- `issueCreditMemo` → `LEDGER_POST` (operate) · staff, service
- `listCreditMemos` → `LEDGER_VIEW` (read) · staff, guest
- `getTaxDocumentRendition` → `LEDGER_VIEW` (read) · staff, guest
- `createBulkRefund` → `ORDER_REFUND_BULK` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listOrderRefunds` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

60 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.12.3 | The system provide the ability for cashiers to issue refund up to a certain value with another user (cashier or supervisor) putting in their name as an audit control. | Ticketing Sales | CONTRACTED | `createRefund` |
| 2.12.13 | The system should change ticket status to Refunded after the Refund transaction is posted. Refund transaction should be linked with the ticket identifier to allow for reconciliation. There should be … | Ticketing Sales | CONTRACTED | `createRefund` |
| 4.2.3 | The system should be able to manually adjust the price of items in a transaction and make sure that these are reflected in the promotion discount | Bundles and Promotions | CONTRACTED | `applyManualDiscount` |
| 19.2.16 | Ticket Upgrade - System shall support ticket upgrades. | Guest Mobile App & Branding | CONTRACTED | `exchangeOrderLines` |
| 19.2.25 | Membership Upgrade - System shall support membership upgrades. | Guest Mobile App & Branding | CONTRACTED | `exchangeOrderLines` |
| 19.2.81 | Self-Service Membership Upgrades - System shall support self-service membership upgrades. | Guest Mobile App & Branding | CONTRACTED | `exchangeOrderLines` |
| 1.1.20 | System shall allow exchange of tickets between ticket types, dates, timeslots and experiences while applying configurable fees, price differences and approval workflows. | Ticketing Catalogue | CONTRACTED | `exchangeOrderLines` |
| 1.1.21 | System shall support ticket upgrades before or after purchase, including automatic calculation of price differences and applicable upgrade fees. | Ticketing Catalogue | CONTRACTED | `exchangeOrderLines` |
| 1.1.22 | System shall support ticket downgrades according to configurable business rules, refund policies and approval requirements. | Ticketing Catalogue | CONTRACTED | `exchangeOrderLines` |
| 1.1.96 | Membership upgrades | Ticketing Catalogue | CONTRACTED | `exchangeOrderLines` |
| 1.1.97 | Membership downgrades | Ticketing Catalogue | CONTRACTED | `exchangeOrderLines` |
| 2.12.36 | System shall maintain relationships between original orders, exchanged orders, upgraded orders, transferred orders, refunded orders, and related transactions for complete traceability. | Ticketing Sales | CONTRACTED | `exchangeOrderLines` |
| … 48 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Online/app returns: customer submits a return request with a reason (and photo if applicable) → approval team → courier pickup → refund after verified receipt. Confirmed: an item bought at the POS can also be returned via the web portal, subject to approval. *(agreed · MoM 19 Aug 2026, 4.7 Returns, Refunds & Exchanges — In-Store and Online; 5. Key Decisions · DI-367)*
- Bulk refunds: select and refund at event or date level (e.g. ~5,000 transactions for a cancelled event), online and on-site bookings, with one approval step before processing. *(agreed · MoM 12 Aug 2026, 18. Bulk Refund Processing and Refund Requests · DI-269)*
- Refunds use preset time-banded percentages (e.g. full refund a set number of days before the event, less closer to/after it), support partial refunds, and let an authorised approver apply a custom override percentage. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-252)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A75** Design the refund engine: a six-step ledger-to-gateway refund flow with configurable time-banded percentages, an authorized-approver override, partial refunds, both operations- and customer-initiated requests, plus bulk … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 12 Aug 2026 · workshop tracker · keyword 'refund')*
- **A80** Implement a currency-locking rule for refunds/change: always issue in the local/base currency, locked at the value recorded at time of purchase; track foreign-currency activity only via a separate report *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 14 Aug 2026 · workshop tracker · keyword 'refund')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'refund')*
- **A140** Centralise policy management (reschedule, exchange, refund, cancellation, upgrade, downgrade, ownership transfer, membership conversion) with each product mapped to pricing, GL code, promotions and channels *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'refund')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'refund')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'refund')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-023` · status **notStarted** · provenance generated
- Flow F09 *Event is cancelled and refunded*, step 3: Reviews the refund exposure → How many orders, how much money, how many across other venues
- Flow F09 *Event is cancelled and refunded*, step 4: Authorises the bulk refund → Refunds queue against the original payment method
- Flow F09 *Event is cancelled and refunded*, step 5: Confirms guests were notified → Told before they travel, not after
- Flow F09 branch at step 4 (requiresStaff): when Original payment method no longer valid, Refund fails and falls to a manual queue. Card expired, account closed. This is common at scale and needs a person.
- Flow F09 branch at step 4 (requiresStaff): when Some tickets already scanned, Partial performance — a show abandoned at the interval. **Refund policy differs from a full cancellation** and the split is a decision, not a rule.
- Flow F09 branch at step 4 (recoverable): when Seats were sold, Seats return to available. If the performance is rescheduled rather than cancelled they must be held, and the two paths diverge here.
- Flow F09 branch at step 4 (requiresStaff): when Entitlement is redeemable at another venue, Cross-cell. The redemption right must be revoked in the other cell too, and that cell may be unreachable.
- Flow F09 branch at step 3 (requiresStaff): when Refund exceeds the manager threshold, Requires a second approver. CF-36 put the threshold at venue level.

#### Acceptance for the design

- [ ] Every input above is drawn (95), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (71 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-023?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create refund, Apply manual discount, Exchange order lines, Modify order, Reprint order, Reschedule order, Void order, Refund every order.
- [ ] Every transition is wired: `BO-008`.
- [ ] Every gated control is gated: `LEDGER_POST`, `LEDGER_VIEW`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_REFUND`, `ORDER_REFUND_BULK`, `ORDER_REPRINT`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-024` Payment Exceptions

**Resolve payments that never resolved themselves.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `LEDGER_POST`, `ORDER_CREATE`, `ORDER_VIEW`, `SHIFT_CLOSE` (3 operate, 1 read); in the flows as cashier, finance controller |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`createPayment`, `addTip`, `capturePayment`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `paymentId` (deepLink), `depositId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/payment-exceptions` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Payment exceptions across currencies. **The rate shown is the one stored on the payment, not today's** (CF-37) — an exception opened in March and worked in August is worked at March's rate, or the reconciliation will never close.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-025): Taking a new payment (createPayment) or adding a tip (addTip) is a till act at workstation scope, and the exceptions screen resolves existing payments; it also … Removed 2 October 2026 (CHG-WIR-025): Taking a new payment (createPayment) or adding a tip (addTip) is a till act at workstation scope, and the exceptions screen resolves existing payments; it also …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Payments that never resolved themselves: a card charged with no response, an authorisation never captured, a deposit not settled, deposit boxes left open at close. A supervisor finds them and resolves each by asking the provider what actually happened, never by assuming failure. The rate shown on a foreign-currency payment is the one stored on it, not today's.

**Fixed on main** (the package already carries these; draw what it says): createPayment and addTip are offered as forms on an exceptions screen. (CHG-WIR-025); No read operation: the screen declares only createPayment, addTip, capturePayment, inquirePaymentStatus, closeDepositBoxes, settleDeposit … (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| id | picker: choose an id (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header. | `CreatePaymentRequest.id` |
| orderId | picker: choose an order (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `CreatePaymentRequest.orderId` |
| tender | select | optional | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). | `CreatePaymentRequest.tender` |
| amount | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `CreatePaymentRequest.amount` |
| tenderedAmount | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the guest handed over, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). | `CreatePaymentRequest.tenderAmount` |
| walletAuthorisationId | text field | optional | — | — | — | Cross-cell wallet hold, where the guest's home cell is elsewhere. | `CreatePaymentRequest.walletAuthorisationId` |
| deviceId | picker: choose a device (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `CreatePaymentRequest.deviceId` |
| recordedAt | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `CreatePaymentRequest.recordedAt` |

**Form: Capture payment** (modal, opened by *Capture payment*; *Capture payment* calls `capturePayment`, *Cancel* sends nothing)

**Collects what `capturePayment` sends before it is called.** Required: `amount`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `capturePayment` body |

Errors to draw in the form: 402 Capture refused by the issuer (`providerDeclined`); the payment moves to `declined` (states/payment.yaml). (PaymentProblem); 409 Only an `authorised` payment is captured (`notAuthorised`). The amount may not exceed what was authorised (`aboveAuthorisedAmount`), and less than that is … (PaymentProblem)

**Form: Settle deposit** (modal, opened by *Settle deposit*; *Settle deposit* calls `settleDeposit`, *Cancel* sends nothing)

**Collects what `settleDeposit` sends before it is called.** Required: `outcome`. Optional: `amount`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | radio group | required | — | Convert to revenue · Return · Forfeit · Partial forfeit | — | — | `settleDeposit` body |
| Amount `amount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | The part kept as income. Required for `partialForfeit`, ignored otherwise. | `settleDeposit` body |
| Reason `reason` | text area | optional | — | — | — | — | `settleDeposit` body |

Errors to draw in the form: 400 `partialForfeit` without an `amount`, or with one that is not above zero and below the deposit, or in another currency.; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The deposit is not `held` (it has already been settled), or a forfeit was asked for while the deposit is still refundable.

**Sent by *Close deposit boxes*** (`closeDepositBoxes`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Boxs `boxIds` | multi-picker: choose boxs | optional | — | — | — | — | `closeDepositBoxes` body |
| All open at venue `allOpenAtVenue` | toggle | optional | — | — | — | — | `closeDepositBoxes` body |
| Counts `counts` | repeatable rows | required | — | Omitting a box that needs one is refused with 422 `deposit-box-count-missing`. | — | One count per box being closed that has traded (audit R123 (4)). Omitting a box that needs one is refused with 422 `deposit-box-count-missing`. | `closeDepositBoxes` body |
| Box `counts[].boxId` | picker: choose a box | required | — | — | shows names, sends the id | — | `closeDepositBoxes` body |
| Counted total `counts[].countedTotal` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `closeDepositBoxes` body |
| Counted denominations `counts[].countedDenominations` | repeatable rows | optional | — | at least 1 | — | A count is a list of lines and the line is the row. Until 24 August this array carried the persistence hint itself, so `orders.cash_count_line` derived a single column — … | `closeDepositBoxes` body |
| ID `counts[].countedDenominations[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `closeDepositBoxes` body |
| Shift `counts[].countedDenominations[].shiftId` | picker: choose a shift | required | — | — | shows names, sends the id | A UUIDv7, as `Shift.id` and `orders.pos_shift.id` are. | `closeDepositBoxes` body |
| Deposit box `counts[].countedDenominations[].depositBoxId` | picker: choose a deposit box | optional | — | — | shows names, sends the id | — | `closeDepositBoxes` body |
| Count kind `counts[].countedDenominations[].countKind` | segmented control | optional | — | Opening float · Close · Movement | — | Which count this line belongs to — the opening float (`openShift`), the close (`closeShift`) or a lift or add (`createCashMovement`). | `closeDepositBoxes` body |
| Cash movement `counts[].countedDenominations[].cashMovementId` | picker: choose a cash movement | optional | — | — | shows names, sends the id | The movement this line counts, where `countKind` is `movement`. How `listCashMovements` rebuilds each movement's `denominations`. | `closeDepositBoxes` body |
| Denomination `counts[].countedDenominations[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` — face value, kind and sort order live there. | `closeDepositBoxes` body |
| Counted quantity `counts[].countedDenominations[].countedQuantity` | number field | required | — | min 0 | — | How many of this note or coin were in the drawer. | `closeDepositBoxes` body |
| Counted value `counts[].countedDenominations[].countedValue` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Quantity times face value, stored. Derivable, and stored anyway: a denomination revalued or deactivated later would silently rewrite a historical count. | `closeDepositBoxes` body |
| Counted by `counts[].countedDenominations[].countedBy` | picker: choose a counted by | optional | — | — | shows names, sends the id | — | `closeDepositBoxes` body |
| Counted at `counts[].countedDenominations[].countedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `closeDepositBoxes` body |
| Recount of `counts[].countedDenominations[].recountOf` | picker: choose a recount of | optional | — | — | shows names, sends the id | A recount points at what it replaces rather than overwriting it. `requestRecount` exists because a variance is a question before it is a fact. | `closeDepositBoxes` body |

#### Outputs: what the screen shows and produces

**Shown**

**Unresolved payments** (data table, from `listPaymentReconciliationException`)

| Shows | Format | Notes |
|---|---|---|
| Transaction | text | Transaction ID |
| External reference | text | External Reference |
| Amount | AED 1,234.50 | Amount |
| Currency | text | Currency |
| Date | 1 Oct 2026, 14:30 | Date |
| Merchant | text | Merchant |
| Order | text | Order |
| Authorization code | text | Authorization Code |
| Source system | chip: Payment gateway, Acquirer, Bank, POS, Ota, Reseller… | Source system. |
| Exception type | text | Exception, e.g. |
| Expected amount | AED 1,234.50 | Expected amount |
| Actual amount | AED 1,234.50 | Actual amount |

**Deposits** (data table, from `listDeposits`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | — |
| Customer | the name it points at, never the id | — |
| Rental agreement | the name it points at, never the id | — |
| Table reservation | the name it points at, never the id | The `fnb.TableReservation` this deposit secures, where the venue's `DepositPolicy.dining` is enabled (decided 29 September, rev 3 REV3-8b). |
| Currency code | text | — |
| Required amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Authorized amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Captured amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Released amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Forfeited amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Status | text | — |
| Settled at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Capture payment (secondary button) | `capturePayment` POST `/payments/{paymentId}/capture` | inline | Payment | 402 Capture refused by the issuer (`providerDeclined`); the payment moves to `declined` (states/payment.yaml). (PaymentProblem); 409 Only an `authorised` payment is captured (`notAuthorised`). The amount may not exceed … | emits `payment.captured`, `order.paid`; opens modal first |
| Inquire payment status (secondary button) | `inquirePaymentStatus` POST `/payments/{paymentId}/inquiry` | — | Payment | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Close deposit boxes (destructive button) | `closeDepositBoxes` POST `/deposit-boxes/close` | inline | DepositBox[] | 422 A box being closed has no entry in `counts`, or its entry has neither a total nor a denomination count (problem type `deposit-box-count-missing`, audit R123 … | — |
| Settle deposit (secondary button) | `settleDeposit` POST `/deposits/{depositId}/settle` | inline | Deposit | 400 `partialForfeit` without an `amount`, or with one that is not above zero and below the deposit, or in another currency.; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in … | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **exception list**: Grouped by kind (Pending confirmation, Authorised not captured, Deposit to settle, Box not closed), oldest first, with age, amount, tender, terminal and provider reference; a payment past the background reconciler's threshold is flagged. *(source: contracts/spine/orders.yaml#inquirePaymentStatus / F99 step 2)*
- **foreign tender**: Shows tender currency and amount, the stored rate and its source (manual, feed, card scheme), and the venue-currency amount. *(source: contracts/spine/orders.yaml#createPayment / screens/P08-venue-back-office.yaml#BO-024)*

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Ask the provider**: Queries the provider and reconciles; the row updates to Captured, Declined or Failed with the provider's answer and time. *(source: contracts/spine/orders.yaml#inquirePaymentStatus)*
- **Settle deposit**: Four outcomes, convert to revenue, return, forfeit, partly forfeit, none of them a refund; partial forfeit asks the amount kept and a reason. *(source: contracts/spine/finance.yaml#settleDeposit)*
- **Close deposit boxes**: One box or all open at the venue; a box closed without its holder is flagged with who counted it, not blocked. *(source: contracts/spine/shift.yaml#closeDepositBoxes / F32 step 8)*

**Data it reads**: `listPaymentReconciliationException` (onLoad, The payments that did not resolve themselves); `listDeposits` (onLoad, Deposits and their authorisation state, to settle or close)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*
- → `PTR-014` Settlement & Payment History: *Settlement & Payment History*

**What opens over it**

- confirmDialog *Close deposit boxes*: **Names what `closeDepositBoxes` changes and what it leaves alone**, in the consequence rather than the verb. A payment exceptions this affects should be identified in the dialog, not just counted. **Collects what `closeDepositBoxes` sends before it is called.** Nothing in the body is required. …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved payment exceptions. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment exceptions untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment exceptions configured. The form opens empty; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listPaymentReconciliationException` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `partialForfeit` without an `amount`, or with one that is not above zero and below the deposit, or in another currency.; 409 Only an `authorised` payment is captured (`notAuthorised`). The amount may not exceed what was authorised (`aboveAuthorisedAmount`), and less than that is … (PaymentProblem); 409 The deposit is not `held` (it has already been settled), or a forfeit was asked for while … |

#### Edge cases to draw

- **Provider still has no answer**: Stays Pending confirmation with "last asked 14:02"; never shown as failed. *(source: contracts/spine/orders.yaml#createPayment)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
exceptions:
- kind: Pending confirmation
  order: DP-2026-104901
  amount: AED 590.00
  tender: Card •••• 0921
  terminal: Gate 2 POS-04
  age: 38 min
- kind: Deposit to settle
  booking: Cabana B09
  amount: AED 300.00
  reason: rental
- kind: Box not closed
  box: Till 07 drawer
  holder: Ahmed Khan
  age: 1 h 12 min
```

#### Permissions

- `capturePayment` → `ORDER_CREATE` (operate) · staff, partner
- `inquirePaymentStatus` → `ORDER_CREATE` (operate) · staff, guest, partner
- `closeDepositBoxes` → `SHIFT_CLOSE` (operate) · staff
- `settleDeposit` → `LEDGER_POST` (operate) · staff, service
- `listPaymentReconciliationException` → `ORDER_VIEW` (read) · staff
- `listDeposits` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listPaymentReconciliationException` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.25 | No ticket can be issued until the payment has been done. | Ticketing Sales | CONTRACTED | `capturePayment` |
| 5.8.6 | The system should allow automated close out of one or more deposit boxes. | F&B & Guest Management | CONTRACTED | `closeDepositBoxes` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-024` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Retail Board 3.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Derived from `wireframes/reference/Retail Board 3.dc.html`
- Drawn by: Claude Design Retail pack, 24 August
- Client design-board frames: `Retail Board 3.dc.html#ret-3k`
- Flow F32 *A till opens, trades and settles*, step 8: The supervisor reviews the shift and the deposit reconciles. → Cash to the safe, shift `closed`, and the ledger posted. **`shift` writes `ledger.posting` here** — a till closing is a ledger act, which is why that cross-contract write is correct.
- Flow F99 *A chargeback arrives and is defended*, step 2: Payment Exceptions. → 6 operations, 0 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (29), with its required mark, default, format and its error state (400, 402, 404, 409, 422).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-024?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Capture payment, Inquire payment status, Close deposit boxes, Settle deposit.
- [ ] Every transition is wired: `BO-008`, `PTR-014`.
- [ ] Every gated control is gated: `LEDGER_POST`, `ORDER_CREATE`, `ORDER_VIEW`, `SHIFT_CLOSE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-025` Chargebacks & Disputes

**Answer the acquirer with the evidence attached.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_REFUND_APPROVE`, `SETTLEMENT_RECONCILE`, `SETTLEMENT_VIEW` (2 operate, 1 read); in the flows as finance controller |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSettlementExceptions` reads the population and `getSettlement` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `settlementId` (deepLink), `chargebackId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/chargebacks-disputes` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** A chargeback is a bank's decision on a clock the venue does not control: the money is already gone, evidence is due by a date, and a missed date loses the case regardless of merit. This screen lists cases by that deadline, assembles evidence the platform already holds, records the bank's answer, and shows whether things are getting worse. The one thing to get right: sort and colour by "evidence due", not by date received.

**Known correction pending (do not draw the wrong version)**

- **The layout shows settlement batches and exceptions only, with no chargeback list or detail.** Why: The chargeback operations are declared but nothing binds them; the screen duplicates BO-043 instead of showing cases. *(source: screens/P08-venue-back-office.yaml#BO-025; Finance, Ledger & Tax · Reporting & Analytics)*
- **The case list and the respond operation are not declared here.** Why: They exist and are consumed only by the platform console; the venue cannot see its cases by deadline or send evidence from its own back office. *(source: contracts/spine/orders.yaml#listChargebacks / contracts/spine/orders.yaml#respondToChargeback; Finance, Ledger & Tax · Reporting & Analytics)*
- **The chargeback analytics read is declared twice.** Why: Duplicate entry in the operations list. *(source: screens/P08-venue-back-office.yaml#BO-025; Finance, Ledger & Tax · Reporting & Analytics)*
- **The no-access state names the settlement permission.** Why: The chargeback operations require the refund-approval permission. *(source: contracts/spine/orders.yaml#recordChargeback; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Provider name | text field | — | — | `listSettlements` ?providerName |
| Status | select | — | Ingesting · Parsing · Matching · Matched · Has exceptions · Resolved · Failed | `listSettlements` ?status |
| Period from | date picker | — | — | `getChargebackAnalytics` ?periodFrom |
| Period to | date picker | — | — | `getChargebackAnalytics` ?periodTo |
| Group by | select | Reason | Reason · Provider · Outcome · Venue · Month · Product · Product category · Customer | `getChargebackAnalytics` ?groupBy |
| Min chargebacks | number field | — | min 1 | `getChargebackAnalytics` ?minChargebacks |
| Product | picker: choose a product | — | — | `getChargebackAnalytics` ?productId |
| Provider | picker: choose a provider | — | — | `getChargebackAnalytics` ?providerId |
| Period from | date picker | — | — | `getChargebackAnalytics` ?periodFrom |
| Period to | date picker | — | — | `getChargebackAnalytics` ?periodTo |
| Group by | select | Reason | Reason · Provider · Outcome · Venue · Month · Product · Product category · Customer | `getChargebackAnalytics` ?groupBy |
| Min chargebacks | number field | — | min 1 | `getChargebackAnalytics` ?minChargebacks |
| Product | picker: choose a product | — | — | `getChargebackAnalytics` ?productId |
| Provider | picker: choose a provider | — | — | `getChargebackAnalytics` ?providerId |

**Form: Resolve settlement exception** (modal, opened by *Resolve settlement exception*; *Resolve settlement exception* calls `resolveSettlementException`, *Cancel* sends nothing)

**Collects what `resolveSettlementException` sends before it is called.** Required: `exceptionId`, `resolution`, `note`. Optional: `matchedPaymentId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Exception `exceptionId` | picker: choose an exception | required | — | — | shows names, sends the id | — | `resolveSettlementException` body |
| Resolution `resolution` | radio group | required | — | Matched manually · Write off · Dispute raised · Provider error · Timing difference | — | How a settlement exception was explained. One vocabulary for the request and the stored exception. | `resolveSettlementException` body |
| Matched payment `matchedPaymentId` | picker: choose a matched payment | optional | — | — | shows names, sends the id | — | `resolveSettlementException` body |
| Note `note` | text area | required | — | min length 3; max length 1000 | — | — | `resolveSettlementException` body |

Errors to draw in the form: 400 `matchedManually` without a `matchedPaymentId`, or one that names no payment. `errors[]` names the field.; 404 The settlement, or an exception with this `exceptionId` under it, does not exist or is outside the caller's scope.; 409 The exception is already resolved.

**Form: Ingest settlement file** (modal, opened by *Ingest settlement file*; *Ingest settlement file* calls `ingestSettlementFile`, *Cancel* sends nothing)

**Collects what `ingestSettlementFile` sends before it is called.** Required: `providerName`, `periodStart`, `periodEnd`, `fileReference`. Optional: `format`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Provider name `providerName` | text field | required | — | — | — | — | `ingestSettlementFile` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | The venue this day of settlement is for (audit R110 (b)). | `ingestSettlementFile` body |
| Period start `periodStart` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | A day in the region's time zone, local midnight to local midnight. | `ingestSettlementFile` body |
| Period end `periodEnd` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | A day in the region's time zone, local midnight to local midnight. | `ingestSettlementFile` body |
| File reference `fileReference` | picker: choose a file reference | required | — | That upload route is staff-only and needs `ASSET_LIBRARY_MANAGE`; a partner caller has no upload route yet. | shows names, sends the id | The `id` of the `MediaAsset` holding the file, uploaded first through `assets.createUpload` then `assets.completeUpload` (direct to object storage through a signed URL). | `ingestSettlementFile` body |
| Format `format` | radio group | optional | — | Csv · Fixed width · Xml · Json | — | — | `ingestSettlementFile` body |

Errors to draw in the form: 400 `fileReference` names no completed upload in the caller's scope, or the period is not a single day (`settlement-period-not-a-day`, audit R110 (b)).

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Record a chargeback (from an acquirer portal)**: Provider, provider case reference, amount, reason, evidence due date; matched to the payment by reference. A repeat of the same reference returns the existing case. *(source: contracts/spine/orders.yaml#recordChargeback)*
- **Assign**: An investigator and a note; notes build an append-only investigation log. *(source: contracts/spine/orders.yaml#assignChargeback / contracts/spine/orders.yaml#/components/schemas/Chargeback)*
- **Respond**: Represent (send evidence) or Accept the loss. Evidence picked from what exists: the order, the admitting scan, delivery, the terms accepted, communications, device fingerprint. Accepting is a legitimate, recorded decision. *(source: contracts/spine/orders.yaml#respondToChargeback / contracts/spine/orders.yaml#/components/schemas/Chargeback)*
- **Outcome**: Won, Lost or Expired, as the bank decided. *(source: contracts/spine/orders.yaml#recordChargebackOutcome)*

#### Outputs: what the screen shows and produces

**Shown**

**Every settlement exception** (data table, from `listSettlementExceptions`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Server-created when parsing finds the exception, so a UUID (naming-and-style 4). |
| Settlement | the name it points at, never the id | — |
| Kind | chip: Unmatched in provider, Unmatched in ledger, Amount mismatch, Duplicate in provider … | — |
| Provider reference | text | — |
| Payment | the name it points at, never the id | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Expected amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Resolution | chip: Matched manually, Write off, Dispute raised, Provider error, Timing difference | Null while the exception is open. |
| Resolved by principal | the name it points at, never the id | — |
| Resolved at | 1 Oct 2026, 14:30 | — |

**Every settlement** (data table, from `listSettlements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Currency code | text | A settlement has no account, so nothing else denominates it. A posting takes its currency from `ledger.account.currency` and a payment from … |
| Provider name | text | — |
| Period start | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| Period end | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| File reference | the name it points at, never the id | The `MediaAsset` holding the provider file, as given to `ingestSettlementFile`. Kept on the row because parsing is asynchronous: the job … |
| Format | chip: Csv, Fixed width, Xml, Json | The file format given at ingest. Null when none was given. |
| Status | chip: Ingesting, Parsing, Matching, Matched, Has exceptions, Resolved… | — |
| Line count | 1,234 | — |
| Matched count | 1,234 | — |
| Exception count | 1,234 | — |
| Provider gross | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**The selected settlement exception** (detail panel, from `listSettlementExceptions`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Server-created when parsing finds the exception, so a UUID (naming-and-style 4). |
| Settlement | the name it points at, never the id | — |
| Kind | chip: Unmatched in provider, Unmatched in ledger, Amount mismatch, Duplicate in provider … | — |
| Provider reference | text | — |
| Payment | the name it points at, never the id | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Expected amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Resolution | chip: Matched manually, Write off, Dispute raised, Provider error, Timing difference | Null while the exception is open. |
| Note | text | The `note` given to `resolveSettlementException`, stored with the resolution. |
| Resolved by principal | the name it points at, never the id | — |
| Resolved at | 1 Oct 2026, 14:30 | — |

**The settlement** (detail panel, from `getSettlement`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Currency code | text | A settlement has no account, so nothing else denominates it. A posting takes its currency from `ledger.account.currency` and a payment from … |
| Provider name | text | — |
| Period start | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| Period end | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| File reference | the name it points at, never the id | The `MediaAsset` holding the provider file, as given to `ingestSettlementFile`. Kept on the row because parsing is asynchronous: the job … |
| Format | chip: Csv, Fixed width, Xml, Json | The file format given at ingest. Null when none was given. |
| Status | chip: Ingesting, Parsing, Matching, Matched, Has exceptions, Resolved… | — |
| Line count | 1,234 | — |
| Matched count | 1,234 | — |
| Exception count | 1,234 | — |
| Provider gross | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Provider fees | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Provider net | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Ledger gross | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Difference | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Resolve settlement exception (primary button) | `resolveSettlementException` POST `/settlements/{settlementId}/exceptions` | inline | SettlementException | 400 `matchedManually` without a `matchedPaymentId`, or one that names no payment. `errors[]` names the field.; 404 The settlement, or an exception with this `exceptionId` under it, does not exist or is outside the … | opens modal first |
| Ingest settlement file (secondary button) | `ingestSettlementFile` POST `/settlements` | inline | Settlement | 400 `fileReference` names no completed upload in the caller's scope, or the period is not a single day (`settlement-period-not-a-day`, audit R110 (b)). | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Case list**: Evidence due (countdown, red under 48 hours), amount and fee, reason in words (Fraudulent, Not received, Not as described, Duplicate, Subscription cancelled, Credit not processed, Unrecognised), status, investigator. Soonest due first. *(source: contracts/spine/orders.yaml#listChargebacks / contracts/spine/orders.yaml#/components/schemas/Chargeback)*
- **Evidence suggestion per reason**: For "Not received", lead with the scan record; for "Fraudulent", lead with device and terms; the reason decides which evidence wins. *(source: contracts/spine/orders.yaml#/components/schemas/Chargeback)*
- **Ledger effect**: The debit and fee posted at intake, and the reversal if won; each links to its journal entry. *(source: contracts/spine/orders.yaml#recordChargeback / contracts/spine/orders.yaml#recordChargebackOutcome)*
- **Analytics panel**: Chargeback rate by count and by value against card payments in the period, win rate, fees, cases lost to a missed deadline, by reason, product or customer; customers with repeated chargebacks show names only to holders of guest personal-data rights. *(source: contracts/spine/orders.yaml#getChargebackAnalytics / MATRIX 4.2.21)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Represent**: Status Evidence submitted; the deadline countdown stops. *(source: contracts/spine/orders.yaml#respondToChargeback)*
- **Accept loss**: Status Accepted; the debit stands. *(source: contracts/spine/orders.yaml#respondToChargeback)*
- **Record outcome**: Won posts the money back; Lost leaves the debit; the case closes. *(source: contracts/spine/orders.yaml#recordChargebackOutcome)*

**Data it reads**: `listSettlements` (onLoad, List settlement batches); `getChargebackAnalytics` (onLoad, Chargeback analytics panel); `getChargebackAnalytics` (onLoad, Chargeback rate by reason, product and customer)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*
- → `BO-024` Payment Exceptions: *Payment Exceptions*; carries `paymentId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The chargebacks disputes list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the chargebacks disputes untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No chargebacks disputes yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listSettlementExceptions` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SETTLEMENT_VIEW`, which `listSettlementExceptions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `fileReference` names no completed upload in the caller's scope, or the period is not a single day (`settlement-period-not-a-day`, audit R110 (b)).; 400 `matchedManually` without a `matchedPaymentId`, or one that names no payment. `errors[]` names the field.; 409 The case already has an outcome, or was `accepted` by the venue (a conceded case cannot be won), or the fiscal period for the … |

#### Edge cases to draw

- **The deadline passed with no response**: The case shows Expired (treated as lost) and counts in "lost to a missed deadline". *(source: contracts/spine/orders.yaml#recordChargebackOutcome)*
- **Responding after the case was decided**: Refused with "This case is already closed (won/lost/accepted/expired)". *(source: contracts/spine/orders.yaml#respondToChargeback)*

#### Consistency with other screens

- Match `ADM-634`: The platform's chargeback command centre uses the same case model and wording.
- Match `BO-043`: Settlement exceptions are a different thing; do not mix the two lists.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cases:
- Due in 1 day 6 h · AED 598.00 + fee AED 55.00 · Not received · NI case 7712093 · Fatima Al Mansoori investigating
- Due in 9 days · AED 1,250.00 · Fraudulent · Stripe dp_3Nx… · unassigned
analytics: September · 14 cases · 0.09% of card payments by count · win rate 64% · fees AED 770.00 · 1 lost to deadline
```

#### Permissions

- `listSettlementExceptions` → `SETTLEMENT_VIEW` (read) · staff, partner
- `resolveSettlementException` → `SETTLEMENT_RECONCILE` (operate) · staff, partner
- `getSettlement` → `SETTLEMENT_VIEW` (read) · staff, partner
- `ingestSettlementFile` → `SETTLEMENT_RECONCILE` (operate) · staff, partner
- `listSettlements` → `SETTLEMENT_VIEW` (read) · staff, partner
- `recordChargeback` → `ORDER_REFUND_APPROVE` (operate) · staff, service
- `assignChargeback` → `ORDER_REFUND_APPROVE` (operate) · staff
- `recordChargebackOutcome` → `ORDER_REFUND_APPROVE` (operate) · staff, service
- `getChargebackAnalytics` → `ORDER_REFUND_APPROVE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `SETTLEMENT_VIEW`, which `listSettlementExceptions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.7.92 | The system shall support chargeback notification handling, dispute management, evidence collection, investigation workflows, resolution tracking, and financial adjustments. Track chargeback status … | F&B & Guest Management | CONTRACTED | `recordChargeback` |
| 8.3.11 | System shall identify transactions with elevated chargeback risk. | Unified Operations Dashboard | CONTRACTED | `recordChargeback` |
| 4.2.21 | The system shall provide tools for tracking chargebacks, managing disputes, storing evidence, monitoring resolution status, and generating chargeback analytics. | Bundles and Promotions | CONTRACTED | `getChargebackAnalytics` |
| 8.3.12 | System shall identify customers with repeated chargebacks. | Unified Operations Dashboard | CONTRACTED | `getChargebackAnalytics` |
| 8.3.13 | System shall identify products with elevated chargeback rates. | Unified Operations Dashboard | CONTRACTED | `getChargebackAnalytics` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-025` · status **notStarted** · provenance generated
- Flow F99 *A chargeback arrives and is defended*, step 1: Chargebacks & Disputes. → 5 operations, 5 of them previously unwalked.
- Flow F99 branch at step 1 (medium): when The acting principal lacks the permission at this scope., **Refused at the first step, not the last.** ADR-0002 makes authorisation user-driven — a person who gets three steps in and then cannot finish has been told the wrong thing.
- ADR-0033 *Every asynchronous handoff has an outbox and a place to fail* (`docs/adr/0033-outbox-and-dead-letters.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (49 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-025?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Resolve settlement exception, Ingest settlement file.
- [ ] Every transition is wired: `BO-008`, `BO-024`.
- [ ] Every gated control is gated: `ORDER_REFUND_APPROVE`, `SETTLEMENT_RECONCILE`, `SETTLEMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-026` Group Bookings

**Handle a booking that arrives as a school, not a guest.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 2 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_REFUND`, `ORDER_REPRINT`… (8 operate, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listOrders` reads the population and `getOrder` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `orderId` (deepLink), `groupBookingId` (navigation) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/venue-operations/group-bookings` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Drawn 31 August** — `Seat Platform Board 7.dc.html` frame `seatp-7e`. **Matched on frame title against screen name, constrained to this board’s platforms.** These packs label by board position (`GM-6C`) rather than naming the screen, so the title is the only join — *Group Booking* matched at 0.96. **A cross-platform title match was refused**: `Outlet Management` scored 0.85 against a partner-portal screen, which is how a mapping goes wrong quietly.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** A booking that arrives as a school, company or party rather than a guest: leader, expected and confirmed size against the minimum, name capture, year group, access and dietary needs, celebrant.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listOrders`. | `listOrders` ?venueId |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listOrders`. | `listOrders` ?principalId |
| Shift id | picker: choose a shift (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?shiftId=` to `listOrders`. | `listOrders` ?shiftId |
| Status | select | optional | — | Pending · Held · Paid · Partially paid · Completed · Voided · Refunded · Partially refunded · Failed; It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed. | — | Sends `?status=` to `listOrders`. | `listOrders` ?status |
| Created from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?createdFrom=` to `listOrders`. | `listOrders` ?createdFrom |
| Created to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?createdTo=` to `listOrders`. | `listOrders` ?createdTo |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listOrders` ?workstationId |
| Subject | picker: choose a subject | — | — | `listOrders` ?subjectId |
| Tender | select | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | `listOrders` ?tender |

**Form: Create group booking** (modal, opened by *Create group booking*; *Create group booking* calls `createGroupBooking`, *Cancel* sends nothing)

**Collects what `createGroupBooking` sends before it is called.** Required: `orderId`, `leaderSubjectId`, `expectedSize`. Optional: `kind`, `packageProductId`, `yearGroup`, `accessAndDietaryNeeds`, `celebrantName`, `celebrantTurningAge`, `allergiesAndRequests`, `finalHeadcountDueBy`, `organisationName`, `minimumSize`, `attendeeCaptureRequired`, `attendeeCaptureDueBy`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Group quote `groupQuoteId` | picker: choose a group quote | optional | — | — | shows names, sends the id | The quote this booking converts (BO-272). Must be the current version and `sent` or `accepted`; conversion sets its `groupBookingId` and moves a `sent` quote to `accepted` … | `createGroupBooking` body |
| Kind `kind` | radio group | optional | General | General · School · Corporate · Party | — | — | `createGroupBooking` body |
| Package product `packageProductId` | text field | optional | — | — | — | The school-trip format or party package. | `createGroupBooking` body |
| Year group `yearGroup` | text field | optional | — | max length 40 | — | — | `createGroupBooking` body |
| Access and dietary needs `accessAndDietaryNeeds` | text area | optional | — | max length 1000 | — | — | `createGroupBooking` body |
| Celebrant name `celebrantName` | text field | optional | — | max length 120 | — | The birthday child. | `createGroupBooking` body |
| Celebrant turning age `celebrantTurningAge` | stepper or slider | optional | — | min 1; max 18 | — | — | `createGroupBooking` body |
| Allergies and requests `allergiesAndRequests` | text area | optional | — | max length 1000 | — | — | `createGroupBooking` body |
| Final headcount due by `finalHeadcountDueBy` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createGroupBooking` body |
| Order `orderId` | picker: choose an order | required | — | — | shows names, sends the id | — | `createGroupBooking` body |
| Leader subject `leaderSubjectId` | picker: choose a leader subject | required | — | — | shows names, sends the id | The person who pays, is called if the coach is late, and collects the names. | `createGroupBooking` body |
| Organisation name `organisationName` | text field | optional | — | max length 200 | — | — | `createGroupBooking` body |
| Expected size `expectedSize` | number field | required | — | min 2 | — | — | `createGroupBooking` body |
| Minimum size `minimumSize` | number field | optional | — | min 1 | — | — | `createGroupBooking` body |
| Attendee capture required `attendeeCaptureRequired` | toggle | optional | off | — | — | — | `createGroupBooking` body |
| Attendee capture due by `attendeeCaptureDueBy` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createGroupBooking` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 The order already has a group booking (`orderAlreadyGrouped`), or is voided (`orderVoided`), or `groupQuoteId` names a quote that cannot be converted … (GroupBookingProblem)

**Form: Save group booking** (modal, opened by *Save group booking*; *Save group booking* calls `updateGroupBooking`, *Cancel* sends nothing)

**Collects what `updateGroupBooking` sends before it is called.** Nothing in the body is required. Optional: `packageProductId`, `yearGroup`, `accessAndDietaryNeeds`, `celebrantName`, `celebrantTurningAge`, `allergiesAndRequests`, `finalHeadcountDueBy`, `leaderSubjectId`, `organisationName`, `expectedSize`, `confirmedSize`, `minimumSize` and 3 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Package product `packageProductId` | text field | optional | — | — | — | The school-trip format or party package. | `updateGroupBooking` body |
| Year group `yearGroup` | text field | optional | — | max length 40 | — | — | `updateGroupBooking` body |
| Access and dietary needs `accessAndDietaryNeeds` | text area | optional | — | max length 1000 | — | — | `updateGroupBooking` body |
| Celebrant name `celebrantName` | text field | optional | — | max length 120 | — | The birthday child. | `updateGroupBooking` body |
| Celebrant turning age `celebrantTurningAge` | stepper or slider | optional | — | min 1; max 18 | — | — | `updateGroupBooking` body |
| Allergies and requests `allergiesAndRequests` | text area | optional | — | max length 1000 | — | — | `updateGroupBooking` body |
| Final headcount due by `finalHeadcountDueBy` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateGroupBooking` body |
| Leader subject `leaderSubjectId` | picker: choose a leader subject | optional | — | — | shows names, sends the id | — | `updateGroupBooking` body |
| Organisation name `organisationName` | text field | optional | — | max length 200 | — | — | `updateGroupBooking` body |
| Expected size `expectedSize` | number field | optional | — | min 2 | — | — | `updateGroupBooking` body |
| Confirmed size `confirmedSize` | number field | optional | — | min 0 | — | — | `updateGroupBooking` body |
| Minimum size `minimumSize` | number field | optional | — | min 1 | — | — | `updateGroupBooking` body |
| Attendee capture required `attendeeCaptureRequired` | toggle | optional | — | — | — | — | `updateGroupBooking` body |
| Attendee capture due by `attendeeCaptureDueBy` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateGroupBooking` body |
| Status `status` | radio group | optional | — | Confirmed · Names pending · Complete · Cancelled | — | — | `updateGroupBooking` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The status change goes backwards (`statusBackwards`), or the group is already cancelled or complete (`groupClosed`). (GroupBookingProblem); 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Form: Create order** (modal, opened by *Create order*; *Create order* calls `createOrder`, *Cancel* sends nothing)

**Collects what `createOrder` sends before it is called.** Required: `id`, `venueId`, `channel`, `lines`, `recordedAt`. Optional: `shiftId`, `subjectId`, `guestLinkId`, `catalogueBundleVersion`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. | `createOrder` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createOrder` body |
| Channel `channel` | select | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `createOrder` body |
| Shift `shiftId` | picker: choose a shift | optional | — | — | shows names, sends the id | — | `createOrder` body |
| Subject `subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | Null for an anonymous sale. Identity and entitlement are separate. | `createOrder` body |
| Guest link `guestLinkId` | text field | optional | — | — | — | Present where the guest is linked across cells. | `createOrder` body |
| Catalogue bundle version `catalogueBundleVersion` | text field | optional | — | — | — | The bundle the client priced from. Lets the server explain a variance rather than merely report one. | `createOrder` body |
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `createOrder` body |
| ID `lines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `createOrder` body |
| Variant `lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `createOrder` body |
| Recommendation `lines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `createOrder` body |
| Performance `lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `createOrder` body |
| Booked window `lines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `createOrder` body |
| Starts at `lines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createOrder` body |
| Ends at `lines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `createOrder` body |
| Inventory hold `lines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `createOrder` body |
| Seats `lines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `createOrder` body |
| Resource hold `lines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `createOrder` body |
| Attributes `lines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `createOrder` body |
| Transport `lines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `createOrder` body |
| Quantity `lines[].quantity` | number field | required | — | min 1 | — | — | `createOrder` body |
| Eligibility declaration `lines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `createOrder` body |
| Age band `lines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `createOrder` body |
| Age years `lines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `createOrder` body |
| Height band index `lines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `createOrder` body |
| Confident swimmer `lines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `createOrder` body |
| Guardian signed `lines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `createOrder` body |
| Quoted unit price `lines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `createOrder` body |
| Holder name `lines[].holderName` | text field | optional | — | — | — | — | `createOrder` body |
| Data mask values `lines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `createOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createOrder` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the client priced from is beyond its … (OrderRefusedProblem); 422 More seats for one performance than the channel allows (`seatLimitExceeded`, decided 29 September, rev 3 REV3-7). (OrderRefusedProblem)

**Form: Apply manual discount** (modal, opened by *Apply manual discount*; *Apply manual discount* calls `applyManualDiscount`, *Cancel* sends nothing)

**Collects what `applyManualDiscount` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `lineId`, `amount`, `percentage`, `reasonCode`, `approverPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this discount, and its idempotency key — it must equal the `Idempotency-Key` header. | `applyManualDiscount` body |
| Line `lineId` | picker: choose a line | optional | — | — | shows names, sends the id | Omit to discount the order rather than a line. | `applyManualDiscount` body |
| Amount `amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `applyManualDiscount` body |
| Percentage `percentage` | stepper or slider (%) | optional | — | min 0; max 100 | — | — | `applyManualDiscount` body |
| Reason `reason` | text area | required | — | min length 3; max length 300 | — | Required, and free text rather than a code list. A cashier forced to pick the nearest reason picks the first one, and the register stops meaning anything. | `applyManualDiscount` body |
| Reason code `reasonCode` | text field | optional | — | — | — | Optional alongside the free text, where the venue maintains a list. | `applyManualDiscount` body |
| Approver principal `approverPrincipalId` | picker: choose an approver principal | optional | — | — | shows names, sends the id | Required above the venue threshold. May not be the requester. | `applyManualDiscount` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `applyManualDiscount` body |

Errors to draw in the form: 403 Above the cashier's limit and no approver supplied (`approverRequired`), or the approver is the requester (`approverIsRequester`). (OrderRefusedProblem)

**Form: Create refund** (modal, opened by *Create refund*; *Create refund* calls `createRefund`, *Cancel* sends nothing)

**Collects what `createRefund` sends before it is called.** Required: `id`, `amount`, `reason`, `recordedAt`. Optional: `lineIds`, `secondaryAuthorisation`, `refundToOriginalTender`, `alternateTender`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the refund, and its idempotency key — it must equal the `Idempotency-Key` header. | `createRefund` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to refund the whole order. | `createRefund` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createRefund` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `createRefund` body |
| Secondary authorisation `secondaryAuthorisation` | group | optional | — | — | — | Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. | `createRefund` body |
| Principal `secondaryAuthorisation.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | — | `createRefund` body |
| Credential `secondaryAuthorisation.credential` | text area | required | — | max length 512 | — | The second person's staff PIN, as they sign in at a till with it. A PIN, never a password (decided 28 September, audit R123 (7)). | `createRefund` body |
| Refund to original tender `refundToOriginalTender` | toggle | optional | on | — | — | — | `createRefund` body |
| Alternate tender `alternateTender` | select | optional | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 … | `createRefund` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createRefund` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Second authorisation required and absent (`secondAuthorisationRequired`), refund window closed (`refundWindowClosed`), or the amount exceeds what remains … (RefundPolicyProblem)

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

**Form: Hold order** (modal, opened by *Hold order*; *Hold order* calls `holdOrder`, *Cancel* sends nothing)

**Collects what `holdOrder` sends before it is called.** Required: `recordedAt`. Optional: `label`, `holdUntil`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Label `label` | text field | optional | — | max length 60 | — | How the cashier will find it again — a name, a description, a party size. A list of unlabelled parked sales is unusable at a busy counter. | `holdOrder` body |
| Hold until `holdUntil` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `holdOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `holdOrder` body |

Errors to draw in the form: 409 Order is already paid (`alreadyPaid`) or voided (`orderVoided`) — only a `pending` order is parked — or a seated line's lease ends before `holdUntil` … (OrderRefusedProblem)

**Form: Modify order** (modal, opened by *Modify order*; *Modify order* calls `modifyOrder`, *Cancel* sends nothing)

**Collects what `modifyOrder` sends before it is called.** Required: `id`, `recordedAt`. Optional: `addLines`, `removeLineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this modification, not of the order — the order is the path's `orderId`. | `modifyOrder` body |
| Add lines `addLines` | repeatable rows | optional | — | — | — | — | `modifyOrder` body |
| ID `addLines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `modifyOrder` body |
| Variant `addLines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `modifyOrder` body |
| Recommendation `addLines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `modifyOrder` body |
| Performance `addLines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `modifyOrder` body |
| Booked window `addLines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `modifyOrder` body |
| Starts at `addLines[].bookedWindow.startsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `modifyOrder` body |
| Ends at `addLines[].bookedWindow.endsAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | After `startsAt`, on the same venue day. | `modifyOrder` body |
| Inventory hold `addLines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `modifyOrder` body |
| Seats `addLines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `modifyOrder` body |
| Resource hold `addLines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `modifyOrder` body |
| Attributes `addLines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `modifyOrder` body |
| Transport `addLines[].attributes.transport` | group | optional | — | — | — | What a transport line is for (decided 29 September, rev 3 REV3-21). Present on a one-way trip, a pass purchase, or a seat reserved with a pass already owned. | `modifyOrder` body |
| Quantity `addLines[].quantity` | number field | required | — | min 1 | — | — | `modifyOrder` body |
| Eligibility declaration `addLines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `modifyOrder` body |
| Age band `addLines[].eligibilityDeclaration[].ageBand` | radio group | optional | — | Infant · Child · Junior · Adult · Senior | — | Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+. | `modifyOrder` body |
| Age years `addLines[].eligibilityDeclaration[].ageYears` | number field | optional | — | — | — | — | `modifyOrder` body |
| Height band index `addLines[].eligibilityDeclaration[].heightBandIndex` | number field | optional | — | — | — | — | `modifyOrder` body |
| Confident swimmer `addLines[].eligibilityDeclaration[].confidentSwimmer` | toggle | optional | — | — | — | Derived, kept for the gate check (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this … | `modifyOrder` body |
| Guardian signed `addLines[].eligibilityDeclaration[].guardianSigned` | toggle | optional | — | — | — | — | `modifyOrder` body |
| Quoted unit price `addLines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `modifyOrder` body |
| Holder name `addLines[].holderName` | text field | optional | — | — | — | — | `modifyOrder` body |
| Data mask values `addLines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `modifyOrder` body |
| Remove lines `removeLineIds` | multi-picker: choose remove lines | optional | — | — | — | — | `modifyOrder` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `modifyOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `modifyOrder` body |

Errors to draw in the form: 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem)

**Form: Reprint order** (modal, opened by *Reprint order*; *Reprint order* calls `reprintOrder`, *Cancel* sends nothing)

**Collects what `reprintOrder` sends before it is called.** Required: `delivery`, `recordedAt`. Optional: `destination`, `lineIds`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Delivery `delivery` | radio group | required | — | Print · Email · SMS · Whatsapp · Wallet | — | — | `reprintOrder` body |
| Destination `destination` | text field | optional | — | — | — | — | `reprintOrder` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to reprint every line. | `reprintOrder` body |
| Reason `reason` | radio group | optional | — | Printer fault · Guest request · Lost ticket · Not received · Other | — | — | `reprintOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the till reprinted — device time, as for every offline-capable write. | `reprintOrder` body |

Errors to draw in the form: 400 Validation failed

**Form: Reschedule order** (modal, opened by *Reschedule order*; *Reschedule order* calls `rescheduleOrder`, *Cancel* sends nothing)

**Collects what `rescheduleOrder` sends before it is called.** Required: `targetPerformanceId`, `recordedAt`. Optional: `lineIds`, `waiveFee`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target performance `targetPerformanceId` | picker: choose a target performance | required | — | — | shows names, sends the id | — | `rescheduleOrder` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to move the whole order. | `rescheduleOrder` body |
| Waive fee `waiveFee` | toggle | optional | off | — | — | — | `rescheduleOrder` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `rescheduleOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `rescheduleOrder` body |

Errors to draw in the form: 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem)

**Sent by *Void order*** (`voidOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of this void, and its idempotency key — it must equal the `Idempotency-Key` header. | `voidOrder` body |
| Reason `reason` | select | required | — | Guest changed mind · Entered in error · Item unavailable · Quality issue · Duplicate · Other | — | The void reason list (decided 28 September, audit R125 (4)): the one list `voidOrder` takes, and the list `fnb.amendFnbOrder` and `fnb.cancelFnbOrder` point to. | `voidOrder` body |
| Note `note` | text area | optional | — | min length 3; max length 500; Required when `reason` is `other` (audit R222); optional otherwise. | — | Required when `reason` is `other` (audit R222); optional otherwise. | `voidOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `voidOrder` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **kind-specific fields**: School shows year group and access and dietary needs; party shows celebrant name and age; corporate neither. *(source: contracts/spine/orders.yaml#createGroupBooking)*

#### Outputs: what the screen shows and produces

**Shown**

**Every order** (data table, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |

**Every refund** (data table, from `listOrderRefunds`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | — |
| Batch | the name it points at, never the id | The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own. |
| FX rate | text | The rate on the original payment, not today's (BL-087, CF-118). `Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the … |
| Tax reversal entry | the name it points at, never the id | A refund reverses the tax entry it created, and this is where that is stated rather than implied. |
| Settle to | chip: Original tender, Advance balance, Wire transfer, Store credit | BL-086. A refund could only go back the way it came. |
| FX variance | AED 1,234.50 | Where the sale rate and the current rate differ, the difference is booked as an FX variance rather than hidden in the refund. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied percentage | 1,234.5 | From the venue's time bands, or an approver override. |
| Status | chip: Pending approval, Pending gateway, Completed, Declined, Failed | — |
| Reason | text | — |
| Requested by principal | the name it points at, never the id | — |

**The selected order** (detail panel, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |
| Principal | the name it points at, never the id | The cashier who raised it — what the held-orders list shows. |
| Hold label | text | As `Order.holdLabel`. |
| Held until | 1 Oct 2026, 14:30 | As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse. |

**The group booking** (detail panel, from `getGroupBooking`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: General, School, Corporate, Party | — |
| Package product | text | The school-trip format or party package. |
| Year group | text | — |
| Access and dietary needs | text | — |
| Celebrant name | text | The birthday child. |
| Celebrant turning age | 1,234 | — |
| Allergies and requests | text | — |
| Final headcount due by | 1 Oct 2026, 14:30 | — |
| Quote sent at | 1 Oct 2026, 14:30 | — |
| Risk assessment sent at | 1 Oct 2026, 14:30 | — |
| Preferred date | 1 Oct 2026 | The date the guest asked for on `requestGroupBooking` — what its `409 dateUnavailable` is checked against. |
| Order | the name it points at, never the id | — |
| Leader subject | the name it points at, never the id | — |
| Organisation name | text | — |
| Expected size | 1,234 | — |

**The order statement** (detail panel, from `getOrderStatement`)

| Shows | Format | Notes |
|---|---|---|
| Order | the name it points at, never the id | — |
| Order number | text | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Entries | list or chips (count when long) | Sequential. What an agent reads to a guest asking about a charge. |
| Total paid | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total refunded | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Current balance | AED 1,234.50 | Positive means the guest owes; negative means a refund is outstanding. |

**The order** (detail panel, from `getOrder`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client UUIDv7 from `CreateOrderRequest.id`. |
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total price variance | AED 1,234.50 | Sum across lines. Zero on a normal order. |
| Lines | list or chips (count when long) | — |
| Payments | list or chips (count when long) | — |
| Principal | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Create order (primary button) | `createOrder` POST `/orders` | CreateOrderRequest | Order | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the … | opens modal first |
| Apply manual discount (secondary button) | `applyManualDiscount` POST `/orders/{orderId}/discounts` | ManualDiscountRequest | Order | 403 Above the cashier's limit and no approver supplied (`approverRequired`), or the approver is the requester (`approverIsRequester`). (OrderRefusedProblem) | opens modal first |
| Create refund (secondary button) | `createRefund` POST `/orders/{orderId}/refunds` | CreateRefundRequest | Refund | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Second authorisation required and absent (`secondAuthorisationRequired`), refund window closed (`refundWindowClosed`), or the amount … | opens modal first |
| Exchange order lines (secondary button) | `exchangeOrderLines` POST `/orders/{orderId}/exchanges` | ExchangeOrderRequest | OrderExchangeResult | 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem) | opens modal first |
| Hold order (secondary button) | `holdOrder` POST `/orders/{orderId}/hold` | inline | Order | 409 Order is already paid (`alreadyPaid`) or voided (`orderVoided`) — only a `pending` order is parked — or a seated line's lease ends before `holdUntil` … (OrderRefusedProblem) | opens modal first |
| Modify order (secondary button) | `modifyOrder` POST `/orders/{orderId}/modify` | ModifyOrderRequest | OrderModificationResult | 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem) | opens modal first |
| Reprint order (secondary button) | `reprintOrder` POST `/orders/{orderId}/reprints` | inline | inline | 400 Validation failed | opens modal first; produces a document or message: Reprint or resend tickets |
| Reschedule order (secondary button) | `rescheduleOrder` POST `/orders/{orderId}/reschedule` | inline | OrderExchangeResult | 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem) | opens modal first |
| Resume order (secondary button) | `resumeOrder` POST `/orders/{orderId}/resume` | — | OrderResumeResult | 409 Held order expired (`holdExpired`), or already resumed at another till (`alreadyResumed`). (OrderRefusedProblem) | — |
| Void order (destructive button) | `voidOrder` POST `/orders/{orderId}/voids` | inline | Order | 409 Settled — a payment on the order has been `captured`, so the money has moved (`alreadySettled`) — or taken in a shift that is now closed (`shiftClosed`). (OrderRefusedProblem) | — |
| Create group booking (secondary button) | `createGroupBooking` POST `/group-bookings` | CreateGroupBookingRequest | GroupBooking | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 The order already has a group booking (`orderAlreadyGrouped`), or is voided (`orderVoided`), or `groupQuoteId` names a quote that … | opens modal first |
| Save group booking (secondary button) | `updateGroupBooking` PATCH `/group-bookings/{groupBookingId}` | UpdateGroupBookingRequest | GroupBooking | 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The status change goes backwards … | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **group header**: Confirmed size against minimum size as the headline; confirming below the minimum is allowed and recorded. *(source: contracts/spine/orders.yaml#updateGroupBooking / contracts/spine/orders.yaml#getGroupBooking)*

**Data it reads**: `listOrders` (onLoad, List orders)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*; carries `variantId`

**What opens over it**

- confirmDialog *Void order*: **Names what `voidOrder` changes and what it leaves alone**, in the consequence rather than the verb. A group bookings this affects should be identified in the dialog, not just counted. **Collects what `voidOrder` sends before it is called.** Required: `id`, `reason`, `recordedAt`. `reason` is the …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group bookings list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group bookings untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group bookings yet. Offers Create group booking (`createGroupBooking`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, principalId, shiftId, status, createdFrom, createdTo and the group bookings are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getGroupBooking` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the client priced from is beyond its … (OrderRefusedProblem); 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem); 409 Held order expired … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
group:
  kind: school
  name: Al Noor Academy Grade 5
  leader: Ms. Huda Karim
  minimum: 25
  confirmed: 31
  finalHeadcountDueBy: '2026-11-20'
```

#### Permissions

- `createGroupBooking` → `ORDER_CREATE` (operate) · staff
- `getGroupBooking` → `ORDER_VIEW` (read) · staff, guest
- `updateGroupBooking` → `ORDER_MODIFY` (operate) · staff
- `listOrders` → `ORDER_VIEW` (read) · staff, guest, partner
- `createOrder` → `ORDER_CREATE` (operate) · staff, guest, partner
- `applyManualDiscount` → `ORDER_DISCOUNT` (operate) · staff, partner
- `createRefund` → `ORDER_REFUND` (operate) · staff, partner
- `exchangeOrderLines` → `ORDER_EXCHANGE` (operate) · staff, partner
- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `getOrderStatement` → `ORDER_VIEW` (read) · staff, partner
- `holdOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `listOrderRefunds` → `ORDER_VIEW` (read) · staff, partner
- `modifyOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `reprintOrder` → `ORDER_REPRINT` (operate) · staff, guest, partner
- `rescheduleOrder` → `ORDER_RESCHEDULE` (operate) · staff, partner
- `resumeOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `voidOrder` → `ORDER_VOID` (operate) · staff, partner

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getGroupBooking` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

77 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.3.7 | The system should allow access to their purchase history and ongoing orders and preferences. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 5.9.4 | The system should be able to provide a detailed log of transactions for each till. Detailed log of transaction should be always accessible, searchable and printable at back office. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 22.2.11 | Ticketing History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.12 | Membership History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.15 | Reservation History | Marketing & CRM | CONTRACTED | `listOrders` |
| 2.1.6 | This system should provide a Ticketing POS solution that enables the operator to sell all the tickets defined in the system including multi-day and combo tickets. The POS solution must also support … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.7.29 | The system should be able to offer ticket sales to various outside business entities through the use of the exposed APIs and dedicated modules. Examples of typical clients that would have discounts … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.7.30 | The system should cater to multiple ways of enabling B2B clients, resellers and partner distribution channels to resell tickets and services offered by the client: - Web-based solution for B2B … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.8.1 | The system should provide an application for call center agents to make new ticket purchases, modify existing ticket purchases and offer refunds for guests. Any modifications done should follow the … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.8.2 | The system should allow call center agents to: - Make ticket sales including individual seat selection. - Look up existing orders after guest verification. - Change demographic data on existing … | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.12.25 | Each order has a unique number. | Ticketing Sales | CONTRACTED | `createOrder` |
| 2.11.11 | The system should correctly allocate the upgrade transaction to the sales channel it was processed on. Upgrade sales channel can be different from the purchase sales channel. | Ticketing Sales | CONTRACTED | `createOrder` |
| … 65 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group bookings: one shared QR for the whole group (redeemed together at the counter) or one QR per person, each of which the guest can link to their own profile in the mobile app. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-289)*
- Group tickets can carry one shared QR code or individual QR codes, with partial check-in tracking; family tickets bundle adult/child pricing. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-137)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-026` · status **notStarted** · provenance generated · **Drawn by Claude Design on `Seat Platform Board 7.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been …
- Derived from `wireframes/reference/Seat Platform Board 7.dc.html`
- Client design-board frames: `Seat Platform Board 7.dc.html#seatp-7e`

#### Acceptance for the design

- [ ] Every input above is drawn (158), with its required mark, default, format and its error state (400, 403, 404, 409, 412, 422).
- [ ] Every output is drawn (69 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-026?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create order, Apply manual discount, Create refund, Exchange order lines, Hold order, Modify order, Reprint order, Reschedule order, Resume order, Void order, Create group booking, Save group booking.
- [ ] Every transition is wired: `BO-008`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_REFUND`, `ORDER_REPRINT`, `ORDER_RESCHEDULE`, `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-027` Reissue & Media Replacement

**Replace media a guest has lost or damaged.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 2 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_EXCHANGE`, `ORDER_VIEW`, `SCOPE_VIEW` (2 operate, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | statusTracker (compact density): `getMediaEntitlements` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `mediaCode` (deepLink), `mediaId` (deepLink), `credentialId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/reissue-media-replacement` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **8 assets operations removed 18 August (CF-114).** The whole media contract was attached to this screen. **A till adding an item to a ticket does not manage a media library** — it reads the asset it needs and nothing else. Same shape as CF-87, one level up: that attached sibling operations, this attached a whole contract. **Absorbed BO-320 and BO-652 on 28 September (audit R276)**: Ticket Reissue & Fulfillment Regeneration brought `listTicketReissueFulfillment` (the reissue history of an order's tickets) and Credential Replacement & Reissue brought `listCredentialReplacementReissue` (lost, damaged and stolen credentials replaced); both are retired, and their hubs BO-314 and BO-644 open this screen.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-025): getMediaAsset and replaceMediaAsset are the image library; media here is a ticket credential, and the replacement act was missing: replaceCredential (access) … Removed 2 October 2026 (CHG-WIR-025): getMediaAsset and replaceMediaAsset are the image library; media here is a ticket credential, and the replacement act was missing: replaceCredential (access) …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Replace media a guest lost or damaged: see what is on the media, issue a replacement that carries the same entitlements, revoke the old one.

**Known correction pending (do not draw the wrong version)**

- **No operation reissues or replaces a credential; only lists are declared.** Why: The replacement act is missing. *(source: contracts/spine/orders.yaml#listTicketReissueFulfillment / contracts/spine/access.yaml#listCredentialReplacementReissue; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) listTicketReissueFulfillment, listCredentialReplacementReissue return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listTicketReissueFulfillment, listCredentialReplacementReissue carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listTicketReissueFulfillment / contracts/spine/access.yaml#listCredentialReplacementReissue; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Fixed on main** (the package already carries these; draw what it says): getMediaAsset and replaceMediaAsset (the image library) are on a ticket media replacement screen. (CHG-WIR-025).

#### Inputs: what the user enters or picks

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

**Form: Replace media** (modal, opened by *Replace media*; *Replace media* calls `replaceCredential`, *Cancel* sends nothing)

**Collects what `replaceCredential` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Lost · Stolen · Damaged · Compromised · Customer changed phone · RFID failure · Wristband replacement · QR compromise · Wallet replacement · Face re enrollment · Incorrect assignment | — | — | `replaceCredential` body |
| New media kind `newMediaKind` | text field | optional | — | — | — | Media type of the replacement (`MediaTypeTechnologyLibraryView.mediaType`); empty keeps the current kind | `replaceCredential` body |
| New media code `newMediaCode` | text field | optional | — | — | — | Code of the new physical media where one is encoded at the counter | `replaceCredential` body |
| Approval request `approvalRequestId` | picker: choose an approval request | optional | — | — | shows names, sends the id | The granted approval, where the replacement rule requires one | `replaceCredential` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `replaceCredential` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 replacement-limit, or approval-required, or the credential is revoked

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

**Ticket reissues** (data table): Carried from BO-320 (merged 28 September, audit R276) — tickets and media regenerated after an amendment, correction, loss or delivery failure. **Cursor pagination, never offset.**

**Credential replacements** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows. Carried from BO-652 (merged 28 September, audit R276).

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Append entitlement to media (primary button) | `appendEntitlementToMedia` POST `/media/{mediaCode}/entitlements` | AppendEntitlementRequest | AppendEntitlementResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Media expired (`mediaExpired`), blocked (`mediaBlocked`), already surrendered at exit (`mediaSurrendered`), or … | opens modal first; produces a document or message: Add something to a ticket the guest already holds |
| Replace media (secondary button) | `replaceCredential` POST `/credentials/{credentialId}/replace` | CredentialReplacementInput | CredentialOperationsCommandCenterView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 replacement-limit, or approval-required, or the credential is revoked | step-up: mfa (Moves a paid ticket onto new media; the old one stops working.); opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **media contents**: What the media holds (entitlements, remaining entries, wallet) before reissue. *(source: contracts/spine/orders.yaml#getMediaEntitlements)*

**Data it reads**: `getMediaEntitlements` (onLoad, What is already on this media); `listTicketReissueFulfillment` (onLoad, Ticket reissue and fulfilment regeneration history …); `listCredentialReplacementReissue` (onLoad, Credential replacement, reissue, revocation and recovery …)

**Where the user goes next**

- → `BO-314` Amendment & After-Sales Command Center: *Back to Amendment & After-Sales Command Center*
- → `BO-644` Credential Issuance Command Center: *Back to Credential Issuance Command Center*
- → `BO-008` Product Detail & Variants: *Product Detail & Variants*; carries `variantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reissue media replacement, read by `getMediaEntitlements`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reissue media replacement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reissue media replacement yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | The ticket reissue or credential replacement history for this media has nothing matching; the media itself is still shown. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getMediaEntitlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Media expired (`mediaExpired`), blocked (`mediaBlocked`), already surrendered at exit (`mediaSurrendered`), or the entitlement cannot share media … (AppendRefusedProblem); 409 replacement-limit, or approval-required, or the credential is revoked |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
media:
  code: WB-0098812
  type: wristband
  holds:
  - Day Pass Adult (used 1 of 1)
  - Locker 214
  replacement: WB-0098844
```

#### Permissions

- `getMediaEntitlements` → `ORDER_VIEW` (read) · staff
- `appendEntitlementToMedia` → `ORDER_CREATE` (operate) · staff
- `listTicketReissueFulfillment` → `ORDER_VIEW` (read) · staff
- `listCredentialReplacementReissue` → `SCOPE_VIEW` (read) · staff
- `replaceCredential` → `ORDER_EXCHANGE` (operate) · staff · step-up mfa

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getMediaEntitlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

22 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 10 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-027` · status **notStarted** · provenance generated
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 12: Works in Reissue & Media Replacement (Ticket Reissue & Fulfillment Regeneration, merged into it on 28 September, audit … → Manage ticket/media regeneration following an amendment, correction, loss, delivery failure, or other authorized event.
- Flow F220 *ACCREDITATION board 4: Credential Issuance Command Center*, step 16: Works in Reissue & Media Replacement (Credential Replacement & Reissue, merged into it on 28 September, audit R276) → Securely manage lost, damaged, stolen or incorrectly issued credentials.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-027?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Append entitlement to media, Replace media.
- [ ] Every transition is wired: `BO-314`, `BO-644`, `BO-008`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_EXCHANGE`, `ORDER_VIEW`, `SCOPE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-028` Refund Approval Queue

**Approve the refunds a cashier is not allowed to make alone.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_REFUND_APPROVE` (1 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the screen declares only writes (`createRefundRequest`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | `refundId` (navigation) |
| Route | `/venue-operations/refund-approval-queue` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-025): The Refund Approval Queue's only operation was createRefundRequest, the guest's own refund request (guest audience, no permission); a staff approval queue … Contract gap recorded 2 October 2026 (CHG-WIR-027): No read lists refunds held for approval across orders.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The queue of refunds a cashier may not make alone and guest-initiated refund requests, for an approver to decide.

**Fixed on main** (the package already carries these; draw what it says): The approval queue declares only the guest's create operation (no permission), no list and no decision. (CHG-WIR-025); No read operation: the screen declares only createRefundRequest and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Form: Approve refund** (modal, opened by *Approve refund*; *Approve refund* calls `approveRefund`, *Cancel* sends nothing)

**Collects what `approveRefund` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Note `note` | text area | optional | — | max length 500 | — | — | `approveRefund` body |
| Override percentage `overridePercentage` | stepper or slider | optional | — | min 0; max 100 | — | Approver may override the time-banded refund percentage. Recorded against the approving principal. | `approveRefund` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 409 The refund is not waiting for approval (`notPendingApproval`) — it was already approved, declined, completed or failed. (RefundPolicyProblem)

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve refund (secondary button) | `approveRefund` POST `/refunds/{refundId}/approve` | inline | Refund | 403 Authenticated but not permitted at the requested scope; 409 The refund is not waiting for approval (`notPendingApproval`) — it was already approved, declined, completed or failed. (RefundPolicyProblem) | step-up: mfa (Money leaves. The one approval a compromised session is most obviously worth taking.); opens modal first |
| Approve refund (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **queue**: Requested by, amount, reason, policy result, age; oldest first. *(source: contracts/spine/orders.yaml#createRefundRequest / DI-252)*

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Figures load; the expected total renders last |
| Error (`?state=error`) | **Could not load. Every action that moves money is blocked** — a figure nobody read must not be reconciled against |
| Empty, first run (`?state=emptyFirstRun`) | Nothing in the period — reported as a result, not an empty screen |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The refund is not waiting for approval (`notPendingApproval`) — it was already approved, declined, completed or failed. (RefundPolicyProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
request:
  order: DP-2026-104901
  amount: AED 1,240.00
  reason: Child unwell, visit cancelled
  requestedBy: Guest app
  policy: 50% band
```

#### Permissions

- `approveRefund` → `ORDER_REFUND_APPROVE` (operate) · staff · step-up mfa

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.7.91 | The system shall support the complete refund lifecycle including refund request, approval, processing, settlement, completion, rejection, and cancellation. Track reason, approver, payment method … | F&B & Guest Management | CONTRACTED | `approveRefund` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Refund-requests screen lists customer-initiated online requests awaiting a finance/operations decision: accept, request more information, or auto-deny. *(agreed · MoM 12 Aug 2026, 18. Bulk Refund Processing and Refund Requests · DI-270)*
- Bulk refunds: select and refund at event or date level (e.g. ~5,000 transactions for a cancelled event), online and on-site bookings, with one approval step before processing. *(agreed · MoM 12 Aug 2026, 18. Bulk Refund Processing and Refund Requests · DI-269)*
- Guests can request a refund from their account/profile; operations are notified and can approve, reject or ask for more information. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-254)*
- A refund started at the POS is routed for approval before it reaches the bank. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-253)*
- Refunds use preset time-banded percentages (e.g. full refund a set number of days before the event, less closer to/after it), support partial refunds, and let an authorised approver apply a custom override percentage. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-252)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A75** Design the refund engine: a six-step ledger-to-gateway refund flow with configurable time-banded percentages, an authorized-approver override, partial refunds, both operations- and customer-initiated requests, plus bulk … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 12 Aug 2026 · workshop tracker · keyword 'refund')*
- **A80** Implement a currency-locking rule for refunds/change: always issue in the local/base currency, locked at the value recorded at time of purchase; track foreign-currency activity only via a separate report *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 14 Aug 2026 · workshop tracker · keyword 'refund')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'refund')*
- **A140** Centralise policy management (reschedule, exchange, refund, cancellation, upgrade, downgrade, ownership transfer, membership conversion) with each product mapped to pricing, GL code, promotions and channels *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'refund')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'refund')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-028` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-028?state=<state>`: loading, error, emptyFirstRun, offline.
- [ ] Every action is wired with its success and its failure: Approve refund, Approve refund.
- [ ] Every transition is wired: `BO-008`.
- [ ] Every gated control is gated: `ORDER_REFUND_APPROVE`.
- [ ] The 5 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-029` Report Builder

**Build the report nobody wrote down, without asking for a release.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 2 · needs the `analytics` module |
| Block | Block A · ticket #20785 (APP-SETUP-BO-029) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_VENUE` (1 configure, 1 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listReports` reads the population and `getFinancialReport` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `conversationId` (deepLink), `reportId` (deepLink) · cold entry: A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. |
| Route | `/venue-operations/report-builder` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **One reporting area, one set of numbers** (decided 2 October 2026, Chinmay; CHG-FIN-006; DI-721, DI-702). This screen is a scoped window onto the reporting area (Analytics, P16): it runs the same seeded report definitions and reads the same seeded KPIs, so its figures equal what Analytics shows for the same scope, period and as-of time. It computes no total of its own and shows the as-of time on every figure. **One reporting area (DI-721, DI-702; decided 8 September and again 2 October 2026 for the finance dashboard, DEC-219):** this builder is the same reporting surface as Venue Analytics (P16), opened from Orders & Money with the venue's reports; it does not keep its own copy of definitions.

**Known gaps.** Statutory statements (P&L, balance sheet, cash flow) are not part of a report builder; they are the finance close's (design-note correction finance-insights BO-029, CHG-SBO-012).

**From the Finance, Ledger & Tax · Reporting & Analytics process.** A venue user builds a report nobody wrote down, without a release: pick a dataset from the business catalogue, choose columns, filters, grouping and run-time prompts, preview, save, run. The one thing to get right: it is the same builder as the analytics app's report builder, not a second one, and it never exposes tables, joins or SQL.

**Fixed on main** (the package already carries these; draw what it says): The no-access state names the venue report-view permission, and the screen loads a P&L. (CHG-SBO-012); A second report builder in the back office. (CHG-SBO-012).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Do advanced users get SQL or scripting templates (12 August) or is it strictly no-code (8 September)?** → Drawn default accepted: No-code only, as the later decision says. *(decided by Chinmay, 2026-10-02; DEC-081 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Category | select | optional | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | — | Sends `?category=` to `listReports`. | `listReports` ?category |
| Search | text field | optional | — | — | — | Sends `?search=` to `listReports`. | `listReports` ?search |

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

**Form: Ask reporting question** (modal, opened by *Ask reporting question*; *Ask reporting question* calls `askReportingQuestion`, *Cancel* sends nothing)

**Collects what `askReportingQuestion` sends before it is called.** Required: `question`. Optional: `conversationId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Question `question` | text area | required | — | min length 3; max length 1000 | — | — | `askReportingQuestion` body |
| Conversation `conversationId` | text field | optional | — | — | — | Continue a prior exchange for follow-up questions. | `askReportingQuestion` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows the answer to one venue. Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | `askReportingQuestion` body |

Errors to draw in the form: 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope

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

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Dataset**: From the published business catalogue only (certified datasets such as Sales, Orders, Admissions); shows what one row means. *(source: contracts/satellite/reporting.yaml#getSemanticModel / DI-708 / MATRIX 8.7.11 / MATRIX 6.1.78)*
- **Who can see this report**: A plain choice (Own figures / Workstation / Venue / Region / Whole company) that maps to the report-view permission tier; never a permission key typed by the user. *(source: contracts/satellite/reporting.yaml#createReport / contracts/shared/permissions.yaml#/components/schemas/Permission)*
- **Maximum date range**: In days; bounds every run of this report so a year-long query cannot be started by accident. *(source: MATRIX 6.1.19)*
- **Prompts (parameters)**: Filters marked "ask when run" become the inputs a runner fills (date range, channel, operating area). *(source: contracts/satellite/reporting.yaml#/components/schemas/ReportParameter / DI-183)*

#### Outputs: what the screen shows and produces

**Shown**

**Every report definition** (data table, from `listReports`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Category | chip: Sales, Admission, Financial, Inventory, Guest, Operations… | — |
| Data source | chip: Orders, Order lines, Payments, Refunds, Shifts, Scan events… | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over … |
| Columns | list or chips (count when long) | — |
| Filters | list or chips (count when long) | — |
| Group by | list or chips (count when long) | — |
| Parameters | list or chips (count when long) | — |
| Required permission | chip: SESSION FORCE LOGOUT, USER MANAGE, ROLE MANAGE, PERMISSION GRANT, PERMISSION VIEW … | Permission needed to run this report, from the shared `Permission` vocabulary. The author cannot assign one they do not hold — otherwise a … |
| Max date range days | 1,234 | Guards against a query spanning years of scan events. When a report sets none, 366 days applies (decided 28 September, audit R158), so … |
| ID | the name it points at, never the id | — |
| Is system | yes / no (icon or chip) | Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). Clone-only (decided 28 September, audit R096): `updateReport` … |

**The selected report definition** (detail panel, from `getReport`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Category | chip: Sales, Admission, Financial, Inventory, Guest, Operations… | — |
| Data source | chip: Orders, Order lines, Payments, Refunds, Shifts, Scan events… | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over … |
| Columns | list or chips (count when long) | — |
| Filters | list or chips (count when long) | — |
| Group by | list or chips (count when long) | — |
| Parameters | list or chips (count when long) | — |
| Required permission | chip: SESSION FORCE LOGOUT, USER MANAGE, ROLE MANAGE, PERMISSION GRANT, PERMISSION VIEW … | Permission needed to run this report, from the shared `Permission` vocabulary. The author cannot assign one they do not hold — otherwise a … |
| Max date range days | 1,234 | Guards against a query spanning years of scan events. When a report sets none, 366 days applies (decided 28 September, audit R158), so … |
| ID | the name it points at, never the id | — |
| Is system | yes / no (icon or chip) | Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). Clone-only (decided 28 September, audit R096): `updateReport` … |
| Is retired | yes / no (icon or chip) | — |
| Estimated cost | chip: Low, Medium, High | Informs whether it may run inline or must be queued. |
| Created by principal | the name it points at, never the id | — |
| Last run at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Create report (primary button) | `createReport` POST `/reports` | CreateReportRequest | ReportDefinition | 400 Unknown field, invalid filter, or estimated cost beyond the limit; 403 Author does not hold the permission they assigned to the report | opens modal first |
| Ask reporting question (secondary button) | `askReportingQuestion` POST `/reports/ask` | inline | NaturalLanguageAnswer | 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope | opens modal first |
| Delete report (destructive button) | `deleteReport` DELETE `/reports/{reportId}` | — | — | 409 Active schedules reference this report (`report-scheduled`), or it is a system report, which is clone-only (`system-report`, audit R096) | — |
| Run report (secondary button) | `runReport` POST `/reports/{reportId}/run` | RunReportRequest | ReportResult | 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope | opens modal first |
| Save natural language query (secondary button) | `saveNaturalLanguageQuery` POST `/reports/ask/{conversationId}/save` | inline | ReportDefinition | — | opens modal first |
| Save report (secondary button) | `updateReport` PUT `/reports/{reportId}` | CreateReportRequest | ReportDefinition | 409 The report is a system report, which is clone-only (audit R096). | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Preview**: First page of results with column totals; currency at its region decimals; "as of" time because results come from the reporting copy. *(source: contracts/satellite/reporting.yaml#runReport / DI-306)*
- **Versions**: Saving publishes a new version; earlier runs keep the version they used, so a past result stays reproducible. *(source: contracts/satellite/reporting.yaml#updateReport / MATRIX 6.1.43)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Save**: Creates or versions the definition; it appears in the report library. *(source: contracts/satellite/reporting.yaml#createReport)*
- **Retire**: Removes it from the library; past runs and their files remain. The confirmation names the schedules that use it. *(source: contracts/satellite/reporting.yaml#deleteReport)*
- **Ask in plain language**: Returns an answer with the query it used; "Save as report" turns it into a definition. *(source: F20 step 3 / contracts/satellite/reporting.yaml#saveNaturalLanguageQuery)*

**Data it reads**: `listReports` (onLoad, List available report definitions)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*

**What opens over it**

- confirmDialog *Delete report*: **Names what `deleteReport` changes and what it leaves alone**, in the consequence rather than the verb. A report this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the report untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report yet. Offers Create report (`createReport`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on category, search and the report are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | You don't have access to building reports — ask your venue manager for the report management access. Building and saving need it; viewing alone does not. **Never an empty table.** |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Question could not be interpreted. (ReportQuestionProblem); 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 400 Unknown field, invalid filter, or estimated cost beyond the limit; 409 Active schedules reference this report (`report-scheduled`), or it is a system report, which is clone-only (`system-report` … |

#### Edge cases to draw

- **A chosen field is personal data**: Marked as such; exporting it later needs the personal-data export permission and is audited. *(source: contracts/satellite/reporting.yaml#/components/schemas/SemanticModel / contracts/shared/permissions.yaml#/components/schemas/Permission)*
- **The run would return a very large result**: It runs in the background and notifies when ready; the screen never freezes. *(source: DI-710 / contracts/satellite/reporting.yaml#runReport)*

#### Consistency with other screens

- Match `ANL-032`: One reporting area: this screen should open the analytics report builder (or embed the same component) rather than be drawn twice.
- Match `BO-058`: Saved reports appear in the report library there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
report: 'Sales by operating area and payment method · dataset Sales · columns: date, operating area, workstation,
  payment method, gross sales, discounts, refunds · prompt: date range (max 31 days)'
```

#### Permissions

- `listReports` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `createReport` → `REPORT_MANAGE` (configure) · staff, partner
- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `deleteReport` → `REPORT_MANAGE` (configure) · staff, partner
- `getReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `saveNaturalLanguageQuery` → `REPORT_MANAGE` (configure) · staff, partner
- `updateReport` → `REPORT_MANAGE` (configure) · staff, partner

**A refused user sees:** You don't have access to building reports — ask your venue manager for the report management access. Building and saving need it; viewing alone does not. **Never an empty table.**

#### Requirements it meets

88 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.40 | System shall provide analytics and dashboards covering ticket sales, attendance, utilization, conversion rates, capacity utilization and revenue performance. | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.104 | Membership analytics | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.135 | Required Reports Operational Reports Donations by Campaign. Donations by Site. Donations by Product. Donations by Sales Channel. Donations by Date. Donations by User/Cashier. Donations by Payment … | Ticketing Catalogue | CONTRACTED | `createReport` |
| 3.2.65 | An Entry or Exit report is expected presenting the readings per outcome (ok/ko), per time and per access point. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.66 | The in park report showing the difference between the Entries and the Exits. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.68 | The length of stay report shall present the difference between the time in scan and the time out scan. | Admission and Access | CONTRACTED | `createReport` |
| 3.5.12 | System shall provide analytics showing bundle sales volume, revenue contribution, conversion rate, redemption rate, average order value impact, profitability, and performance by channel. | Admission and Access | CONTRACTED | `createReport` |
| 3.7.11 | System shall provide reporting on upsell impressions, conversion rates, revenue generated, average order value uplift, and campaign effectiveness across channels. | Admission and Access | CONTRACTED | `createReport` |
| 5.6.28 | Provide reporting on wait times, abandonment rates, no-shows, throughput, utilization, and satisfaction. | F&B & Guest Management | CONTRACTED | `createReport` |
| 6.1.5 | The system should be able to Generate reports with admission types/information. | Retail POS | CONTRACTED | `createReport` |
| 6.1.8 | The system should have the ability to retrieve information "on the fly" for items, (e.g., keyword, item #, description, category etc.) in user-friendly format such as pull-down menus and/or auto fill … | Retail POS | CONTRACTED | `createReport` |
| 6.1.9 | The system should be able to report historical sales look up by item, ticket number etc.. | Retail POS | CONTRACTED | `createReport` |
| … 76 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Custom report templates (advanced users, SQL/scripting) exported as PDF or Excel; ticket and receipt layouts built in a drag-and-drop template builder placing dynamic variables (guest name, ticket number, QR) on a background image. *(agreed · MoM 7 Aug 2026, 22. Report & Document Template Design · DI-184)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-029` · status **notStarted** · provenance generated
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)
- ADR-0059 *AI phasing against the six-month plan* (`docs/adr/0059-ai-phasing-against-the-six-month-plan.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (76), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-029?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create report, Ask reporting question, Delete report, Run report, Save natural language query, Save report.
- [ ] Every transition is wired: `BO-008`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-039` Shift Directory

**See every till, open or closed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_WORKSTATION`, `SCOPE_VIEW` (1 operate, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (compact density): `approveShiftOpen` decides items that `listShifts` queues — every row is waiting for a person, so the empty state is success |
| Offline | online only |
| Opens with | `shiftId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/venue-operations/shift-directory` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **A pending shift never blocks the next one (decided 2 October 2026 by Chinmay, DEC-059; CHG-CSP-012).** A cashier may sign out with the variance pending; the shift shows "Under review" on the cashier's view and the next cashier opens a shift on the same till. A supervisor closes or resolves shifts with their PIN at any till, on POS-007, or from the daily cash reconciliation (BO-043). Kept separate from BO-040 (DEC-172: keep both).

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): Till acts were bound to the back-office directory, including getCurrentShift ("the shift on the session's workstation", which a browser has not) and … Removed 2 October 2026 (CHG-WIR-008): Till acts were bound to the back-office directory, including getCurrentShift ("the shift on the session's workstation", which a browser has not) and … Removed 2 October 2026 (CHG-WIR-008): Till acts were bound to the back-office directory, including getCurrentShift ("the shift on the session's workstation", which a browser has not) and …

**From the Food, Beverage & Retail process.** A directory of every till session at the venue — open, on break, counting, waiting for a variance to be accepted, closed, auto-closed — for the duty manager, cash office and finance. It watches tills; it does not run them. One thing to get right: the blind count binds the cashier, not the back office — once a shift is counted, expected, counted and variance are shown here (the expected figure stays hidden until the count is in).

**Known correction pending (do not draw the wrong version)**

- **Pattern approvalInbox, table "Waiting for a decision", empty state "Nothing is waiting, which is the good outcome".** Why: It is a directory of all sessions; an empty list on a trading day is not success. *(source: screens/P08-venue-back-office.yaml#BO-039 / DI-273; Food, Beverage & Retail)*
- **Text fields "Workstation id" and "Status"; columns id, workstationId, venueId, scopePath, principalId, currency, currencyScale.** Why: Plumbing on a user's screen. *(source: screens/P08-venue-back-office.yaml#BO-039; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): Till acts are bound to the back-office directory: Open shift, Close shift, Suspend, Resume, Record no sale, Create cash movement, and … (CHG-WIR-008); "Accept shift variance" (acceptShiftVariance) is a button on BO-039. (CHG-WIR-008); Navigation exits to BO-008 "Product Detail & Variants"; entry state takes shiftId from the session; no entry from the Orders & Money hub. (CHG-WIR-009); DI-273 asks for open and closed sessions "with expected cash and card totals" and a live till monitor; the contract withholds expectedCash … (CHG-WIR-008).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **May a supervisor approve an out-of-tolerance opening float remotely from the back office, or only at the till?** → Drawn default stands (answer: "Back office too"): Draw "Approve opening float" here; the contract does not restrict it to the till. *(decided by Chinmay, 2026-10-02; DEC-171 / CHG-NOTE-004)*
- **Allam asked to explore merging shift-closing and till-closing screens; is BO-039 also the place for BO-040's list?** → Drawn default stands (answer: "Keep both"): Keep both (BO-040 is a filtered view of BO-039 with the variance columns first). *(decided by Chinmay, 2026-10-02; DEC-172 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Till | picker: choose an id | optional | — | — | shows names, sends the id | A pick list in words, never a typed id (design-note correction, 2 October 2026). | `Workstation.id` |
| Status | select | optional | — | Pending approval · Open · Suspended · Pending variance · Pending closure · Closed · Auto closed | — | Shift statuses in words; "Under review" is a counted shift waiting for a supervisor. | `Shift.status` |
| Opened from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedFrom=` to `listShifts`. | `listShifts` ?openedFrom |
| Opened to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedTo=` to `listShifts`. | `listShifts` ?openedTo |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listShifts` ?workstationId |
| Status | select | — | Pending approval · Open · Suspended · Pending variance · Pending closure · Closed · Auto closed | `listShifts` ?status |
| Sale board kind | radio group | — | Ticketing · Fnb · Retail · Mixed | `listWorkstations` ?saleBoardKind |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Till**: A picker of till names grouped by outlet/department, not a "Workstation id" text field. *(source: contracts/spine/shift.yaml#listShifts / R156)*
- **Status**: Chips with staff words for ShiftStatus: Awaiting approval (pendingApproval), Open, On break (suspended), Counting (pendingClosure), Variance to accept (pendingVariance), Closed, Auto-closed. Default all statuses. *(source: contracts/spine/shift.yaml#/components/schemas/ShiftStatus)*
- **Opened between**: One date-range control with presets Today (default), Yesterday, This week; times in GST. *(source: contracts/spine/shift.yaml#listShifts)*

#### Outputs: what the screen shows and produces

**Shown**

**Shifts** (data table, from `listShifts`)

| Shows | Format | Notes |
|---|---|---|
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |

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
| Deposit box | the name it points at, never the id | The box the cash moved in or out of. Set on every lift `withdrawFromDepositBox` records (26 September, pull audit R099). |
| Witness principal | the name it points at, never the id | The cashier who countersigned a withdrawal. Null on other movements. |
| Withdrawal reason | chip: Banking, Safe drop, Change order, Other | Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records. |
| Authorised by principal | the name it points at, never the id | The principal who authorised the movement, recorded for audit. |

**The shift** (detail panel, from `getShift`)

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

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Shift rows**: Till, Cashier, Status, Opened, Closed, Opening float, Sales, Refunds, Cash out, Counted, Variance (signed; short in red as "AED −40.00 short", over as "AED +5.00 over"), Deposit box / bag number. No ids, venue, scope path or currency-scale columns. Amounts use the region currency and its decimals (3 for BHD/KWD, third decimal never rounded). *(source: DI-273 / DI-306 / ADR-0018 / contracts/spine/shift.yaml#/components/schemas/Shift)*
- **Expected cash**: Empty for a shift not yet counted, shown as "— (revealed after count)"; filled once the count is in, together with counted and variance. Variance beyond the venue threshold (proposed AED 20.00) is flagged. *(source: R094 / contracts/spine/shift.yaml#closeShift)*
- **Exceptions badge**: Count of incidents (no-sales, drawer opened without a sale, overrides) per shift; a high no-sale count against few sales is emphasised. *(source: contracts/spine/shift.yaml#recordNoSale / contracts/spine/shift.yaml#/components/schemas/Shift)*
- **Shift detail**: Cash movements in sequence (float, cash out/in, safe drops), approvals (who approved the open, who accepted the variance, reason), suspend reason, closed-by when not the holder, held inventory leases on an open shift, and an "unsynced sales" warning while syncedAt is empty. *(source: contracts/spine/shift.yaml#listCashMovements / contracts/spine/shift.yaml#/components/schemas/Shift)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Approve opening float**: Only on Awaiting approval rows; reason required (3–300). The shift becomes Open and can trade. 409 when it is no longer waiting. *(source: contracts/spine/shift.yaml#approveShiftOpen / F32 step 1 / MATRIX 5.9.8)*
- **Reopen shift**: Only on Closed rows. Needs a supervisor who did not close it to enter their PIN on this device, plus a reason. Refusals say which: "You closed this shift — another supervisor must reopen it", "PIN not accepted", or "The fiscal period is closed". The first count is kept. *(source: R144 / contracts/spine/shift.yaml#reopenShift / MATRIX 5.9.5)*

**Data it reads**: `listShifts` (onLoad, List shifts); `getShift` (onLoad, Read a shift); `listCashMovements` (onLoad, Lifts, adds and the opening float); `listWorkstations` (onLoad, List workstations (the pick list))

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The shift list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the shift untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on workstationId, status, openedFrom, openedTo and the shift are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A shift auto-closed after the venue limit**: Labelled "Auto-closed — not counted"; it has no counted figure and is never shown as balanced. *(source: MATRIX 5.9.5)*
- **A shift closed with sales still journalled offline**: "Unsynced sales — settlement waits"; the variance is provisional until sync. *(source: F32 step 8)*
- **A shift waiting for a variance with no supervisor at the till**: Stays "Variance to accept" with time waiting; acceptance is not offered here. *(source: R080 / DI-805)*
- **One till, three cashiers in a day**: Three rows; each cashier answers for their own box and variance. *(source: F32 step 6 / contracts/spine/shift.yaml#listDepositBoxes)*

#### Consistency with other screens

- Match `POS-007`: Close, blind count and variance acceptance happen there; status words must match.
- Match `BO-040`: The "Variance to accept" rows are the same shifts BO-040 lists.
- Match `BO-041`: Shift detail movements use the same row format as Cash Movements.
- Match `POS-015`: The till-side live cash monitor; DI-273 asks for the same per-till view in both.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
shifts:
- till: Till 3 — Bite & Go
  cashier: Priya Nair
  status: Open
  opened: 06:58 GST
  float: AED 500.00
  sales: AED 6,240.00
  cash_out: AED 2,000.00
  expected: — (revealed after count)
- till: Till 1 — Main Gate ticket office
  cashier: Khalid Al Mansoori
  status: Variance to accept
  opened: 07:02
  closed: '15:05'
  expected: AED 8,480.00
  counted: AED 8,440.00
  variance: AED −40.00 short
- till: Till 2 — Marina Bay retail store
  cashier: Fatima Al Suwaidi
  status: Closed
  variance: AED +5.00 over
  accepted_by: none needed
```

#### Permissions

- `listShifts` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `getShift` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listCashMovements` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listWorkstations` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.44 | Incident & Exception Logging | Ticketing Sales | CONTRACTED | data `Shift` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Shift management: assignment and scheduling by cashier/department, templates and policies, opening/closing, exceptions/alerts. Allam: explore merging shift-closing and till-closing screens to reduce dashboard count. *(client request · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-309)*
- Shift/session view shows open and closed sessions per workstation with expected cash and card totals; a live till monitor shows real-time cash status per workstation and open/close codes. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-273)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-039` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (35 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-039?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `REPORT_VIEW_WORKSTATION`, `SCOPE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-040` Variance Approval

**See which tills are waiting for a variance to be accepted at the till, and which were.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `OVERSHORT_ACCEPT`, `REPORT_VIEW_WORKSTATION`, `SCOPE_VIEW`, `SHIFT_CLOSE` (3 operate, 1 read); in the flows as finance controller |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (compact density): `approveShiftOpen` decides items that `listShifts` queues — every row is waiting for a person, so the empty state is success |
| Offline | online only |
| Opens with | `shiftId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/venue-operations/variance-approval` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Where the variance goes** (decided 2 October 2026, Chinmay; CHG-FIN-003). The cashier counts blind (`submitShiftCount`) and never sees expected cash or the variance; a count beyond the venue threshold (`shiftVarianceThreshold`, proposed AED 20.00) alerts the supervisors holding OVERSHORT_ACCEPT on the venue's alerting channel and lands here. The supervisor sees counted, expected, the variance (over or short), the cashier's reason and note, and accepts it (`acceptShiftVariance`, never their own shift) or asks for a blind recount at the till. Over and short are both exceptions: an overage is as much a control failure as a shortage. **As POS-007 (decided 2 October 2026 by Chinmay, DEC-173):** the cashier signs out, the shift is "Under review", and the next cashier can start; the supervisor accepts, rejects for a recount, or closes.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): acceptShiftVariance on BO-040 contradicts R080 (e) and the contract itself ("BO-040 lists the shifts waiting here; it does not approve them by another route") … Removed 2 October 2026 (CHG-WIR-008): acceptShiftVariance on BO-040 contradicts R080 (e) and the contract itself ("BO-040 lists the shifts waiting here; it does not approve them by another route") … Removed 2 October 2026 (CHG-WIR-008): acceptShiftVariance on BO-040 contradicts R080 (e) and the contract itself ("BO-040 lists the shifts waiting here; it does not approve them by another route") …

**From the Food, Beverage & Retail process.** Since R080 (e) this is a watch list, not an approval screen. It lists the shifts whose count left a variance beyond the venue threshold, waiting for a supervisor to accept it on the till, and the history of variances accepted (who, when, why) for finance. A duty manager uses it to chase tills still waiting; finance uses it before month-end and for the over/short report. The one thing to get right: there is no Accept or Refuse button here — the screen says where the act happens.

**Fixed on main** (the package already carries these; draw what it says): Primary action "Accept shift variance" (acceptShiftVariance) on BO-040. (CHG-WIR-008); Bulk-attached till and lifecycle operations: Approve shift open, Close shift, Create cash movement, Open shift, Record no sale, Reopen … (CHG-WIR-008); Name "Variance Approval" and purpose "Accept or refuse a till that did not balance". (CHG-WIR-008); Flow F13 step 2 has the finance controller "clear outstanding shift variances" on BO-040 with acceptShiftVariance. (CHG-WIR-008); Pattern approvalInbox with columns id, workstationId, venueId, scopePath, currency; text filters "Workstation id", "Status"; exits to … (CHG-WIR-009).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **If no supervisor is available, may the cashier log out with the variance logged for later review?** → As POS-007: the cashier signs out, the shift is pending ('Under review') and the next cashier can start. *(decided by Chinmay, 2026-10-02; DEC-173 / CHG-NOTE-004)*
- **Must the variance be accepted on the same till the shift was counted on, or any till at the venue?** → Drawn default stands (answer: "Any till, with supervisor PIN"): Any till at the venue, with the supervisor's PIN (the contract names the shift, not the device). *(decided by Chinmay, 2026-10-02; DEC-174 / CHG-NOTE-004)*
- **The client asked that a supervisor can reject a variance so the cashier recounts and resubmits; the contract has accept only (reopen is the way back). Is reject needed?** → A supervisor can reject a variance so the cashier recounts and resubmits (DI-804). *(decided by Chinmay, 2026-10-02; DEC-175 / CHG-NOTE-004)*
- **Which screen shows the denomination breakdown of the closing count for review (no read returns the count lines)?** → Add a read for the closing count lines (denomination breakdown) for review. *(decided by Chinmay, 2026-10-02; DEC-176 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Till | picker: choose an id | optional | — | — | shows names, sends the id | A pick list in words, never a typed id (design-note correction, 2 October 2026). | `Workstation.id` |
| Status | select | optional | — | Pending approval · Open · Suspended · Pending variance · Pending closure · Closed · Auto closed | — | A pick list in words, never a typed id (design-note correction, 2 October 2026). | `Shift.status` |
| Opened from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedFrom=` to `listShifts`. | `listShifts` ?openedFrom |
| Opened to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedTo=` to `listShifts`. | `listShifts` ?openedTo |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listShifts` ?workstationId |
| Status | select | — | Pending approval · Open · Suspended · Pending variance · Pending closure · Closed · Auto closed | `listShifts` ?status |
| Sale board kind | radio group | — | Ticketing · Fnb · Retail · Mixed | `listWorkstations` ?saleBoardKind |
| Count kind | segmented control | — | Opening float · Close · Movement | `getShiftCountLines` ?countKind |

**Form: Accept variance** (modal, opened by *Accept variance*; *Accept variance* calls `acceptShiftVariance`, *Cancel* sends nothing)

**Collects what `acceptShiftVariance` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | Retained for audit. The accepting principal is recorded. | `acceptShiftVariance` body |

Errors to draw in the form: 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (problem type `approver-is-cashier`) — a cashier signing off their own …; 409 Shift is not `pendingVariance` (problem type `shift-not-pending-variance`) — within tolerance, still open, or already accepted.

**Form: Reject and recount** (modal, opened by *Reject and recount*; *Reject and recount* calls `rejectShiftVariance`, *Cancel* sends nothing)

**Collects what `rejectShiftVariance` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | Why a recount is needed, shown to the cashier. Never the amount: "Count the AED 100 notes again", not "you are AED 100 short". | `rejectShiftVariance` body |

Errors to draw in the form: 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (`approver-is-cashier`).; 409 Shift is not `pendingVariance` (`shift-not-pending-variance`), or a recount is already requested and not yet submitted (`recount-already-requested`).

**Form: Close shift** (modal, opened by *Close shift*; *Close shift* calls `closeShift`, *Cancel* sends nothing)

**Collects what `closeShift` sends before it is called.** Required: `countedCash`, `recordedAt`. Optional: `nonCashDeclared`, `notes`, `cashierReason`, `releaseHeldLeases`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Counted cash `countedCash` | repeatable rows | required | — | at least 1; A denomination may appear once; a repeat is refused with 422 `duplicate-denomination`. | — | The cashier's blind count, one line per denomination counted (decided 29 September, readiness close-out; our build plan). | `closeShift` body |
| Denomination `countedCash[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` (`Denomination.id`) — face value, kind and counting order live there. | `closeShift` body |
| Count `countedCash[].count` | number field | required | — | min 0; max 100000 | — | How many of this note or coin were counted. Zero is a line, not an omission: a denomination counted and found empty. | `closeShift` body |
| Total `countedCash[].total` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | `count` times the face value, in the denomination's currency. Optional on the way in (the server computes it) and checked when sent. | `closeShift` body |
| Non cash declared `nonCashDeclared` | repeatable rows | optional | — | — | — | Declared totals per non-cash tender, for reconciliation against captured payments. | `closeShift` body |
| Tender `nonCashDeclared[].tender` | text field | required | — | — | — | — | `closeShift` body |
| Amount `nonCashDeclared[].amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `closeShift` body |
| Notes `notes` | text area | optional | — | max length 1000 | — | The cashier's note on the count. Asked of every cashier on a blind count, never only after a variance is shown (CHG-FIN-003, DI-803). | `closeShift` body |
| Cashier reason `cashierReason` | radio group | optional | — | Till error · Unrecorded refund · Miscount · Other | — | Anything the cashier knows went wrong in the shift (DI-803: till error, unrecorded refund, miscount, other). | `closeShift` body |
| Release held leases `releaseHeldLeases` | toggle | optional | on | — | — | Return unsold inventory leases held by this workstation (ADR-0013 C103). Closing without releasing strands capacity until TTL expiry, which is visible at a gate during peak. | `closeShift` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `closeShift` body |

Errors to draw in the form: 400 Validation failed; 403 The caller is the cashier whose shift it is and does not hold OVERSHORT_ACCEPT (problem type `blind-count-required`): their count goes through …; 409 Shift is not `open` or `suspended` — already closing or closed (problem type `shift-not-open`) — or open orders remain (`open-orders-remain`); 422 A counted line names an unknown or inactive denomination (`unknown-denomination`), repeats one (`duplicate-denomination`), or sends a `total` that disagrees …

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **View**: Two tabs: "Waiting at the till" (status pendingVariance, default) and "Accepted" (closed shifts with a variance acceptance in their approvals). Optional "Waiting for close approval" (pendingClosure) where the venue supervises closes. *(source: contracts/spine/shift.yaml#approveShiftClose)*
- **Period**: Presets Today, This week, This fiscal period (for month-end); outlet/till picker; dates GST. *(source: F13 step 2 / contracts/spine/shift.yaml#listShifts)*

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listShifts`)

| Shows | Format | Notes |
|---|---|---|
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |
| Counted cash | AED 1,234.50 | What the close count found. Null until the shift is counted. |
| Expected cash | AED 1,234.50 | 26 September, pull audit R207. The figure the blind count was measured against, revealed once the count is in — null until then. |
| Variance | AED 1,234.50 | Counted minus expected, as `ShiftCloseResult.variance`. Negative is short. |
| Cashier reason | chip: Till error, Unrecorded refund, Miscount, Other | What the cashier said went wrong, given with the blind count (`CloseShiftRequest.cashierReason`, DI-803) without seeing the variance; the … |
| Cashier note | text | The cashier's note with the count (`CloseShiftRequest.notes`; CHG-FIN-003). |

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
| Deposit box | the name it points at, never the id | The box the cash moved in or out of. Set on every lift `withdrawFromDepositBox` records (26 September, pull audit R099). |
| Witness principal | the name it points at, never the id | The cashier who countersigned a withdrawal. Null on other movements. |
| Withdrawal reason | chip: Banking, Safe drop, Change order, Other | Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records. |
| Authorised by principal | the name it points at, never the id | The principal who authorised the movement, recorded for audit. |

**The shift** (detail panel, from `getShift`)

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
| Counted cash | AED 1,234.50 | What the close count found. Null until the shift is counted. |
| Expected cash | AED 1,234.50 | 26 September, pull audit R207. The figure the blind count was measured against, revealed once the count is in — null until then. |
| Variance | AED 1,234.50 | Counted minus expected, as `ShiftCloseResult.variance`. Negative is short. |
| Cashier reason | chip: Till error, Unrecorded refund, Miscount, Other | What the cashier said went wrong, given with the blind count (`CloseShiftRequest.cashierReason`, DI-803) without seeing the variance; the … |
| Cashier note | text | The cashier's note with the count (`CloseShiftRequest.notes`; CHG-FIN-003). |

**Count by denomination** (data table, from `getShiftCountLines`): **The denomination breakdown of the closing count (decided 2 October 2026 by Chinmay, DEC-176).** Counted figures only, never the expected amount (blind close).

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Shift | the name it points at, never the id | A UUIDv7, as `Shift.id` and `orders.pos_shift.id` are. |
| Deposit box | the name it points at, never the id | — |
| Count kind | chip: Opening float, Close, Movement | Which count this line belongs to — the opening float (`openShift`), the close (`closeShift`) or a lift or add (`createCashMovement`). |
| Cash movement | the name it points at, never the id | The movement this line counts, where `countKind` is `movement`. How `listCashMovements` rebuilds each movement's `denominations`. |
| Denomination | the name it points at, never the id | References `platform.denomination` — face value, kind and sort order live there. |
| Counted quantity | 1,234 | How many of this note or coin were in the drawer. |
| Counted value | AED 1,234.50 | Quantity times face value, stored. Derivable, and stored anyway: a denomination revalued or deactivated later would silently rewrite a … |
| Counted by | the name it points at, never the id | — |
| Counted at | 1 Oct 2026, 14:30 | — |
| Recount of | the name it points at, never the id | A recount points at what it replaces rather than overwriting it. `requestRecount` exists because a variance is a question before it is a … |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Accept variance (primary button) | `acceptShiftVariance` POST `/shifts/{shiftId}/accept-variance` | inline | Shift | 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (problem type `approver-is-cashier`) — a cashier signing off their own …; 409 Shift is not `pendingVariance` (problem type … | step-up: pin (A supervisor signs off a cashier's over/short in person, with their own PIN on the device they use (audit R080 (e); any …); opens modal first |
| Reject and recount (secondary button) | `rejectShiftVariance` POST `/shifts/{shiftId}/reject-variance` | inline | Shift | 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (`approver-is-cashier`).; 409 Shift is not `pendingVariance` (`shift-not-pending-variance`), or a recount is already requested and … | step-up: pin (The same supervisor act as accepting a variance, in person with their own PIN (audit R080 (e); DEC-175).); opens modal first |
| Close shift (secondary button) | `closeShift` POST `/shifts/{shiftId}/close` | CloseShiftRequest | ShiftCloseResult | 400 Validation failed; 403 The caller is the cashier whose shift it is and does not hold OVERSHORT_ACCEPT (problem type `blind-count-required`): their count goes through …; 409 Shift is not `open` or `suspended` — … | step-up: pin (A supervisor closes a cashier's shift and sees the expected cash and the variance (CHG-FIN-003); their own PIN on the …); opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Waiting rows**: Till, Cashier, Count submitted at, Expected, Counted, Variance (signed, "AED −40.00 short"), Over the threshold by (threshold proposed AED 20.00), Waiting for (minutes/hours), Cashier's note from the close. Oldest first. A row in a past fiscal period is marked "Blocks period close". *(source: R094 / DI-275 / F13 step 1 / contracts/spine/shift.yaml#closeShift)*
- **Non-cash variances**: Card/wallet declared versus captured, per tender, beside the cash variance. *(source: contracts/spine/shift.yaml#closeShift)*
- **Accepted rows**: Variance, accepted by (supervisor name), accepted at, reason; never the cashier's own name (approver-is-cashier). *(source: contracts/spine/shift.yaml#acceptShiftVariance)*
- **Where it is resolved**: Each waiting row carries the instruction "A supervisor accepts this on any till (Close Shift) with their PIN, or asks for a recount", not a button. *(source: R080 / F32 step 7 / decided 2 October 2026 by Chinmay (CHG-NOTE-004))*
- **Count breakdown**: The closing count by denomination (the shift's count lines), beside the totals, for review; a read of the count lines is to be added. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Open shift details**: Opens the shift in the Shift Directory with movements and approvals; no decision act on this screen. *(source: R080 / contracts/spine/shift.yaml#acceptShiftVariance)*

**Data it reads**: `listShifts` (onLoad, List shifts); `getShift` (onLoad, Read a shift); `listCashMovements` (onLoad, Lifts, adds and the opening float); `listWorkstations` (onLoad, List workstations (the pick list)); `getShiftCountLines` (onLoad, The closing count by denomination, for review (DEC-176 …)

**Where the user goes next**

- → `BO-089` Journal Entries: *Posts the remaining journals*; calls `listShifts`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The variance approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the variance approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on workstationId, status, openedFrom, openedTo and the variance approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Shift is not `open` or `suspended` — already closing or closed (problem type `shift-not-open`) — or open orders remain (`open-orders-remain`); 409 Shift is not `pendingVariance` (`shift-not-pending-variance`), or a recount is already requested and not yet submitted (`recount-already-requested`).; 409 Shift is not `pendingVariance` (problem type … |

#### Edge cases to draw

- **Variance exactly equal to the threshold**: Not listed — only a variance beyond the threshold waits. *(source: contracts/spine/shift.yaml#closeShift / R094)*
- **Supervisor is also the cashier of that shift**: Acceptance is refused on the till; the row stays waiting until another supervisor accepts. *(source: contracts/spine/shift.yaml#acceptShiftVariance)*
- **The cashier left with the variance unaccepted and no supervisor present**: The cashier signs out and the shift is pending ("Under review" on the cashier's view); the next cashier can open a shift. The row stays waiting with its age until a supervisor resolves it, and the daily cash reconciliation lists it. *(source: DI-805 / TRACKER 30-Sep/Tracker row 30 / TRACKER Workshops/Client Inputs row 59 / decided 2 October 2026 by Chinmay (CHG-NOTE-004))*
- **Month-end with a shift still waiting**: Shown as a period-close blocker with the till and supervisor to chase. *(source: F13 step 1)*
- **3-decimal currency venue (BHD/KWD)**: All amounts at 3 decimals, never rounded. *(source: DI-306)*
- **The supervisor does not accept the variance**: The supervisor asks for a recount (reject): the cashier counts blind again and resubmits through submitShiftCount; every count is kept and the latest is measured (DI-804). *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

#### Consistency with other screens

- Match `POS-007`: The till's close screen is where the variance is accepted; its wording for the variance must match this list.
- Match `BO-039`: Same shift rows filtered to variances; same column formats.
- Match `BO-090`: Period Close lists these shifts as blockers; the counts must agree.
- Match `BO-043`: Daily Reconciliation reports the accepted over/short (DI-275 example AED 8,480 vs 8,460).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
waiting:
- till: Till 1 — Main Gate ticket office
  cashier: Khalid Al Mansoori
  submitted: 15:05 GST
  expected: AED 8,480.00
  counted: AED 8,440.00
  variance: AED −40.00 short
  over_threshold_by: AED 20.00
  waiting: 38 min
  note: Possible unrecorded refund at 13:10
accepted:
- till: Till 4 — Oasis Bistro
  cashier: Daniel Brooks
  variance: AED −20.50 short
  accepted_by: Omar Ziad
  at: 23:14 GST
  reason: Miscount of 50 fils coins, recounted at the till
```

#### Permissions

- `listShifts` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `getShift` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listCashMovements` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listWorkstations` → `SCOPE_VIEW` (read) · staff
- `getShiftCountLines` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `acceptShiftVariance` → `OVERSHORT_ACCEPT` (operate) · staff · step-up pin
- `rejectShiftVariance` → `OVERSHORT_ACCEPT` (operate) · staff · step-up pin
- `closeShift` → `SHIFT_CLOSE` (operate) · staff · step-up pin

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.8.3 | The system should allow the cashier to enter a total amount counted, or to count by denomination. For denomination counts, the cashier counts and enters each denomination separately and each count is … | F&B & Guest Management | CONTRACTED | `closeShift` |
| 5.9.1 | The system should be able to manage end of day shift closing and provide the ability to close out each cash register. | F&B & Guest Management | CONTRACTED | `closeShift` |
| 5.9.2 | The system should have the ability to do a "blind" cashier close-out. Over-shorts should be captured and recorded. | F&B & Guest Management | CONTRACTED | `closeShift` |
| 5.9.5 | The system should allow automatic closing of a cashier's session after a configurable time period. The supervisor should be notified on closing of the session. | F&B & Guest Management | CONTRACTED | `closeShift` |
| 2.13.44 | Incident & Exception Logging | Ticketing Sales | CONTRACTED | data `Shift` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Blind cash-out: when closing, the cashier does not see the expected total; the system flags shortage/overage for supervisor review and can optionally block shift closure until the variance is resolved or explained. *(agreed · MoM 12 Aug 2026, 19. Cash/Shift and Till Management · DI-271)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-040` · status **notStarted** · provenance generated
- Flow F13 *Month end closes*, step 2: Clears outstanding shift variances → A shift left open in the period blocks the close
- Flow F13 branch at step 2 (recoverable): when FX revaluation is pending, Inter-entity obligations in a foreign currency must be revalued before the balance means anything.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (59 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-040?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Accept variance, Reject and recount, Close shift.
- [ ] Every transition is wired: `BO-089`.
- [ ] Every gated control is gated: `OVERSHORT_ACCEPT`, `REPORT_VIEW_WORKSTATION`, `SCOPE_VIEW`, `SHIFT_CLOSE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 6 edge case(s) from the process notes are drawn.
- [ ] The 4 decision(s) taken on this screen are drawn as decided, not as the old default.
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

### In P08 · Orders & Money

- AI-assisted reporting for accountants/finance managers is phase two; phase-one finance screens do not include it. *(agreed · MoM 12 Aug 2026, 6. Finance & Ledger Architecture Overview · DI-278)*
- Financial reports generated automatically: P&L (revenue per category less cost of sales), balance sheet, trial balance and ledger view, cash flow, revenue and deferred-revenue analytics, site-wise revenue; plus daily/weekly/monthly finance summaries. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-276)*
- Legal entities view lists all tenant sites with country, currency and active/inactive status. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-261)*
- Allam: Bulk QR option — for partners with no technical capability, the platform generates a bulk batch of tickets (e.g. 5,000) with a validity window, delivered as QR codes (e.g. CSV) for the partner to import and resell. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-135)*
- Full card numbers are never stored or shown; only a masked representation (e.g. last four digits) so the user can identify which card was used. *(agreed · MoM 31 Jul 2026, 10. Compliance & Data Protection · DI-069)*

**15 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"acceptShiftVariance": {"method":"POST","path":"/shifts/{shiftId}/accept-variance","contract":"shift","summary":"Accept an over/short beyond the threshold","permission":"OVERSHORT_ACCEPT","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"appendEntitlementToMedia": {"method":"POST","path":"/media/{mediaCode}/entitlements","contract":"orders","summary":"Add something to a ticket the guest already holds","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AppendEntitlementRequest","responds":"AppendEntitlementResult"},
"applyManualDiscount": {"method":"POST","path":"/orders/{orderId}/discounts","contract":"orders","summary":"Apply a discount a cashier chose","permission":"ORDER_DISCOUNT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ManualDiscountRequest","responds":"Order"},
"approveRefund": {"method":"POST","path":"/refunds/{refundId}/approve","contract":"orders","summary":"Approve a refund held for approval","permission":"ORDER_REFUND_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Refund"},
"askReportingQuestion": {"method":"POST","path":"/reports/ask","contract":"reporting","summary":"Natural-language reporting query","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"NaturalLanguageAnswer"},
"assignChargeback": {"method":"POST","path":"/chargebacks/{chargebackId}/assign","contract":"orders","summary":"Give a chargeback to an investigator, with a note","permission":"ORDER_REFUND_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Chargeback"},
"capturePayment": {"method":"POST","path":"/payments/{paymentId}/capture","contract":"orders","summary":"Capture a previously authorised payment","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Payment"},
"closeDepositBoxes": {"method":"POST","path":"/deposit-boxes/close","contract":"shift","summary":"Close one box or all of them","permission":"SHIFT_CLOSE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DepositBox"},
"closeShift": {"method":"POST","path":"/shifts/{shiftId}/close","contract":"shift","summary":"Blind close-out","permission":"SHIFT_CLOSE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CloseShiftRequest","responds":"ShiftCloseResult"},
"createBulkRefund": {"method":"POST","path":"/refunds/bulk","contract":"orders","summary":"Refund every order against an event, performance or date","permission":"ORDER_REFUND_BULK","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createGroupBooking": {"method":"POST","path":"/group-bookings","contract":"orders","summary":"Turn an order into a group booking","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateGroupBookingRequest","responds":"GroupBooking"},
"createOrder": {"method":"POST","path":"/orders","contract":"orders","summary":"Create an order","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateOrderRequest","responds":"Order"},
"createRefund": {"method":"POST","path":"/orders/{orderId}/refunds","contract":"orders","summary":"Refund an order, wholly or in part","permission":"ORDER_REFUND","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateRefundRequest","responds":null},
"createReport": {"method":"POST","path":"/reports","contract":"reporting","summary":"Create a custom report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportRequest","responds":"ReportDefinition"},
"deleteReport": {"method":"DELETE","path":"/reports/{reportId}","contract":"reporting","summary":"Retire a report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"exchangeOrderLines": {"method":"POST","path":"/orders/{orderId}/exchanges","contract":"orders","summary":"Exchange lines for different products or dates","permission":"ORDER_EXCHANGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ExchangeOrderRequest","responds":"OrderExchangeResult"},
"getChargebackAnalytics": {"method":"GET","path":"/chargebacks/analytics","contract":"orders","summary":"Chargeback rate, win and loss, by reason, provider, outcome and period","permission":"ORDER_REFUND_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"periodFrom","in":"query","required":true},{"name":"periodTo","in":"query","required":true},{"name":"groupBy","in":"query","required":null},{"name":"minChargebacks","in":"query","required":null},{"name":"productId","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"providerId","in":"query","required":null}],"requestBody":null,"responds":"OrdChargebackAnalytics"},
"getGroupBooking": {"method":"GET","path":"/group-bookings/{groupBookingId}","contract":"orders","summary":"A group, its leader and its name-capture duty","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GroupBooking"},
"getMediaEntitlements": {"method":"GET","path":"/media/{mediaCode}/entitlements","contract":"orders","summary":"What is already on this media","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaEntitlements"},
"getOrder": {"method":"GET","path":"/orders/{orderId}","contract":"orders","summary":"Read an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"getOrderStatement": {"method":"GET","path":"/orders/{orderId}/statement","contract":"orders","summary":"Full financial history of an order","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"OrderStatement"},
"getRefundPolicy": {"method":"GET","path":"/venues/{venueId}/refund-policy","contract":"orders","summary":"Read a venue's refund policy","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RefundPolicy"},
"getReport": {"method":"GET","path":"/reports/{reportId}","contract":"reporting","summary":"Read a report definition","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ReportDefinition"},
"getSettlement": {"method":"GET","path":"/settlements/{settlementId}","contract":"finance","summary":"Settlement detail with match results","permission":"SETTLEMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"Settlement"},
"getShift": {"method":"GET","path":"/shifts/{shiftId}","contract":"shift","summary":"Read a shift","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Shift"},
"getShiftCountLines": {"method":"GET","path":"/shifts/{shiftId}/count-lines","contract":"shift","summary":"The denomination breakdown of a shift's counts","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"countKind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getTaxDocumentRendition": {"method":"GET","path":"/tax-documents/{documentId}/rendition","contract":"finance","summary":"The PDF of a tax invoice or credit memo, in a language","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"language","in":"query","required":null}],"requestBody":null,"responds":"FinTaxDocumentRendition"},
"getTaxInvoice": {"method":"GET","path":"/tax-invoices/{invoiceId}","contract":"finance","summary":"One tax invoice, with its lines, VAT per rate and credit memos","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"FinTaxInvoice"},
"holdOrder": {"method":"POST","path":"/orders/{orderId}/hold","contract":"orders","summary":"Park a sale and free the till","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"ingestSettlementFile": {"method":"POST","path":"/settlements","contract":"finance","summary":"Ingest a provider settlement file","permission":"SETTLEMENT_RECONCILE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"inquirePaymentStatus": {"method":"POST","path":"/payments/{paymentId}/inquiry","contract":"orders","summary":"Ask the provider what actually happened","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Payment"},
"issueCreditMemo": {"method":"POST","path":"/tax-invoices/{invoiceId}/credit-memos","contract":"finance","summary":"Credit all or part of a tax invoice","permission":"LEDGER_POST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FinIssueCreditMemoRequest","responds":"FinCreditMemo"},
"issueTaxInvoice": {"method":"POST","path":"/tax-invoices","contract":"finance","summary":"Issue a tax invoice for one or more paid orders","permission":"LEDGER_POST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FinIssueTaxInvoiceRequest","responds":"FinTaxInvoice"},
"listCashMovements": {"method":"GET","path":"/shifts/{shiftId}/cash-movements","contract":"shift","summary":"Lifts, adds and the opening float","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCredentialReplacementReissue": {"method":"GET","path":"/credential-replacement-reissue","contract":"access","summary":"Credential Replacement, Reissue, Revocation & Recovery","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CredentialReplacementReissueRevocationRecoveryView"},
"listCreditMemos": {"method":"GET","path":"/credit-memos","contract":"finance","summary":"Credit memos issued, newest first","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"taxInvoiceId","in":"query","required":null},{"name":"refundId","in":"query","required":null},{"name":"legalEntityId","in":"query","required":null},{"name":"issuedFrom","in":"query","required":null},{"name":"issuedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDeposits": {"method":"GET","path":"/deposits","contract":"orders","summary":"Deposits and their authorisation state","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrderRefunds": {"method":"GET","path":"/orders/{orderId}/refunds","contract":"orders","summary":"List refunds against an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrders": {"method":"GET","path":"/orders","contract":"orders","summary":"List orders","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"createdFrom","in":"query","required":null},{"name":"createdTo","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":"tender","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPaymentReconciliationException": {"method":"GET","path":"/payment-reconciliation-exception","contract":"orders","summary":"Payment Reconciliation & Exception Management","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PaymentReconciliationExceptionManagementView"},
"listReports": {"method":"GET","path":"/reports","contract":"reporting","summary":"List available report definitions","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"category","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSettlementExceptions": {"method":"GET","path":"/settlements/{settlementId}/exceptions","contract":"finance","summary":"Unmatched or mismatched settlement lines","permission":"SETTLEMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSettlements": {"method":"GET","path":"/settlements","contract":"finance","summary":"List settlement batches","permission":"SETTLEMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"providerName","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listShifts": {"method":"GET","path":"/shifts","contract":"shift","summary":"List shifts","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"openedFrom","in":"query","required":null},{"name":"openedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTaxInvoices": {"method":"GET","path":"/tax-invoices","contract":"finance","summary":"Tax invoices issued, newest first","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"orderId","in":"query","required":null},{"name":"legalEntityId","in":"query","required":null},{"name":"invoiceType","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"issuedFrom","in":"query","required":null},{"name":"issuedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTicketReissueFulfillment": {"method":"GET","path":"/ticket-reissue-fulfillment","contract":"orders","summary":"Ticket Reissue & Fulfillment Regeneration","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TicketReissueFulfillmentRegenerationView"},
"listWorkstations": {"method":"GET","path":"/workstations","contract":"tenancy","summary":"List workstations","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"saleBoardKind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"modifyOrder": {"method":"POST","path":"/orders/{orderId}/modify","contract":"orders","summary":"Add or remove lines on an existing order","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ModifyOrderRequest","responds":"OrderModificationResult"},
"recordChargeback": {"method":"POST","path":"/chargebacks/intake","contract":"orders","summary":"Take in a chargeback notified by a provider","permission":"ORDER_REFUND_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Chargeback"},
"recordChargebackOutcome": {"method":"POST","path":"/chargebacks/{chargebackId}/outcome","contract":"orders","summary":"Record the bank's decision and adjust the ledger","permission":"ORDER_REFUND_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Chargeback"},
"rejectShiftVariance": {"method":"POST","path":"/shifts/{shiftId}/reject-variance","contract":"shift","summary":"Send a counted shift back for a recount","permission":"OVERSHORT_ACCEPT","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"replaceCredential": {"method":"POST","path":"/credentials/{credentialId}/replace","contract":"access","summary":"Replace a credential's media","permission":"ORDER_EXCHANGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CredentialReplacementInput","responds":"CredentialOperationsCommandCenterView"},
"reprintOrder": {"method":"POST","path":"/orders/{orderId}/reprints","contract":"orders","summary":"Reprint or resend tickets","permission":"ORDER_REPRINT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"rescheduleOrder": {"method":"POST","path":"/orders/{orderId}/reschedule","contract":"orders","summary":"Move an order to another performance","permission":"ORDER_RESCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderExchangeResult"},
"resolveSettlementException": {"method":"POST","path":"/settlements/{settlementId}/exceptions","contract":"finance","summary":"Resolve a settlement exception","permission":"SETTLEMENT_RECONCILE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SettlementException"},
"resumeOrder": {"method":"POST","path":"/orders/{orderId}/resume","contract":"orders","summary":"Bring a parked sale back to a till","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderResumeResult"},
"runReport": {"method":"POST","path":"/reports/{reportId}/run","contract":"reporting","summary":"Run a report","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RunReportRequest","responds":"ReportResult"},
"saveNaturalLanguageQuery": {"method":"POST","path":"/reports/ask/{conversationId}/save","contract":"reporting","summary":"Save a natural-language answer as a report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReportDefinition"},
"settleDeposit": {"method":"POST","path":"/deposits/{depositId}/settle","contract":"finance","summary":"Convert to revenue, return it, or forfeit it","permission":"LEDGER_POST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Deposit"},
"updateGroupBooking": {"method":"PATCH","path":"/group-bookings/{groupBookingId}","contract":"orders","summary":"Confirm numbers, change the leader or cancel a group","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"UpdateGroupBookingRequest","responds":"GroupBooking"},
"updateReport": {"method":"PUT","path":"/reports/{reportId}","contract":"reporting","summary":"Publish a new version of a definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportRequest","responds":"ReportDefinition"},
"voidOrder": {"method":"POST","path":"/orders/{orderId}/voids","contract":"orders","summary":"Void an order","permission":"ORDER_VOID","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AppendEntitlementRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the new order this creates, and its idempotency key — it must equal the `Idempotency-Key` header."},"lines":{"type":"array","minItems":1,"items":{"type":"object","required":["variantId","quantity"],"properties":{"variantId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"performanceId":{"type":"string","format":"uuid","nullable":true}}}},"paymentMethod":{"type":"string","enum":["card","cash","wallet","giftCard","chargeToAccount"]},"note":{"type":"string","maxLength":300},"recordedAt":{"type":"string","format":"date-time"}}},
"AppendEntitlementResult": {"type":"object","x-ticvai-persistence":"none — computed","required":["order","media"],"properties":{"order":{"allOf":[{"$ref":"#/components/schemas/Order"}],"description":"A **new** order. The original is untouched — it was paid, receipted and possibly reported on, and editing it would move yesterday's revenue.\n"},"media":{"allOf":[{"$ref":"#/components/schemas/MediaEntitlements"}],"description":"The full set now on the media, so the cashier can say what the QR does."},"addedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"CashCountLine": {"x-ticvai-persistence":"orders.cash_count_line","type":"object","description":"**One denomination, counted once, against one shift.** Raised in review on 24 August: the table was a stub.\n**The denomination is referenced rather than described** — `platform.denomination` already holds the note and coin definitions per currency, and a count line that repeats the face value is a count line that can disagree with the till it was counted on.\n**`countedQuantity` is a quantity and `expectedQuantity` is derived**, not stored: the expectation is the opening float plus every movement, and a stored expectation that drifts from the movements is a variance nobody can explain.\n","required":["shiftId","denominationId","countedQuantity"],"properties":{"id":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","description":"A UUIDv7, as `Shift.id` and `orders.pos_shift.id` are."},"depositBoxId":{"type":"string","format":"uuid","nullable":true},"countKind":{"type":"string","enum":["openingFloat","close","movement"],"description":"Which count this line belongs to — the opening float (`openShift`), the close (`closeShift`) or a lift or add (`createCashMovement`). **Until 26 September the three were indistinguishable on one shift** (pull audit R099). Set by the server from the operation that wrote the line.\n"},"cashMovementId":{"type":"string","format":"uuid","nullable":true,"description":"The movement this line counts, where `countKind` is `movement`. How `listCashMovements` rebuilds each movement's `denominations`.\n"},"denominationId":{"type":"string","format":"uuid","description":"References `platform.denomination` — face value, kind and sort order live there."},"countedQuantity":{"type":"integer","minimum":0,"description":"**How many of this note or coin were in the drawer.**"},"countedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"**Quantity times face value, stored.** Derivable, and stored anyway: a denomination revalued or deactivated later would silently rewrite a historical count.\n"},"countedBy":{"type":"string","format":"uuid","nullable":true},"countedAt":{"type":"string","format":"date-time"},"recountOf":{"type":"string","format":"uuid","nullable":true,"description":"**A recount points at what it replaces rather than overwriting it.** `requestRecount` exists because a variance is a question before it is a fact.\n"}}},
"CashMovement": {"x-ticvai-persistence":"orders.cash_movement","allOf":[{"$ref":"#/components/schemas/CreateCashMovementRequest"},{"type":"object","required":["shiftId","authorisedByPrincipalId","sequence"],"properties":{"shiftId":{"type":"string","format":"uuid"},"depositBoxId":{"type":"string","format":"uuid","nullable":true,"description":"The box the cash moved in or out of. Set on every lift `withdrawFromDepositBox` records (26 September, pull audit R099).\n"},"witnessPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The cashier who countersigned a withdrawal. Null on other movements."},"withdrawalReason":{"allOf":[{"$ref":"#/components/schemas/WithdrawalReason"}],"nullable":true},"authorisedByPrincipalId":{"type":"string","format":"uuid","description":"The principal who authorised the movement, recorded for audit."},"sequence":{"type":"integer","description":"Monotonic within the shift. Preserves order across an offline batch."},"syncedAt":{"type":"string","format":"date-time","nullable":true}}}]},
"CatalogueState": {"x-ticvai-persistence":"none — computed from workstation bundle_version","type":"object","description":"The workstation's local catalogue position. A terminal beyond `staleAfter` must refuse to trade rather than transact against stale prices.\n","required":["appliedBundleVersion","appliedAt","staleAfter","isStale"],"properties":{"appliedBundleVersion":{"type":"string"},"appliedAt":{"type":"string","format":"date-time"},"staleAfter":{"type":"string","format":"date-time","description":"Beyond this the terminal refuses to trade."},"isStale":{"type":"boolean"},"pendingBundleVersion":{"type":"string","nullable":true,"description":"Published but not yet applied."}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"Chargeback": {"type":"object","x-ticvai-persistence":"orders.chargeback + orders.chargeback_evidence + orders.chargeback_investigation_log","description":"BL-118, CF-144. **A chargeback is not a refund**, and treating it as one is how a venue loses them by default.\nA refund is a decision the venue makes. **A chargeback is a decision a bank makes, on a clock the venue does not control** — evidence is due in days, a deadline missed is a case lost regardless of merit, and there is a fee either way.\nThe money is already gone when this record is created. **Representment is an argument, not a reversal.**\n","required":["id","paymentId","amount","reason","status","evidenceDueBy"],"properties":{"id":{"type":"string","format":"uuid"},"paymentId":{"type":"string","format":"uuid"},"providerId":{"type":"string","format":"uuid"},"providerCaseReference":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"feeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reason":{"type":"string","enum":["fraudulent","productNotReceived","productUnacceptable","duplicate","subscriptionCancelled","creditNotProcessed","unrecognised","other"],"description":"**The scheme's reason code, mapped.** Which evidence wins depends entirely on it — a *product not received* case is answered by a scan record and a *fraudulent* case is not.\n"},"status":{"type":"string","enum":["received","underReview","evidenceSubmitted","won","lost","accepted","expired"]},"evidenceDueBy":{"type":"string","format":"date-time","description":"**The field the whole record exists for.** A deadline missed is a case lost on merit nobody read, and it is the one date that must reach a person rather than a report.\n"},"evidenceSubmittedAt":{"type":"string","format":"date-time","nullable":true},"evidence":{"type":"array","description":"**What the platform can prove**, assembled rather than typed: the order, the scan that admitted them, the delivery, the terms accepted, the IP and device. A venue answering a chargeback by hand is a venue answering it late.\nHeld as rows of `orders.chargeback_evidence`, one per item (29 September, build: a list of objects needs its own table to be stored at all).\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["order","scanRecord","deliveryProof","termsAccepted","communication","deviceFingerprint","other"]},"reference":{"type":"string"}}}},"outcomeAt":{"type":"string","format":"date-time","nullable":true},"schemeReasonCode":{"type":"string","nullable":true,"description":"The card scheme's own reason code as notified, beside the mapped `reason` (5.7.92)."},"notifiedAt":{"type":"string","format":"date-time","nullable":true,"description":"When the provider notified the case; the date its debit posts to (`recordChargeback`)."},"assigneePrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who is investigating (`assignChargeback`)."},"investigationLog":{"type":"array","description":"Notes from `assignChargeback` and `recordChargebackOutcome`, oldest first, with who wrote each and when. Append-only. Held as rows of `orders.chargeback_investigation_log` (29 September, build).","items":{"type":"object","properties":{"note":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"}}}},"debitJournalEntryId":{"type":"string","format":"uuid","nullable":true,"description":"The `chargebackDebit` (and `chargebackFee`) entry posted at intake."},"outcomeJournalEntryId":{"type":"string","format":"uuid","nullable":true,"description":"The `chargebackReversal` entry posted when the case is won, or the additional fee when lost."}}},
"CloseShiftRequest": {"type":"object","required":["countedCash","recordedAt"],"properties":{"countedCash":{"type":"array","minItems":1,"description":"**The cashier's blind count, one line per denomination counted** (decided 29 September, readiness close-out; our build plan). The server writes each line as one `CashCountLine` (`countKind` close) against the shift, taking the face value from `platform.denomination`. A denomination may appear once; a repeat is refused with 422 `duplicate-denomination`.\n","items":{"$ref":"#/components/schemas/CountedDenominationLine"}},"nonCashDeclared":{"type":"array","description":"Declared totals per non-cash tender, for reconciliation against captured payments.\n","items":{"type":"object","required":["tender","amount"],"properties":{"tender":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"notes":{"type":"string","maxLength":1000,"description":"The cashier's note on the count. Asked of every cashier on a blind count, never only after a variance is shown (CHG-FIN-003, DI-803).\n"},"cashierReason":{"type":"string","nullable":true,"enum":["tillError","unrecordedRefund","miscount","other"],"description":"Anything the cashier knows went wrong in the shift (DI-803: till error, unrecorded refund, miscount, other). Optional and given without seeing the variance (CHG-FIN-003); the supervisor reads it beside the variance on BO-040.\n"},"releaseHeldLeases":{"type":"boolean","default":true,"description":"Return unsold inventory leases held by this workstation (ADR-0013 C103). Closing without releasing strands capacity until TTL expiry, which is visible at a gate during peak.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"CountedDenominationLine": {"type":"object","x-ticvai-persistence":"none — request only; lands as `CashCountLine` rows","description":"**One line of a cash count as the cashier types it: which note or coin, how many, and what they come to** (decided 29 September, readiness close-out; our build plan). The shape of the blind count on close (`closeShift`) and of the count columns on the till screens (POS-007, POS-011). It is the request side of `CashCountLine`, which is the stored row and adds the shift, the count kind, who counted and when.\n**`total` is shown to the cashier and checked, not trusted**: the server recomputes `count` times the denomination's face value and refuses a line whose `total` disagrees with 422 `count-total-mismatch`. An inactive or unknown denomination is refused with 422 `unknown-denomination`.\n","required":["denominationId","count"],"properties":{"denominationId":{"type":"string","format":"uuid","description":"References `platform.denomination` (`Denomination.id`) — face value, kind and counting order live there."},"count":{"type":"integer","minimum":0,"maximum":100000,"description":"**How many of this note or coin were counted.** Zero is a line, not an omission: a denomination counted and found empty."},"total":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"`count` times the face value, in the denomination's currency. Optional on the way in (the server computes it) and checked when sent.\n"}}},
"CreateCashMovementRequest": {"type":"object","required":["id","kind","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7."},"kind":{"$ref":"#/components/schemas/CashMovementKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"denominations":{"$ref":"#/components/schemas/DenominationCount","x-ticvai-persisted":false,"description":"**Stored as `orders.cash_count_line` rows** with `countKind: movement` and this movement's `cashMovementId`, not as a column. The jsonb blob this used to land in is what `Denomination` was created to replace (26 September, pull audit R099).\n"},"reference":{"type":"string","maxLength":64,"description":"Safe drop reference or bag number."},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateGroupBookingRequest": {"type":"object","description":"Request only. Persisted as `GroupBooking`.","required":["orderId","leaderSubjectId","expectedSize"],"properties":{"groupQuoteId":{"x-ticvai-references":"orders.group_quote","type":"string","format":"uuid","nullable":true,"description":"**The quote this booking converts** (BO-272). Must be the current version and `sent` or `accepted`; conversion sets its `groupBookingId` and moves a `sent` quote to `accepted` (decided 29 September, writers pass)."},"kind":{"type":"string","enum":["general","school","corporate","party"],"default":"general"},"packageProductId":{"type":"string","nullable":true,"description":"The school-trip format or party package."},"yearGroup":{"type":"string","maxLength":40,"nullable":true},"accessAndDietaryNeeds":{"type":"string","maxLength":1000,"nullable":true},"celebrantName":{"type":"string","maxLength":120,"nullable":true,"description":"The birthday child."},"celebrantTurningAge":{"type":"integer","minimum":1,"maximum":18,"nullable":true},"allergiesAndRequests":{"type":"string","maxLength":1000,"nullable":true},"finalHeadcountDueBy":{"type":"string","format":"date-time","nullable":true},"orderId":{"type":"string","format":"uuid"},"leaderSubjectId":{"type":"string","format":"uuid","description":"The person who pays, is called if the coach is late, and collects the names."},"organisationName":{"type":"string","maxLength":200,"nullable":true},"expectedSize":{"type":"integer","minimum":2},"minimumSize":{"type":"integer","minimum":1,"nullable":true},"attendeeCaptureRequired":{"type":"boolean","default":false},"attendeeCaptureDueBy":{"type":"string","format":"date-time","nullable":true}}},
"CreateOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","variantId","quantity","quotedUnitPrice"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these."},"variantId":{"type":"string","format":"uuid"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"inventoryHoldId":{"type":"string","nullable":true,"description":"Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"},"description":"Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"quantity":{"type":"integer","minimum":1},"eligibilityDeclaration":{"type":"array","nullable":true,"x-ticvai-note":"One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n","items":{"type":"object","properties":{"ageBand":{"type":"string","enum":["infant","child","junior","adult","senior"],"description":"Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."},"ageYears":{"type":"integer","nullable":true},"heightBandIndex":{"type":"integer","nullable":true},"confidentSwimmer":{"type":"boolean","nullable":true,"description":"**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"},"guardianSigned":{"type":"boolean"}}},"description":"What was declared for each guest on this line, kept as the record staff check at the gate."},"quotedUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the client charged, from its local bundle."},"holderName":{"type":"string","nullable":true},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"}}},
"CreateOrderRequest": {"type":"object","required":["id","venueId","channel","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. Offline replay through `syncOrders` carries no header, and this id alone deduplicates there.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"#/components/schemas/Channel"},"shiftId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null for an anonymous sale. Identity and entitlement are separate."},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells."},"catalogueBundleVersion":{"type":"string","description":"The bundle the client priced from. Lets the server explain a variance rather than merely report one.\n"},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateRefundRequest": {"type":"object","required":["id","amount","reason","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the refund, and its idempotency key — it must equal the `Idempotency-Key` header."},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Omit to refund the whole order."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reason":{"type":"string","minLength":3,"maxLength":500},"secondaryAuthorisation":{"type":"object","description":"Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. This is dual-authorisation, not escalation.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid"},"credential":{"type":"string","maxLength":512,"description":"The second person's staff PIN, as they sign in at a till with it. **A PIN, never a password** (decided 28 September, audit R123 (7))."}}},"refundToOriginalTender":{"type":"boolean","default":true},"alternateTender":{"$ref":"#/components/schemas/TenderKind"},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","category","dataSource","columns","requiredPermission"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"category":{"$ref":"#/components/schemas/ReportCategory"},"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"parameters":{"type":"array","items":{"$ref":"#/components/schemas/ReportParameter"}},"requiredPermission":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission","description":"Permission needed to run this report, from the shared `Permission` vocabulary. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"},"maxDateRangeDays":{"type":"integer","nullable":true,"minimum":1,"default":366,"description":"Guards against a query spanning years of scan events. **When a report sets none, 366 days applies (decided 28 September, audit R158)**, so `runReport`'s date-range 400 always has a limit."}}},
"CredentialOperationsCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"virtualTicketId":{"type":"string","description":"Virtual Ticket ID"},"credentialId":{"type":"string","description":"Credential ID"},"mediaType":{"type":"string","description":"Media Type"},"customerParticipant":{"type":"string","description":"Customer / Participant"},"product":{"type":"string","description":"Product"},"event":{"type":"string","description":"Event"},"credentialStatus":{"type":"string","enum":["pendingGeneration","generated","pendingActivation","active","suspended","revoked","expired","failed"],"description":"Credential status"},"deliveryStatus":{"type":"string","enum":["notRequired","pending","sent","delivered","openedDownloaded","completed","failed","bounced","expired","cancelled"],"description":"Delivery status (15.3.4)"},"activationStatus":{"type":"string","enum":["pending","scheduled","active","notRequired"],"description":"Activation status"},"bindingStatus":{"type":"string","enum":["pending","bound","unbound","failed"],"description":"Binding status"},"provider":{"type":"string","description":"Provider"},"lastActivity":{"type":"string","format":"date-time","description":"Last Activity"},"exception":{"type":"string","description":"Exception"},"owner":{"type":"string","description":"Owner"}}},
"CredentialReplacementInput": {"type":"object","x-ticvai-persistence":"none — request only (decided 29 September, VM close-out)","description":"Replace the media of a credential while the Virtual Ticket stays the same (decided 29 September, VM close-out).","required":["reason"],"properties":{"reason":{"type":"string","enum":["lost","stolen","damaged","compromised","customerChangedPhone","rfidFailure","wristbandReplacement","qrCompromise","walletReplacement","faceReEnrollment","incorrectAssignment"]},"newMediaKind":{"type":"string","description":"Media type of the replacement (`MediaTypeTechnologyLibraryView.mediaType`); empty keeps the current kind"},"newMediaCode":{"type":"string","description":"Code of the new physical media where one is encoded at the counter"},"approvalRequestId":{"type":"string","format":"uuid","description":"The granted approval, where the replacement rule requires one"},"note":{"type":"string","maxLength":500}}},
"CredentialReplacementReissueRevocationRecoveryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Credential Replacement, Reissue, Revocation & Recovery displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"reason":{"type":"string","enum":["lost","stolen","damaged","compromised","customerChangedPhone","rfidFailure","wristbandReplacement","qrCompromise","walletReplacement","faceReEnrollment","incorrectAssignment"],"description":"Replacement reason this policy covers"},"immediateOldMediaRevocation":{"type":"boolean","description":"Immediate old-media revocation"},"gracePeriod":{"type":"string","description":"ISO 8601 duration, e.g. PT30M"},"maximumReplacements":{"type":"integer","description":"Maximum replacements"},"identityVerification":{"type":"boolean","description":"Identity verification"},"supervisorApproval":{"type":"boolean","description":"Supervisor approval"},"reasonCodes":{"type":"array","items":{"type":"string"},"description":"Reason codes"},"recoveryAllowed":{"type":"boolean","description":"A suspended credential may be restored under this policy"}},"required":["reason"]},
"DataSource": {"type":"string","description":"What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n\n**`forecastPoints` added 29 September** (8.2.55, build pass, group G2): the points of published AI forecast versions; see `x-ticvai-forecast-points`.\n\n**Three accreditation sources added 29 September** (12.1.50, build pass): `accreditationApplications`, `accreditationHolders` and `accreditationCredentials`, over `accreditation.application`, `accreditation.holder` and `accreditation.credential`. They are what the accreditation KPIs and any accreditation report or export (`exportReportResult`, csv or xlsx) are built over. **All three name a person**, and `REPORT_EXPORT_PII` gates them as it gates `guests`.\n","enum":["orders","orderLines","payments","refunds","shifts","scanEvents","entitlements","products","inventory","stockMovements","stockCounts","waste","workstations","devices","principals","loyalty","reviews","queueEntries","guests","campaigns","cases","ledgerEntries","workOrders","approvals","purchaseOrders","receipts","requisitions","stockBatches","resourceBookings","delegations","forms","challenges","wallets","resaleListings","accreditationApplications","accreditationHolders","accreditationCredentials","forecastPoints"],"x-ticvai-forecast-points":"**`forecastPoints` added 29 September (build pass, group G2; 8.2.55)**: one row per forecast point (`ai.forecast_point`) of a **published** forecast version (`ai.forecast_version` status `published`), with the definition it belongs to (`ai.forecast_definition`: subject, grain, unit), the period, the dimension key and the p10, p50 and p90 values. Draft, awaiting-approval and superseded versions are not reachable, and scenario points (`scenarioId` set) only with the scenario named as a filter: **a forecast leaves the platform as the one somebody published**. It is how a forecast is exported (`runReport` then `exportReportResult`, csv or xlsx), scheduled or put on a dashboard. Names no person, so `REPORT_EXPORT` is enough. Read from the reporting replica of the AI log database (design 2.4), never from the model service.\n"},
"DenominationCount": {"type":"array","description":"**A count is a list of lines and the line is the row.** Until 24 August this array carried the persistence hint itself, so `orders.cash_count_line` derived a single column — `shift_id` — and a count line had no denomination, no quantity and no variance.\n**The array is the transport; `CashCountLine` is the row.**\n","items":{"$ref":"#/components/schemas/CashCountLine"},"minItems":1},
"DeploymentProfile": {"type":"string","description":"How this workstation obtains catalogue and inventory (ADR-0013).\n- `terminalLocal` — own SQLite, leases direct from the cell. Small venues, 4G sites - `venueEdge` — own SQLite, distributed via the venue edge node which holds the\n  venue lease and sub-leases to terminals. Mid and large venues, stadium gates\n- `thin` — no local catalogue, server reads. Non-transactional surfaces only\n","enum":["terminalLocal","venueEdge","thin"]},
"Deposit": {"type":"object","x-ticvai-persistence":"ledger.deposit","description":"**Money taken before the sale is complete.** Not deferred revenue — that is a sold entitlement not yet consumed, and the sale happened.\n","required":["id","amount","reason","status"],"properties":{"id":{"type":"string","format":"uuid"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reason":{"type":"string","enum":["reservation","rental","event","damageBond","other"]},"status":{"type":"string","enum":["held","convertedToRevenue","returned","forfeited","partiallyForfeited"]},"subjectId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true},"bookingId":{"type":"string","format":"uuid","nullable":true},"refundableUntil":{"type":"string","format":"date-time","nullable":true,"description":"**After which a forfeit is permitted rather than a return.** The date is the cancellation term, and a deposit with no date is refundable indefinitely.\n"},"liabilityAccountId":{"type":"string","format":"uuid"},"settledAt":{"type":"string","format":"date-time","nullable":true}}},
"DepositBox": {"type":"object","x-ticvai-persistence":"orders.deposit_box + orders.deposit_box_opening_denomination + orders.deposit_box_foreign_holding","description":"5.8. **Allocated to a cashier, not to a workstation.** A cashier moving between tills takes their float with them, which is what makes a variance attributable to a person.\n**`openingDenominations` and `foreignHoldings` are child rows** (26 September, pull audit R099): `orders.deposit_box_opening_denomination` and `orders.deposit_box_foreign_holding`, one row per item, keyed to the box. Until then the contract carried both and the table had nowhere to put either.\n","required":["cashierPrincipalId","venueId","openingFloat"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"cashierPrincipalId":{"type":"string","format":"uuid"},"cashierName":{"type":"string","readOnly":true},"venueId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Where it is being used now. **Changes during a shift; the box does not.**"},"shiftId":{"type":"string","format":"uuid","nullable":true,"description":"The shift trading from this box. A UUIDv7, as `Shift.id` is."},"status":{"$ref":"#/components/schemas/DepositBoxStatus"},"openingFloat":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"openingDenominations":{"type":"array","description":"5.8.3. **Either this or a total** — a supervisor handing over a counted bag should not have to re-count it into fields. POS-001 offered only denominations until 14 August.\n","items":{"type":"object","required":["denominationId","count"],"properties":{"denominationId":{"type":"string","format":"uuid","description":"References `platform.denomination`, as `CashCountLine.denominationId` does. Until 26 September this was `denomination: number` — a face value as a JSON float, which naming-and-style 5.1 forbids and which could disagree with the note it named (pull audit R122).\n"},"count":{"type":"integer","minimum":0}}}},"withdrawnTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"**Reduces the expected close figure.** Cash skimmed for banking is not a shortfall, and a system that treats it as one makes every busy cashier look short.\n"},"overDrawerLimit":{"type":"boolean","readOnly":true,"default":false,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"**The box holds more than its till's drawer limit** (decided 2 October 2026, Chinmay, BO-042; DEC-179; CHG-CSP-016): computed on read from the box's expected cash against `tenancy.Workstation.cashDrawerLimit` or the venue's `cashDrawerLimit`. BO-042 flags the box and offers a lift; false where no limit is set. A flag, not a figure: it tells the cashier nothing about the expected cash (CHG-FIN-003).\n"},"foreignHoldings":{"type":"array","description":"4.6.11 and 6.1.10. **Foreign cash accepted at this till, counted separately by currency.** A till taking USD and EUR alongside AED has three counts and three variances — collapsing them into a base-currency total makes a variance unattributable to the currency that caused it.\n**No opening float in a foreign currency and no change given in one.** Foreign cash only ever comes in, which is what keeps this to one number per currency rather than a full reconciliation each.\n","items":{"type":"object","required":["currency","countedAmount"],"properties":{"currency":{"type":"string","pattern":"^[A-Z]{3}$","description":"**Stored, because it is the one thing that is not the region's.** A foreign holding is by definition cash in a currency the till does not trade in, so it cannot resolve from the region (ADR-0018) the way the box's own amounts do; it is the key of the row, one per currency per box. The amounts on this item are in this currency.\n"},"expectedAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The sum of tenders taken in this currency during the shift."},"countedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"baseEquivalent":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**At the rates on the payments, not today's.** A shift closed on Friday and reviewed on Monday is reviewed at Friday's rates (CF-37).\n"}}}},"expectedTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"countedTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**Flagged where it is not the holder.** A box closed without its holder present is allowed — the cash is counted by somebody, and who counted it is the record.\n"},"allocatedAt":{"type":"string","format":"date-time","description":"When the device recorded the allocation. `allocateDepositBox` is offline-capable, so for a box allocated offline this differs from the server's receipt time.\n"},"closedAt":{"type":"string","format":"date-time","nullable":true}}},
"DepositBoxStatus": {"type":"string","enum":["allocated","open","suspended","closing","closed","reconciled"]},
"DeviceBinding": {"x-ticvai-persistence":"platform.device","type":"object","required":["kind","driver"],"properties":{"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Driver identifier. Adding a vendor is a driver plus configuration, never a core change — every venue arrives with hardware not previously seen.\n"},"identifier":{"type":"string","description":"Serial","port or network address.":null},"isRequired":{"type":"boolean","default":false,"description":"When true, the workstation refuses to open a shift if the device is absent.\n"}}},
"EntitlementStatus": {"type":"string","description":"**What the storage layer holds, and what a guest is shown.** `MediaEntitlements` carried only `isValid` and a reason string — a boolean cannot distinguish a ticket that was used from one that expired, was refunded, or was transferred to somebody else, and those are four different conversations at a gate.\nAdded 17 August. `states/entitlement.yaml` had modelled these six since 14 August and the contract had no enum behind it, which the state checker reported correctly for three days.\n\n**The client's 13 Virtual Ticket statuses map onto these six** (decided 2 October 2026, Chinmay, critical set 2, BO-336: \"Map the pack's 13 names onto the model; add any missing states\"; DEC-266; CHG-CSP-033). Every name maps, so no value is added (one would be a breaking change against r1): Active is `issued`, Partially used `partiallyConsumed`, Used `fullyConsumed`, Expired `expired`, Transferred `surrendered`, Suspended and Blocked are `issued` with the suspended flag or an identity lock, and Cancelled, Voided, Refunded and Reissued / superseded are `cancelled` told apart by access `Entitlement.cancellationKind`. Created and Pending fulfilment (DI-670's Reserved) are the order before an entitlement exists. The table is `states/entitlement-status.yaml` (`pack_status_map`); access `Entitlement.lifecycleLabel` carries the name.\n","enum":["issued","partiallyConsumed","fullyConsumed","expired","cancelled","surrendered"]},
"ExchangeOrderRequest": {"type":"object","required":["id","outgoingLineIds","incomingLines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header."},"outgoingLineIds":{"type":"array","minItems":1,"items":{"type":"string","format":"uuid"}},"incomingLines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"waiveFee":{"type":"boolean","default":false},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"FinCreditMemo": {"x-ticvai-persistence":"ledger.credit_memo + ledger.credit_memo_line","type":"object","description":"5.7.94. **A tax credit note against one tax invoice**, with its own series. Never edited.","required":["id","creditMemoNumber","taxInvoiceId","kind","reason","legalEntityId","issuedAt","currency","netAmount","taxAmount","grossAmount","lines"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"creditMemoNumber":{"type":"string","readOnly":true,"description":"Server-assigned from the legal entity's credit memo series, in sequence without gaps."},"taxInvoiceId":{"type":"string","format":"uuid"},"taxInvoiceNumber":{"type":"string","readOnly":true},"kind":{"type":"string","enum":["full","partial"]},"reason":{"type":"string","enum":["refund","cancellation","priceAdjustment","returnOfGoods","billingError","other"]},"refundId":{"type":"string","format":"uuid","nullable":true},"cancelledOrderId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid"},"buyerSubjectId":{"type":"string","format":"uuid","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmountInLegalCurrency":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"legalFxRate":{"allOf":[{"$ref":"#/components/schemas/FxRateValue"}],"nullable":true,"readOnly":true,"description":"The invoice's own `legalFxRate`, never today's (CHG-FIN-011)."},"invoiceSupplyValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"**The value of the supply shown on the tax invoice** (Executive Regulation Art. 60(1)(e)), adjusted by any earlier credit note on the same invoice. With `correctedSupplyValue` and `netAmount` (the difference) and `taxAmountInLegalCurrency` (the tax on the difference in AED), the four figures the law requires (CHG-FIN-011)."},"correctedSupplyValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The correct value of the supply after this credit note (Art. 60(1)(e))."},"supplierName":{"type":"string","readOnly":true,"description":"Snapshot of the legal entity at issue, as on the invoice (Art. 60(1)(b))."},"supplierAddress":{"type":"string","nullable":true,"readOnly":true},"supplierTaxRegistrationNumber":{"type":"string","nullable":true,"readOnly":true},"buyerName":{"type":"string","nullable":true,"readOnly":true,"description":"The recipient as on the invoice; name, address and TRN where they are registered (Art. 60(1)(c))."},"buyerAddress":{"type":"string","nullable":true,"readOnly":true},"buyerTaxRegistrationNumber":{"type":"string","nullable":true,"readOnly":true},"note":{"type":"string","nullable":true,"description":"The brief explanation of why the credit note was issued, printed on it (Art. 60(1)(f)); the reason's own wording when no note is given (CHG-FIN-011)."},"renditionAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"eInvoiceStatus":{"$ref":"#/components/schemas/FinEInvoiceTransmissionStatus"},"issuedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"lines":{"type":"array","items":{"$ref":"#/components/schemas/FinCreditMemoLine"}},"scopePath":{"type":"string","readOnly":true}}},
"FinCreditMemoLine": {"type":"object","required":["invoiceLineNumber","netAmount","taxAmount","grossAmount"],"properties":{"invoiceLineNumber":{"type":"integer","minimum":1},"description":{"type":"string","maxLength":500},"quantity":{"type":"number","nullable":true},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxRate":{"type":"number"},"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"FinEInvoiceTransmissionStatus": {"type":"string","description":"6.1.1. `notRequired` where the legal entity's provider is `disabled` or absent.","enum":["notRequired","queued","sent","accepted","rejected","failed"]},
"FinIssueCreditMemoRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["kind","reason"],"properties":{"kind":{"type":"string","enum":["full","partial"]},"reason":{"type":"string","enum":["refund","cancellation","priceAdjustment","returnOfGoods","billingError","other"]},"refundId":{"type":"string","format":"uuid","nullable":true},"cancelledOrderId":{"type":"string","format":"uuid","nullable":true},"lines":{"type":"array","description":"Required for `partial`. Each names an invoice line and the quantity or amount credited.","items":{"type":"object","required":["lineNumber"],"properties":{"lineNumber":{"type":"integer","minimum":1},"quantity":{"type":"number","nullable":true},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"note":{"type":"string","maxLength":500,"nullable":true}}},
"FinIssueTaxInvoiceRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["invoiceType","orderIds"],"properties":{"invoiceType":{"$ref":"#/components/schemas/FinTaxInvoiceType"},"orderIds":{"type":"array","minItems":1,"description":"One order for `simplified` and `full`; one or more for `consolidated`. Every order must be paid, of one buyer, one legal entity and one currency.","items":{"type":"string","format":"uuid"}},"recipient":{"$ref":"#/components/schemas/FinTaxInvoiceRecipient"},"languages":{"type":"array","description":"Overrides the template's languages for this document, within those the template offers.","items":{"type":"string","pattern":"^[a-z]{2}(-[A-Z]{2})?$"}},"supersedesInvoiceId":{"type":"string","format":"uuid","nullable":true,"description":"A simplified invoice this full invoice replaces for the same supply. Refused unless the law allows it (make-or-break on issueTaxInvoice)."},"deliverToEmail":{"type":"string","format":"email","nullable":true,"description":"Sends the PDF on issue as well as returning it."}}},
"FinTaxCategory": {"type":"string","description":"How a line is treated for VAT. Taken from the tax code the line was posted with.","enum":["standardRated","zeroRated","exempt","outOfScope","reverseCharge"]},
"FinTaxDocumentRendition": {"x-ticvai-persistence":"none — a signed link to the stored PDF","type":"object","required":["documentId","documentKind","url","expiresAt"],"properties":{"documentId":{"type":"string","format":"uuid"},"documentKind":{"type":"string","enum":["taxInvoice","creditMemo"]},"documentNumber":{"type":"string"},"language":{"type":"string","nullable":true},"contentType":{"type":"string","default":"application/pdf"},"url":{"type":"string","format":"uri"},"expiresAt":{"type":"string","format":"date-time"}}},
"FinTaxInvoice": {"x-ticvai-persistence":"ledger.tax_invoice + ledger.tax_invoice_line","type":"object","description":"5.7.93, 5.10.3. **A guest tax invoice, as issued, never edited.** Corrections are credit memos. The supplier block is a snapshot of the legal entity at issue, so a later change of address does not change a document already given to a guest.","required":["id","invoiceNumber","invoiceType","status","legalEntityId","issuedAt","supplyDate","currency","netAmount","taxAmount","grossAmount","lines"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"invoiceNumber":{"type":"string","readOnly":true,"description":"Server-assigned from the legal entity's series for the document kind, in sequence and without gaps, e.g. `INV-2026-000123`. Never reused."},"invoiceType":{"$ref":"#/components/schemas/FinTaxInvoiceType"},"status":{"$ref":"#/components/schemas/FinTaxInvoiceStatus"},"legalEntityId":{"type":"string","format":"uuid"},"templateId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"orderIds":{"type":"array","items":{"type":"string","format":"uuid"}},"supplierName":{"type":"string"},"supplierAddress":{"type":"string","nullable":true},"supplierTaxRegistrationNumber":{"type":"string","nullable":true},"buyerSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest the orders belong to; the key a guest's own reads filter on."},"buyerName":{"type":"string","nullable":true},"buyerAddress":{"type":"string","nullable":true},"buyerCountryCode":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"buyerTaxRegistrationNumber":{"type":"string","nullable":true},"customerAccountId":{"type":"string","format":"uuid","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"supplyDate":{"type":"string","format":"date","description":"The date of supply where it differs from the issue date (the latest order's payment date on a consolidated invoice). A day in the region's time zone."},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmountInLegalCurrency":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"The tax in the legal entity's currency (AED in the UAE) where the invoice currency differs. **In the UAE the converted amounts use the UAE Central Bank rate at the date of supply** (Decree-Law Art. 69) and the rate is printed (`legalFxRate`, Executive Regulation Art. 59(1)(k)); CHG-FIN-011."},"legalCurrency":{"type":"string","pattern":"^[A-Z]{3}$","readOnly":true,"description":"The legal entity's currency (AED in the UAE), in which the law requires the tax and the gross amount (CHG-FIN-011)."},"grossAmountInLegalCurrency":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The gross amount payable in the legal currency (Executive Regulation Art. 59(1)(j); for a simplified invoice the total consideration, Art. 59(2)(e)). Equal to `grossAmount` when the invoice is in the legal currency (CHG-FIN-011)."},"legalFxRate":{"allOf":[{"$ref":"#/components/schemas/FxRateValue"}],"nullable":true,"readOnly":true,"description":"Units of the legal currency per one unit of `currency`, printed with the tax where the invoice is not in the legal currency (Art. 59(1)(k)). Null when it is (CHG-FIN-011)."},"legalFxRateSource":{"allOf":[{"$ref":"#/components/schemas/FxRateSource"}],"nullable":true,"readOnly":true,"description":"`uaeCentralBank` for a UAE legal entity (Decree-Law Art. 69)."},"paidCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"Where the guest paid in a currency they selected (`orders.Order.chargeCurrency`, CHG-FIN-001), printed as payment information with `paidAmount` and the charge rate. The invoice itself is in the base currency, so the AED amounts the law requires are the invoice's own figures (CHG-FIN-011)."},"paidAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"What the guest paid in `paidCurrency` (`orders.Order.chargeTotal`)."},"reverseChargeStatement":{"type":"string","nullable":true,"readOnly":true,"description":"Where the recipient must account for the tax, the statement saying so and the Decree-Law provision (Art. 59(1)(l), Art. 48). Null otherwise (CHG-FIN-011)."},"creditedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"languages":{"type":"array","items":{"type":"string"}},"supersedesInvoiceId":{"type":"string","format":"uuid","nullable":true},"renditionAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The PDF rendered at issue; read through getTaxDocumentRendition."},"eInvoiceStatus":{"$ref":"#/components/schemas/FinEInvoiceTransmissionStatus"},"issuedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Null where the platform issued it."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/FinTaxInvoiceLine"}},"taxSummary":{"type":"array","x-ticvai-persisted":false,"description":"VAT per rate and category, summed from the lines for the response.","items":{"type":"object","properties":{"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxRate":{"type":"number"},"taxableAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Written at the scope of the venue the orders were sold at, or the region for a consolidated invoice across venues."}}},
"FinTaxInvoiceLine": {"type":"object","description":"One line as it was sold and taxed. Amounts are in the invoice currency.","required":["lineNumber","description","quantity","netAmount","taxAmount","grossAmount","taxCategory"],"properties":{"lineNumber":{"type":"integer","minimum":1},"orderId":{"type":"string","format":"uuid"},"orderLineId":{"type":"string","format":"uuid","nullable":true},"description":{"type":"string","maxLength":500},"quantity":{"type":"number"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeId":{"type":"string","format":"uuid","nullable":true},"taxRate":{"type":"number","minimum":0,"maximum":100},"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"creditedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmountInLegalCurrency":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The amount payable for the line in the legal currency (AED), Executive Regulation Art. 59(1)(h); equal to `grossAmount` on an invoice in the legal currency (CHG-FIN-011)."}}},
"FinTaxInvoiceRecipient": {"x-ticvai-persistence":"none — copied onto the invoice as buyer columns","type":"object","description":"Who the invoice is addressed to. Required for `full` and `consolidated`.","required":["name"],"properties":{"name":{"type":"string","maxLength":300},"address":{"type":"string","maxLength":1000,"nullable":true},"countryCode":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"taxRegistrationNumber":{"type":"string","maxLength":30,"nullable":true,"description":"The recipient's TRN where they are VAT-registered."},"customerAccountId":{"type":"string","format":"uuid","nullable":true,"description":"The B2B credit account (payments `B2bCreditAccount`) where a company is invoiced."}}},
"FinTaxInvoiceStatus": {"type":"string","description":"`issued` until a credit memo is issued against it; `superseded` where a full invoice replaced a simplified one for the same supply (only if the law allows it; see issueTaxInvoice).","enum":["issued","partiallyCredited","fullyCredited","superseded"]},
"FinTaxInvoiceType": {"type":"string","description":"5.7.93. `simplified` for one order with no recipient details, `full` for one order with them, `consolidated` for several paid orders of one buyer on one invoice.\n**When a simplified tax invoice is allowed in the UAE** (research 2 October 2026, CHG-FIN-011; Executive Regulation, Cabinet Decision 52 of 2017 as amended, Art. 59(5)): the recipient is not VAT-registered, or is registered and the consideration does not exceed AED 10,000, and the reverse charge does not apply. Otherwise the invoice is `full`. Both kinds carry the title \"Tax Invoice\" (Art. 59(1)(a), 59(2)(a)); a simplified one is issued on the date of supply (Art. 59(13)(1)), a full one within 14 days (Decree-Law Art. 67(1)).","enum":["simplified","full","consolidated"]},
"FxRateSource": {"type":"string","description":"**Where the rate came from, and which provider specifically.** `source: provider` said a feed set it and not which one — two tenants on different feeds were indistinguishable in the ledger, and a rate cannot be defended in an audit without naming its origin.\n\n**`uaeCentralBank` is the default for AED pairs.** The UAE Central Bank publishes an official daily rate and it is what a UAE auditor expects to see — a commercial feed is defensible for tender and awkward for statutory reporting.\n\n**`openExchangeRates` and `ecb` are the commercial and reference options.** ECB publishes daily reference rates free and is the usual fallback for non-AED pairs; Open Exchange Rates is the common commercial feed with intraday granularity. **The choice is per purpose, not per platform** — a tender rate wants intraday, a reporting rate wants the official daily close.","enum":["manual","uaeCentralBank","ecb","openExchangeRates","cardScheme","provider"]},
"FxRateValue": {"x-ticvai-persistence-column":"numeric(18,6)","type":"string","pattern":"^\\d+(\\.\\d{1,6})?$","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one (naming-and-style 5.1). Up to six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly — and stored as `numeric(18,6)` so the six places the wire carries survive the database.\n"},
"GeneratedQuery": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n","properties":{"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"compiledSql":{"type":"string","nullable":true,"description":"The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"}}},
"GroupBooking": {"type":"object","x-ticvai-persistence":"orders.group_booking","description":"BL-028. **`BO-026 Group Bookings` ran on generic order operations** — no group size, no quota, no leader, no per-attendee capture.\n**The leader is the point.** A school booking forty places has one person who pays, one who is called if the coach is late, and forty who need names collecting — and a generic order has one guest.\n","required":["id","orderId","leaderSubjectId","expectedSize","status"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["general","school","corporate","party"],"default":"general"},"packageProductId":{"type":"string","nullable":true,"description":"The school-trip format or party package."},"yearGroup":{"type":"string","maxLength":40,"nullable":true},"accessAndDietaryNeeds":{"type":"string","maxLength":1000,"nullable":true},"celebrantName":{"type":"string","maxLength":120,"nullable":true,"description":"The birthday child."},"celebrantTurningAge":{"type":"integer","minimum":1,"maximum":18,"nullable":true},"allergiesAndRequests":{"type":"string","maxLength":1000,"nullable":true},"finalHeadcountDueBy":{"type":"string","format":"date-time","nullable":true},"quoteSentAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"riskAssessmentSentAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"preferredDate":{"type":"string","format":"date","nullable":true,"description":"The date the guest asked for on `requestGroupBooking` — what its `409 dateUnavailable` is checked against. Null for a group a member of staff built from an order."},"orderId":{"type":"string","format":"uuid"},"leaderSubjectId":{"type":"string","format":"uuid"},"organisationName":{"type":"string","nullable":true},"expectedSize":{"type":"integer"},"confirmedSize":{"type":"integer","nullable":true},"minimumSize":{"type":"integer","nullable":true,"description":"**Below which the group rate does not apply.** A booking for forty that arrives as twelve is a pricing question somebody has to answer at the gate, and stating the threshold means answering it at booking instead.\n"},"attendeeCaptureRequired":{"type":"boolean","default":false,"description":"**Whether names are needed before admission.** A school trip usually needs them and a corporate day out usually does not, and the difference is a safeguarding requirement rather than a preference.\n"},"attendeeCaptureDueBy":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["provisional","confirmed","namesPending","complete","cancelled"]}}},
"ManualDiscountRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","reason","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of this discount, and its idempotency key — it must equal the `Idempotency-Key` header."},"lineId":{"type":"string","format":"uuid","nullable":true,"description":"Omit to discount the order rather than a line."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"percentage":{"type":"number","minimum":0,"maximum":100},"reason":{"type":"string","minLength":3,"maxLength":300,"description":"Required, and free text rather than a code list. A cashier forced to pick the nearest reason picks the first one, and the register stops meaning anything.\n"},"reasonCode":{"type":"string","nullable":true,"description":"Optional alongside the free text, where the venue maintains a list."},"approverPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Required above the venue threshold. May not be the requester."},"recordedAt":{"type":"string","format":"date-time"}}},
"MediaEntitlements": {"type":"object","x-ticvai-persistence":"none — projection over entitlement and scan history","required":["mediaCode","isValid","entitlements"],"properties":{"mediaCode":{"type":"string"},"mediaKind":{"type":"string","enum":["qr","wristband","card","nfc","mobilePass"]},"subjectId":{"type":"string","format":"uuid","nullable":true},"isValid":{"type":"boolean"},"invalidReason":{"type":"string","nullable":true},"canAcceptMore":{"type":"boolean","description":"False where the media has been surrendered, expired or blocked. A cashier should know before taking money, not after.\n"},"entitlements":{"type":"array","items":{"type":"object","properties":{"entitlementId":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","enum":["admission","locker","fnb","retail","parking","rental","experience","membership"]},"orderId":{"type":"string","format":"uuid"},"addedAt":{"type":"string","format":"date-time"},"status":{"allOf":[{"$ref":"#/components/schemas/EntitlementStatus"}],"description":"**Replaced `isRedeemed` on 17 August.** A boolean could not distinguish a ticket that was used from one that expired, was refunded, or was transferred — four different conversations at a gate, and the steward could see only \"not valid\".\n"},"entriesUsed":{"type":"integer"},"entriesAllowed":{"type":"integer","nullable":true},"redeemedAt":{"type":"string","format":"date-time","nullable":true},"transferredToSubjectId":{"type":"string","format":"uuid","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true}}}}}},
"ModifyOrderRequest": {"type":"object","required":["id","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 **of this modification, not of the order** — the order is the path's `orderId`. It is the modification's idempotency key and must equal the `Idempotency-Key` header.\n"},"addLines":{"type":"array","items":{"$ref":"#/components/schemas/CreateOrderLine"}},"removeLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"NaturalLanguageAnswer": {"x-ticvai-persistence":"none — computed","type":"object","required":["conversationId","question","interpretation","result","reliability"],"properties":{"conversationId":{"type":"string"},"question":{"type":"string"},"interpretation":{"type":"string","description":"What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."},"semanticSpec":{"allOf":[{"$ref":"#/components/schemas/ReportingSemanticQuerySpec"}],"nullable":true,"description":"What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"},"generatedQuery":{"allOf":[{"$ref":"#/components/schemas/GeneratedQuery"}],"nullable":true,"description":"The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"},"result":{"allOf":[{"$ref":"#/components/schemas/ReportResult"}],"nullable":true,"description":"Null when the question is outside the semantic model."},"dataAsOf":{"type":"string","format":"date-time","nullable":true,"description":"Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."},"reliability":{"$ref":"#/components/schemas/ReportingAnswerReliability"},"unavailableReason":{"allOf":[{"$ref":"#/components/schemas/ReportingUnavailableReason"}],"nullable":true,"description":"Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."},"confidence":{"type":"number","minimum":0,"maximum":1,"deprecated":true,"description":"Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."},"suggestedFollowUps":{"type":"array","items":{"type":"string"}},"modelVersion":{"type":"string"},"tokensUsed":{"type":"integer"}}},
"OrdChargebackAnalytics": {"x-ticvai-persistence":"none — computed from orders.chargeback and orders.payment on the reporting replica","type":"object","description":"4.2.21. Chargeback measures for a period, in total and per group.","required":["periodFrom","periodTo","groupBy","totals","groups"],"properties":{"periodFrom":{"type":"string","format":"date"},"periodTo":{"type":"string","format":"date"},"groupBy":{"type":"string"},"totals":{"$ref":"#/components/schemas/OrdChargebackMeasures"},"groups":{"type":"array","items":{"allOf":[{"$ref":"#/components/schemas/OrdChargebackMeasures"},{"type":"object","required":["key"],"properties":{"key":{"type":"string","description":"The reason, provider id, outcome, venue id, month (`YYYY-MM`), product id, product category id, or guest `subjectId` (`anonymous` for purchases with no guest) of the group."},"label":{"type":"string","nullable":true,"description":"The display name of the group's key. Null for `customer` unless the caller holds `GUEST_VIEW_PII`."}}}]}}}},
"OrdChargebackMeasures": {"x-ticvai-persistence":"none — computed","type":"object","properties":{"chargebackCount":{"type":"integer"},"chargebackAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"cardPaymentCount":{"type":"integer"},"chargebackRateByCount":{"type":"number","description":"Chargebacks received per card payment captured in the period, as a fraction."},"chargebackRateByValue":{"type":"number"},"decidedCount":{"type":"integer"},"wonCount":{"type":"integer"},"lostCount":{"type":"integer"},"acceptedCount":{"type":"integer"},"expiredCount":{"type":"integer","description":"Lost to a missed evidence deadline."},"winRate":{"type":"number","nullable":true,"description":"Won over decided (won, lost, expired); null with none decided."},"recoveredAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"feeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"openCount":{"type":"integer"}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**The currency the guest selected and is charged in** (CHG-FIN-001, 2 October 2026). Null or equal to `currency` for a sale in the base currency. Everything else on the order, and every ledger posting, stays in the base currency `currency`."},"chargeFxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`), stored on the order so the payment, the receipt, the tax invoice and any refund use the same rate (CHG-FIN-001)."},"chargeFxRateId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `finance.FxRate` row the rate was taken from, for audit."},"chargeTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"`grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to the provider asks for (CHG-FIN-001)."},"chargeRateLockedUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms the new amount (CHG-FIN-001)."},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderExchangeResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["orderId","outgoingValue","incomingValue","difference"],"properties":{"orderId":{"type":"string","format":"uuid"},"outgoingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incomingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"exchangeFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Only the difference settles. The replacement is held before the original is released, never the other way round.\n"},"newLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderModificationResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["order","balanceDue"],"properties":{"order":{"$ref":"#/components/schemas/Order"},"addedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"removedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceDue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Positive means the guest pays; negative means a refund is due."},"refundId":{"type":"string","format":"uuid","nullable":true},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"OrderResumeResult": {"type":"object","x-ticvai-persistence":"none — computed","required":["order","hasChanged"],"properties":{"order":{"$ref":"#/components/schemas/Order"},"hasChanged":{"type":"boolean","description":"True where anything moved while the sale was parked. The cashier decides — silently charging the old price loses money, silently charging the new one loses the guest.\n"},"changes":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["priceChanged","promotionExpired","promotionNowApplies","soldOut","seatHoldExpired","productWithdrawn"]},"lineId":{"type":"string","format":"uuid"},"detail":{"type":"string"},"wasAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"nowAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"OrderStatement": {"x-ticvai-persistence":"none — computed from order, payment, refund and ledger","type":"object","required":["orderId","orderNumber","currency","entries","currentBalance"],"properties":{"orderId":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"entries":{"type":"array","description":"Sequential. What an agent reads to a guest asking about a charge.","items":{"type":"object","required":["kind","amount","runningBalance","occurredAt"],"properties":{"kind":{"type":"string","enum":["sale","payment","refund","void","modification","exchange","fee","variance","chargeback"]},"description":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"runningBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"referenceId":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"occurredAt":{"type":"string","format":"date-time"}}}},"totalPaid":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalRefunded":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"currentBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Positive means the guest owes; negative means a refund is outstanding."}}},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"OrderSummary": {"x-ticvai-persistence":"none — projection","type":"object","required":["id","orderNumber","status","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"The same vocabulary as `Order.channel`, which this projects."},"lineCount":{"type":"integer"},"principalId":{"type":"string","format":"uuid","description":"The cashier who raised it — what the held-orders list shows."},"holdLabel":{"type":"string","nullable":true,"description":"As `Order.holdLabel`."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"description":"As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."},"createdAt":{"type":"string","format":"date-time"}}},
"OrdersDeposit": {"type":"object","x-ticvai-persistence":"orders.deposit","description":"**Taken from the backend workbook, 20 September.** NEW TABLE. Stores the financial/security deposit associated with a rental order, including hold, release, forfeiture, and settlement totals.","required":["orderId","currencyCode","requiredAmount","authorizedAmount","capturedAmount","releasedAmount","forfeitedAmount","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"orderId":{"type":"string","format":"uuid"},"customerId":{"type":"string","format":"uuid","nullable":true},"rentalAgreementId":{"type":"string","format":"uuid","nullable":true},"tableReservationId":{"type":"string","format":"uuid","nullable":true,"description":"The `fnb.TableReservation` this deposit secures, where the venue's `DepositPolicy.dining` is enabled (decided 29 September, rev 3 REV3-8b). Written at checkout from the cart line's `tableReservationId`.\n"},"currencyCode":{"type":"string","maxLength":10},"requiredAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"authorizedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"capturedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"releasedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"forfeitedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","maxLength":30},"settledAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n**Cash at a till only** (CHG-FIN-001, 2 October 2026). A card or wallet payment the guest made in a currency they selected is refunded in that currency (`Refund.tenderCurrency`).\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"PaymentReconciliationExceptionManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Payment Reconciliation & Exception Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"transactionId":{"type":"string","description":"Transaction ID"},"externalReference":{"type":"string","description":"External Reference"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount"},"currency":{"type":"string","description":"Currency"},"date":{"type":"string","format":"date-time","description":"Date"},"merchant":{"type":"string","description":"Merchant"},"order":{"type":"string","description":"Order"},"authorizationCode":{"type":"string","description":"Authorization Code"},"sourceSystem":{"type":"string","enum":["paymentGateway","acquirer","bank","pos","ota","reseller","wallet","erp"],"description":"Source system."},"exceptionType":{"type":"string","description":"Exception, e.g. amount mismatch, unmatched settlement"},"expectedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Expected amount"},"actualAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Actual amount"}}},
"Refund": {"x-ticvai-persistence":"orders.refund","type":"object","required":["id","orderId","amount","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"batchId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"**The rate on the original payment, not today's** (BL-087, CF-118).\n`Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the moment of sale, so the sale rate is always retrievable. **Refunding at today's rate repays a different amount of money than was taken** — a guest who paid 100 USD at 3.67 and is refunded at 3.72 gets back more AED than they gave, and the venue carries the difference on every refund.\nThe exposure runs both ways and neither direction is defensible: a guest short-changed by a moving rate has a complaint the venue cannot answer, because **the guest did nothing but wait.**\n"},"taxReversalEntryId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**A refund reverses the tax entry it created, and this is where that is stated rather than implied.** `reverseJournalEntry` and `calculateTax` both exist, so both halves were present and the obligation was assumed — **an implied obligation is one a developer can miss without failing anything.**\nNull only where the original sale carried no tax.\n"},"settleTo":{"type":"string","enum":["originalTender","advanceBalance","wireTransfer","storeCredit"],"default":"originalTender","description":"BL-086. **A refund could only go back the way it came.** A guest whose card has expired, a partner settling by wire, a guest who would rather have the credit — three real cases with one answer.\n**`originalTender` stays the default** because refunding elsewhere is how money laundering works, and anything else needs a reason.\n\n**`storeCredit` is a gift card issued for the refund amount** (decided 2 October 2026, Chinmay, batch 1, POS-011; DEC-061; CHG-CSP-037; DI-796), never a voucher or a wallet top-up.\n"},"fxVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Where the sale rate and the current rate differ, **the difference is booked as an FX variance rather than hidden in the refund**. `runFxRevaluation` already handles this class of movement and this is the same act at a smaller scale.\n"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**A refund goes back in the currency the guest paid** (decided 2 October 2026, Chinmay; CHG-FIN-001). For a card or wallet payment taken in a guest-selected currency, the refund request to the provider is in that currency, and `tenderAmount` is the refunded share of the original `Payment.tenderAmount` at the sale rate (`fxRate`), so a full refund returns exactly what was charged. `amount` stays in base currency for the ledger. Null for a refund in the base currency. Foreign cash refunded at a till is paid in base currency (DI-282)."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The refund in `tenderCurrency`, at that currency's own scale (CHG-FIN-001)."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPercentage":{"type":"number","description":"From the venue's time bands, or an approver override."},"status":{"type":"string","enum":["pendingApproval","pendingGateway","completed","declined","failed"]},"reason":{"type":"string"},"requestedByPrincipalId":{"type":"string","format":"uuid"},"secondaryPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"ledgerEntryId":{"type":"string","format":"uuid","nullable":true,"description":"Written before the gateway is called."},"gatewayReference":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"RefundPolicy": {"x-ticvai-persistence":"orders.refund_policy + orders.refund_policy_time_band","type":"object","description":"Venue-configured. Thresholds are policy, not permission scope — venues run different policies and the permission model should not encode commercial rules.\n**The three thresholds must ascend** (decided 28 September, audit R123 (6)): `selfAuthoriseLimit` <= `requiresSecondUserAbove` <= `requiresApprovalAbove`, where the second is set. `setRefundPolicy` refuses a policy that does not with 422 `refund-thresholds-not-ascending`.\n","required":["venueId","selfAuthoriseLimit","requiresApprovalAbove"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The venue in the path. Not taken from a `setRefundPolicy` body."},"selfAuthoriseLimit":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Up to this, a holder of ORDER_REFUND refunds alone. Zero means every refund needs a second authoriser.\n"},"requiresSecondUserAbove":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Above this, a second user — cashier OR supervisor — names themselves as audit control. Dual-authorisation, not escalation (2.12.3).\n"},"requiresApprovalAbove":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Above this, an ORDER_REFUND_APPROVE holder must approve."},"timeBands":{"type":"array","description":"Refundable percentage by time before the performance. Evaluated most-specific first.\n","items":{"type":"object","required":["hoursBefore","percentage"],"properties":{"hoursBefore":{"type":"integer","minimum":0},"percentage":{"type":"number","minimum":0,"maximum":100}}}},"allowPartial":{"type":"boolean","default":true},"refundWindowDays":{"type":"integer","nullable":true,"minimum":0,"description":"Days after purchase within which a refund may be made. 0 is allowed and means the day of purchase only; null means no window (decided 28 September, audit R123 (6))."},"varianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Price variance above this is an exception requiring review rather than a routine posting (CF-38). Venue-configured.\n**A venue setting with a tenant default** (decided 28 September, audit R094). **Proposed default, client to correct (audit R094): AED 5.00 per order line.**\n"}}},
"ReportCategory": {"type":"string","enum":["sales","admission","financial","inventory","guest","operations","marketing","workforce","compliance","custom"]},
"ReportColumn": {"x-ticvai-persistence":"reporting.report_column","type":"object","required":["field"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"field":{"type":"string"},"label":{"type":"string"},"aggregation":{"allOf":[{"$ref":"#/components/schemas/Aggregation"}],"default":"none"},"sortOrder":{"type":"integer"},"sortDirection":{"type":"string","enum":["asc","desc"]},"format":{"type":"string","nullable":true},"role":{"type":"string","nullable":true,"enum":["dimension","measure"],"description":"**What the column is to a chart** (decided 2 October 2026, Chinmay; CHG-FIN-007). A `dimension` groups (date, venue, channel, product); a `measure` is aggregated (sum of net revenue, count of admissions). Null on a column only a table shows."},"encoding":{"type":"string","nullable":true,"enum":["category","x","y","series","value","size","colour","location","stage","source","target","row","column","hierarchyLevel","label","tooltip"],"description":"**Which field well the column fills** (CHG-FIN-007), the binding the twenty marks of `DashboardTile.visualisation` need. The per-mark rule is on that field."},"axis":{"type":"string","nullable":true,"enum":["primary","secondary"],"description":"For a measure on a `combo`, the axis it is drawn against. A secondary axis needs its own `unitLabel` (CHG-FIN-007)."},"seriesType":{"type":"string","nullable":true,"enum":["bar","line","area"],"description":"For a measure on a `combo`, how that series is drawn (CHG-FIN-007)."},"hierarchyLevel":{"type":"integer","nullable":true,"minimum":1,"description":"For `matrix` rows and columns, `treemap` nesting and `decompositionTree` levels, the depth of this dimension, 1 outermost. Levels must follow a real hierarchy (DI-709), for example year, month, day, or region, venue, outlet (CHG-FIN-007)."},"unitLabel":{"type":"string","nullable":true,"maxLength":40,"description":"The unit an axis states, for example \"AED\" or \"Admissions\". Required on a secondary axis (CHG-FIN-007)."}}},
"ReportDefinition": {"x-ticvai-persistence":"reporting.report_definition + reporting.report_column + reporting.report_filter","allOf":[{"$ref":"#/components/schemas/CreateReportRequest"},{"type":"object","required":["id","version","isSystem","isRetired","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"version":{"type":"string","description":"The current version. Assigned by the server on each publish; earlier ones are kept as `ReportDefinitionVersion`."},"isSystem":{"type":"boolean","description":"Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). **Clone-only (decided 28 September, audit R096)**: `updateReport` and `deleteReport` refuse it with 409 `system-report`; a venue changes a copy made with `createReport`.\n"},"isRetired":{"type":"boolean"},"estimatedCost":{"type":"string","enum":["low","medium","high"],"description":"Informs whether it may run inline or must be queued."},"createdByPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}}]},
"ReportFilter": {"x-ticvai-persistence":"reporting.report_filter","type":"object","required":["field","operator"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"field":{"type":"string"},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","contains","isNull","isNotNull"]},"value":{"description":"**Open on purpose; its type is the field's.** One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a string. Absent for `in`, `notIn`, `between`, `isNull` and `isNotNull`.\n"},"values":{"type":"array","description":"The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`.","items":{}},"isParameter":{"type":"boolean","default":false,"description":"Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope.\n"}}},
"ReportParameter": {"x-ticvai-persistence":"reporting.report_parameter","type":"object","required":["key","label","type","isRequired"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"},"isRequired":{"type":"boolean"},"defaultValue":{"description":"Open on purpose. A value of this parameter's `type`, used when a run supplies none."}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"ReportingAnswerReliability": {"type":"string","description":"**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},
"ReportingSemanticQuerySpec": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n","required":["metric","period"],"properties":{"metric":{"type":"string","description":"A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."},"dimensions":{"type":"array","maxItems":5,"description":"Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.","items":{"type":"string"}},"filters":{"type":"array","items":{"type":"object","required":["field","operator"],"properties":{"field":{"type":"string","description":"A `SemanticModel` field code."},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","isNull","isNotNull"]},"values":{"type":"array","description":"**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n","items":{}}}}},"period":{"type":"string","description":"ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."},"comparison":{"type":"string","nullable":true,"description":"As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.","enum":["previousPeriod","samePeriodLastYear","target","benchmark"]},"semanticModelVersion":{"type":"integer","readOnly":true,"description":"The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."}}},
"ReportingUnavailableReason": {"type":"string","description":"Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.","enum":["metricNotModelled","dimensionNotModelled","filterNotModelled","comparisonNotAvailable","periodOutsideHistory"]},
"RunReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","properties":{"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"},"venueId":{"type":"string","format":"uuid","description":"Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"},"dateFrom":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."},"dateTo":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (audit R158)."},"forceAsync":{"type":"boolean","default":false,"description":"Queue regardless of size, for a result to be collected later."}}},
"SaleBoardKind": {"type":"string","enum":["ticketing","fnb","retail","mixed"]},
"Settlement": {"x-ticvai-persistence":"ledger.settlement","type":"object","required":["id","providerName","periodStart","periodEnd","status","ingestedAt"],"properties":{"id":{"type":"string","format":"uuid"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","description":"**A settlement has no account, so nothing else denominates it.** A posting takes its currency from `ledger.account.currency` and a payment from `tenderCurrency`, but a settlement is a provider file for a period: `providerGross`, `ledgerGross` and `difference` are bare amounts, and a provider file in one currency against a ledger in another computes a difference that means nothing. Added 20 September, when a venue became able to trade outside its region's currency.\n"},"providerName":{"type":"string"},"venueId":{"type":"string","format":"uuid","description":"The venue this settlement is for. **Reconciled daily per venue** (decided 28 September, audit R110 (b)), so `periodStart` and `periodEnd` are the same day."},"periodStart":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"periodEnd":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"fileReference":{"type":"string","format":"uuid","description":"The `MediaAsset` holding the provider file, as given to `ingestSettlementFile`. **Kept on the row because parsing is asynchronous**: the job that parses the file reads it from here.\n"},"format":{"type":"string","nullable":true,"enum":["csv","fixedWidth","xml","json"],"description":"The file format given at ingest. Null when none was given."},"status":{"$ref":"#/components/schemas/SettlementStatus"},"lineCount":{"type":"integer"},"matchedCount":{"type":"integer"},"exceptionCount":{"type":"integer"},"providerGross":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"providerFees":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"providerNet":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ledgerGross":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ingestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `region` scope.**"}}},
"SettlementException": {"x-ticvai-persistence":"ledger.settlement_exception","type":"object","required":["id","settlementId","kind","providerReference","amount"],"properties":{"id":{"type":"string","format":"uuid","description":"Server-created when parsing finds the exception, so a UUID (naming-and-style 4)."},"settlementId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["unmatchedInProvider","unmatchedInLedger","amountMismatch","duplicateInProvider","feeUnexplained"]},"providerReference":{"type":"string","nullable":true},"paymentId":{"type":"string","format":"uuid","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"expectedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"resolution":{"allOf":[{"$ref":"#/components/schemas/SettlementResolution"}],"nullable":true,"description":"Null while the exception is open."},"note":{"type":"string","nullable":true,"description":"The `note` given to `resolveSettlementException`, stored with the resolution."},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"SettlementResolution": {"type":"string","description":"How a settlement exception was explained. One vocabulary for the request and the stored exception.","enum":["matchedManually","writeOff","disputeRaised","providerError","timingDifference"]},
"SettlementStatus": {"type":"string","enum":["ingesting","parsing","matching","matched","hasExceptions","resolved","failed"]},
"Shift": {"x-ticvai-persistence":"orders.pos_shift + orders.pos_shift_approval + orders.pos_shift_incident","description":"**`approvals` and `incidents` are child rows** (26 September, pull audit R099): `orders.pos_shift_approval` and `orders.pos_shift_incident`, one row per item, keyed to the shift. Until then the contract carried both and `orders.pos_shift` had nowhere to put either.\n","type":"object","required":["id","workstationId","venueId","scopePath","principalId","status","currency","currencyScale","openedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key."},"workstationId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"principalId":{"type":"string","format":"uuid","description":"Who opened it. Cash reconciles to a person and a drawer."},"principalDisplayName":{"type":"string"},"incidents":{"type":"array","description":"BL-097. **A till has exceptions and there was nowhere to write them** — a no-sale, a drawer opened without a transaction, a manager override, a guest dispute.\n**This is the log a cash-up investigation starts from**, and a shift that balances with four unexplained no-sales is not a shift that balanced.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["noSale","drawerOpen","override","voidAfterPayment","guestDispute","tillJam","priceQuery","other"]},"at":{"type":"string","format":"date-time"},"principalId":{"type":"string","format":"uuid"},"note":{"type":"string","nullable":true}}}},"status":{"$ref":"#/components/schemas/ShiftStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"depositBoxCode":{"type":"string","nullable":true},"bagNumber":{"type":"string","nullable":true},"openingFloat":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"salesTotal":{"x-ticvai-column":"gross_sales_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till took in sales, as the guest paid it — tax included: the shift's takings, not Gross sales (CHG-FIN-002, CHG-FIN-010). **Never shown to the shift's own cashier before the count is in** (CHG-FIN-003): with the float and the lifts it gives away the expected cash.\n"},"refundsTotal":{"x-ticvai-column":"gross_refunded_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till paid back, as the guest was refunded it — tax included."},"liftsTotal":{"x-ticvai-column":"lifted_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net."},"expectedCash":{"x-ticvai-column":"expected_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"26 September, pull audit R207. **The figure the blind count was measured against**, revealed once the count is in — null until then. Until this date only `ShiftCloseResult` carried it, returned once by `closeShift`, so BO-040 could not show the over/short it exists to accept. **Null to the shift's own cashier on every read** (CHG-FIN-003, 2 October): returned only to a caller holding OVERSHORT_ACCEPT or SHIFT_CLOSE_OTHER at the venue.\n"},"countedCash":{"x-ticvai-column":"counted_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"What the close count found. Null until the shift is counted."},"variance":{"x-ticvai-column":"variance_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"Counted minus expected, as `ShiftCloseResult.variance`. Negative is short. Null to the shift's own cashier, as `expectedCash` (CHG-FIN-003)."},"cashierReason":{"type":"string","nullable":true,"readOnly":true,"enum":["tillError","unrecordedRefund","miscount","other"],"description":"What the cashier said went wrong, given with the blind count (`CloseShiftRequest.cashierReason`, DI-803) without seeing the variance; the supervisor reads it beside the variance on BO-040 (CHG-FIN-003).\n"},"cashierNote":{"type":"string","nullable":true,"readOnly":true,"maxLength":1000,"description":"The cashier's note with the count (`CloseShiftRequest.notes`; CHG-FIN-003)."},"heldLeaseCount":{"type":"integer","description":"Inventory leases currently held by this workstation. Surfaced so an operator closing a shift can see what will be returned.\n"},"openedAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time","description":"When the device recorded the open. `openedAt` is the server's time."},"suspendedAt":{"type":"string","format":"date-time","nullable":true},"suspendReason":{"type":"string","maxLength":200,"nullable":true,"description":"The `reason` given to `suspendShift`. Cleared on resume."},"closedAt":{"type":"string","format":"date-time","nullable":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who submitted the close count. `reopenShift` refuses an approver who is this principal, and until 26 September there was nothing to compare against (pull audit R099).\n"},"recountRequestedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `rejectShiftVariance`, cleared by the cashier's recount** (decided 2 October 2026, Chinmay; DEC-175; CHG-CSP-013; DI-804). While set, the shift is `pendingVariance` waiting for the cashier rather than the supervisor: the cashier's view says \"Recount requested\" instead of \"Under review\".\n"},"recountRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The supervisor who sent the count back (CHG-CSP-013)."},"recountReason":{"type":"string","nullable":true,"readOnly":true,"maxLength":500,"description":"The supervisor's reason, shown to the cashier; never an amount (CHG-CSP-013, CHG-FIN-003)."},"countNumber":{"type":"integer","minimum":0,"readOnly":true,"description":"How many close counts the shift has had: 0 before the first, 1 after it, 2 after a recount (CHG-CSP-013). The latest is the one measured.\n"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while the shift has unsynced operations."},"approvals":{"type":"array","items":{"type":"object","required":["kind","principalId","at"],"properties":{"kind":{"type":"string","enum":["open","close","variance"],"description":"`open` from `approveShiftOpen`, `close` from `approveShiftClose`, `variance` from `acceptShiftVariance`.\n"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"reason":{"type":"string"}}}}}},
"ShiftCloseResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["shift","expectedCash","countedCash","variance","requiresAcceptance"],"properties":{"shift":{"$ref":"#/components/schemas/Shift"},"expectedCash":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"countedCash":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Counted minus expected. Negative is short."},"requiresAcceptance":{"type":"boolean","description":"True when the variance exceeds the venue's `shiftVarianceThreshold` (audit R094). The shift is then `pendingVariance` and only `acceptShiftVariance` finalises it (audit R080 (e)).\n"},"nonCashVariances":{"type":"array","items":{"type":"object","required":["tender","declared","captured","variance"],"properties":{"tender":{"type":"string"},"declared":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"captured":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"ShiftStatus": {"type":"string","enum":["pendingApproval","open","suspended","pendingVariance","pendingClosure","closed","autoClosed"]},
"TenderKind": {"type":"string","description":"`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n","enum":["cash","card","wallet","voucher","bankTransfer","hotelCharge","installment","giftCard","complimentary"]},
"TicketReissueFulfillmentRegenerationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Ticket Reissue & Fulfillment Regeneration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"maximumReissues":{"type":"string","description":"Maximum Reissues"},"freeReissueCount":{"type":"integer","description":"Free Reissue Count"},"supervisorThreshold":{"type":"integer","description":"Supervisor Threshold"},"reissueReason":{"type":"string","enum":["dateChanged","timeslotChanged","seatChanged","attendeeChanged","lostTicket","damagedCredential","emailNotReceived","walletPassIssue","printingError","credentialCompromised","administrativeCorrection"],"description":"Why the ticket is reissued."},"credentialMedia":{"type":"string","enum":["qr","dynamicQr","barcode","rfid","nfc","printedTicket","wearable"],"description":"Credential media regenerated."},"deliveryMethod":{"type":"string","enum":["email","smsWhatsappLink","mobileApp","walletPass","walletUpdate","posPrint","boxOfficeCollection"],"description":"How the reissue is delivered."},"reissueOption":{"type":"string","enum":["regenerateNew","resendExisting"],"description":"Regenerate a new credential (old one invalidated) or resend the existing one"}}},
"UpdateGroupBookingRequest": {"type":"object","description":"Request only. Every field optional; absent means unchanged.","properties":{"packageProductId":{"type":"string","nullable":true,"description":"The school-trip format or party package."},"yearGroup":{"type":"string","maxLength":40,"nullable":true},"accessAndDietaryNeeds":{"type":"string","maxLength":1000,"nullable":true},"celebrantName":{"type":"string","maxLength":120,"nullable":true,"description":"The birthday child."},"celebrantTurningAge":{"type":"integer","minimum":1,"maximum":18,"nullable":true},"allergiesAndRequests":{"type":"string","maxLength":1000,"nullable":true},"finalHeadcountDueBy":{"type":"string","format":"date-time","nullable":true},"leaderSubjectId":{"type":"string","format":"uuid"},"organisationName":{"type":"string","maxLength":200,"nullable":true},"expectedSize":{"type":"integer","minimum":2},"confirmedSize":{"type":"integer","minimum":0},"minimumSize":{"type":"integer","minimum":1,"nullable":true},"attendeeCaptureRequired":{"type":"boolean"},"attendeeCaptureDueBy":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["confirmed","namesPending","complete","cancelled"]}}},
"VoidReason": {"type":"string","description":"**The void reason list** (decided 28 September, audit R125 (4)): the one list `voidOrder` takes, and the list `fnb.amendFnbOrder` and `fnb.cancelFnbOrder` point to. `other` requires a note (audit R222), and the notes are reviewed quarterly to add real reasons. Proposed, client to correct.\n","enum":["guestChangedMind","enteredInError","itemUnavailable","qualityIssue","duplicate","other"]},
"WithdrawalReason": {"type":"string","description":"Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records.","enum":["banking","safeDrop","changeOrder","other"]},
"Workstation": {"x-ticvai-persistence":"platform.workstation","type":"object","required":["id","code","name","venueId","regionId","scopePath","saleBoard","currency","currencyScale","timeZone"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"**The outlet this till stands in** (CHG-CSP-006). Its board is the till's board unless the till overrides it. Null on a workstation that belongs to no outlet (a ticket office counter set up before outlets), which must then carry its own board.\n"},"scopePath":{"type":"string"},"saleBoard":{"type":"object","description":"Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. What the operator may then DO within it is governed by their permissions.\n**The effective board** since 2 October 2026 (DEC-183; CHG-CSP-006): the till's own when it overrides the outlet, otherwise the outlet's (`saleBoardSource`).\n","required":["id","kind"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SaleBoardKind"},"name":{"type":"string"}}},"saleBoardSource":{"type":"string","enum":["outlet","workstation"],"readOnly":true,"description":"**Where `saleBoard` came from** (decided 2 October 2026, Chinmay, BO-109: \"Per outlet, with a till override\"; DEC-183; CHG-CSP-006): `outlet` when the till uses its outlet's layout, `workstation` when this till overrides it. BO-109 shows which tills differ from their outlet.\n"},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**This till's drawer limit, overriding the venue's** (`VenueSettings.cashDrawerLimit`; DEC-179; CHG-CSP-016). Null inherits the venue's. Above it the till warns and offers a cash lift.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point.\n"},"devices":{"type":"array","items":{"$ref":"#/components/schemas/DeviceBinding"}},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"timeZone":{"type":"string"},"deploymentProfile":{"$ref":"#/components/schemas/DeploymentProfile"},"edgeNodeId":{"type":"string","format":"uuid","nullable":true,"description":"Present when `deploymentProfile` is `venueEdge`."},"healthScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"readOnly":true,"description":"Board 1 of the client's POS set. **A number a manager can sort by** — the package held `lastHeartbeatAt` and a heartbeat timestamp is not a score.\nThe client's board shows 1,248 workstations at 96% healthy, and **the value of that figure is that it ranks**: a fleet dashboard exists so somebody can open the worst one first.\n**Derived from its devices, its heartbeat age, its firmware currency and its error rate.** Read-only, because a workstation that could set its own score would.\n**The formula, proposed, client to correct (audit R096 (2)):** score = 40% device online share (the share of its devices reporting online) + 25% heartbeat freshness (100 at one minute old or less, 0 at 15 minutes or more, linear between) + 20% firmware and profile currency (100 on the latest, 50 one version behind, 0 older) + 15% error rate (100 at 0 errors an hour, 0 at 10 or more, linear between), rounded to a whole number. **Below 80 is a warning and below 60 a failure.**\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"description":"Which profile this workstation runs, and at which version. **The client's board shows a fleet split four ways — 72% latest, 18.8% one behind, 6.1% outdated** — and the package had a firmware version field and no profile.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks*.\n"},"catalogueState":{"$ref":"#/components/schemas/CatalogueState"},"offlineCapable":{"type":"boolean","description":"Derived from `deploymentProfile`. False only for `thin`. Under local-first, catalogue READS are always local on transactional surfaces; this flag governs whether WRITES can be queued.\n"},"isActive":{"type":"boolean"}}}
}
```
