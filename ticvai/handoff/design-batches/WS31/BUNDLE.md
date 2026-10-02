# WS31 — Order   Reservation Management board 1

**10 screens · 11 operations · 20 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `ORDER_CREATE, ORDER_VIEW`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-304` | Order & Reservation Command Center | B–D | 0 | 46 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-305` | Order Detail & Transaction Workspace | B–D | 0 | 50 | 6 | 12 | 1 | 0 | — | notStarted (generated) |
| `BO-306` | Reservation & Hold Policy Configuration | B–D | 12 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-307` | Order & Reservation Status Lifecycle Configuration | B–D | 8 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-308` | Order Creation & Source/Channel Configuration | B–D | 24 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-309` | Customer, Guest & Account Assignment | B–D | 10 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-310` | Order Line, Product & Entitlement Composition | B–D | 15 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-311` | Capacity Reservation & Inventory Commitment | B–D | 0 | 0 | 6 | 0 | 0 | 4 | — | notStarted (generated) |
| `BO-312` | Reservation Confirmation, Expiry & Fulfillment Readiness | B–D | 9 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-313` | Order Lifecycle Timeline, SLA, Exceptions & AI Operations | B–D | 0 | 4 | 6 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-304, BO-311, BO-313 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-304` Order & Reservation Command Center

**Provide the central operational workspace for searching, monitoring, opening, and managing every order and reservation across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/order-reservation-command-center-bo-304` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Search, monitor and open every order and reservation across channels.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listOrderReservation return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listOrderReservation; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Order number | text field | — | — | `listOrderReservation` ?orderNumber |
| Reservation number | text field | — | — | `listOrderReservation` ?reservationNumber |
| Ticket number | text field | — | — | `listOrderReservation` ?ticketNumber |
| Customer name | text field | — | — | `listOrderReservation` ?customerName |
| Email | text field | — | — | `listOrderReservation` ?email |
| Mobile | phone field | — | — | `listOrderReservation` ?mobile |
| Membership | text field | — | — | `listOrderReservation` ?membershipId |
| Transaction reference | text field | — | — | `listOrderReservation` ?transactionReference |
| Payment reference | text field | — | — | `listOrderReservation` ?paymentReference |
| External partner reference | text field | — | — | `listOrderReservation` ?externalPartnerReference |
| Barcode QR | text field | — | — | `listOrderReservation` ?barcodeQr |
| Event | text field | — | — | `listOrderReservation` ?event |
| Product | text field | — | — | `listOrderReservation` ?product |
| Customer | text field | — | — | `listOrderReservation` ?customer |
| Product event | text field | — | — | `listOrderReservation` ?productEvent |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every order reservation** (data table, from `listOrderReservation`)

| Shows | Format | Notes |
|---|---|---|
| Orders today | text | Orders Today |
| Confirmed orders | 1,234 | Confirmed Orders |
| Active reservations | 1,234 | Active Reservations |
| Temporary holds | 1,234 | Temporary Holds |
| Pending payment | 1,234 | Pending Payment |
| Expiring reservations | 1,234 | Expiring Reservations |
| Failed orders | 1,234 | Failed Orders |
| Partially fulfilled | text | Partially Fulfilled |
| Completed orders | 1,234 | Completed Orders |
| Cancelled orders | 1,234 | Cancelled Orders |
| Orders requiring attention | text | Orders Requiring Attention |
| Gross order value | text | Gross Order Value |
| Order | text | Order ID |
| Reservation | text | Reservation ID |
| Channel | text | Channel |
| Venue | text | Venue |
| Order value | text | Order Value |
| Payment status | 1,234 | Payment Status |
| Reservation status | 1,234 | Reservation Status |
| Fulfillment status | 1,234 | Fulfillment Status |
| Created date | 1 Oct 2026, 14:30 | Created Date |
| Expiry | 1 Oct 2026, 14:30 | Expiry |
| Owner agent | text | Owner/Agent |

**The selected order reservation** (detail panel): The pack groups this record's detail under its own headings: “Search using”.

| Shows | Format | Notes |
|---|---|---|
| Orders today | text | Orders Today |
| Confirmed orders | 1,234 | Confirmed Orders |
| Active reservations | 1,234 | Active Reservations |
| Temporary holds | 1,234 | Temporary Holds |
| Pending payment | 1,234 | Pending Payment |
| Expiring reservations | 1,234 | Expiring Reservations |
| Failed orders | 1,234 | Failed Orders |
| Partially fulfilled | text | Partially Fulfilled |
| Completed orders | 1,234 | Completed Orders |
| Cancelled orders | 1,234 | Cancelled Orders |
| Orders requiring attention | text | Orders Requiring Attention |
| Gross order value | text | Gross Order Value |
| Order | text | Order ID |
| Reservation | text | Reservation ID |
| Channel | text | Channel |
| Venue | text | Venue |
| Order value | text | Order Value |
| Payment status | 1,234 | Payment Status |
| Reservation status | 1,234 | Reservation Status |
| Fulfillment status | 1,234 | Fulfillment Status |
| Created date | 1 Oct 2026, 14:30 | Created Date |
| Expiry | 1 Oct 2026, 14:30 | Expiry |
| Owner agent | text | Owner/Agent |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Open Order, Open Reservation, Extend Hold, Resend Confirmation, Collect Payment, Add Note, View Timeline. Each needs attaching to the control it gates, or the screen needs the control.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **order search**: Search by order number, guest, phone, email, media code; filters for channel, status, date. *(source: contracts/spine/orders.yaml#listOrderReservation / contracts/spine/orders.yaml#listOrders)*

**Data it reads**: `listOrderReservation` (onLoad, Order & Reservation Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-305` Order Detail & Transaction Workspace: *Works in Order Detail & Transaction Workspace*; carries `orderId`; calls `listOrderReservation`
- → `BO-306` Reservation & Hold Policy Configuration: *Works in Reservation & Hold Policy Configuration*; calls `listOrderReservation`
- → `BO-307` Order & Reservation Status Lifecycle Configuration: *Works in Order & Reservation Status Lifecycle Configuration*; calls `listOrderReservation`
- → `BO-308` Order Creation & Source/Channel Configuration: *Works in Order Creation & Source/Channel Configuration*; calls `listOrderReservation`
- → `BO-309` Customer, Guest & Account Assignment: *Works in Customer, Guest & Account Assignment*; calls `listOrderReservation`
- → `BO-310` Order Line, Product & Entitlement Composition: *Works in Order Line, Product & Entitlement Composition*; calls `listOrderReservation`
- → `BO-311` Capacity Reservation & Inventory Commitment: *Works in Capacity Reservation & Inventory Commitment*; calls `listOrderReservation`
- → `BO-312` Reservation Confirmation, Expiry & Fulfillment Readiness: *Works in Reservation Confirmation, Expiry & Fulfillment Readiness*; calls `listOrderReservation`
- → `BO-313` Order Lifecycle Timeline, SLA, Exceptions & AI Operations: *Works in Order Lifecycle Timeline, SLA, Exceptions & AI Operations*; calls `listOrderReservation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order reservation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order reservation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order reservation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the order reservation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
results:
- order: DP-2026-104882
  guest: Mariam Al Suwaidi
  status: Paid
```

#### Permissions

- `listOrderReservation` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Sales team creates bookings for any customer type and sends a confirmation; on arrival the guest presents it to collect physical media or scans directly at access control. Dashboard: today's orders/ reservations, confirmed guests, booking status; order detail shows customer and items. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-611)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-304` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS84 Order   Reservation Management Board 1.dc.html#bo-304`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 1
- Flow F140 *Order Reservation Management board 1: Order & Reservation Command Center*, step 1: Opens Order & Reservation Command Center → Provide the central operational workspace for searching, monitoring, opening, and managing every order and reservation across TICVAI.
- Flow F140 *Order Reservation Management board 1: Order & Reservation Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F140 *Order Reservation Management board 1: Order & Reservation Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F140 *Order Reservation Management board 1: Order & Reservation Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F140 *Order Reservation Management board 1: Order & Reservation Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F140 *Order Reservation Management board 1: Order & Reservation Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F140 *Order Reservation Management board 1: Order & Reservation Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F140 *Order Reservation Management board 1: Order & Reservation Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F140 branch at step 1 (expected): when Nothing has been set up on Order & Reservation Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F140 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (46 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-304?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-305`, `BO-306`, `BO-307`, `BO-308`, `BO-309`, `BO-310`, `BO-311`, `BO-312`, `BO-313`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-305` Order Detail & Transaction Workspace

**Provide the authoritative 360-degree view of a single order. This should become one of the most important operational screens in TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display; Show) and a per-row directory (§Each line should display) — counts over a population, then the population |
| Offline | online only |
| Opens with | `orderId` (navigation) |
| Route | `/orders-money/order-detail-transaction-workspace-bo-305` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-025): The 360 view of one order declared only a write (setOrderDetailTransaction with order number and lines), which would edit lines outside modify, exchange and …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The authoritative 360 view of one order: lines, entitlements, payments, history.

**Fixed on main** (the package already carries these; draw what it says): The 360 view declares only a write (setOrderDetailTransaction with order number and lines). (CHG-WIR-025); No read operation: the screen declares only setOrderDetailTransaction and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Order Number** (metric tile)

**Order Date/Time** (metric tile)

**Order Status** (metric tile)

**Reservation Status** (metric tile)

**Customer** (metric tile)

**Channel** (metric tile)

**Sales Location** (metric tile)

**Cashier/Agent** (metric tile)

**Currency** (metric tile)

**Total** (metric tile)

**Payment Status** (metric tile)

**Fulfillment Status** (metric tile)

**Tickets** (metric tile)

**Reservations** (metric tile)

**Payments** (metric tile)

**Refunds** (metric tile)

**Invoices** (metric tile)

**Credentials** (metric tile)

**Membership** (metric tile)

**Waivers** (metric tile)

**Related Orders** (metric tile)

**Order** (detail panel, from `getOrder`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The client UUIDv7 from `CreateOrderRequest.id`. |
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for … |
| Venue | the name it points at, never the id | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Charge currency | text | The currency the guest selected and is charged in (CHG-FIN-001, 2 October 2026). |
| Charge FX rate | text | Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`) … |
| Charge FX rate | the name it points at, never the id | The `finance.FxRate` row the rate was taken from, for audit. |
| Charge total | AED 1,234.50 | `grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to … |
| Charge rate locked until | 1 Oct 2026, 14:30 | The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms … |
| Dropped promotions | list or chips (count when long) | Promotions left off this order at checkout because their budget cap would have been exceeded (decided 28 September, audit R101 (8)). |
| Promotion | the name it points at, never the id | — |
| Name | text | — |
| Reason | chip: Budget cap reached | — |

**Statement** (detail panel, from `getOrderStatement`)

| Shows | Format | Notes |
|---|---|---|
| Order | the name it points at, never the id | — |
| Order number | text | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Entries | list or chips (count when long) | Sequential. What an agent reads to a guest asking about a charge. |
| Kind | chip: Sale, Payment, Refund, Void, Modification, Exchange… | — |
| Description | text | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Running balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Reference | text | — |
| Principal | the name it points at, never the id | — |
| Occurred at | 1 Oct 2026, 14:30 | — |
| Total paid | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total refunded | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Current balance | AED 1,234.50 | Positive means the guest owes; negative means a refund is outstanding. |

**The selected order detail transaction** (detail panel): The pack groups this record's detail under its own headings: “Order Total”, “Internal Notes”.

| Shows | Format | Notes |
|---|---|---|
| Product | text | Product |
| Ticket type | text | Ticket type |
| Event | text | Event |
| Performance | text | Performance |
| Date | 1 Oct 2026, 14:30 | Date |
| Timeslot | text | Timeslot |
| Quantity | 1,234 | Quantity |
| Person type | text | Person type |
| Seat | text | Seat |
| Unit price | AED 1,234.50 | Unit price |
| Discount | AED 1,234.50 | Discount |
| Tax | AED 1,234.50 | Tax |
| Fee | AED 1,234.50 | Fee |
| Total | 1,234 | Total |
| Ticket status | text | Ticket status |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `getOrder` (onLoad, The order, its lines and its status); `getOrderStatement` (onLoad, The full financial history of the order)

**Where the user goes next**

- → `BO-304` Order & Reservation Command Center: *Returns to the board's landing screen*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order detail transaction list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order detail transaction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order detail transaction yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the order detail transaction are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-022`: Same order view; keep one design.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
order:
  number: DP-2026-104882
```

#### Permissions

- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `getOrderStatement` → `ORDER_VIEW` (read) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.12 | Ticket Viewing - System shall display ticket details. | Guest Mobile App & Branding | CONTRACTED | `getOrder` |
| 2.6.2 | Post-order service 1) On the order details page, users can view the order number, amount, time, payment method, user information, refund/change policies, and the QR code of the e-ticket 2) During the … | Ticketing Sales | CONTRACTED | `getOrder` |
| 2.12.27 | All orders can be finalized for payment registration or modified or even cancelled at the Guest Service or any reservation PC. | Ticketing Sales | CONTRACTED | `getOrder` |
| 5.7.8 | The system should be able to use of a unique Order or Reference number (PNR) for each transaction, which can be communicated to the Payment Gateway, Acquiring Bank and the ERP system for … | F&B & Guest Management | CONTRACTED | `getOrder` |
| 1.6.16 | System shall maintain immutable audit logs for listings, approvals, purchases, ownership transfers, cancellations, and administrative actions. | Ticketing Catalogue | CONTRACTED | `getOrderStatement` |
| 2.7.40 | The system should provide: - Management and display/communication of payments due and balance. - Management of the possibility to cancel or refund an order. - Alerts to B2B clients for credit limit … | Ticketing Sales | CONTRACTED | `getOrderStatement` |
| 2.12.32 | System shall maintain a complete audit history showing all order activities including creation, modifications, upgrades, refunds, cancellations, transfers, communications, redemptions, and user … | Ticketing Sales | CONTRACTED | `getOrderStatement` |
| 5.3.11 | The system should store all information related to a guest's purchase of any offering including purchased tickets, retail items and F&B offerings. | F&B & Guest Management | CONTRACTED | `getOrderStatement` |
| 5.3.12 | The system should store all information related to a guest's ticket usage and redemption. This should include information on all the attractions visited by the guest, with the corresponding number of … | F&B & Guest Management | CONTRACTED | `getOrderStatement` |
| 5.3.27 | Provide complete visit history including dates, attractions visited, duration, purchases, and spending behavior. | F&B & Guest Management | CONTRACTED | `getOrderStatement` |
| 5.5.9 | Maintain a complete history of purchases, transfers, upgrades, refunds, reservations, validations, and consumption. | F&B & Guest Management | CONTRACTED | `getOrderStatement` |
| 5.5.18 | Maintain a complete audit trail for transfers, ownership changes, credit movements, and entitlement assignments. | F&B & Guest Management | CONTRACTED | `getOrderStatement` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Sales team creates bookings for any customer type and sends a confirmation; on arrival the guest presents it to collect physical media or scans directly at access control. Dashboard: today's orders/ reservations, confirmed guests, booking status; order detail shows customer and items. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-611)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-305` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS84 Order   Reservation Management Board 1.dc.html#bo-305`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 1
- Flow F140 *Order Reservation Management board 1: Order & Reservation Command Center*, step 2: Works in Order Detail & Transaction Workspace → Provide the authoritative 360-degree view of a single order. This should become one of the most important operational screens in TICVAI.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (50 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-305?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-304`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-306` Reservation & Hold Policy Configuration

**Configure how TICVAI temporarily reserves inventory before an order is fully confirmed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure by; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/reservation-hold-policy-configuration-bo-306` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the reservation and hold policy that setReservationHoldPolicy writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How long inventory is held before an order is confirmed, per channel and product, and whether holds may be extended and by whom.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setReservationHoldPolicy and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Channel | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Event | select field | — | — | — | — | — | — |
| Performance | select field | — | — | — | — | — | — |
| Ticket Type | select field | — | — | — | — | — | — |
| Customer Segment | select field | — | — | — | — | — | — |
| Reservation Type | select field | — | — | — | — | — | — |
| Extension Allowed | select field | — | — | — | — | — | — |
| Maximum Extensions | select field | — | — | — | — | — | — |
| Extension Duration | select field | — | — | — | — | — | — |
| Authorized Role | select field | — | — | — | — | — | — |
| Approval Requirement | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **hold**: Duration and extensions; the default hold is 15 minutes, between 30 seconds and 1 hour. *(source: contracts/spine/orders.yaml#setReservationHoldPolicy / contracts/spine/catalogue.yaml#acquireInventoryHold)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Cart Hold (primary button) | navigation or local | — | — | — | — |
| Checkout Hold (secondary button) | navigation or local | — | — | — | — |
| Agent Reservation (secondary button) | navigation or local | — | — | — | — |
| Group Reservation (secondary button) | navigation or local | — | — | — | — |
| B2B Reservation (secondary button) | navigation or local | — | — | — | — |
| Corporate Reservation (secondary button) | navigation or local | — | — | — | — |
| Manual Hold (secondary button) | navigation or local | — | — | — | — |
| Payment Hold (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-304` Order & Reservation Command Center: *Returns to the board's landing screen*; calls `setReservationHoldPolicy`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reservation hold policy configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reservation hold policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reservation hold policy configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  channel: Website
  hold: 15 min
  extensions: 1
  extension: 5 min
```

#### Permissions

- `setReservationHoldPolicy` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Booking statuses: draft > reserved (awaiting payment) > completed, with cancelled or expired paths. Hold policy sets how long a capacity booking is held pending payment before release to inventory. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-612)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-306` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS84 Order   Reservation Management Board 1.dc.html#bo-306`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 1
- Flow F140 *Order Reservation Management board 1: Order & Reservation Command Center*, step 4: Works in Reservation & Hold Policy Configuration → Configure how TICVAI temporarily reserves inventory before an order is fully confirmed.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-306?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Cart Hold, Checkout Hold, Agent Reservation, Group Reservation, B2B Reservation, Corporate Reservation, Manual Hold, Payment Hold.
- [ ] Every transition is wired: `BO-304`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-307` Order & Reservation Status Lifecycle Configuration

**Define the governed state machine for orders and reservations. SoftLab should not hard-code status transitions independently in every channel.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§For each transition define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/order-reservation-status-lifecycle-configuration-bo-307` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the order and reservation status configuration that setOrderReservationStatus writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The governed state machine of orders and reservations: allowed transitions, conditions, roles, notifications.

**Known correction pending (do not draw the wrong version)**

- **Configurable transitions contradict the fixed OrderStatus enum that the order operations move along.** Why: A tenant cannot add states the order engine does not know. *(source: contracts/spine/orders.yaml#setOrderReservationStatus / contracts/spine/orders.yaml#voidOrder; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setOrderReservationStatus and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From Status | select field | — | — | — | — | — | — |
| Trigger | select field | — | — | — | — | — | — |
| Required Conditions | select field | — | — | — | — | — | — |
| User/System Action | select field | — | — | — | — | — | — |
| Allowed Role | select field | — | — | — | — | — | — |
| Integration Requirement | select field | — | — | — | — | — | — |
| Notification | select field | — | — | — | — | — | — |
| Audit Requirement | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **state diagram**: States and allowed arrows; system-controlled transitions marked. *(source: contracts/spine/orders.yaml#setOrderReservationStatus)*

**Where the user goes next**

- → `BO-304` Order & Reservation Command Center: *Returns to the board's landing screen*; calls `setOrderReservationStatus`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order reservation status configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order reservation status untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order reservation status configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
transition:
  from: held
  to: paid
  by: system
```

#### Permissions

- `setOrderReservationStatus` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Booking statuses: draft > reserved (awaiting payment) > completed, with cancelled or expired paths. Hold policy sets how long a capacity booking is held pending payment before release to inventory. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-612)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-307` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS84 Order   Reservation Management Board 1.dc.html#bo-307`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 1
- Flow F140 *Order Reservation Management board 1: Order & Reservation Command Center*, step 6: Works in Order & Reservation Status Lifecycle Configuration → Define the governed state machine for orders and reservations. SoftLab should not hard-code status transitions independently in every channel.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-307?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-304`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-308` Order Creation & Source/Channel Configuration

**Configure how orders can originate from different TICVAI sales channels while using one common transaction engine.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture; Configure numbering rules; Configure whether a channel may) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/order-creation-source-channel-configuration-bo-308` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the order source and channel configuration that createOrderSourceChannel writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Where orders come from and what each source captures: sub-channel, location, terminal, agent, partner, campaign, affiliate, external reference.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only createOrderSourceChannel and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Channel | select field | — | — | — | — | — | — |
| Sub-Channel | select field | — | — | — | — | — | — |
| Sales Location | select field | — | — | — | — | — | — |
| Terminal | select field | — | — | — | — | — | — |
| Device | select field | — | — | — | — | — | — |
| Agent | select field | — | — | — | — | — | — |
| Partner | select field | — | — | — | — | — | — |
| Reseller | select field | — | — | — | — | — | — |
| Campaign | select field | — | — | — | — | — | — |
| Affiliate | select field | — | — | — | — | — | — |
| API Consumer | select field | — | — | — | — | — | — |
| External Reference | select field | — | — | — | — | — | — |
| Global Sequence | select field | — | — | — | — | — | — |
| Tenant Sequence | select field | — | — | — | — | — | — |
| Venue Sequence | select field | — | — | — | — | — | — |
| Channel Prefix | select field | — | — | — | — | — | — |
| Year/Month Prefix | select field | — | — | — | — | — | — |
| Custom Pattern | select field | — | — | — | — | — | — |
| Create Reservation | select field | — | — | — | — | — | — |
| Create Immediate Order | select field | — | — | — | — | — | — |
| Create Unpaid Order | select field | — | — | — | — | — | — |
| Create Group Order | select field | — | — | — | — | — | — |
| Hold Inventory | select field | — | — | — | — | — | — |
| Issue Ticket Immediately | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **source**: Source type, then the fields that apply. *(source: contracts/spine/orders.yaml#createOrderSourceChannel)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| OTA Booking Reference (primary button) | navigation or local | — | — | — | — |
| Reseller Order ID (secondary button) | navigation or local | — | — | — | — |
| External CRM Reference (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-304` Order & Reservation Command Center: *Returns to the board's landing screen*; calls `createOrderSourceChannel`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order creation source configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order creation source untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order creation source configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
origin:
  type: mobileFlyingPos
  location: Splash Zone
  holdInventory: true
```

#### Permissions

- `createOrderSourceChannel` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Channel rules govern which actions each channel can perform (create, upgrade, cancel) and whether checkout is guest checkout (name, phone, email only) or full registration/sign-in. Customer category (corporate, travel agent/B2B, school) determines extra information collected. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-613)*
- Sales team creates bookings for any customer type and sends a confirmation; on arrival the guest presents it to collect physical media or scans directly at access control. Dashboard: today's orders/ reservations, confirmed guests, booking status; order detail shows customer and items. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-611)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-308` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS84 Order   Reservation Management Board 1.dc.html#bo-308`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 1
- Flow F140 *Order Reservation Management board 1: Order & Reservation Command Center*, step 8: Works in Order Creation & Source/Channel Configuration → Configure how orders can originate from different TICVAI sales channels while using one common transaction engine.

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-308?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: OTA Booking Reference, Reseller Order ID, External CRM Reference.
- [ ] Every transition is wired: `BO-304`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-309` Customer, Guest & Account Assignment

**Define how customers are identified and associated with orders/reservations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Depending on configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/customer-guest-account-assignment-bo-309` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the customer, guest and account assignment rules that setCustomerGuestAccount writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How a guest or account is attached to an order: identified, anonymous, company, partner, reseller.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setCustomerGuestAccount and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Name | select field | — | — | — | — | — | — |
| Email | select field | — | — | — | — | — | — |
| Mobile | select field | — | — | — | — | — | — |
| Country | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Date of Birth | select field | — | — | — | — | — | — |
| Customer ID | select field | — | — | — | — | — | — |
| Membership ID | select field | — | — | — | — | — | — |
| Company | select field | — | — | — | — | — | — |
| Tax Details | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **identification**: Either email or mobile is enough to identify; anonymous sale allowed where the product permits. *(source: contracts/spine/orders.yaml#setCustomerGuestAccount / TRACKER Actions row 92)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Guest Checkout (primary button) | navigation or local | — | — | — | — |
| Registered Customer (secondary button) | navigation or local | — | — | — | — |
| Anonymous Sale where permitted (secondary button) | navigation or local | — | — | — | — |
| Link Existing (secondary button) | navigation or local | — | — | — | — |
| Continue Guest (secondary button) | navigation or local | — | — | — | — |
| Review Match (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-304` Order & Reservation Command Center: *Returns to the board's landing screen*; calls `setCustomerGuestAccount`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer guest account configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer guest account untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer guest account configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
assignment:
  name: Omar Haddad
  mobile: +971 50 123 4567
  company: null
```

#### Permissions

- `setCustomerGuestAccount` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Channel rules govern which actions each channel can perform (create, upgrade, cancel) and whether checkout is guest checkout (name, phone, email only) or full registration/sign-in. Customer category (corporate, travel agent/B2B, school) determines extra information collected. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-613)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-309` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS84 Order   Reservation Management Board 1.dc.html#bo-309`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 1
- Flow F140 *Order Reservation Management board 1: Order & Reservation Command Center*, step 10: Works in Customer, Guest & Account Assignment → Define how customers are identified and associated with orders/reservations.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-309?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Guest Checkout, Registered Customer, Anonymous Sale where permitted, Link Existing, Continue Guest, Review Match.
- [ ] Every transition is wired: `BO-304`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-310` Order Line, Product & Entitlement Composition

**Manage the products and commercial components contained within an order.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Each line captures) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/order-line-product-entitlement-composition-bo-310` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The products and components in an order and the entitlements each line issues.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listOrderLineProduct return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listOrderLineProduct carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listOrderLineProduct; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Product | select field | — | — | — | — | — | — |
| Variant | select field | — | — | — | — | — | — |
| Quantity | select field | — | — | — | — | — | — |
| Person Type | select field | — | — | — | — | — | — |
| Event | select field | — | — | — | — | — | — |
| Performance | select field | — | — | — | — | — | — |
| Date | select field | — | — | — | — | — | — |
| Timeslot | select field | — | — | — | — | — | — |
| Seat | select field | — | — | — | — | — | — |
| Entitlement | select field | — | — | — | — | — | — |
| Price | select field | — | — | — | — | — | — |
| Discount | select field | — | — | — | — | — | — |
| Tax | select field | — | — | — | — | — | — |
| Fee | select field | — | — | — | — | — | — |
| Fulfillment Method | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **lines**: Each line with its entitlements and their state. *(source: contracts/spine/orders.yaml#listOrderLineProduct)*

**Data it reads**: `listOrderLineProduct` (onLoad, Order Line, Product & Entitlement Composition)

**Where the user goes next**

- → `BO-304` Order & Reservation Command Center: *Returns to the board's landing screen*; calls `listOrderLineProduct`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order line product configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order line product untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order line product configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
line:
  product: Family Fun Bundle
  entitlements:
  - Day Pass x4 issued
  - Lunch x4 issued
```

#### Permissions

- `listOrderLineProduct` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Order lines show all contents (tickets, retail, F&B) with inventory hold/availability; a completeness check confirms payment, customer and capacity before finalising; an at-risk view flags bookings nearing expiry (e.g. payment not completed). *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-614)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-310` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS84 Order   Reservation Management Board 1.dc.html#bo-310`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 1
- Flow F140 *Order Reservation Management board 1: Order & Reservation Command Center*, step 12: Works in Order Line, Product & Entitlement Composition → Manage the products and commercial components contained within an order.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-310?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-304`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-311` Capacity Reservation & Inventory Commitment

**Control when and how order activity consumes real capacity/inventory. This is the transactional bridge between the Order Engine and the Capacity/Inventory Engines.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/capacity-reservation-inventory-commitment-bo-311` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** When orders consume real capacity: at hold, at payment, at confirmation.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listCapacityReservationInventory return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listCapacityReservationInventory; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **commitment points**: Per product kind, when capacity is held, committed and released. *(source: contracts/spine/orders.yaml#listCapacityReservationInventory)*

**Data it reads**: `listCapacityReservationInventory` (onLoad, Capacity Reservation & Inventory Commitment)

**Where the user goes next**

- → `BO-304` Order & Reservation Command Center: *Returns to the board's landing screen*; calls `listCapacityReservationInventory`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The capacity reservation inventory list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the capacity reservation inventory untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No capacity reservation inventory yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the capacity reservation inventory are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  kind: timedAdmission
  hold: at basket
  commit: at payment
  release: hold expiry
```

#### Permissions

- `listCapacityReservationInventory` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-311` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS84 Order   Reservation Management Board 1.dc.html#bo-311`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 1
- Flow F140 *Order Reservation Management board 1: Order & Reservation Command Center*, step 14: Works in Capacity Reservation & Inventory Commitment → Control when and how order activity consumes real capacity/inventory. This is the transactional bridge between the Order Engine and the Capacity/Inventory Engines.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-311?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-304`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-312` Reservation Confirmation, Expiry & Fulfillment Readiness

**Determine when a reservation becomes a confirmed order and when it is ready for ticket/media fulfillment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure combinations of) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/reservation-confirmation-expiry-fulfillment-readiness-bo-312` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** When a reservation becomes a confirmed order and is ready for ticket fulfilment, and when it expires.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listReservationConfirmationExpiry return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listReservationConfirmationExpiry; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Payment Complete | select field | — | — | — | — | — | — |
| Deposit Received | select field | — | — | — | — | — | — |
| Credit Approved | select field | — | — | — | — | — | — |
| Capacity Confirmed | select field | — | — | — | — | — | — |
| Customer Data Complete | select field | — | — | — | — | — | — |
| Required Waiver Complete | select field | — | — | — | — | — | — |
| Required Approval Complete | select field | — | — | — | — | — | — |
| Partner Confirmation Received | select field | — | — | — | — | — | — |
| Example — B2C | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **expiry list**: Reservations expiring soon with countdown. *(source: contracts/spine/orders.yaml#listReservationConfirmationExpiry)*

**Data it reads**: `listReservationConfirmationExpiry` (onLoad, Reservation Confirmation, Expiry & Fulfillment Readiness)

**Where the user goes next**

- → `BO-304` Order & Reservation Command Center: *Returns to the board's landing screen*; calls `listReservationConfirmationExpiry`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reservation confirmation expiry configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reservation confirmation expiry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reservation confirmation expiry configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
reservation:
  ref: RS-2026-3301
  expiresIn: 3 h
  payment: link sent
```

#### Permissions

- `listReservationConfirmationExpiry` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Order lines show all contents (tickets, retail, F&B) with inventory hold/availability; a completeness check confirms payment, customer and capacity before finalising; an at-risk view flags bookings nearing expiry (e.g. payment not completed). *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-614)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-312` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS84 Order   Reservation Management Board 1.dc.html#bo-312`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 1
- Flow F140 *Order Reservation Management board 1: Order & Reservation Command Center*, step 16: Works in Reservation Confirmation, Expiry & Fulfillment Readiness → Determine when a reservation becomes a confirmed order and when it is ready for ticket/media fulfillment.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-312?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-304`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-313` Order Lifecycle Timeline, SLA, Exceptions & AI Operations

**Provide complete lifecycle visibility and proactively identify orders/reservations that require operational intervention.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Detect) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/order-lifecycle-timeline-sla-exceptions-ai-operations-bo-313` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Lifecycle visibility and orders needing intervention: SLA breaches, stuck states, AI-flagged exceptions.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listOrderLifecycleTimeline return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listOrderLifecycleTimeline; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every order lifecycle timeline** (data table, from `listOrderLifecycleTimeline`)

| Shows | Format | Notes |
|---|---|---|
| Exception type | chip: Stuck order, Orphan reservation, Payment order mismatch, Capacity mismatch, Missing … | Exception detected. |
| Duplicate transaction risk | text | not in the schema: `Duplicate Transaction Risk` |

**The selected order lifecycle timeline** (detail panel): The pack groups this record's detail under its own headings: “Prioritize by”, “Depending on exception”, “Order & Reservation Command Center”, “Transaction state machine”, “Omnichannel order creation”, “Customer, Guest & Account Assignment”.

| Shows | Format | Notes |
|---|---|---|
| Exception type | chip: Stuck order, Orphan reservation, Payment order mismatch, Capacity mismatch, Missing … | Exception detected. |
| Duplicate transaction risk | text | not in the schema: `Duplicate Transaction Risk` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **exception list**: Order, issue, age, SLA status. *(source: contracts/spine/orders.yaml#listOrderLifecycleTimeline)*

**Data it reads**: `listOrderLifecycleTimeline` (onLoad, Order Lifecycle Timeline, SLA, Exceptions & AI Operations)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order lifecycle timeline list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order lifecycle timeline untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order lifecycle timeline yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the order lifecycle timeline are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
exception:
  order: DP-2026-104990
  issue: Paid, tickets not issued
  age: 42 min
```

#### Permissions

- `listOrderLifecycleTimeline` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Order lines show all contents (tickets, retail, F&B) with inventory hold/availability; a completeness check confirms payment, customer and capacity before finalising; an at-risk view flags bookings nearing expiry (e.g. payment not completed). *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-614)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-313` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS84 Order   Reservation Management Board 1.dc.html#bo-313`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 1
- Flow F140 *Order Reservation Management board 1: Order & Reservation Command Center*, step 18: Works in Order Lifecycle Timeline, SLA, Exceptions & AI Operations → Provide complete lifecycle visibility and proactively identify orders/reservations that require operational intervention.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-313?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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
"createOrderSourceChannel": {"method":"POST","path":"/order-source-channel","contract":"orders","summary":"Order Creation & Source/Channel Configuration","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OrderCreationSourceChannelConfigurationInput","responds":"OrderCreationSourceChannelConfigurationView"},
"getOrder": {"method":"GET","path":"/orders/{orderId}","contract":"orders","summary":"Read an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"getOrderStatement": {"method":"GET","path":"/orders/{orderId}/statement","contract":"orders","summary":"Full financial history of an order","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"OrderStatement"},
"listCapacityReservationInventory": {"method":"GET","path":"/capacity-reservation-inventory","contract":"orders","summary":"Capacity Reservation & Inventory Commitment","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CapacityReservationInventoryCommitmentView"},
"listOrderLifecycleTimeline": {"method":"GET","path":"/order-lifecycle-timeline","contract":"orders","summary":"Order Lifecycle Timeline, SLA, Exceptions & AI Operations","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderLifecycleTimelineSlaExceptionsAiOperationsView"},
"listOrderLineProduct": {"method":"GET","path":"/order-line-product","contract":"orders","summary":"Order Line, Product & Entitlement Composition","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderLineProductEntitlementCompositionView"},
"listOrderReservation": {"method":"GET","path":"/order-reservation","contract":"orders","summary":"Order & Reservation Command Center","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"orderNumber","in":"query","required":false},{"name":"reservationNumber","in":"query","required":false},{"name":"ticketNumber","in":"query","required":false},{"name":"customerName","in":"query","required":false},{"name":"email","in":"query","required":false},{"name":"mobile","in":"query","required":false},{"name":"membershipId","in":"query","required":false},{"name":"transactionReference","in":"query","required":false},{"name":"paymentReference","in":"query","required":false},{"name":"externalPartnerReference","in":"query","required":false},{"name":"barcodeQr","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"customer","in":"query","required":false},{"name":"productEvent","in":"query","required":false}],"requestBody":null,"responds":"OrderReservationCommandCenterView"},
"listReservationConfirmationExpiry": {"method":"GET","path":"/reservation-confirmation-expiry","contract":"orders","summary":"Reservation Confirmation, Expiry & Fulfillment Readiness","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReservationConfirmationExpiryFulfillmentReadinessView"},
"setCustomerGuestAccount": {"method":"PUT","path":"/customer-guest-account","contract":"orders","summary":"Customer, Guest & Account Assignment","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CustomerGuestAccountAssignmentInput","responds":"CustomerGuestAccountAssignmentView"},
"setOrderReservationStatus": {"method":"PUT","path":"/order-reservation-statu","contract":"orders","summary":"Order & Reservation Status Lifecycle Configuration","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"OrderReservationStatusLifecycleConfigurationInput","responds":"OrderReservationStatusLifecycleConfigurationView"},
"setReservationHoldPolicy": {"method":"PUT","path":"/reservation-hold-policy","contract":"orders","summary":"Reservation & Hold Policy Configuration","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"ReservationHoldPolicyConfigurationInput","responds":"ReservationHoldPolicyConfigurationView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CapacityReservationInventoryCommitmentView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Capacity Reservation & Inventory Commitment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"inventoryType":{"type":"string","enum":["generalAdmissionCapacity","seatInventory","timeslotCapacity","eventCapacity","productInventory","rentalInventory","fBRetailInventoryWhereApplicable"],"description":"Inventory the commitment is against."},"releaseReason":{"type":"string","enum":["holdExpires","reservationCancels","paymentFailsAccordingToPolicy","orderFails","authorizedAmendmentRemovesProduct"],"description":"Why the inventory was released."},"commitmentType":{"type":"string","enum":["temporaryHold","confirmedConsumption"],"description":"Temporary availability protection or confirmed consumption"},"orderId":{"type":"string","description":"Order ID"},"reservationId":{"type":"string","description":"Reservation ID"},"quantity":{"type":"integer","description":"Quantity committed"},"expiresAt":{"type":"string","format":"date-time","description":"When a temporary hold ends"}}},
"CustomerGuestAccountAssignmentInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Customer, Guest & Account Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"name":{"type":"string","description":"Name"},"email":{"type":"string","description":"Email"},"mobile":{"type":"string","description":"Mobile"},"country":{"type":"string","description":"Country"},"language":{"type":"string","description":"Language"},"dateOfBirth":{"type":"string","format":"date-time","description":"Date of Birth"},"customerId":{"type":"string","description":"Customer ID"},"membershipId":{"type":"string","description":"Membership ID"},"company":{"type":"string","description":"Company"},"taxDetails":{"type":"string","description":"Tax Details"},"partner":{"type":"string","description":"Partner"},"reseller":{"type":"string","description":"Reseller"},"agent":{"type":"string","description":"Agent"},"anonymousSale":{"type":"string","description":"Anonymous Sale where permitted"},"costCenter":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cost Center where applicable"},"customerType":{"type":"string","enum":["guestCheckout","registeredCustomer","member","corporateAccount","b2bAccount","groupOrganizer","anonymousSale"],"description":"How the order is attributed."}}},
"CustomerGuestAccountAssignmentView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Customer, Guest & Account Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string","description":"Name"},"email":{"type":"string","description":"Email"},"mobile":{"type":"string","description":"Mobile"},"country":{"type":"string","description":"Country"},"language":{"type":"string","description":"Language"},"dateOfBirth":{"type":"string","format":"date-time","description":"Date of Birth"},"customerId":{"type":"string","description":"Customer ID"},"membershipId":{"type":"string","description":"Membership ID"},"company":{"type":"string","description":"Company"},"taxDetails":{"type":"string","description":"Tax Details"},"partner":{"type":"string","description":"Partner"},"reseller":{"type":"string","description":"Reseller"},"agent":{"type":"string","description":"Agent"},"anonymousSale":{"type":"string","description":"Anonymous Sale where permitted"},"costCenter":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cost Center where applicable"},"customerType":{"type":"string","enum":["guestCheckout","registeredCustomer","member","corporateAccount","b2bAccount","groupOrganizer","anonymousSale"],"description":"How the order is attributed."}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**The currency the guest selected and is charged in** (CHG-FIN-001, 2 October 2026). Null or equal to `currency` for a sale in the base currency. Everything else on the order, and every ledger posting, stays in the base currency `currency`."},"chargeFxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`), stored on the order so the payment, the receipt, the tax invoice and any refund use the same rate (CHG-FIN-001)."},"chargeFxRateId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `finance.FxRate` row the rate was taken from, for audit."},"chargeTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"`grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to the provider asks for (CHG-FIN-001)."},"chargeRateLockedUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms the new amount (CHG-FIN-001)."},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderCreationSourceChannelConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in `orders.order_source_channel` (DM5, 29 September)","description":"**What Order Creation & Source/Channel Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"subChannel":{"type":"string","description":"Sub-Channel"},"salesLocation":{"type":"string","description":"Sales Location"},"terminal":{"type":"string","description":"Terminal"},"device":{"type":"string","description":"Device"},"agent":{"type":"string","description":"Agent"},"partner":{"type":"string","description":"Partner"},"campaign":{"type":"string","description":"Campaign"},"affiliate":{"type":"string","description":"Affiliate"},"apiConsumer":{"type":"string","description":"API Consumer"},"externalReference":{"type":"string","description":"External Reference"},"holdInventory":{"type":"string","description":"Hold Inventory"},"source":{"type":"string","enum":["b2cWeb","mobileApp","pos","mobileFlyingPos","kiosk","callCenter","boxOffice","b2bPortal","reseller","ota","api","administrativeBackend"],"description":"Order source."},"numberingRule":{"type":"string","enum":["globalSequence","tenantSequence","venueSequence","yearMonthPrefix","customPattern"],"description":"Order numbering rule."},"channelPrefix":{"type":"string","description":"Channel prefix for the order number"},"partnerReferenceType":{"type":"string","enum":["otaBookingReference","resellerOrderId","erpReference","externalCrmReference"],"description":"Kind of partner identifier held in externalReference"}}},
"OrderCreationSourceChannelConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Order Creation & Source/Channel Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"subChannel":{"type":"string","description":"Sub-Channel"},"salesLocation":{"type":"string","description":"Sales Location"},"terminal":{"type":"string","description":"Terminal"},"device":{"type":"string","description":"Device"},"agent":{"type":"string","description":"Agent"},"partner":{"type":"string","description":"Partner"},"campaign":{"type":"string","description":"Campaign"},"affiliate":{"type":"string","description":"Affiliate"},"apiConsumer":{"type":"string","description":"API Consumer"},"externalReference":{"type":"string","description":"External Reference"},"holdInventory":{"type":"string","description":"Hold Inventory"},"source":{"type":"string","enum":["b2cWeb","mobileApp","pos","mobileFlyingPos","kiosk","callCenter","boxOffice","b2bPortal","reseller","ota","api","administrativeBackend"],"description":"Order source."},"numberingRule":{"type":"string","enum":["globalSequence","tenantSequence","venueSequence","yearMonthPrefix","customPattern"],"description":"Order numbering rule."},"channelPrefix":{"type":"string","description":"Channel prefix for the order number"},"partnerReferenceType":{"type":"string","enum":["otaBookingReference","resellerOrderId","erpReference","externalCrmReference"],"description":"Kind of partner identifier held in externalReference"}}},
"OrderLifecycleTimelineSlaExceptionsAiOperationsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Order Lifecycle Timeline, SLA, Exceptions & AI Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"timestamp":{"type":"string","format":"date-time","description":"Timestamp"},"eventType":{"type":"string","description":"Event Type"},"userSystem":{"type":"string","description":"User/System"},"channel":{"type":"string","description":"Channel"},"previousState":{"type":"string","description":"Previous State"},"newState":{"type":"integer","description":"New State"},"relatedTransaction":{"type":"string","description":"Related Transaction"},"correlationId":{"type":"string","description":"Correlation ID"},"result":{"type":"string","description":"Result"},"exceptionType":{"type":"string","enum":["stuckOrder","orphanReservation","paymentOrderMismatch","capacityMismatch","missingCustomerData","fulfillmentFailure","externalSynchronizationFailure"],"description":"Exception detected."}}},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderLineProductEntitlementCompositionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Order Line, Product & Entitlement Composition displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"product":{"type":"string","description":"Product"},"variant":{"type":"string","description":"Variant"},"quantity":{"type":"integer","description":"Quantity"},"personType":{"type":"string","description":"Person Type"},"event":{"type":"string","description":"Event"},"performance":{"type":"string","description":"Performance"},"date":{"type":"string","format":"date-time","description":"Date"},"timeslot":{"type":"string","description":"Timeslot"},"seat":{"type":"string","description":"Seat"},"entitlement":{"type":"string","description":"Entitlement"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount"},"tax":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Tax"},"fee":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fee"},"fulfillmentMethod":{"type":"string","description":"Fulfillment Method"},"lineType":{"type":"string","enum":["tickets","memberships","addOns","fB","retail","rental","parking","experiences","packages","vouchers","otherConfiguredProducts"],"description":"What the line sells."}}},
"OrderReservationCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Order & Reservation Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ordersToday":{"type":"string","description":"Orders Today"},"confirmedOrders":{"type":"integer","description":"Confirmed Orders"},"activeReservations":{"type":"integer","description":"Active Reservations"},"temporaryHolds":{"type":"integer","description":"Temporary Holds"},"pendingPayment":{"type":"integer","description":"Pending Payment"},"expiringReservations":{"type":"integer","description":"Expiring Reservations"},"failedOrders":{"type":"integer","description":"Failed Orders"},"partiallyFulfilled":{"type":"string","description":"Partially Fulfilled"},"completedOrders":{"type":"integer","description":"Completed Orders"},"cancelledOrders":{"type":"integer","description":"Cancelled Orders"},"ordersRequiringAttention":{"type":"string","description":"Orders Requiring Attention"},"grossOrderValue":{"type":"string","description":"Gross Order Value"},"orderId":{"type":"string","description":"Order ID"},"reservationId":{"type":"string","description":"Reservation ID"},"channel":{"type":"string","description":"Channel"},"venue":{"type":"string","description":"Venue"},"orderValue":{"type":"string","description":"Order Value"},"paymentStatus":{"type":"integer","description":"Payment Status"},"reservationStatus":{"type":"integer","description":"Reservation Status"},"fulfillmentStatus":{"type":"integer","description":"Fulfillment Status"},"createdDate":{"type":"string","format":"date-time","description":"Created Date"},"expiry":{"type":"string","format":"date-time","description":"Expiry"},"ownerAgent":{"type":"string","description":"Owner/Agent"}}},
"OrderReservationStatusLifecycleConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in `orders.status_transition_rule` (DM5, 29 September)","description":"**What Order & Reservation Status Lifecycle Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each transition define* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.","properties":{"fromStatus":{"type":"string","description":"From Status"},"toStatus":{"type":"string","description":"To Status"},"requiredConditions":{"type":"string","description":"Required Conditions"},"userSystemAction":{"type":"string","description":"User/System Action"},"allowedRole":{"type":"string","description":"Allowed Role"},"integrationRequirement":{"type":"string","description":"Integration Requirement"},"notification":{"type":"string","description":"Notification"},"auditRequirement":{"type":"string","description":"Audit Requirement"},"systemControlledStatus":{"type":"string","description":"System-Controlled Status"},"operationalStatus":{"type":"string","description":"Operational Status"},"userEditableStatus":{"type":"string","description":"User-Editable Status"}},"x-ticvai-record-definition":"For each transition define"},
"OrderReservationStatusLifecycleConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Order & Reservation Status Lifecycle Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"fromStatus":{"type":"string","description":"From Status"},"toStatus":{"type":"string","description":"To Status"},"requiredConditions":{"type":"string","description":"Required Conditions"},"userSystemAction":{"type":"string","description":"User/System Action"},"allowedRole":{"type":"string","description":"Allowed Role"},"integrationRequirement":{"type":"string","description":"Integration Requirement"},"notification":{"type":"string","description":"Notification"},"auditRequirement":{"type":"string","description":"Audit Requirement"},"systemControlledStatus":{"type":"string","description":"System-Controlled Status"},"operationalStatus":{"type":"string","description":"Operational Status"},"userEditableStatus":{"type":"string","description":"User-Editable Status"}}},
"OrderStatement": {"x-ticvai-persistence":"none — computed from order, payment, refund and ledger","type":"object","required":["orderId","orderNumber","currency","entries","currentBalance"],"properties":{"orderId":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"entries":{"type":"array","description":"Sequential. What an agent reads to a guest asking about a charge.","items":{"type":"object","required":["kind","amount","runningBalance","occurredAt"],"properties":{"kind":{"type":"string","enum":["sale","payment","refund","void","modification","exchange","fee","variance","chargeback"]},"description":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"runningBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"referenceId":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"occurredAt":{"type":"string","format":"date-time"}}}},"totalPaid":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalRefunded":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"currentBalance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Positive means the guest owes; negative means a refund is outstanding."}}},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n**Cash at a till only** (CHG-FIN-001, 2 October 2026). A card or wallet payment the guest made in a currency they selected is refunded in that currency (`Refund.tenderCurrency`).\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"ReservationConfirmationExpiryFulfillmentReadinessView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Reservation Confirmation, Expiry & Fulfillment Readiness displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"confirmationConditions":{"type":"array","items":{"type":"string","enum":["paymentComplete","depositReceived","creditApproved","capacityConfirmed","customerDataComplete","requiredWaiverComplete","requiredApprovalComplete","partnerConfirmationReceived"]},"description":"Conditions that confirm the reservation."},"failedIssueChecks":{"type":"array","items":{"type":"string","enum":["orderConfirmed","paymentConditionMet","requiredCustomerData","entitlementValid","waiverRequirement","credentialConfiguration","deliveryMethod"]},"description":"Checks before issuing ticket/media that fail."},"reservationId":{"type":"string","description":"Reservation ID"},"orderId":{"type":"string","description":"Order ID"},"status":{"type":"string","description":"Reservation status (states/reservation.yaml)"},"expiresAt":{"type":"string","format":"date-time","description":"Expiry"}}},
"ReservationHoldPolicyConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in `orders.reservation_hold_policy` (DM5, 29 September)","description":"**What Reservation & Hold Policy Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"channel":{"type":"string","description":"Channel"},"product":{"type":"string","description":"Product"},"event":{"type":"string","description":"Event"},"performance":{"type":"string","description":"Performance"},"ticketType":{"type":"string","description":"Ticket Type"},"customerSegment":{"type":"string","description":"Customer Segment"},"reservationType":{"type":"string","description":"Reservation Type"},"extensionAllowed":{"type":"boolean","description":"Extension Allowed"},"maximumExtensions":{"type":"string","description":"Maximum Extensions"},"extensionDuration":{"type":"string","format":"date-time","description":"Extension Duration"},"authorizedRole":{"type":"string","description":"Authorized Role"},"approvalRequirement":{"type":"string","description":"Approval Requirement"},"holdType":{"type":"string","enum":["cartHold","checkoutHold","agentReservation","groupReservation","b2bReservation","corporateReservation","manualHold","paymentHold","seatHold","inventoryHold"],"description":"Kind of hold."},"lockedCapacity":{"type":"array","items":{"type":"string","enum":["admissionCapacity","seat","inventory","timeslotCapacity","entitlementCapacity"]},"description":"What the reservation locks through the central capacity services."},"holdDurationMinutes":{"type":"integer","description":"Hold duration in minutes"},"onExpiry":{"type":"array","items":{"type":"string","enum":["releaseInventory","releaseSeats","cancelReservation","notifyCustomer","notifyAgent"]},"description":"What happens on expiry"}}},
"ReservationHoldPolicyConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Reservation & Hold Policy Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channel":{"type":"string","description":"Channel"},"product":{"type":"string","description":"Product"},"event":{"type":"string","description":"Event"},"performance":{"type":"string","description":"Performance"},"ticketType":{"type":"string","description":"Ticket Type"},"customerSegment":{"type":"string","description":"Customer Segment"},"reservationType":{"type":"string","description":"Reservation Type"},"extensionAllowed":{"type":"boolean","description":"Extension Allowed"},"maximumExtensions":{"type":"string","description":"Maximum Extensions"},"extensionDuration":{"type":"string","format":"date-time","description":"Extension Duration"},"authorizedRole":{"type":"string","description":"Authorized Role"},"approvalRequirement":{"type":"string","description":"Approval Requirement"},"holdType":{"type":"string","enum":["cartHold","checkoutHold","agentReservation","groupReservation","b2bReservation","corporateReservation","manualHold","paymentHold","seatHold","inventoryHold"],"description":"Kind of hold."},"lockedCapacity":{"type":"array","items":{"type":"string","enum":["admissionCapacity","seat","inventory","timeslotCapacity","entitlementCapacity"]},"description":"What the reservation locks through the central capacity services."},"holdDurationMinutes":{"type":"integer","description":"Hold duration in minutes (e.g. B2C checkout 10, call centre 20, B2B group 2,880)"},"onExpiry":{"type":"array","items":{"type":"string","enum":["releaseInventory","releaseSeats","cancelReservation","notifyCustomer","notifyAgent"]},"description":"What happens on expiry; an audit record is always kept"}}}
}
```
