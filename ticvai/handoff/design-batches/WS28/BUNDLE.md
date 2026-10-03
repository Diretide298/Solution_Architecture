# WS28 — Group Sales   Corporate Booking Management board 2

**10 screens · 19 operations · 29 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `ORDER_CREATE, ORDER_MODIFY, ORDER_RESCHEDULE, ORDER_VIEW`. A control nobody can use must say so,
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
| `BO-274` | Group Booking Operations Command Center | B–D | 0 | 14 | 6 | 0 | 2 | 6 | — | notStarted (generated) |
| `BO-275` | Group Operational Planning & Task Workspace | B–D | 18 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-276` | Participants, Guest Lists & Group Structure | B–D | 8 | 6 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-277` | Group Payment, Deposit & Balance Management | B–D | 5 | 16 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-278` | Group Ticket, Seat & Entitlement Allocation | B–D | 8 | 16 | 6 | 0 | 1 | 6 | — | notStarted (generated) |
| `BO-279` | Group Ticket Fulfillment & Distribution | B–D | 3 | 16 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-280` | Group Arrival, Check-In & Admission Operations | B–D | 6 | 20 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-281` | Group Amendments, Cancellation & Refund Operations | B–D | 0 | 0 | 6 | 9 | 0 | 6 | — | notStarted (generated) |
| `BO-282` | Group Booking Reconciliation, Closure & Performance | B–D | 0 | 12 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `BO-283` | Group Sales Analytics & AI Intelligence Center | B–D | 2 | 28 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-274, BO-280, BO-282 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-274` Group Booking Operations Command Center

**Provide Operations with a real-time command center for all confirmed and upcoming group bookings.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/group-booking-operations-command-center-bo-274` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Operations' view of confirmed and upcoming groups: arrivals today, deposits outstanding, readiness.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listGroupBooking, listGroupBookingReconciliation return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listGroupBookingReconciliation carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listGroupBooking / contracts/spine/orders.yaml#listGroupBookingReconciliation; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every group booking operations** (data table, from `listGroupBooking`)

| Shows | Format | Notes |
|---|---|---|
| Booking value | text | Booking Value |
| Payment status | 1,234 | Payment Status |
| Guest list status | 1,234 | Guest List Status |
| Ticket status | 1,234 | Ticket Status |
| Resource status | 1,234 | Resource Status |
| Readiness | 1,234.5 | Readiness % |

**The selected group booking operations** (detail panel): The pack groups this record's detail under its own headings: “Use”.

| Shows | Format | Notes |
|---|---|---|
| Group type | text | Group Type |
| Visit date | 1 Oct 2026, 14:30 | Visit Date |
| Booking value | text | Booking Value |
| Payment status | 1,234 | Payment Status |
| Guest list status | 1,234 | Guest List Status |
| Ticket status | 1,234 | Ticket Status |
| Resource status | 1,234 | Resource Status |
| Readiness | 1,234.5 | Readiness % |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **arrivals board**: Today and next 7 days, with deposit flags and staff assigned. *(source: contracts/spine/orders.yaml#listGroupBooking)*

**Data it reads**: `listGroupBooking` (onLoad, Group Booking Operations Command Center); `listGroupBookingReconciliation` (onLoad, Group Booking Reconciliation, Closure & Performance)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-275` Group Operational Planning & Task Workspace: *Works in Group Operational Planning & Task Workspace*; calls `listGroupBooking`
- → `BO-282` Group Booking Reconciliation, Closure & Performance: *Works in Group Booking Reconciliation, Closure & Performance*; calls `listGroupBooking`
- → `BO-283` Group Sales Analytics & AI Intelligence Center: *Works in Group Sales Analytics & AI Intelligence Center*; calls `listGroupBooking`
- → `BO-276` Participants, Guest Lists & Group Structure: *Works in Participants, Guest Lists & Group Structure*; carries `groupBookingId`; calls `listGroupBooking`
- → `BO-277` Group Payment, Deposit & Balance Management: *Works in Group Payment, Deposit & Balance Management*; carries `groupBookingId`; calls `listGroupBooking`
- → `BO-278` Group Ticket, Seat & Entitlement Allocation: *Works in Group Ticket, Seat & Entitlement Allocation*; carries `groupBookingId`; calls `listGroupBooking`
- → `BO-279` Group Ticket Fulfillment & Distribution: *Works in Group Ticket Fulfillment & Distribution*; carries `groupBookingId`; calls `listGroupBooking`
- → `BO-280` Group Arrival, Check-In & Admission Operations: *Works in Group Arrival, Check-In & Admission Operations*; carries `groupBookingId`; calls `listGroupBooking`
- → `BO-281` Group Amendments, Cancellation & Refund Operations: *Works in Group Amendments, Cancellation & Refund Operations*; carries `groupBookingId`; calls `listGroupBooking`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group booking operations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group booking operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group booking operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group booking operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
arrivals:
- group: Al Noor Academy
  at: 09:30
  size: 31
  deposit: paid
```

#### Permissions

- `listGroupBooking` → `ORDER_VIEW` (read) · staff
- `listGroupBookingReconciliation` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Group operations view shows upcoming arrivals for the day/period and flags deposits still required; staff (e.g. tour guide, educator) can be assigned to a group ahead of arrival; participant details captured where required. *(client request · MoM 31 Aug 2026, 4.8 Group Operations, Payment Links & Check-In · DI-566)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-274` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-274`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 2
- Flow F137 *Group Sales Corporate Booking Management board 2: Group Booking Operations …*, step 1: Opens Group Booking Operations Command Center → Provide Operations with a real-time command center for all confirmed and upcoming group bookings.
- Flow F137 *Group Sales Corporate Booking Management board 2: Group Booking Operations …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F137 *Group Sales Corporate Booking Management board 2: Group Booking Operations …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F137 *Group Sales Corporate Booking Management board 2: Group Booking Operations …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F137 *Group Sales Corporate Booking Management board 2: Group Booking Operations …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F137 *Group Sales Corporate Booking Management board 2: Group Booking Operations …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F137 *Group Sales Corporate Booking Management board 2: Group Booking Operations …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F137 *Group Sales Corporate Booking Management board 2: Group Booking Operations …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F137 branch at step 1 (expected): when Nothing has been set up on Group Booking Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F137 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-274?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-275`, `BO-282`, `BO-283`, `BO-276`, `BO-277`, `BO-278`, `BO-279`, `BO-280`, `BO-281`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-275` Group Operational Planning & Task Workspace

**Convert the commercial booking into a detailed operational execution plan.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure/reference) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/group-operational-planning-task-workspace-bo-275` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the group operational plan and its tasks that setGroupOperationalPlanning writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The group's operational plan: arrival and departure, meeting point, gate, leaders, ticketing method, tasks.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setGroupOperationalPlanning and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Arrival Date | select field | — | — | — | — | — | — |
| Arrival Time | select field | — | — | — | — | — | — |
| Arrival Location | select field | — | — | — | — | — | — |
| Group Meeting Point | select field | — | — | — | — | — | — |
| Entry Gate | select field | — | — | — | — | — | — |
| Departure Time | select field | — | — | — | — | — | — |
| Group Size | select field | — | — | — | — | — | — |
| Group Leaders | select field | — | — | — | — | — | — |
| Contact Person | select field | — | — | — | — | — | — |
| Ticketing Method | select field | — | — | — | — | — | — |
| Seating | select field | — | — | — | — | — | — |
| Guides | select field | — | — | — | — | — | — |
| Catering | select field | — | — | — | — | — | — |
| Transportation | select field | — | — | — | — | — | — |
| Parking | select field | — | — | — | — | — | — |
| Accessibility | select field | — | — | — | — | — | — |
| Equipment | select field | — | — | — | — | — | — |
| Special Requirements | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **plan**: Arrival gate picked from access points; leaders from the participant list. *(source: contracts/spine/orders.yaml#setGroupOperationalPlanning)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-274` Group Booking Operations Command Center: *Returns to the board's landing screen*; calls `setGroupOperationalPlanning`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group operational planning configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group operational planning untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group operational planning configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
plan:
  arrival: 2026-12-10 09:30
  gate: Gate 2
  meetingPoint: Group plaza
```

#### Permissions

- `setGroupOperationalPlanning` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group operations view shows upcoming arrivals for the day/period and flags deposits still required; staff (e.g. tour guide, educator) can be assigned to a group ahead of arrival; participant details captured where required. *(client request · MoM 31 Aug 2026, 4.8 Group Operations, Payment Links & Check-In · DI-566)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-275` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-275`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 2
- Flow F137 *Group Sales Corporate Booking Management board 2: Group Booking Operations …*, step 2: Works in Group Operational Planning & Task Workspace → Convert the commercial booking into a detailed operational execution plan.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-275?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-274`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-276` Participants, Guest Lists & Group Structure

**Manage the people participating in the group where individual information is required.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Detect) and no metric row |
| Offline | online only |
| Opens with | `groupBookingId` (navigation) |
| Route | `/sell/participants-guest-lists-group-structure-bo-276` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The people in a group where names are required: entered, imported from CSV or Excel, uploaded by the customer or by API.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listParticipantGuestList return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listParticipantGuestList carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listParticipantGuestList; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Sent by *Save participant list*** (`setParticipantGuestList`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Source `source` | radio group | required | — | Manual entry · Csv excel import · Customer upload · API | — | How the names arrived (decided 29 September, readiness close-out). | `setParticipantGuestList` body |
| Participants `participants` | repeatable rows | required | — | — | — | — | `setParticipantGuestList` body |
| Full name `participants[].fullName` | text field | required | — | max length 200 | — | — | `setParticipantGuestList` body |
| Role `participants[].role` | segmented control | optional | Participant | Participant · Leader · Supervisor | — | — | `setParticipantGuestList` body |
| Email `participants[].email` | email field | optional | — | — | name@example.ae | — | `setParticipantGuestList` body |
| Phone `participants[].phone` | phone field | optional | — | max length 30 | +971 5X XXX XXXX (E.164) | — | `setParticipantGuestList` body |
| Date of birth `participants[].dateOfBirth` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setParticipantGuestList` body |
| File ref `fileRef` | picker: choose a file ref | optional | — | — | shows names, sends the id | The uploaded file the names came from. Required for `csvExcelImport` and `customerUpload`. | `setParticipantGuestList` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **participants**: Import with a preview and errors per row; the list replaces the previous one. *(source: contracts/spine/orders.yaml#setParticipantGuestList)*

#### Outputs: what the screen shows and produces

**Shown**

**Every participants guest lists** (data table, from `listParticipantGuestList`)

| Shows | Format | Notes |
|---|---|---|
| Duplicate guest | text | not in the schema: `Duplicate guest` |
| Validation issues | list or chips (count when long) | Problems detected on the list. |
| Duplicate ticket assignment | text | not in the schema: `Duplicate ticket assignment` |

**The selected participants guest lists** (detail panel): The pack groups this record's detail under its own headings: “Named Guests”, “Quantity-Based”, “Hybrid”, “Where required”, “Privacy”.

| Shows | Format | Notes |
|---|---|---|
| Duplicate guest | text | not in the schema: `Duplicate guest` |
| Validation issues | list or chips (count when long) | Problems detected on the list. |
| Duplicate ticket assignment | text | not in the schema: `Duplicate ticket assignment` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Manual Entry (primary button) | navigation or local | — | — | — | — |
| CSV/Excel Import (secondary button) | navigation or local | — | — | — | — |
| Customer Upload (secondary button) | navigation or local | — | — | — | — |
| API (secondary button) | navigation or local | — | — | — | — |
| Save participant list (primary button) | `setParticipantGuestList` PUT `/group-bookings/{groupBookingId}/participants` | ParticipantGuestListInput | ParticipantGuestListView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The group is cancelled or complete (`groupClosed`). (GroupBookingProblem); 412 The row changed since the … | — |

**Data it reads**: `listParticipantGuestList` (onLoad, Participants, Guest Lists & Group Structure)

**Where the user goes next**

- → `BO-274` Group Booking Operations Command Center: *Returns to the board's landing screen*; calls `listParticipantGuestList`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The participants guest lists list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the participants guest lists untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No participants guest lists yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the participants guest lists are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The group is cancelled or complete (`groupClosed`). (GroupBookingProblem); 422 `csvExcelImport` or `customerUpload` with no `fileRef` (`participant-file-missing`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
participants:
- name: Ahmed Saleh
  age: 10
- name: Sara Nabil
  age: 11
```

#### Permissions

- `listParticipantGuestList` → `ORDER_VIEW` (read) · staff
- `setParticipantGuestList` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group operations view shows upcoming arrivals for the day/period and flags deposits still required; staff (e.g. tour guide, educator) can be assigned to a group ahead of arrival; participant details captured where required. *(client request · MoM 31 Aug 2026, 4.8 Group Operations, Payment Links & Check-In · DI-566)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-276` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-276`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 2
- Flow F137 *Group Sales Corporate Booking Management board 2: Group Booking Operations …*, step 4: Works in Participants, Guest Lists & Group Structure → Manage the people participating in the group where individual information is required.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (404, 409, 412, 422).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-276?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Manual Entry, CSV/Excel Import, Customer Upload, API, Save participant list.
- [ ] Every transition is wired: `BO-274`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-277` Group Payment, Deposit & Balance Management

**Track the complete payment lifecycle of a group booking.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `groupBookingId` (navigation) |
| Route | `/sell/group-payment-deposit-balance-management-bo-277` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** A group's payment schedule and status: deposit then balance, milestones or custom, paid and outstanding.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listGroupPaymentDeposit return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listGroupPaymentDeposit carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listGroupPaymentDeposit; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Sent by *Save payment schedule*** (`setGroupPaymentSchedule`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Schedule type `scheduleType` | radio group | required | — | Deposit then balance · Milestone payment · Final balance · Custom schedule | — | The shape of the schedule (decided 29 September, readiness close-out). | `setGroupPaymentSchedule` body |
| Milestones `milestones` | repeatable rows | required | — | at least 1 | — | — | `setGroupPaymentSchedule` body |
| Due date `milestones[].dueDate` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setGroupPaymentSchedule` body |
| Amount `milestones[].amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setGroupPaymentSchedule` body |
| Label `milestones[].label` | text field | optional | — | max length 60 | — | — | `setGroupPaymentSchedule` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **schedule**: Type then milestones (date, amount or percent); totals must equal the booking. *(source: contracts/spine/orders.yaml#setGroupPaymentSchedule)*

#### Outputs: what the screen shows and produces

**Shown**

**Every group payment deposit** (data table, from `listGroupPaymentDeposit`)

| Shows | Format | Notes |
|---|---|---|
| Booking value | text | Booking Value |
| Deposit required | yes / no (icon or chip) | Deposit Required |
| Deposit paid | AED 1,234.50 | Deposit Paid |
| Balance | AED 1,234.50 | Balance |
| Amount paid | AED 1,234.50 | Amount Paid |
| Amount outstanding | AED 1,234.50 | Amount Outstanding |
| Next due date | 1 Oct 2026, 14:30 | Next Due Date |
| Payment status | 1,234 | Payment Status |

**The selected group payment deposit** (detail panel): The pack groups this record's detail under its own headings: “Payment Methods”, “Architecture”.

| Shows | Format | Notes |
|---|---|---|
| Booking value | text | Booking Value |
| Deposit required | yes / no (icon or chip) | Deposit Required |
| Deposit paid | AED 1,234.50 | Deposit Paid |
| Balance | AED 1,234.50 | Balance |
| Amount paid | AED 1,234.50 | Amount Paid |
| Amount outstanding | AED 1,234.50 | Amount Outstanding |
| Next due date | 1 Oct 2026, 14:30 | Next Due Date |
| Payment status | 1,234 | Payment Status |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Deposit (primary button) | navigation or local | — | — | — | — |
| Milestone Payment (secondary button) | navigation or local | — | — | — | — |
| Final Balance (secondary button) | navigation or local | — | — | — | — |
| Custom Schedule (secondary button) | navigation or local | — | — | — | — |
| Save payment schedule (primary button) | `setGroupPaymentSchedule` PUT `/group-bookings/{groupBookingId}/payment-schedule` | GroupPaymentScheduleInput | GroupPaymentScheduleView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The group is cancelled or complete (`groupClosed`). (GroupBookingProblem); 412 The row changed since the … | — |

**Data it reads**: `listGroupPaymentDeposit` (onLoad, Group Payment, Deposit & Balance Management)

**Where the user goes next**

- → `BO-274` Group Booking Operations Command Center: *Returns to the board's landing screen*; calls `listGroupPaymentDeposit`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group payment deposit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group payment deposit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group payment deposit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group payment deposit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The group is cancelled or complete (`groupClosed`). (GroupBookingProblem); 422 The milestones do not sum to the group booking's total (`group-payment-schedule-unbalanced`), or a milestone already paid was removed or changed … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
schedule:
  type: depositThenBalance
  deposit: AED 9,000.00 by 2026-11-25
  balance: AED 27,000.00 on arrival
```

#### Permissions

- `listGroupPaymentDeposit` → `ORDER_VIEW` (read) · staff
- `setGroupPaymentSchedule` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Amendments/cancellations/reschedules are checked against the applicable policy before being allowed. A booking's financial status (deposit required, partial payment, full payment) is tracked; schools and corporates can pay a 20-30% deposit with the balance due on or before arrival. *(agreed · MoM 1 Sep 2026, 4.12 Amendment, Cancellation & Booking Status · DI-615)*
- Send Payment Link (deposit or full) opens a B2C-style cart-review and checkout page showing the booking the sales team created. Configurable expiry (e.g. 24 hours, a week); unpaid bookings auto-cancel on expiry. Applies to B2C, schools, corporates and groups. *(agreed · MoM 31 Aug 2026, 4.8 Send Payment Link · DI-567)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-277` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-277`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 2
- Flow F137 *Group Sales Corporate Booking Management board 2: Group Booking Operations …*, step 6: Works in Group Payment, Deposit & Balance Management → Track the complete payment lifecycle of a group booking.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (404, 409, 412, 422).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-277?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Deposit, Milestone Payment, Final Balance, Custom Schedule, Save payment schedule.
- [ ] Every transition is wired: `BO-274`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-278` Group Ticket, Seat & Entitlement Allocation

**Allocate the confirmed group inventory to individual guests, subgroups or quantity blocks.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `groupBookingId` (navigation) |
| Route | `/sell/group-ticket-seat-entitlement-allocation-bo-278` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Allocate the group's inventory: individual, bulk, named, by quantity or by zone; keep together; VIP.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listGroupTicketSeat return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listGroupTicketSeat carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listGroupTicketSeat; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Sent by *Save allocation*** (`setGroupTicketAllocation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Allocation mode `allocationMode` | radio group | required | — | Individual ticket · Bulk ticket · Named ticket · Quantity based ticket · Zone allocation | — | How the group's tickets are allocated (decided 29 September, readiness close-out). | `setGroupTicketAllocation` body |
| Keep group together `keepGroupTogether` | toggle | optional | off | — | — | — | `setGroupTicketAllocation` body |
| Vip allocation `vipAllocation` | toggle | optional | off | — | — | Set aside the group's VIP places. | `setGroupTicketAllocation` body |
| Allocations `allocations` | repeatable rows | required | — | — | — | — | `setGroupTicketAllocation` body |
| Product `allocations[].productId` | picker: choose a product | required | — | — | shows names, sends the id | — | `setGroupTicketAllocation` body |
| Quantity `allocations[].quantity` | number field | required | — | min 1 | — | — | `setGroupTicketAllocation` body |
| Zone `allocations[].zoneId` | picker: choose a zone | optional | — | — | shows names, sends the id | Required for `zoneAllocation`. | `setGroupTicketAllocation` body |
| Participant `allocations[].participantId` | picker: choose a participant | optional | — | — | shows names, sends the id | The participant a `namedTicket` line is for. Required for `namedTicket`. | `setGroupTicketAllocation` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **allocationMode**: Mode first, then the allocation grid. *(source: contracts/spine/orders.yaml#setGroupTicketAllocation)*

#### Outputs: what the screen shows and produces

**Shown**

**Every group ticket seat** (data table, from `listGroupTicketSeat`)

| Shows | Format | Notes |
|---|---|---|
| Product | text | Product |
| Quantity booked | 1,234 | Quantity Booked |
| Quantity allocated | 1,234 | Quantity Allocated |
| Remaining | text | Remaining |
| Ticket type | text | Ticket Type |
| Seat zone | text | Seat/Zone |
| Guest subgroup | text | Guest/Subgroup |
| Credential status | 1,234 | Credential Status |

**The selected group ticket seat** (detail panel): The pack groups this record's detail under its own headings: “Reserved Seating”, “Assigned”, “Allocate associated”.

| Shows | Format | Notes |
|---|---|---|
| Product | text | Product |
| Quantity booked | 1,234 | Quantity Booked |
| Quantity allocated | 1,234 | Quantity Allocated |
| Remaining | text | Remaining |
| Ticket type | text | Ticket Type |
| Seat zone | text | Seat/Zone |
| Guest subgroup | text | Guest/Subgroup |
| Credential status | 1,234 | Credential Status |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Individual Ticket (primary button) | navigation or local | — | — | — | — |
| Bulk Ticket (secondary button) | navigation or local | — | — | — | — |
| Named Ticket (secondary button) | navigation or local | — | — | — | — |
| Quantity-Based Ticket (secondary button) | navigation or local | — | — | — | — |
| Zone Allocation (secondary button) | navigation or local | — | — | — | — |
| Keep group together (secondary button) | navigation or local | — | — | — | — |
| VIP allocation (secondary button) | navigation or local | — | — | — | — |
| Save allocation (primary button) | `setGroupTicketAllocation` PUT `/group-bookings/{groupBookingId}/allocation` | GroupTicketAllocationInput | GroupTicketAllocationView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The group is cancelled or complete (`groupClosed`). (GroupBookingProblem); 412 The row changed since the … | produces a document or message: Set how a group's tickets are allocated |

**Data it reads**: `listGroupTicketSeat` (onLoad, Group Ticket, Seat & Entitlement Allocation)

**Where the user goes next**

- → `BO-274` Group Booking Operations Command Center: *Returns to the board's landing screen*; calls `listGroupTicketSeat`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group ticket seat list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group ticket seat untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group ticket seat yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group ticket seat are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The group is cancelled or complete (`groupClosed`). (GroupBookingProblem); 422 A `namedTicket` line with no `participantId`, or a `zoneAllocation` line with no `zoneId` (`allocation-line-incomplete`). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
allocation:
  mode: namedTicket
  keepTogether: true
  tickets: 31
```

#### Permissions

- `listGroupTicketSeat` → `ORDER_VIEW` (read) · staff
- `setGroupTicketAllocation` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group ticket QR options: one QR valid for a defined headcount, individual QR per member, or a single rotating/multi-use QR scanned until the headcount is exhausted. *(client request · MoM 31 Aug 2026, 4.8 Group Operations, Payment Links & Check-In · DI-569)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-278` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-278`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 2
- Flow F137 *Group Sales Corporate Booking Management board 2: Group Booking Operations …*, step 8: Works in Group Ticket, Seat & Entitlement Allocation → Allocate the confirmed group inventory to individual guests, subgroups or quantity blocks.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (404, 409, 412, 422).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-278?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Individual Ticket, Bulk Ticket, Named Ticket, Quantity-Based Ticket, Zone Allocation, Keep group together, VIP allocation, Save allocation.
- [ ] Every transition is wired: `BO-274`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-279` Group Ticket Fulfillment & Distribution

**Control how tickets and other credentials are delivered to the group.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `groupBookingId` (navigation) |
| Route | `/sell/group-ticket-fulfillment-distribution-bo-279` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How the group's tickets are delivered: email, SMS, wallet, bulk PDF, POS print or collection, to the organiser or each participant, and when released.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listGroupTicketFulfillment return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listGroupTicketFulfillment carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listGroupTicketFulfillment; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Sent by *Save fulfilment*** (`setGroupTicketFulfillment`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Method `method` | select | required | — | Email · SMS · Wallet · Bulk pdf · POS print · Physical collection | — | How the tickets are delivered (decided 29 September, readiness close-out). | `setGroupTicketFulfillment` body |
| Recipients `recipients` | segmented control | required | — | Organiser · Each participant | — | Who receives them (decided 29 September, readiness close-out). | `setGroupTicketFulfillment` body |
| Release at `releaseAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Hold the tickets back until then; null releases them when the group is confirmed. | `setGroupTicketFulfillment` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **method and recipients**: One method; recipients organiser or each participant; release time optional. *(source: contracts/spine/orders.yaml#setGroupTicketFulfillment)*

#### Outputs: what the screen shows and produces

**Shown**

**Every group ticket fulfillment** (data table, from `listGroupTicketFulfillment`)

| Shows | Format | Notes |
|---|---|---|
| Tickets required | yes / no (icon or chip) | Tickets Required |
| Generated | text | Generated |
| Sent | text | Sent |
| Delivered | text | Delivered |
| Opened | text | Opened |
| Downloaded | text | Downloaded |
| Failed | 1,234 | Failed |
| Reissued | text | Reissued |

**The selected group ticket fulfillment** (detail panel): The pack groups this record's detail under its own headings: “Central Distribution”, “Individual Distribution”, “Subgroup Distribution”, “Generate an operational manifest showing”, “Important Architecture”.

| Shows | Format | Notes |
|---|---|---|
| Tickets required | yes / no (icon or chip) | Tickets Required |
| Generated | text | Generated |
| Sent | text | Sent |
| Delivered | text | Delivered |
| Opened | text | Opened |
| Downloaded | text | Downloaded |
| Failed | 1,234 | Failed |
| Reissued | text | Reissued |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Generate Tickets, Send, Resend, Reissue, Change Delivery Method, Revoke where permitted. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| POS Print (primary button) | navigation or local | — | — | — | — |
| Physical Collection (secondary button) | navigation or local | — | — | — | — |
| Save fulfilment (primary button) | `setGroupTicketFulfillment` PUT `/group-bookings/{groupBookingId}/fulfillment` | GroupTicketFulfillmentInput | GroupTicketFulfillmentView | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The group is cancelled or complete (`groupClosed`). (GroupBookingProblem); 412 The row changed since the … | produces a document or message: Set how a group's tickets are delivered |

**Data it reads**: `listGroupTicketFulfillment` (onLoad, Group Ticket Fulfillment & Distribution)

**Where the user goes next**

- → `BO-274` Group Booking Operations Command Center: *Returns to the board's landing screen*; calls `listGroupTicketFulfillment`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group ticket fulfillment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group ticket fulfillment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group ticket fulfillment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group ticket fulfillment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The group is cancelled or complete (`groupClosed`). (GroupBookingProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
fulfilment:
  method: bulkPdf
  recipients: organiser
  release: 2026-12-08 09:00
```

#### Permissions

- `listGroupTicketFulfillment` → `ORDER_VIEW` (read) · staff
- `setGroupTicketFulfillment` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group fulfilment via email/WhatsApp with reprint/resend. Group check-in status (arrived/checked-in vs not yet arrived) is tracked separately from the access-control scan, to run dedicated group counters. *(agreed · MoM 31 Aug 2026, 4.8 Group Operations, Payment Links & Check-In · DI-568)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-279` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-279`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 2
- Flow F137 *Group Sales Corporate Booking Management board 2: Group Booking Operations …*, step 10: Works in Group Ticket Fulfillment & Distribution → Control how tickets and other credentials are delivered to the group.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (404, 409, 412).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-279?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: POS Print, Physical Collection, Save fulfilment.
- [ ] Every transition is wired: `BO-274`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-280` Group Arrival, Check-In & Admission Operations

**Manage the physical arrival and admission of large groups efficiently.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `groupBookingId` (navigation) |
| Route | `/sell/group-arrival-check-in-admission-operations-bo-280` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The group's arrival: count arrived, extra guests, leaders, gate, issues; group check-in is distinct from the access scan.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listGroupArrivalCheck return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listGroupArrivalCheck carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listGroupArrivalCheck; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Form: Record group check in** (modal, opened by *Record group check in*; *Record group check in* calls `recordGroupCheckIn`, *Cancel* sends nothing)

**Collects what `recordGroupCheckIn` sends before it is called.** Required: `arrivedCount`. Optional: `additionalGuests`, `staffLeadersCount`, `arrivalGateId`, `actualArrivalAt`, `checkInIssues`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Arrived count `arrivedCount` | number field | required | — | min 0 | — | Members of the booked group who have arrived. | `recordGroupCheckIn` body |
| Additional guests `additionalGuests` | number field | optional | 0 | min 0 | — | People who arrived beyond the booked size; they still need entitlements to be admitted. | `recordGroupCheckIn` body |
| Staff leaders count `staffLeadersCount` | number field | optional | 0 | min 0 | — | — | `recordGroupCheckIn` body |
| Arrival gate `arrivalGateId` | picker: choose an arrival gate | optional | — | — | shows names, sends the id | — | `recordGroupCheckIn` body |
| Actual arrival at `actualArrivalAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Defaults to now on the first call; later calls keep the first arrival time. | `recordGroupCheckIn` body |
| Check in issues `checkInIssues` | multi-select chips | optional | — | Missing guest · Extra guest · Invalid ticket · Wrong date · Late arrival · Payment hold · Missing credential · Accessibility requirement | — | — | `recordGroupCheckIn` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The booking is cancelled (`groupClosed`). (GroupBookingProblem)

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **arrival**: Arrived count against confirmed, issues as chips (missing guest, extra guest, invalid ticket). *(source: contracts/spine/orders.yaml#recordGroupCheckIn)*

#### Outputs: what the screen shows and produces

**Shown**

**Every group arrival check-in** (data table, from `listGroupArrivalCheck`)

| Shows | Format | Notes |
|---|---|---|
| Groups expected today | text | Groups Expected Today |
| Arrival time | 1 Oct 2026, 14:30 | Arrival Time |
| Actual arrival | text | Actual Arrival |
| Group size | text | Group Size |
| Checked in | text | Checked In |
| Remaining | text | Remaining |
| Gate | text | Gate |
| Group leader | text | Group Leader |
| Readiness | text | Readiness |
| Issues | list or chips (count when long) | Arrival issues raised. |

**The selected group arrival check-in** (detail panel): The pack groups this record's detail under its own headings: “Single Group Check-In”, “Batch Check-In”, “Individual Check-In”, “Group Arrives”, “Handle”, “Integration”.

| Shows | Format | Notes |
|---|---|---|
| Groups expected today | text | Groups Expected Today |
| Arrival time | 1 Oct 2026, 14:30 | Arrival Time |
| Actual arrival | text | Actual Arrival |
| Group size | text | Group Size |
| Checked in | text | Checked In |
| Remaining | text | Remaining |
| Gate | text | Gate |
| Group leader | text | Group Leader |
| Readiness | text | Readiness |
| Issues | list or chips (count when long) | Arrival issues raised. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Record group check in (primary button) | `recordGroupCheckIn` POST `/group-bookings/{groupBookingId}/check-in` | GroupCheckInRequest | GroupVisitPlan | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ORDER_MODIFY`; opens modal first |

**Data it reads**: `listGroupArrivalCheck` (onLoad, Group Arrival, Check-In & Admission Operations)

**Where the user goes next**

- → `BO-274` Group Booking Operations Command Center: *Returns to the board's landing screen*; calls `listGroupArrivalCheck`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group arrival check-in list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group arrival check-in untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group arrival check-in yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group arrival check-in are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 The booking is cancelled (`groupClosed`). (GroupBookingProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
arrival:
  group: Al Noor Academy
  arrived: 29
  confirmed: 31
  leaders: 3
  gate: Gate 2
```

#### Permissions

- `listGroupArrivalCheck` → `ORDER_VIEW` (read) · staff
- `recordGroupCheckIn` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group check-in is a status distinct from the access scan: the group arrival screen records "Record group check in" separately. *(agreed · MoM 31 Aug 2026, Key Decisions · DI-590)*
- Group fulfilment via email/WhatsApp with reprint/resend. Group check-in status (arrived/checked-in vs not yet arrived) is tracked separately from the access-control scan, to run dedicated group counters. *(agreed · MoM 31 Aug 2026, 4.8 Group Operations, Payment Links & Check-In · DI-568)*

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-280` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-280`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 2
- Flow F137 *Group Sales Corporate Booking Management board 2: Group Booking Operations …*, step 12: Works in Group Arrival, Check-In & Admission Operations → Manage the physical arrival and admission of large groups efficiently.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-280?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Record group check in.
- [ ] Every transition is wired: `BO-274`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-281` Group Amendments, Cancellation & Refund Operations

**Manage changes occurring after group confirmation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_RESCHEDULE`, `ORDER_VIEW` (2 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `groupBookingId` (navigation), `orderId` (navigation) · cold entry: Opened from BO-274 with the group booking picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and … |
| Route | `/sell/group-amendments-cancellation-refund-operations-bo-281` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Changes after a group is confirmed: numbers, dates, cancellation and refund under policy.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listGroupAmendmentCancellation return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listGroupAmendmentCancellation carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listGroupAmendmentCancellation; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Increase Guest Count (primary button) | navigation or local | — | — | — | — |
| Reduce Guest Count (secondary button) | navigation or local | — | — | — | — |
| Date Change (secondary button) | navigation or local | — | — | — | — |
| Time Change (secondary button) | navigation or local | — | — | — | — |
| Product Change (secondary button) | navigation or local | — | — | — | — |
| Package Change (secondary button) | navigation or local | — | — | — | — |
| Seat Change (secondary button) | navigation or local | — | — | — | — |
| Catering Change (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **amendment list**: Each amendment with financial effect. *(source: contracts/spine/orders.yaml#listGroupAmendmentCancellation)*

**Data it reads**: `listGroupAmendmentCancellation` (onLoad, Group Amendments, Cancellation & Refund Operations)

**Where the user goes next**

- → `BO-274` Group Booking Operations Command Center: *Returns to the board's landing screen*; calls `listGroupAmendmentCancellation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group amendments cancellation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group amendments cancellation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group amendments cancellation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group amendments cancellation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem); 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem); 409 The status change goes backwards (`statusBackwards`), or the group is already cancelled or … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
amendment:
  group: Gulf Engineering
  change: 120 to 104 guests
  refund: AED 4,800.00
```

#### Permissions

- `listGroupAmendmentCancellation` → `ORDER_VIEW` (read) · staff
- `updateGroupBooking` → `ORDER_MODIFY` (operate) · staff
- `rescheduleOrder` → `ORDER_RESCHEDULE` (operate) · staff, partner
- `modifyOrder` → `ORDER_MODIFY` (operate) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.17 | Ticket Rebooking - System shall support ticket rebooking. | Guest Mobile App & Branding | CONTRACTED | `rescheduleOrder` |
| 19.2.18 | Visit Date Changes - System shall support changing visit dates. | Guest Mobile App & Branding | CONTRACTED | `rescheduleOrder` |
| 19.2.79 | Self-Service Ticket Changes - System shall support self-service ticket changes. | Guest Mobile App & Branding | CONTRACTED | `rescheduleOrder` |
| 1.1.19 | System shall allow guests to reschedule visit dates within configurable rules, fees, blackout periods and availability constraints. | Ticketing Catalogue | CONTRACTED | `rescheduleOrder` |
| 2.6.21 | Configurable, fee-based self-service reschedule or without any fees / refund transactions (no call-center dependency) | Ticketing Sales | CONTRACTED | `rescheduleOrder` |
| 2.6.41 | Customer should be able to reschedule the tickets based on the reschedule policy | Ticketing Sales | CONTRACTED | `rescheduleOrder` |
| 2.7.9 | Unused tickets support self-service rescheduling or refunds. | Ticketing Sales | CONTRACTED | `rescheduleOrder` |
| 2.12.2 | The system should allow for order adjustments. Following adjustments should be supported: - Users to refund guests (with supervisor approval) - Users to manually adjust guest orders (date, time … | Ticketing Sales | CONTRACTED | `modifyOrder` |
| 2.12.26 | Based on user’s privileges, an order can be modified or cancelled | Ticketing Sales | CONTRACTED | `modifyOrder` |

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A75** Design the refund engine: a six-step ledger-to-gateway refund flow with configurable time-banded percentages, an authorized-approver override, partial refunds, both operations- and customer-initiated requests, plus bulk … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 12 Aug 2026 · workshop tracker · keyword 'refund')*
- **A80** Implement a currency-locking rule for refunds/change: always issue in the local/base currency, locked at the value recorded at time of purchase; track foreign-currency activity only via a separate report *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 14 Aug 2026 · workshop tracker · keyword 'refund')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'refund')*
- **A140** Centralise policy management (reschedule, exchange, refund, cancellation, upgrade, downgrade, ownership transfer, membership conversion) with each product mapped to pricing, GL code, promotions and channels *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'refund')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'refund')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'refund')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-281` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-281`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 2
- Flow F137 *Group Sales Corporate Booking Management board 2: Group Booking Operations …*, step 14: Works in Group Amendments, Cancellation & Refund Operations → Manage changes occurring after group confirmation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404, 409, 412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-281?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Increase Guest Count, Reduce Guest Count, Date Change, Time Change, Product Change, Package Change, Seat Change, Catering Change.
- [ ] Every transition is wired: `BO-274`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_RESCHEDULE`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-282` Group Booking Reconciliation, Closure & Performance

**Close the group booking after the visit and reconcile what was sold against what actually occurred.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Measure; Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/group-booking-reconciliation-closure-performance-bo-282` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Close a group after the visit: sold vs used, payments reconciled, performance.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listGroupBookingReconciliation return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listGroupBookingReconciliation carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listGroupBookingReconciliation; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every group booking reconciliation** (data table, from `listGroupBookingReconciliation`)

| Shows | Format | Notes |
|---|---|---|
| Final booking value | text | Final Booking Value |
| Amount paid | AED 1,234.50 | Amount Paid |
| Refunds | 1,234 | Refunds |
| Additional charges | 1,234 | Additional Charges |
| Outstanding balance | AED 1,234.50 | Outstanding Balance |
| Final revenue | AED 1,234.50 | Final Revenue |

**The selected group booking reconciliation** (detail panel): The pack groups this record's detail under its own headings: “Quoted”, “Booked”, “Paid”, “Allocated”, “Issued”, “Attended”.

| Shows | Format | Notes |
|---|---|---|
| Final booking value | text | Final Booking Value |
| Amount paid | AED 1,234.50 | Amount Paid |
| Refunds | 1,234 | Refunds |
| Additional charges | 1,234 | Additional Charges |
| Outstanding balance | AED 1,234.50 | Outstanding Balance |
| Final revenue | AED 1,234.50 | Final Revenue |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **reconciliation**: Booked, arrived, used, paid, outstanding. *(source: contracts/spine/orders.yaml#listGroupBookingReconciliation)*

**Data it reads**: `listGroupBookingReconciliation` (onLoad, Group Booking Reconciliation, Closure & Performance)

**Where the user goes next**

- → `BO-274` Group Booking Operations Command Center: *Returns to the board's landing screen*; calls `listGroupBookingReconciliation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group booking reconciliation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group booking reconciliation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group booking reconciliation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group booking reconciliation are still there. The pack's own statuses are Operationally Complete → Financially Complete → Closed — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
closure:
  booked: 31
  arrived: 29
  paid: AED 36,000.00
  outstanding: AED 0.00
```

#### Permissions

- `listGroupBookingReconciliation` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker · keyword 'ticket-booking ux')*
- **A46** Evaluate a dynamic bundle/package builder that auto-applies a discount when a guest adds multiple product types (ticket + F&B + retail) to cart, in addition to pre-defined packages *(Reshma Bandiwdekar · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'cart')*
- **A96** Build the journey library (abandoned cart with min-value/product filters, birthday, anniversary, cross-sell, survey — all consent-gated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'cart')*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'b2c checkout')*
- **A157** Keep F&B and retail online sale entirely within the platform (browse, cart, checkout, pickup or ship) with no redirect to a separate app *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 26 Aug 2026 · workshop tracker · keyword 'cart')*
- **A158** Obtain the resource-management reference documentation, review the hardware/ticketing docs, route follow-up questions to Qossai, and review the House of Wisdom booking flow as a UX reference *(Allam / Chinmay Parab / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 26 Aug 2026 · workshop tracker · keyword 'booking flow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-282` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-282`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 2
- Flow F137 *Group Sales Corporate Booking Management board 2: Group Booking Operations …*, step 16: Works in Group Booking Reconciliation, Closure & Performance → Close the group booking after the visit and reconcile what was sold against what actually occurred.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-282?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-274`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-283` Group Sales Analytics & AI Intelligence Center

**Provide management with intelligence across the complete group-sales lifecycle. This should combine data from Board 1 + Board 2.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Sell · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Analyze) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/sell/group-sales-analytics-ai-intelligence-center-bo-283` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Management intelligence across group sales: conversion, value, seasonality, AI insights.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listGroupSale2, listGroupSale return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listGroupSale2 carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listGroupSale2 / contracts/spine/orders.yaml#listGroupSale; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search group sales analytics | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by customer type, organization, venue, event, sales owner, group type and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Customer type | text field | — | — | `listGroupSale2` ?customerType |
| Organization | text field | — | — | `listGroupSale2` ?organization |
| Venue | text field | — | — | `listGroupSale2` ?venue |
| Event | text field | — | — | `listGroupSale2` ?event |
| Sales owner | text field | — | — | `listGroupSale2` ?salesOwner |
| Group type | text field | — | — | `listGroupSale2` ?groupType |
| Product | text field | — | — | `listGroupSale2` ?product |
| Date | text field | — | — | `listGroupSale2` ?date |
| Campaign | text field | — | — | `listGroupSale2` ?campaign |
| Market | text field | — | — | `listGroupSale2` ?market |

#### Outputs: what the screen shows and produces

**Shown**

**Every group sales analytics** (data table, from `listGroupSale2`)

| Shows | Format | Notes |
|---|---|---|
| Enquiries | text | Enquiries |
| Quotes | text | Quotes |
| Conversion rate | 12.5% | Conversion Rate |
| Group bookings | text | Group Bookings |
| Guests | text | Guests |
| Revenue | AED 1,234.50 | Revenue |
| Average group size | 1,234.5 | Average Group Size |
| Average booking value | 1,234.5 | Average Booking Value |
| Discount | 1,234.5 | Discount % |
| Revenue per guest | AED 1,234.50 | Revenue per Guest |
| Cancellation rate | 12.5% | Cancellation Rate |
| No show rate | 12.5% | No-Show Rate |
| Outstanding receivables | text | Outstanding Receivables |
| Repeat customer rate | 12.5% | Repeat Customer Rate |

**The selected group sales analytics** (detail panel): The pack groups this record's detail under its own headings: “Visualize”, “Conversion Insight”, “Pricing Insight”, “Capacity Insight”, “Operational Insight”, “Natural-Language Copilot”.

| Shows | Format | Notes |
|---|---|---|
| Enquiries | text | Enquiries |
| Quotes | text | Quotes |
| Conversion rate | 12.5% | Conversion Rate |
| Group bookings | text | Group Bookings |
| Guests | text | Guests |
| Revenue | AED 1,234.50 | Revenue |
| Average group size | 1,234.5 | Average Group Size |
| Average booking value | 1,234.5 | Average Booking Value |
| Discount | 1,234.5 | Discount % |
| Revenue per guest | AED 1,234.50 | Revenue per Guest |
| Cancellation rate | 12.5% | Cancellation Rate |
| No show rate | 12.5% | No-Show Rate |
| Outstanding receivables | text | Outstanding Receivables |
| Repeat customer rate | 12.5% | Repeat Customer Rate |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **analytics**: KPIs with deltas (DI-041) and insight cards (DI-043). *(source: contracts/spine/orders.yaml#listGroupSale2)*

**Data it reads**: `listGroupSale2` (onLoad, Group Sales Analytics & AI Intelligence Center); `listGroupSale` (onLoad, Group Sales Command Center)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group sales analytics list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group sales analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group sales analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the group sales analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  conversion: 39%
  averageGroup: 46
  value: AED 1.2m YTD
```

#### Permissions

- `listGroupSale2` → `ORDER_VIEW` (read) · staff
- `listGroupSale` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 4 for P08 · Sell, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-283` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS69 Group Sales   Corporate Booking Management Board 2.dc.html#bo-283`
- Workshop pack: Group_Sales___Corporate_Booking_Management_Reference.pdf board 2
- Flow F137 *Group Sales Corporate Booking Management board 2: Group Booking Operations …*, step 18: Works in Group Sales Analytics & AI Intelligence Center → Provide management with intelligence across the complete group-sales lifecycle. This should combine data from Board 1 + Board 2.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-283?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
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

### In P08 · Sell

- Allam: back-end configuration is the most critical part; the screens must make visually clear how administrators configure products, pricing per channel, attributes/components, entitlements, validity and access permissions, comparable to the structured product/metric-sheet approach of an earlier reference system. *(agreed · MoM 24 Sep 2026, 4.3 Back-End Configuration Detail — Requested Format (Screens, Not Just Functional Lists) · DI-985)*
- Chinmay: reduce the number of configuration screens/pages and consolidate related settings/toggles to avoid a long, click-heavy admin flow; Allam agreed, citing the previous system's demo as a starting reference. *(agreed · MoM 25 Aug 2026, 4.11 UX Simplification & Distributed Inventory · DI-474)*
- Retail dashboard gives a consolidated real-time view across outlets — total retail sales, total and average transactions, store performance snapshot, system alerts and out-of-stock indicators — viewable by day, week or month. *(client request · MoM 19 Aug 2026, 4.1 Retail Command Center — Dashboard & Store Setup · DI-349)*
- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*

**10 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listGroupAmendmentCancellation": {"method":"GET","path":"/group-amendment-cancellation","contract":"orders","summary":"Group Amendments, Cancellation & Refund Operations","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GroupAmendmentsCancellationRefundOperationsView"},
"listGroupArrivalCheck": {"method":"GET","path":"/group-arrival-check","contract":"orders","summary":"Group Arrival, Check-In & Admission Operations","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GroupArrivalCheckInAdmissionOperationsView"},
"listGroupBooking": {"method":"GET","path":"/group-booking","contract":"orders","summary":"Group Booking Operations Command Center","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GroupBookingOperationsCommandCenterView"},
"listGroupBookingReconciliation": {"method":"GET","path":"/group-booking-reconciliation","contract":"orders","summary":"Group Booking Reconciliation, Closure & Performance","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GroupBookingReconciliationClosurePerformanceView"},
"listGroupPaymentDeposit": {"method":"GET","path":"/group-payment-deposit","contract":"orders","summary":"Group Payment, Deposit & Balance Management","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GroupPaymentDepositBalanceManagementView"},
"listGroupSale": {"method":"GET","path":"/group-sale","contract":"orders","summary":"Group Sales Command Center","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GroupSalesCommandCenterView"},
"listGroupSale2": {"method":"GET","path":"/group-sale-2","contract":"orders","summary":"Group Sales Analytics & AI Intelligence Center","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"customerType","in":"query","required":false},{"name":"organization","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"salesOwner","in":"query","required":false},{"name":"groupType","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"date","in":"query","required":false},{"name":"campaign","in":"query","required":false},{"name":"market","in":"query","required":false}],"requestBody":null,"responds":"GroupSalesAnalyticsAiIntelligenceCenterView"},
"listGroupTicketFulfillment": {"method":"GET","path":"/group-ticket-fulfillment","contract":"orders","summary":"Group Ticket Fulfillment & Distribution","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GroupTicketFulfillmentDistributionView"},
"listGroupTicketSeat": {"method":"GET","path":"/group-ticket-seat","contract":"orders","summary":"Group Ticket, Seat & Entitlement Allocation","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GroupTicketSeatEntitlementAllocationView"},
"listParticipantGuestList": {"method":"GET","path":"/participant-guest-list","contract":"orders","summary":"Participants, Guest Lists & Group Structure","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ParticipantsGuestListsGroupStructureView"},
"modifyOrder": {"method":"POST","path":"/orders/{orderId}/modify","contract":"orders","summary":"Add or remove lines on an existing order","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ModifyOrderRequest","responds":"OrderModificationResult"},
"recordGroupCheckIn": {"method":"POST","path":"/group-bookings/{groupBookingId}/check-in","contract":"orders","summary":"Record a group's arrival at the venue","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GroupCheckInRequest","responds":"GroupVisitPlan"},
"rescheduleOrder": {"method":"POST","path":"/orders/{orderId}/reschedule","contract":"orders","summary":"Move an order to another performance","permission":"ORDER_RESCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderExchangeResult"},
"setGroupOperationalPlanning": {"method":"PUT","path":"/group-operational-planning","contract":"orders","summary":"Group Operational Planning & Task Workspace","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"GroupOperationalPlanningTaskWorkspaceInput","responds":"GroupOperationalPlanningTaskWorkspaceView"},
"setGroupPaymentSchedule": {"method":"PUT","path":"/group-bookings/{groupBookingId}/payment-schedule","contract":"orders","summary":"Set a group's payment schedule","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"GroupPaymentScheduleInput","responds":"GroupPaymentScheduleView"},
"setGroupTicketAllocation": {"method":"PUT","path":"/group-bookings/{groupBookingId}/allocation","contract":"orders","summary":"Set how a group's tickets are allocated","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"GroupTicketAllocationInput","responds":"GroupTicketAllocationView"},
"setGroupTicketFulfillment": {"method":"PUT","path":"/group-bookings/{groupBookingId}/fulfillment","contract":"orders","summary":"Set how a group's tickets are delivered","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"GroupTicketFulfillmentInput","responds":"GroupTicketFulfillmentView"},
"setParticipantGuestList": {"method":"PUT","path":"/group-bookings/{groupBookingId}/participants","contract":"orders","summary":"Set a group's participant list","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"ParticipantGuestListInput","responds":"ParticipantGuestListView"},
"updateGroupBooking": {"method":"PATCH","path":"/group-bookings/{groupBookingId}","contract":"orders","summary":"Confirm numbers, change the leader or cancel a group","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"UpdateGroupBookingRequest","responds":"GroupBooking"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CreateOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","variantId","quantity","quotedUnitPrice"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these."},"variantId":{"type":"string","format":"uuid"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"inventoryHoldId":{"type":"string","nullable":true,"description":"Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"},"description":"Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"quantity":{"type":"integer","minimum":1},"eligibilityDeclaration":{"type":"array","nullable":true,"x-ticvai-note":"One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n","items":{"type":"object","properties":{"ageBand":{"type":"string","enum":["infant","child","junior","adult","senior"],"description":"Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."},"ageYears":{"type":"integer","nullable":true},"heightBandIndex":{"type":"integer","nullable":true},"confidentSwimmer":{"type":"boolean","nullable":true,"description":"**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"},"guardianSigned":{"type":"boolean"}}},"description":"What was declared for each guest on this line, kept as the record staff check at the gate."},"quotedUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the client charged, from its local bundle."},"holderName":{"type":"string","nullable":true},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"}}},
"GroupAmendmentsCancellationRefundOperationsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Amendments, Cancellation & Refund Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"originalValue":{"type":"string","description":"Original Value"},"newValue":{"type":"integer","description":"New Value"},"additionalCharge":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Additional Charge"},"refundCredit":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Refund/Credit"},"fees":{"type":"string","description":"Fees"},"ticketsAdded":{"type":"string","description":"Tickets added"},"ticketsReleased":{"type":"string","description":"Tickets released"},"seatsAffected":{"type":"integer","description":"Seats affected"},"guides":{"type":"string","description":"Guides"},"rooms":{"type":"string","description":"Rooms"},"equipment":{"type":"string","description":"Equipment"},"tasks":{"type":"string","description":"Tasks"},"tickets":{"type":"string","description":"Tickets"},"guestLists":{"type":"string","description":"Guest lists"},"amendmentType":{"type":"string","enum":["increaseGuestCount","reduceGuestCount","dateChange","timeChange","productChange","packageChange","seatChange","cateringChange","resourceChange","fullCancellation","partialCancellation"],"description":"Amendment requested."},"approvalReasons":{"type":"array","items":{"type":"string","enum":["lateCancellation","waivedFee","largeRefund","capacityOverride","contractException"]},"description":"Exceptions that trigger approval."}}},
"GroupArrivalCheckInAdmissionOperationsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Arrival, Check-In & Admission Operations displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"groupsExpectedToday":{"type":"string","description":"Groups Expected Today"},"arrivalTime":{"type":"string","format":"date-time","description":"Arrival Time"},"actualArrival":{"type":"string","description":"Actual Arrival"},"groupSize":{"type":"string","description":"Group Size"},"checkedIn":{"type":"string","description":"Checked In"},"remaining":{"type":"string","description":"Remaining"},"gate":{"type":"string","description":"Gate"},"groupLeader":{"type":"string","description":"Group Leader"},"readiness":{"type":"string","description":"Readiness"},"booked":{"type":"string","description":"Booked"},"expected":{"type":"string","description":"Expected"},"arrived":{"type":"string","description":"Arrived"},"noShow":{"type":"string","description":"No-Show"},"additionalGuests":{"type":"string","description":"Additional Guests"},"staffLeaders":{"type":"string","description":"Staff/Leaders"},"issues":{"type":"array","items":{"type":"string","enum":["missingGuest","extraGuest","invalidTicket","wrongDate","lateArrival","paymentHold","missingCredential","accessibilityRequirement"]},"description":"Arrival issues raised."}}},
"GroupBooking": {"type":"object","x-ticvai-persistence":"orders.group_booking","description":"BL-028. **`BO-026 Group Bookings` ran on generic order operations** — no group size, no quota, no leader, no per-attendee capture.\n**The leader is the point.** A school booking forty places has one person who pays, one who is called if the coach is late, and forty who need names collecting — and a generic order has one guest.\n","required":["id","orderId","leaderSubjectId","expectedSize","status"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["general","school","corporate","party"],"default":"general"},"packageProductId":{"type":"string","nullable":true,"description":"The school-trip format or party package."},"yearGroup":{"type":"string","maxLength":40,"nullable":true},"accessAndDietaryNeeds":{"type":"string","maxLength":1000,"nullable":true},"celebrantName":{"type":"string","maxLength":120,"nullable":true,"description":"The birthday child."},"celebrantTurningAge":{"type":"integer","minimum":1,"maximum":18,"nullable":true},"allergiesAndRequests":{"type":"string","maxLength":1000,"nullable":true},"finalHeadcountDueBy":{"type":"string","format":"date-time","nullable":true},"quoteSentAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"riskAssessmentSentAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"preferredDate":{"type":"string","format":"date","nullable":true,"description":"The date the guest asked for on `requestGroupBooking` — what its `409 dateUnavailable` is checked against. Null for a group a member of staff built from an order."},"orderId":{"type":"string","format":"uuid"},"leaderSubjectId":{"type":"string","format":"uuid"},"organisationName":{"type":"string","nullable":true},"expectedSize":{"type":"integer"},"confirmedSize":{"type":"integer","nullable":true},"minimumSize":{"type":"integer","nullable":true,"description":"**Below which the group rate does not apply.** A booking for forty that arrives as twelve is a pricing question somebody has to answer at the gate, and stating the threshold means answering it at booking instead.\n"},"attendeeCaptureRequired":{"type":"boolean","default":false,"description":"**Whether names are needed before admission.** A school trip usually needs them and a corporate day out usually does not, and the difference is a safeguarding requirement rather than a preference.\n"},"attendeeCaptureDueBy":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["provisional","confirmed","namesPending","complete","cancelled"]}}},
"GroupBookingOperationsCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Booking Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"upcomingGroups":{"type":"integer","description":"Upcoming Groups"},"groupsToday":{"type":"string","description":"Groups Today"},"expectedGuestsToday":{"type":"string","description":"Expected Guests Today"},"groupsAwaitingDeposit":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Groups Awaiting Deposit"},"guestListsPending":{"type":"integer","description":"Guest Lists Pending"},"ticketsPending":{"type":"integer","description":"Tickets Pending"},"resourcesPending":{"type":"integer","description":"Resources Pending"},"groupsReady":{"type":"string","description":"Groups Ready"},"groupsWithIssues":{"type":"integer","description":"Groups With Issues"},"outstandingPayments":{"type":"integer","description":"Outstanding Payments"},"checkInsToday":{"type":"string","description":"Check-Ins Today"},"completedGroups":{"type":"integer","description":"Completed Groups"},"groupBookingId":{"type":"string","description":"Group Booking ID"},"organization":{"type":"string","description":"Organization"},"groupType":{"type":"string","description":"Group Type"},"venueEvent":{"type":"string","description":"Venue/Event"},"visitDate":{"type":"string","format":"date-time","description":"Visit Date"},"arrivalTime":{"type":"string","format":"date-time","description":"Arrival Time"},"guests":{"type":"integer","description":"Guests"},"bookingValue":{"type":"string","description":"Booking Value"},"paymentStatus":{"type":"integer","description":"Payment Status"},"guestListStatus":{"type":"integer","description":"Guest List Status"},"ticketStatus":{"type":"integer","description":"Ticket Status"},"resourceStatus":{"type":"integer","description":"Resource Status"},"readiness":{"type":"number","description":"Readiness %"},"operationalOwner":{"type":"string","description":"Operational Owner"}}},
"GroupBookingReconciliationClosurePerformanceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Booking Reconciliation, Closure & Performance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"finalBookingValue":{"type":"string","description":"Final Booking Value"},"amountPaid":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount Paid"},"refunds":{"type":"integer","description":"Refunds"},"additionalCharges":{"type":"integer","description":"Additional Charges"},"outstandingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Outstanding Balance"},"finalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Final Revenue"},"mealsBookedVsRedeemed":{"type":"string","description":"Meals booked vs redeemed"},"workshopsBookedVsAttended":{"type":"string","description":"Workshops booked vs attended"},"parkingUsed":{"type":"string","description":"Parking used"},"merchandiseFulfilled":{"type":"string","description":"Merchandise fulfilled"},"resourcesConsumed":{"type":"string","description":"Resources consumed"},"admissionReconciled":{"type":"string","description":"Admission reconciled"},"financeReconciled":{"type":"string","description":"Finance reconciled"},"refundsResolved":{"type":"string","description":"Refunds resolved"},"resourcesClosed":{"type":"integer","description":"Resources closed"},"attendance":{"type":"integer","description":"Attendance %"},"noShow":{"type":"number","description":"No-Show %"},"revenuePerGuest":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue per Guest"},"packageAttachment":{"type":"string","description":"Package Attachment"},"operationalIssues":{"type":"string","description":"Operational Issues"},"customerFeedbackCaptured":{"type":"string","description":"Customer feedback captured where applicable"},"customerSatisfaction":{"type":"string","description":"Customer Satisfaction where available"}}},
"GroupCheckInRequest": {"type":"object","x-ticvai-persistence":"none — request only; lands in the check-in columns of `orders.group_visit_plan`","description":"**What the group check-in desk records** (BO-280). Counts are the running totals for the group, not increments: a second call as the rest of the group arrives sends the new totals.","required":["arrivedCount"],"properties":{"arrivedCount":{"type":"integer","minimum":0,"description":"Members of the booked group who have arrived."},"additionalGuests":{"type":"integer","minimum":0,"default":0,"description":"People who arrived beyond the booked size; they still need entitlements to be admitted."},"staffLeadersCount":{"type":"integer","minimum":0,"default":0},"arrivalGateId":{"type":"string","format":"uuid","nullable":true},"actualArrivalAt":{"type":"string","format":"date-time","nullable":true,"description":"Defaults to now on the first call; later calls keep the first arrival time."},"checkInIssues":{"type":"array","items":{"type":"string","enum":["missingGuest","extraGuest","invalidTicket","wrongDate","lateArrival","paymentHold","missingCredential","accessibilityRequirement"]}}}},
"GroupOperationalPlanningTaskWorkspaceInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in `orders.group_visit_plan` and `orders.group_task` (DM5, 29 September)","description":"**What Group Operational Planning & Task Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *Each task should contain* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.","properties":{"arrivalDate":{"type":"string","format":"date-time","description":"Arrival Date"},"arrivalTime":{"type":"string","format":"date-time","description":"Arrival Time"},"arrivalLocation":{"type":"string","description":"Arrival Location"},"groupMeetingPoint":{"type":"string","description":"Group Meeting Point"},"entryGate":{"type":"string","description":"Entry Gate"},"departureTime":{"type":"string","format":"date-time","description":"Departure Time"},"groupSize":{"type":"string","description":"Group Size"},"groupLeaders":{"type":"string","description":"Group Leaders"},"contactPerson":{"type":"string","description":"Contact Person"},"ticketingMethod":{"type":"string","description":"Ticketing Method"},"seating":{"type":"string","description":"Seating"},"guides":{"type":"string","description":"Guides"},"catering":{"type":"string","description":"Catering"},"transportation":{"type":"string","description":"Transportation"},"parking":{"type":"string","description":"Parking"},"accessibility":{"type":"string","description":"Accessibility"},"equipment":{"type":"string","description":"Equipment"},"specialRequirements":{"type":"string","description":"Special Requirements"},"tasks":{"type":"array","description":"Department tasks","items":{"type":"object","properties":{"department":{"type":"string","description":"Department"},"task":{"type":"string","description":"Task"},"owner":{"type":"string","description":"Owner"},"dueDate":{"type":"string","format":"date-time","description":"Due date"},"dueTime":{"type":"string","description":"Due time"},"priority":{"type":"string","description":"Priority"},"dependency":{"type":"string","description":"Dependency"},"status":{"type":"string","description":"Status"},"notes":{"type":"string","description":"Notes"}}}}},"x-ticvai-record-definition":"Each task should contain"},
"GroupOperationalPlanningTaskWorkspaceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Operational Planning & Task Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"arrivalDate":{"type":"string","format":"date-time","description":"Arrival Date"},"arrivalTime":{"type":"string","format":"date-time","description":"Arrival Time"},"arrivalLocation":{"type":"string","description":"Arrival Location"},"groupMeetingPoint":{"type":"string","description":"Group Meeting Point"},"entryGate":{"type":"string","description":"Entry Gate"},"departureTime":{"type":"string","format":"date-time","description":"Departure Time"},"groupSize":{"type":"string","description":"Group Size"},"groupLeaders":{"type":"string","description":"Group Leaders"},"contactPerson":{"type":"string","description":"Contact Person"},"ticketingMethod":{"type":"string","description":"Ticketing Method"},"seating":{"type":"string","description":"Seating"},"guides":{"type":"string","description":"Guides"},"catering":{"type":"string","description":"Catering"},"transportation":{"type":"string","description":"Transportation"},"parking":{"type":"string","description":"Parking"},"accessibility":{"type":"string","description":"Accessibility"},"equipment":{"type":"string","description":"Equipment"},"specialRequirements":{"type":"string","description":"Special Requirements"},"tasks":{"type":"array","description":"Department tasks, e.g. admissions prepare group entry, F&B confirm meal quantities, finance confirm payment","items":{"type":"object","properties":{"department":{"type":"string","description":"Department"},"task":{"type":"string","description":"Task"},"owner":{"type":"string","description":"Owner"},"dueDate":{"type":"string","format":"date-time","description":"Due date"},"dueTime":{"type":"string","description":"Due time"},"priority":{"type":"string","description":"Priority"},"dependency":{"type":"string","description":"Dependency"},"status":{"type":"string","description":"Status"},"notes":{"type":"string","description":"Notes"}}}}}},
"GroupPaymentDepositBalanceManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Payment, Deposit & Balance Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"bookingValue":{"type":"string","description":"Booking Value"},"depositRequired":{"type":"boolean","description":"Deposit Required"},"depositPaid":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Deposit Paid"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Balance"},"amountPaid":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount Paid"},"amountOutstanding":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount Outstanding"},"nextDueDate":{"type":"string","format":"date-time","description":"Next Due Date"},"paymentStatus":{"type":"integer","description":"Payment Status"},"deposit":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Deposit"},"finalBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Final Balance"},"scheduleType":{"type":"string","enum":["milestonePayment","installment","customSchedule"],"description":"Payment schedule."},"paymentMethods":{"type":"array","items":{"type":"string","enum":["paymentLink","card","bankTransfer","accountCredit","cash","otherApprovedMethod"]},"description":"Methods offered."}}},
"GroupPaymentScheduleInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `setGroupPaymentSchedule` takes. The milestones must sum to the group booking's total (decided 29 September, readiness close-out).","required":["scheduleType","milestones"],"properties":{"scheduleType":{"type":"string","description":"The shape of the schedule (decided 29 September, readiness close-out).","enum":["depositThenBalance","milestonePayment","finalBalance","customSchedule"]},"milestones":{"type":"array","minItems":1,"items":{"type":"object","required":["dueDate","amount"],"properties":{"dueDate":{"type":"string","format":"date"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"label":{"type":"string","maxLength":60,"nullable":true}}}}}},
"GroupPaymentScheduleView": {"type":"object","x-ticvai-persistence":"orders.group_payment_schedule + orders.group_payment_milestone","description":"**One group's payment schedule.** Written by `setGroupPaymentSchedule` (decided 29 September, readiness close-out); `DepositPolicy` stays the venue-wide default.\n","required":["groupBookingId","scheduleType","milestones"],"properties":{"groupBookingId":{"type":"string","format":"uuid","readOnly":true},"scheduleType":{"type":"string","enum":["depositThenBalance","milestonePayment","finalBalance","customSchedule"]},"total":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The group booking's total, which the milestones sum to."},"milestones":{"type":"array","items":{"type":"object","required":["id","dueDate","amount","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"dueDate":{"type":"string","format":"date"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"label":{"type":"string","maxLength":60,"nullable":true},"status":{"type":"string","readOnly":true,"enum":["due","paid","overdue"]}}}},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"GroupSalesAnalyticsAiIntelligenceCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Sales Analytics & AI Intelligence Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"enquiries":{"type":"string","description":"Enquiries"},"quotes":{"type":"string","description":"Quotes"},"conversionRate":{"type":"number","description":"Conversion Rate"},"groupBookings":{"type":"string","description":"Group Bookings"},"guests":{"type":"string","description":"Guests"},"revenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue"},"averageGroupSize":{"type":"number","description":"Average Group Size"},"averageBookingValue":{"type":"number","description":"Average Booking Value"},"discount":{"type":"number","description":"Discount %"},"revenuePerGuest":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue per Guest"},"cancellationRate":{"type":"number","description":"Cancellation Rate"},"noShowRate":{"type":"number","description":"No-Show Rate"},"outstandingReceivables":{"type":"string","description":"Outstanding Receivables"},"repeatCustomerRate":{"type":"number","description":"Repeat Customer Rate"},"additionalGroups":{"type":"string","description":"Additional groups"},"capacityUtilization":{"type":"integer","description":"Capacity utilization"},"discountCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount cost"},"expectedContribution":{"type":"string","description":"Expected contribution"}}},
"GroupSalesCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Sales Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"newEnquiries":{"type":"integer","description":"New Enquiries"},"quotationsOutstanding":{"type":"string","description":"Quotations Outstanding"},"quotesAwaitingApproval":{"type":"string","description":"Quotes Awaiting Approval"},"confirmedGroups":{"type":"integer","description":"Confirmed Groups"},"expectedGuests":{"type":"integer","description":"Expected Guests"},"pipelineValue":{"type":"string","description":"Pipeline Value"},"confirmedRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Confirmed Revenue"},"conversionRate":{"type":"number","description":"Conversion Rate"},"averageGroupValue":{"type":"number","description":"Average Group Value"},"expiringQuotes":{"type":"integer","description":"Expiring Quotes"},"salesTargetAchievement":{"type":"string","description":"Sales Target Achievement"},"enquiryId":{"type":"string","description":"Enquiry ID"},"organizationCustomer":{"type":"string","description":"Organization/Customer"},"groupType":{"type":"string","description":"Group Type"},"eventAttraction":{"type":"string","description":"Event/Attraction"},"visitDate":{"type":"string","format":"date-time","description":"Visit Date"},"guestCount":{"type":"integer","description":"Guest Count"},"salesOwner":{"type":"string","description":"Sales Owner"},"estimatedValue":{"type":"string","description":"Estimated Value"},"quoteStatus":{"type":"string","description":"Quote Status"},"probability":{"type":"string","description":"Probability"},"nextAction":{"type":"string","format":"date-time","description":"Next Action"},"expectedCloseDate":{"type":"string","format":"date-time","description":"Expected Close Date"},"followUpsDue":{"type":"string","description":"Follow-ups due"},"quotesExpiring":{"type":"string","description":"Quotes expiring"},"customerResponses":{"type":"integer","description":"Customer responses"},"approvalRequests":{"type":"integer","description":"Approval requests"},"depositsPending":{"type":"integer","description":"Deposits pending"}}},
"GroupTicketAllocationInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `setGroupTicketAllocation` takes (decided 29 September, readiness close-out).","required":["allocationMode","allocations"],"properties":{"allocationMode":{"type":"string","description":"How the group's tickets are allocated (decided 29 September, readiness close-out).","enum":["individualTicket","bulkTicket","namedTicket","quantityBasedTicket","zoneAllocation"]},"keepGroupTogether":{"type":"boolean","default":false},"vipAllocation":{"type":"boolean","default":false,"description":"Set aside the group's VIP places."},"allocations":{"type":"array","items":{"type":"object","required":["productId","quantity"],"properties":{"productId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"zoneId":{"type":"string","format":"uuid","nullable":true,"description":"Required for `zoneAllocation`."},"participantId":{"type":"string","format":"uuid","nullable":true,"description":"The participant a `namedTicket` line is for. Required for `namedTicket`."}}}}}},
"GroupTicketAllocationView": {"type":"object","x-ticvai-persistence":"orders.group_ticket_allocation + orders.group_ticket_allocation_line","description":"**How one group's tickets are allocated.** Written by `setGroupTicketAllocation` (decided 29 September, readiness close-out).\n","required":["groupBookingId","allocationMode","allocations"],"properties":{"groupBookingId":{"type":"string","format":"uuid","readOnly":true},"allocationMode":{"type":"string","enum":["individualTicket","bulkTicket","namedTicket","quantityBasedTicket","zoneAllocation"]},"keepGroupTogether":{"type":"boolean"},"vipAllocation":{"type":"boolean"},"allocations":{"type":"array","items":{"type":"object","required":["id","productId","quantity"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"productId":{"type":"string","format":"uuid"},"quantity":{"type":"integer","minimum":1},"zoneId":{"type":"string","format":"uuid","nullable":true},"participantId":{"type":"string","format":"uuid","nullable":true}}}},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"GroupTicketFulfillmentDistributionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Ticket Fulfillment & Distribution displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ticketsRequired":{"type":"boolean","description":"Tickets Required"},"generated":{"type":"string","description":"Generated"},"sent":{"type":"string","description":"Sent"},"delivered":{"type":"string","description":"Delivered"},"opened":{"type":"string","description":"Opened"},"downloaded":{"type":"string","description":"Downloaded"},"failed":{"type":"integer","description":"Failed"},"reissued":{"type":"string","description":"Reissued"},"guest":{"type":"string","description":"Guest"},"ticket":{"type":"string","description":"Ticket"},"seat":{"type":"string","description":"Seat"},"credential":{"type":"string","description":"Credential"},"entitlements":{"type":"string","description":"Entitlements"},"checkInStatus":{"type":"string","description":"Check-In Status"},"deliveryMethod":{"type":"string","enum":["oneGroupQr","individualQr","groupLeaderWallet","individualMobileTickets","email","posPrint","rfid","nfc","wristband","physicalCollection"],"description":"How the group receives credentials: one QR for a headcount, a QR each, or others (MoM 31 Aug)."},"distributionMode":{"type":"string","enum":["coordinator","eachParticipant","teachersTeamLeaders"],"description":"Who the credentials go to"}}},
"GroupTicketFulfillmentInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `setGroupTicketFulfillment` takes (decided 29 September, readiness close-out).","required":["method","recipients"],"properties":{"method":{"type":"string","description":"How the tickets are delivered (decided 29 September, readiness close-out).","enum":["email","sms","wallet","bulkPdf","posPrint","physicalCollection"]},"recipients":{"type":"string","description":"Who receives them (decided 29 September, readiness close-out).","enum":["organiser","eachParticipant"]},"releaseAt":{"type":"string","format":"date-time","nullable":true,"description":"Hold the tickets back until then; null releases them when the group is confirmed."}}},
"GroupTicketFulfillmentView": {"type":"object","x-ticvai-persistence":"orders.group_ticket_fulfillment","description":"**How one group's tickets reach them.** Written by `setGroupTicketFulfillment` (decided 29 September, readiness close-out).\n","required":["groupBookingId","method","recipients"],"properties":{"groupBookingId":{"type":"string","format":"uuid","readOnly":true},"method":{"type":"string","enum":["email","sms","wallet","bulkPdf","posPrint","physicalCollection"]},"recipients":{"type":"string","enum":["organiser","eachParticipant"]},"releaseAt":{"type":"string","format":"date-time","nullable":true},"releasedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"GroupTicketSeatEntitlementAllocationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Group Ticket, Seat & Entitlement Allocation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"product":{"type":"string","description":"Product"},"quantityBooked":{"type":"integer","description":"Quantity Booked"},"quantityAllocated":{"type":"integer","description":"Quantity Allocated"},"remaining":{"type":"string","description":"Remaining"},"ticketType":{"type":"string","description":"Ticket Type"},"seatZone":{"type":"string","description":"Seat/Zone"},"guestSubgroup":{"type":"string","description":"Guest/Subgroup"},"credentialStatus":{"type":"integer","description":"Credential Status"},"ticketModel":{"type":"string","enum":["individualTicket","bulkTicket","groupCredential","namedTicket","quantityBasedTicket","reservedSeat","generalAdmission","zoneAllocation"],"description":"How the group is ticketed."},"seatingPreferences":{"type":"array","items":{"type":"string","enum":["keepGroupTogether","accessibleSeats","teacherLeaderAdjacentSeating","vipAllocation","companionSeats"]},"description":"Seating preferences applied."},"associatedAllocations":{"type":"array","items":{"type":"string","enum":["meal","workshop","parking","fastTrack","merchandise","otherPackageComponents"]},"description":"Package items allocated with the tickets."}}},
"GroupVisitPlan": {"type":"object","x-ticvai-persistence":"orders.group_visit_plan","description":"**The day-of-visit record for one group booking: the operational plan, the sales-to-operations handover, and the group check-in** (DM5, 29 September: data model for the agreed operations; MoM 31 Aug 4.7-4.8 and Key Decisions: group check-in is a status distinct from the access scan).\n**One row per group booking, beside it rather than on it**: operations writes this, sales owns the booking, and the booking's shape stays what its operations already return. Tasks are `orders.group_task` rows against the same booking.\n**Check-in here is the group's arrival, not admission.** Each guest is still admitted by their own entitlement scan; `arrivedCount` is what the group leader and the gate agree on, which is why it can differ from the scans.","required":["id","groupBookingId","checkInStatus","createdAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"groupBookingId":{"x-ticvai-references":"orders.group_booking","type":"string","format":"uuid","description":"Unique; one plan per group booking."},"arrivalAt":{"type":"string","format":"date-time","nullable":true},"arrivalLocation":{"type":"string","maxLength":200,"nullable":true},"meetingPoint":{"type":"string","maxLength":200,"nullable":true},"entryGateId":{"type":"string","format":"uuid","nullable":true},"departureAt":{"type":"string","format":"date-time","nullable":true},"groupLeaders":{"type":"string","maxLength":500,"nullable":true},"contactId":{"x-ticvai-references":"orders.group_customer_organization_contact","type":"string","format":"uuid","nullable":true},"ticketingMethod":{"type":"string","maxLength":60,"nullable":true},"requirements":{"type":"object","nullable":true,"description":"Seating, guides, catering, transportation, parking, accessibility, equipment and special requirements, as free text keyed by those names. **Free text on purpose**: each is fulfilled by its own service (resources, F&B, transport), and this is the brief they are fulfilled against, not the booking of them."},"operationalOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true},"handoverNotes":{"type":"string","maxLength":4000,"nullable":true},"handoverAttachmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"handoverAcknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"handoverAcknowledgedAt":{"type":"string","format":"date-time","nullable":true},"checkInStatus":{"type":"string","default":"expected","enum":["expected","partiallyArrived","arrived","noShow"]},"actualArrivalAt":{"type":"string","format":"date-time","nullable":true},"arrivalGateId":{"type":"string","format":"uuid","nullable":true},"arrivedCount":{"type":"integer","minimum":0,"default":0},"additionalGuests":{"type":"integer","minimum":0,"default":0},"staffLeadersCount":{"type":"integer","minimum":0,"default":0},"checkInIssues":{"type":"array","items":{"type":"string","enum":["missingGuest","extraGuest","invalidTicket","wrongDate","lateArrival","paymentHold","missingCredential","accessibilityRequirement"]}},"checkedInByPrincipalId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"ModifyOrderRequest": {"type":"object","required":["id","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 **of this modification, not of the order** — the order is the path's `orderId`. It is the modification's idempotency key and must equal the `Idempotency-Key` header.\n"},"addLines":{"type":"array","items":{"$ref":"#/components/schemas/CreateOrderLine"}},"removeLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**The currency the guest selected and is charged in** (CHG-FIN-001, 2 October 2026). Null or equal to `currency` for a sale in the base currency. Everything else on the order, and every ledger posting, stays in the base currency `currency`."},"chargeFxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`), stored on the order so the payment, the receipt, the tax invoice and any refund use the same rate (CHG-FIN-001)."},"chargeFxRateId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `finance.FxRate` row the rate was taken from, for audit."},"chargeTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"`grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to the provider asks for (CHG-FIN-001)."},"chargeRateLockedUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms the new amount (CHG-FIN-001)."},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderExchangeResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["orderId","outgoingValue","incomingValue","difference"],"properties":{"orderId":{"type":"string","format":"uuid"},"outgoingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incomingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"exchangeFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Only the difference settles. The replacement is held before the original is released, never the other way round.\n"},"newLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"OrderModificationResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["order","balanceDue"],"properties":{"order":{"$ref":"#/components/schemas/Order"},"addedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"removedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceDue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Positive means the guest pays; negative means a refund is due."},"refundId":{"type":"string","format":"uuid","nullable":true},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"ParticipantGuestListInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `setParticipantGuestList` takes. It replaces the whole list (decided 29 September, readiness close-out).","required":["source","participants"],"properties":{"source":{"type":"string","description":"How the names arrived (decided 29 September, readiness close-out).","enum":["manualEntry","csvExcelImport","customerUpload","api"]},"participants":{"type":"array","items":{"type":"object","required":["fullName"],"properties":{"fullName":{"type":"string","maxLength":200},"role":{"type":"string","enum":["participant","leader","supervisor"],"default":"participant"},"email":{"type":"string","format":"email","nullable":true},"phone":{"type":"string","maxLength":30,"nullable":true},"dateOfBirth":{"type":"string","format":"date","nullable":true}}}},"fileRef":{"type":"string","format":"uuid","nullable":true,"description":"The uploaded file the names came from. Required for `csvExcelImport` and `customerUpload`."}}},
"ParticipantGuestListView": {"type":"object","x-ticvai-persistence":"orders.group_participant_list + orders.group_participant","description":"**A group's participants, and how the list arrived.** Written by `setParticipantGuestList` (decided 29 September, readiness close-out).\n","required":["groupBookingId","source","participants"],"properties":{"groupBookingId":{"type":"string","format":"uuid","readOnly":true},"source":{"type":"string","enum":["manualEntry","csvExcelImport","customerUpload","api"]},"fileRef":{"type":"string","format":"uuid","nullable":true},"participants":{"type":"array","items":{"type":"object","required":["id","fullName"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"fullName":{"type":"string","maxLength":200},"role":{"type":"string","enum":["participant","leader","supervisor"]},"email":{"type":"string","format":"email","nullable":true},"phone":{"type":"string","maxLength":30,"nullable":true},"dateOfBirth":{"type":"string","format":"date","nullable":true}}}},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ParticipantsGuestListsGroupStructureView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Participants, Guest Lists & Group Structure displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"firstName":{"type":"string","description":"First Name"},"lastName":{"type":"string","format":"date-time","description":"Last Name"},"guestType":{"type":"string","description":"Guest Type"},"ticketCategory":{"type":"string","description":"Ticket Category"},"email":{"type":"string","description":"Email"},"mobile":{"type":"string","description":"Mobile"},"membership":{"type":"string","description":"Membership"},"accessibilityRequirement":{"type":"string","description":"Accessibility Requirement"},"dietaryRequirement":{"type":"string","description":"Dietary Requirement"},"groupSubgroup":{"type":"string","description":"Group/Subgroup"},"seat":{"type":"string","description":"Seat"},"credentialStatus":{"type":"string","description":"Credential Status"},"dateOfBirth":{"type":"string","format":"date-time","description":"Age/Date of Birth where applicable"},"captureSource":{"type":"string","enum":["manualEntry","csvExcelImport","customerUpload","api","previousGroupTemplate"],"description":"How the participant was captured."},"validationIssues":{"type":"array","items":{"type":"string","enum":["missingRequiredField","invalidCategory","guestCountMismatch","ageTicketMismatch"]},"description":"Problems detected on the list."}}},
"UpdateGroupBookingRequest": {"type":"object","description":"Request only. Every field optional; absent means unchanged.","properties":{"packageProductId":{"type":"string","nullable":true,"description":"The school-trip format or party package."},"yearGroup":{"type":"string","maxLength":40,"nullable":true},"accessAndDietaryNeeds":{"type":"string","maxLength":1000,"nullable":true},"celebrantName":{"type":"string","maxLength":120,"nullable":true,"description":"The birthday child."},"celebrantTurningAge":{"type":"integer","minimum":1,"maximum":18,"nullable":true},"allergiesAndRequests":{"type":"string","maxLength":1000,"nullable":true},"finalHeadcountDueBy":{"type":"string","format":"date-time","nullable":true},"leaderSubjectId":{"type":"string","format":"uuid"},"organisationName":{"type":"string","maxLength":200,"nullable":true},"expectedSize":{"type":"integer","minimum":2},"confirmedSize":{"type":"integer","minimum":0},"minimumSize":{"type":"integer","minimum":1,"nullable":true},"attendeeCaptureRequired":{"type":"boolean"},"attendeeCaptureDueBy":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["confirmed","namesPending","complete","cancelled"]}}}
}
```
