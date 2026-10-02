# WS32 — Order   Reservation Management board 2

**9 screens · 18 operations · 30 schemas · 9 permissions**

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

- **Every control that can be refused must be gated.** 9 permissions apply here:
  `ORDER_CREATE, ORDER_EXCHANGE, ORDER_MODIFY, ORDER_RESCHEDULE, ORDER_VIEW, ORDER_VOID, PAYMENT_VOID, PRODUCT_CONFIGURE, REGION_CONFIGURE`. A control nobody can use must say so,
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
| `BO-314` | Amendment & After-Sales Command Center | B–D | 2 | 48 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-315` | Order Amendment Workspace | B–D | 60 | 30 | 6 | 32 | 0 | 0 | — | notStarted (generated) |
| `BO-316` | Amendment Eligibility & Policy Rule Builder | B–D | 15 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-317` | Cancellation & Partial Cancellation Policy Configuration | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-318` | Refund Policy & Refund Calculation Configuration | B–D | 16 | 11 | 5 | 0 | 3 | 6 | — | notStarted (generated) |
| `BO-319` | Void, Reversal & Same-Day Correction Management | B–D | 11 | 0 | 5 | 1 | 0 | 0 | — | notStarted (generated) |
| `BO-321` | After-Sales Financial Settlement & Adjustment Workspace | B–D | 0 | 26 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-322` | Approval, Exception & Service Recovery Management | B–D | 9 | 0 | 5 | 0 | 0 | 3 | — | notStarted (generated) |
| `BO-323` | Amendment History, Audit & After-Sales Analytics | B–D | 17 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-321 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-314` Amendment & After-Sales Command Center

**Provide one operational workspace for all post-sale activities affecting confirmed orders and reservations.**

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
| Route | `/orders-money/amendment-after-sales-command-center-bo-314` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** One workspace for post-sale activity on confirmed orders: amendments, cancellations, refunds, exchanges.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listAmendmentAfterSale2, listAmendmentAfterSale return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listAmendmentAfterSale2 / contracts/spine/orders.yaml#listAmendmentAfterSale; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search amendment after-sales | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, event, product, request type, channel, customer and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listAmendmentAfterSale2` ?venue |
| Product | text field | — | — | `listAmendmentAfterSale2` ?product |
| Event | text field | — | — | `listAmendmentAfterSale2` ?event |
| Agent | text field | — | — | `listAmendmentAfterSale2` ?agent |
| Customer segment | text field | — | — | `listAmendmentAfterSale2` ?customerSegment |
| Reason | text area | — | — | `listAmendmentAfterSale2` ?reason |
| Period | text field | — | — | `listAmendmentAfterSale2` ?period |
| Venue | text field | — | — | `listAmendmentAfterSale` ?venue |
| Event | text field | — | — | `listAmendmentAfterSale` ?event |
| Product | text field | — | — | `listAmendmentAfterSale` ?product |
| Agent | text field | — | — | `listAmendmentAfterSale` ?agent |
| Status | text field | — | — | `listAmendmentAfterSale` ?status |
| Approval | text field | — | — | `listAmendmentAfterSale` ?approval |
| Date | text field | — | — | `listAmendmentAfterSale` ?date |
| Request type | text field | — | — | `listAmendmentAfterSale` ?requestType |
| Channel | text field | — | — | `listAmendmentAfterSale` ?channel |
| … 1 more | | | | `operations.json` |

#### Outputs: what the screen shows and produces

**Shown**

**Every amendment after-sales** (data table, from `listAmendmentAfterSale`)

| Shows | Format | Notes |
|---|---|---|
| Amendments today | text | Amendments Today |
| Pending amendments | 1,234 | Pending Amendments |
| Cancellations | 1,234 | Cancellations |
| Refund requests | text | not in the schema: `Refund Requests` |
| Refund value | text | not in the schema: `Refund Value` |
| Voids | 1,234 | Voids |
| Reissues | 1,234 | Reissues |
| Date time changes | 1,234 | Date/Time Changes |
| Partial cancellations | 1,234 | Partial Cancellations |
| Pending approvals | 1,234 | Pending Approvals |
| Failed actions | 1,234 | Failed Actions |
| Sla breaches | 1,234 | SLA Breaches |
| Request | text | Request ID |
| Order number | text | Order Number |
| Customer | text | Customer |
| Request type | chip: Order amendment, Reservation amendment, Date change, Timeslot change, Performance … | Request type. |
| Product event | text | Product/Event |
| Original value | text | Original Value |
| Financial impact | text | Financial Impact |
| Channel | text | Channel |
| Requested by | text | Requested By |
| Approval status | 1,234 | Approval Status |
| Processing status | 1,234 | Processing Status |
| Created time | 1 Oct 2026, 14:30 | Created Time |

**The selected amendment after-sales** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Amendments today | text | Amendments Today |
| Pending amendments | 1,234 | Pending Amendments |
| Cancellations | 1,234 | Cancellations |
| Refund requests | text | not in the schema: `Refund Requests` |
| Refund value | text | not in the schema: `Refund Value` |
| Voids | 1,234 | Voids |
| Reissues | 1,234 | Reissues |
| Date time changes | 1,234 | Date/Time Changes |
| Partial cancellations | 1,234 | Partial Cancellations |
| Pending approvals | 1,234 | Pending Approvals |
| Failed actions | 1,234 | Failed Actions |
| Sla breaches | 1,234 | SLA Breaches |
| Request | text | Request ID |
| Order number | text | Order Number |
| Customer | text | Customer |
| Request type | chip: Order amendment, Reservation amendment, Date change, Timeslot change, Performance … | Request type. |
| Product event | text | Product/Event |
| Original value | text | Original Value |
| Financial impact | text | Financial Impact |
| Channel | text | Channel |
| Requested by | text | Requested By |
| Approval status | 1,234 | Approval Status |
| Processing status | 1,234 | Processing Status |
| Created time | 1 Oct 2026, 14:30 | Created Time |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Order Amendment (primary button) | navigation or local | — | — | — | — |
| Reservation Amendment (secondary button) | navigation or local | — | — | — | — |
| Date Change (secondary button) | navigation or local | — | — | — | — |
| Timeslot Change (secondary button) | navigation or local | — | — | — | — |
| Performance Change (secondary button) | navigation or local | — | — | — | — |
| Quantity Change (secondary button) | navigation or local | — | — | — | — |
| Attendee Change (secondary button) | navigation or local | — | — | — | — |
| Refund (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **after-sales queue**: Requests by type and state. *(source: contracts/spine/orders.yaml#listAmendmentAfterSale)*

**Data it reads**: `listAmendmentAfterSale2` (onLoad, Amendment History, Audit & After-Sales Analytics); `listAmendmentAfterSale` (onLoad, Amendment & After-Sales Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-318` Refund Policy & Refund Calculation Configuration: *Refund Policy & Refund Calculation Configuration*
- → `BO-315` Order Amendment Workspace: *Works in Order Amendment Workspace*; carries `orderId`; calls `listAmendmentAfterSale`
- → `BO-316` Amendment Eligibility & Policy Rule Builder: *Works in Amendment Eligibility & Policy Rule Builder*; calls `listAmendmentAfterSale`
- → `BO-317` Cancellation & Partial Cancellation Policy Configuration: *Works in Cancellation & Partial Cancellation Policy Configuration*; calls `listAmendmentAfterSale`
- → `BO-321` After-Sales Financial Settlement & Adjustment Workspace: *Works in After-Sales Financial Settlement & Adjustment Workspace*; calls `listAmendmentAfterSale`
- → `BO-322` Approval, Exception & Service Recovery Management: *Works in Approval, Exception & Service Recovery Management*; calls `listAmendmentAfterSale`
- → `BO-323` Amendment History, Audit & After-Sales Analytics: *Works in Amendment History, Audit & After-Sales Analytics*; calls `listAmendmentAfterSale`
- → `BO-027` Reissue & Media Replacement: *Works in Reissue & Media Replacement (Ticket Reissue & Fulfillment Regeneration, merged into it on 28…*; calls `listAmendmentAfterSale`
- → `BO-319` Void, Reversal & Same-Day Correction Management: *Works in Void, Reversal & Same-Day Correction Management*; carries `orderId`; calls `listAmendmentAfterSale`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The amendment after-sales list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the amendment after-sales untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No amendment after-sales yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the amendment after-sales are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
queue:
  amendments: 14
  cancellations: 6
  refunds: 9
```

#### Permissions

- `listAmendmentAfterSale2` → `ORDER_VIEW` (read) · staff
- `listAmendmentAfterSale` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Amendments/cancellations/reschedules are checked against the applicable policy before being allowed. A booking's financial status (deposit required, partial payment, full payment) is tracked; schools and corporates can pay a 20-30% deposit with the balance due on or before arrival. *(agreed · MoM 1 Sep 2026, 4.12 Amendment, Cancellation & Booking Status · DI-615)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-314` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-314`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 2
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 1: Opens Amendment & After-Sales Command Center → Provide one operational workspace for all post-sale activities affecting confirmed orders and reservations.
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F141 branch at step 1 (expected): when Nothing has been set up on Amendment & After-Sales Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F141 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (48 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-314?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Order Amendment, Reservation Amendment, Date Change, Timeslot Change, Performance Change, Quantity Change, Attendee Change, Refund.
- [ ] Every transition is wired: `BO-100`, `BO-318`, `BO-315`, `BO-316`, `BO-317`, `BO-321`, `BO-322`, `BO-323`, `BO-027`, `BO-319`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-315` Order Amendment Workspace

**Provide agents with a controlled workspace for modifying an existing order without directly editing historical transaction records. The original order must always remain reconstructable.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_RESCHEDULE`, `ORDER_VIEW` (3 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `orderId` (navigation) |
| Route | `/orders-money/order-amendment-workspace-bo-315` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-025): setOrderAmendment takes the new values as loose strings with no order id and duplicates modify, exchange and reschedule without their rules; the workspace reads …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Change an existing order (date, slot, quantity, holder, delivery, seat) without editing history.

**Fixed on main** (the package already carries these; draw what it says): setOrderAmendment takes the new values as loose strings with no order id. (CHG-WIR-025); No read operation: the screen declares only setOrderAmendment and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**Form: Modify order** (modal, opened by *Modify order*; *Modify order* calls `modifyOrder`, *Cancel* sends nothing)

**Collects what `modifyOrder` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

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

**Form: Exchange lines** (modal, opened by *Exchange lines*; *Exchange lines* calls `exchangeOrderLines`, *Cancel* sends nothing)

**Collects what `exchangeOrderLines` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

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

**Form: Reschedule** (modal, opened by *Reschedule*; *Reschedule* calls `rescheduleOrder`, *Cancel* sends nothing)

**Collects what `rescheduleOrder` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Target performance `targetPerformanceId` | picker: choose a target performance | required | — | — | shows names, sends the id | — | `rescheduleOrder` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | Omit to move the whole order. | `rescheduleOrder` body |
| Waive fee `waiveFee` | toggle | optional | off | — | — | — | `rescheduleOrder` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `rescheduleOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `rescheduleOrder` body |

Errors to draw in the form: 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem)

#### Outputs: what the screen shows and produces

**Shown**

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

**The selected order amendment** (detail panel): The pack groups this record's detail under its own headings: “Original Proposed”, “Before committing, validate”.

| Shows | Format | Notes |
|---|---|---|
| Order | text | Order ID |
| Customer | text | Customer |
| Original channel | text | Original Channel |
| Venue | text | Venue |
| Order date | 1 Oct 2026, 14:30 | Order Date |
| Payment status | 1,234 | Payment Status |
| Fulfillment status | 1,234 | Fulfillment Status |
| Total | 1,234 | Total |
| Tickets | 1,234 | Tickets |
| Current reservation | text | Current Reservation |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Timeslot (primary button) | navigation or local | — | — | — | — |
| Quantity (secondary button) | navigation or local | — | — | — | — |
| Ticket Holder (secondary button) | navigation or local | — | — | — | — |
| Customer Details (secondary button) | navigation or local | — | — | — | — |
| Delivery Method (secondary button) | navigation or local | — | — | — | — |
| Eligible Product Attributes (secondary button) | navigation or local | — | — | — | — |
| Seat where applicable (secondary button) | navigation or local | — | — | — | — |
| Save Draft (secondary button) | navigation or local | — | — | — | — |
| Modify order (secondary button) | `modifyOrder` POST `/orders/{orderId}/modify` | ModifyOrderRequest | OrderModificationResult | 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem) | opens modal first |
| Exchange lines (secondary button) | `exchangeOrderLines` POST `/orders/{orderId}/exchanges` | ExchangeOrderRequest | OrderExchangeResult | 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem) | opens modal first |
| Reschedule (secondary button) | `rescheduleOrder` POST `/orders/{orderId}/reschedule` | inline | OrderExchangeResult | 409 Target performance is unavailable (`targetUnavailable`) or outside the reschedule window (`outsideRescheduleWindow`). (OrderRefusedProblem) | opens modal first |

**Data it reads**: `getOrder` (onLoad, The order being amended, as it stands)

**Where the user goes next**

- → `BO-314` Amendment & After-Sales Command Center: *Returns to the board's landing screen*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order amendment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order amendment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order amendment yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the order amendment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A targeted line's entitlement has been redeemed (`lineRedeemed`, naming it in `lineIds`), or the order is voided (`orderVoided`). (OrderRefusedProblem); 409 Replacement unavailable (`replacementUnavailable`), outside the exchange window (`outsideExchangeWindow`), or the original is redeemed (`lineRedeemed`). (OrderRefusedProblem); 409 Target performance is unavailable (`targetUnavailable`) or … |

#### Consistency with other screens

- Match `BO-023`: The change acts are modifyOrder, exchangeOrderLines and rescheduleOrder; same dialogs.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
amendment:
  order: DP-2026-104882
  change: visit date 14 Nov to 21 Nov
```

#### Permissions

- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `modifyOrder` → `ORDER_MODIFY` (operate) · staff, partner
- `exchangeOrderLines` → `ORDER_EXCHANGE` (operate) · staff, partner
- `rescheduleOrder` → `ORDER_RESCHEDULE` (operate) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

32 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.12 | Ticket Viewing - System shall display ticket details. | Guest Mobile App & Branding | CONTRACTED | `getOrder` |
| 2.6.2 | Post-order service 1) On the order details page, users can view the order number, amount, time, payment method, user information, refund/change policies, and the QR code of the e-ticket 2) During the … | Ticketing Sales | CONTRACTED | `getOrder` |
| 2.12.27 | All orders can be finalized for payment registration or modified or even cancelled at the Guest Service or any reservation PC. | Ticketing Sales | CONTRACTED | `getOrder` |
| 5.7.8 | The system should be able to use of a unique Order or Reference number (PNR) for each transaction, which can be communicated to the Payment Gateway, Acquiring Bank and the ERP system for … | F&B & Guest Management | CONTRACTED | `getOrder` |
| 2.12.2 | The system should allow for order adjustments. Following adjustments should be supported: - Users to refund guests (with supervisor approval) - Users to manually adjust guest orders (date, time … | Ticketing Sales | CONTRACTED | `modifyOrder` |
| 2.12.26 | Based on user’s privileges, an order can be modified or cancelled | Ticketing Sales | CONTRACTED | `modifyOrder` |
| 19.2.16 | Ticket Upgrade - System shall support ticket upgrades. | Guest Mobile App & Branding | CONTRACTED | `exchangeOrderLines` |
| 19.2.25 | Membership Upgrade - System shall support membership upgrades. | Guest Mobile App & Branding | CONTRACTED | `exchangeOrderLines` |
| 19.2.81 | Self-Service Membership Upgrades - System shall support self-service membership upgrades. | Guest Mobile App & Branding | CONTRACTED | `exchangeOrderLines` |
| 1.1.20 | System shall allow exchange of tickets between ticket types, dates, timeslots and experiences while applying configurable fees, price differences and approval workflows. | Ticketing Catalogue | CONTRACTED | `exchangeOrderLines` |
| 1.1.21 | System shall support ticket upgrades before or after purchase, including automatic calculation of price differences and applicable upgrade fees. | Ticketing Catalogue | CONTRACTED | `exchangeOrderLines` |
| 1.1.22 | System shall support ticket downgrades according to configurable business rules, refund policies and approval requirements. | Ticketing Catalogue | CONTRACTED | `exchangeOrderLines` |
| … 20 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-315` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-315`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 2
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 2: Works in Order Amendment Workspace → Provide agents with a controlled workspace for modifying an existing order without directly editing historical transaction records. The original order must always remain reconstructable.

#### Acceptance for the design

- [ ] Every input above is drawn (60), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-315?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Timeslot, Quantity, Ticket Holder, Customer Details, Delivery Method, Eligible Product Attributes, Seat where applicable, Save Draft, Modify order, Exchange lines, Reschedule.
- [ ] Every transition is wired: `BO-314`.
- [ ] Every gated control is gated: `ORDER_EXCHANGE`, `ORDER_MODIFY`, `ORDER_RESCHEDULE`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-316` Amendment Eligibility & Policy Rule Builder

**Define when an order or reservation may be amended and which changes are permitted.**

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
| Route | `/orders-money/amendment-eligibility-policy-rule-builder-bo-316` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the amendment eligibility policy that setAmendmentEligibilityPolicy writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** When an order may be amended and what may change, by product, channel, segment, status and time before the visit.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setAmendmentEligibilityPolicy and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Ticket Type | select field | — | — | — | — | — | — |
| Event | select field | — | — | — | — | — | — |
| Performance | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Customer Segment | select field | — | — | — | — | — | — |
| Membership | select field | — | — | — | — | — | — |
| Order Status | select field | — | — | — | — | — | — |
| Ticket Status | select field | — | — | — | — | — | — |
| Maximum Amendments per Order | text field | — | — | — | — | — | — |
| Maximum Amendments per Ticket | text field | — | — | — | — | — | — |
| Maximum Date Changes | select field | — | — | — | — | — | — |
| Cooling Period | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **rule**: Scope and conditions as a builder; reschedule is a product-level switch with its own window (allowed up to 24 h before). *(source: contracts/spine/orders.yaml#setAmendmentEligibilityPolicy / DI-446)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Date Change (primary button) | navigation or local | — | — | — | — |
| Timeslot Change (secondary button) | navigation or local | — | — | — | — |
| Performance Change (secondary button) | navigation or local | — | — | — | — |
| Quantity Increase (secondary button) | navigation or local | — | — | — | — |
| Quantity Reduction (secondary button) | navigation or local | — | — | — | — |
| Seat Change (secondary button) | navigation or local | — | — | — | — |
| Attendee Change (secondary button) | navigation or local | — | — | — | — |
| Delivery Change (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-314` Amendment & After-Sales Command Center: *Returns to the board's landing screen*; calls `setAmendmentEligibilityPolicy`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The amendment eligibility policy configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the amendment eligibility policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No amendment eligibility policy configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  product: Day Pass
  dateChange: allowed until 24 h before
  fee: AED 20.00
```

#### Permissions

- `setAmendmentEligibilityPolicy` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Amendments/cancellations/reschedules are checked against the applicable policy before being allowed. A booking's financial status (deposit required, partial payment, full payment) is tracked; schools and corporates can pay a 20-30% deposit with the balance due on or before arrival. *(agreed · MoM 1 Sep 2026, 4.12 Amendment, Cancellation & Booking Status · DI-615)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-316` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-316`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 2
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 4: Works in Amendment Eligibility & Policy Rule Builder → Define when an order or reservation may be amended and which changes are permitted.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-316?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Date Change, Timeslot Change, Performance Change, Quantity Increase, Quantity Reduction, Seat Change, Attendee Change, Delivery Change.
- [ ] Every transition is wired: `BO-314`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-317` Cancellation & Partial Cancellation Policy Configuration

**Configure whether an order, reservation, or selected order lines may be cancelled.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/cancellation-partial-cancellation-policy-configuration-bo-317` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the cancellation and partial cancellation policy that setCancellationPartialPolicy writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Whether an order, reservation or some lines may be cancelled, and on what conditions.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setCancellationPartialPolicy and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **scopes and conditions**: Permitted scopes as checkboxes; conditions as a list. *(source: contracts/spine/orders.yaml#setCancellationPartialPolicy)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Entire Order (primary button) | navigation or local | — | — | — | — |
| Entire Reservation (secondary button) | navigation or local | — | — | — | — |
| Individual Ticket (secondary button) | navigation or local | — | — | — | — |
| Selected Order Lines (secondary button) | navigation or local | — | — | — | — |
| Selected Quantity (secondary button) | navigation or local | — | — | — | — |
| Add-On Only (secondary button) | navigation or local | — | — | — | — |
| Package Component where permitted (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-314` Amendment & After-Sales Command Center: *Returns to the board's landing screen*; calls `setCancellationPartialPolicy`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cancellation partial cancellation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cancellation partial cancellation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cancellation partial cancellation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the cancellation partial cancellation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  scopes:
  - entireOrder
  - selectedOrderLines
  window: until 48 h before
```

#### Permissions

- `setCancellationPartialPolicy` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-317` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-317`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 2
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 6: Works in Cancellation & Partial Cancellation Policy Configuration → Configure whether an order, reservation, or selected order lines may be cancelled.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-317?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Entire Order, Entire Reservation, Individual Ticket, Selected Order Lines, Selected Quantity, Add-On Only, Package Component where permitted.
- [ ] Every transition is wired: `BO-314`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-318` Refund Policy & Refund Calculation Configuration

**Define when a cancellation/amendment creates a refundable amount and how refund entitlement is determined.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `REGION_CONFIGURE` (1 read, 2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure separately) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `venueId` (navigation) · cold entry: **Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that … |
| Route | `/orders-money/refund-policy-refund-calculation-configuration-bo-318` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How a refund is calculated and where it goes: full, partial, percentage, pro rata, less fees; to original payment, wallet or credit note; with authority limits and time bands.

**Fixed on main** (the package already carries these; draw what it says): No read operation: the screen declares only setRefundPolicy, setRefundCalculationPolicy and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Base Price | select field | — | — | — | — | — | — |
| Tax | select field | — | — | — | — | — | — |
| Booking Fee | select field | — | — | — | — | — | — |
| Service Fee | select field | — | — | — | — | — | — |
| Delivery Fee | select field | — | — | — | — | — | — |
| Add-On | select field | — | — | — | — | — | — |
| Discount | select field | — | — | — | — | — | — |
| Promotion | select field | — | — | — | — | — | — |
| Convenience Fee | select field | — | — | — | — | — | — |

**Sent by *Save refund policy*** (`setRefundCalculationPolicy`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Refund types `refundTypes` | multi-select chips | required | — | Full refund · Partial refund · Percentage refund · Pro rata refund · Original value less fees; at least 1 | — | The calculations a refund may use (decided 29 September, readiness close-out). | `setRefundCalculationPolicy` body |
| Refund destinations `refundDestinations` | multi-select chips | required | — | Original payment · Wallet credit · Voucher credit note; at least 1 | — | Where refunded money may go (decided 29 September, readiness close-out). | `setRefundCalculationPolicy` body |
| Percentage `percentage` | stepper or slider (%) | optional | — | min 0; max 100; Required when `percentageRefund` is allowed. | — | Required when `percentageRefund` is allowed. | `setRefundCalculationPolicy` body |
| Non refundable fees `nonRefundableFees` | list of values (chips) | optional | — | — | — | Order-fee categories (`orders.order_fee.category`) that `originalValueLessFees` keeps back. | `setRefundCalculationPolicy` body |
| Scope `scope` | group | optional | — | — | — | Narrows the policy; null applies it venue-wide. | `setRefundCalculationPolicy` body |
| Products `scope.productIds` | multi-picker: choose products | optional | — | — | — | — | `setRefundCalculationPolicy` body |
| Channels `scope.channels` | multi-select chips | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | — | `setRefundCalculationPolicy` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **refundTypes and destinations**: Types and destinations as checkboxes; time bands as a table. *(source: contracts/spine/orders.yaml#setRefundCalculationPolicy / contracts/spine/orders.yaml#setRefundPolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Read a venue's refund policy** (detail panel, from `getRefundPolicy`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | The venue in the path. Not taken from a `setRefundPolicy` body. |
| Self authorise limit | AED 1,234.50 | Up to this, a holder of ORDER_REFUND refunds alone. Zero means every refund needs a second authoriser. |
| Requires second user above | AED 1,234.50 | Above this, a second user — cashier OR supervisor — names themselves as audit control. |
| Requires approval above | AED 1,234.50 | Above this, an ORDER_REFUND_APPROVE holder must approve. |
| Time bands | list or chips (count when long) | Refundable percentage by time before the performance. Evaluated most-specific first. |
| Hours before | 1,234 | — |
| Percentage | 12.5% | — |
| Allow partial | yes / no (icon or chip) | — |
| Refund window days | 1,234 | Days after purchase within which a refund may be made. 0 is allowed and means the day of purchase only; null means no window (decided 28 … |
| Variance threshold | AED 1,234.50 | Price variance above this is an exception requiring review rather than a routine posting (CF-38). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Full Refund (primary button) | navigation or local | — | — | — | — |
| Partial Refund (secondary button) | navigation or local | — | — | — | — |
| Percentage Refund (secondary button) | navigation or local | — | — | — | — |
| Pro-Rata Refund (secondary button) | navigation or local | — | — | — | — |
| Original Value Less Fees (secondary button) | navigation or local | — | — | — | — |
| Wallet Credit (secondary button) | navigation or local | — | — | — | — |
| Voucher/Credit Note (secondary button) | navigation or local | — | — | — | — |
| Save refund policy (primary button) | `setRefundCalculationPolicy` PUT `/refund-calculation-policy` | RefundCalculationPolicyInput | RefundCalculationPolicyView | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.; 422 `percentageRefund` allowed with no `percentage` (`refund-percentage-missing`). | — |

**Data it reads**: `getRefundPolicy` (onLoad, Read a venue's refund policy)

**Where the user goes next**

- → `BO-314` Amendment & After-Sales Command Center: *Returns to the board's landing screen*; calls `setRefundPolicy`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The refund policy refund configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the refund policy refund untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No refund policy refund configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 The thresholds do not ascend: `selfAuthoriseLimit` above `requiresSecondUserAbove`, or either above `requiresApprovalAbove` (`refund-thresholds-not-ascending` …; 422 `percentageRefund` allowed with no `percentage` (`refund-percentage-missing`). |

#### Consistency with other screens

- Match `BO-1146`: Destinations must agree with the refund-to-wallet policy.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  types:
  - percentageRefund
  destinations:
  - originalPayment
  - walletCredit
  bands:
  - 72 h+ 100%
  - 24-72 h 50%
```

#### Permissions

- `setRefundPolicy` → `REGION_CONFIGURE` (configure) · staff
- `setRefundCalculationPolicy` → `PRODUCT_CONFIGURE` (configure) · staff
- `getRefundPolicy` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approved refunds go back to the original payment method or are credited to the guest's wallet for future purchases. *(client request · MoM 7 Sep 2026, 4.11 Entitlements Usage, Upgrades & Refund/Credit Recovery · DI-673)*
- Refunds use preset time-banded percentages (e.g. full refund a set number of days before the event, less closer to/after it), support partial refunds, and let an authorised approver apply a custom override percentage. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-252)*
- Refund policy shown to guests is tiered and driven by back-office rules per business, e.g. no refund <24h, 50% between 24–48h, 100% >48h. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-192)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A75** Design the refund engine: a six-step ledger-to-gateway refund flow with configurable time-banded percentages, an authorized-approver override, partial refunds, both operations- and customer-initiated requests, plus bulk … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 12 Aug 2026 · workshop tracker · keyword 'refund')*
- **A80** Implement a currency-locking rule for refunds/change: always issue in the local/base currency, locked at the value recorded at time of purchase; track foreign-currency activity only via a separate report *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 14 Aug 2026 · workshop tracker · keyword 'refund')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'refund')*
- **A140** Centralise policy management (reschedule, exchange, refund, cancellation, upgrade, downgrade, ownership transfer, membership conversion) with each product mapped to pricing, GL code, promotions and channels *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'refund')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'refund')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'refund')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-318` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-318`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 2
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 8: Works in Refund Policy & Refund Calculation Configuration → Define when a cancellation/amendment creates a refundable amount and how refund entitlement is determined.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (404, 412, 422).
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-318?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Full Refund, Partial Refund, Percentage Refund, Pro-Rata Refund, Original Value Less Fees, Wallet Credit, Voucher/Credit Note, Save refund policy.
- [ ] Every transition is wired: `BO-314`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `PRODUCT_CONFIGURE`, `REGION_CONFIGURE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-319` Void, Reversal & Same-Day Correction Management

**Separate genuine void/correction operations from normal customer cancellations and refunds. This is important financially and operationally.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW`, `ORDER_VOID`, `PAYMENT_VOID` (1 read, 2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `orderId` (navigation), `paymentId` (navigation), `entitlementId` (navigation) · cold entry: Opened from BO-314 with the order picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says … |
| Route | `/orders-money/void-reversal-same-day-correction-management-bo-319` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Genuine voids and same-day corrections, kept apart from cancellations and refunds: void an order or one ticket, void an uncaptured authorisation, clear a failed payment.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listVoidReversalSame return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listVoidReversalSame carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listVoidReversalSame; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Same Business Day Only | text field | — | — | — | — | — | — |
| Before Settlement | select field | — | — | — | — | — | — |
| Before Ticket Use | select field | — | — | — | — | — | — |
| Before Fiscal Closure | select field | — | — | — | — | — | — |
| Supervisor Required | select field | — | — | — | — | — | — |
| Specific Channels Only | select field | — | — | — | — | — | — |

**Sent by *Ticket Void*** (`voidEntitlement`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Guest changed mind · Entered in error · Item unavailable · Quality issue · Duplicate · Other | — | The void reason list (decided 28 September, audit R125 (4)): the one list `voidOrder` takes, and the list `fnb.amendFnbOrder` and `fnb.cancelFnbOrder` point to. | `voidEntitlement` body |
| Note `note` | text area | optional | — | min length 3; max length 500; Required when `reason` is `other`; optional otherwise. | — | Required when `reason` is `other`; optional otherwise. | `voidEntitlement` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `voidEntitlement` body |

**Sent by *Failed Transaction Cleanup*** (`cleanupFailedPayment`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | segmented control | required | — | Release hold · Cancel pending · Mark abandoned | — | How the payment is cleared (decided 29 September, readiness close-out). | `cleanupFailedPayment` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `cleanupFailedPayment` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Order Void (primary button) | navigation or local | — | — | — | — |
| Payment Void Request (secondary button) | navigation or local | — | — | — | — |
| Ticket Void (secondary button) | `voidEntitlement` POST `/entitlements/{entitlementId}/void` | VoidEntitlementInput | Entitlement | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already used, already voided or expired (`entitlementNotVoidable`), or its order has a captured payment … | produces a document or message: Void a single ticket |
| Accidental Sale Reversal (secondary button) | navigation or local | — | — | — | — |
| Duplicate Transaction Correction (secondary button) | navigation or local | — | — | — | — |
| Failed Transaction Cleanup (secondary button) | `cleanupFailedPayment` POST `/payments/{paymentId}/cleanup` | FailedPaymentCleanupInput | Payment | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The payment's state does not allow the action - captured, refunded, or an action that does not fit its status … | — |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Void ticket**: Reason from the void list; only before settlement and within the shift. *(source: contracts/spine/orders.yaml#voidEntitlement)*
- **Clear failed payment**: Release a hold, cancel a pending payment or mark abandoned, with a reason. *(source: contracts/spine/orders.yaml#cleanupFailedPayment)*

**Data it reads**: `listVoidReversalSame` (onLoad, Void, Reversal & Same-Day Correction Management)

**Where the user goes next**

- → `BO-314` Amendment & After-Sales Command Center: *Returns to the board's landing screen*; calls `listVoidReversalSame`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The void reversal same-day configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the void reversal same-day untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No void reversal same-day configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already captured (`alreadyCaptured`). The response says so rather than failing generically, because the correct next action is a refund and the cashier needs … (PaymentProblem); 409 Already used, already voided or expired (`entitlementNotVoidable`), or its order has a captured payment (`entitlementSettled`). (EntitlementRefusedProblem); 409 Settled — a payment on the order has been … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
void:
  ticket: T-77821
  reason: enteredInError
```

#### Permissions

- `listVoidReversalSame` → `ORDER_VIEW` (read) · staff
- `voidOrder` → `ORDER_VOID` (operate) · staff, partner
- `voidPayment` → `PAYMENT_VOID` (operate) · staff
- `voidEntitlement` → `ORDER_VOID` (operate) · staff
- `cleanupFailedPayment` → `ORDER_VOID` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.2.4 | The system should not include voided item/s for promotional triggers irrespective of: - Percentage discount - Total value - Item count | Bundles and Promotions | CONTRACTED | `voidOrder` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-319` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-319`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 2
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 10: Works in Void, Reversal & Same-Day Correction Management → Separate genuine void/correction operations from normal customer cancellations and refunds. This is important financially and operationally.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-319?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Order Void, Payment Void Request, Ticket Void, Accidental Sale Reversal, Duplicate Transaction Correction, Failed Transaction Cleanup.
- [ ] Every transition is wired: `BO-314`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `ORDER_VOID`, `PAYMENT_VOID`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-321` After-Sales Financial Settlement & Adjustment Workspace

**Provide a consolidated view of the financial consequences of amendments, cancellations, refunds, exchanges and corrections. This is not the payment engine; it is the after-sales financial orchestration layer.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Track) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/after-sales-financial-settlement-adjustment-workspace-bo-321` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the after-sales financial settlements and adjustments that setAfterSaleFinancial writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The financial consequences of after-sales acts in one place: amounts owed each way, settled or pending.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only setAfterSaleFinancial and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every after-sales financial settlement** (data table, from `setAfterSaleFinancial`)

| Shows | Format | Notes |
|---|---|---|
| Original order value | text | Original Order Value |
| Current order value | text | Current Order Value |
| Additional charge | AED 1,234.50 | Additional Charge |
| Refund due | text | not in the schema: `Refund Due` |
| Fees | 1,234 | Fees |
| Tax adjustment | text | Tax Adjustment |
| Credits | 1,234 | Credits |
| Already refunded | text | Already Refunded |
| Outstanding balance | AED 1,234.50 | Outstanding Balance |
| Net transaction impact | text | Net Transaction Impact |
| Payment status | chip: Collection required, Payment pending, Payment complete, Failed, Reconciliation … | After-sales payment status. |
| Refund pending | text | not in the schema: `Refund Pending` |
| Refund complete | text | not in the schema: `Refund Complete` |

**The selected after-sales financial settlement** (detail panel): The pack groups this record's detail under its own headings: “Customer Receives Refund”, “No Financial Difference”, “Commit Control”, “Before payment”, “Only after successful payment”, “Trigger relevant”.

| Shows | Format | Notes |
|---|---|---|
| Original order value | text | Original Order Value |
| Current order value | text | Current Order Value |
| Additional charge | AED 1,234.50 | Additional Charge |
| Refund due | text | not in the schema: `Refund Due` |
| Fees | 1,234 | Fees |
| Tax adjustment | text | Tax Adjustment |
| Credits | 1,234 | Credits |
| Already refunded | text | Already Refunded |
| Outstanding balance | AED 1,234.50 | Outstanding Balance |
| Net transaction impact | text | Net Transaction Impact |
| Payment status | chip: Collection required, Payment pending, Payment complete, Failed, Reconciliation … | After-sales payment status. |
| Refund pending | text | not in the schema: `Refund Pending` |
| Refund complete | text | not in the schema: `Refund Complete` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **settlement**: Per order, owed to guest and owed by guest with status. *(source: contracts/spine/orders.yaml#setAfterSaleFinancial)*

**Where the user goes next**

- → `BO-314` Amendment & After-Sales Command Center: *Returns to the board's landing screen*; calls `setAfterSaleFinancial`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The after-sales financial settlement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the after-sales financial settlement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No after-sales financial settlement yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the after-sales financial settlement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
order:
  number: DP-2026-104882
  owedToGuest: AED 245.00
  status: pending
```

#### Permissions

- `setAfterSaleFinancial` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-321` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-321`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 2
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 14: Works in After-Sales Financial Settlement & Adjustment Workspace → Provide a consolidated view of the financial consequences of amendments, cancellations, refunds, exchanges and corrections. This is not the payment engine; it is the after-sales financial …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-321?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-314`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-322` Approval, Exception & Service Recovery Management

**Govern after-sales actions that fall outside normal policies or exceed financial/operational authority.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/approval-exception-service-recovery-management-bo-322` |

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-027): A read (get or list) of the after-sales exceptions awaiting approval that approveExceptionServiceRecovery writes.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** After-sales actions outside policy or authority: the exception requested, the policy result, the financial impact, the remedy (complimentary reissue, fee waiver, partial refund, voucher), approval.

**Known correction pending (do not draw the wrong version)**

- **Financial impact, customer and order are strings.** Why: Money and ids need types. *(source: contracts/spine/orders.yaml#approveExceptionServiceRecovery; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No read operation: the screen declares only approveExceptionServiceRecovery and nothing that returns the current configuration. (CHG-WIR-027)

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Requested Action | select field | — | — | — | — | — | — |
| Customer | select field | — | — | — | — | — | — |
| Order | select field | — | — | — | — | — | — |
| Standard Policy Result | select field | — | — | — | — | — | — |
| Requested Exception | select field | — | — | — | — | — | — |
| Financial Impact | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |
| Supporting Documents | select field | — | — | — | — | — | — |
| Requestor | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **remedy**: Remedy from the list; financial impact as Money. *(source: contracts/spine/orders.yaml#approveExceptionServiceRecovery)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Fee Waiver (primary button) | navigation or local | — | — | — | — |
| Partial Refund (secondary button) | navigation or local | — | — | — | — |
| Voucher (secondary button) | navigation or local | — | — | — | — |
| Wallet Credit (secondary button) | navigation or local | — | — | — | — |
| Alternative Event (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-314` Amendment & After-Sales Command Center: *Returns to the board's landing screen*; calls `approveExceptionServiceRecovery`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval exception service configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval exception service untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval exception service configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
exception:
  order: DP-2026-104990
  remedy: feeWaiver
  impact: AED 20.00
```

#### Permissions

- `approveExceptionServiceRecovery` → `ORDER_CREATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-322` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-322`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 2
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 16: Works in Approval, Exception & Service Recovery Management → Govern after-sales actions that fall outside normal policies or exceed financial/operational authority.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-322?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Fee Waiver, Partial Refund, Voucher, Wallet Credit, Alternative Event.
- [ ] Every transition is wired: `BO-314`.
- [ ] Every gated control is gated: `ORDER_CREATE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-323` Amendment History, Audit & After-Sales Analytics

**Provide complete traceability and analytical visibility across all changes made after original order creation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/amendment-history-audit-after-sales-analytics-bo-323` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Every change after order creation, traceable and analysed.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listAmendmentAfterSale2, listAmendmentAfterSale return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listAmendmentAfterSale2 / contracts/spine/orders.yaml#listAmendmentAfterSale; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search amendment history audit | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, product, event, channel, agent, customer segment and 2 more — which are present is a decision the pack already made. | — |
| Request ID | select field | — | — | — | — | — | — |
| Order ID | select field | — | — | — | — | — | — |
| Ticket ID | select field | — | — | — | — | — | — |
| Customer | select field | — | — | — | — | — | — |
| Action | select field | — | — | — | — | — | — |
| Before Value | select field | — | — | — | — | — | — |
| After Value | select field | — | — | — | — | — | — |
| Financial Impact | select field | — | — | — | — | — | — |
| Rule Applied | select field | — | — | — | — | — | — |
| Exception | select field | — | — | — | — | — | — |
| Approval | select field | — | — | — | — | — | — |
| User | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Timestamp | select field | — | — | — | — | — | — |
| Result | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listAmendmentAfterSale2` ?venue |
| Product | text field | — | — | `listAmendmentAfterSale2` ?product |
| Event | text field | — | — | `listAmendmentAfterSale2` ?event |
| Agent | text field | — | — | `listAmendmentAfterSale2` ?agent |
| Customer segment | text field | — | — | `listAmendmentAfterSale2` ?customerSegment |
| Reason | text area | — | — | `listAmendmentAfterSale2` ?reason |
| Period | text field | — | — | `listAmendmentAfterSale2` ?period |
| Venue | text field | — | — | `listAmendmentAfterSale` ?venue |
| Event | text field | — | — | `listAmendmentAfterSale` ?event |
| Product | text field | — | — | `listAmendmentAfterSale` ?product |
| Agent | text field | — | — | `listAmendmentAfterSale` ?agent |
| Status | text field | — | — | `listAmendmentAfterSale` ?status |
| Approval | text field | — | — | `listAmendmentAfterSale` ?approval |
| Date | text field | — | — | `listAmendmentAfterSale` ?date |
| Request type | text field | — | — | `listAmendmentAfterSale` ?requestType |
| Channel | text field | — | — | `listAmendmentAfterSale` ?channel |
| … 1 more | | | | `operations.json` |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **amendment audit**: Who, what, when, before and after. *(source: contracts/spine/orders.yaml#listAmendmentAfterSale2)*

**Data it reads**: `listAmendmentAfterSale2` (onLoad, Amendment History, Audit & After-Sales Analytics); `listAmendmentAfterSale` (onLoad, Amendment & After-Sales Command Center)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The amendment history audit configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the amendment history audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No amendment history audit configured yet. Carries the create action and says what the platform does in the meantime. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the amendment history audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
event:
  order: DP-2026-104882
  change: reschedule
  by: Call centre agent 12
```

#### Permissions

- `listAmendmentAfterSale2` → `ORDER_VIEW` (read) · staff
- `listAmendmentAfterSale` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-323` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS85 Order   Reservation Management Board 2.dc.html#bo-323`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 2
- Flow F141 *Order Reservation Management board 2: Amendment & After-Sales Command Center*, step 18: Works in Amendment History, Audit & After-Sales Analytics → Provide complete traceability and analytical visibility across all changes made after original order creation.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-323?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
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

### In P08 · Orders & Money

- AI-assisted reporting for accountants/finance managers is phase two; phase-one finance screens do not include it. *(agreed · MoM 12 Aug 2026, 6. Finance & Ledger Architecture Overview · DI-278)*
- Financial reports generated automatically: P&L (revenue per category less cost of sales), balance sheet, trial balance and ledger view, cash flow, revenue and deferred-revenue analytics, site-wise revenue; plus daily/weekly/monthly finance summaries. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-276)*
- Legal entities view lists all tenant sites with country, currency and active/inactive status. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-261)*
- Allam: Bulk QR option — for partners with no technical capability, the platform generates a bulk batch of tickets (e.g. 5,000) with a validity window, delivered as QR codes (e.g. CSV) for the partner to import and resell. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-135)*
- Full card numbers are never stored or shown; only a masked representation (e.g. last four digits) so the user can identify which card was used. *(agreed · MoM 31 Jul 2026, 10. Compliance & Data Protection · DI-069)*

**6 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"approveExceptionServiceRecovery": {"method":"PUT","path":"/exception-service-recovery","contract":"orders","summary":"Approval, Exception & Service Recovery Management","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"ApprovalExceptionServiceRecoveryManagementInput","responds":"ApprovalExceptionServiceRecoveryManagementView"},
"cleanupFailedPayment": {"method":"POST","path":"/payments/{paymentId}/cleanup","contract":"orders","summary":"Clear a failed or orphaned payment","permission":"ORDER_VOID","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FailedPaymentCleanupInput","responds":"Payment"},
"exchangeOrderLines": {"method":"POST","path":"/orders/{orderId}/exchanges","contract":"orders","summary":"Exchange lines for different products or dates","permission":"ORDER_EXCHANGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ExchangeOrderRequest","responds":"OrderExchangeResult"},
"getOrder": {"method":"GET","path":"/orders/{orderId}","contract":"orders","summary":"Read an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"getRefundPolicy": {"method":"GET","path":"/venues/{venueId}/refund-policy","contract":"orders","summary":"Read a venue's refund policy","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RefundPolicy"},
"listAmendmentAfterSale": {"method":"GET","path":"/amendment-after-sale","contract":"orders","summary":"Amendment & After-Sales Command Center","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venue","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"agent","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"approval","in":"query","required":false},{"name":"date","in":"query","required":false},{"name":"requestType","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"customer","in":"query","required":false}],"requestBody":null,"responds":"AmendmentAfterSalesCommandCenterView"},
"listAmendmentAfterSale2": {"method":"GET","path":"/amendment-after-sale-2","contract":"orders","summary":"Amendment History, Audit & After-Sales Analytics","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venue","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"agent","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"reason","in":"query","required":false},{"name":"period","in":"query","required":false}],"requestBody":null,"responds":"AmendmentHistoryAuditAfterSalesAnalyticsView"},
"listVoidReversalSame": {"method":"GET","path":"/void-reversal-same","contract":"orders","summary":"Void, Reversal & Same-Day Correction Management","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"VoidReversalSameDayCorrectionManagementView"},
"modifyOrder": {"method":"POST","path":"/orders/{orderId}/modify","contract":"orders","summary":"Add or remove lines on an existing order","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ModifyOrderRequest","responds":"OrderModificationResult"},
"rescheduleOrder": {"method":"POST","path":"/orders/{orderId}/reschedule","contract":"orders","summary":"Move an order to another performance","permission":"ORDER_RESCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderExchangeResult"},
"setAfterSaleFinancial": {"method":"PUT","path":"/after-sale-financial","contract":"orders","summary":"After-Sales Financial Settlement & Adjustment Workspace","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"AfterSalesFinancialSettlementAdjustmentWorkspaceInput","responds":"AfterSalesFinancialSettlementAdjustmentWorkspaceView"},
"setAmendmentEligibilityPolicy": {"method":"PUT","path":"/amendment-eligibility-policy","contract":"orders","summary":"Amendment Eligibility & Policy Rule Builder","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"AmendmentEligibilityPolicyRuleBuilderInput","responds":"AmendmentEligibilityPolicyRuleBuilderView"},
"setCancellationPartialPolicy": {"method":"PUT","path":"/cancellation-partial-policy","contract":"orders","summary":"Cancellation & Partial Cancellation Policy Configuration","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CancellationPartialCancellationPolicyConfigurationInput","responds":"CancellationPartialCancellationPolicyConfigurationView"},
"setRefundCalculationPolicy": {"method":"PUT","path":"/refund-calculation-policy","contract":"orders","summary":"Set how a venue calculates a refund and where it goes","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"RefundCalculationPolicyInput","responds":"RefundCalculationPolicyView"},
"setRefundPolicy": {"method":"PUT","path":"/venues/{venueId}/refund-policy","contract":"orders","summary":"Set a venue's refund policy","permission":"REGION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"RefundPolicy","responds":"RefundPolicy"},
"voidEntitlement": {"method":"POST","path":"/entitlements/{entitlementId}/void","contract":"orders","summary":"Void a single ticket","permission":"ORDER_VOID","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VoidEntitlementInput","responds":"Entitlement"},
"voidOrder": {"method":"POST","path":"/orders/{orderId}/voids","contract":"orders","summary":"Void an order","permission":"ORDER_VOID","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"voidPayment": {"method":"POST","path":"/payments/{paymentId}/void","contract":"orders","summary":"Release an authorisation before it is captured","permission":"PAYMENT_VOID","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Payment"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AfterSalesFinancialSettlementAdjustmentWorkspaceInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What After-Sales Financial Settlement & Adjustment Workspace submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"commitPolicy":{"type":"string","enum":["beforePayment","afterSuccessfulPayment"],"description":"Whether the change commits before payment or only after successful payment; default afterSuccessfulPayment"},"orderId":{"type":"string","description":"Order ID"}}},
"AfterSalesFinancialSettlementAdjustmentWorkspaceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What After-Sales Financial Settlement & Adjustment Workspace displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"originalOrderValue":{"type":"string","description":"Original Order Value"},"currentOrderValue":{"type":"string","description":"Current Order Value"},"additionalCharge":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Additional Charge"},"fees":{"type":"integer","description":"Fees"},"taxAdjustment":{"type":"string","description":"Tax Adjustment"},"credits":{"type":"integer","description":"Credits"},"alreadyRefunded":{"type":"string","description":"Already Refunded"},"outstandingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Outstanding Balance"},"netTransactionImpact":{"type":"string","description":"Net Transaction Impact"},"paymentStatus":{"type":"string","enum":["collectionRequired","paymentPending","paymentComplete","failed","reconciliationRequired"],"description":"After-sales payment status."},"refundDue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Refund due, subject to policy"},"commitPolicy":{"type":"string","enum":["beforePayment","afterSuccessfulPayment"],"description":"Whether the change commits before payment or only after successful payment; default afterSuccessfulPayment (pack: calculate, collect, commit)"},"orderId":{"type":"string","description":"Order ID"}}},
"AmendmentAfterSalesCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Amendment & After-Sales Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"amendmentsToday":{"type":"string","description":"Amendments Today"},"pendingAmendments":{"type":"integer","description":"Pending Amendments"},"cancellations":{"type":"integer","description":"Cancellations"},"voids":{"type":"integer","description":"Voids"},"reissues":{"type":"integer","description":"Reissues"},"dateTimeChanges":{"type":"integer","description":"Date/Time Changes"},"partialCancellations":{"type":"integer","description":"Partial Cancellations"},"pendingApprovals":{"type":"integer","description":"Pending Approvals"},"failedActions":{"type":"integer","description":"Failed Actions"},"slaBreaches":{"type":"integer","description":"SLA Breaches"},"requestId":{"type":"string","description":"Request ID"},"orderNumber":{"type":"string","description":"Order Number"},"customer":{"type":"string","description":"Customer"},"productEvent":{"type":"string","description":"Product/Event"},"originalValue":{"type":"string","description":"Original Value"},"financialImpact":{"type":"string","description":"Financial Impact"},"channel":{"type":"string","description":"Channel"},"requestedBy":{"type":"string","description":"Requested By"},"approvalStatus":{"type":"integer","description":"Approval Status"},"processingStatus":{"type":"integer","description":"Processing Status"},"createdTime":{"type":"string","format":"date-time","description":"Created Time"},"requestType":{"type":"string","enum":["orderAmendment","reservationAmendment","dateChange","timeslotChange","performanceChange","quantityChange","attendeeChange"],"description":"Request type."},"requestTypeCancellation":{"type":"boolean","description":"The request is a full or partial cancellation"}}},
"AmendmentEligibilityPolicyRuleBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in the amendment columns of `orders.after_sale_policy` (DM5, 29 September)","description":"**What Amendment Eligibility & Policy Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"tenant":{"type":"string","description":"Tenant"},"venue":{"type":"string","description":"Venue"},"product":{"type":"string","description":"Product"},"ticketType":{"type":"string","description":"Ticket Type"},"event":{"type":"string","description":"Event"},"performance":{"type":"string","description":"Performance"},"channel":{"type":"string","description":"Channel"},"customerSegment":{"type":"string","description":"Customer Segment"},"membership":{"type":"string","description":"Membership"},"orderStatus":{"type":"string","description":"Order Status"},"ticketStatus":{"type":"string","description":"Ticket Status"},"dateChange":{"type":"string","format":"date-time","description":"Date Change"},"timeslotChange":{"type":"string","description":"Timeslot Change"},"performanceChange":{"type":"string","description":"Performance Change"},"quantityIncrease":{"type":"integer","description":"Quantity Increase"},"quantityReduction":{"type":"integer","description":"Quantity Reduction"},"seatChange":{"type":"string","description":"Seat Change"},"attendeeChange":{"type":"string","description":"Attendee Change"},"deliveryChange":{"type":"string","description":"Delivery Change"},"otherPermittedModifications":{"type":"string","description":"Other permitted modifications"},"maximumAmendmentsPerOrder":{"type":"string","description":"Maximum Amendments per Order"},"maximumAmendmentsPerTicket":{"type":"string","description":"Maximum Amendments per Ticket"},"maximumDateChanges":{"type":"string","format":"date-time","description":"Maximum Date Changes"},"coolingPeriod":{"type":"string","format":"date-time","description":"Cooling Period"},"eligibleTicketStatuses":{"type":"array","items":{"type":"string","enum":["unused","partiallyUsed","fullyUsed","expired","cancelled","suspended"]},"description":"Ticket usage statuses from which amendment is allowed."}}},
"AmendmentEligibilityPolicyRuleBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Amendment Eligibility & Policy Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"tenant":{"type":"string","description":"Tenant"},"venue":{"type":"string","description":"Venue"},"product":{"type":"string","description":"Product"},"ticketType":{"type":"string","description":"Ticket Type"},"event":{"type":"string","description":"Event"},"performance":{"type":"string","description":"Performance"},"channel":{"type":"string","description":"Channel"},"customerSegment":{"type":"string","description":"Customer Segment"},"membership":{"type":"string","description":"Membership"},"orderStatus":{"type":"string","description":"Order Status"},"ticketStatus":{"type":"string","description":"Ticket Status"},"dateChange":{"type":"string","format":"date-time","description":"Date Change"},"timeslotChange":{"type":"string","description":"Timeslot Change"},"performanceChange":{"type":"string","description":"Performance Change"},"quantityIncrease":{"type":"integer","description":"Quantity Increase"},"quantityReduction":{"type":"integer","description":"Quantity Reduction"},"seatChange":{"type":"string","description":"Seat Change"},"attendeeChange":{"type":"string","description":"Attendee Change"},"deliveryChange":{"type":"string","description":"Delivery Change"},"otherPermittedModifications":{"type":"string","description":"Other permitted modifications"},"maximumAmendmentsPerOrder":{"type":"string","description":"Maximum Amendments per Order"},"maximumAmendmentsPerTicket":{"type":"string","description":"Maximum Amendments per Ticket"},"maximumDateChanges":{"type":"string","format":"date-time","description":"Maximum Date Changes"},"coolingPeriod":{"type":"string","format":"date-time","description":"Cooling Period"},"eligibleTicketStatuses":{"type":"array","items":{"type":"string","enum":["unused","partiallyUsed","fullyUsed","expired","cancelled","suspended"]},"description":"Ticket usage statuses from which amendment is allowed."},"exceptionRole":{"type":"string","enum":["agent","supervisor","manager"],"description":"Lowest role that may make an out-of-policy exception"}}},
"AmendmentHistoryAuditAfterSalesAnalyticsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Amendment History, Audit & After-Sales Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"requestId":{"type":"string","description":"Request ID"},"orderId":{"type":"string","description":"Order ID"},"ticketId":{"type":"string","description":"Ticket ID"},"customer":{"type":"string","description":"Customer"},"action":{"type":"string","description":"Action"},"beforeValue":{"type":"string","description":"Before Value"},"afterValue":{"type":"string","description":"After Value"},"financialImpact":{"type":"string","description":"Financial Impact"},"ruleApplied":{"type":"string","description":"Rule Applied"},"exception":{"type":"string","description":"Exception"},"approval":{"type":"string","description":"Approval"},"user":{"type":"string","description":"User"},"channel":{"type":"string","description":"Channel"},"timestamp":{"type":"string","format":"date-time","description":"Timestamp"},"result":{"type":"string","description":"Result"},"amendmentRate":{"type":"number","description":"Amendment Rate"},"cancellationRate":{"type":"number","description":"Cancellation Rate"},"averageRefund":{"type":"number","description":"Average Refund"},"exceptionRate":{"type":"number","description":"Exception Rate"},"approvalRate":{"type":"number","description":"Approval Rate"},"serviceRecoveryCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Service-Recovery Cost"},"anomalyType":{"type":"string","enum":["excessiveVoids","repeatedManualRefunds","frequentFeeWaivers","highReissueFrequency","repeatedOutOfPolicyExceptions"],"description":"Unusual pattern surfaced."}}},
"ApprovalExceptionServiceRecoveryManagementInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in `orders.after_sale_request` (DM5, 29 September)","description":"**What Approval, Exception & Service Recovery Management submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"requestedAction":{"type":"string","description":"Requested Action"},"customer":{"type":"string","description":"Customer"},"order":{"type":"string","description":"Order"},"standardPolicyResult":{"type":"string","description":"Standard Policy Result"},"requestedException":{"type":"string","description":"Requested Exception"},"financialImpact":{"type":"string","description":"Financial Impact"},"reason":{"type":"string","description":"Reason"},"supportingDocuments":{"type":"string","description":"Supporting Documents"},"requestor":{"type":"string","description":"Requestor"},"remedy":{"type":"string","enum":["complimentaryReissue","feeWaiver","partialRefund","voucher","walletCredit","alternativeDate","alternativeEvent","complimentaryAddOn"],"description":"Governed remedy granted."},"decision":{"type":"string","enum":["approve","reject","escalate"],"description":"Approver decision"}}},
"ApprovalExceptionServiceRecoveryManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Approval, Exception & Service Recovery Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"requestedAction":{"type":"string","description":"Requested Action"},"customer":{"type":"string","description":"Customer"},"order":{"type":"string","description":"Order"},"standardPolicyResult":{"type":"string","description":"Standard Policy Result"},"requestedException":{"type":"string","description":"Requested Exception"},"financialImpact":{"type":"string","description":"Financial Impact"},"reason":{"type":"string","description":"Reason"},"supportingDocuments":{"type":"string","description":"Supporting Documents"},"requestor":{"type":"string","description":"Requestor"},"remedy":{"type":"string","enum":["complimentaryReissue","feeWaiver","partialRefund","voucher","walletCredit","alternativeDate","alternativeEvent","complimentaryAddOn"],"description":"Governed remedy granted."},"decision":{"type":"string","enum":["approve","reject","escalate"],"description":"Approver decision"},"approvalLevel":{"type":"string","enum":["supervisor","manager","finance","director"],"description":"Approval level reached"}}},
"CancellationPartialCancellationPolicyConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in `orders.after_sale_policy` and its `orders.after_sale_policy_window` rows (DM5, 29 September)","description":"**What Cancellation & Partial Cancellation Policy Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"permittedScopes":{"type":"array","items":{"type":"string","enum":["entireOrder","entireReservation","individualTicket","selectedOrderLines","selectedQuantity","addOnOnly","groupMember","packageComponent"]},"description":"What may be cancelled."},"evaluatedConditions":{"type":"array","items":{"type":"string","enum":["orderStatus","paymentStatus","ticketStatus","usage","eventDate","cancellationWindow","product","channel","customerSegment"]},"description":"What the policy evaluates."},"windows":{"type":"array","description":"Cancellation windows; thresholds ascend (audit R123 (6))","items":{"type":"object","properties":{"minHoursBefore":{"type":"integer","description":"Window starts this many hours before the event"},"maxHoursBefore":{"type":"integer","description":"Window ends this many hours before the event (empty = no upper bound)"},"outcome":{"type":"string","enum":["permitted","permittedWithFee","notPermitted"],"description":"Outcome in this window"},"feePercent":{"type":"number","description":"Cancellation fee, percent"},"feeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cancellation fee, fixed"},"supervisorExceptionAllowed":{"type":"boolean","description":"A supervisor may override notPermitted"}}}},"reasonCodes":{"type":"array","items":{"type":"string","enum":["customerRequest","eventCancelled","operationalIssue","duplicateOrder","weather","serviceRecovery","fraudReview","other"]},"description":"Cancellation reason codes offered"}}},
"CancellationPartialCancellationPolicyConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Cancellation & Partial Cancellation Policy Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"permittedScopes":{"type":"array","items":{"type":"string","enum":["entireOrder","entireReservation","individualTicket","selectedOrderLines","selectedQuantity","addOnOnly","groupMember","packageComponent"]},"description":"What may be cancelled."},"evaluatedConditions":{"type":"array","items":{"type":"string","enum":["orderStatus","paymentStatus","ticketStatus","usage","eventDate","cancellationWindow","product","channel","customerSegment"]},"description":"What the policy evaluates."},"windows":{"type":"array","description":"Cancellation windows, e.g. over 72 hours permitted; 24-72 hours with fee; under 24 hours not permitted except supervisor exception. Thresholds ascend (audit R123 (6))","items":{"type":"object","properties":{"minHoursBefore":{"type":"integer","description":"Window starts this many hours before the event"},"maxHoursBefore":{"type":"integer","description":"Window ends this many hours before the event (empty = no upper bound)"},"outcome":{"type":"string","enum":["permitted","permittedWithFee","notPermitted"],"description":"Outcome in this window"},"feePercent":{"type":"number","description":"Cancellation fee, percent"},"feeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cancellation fee, fixed"},"supervisorExceptionAllowed":{"type":"boolean","description":"A supervisor may override notPermitted"}}}},"reasonCodes":{"type":"array","items":{"type":"string","enum":["customerRequest","eventCancelled","operationalIssue","duplicateOrder","weather","serviceRecovery","fraudReview","other"]},"description":"Cancellation reason codes offered"}}},
"CreateOrderLine": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","variantId","quantity","quotedUnitPrice"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these."},"variantId":{"type":"string","format":"uuid"},"recommendationId":{"type":"string","format":"uuid","nullable":true,"description":"The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation that led to it rather than guessed. Carried from the cart line at checkout; stored on `orders.order_line` and sent in `order.completed` lines.\n"},"performanceId":{"type":"string","format":"uuid"},"bookedWindow":{"$ref":"#/components/schemas/BookedWindow"},"inventoryHoldId":{"type":"string","nullable":true,"description":"Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products."},"seatIds":{"type":"array","maxItems":50,"items":{"type":"string","format":"uuid"},"description":"Seated products only, as `seating.Seat.id`. Not available offline. **At most `VenueSettings.seating.maxSeatsPerGuestOrder` seats per booking on a guest channel** (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); **at most 10 per sale on staff and POS** (audit R080 (c)), across all the lines of one order for one performance. `createOrder` refuses more with 422 `seatLimitExceeded` (problem type `seat-limit-exceeded`)."},"resourceHoldId":{"type":"string","format":"uuid","nullable":true,"description":"A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. `createOrder` converts the hold into a `ResourceBooking` without releasing it. Not available offline."},"attributes":{"$ref":"#/components/schemas/OrderLineAttributes"},"quantity":{"type":"integer","minimum":1},"eligibilityDeclaration":{"type":"array","nullable":true,"x-ticvai-note":"One row per declared guest in `orders.order_line_eligibility` (named on `OrderLine`), because an array of objects is a child table's rows, not a column.\n","items":{"type":"object","properties":{"ageBand":{"type":"string","enum":["infant","child","junior","adult","senior"],"description":"Infant under 3, child 3–12, junior 13–17, adult 18–59, senior 60+."},"ageYears":{"type":"integer","nullable":true},"heightBandIndex":{"type":"integer","nullable":true},"confidentSwimmer":{"type":"boolean","nullable":true,"description":"**Derived, kept for the gate check** (decided 29 September, rev 3 REV3-26). The swim question is a consent: the answer is a `marketing.BookingConsentRecord` of kind `swim`, and this is filled from it (true for a `yes` covering this person, whether answered for them or once for the booking). A value sent that contradicts the record is ignored and the record wins. No longer the place a swim answer is captured.\n"},"guardianSigned":{"type":"boolean"}}},"description":"What was declared for each guest on this line, kept as the record staff check at the gate."},"quotedUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the client charged, from its local bundle."},"holderName":{"type":"string","nullable":true},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"**Deliberately open.** Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the venue's to define, as on `catalogue`'s own `dataMaskValues`.\n"}}},
"Entitlement": {"type":"object","x-ticvai-persistence":"access.entitlement","description":"**What a guest actually holds.** Found missing on 18 August by the schema audit — 33 tables in `orders`, seven in `access`, and none of them stored an issued ticket.\nThe package sold products, defined `EntitlementTemplate`, recorded `ScanEvent.ticketId`, transferred `ticket_transfer.ticketIds` and issued `wallet_pass.entitlementId` — **five artefacts referring to a thing that did not exist.** `validateAccess` read the *template* and never the instance, and `suspendEntitlement` suspended the template, **which would have suspended it for every guest who held one.**\n**The template is the definition and this is the instance.** A template says *an annual pass admits once a day for a year*; this says *this guest's annual pass, bought on 3 March, used eleven times, frozen for two weeks in July, valid until 2 March.*\n","required":["id","templateId","productId","orderId","subjectId","status","validFrom","validTo"],"properties":{"id":{"type":"string","format":"uuid","description":"A UUIDv7, matching `TicketStatus.ticketId` — **stable for the life of the ticket and independent of the media carrying it.** A guest whose wristband broke keeps the same entitlement with a new `mediaCode`.\n**This is the ticket id.** Wherever an operation takes a `ticketId` or `ticketIds` — `lookupTicket`, `listScans`, `ScanEvent`, the offline package and `transferOrderTickets` — it is this value. An order line's `entitlementIds` are the ticket ids of that line.\n"},"templateId":{"type":"string","format":"uuid","description":"The definition it was issued against. **Pinned at issue** — a template edited next month must not change what this guest bought.\n"},"productId":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","description":"The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`)."},"orderLineId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Who holds it. **Null is legitimate** — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is claimed.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"mediaCode":{"type":"string","description":"What is scanned — a QR payload, a wristband serial, a card number. **Rotatable without reissuing**, because a guest whose wristband broke should not need a new ticket.\n"},"status":{"$ref":"../spine/orders.yaml#/components/schemas/EntitlementStatus"},"statusNote":{"type":"string","nullable":true,"description":"**Not `TicketStatus` — that is a validation result with a misleading name**, computed at scan time and carrying `isValid` and `isInsideVenue`. The lifecycle is `orders.EntitlementStatus`, and `states/entitlement-status.yaml` has modelled it since before this table existed.\n**Which is the finding in one line: the package had the lifecycle, the state model and the validation result, and no row to hang them on.**\n"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time","description":"**Resolved at issue from the template, then owned here.** A freeze extends it, a reissue replaces it, and neither reaches back to the template.\n**What the pre-expiry notice is measured from** (29 September, build pass, group G2; 5.5.30). A daily run in access publishes `entitlement.expiringSoon` once per entitlement and `validTo` when an entitlement in `issued` or `partiallyConsumed` comes within its template's `expiryNoticeDays` (`catalogue.EntitlementTemplate`), and not for one bought inside that window. Marketing turns it into the reminder (a `MessageTrigger` on the event, or a triggered campaign on `entitlementExpiring`); access only says the date is near. A freeze or renewal that moves `validTo` raises the next notice once.\n"},"entriesUsed":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**The number `validateAccess` decrements and nothing was decrementing.** A ten-entry pass with no counter is a ten-entry pass that admits forever.\n**Maintained on write**, in the same transaction as the admitting `access.scan_event` row: by `validateAccess`, `validateGroupAccess` (by the count admitted) and `syncScans` for each replayed admission the server accepts. A replayed scan the server downgrades to `denied` does not count.\n"},"entriesAllowed":{"type":"integer","nullable":true},"lastEntryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. A scan replayed late with an earlier `recordedAt` does not move it back.\n"},"firstEntryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`recordedAt` of the first admission, written by the same writes as `lastEntryAt`; it starts a time-bound entitlement's window (DEC-232; CHG-CSP-030). A replayed earlier scan moves it back."},"timeBoundUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Where the template is time-bound, when its window closes**: `firstEntryAt` plus the validity rule's `minutesAfterFirstScan` (decided 2 October 2026, Chinmay, BO-159; DEC-232; CHG-CSP-030). Null until the first scan and on an entitlement with no time bound. A scan after it is denied (`timeBoundWindowElapsed`); it never extends `validTo`, and the earlier of the two wins."},"lifecycleLabel":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","enum":["created","pendingFulfillment","active","partiallyUsed","used","expired","suspended","cancelled","voided","reissuedSuperseded","refunded","transferred","blocked"],"description":"**The Virtual Ticket status in the client's 13 names, mapped onto the entitlement model** (decided 2 October 2026, Chinmay, critical set 2, BO-336: \"Map the pack's 13 names onto the model; add any missing states\", and BO-336/DI-670: \"Reserved maps to Pending fulfilment\"; DEC-266; CHG-CSP-033). Computed on read from `status` (orders `EntitlementStatus`), `suspendedReason`, `cancellationKind`, `issuedVia` and an active identity lock; the mapping is in `states/entitlement-status.yaml`. It is what BO-334, BO-336 and the ticket status transition matrix (`AccessTicketStatusTransition`) show; logic still reads `status`."},"cancellationKind":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","enum":["voided","refunded","performanceCancelled","superseded"],"description":"**Which act cancelled the entitlement**, so the pack's Voided, Refunded and Reissued / superseded are told apart while `status` keeps the one r1 value `cancelled` (DEC-266; CHG-CSP-033). Written with the cancelling transition: `voidEntitlement`, `createRefund`, `cancelPerformance`, or a reissue that supersedes it (`supersedesEntitlementId` on the new one). Null unless `cancelled`."},"frozenDays":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"Days added by a freeze. **Maintained on write** by the freeze operation (`freezeEntitlement`), in the same write that extends `validTo` by those days. **Held here rather than computed from a freeze log**, because a gate has to answer in under 300ms and cannot replay a history to decide validity.\n"},"suspendedReason":{"type":"string","nullable":true},"freezeReason":{"type":"string","nullable":true,"enum":["travelling","injury","personal","seasonal","other"],"description":"The `reason` of the latest `freezeEntitlement` (audit R222). Null when never frozen."},"freezeNote":{"type":"string","nullable":true,"maxLength":500,"description":"The `note` the latest `freezeEntitlement` took, required there when `reason` is `other` (decided 28 September, audit R222). Kept so the quarterly review of `other` notes has something to read."},"isNameBound":{"type":"boolean","default":false},"holderName":{"type":"string","nullable":true},"sharedWithSubjectIds":{"type":"array","description":"`shareEntitlement`. **The owner keeps it and a second person may present it** — the asymmetry that stops a shared family pass becoming a resale chain.\n","items":{"type":"string","format":"uuid"}},"issuedVia":{"type":"string","enum":["sale","invitation","reissue","transfer","resale","membership","groupBooking"],"description":"**How it came to exist, and it matters to finance.** A sold entitlement carries deferred revenue; an invitation carries a marketing cost; a reissue carries neither.\n"},"supersedesEntitlementId":{"type":"string","format":"uuid","nullable":true,"description":"For a reissue or a resale. **The chain is traceable** — a ticket appearing from nowhere is indistinguishable from a fraudulent one.\n"},"walletValueId":{"type":"string","format":"uuid","nullable":true,"description":"Where the template carries stored value. **A `retail.Wallet` bound to the entitlement, not a balance on it** (CF-126).\n"},"facePassEnrolmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"The active `facePass` enrolment on this entitlement (`FacePassEnrolment.id`), or null when none is. **Computed on read from `pii.subject_biometric` and not stored here** — the PII split keeps the biometric on its own side, and this carries only its id. It is how a screen holding a pass finds the enrolment `getFacePassEnrolment` and `revokeFacePass` take.\n"}}},
"ExchangeOrderRequest": {"type":"object","required":["id","outgoingLineIds","incomingLines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of this exchange, and its idempotency key — it must equal the `Idempotency-Key` header."},"outgoingLineIds":{"type":"array","minItems":1,"items":{"type":"string","format":"uuid"}},"incomingLines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"waiveFee":{"type":"boolean","default":false},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"FailedPaymentCleanupInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `cleanupFailedPayment` takes (decided 29 September, readiness close-out).","required":["action","reason"],"properties":{"action":{"type":"string","description":"How the payment is cleared (decided 29 September, readiness close-out).","enum":["releaseHold","cancelPending","markAbandoned"]},"reason":{"type":"string","minLength":3,"maxLength":500}}},
"ModifyOrderRequest": {"type":"object","required":["id","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 **of this modification, not of the order** — the order is the path's `orderId`. It is the modification's idempotency key and must equal the `Idempotency-Key` header.\n"},"addLines":{"type":"array","items":{"$ref":"#/components/schemas/CreateOrderLine"}},"removeLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**The currency the guest selected and is charged in** (CHG-FIN-001, 2 October 2026). Null or equal to `currency` for a sale in the base currency. Everything else on the order, and every ledger posting, stays in the base currency `currency`."},"chargeFxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`), stored on the order so the payment, the receipt, the tax invoice and any refund use the same rate (CHG-FIN-001)."},"chargeFxRateId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `finance.FxRate` row the rate was taken from, for audit."},"chargeTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"`grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to the provider asks for (CHG-FIN-001)."},"chargeRateLockedUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms the new amount (CHG-FIN-001)."},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderExchangeResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["orderId","outgoingValue","incomingValue","difference"],"properties":{"orderId":{"type":"string","format":"uuid"},"outgoingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"incomingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"exchangeFee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Only the difference settles. The replacement is held before the original is released, never the other way round.\n"},"newLineIds":{"type":"array","items":{"type":"string","format":"uuid"}},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderModificationResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["order","balanceDue"],"properties":{"order":{"$ref":"#/components/schemas/Order"},"addedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"removedValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceDue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Positive means the guest pays; negative means a refund is due."},"refundId":{"type":"string","format":"uuid","nullable":true},"revokedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"issuedEntitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n**Cash at a till only** (CHG-FIN-001, 2 October 2026). A card or wallet payment the guest made in a currency they selected is refunded in that currency (`Refund.tenderCurrency`).\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"RefundCalculationPolicyInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `setRefundCalculationPolicy` takes (decided 29 September, readiness close-out).","required":["refundTypes","refundDestinations"],"properties":{"refundTypes":{"type":"array","minItems":1,"description":"The calculations a refund may use (decided 29 September, readiness close-out).","items":{"type":"string","enum":["fullRefund","partialRefund","percentageRefund","proRataRefund","originalValueLessFees"]}},"refundDestinations":{"type":"array","minItems":1,"description":"Where refunded money may go (decided 29 September, readiness close-out).","items":{"type":"string","enum":["originalPayment","walletCredit","voucherCreditNote"]}},"percentage":{"type":"number","minimum":0,"maximum":100,"nullable":true,"description":"Required when `percentageRefund` is allowed."},"nonRefundableFees":{"type":"array","description":"Order-fee categories (`orders.order_fee.category`) that `originalValueLessFees` keeps back.","items":{"type":"string","maxLength":20}},"scope":{"type":"object","nullable":true,"description":"Narrows the policy; null applies it venue-wide.","properties":{"productIds":{"type":"array","items":{"type":"string","format":"uuid"}},"channels":{"type":"array","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}}}}}},
"RefundCalculationPolicyView": {"type":"object","x-ticvai-persistence":"orders.refund_calculation_policy","description":"**How a venue calculates a refund and where the money goes.** Set by `setRefundCalculationPolicy` (decided 29 September, readiness close-out). The authority limits and time bands stay on `RefundPolicy`.\n","required":["refundTypes","refundDestinations"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"refundTypes":{"type":"array","items":{"type":"string","enum":["fullRefund","partialRefund","percentageRefund","proRataRefund","originalValueLessFees"]}},"refundDestinations":{"type":"array","items":{"type":"string","enum":["originalPayment","walletCredit","voucherCreditNote"]}},"percentage":{"type":"number","minimum":0,"maximum":100,"nullable":true},"nonRefundableFees":{"type":"array","items":{"type":"string","maxLength":20}},"scope":{"type":"object","nullable":true,"properties":{"productIds":{"type":"array","items":{"type":"string","format":"uuid"}},"channels":{"type":"array","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}}}},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"RefundPolicy": {"x-ticvai-persistence":"orders.refund_policy + orders.refund_policy_time_band","type":"object","description":"Venue-configured. Thresholds are policy, not permission scope — venues run different policies and the permission model should not encode commercial rules.\n**The three thresholds must ascend** (decided 28 September, audit R123 (6)): `selfAuthoriseLimit` <= `requiresSecondUserAbove` <= `requiresApprovalAbove`, where the second is set. `setRefundPolicy` refuses a policy that does not with 422 `refund-thresholds-not-ascending`.\n","required":["venueId","selfAuthoriseLimit","requiresApprovalAbove"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The venue in the path. Not taken from a `setRefundPolicy` body."},"selfAuthoriseLimit":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Up to this, a holder of ORDER_REFUND refunds alone. Zero means every refund needs a second authoriser.\n"},"requiresSecondUserAbove":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Above this, a second user — cashier OR supervisor — names themselves as audit control. Dual-authorisation, not escalation (2.12.3).\n"},"requiresApprovalAbove":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Above this, an ORDER_REFUND_APPROVE holder must approve."},"timeBands":{"type":"array","description":"Refundable percentage by time before the performance. Evaluated most-specific first.\n","items":{"type":"object","required":["hoursBefore","percentage"],"properties":{"hoursBefore":{"type":"integer","minimum":0},"percentage":{"type":"number","minimum":0,"maximum":100}}}},"allowPartial":{"type":"boolean","default":true},"refundWindowDays":{"type":"integer","nullable":true,"minimum":0,"description":"Days after purchase within which a refund may be made. 0 is allowed and means the day of purchase only; null means no window (decided 28 September, audit R123 (6))."},"varianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Price variance above this is an exception requiring review rather than a routine posting (CF-38). Venue-configured.\n**A venue setting with a tenant default** (decided 28 September, audit R094). **Proposed default, client to correct (audit R094): AED 5.00 per order line.**\n"}}},
"TenderKind": {"type":"string","description":"`wallet` is a **digital wallet** (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 (a)). **The stored-value TICVAI wallet is a separate tender**: it is spent through `authoriseStoredValue` and `captureStoredValue` (`StoredValueKind` `wallet`), never as this value, so the client can see which of the two the decision meant.\n","enum":["cash","card","wallet","voucher","bankTransfer","hotelCharge","installment","giftCard","complimentary"]},
"VoidEntitlementInput": {"type":"object","x-ticvai-persistence":"none — request only","description":"What `voidEntitlement` takes. The reason comes from the void reason list, as for `voidOrder` (decided 29 September, readiness close-out).","required":["reason","recordedAt"],"properties":{"reason":{"$ref":"#/components/schemas/VoidReason"},"note":{"type":"string","minLength":3,"maxLength":500,"nullable":true,"description":"Required when `reason` is `other`; optional otherwise."},"recordedAt":{"type":"string","format":"date-time"}}},
"VoidReason": {"type":"string","description":"**The void reason list** (decided 28 September, audit R125 (4)): the one list `voidOrder` takes, and the list `fnb.amendFnbOrder` and `fnb.cancelFnbOrder` point to. `other` requires a note (audit R222), and the notes are reviewed quarterly to add real reasons. Proposed, client to correct.\n","enum":["guestChangedMind","enteredInError","itemUnavailable","qualityIssue","duplicate","other"]},
"VoidReversalSameDayCorrectionManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Void, Reversal & Same-Day Correction Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"sameBusinessDayOnly":{"type":"string","description":"Same Business Day Only"},"beforeSettlement":{"type":"string","description":"Before Settlement"},"beforeTicketUse":{"type":"string","description":"Before Ticket Use"},"beforeFiscalClosure":{"type":"string","description":"Before Fiscal Closure"},"supervisorRequired":{"type":"boolean","description":"Supervisor Required"},"specificChannelsOnly":{"type":"string","description":"Specific Channels Only"},"rolePermission":{"type":"string","description":"Role Permission"},"supervisorApproval":{"type":"string","description":"Supervisor Approval"},"optionalDualAuthorization":{"type":"string","description":"Optional Dual Authorization"},"voidType":{"type":"string","enum":["orderVoid","paymentVoidRequest","ticketVoid","accidentalSaleReversal","sameDayCorrection","failedTransactionCleanup"],"description":"What is voided or reversed."},"reasonCode":{"type":"string","enum":["operatorError","wrongProduct","wrongQuantity","wrongPayment","technicalFailure"],"description":"Mandatory reason."}}}
}
```
