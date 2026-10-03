# WS91 — Rental Management board 4

**10 screens · 8 operations · 8 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `RENTAL_OVERRIDE, RENTAL_PRICE, RENTAL_VIEW`. A control nobody can use must say so,
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
| `BO-524` | Rental Pricing Command Center | D | 2 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-525` | Pricing Profile Builder | D | 8 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-526` | Duration & Tiered Pricing Configuration | D | 7 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-527` | Calendar, Peak & Seasonal Pricing | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-528` | Dynamic Pricing & AI Recommendation | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-529` | Deposit & Security Hold Policy | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-530` | Deposit Lifecycle & Settlement Rules | D | 7 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-531` | Late Fee, Grace Period & Extension Pricing | D | 7 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-532` | Commercial Exceptions, Waivers & Overrides | D | 0 | 0 | 6 | 0 | 1 | 4 | — | notStarted (—) |
| `BO-533` | Pricing Simulation, Validation & AI Commercial Intelligence | D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-527, BO-528, BO-529, BO-532, BO-533 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-524` Rental Pricing Command Center

**Central management screen for all rental pricing and commercial policies.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-524 |
| Who uses it | venue staff holding `RENTAL_PRICE`, `RENTAL_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/rental-pricing-command-center-bo-524` |

**From the Food, Beverage & Retail process.** All rental pricing profiles and commercial policies: active profiles, products without pricing, deposit policies, upcoming price changes, approvals pending. The one thing to get right: "products without pricing" is the first thing a manager fixes.

**Known correction pending (do not draw the wrong version)**

- **An "AI Recommendations" tile.** Why: The client limited rental AI to reporting and maintenance recommendations. *(source: DI-772; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search rental pricing | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, location, product, category, pricing model, deposit type and 2 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `listRentalPricingProfiles` ?productId |
| Unpriced only | toggle | — | — | `listRentalPricingProfiles` ?unpricedOnly |

#### Outputs: what the screen shows and produces

**Shown**

**Active Pricing Profiles** (metric tile)

**Products Without Pricing** (metric tile)

**Deposit Policies** (metric tile)

**Dynamic Pricing Enabled** (metric tile)

**Upcoming Price Changes** (metric tile)

**Pricing Exceptions** (metric tile)

**Approval Pending** (metric tile)

**AI Recommendations** (metric tile)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| + Create Pricing Profile (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Profiles**: Name, product, model, base price, channels, effective dates, status (Draft · Pending approval · Active · Scheduled · Expired). *(source: DI-751 / contracts/satellite/rental.yaml#listRentalPricingProfiles)*

**Data it reads**: `listRentalPricingProfiles` (onLoad, Profiles, and products without one)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-525` Pricing Profile Builder: *Pricing Profile Builder*; carries `profileId`
- → `BO-526` Duration & Tiered Pricing Configuration: *Duration & Tiered Pricing Configuration*; carries `profileId`
- → `BO-527` Calendar, Peak & Seasonal Pricing: *Calendar, Peak & Seasonal Pricing*; carries `profileId`
- → `BO-528` Dynamic Pricing & AI Recommendation: *Dynamic Pricing & AI Recommendation*
- → `BO-529` Deposit & Security Hold Policy: *Deposit & Security Hold Policy*
- → `BO-530` Deposit Lifecycle & Settlement Rules: *Deposit Lifecycle & Settlement Rules*
- → `BO-531` Late Fee, Grace Period & Extension Pricing: *Late Fee, Grace Period & Extension Pricing*
- → `BO-532` Commercial Exceptions, Waivers & Overrides: *Commercial Exceptions, Waivers & Overrides*
- → `BO-533` Pricing Simulation, Validation & AI Commercial Intelligence: *Pricing Simulation, Validation & AI Commercial Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental pricing list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental pricing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental pricing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profile: Bicycle standard · City Bicycle · Duration tiers · AED 35 / 30 min · Active from 1 Nov
```

#### Permissions

- `listRentalPricingProfiles` → `RENTAL_VIEW` (read) · staff
- `createRentalPricingProfile` → `RENTAL_PRICE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental pricing: fixed and dynamic models; top-products-by-revenue view; pricing profile valid across a date range, optionally restricted to channels; tiered duration pricing (30/60/90 min at falling per-minute rates); weekday/weekend and peak pricing; demand-based pricing within min/max bounds. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-751)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-524` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-524`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 1: Opens Rental Pricing Command Center → Central management screen for all rental pricing and commercial policies.
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F200 branch at step 1 (expected): when Nothing has been set up on Rental Pricing Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F200 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-524?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: + Create Pricing Profile.
- [ ] Every transition is wired: `BO-100`, `BO-525`, `BO-526`, `BO-527`, `BO-528`, `BO-529`, `BO-530`, `BO-531`, `BO-532`, `BO-533`.
- [ ] Every gated control is gated: `RENTAL_PRICE`, `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-525` Pricing Profile Builder

**Create the master commercial pricing profile associated with a rental product.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-525 |
| Who uses it | venue staff holding `RENTAL_PRICE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/rentals/pricing-profile-builder-bo-525` |

**Known gaps.** **Pricing Profile Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write …

**From the Food, Beverage & Retail process.** Build a pricing profile: model (flat, duration-based, tiered, peak/off-peak, weekend, seasonal, dynamic, hybrid), base price, channel, segment, locations, dates. The one thing to get right: one model picked, then only its fields.

**Known correction pending (do not draw the wrong version)**

- **Each model drawn as a separate select field.** Why: The model is one choice. *(source: screens/P08-venue-back-office.yaml#BO-525; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Flat Rate | select field | — | — | — | — | — | — |
| Duration Based | select field | — | — | — | — | — | — |
| Tiered | select field | — | — | — | — | — | — |
| Peak / Off-Peak | select field | — | — | — | — | — | — |
| Weekend | select field | — | — | — | — | — | — |
| Seasonal | select field | — | — | — | — | — | — |
| Dynamic / AI-Assisted | select field | — | — | — | — | — | — |
| Hybrid | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Model**: One of the eight models; dynamic shows its maximum increase and decrease percentages. *(source: DI-751 / contracts/satellite/rental.yaml#/components/schemas/RentalPricingProfile)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing profile configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing profile configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
profile: Kayak weekend · tiered · AED 90 first hour · channels online and POS · 1 Nov 2026 – 31 Mar 2027
```

#### Permissions

- `createRentalPricingProfile` → `RENTAL_PRICE` (operate) · staff
- `updateRentalPricingProfile` → `RENTAL_PRICE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental pricing: fixed and dynamic models; top-products-by-revenue view; pricing profile valid across a date range, optionally restricted to channels; tiered duration pricing (30/60/90 min at falling per-minute rates); weekday/weekend and peak pricing; demand-based pricing within min/max bounds. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-751)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-525` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-525`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 2: Works in Pricing Profile Builder → Create the master commercial pricing profile associated with a rental product.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-525?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-524`.
- [ ] Every gated control is gated: `RENTAL_PRICE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-526` Duration & Tiered Pricing Configuration

**Configure pricing according to rental duration. This directly implements the fixed and dynamic-duration requirements.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-526 |
| Who uses it | venue staff holding `RENTAL_PRICE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§For customer-defined durations; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/rentals/duration-tiered-pricing-configuration-bo-526` |

**From the Food, Beverage & Retail process.** Duration pricing: tiers (30/60/90 min at falling per-minute rates), minimum charge, billing increment and rounding. The one thing to get right: a worked example price for a sample duration beside the settings.

**Known correction pending (do not draw the wrong version)**

- **Values drawn as labels ("Minimum Charge - AED 40", "Billing Increment - 15 minutes").** Why: Sample values used as labels; fields need labels and inputs. *(source: screens/P08-venue-back-office.yaml#BO-526; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Minimum Charge: AED 40 | text field | — | — | — | — | — | — |
| Billing Increment: 15 minutes | text field | — | — | — | — | — | — |
| Additional Increment: AED 10 | text field | — | — | — | — | — | — |
| Exact usage | select field | — | — | — | — | — | — |
| Round up to 15 minutes | text field | — | — | — | — | — | — |
| Round up to 30 minutes | text field | — | — | — | — | — | — |
| Full next hour | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Tiers and rounding**: Tiers with price; minimum charge; increment; rounding Exact · Up to 15 · Up to 30 · Up to next hour. *(source: DI-751 / contracts/satellite/rental.yaml#/components/schemas/RentalPricingProfile)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The duration tiered pricing configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the duration tiered pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No duration tiered pricing configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
example: Minimum AED 40 · increment 15 min at AED 10 · 75 min rounds up to 90 → AED 80
```

#### Permissions

- `updateRentalPricingProfile` → `RENTAL_PRICE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental pricing: fixed and dynamic models; top-products-by-revenue view; pricing profile valid across a date range, optionally restricted to channels; tiered duration pricing (30/60/90 min at falling per-minute rates); weekday/weekend and peak pricing; demand-based pricing within min/max bounds. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-751)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-526` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-526`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 4: Works in Duration & Tiered Pricing Configuration → Configure pricing according to rental duration. This directly implements the fixed and dynamic-duration requirements.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-526?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-524`.
- [ ] Every gated control is gated: `RENTAL_PRICE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-527` Calendar, Peak & Seasonal Pricing

**Allow price differentiation according to date and time.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-527 |
| Who uses it | venue staff holding `RENTAL_PRICE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/rentals/calendar-peak-seasonal-pricing-bo-527` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Date and time pricing: weekday/weekend, peak hours, seasons, special dates. The one thing to get right: a calendar showing which rule applies on each day.

**Known correction pending (do not draw the wrong version)**

- **Layout is only Save and Cancel.** Why: Nothing to draw. *(source: screens/P08-venue-back-office.yaml#BO-527; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The calendar peak seasonal list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the calendar peak seasonal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No calendar peak seasonal yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the calendar peak seasonal are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules: Weekend +20% · 16:00–18:00 peak +AED 10 · Winter season Nov–Mar
```

#### Permissions

- `updateRentalPricingProfile` → `RENTAL_PRICE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental pricing: fixed and dynamic models; top-products-by-revenue view; pricing profile valid across a date range, optionally restricted to channels; tiered duration pricing (30/60/90 min at falling per-minute rates); weekday/weekend and peak pricing; demand-based pricing within min/max bounds. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-751)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-527` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-527`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 6: Works in Calendar, Peak & Seasonal Pricing → Allow price differentiation according to date and time.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-527?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-524`.
- [ ] Every gated control is gated: `RENTAL_PRICE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-528` Dynamic Pricing & AI Recommendation

**Connect Rental Management to TICVAI's broader Dynamic Pricing capability without duplicating the core Dynamic Pricing module. The original rental requirements explicitly support dynamic pricing (merged into ADM-088 Dynamic Pricing Strategy Command Center).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block B · task VM-BO-528 |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/rentals/dynamic-pricing-ai-recommendation-bo-528` |

**What the spec says about it.** **Merged into ADM-088** (decided 2 October 2026, Chinmay: duplicate screens merged as proposed; CHG-SBO-021). Rental dynamic pricing is the one dynamic pricing strategy list (ADM-088), filtered to rental resources; BO-528 duplicated it with the same list operation. **One implementation, both ids kept**, as the M24-03 merges do: this id stays for traceability and routes to ADM-088, and nothing on it is built separately.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Rental pricing's link into the venue's dynamic pricing strategies rather than a second engine: see the strategies that apply to rental products and activate, pause, resume or retire them.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Activate / Pause / Resume / Retire**: Activate refuses a strategy without a price ladder and at least one rule ("strategy incomplete"); freeze is not offered here (it lives on the guardrails). *(source: contracts/spine/catalogue.yaml#transitionDynamicPricingStrategy)*

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Routes to ADM-088 while it opens. |
| Error (`?state=error`) | Could not open ADM-088; says so and offers to retry. |
| Empty, first run (`?state=emptyFirstRun`) | Never shown: this id routes to ADM-088, whose empty states apply. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: this id routes to ADM-088. |
| Permission denied (`?state=emptyNoAccess`) | As ADM-088: shown when the caller lacks the access ADM-088 requires, named in words. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
strategy:
  code: CABANA-WKND
  name: Cabana weekend demand
  type: demandBased
  scope: 'product: Cabana half day'
  status: active
```

#### Permissions

**A refused user sees:** As ADM-088: shown when the caller lacks the access ADM-088 requires, named in words.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental pricing: fixed and dynamic models; top-products-by-revenue view; pricing profile valid across a date range, optionally restricted to channels; tiered duration pricing (30/60/90 min at falling per-minute rates); weekday/weekend and peak pricing; demand-based pricing within min/max bounds. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-751)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-528` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-528`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 8: Works in Dynamic Pricing & AI Recommendation → Connect Rental Management to TICVAI's broader Dynamic Pricing capability without duplicating the core Dynamic Pricing module. The original rental requirements explicitly support dynamic pricing.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-528?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-524`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-529` Deposit & Security Hold Policy

**Configure financial security required before equipment is released. The original scope supports fixed and percentage deposits and multiple deposit methods.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-529 |
| Who uses it | venue staff holding `RENTAL_PRICE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/deposit-security-hold-policy-bo-529` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** The deposit policy: required or not, fixed, percentage or risk-based, minimum and maximum, and accepted methods (card pre-authorisation, card charge, cash, wallet). The one thing to get right: show the guest-facing result ("AED 200 held on your card, released on return").

**Known correction pending (do not draw the wrong version)**

- **Payment methods drawn as three buttons.** Why: Methods are a multi-select setting. *(source: screens/P08-venue-back-office.yaml#BO-529; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Deposit**: Basis Fixed · Percentage · Risk-based; amount or percentage; min/max; methods allowed. *(source: DI-752 / contracts/satellite/rental.yaml#/components/schemas/RentalDepositPolicy)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Credit Card Pre-Authorization (primary button) | navigation or local | — | — | — | — |
| Card Charge (secondary button) | navigation or local | — | — | — | — |
| Wallet (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The deposit security hold list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the deposit security hold untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No deposit security hold yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the deposit security hold are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy: City Bicycle · AED 200 fixed · card hold or cash · released on return after inspection
```

#### Permissions

- `setRentalDepositPolicy` → `RENTAL_PRICE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Refundable deposit (fixed amount or %), payable by cash or card per business policy; auto-release on return; partial capture (deduct damage charge, refund remainder). *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-752)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-529` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-529`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 10: Works in Deposit & Security Hold Policy → Configure financial security required before equipment is released. The original scope supports fixed and percentage deposits and multiple deposit methods.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-529?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Credit Card Pre-Authorization, Card Charge, Wallet.
- [ ] Every transition is wired: `BO-524`.
- [ ] Every gated control is gated: `RENTAL_PRICE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-530` Deposit Lifecycle & Settlement Rules

**Control what happens to the deposit throughout the rental lifecycle.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-530 |
| Who uses it | venue staff holding `RENTAL_PRICE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/deposit-lifecycle-settlement-rules-bo-530` |

**From the Food, Beverage & Retail process.** What happens to the deposit after return: automatic release, inspection first, release delay, partial capture, supervisor threshold. The one thing to get right: partial capture always releases the remainder to the guest.

**Known correction pending (do not draw the wrong version)**

- **Shares one setter with BO-529, and lists "Refund method" and "Full capture permitted", which the policy has no field for.** Why: Two screens for one record, and fields without data; consolidate. *(source: contracts/satellite/rental.yaml#/components/schemas/RentalDepositPolicy / DI-671; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Automatic release | select field | — | — | — | — | — | — |
| Manual inspection required | select field | — | — | — | — | — | — |
| Supervisor approval threshold | select field | — | — | — | — | — | — |
| Partial capture permitted | select field | — | — | — | — | — | — |
| Full capture permitted | select field | — | — | — | — | — | — |
| Auto-release delay | select field | — | — | — | — | — | — |
| Refund method | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Settlement**: Auto-release yes/no, inspection required, delay hours, partial capture allowed, supervisor approval above an amount. *(source: DI-752 / contracts/satellite/rental.yaml#/components/schemas/RentalDepositPolicy / R127)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The deposit lifecycle settlement configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the deposit lifecycle settlement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No deposit lifecycle settlement configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: Auto-release 0 h after inspection · partial capture allowed · supervisor above AED 150
```

#### Permissions

- `setRentalDepositPolicy` → `RENTAL_PRICE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Refundable deposit (fixed amount or %), payable by cash or card per business policy; auto-release on return; partial capture (deduct damage charge, refund remainder). *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-752)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-530` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-530`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 12: Works in Deposit Lifecycle & Settlement Rules → Control what happens to the deposit throughout the rental lifecycle.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-530?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-524`.
- [ ] Every gated control is gated: `RENTAL_PRICE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-531` Late Fee, Grace Period & Extension Pricing

**Configure the commercial treatment of rentals that extend beyond the original return time. The source explicitly requires automatic late-fee calculation and grace-period configuration.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-531 |
| Who uses it | venue staff holding `RENTAL_PRICE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/late-fee-grace-period-extension-pricing-bo-531` |

**From the Food, Beverage & Retail process.** Late returns and extensions: grace period, late fee basis, tiers, daily cap, extension price, "not returned" after N hours, damage and missing-item fees. The one thing to get right: an example timeline of a late return with its fees.

**Known correction pending (do not draw the wrong version)**

- **Each fee basis drawn as a separate select.** Why: Basis is one choice. *(source: screens/P08-venue-back-office.yaml#BO-531; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Fixed Fee | select field | — | — | — | — | — | — |
| Per Minute | select field | — | — | — | — | — | — |
| Per 15 Minutes | select field | — | — | — | — | — | — |
| Per 30 Minutes | select field | — | — | — | — | — | — |
| Per Hour | select field | — | — | — | — | — | — |
| Tiered | select field | — | — | — | — | — | — |
| Maximum Daily Charge | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Late fee**: Grace minutes; basis Fixed · Per minute · Per 15 · Per 30 · Per hour · Tiered; daily cap. *(source: DI-753 / contracts/satellite/rental.yaml#/components/schemas/RentalFeePolicy)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The late fee grace configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the late fee grace untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No late fee grace configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
example: Grace 10 min · AED 15 per 30 min after · capped AED 150/day · not returned after 6 h
```

#### Permissions

- `setRentalFeePolicy` → `RENTAL_PRICE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Late fee, grace period and extension pricing; fee waiver full or partial (amount or %), e.g. when equipment malfunctioned through no fault of the customer; a simulation tests pricing/deposit rules before publishing. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-753)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-531` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-531`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 14: Works in Late Fee, Grace Period & Extension Pricing → Configure the commercial treatment of rentals that extend beyond the original return time. The source explicitly requires automatic late-fee calculation and grace-period configuration.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-531?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-524`.
- [ ] Every gated control is gated: `RENTAL_PRICE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-532` Commercial Exceptions, Waivers & Overrides

**Control authorized deviations from normal commercial policies.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-532 |
| Who uses it | venue staff holding `RENTAL_OVERRIDE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/commercial-exceptions-waivers-overrides-bo-532` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Food, Beverage & Retail process.** Authorised deviations: price override, complimentary, deposit waiver or reduction, late, damage or extension fee waiver, manual refund, goodwill — each with original and adjusted amount, reason and approver. The one thing to get right: a log of who asked and who approved.

**Known correction pending (do not draw the wrong version)**

- **Primary button has no label and there is no list of overrides.** Why: The screen cannot show history. *(source: screens/P08-venue-back-office.yaml#BO-532; Food, Beverage & Retail)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Override**: Kind, original and adjusted amount (or %), reason; Other needs a note; above threshold goes for approval. *(source: DI-753 / contracts/satellite/rental.yaml#requestRentalCommercialOverride / R222)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial exceptions waivers list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial exceptions waivers untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial exceptions waivers yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial exceptions waivers are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
override: Late fee waiver · AED 45 → 0 · 'brake failure, not guest fault' · requested Priya Nair · approved Omar
  Ziad
```

#### Permissions

- `requestRentalCommercialOverride` → `RENTAL_OVERRIDE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Late fee, grace period and extension pricing; fee waiver full or partial (amount or %), e.g. when equipment malfunctioned through no fault of the customer; a simulation tests pricing/deposit rules before publishing. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-753)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-532` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-532`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 16: Works in Commercial Exceptions, Waivers & Overrides → Control authorized deviations from normal commercial policies.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-532?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-524`.
- [ ] Every gated control is gated: `RENTAL_OVERRIDE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-533` Pricing Simulation, Validation & AI Commercial Intelligence

**Allow administrators to test commercial configuration before publishing it. This is particularly important because rental pricing can involve duration, calendar, location, deposit and dynamic pricing simultaneously.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-533 |
| Who uses it | venue staff holding `RENTAL_PRICE`, `RENTAL_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/pricing-simulation-validation-ai-commercial-intelligence-bo-533` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-008): listCommercialPricing is ticket catalogue pricing, not rental pricing; bulk-attached (R254; design-notes correction fnb-retail BO-533).

**From the Food, Beverage & Retail process.** Test a commercial configuration before publishing: enter product, station, date, duration and channel, see the price and deposit and the rule-by-rule explanation. The one thing to get right: the explanation lists each rule that applied and its amount.

**Fixed on main** (the package already carries these; draw what it says): listCommercialPricing (ticket catalogue pricing) is attached. (CHG-WIR-008).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Food, Beverage & Retail process; these refine the tables above and win where they differ)

- **Simulation**: Price, deposit, and each rule applied with its effect. *(source: DI-753 / contracts/satellite/rental.yaml#simulateRentalPricing / contracts/satellite/rental.yaml#explainRentalPrice)*

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing simulation validation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing simulation validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing simulation validation yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pricing simulation validation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
result: Double Kayak · Sat 2 h · online → base AED 90 + 1 h AED 60 + weekend 20% = AED 180 · deposit AED 300
```

#### Permissions

- `simulateRentalPricing` → `RENTAL_PRICE` (operate) · staff
- `explainRentalPrice` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Late fee, grace period and extension pricing; fee waiver full or partial (amount or %), e.g. when equipment malfunctioned through no fault of the customer; a simulation tests pricing/deposit rules before publishing. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-753)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-533` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-533`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 18: Works in Pricing Simulation, Validation & AI Commercial Intelligence → Allow administrators to test commercial configuration before publishing it. This is particularly important because rental pricing can involve duration, calendar, location, deposit and dynamic pricing …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-533?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-524`.
- [ ] Every gated control is gated: `RENTAL_PRICE`, `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**10 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createRentalPricingProfile": {"method":"POST","path":"/rental-pricing-profiles","contract":"rental","summary":"Define how a rental is priced","permission":"RENTAL_PRICE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalPricingProfile","responds":"RentalPricingProfile"},
"explainRentalPrice": {"method":"POST","path":"/rental-price/explain","contract":"rental","summary":"Why the price is what it is, rule by rule","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalQuoteRequest","responds":"RentalPriceExplanation"},
"listRentalPricingProfiles": {"method":"GET","path":"/rental-pricing-profiles","contract":"rental","summary":"Pricing profiles, and the products with none","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":null},{"name":"unpricedOnly","in":"query","required":null}],"requestBody":null,"responds":"RentalPricingProfile"},
"requestRentalCommercialOverride": {"method":"POST","path":"/rental-overrides","contract":"rental","summary":"Deviate from policy, with a reason and an approver","permission":"RENTAL_OVERRIDE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalOverride","responds":"RentalOverride"},
"setRentalDepositPolicy": {"method":"PUT","path":"/rental-deposit-policies","contract":"rental","summary":"How much is held, how, and what happens to it","permission":"RENTAL_PRICE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalDepositPolicy","responds":"RentalDepositPolicy"},
"setRentalFeePolicy": {"method":"PUT","path":"/rental-fee-policies","contract":"rental","summary":"Grace period, late fees and extension pricing","permission":"RENTAL_PRICE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalFeePolicy","responds":"RentalFeePolicy"},
"simulateRentalPricing": {"method":"POST","path":"/rental-price/simulate","contract":"rental","summary":"Test a commercial configuration before publishing it","permission":"RENTAL_PRICE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalQuoteRequest","responds":null},
"updateRentalPricingProfile": {"method":"PUT","path":"/rental-pricing-profiles/{profileId}","contract":"rental","summary":"Change a pricing profile","permission":"RENTAL_PRICE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalPricingProfile","responds":"RentalPricingProfile"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"RentalConfigurationFinding": {"type":"object","description":"Boards 1.10 and 4.10. **Severity travels with the finding**, so the publish gate can distinguish a missing turnaround buffer from a missing price.\n","properties":{"code":{"type":"string"},"severity":{"type":"string","enum":["blocking","warning","advisory"]},"message":{"type":"string"},"field":{"type":"string","nullable":true},"source":{"type":"string","enum":["validation","ai"],"default":"validation","description":"**AI findings are advisory unless the client configures otherwise** (board 1.10), so the origin is on the record rather than assumed by the reader.\n"}}},
"RentalDepositPolicy": {"type":"object","x-ticvai-persistence":"rental.deposit_policy","description":"Boards 4.6 and 4.7. **Held, not taken**, and settled against an inspection.","properties":{"id":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid","nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"required":{"type":"boolean","default":true},"basis":{"type":"string","enum":["fixed","percentage","riskBased"]},"fixedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"percentage":{"type":"number","nullable":true},"minimumAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"instruments":{"type":"array","items":{"type":"string","enum":["cardPreAuthorisation","cardCharge","cash","wallet"]}},"autoRelease":{"type":"boolean","default":true},"inspectionRequiredBeforeRelease":{"type":"boolean","default":false},"autoReleaseDelayHours":{"type":"integer","default":0},"partialCapturePermitted":{"type":"boolean","default":true},"supervisorApprovalThreshold":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"waiverEligible":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"RentalFeePolicy": {"type":"object","x-ticvai-persistence":"rental.fee_policy","description":"Board 4.8. **Extension is priced below late return on purpose** — *\"this encourages customers to extend properly rather than returning late.\"*\n","properties":{"id":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid","nullable":true},"gracePeriodMinutes":{"type":"integer","default":0},"lateFeeBasis":{"type":"string","enum":["fixed","perMinute","per15Minutes","per30Minutes","perHour","tiered"]},"lateFeeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lateFeeTiers":{"type":"array","items":{"type":"object","properties":{"afterMinutes":{"type":"integer"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"maximumDailyCharge":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"extensionPricePerIncrement":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"extensionIncrementMinutes":{"type":"integer","default":30},"notReturnedAfterHours":{"type":"integer","nullable":true,"description":"**When a late rental becomes a lost one.** The deposit is captured in full and the asset retired; without a threshold the fee accrues forever and nobody decides.\n"},"damageFeeMaximum":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"**A ceiling, not a rate.** Added 22 September: `rental.settlement.damage_fee` was stored with nothing bounding it. **A dent is assessed, not tabulated** — the amount is entered per incident against the actual damage, so the control is how high an operator may go, the same shape `maximumDailyCharge` already gives the late fee.\n"},"damageFeeApprovalAbove":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"**Above this, a second person signs it off.** A damage fee is the one charge on a settlement that a single operator decides alone, and the one a guest is most likely to dispute. The shape is `orders.RefundPolicy.requiresApprovalAbove`, applied to the other direction of money.\n"},"missingItemFeeBasis":{"type":"string","enum":["replacementCost","fixedAmount"],"description":"**What an unreturned item costs.** `replacementCost` reads the item's own replacement value, which is what the fee usually is; `fixedAmount` uses `missingItemFeeAmount`. Added 22 September — `rental.settlement.missing_item_fee` was stored with no source.\n"},"missingItemFeeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Used when `missingItemFeeBasis` is `fixedAmount`."},"scopePath":{"type":"string"}}},
"RentalOverride": {"type":"object","x-ticvai-persistence":"rental.override","description":"Board 4.9. **The original amount is recorded as well as the adjusted one.**","required":["kind","reason"],"properties":{"id":{"type":"string","format":"uuid"},"bookingId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["priceOverride","complimentary","depositWaiver","depositReduction","lateFeeWaiver","damageFeeWaiver","extensionFeeWaiver","manualRefund","goodwill"]},"originalAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"adjustedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reason":{"type":"string"},"requestedBy":{"type":"string","format":"uuid"},"approvedBy":{"type":"string","format":"uuid","nullable":true},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time"},"scopePath":{"type":"string"}}},
"RentalPriceExplanation": {"type":"object","description":"Board 4.10 — *\"show why the price was calculated.\"* **The ordered trace, including the rules that did not apply**, because *\"why is it not the peak price\"* is asked as often as *\"why is it\"*.\n","properties":{"quote":{"$ref":"#/components/schemas/RentalQuote"},"steps":{"type":"array","items":{"type":"object","properties":{"order":{"type":"integer"},"stage":{"type":"string","enum":["basePrice","locationRule","calendarRule","dynamicPricing","channelEligibility","promotion","manualOverride","tax"]},"ruleId":{"type":"string","format":"uuid","nullable":true},"ruleName":{"type":"string","nullable":true},"applied":{"type":"boolean"},"skippedBecause":{"type":"string","nullable":true},"amountBefore":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amountAfter":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"RentalPricingProfile": {"type":"object","x-ticvai-persistence":"rental.pricing_profile","description":"Board 4.2. **Several will apply at once**, and the precedence is configurable and auditable (board 4.10).\n","required":["code","name","model"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"productId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid","nullable":true},"locationIds":{"type":"array","items":{"type":"string","format":"uuid"}},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018). Region-scoped and not overridable below it, so a row in a UAE region is AED and cannot be anything else. Kept on the wire, removed from the table.\n"},"salesChannel":{"type":"string","nullable":true},"customerSegmentId":{"type":"string","format":"uuid","nullable":true},"model":{"type":"string","enum":["flat","durationBased","tiered","peakOffPeak","weekend","seasonal","dynamic","hybrid"]},"basePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"durationTiers":{"type":"array","description":"Board 4.3. *30 min AED 40, 60 min AED 60, 90 min AED 80, 120 min AED 95.*","items":{"type":"object","properties":{"minutes":{"type":"integer"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"minimumCharge":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"billingIncrementMinutes":{"type":"integer","nullable":true},"additionalIncrementPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"rounding":{"type":"string","enum":["exactUsage","roundUp15","roundUp30","roundUpHour"],"default":"exactUsage"},"calendarRules":{"type":"array","description":"Board 4.4. *Peak 16:00–20:00 AED 90/hr; off-peak 09:00–12:00 AED 50/hr; peak season 1 Nov – 31 Mar.*\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["peak","offPeak","weekend","seasonal","special"]},"from":{"type":"string","nullable":true},"to":{"type":"string","nullable":true},"dateFrom":{"type":"string","format":"date","nullable":true},"dateTo":{"type":"string","format":"date","nullable":true},"adjustmentPercent":{"type":"number","nullable":true},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"dynamicEnabled":{"type":"boolean","default":false},"dynamicMaxIncreasePercent":{"type":"number","default":25},"dynamicMaxDecreasePercent":{"type":"number","default":15},"priority":{"type":"integer","default":0},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"status":{"type":"string","enum":["draft","pendingApproval","active","scheduled","expired"]},"scopePath":{"type":"string"}}},
"RentalQuote": {"type":"object","x-ticvai-persistence":"rental.quote","description":"Board 4.10. **Rental amount and deposit are returned apart, because the deposit is not revenue.**\n**A quote `quoteRentalPrice` issues is stored until `expiresAt`**, with what was asked, so the figures it gave can be held to and checked later. `explainRentalPrice` and `simulateRentalPricing` return the same shape and store nothing (decided 29 September, data model DM4).\n**Consumed by `acceptedQuoteId`** on `createRentalBooking` and the extension. A quote is not deleted when it is used or expires: a nightly job removes quotes 30 days past `expiresAt` that no booking references, so a booking can always show the quote it was priced at (decided 29 September, writers pass; DM4).\n","required":["quoteId","productId","from","to","rentalAmount","depositAmount"],"properties":{"quoteId":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid","description":"The request's product; with `locationId`, `from`, `to` and `quantity`, what was quoted."},"locationId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer","default":1},"customerId":{"type":"string","format":"uuid","nullable":true},"rentalAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"addOnAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalPayable":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"depositInstrument":{"type":"string","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005), written at `venue` scope."}}},
"RentalQuoteRequest": {"type":"object","required":["productId","from","to"],"properties":{"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer","default":1},"salesChannel":{"type":"string","nullable":true},"customerId":{"type":"string","format":"uuid","nullable":true},"promotionCode":{"type":"string","nullable":true}}}
}
```
