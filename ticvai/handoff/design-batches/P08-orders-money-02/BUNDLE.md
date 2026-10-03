# P08-orders-money-02 — P08 · Orders & Money (2 of 3)

**10 screens · 66 operations · 88 schemas · 28 permissions**

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
  `ACCOUNT_CONFIGURE, CASH_LIFT, LEDGER_VIEW, ORDER_CREATE, ORDER_DISCOUNT, ORDER_EXCHANGE, ORDER_MODIFY, ORDER_REFUND, ORDER_REPRINT, ORDER_RESCHEDULE, ORDER_VIEW, ORDER_VOID`…. A control nobody can use must say so,
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
| `BO-041` | Cash Movements | B–D | 18 | 28 | 6 | 1 | 0 | 6 | — | notStarted (generated) |
| `BO-042` | Banking & Safe | B–D | 27 | 26 | 6 | 18 | 0 | 0 | — | notStarted (generated) |
| `BO-043` | Daily Reconciliation | B–D | 34 | 66 | 6 | 24 | 3 | 0 | — | notStarted (generated) |
| `BO-047` | Order Corrections & Exceptions | B–D | 127 | 39 | 6 | 70 | 0 | 0 | — | notStarted (generated) |
| `BO-048` | Retail Products | B–D | 26 | 19 | 6 | 5 | 1 | 0 | — | notStarted (generated) |
| `BO-059` | Sales Reports | B–D | 76 | 20 | 6 | 93 | 3 | 0 | — | notStarted (generated) |
| `BO-061` | Scheduled Reports | B–D | 26 | 12 | 6 | 7 | 0 | 0 | — | notStarted (generated) |
| `BO-062` | Venue Profile | B–D | 9 | 7 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-065` | Venue Configuration | A | 98 | 16 | 6 | 17 | 2 | 0 | — | notStarted (generated) |
| `BO-074` | Chart of Accounts | A | 35 | 26 | 6 | 39 | 2 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-062 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-041` Cash Movements

**Track money in and out of a drawer that is not a sale.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASH_LIFT`, `REPORT_VIEW_WORKSTATION` (2 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (compact density): `listCashMovements` queues a shift's lifts, adds and no-sales for review; the reviewer records a correcting lift or add with `createCashMovement` — every row is looked at, so the empty state is … |
| Offline | online only |
| Opens with | `shiftId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/venue-operations/cash-movements` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Kept separate from BO-042, each with its own operations (decided 28 September, audit R276)** — the two carried the same thirteen shift operations. This screen keeps cash lifts, adds and no-sales (`listCashMovements`, `createCashMovement`, `recordNoSale`) with the shift they belong to; opening, suspending, closing and reopening shifts stay on BO-039 and BO-040, and banking and safe drops are BO-042.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): A no-sale is a drawer opening at a till (F32 step 5, POS-020); recorded from a browser it opens no drawer and fabricates an incident. Keep the log, drop the act …

**From the Food, Beverage & Retail process.** The log of cash that moves in or out of a till without a sale: opening float, cash out (lift), cash in (add), safe drops and banking taken from a box, and no-sales. A supervisor or the cash office reads it per shift to see who moved what, when, authorised by whom and witnessed by whom. One thing to get right: it is a log, read per shift, and every movement changes the expected figure at close — so a mistaken entry is corrected by a second movement with a reason, never edited.

**Known correction pending (do not draw the wrong version)**

- **listCashMovements is per shift (path shiftId); there is no venue- or day-level movement list.** Why: "Every cash movement" across tills cannot be shown; the design is shift-first until a venue-level read exists. *(source: contracts/spine/shift.yaml#listCashMovements; Food, Beverage & Retail)*
- **Pattern approvalInbox with a table titled "Waiting for a decision" and "nothing waiting is the good outcome".** Why: Cash movements await no decision; this is a log. *(source: screens/P08-venue-back-office.yaml#BO-041; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): "Record no sale" (recordNoSale) is an action on the back-office screen. (CHG-WIR-008); No read returns no-sales; listCashMovements returns lifts, adds and the float only. (CHG-WIR-008); Button label "Create cash movement"; columns id, shiftId, sequence, syncedAt, authorisedByPrincipalId as raw ids; exit to BO-008 Product … (CHG-WIR-009).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should a lift or add be recordable from the back office at all, when the cash is at the till?** → Drawn default stands (answer: "Yes: supervisor entry with mandatory reason"): Keep it (R276 kept createCashMovement here) as a supervisor entry with a mandatory reason. *(decided by Chinmay, 2026-10-02; DEC-177 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listShifts` ?workstationId |
| Status | select | — | Pending approval · Open · Suspended · Pending variance · Pending closure · Closed · Auto closed | `listShifts` ?status |
| Opened from | date and time picker | — | — | `listShifts` ?openedFrom |
| Opened to | date and time picker | — | — | `listShifts` ?openedTo |

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

- **Shift**: Pick the shift first (till, cashier, date) from the shift list; the movement list is per shift. Default: shifts open now at the user's outlets. *(source: contracts/spine/shift.yaml#listCashMovements / contracts/spine/shift.yaml#listShifts)*
- **Record cash out / cash in — type**: Two choices only, Cash out (lift) and Cash in (add). Opening float is never chosen here (openShift writes it). *(source: contracts/spine/shift.yaml#/components/schemas/CashMovementKind / DI-274)*
- **Amount**: Either a total or a denomination count (notes and coins of the region, counting order, note images, typed quantities); when both are given the denomination count wins. Cash out may not exceed the float counted at the last count, less cash out since, plus cash in since — cash taken in sales since the last count does not count towards it. *(source: R123 / DI-775 / DI-776 / contracts/spine/shift.yaml#createCashMovement)*
- **Reference and reason**: Reference is the safe-drop reference or bag number (max 64); reason max 500, required in practice for any back-office entry. *(source: contracts/spine/shift.yaml#createCashMovement / R222)*

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listCashMovements`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Opening float, Lift, Add | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Reference | text | Safe drop reference or bag number. |
| Reason | text | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Synced at | 1 Oct 2026, 14:30 | — |

**Every shift** (data table, from `listShifts`)

| Shows | Format | Notes |
|---|---|---|
| Principal display name | text | — |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |

**The selected cash movement** (detail panel, from `listCashMovements`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Opening float, Lift, Add | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Denominations | list or chips (count when long) | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. |
| Reference | text | Safe drop reference or bag number. |
| Reason | text | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Withdrawal reason | chip: Banking, Safe drop, Change order, Other | Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records. |
| Synced at | 1 Oct 2026, 14:30 | — |

**The shift** (detail panel, from `getShift`)

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create cash movement (primary button) | `createCashMovement` POST `/shifts/{shiftId}/cash-movements` | CreateCashMovementRequest | CashMovement | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since … | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Movement rows**: In sequence order: time (GST), type (Opening float, Cash out, Cash in, Safe drop, Banking, Change order — from kind and withdrawal reason), amount signed (out negative), denominations summary, reference, reason, authorised by, witness (the cashier, on box withdrawals). A row recorded offline and not yet synced is marked. *(source: contracts/spine/shift.yaml#/components/schemas/CashMovement)*
- **No-sales**: Listed with reason (Change for guest, Correct float, Retrieve dropped cash, Till check, Other + note) and a running count per shift; "9 no-sales, 4 sales" is emphasised. *(source: contracts/spine/shift.yaml#recordNoSale / F32 step 5)*
- **Shift header**: Till, cashier, status, opening float, cash out total, cash in total; expected cash only after the shift is counted. *(source: contracts/spine/shift.yaml#getShift)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Record cash out / cash in**: Confirm names the till, cashier and amount ("Cash out AED 1,000.00 from Till 3 — Priya Nair"). Success adds the row and lowers/raises the expected close figure. Refusals: "The shift is not open"; "More than the counted float available (AED 1,250.00)". *(source: contracts/spine/shift.yaml#createCashMovement / R123)*

**Data it reads**: `listCashMovements` (onLoad, Lifts, adds and the opening float); `getShift` (onLoad, Read a shift); `listShifts` (onLoad, List shifts)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cash movements list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cash movements untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCashMovements` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listCashMovements` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CASH_LIFT` for `createCashMovement`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since (`lift-exceeds-float`, audit R123 … |

#### Edge cases to draw

- **Movements recorded on an offline till**: Arrive later but keep their sequence; the list orders by sequence, not by arrival. *(source: contracts/spine/shift.yaml#/components/schemas/CashMovement)*
- **Shift already closed**: No record action; a correction after close goes through Reopen shift (BO-039). *(source: contracts/spine/shift.yaml#createCashMovement / R144)*

#### Consistency with other screens

- Match `POS-017`: Cash In / Cash Out at the till records the same movements; same type words.
- Match `BO-042`: A safe drop or banking from a box appears here as a lift with its reason.
- Match `POS-020`: No-sales are recorded at the till (Shift Exceptions & Alerts); this screen only lists them.
- Match `BO-039`: The shift detail there uses this row format.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
shift:
  till: Till 3 — Bite & Go
  cashier: Priya Nair
  date: 14 Oct 2026
movements:
- seq: 1
  time: 06:58
  type: Opening float
  amount: AED 500.00
  denominations: 5 × 50, 10 × 20, 5 × 10
- seq: 2
  time: '12:15'
  type: Safe drop
  amount: AED −2,000.00
  reference: SD-0451
  authorised_by: Omar Ziad
  witness: Priya Nair
- seq: 3
  time: '14:40'
  type: Cash in
  amount: AED +200.00
  reason: 'Change top-up: 25 fils and 1 AED coins'
  authorised_by: Omar Ziad
no_sales:
- time: '10:02'
  reason: Change for guest
- time: '11:47'
  reason: Till check
```

#### Permissions

- `listCashMovements` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `createCashMovement` → `CASH_LIFT` (operate) · staff
- `getShift` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listShifts` → `REPORT_VIEW_WORKSTATION` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listCashMovements` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CASH_LIFT` for `createCashMovement`.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.44 | Incident & Exception Logging | Ticketing Sales | CONTRACTED | data `Shift` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-041` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-041?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create cash movement.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `CASH_LIFT`, `REPORT_VIEW_WORKSTATION`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-042` Banking & Safe

**Move the day’s cash out of the tills.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASH_LIFT`, `SHIFT_OPEN`, `TENANT_VIEW` (2 operate, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (compact density): `listDepositBoxes` queues the boxes holding cash; a supervisor takes cash out of each for banking or the safe with `withdrawFromDepositBox` — every open box is waiting for a person, so the empty … |
| Offline | online only |
| Opens with | `boxId` (navigation), `shiftId` (navigation), `venueId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/venue-operations/banking-safe` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Kept separate from BO-041, each with its own operations (decided 28 September, audit R276)** — the two carried the same thirteen shift operations. This screen moves cash out of the tills — `listDepositBoxes` and `withdrawFromDepositBox` with reason banking or safeDrop — and reads the lifts that result; cash lifts and adds at a till are BO-041, and the shift lifecycle stays on BO-039 and BO-040.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): The box list is the queue; the "Waiting for a decision" cash-movement table and the "Every shift" table were bulk plumbing (R251; design-notes correction … Removed 2 October 2026 (CHG-WIR-008): The box list is the queue; the "Waiting for a decision" cash-movement table and the "Every shift" table were bulk plumbing (R251; design-notes correction … Removed 2 October 2026 (CHG-WIR-008): The box list is the queue; the "Waiting for a decision" cash-movement table and the "Every shift" table were bulk plumbing (R251; design-notes correction …

**From the Food, Beverage & Retail process.** The cash office takes cash out of cashiers' deposit boxes mid-shift — to the safe or for banking — so a busy drawer never holds more than it should. Each withdrawal is a lift that lowers the box's expected close figure, so it is never a variance. Two people sign: the supervisor taking it and the cashier it came from. One thing to get right: a deposit box belongs to a cashier, not a till — the list is by cashier, with the till they are on now.

**Known correction pending (do not draw the wrong version)**

- **"Banking & Safe" has no safe or bank side: no operation records the safe balance, a bank deposit (bag, slip, bank, date) or the transfer from safe to bank; F32 step 8 uses finance.settleDeposit, which settles a guest's held deposit, not a cash banking.** Why: The screen can only take cash out of boxes; the "deposited" figure DI-275 reconciles against has no source. *(source: F32 step 8 / DI-275 / contracts/spine/finance.yaml#settleDeposit; Food, Beverage & Retail)*
- **listDepositBoxes requires SHIFT_OPEN.** Why: A cash-office supervisor reading boxes in the back office should not need the permission to open a till shift; a permission borrowed from the wrong act. *(source: contracts/spine/shift.yaml#listDepositBoxes / R091; Food, Beverage & Retail)*

**Fixed on main** (the package already carries these; draw what it says): Bulk tables "Waiting for a decision" (every cash movement) and "Every shift" with raw ids; approvalInbox empty state; exit to BO-008; entry … (CHG-WIR-009).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How does the cashier sign as witness — PIN step-up on the same device, or named only?** → The cashier signs as witness with a PIN on the same device (step-up). *(decided by Chinmay, 2026-10-02; DEC-178 / CHG-NOTE-004)*
- **Where is the drawer ceiling configured, so the screen can flag boxes over it?** → Drawer limit setting: the till warns when the drawer is over the limit and offers a cash lift. *(decided by Chinmay, 2026-10-02; DEC-179 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Open only | toggle | — | — | `listDepositBoxes` ?openOnly |

**Form: Bank or safe-drop cash** (modal, opened by *Bank or safe-drop cash*; *Bank or safe-drop cash* calls `withdrawFromDepositBox`, *Cancel* sends nothing)

**Collects what `withdrawFromDepositBox` sends before it is called.** Required: `amount`, `witnessPrincipalId`. Optional: `reason`, `note`. `id` is a client UUIDv7 generated silently, never asked. **The cashier signs as witness with their own PIN on the same device (decided 2 October 2026 by Chinmay, DEC-178; CHG-CSP-015).** `recordedAt` is the device clock. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the `CashMovement` this records. | `withdrawFromDepositBox` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `withdrawFromDepositBox` body |
| Witness principal `witnessPrincipalId` | picker: choose a witness principal | required | — | — | shows names, sends the id | The cashier the cash came from. Kept as `CashMovement.witnessPrincipalId`. | `withdrawFromDepositBox` body |
| Reason `reason` | radio group | optional | — | Banking · Safe drop · Change order · Other | — | Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records. | `withdrawFromDepositBox` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `withdrawFromDepositBox` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `withdrawFromDepositBox` body |
| Witness step up `witnessStepUp` | group | optional | — | — | — | The witnessing cashier's countersignature on this device (CHG-RUL-019): `principalId` is `witnessPrincipalId`, `credential` their PIN. | `withdrawFromDepositBox` body |
| Principal `witnessStepUp.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | The supervisor signing. Recorded against the act. | `withdrawFromDepositBox` body |
| Credential `witnessStepUp.credential` | text area | required | — | max length 512 | — | The supervisor's staff PIN, as they sign in at a till with it. A PIN, never a password (audit R123 (7)). | `withdrawFromDepositBox` body |

Errors to draw in the form: 400 Validation failed; 403 The caller lacks CASH_LIFT, or the witness's step-up is missing, failed, or is not `witnessPrincipalId` (`supervisor-step-up-refused`; CHG-RUL-019).; 409 The box is being counted or has been counted — `closing`, `closed` or `reconciled` (problem type `deposit-box-not-open`).

**Form: Record a cash lift** (modal, opened by *Record a cash lift*; *Record a cash lift* calls `createCashMovement`, *Cancel* sends nothing)

**Collects what `createCashMovement` sends before it is called.** Required: `kind`, `amount`, `recordedAt`. Optional: `denominations`, `reference`, `reason`. `id` is a client UUIDv7 generated silently, never asked. Dismissing sends nothing; the screen behind is unchanged.

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

- **Amount**: Total in the region currency (AED 2 decimals; 3 for BHD/KWD). The contract carries no denomination lines for a withdrawal, so a denomination helper may only total into the amount. *(source: contracts/spine/shift.yaml#withdrawFromDepositBox / DI-306)*
- **Reason**: Banking, Safe drop (default), Change order, Other; Other makes the note required (max 300). *(source: contracts/spine/shift.yaml#/components/schemas/WithdrawalReason / R222)*
- **Cashier (witness)**: Prefilled with the box holder; the cashier signs as witness with their PIN on the same device (step-up), and the withdrawal records them as the witness. *(source: contracts/spine/shift.yaml#withdrawFromDepositBox / decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

#### Outputs: what the screen shows and produces

**Shown**

**Deposit boxes holding cash** (data table, from `listDepositBoxes`): Sends `?openOnly=true` to `listDepositBoxes`. A box being counted (`closing`, `closed`, `reconciled`) takes nothing out and is shown without the action.

| Shows | Format | Notes |
|---|---|---|
| Cashier name | text | — |
| Workstation | the name it points at, never the id | Where it is being used now. Changes during a shift; the box does not. |
| Shift | the name it points at, never the id | The shift trading from this box. A UUIDv7, as `Shift.id` is. |
| Status | chip: Allocated, Open, Suspended, Closing, Closed, Reconciled | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Withdrawn total | AED 1,234.50 | Reduces the expected close figure. Cash skimmed for banking is not a shortfall, and a system that treats it as one makes every busy cashier … |

**Over the drawer limit** (banner, from `getVenueSettings`): **Drawer limit (decided 2 October 2026 by Chinmay, DEC-179; CHG-CSP-016):** boxes holding more than `cashDrawerLimit` (venue default, till override) are flagged here, and the till warns and offers a cash lift.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | From the path of `setVenueSettings`. |
| Calendar day start hour | 1,234 | Where the venue's calendar day starts (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar … |
| Currency code | text | `readOnly` is the freeze. `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the … |
| Currency scale | 1,234 | Scale travels with currency (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency … |
| Support hours | grouped details | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. |
| Mode | chip: Always on, Business hours, Custom, None | — |
| Timezone | text | IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract. |
| Windows | list or chips (count when long) | — |
| Day | chip: Mon, Tue, Wed, Thu, Fri, Sat… | — |
| From | text | Wall-clock time the desk opens. |
| To | text | Wall-clock time the desk closes. |
| Out of hours message | text | — |
| Quiet hours | grouped details | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. |
| From | text | Wall-clock time sending stops |
| To | text | Wall-clock time sending resumes |
| Biometrics | grouped details | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. |
| Is enabled | yes / no (icon or chip) | Off by default, and turning it on is refused without the two fields below. `setVenueSettings` answers 422 rather than accepting an enable … |
| Dpia reference | text | The venue's own reference for its Article 21 assessment. The platform does not hold the document and does not judge it; it records that one … |
| Consent notice acknowledged at | 1 Oct 2026, 14:30 | When somebody confirmed the consent forms are in place at the point of capture. A guest consenting in an app is a record; a guest … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Bank or safe-drop cash (primary button) | `withdrawFromDepositBox` POST `/deposit-boxes/{boxId}/withdraw` | inline | DepositBox | 400 Validation failed; 403 The caller lacks CASH_LIFT, or the witness's step-up is missing, failed, or is not `witnessPrincipalId` (`supervisor-step-up-refused`; CHG-RUL-019).; 409 The box is being counted or has been … | step-up: pin (The cashier the cash came from countersigns the withdrawal with their own PIN on the same device (DEC-178; CHG-CSP-015).); opens modal first |
| Record a cash lift (secondary button) | `createCashMovement` POST `/shifts/{shiftId}/cash-movements` | CreateCashMovementRequest | CashMovement | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since … | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Boxes holding cash**: Cashier, till now (changes during the shift), status (Open, On break), opening float, withdrawn so far, foreign cash held per currency where the till takes it. Boxes being counted, counted or reconciled are shown without the action. *(source: contracts/spine/shift.yaml#listDepositBoxes / DI-282)*
- **Withdrawal history per box**: Time, amount, reason, taken by, witnessed by, reference; the same rows appear in Cash Movements. *(source: contracts/spine/shift.yaml#withdrawFromDepositBox)*
- **Over the drawer limit**: A box above the venue's drawer limit (a setting to be added) is flagged; the till warns the cashier and offers a cash lift. *(source: decided 2 October 2026 by Chinmay (CHG-NOTE-004))*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Bank or safe-drop cash**: Confirm "Take AED 2,000.00 from Priya Nair's box (Till 3, Bite & Go) to the safe". Success raises withdrawn-so-far and lowers the expected close figure. 409 "This box is being counted" when it is closing, closed or reconciled. *(source: contracts/spine/shift.yaml#withdrawFromDepositBox / F32 step 4)*

**Data it reads**: `listDepositBoxes` (onLoad, Cash boxes and who holds them — the cash to move out of the …); `getVenueSettings` (onLoad, The drawer limit, to flag boxes over it (DEC-179))

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The banking safe list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the banking safe untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: nothing on this screen filters its list, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SHIFT_OPEN`, which `listDepositBoxes` requires to show this screen, and names that permission (the screen's other reads need `TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CASH_LIFT` for `withdrawFromDepositBox`, `createCashMovement`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since (`lift-exceeds-float`, audit R123 …; 409 The box is being counted or has been counted — `closing`, `closed` or `reconciled` (problem type `deposit-box-not-open`). |

#### Edge cases to draw

- **Cashier moved to another till during the shift**: The box follows the cashier; the row shows the new till. *(source: contracts/spine/shift.yaml#listDepositBoxes)*
- **Withdrawal recorded on an offline device**: Accepted later in sequence; the box total updates when it syncs. *(source: contracts/spine/shift.yaml#withdrawFromDepositBox)*
- **Box on break (suspended shift)**: Withdrawal still allowed; only closing/closed/reconciled boxes refuse. *(source: contracts/spine/shift.yaml#withdrawFromDepositBox)*

#### Consistency with other screens

- Match `POS-018`: Safe Drop & Cash Transfer at the till records the same withdrawal; same reason words.
- Match `BO-041`: Each withdrawal appears there as a lift.
- Match `BO-043`: Daily Reconciliation compares expected against deposited; banking feeds it.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
boxes:
- cashier: Priya Nair
  till: Till 3 — Bite & Go
  status: Open
  float: AED 500.00
  withdrawn: AED 2,000.00
- cashier: Khalid Al Mansoori
  till: Till 1 — Main Gate ticket office
  status: Open
  float: AED 1,000.00
  withdrawn: AED 0.00
  foreign: USD 120.00
withdrawal:
  amount: AED 3,000.00
  reason: Banking
  reference: BAG-2026-1014-07
  taken_by: Omar Ziad
  witness: Khalid Al Mansoori
```

#### Permissions

- `listDepositBoxes` → `SHIFT_OPEN` (operate) · staff
- `withdrawFromDepositBox` → `CASH_LIFT` (operate) · staff · step-up pin
- `getVenueSettings` → `TENANT_VIEW` (read) · staff
- `createCashMovement` → `CASH_LIFT` (operate) · staff

**A refused user sees:** Shown when the caller lacks `SHIFT_OPEN`, which `listDepositBoxes` requires to show this screen, and names that permission (the screen's other reads need `TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `CASH_LIFT` for `withdrawFromDepositBox`, `createCashMovement`.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.8.8 | The system should allow the supervisor to withdraw some cash during the day from an cashier’s cash float and trace it in the system. | F&B & Guest Management | CONTRACTED | `withdrawFromDepositBox` |
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

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-042` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (27), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-042?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Bank or safe-drop cash, Record a cash lift.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `CASH_LIFT`, `SHIFT_OPEN`, `TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-043` Daily Reconciliation

**Prove the day balances before anyone goes home.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `LEDGER_VIEW`, `OVERSHORT_ACCEPT`, `REPORT_VIEW_WORKSTATION`, `SETTLEMENT_RECONCILE`, `SETTLEMENT_VIEW`, `SHIFT_CLOSE` (2 read, 4 operate); in the flows as finance controller, venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listSettlements` reads the population and `getTrialBalance` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `settlementId` (deepLink), `shiftId` (session) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/daily-reconciliation` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Reconciliation is daily, per venue** (decided 2 October 2026, Chinmay; CHG-FIN-009; audit R110 (b)). The unit of work and of sign-off is one venue-day: POS cash, gateway settlements, bank and wallet against the ledger for that day. A longer range reviews days already reconciled; a provider's monthly file (DI-268) is matched day by day.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Finance proves each venue's day balances: every money source (till cash, card gateway settlements, bank, wallet) set against the ledger, with the differences named and the unmatched settlement lines to resolve. Reconciliation is daily per venue. Provider files are matched automatically (ingest, parse, match, classify, auto-resolve) so a person only sees genuine mismatches. The one thing to get right: a variance always says between which two sources it sits ("gateway against ledger: AED 500.00 short"), because "out by 500" is not actionable.

**Known correction pending (do not draw the wrong version)**

- **The read that sets POS cash, gateway, bank, wallet and ledger side by side is not declared on this screen.** Why: It exists for exactly this purpose ("a venue closing a day needs them side by side") but only the finance dashboard and audit screens declare it. *(source: contracts/spine/finance.yaml#getUnifiedReconciliation / screens/P08-venue-back-office.yaml#BO-043; Finance, Ledger & Tax · Reporting & Analytics)*
- **The trial balance is shown on a daily screen.** Why: A trial balance is per fiscal period and belongs to the period close; for a day it says nothing. *(source: contracts/spine/finance.yaml#/components/schemas/TrialBalance / F13 step 5; Finance, Ledger & Tax · Reporting & Analytics)*
- **Provider and status filters are free text.** Why: Pick lists of the providers the venue uses and the settlement statuses. *(source: screens/P08-venue-back-office.yaml#BO-043; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Daily per venue (R110) against the weekly or monthly runs in the 12 August minutes. Is a monthly roll-up also needed?** → Daily per venue (applied by CHG-FIN-009), plus a month view listing the days. *(decided by Chinmay, 2026-10-02; DEC-215 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Provider name | text field | optional | — | — | — | Sends `?providerName=` to `listSettlements`. | `listSettlements` ?providerName |
| Status | select | optional | — | Ingesting · Parsing · Matching · Matched · Has exceptions · Resolved · Failed | — | Sends `?status=` to `listSettlements`. | `listSettlements` ?status |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Fiscal period | picker: choose a fiscal period | — | — | `getTrialBalance` ?fiscalPeriodId |
| Legal entity | picker: choose a legal entity | — | — | `getTrialBalance` ?legalEntityId |
| Account | picker: choose an account | — | — | `listLedgerEntries` ?accountId |
| Cost center | picker: choose a cost center | — | — | `listLedgerEntries` ?costCenterId |
| Source type | select | — | Manual · Order · Refund · Void · Shift · Recognition · Settlement · Variance · Reversal · Write off · Chargeback | `listLedgerEntries` ?sourceType |
| Source | text field | — | — | `listLedgerEntries` ?sourceId |
| Posted from | date picker | — | — | `listLedgerEntries` ?postedFrom |
| Posted to | date picker | — | — | `listLedgerEntries` ?postedTo |
| Workstation | picker: choose a workstation | — | — | `listShifts` ?workstationId |
| Status | select | — | Pending approval · Open · Suspended · Pending variance · Pending closure · Closed · Auto closed | `listShifts` ?status |
| Opened from | date and time picker | — | — | `listShifts` ?openedFrom |
| Opened to | date and time picker | — | — | `listShifts` ?openedTo |
| Count kind | segmented control | — | Opening float · Close · Movement | `getShiftCountLines` ?countKind |

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

**Form: Resolve settlement exception** (modal, opened by *Resolve settlement exception*; *Resolve settlement exception* calls `resolveSettlementException`, *Cancel* sends nothing)

**Collects what `resolveSettlementException` sends before it is called.** Required: `exceptionId`, `resolution`, `note`. Optional: `matchedPaymentId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Exception `exceptionId` | picker: choose an exception | required | — | — | shows names, sends the id | — | `resolveSettlementException` body |
| Resolution `resolution` | radio group | required | — | Matched manually · Write off · Dispute raised · Provider error · Timing difference | — | How a settlement exception was explained. One vocabulary for the request and the stored exception. | `resolveSettlementException` body |
| Matched payment `matchedPaymentId` | picker: choose a matched payment | optional | — | — | shows names, sends the id | — | `resolveSettlementException` body |
| Note `note` | text area | required | — | min length 3; max length 1000 | — | — | `resolveSettlementException` body |

Errors to draw in the form: 400 `matchedManually` without a `matchedPaymentId`, or one that names no payment. `errors[]` names the field.; 404 The settlement, or an exception with this `exceptionId` under it, does not exist or is outside the caller's scope.; 409 The exception is already resolved.

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
| Supervisor step up `supervisorStepUp` | group | optional | — | — | — | The supervisor closing the shift, signing on this device (CHG-RUL-019). Refused without it (`403 supervisor-step-up-refused`). | `closeShift` body |
| Principal `supervisorStepUp.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | The supervisor signing. Recorded against the act. | `closeShift` body |
| Credential `supervisorStepUp.credential` | text area | required | — | max length 512 | — | The supervisor's staff PIN, as they sign in at a till with it. A PIN, never a password (audit R123 (7)). | `closeShift` body |

Errors to draw in the form: 400 Validation failed; 403 The caller is the cashier whose shift it is and does not hold OVERSHORT_ACCEPT (problem type `blind-count-required`): their count goes through …; 409 Shift is not `open` or `suspended` — already closing or closed (problem type `shift-not-open`) — or open orders remain (`open-orders-remain`); 422 A counted line names an unknown or inactive denomination (`unknown-denomination`), repeats one (`duplicate-denomination`), or sends a `total` that disagrees …

**Form: Accept variance** (modal, opened by *Accept variance*; *Accept variance* calls `acceptShiftVariance`, *Cancel* sends nothing)

**Collects what `acceptShiftVariance` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | Retained for audit. The accepting principal is recorded. | `acceptShiftVariance` body |
| Supervisor step up `supervisorStepUp` | group | optional | — | — | — | The supervisor accepting, signing on this device (CHG-RUL-019). Refused without it (`403 supervisor-step-up-refused`). | `acceptShiftVariance` body |
| Principal `supervisorStepUp.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | The supervisor signing. Recorded against the act. | `acceptShiftVariance` body |
| Credential `supervisorStepUp.credential` | text area | required | — | max length 512 | — | The supervisor's staff PIN, as they sign in at a till with it. A PIN, never a password (audit R123 (7)). | `acceptShiftVariance` body |

Errors to draw in the form: 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (problem type `approver-is-cashier`) — a cashier signing off their own …; 409 Shift is not `pendingVariance` (problem type `shift-not-pending-variance`) — within tolerance, still open, or already accepted.

**Form: Reject and recount** (modal, opened by *Reject and recount*; *Reject and recount* calls `rejectShiftVariance`, *Cancel* sends nothing)

**Collects what `rejectShiftVariance` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | Why a recount is needed, shown to the cashier. Never the amount: "Count the AED 100 notes again", not "you are AED 100 short". | `rejectShiftVariance` body |
| Supervisor step up `supervisorStepUp` | group | optional | — | — | — | The supervisor sending the shift back, signing on this device (CHG-RUL-014, as `reopenShift`). | `rejectShiftVariance` body |
| Principal `supervisorStepUp.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | The supervisor signing. Recorded against the act. | `rejectShiftVariance` body |
| Credential `supervisorStepUp.credential` | text area | required | — | max length 512 | — | The supervisor's staff PIN, as they sign in at a till with it. A PIN, never a password (audit R123 (7)). | `rejectShiftVariance` body |

Errors to draw in the form: 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (`approver-is-cashier`); or the supervisor step-up is missing or failed …; 409 Shift is not `pendingVariance` (`shift-not-pending-variance`), or a recount is already requested and not yet submitted (`recount-already-requested`).

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Day and venue**: One day (yesterday by default) and one venue; the day runs midnight to midnight in the region's time zone. *(source: R110 / contracts/spine/finance.yaml#/components/schemas/Settlement)*
- **Upload settlement file**: Provider (Stripe, Network International…), the day it covers, the file, and its format (CSV, fixed width, XML, JSON) if not detected. Parsing runs in the background; the row shows Ingesting, Parsing, Matching, then Matched or Has exceptions. *(source: contracts/spine/finance.yaml#ingestSettlementFile / contracts/spine/finance.yaml#/components/schemas/SettlementStatus)*
- **Resolve an exception**: Outcome (Matched by hand, Write off, Dispute raised, Provider error, Timing difference), a required note, and the matching payment when matching by hand. *(source: contracts/spine/finance.yaml#/components/schemas/SettlementResolution / contracts/spine/finance.yaml#resolveSettlementException)*

#### Outputs: what the screen shows and produces

**Shown**

**Shifts of the day** (data table, from `listShifts`): **The daily cash reconciliation lists every shift and resolves them one by one (decided 2 October 2026 by Chinmay, DEC-059).**

| Shows | Format | Notes |
|---|---|---|
| Principal display name | text | — |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Closed at | 1 Oct 2026, 14:30 | — |

**Every settlement** (data table, from `listSettlements`)

| Shows | Format | Notes |
|---|---|---|
| Provider name | text | — |
| Status | chip: Ingesting, Parsing, Matching, Matched, Has exceptions, Resolved… | — |
| Line count | 1,234 | — |
| Matched count | 1,234 | — |
| Exception count | 1,234 | — |
| Provider fees | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Every posting** (data table, from `listLedgerEntries`)

| Shows | Format | Notes |
|---|---|---|
| Account code | text | — |
| Description | text | — |
| Posted at | 1 Oct 2026, 14:30 | — |

**Every settlement exception** (data table, from `listSettlementExceptions`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Unmatched in provider, Unmatched in ledger, Amount mismatch, Duplicate in provider … | — |
| Provider reference | text | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Expected amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Resolution | chip: Matched manually, Write off, Dispute raised, Provider error, Timing difference | Null while the exception is open. |
| Resolved at | 1 Oct 2026, 14:30 | — |

**Month view** (calendar view, from `listSettlements`): **Daily per venue (CHG-FIN-009), plus a month view listing the days (decided 2 October 2026 by Chinmay, DEC-215).**

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Currency code | text | A settlement has no account, so nothing else denominates it. A posting takes its currency from `ledger.account.currency` and a payment from … |
| Provider name | text | — |
| Venue | the name it points at, never the id | The venue this settlement is for. Reconciled daily per venue (decided 28 September, audit R110 (b)), so `periodStart` and `periodEnd` are … |
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
| Ingested at | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |

**The selected settlement** (detail panel, from `getSettlement`)

| Shows | Format | Notes |
|---|---|---|
| Currency code | text | A settlement has no account, so nothing else denominates it. A posting takes its currency from `ledger.account.currency` and a payment from … |
| Provider name | text | — |
| File reference | the name it points at, never the id | The `MediaAsset` holding the provider file, as given to `ingestSettlementFile`. Kept on the row because parsing is asynchronous: the job … |
| Status | chip: Ingesting, Parsing, Matching, Matched, Has exceptions, Resolved… | — |
| Line count | 1,234 | — |
| Matched count | 1,234 | — |
| Exception count | 1,234 | — |
| Provider fees | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**The trial balance** (detail panel, from `getTrialBalance`)

| Shows | Format | Notes |
|---|---|---|
| Fiscal period | the name it points at, never the id | — |
| Is balanced | yes / no (icon or chip) | False indicates a defect, not a business condition. Double-entry cannot be unbalanced by legitimate activity. |
| Total debit | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total credit | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Accounts | list or chips (count when long) | — |

**Count by denomination** (data table, from `getShiftCountLines`)

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
| Ingest settlement file (primary button) | `ingestSettlementFile` POST `/settlements` | inline | Settlement | 400 `fileReference` names no completed upload in the caller's scope, or the period is not a single day (`settlement-period-not-a-day`, audit R110 (b)). | opens modal first |
| Resolve settlement exception (secondary button) | `resolveSettlementException` POST `/settlements/{settlementId}/exceptions` | inline | SettlementException | 400 `matchedManually` without a `matchedPaymentId`, or one that names no payment. `errors[]` names the field.; 404 The settlement, or an exception with this `exceptionId` under it, does not exist or is outside the … | opens modal first |
| Close shift (secondary button) | `closeShift` POST `/shifts/{shiftId}/close` | CloseShiftRequest | ShiftCloseResult | 400 Validation failed; 403 The caller is the cashier whose shift it is and does not hold OVERSHORT_ACCEPT (problem type `blind-count-required`): their count goes through …; 409 Shift is not `open` or `suspended` — … | step-up: pin (A supervisor closes a cashier's shift and sees the expected cash and the variance (CHG-FIN-003); their own PIN on the …); opens modal first |
| Accept variance (secondary button) | `acceptShiftVariance` POST `/shifts/{shiftId}/accept-variance` | inline | Shift | 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (problem type `approver-is-cashier`) — a cashier signing off their own …; 409 Shift is not `pendingVariance` (problem type … | step-up: pin (A supervisor signs off a cashier's over/short in person, with their own PIN on the device they use (audit R080 (e); any …); opens modal first |
| Reject and recount (secondary button) | `rejectShiftVariance` POST `/shifts/{shiftId}/reject-variance` | inline | Shift | 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (`approver-is-cashier`); or the supervisor step-up is missing or failed …; 409 Shift is not `pendingVariance` … | step-up: pin (The same supervisor act as accepting a variance, in person with their own PIN (audit R080 (e); DEC-175).); opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Sources against the ledger**: One row per source (POS cash, each gateway, bank, wallet, ledger) with its total and count, and below them each variance with the two sources it lies between, the amount and the likely cause. A day with no variance says "Balanced" in words. *(source: contracts/spine/finance.yaml#getUnifiedReconciliation / contracts/spine/finance.yaml#/components/schemas/UnifiedReconciliation)*
- **Settlement batches**: Provider, day, status, lines, matched, exceptions, provider gross, fees, net, ledger gross, difference. Differences in red with sign; fees shown separately so fees are never mistaken for a shortfall. *(source: contracts/spine/finance.yaml#/components/schemas/Settlement / DI-268)*
- **Exceptions**: Kind in words (In provider file but not in our records; In our records but not in the file; Amount differs; Duplicate in file; Fee not explained), provider reference, amount against expected. Open first. *(source: contracts/spine/finance.yaml#/components/schemas/SettlementException)*
- **Cash**: Expected against deposited per till and the over/short, which posts to the over/short account visible at month end. *(source: DI-275)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Upload file**: The batch appears with its progress; the page updates when matching finishes. *(source: contracts/spine/finance.yaml#ingestSettlementFile)*
- **Resolve**: The exception closes with who and why; the batch becomes Resolved when none are open. *(source: contracts/spine/finance.yaml#resolveSettlementException)*
- **Open ledger entries**: Shows the postings behind a figure for that day, read-only. *(source: contracts/spine/finance.yaml#listLedgerEntries)*

**Data it reads**: `getTrialBalance` (onLoad, Trial balance for a period); `listSettlements` (onLoad, List settlement batches); `listLedgerEntries` (onLoad, Query the ledger); `listShifts` (onLoad, Every shift of the venue day, to resolve one by one …); `getShiftCountLines` (onLoad, The count lines of the shift being resolved)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*
- → `BO-074` Chart of Accounts: *Chart of Accounts*; carries `accountId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The daily reconciliation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the daily reconciliation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No daily reconciliation yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on providerName, status and the daily reconciliation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `LEDGER_VIEW`, which `getTrialBalance` requires to show this screen, and names that permission (the screen's other reads need `REPORT_VIEW_WORKSTATION`, `SETTLEMENT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `OVERSHORT_ACCEPT` for … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 400 `fileReference` names no completed upload in the caller's scope, or the period is not a single day (`settlement-period-not-a-day`, audit R110 (b)).; 400 `matchedManually` without a `matchedPaymentId`, or one that names no payment. `errors[]` names the field.; 409 Shift is not `open` or `suspended` — already closing or closed (problem type `shift-not-open`) — or open … |

#### Edge cases to draw

- **The file is for a different currency than the venue trades in**: Show both currencies and refuse to compute a difference that means nothing. *(source: contracts/spine/finance.yaml#/components/schemas/Settlement)*
- **A file arrives for a day already reconciled**: A new batch; never overwrites the earlier one. *(source: contracts/spine/finance.yaml#ingestSettlementFile)*
- **Parsing fails**: Status Failed with the reason and an "Upload again" action. *(source: contracts/spine/finance.yaml#/components/schemas/SettlementStatus)*
- **Exceptions still open at month end**: They block the period close; the close screen links back here. *(source: F13 step 1)*

#### Consistency with other screens

- Match `BO-090`: "Settlements reconciled" is one of the close checks; same counts.
- Match `BO-025`: A chargeback found in a settlement file is defended there.
- Match `BO-1081`: The finance dashboard shows the same variance figures.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
day: Tue 29 Sep 2026 · Aquaventure Waterpark
sources:
- POS cash AED 8,460.00 deposited (expected AED 8,480.00) · short AED 20.00
- 'Network International AED 9,500.00 · ledger AED 10,000.00 · gateway against ledger AED 500.00 short · likely
  cause: 3 refunds settled next day'
- Stripe AED 41,322.50 · matched
exception: Amount differs · ref NI-88231907 · AED 449.00 against AED 499.00
```

#### Permissions

- `getTrialBalance` → `LEDGER_VIEW` (read) · staff
- `listSettlements` → `SETTLEMENT_VIEW` (read) · staff, partner
- `getSettlement` → `SETTLEMENT_VIEW` (read) · staff, partner
- `ingestSettlementFile` → `SETTLEMENT_RECONCILE` (operate) · staff, partner
- `listLedgerEntries` → `LEDGER_VIEW` (read) · staff
- `listSettlementExceptions` → `SETTLEMENT_VIEW` (read) · staff, partner
- `resolveSettlementException` → `SETTLEMENT_RECONCILE` (operate) · staff, partner
- `listShifts` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `getShiftCountLines` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `closeShift` → `SHIFT_CLOSE` (operate) · staff · step-up pin
- `acceptShiftVariance` → `OVERSHORT_ACCEPT` (operate) · staff · step-up pin
- `rejectShiftVariance` → `OVERSHORT_ACCEPT` (operate) · staff · step-up pin

**A refused user sees:** Shown when the caller lacks `LEDGER_VIEW`, which `getTrialBalance` requires to show this screen, and names that permission (the screen's other reads need `REPORT_VIEW_WORKSTATION`, `SETTLEMENT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `OVERSHORT_ACCEPT` for …

#### Requirements it meets

24 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.7.63 | Revenue recognition audit reporting. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 5.7.64 | Revenue recognition reconciliation reports. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 5.7.71 | General Ledger reporting. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 5.7.72 | Trial Balance reporting. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 5.7.75 | Revenue reporting by account. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 5.7.76 | Revenue reporting by site. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 5.7.77 | Deferred revenue reporting. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 5.7.78 | Account activity reporting. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 5.7.79 | Account balance reporting. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 4.2.25 | The system shall maintain a complete audit log of all payment activities including authorizations, captures, settlements, refunds, voids, gateway responses, and user actions. | Bundles and Promotions | CONTRACTED | `listLedgerEntries` |
| 4.3.35 | Maintain audit trail for wallet transactions. | Bundles and Promotions | CONTRACTED | `listLedgerEntries` |
| 5.7.10 | The system should create standard debit and credit journal entries when an admission item is paid for (e.g., debit cash, credit unearned revenue), and additional journal entries when a ticket is … | F&B & Guest Management | CONTRACTED | `listLedgerEntries` |
| … 12 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- End-of-day reports: cashier shift, till, sales by location, payment type summary, cash management, variance, refund, and consolidated end-of-day (e.g. expected 8,480 AED vs deposited 8,460 AED = 20 AED shortage, posted to an overage/shortage account visible at month-end). *(agreed · MoM 12 Aug 2026, 20. End-of-Day Reports and Overage/Shortage Handling · DI-275)*
- Payments screen consolidates gateway (Stripe, NI) and on-site (cash, card) payments and flags variances from a monthly reconciliation file (e.g. gateway 10,000 AED vs 9,500 AED recorded). *(agreed · MoM 12 Aug 2026, 17. Payments Reconciliation · DI-268)*
- Weekly/monthly reconciliation runs ingest → parse → match → classify → auto-resolve, so only genuinely mismatched amounts are shown for human review. *(agreed · MoM 12 Aug 2026, 11. Settlement and Reconciliation Process · DI-258)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-043` · status **notStarted** · provenance generated
- Flow F74 *A shift closes and the day is reported*, step 4: The daily cash reconciliation lists every shift of the day and resolves the ones still under review, one by one. → **Daily per venue, shift by shift** (decided 2 October 2026, Chinmay, batch 3 #1 and batch 6 #215; DEC-059, CHG-CSP-012). Each pending shift is accepted, sent back for a recount or closed by a …
- Flow F98 *A day is reconciled from takings to the ledger*, step 1: Daily Reconciliation. → 6 operations, 6 of them previously unwalked.
- Flow F74 branch at step 4 (requiresStaff): when The supervisor does not accept the count., **Sent back for a recount, not reopened for trading** (decided 2 October 2026, batch 6 #175, BO-040: "Add Reject + recount (DI-804)"; CHG-CSP-013). The shift stays `pendingVariance` and the cashier …
- Flow F74 branch at step 4 (recoverable): when A shift is still under review when the day is reported., **The day report names it as under review rather than leaving it out.** Its counted figure is in the day; its variance is pending until the reconciliation resolves it.
- Flow F98 branch at step 1 (medium): when The acting principal lacks the permission at this scope., **Refused at the first step, not the last.** ADR-0002 makes authorisation user-driven — a person who gets three steps in and then cannot finish has been told the wrong thing.

#### Acceptance for the design

- [ ] Every input above is drawn (34), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (66 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-043?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Ingest settlement file, Resolve settlement exception, Close shift, Accept variance, Reject and recount.
- [ ] Every transition is wired: `BO-008`, `BO-074`.
- [ ] Every gated control is gated: `LEDGER_VIEW`, `OVERSHORT_ACCEPT`, `REPORT_VIEW_WORKSTATION`, `SETTLEMENT_RECONCILE`, `SETTLEMENT_VIEW`, `SHIFT_CLOSE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-047` Order Corrections & Exceptions

**Fix an order that has gone wrong.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 2 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_REFUND`, `ORDER_REPRINT`… (8 operate, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listOrders` reads the population and `getOrder` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `orderId` (deepLink) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/venue-operations/f-b-order-management` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Fix an order that went wrong: wrong product, wrong date, duplicate, price error, using modify, exchange, reschedule, void or refund with a reason, never by editing history.

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
| FX rate | text | The rate on the original payment, not today's (BL-087, CF-118). `Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the … |
| Settle to | chip: Original tender, Advance balance, Wire transfer, Store credit | BL-086. A refund could only go back the way it came. |
| FX variance | AED 1,234.50 | Where the sale rate and the current rate differ, the difference is booked as an FX variance rather than hidden in the refund. |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Applied percentage | 1,234.5 | From the venue's time bands, or an approver override. |
| Status | chip: Pending approval, Pending gateway, Completed, Declined, Failed | — |

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
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for … |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total price variance | AED 1,234.50 | Sum across lines. Zero on a normal order. |

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

- **correction choice**: The screen asks what went wrong first and proposes the right act (void if same shift and unsettled, otherwise refund or exchange). *(source: contracts/spine/orders.yaml#voidOrder / contracts/spine/orders.yaml#modifyOrder)*

**Data it reads**: `listOrders` (onLoad, List orders)

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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_CREATE` for `createOrder`; `ORDER_DISCOUNT` for `applyManualDiscount`; `ORDER_EXCHANGE` for `exchangeOrderLines`; `ORDER_MODIFY` for `holdOrder` … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A lease covering a line has expired (`leaseExpired`), capacity is exhausted (`capacityExhausted`), or the catalogue bundle the client priced from is beyond its … (OrderRefusedProblem); 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem); 409 Held order expired … |

#### Consistency with other screens

- Match `BO-023`: Same dialogs.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
correction:
  order: DP-2026-105010
  issue: Sold Adult instead of Child
  act: exchange, difference AED 50.00 refunded
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
- `reprintOrder` → `ORDER_REPRINT` (operate) · staff, guest, partner, device
- `rescheduleOrder` → `ORDER_RESCHEDULE` (operate) · staff, partner
- `resumeOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `voidOrder` → `ORDER_VOID` (operate) · staff, partner

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listOrders` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ORDER_CREATE` for `createOrder`; `ORDER_DISCOUNT` for `applyManualDiscount`; `ORDER_EXCHANGE` for `exchangeOrderLines`; `ORDER_MODIFY` for `holdOrder` …

#### Requirements it meets

70 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 58 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-047` · status **notStarted** · provenance generated
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (127), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (39 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-047?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create order, Apply manual discount, Create refund, Exchange order lines, Hold order, Modify order, Reprint order, Reschedule order, Resume order, Void order.
- [ ] Every transition is wired: `BO-008`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_DISCOUNT`, `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_REFUND`, `ORDER_REPRINT`, `ORDER_RESCHEDULE`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-048` Retail Products

**Manage what the shop sells.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `retail` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW` (1 configure, 2 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listMerchandise` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `merchandiseId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/venue-operations/retail-products` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Cross-platform navigation removed 24 August**: GST-026. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): On a back-office product list search covers lookup and the primary act is adding an item; the price check (lookupMerchandise) belongs to the till and the …

**From the Food, Beverage & Retail process.** Retail Products is where a venue manager sets up what each shop sells. A merchandise item links a catalogue variant (which carries the price and VAT) to an outlet and to the inventory item that a sale depletes. The one thing to get right is that link. An item with no stock link sells but never runs out, and the venue's stock figures become fiction.

**Fixed on main** (the package already carries these; draw what it says): The filters are text fields "Outlet id" and "Category id". The table is "Every merchandise" with id, variantId, inventoryItemId and … (CHG-SBO-008); The primary button is "Lookup merchandise" (the shop-floor price check). (CHG-WIR-008); A barcode exists in three places: the catalogue variant (updateProductVariant), the merchandise item and the inventory item. (CHG-WIR-008); The flow transition to GST-026 ("Guest tracks it in the app") and the F17 shop-and-drop steps are attached to this configuration screen. (CHG-CLN-005).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should a merchandise item require a stock link? Sales are gated on system stock per venue, and an unlinked item cannot be gated.** → Drawn default stands (answer: "Default / recommended accepted"): Draw the stock item as required, with an explicit "Not stock-tracked" escape and a warning. *(decided by Chinmay, 2026-10-02; DEC-037 / CHG-NOTE-004)*
- **The client asked for a product command centre (products per store, top sellers, by category). Which reads feed it?** → Drawn default stands (answer: "Default / recommended accepted"): No KPI tiles on this screen until a summary read exists. *(decided by Chinmay, 2026-10-02; DEC-038 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Shop | picker: choose an id | optional | — | — | shows names, sends the id | A pick list in words, never a typed id (design-note correction, 2 October 2026). | `Outlet.id` |
| Category | picker: choose a category | optional | — | — | shows names, sends the id | A pick list of the shop's categories by name. | `MerchandiseItem.categoryId` |
| In stock only | toggle | optional | off | — | — | Sends `?inStockOnly=` to `listMerchandise`. | `listMerchandise` ?inStockOnly |
| Search | text field | optional | — | min length 1; max length 100 | — | Sends `?search=` to `listMerchandise`. | `listMerchandise` ?search |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Outlet | picker: choose an outlet | — | — | `listMerchandise` ?outletId |
| Category | picker: choose a category | — | — | `listMerchandise` ?categoryId |
| Kind | select | — | Shop · Restaurant · Bar · Cafe · Kiosk · Game floor · Ticket office · Mobile | `listOutlets` ?kind |

**Form: Create merchandise** (modal, opened by *Create merchandise*; *Create merchandise* calls `createMerchandise`, *Cancel* sends nothing)

**Collects what `createMerchandise` sends before it is called.** Required: `sku`, `name`, `outletId`, `variantId`. Optional: `barcode`, `description`, `categoryId`, `inventoryItemId`, `isReturnable`, `returnWindowDays`, `requiresSerialNumber`, `imageAssetRef`. `outletId`, `variantId`, `categoryId` and `inventoryItemId` are pickers (the shop, the catalogue variant by product name, the category, the stock item by name), never typed ids. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| SKU `sku` | text field | required | — | max length 64 | — | — | `createMerchandise` body |
| Barcode `barcode` | text field | optional | — | max length 128 | — | — | `createMerchandise` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createMerchandise` body |
| Description `description` | text area | optional | — | — | — | What the item is, in the guest's words. Indexed for guest-app search. | `createMerchandise` body |
| Outlet `outletId` | picker: choose an outlet | required | — | — | shows names, sends the id | — | `createMerchandise` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `createMerchandise` body |
| Variant `variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `createMerchandise` body |
| Inventory item `inventoryItemId` | picker: choose an inventory item | optional | — | — | shows names, sends the id | — | `createMerchandise` body |
| Is returnable `isReturnable` | toggle | optional | on | — | — | — | `createMerchandise` body |
| Return window days `returnWindowDays` | number field (days) | optional | — | — | — | — | `createMerchandise` body |
| Requires serial number `requiresSerialNumber` | toggle | optional | off | — | — | — | `createMerchandise` body |
| Image `imageAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `createMerchandise` body |

Errors to draw in the form: 400 Validation failed; 409 Barcode already in use in this venue. `refusedReason` is `barcodeInUse`. (MerchandiseConflictProblem)

**Form: Save merchandise** (modal, opened by *Save merchandise*; *Save merchandise* calls `updateMerchandise`, *Cancel* sends nothing)

**Collects what `updateMerchandise` sends before it is called.** Nothing in the body is required. Optional: `name`, `description`, `barcode`, `categoryId`, `inventoryItemId`, `imageAssetRef`, `isReturnable`, `returnWindowDays`, `requiresSerialNumber`, `isActive`. `categoryId` and `inventoryItemId` are pickers by name. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateMerchandise` body |
| Description `description` | text area | optional | — | — | — | What the item is, in the guest's words. Null clears it. | `updateMerchandise` body |
| Barcode `barcode` | text field | optional | — | max length 128 | — | Must stay unique in the venue. Null clears it. | `updateMerchandise` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateMerchandise` body |
| Inventory item `inventoryItemId` | picker: choose an inventory item | optional | — | — | shows names, sends the id | Re-points the stock item a sale depletes. Sales already made keep the movements they wrote. | `updateMerchandise` body |
| Image `imageAssetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `updateMerchandise` body |
| Is returnable `isReturnable` | toggle | optional | — | — | — | — | `updateMerchandise` body |
| Return window days `returnWindowDays` | number field (days) | optional | — | min 0 | — | — | `updateMerchandise` body |
| Requires serial number `requiresSerialNumber` | toggle | optional | — | — | — | — | `updateMerchandise` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateMerchandise` body |

Errors to draw in the form: 409 The new barcode is already in use in this venue. `refusedReason` is `barcodeInUse`. (MerchandiseConflictProblem)

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Outlet**: Picker of the venue's retail outlets (Marina Bay Store, Beach Hut, Main Gate Kiosk). Merchandise rows are per outlet (outlet-level configuration), so the same T-shirt sold in two shops is two rows. Never a text field for an id. *(source: DI-330 / DI-350 / contracts/satellite/retail.yaml#/components/schemas/MerchandiseItem)*
- **Product and variant**: Chosen as product, then its size/colour combination (for example "Aqua Park logo T-shirt" → Green / M), from the catalogue. Price and VAT come from the variant and are shown read-only, with a link to edit pricing in the catalogue. The form never asks for a variant id. *(source: DI-354 / contracts/satellite/retail.yaml#createMerchandise)*
- **Stock item**: Picker of inventory items (name, SKU, base unit). It looks mandatory. Leaving it empty needs an explicit choice, "Not stock-tracked (sells without running out)", and shows a warning. *(source: contracts/satellite/retail.yaml#/components/schemas/MerchandiseItem / DI-294)*
- **SKU / Barcode**: SKU up to 64 characters, e.g. TSH-AQP-GRN-M. Barcode up to 128 characters, unique in the venue. On a duplicate the save fails inline with "This barcode is already used by another item in this venue". SKU and outlet cannot change after creation; show them read-only on edit. *(source: contracts/satellite/retail.yaml#createMerchandise / contracts/satellite/retail.yaml#updateMerchandise)*
- **Returns**: "Returnable" on by default. When on, "Return window (days)" shows. When empty, the window is the outlet's return policy default, and that default is shown as the placeholder. *(source: contracts/satellite/retail.yaml#/components/schemas/ReturnPolicy / R215)*
- **Requires serial number**: Off by default. On, the till asks for the serial at sale, and the item appears in serialised stock (BO-114 / EMP-069). *(source: DI-406 / contracts/satellite/retail.yaml#createMerchandise)*
- **Guest description and image**: The description is the guest's words and is indexed for guest-app search. Show a character count and a guest-card preview. *(source: contracts/satellite/retail.yaml#/components/schemas/MerchandiseItem)*

#### Outputs: what the screen shows and produces

**Shown**

**Products** (data table, from `listMerchandise`)

| Shows | Format | Notes |
|---|---|---|
| SKU | text | — |
| Barcode | text | — |
| Name | text | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| On hand | 1,234.5 | — |
| Is returnable | yes / no (icon or chip) | — |
| Return window days | 1,234 | — |

**The selected merchandise** (detail panel, from `listMerchandise`)

| Shows | Format | Notes |
|---|---|---|
| SKU | text | — |
| Barcode | text | — |
| Name | text | — |
| Outlet | the name it points at, never the id | — |
| Category | the name it points at, never the id | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| On hand | 1,234.5 | — |
| Is returnable | yes / no (icon or chip) | — |
| Return window days | 1,234 | — |
| Requires serial number | yes / no (icon or chip) | — |
| Image | the image or video | — |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create merchandise (secondary button) | `createMerchandise` POST `/merchandise` | CreateMerchandiseRequest | MerchandiseItem | 400 Validation failed; 409 Barcode already in use in this venue. `refusedReason` is `barcodeInUse`. (MerchandiseConflictProblem) | opens modal first |
| Save merchandise (secondary button) | `updateMerchandise` PATCH `/merchandise/{merchandiseId}` | inline | MerchandiseItem | 409 The new barcode is already in use in this venue. `refusedReason` is `barcodeInUse`. (MerchandiseConflictProblem) | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Product list**: Grouped by product, with outlet rows beneath: image thumbnail, name, variant (size/colour), SKU, barcode, outlet, price (AED, 2 decimals, VAT-inclusive as the shop shows it), on hand, status (Active / Inactive). Badges for "Not stock-tracked" and "Serialised". Filters: outlet, category, "In stock only", search. *(source: contracts/satellite/retail.yaml#listMerchandise / DI-353)*
- **Inactive items**: Shown in the list greyed with "Inactive". Explain that an inactive item scans as "not found" at the till. *(source: R215 / contracts/satellite/retail.yaml#lookupMerchandise)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Add merchandise item**: Primary action. Saves and the row appears under its product. If the barcode is in use, nothing is saved and the field shows the error. *(source: contracts/satellite/retail.yaml#createMerchandise)*
- **Save changes**: Edits name, description, barcode, category, stock item, image, returns and serial flag, or deactivates the item. Re-pointing the stock item asks for confirmation: "Sales from now on will deplete <new item>. Past sales keep their movements." *(source: contracts/satellite/retail.yaml#updateMerchandise)*

**Data it reads**: `listMerchandise` (onLoad, List merchandise); `listOutlets` (onLoad, List outlets (the pick list))

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The retail products list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the retail products untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No retail products yet. Offers Create merchandise (`createMerchandise`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on outletId, categoryId, inStockOnly, search and the retail products are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PRODUCT_VIEW`, which `listMerchandise` requires to show this screen, and names that permission (the screen's other reads need `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `createMerchandise`, `updateMerchandise`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Barcode already in use in this venue. `refusedReason` is `barcodeInUse`. (MerchandiseConflictProblem); 409 The new barcode is already in use in this venue. `refusedReason` is `barcodeInUse`. (MerchandiseConflictProblem) |

#### Edge cases to draw

- **Item has no stock link**: Row badge "Not stock-tracked". Detail panel warning: "This item will sell without reducing stock." Offer "Link a stock item". *(source: contracts/satellite/retail.yaml#/components/schemas/MerchandiseItem)*
- **Search returned nothing vs nothing set up**: Two different empty states. A search that matches nothing names the search and offers to clear it. *(source: screens/P08-venue-back-office.yaml#BO-048)*

#### Consistency with other screens

- Match `BO-008`: Variants (size/colour), price and the variant's barcode are set in Product Detail & Variants. This screen picks them and shows them read-only.
- Match `POS-023`: The barcode entered here is the one the till scans to price-check and sell.
- Match `BO-142`: The return window default comes from the outlet's return policy, the same rule the till applies.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- product: Aqua Park logo T-shirt
  variant: Green / M
  sku: TSH-AQP-GRN-M
  barcode: '6291100456781'
  outlet: Marina Bay Store
  price: AED 89.00
  onHand: 42
  returnable: true
  returnWindowDays: 14
- product: Kids swim goggles
  variant: Blue
  sku: GOG-KID-BLU
  barcode: '6291100456798'
  outlet: Beach Hut
  price: AED 35.00
  onHand: 120
- product: Waterproof phone pouch
  variant: Black
  sku: ACC-PCH-BLK
  outlet: Main Gate Kiosk
  price: AED 25.00
  stock: Not stock-tracked
```

#### Permissions

- `listMerchandise` → `PRODUCT_VIEW` (read) · staff, guest
- `createMerchandise` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateMerchandise` → `PRODUCT_CONFIGURE` (configure) · staff
- `listOutlets` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PRODUCT_VIEW`, which `listMerchandise` requires to show this screen, and names that permission (the screen's other reads need `SCOPE_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for `createMerchandise`, `updateMerchandise`.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.51 | Merchandise Catalog - System shall provide merchandise browsing. | Guest Mobile App & Branding | CONTRACTED | `listMerchandise` |
| 13.3.10 | APIs shall support product catalogs, inventory availability, promotions, orders, exchanges and returns. | Developer & API Management | CONTRACTED | `listMerchandise` |
| 4.4.10 | Centralized catalog management for retail products including SKU, barcode, category, pricing, images, supplier information, status management, and product lifecycle control. | Bundles and Promotions | CONTRACTED | `createMerchandise` |
| 4.4.11 | Support product variants such as size, color, style, material, and edition. Each variant may have independent SKU, barcode, inventory, and pricing. | Bundles and Promotions | CONTRACTED | `createMerchandise` |
| 4.4.12 | Support automatic and manual SKU generation, barcode assignment, barcode printing, barcode scanning, and duplicate validation. | Bundles and Promotions | CONTRACTED | `createMerchandise` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Retail Product & Catalog Command Center tracks total products per store, classification into catalogs, top products sold and product-by-category breakdowns. *(client request · MoM 19 Aug 2026, 4.2 Product Catalog, Variant & Pricing Management · DI-353)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-048` · status **notStarted** · provenance generated
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (26), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (19 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-048?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create merchandise, Save merchandise.
- [ ] Every transition is wired: `BO-008`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`, `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-059` Sales Reports

**See what sold, through which channel.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_VENUE` (1 configure, 1 operate) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listReports` reads the population and `getFinancialReport` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `conversationId` (deepLink), `reportId` (deepLink) · cold entry: A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. |
| Route | `/venue-operations/sales-reports` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **One reporting area, one set of numbers** (decided 2 October 2026, Chinmay; CHG-FIN-006; DI-721, DI-702). This screen is a scoped window onto the reporting area (Analytics, P16): it runs the same seeded report definitions and reads the same seeded KPIs, so its figures equal what Analytics shows for the same scope, period and as-of time. It computes no total of its own and shows the as-of time on every figure.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** What sold, through which channel: the seeded sales-by-channel report with the end-of-day breakdowns the finance team asked for (payment methods, totals, voids, deposits, itemised ticket sales). Scope can narrow to an operating area, showing all transactions from its workstations. The one thing to get right: the measures are labelled as what they are (gross sales, discounts, refunds, net revenue), and channels use one fixed list so two reports never bucket a day differently.

**Known correction pending (do not draw the wrong version)**

- **Authoring actions (create, save, retire report, save a natural-language query) and a P&L load are on a sales report.** Why: Authoring is the builder's and the library's job; this screen runs one report. *(source: screens/P08-venue-back-office.yaml#BO-059 / R276; Finance, Ledger & Tax · Reporting & Analytics)*
- **The channel list differs across the catalogue, F&B and retail contracts.** Why: Sales by channel is reported three ways today; one closed list is needed. *(source: MoM 2026-08-18 4.2 Recipes, Operating Hours & Service Channels / MATRIX 1.4.7; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does net revenue here include VAT?** → Net revenue excludes VAT. *(decided by Chinmay, 2026-10-02; DEC-354 / CHG-FIN-007 / CHG-FIN-006 / CHG-NOTE-003)*

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

- **Filters**: Date range, site, operating area, sales channel, workstation, user; defaults to yesterday for the user's venue. *(source: DI-183 / DI-151)*

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
| Create report (primary button) | `createReport` POST `/reports` | CreateReportRequest | ReportDefinition | 400 Unknown field, invalid filter, or estimated cost beyond the limit; 403 Author does not hold the permission they assigned to the report | opens modal first |
| Ask reporting question (secondary button) | `askReportingQuestion` POST `/reports/ask` | inline | NaturalLanguageAnswer | 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope | opens modal first |
| Delete report (destructive button) | `deleteReport` DELETE `/reports/{reportId}` | — | — | 409 Active schedules reference this report (`report-scheduled`), or it is a system report, which is clone-only (`system-report`, audit R096) | — |
| Run report (secondary button) | `runReport` POST `/reports/{reportId}/run` | RunReportRequest | ReportResult | 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope | opens modal first |
| Save natural language query (secondary button) | `saveNaturalLanguageQuery` POST `/reports/ask/{conversationId}/save` | inline | ReportDefinition | — | opens modal first |
| Save report (secondary button) | `updateReport` PUT `/reports/{reportId}` | CreateReportRequest | ReportDefinition | 409 The report is a system report, which is clone-only (audit R096). | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Channel table**: One row per channel (POS, Web, App, Kiosk, B2B, OTA): orders, gross sales, discounts, refunds, net revenue, share; totals row. Drill a channel to its workstations, then transactions. *(source: R282 / DI-709 / MATRIX 8.7.4)*
- **Payment summary**: By payment method and by cashier; foreign currency shown with the AED equivalent. *(source: DI-183 / DI-282)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Run**: Runs the seeded sales-by-channel report with the filters. *(source: contracts/satellite/reporting.yaml#runReport / R282)*
- **Export**: PDF or Excel of exactly what is on screen. *(source: DI-708)*

**Data it reads**: `getFinancialReport` (onLoad, P&L, balance sheet or cash flow); `listReports` (onLoad, List available report definitions)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*

**What opens over it**

- confirmDialog *Delete report*: **Names what `deleteReport` changes and what it leaves alone**, in the consequence rather than the verb. A sales reports this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sales reports list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sales reports untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sales reports yet. Offers Create report (`createReport`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on category, search and the sales reports are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `getFinancialReport` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `REPORT_MANAGE` for `createReport`, `deleteReport`, `saveNaturalLanguageQuery`, `updateReport`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Question could not be interpreted. (ReportQuestionProblem); 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 400 Unknown field, invalid filter, or estimated cost beyond the limit; 409 Active schedules reference this report (`report-scheduled`), or it is a system report, which is clone-only (`system-report` … |

#### Edge cases to draw

- **A till not yet closed in the range**: Banner "2 tills still open; figures may change" rather than a silent partial total. *(source: F74 step 2)*

#### Consistency with other screens

- Match `ANL-016`: Same channel names and the same net revenue definition as the analytics sales board.
- Match `BO-058`: Opened from the library; not a library itself.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
range: 29 Sep 2026 · Aquaventure Waterpark · all areas
rows:
- POS · 1,204 orders · gross AED 186,420.00 · discounts AED 4,120.00 · refunds AED 1,196.00 · net AED 181,104.00
- Web · 812 · gross AED 241,700.00 · net AED 236,880.00
- OTA · 96 · gross AED 28,704.00 · net AED 28,704.00
```

#### Permissions

- `getFinancialReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `listReports` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `createReport` → `REPORT_MANAGE` (configure) · staff, partner
- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `deleteReport` → `REPORT_MANAGE` (configure) · staff, partner
- `getReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `saveNaturalLanguageQuery` → `REPORT_MANAGE` (configure) · staff, partner
- `updateReport` → `REPORT_MANAGE` (configure) · staff, partner

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `getFinancialReport` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `REPORT_MANAGE` for `createReport`, `deleteReport`, `saveNaturalLanguageQuery`, `updateReport`.

#### Requirements it meets

93 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.7.45 | Support account consolidation. | F&B & Guest Management | CONTRACTED | `getFinancialReport` |
| 5.7.53 | Cross-site financial consolidation. | F&B & Guest Management | CONTRACTED | `getFinancialReport` |
| 5.7.55 | Site-level profit and loss reporting. | F&B & Guest Management | CONTRACTED | `getFinancialReport` |
| 5.7.73 | Profit & Loss reporting. | F&B & Guest Management | CONTRACTED | `getFinancialReport` |
| 5.7.74 | Balance Sheet reporting. | F&B & Guest Management | CONTRACTED | `getFinancialReport` |
| 1.1.40 | System shall provide analytics and dashboards covering ticket sales, attendance, utilization, conversion rates, capacity utilization and revenue performance. | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.104 | Membership analytics | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.135 | Required Reports Operational Reports Donations by Campaign. Donations by Site. Donations by Product. Donations by Sales Channel. Donations by Date. Donations by User/Cashier. Donations by Payment … | Ticketing Catalogue | CONTRACTED | `createReport` |
| 3.2.65 | An Entry or Exit report is expected presenting the readings per outcome (ok/ko), per time and per access point. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.66 | The in park report showing the difference between the Entries and the Exits. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.68 | The length of stay report shall present the difference between the time in scan and the time out scan. | Admission and Access | CONTRACTED | `createReport` |
| 3.5.12 | System shall provide analytics showing bundle sales volume, revenue contribution, conversion rate, redemption rate, average order value impact, profitability, and performance by channel. | Admission and Access | CONTRACTED | `createReport` |
| … 81 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- End-of-day reports: cashier shift, till, sales by location, payment type summary, cash management, variance, refund, and consolidated end-of-day (e.g. expected 8,480 AED vs deposited 8,460 AED = 20 AED shortage, posted to an overage/shortage account visible at month-end). *(agreed · MoM 12 Aug 2026, 20. End-of-Day Reports and Overage/Shortage Handling · DI-275)*
- Report library filterable by site, operating area, sales channel, workstation or user; e.g. Sales Report (payment-method breakdown, totals, voids, deposits, itemised ticket sales) and Payment Summary (per-cashier breakdown). *(agreed · MoM 7 Aug 2026, 21. Dashboards & Reporting · DI-183)*
- Sales reporting can be scoped to an operating area, showing all transactions from its workstations. *(agreed · MoM 7 Aug 2026, 3. Operating Areas, Workstations & Permissions Hierarchy · DI-151)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-059` · status **notStarted** · provenance generated
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)
- ADR-0059 *AI phasing against the six-month plan* (`docs/adr/0059-ai-phasing-against-the-six-month-plan.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (76), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-059?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create report, Ask reporting question, Delete report, Run report, Save natural language query, Save report.
- [ ] Every transition is wired: `BO-008`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_VENUE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-061` Scheduled Reports

**Send a report to somebody without them asking.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_SCHEDULE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listReportSchedules` reads the population and `listReportExecutions` reads the delivery history of the selected one — list, select, act |
| Offline | online only |
| Opens with | `reportId` (deepLink), `scheduleId` (navigation) · cold entry: A link to a report's schedules. Opens the list filtered to that report, or says the report no longer exists. |
| Route | `/venue-operations/scheduled-reports` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Rebound 28 September to report schedules (audit R254, R261)** — the screen carried report-definition and natural-language operations (`askReportingQuestion`, `saveNaturalLanguageQuery`, `getFinancialReport`, `deleteReport` and five more) that serve BO-058 and BO-060; it now lists, creates, changes and deletes schedules and shows each schedule's delivery history.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** A list of report schedules: which report goes to whom, how often, in what format, and whether the last delivery worked. A schedule runs under its owner's access, not the recipients', so the owner is accountable for who gets the data.

**Known correction pending (do not draw the wrong version)**

- **BO-061 duplicates P16 ANL-042 Report Scheduler (same list and create operations).** Why: DI-721 (agreed) is one consolidated reporting area, not schedulers per module. *(source: DI-721 / screens/P16-venue-analytics.yaml#ANL-042; Finance, Ledger & Tax · Reporting & Analytics)*
- **A transition to BO-008 Product Detail & Variants is declared.** Why: Inferred edge with no meaning for scheduling. *(source: screens/P08-venue-back-office.yaml#BO-061; Finance, Ledger & Tax · Reporting & Analytics)*
- **Export formats are CSV, Excel, PDF and JSON; XML, which the reporting requirement lists, is missing.** Why: The requirement names PDF, Excel, delimited text and XML. *(source: contracts/satellite/reporting.yaml#/components/schemas/ExportFormat / screens/P16-venue-analytics.yaml#ANL-045; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

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

**Form: Save report schedule** (modal, opened by *Save report schedule*; *Save report schedule* calls `updateReportSchedule`, *Cancel* sends nothing)

**Collects what `updateReportSchedule` sends before it is called.** At least one of `isPaused`, `cadence`, `recipients`, `format`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Is paused `isPaused` | toggle | optional | — | — | — | — | `updateReportSchedule` body |
| Cadence `cadence` | group | optional | — | — | — | What each frequency needs (decided 28 September, audit R158). `daily`: `timeOfDay`. | `updateReportSchedule` body |
| Frequency `cadence.frequency` | select | required | — | Daily · Weekly · Monthly · Quarterly · On shift close · On period close | — | — | `updateReportSchedule` body |
| Day of week `cadence.dayOfWeek` | stepper or slider | optional | — | min 0; max 6 | — | — | `updateReportSchedule` body |
| Day of month `cadence.dayOfMonth` | stepper or slider | optional | — | min 1; max 31 | — | — | `updateReportSchedule` body |
| Time of day `cadence.timeOfDay` | text field | optional | — | pattern `^([01]\d/2[0-3]):[0-5]\d$` | — | — | `updateReportSchedule` body |
| Recipients `recipients` | repeatable rows | optional | — | — | — | — | `updateReportSchedule` body |
| Kind `recipients[].kind` | radio group | required | — | Principal · Email · Sftp · Webhook | — | — | `updateReportSchedule` body |
| Address `recipients[].address` | text field | required | — | — | — | — | `updateReportSchedule` body |
| Principal `recipients[].principalId` | picker: choose a principal | optional | — | — | shows names, sends the id | — | `updateReportSchedule` body |
| Format `format` | radio group | optional | — | Csv · Xlsx · Pdf · Json | — | — | `updateReportSchedule` body |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **cadence**: Daily (time), weekly (day and time), monthly (day and time; 31 runs on the last day), quarterly (day in the first month and time), on shift close, on period close. Times are in the venue's time zone, shown next to the field. *(source: contracts/satellite/reporting.yaml#/components/schemas/Cadence / R158)*
- **recipients**: People in the system, email addresses, SFTP or webhook; at least one. External addresses show a warning that the data leaves the system. *(source: contracts/satellite/reporting.yaml#/components/schemas/Recipient)*
- **include personal data**: Off by default; only offered to users allowed to export personal data, and recorded. *(source: contracts/satellite/reporting.yaml#/components/schemas/CreateReportScheduleRequest / contracts/shared/permissions.yaml#/components/schemas/Permission)*
- **skip if empty**: On by default, explained as "Don't send an empty report". *(source: contracts/satellite/reporting.yaml#/components/schemas/CreateReportScheduleRequest)*

#### Outputs: what the screen shows and produces

**Shown**

**Every report schedule** (data table, from `listReportSchedules`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Is paused | yes / no (icon or chip) | — |
| Last run at | 1 Oct 2026, 14:30 | — |
| Last run status | chip: Queued, Running, Completed, Failed, Cancelled, Expired | — |
| Next run at | 1 Oct 2026, 14:30 | — |
| Consecutive failures | 1,234 | — |

**Delivery history** (data table, from `listReportExecutions`): Sends `?reportId=` of the selected schedule to `listReportExecutions`; each run the schedule made is a row, with its status and any error, so a recipient who says they never got it can be answered.

| Shows | Format | Notes |
|---|---|---|
| Requested at | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |
| Status | chip: Queued, Running, Completed, Failed, Cancelled, Expired | — |
| Row count | 1,234 | — |
| Error | text | — |
| Expires at | 1 Oct 2026, 14:30 | Results are retained for a limited period, then discarded. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create report schedule (primary button) | `createReportSchedule` POST `/report-schedules` | CreateReportScheduleRequest | ReportSchedule | 400 Invalid cadence (a field its frequency needs is missing, or one it does not take is sent, audit R158), or no recipients | opens modal first |
| Save report schedule (secondary button) | `updateReportSchedule` PATCH `/report-schedules/{scheduleId}` | inline | ReportSchedule | — | opens modal first |
| Delete report schedule (destructive button) | `deleteReportSchedule` DELETE `/report-schedules/{scheduleId}` | — | — | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **schedule row**: Report, cadence in words ("Every Monday 08:00, Dubai time"), recipients count, format, owner, next run, last run with status; a failing schedule shows its consecutive failures in red. *(source: contracts/satellite/reporting.yaml#/components/schemas/ReportSchedule)*
- **delivery history**: Each run with time, status, rows, and the error in words, so "I never got it" can be answered. *(source: F107 step 3 / MATRIX 6.1.15)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Pause or resume**: Stops future runs without deleting; paused rows are greyed with "Paused by …". *(source: contracts/satellite/reporting.yaml#updateReportSchedule)*
- **Delete**: Confirmation names the schedule and who stops receiving it; history stays. *(source: screens/P08-venue-back-office.yaml#BO-061)*

**Data it reads**: `listReportSchedules` (onLoad, Every scheduled delivery)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*
- → `BO-060` Attendance & Footfall: *Attendance & Footfall*; carries `reportId`

**What opens over it**

- confirmDialog *Delete report schedule*: **Names the schedule and who stops receiving it.** Deleting stops future deliveries; the delivery history already made stays.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report schedules. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the schedules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report schedules yet. Offers Create report schedule (`createReportSchedule`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listReportSchedules` takes no filter here, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listReportSchedules` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `REPORT_SCHEDULE` for `createReportSchedule`, `updateReportSchedule`, `deleteReportSchedule`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Invalid cadence (a field its frequency needs is missing, or one it does not take is sent, audit R158), or no recipients |

#### Edge cases to draw

- **the owner leaves or loses access**: The schedule fails and says why; it never silently continues under someone else. *(source: contracts/satellite/reporting.yaml#/components/schemas/ReportSchedule)*
- **changing a schedule's parameters**: Not editable after creation; offer "Duplicate with new parameters". *(source: contracts/satellite/reporting.yaml#updateReportSchedule)*

#### Consistency with other screens

- Match `P16 ANL-042 Report Scheduler, ANL-043 Subscription Manager, ANL-048 Delivery Monitoring`: Same operations and same list; DI-721 wants this in the one reporting area.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- Daily takings by outlet · every day 07:00 Dubai time · 4 recipients · PDF · owner Fatima Al Mansoori · last run
  1 Oct 07:00 delivered, 38 rows
- Month-end deferred revenue · on period close · finance@aquaventure.ae · Excel · last run 2 Sep delivered
- Weekly admissions by channel · Mondays 08:00 · 3 recipients · CSV · 3 failures · 'Mailbox rejected the message
  (550)'
```

#### Permissions

- `listReportSchedules` → `REPORT_VIEW_VENUE` (operate) · staff
- `createReportSchedule` → `REPORT_SCHEDULE` (operate) · staff
- `updateReportSchedule` → `REPORT_SCHEDULE` (operate) · staff
- `deleteReportSchedule` → `REPORT_SCHEDULE` (operate) · staff
- `listReportExecutions` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listReportSchedules` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `REPORT_SCHEDULE` for `createReportSchedule`, `updateReportSchedule`, `deleteReportSchedule`.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.14 | The system should have scheduling of report generation and delivery to web address location or list of email addresses. | Retail POS | CONTRACTED | `createReportSchedule` |
| 8.7.15 | System shall support report scheduling. | Unified Operations Dashboard | CONTRACTED | `createReportSchedule` |
| 8.7.16 | System shall support report subscriptions. | Unified Operations Dashboard | CONTRACTED | `createReportSchedule` |
| 8.7.17 | System shall support report sharing. | Unified Operations Dashboard | CONTRACTED | `createReportSchedule` |
| 6.1.15 | The system should be able to generate report logs (e.g. user logs). | Retail POS | CONTRACTED | `listReportExecutions` |
| 6.1.77 | Required Reports User Activity Audit Security Configuration Audit Login Audit Access Control Override Report Ticket Reissue Audit Refund Approval Audit Waiver Audit Trail Payment Audit Trail | Retail POS | CONTRACTED | `listReportExecutions` |
| 8.7.32 | System shall support report audit trails. | Unified Operations Dashboard | CONTRACTED | `listReportExecutions` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-061` · status **notStarted** · provenance generated
- Flow F107 *A report is defined, scheduled and delivered*, step 2: It is scheduled to the people who need it. → **Every Monday, to these people**, without anybody remembering to run it.
- Flow F107 *A report is defined, scheduled and delivered*, step 3: Each delivery is checked. → **Delivered, or failed and said so.** A schedule that silently stops is worse than none.

#### Acceptance for the design

- [ ] Every input above is drawn (26), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-061?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create report schedule, Save report schedule, Delete report schedule.
- [ ] Every transition is wired: `BO-008`, `BO-060`.
- [ ] Every gated control is gated: `REPORT_SCHEDULE`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-062` Venue Profile

**The facts every other surface reads.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW`, `REGION_CONFIGURE` (1 read, 1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listDiningOutlets` reads the population and `getRefundPolicy` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/venue-operations/venue-profile` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-025): listDiningOutlets and listDeliveryLocations are guest-audience reads with no permission; a staff screen calling them bypasses the staff permission model, as … Removed 2 October 2026 (CHG-WIR-025): listDiningOutlets and listDeliveryLocations are guest-audience reads with no permission; a staff screen calling them bypasses the staff permission model, as …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The venue facts other surfaces read: refund policy, dining outlets and delivery locations.

#### Inputs: what the user enters or picks

**Form: Save refund policy** (modal, opened by *Save refund policy*; *Save refund policy* calls `setRefundPolicy`, *Cancel* sends nothing)

**Collects what `setRefundPolicy` sends before it is called.** Required: `selfAuthoriseLimit`, `requiresApprovalAbove`. Optional: `requiresSecondUserAbove`, `timeBands`, `allowPartial`, `refundWindowDays`, `varianceThreshold`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `venueId` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Self authorise limit `selfAuthoriseLimit` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Up to this, a holder of ORDER_REFUND refunds alone. Zero means every refund needs a second authoriser. | `setRefundPolicy` body |
| Requires second user above `requiresSecondUserAbove` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Above this, a second user — cashier OR supervisor — names themselves as audit control. | `setRefundPolicy` body |
| Requires approval above `requiresApprovalAbove` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Above this, an ORDER_REFUND_APPROVE holder must approve. | `setRefundPolicy` body |
| Time bands `timeBands` | repeatable rows | optional | — | — | — | Refundable percentage by time before the performance. Evaluated most-specific first. | `setRefundPolicy` body |
| Hours before `timeBands[].hoursBefore` | number field | required | — | min 0 | — | — | `setRefundPolicy` body |
| Percentage `timeBands[].percentage` | stepper or slider (%) | required | — | min 0; max 100 | — | — | `setRefundPolicy` body |
| Allow partial `allowPartial` | toggle | optional | on | — | — | — | `setRefundPolicy` body |
| Refund window days `refundWindowDays` | number field (days) | optional | — | min 0 | — | Days after purchase within which a refund may be made. 0 is allowed and means the day of purchase only; null means no window (decided 28 September, audit R123 (6)). | `setRefundPolicy` body |
| Variance threshold `varianceThreshold` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Price variance above this is an exception requiring review rather than a routine posting (CF-38). | `setRefundPolicy` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.; 422 The thresholds do not ascend: `selfAuthoriseLimit` above `requiresSecondUserAbove`, or either above `requiresApprovalAbove` (`refund-thresholds-not-ascending` …

#### Outputs: what the screen shows and produces

**Shown**

**The refund policy** (detail panel, from `getRefundPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Self authorise limit | AED 1,234.50 | Up to this, a holder of ORDER_REFUND refunds alone. Zero means every refund needs a second authoriser. |
| Requires second user above | AED 1,234.50 | Above this, a second user — cashier OR supervisor — names themselves as audit control. |
| Requires approval above | AED 1,234.50 | Above this, an ORDER_REFUND_APPROVE holder must approve. |
| Time bands | list or chips (count when long) | Refundable percentage by time before the performance. Evaluated most-specific first. |
| Allow partial | yes / no (icon or chip) | — |
| Refund window days | 1,234 | Days after purchase within which a refund may be made. 0 is allowed and means the day of purchase only; null means no window (decided 28 … |
| Variance threshold | AED 1,234.50 | Price variance above this is an exception requiring review rather than a routine posting (CF-38). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save refund policy (primary button) | `setRefundPolicy` PUT `/venues/{venueId}/refund-policy` | RefundPolicy | RefundPolicy | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.; 422 The thresholds do not ascend: `selfAuthoriseLimit` above `requiresSecondUserAbove`, or either above `requiresApprovalAbove` … | opens modal first |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **profile sections**: Refund policy summary with thresholds and time bands; outlets open now; delivery locations by kind (tables, seats, cabanas). *(source: contracts/spine/orders.yaml#getRefundPolicy / contracts/satellite/fnb.yaml#listDeliveryLocations)*

**Data it reads**: `getRefundPolicy` (onLoad, Read a venue's refund policy)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue profile list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue profile yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on openNow, orderingMethod and the venue profile are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getRefundPolicy` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `REGION_CONFIGURE` for `setRefundPolicy`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 The thresholds do not ascend: `selfAuthoriseLimit` above `requiresSecondUserAbove`, or either above `requiresApprovalAbove` (`refund-thresholds-not-ascending` … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue:
  name: Dune Park
  refund: self-authorise to AED 500.00, approval above AED 2,000.00
  outletsOpen: 6
```

#### Permissions

- `getRefundPolicy` → `ORDER_VIEW` (read) · staff
- `setRefundPolicy` → `REGION_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getRefundPolicy` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `REGION_CONFIGURE` for `setRefundPolicy`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-062` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (404, 412, 422).
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-062?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save refund policy.
- [ ] Every transition is wired: `BO-008`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `REGION_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-065` Venue Configuration

**Set the venue-level values everything inherits from.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | Block A · task APP-SETUP-BO-065 |
| Who uses it | venue staff holding `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `REGION_CONFIGURE`, `SCOPE_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW`… (3 read, 4 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listDiningOutlets` reads the population and `getRefundPolicy` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `locationId` (navigation) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/venue-operations/venue-configuration` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. CF-53 — 67 of these 73 had no definition at all. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-008): listDiningOutlets (a guest read of outlets open now) and listDeliveryLocations are guest-audience reads, not venue configuration; outlets are configured on … Removed 2 October 2026 (CHG-WIR-008): listDiningOutlets (a guest read of outlets open now) and listDeliveryLocations are guest-audience reads, not venue configuration; outlets are configured on … Contract gap recorded 2 October 2026 (CHG-WIR-011): No staff-audience read of delivery locations.

**From the Food, Beverage & Retail process.** The venue's own settings, which everything at the venue inherits: the configured limits (cart hold, resale/exchange/reschedule cut-offs, shift variance threshold, F&B recall window and comp escalation, food-safety lead, stock-count tolerances…), support and quiet hours, biometrics, segregated access, alerting, display currencies and guest two-step verification; the refund policy; and where food can be delivered. One thing to get right: every limit left empty inherits the tenant default, and the screen shows that default and where each value comes from.

**Fixed on main** (the package already carries these; draw what it says): requiresModule ticketing. (CHG-SBO-003); The main list is "Every dining outlet" from listDiningOutlets (a guest read that returns only outlets open now) with an "Open now" toggle … (CHG-WIR-008); Only guest two-step is laid out; the venue-settings modal lists 18 raw property names with "nothing required", although they are the … (CHG-SBO-008); The cash settings agreed for this screen have no field anywhere: opening-float entry mode (total or by denomination, per venue) … (CHG-SBO-008); Exit to BO-008 Product Detail & Variants; module "Orders & Money". (CHG-WIR-009).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the trading day configurable (midnight-to-midnight or 6am-to-6am)?** → Drawn default stands (answer: "Default / recommended accepted"): Draw "Calendar day starts at 06:00" (calendarDayStartHour) as the calendar view setting only, and do not label it as the trading/business day. *(decided by Chinmay, 2026-10-02; DEC-039 / CHG-NOTE-004)*
- **Who may read venue settings — TENANT_VIEW, or a dedicated read permission?** → Drawn default stands (answer: "Default / recommended accepted"): Read-only view for anyone who can open the screen; edit with the configure permission. *(decided by Chinmay, 2026-10-02; DEC-040 / CHG-NOTE-004)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Guest two-step verification | toggle | optional | off | — | — | **A venue option, off unless the venue enables it** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167 "no guest MFA"; guests still never use enterprise SSO). … | `VenueSettings.identity.guestTwoStep.enabled` |
| Actions that ask again | multi-select chips | optional | Change contact details, Change password, Manage payment methods, Delete account | Change contact details · Change password · Manage payment methods · Transfer tickets · Delete account; no duplicates | — | The guest actions at this venue that ask an enrolled guest for the factor again, whatever the age of the session: change contact details, change password, manage payment methods, transfer tickets … | `VenueSettings.identity.guestTwoStep.stepUpActions` |

**Form: Save refund policy** (modal, opened by *Save refund policy*; *Save refund policy* calls `setRefundPolicy`, *Cancel* sends nothing)

**Collects what `setRefundPolicy` sends before it is called.** Required: `selfAuthoriseLimit`, `requiresApprovalAbove`. Optional: `requiresSecondUserAbove`, `timeBands`, `allowPartial`, `refundWindowDays`, `varianceThreshold`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `venueId` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Self authorise limit `selfAuthoriseLimit` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Up to this, a holder of ORDER_REFUND refunds alone. Zero means every refund needs a second authoriser. | `setRefundPolicy` body |
| Requires second user above `requiresSecondUserAbove` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Above this, a second user — cashier OR supervisor — names themselves as audit control. | `setRefundPolicy` body |
| Requires approval above `requiresApprovalAbove` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Above this, an ORDER_REFUND_APPROVE holder must approve. | `setRefundPolicy` body |
| Time bands `timeBands` | repeatable rows | optional | — | — | — | Refundable percentage by time before the performance. Evaluated most-specific first. | `setRefundPolicy` body |
| Hours before `timeBands[].hoursBefore` | number field | required | — | min 0 | — | — | `setRefundPolicy` body |
| Percentage `timeBands[].percentage` | stepper or slider (%) | required | — | min 0; max 100 | — | — | `setRefundPolicy` body |
| Allow partial `allowPartial` | toggle | optional | on | — | — | — | `setRefundPolicy` body |
| Refund window days `refundWindowDays` | number field (days) | optional | — | min 0 | — | Days after purchase within which a refund may be made. 0 is allowed and means the day of purchase only; null means no window (decided 28 September, audit R123 (6)). | `setRefundPolicy` body |
| Variance threshold `varianceThreshold` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Price variance above this is an exception requiring review rather than a routine posting (CF-38). | `setRefundPolicy` body |

Errors to draw in the form: 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.; 422 The thresholds do not ascend: `selfAuthoriseLimit` above `requiresSecondUserAbove`, or either above `requiresApprovalAbove` (`refund-thresholds-not-ascending` …

**Form: Save venue settings** (modal, opened by *Save venue settings*; *Save venue settings* calls `setVenueSettings`, *Cancel* sends nothing)

**Collects what `setVenueSettings` sends before it is called, in sections, not property names.** Nothing in the body is required. **Day and hours**: calendar day start, support hours, quiet hours. **Money**: display and charge currencies (the guest selects among them, CHG-FIN-001), cash drawer limit (warns and offers a cash lift, DEC-179), shift variance threshold. **Carts and resale**: cart lease, extensions, resale, exchange and reschedule cut-offs. **F&B limits**: recall window, comp escalation, table reserved lead, food-safety lead. **Biometrics** (master switch, consent form, minors) and **segregated access**. **Alerting**: channel, acknowledgement, escalation. Currency code and scale …

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Calendar day start hour `calendarDayStartHour` | stepper or slider | optional | 6 | min 0; max 23 | — | Where the venue's calendar day starts (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in … | `setVenueSettings` body |
| Support hours `supportHours` | group | optional | — | — | — | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. | `setVenueSettings` body |
| Mode `supportHours.mode` | radio group | optional | — | Always on · Business hours · Custom · None | — | — | `setVenueSettings` body |
| Timezone `supportHours.timezone` | text field | optional | — | — | — | IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract. | `setVenueSettings` body |
| Windows `supportHours.windows` | repeatable rows | optional | — | — | — | — | `setVenueSettings` body |
| Day `supportHours.windows[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettings` body |
| From `supportHours.windows[].from` | text field | optional | — | — | — | Wall-clock time the desk opens. | `setVenueSettings` body |
| To `supportHours.windows[].to` | text field | optional | — | — | — | Wall-clock time the desk closes. | `setVenueSettings` body |
| Out of hours message `supportHours.outOfHoursMessage` | text field | optional | — | — | — | — | `setVenueSettings` body |
| Quiet hours `quietHours` | group | optional | — | — | — | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. | `setVenueSettings` body |
| From `quietHours.from` | text field | optional | — | — | — | Wall-clock time sending stops | `setVenueSettings` body |
| To `quietHours.to` | text field | optional | — | — | — | Wall-clock time sending resumes | `setVenueSettings` body |
| Biometrics `biometrics` | group | optional | — | — | — | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. | `setVenueSettings` body |
| Is enabled `biometrics.isEnabled` | toggle | optional | off | Off by default, and turning it on is refused without the two fields below. | — | Off by default, and turning it on is refused without the two fields below. `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — a DPIA nobody can … | `setVenueSettings` body |
| Dpia reference `biometrics.dpiaReference` | text field | optional | — | max length 200 | — | The venue's own reference for its Article 21 assessment. The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is … | `setVenueSettings` body |
| Consent notice acknowledged at `biometrics.consentNoticeAcknowledgedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When somebody confirmed the consent forms are in place at the point of capture. A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice … | `setVenueSettings` body |
| Face tag purge minutes after close `biometrics.faceTagPurgeMinutesAfterClose` | number field (minutes) | optional | 0 | — | — | BL-106. How long a same-visit Face Tag survives past the close of the operating day, and zero is the default because that is what 3.2.44 describes. | `setVenueSettings` body |
| Consent form `biometrics.consentFormId` | picker: choose a consent form | optional | — | Turning `isEnabled` on without one is refused `422 consent-form-required`, as a missing DPIA is; each Face Pass and Face Tag capture records the form and its version it was consented on (access … | shows names, sends the id | The venue's own consent form, which every biometric capture is taken on (decided 2 October 2026, Chinmay, batch 4, BO-188: "Consent first, on the venue's consent form"; DEC-128 … | `setVenueSettings` body |
| Allow minors `biometrics.allowMinors` | toggle | optional | on | Off: a minor's enrolment is refused (`422 minors-not-enrolled`) and the guest uses another verification method. | — | Whether this venue enrols minors at all (decided 2 October 2026, Chinmay, critical set 1, BO-187 and CMS-029: "Guardian consent on the venue's form; minor age per country; the … | `setVenueSettings` body |
| Accreditation face matching `biometrics.accreditationFaceMatching` | group | optional | — | Face matching to find duplicate accreditation applicants, off unless the venue enables it (decided 2 October 2026, Chinmay, critical set 3, BO-631: "Only where the venue enables it, with applicant …; Enabling it is refused without `legalSignOffReference` … | — | Face matching to find duplicate accreditation applicants, off unless the venue enables it (decided 2 October 2026, Chinmay, critical set 3, BO-631: "Only where the venue enables … | `setVenueSettings` body |
| Is enabled `biometrics.accreditationFaceMatching.isEnabled` | toggle | optional | off | — | — | — | `setVenueSettings` body |
| Legal sign off reference `biometrics.accreditationFaceMatching.legalSignOffReference` | text field | optional | — | max length 200 | — | The venue's own reference for its legal sign-off; the platform records that one was named, by whom and when. | `setVenueSettings` body |
| Segregated access `segregatedAccess` | group | optional | — | — | — | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a prayer-time closure. | `setVenueSettings` body |
| Is enabled `segregatedAccess.isEnabled` | toggle | optional | off | — | — | — | `setVenueSettings` body |
| Applies to access points `segregatedAccess.appliesToAccessPointIds` | multi-picker: choose applies to access points | optional | — | — | — | — | `setVenueSettings` body |
| Schedule `segregatedAccess.schedule` | repeatable rows | optional | — | — | — | — | `setVenueSettings` body |
| Day `segregatedAccess.schedule[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettings` body |
| From `segregatedAccess.schedule[].from` | text field | optional | — | — | — | Wall-clock time | `setVenueSettings` body |
| To `segregatedAccess.schedule[].to` | text field | optional | — | — | — | Wall-clock time | `setVenueSettings` body |
| Admits `segregatedAccess.schedule[].admits` | radio group | optional | — | All · Women · Women and children · Families · Members | — | — | `setVenueSettings` body |
| Gender verification `segregatedAccess.genderVerification` | segmented control | optional | Off | Off · Staff assisted · Device assisted; Available only where the driver reports the capability, and the result is advisory to the steward rather than decisive at the turnstile (3. | — | `off` — the entitlement decides and a steward handles exceptions. The default, and what is contracted. | `setVenueSettings` body |
| Override rate alert threshold `segregatedAccess.overrideRateAlertThreshold` | number field | optional | — | — | — | Where `deviceAssisted` is on. An override rate near zero means the steward has stopped deciding, and that is the number that says whether the human safeguard is working or … | `setVenueSettings` body |
| Alerting `alerting` | group | optional | — | The panel is the default and email or WhatsApp only where the matrix names them — an operational alert that arrives by email is an alert nobody sees in time. | — | CF-134. On-platform notification, marked as read. | `setVenueSettings` body |
| Channel `alerting.channel` | segmented control | optional | Dashboard panel | Dashboard panel · Dashboard and email · Dashboard and whatsapp | — | — | `setVenueSettings` body |
| Acknowledgement required `alerting.acknowledgementRequired` | toggle | optional | on | — | — | — | `setVenueSettings` body |
| Escalate after minutes `alerting.escalateAfterMinutes` | number field (minutes) | optional | — | — | — | — | `setVenueSettings` body |
| Display currencies `displayCurrencies` | list of values (chips) | optional | — | A code the region has no rate for is refused `400`. | — | Which currencies this venue shows guests (decided 28 September, audit R120 (a)). | `setVenueSettings` body |
| Charge currencies `chargeCurrencies` | list of values (chips) | optional | — | presentmentCurrencies`) and one the region holds a `tender` rate for; anything else is refused `400`. | — | Which currencies a guest may select and pay in (decided 2 October 2026, Chinmay; CHG-FIN-001; MoM 10 Aug 2026 4.7 option (b), DI-211). | `setVenueSettings` body |
| Cart lease seconds `cartLeaseSeconds` | number field (seconds) | optional | 900 | min 30; max 3600 | — | How long a cart holds capacity (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. | `setVenueSettings` body |
| Cart hold extension minutes `cartHoldExtensionMinutes` | stepper or slider (minutes) | optional | 5 | min 1; max 30 | — | How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094). | `setVenueSettings` body |
| Cart max extensions `cartMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). | `setVenueSettings` body |
| Resale cutoff hours `resaleCutoffHours` | number field (hours) | optional | 24 | min 0; max 168 | — | Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). | `setVenueSettings` body |
| Exchange cutoff hours `exchangeCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). | `setVenueSettings` body |
| Reschedule cutoff hours `rescheduleCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). | `setVenueSettings` body |
| Reservation max extensions `reservationMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094). | `setVenueSettings` body |
| … 34 more | | | | | | the rest are in `schemas.json` | `setVenueSettings` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 An enable the venue cannot evidence. Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender …

**Form: Save cash and shift rules** (modal, opened by *Save cash and shift rules*; *Save cash and shift rules* calls `setTillShiftPolicy`, *Cancel* sends nothing)

**Collects what `setTillShiftPolicy` sends before it is called.** Required: `venueId`. Optional: `requireOpenApproval`, `openingFloatTolerance`, `depositBoxRequired`, `bagNumberRequired`, `requireCloseApproval`, `autoCloseAfterHours`, `noSaleAlertCount`. Dismissing sends nothing; the screen behind is unchanged.

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

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Every configured limit**: Empty means "use the tenant default"; the placeholder shows that default ("Tenant default: 15 min") and a "Use default" control clears an override. Save replaces the whole record, so the form always sends every field it loaded. *(source: R094 / contracts/spine/tenancy.yaml#setVenueSettings / contracts/spine/tenancy.yaml#getVenueSettingsDefaults)*
- **Shift variance threshold**: Money in the venue currency, 0 to 1,000; proposed tenant default AED 20.00, over or short. *(source: R094 / contracts/spine/tenancy.yaml#/components/schemas/VenueSettings)*
- **Cart hold**: Shown in minutes (stored as seconds, 30–3,600); default 15 min; extension 1–30 min (default 5), at most 0–5 extensions (default 1). *(source: R169 / R094)*
- **F&B limits**: Recall window 0–60 min (default 10); comp escalation amount (proposed AED 100.00); food-safety lead — a person picker with no default (escalations are refused while empty). *(source: R094 / R096 / R197)*
- **Currency**: Read-only, "Set by the region"; the trading currency and its decimals cannot change here. *(source: ADR-0018 / contracts/spine/tenancy.yaml#/components/schemas/VenueSettings)*
- **Display currencies**: Currencies shown to guests, only those the region has an exchange rate for (e.g. AED, SAR, USD, INR, GBP). *(source: R120 / DI-1071)*
- **Refund policy thresholds**: Self-authorise up to ≤ second user above ≤ approval above; inline error when they do not ascend. Refund window 0 = day of purchase only, empty = no window. Partial refunds on by default. *(source: R123 / contracts/spine/orders.yaml#setRefundPolicy)*
- **Guest two-step verification**: Off by default; "actions that ask again" default to all except transfer tickets. *(source: contracts/spine/tenancy.yaml#setVenueSettings)*
- **Delivery location**: Kind (table, seat, cabana, sunbed, poolside, box, suite, lawn, collection point, named location); a table location picks the table, a seat location the seat; label unique in the venue and is what the runner reads ("Cabana 12"); walk time from the serving outlet; out of service with a reason. *(source: contracts/satellite/fnb.yaml#createDeliveryLocation / contracts/satellite/fnb.yaml#updateDeliveryLocation)*

#### Outputs: what the screen shows and produces

**Shown**

**The refund policy** (detail panel, from `getRefundPolicy`)

| Shows | Format | Notes |
|---|---|---|
| Self authorise limit | AED 1,234.50 | Up to this, a holder of ORDER_REFUND refunds alone. Zero means every refund needs a second authoriser. |
| Requires second user above | AED 1,234.50 | Above this, a second user — cashier OR supervisor — names themselves as audit control. |
| Requires approval above | AED 1,234.50 | Above this, an ORDER_REFUND_APPROVE holder must approve. |
| Time bands | list or chips (count when long) | Refundable percentage by time before the performance. Evaluated most-specific first. |
| Allow partial | yes / no (icon or chip) | — |
| Refund window days | 1,234 | Days after purchase within which a refund may be made. 0 is allowed and means the day of purchase only; null means no window (decided 28 … |
| Variance threshold | AED 1,234.50 | Price variance above this is an exception requiring review rather than a routine posting (CF-38). |

**Cash and shift rules** (detail panel, from `getTillShiftPolicy`): The opening float (total or by denomination), approval on open and close, mandatory bag number and deposit-box allocation, read from the till shift policy (CHG-CSP-020); the drawer limit is `cashDrawerLimit` (DEC-179).

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
| Save refund policy (primary button) | `setRefundPolicy` PUT `/venues/{venueId}/refund-policy` | RefundPolicy | RefundPolicy | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.; 422 The thresholds do not ascend: `selfAuthoriseLimit` above `requiresSecondUserAbove`, or either above `requiresApprovalAbove` … | opens modal first |
| Save venue settings (secondary button) | `setVenueSettings` PUT `/venues/{venueId}/settings` | VenueSettings | VenueSettings | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Save cash and shift rules (secondary button) | `setTillShiftPolicy` PUT `/venues/{venueId}/till-shift-policy` | TillShiftPolicy | TillShiftPolicy | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Settings sections**: Grouped: Trading & calendar, Cart & changes, Cash (variance threshold), Food & beverage, Stock, Guests & privacy (two-step, biometrics, segregated access), Notifications (quiet hours, alerting), Refunds, Delivery locations. Each value shows "Venue" or "Tenant default". *(source: R094 / contracts/spine/tenancy.yaml#/components/schemas/VenueSettings)*

**What each action does** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Save venue settings**: Success shows what changed; 422 names each missing item when biometrics are switched on without a DPIA reference and consent acknowledgement; 412 asks to reload. *(source: contracts/spine/tenancy.yaml#setVenueSettings)*
- **Save refund policy**: 422 "thresholds must ascend" points at the field. *(source: R123 / contracts/spine/orders.yaml#setRefundPolicy)*
- **Assign serving outlets**: Sets which outlets deliver to each location; a location nothing serves shows "Not serviceable", not hidden. *(source: contracts/satellite/fnb.yaml#setDeliveryLocationOutletMapping)*

**Data it reads**: `getRefundPolicy` (onLoad, Read a venue's refund policy); `getVenueSettings` (onLoad, The venue's settings, with the tenant default each empty …); `getTillShiftPolicy` (onLoad, The till shift policy: opening-float entry, open and close …)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on openNow, orderingMethod and the venue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `getRefundPolicy` requires to show this screen, and names that permission (the screen's other reads need `SCOPE_VIEW`, `TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for … |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A location with the same label already exists in the venue.; 422 A `table` location without `tableId`, a `seat` location without `seatId`, or a table of another venue.; 422 An enable the venue cannot evidence. Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender … |

#### Edge cases to draw

- **Shift rules changed while a shift is open**: F73 says the change is refused (a shift must close under the rules it opened under); show which tills are open if refused. *(source: F73 step 2)*
- **Delivery location label already used**: 409 names the existing location. *(source: contracts/satellite/fnb.yaml#createDeliveryLocation)*

#### Consistency with other screens

- Match `BO-1065`: Currency, decimals, time zone and denominations are region settings there; this screen shows currency read-only.
- Match `POS-019`: Shift Templates & Policies writes the same venue settings (F73 step 2); values must agree.
- Match `BO-063`: Venue opening hours and calendar are there, not here.
- Match `BO-044`: Outlet-level delivery rules are per outlet there; locations are venue-level here.
- Match `BO-1063`: seating.maxSeatsPerGuestOrder is set there, not here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Aqua Park Dubai
limits:
  cart_hold: 15 min (tenant default)
  shift_variance_threshold: AED 20.00 (tenant default)
  fnb_recall_window: 10 min
  comp_escalation: AED 100.00
  food_safety_lead: Fatima Al Suwaidi
display_currencies:
- AED
- SAR
- USD
- GBP
refund_policy:
  self_authorise: AED 200.00
  second_user_above: AED 500.00
  approval_above: AED 1,000.00
  window_days: 14
delivery_locations:
- label: Cabana 12
  kind: cabana
  zone: Wave Pool
  serving:
  - Pool Bar
  walk_time: 6 min
- label: Sunbed row C
  kind: sunbed
  serviceable: false
  reason: Section closed — weather
```

#### Permissions

- `getRefundPolicy` → `ORDER_VIEW` (read) · staff
- `setRefundPolicy` → `REGION_CONFIGURE` (configure) · staff
- `setVenueSettings` → `TENANT_CONFIGURE` (configure) · staff
- `getVenueSettings` → `TENANT_VIEW` (read) · staff
- `setDeliveryLocationOutletMapping` → `PRODUCT_CONFIGURE` (configure) · staff
- `createDeliveryLocation` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateDeliveryLocation` → `PRODUCT_CONFIGURE` (configure) · staff
- `getTillShiftPolicy` → `SCOPE_VIEW` (read) · staff
- `setTillShiftPolicy` → `WORKSTATION_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `getRefundPolicy` requires to show this screen, and names that permission (the screen's other reads need `SCOPE_VIEW`, `TENANT_VIEW` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PRODUCT_CONFIGURE` for …

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
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
| 16.9.58 | Device Incident Management - System shall support device incident management. | Device Management | CONTRACTED | data `VenueSettings` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Denominations configurable per currency/region (e.g. UAE 500, 200, 100, 50, 20; Bahrain has no 1000); amounts use 2 decimals (UAE) or 3 (Bahrain/Kuwait) with no rounding of the third decimal (2.013 stays 2.013). *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-306)*
- The operating calendar is configurable: a midnight-to-midnight transaction day or an alternative such as 6am to 6am. *(agreed · MoM 7 Aug 2026, 2. System Organization: Tenant & Site Setup · DI-149)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-065` · status **notStarted** · provenance generated
- ADR-0008 *Money carries per-region scale* (`docs/adr/0008-money-carries-per-region-scale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (98), with its required mark, default, format and its error state (400, 403, 404, 409, 412, 422).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-065?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save refund policy, Save venue settings, Save cash and shift rules.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `REGION_CONFIGURE`, `SCOPE_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW`, `WORKSTATION_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-074` Chart of Accounts

**Accounts, cost centres and legal entities.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | Block A · task APP-SETUP-BO-074 |
| Who uses it | venue staff holding `ACCOUNT_CONFIGURE`, `LEDGER_VIEW` (1 configure, 1 read); in the flows as finance controller, platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAccounts` reads the population and `getAccount` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `accountId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/finance/chart-of-accounts` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. Pulled to Wave 1 (CF-101). **F16 says it itself** — no chart of accounts blocks the first sale, so it cannot be built after venue provisioning.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Finance sets up the chart of accounts, cost centres and legal entities before the first sale (every sale posts somewhere). The chart is either built natively or mirrors the client's ERP chart through an external code per account. The one thing to get right: the chart is a hierarchy read by type, and what may change after an account has been posted to is limited, so the design must show what is locked and why.

**Fixed on main** (the package already carries these; draw what it says): Filters are typed ids ("Legal entity id") and a type text field. (CHG-SBO-012).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Must a client's chart be importable from a CSV file?** → Drawn default accepted: Draw an "Import" entry point marked later; the contract has no import operation. *(decided by Chinmay, 2026-10-02; DEC-082 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Legal entity | picker: choose an id | optional | — | — | shows names, sends the id | The entity switcher: legal entities by name. | `LegalEntity.id` |
| Account type | radio group | optional | — | Asset · Liability · Equity · Revenue · Expense | — | The five account types in words (asset, liability, equity, revenue, expense). | `Account.type` |
| Is postable | toggle | optional | — | Parent accounts aggregate and cannot be posted to. | — | Sends `?isPostable=` to `listAccounts`. | `listAccounts` ?isPostable |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Legal entity | picker: choose a legal entity | — | — | `listAccounts` ?legalEntityId |
| Type | radio group | — | Asset · Liability · Equity · Revenue · Expense | `listAccounts` ?type |

**Form: Create account** (modal, opened by *Create account*; *Create account* calls `createAccount`, *Cancel* sends nothing)

**Collects what `createAccount` sends before it is called.** Required: `code`, `name`, `type`, `legalEntityId`. Optional: `externalCode`, `parentId`, `isPostable`, `isSuspense`, `subType`, `tags`, `notes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64; pattern `^[A-Za-z0-9._-]+$` | — | — | `createAccount` body |
| External code `externalCode` | text field | optional | — | max length 64 | — | — | `createAccount` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createAccount` body |
| Type `type` | radio group | required | — | Asset · Liability · Equity · Revenue · Expense | — | — | `createAccount` body |
| Parent `parentId` | picker: choose a parent | optional | — | — | shows names, sends the id | — | `createAccount` body |
| Legal entity `legalEntityId` | picker: choose a legal entity | required | — | — | shows names, sends the id | — | `createAccount` body |
| Is postable `isPostable` | toggle | optional | on | — | — | — | `createAccount` body |
| Is suspense `isSuspense` | toggle | optional | off | — | — | See `Account.isSuspense`. | `createAccount` body |
| Sub type `subType` | text field | optional | — | — | — | See `Account.subType`. | `createAccount` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | See `Account.tags`. | `createAccount` body |
| Notes `notes` | text area | optional | — | — | — | See `Account.notes`. | `createAccount` body |

Errors to draw in the form: 400 Validation failed; 409 Code already in use within this legal entity

**Form: Save account** (modal, opened by *Save account*; *Save account* calls `updateAccount`, *Cancel* sends nothing)

**Collects what `updateAccount` sends before it is called.** Nothing in the body is required. Optional: `code`, `name`, `externalCode`, `isActive`, `isSuspense`, `subType`, `tags`, `notes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | optional | — | max length 64; pattern `^[A-Za-z0-9._-]+$` | — | Accepted only while the account has no entries. | `updateAccount` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `updateAccount` body |
| External code `externalCode` | text field | optional | — | max length 64 | — | — | `updateAccount` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateAccount` body |
| Is suspense `isSuspense` | toggle | optional | — | — | — | — | `updateAccount` body |
| Sub type `subType` | text field | optional | — | — | — | — | `updateAccount` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | — | `updateAccount` body |
| Notes `notes` | text area | optional | — | — | — | — | `updateAccount` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `code` sent for an account that already has entries, or a new code already in use within the legal entity.

**Form: Create cost center** (modal, opened by *Create cost center*; *Create cost center* calls `createCostCenter`, *Cancel* sends nothing)

**Collects what `createCostCenter` sends before it is called.** Required: `code`, `name`. Optional: `parentId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createCostCenter` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createCostCenter` body |
| Parent `parentId` | picker: choose a parent | optional | — | — | shows names, sends the id | — | `createCostCenter` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createCostCenter` body |

**Form: Create legal entity** (modal, opened by *Create legal entity*; *Create legal entity* calls `createLegalEntity`, *Cancel* sends nothing)

**Collects what `createLegalEntity` sends before it is called.** Required: `code`, `name`, `countryCode`, `currency`, `currencyScale`, `fiscalYearStartMonth`. Optional: `taxRegistrationNumber`, `regionIds`, `isActive`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets them (readOnly in the contract): `id`, `scopePath` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createLegalEntity` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createLegalEntity` body |
| Country code `countryCode` | text field | required | — | pattern `^[A-Z]{2}$` | — | — | `createLegalEntity` body |
| Currency `currency` | text field | required | — | pattern `^[A-Z]{3}$` | — | — | `createLegalEntity` body |
| Currency scale `currencyScale` | stepper or slider | required | — | min 0; max 4 | — | — | `createLegalEntity` body |
| Tax registration number `taxRegistrationNumber` | text field | optional | — | — | — | — | `createLegalEntity` body |
| Fiscal year start month `fiscalYearStartMonth` | stepper or slider | required | — | min 1; max 12 | — | — | `createLegalEntity` body |
| Regions `regionIds` | multi-picker: choose regions | optional | — | — | — | — | `createLegalEntity` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `createLegalEntity` body |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Account code**: Letters, digits, dot, underscore, hyphen; up to 64 characters; unique within the legal entity. Editable only until the first posting; after that the field is locked with "Posted to: code is fixed". *(source: contracts/spine/finance.yaml#/components/schemas/CreateAccountRequest / contracts/spine/finance.yaml#updateAccount)*
- **Type**: Asset, Liability, Equity, Revenue, Expense (closed list). A finer grouping such as "Deferred revenue – Annual pass" is a sub-type, not a sixth type. Type is fixed from the account's first posting. *(source: contracts/spine/finance.yaml#/components/schemas/AccountType / contracts/spine/finance.yaml#/components/schemas/Account / R127)*
- **Parent account**: Optional; a parent is a header that aggregates and cannot be posted to ("Postable" off). Pick from accounts of the same type in the same legal entity. *(source: DI-262 / contracts/spine/finance.yaml#/components/schemas/Account)*
- **External (ERP) code**: The code in the client's own chart; used on every export so their team sees their codes. The only field that can change on a posted account. *(source: DI-259 / contracts/spine/finance.yaml#updateAccount)*
- **Suspense account flag**: At most one suspense account per legal entity is the working expectation; it catches postings with no mapping and is shown with its balance as a work queue that should trend to zero. *(source: contracts/spine/finance.yaml#/components/schemas/Account)*
- **Legal entity (create)**: Code, name, country, currency, currency decimals (2 or 3), fiscal year start month (January for UAE, April for India), tax registration number. Currency and decimals come from the region the entity trades in and cannot differ from it. *(source: DI-263 / DI-261 / contracts/shared/common.yaml#/components/schemas/Money / ADR-0018)*
- **Cost centre**: Code, name, optional parent and venue; used as a dimension on journal lines (profit centre, outlet). *(source: DI-262 / contracts/spine/finance.yaml#/components/schemas/CostCenter)*

#### Outputs: what the screen shows and produces

**Shown**

**Every account** (data table, from `listAccounts`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| External code | text | Code in the client's own chart. Used on export so their team sees their codes. |
| Sub type | text | 5.7.27. `AccountType` stays a closed enum of asset, liability, equity, revenue and expense because that is correct accounting, and a venue … |
| Notes | text | 5.7.27. Annotations on the account, which an auditor reads before the balance. |
| Name | text | — |
| Type | chip: Asset, Liability, Equity, Revenue, Expense | — |

**Every cost center** (data table, from `listCostCenters`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Parent | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Is active | yes / no (icon or chip) | — |

**Every legal entity** (data table, from `listLegalEntities`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Country code | text | — |
| Currency | text | — |
| Currency scale | 1,234 | — |
| Tax registration number | text | — |

**The selected account** (detail panel, from `getAccount`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| External code | text | Code in the client's own chart. Used on export so their team sees their codes. |
| Sub type | text | 5.7.27. `AccountType` stays a closed enum of asset, liability, equity, revenue and expense because that is correct accounting, and a venue … |
| Tags | list or chips (count when long) | How a venue groups accounts for its own reporting. Free-form, and outside the type. |
| Notes | text | 5.7.27. Annotations on the account, which an auditor reads before the balance. |
| Name | text | — |
| Type | chip: Asset, Liability, Equity, Revenue, Expense | — |
| Balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create account (primary button) | `createAccount` POST `/accounts` | CreateAccountRequest | Account | 400 Validation failed; 409 Code already in use within this legal entity | opens modal first |
| Save account (secondary button) | `updateAccount` PATCH `/accounts/{accountId}` | inline | Account | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `code` sent for an account that already has entries, or a new code already in use within the legal entity. | opens modal first |
| Create cost center (secondary button) | `createCostCenter` POST `/cost-centers` | inline | CostCenter | — | opens modal first |
| Create legal entity (secondary button) | `createLegalEntity` POST `/legal-entities` | LegalEntity | LegalEntity | — | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Chart**: A tree grouped by type in accounting order (Assets, Liabilities, Equity, Revenue, Expenses), each row: code, name, external code, postable, active, balance. Inactive accounts dimmed and filterable, never hidden by default. *(source: DI-262 / contracts/spine/finance.yaml#/components/schemas/Account)*
- **Legal entities**: Every entity with country, currency and active status, as the 12 August walkthrough showed. *(source: DI-261)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Create account / cost centre / legal entity**: Adds the row; the tree opens on it. *(source: contracts/spine/finance.yaml#createAccount)*
- **Deactivate account**: Stops new postings and keeps history; the confirmation names the mappings that point at it, because those postings would go to suspense. *(source: contracts/spine/finance.yaml#updateAccount / contracts/spine/finance.yaml#setAccountMappings)*

**Data it reads**: `listAccounts` (onLoad, List the chart of accounts); `listCostCenters` (onLoad, List cost centres); `listLegalEntities` (onLoad, List legal entities)

**Where the user goes next**

- → `BO-075` Account Mapping: *Maps products to accounts*
- → `BO-077` FX Rates & Variances: *FX Rates & Variances*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The chart accounts list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the chart accounts untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No chart accounts yet. Offers Create account (`createAccount`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on legalEntityId, type, isPostable and the chart accounts are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `LEDGER_VIEW`, which `listAccounts` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCOUNT_CONFIGURE` for `createAccount`, `updateAccount`, `createCostCenter`, `createLegalEntity`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Code already in use within this legal entity; 409 `code` sent for an account that already has entries, or a new code already in use within the legal entity. |

#### Edge cases to draw

- **First run, no chart**: A setup panel ("Create your chart or import your ERP codes") rather than an empty table; selling cannot start until mappings exist. *(source: F16 step 5 / F16 step 6)*
- **Two legal entities in different countries**: The chart is per legal entity; the entity switcher is at the top and each tree shows its own currency. *(source: contracts/spine/finance.yaml#/components/schemas/Account)*

#### Consistency with other screens

- Match `BO-075`: Mappings pick accounts from this chart; an account shown here lists the event types that post to it.
- Match `BO-089`: Journal lines pick postable, active accounts only.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
legalEntity: Aquaventure Leisure LLC · AE · AED · 2 decimals · year starts January · TRN 100123456700003
accounts:
- 1000 Assets (header)
- 1100 Cash on hand – Main Gate · ERP 110010 · balance AED 48,210.00
- 1120 Card clearing – Network International · ERP 110250
- 2300 Deferred revenue – Annual pass · ERP 230010 · balance AED 1,284,600.00
- 2400 VAT payable · ERP 240100
- 4100 Ticket revenue · ERP 410000
- 6900 Cash over/short · ERP 690050
- 9999 Suspense · balance AED 0.00
costCentres:
- CC-FNB-01 Surf Café
- CC-RET-02 Beach Shop
```

#### Permissions

- `listAccounts` → `LEDGER_VIEW` (read) · staff
- `getAccount` → `LEDGER_VIEW` (read) · staff
- `createAccount` → `ACCOUNT_CONFIGURE` (configure) · staff
- `updateAccount` → `ACCOUNT_CONFIGURE` (configure) · staff
- `listCostCenters` → `LEDGER_VIEW` (read) · staff
- `createCostCenter` → `ACCOUNT_CONFIGURE` (configure) · staff
- `listLegalEntities` → `LEDGER_VIEW` (read) · staff
- `createLegalEntity` → `ACCOUNT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `LEDGER_VIEW`, which `listAccounts` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCOUNT_CONFIGURE` for `createAccount`, `updateAccount`, `createCostCenter`, `createLegalEntity`.

#### Requirements it meets

39 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.12.97 | System shall support account type filtering during journal entry creation. | F&B & Guest Management | CONTRACTED | `listAccounts` |
| 5.12.102 | System shall support account lookup and search capabilities. | F&B & Guest Management | CONTRACTED | `listAccounts` |
| 5.7.1 | The system should support entry and maintenance of data in accounts related information tables. The primary usage of this data will be to derive accounts for billing records and interface with the … | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.25 | System shall provide a configurable Chart of Accounts structure. | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.26 | System shall support Asset, Liability, Equity, Revenue, and Expense account types. | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.28 | System shall support account codes, names, and descriptions. | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.32 | System shall provide account search and filtering capabilities. | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.33 | Create and manage General Ledger accounts. | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.34 | Support configurable account numbering structures. | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.36 | Allow account classification by account type. | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.37 | Support account status management (active/inactive). | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.39 | Support account-level descriptions and metadata. | F&B & Guest Management | CONTRACTED | `createAccount` |
| … 27 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Chart of accounts screen: external-system codes for ERP mapping, classification (asset, liability, income, expense), parent-account hierarchy and edit view with financial dimensions (profit centre, cost centres); plus transaction-to-account and payment/offset account mapping. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-262)*
- Chart of accounts can be created natively in TICVAI or mapped to a client's external/ERP chart of accounts. *(agreed · MoM 12 Aug 2026, 13. Chart of Accounts and Account Mapping · DI-259)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-074` · status **notStarted** · provenance generated
- Flow F16 *A venue opens for the first time*, step 5: Finance sets the chart of accounts → **Before the first sale.** Every sale posts somewhere
- Flow F98 *A day is reconciled from takings to the ledger*, step 2: Chart of Accounts. → 6 operations, 6 of them previously unwalked.
- Flow F16 branch at step 5 (abandonsFlow): when No chart of accounts, **Blocks the first sale**, and it is the failure a venue discovers on opening morning rather than in setup.

#### Acceptance for the design

- [ ] Every input above is drawn (35), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-074?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create account, Save account, Create cost center, Create legal entity.
- [ ] Every transition is wired: `BO-075`, `BO-077`.
- [ ] Every gated control is gated: `ACCOUNT_CONFIGURE`, `LEDGER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
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

### In P08 · Orders & Money

- AI-assisted reporting for accountants/finance managers is phase two; phase-one finance screens do not include it. *(agreed · MoM 12 Aug 2026, 6. Finance & Ledger Architecture Overview · DI-278)*
- Financial reports generated automatically: P&L (revenue per category less cost of sales), balance sheet, trial balance and ledger view, cash flow, revenue and deferred-revenue analytics, site-wise revenue; plus daily/weekly/monthly finance summaries. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-276)*
- Legal entities view lists all tenant sites with country, currency and active/inactive status. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-261)*
- Allam: Bulk QR option — for partners with no technical capability, the platform generates a bulk batch of tickets (e.g. 5,000) with a validity window, delivered as QR codes (e.g. CSV) for the partner to import and resell. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-135)*
- Full card numbers are never stored or shown; only a masked representation (e.g. last four digits) so the user can identify which card was used. *(agreed · MoM 31 Jul 2026, 10. Compliance & Data Protection · DI-069)*

**11 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"acceptShiftVariance": {"method":"POST","path":"/shifts/{shiftId}/accept-variance","contract":"shift","summary":"Accept an over/short beyond the threshold","permission":"OVERSHORT_ACCEPT","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"applyManualDiscount": {"method":"POST","path":"/orders/{orderId}/discounts","contract":"orders","summary":"Apply a discount a cashier chose","permission":"ORDER_DISCOUNT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ManualDiscountRequest","responds":"Order"},
"askReportingQuestion": {"method":"POST","path":"/reports/ask","contract":"reporting","summary":"Natural-language reporting query","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"NaturalLanguageAnswer"},
"closeShift": {"method":"POST","path":"/shifts/{shiftId}/close","contract":"shift","summary":"Blind close-out","permission":"SHIFT_CLOSE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CloseShiftRequest","responds":"ShiftCloseResult"},
"createAccount": {"method":"POST","path":"/accounts","contract":"finance","summary":"Create an account","permission":"ACCOUNT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateAccountRequest","responds":"Account"},
"createCashMovement": {"method":"POST","path":"/shifts/{shiftId}/cash-movements","contract":"shift","summary":"Record a cash lift or add","permission":"CASH_LIFT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCashMovementRequest","responds":"CashMovement"},
"createCostCenter": {"method":"POST","path":"/cost-centers","contract":"finance","summary":"Create a cost centre","permission":"ACCOUNT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CostCenter"},
"createDeliveryLocation": {"method":"POST","path":"/delivery-locations","contract":"fnb","summary":"Add a place food can be delivered to","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DeliveryLocation"},
"createLegalEntity": {"method":"POST","path":"/legal-entities","contract":"finance","summary":"Create a legal entity","permission":"ACCOUNT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LegalEntity","responds":"LegalEntity"},
"createMerchandise": {"method":"POST","path":"/merchandise","contract":"retail","summary":"Create a merchandise item","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateMerchandiseRequest","responds":"MerchandiseItem"},
"createOrder": {"method":"POST","path":"/orders","contract":"orders","summary":"Create an order","permission":"ORDER_CREATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateOrderRequest","responds":"Order"},
"createRefund": {"method":"POST","path":"/orders/{orderId}/refunds","contract":"orders","summary":"Refund an order, wholly or in part","permission":"ORDER_REFUND","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateRefundRequest","responds":null},
"createReport": {"method":"POST","path":"/reports","contract":"reporting","summary":"Create a custom report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportRequest","responds":"ReportDefinition"},
"createReportSchedule": {"method":"POST","path":"/report-schedules","contract":"reporting","summary":"Schedule a report","permission":"REPORT_SCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportScheduleRequest","responds":"ReportSchedule"},
"deleteReport": {"method":"DELETE","path":"/reports/{reportId}","contract":"reporting","summary":"Retire a report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"deleteReportSchedule": {"method":"DELETE","path":"/report-schedules/{scheduleId}","contract":"reporting","summary":"Delete a schedule","permission":"REPORT_SCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"exchangeOrderLines": {"method":"POST","path":"/orders/{orderId}/exchanges","contract":"orders","summary":"Exchange lines for different products or dates","permission":"ORDER_EXCHANGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ExchangeOrderRequest","responds":"OrderExchangeResult"},
"getAccount": {"method":"GET","path":"/accounts/{accountId}","contract":"finance","summary":"Read an account","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"Account"},
"getFinancialReport": {"method":"GET","path":"/reports/financial","contract":"finance","summary":"Financial statements, revenue and tax summaries","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"report","in":"query","required":true},{"name":"fiscalPeriodId","in":"query","required":true},{"name":"legalEntityId","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"costCenterId","in":"query","required":null}],"requestBody":null,"responds":"FinancialReport"},
"getOrder": {"method":"GET","path":"/orders/{orderId}","contract":"orders","summary":"Read an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"getOrderStatement": {"method":"GET","path":"/orders/{orderId}/statement","contract":"orders","summary":"Full financial history of an order","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"OrderStatement"},
"getRefundPolicy": {"method":"GET","path":"/venues/{venueId}/refund-policy","contract":"orders","summary":"Read a venue's refund policy","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RefundPolicy"},
"getReport": {"method":"GET","path":"/reports/{reportId}","contract":"reporting","summary":"Read a report definition","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ReportDefinition"},
"getSettlement": {"method":"GET","path":"/settlements/{settlementId}","contract":"finance","summary":"Settlement detail with match results","permission":"SETTLEMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"Settlement"},
"getShift": {"method":"GET","path":"/shifts/{shiftId}","contract":"shift","summary":"Read a shift","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Shift"},
"getShiftCountLines": {"method":"GET","path":"/shifts/{shiftId}/count-lines","contract":"shift","summary":"The denomination breakdown of a shift's counts","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"countKind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getTillShiftPolicy": {"method":"GET","path":"/venues/{venueId}/till-shift-policy","contract":"shift","summary":"The rules every till in the venue opens and closes to","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"TillShiftPolicy"},
"getTrialBalance": {"method":"GET","path":"/ledger/trial-balance","contract":"finance","summary":"Trial balance for a period","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"fiscalPeriodId","in":"query","required":true},{"name":"legalEntityId","in":"query","required":null}],"requestBody":null,"responds":"TrialBalance"},
"getVenueSettings": {"method":"GET","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Operational settings for this venue","permission":"TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"holdOrder": {"method":"POST","path":"/orders/{orderId}/hold","contract":"orders","summary":"Park a sale and free the till","permission":"ORDER_MODIFY","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"ingestSettlementFile": {"method":"POST","path":"/settlements","contract":"finance","summary":"Ingest a provider settlement file","permission":"SETTLEMENT_RECONCILE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listAccounts": {"method":"GET","path":"/accounts","contract":"finance","summary":"List the chart of accounts","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"legalEntityId","in":"query","required":null},{"name":"type","in":"query","required":null},{"name":"isPostable","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCashMovements": {"method":"GET","path":"/shifts/{shiftId}/cash-movements","contract":"shift","summary":"Lifts, adds and the opening float","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCostCenters": {"method":"GET","path":"/cost-centers","contract":"finance","summary":"List cost centres","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDepositBoxes": {"method":"GET","path":"/deposit-boxes","contract":"shift","summary":"Cash boxes and who holds them","permission":"SHIFT_OPEN","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"openOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listLedgerEntries": {"method":"GET","path":"/ledger/entries","contract":"finance","summary":"Query the ledger","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"accountId","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"costCenterId","in":"query","required":null},{"name":"sourceType","in":"query","required":null},{"name":"sourceId","in":"query","required":null},{"name":"postedFrom","in":"query","required":null},{"name":"postedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listLegalEntities": {"method":"GET","path":"/legal-entities","contract":"finance","summary":"List legal entities","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMerchandise": {"method":"GET","path":"/merchandise","contract":"retail","summary":"List merchandise","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"outletId","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"inStockOnly","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrderRefunds": {"method":"GET","path":"/orders/{orderId}/refunds","contract":"orders","summary":"List refunds against an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrders": {"method":"GET","path":"/orders","contract":"orders","summary":"List orders","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"createdFrom","in":"query","required":null},{"name":"createdTo","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":"tender","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOutlets": {"method":"GET","path":"/outlets","contract":"tenancy","summary":"List outlets","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"Outlet"},
"listReportExecutions": {"method":"GET","path":"/report-executions","contract":"reporting","summary":"List executions","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"reportId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"mineOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listReportSchedules": {"method":"GET","path":"/report-schedules","contract":"reporting","summary":"List scheduled reports","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listReports": {"method":"GET","path":"/reports","contract":"reporting","summary":"List available report definitions","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"category","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSettlementExceptions": {"method":"GET","path":"/settlements/{settlementId}/exceptions","contract":"finance","summary":"Unmatched or mismatched settlement lines","permission":"SETTLEMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSettlements": {"method":"GET","path":"/settlements","contract":"finance","summary":"List settlement batches","permission":"SETTLEMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"providerName","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listShifts": {"method":"GET","path":"/shifts","contract":"shift","summary":"List shifts","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"openedFrom","in":"query","required":null},{"name":"openedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"modifyOrder": {"method":"POST","path":"/orders/{orderId}/modify","contract":"orders","summary":"Add or remove lines on an existing order","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ModifyOrderRequest","responds":"OrderModificationResult"},
"rejectShiftVariance": {"method":"POST","path":"/shifts/{shiftId}/reject-variance","contract":"shift","summary":"Send a counted shift back for a recount","permission":"OVERSHORT_ACCEPT","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"reprintOrder": {"method":"POST","path":"/orders/{orderId}/reprints","contract":"orders","summary":"Reprint or resend tickets","permission":"ORDER_REPRINT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"rescheduleOrder": {"method":"POST","path":"/orders/{orderId}/reschedule","contract":"orders","summary":"Move an order to another performance","permission":"ORDER_RESCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderExchangeResult"},
"resolveSettlementException": {"method":"POST","path":"/settlements/{settlementId}/exceptions","contract":"finance","summary":"Resolve a settlement exception","permission":"SETTLEMENT_RECONCILE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SettlementException"},
"resumeOrder": {"method":"POST","path":"/orders/{orderId}/resume","contract":"orders","summary":"Bring a parked sale back to a till","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderResumeResult"},
"runReport": {"method":"POST","path":"/reports/{reportId}/run","contract":"reporting","summary":"Run a report","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RunReportRequest","responds":"ReportResult"},
"saveNaturalLanguageQuery": {"method":"POST","path":"/reports/ask/{conversationId}/save","contract":"reporting","summary":"Save a natural-language answer as a report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReportDefinition"},
"setDeliveryLocationOutletMapping": {"method":"PUT","path":"/venues/{venueId}/delivery-location-outlets","contract":"fnb","summary":"Set which outlets deliver to which delivery locations","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DeliveryLocation"},
"setRefundPolicy": {"method":"PUT","path":"/venues/{venueId}/refund-policy","contract":"orders","summary":"Set a venue's refund policy","permission":"REGION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"RefundPolicy","responds":"RefundPolicy"},
"setTillShiftPolicy": {"method":"PUT","path":"/venues/{venueId}/till-shift-policy","contract":"shift","summary":"Set the rules every till in the venue opens and closes to","permission":"WORKSTATION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TillShiftPolicy","responds":"TillShiftPolicy"},
"setVenueSettings": {"method":"PUT","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Set support hours, quiet hours, segregated access and alerting","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VenueSettings","responds":"VenueSettings"},
"updateAccount": {"method":"PATCH","path":"/accounts/{accountId}","contract":"finance","summary":"Rename, remap or deactivate an account","permission":"ACCOUNT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Account"},
"updateDeliveryLocation": {"method":"PATCH","path":"/delivery-locations/{locationId}","contract":"fnb","summary":"Rename a delivery location, or take it out of service","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DeliveryLocation"},
"updateMerchandise": {"method":"PATCH","path":"/merchandise/{merchandiseId}","contract":"retail","summary":"Amend a merchandise item","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MerchandiseItem"},
"updateReport": {"method":"PUT","path":"/reports/{reportId}","contract":"reporting","summary":"Publish a new version of a definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportRequest","responds":"ReportDefinition"},
"updateReportSchedule": {"method":"PATCH","path":"/report-schedules/{scheduleId}","contract":"reporting","summary":"Amend, pause or resume a schedule","permission":"REPORT_SCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReportSchedule"},
"voidOrder": {"method":"POST","path":"/orders/{orderId}/voids","contract":"orders","summary":"Void an order","permission":"ORDER_VOID","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"withdrawFromDepositBox": {"method":"POST","path":"/deposit-boxes/{boxId}/withdraw","contract":"shift","summary":"A supervisor takes cash out mid-shift","permission":"CASH_LIFT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DepositBox"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Account": {"x-ticvai-persistence":"ledger.account","type":"object","required":["id","code","name","type","legalEntityId","isPostable","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"externalCode":{"type":"string","nullable":true,"description":"Code in the client's own chart. Used on export so their team sees their codes."},"isSuspense":{"type":"boolean","default":false,"description":"5.7.x. **Where a posting with no account mapping goes.** Today it has no destination, and a posting event that cannot be booked is a posting event that is silently dropped.\n**A suspense balance is a work queue, not a resting place.** It should trend to zero, and a balance that grows is the signal that a mapping is missing — which is the whole reason for having one rather than refusing the posting.\n"},"subType":{"type":"string","nullable":true,"description":"5.7.27. **`AccountType` stays a closed enum of asset, liability, equity, revenue and expense because that is correct accounting**, and a venue wanting *Deferred Revenue — Annual Pass* is asking for a sub-type rather than a sixth type.\n"},"tags":{"type":"array","items":{"type":"string"},"description":"How a venue groups accounts for its own reporting. Free-form, and outside the type."},"notes":{"type":"string","nullable":true,"description":"5.7.27. Annotations on the account, which an auditor reads before the balance."},"name":{"type":"string","maxLength":200},"type":{"$ref":"#/components/schemas/AccountType"},"parentId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"isPostable":{"type":"boolean","description":"False for parent accounts, which aggregate only."},"isActive":{"type":"boolean"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"AccountType": {"type":"string","enum":["asset","liability","equity","revenue","expense"]},
"Cadence": {"x-ticvai-persistence":"none — embedded in schedule","type":"object","description":"**What each frequency needs (decided 28 September, audit R158).** `daily`: `timeOfDay`. `weekly`: `dayOfWeek` and `timeOfDay`. `monthly`: `dayOfMonth` and `timeOfDay`, a day past the month's end running on its last day. `quarterly`: `dayOfMonth` and `timeOfDay`, in the first month of each quarter. `onShiftClose` and `onPeriodClose`: nothing else, they run on the event. A field a frequency needs and does not have, or one it does not take, is the 400 on `createReportSchedule`. **Times are in the venue's time zone.**\n","required":["frequency"],"properties":{"frequency":{"type":"string","enum":["daily","weekly","monthly","quarterly","onShiftClose","onPeriodClose"]},"dayOfWeek":{"type":"integer","minimum":0,"maximum":6},"dayOfMonth":{"type":"integer","minimum":1,"maximum":31},"timeOfDay":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$"},"timeZone":{"type":"string","readOnly":true,"description":"Always the venue's time zone (decided 28 September, audit R158), returned so a reader knows which. Not taken on a write."}}},
"CashCountLine": {"x-ticvai-persistence":"orders.cash_count_line","type":"object","description":"**One denomination, counted once, against one shift.** Raised in review on 24 August: the table was a stub.\n**The denomination is referenced rather than described** — `platform.denomination` already holds the note and coin definitions per currency, and a count line that repeats the face value is a count line that can disagree with the till it was counted on.\n**`countedQuantity` is a quantity and `expectedQuantity` is derived**, not stored: the expectation is the opening float plus every movement, and a stored expectation that drifts from the movements is a variance nobody can explain.\n","required":["shiftId","denominationId","countedQuantity"],"properties":{"id":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","description":"A UUIDv7, as `Shift.id` and `orders.pos_shift.id` are."},"depositBoxId":{"type":"string","format":"uuid","nullable":true},"countKind":{"type":"string","enum":["openingFloat","close","movement"],"description":"Which count this line belongs to — the opening float (`openShift`), the close (`closeShift`) or a lift or add (`createCashMovement`). **Until 26 September the three were indistinguishable on one shift** (pull audit R099). Set by the server from the operation that wrote the line.\n"},"cashMovementId":{"type":"string","format":"uuid","nullable":true,"description":"The movement this line counts, where `countKind` is `movement`. How `listCashMovements` rebuilds each movement's `denominations`.\n"},"denominationId":{"type":"string","format":"uuid","description":"References `platform.denomination` — face value, kind and sort order live there."},"countedQuantity":{"type":"integer","minimum":0,"description":"**How many of this note or coin were in the drawer.**"},"countedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"**Quantity times face value, stored.** Derivable, and stored anyway: a denomination revalued or deactivated later would silently rewrite a historical count.\n"},"countedBy":{"type":"string","format":"uuid","nullable":true},"countedAt":{"type":"string","format":"date-time"},"recountOf":{"type":"string","format":"uuid","nullable":true,"description":"**A recount points at what it replaces rather than overwriting it.** `requestRecount` exists because a variance is a question before it is a fact.\n"}}},
"CashMovement": {"x-ticvai-persistence":"orders.cash_movement","allOf":[{"$ref":"#/components/schemas/CreateCashMovementRequest"},{"type":"object","required":["shiftId","authorisedByPrincipalId","sequence"],"properties":{"shiftId":{"type":"string","format":"uuid"},"depositBoxId":{"type":"string","format":"uuid","nullable":true,"description":"The box the cash moved in or out of. Set on every lift `withdrawFromDepositBox` records (26 September, pull audit R099).\n"},"witnessPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The cashier who countersigned a withdrawal. Null on other movements."},"withdrawalReason":{"allOf":[{"$ref":"#/components/schemas/WithdrawalReason"}],"nullable":true},"authorisedByPrincipalId":{"type":"string","format":"uuid","description":"The principal who authorised the movement, recorded for audit."},"sequence":{"type":"integer","description":"Monotonic within the shift. Preserves order across an offline batch."},"syncedAt":{"type":"string","format":"date-time","nullable":true}}}]},
"CashMovementKind": {"type":"string","enum":["openingFloat","lift","add"],"description":"`openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one cashier's box; `add` by `createCashMovement`.\n"},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"CloseShiftRequest": {"type":"object","required":["countedCash","recordedAt"],"properties":{"countedCash":{"type":"array","minItems":1,"description":"**The cashier's blind count, one line per denomination counted** (decided 29 September, readiness close-out; our build plan). The server writes each line as one `CashCountLine` (`countKind` close) against the shift, taking the face value from `platform.denomination`. A denomination may appear once; a repeat is refused with 422 `duplicate-denomination`.\n","items":{"$ref":"#/components/schemas/CountedDenominationLine"}},"nonCashDeclared":{"type":"array","description":"Declared totals per non-cash tender, for reconciliation against captured payments.\n","items":{"type":"object","required":["tender","amount"],"properties":{"tender":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"notes":{"type":"string","maxLength":1000,"description":"The cashier's note on the count. Asked of every cashier on a blind count, never only after a variance is shown (CHG-FIN-003, DI-803).\n"},"cashierReason":{"type":"string","nullable":true,"enum":["tillError","unrecordedRefund","miscount","other"],"description":"Anything the cashier knows went wrong in the shift (DI-803: till error, unrecorded refund, miscount, other). Optional and given without seeing the variance (CHG-FIN-003); the supervisor reads it beside the variance on BO-040.\n"},"releaseHeldLeases":{"type":"boolean","default":true,"description":"Return unsold inventory leases held by this workstation (ADR-0013 C103). Closing without releasing strands capacity until TTL expiry, which is visible at a gate during peak.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"CostCenter": {"x-ticvai-persistence":"ledger.cost_center","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"parentId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"isActive":{"type":"boolean"}}},
"CountedDenominationLine": {"type":"object","x-ticvai-persistence":"none — request only; lands as `CashCountLine` rows","description":"**One line of a cash count as the cashier types it: which note or coin, how many, and what they come to** (decided 29 September, readiness close-out; our build plan). The shape of the blind count on close (`closeShift`) and of the count columns on the till screens (POS-007, POS-011). It is the request side of `CashCountLine`, which is the stored row and adds the shift, the count kind, who counted and when.\n**`total` is shown to the cashier and checked, not trusted**: the server recomputes `count` times the denomination's face value and refuses a line whose `total` disagrees with 422 `count-total-mismatch`. An inactive or unknown denomination is refused with 422 `unknown-denomination`.\n","required":["denominationId","count"],"properties":{"denominationId":{"type":"string","format":"uuid","description":"References `platform.denomination` (`Denomination.id`) — face value, kind and counting order live there."},"count":{"type":"integer","minimum":0,"maximum":100000,"description":"**How many of this note or coin were counted.** Zero is a line, not an omission: a denomination counted and found empty."},"total":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"`count` times the face value, in the denomination's currency. Optional on the way in (the server computes it) and checked when sent.\n"}}},
"CreateAccountRequest": {"type":"object","required":["code","name","type","legalEntityId"],"properties":{"code":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9._-]+$"},"externalCode":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"type":{"$ref":"#/components/schemas/AccountType"},"parentId":{"type":"string","format":"uuid"},"legalEntityId":{"type":"string","format":"uuid"},"isPostable":{"type":"boolean","default":true},"isSuspense":{"type":"boolean","default":false,"description":"See `Account.isSuspense`."},"subType":{"type":"string","nullable":true,"description":"See `Account.subType`."},"tags":{"type":"array","items":{"type":"string"},"description":"See `Account.tags`."},"notes":{"type":"string","nullable":true,"description":"See `Account.notes`."}}},
"CreateCashMovementRequest": {"type":"object","required":["id","kind","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7."},"kind":{"$ref":"#/components/schemas/CashMovementKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"denominations":{"$ref":"#/components/schemas/DenominationCount","x-ticvai-persisted":false,"description":"**Stored as `orders.cash_count_line` rows** with `countKind: movement` and this movement's `cashMovementId`, not as a column. The jsonb blob this used to land in is what `Denomination` was created to replace (26 September, pull audit R099).\n"},"reference":{"type":"string","maxLength":64,"description":"Safe drop reference or bag number."},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateMerchandiseRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["sku","name","outletId","variantId"],"properties":{"sku":{"type":"string","maxLength":64},"barcode":{"type":"string","maxLength":128},"name":{"type":"string","maxLength":200},"description":{"type":"string","description":"What the item is, in the guest's words. Indexed for guest-app search."},"outletId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"inventoryItemId":{"type":"string","format":"uuid"},"isReturnable":{"type":"boolean","default":true},"returnWindowDays":{"type":"integer"},"requiresSerialNumber":{"type":"boolean","default":false},"imageAssetRef":{"type":"string"}}},
"CreateOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","variantId","quantity","quotedUnitPrice"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these."},"variantId":{"type":"string","format":"uuid"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"inventoryHoldId":{"type":"string","nullable":true,"description":"Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"},"description":"Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"quantity":{"type":"integer","minimum":1},"eligibilityDeclaration":{"type":"array","nullable":true,"x-ticvai-note":"One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n","items":{"type":"object","properties":{"ageBand":{"type":"string","enum":["infant","child","junior","adult","senior"],"description":"Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."},"ageYears":{"type":"integer","nullable":true},"heightBandIndex":{"type":"integer","nullable":true},"confidentSwimmer":{"type":"boolean","nullable":true,"description":"**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"},"guardianSigned":{"type":"boolean"}}},"description":"What was declared for each guest on this line, kept as the record staff check at the gate."},"quotedUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the client charged, from its local bundle."},"holderName":{"type":"string","nullable":true},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"}}},
"CreateOrderRequest": {"type":"object","required":["id","venueId","channel","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. Offline replay through `syncOrders` carries no header, and this id alone deduplicates there.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"#/components/schemas/Channel"},"shiftId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null for an anonymous sale. Identity and entitlement are separate."},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells."},"catalogueBundleVersion":{"type":"string","description":"The bundle the client priced from. Lets the server explain a variance rather than merely report one.\n"},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateRefundRequest": {"type":"object","required":["id","amount","reason","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the refund, and its idempotency key — it must equal the `Idempotency-Key` header."},"lineIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Omit to refund the whole order."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reason":{"type":"string","minLength":3,"maxLength":500},"secondaryAuthorisation":{"type":"object","description":"Required above the venue's `requiresSecondUserAbove`. A second user — cashier or supervisor — names themselves. This is dual-authorisation, not escalation.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid"},"credential":{"type":"string","maxLength":512,"description":"The second person's staff PIN, as they sign in at a till with it. **A PIN, never a password** (decided 28 September, audit R123 (7))."}}},"refundToOriginalTender":{"type":"boolean","default":true},"alternateTender":{"$ref":"#/components/schemas/TenderKind"},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","category","dataSource","columns","requiredPermission"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"category":{"$ref":"#/components/schemas/ReportCategory"},"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"parameters":{"type":"array","items":{"$ref":"#/components/schemas/ReportParameter"}},"requiredPermission":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission","description":"Permission needed to run this report, from the shared `Permission` vocabulary. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"},"maxDateRangeDays":{"type":"integer","nullable":true,"minimum":1,"default":366,"description":"Guards against a query spanning years of scan events. **When a report sets none, 366 days applies (decided 28 September, audit R158)**, so `runReport`'s date-range 400 always has a limit."}}},
"CreateReportScheduleRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["reportId","cadence","recipients","format"],"properties":{"reportId":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":200},"cadence":{"$ref":"#/components/schemas/Cadence"},"parameters":{"type":"object","additionalProperties":true,"description":"As `RunReportRequest.parameters` — keyed by the report's `ReportParameter.key`, applied to every run."},"recipients":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/Recipient"}},"format":{"$ref":"#/components/schemas/ExportFormat"},"includePersonalData":{"type":"boolean","default":false},"skipIfEmpty":{"type":"boolean","default":true,"description":"An empty report every morning trains people to ignore the report."}}},
"DataSource": {"type":"string","description":"What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n\n**`forecastPoints` added 29 September** (8.2.55, build pass, group G2): the points of published AI forecast versions; see `x-ticvai-forecast-points`.\n\n**Three accreditation sources added 29 September** (12.1.50, build pass): `accreditationApplications`, `accreditationHolders` and `accreditationCredentials`, over `accreditation.application`, `accreditation.holder` and `accreditation.credential`. They are what the accreditation KPIs and any accreditation report or export (`exportReportResult`, csv or xlsx) are built over. **All three name a person**, and `REPORT_EXPORT_PII` gates them as it gates `guests`.\n","enum":["orders","orderLines","payments","refunds","shifts","scanEvents","entitlements","products","inventory","stockMovements","stockCounts","waste","workstations","devices","principals","loyalty","reviews","queueEntries","guests","campaigns","cases","ledgerEntries","workOrders","approvals","purchaseOrders","receipts","requisitions","stockBatches","resourceBookings","delegations","forms","challenges","wallets","resaleListings","accreditationApplications","accreditationHolders","accreditationCredentials","forecastPoints"],"x-ticvai-forecast-points":"**`forecastPoints` added 29 September (build pass, group G2; 8.2.55)**: one row per forecast point (`ai.forecast_point`) of a **published** forecast version (`ai.forecast_version` status `published`), with the definition it belongs to (`ai.forecast_definition`: subject, grain, unit), the period, the dimension key and the p10, p50 and p90 values. Draft, awaiting-approval and superseded versions are not reachable, and scenario points (`scenarioId` set) only with the scenario named as a filter: **a forecast leaves the platform as the one somebody published**. It is how a forecast is exported (`runReport` then `exportReportResult`, csv or xlsx), scheduled or put on a dashboard. Names no person, so `REPORT_EXPORT` is enough. Read from the reporting replica of the AI log database (design 2.4), never from the model service.\n"},
"DeliveryLocation": {"type":"object","x-ticvai-persistence":"fnb.delivery_location","required":["id","venueId","kind","label","isServiceable"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/DeliveryLocationKind"},"label":{"type":"string","description":"What a runner is told. \"Cabana 12\", \"Row H Seat 4\", \"Lawn — north gate\"."},"zone":{"type":"string","nullable":true},"tableId":{"type":"string","format":"uuid","nullable":true,"description":"Set where the location is a restaurant table, so it shares table state."},"seatId":{"type":"string","nullable":true,"description":"Set where the seat is the address. References the seat map."},"servingOutletIds":{"type":"array","description":"Which outlets deliver here. A cabana served by the pool bar and not the restaurant is normal, and a location nothing serves is not an address.\n","items":{"type":"string","format":"uuid"}},"isServiceable":{"type":"boolean","description":"False where the location exists but is not currently taking delivery — closed section, weather, no runner on shift.\n"},"unserviceableReason":{"type":"string","nullable":true},"walkTimeMinutes":{"type":"integer","nullable":true,"description":"From the serving outlet. Feeds the guest's estimate — a cabana eight minutes away is not the same promise as a table by the kitchen.\n"}}},
"DeliveryLocationKind": {"type":"string","description":"4.6.26. One concept, because a runner needs one instruction.","enum":["table","seat","cabana","sunbed","poolside","box","suite","lawn","collectionPoint","namedLocation"]},
"DenominationCount": {"type":"array","description":"**A count is a list of lines and the line is the row.** Until 24 August this array carried the persistence hint itself, so `orders.cash_count_line` derived a single column — `shift_id` — and a count line had no denomination, no quantity and no variance.\n**The array is the transport; `CashCountLine` is the row.**\n","items":{"$ref":"#/components/schemas/CashCountLine"},"minItems":1},
"DepositBox": {"type":"object","x-ticvai-persistence":"orders.deposit_box + orders.deposit_box_opening_denomination + orders.deposit_box_foreign_holding","description":"5.8. **Allocated to a cashier, not to a workstation.** A cashier moving between tills takes their float with them, which is what makes a variance attributable to a person.\n**`openingDenominations` and `foreignHoldings` are child rows** (26 September, pull audit R099): `orders.deposit_box_opening_denomination` and `orders.deposit_box_foreign_holding`, one row per item, keyed to the box. Until then the contract carried both and the table had nowhere to put either.\n","required":["cashierPrincipalId","venueId","openingFloat"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"cashierPrincipalId":{"type":"string","format":"uuid"},"cashierName":{"type":"string","readOnly":true},"venueId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Where it is being used now. **Changes during a shift; the box does not.**"},"shiftId":{"type":"string","format":"uuid","nullable":true,"description":"The shift trading from this box. A UUIDv7, as `Shift.id` is."},"status":{"$ref":"#/components/schemas/DepositBoxStatus"},"openingFloat":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"openingDenominations":{"type":"array","description":"5.8.3. **Either this or a total** — a supervisor handing over a counted bag should not have to re-count it into fields. POS-001 offered only denominations until 14 August.\n","items":{"type":"object","required":["denominationId","count"],"properties":{"denominationId":{"type":"string","format":"uuid","description":"References `platform.denomination`, as `CashCountLine.denominationId` does. Until 26 September this was `denomination: number` — a face value as a JSON float, which naming-and-style 5.1 forbids and which could disagree with the note it named (pull audit R122).\n"},"count":{"type":"integer","minimum":0}}}},"withdrawnTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"**Reduces the expected close figure.** Cash skimmed for banking is not a shortfall, and a system that treats it as one makes every busy cashier look short.\n"},"overDrawerLimit":{"type":"boolean","readOnly":true,"default":false,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"**The box holds more than its till's drawer limit** (decided 2 October 2026, Chinmay, BO-042; DEC-179; CHG-CSP-016): computed on read from the box's expected cash against `tenancy.Workstation.cashDrawerLimit` or the venue's `cashDrawerLimit`. BO-042 flags the box and offers a lift; false where no limit is set. A flag, not a figure: it tells the cashier nothing about the expected cash (CHG-FIN-003).\n"},"foreignHoldings":{"type":"array","description":"4.6.11 and 6.1.10. **Foreign cash accepted at this till, counted separately by currency.** A till taking USD and EUR alongside AED has three counts and three variances — collapsing them into a base-currency total makes a variance unattributable to the currency that caused it.\n**No opening float in a foreign currency and no change given in one.** Foreign cash only ever comes in, which is what keeps this to one number per currency rather than a full reconciliation each.\n","items":{"type":"object","required":["currency","countedAmount"],"properties":{"currency":{"type":"string","pattern":"^[A-Z]{3}$","description":"**Stored, because it is the one thing that is not the region's.** A foreign holding is by definition cash in a currency the till does not trade in, so it cannot resolve from the region (ADR-0018) the way the box's own amounts do; it is the key of the row, one per currency per box. The amounts on this item are in this currency.\n"},"expectedAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The sum of tenders taken in this currency during the shift."},"countedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"baseEquivalent":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**At the rates on the payments, not today's.** A shift closed on Friday and reviewed on Monday is reviewed at Friday's rates (CF-37).\n"}}}},"expectedTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"countedTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**Flagged where it is not the holder.** A box closed without its holder present is allowed — the cash is counted by somebody, and who counted it is the record.\n"},"allocatedAt":{"type":"string","format":"date-time","description":"When the device recorded the allocation. `allocateDepositBox` is offline-capable, so for a box allocated offline this differs from the server's receipt time.\n"},"closedAt":{"type":"string","format":"date-time","nullable":true}}},
"DepositBoxStatus": {"type":"string","enum":["allocated","open","suspended","closing","closed","reconciled"]},
"ExchangeOrderRequest": {"type":"object","required":["id","outgoingLineIds","incomingLines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header."},"outgoingLineIds":{"type":"array","minItems":1,"items":{"type":"string","format":"uuid"}},"incomingLines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"waiveFee":{"type":"boolean","default":false},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"ExecutionStatus": {"type":"string","enum":["queued","running","completed","failed","cancelled","expired"]},
"ExportFormat": {"type":"string","enum":["csv","xlsx","pdf","json"]},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"FinancialReport": {"x-ticvai-persistence":"none — computed from replica","type":"object","required":["report","fiscalPeriodId","currency","generatedAt","sections"],"properties":{"report":{"$ref":"#/components/schemas/FinancialReportKind"},"fiscalPeriodId":{"type":"string","format":"uuid"},"legalEntityId":{"type":"string","format":"uuid","nullable":true},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer"},"generatedAt":{"type":"string","format":"date-time"},"sections":{"type":"array","items":{"type":"object","required":["name","lines","total"],"properties":{"name":{"type":"string"},"lines":{"type":"array","items":{"type":"object","properties":{"label":{"type":"string"},"accountCode":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"priorPeriodAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The same line for **the same period last year** (decided 28 September, audit R127 (3)). Absent where that period did not exist."}}}},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"FinancialReportKind": {"type":"string","description":"The report `getFinancialReport` returns. One vocabulary for the query and the response.","enum":["profitAndLoss","balanceSheet","cashFlow","revenueByVenue","revenueByProduct","taxSummary"]},
"GeneratedQuery": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n","properties":{"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"compiledSql":{"type":"string","nullable":true,"description":"The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"}}},
"GuestMerchandiseItem": {"x-ticvai-persistence":"none — guest projection of MerchandiseItem","type":"object","description":"**What a guest caller of `listMerchandise` receives.** The fields a shop screen shows and the ids a guest needs to reserve or buy, and nothing else: no inventory link, no catalogue variant, no stock count, no serial-number flag. `additionalProperties: false` is the guarantee: a staff field added to `MerchandiseItem` does not reach a guest by default.\n","additionalProperties":false,"required":["id","name","outletId","price","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"sku":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"outletId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"isAvailable":{"type":"boolean","description":"True when the item is active and in stock at its outlet. An item with no `inventoryItemId` never runs out, so it is available while active.\n"},"isReturnable":{"type":"boolean"},"returnWindowDays":{"type":"integer","nullable":true},"imageAssetRef":{"type":"string","nullable":true}}},
"JournalSource": {"type":"string","enum":["manual","order","refund","void","shift","recognition","settlement","variance","reversal","writeOff","chargeback"]},
"LegalEntity": {"x-ticvai-persistence":"ledger.legal_entity","type":"object","description":"Also the `createLegalEntity` body. **`id` and `scopePath` are server-owned** (`readOnly`) and ignored if sent.\n","required":["id","code","name","countryCode","currency","currencyScale","fiscalYearStartMonth"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"countryCode":{"type":"string","pattern":"^[A-Z]{2}$"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"taxRegistrationNumber":{"type":"string","nullable":true},"fiscalYearStartMonth":{"type":"integer","minimum":1,"maximum":12},"regionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"isActive":{"type":"boolean"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"ManualDiscountRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["id","reason","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of this discount, and its idempotency key — it must equal the `Idempotency-Key` header."},"lineId":{"type":"string","format":"uuid","nullable":true,"description":"Omit to discount the order rather than a line."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"percentage":{"type":"number","minimum":0,"maximum":100},"reason":{"type":"string","minLength":3,"maxLength":300,"description":"Required, and free text rather than a code list. A cashier forced to pick the nearest reason picks the first one, and the register stops meaning anything.\n"},"reasonCode":{"type":"string","nullable":true,"description":"Optional alongside the free text, where the venue maintains a list."},"approverPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Required above the venue threshold. May not be the requester."},"recordedAt":{"type":"string","format":"date-time"}}},
"MerchandiseItem": {"x-ticvai-persistence":"retail.merchandise","type":"object","required":["id","sku","name","outletId","variantId","price","onHand","isActive"],"properties":{"description":{"type":"string","description":"What the item is, in the guest's words. Indexed for guest-app search.\n"},"id":{"type":"string","format":"uuid"},"sku":{"type":"string"},"barcode":{"type":"string","nullable":true},"name":{"type":"string"},"outletId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true},"variantId":{"type":"string","format":"uuid","description":"The catalogue variant sold. Price and tax come from there."},"inventoryItemId":{"type":"string","format":"uuid","nullable":true,"description":"The stock item depleted on sale. Null means the item sells but never runs out, which is almost always a configuration error.\n"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money","x-ticvai-column":"list_price"},"onHand":{"type":"number"},"isReturnable":{"type":"boolean","default":true},"returnWindowDays":{"type":"integer","nullable":true},"requiresSerialNumber":{"type":"boolean","default":false},"imageAssetRef":{"type":"string","nullable":true},"isActive":{"type":"boolean"}}},
"ModifyOrderRequest": {"type":"object","required":["id","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 **of this modification, not of the order** — the order is the path's `orderId`. It is the modification's idempotency key and must equal the `Idempotency-Key` header.\n"},"addLines":{"type":"array","items":{"$ref":"#/components/schemas/CreateOrderLine"}},"removeLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"NaturalLanguageAnswer": {"x-ticvai-persistence":"none — computed","type":"object","required":["conversationId","question","interpretation","result","reliability"],"properties":{"conversationId":{"type":"string"},"question":{"type":"string"},"interpretation":{"type":"string","description":"What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."},"semanticSpec":{"allOf":[{"$ref":"#/components/schemas/ReportingSemanticQuerySpec"}],"nullable":true,"description":"What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"},"generatedQuery":{"allOf":[{"$ref":"#/components/schemas/GeneratedQuery"}],"nullable":true,"description":"The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"},"result":{"allOf":[{"$ref":"#/components/schemas/ReportResult"}],"nullable":true,"description":"Null when the question is outside the semantic model."},"dataAsOf":{"type":"string","format":"date-time","nullable":true,"description":"Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."},"reliability":{"$ref":"#/components/schemas/ReportingAnswerReliability"},"unavailableReason":{"allOf":[{"$ref":"#/components/schemas/ReportingUnavailableReason"}],"nullable":true,"description":"Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."},"confidence":{"type":"number","minimum":0,"maximum":1,"deprecated":true,"description":"Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."},"suggestedFollowUps":{"type":"array","items":{"type":"string"}},"modelVersion":{"type":"string"},"tokensUsed":{"type":"integer"}}},
"OpeningHoursWindow": {"type":"object","description":"26 September, pull audit R088. **One weekly window an outlet is open.** `Outlet.openingHours` was an array of untyped objects. The shape is the one `supportHours.windows` already uses — a day and a from/to — with the times as local `HH:MM` in the region's time zone. Several windows on one day are a split shift, such as lunch and dinner.\n","required":["day","from","to"],"properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet opens."},"to":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","description":"Local time, 24-hour `HH:MM`, when the outlet closes."},"endsNextDay":{"type":"boolean","default":false,"description":"**A late-night window is one window past midnight** (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-731; DEC-197; CHG-CSP-007). A bar open 23:00 to 01:00 on Friday is `day: fri`, `from: '23:00'`, `to: '01:00'`, `endsNextDay: true`: one service period, and its takings belong to Friday's trading day, not split across two days. With `endsNextDay` false, `to` must be later than `from` (`422 window-ends-before-start`); with it true, `to` must be earlier than or equal to `from`, so a window never spans more than 24 hours.\n"}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**The currency the guest selected and is charged in** (CHG-FIN-001, 2 October 2026). Null or equal to `currency` for a sale in the base currency. Everything else on the order, and every ledger posting, stays in the base currency `currency`."},"chargeFxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`), stored on the order so the payment, the receipt, the tax invoice and any refund use the same rate (CHG-FIN-001)."},"chargeFxRateId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `finance.FxRate` row the rate was taken from, for audit."},"chargeTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"`grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to the provider asks for (CHG-FIN-001)."},"chargeRateLockedUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms the new amount (CHG-FIN-001)."},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderExchangeResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["orderId","outgoingValue","incomingValue","difference"],"properties":{"orderId":{"type":"string","format":"uuid"},"outgoingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incomingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"exchangeFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Only the difference settles. The replacement is held before the original is released, never the other way round.\n"},"newLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderModificationResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["order","balanceDue"],"properties":{"order":{"$ref":"#/components/schemas/Order"},"addedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"removedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceDue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Positive means the guest pays; negative means a refund is due."},"refundId":{"type":"string","format":"uuid","nullable":true},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"OrderResumeResult": {"type":"object","x-ticvai-persistence":"none — computed","required":["order","hasChanged"],"properties":{"order":{"$ref":"#/components/schemas/Order"},"hasChanged":{"type":"boolean","description":"True where anything moved while the sale was parked. The cashier decides — silently charging the old price loses money, silently charging the new one loses the guest.\n"},"changes":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["priceChanged","promotionExpired","promotionNowApplies","soldOut","seatHoldExpired","productWithdrawn"]},"lineId":{"type":"string","format":"uuid"},"detail":{"type":"string"},"wasAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"nowAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"OrderStatement": {"x-ticvai-persistence":"none — computed from order, payment, refund and ledger","type":"object","required":["orderId","orderNumber","currency","entries","currentBalance"],"properties":{"orderId":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"entries":{"type":"array","description":"Sequential. What an agent reads to a guest asking about a charge.","items":{"type":"object","required":["kind","amount","runningBalance","occurredAt"],"properties":{"kind":{"type":"string","enum":["sale","payment","refund","void","modification","exchange","fee","variance","chargeback"]},"description":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"runningBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"referenceId":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"occurredAt":{"type":"string","format":"date-time"}}}},"totalPaid":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalRefunded":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"currentBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Positive means the guest owes; negative means a refund is outstanding."}}},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"OrderSummary": {"x-ticvai-persistence":"none — projection","type":"object","required":["id","orderNumber","status","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"The same vocabulary as `Order.channel`, which this projects."},"lineCount":{"type":"integer"},"principalId":{"type":"string","format":"uuid","description":"The cashier who raised it — what the held-orders list shows."},"holdLabel":{"type":"string","nullable":true,"description":"As `Order.holdLabel`."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"description":"As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."},"createdAt":{"type":"string","format":"date-time"}}},
"Outlet": {"type":"object","x-ticvai-persistence":"platform.outlet","required":["id","code","name","venueId","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200,"description":"The outlet's name in English. Other languages are `nameTranslations` (CHG-CSP-005)."},"nameTranslations":{"$ref":"#/components/schemas/OutletNameTranslations"},"venueId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/OutletKind"},"outletType":{"allOf":[{"$ref":"#/components/schemas/OutletType"}],"nullable":true,"description":"The service model (DI-319; DEC-196; CHG-CSP-005). Null on an outlet that is not F&B or retail."},"departmentId":{"type":"string","format":"uuid","nullable":true,"description":"**The department the outlet belongs to** (DI-319: department, sub-department, cost centre and status; DEC-196; CHG-CSP-005): an `OrgUnit` of kind department, as `Workstation.departmentId`. The outlet itself is the sub-department, so it needs no second field.\n"},"zone":{"type":"string","nullable":true},"stockLocationId":{"type":"string","format":"uuid","nullable":true,"description":"Where this outlet draws stock from. A shop and its stockroom are one location; a bar drawing from a central cellar is not.\n"},"costCenterId":{"type":"string","format":"uuid","nullable":true,"description":"Revenue and cost attribution. Outlet is the natural grain for both."},"paymentTiming":{"allOf":[{"$ref":"#/components/schemas/OutletPaymentTiming"}],"default":"sendFirst","description":"Pay first, or send to the kitchen first then pay (DEC-064; CHG-CSP-004)."},"admissionContext":{"allOf":[{"$ref":"#/components/schemas/OutletAdmissionContext"}],"default":"insideVenue","description":"Inside the venue (needs an admission ticket) or standalone (no ticket) (DEC-070; CHG-CSP-004)."},"producesForOutletIds":{"type":"array","default":[],"description":"**One kitchen serving several outlets is a producing outlet** (decided 2 October 2026, Chinmay, batch 6 set 5, BO-134: \"Yes: via a producing outlet (one kitchen outlet produces for several)\"; DEC-188; CHG-CSP-005). The outlets this one prepares food for, in the same venue. The model stays per outlet (DI-330): each outlet keeps its own menu and stations, and an order at a listed outlet may route to this outlet's kitchen stations (fnb `KitchenStation`). Empty on an outlet that only produces for itself. An outlet may not list itself, an outlet of another venue (`422 outlet-not-in-venue`), or one that lists it back.\n","items":{"type":"string","format":"uuid"}},"saleBoardId":{"type":"string","format":"uuid","nullable":true,"description":"**The till layout every till in this outlet uses, unless a till overrides it** (decided 2 October 2026, Chinmay, batch 6 set 4, BO-109: \"Per outlet, with a till override\"; DEC-183; CHG-CSP-006). DI-326 puts the layout at the outlet; MATRIX 2.1.9 binds a board to a workstation. Both hold: a workstation with no board of its own (`ConfigureWorkstationRequest.saleBoardId` absent or null) uses this one, and `Workstation.saleBoardSource` says which applied.\n"},"openingHours":{"type":"array","description":"The weekly pattern, one entry per window. Several windows on a day are allowed.","items":{"$ref":"#/components/schemas/OpeningHoursWindow"}},"isActive":{"type":"boolean"}}},
"OutletAdmissionContext": {"type":"string","description":"**Whether an outlet sits behind the admission gate** (decided 2 October 2026, Chinmay, batch 1, WEB-036: \"Inside the venue, a ticket is needed. A restaurant outside the venue (standalone) can sell without one\"; DEC-070; CHG-CSP-004). `insideVenue` (the default): a guest ordering food needs an admission ticket or a place inside, as DI-292 (14 August) decided. `standalone`: a restaurant outside the gate, which may sell takeaway and delivery (DI-1039) with no ticket. DI-292 is amended for standalone outlets only. The admission check itself stays in Access (ADR-0068). F&B keeps its own payment and its own receipt either way. **The canonical name** (2 October 2026, CHG-CLN-008): the field is `admissionContext` on the outlet and on F&B's guest `DiningOutlet`; common `OutletSiting` and the word \"siting\" are deprecated aliases of this.\n","enum":["insideVenue","standalone"]},
"OutletKind": {"type":"string","enum":["shop","restaurant","bar","cafe","kiosk","gameFloor","ticketOffice","mobile"]},
"OutletNameTranslations": {"type":"object","x-ticvai-persistence":"none — jsonb column on platform.outlet","description":"**The outlet's name in other languages, keyed by ISO 639-1 code** (decided 2 October 2026, Chinmay, batch 2 #26, BO-044: \"Yes, where a country needs it: the local language plus English\"; DEC-031; CHG-CSP-005). `Outlet.name` stays the English name. Where the region requires a local name (`RegionSettings.localLanguageNameLocales`, Arabic in the UAE), creating or amending an outlet without it is refused `422 local-name-required`. The same shape as catalogue's `LocalisedText` (DI-210).\n","additionalProperties":{"type":"string","maxLength":200}},
"OutletPaymentTiming": {"type":"string","description":"**When an F&B order is paid, set per outlet** (Chinmay, 2 October, workbook Q64; refines audit R261 per outlet; CHG-CSA-010). `sendFirst`, the default and R261's rule: the order goes to the kitchen, then the till charges (table service, and quick service where the venue wants the kitchen started while the guest pays). `payFirst`: the till charges before anything reaches the kitchen; an unpaid order at a `payFirst` outlet is never sent (`fnb.createFnbOrder`, `fnb.fireCourse`). Shared because the outlet (tenancy `Outlet`) holds it and F&B enforces it.\n","enum":["sendFirst","payFirst"],"default":"sendFirst"},
"OutletType": {"type":"string","description":"**How an F&B or retail outlet trades, which switches features on or off** (decided 2 October 2026, Chinmay, batch 6 set 6a, BO-729: \"Add both fields: outlet type and department (DI-319)\"; DEC-196; CHG-CSP-005). DI-319: a quick-service outlet needs no table booking, a fine-dining outlet needs a table layout. `kind` stays the physical place (a shop, a restaurant, a kiosk); this is the service model inside it. `commissary` is a producing kitchen (DEC-186, DEC-188).\n","enum":["fineDining","casualDining","quickService","coffeeShop","barLounge","foodCourt","buffet","commissary","retail"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n**Cash at a till only** (CHG-FIN-001, 2 October 2026). A card or wallet payment the guest made in a currency they selected is refunded in that currency (`Refund.tenderCurrency`).\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"Posting": {"x-ticvai-persistence":"ledger.posting","type":"object","required":["id","journalEntryId","accountId","debit","credit","postedAt"],"properties":{"id":{"type":"string"},"journalEntryId":{"type":"string","format":"uuid"},"accountId":{"type":"string","format":"uuid"},"accountCode":{"type":"string"},"debit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"credit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"venueId":{"type":"string","format":"uuid","nullable":true},"costCenterId":{"type":"string","format":"uuid","nullable":true},"source":{"$ref":"#/components/schemas/JournalSource"},"sourceId":{"type":"string","nullable":true},"description":{"type":"string"},"postedAt":{"type":"string","format":"date-time"}}},
"Recipient": {"x-ticvai-persistence":"reporting.schedule_recipient","type":"object","description":"One recipient of a schedule. **A row of `reporting.schedule_recipient`, a child of `reporting.schedule`** — `ReportSchedule` declares the pair, which is what gives the table its `schedule_id`. Pull audit 26 September: declared on its own, the table had no column tying a recipient to its schedule.\n","required":["kind","address"],"properties":{"kind":{"type":"string","enum":["principal","email","sftp","webhook"]},"address":{"type":"string"},"principalId":{"type":"string","format":"uuid"}}},
"Refund": {"x-ticvai-persistence":"orders.refund","type":"object","required":["id","orderId","amount","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"batchId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `RefundBatch` that raised this refund, where `createBulkRefund` did. Null for a refund raised on its own."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"**The rate on the original payment, not today's** (BL-087, CF-118).\n`Payment` records `tenderCurrency`, `fxRate` and `fxRateSource` at the moment of sale, so the sale rate is always retrievable. **Refunding at today's rate repays a different amount of money than was taken** — a guest who paid 100 USD at 3.67 and is refunded at 3.72 gets back more AED than they gave, and the venue carries the difference on every refund.\nThe exposure runs both ways and neither direction is defensible: a guest short-changed by a moving rate has a complaint the venue cannot answer, because **the guest did nothing but wait.**\n"},"taxReversalEntryId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**A refund reverses the tax entry it created, and this is where that is stated rather than implied.** `reverseJournalEntry` and `calculateTax` both exist, so both halves were present and the obligation was assumed — **an implied obligation is one a developer can miss without failing anything.**\nNull only where the original sale carried no tax.\n"},"settleTo":{"type":"string","enum":["originalTender","advanceBalance","wireTransfer","storeCredit"],"default":"originalTender","description":"BL-086. **A refund could only go back the way it came.** A guest whose card has expired, a partner settling by wire, a guest who would rather have the credit — three real cases with one answer.\n**`originalTender` stays the default** because refunding elsewhere is how money laundering works, and anything else needs a reason.\n\n**`storeCredit` is a gift card issued for the refund amount** (decided 2 October 2026, Chinmay, batch 1, POS-011; DEC-061; CHG-CSP-037; DI-796), never a voucher or a wallet top-up.\n"},"fxVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Where the sale rate and the current rate differ, **the difference is booked as an FX variance rather than hidden in the refund**. `runFxRevaluation` already handles this class of movement and this is the same act at a smaller scale.\n"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**A refund goes back in the currency the guest paid** (decided 2 October 2026, Chinmay; CHG-FIN-001). For a card or wallet payment taken in a guest-selected currency, the refund request to the provider is in that currency, and `tenderAmount` is the refunded share of the original `Payment.tenderAmount` at the sale rate (`fxRate`), so a full refund returns exactly what was charged. `amount` stays in base currency for the ledger. Null for a refund in the base currency. Foreign cash refunded at a till is paid in base currency (DI-282)."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The refund in `tenderCurrency`, at that currency's own scale (CHG-FIN-001)."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPercentage":{"type":"number","description":"From the venue's time bands, or an approver override."},"status":{"type":"string","enum":["pendingApproval","pendingGateway","completed","declined","failed"]},"reason":{"type":"string"},"requestedByPrincipalId":{"type":"string","format":"uuid"},"secondaryPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"ledgerEntryId":{"type":"string","format":"uuid","nullable":true,"description":"Written before the gateway is called."},"gatewayReference":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"RefundPolicy": {"x-ticvai-persistence":"orders.refund_policy + orders.refund_policy_time_band","type":"object","description":"Venue-configured. Thresholds are policy, not permission scope — venues run different policies and the permission model should not encode commercial rules.\n**The three thresholds must ascend** (decided 28 September, audit R123 (6)): `selfAuthoriseLimit` <= `requiresSecondUserAbove` <= `requiresApprovalAbove`, where the second is set. `setRefundPolicy` refuses a policy that does not with 422 `refund-thresholds-not-ascending`.\n","required":["venueId","selfAuthoriseLimit","requiresApprovalAbove"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The venue in the path. Not taken from a `setRefundPolicy` body."},"selfAuthoriseLimit":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Up to this, a holder of ORDER_REFUND refunds alone. Zero means every refund needs a second authoriser.\n"},"requiresSecondUserAbove":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Above this, a second user — cashier OR supervisor — names themselves as audit control. Dual-authorisation, not escalation (2.12.3).\n"},"requiresApprovalAbove":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Above this, an ORDER_REFUND_APPROVE holder must approve."},"timeBands":{"type":"array","description":"Refundable percentage by time before the performance. Evaluated most-specific first.\n","items":{"type":"object","required":["hoursBefore","percentage"],"properties":{"hoursBefore":{"type":"integer","minimum":0},"percentage":{"type":"number","minimum":0,"maximum":100}}}},"allowPartial":{"type":"boolean","default":true},"refundWindowDays":{"type":"integer","nullable":true,"minimum":0,"description":"Days after purchase within which a refund may be made. 0 is allowed and means the day of purchase only; null means no window (decided 28 September, audit R123 (6))."},"varianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Price variance above this is an exception requiring review rather than a routine posting (CF-38). Venue-configured.\n**A venue setting with a tenant default** (decided 28 September, audit R094). **Proposed default, client to correct (audit R094): AED 5.00 per order line.**\n"}}},
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
"RunReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","properties":{"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"},"venueId":{"type":"string","format":"uuid","description":"Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"},"dateFrom":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."},"dateTo":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (audit R158)."},"forceAsync":{"type":"boolean","default":false,"description":"Queue regardless of size, for a result to be collected later."}}},
"Settlement": {"x-ticvai-persistence":"ledger.settlement","type":"object","required":["id","providerName","periodStart","periodEnd","status","ingestedAt"],"properties":{"id":{"type":"string","format":"uuid"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","description":"**A settlement has no account, so nothing else denominates it.** A posting takes its currency from `ledger.account.currency` and a payment from `tenderCurrency`, but a settlement is a provider file for a period: `providerGross`, `ledgerGross` and `difference` are bare amounts, and a provider file in one currency against a ledger in another computes a difference that means nothing. Added 20 September, when a venue became able to trade outside its region's currency.\n"},"providerName":{"type":"string"},"venueId":{"type":"string","format":"uuid","description":"The venue this settlement is for. **Reconciled daily per venue** (decided 28 September, audit R110 (b)), so `periodStart` and `periodEnd` are the same day."},"periodStart":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"periodEnd":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"fileReference":{"type":"string","format":"uuid","description":"The `MediaAsset` holding the provider file, as given to `ingestSettlementFile`. **Kept on the row because parsing is asynchronous**: the job that parses the file reads it from here.\n"},"format":{"type":"string","nullable":true,"enum":["csv","fixedWidth","xml","json"],"description":"The file format given at ingest. Null when none was given."},"status":{"$ref":"#/components/schemas/SettlementStatus"},"lineCount":{"type":"integer"},"matchedCount":{"type":"integer"},"exceptionCount":{"type":"integer"},"providerGross":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"providerFees":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"providerNet":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ledgerGross":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ingestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `region` scope.**"}}},
"SettlementException": {"x-ticvai-persistence":"ledger.settlement_exception","type":"object","required":["id","settlementId","kind","providerReference","amount"],"properties":{"id":{"type":"string","format":"uuid","description":"Server-created when parsing finds the exception, so a UUID (naming-and-style 4)."},"settlementId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["unmatchedInProvider","unmatchedInLedger","amountMismatch","duplicateInProvider","feeUnexplained"]},"providerReference":{"type":"string","nullable":true},"paymentId":{"type":"string","format":"uuid","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"expectedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"resolution":{"allOf":[{"$ref":"#/components/schemas/SettlementResolution"}],"nullable":true,"description":"Null while the exception is open."},"note":{"type":"string","nullable":true,"description":"The `note` given to `resolveSettlementException`, stored with the resolution."},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"SettlementResolution": {"type":"string","description":"How a settlement exception was explained. One vocabulary for the request and the stored exception.","enum":["matchedManually","writeOff","disputeRaised","providerError","timingDifference"]},
"SettlementStatus": {"type":"string","enum":["ingesting","parsing","matching","matched","hasExceptions","resolved","failed"]},
"Shift": {"x-ticvai-persistence":"orders.pos_shift + orders.pos_shift_approval + orders.pos_shift_incident","description":"**`approvals` and `incidents` are child rows** (26 September, pull audit R099): `orders.pos_shift_approval` and `orders.pos_shift_incident`, one row per item, keyed to the shift. Until then the contract carried both and `orders.pos_shift` had nowhere to put either.\n","type":"object","required":["id","workstationId","venueId","scopePath","principalId","status","currency","currencyScale","openedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key."},"workstationId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"principalId":{"type":"string","format":"uuid","description":"Who opened it. Cash reconciles to a person and a drawer."},"principalDisplayName":{"type":"string"},"incidents":{"type":"array","description":"BL-097. **A till has exceptions and there was nowhere to write them** — a no-sale, a drawer opened without a transaction, a manager override, a guest dispute.\n**This is the log a cash-up investigation starts from**, and a shift that balances with four unexplained no-sales is not a shift that balanced.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["noSale","drawerOpen","override","voidAfterPayment","guestDispute","tillJam","priceQuery","other"]},"at":{"type":"string","format":"date-time"},"principalId":{"type":"string","format":"uuid"},"note":{"type":"string","nullable":true}}}},"status":{"$ref":"#/components/schemas/ShiftStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"depositBoxCode":{"type":"string","nullable":true},"bagNumber":{"type":"string","nullable":true},"openingFloat":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"salesTotal":{"x-ticvai-column":"gross_sales_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till took in sales, as the guest paid it — tax included: the shift's takings, not Gross sales (CHG-FIN-002, CHG-FIN-010). **Never shown to the shift's own cashier before the count is in** (CHG-FIN-003): with the float and the lifts it gives away the expected cash.\n"},"refundsTotal":{"x-ticvai-column":"gross_refunded_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till paid back, as the guest was refunded it — tax included."},"liftsTotal":{"x-ticvai-column":"lifted_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net."},"expectedCash":{"x-ticvai-column":"expected_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"26 September, pull audit R207. **The figure the blind count was measured against**, revealed once the count is in — null until then. Until this date only `ShiftCloseResult` carried it, returned once by `closeShift`, so BO-040 could not show the over/short it exists to accept. **Null to the shift's own cashier on every read** (CHG-FIN-003, 2 October): returned only to a caller holding OVERSHORT_ACCEPT or SHIFT_CLOSE_OTHER at the venue.\n"},"countedCash":{"x-ticvai-column":"counted_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"What the close count found. Null until the shift is counted."},"variance":{"x-ticvai-column":"variance_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"Counted minus expected, as `ShiftCloseResult.variance`. Negative is short. Null to the shift's own cashier, as `expectedCash` (CHG-FIN-003)."},"cashierReason":{"type":"string","nullable":true,"readOnly":true,"enum":["tillError","unrecordedRefund","miscount","other"],"description":"What the cashier said went wrong, given with the blind count (`CloseShiftRequest.cashierReason`, DI-803) without seeing the variance; the supervisor reads it beside the variance on BO-040 (CHG-FIN-003).\n"},"cashierNote":{"type":"string","nullable":true,"readOnly":true,"maxLength":1000,"description":"The cashier's note with the count (`CloseShiftRequest.notes`; CHG-FIN-003)."},"heldLeaseCount":{"type":"integer","description":"Inventory leases currently held by this workstation. Surfaced so an operator closing a shift can see what will be returned.\n"},"openedAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time","description":"When the device recorded the open. `openedAt` is the server's time."},"suspendedAt":{"type":"string","format":"date-time","nullable":true},"suspendReason":{"type":"string","maxLength":200,"nullable":true,"description":"The `reason` given to `suspendShift`. Cleared on resume."},"closedAt":{"type":"string","format":"date-time","nullable":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who submitted the close count. `reopenShift` refuses an approver who is this principal, and until 26 September there was nothing to compare against (pull audit R099).\n"},"recountRequestedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `rejectShiftVariance`, cleared by the cashier's recount** (decided 2 October 2026, Chinmay; DEC-175; CHG-CSP-013; DI-804). While set, the shift is `pendingVariance` waiting for the cashier rather than the supervisor: the cashier's view says \"Recount requested\" instead of \"Under review\".\n"},"recountRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The supervisor who sent the count back (CHG-CSP-013)."},"recountReason":{"type":"string","nullable":true,"readOnly":true,"maxLength":500,"description":"The supervisor's reason, shown to the cashier; never an amount (CHG-CSP-013, CHG-FIN-003)."},"countNumber":{"type":"integer","minimum":0,"readOnly":true,"description":"How many close counts the shift has had: 0 before the first, 1 after it, 2 after a recount (CHG-CSP-013). The latest is the one measured.\n"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while the shift has unsynced operations."},"approvals":{"type":"array","items":{"type":"object","required":["kind","principalId","at"],"properties":{"kind":{"type":"string","enum":["open","close","variance"],"description":"`open` from `approveShiftOpen`, `close` from `approveShiftClose`, `variance` from `acceptShiftVariance`.\n"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"reason":{"type":"string"}}}}}},
"ShiftCloseResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["shift","expectedCash","countedCash","variance","requiresAcceptance"],"properties":{"shift":{"$ref":"#/components/schemas/Shift"},"expectedCash":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"countedCash":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Counted minus expected. Negative is short."},"requiresAcceptance":{"type":"boolean","description":"True when the variance exceeds the venue's `shiftVarianceThreshold` (audit R094). The shift is then `pendingVariance` and only `acceptShiftVariance` finalises it (audit R080 (e)).\n"},"nonCashVariances":{"type":"array","items":{"type":"object","required":["tender","declared","captured","variance"],"properties":{"tender":{"type":"string"},"declared":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"captured":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"ShiftStatus": {"type":"string","enum":["pendingApproval","open","suspended","pendingVariance","pendingClosure","closed","autoClosed"]},
"SupervisorStepUp": {"type":"object","description":"**A supervisor signs the act in place, on the device making the call** (decided 28 September, audit R144). Used where the decision is a same-device step-up rather than an approval request: reopening a shift, recounting a stock count, a retail return above the venue threshold, and (proposed by the coordinator, client to confirm) closing a stock transfer short and cancelling a performance.\n\n**The verification rule, the same on every operation that takes it:** the server checks `credential` against `principalId`; that principal must hold the operation's `x-ticvai-permission` at the operation's scope, must be active at that venue, and must not be the person whose act is being reversed where the operation says so. Any failure is a `403` (`supervisor-step-up-refused`) and nothing is written. **No approval request is raised**, and the operation declares `x-ticvai-step-up: pin`.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid","description":"The supervisor signing. Recorded against the act."},"credential":{"type":"string","maxLength":512,"writeOnly":true,"description":"The supervisor's staff PIN, as they sign in at a till with it. **A PIN, never a password** (audit R123 (7)). Never stored or returned."}}},
"TenderKind": {"type":"string","description":"`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n","enum":["cash","card","wallet","voucher","bankTransfer","hotelCharge","installment","giftCard","complimentary"]},
"TillShiftPolicy": {"x-ticvai-persistence":"orders.till_shift_policy","type":"object","description":"**The venue's opening, closing and exception rules for every till** (CHG-CSP-020; POS-019; DI-309). One per venue. Proposed defaults are ours, client to correct.\n","required":["venueId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","readOnly":true},"requireOpenApproval":{"type":"boolean","default":false,"description":"Every shift opens `pendingApproval` and waits for `approveShiftOpen` (SHIFT_APPROVE_OPEN). Off by default: only a float outside `openingFloatTolerance` waits.\n"},"openingFloatTolerance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"How far a declared opening float may differ from the box's allocated float before the shift waits for approval (`states/shift.yaml`, pendingApproval). Null: any difference waits.\n"},"depositBoxRequired":{"type":"boolean","default":true,"description":"A shift cannot open without a deposit box (`OpenShiftRequest.depositBoxCode`); refused `400` otherwise."},"bagNumberRequired":{"type":"boolean","default":false,"description":"A shift cannot open without a bag number (`OpenShiftRequest.bagNumber`)."},"requireCloseApproval":{"type":"boolean","default":false,"description":"Every counted shift waits in `pendingClosure` for `approveShiftClose` (SHIFT_APPROVE_CLOSE), even within the variance threshold.\n"},"autoCloseAfterHours":{"type":"integer","nullable":true,"minimum":1,"maximum":48,"default":14,"description":"Hours after which an open or suspended shift nobody closed is closed by the inactivity job as `autoClosed` and the supervisors are told (`states/shift.yaml`). Null never auto-closes.\n"},"noSaleAlertCount":{"type":"integer","nullable":true,"minimum":1,"default":10,"description":"No-sales in one shift (`recordNoSale`) at which the supervisors are alerted on the venue's alerting channel; the count is on POS-020. Null sends no alert.\n"},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"TrialBalance": {"x-ticvai-persistence":"none — computed","type":"object","required":["fiscalPeriodId","isBalanced","totalDebit","totalCredit","accounts"],"properties":{"fiscalPeriodId":{"type":"string","format":"uuid"},"isBalanced":{"type":"boolean","description":"False indicates a defect, not a business condition. Double-entry cannot be unbalanced by legitimate activity.\n"},"totalDebit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCredit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accounts":{"type":"array","items":{"type":"object","required":["accountId","accountCode","accountName","debit","credit","balance"],"properties":{"accountId":{"type":"string","format":"uuid"},"accountCode":{"type":"string"},"accountName":{"type":"string"},"type":{"$ref":"#/components/schemas/AccountType"},"debit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"credit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"},"consentFormId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's own consent form, which every biometric capture is taken on** (decided 2 October 2026, Chinmay, batch 4, BO-188: \"Consent first, on the venue's consent form\"; DEC-128, DEC-549; CHG-CSP-018). A form from the venue's consent-form builder in Venue Management (the one builder Face Pass, Face Tag, marketing and waivers share; marketing-crm `setDigitalWaiverForm`). Turning `isEnabled` on without one is refused `422 consent-form-required`, as a missing DPIA is; each Face Pass and Face Tag capture records the form and its version it was consented on (access `enrolFacePass`, `enrolFaceTag`).\n"},"templatesHeldByTicvai":{"type":"boolean","readOnly":true,"description":"**True where TICVAI's platform stores this venue's biometric templates** (rather than the venue's own on-premises reader estate). Derived from the venue's access deployment. While true, Venue Management shows the venue a standing warning that every guest must accept the venue's consent form before capture, because the data sits with TICVAI as the venue's processor (decided 2 October 2026, Chinmay, batch 4, BO-188: \"If we store the data, highlight or notify the venue that the client must accept a consent form\"; DEC-128; CHG-CSP-018).\n"},"allowMinors":{"type":"boolean","default":true,"description":"**Whether this venue enrols minors at all** (decided 2 October 2026, Chinmay, critical set 1, BO-187 and CMS-029: \"Guardian consent on the venue's form; minor age per country; the venue can switch minors off\"; supersedes the GST-069 default; DEC-237; CHG-CSP-019). On: a minor (below `RegionSettings.minorAgeThreshold`) is enrolled only with a guardian's consent on the venue's consent form. Off: a minor's enrolment is refused (`422 minors-not-enrolled`) and the guest uses another verification method.\n"},"accreditationFaceMatching":{"type":"object","nullable":true,"description":"**Face matching to find duplicate accreditation applicants, off unless the venue enables it** (decided 2 October 2026, Chinmay, critical set 3, BO-631: \"Only where the venue enables it, with applicant consent and the venue's legal sign-off; off by default\"; DEC-461; CHG-CSP-022). Enabling it is refused without `legalSignOffReference` (`422 legal-sign-off-required`); each applicant matched must have consented on the application (accreditation's own record). Null is off.\n","properties":{"isEnabled":{"type":"boolean","default":false},"legalSignOffReference":{"type":"string","nullable":true,"maxLength":200,"description":"The venue's own reference for its legal sign-off; the platform records that one was named, by whom and when."},"signedOffByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"signedOffAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"chargeCurrencies":{"type":"array","nullable":true,"description":"**Which currencies a guest may select and pay in** (decided 2 October 2026, Chinmay; CHG-FIN-001; MoM 10 Aug 2026 4.7 option (b), DI-211). A subset of `displayCurrencies`: each code must also be one the venue's payment provider can charge (`orders.PaymentProvider.presentmentCurrencies`) and one the region holds a `tender` rate for; anything else is refused `400`. Null or empty: guests pay in the trading (base) currency only and the other display currencies stay approximate. The ledger is always in the base currency, with the rate recorded on every payment and refund.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**The most cash a till drawer should hold before some is lifted to the safe** (decided 2 October 2026, Chinmay, batch 6 set 3, BO-042: \"Add drawer limit setting (warn + offer cash lift)\"; DEC-179; CHG-CSP-016; DI-274: on a busy day the cashier unloads excess cash mid-shift and it is reconciled at close). The venue default; a till may set its own (`Workstation.cashDrawerLimit`). When the cash a till has taken since its last count takes the drawer over it, the till warns and offers a cash lift (`shift.createCashMovement` kind `lift`) and BO-042 flags the box (`shift.DepositBox.overDrawerLimit`). A warning, never a block: a sale is not refused because the drawer is full. Null sets no limit. **No proposed default: the client's finance team sets it.**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"tableReservedLeadMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":240,"default":30,"deprecated":true,"description":"**Deprecated (2 October 2026, CHG-CLN-009): `fnb.FnbReservationPolicy.reservedLeadMinutes` is canonical.** The table state model reads the reservation policy (`states/table.yaml`); this venue setting is kept for compatibility, never read, and not drawn. Its former meaning: **How long before a pre-allocated booking its table shows Reserved** (decided 2 October 2026, Chinmay, batch 6 set 6b, EMP-052: \"Reserved when a booking names the table, or N minutes (venue-set) before a pre-allocated booking\"; DEC-202; CHG-CSP-017; DI-689, DI-336). A booking that names its table holds it as Reserved for the booking's whole slot; a booking the host pre-allocated shows its table Reserved from this many minutes before it. Zero shows Reserved only once the booking is due. The fnb table state model applies it (`states/table.yaml`, owned by fnb). Proposed default 30 minutes, client to correct.\n"},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}},
"VoidReason": {"type":"string","description":"**The void reason list** (decided 28 September, audit R125 (4)): the one list `voidOrder` takes, and the list `fnb.amendFnbOrder` and `fnb.cancelFnbOrder` point to. `other` requires a note (audit R222), and the notes are reviewed quarterly to add real reasons. Proposed, client to correct.\n","enum":["guestChangedMind","enteredInError","itemUnavailable","qualityIssue","duplicate","other"]},
"WithdrawalReason": {"type":"string","description":"Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records.","enum":["banking","safeDrop","changeOrder","other"]}
}
```
