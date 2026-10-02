# WS33 — Order   Reservation Management board 3

**10 screens · 21 operations · 26 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `ORDER_CREATE, ORDER_MODIFY, ORDER_VIEW, PAYMENT_CONFIGURE, PAYMENT_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `BO-324` | Payment & Order Financial Command Center | B–D | 2 | 46 | 6 | 1 | 1 | 0 | — | notStarted (generated) |
| `BO-325` | Order Payment Detail & Transaction Ledger | B–D | 0 | 20 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-326` | Multi-Payment, Split Tender & Payment Allocation Configuration | B–D | 16 | 9 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-327` | Deposit, Partial Payment & Outstanding Balance Management | B–D | 21 | 26 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-328` | Order Split, Merge & Transaction Relationship Management | B–D | 2 | 0 | 6 | 2 | 0 | 2 | — | notStarted (generated) |
| `BO-329` | Related Order & Transaction Relationship Explorer | B–D | 2 | 14 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-330` | External Payment, Partner & Settlement Reference Mapping | B–D | 26 | 12 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-331` | Payment Reconciliation & Exception Management | B–D | 0 | 2 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-332` | Financial Traceability, Control & Audit Explorer | B–D | 1 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-333` | Order Financial Analytics & AI Reconciliation Intelligence | B–D | 2 | 10 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-331, BO-332 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-324` Payment & Order Financial Command Center

**Provide operations and finance teams with a centralized view of the financial status of all**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_VIEW`, `PAYMENT_VIEW` (1 operate, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/payment-order-financial-command-center-bo-324` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The financial status of orders: paid, part-paid, outstanding, instalment plans and their next due dates.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listPaymentOrderFinancial return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listPaymentOrderFinancial; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search payment order financial | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, channel, payment method, payment provider, currency, order status and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listPaymentOrderFinancial` ?venue |
| Payment provider | text field | — | — | `listPaymentOrderFinancial` ?paymentProvider |
| Currency | text field | — | — | `listPaymentOrderFinancial` ?currency |
| Order status | text field | — | — | `listPaymentOrderFinancial` ?orderStatus |
| Order | picker: choose an order | — | — | `listInstalmentPlans` ?orderId |
| Status | radio group | — | Active · Completed · In arrears · Cancelled | `listInstalmentPlans` ?status |

#### Outputs: what the screen shows and produces

**Shown**

**Every payment order financial** (data table, from `listPaymentOrderFinancial`)

| Shows | Format | Notes |
|---|---|---|
| Gross order value | text | Gross Order Value |
| Fully paid orders | 1,234 | Fully Paid Orders |
| Partially paid orders | 1,234 | Partially Paid Orders |
| Unpaid orders | 1,234 | Unpaid Orders |
| Outstanding balance | AED 1,234.50 | Outstanding Balance |
| Payments today | text | Payments Today |
| Failed payments | 1,234 | Failed Payments |
| Pending payments | 1,234 | Pending Payments |
| Refunds pending | 1,234 | Refunds Pending |
| Reconciliation exceptions | 1,234 | Reconciliation Exceptions |
| Unallocated payments | 1,234 | Unallocated Payments |
| Settlement variance | text | Settlement Variance |
| Order | text | Order ID |
| Customer | text | Customer |
| Channel | text | Channel |
| Order value | text | Order Value |
| Amount paid | AED 1,234.50 | Amount Paid |
| Refunded | text | Refunded |
| Outstanding | text | Outstanding |
| Payment methods | 1,234 | Payment Methods |
| Payment status | chip: Not required, Unpaid, Payment initiated, Authorized, Partially paid, Paid… | Payment status |
| Settlement status | 1,234 | Settlement Status |
| Reconciliation status | 1,234 | Reconciliation Status |

**The selected payment order financial** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Gross order value | text | Gross Order Value |
| Fully paid orders | 1,234 | Fully Paid Orders |
| Partially paid orders | 1,234 | Partially Paid Orders |
| Unpaid orders | 1,234 | Unpaid Orders |
| Outstanding balance | AED 1,234.50 | Outstanding Balance |
| Payments today | text | Payments Today |
| Failed payments | 1,234 | Failed Payments |
| Pending payments | 1,234 | Pending Payments |
| Refunds pending | 1,234 | Refunds Pending |
| Reconciliation exceptions | 1,234 | Reconciliation Exceptions |
| Unallocated payments | 1,234 | Unallocated Payments |
| Settlement variance | text | Settlement Variance |
| Order | text | Order ID |
| Customer | text | Customer |
| Channel | text | Channel |
| Order value | text | Order Value |
| Amount paid | AED 1,234.50 | Amount Paid |
| Refunded | text | Refunded |
| Outstanding | text | Outstanding |
| Payment methods | 1,234 | Payment Methods |
| Payment status | chip: Not required, Unpaid, Payment initiated, Authorized, Partially paid, Paid… | Payment status |
| Settlement status | 1,234 | Settlement Status |
| Reconciliation status | 1,234 | Reconciliation Status |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Payment Initiated (primary button) | navigation or local | — | — | — | — |
| Authorized (secondary button) | navigation or local | — | — | — | — |
| Failed (secondary button) | navigation or local | — | — | — | — |
| Reconciliation Required (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **finance view**: Outstanding balances and plans due this week first. *(source: contracts/spine/orders.yaml#listPaymentOrderFinancial / contracts/satellite/payments.yaml#listInstalmentPlans)*

**Data it reads**: `listPaymentOrderFinancial` (onLoad, Payment & Order Financial Command Center); `listInstalmentPlans` (onLoad, Instalment plans and schedule)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-325` Order Payment Detail & Transaction Ledger: *Works in Order Payment Detail & Transaction Ledger*; calls `listPaymentOrderFinancial`
- → `BO-326` Multi-Payment, Split Tender & Payment Allocation Configuration: *Works in Multi-Payment, Split Tender & Payment Allocation Configuration*; calls `listPaymentOrderFinancial`
- → `BO-327` Deposit, Partial Payment & Outstanding Balance Management: *Works in Deposit, Partial Payment & Outstanding Balance Management*; calls `listPaymentOrderFinancial`
- → `BO-329` Related Order & Transaction Relationship Explorer: *Works in Related Order & Transaction Relationship Explorer*; calls `listPaymentOrderFinancial`
- → `BO-331` Payment Reconciliation & Exception Management: *Works in Payment Reconciliation & Exception Management*; calls `listPaymentOrderFinancial`
- → `BO-332` Financial Traceability, Control & Audit Explorer: *Works in Financial Traceability, Control & Audit Explorer*; calls `listPaymentOrderFinancial`
- → `BO-333` Order Financial Analytics & AI Reconciliation Intelligence: *Works in Order Financial Analytics & AI Reconciliation Intelligence*; calls `listPaymentOrderFinancial`
- → `BO-328` Order Split, Merge & Transaction Relationship Management: *Works in Order Split, Merge & Transaction Relationship Management*; carries `orderId`; calls `listPaymentOrderFinancial`
- → `BO-330` External Payment, Partner & Settlement Reference Mapping: *Works in External Payment, Partner & Settlement Reference Mapping*; carries `orderId`; calls `listPaymentOrderFinancial`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment order financial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment order financial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment order financial yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment order financial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The order already has a plan, or is already paid in full.; 422 The order or product does not qualify under the instalment policy, or the count or frequency is outside it, or the first instalment was declined. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
plans:
- order: MB-2026-0112
  next: '2026-12-01'
  amount: AED 120.83
```

#### Permissions

- `listPaymentOrderFinancial` → `ORDER_VIEW` (read) · staff
- `listInstalmentPlans` → `PAYMENT_VIEW` (read) · staff, guest
- `createInstalmentPlan` → `ORDER_CREATE` (operate) · staff, guest, service

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.2.17 | The system shall support recurring and subscription-based payments for memberships, annual passes, installment plans, wallet auto-top-ups, and auto-renewal products. | Bundles and Promotions | CONTRACTED | `createInstalmentPlan` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-324` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-324`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 3
- Flow F142 *Order Reservation Management board 3: Payment & Order Financial Command Center*, step 1: Opens Payment & Order Financial Command Center → Provide operations and finance teams with a centralized view of the financial status of all
- Flow F142 *Order Reservation Management board 3: Payment & Order Financial Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F142 *Order Reservation Management board 3: Payment & Order Financial Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F142 *Order Reservation Management board 3: Payment & Order Financial Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F142 *Order Reservation Management board 3: Payment & Order Financial Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F142 *Order Reservation Management board 3: Payment & Order Financial Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F142 *Order Reservation Management board 3: Payment & Order Financial Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F142 *Order Reservation Management board 3: Payment & Order Financial Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F142 branch at step 1 (expected): when Nothing has been set up on Payment & Order Financial Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F142 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (46 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-324?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Payment Initiated, Authorized, Failed, Reconciliation Required.
- [ ] Every transition is wired: `BO-100`, `BO-325`, `BO-326`, `BO-327`, `BO-329`, `BO-331`, `BO-332`, `BO-333`, `BO-328`, `BO-330`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_VIEW`, `PAYMENT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-325` Order Payment Detail & Transaction Ledger

**Provide the complete payment history associated with an individual order.**

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
| Route | `/orders-money/order-payment-detail-transaction-ledger-bo-325` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Every payment on one order: tender, amount, status, provider reference, refunds.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listOrderPaymentDetail return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listOrderPaymentDetail carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listOrderPaymentDetail; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every order payment detail** (data table, from `listOrderPaymentDetail`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | Order Number |
| Customer | text | Customer |
| Order total | text | Order Total |
| Currency | text | Currency |
| Paid | text | Paid |
| Refunded | text | Refunded |
| Outstanding | text | Outstanding |
| Credit applied | text | Credit Applied |
| Payment status | 1,234 | Payment Status |
| Settlement status | 1,234 | Settlement Status |

**The selected order payment detail** (detail panel): The pack groups this record's detail under its own headings: “Transaction Ledger”, “Type Status”, “PAY-001 Visa Settled”, “PAY-002 Wallet Settled”, “REF-001 Refund Visa”, “Immutable Financial History”.

| Shows | Format | Notes |
|---|---|---|
| Order number | text | Order Number |
| Customer | text | Customer |
| Order total | text | Order Total |
| Currency | text | Currency |
| Paid | text | Paid |
| Refunded | text | Refunded |
| Outstanding | text | Outstanding |
| Credit applied | text | Credit Applied |
| Payment status | 1,234 | Payment Status |
| Settlement status | 1,234 | Settlement Status |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Capture (primary button) | navigation or local | — | — | — | — |
| Payment (secondary button) | navigation or local | — | — | — | — |
| Deposit (secondary button) | navigation or local | — | — | — | — |
| Additional Collection (secondary button) | navigation or local | — | — | — | — |
| Refund (secondary button) | navigation or local | — | — | — | — |
| Partial Refund (secondary button) | navigation or local | — | — | — | — |
| Void (destructive button) | navigation or local | — | — | — | — |
| Reversal (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **payment ledger**: Chronological with running balance; card masked. *(source: contracts/spine/orders.yaml#listOrderPaymentDetail / DI-069)*

**Data it reads**: `listOrderPaymentDetail` (onLoad, Order Payment Detail & Transaction Ledger)

**Where the user goes next**

- → `BO-324` Payment & Order Financial Command Center: *Returns to the board's landing screen*; calls `listOrderPaymentDetail`

**What opens over it**

- confirmDialog *Void*: **Void on a order payment detail is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order payment detail list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order payment detail untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order payment detail yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the order payment detail are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
payment:
  tender: Card •••• 4417
  amount: AED 1,180.00
  status: captured
```

#### Permissions

- `listOrderPaymentDetail` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Transactions ledger lists all transactions with daily counts/totals and pending/failed sync status; detail shows chart-of-account mapping, payment method, product lines and whether each line is in sale, deferred or redemption status. *(client request · MoM 12 Aug 2026, 15. Financial Transactions Ledger and Journal Entries · DI-264)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-325` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-325`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 3
- Flow F142 *Order Reservation Management board 3: Payment & Order Financial Command Center*, step 2: Works in Order Payment Detail & Transaction Ledger → Provide the complete payment history associated with an individual order.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-325?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Capture, Payment, Deposit, Additional Collection, Refund, Partial Refund, Void, Reversal.
- [ ] Every transition is wired: `BO-324`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-326` Multi-Payment, Split Tender & Payment Allocation Configuration

**Support orders paid using multiple payment methods and determine how each payment is allocated.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_CREATE`, `ORDER_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure by; Configure whether payment is allocated) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/multi-payment-split-tender-payment-allocation-configurat-bo-326` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** How a split-tender payment is allocated (order, line, product, tax and fee component, ticket, deposit), per channel, terminal and product.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Channel | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Terminal | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Order Type | select field | — | — | — | — | — | — |
| Customer Type | select field | — | — | — | — | — | — |
| Order Level | select field | — | — | — | — | — | — |
| Order-Line Level | select field | — | — | — | — | — | — |
| Product Level | select field | — | — | — | — | — | — |
| Tax/Fee Component | select field | — | — | — | — | — | — |
| Specific Ticket | select field | — | — | — | — | — | — |
| Deposit | select field | — | — | — | — | — | — |
| Channel | text field | optional | — | max length 40 | — | Sends `?channel=` to `listPaymentAllocationRules`. | `listPaymentAllocationRules` ?channel |
| Terminal id | picker: choose a terminal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?terminalId=` to `listPaymentAllocationRules`. | `listPaymentAllocationRules` ?terminalId |
| Product id | picker: choose a product (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?productId=` to `listPaymentAllocationRules`. | `listPaymentAllocationRules` ?productId |
| Is active | toggle | optional | on | — | — | Sends `?isActive=` to `listPaymentAllocationRules`. | `listPaymentAllocationRules` ?isActive |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **allocationLevel**: One level per rule; rules listed beside. *(source: contracts/spine/orders.yaml#setMultiPaymentSplit / contracts/spine/orders.yaml#listPaymentAllocationRules)*

#### Outputs: what the screen shows and produces

**Shown**

**Every payment allocation rule** (data table, from `listPaymentAllocationRules`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Channel | text | — |
| Terminal | the name it points at, never the id | — |
| Product | the name it points at, never the id | — |
| Order type | text | — |
| Customer type | text | — |
| Allocation level | chip: Order level, Order line level, Product level, Tax fee component, Specific ticket … | — |
| Is active | yes / no (icon or chip) | — |
| Scope path | text | The partition key (ADR-0005). Operations write it at `venue` scope. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listPaymentAllocationRules` (onLoad, The venue's split-tender allocation rules)

**Where the user goes next**

- → `BO-324` Payment & Order Financial Command Center: *Returns to the board's landing screen*; calls `setMultiPaymentSplit`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-payment split tender configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-payment split tender untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-payment split tender configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule:
  channel: Point of sale
  level: orderLineLevel
```

#### Permissions

- `setMultiPaymentSplit` → `ORDER_CREATE` (operate) · staff
- `listPaymentAllocationRules` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-326` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-326`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 3
- Flow F142 *Order Reservation Management board 3: Payment & Order Financial Command Center*, step 4: Works in Multi-Payment, Split Tender & Payment Allocation Configuration → Support orders paid using multiple payment methods and determine how each payment is allocated.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (403, 412).
- [ ] Every output is drawn (9 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-326?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `BO-324`.
- [ ] Every gated control is gated: `ORDER_CREATE`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-327` Deposit, Partial Payment & Outstanding Balance Management

**Support commercial scenarios where an order may be confirmed or reserved without full immediate payment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW`, `PAYMENT_CONFIGURE`, `PAYMENT_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (3 read, 2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `depositId` (navigation) |
| Route | `/orders-money/deposit-partial-payment-outstanding-balance-management-bo-327` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Deposits and balances: how deposits work (fixed, per guest, percent, bands), when the balance is due, and the movements on each deposit.

**Known correction pending (do not draw the wrong version)**

- **recordDepositActivity takes amount as a plain number and type as free text.** Why: Money and an enumerated movement type (authorise, capture, release, forfeit). *(source: contracts/satellite/payments.yaml#recordDepositActivity; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **List operation(s) listDepositPartialPayment, listDepositActivity return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listDepositPartialPayment carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listDepositPartialPayment / contracts/satellite/payments.yaml#listDepositActivity; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Form: Save table deposit** (modal, opened by *Save table deposit*; *Save table deposit* calls `setDepositPolicy`, *Cancel* sends nothing)

**Collects the `dining` block of what `setDepositPolicy` sends before it is called** (decided 29 September, rev 3 REV3-8b). `enabled` (off by default), `basis` (`fixedPerGuest`, `fixedPerTable` or `percentOfMinimumSpend`), `amount` for the fixed bases, `percent` and `minimumSpendPerGuest` for the percentage basis, `appliesFromPartySize`, `outletIds` (empty means every outlet that takes bookings), `collection` (authorise and capture only on a late cancel or no-show, or charge), `depositVariantId`, `refundableUntilHours`, `onLateCancelOrNoShow`, `onArrival`. **Switched on with no amount or percent for its basis, or no deposit variant, it is refused `400`** and the modal stays open with the …

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Applies to `appliesTo` | multi-select chips | optional | — | Party · Dining · School · Event | — | Which bookings the top-level `basis` covers. `dining` is deprecated here since 29 September (rev 3 REV3-8b): a table deposit is the `dining` block below, with its own switch … | `setDepositPolicy` body |
| Dining `dining` | group | optional | — | — | — | The table deposit hold: a venue option, off unless the venue enables it (decided 29 September, rev 3 REV3-8b, superseding audit R077 (a) "no table deposit in the first release" … | `setDepositPolicy` body |
| Enabled `dining.enabled` | toggle | optional | off | — | — | Off unless the venue enables it. While false every other field is kept but not applied. | `setDepositPolicy` body |
| Basis `dining.basis` | segmented control | optional | Fixed per guest | Fixed per guest · Fixed per table · Percent of minimum spend | — | `fixedPerGuest`, `amount` times the party size; `fixedPerTable`, `amount` once per booking; `percentOfMinimumSpend`, `percent` of `minimumSpendPerGuest` times the party size. | `setDepositPolicy` body |
| Amount `dining.amount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Required for the two fixed bases. | `setDepositPolicy` body |
| Percent `dining.percent` | stepper or slider (%) | optional | — | min 0; max 100 | — | Required for `percentOfMinimumSpend`. | `setDepositPolicy` body |
| Minimum spend per guest `dining.minimumSpendPerGuest` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Required for `percentOfMinimumSpend`. | `setDepositPolicy` body |
| Applies from party size `dining.appliesFromPartySize` | stepper or slider | optional | 1 | min 1; max 50 | — | A party smaller than this books with no deposit. Proposed default, client to correct. | `setDepositPolicy` body |
| Outlets `dining.outletIds` | multi-picker: choose outlets | optional | — | — | — | The outlets it applies to. Empty means every outlet of the venue that takes bookings. | `setDepositPolicy` body |
| Collection `dining.collection` | segmented control | optional | Authorisation hold | Authorisation hold · Charge | — | `authorisationHold` authorises the card and captures only on a late cancel or no-show; `charge` takes the money now and holds it as a deposit. | `setDepositPolicy` body |
| Deposit variant `dining.depositVariantId` | picker: choose a deposit variant | optional | — | — | shows names, sends the id | The catalogue variant the deposit line is sold as: a non-inventory product the venue set up whose ledger mapping posts to deposit liability, not revenue. | `setDepositPolicy` body |
| Refundable until hours `dining.refundableUntilHours` | number field (hours) | optional | 24 | min 0; max 168 | — | Cancelling at least this long before the booking releases the deposit in full. Proposed default, client to correct. | `setDepositPolicy` body |
| On late cancel or no show `dining.onLateCancelOrNoShow` | segmented control | optional | Forfeit | Forfeit · Release | — | What happens to the deposit on a later cancel or a `noShow`. Settled through `finance.settleDeposit`. | `setDepositPolicy` body |
| On arrival `dining.onArrival` | segmented control | optional | Release hold | Release hold · Apply to bill | — | When the party is seated, release the deposit or put it towards the bill. | `setDepositPolicy` body |
| Basis `basis` | radio group | required | — | Fixed per booking · Fixed per guest · Percent of total · Per band | — | — | `setDepositPolicy` body |
| Amount `amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setDepositPolicy` body |
| Percent `percent` | stepper or slider (%) | optional | — | min 0; max 100 | — | — | `setDepositPolicy` body |
| Band size `bandSize` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | `perBand`: one `amount` per this much of the total, e.g. AED 100 per AED 400. | `setDepositPolicy` body |
| Balance due `balanceDue` | segmented control | optional | On the day | On the day · Days before | — | — | `setDepositPolicy` body |
| Balance due days before `balanceDueDaysBefore` | number field | optional | — | min 0 | — | — | `setDepositPolicy` body |
| Refundable until hours `refundableUntilHours` | number field (hours) | optional | 24 | min 0 | — | — | `setDepositPolicy` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry.

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **deposit policy**: Applies to party, dining, school, event; basis and amount; balance due rule. *(source: contracts/spine/orders.yaml#setDepositPolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Every deposit partial payment** (data table, from `listDepositPartialPayment`)

| Shows | Format | Notes |
|---|---|---|
| Total | 1,234 | Total |
| Deposit required | yes / no (icon or chip) | Deposit Required |
| Deposit paid | AED 1,234.50 | Deposit Paid |
| Remaining balance | AED 1,234.50 | Remaining Balance |
| Due date | 1 Oct 2026, 14:30 | Due Date |
| Days remaining | text | Days Remaining |
| Status | 1,234 | Status |

**The selected deposit partial payment** (detail panel): The pack groups this record's detail under its own headings: “Important for”, “Required Deposit”, “Due”, “Notifications”.

| Shows | Format | Notes |
|---|---|---|
| Total | 1,234 | Total |
| Deposit required | yes / no (icon or chip) | Deposit Required |
| Deposit paid | AED 1,234.50 | Deposit Paid |
| Remaining balance | AED 1,234.50 | Remaining Balance |
| Due date | 1 Oct 2026, 14:30 | Due Date |
| Days remaining | text | Days Remaining |
| Status | 1,234 | Status |

**Table deposit (dining)** (detail panel, from `getDepositPolicy`): **A venue option, off unless the venue switches it on here** (decided 29 September, rev 3 REV3-8b, superseding audit R077 (a) "no table deposit in the first release": the capability ships, disabled by default). The venue sets from what party size it applies, the basis (per guest, per table, or a percentage of a minimum spend) and the amount; nothing about the amount is fixed in code. While it is …

| Shows | Format | Notes |
|---|---|---|
| Enabled | yes / no (icon or chip) | Off unless the venue enables it. While false every other field is kept but not applied. |
| Basis | chip: Fixed per guest, Fixed per table, Percent of minimum spend | `fixedPerGuest`, `amount` times the party size; `fixedPerTable`, `amount` once per booking; `percentOfMinimumSpend`, `percent` of … |
| Amount | AED 1,234.50 | Required for the two fixed bases. |
| Percent | 12.5% | Required for `percentOfMinimumSpend`. |
| Minimum spend per guest | AED 1,234.50 | Required for `percentOfMinimumSpend`. |
| Applies from party size | 1,234 | A party smaller than this books with no deposit. Proposed default, client to correct. |
| Outlets | list or chips (count when long) | The outlets it applies to. Empty means every outlet of the venue that takes bookings. |
| Collection | chip: Authorisation hold, Charge | `authorisationHold` authorises the card and captures only on a late cancel or no-show; `charge` takes the money now and holds it as a … |
| Deposit variant | the name it points at, never the id | The catalogue variant the deposit line is sold as: a non-inventory product the venue set up whose ledger mapping posts to deposit … |
| Refundable until hours | 1,234 | Cancelling at least this long before the booking releases the deposit in full. Proposed default, client to correct. |
| On late cancel or no show | chip: Forfeit, Release | What happens to the deposit on a later cancel or a `noShow`. Settled through `finance.settleDeposit`. |
| On arrival | chip: Release hold, Apply to bill | When the party is seated, release the deposit or put it towards the bill. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Full Payment (primary button) | navigation or local | — | — | — | — |
| Fixed Deposit (secondary button) | navigation or local | — | — | — | — |
| Percentage Deposit (secondary button) | navigation or local | — | — | — | — |
| Staged Payment (secondary button) | navigation or local | — | — | — | — |
| Balance Before Visit (secondary button) | navigation or local | — | — | — | — |
| Balance by Fixed Date (secondary button) | navigation or local | — | — | — | — |
| Credit Account (secondary button) | navigation or local | — | — | — | — |
| Save table deposit (secondary button) | `setDepositPolicy` PUT `/deposit-policy` | DepositPolicy | DepositPolicy | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | opens modal first |

**Data it reads**: `getDepositPolicy` (onLoad, How deposits work); `listDepositPartialPayment` (onLoad, Deposit, Partial Payment & Outstanding Balance Management)

**Where the user goes next**

- → `BO-324` Payment & Order Financial Command Center: *Returns to the board's landing screen*; calls `listDepositPartialPayment`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The deposit partial payment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the deposit partial payment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No deposit partial payment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the deposit partial payment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  appliesTo:
  - party
  basis: percentOfTotal
  percent: 30
  balanceDue: on the day
  refundableUntil: 24 h before
```

#### Permissions

- `getDepositPolicy` → `PRODUCT_VIEW` (read) · staff
- `setDepositPolicy` → `PRODUCT_CONFIGURE` (configure) · staff
- `listDepositPartialPayment` → `ORDER_VIEW` (read) · staff
- `listDepositActivity` → `PAYMENT_VIEW` (read) · staff
- `recordDepositActivity` → `PAYMENT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-327` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-327`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 3
- Flow F142 *Order Reservation Management board 3: Payment & Order Financial Command Center*, step 6: Works in Deposit, Partial Payment & Outstanding Balance Management → Support commercial scenarios where an order may be confirmed or reserved without full immediate payment.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (400, 403, 412).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-327?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Full Payment, Fixed Deposit, Percentage Deposit, Staged Payment, Balance Before Visit, Balance by Fixed Date, Credit Account, Save table deposit.
- [ ] Every transition is wired: `BO-324`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `PAYMENT_CONFIGURE`, `PAYMENT_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-328` Order Split, Merge & Transaction Relationship Management

**Allow complex orders to be reorganized without destroying transaction history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `orderId` (navigation) · cold entry: Opened from BO-324 with the order picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says … |
| Route | `/orders-money/order-split-merge-transaction-relationship-management-bo-328` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Split one order into independent orders, or merge orders, without destroying history; payments follow the lines they paid for.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listOrderSplitMerge return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listOrderSplitMerge carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listOrderSplitMerge; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**Sent by *Merge orders*** (`mergeOrders`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Source orders `sourceOrderIds` | multi-picker: choose source orders | required | — | at least 1; at most 20; no duplicates | — | The orders merged into this one. Must not include it. | `mergeOrders` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `mergeOrders` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Ticket (primary button) | navigation or local | — | — | — | — |
| Product (secondary button) | navigation or local | — | — | — | — |
| Order Line (secondary button) | navigation or local | — | — | — | — |
| Payment Responsibility (secondary button) | navigation or local | — | — | — | — |
| Merge orders (destructive button) | `mergeOrders` POST `/orders/{orderId}/merge` | inline | Order | 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The orders differ in customer, venue or currency … | gated `ORDER_MODIFY` |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Split**: Select lines into new orders; shows how payments follow. *(source: contracts/spine/orders.yaml#splitOrder)*

**Data it reads**: `listOrderSplitMerge` (onLoad, Order Split, Merge & Transaction Relationship Management)

**Where the user goes next**

- → `BO-324` Payment & Order Financial Command Center: *Returns to the board's landing screen*; calls `listOrderSplitMerge`

**What opens over it**

- confirmDialog *Merge orders*: **Names what `mergeOrders` changes and what it leaves alone**, in the consequence rather than the verb. A order this affects should be identified in the dialog, not just counted. **Collects what `mergeOrders` sends before it is called.** Required: `sourceOrderIds`. Optional: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order split merge list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order split merge untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order split merge yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the order split merge are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The order is partly paid and the payment is not yet allocated to lines (`paymentNotAllocated`), which the description makes a precondition of splitting. (OrderRefusedProblem); 409 The orders differ in customer, venue or currency (`mergeMismatch`), or one is voided (`orderVoided`). (OrderRefusedProblem) |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
split:
  order: GB-2026-0077
  into:
  - Engineering dept
  - Finance dept
```

#### Permissions

- `listOrderSplitMerge` → `ORDER_VIEW` (read) · staff
- `splitOrder` → `ORDER_MODIFY` (operate) · staff
- `mergeOrders` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.12.33 | System shall allow operators to split a booking into multiple independent orders while preserving transaction history and financial traceability. | Ticketing Sales | CONTRACTED | `splitOrder` |
| 2.12.34 | System shall allow combining multiple reservations, bookings, or orders into a single consolidated order while maintaining full audit history. | Ticketing Sales | CONTRACTED | `splitOrder` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A69** Implement duplicate-account detection and profile-merge functionality (consolidating two profiles into one, carrying over the combined transaction history) *(Softlabs Backend Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Aug 2026 · workshop tracker · keyword 'duplicate-account')*
- **A90** Implement consent-gated duplicate merge (fuzzy name / exact mobile / exact email matching, customer confirmation required, admin review queue, login-of-record rule) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'duplicate merge')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-328` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-328`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 3
- Flow F142 *Order Reservation Management board 3: Payment & Order Financial Command Center*, step 8: Works in Order Split, Merge & Transaction Relationship Management → Allow complex orders to be reorganized without destroying transaction history.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-328?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Ticket, Product, Order Line, Payment Responsibility, Merge orders.
- [ ] Every transition is wired: `BO-324`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-329` Related Order & Transaction Relationship Explorer

**Provide a visual relationship map for complex transaction histories. This becomes especially useful after amendments, upgrades, exchanges, reissues, splits and refunds.**

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
| Route | `/orders-money/related-order-transaction-relationship-explorer-bo-329` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** A visual map of related orders and transactions after amendments, exchanges, reissues, splits and refunds.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listRelatedOrderTransaction return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listRelatedOrderTransaction; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search related order transaction | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by order, ticket, customer, payment, refund, external reference and 1 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Order | text field | — | — | `listRelatedOrderTransaction` ?order |
| Ticket | text field | — | — | `listRelatedOrderTransaction` ?ticket |
| Customer | text field | — | — | `listRelatedOrderTransaction` ?customer |
| External reference | text field | — | — | `listRelatedOrderTransaction` ?externalReference |
| Partner booking | text field | — | — | `listRelatedOrderTransaction` ?partnerBooking |
| Payment | text field | — | — | `listRelatedOrderTransaction` ?payment |
| Refund | text field | — | — | `listRelatedOrderTransaction` ?refund |

#### Outputs: what the screen shows and produces

**Shown**

**Every related order transaction** (data table, from `listRelatedOrderTransaction`)

| Shows | Format | Notes |
|---|---|---|
| Relationship type | chip: Original, Amendment, Ticket upgrade, Additional payment, Partial cancellation … | Relationship to the original. |
| Amendment | text | not in the schema: `Amendment` |
| Upgrade | text | not in the schema: `Upgrade` |
| Split | text | not in the schema: `Split` |
| Merge | text | not in the schema: `Merge` |
| Reissue | text | not in the schema: `Reissue` |
| Refund | text | not in the schema: `Refund` |

**The selected related order transaction** (detail panel): The pack groups this record's detail under its own headings: “Original Order ORD-1001”, “ORD-1001-A”, “Upgrade TXN UPG-1042”, “PAY-2014”, “CAN-3021”, “Graph Interaction”.

| Shows | Format | Notes |
|---|---|---|
| Relationship type | chip: Original, Amendment, Ticket upgrade, Additional payment, Partial cancellation … | Relationship to the original. |
| Amendment | text | not in the schema: `Amendment` |
| Upgrade | text | not in the schema: `Upgrade` |
| Split | text | not in the schema: `Split` |
| Merge | text | not in the schema: `Merge` |
| Reissue | text | not in the schema: `Reissue` |
| Refund | text | not in the schema: `Refund` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **relationship graph**: Nodes for orders and transactions, edges labelled by relation. *(source: contracts/spine/orders.yaml#listRelatedOrderTransaction)*

**Data it reads**: `listRelatedOrderTransaction` (onLoad, Related Order & Transaction Relationship Explorer)

**Where the user goes next**

- → `BO-324` Payment & Order Financial Command Center: *Returns to the board's landing screen*; calls `listRelatedOrderTransaction`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The related order transaction list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the related order transaction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No related order transaction yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the related order transaction are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
graph:
- DP-2026-104882 → exchange → DP-2026-105120
```

#### Permissions

- `listRelatedOrderTransaction` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-329` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-329`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 3
- Flow F142 *Order Reservation Management board 3: Payment & Order Financial Command Center*, step 10: Works in Related Order & Transaction Relationship Explorer → Provide a visual relationship map for complex transaction histories. This becomes especially useful after amendments, upgrades, exchanges, reissues, splits and refunds.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-329?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-324`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-330` External Payment, Partner & Settlement Reference Mapping

**Maintain the relationship between TICVAI transactions and external financial/channel references.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_MODIFY`, `ORDER_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `orderId` (navigation) |
| Route | `/orders-money/external-payment-partner-settlement-reference-mapping-bo-330` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Map orders to references other systems hold: gateways, acquirers, banks, partners, OTAs, ERP, settlement batches.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listExternalPaymentPartner return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listExternalPaymentPartner; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| TICVAI Order ID | select field | — | — | — | — | — | — |
| TICVAI Payment ID | select field | — | — | — | — | — | — |
| Provider | select field | — | — | — | — | — | — |
| Merchant ID | select field | — | — | — | — | — | — |
| External Transaction ID | select field | — | — | — | — | — | — |
| Authorization Code | select field | — | — | — | — | — | — |
| Partner Order ID | select field | — | — | — | — | — | — |
| Settlement Batch | select field | — | — | — | — | — | — |
| Settlement Date | select field | — | — | — | — | — | — |
| ERP Reference | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Amount | select field | — | — | — | — | — | — |

**Form: Record external reference** (modal, opened by *Record external reference*; *Record external reference* calls `recordExternalReference`, *Cancel* sends nothing)

**Collects what `recordExternalReference` sends before it is called.** Required: `sourceSystem`, `reason`. Optional: `paymentId`, `refundId`, `provider`, `merchantId`, `externalTransactionId`, `authorizationCode`, `partnerOrderId`, `settlementBatch`, `settlementDate`, `erpReference`, `amount`, `approvalReference`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Payment `paymentId` | picker: choose a payment | optional | — | — | shows names, sends the id | — | `recordExternalReference` body |
| Refund `refundId` | picker: choose a refund | optional | — | — | shows names, sends the id | — | `recordExternalReference` body |
| Source system `sourceSystem` | select | required | — | Payment gateways · Acquirers · Banks · POS terminals · B2B partners · Resellers · Otas · Erp · Finance systems · Wallet providers | — | — | `recordExternalReference` body |
| Provider `provider` | text field | optional | — | max length 60 | — | — | `recordExternalReference` body |
| Merchant `merchantId` | text field | optional | — | max length 60 | — | — | `recordExternalReference` body |
| External transaction `externalTransactionId` | text field | optional | — | max length 100 | — | — | `recordExternalReference` body |
| Authorization code `authorizationCode` | text field | optional | — | max length 40 | — | — | `recordExternalReference` body |
| Partner order `partnerOrderId` | text field | optional | — | max length 100 | — | — | `recordExternalReference` body |
| Settlement batch `settlementBatch` | text field | optional | — | max length 100 | — | — | `recordExternalReference` body |
| Settlement date `settlementDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `recordExternalReference` body |
| Erp reference `erpReference` | text field | optional | — | max length 100 | — | — | `recordExternalReference` body |
| Amount `amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `recordExternalReference` body |
| Reason `reason` | text area | required | — | min length 1; max length 500 | — | — | `recordExternalReference` body |
| Approval reference `approvalReference` | text field | optional | — | max length 100 | — | — | `recordExternalReference` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

#### Outputs: what the screen shows and produces

**Shown**

**Every external reference mapping** (data table, from `listExternalReferenceMappings`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | — |
| Payment | the name it points at, never the id | — |
| Refund | the name it points at, never the id | — |
| Source system | chip: Payment gateways, Acquirers, Banks, POS terminals, B2B partners, Resellers… | — |
| Provider | text | — |
| Merchant | text | — |
| External transaction | text | — |
| Authorization code | text | — |
| Partner order | text | — |
| Settlement batch | text | — |
| Settlement date | 1 Oct 2026 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Payment Gateways (primary button) | navigation or local | — | — | — | — |
| POS Terminals (secondary button) | navigation or local | — | — | — | — |
| Finance Systems (secondary button) | navigation or local | — | — | — | — |
| Wallet Providers (secondary button) | navigation or local | — | — | — | — |
| Record external reference (secondary button) | `recordExternalReference` POST `/orders/{orderId}/external-references` | CreateExternalReferenceMappingRequest | ExternalReferenceMapping | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | gated `ORDER_MODIFY`; opens modal first |

**What each action does** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **Map by hand**: Source system, provider, external reference, linked payment or refund. *(source: contracts/spine/orders.yaml#recordExternalReference)*

**Data it reads**: `listExternalPaymentPartner` (onLoad, External Payment, Partner & Settlement Reference Mapping); `listExternalReferenceMappings` (onLoad, The references other systems hold for this order)

**Where the user goes next**

- → `BO-324` Payment & Order Financial Command Center: *Returns to the board's landing screen*; calls `listExternalPaymentPartner`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The external payment partner configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the external payment partner untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No external payment partner configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
mapping:
  order: DP-2026-104882
  system: otas
  provider: Klook
  ref: KLK-55120931
```

#### Permissions

- `listExternalPaymentPartner` → `ORDER_VIEW` (read) · staff
- `listExternalReferenceMappings` → `ORDER_VIEW` (read) · staff
- `recordExternalReference` → `ORDER_MODIFY` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-330` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-330`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 3
- Flow F142 *Order Reservation Management board 3: Payment & Order Financial Command Center*, step 12: Works in External Payment, Partner & Settlement Reference Mapping → Maintain the relationship between TICVAI transactions and external financial/channel references.

#### Acceptance for the design

- [ ] Every input above is drawn (26), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-330?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Payment Gateways, POS Terminals, Finance Systems, Wallet Providers, Record external reference.
- [ ] Every transition is wired: `BO-324`.
- [ ] Every gated control is gated: `ORDER_MODIFY`, `ORDER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-331` Payment Reconciliation & Exception Management

**Automatically compare TICVAI payment records with external payment and settlement records.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Compare) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/payment-reconciliation-exception-management-bo-331` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Payment records compared with external settlement records; mismatches as exceptions to resolve.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listPaymentReconciliationException return a bare array, not the paged list envelope (items, nextCursor, hasMore).** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listPaymentReconciliationException; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every payment reconciliation exception** (data table, from `listPaymentReconciliationException`)

| Shows | Format | Notes |
|---|---|---|
| Source system | chip: Payment gateway, Acquirer, Bank, POS, Ota, Reseller… | Source system. |

**The selected payment reconciliation exception** (detail panel): The pack groups this record's detail under its own headings: “Use”, “AED 20”, “Missing AED”, “Resolution Actions”.

| Shows | Format | Notes |
|---|---|---|
| Source system | chip: Payment gateway, Acquirer, Bank, POS, Ota, Reseller… | Source system. |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **exceptions**: Unmatched, amount mismatch, duplicate, with both sides shown. *(source: contracts/spine/orders.yaml#listPaymentReconciliationException)*

**Data it reads**: `listPaymentReconciliationException` (onLoad, Payment Reconciliation & Exception Management)

**Where the user goes next**

- → `BO-324` Payment & Order Financial Command Center: *Returns to the board's landing screen*; calls `listPaymentReconciliationException`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment reconciliation exception list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment reconciliation exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment reconciliation exception yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment reconciliation exception are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
exception:
  type: amount mismatch
  ticvai: AED 590.00
  provider: AED 580.00
```

#### Permissions

- `listPaymentReconciliationException` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Payments screen consolidates gateway (Stripe, NI) and on-site (cash, card) payments and flags variances from a monthly reconciliation file (e.g. gateway 10,000 AED vs 9,500 AED recorded). *(agreed · MoM 12 Aug 2026, 17. Payments Reconciliation · DI-268)*
- Weekly/monthly reconciliation runs ingest → parse → match → classify → auto-resolve, so only genuinely mismatched amounts are shown for human review. *(agreed · MoM 12 Aug 2026, 11. Settlement and Reconciliation Process · DI-258)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-331` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-331`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 3
- Flow F142 *Order Reservation Management board 3: Payment & Order Financial Command Center*, step 14: Works in Payment Reconciliation & Exception Management → Automatically compare TICVAI payment records with external payment and settlement records.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-331?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-324`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-332` Financial Traceability, Control & Audit Explorer

**Provide a complete financial audit trail across the order lifecycle.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Where configured) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/financial-traceability-control-audit-explorer-bo-332` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** The financial audit trail across the order lifecycle.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listFinancialTraceability return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listFinancialTraceability carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listFinancialTraceability; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*
- **No write operation: a configuration screen (Financial Traceability, Control & Audit Explorer) declares only reads (listFinancialTraceability).** Why: Nothing it shows can be changed from it; either it is a view (and its edits happen on the record editor, which it should link to) or a write is missing. *(source: contracts/spine/orders.yaml#listFinancialTraceability; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Creator ≠ Approver | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Export | radio group | — | Finance · Internal audit · External audit · Compliance · Management | `listFinancialTraceability` ?export |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **audit**: Filter by order, user, event. *(source: contracts/spine/orders.yaml#listFinancialTraceability)*

**Data it reads**: `listFinancialTraceability` (onLoad, Financial Traceability, Control & Audit Explorer)

**Where the user goes next**

- → `BO-324` Payment & Order Financial Command Center: *Returns to the board's landing screen*; calls `listFinancialTraceability`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The financial traceability audit configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the financial traceability audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No financial traceability audit configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
event:
  order: DP-2026-104882
  event: refund posted
  ledger: JE-2026-77812
```

#### Permissions

- `listFinancialTraceability` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Transactions ledger lists all transactions with daily counts/totals and pending/failed sync status; detail shows chart-of-account mapping, payment method, product lines and whether each line is in sale, deferred or redemption status. *(client request · MoM 12 Aug 2026, 15. Financial Transactions Ledger and Journal Entries · DI-264)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-332` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-332`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 3
- Flow F142 *Order Reservation Management board 3: Payment & Order Financial Command Center*, step 16: Works in Financial Traceability, Control & Audit Explorer → Provide a complete financial audit trail across the order lifecycle.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-332?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-324`.
- [ ] Every gated control is gated: `ORDER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-333` Order Financial Analytics & AI Reconciliation Intelligence

**Provide management-level analytics across order payment performance, balances, settlement and reconciliation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Compare) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/order-financial-analytics-ai-reconciliation-intelligence-bo-333` |

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Management analytics on payment performance, balances, settlement and reconciliation.

**Known correction pending (do not draw the wrong version)**

- **List operation(s) listOrderFinancialReconciliation return a bare array, not the paged list envelope (items, nextCursor, hasMore); rows of listOrderFinancialReconciliation carry no identifier.** Why: The table cannot page, and a row without an id cannot open, edit or link to the record it summarises. *(source: contracts/spine/orders.yaml#listOrderFinancialReconciliation; Ticketing & Guest Commerce, as the venue and TICVAI configure and run it)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search order financial analytics | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, event, product, channel, payment method, gateway and 6 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listOrderFinancialReconciliation` ?venue |
| Event | text field | — | — | `listOrderFinancialReconciliation` ?event |
| Product | text field | — | — | `listOrderFinancialReconciliation` ?product |
| Channel | text field | — | — | `listOrderFinancialReconciliation` ?channel |
| Payment method | text field | — | — | `listOrderFinancialReconciliation` ?paymentMethod |
| Gateway | text field | — | — | `listOrderFinancialReconciliation` ?gateway |
| Customer segment | text field | — | — | `listOrderFinancialReconciliation` ?customerSegment |
| B2B partner | text field | — | — | `listOrderFinancialReconciliation` ?b2bPartner |

#### Outputs: what the screen shows and produces

**Shown**

**Every order financial analytics** (data table, from `listOrderFinancialReconciliation`)

| Shows | Format | Notes |
|---|---|---|
| Approval rate | 12.5% | Approval Rate |
| Failure rate | 12.5% | Failure Rate |
| Settlement delay | text | Settlement Delay |
| Reconciliation exceptions | text | Reconciliation Exceptions |
| Refund processing time | text | not in the schema: `Refund Processing Time` |

**The selected order financial analytics** (detail panel): The pack groups this record's detail under its own headings: “Include”, “Payment Initiated”, “Buckets”, “Natural-Language Query”, “Creates and governs the core”.

| Shows | Format | Notes |
|---|---|---|
| Approval rate | 12.5% | Approval Rate |
| Failure rate | 12.5% | Failure Rate |
| Settlement delay | text | Settlement Delay |
| Reconciliation exceptions | text | Reconciliation Exceptions |
| Refund processing time | text | not in the schema: `Refund Processing Time` |

**Rules for what is shown** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **KPIs**: KPI cards with deltas (DI-041). *(source: contracts/spine/orders.yaml#listOrderFinancialReconciliation)*

**Data it reads**: `listOrderFinancialReconciliation` (onLoad, Order Financial Analytics & AI Reconciliation Intelligence)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order financial analytics list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order financial analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order financial analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the order financial analytics are still there. The pack's own statuses are 4 Management — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  reconciled: 99.2%
  outstanding: AED 184,200.00
```

#### Permissions

- `listOrderFinancialReconciliation` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-333` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS86 Order   Reservation Management Board 3.dc.html#bo-333`
- Workshop pack: Order___Reservation_Management_Reference.pdf board 3
- Flow F142 *Order Reservation Management board 3: Payment & Order Financial Command Center*, step 18: Works in Order Financial Analytics & AI Reconciliation Intelligence → Provide management-level analytics across order payment performance, balances, settlement and reconciliation.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-333?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
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

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createInstalmentPlan": {"method":"POST","path":"/instalment-plans","contract":"payments","summary":"Split an order's payment into scheduled instalments on a stored card","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PayInstalmentPlan"},
"getDepositPolicy": {"method":"GET","path":"/deposit-policy","contract":"orders","summary":"What a deposit booking takes now and when the rest is due","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"DepositPolicy"},
"listDepositActivity": {"method":"GET","path":"/deposits/{depositId}/activity","contract":"payments","summary":"Movements on a deposit","permission":"PAYMENT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"depositId","in":"path","required":true}],"requestBody":null,"responds":"PaymentsDepositActivity"},
"listDepositPartialPayment": {"method":"GET","path":"/deposit-partial-payment","contract":"orders","summary":"Deposit, Partial Payment & Outstanding Balance Management","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DepositPartialPaymentOutstandingBalanceManagementView"},
"listExternalPaymentPartner": {"method":"GET","path":"/external-payment-partner","contract":"orders","summary":"External Payment, Partner & Settlement Reference Mapping","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ExternalPaymentPartnerSettlementReferenceMappingView"},
"listExternalReferenceMappings": {"method":"GET","path":"/orders/{orderId}/external-references","contract":"orders","summary":"The references other systems hold for this order","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFinancialTraceability": {"method":"GET","path":"/financial-traceability","contract":"orders","summary":"Financial Traceability, Control & Audit Explorer","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"export","in":"query","required":false}],"requestBody":null,"responds":"FinancialTraceabilityControlAuditExplorerView"},
"listInstalmentPlans": {"method":"GET","path":"/instalment-plans","contract":"payments","summary":"Instalment plans and their schedules","permission":"PAYMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"orderId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrderFinancialReconciliation": {"method":"GET","path":"/order-financial-reconciliation","contract":"orders","summary":"Order Financial Analytics & AI Reconciliation Intelligence","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venue","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"paymentMethod","in":"query","required":false},{"name":"gateway","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"b2bPartner","in":"query","required":false}],"requestBody":null,"responds":"OrderFinancialAnalyticsAiReconciliationIntelligenceView"},
"listOrderPaymentDetail": {"method":"GET","path":"/order-payment-detail","contract":"orders","summary":"Order Payment Detail & Transaction Ledger","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderPaymentDetailTransactionLedgerView"},
"listOrderSplitMerge": {"method":"GET","path":"/order-split-merge","contract":"orders","summary":"Order Split, Merge & Transaction Relationship Management","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderSplitMergeTransactionRelationshipManagementView"},
"listPaymentAllocationRules": {"method":"GET","path":"/payment-allocation-rules","contract":"orders","summary":"The venue's split-tender allocation rules","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"channel","in":"query","required":null},{"name":"terminalId","in":"query","required":null},{"name":"productId","in":"query","required":null},{"name":"isActive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPaymentOrderFinancial": {"method":"GET","path":"/payment-order-financial","contract":"orders","summary":"Payment & Order Financial Command Center","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venue","in":"query","required":false},{"name":"paymentProvider","in":"query","required":false},{"name":"currency","in":"query","required":false},{"name":"orderStatus","in":"query","required":false}],"requestBody":null,"responds":"PaymentOrderFinancialCommandCenterView"},
"listPaymentReconciliationException": {"method":"GET","path":"/payment-reconciliation-exception","contract":"orders","summary":"Payment Reconciliation & Exception Management","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PaymentReconciliationExceptionManagementView"},
"listRelatedOrderTransaction": {"method":"GET","path":"/related-order-transaction","contract":"orders","summary":"Related Order & Transaction Relationship Explorer","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"order","in":"query","required":false},{"name":"ticket","in":"query","required":false},{"name":"customer","in":"query","required":false},{"name":"externalReference","in":"query","required":false},{"name":"partnerBooking","in":"query","required":false},{"name":"payment","in":"query","required":false},{"name":"refund","in":"query","required":false}],"requestBody":null,"responds":"RelatedOrderTransactionRelationshipExplorerView"},
"mergeOrders": {"method":"POST","path":"/orders/{orderId}/merge","contract":"orders","summary":"Merge orders into one","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"recordDepositActivity": {"method":"POST","path":"/deposits/{depositId}/activity","contract":"payments","summary":"Record a movement on a deposit","permission":"PAYMENT_CONFIGURE","offlineCapable":null,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":"depositId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"PaymentsDepositActivity","responds":"PaymentsDepositActivity"},
"recordExternalReference": {"method":"POST","path":"/orders/{orderId}/external-references","contract":"orders","summary":"Map an order to a reference another system holds, by hand","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateExternalReferenceMappingRequest","responds":"ExternalReferenceMapping"},
"setDepositPolicy": {"method":"PUT","path":"/deposit-policy","contract":"orders","summary":"Set how deposits work","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"DepositPolicy","responds":"DepositPolicy"},
"setMultiPaymentSplit": {"method":"PUT","path":"/multi-payment-split","contract":"orders","summary":"Multi-Payment, Split Tender & Payment Allocation Configuration","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"MultiPaymentSplitTenderPaymentAllocationConfiguratioInput","responds":"MultiPaymentSplitTenderPaymentAllocationConfiguratioView"},
"splitOrder": {"method":"POST","path":"/orders/{orderId}/split","contract":"orders","summary":"Break one order into independent orders","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CreateExternalReferenceMappingRequest": {"type":"object","x-ticvai-persistence":"none — request only; lands in `orders.external_reference_mapping` with `isManual` true","description":"A manual mapping. `reason` is required because a manual mapping is only trusted with one.","required":["sourceSystem","reason"],"properties":{"paymentId":{"type":"string","format":"uuid","nullable":true},"refundId":{"type":"string","format":"uuid","nullable":true},"sourceSystem":{"type":"string","enum":["paymentGateways","acquirers","banks","posTerminals","b2bPartners","resellers","otas","erp","financeSystems","walletProviders"]},"provider":{"type":"string","maxLength":60,"nullable":true},"merchantId":{"type":"string","maxLength":60,"nullable":true},"externalTransactionId":{"type":"string","maxLength":100,"nullable":true},"authorizationCode":{"type":"string","maxLength":40,"nullable":true},"partnerOrderId":{"type":"string","maxLength":100,"nullable":true},"settlementBatch":{"type":"string","maxLength":100,"nullable":true},"settlementDate":{"type":"string","format":"date","nullable":true},"erpReference":{"type":"string","maxLength":100,"nullable":true},"amount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"reason":{"type":"string","minLength":1,"maxLength":500},"approvalReference":{"type":"string","maxLength":100,"nullable":true}}},
"DepositPartialPaymentOutstandingBalanceManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Deposit, Partial Payment & Outstanding Balance Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"total":{"type":"integer","description":"Total"},"depositRequired":{"type":"boolean","description":"Deposit Required"},"depositPaid":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Deposit Paid"},"remainingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Remaining Balance"},"dueDate":{"type":"string","format":"date-time","description":"Due Date"},"daysRemaining":{"type":"string","description":"Days Remaining"},"status":{"type":"integer","description":"Status"},"warning":{"type":"string","description":"Warning"},"gracePeriod":{"type":"string","format":"date-time","description":"Grace Period"},"requireApproval":{"type":"boolean","description":"Require Approval"},"appliesTo":{"type":"array","items":{"type":"string","enum":["groups","b2b","corporateSales","schools","events","largeReservations"]},"description":"Bookings this deposit model applies to."},"paymentModel":{"type":"string","enum":["fullPayment","fixedDeposit","percentageDeposit","stagedPayment","balanceBeforeVisit","balanceByFixedDate","creditAccount","payOnCollection"],"description":"Payment model."},"reminderStage":{"type":"string","enum":["paymentReminder","dueSoon","overdue","finalNotice"],"description":"Balance reminder stage."}}},
"DepositPolicy": {"type":"object","x-ticvai-persistence":"orders.deposit_policy","required":["basis"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"appliesTo":{"type":"array","description":"Which bookings the top-level `basis` covers. **`dining` is deprecated here since 29 September** (rev 3 REV3-8b): a table deposit is the `dining` block below, with its own switch, basis and amount, and `setDepositPolicy` refuses `dining` in this list with 400.\n","items":{"type":"string","enum":["party","dining","school","event"]}},"dining":{"$ref":"#/components/schemas/DiningDepositPolicy"},"basis":{"type":"string","enum":["fixedPerBooking","fixedPerGuest","percentOfTotal","perBand"]},"amount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"percent":{"type":"number","minimum":0,"maximum":100,"nullable":true},"bandSize":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"`perBand`: one `amount` per this much of the total, e.g. AED 100 per AED 400."},"balanceDue":{"type":"string","enum":["onTheDay","daysBefore"],"default":"onTheDay"},"balanceDueDaysBefore":{"type":"integer","minimum":0,"nullable":true},"refundableUntilHours":{"type":"integer","minimum":0,"default":24},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"DiningDepositPolicy": {"type":"object","x-ticvai-persistence":"none — embedded as the dining jsonb column of orders.deposit_policy","description":"**The table deposit hold: a venue option, off unless the venue enables it** (decided 29 September, rev 3 REV3-8b, superseding audit R077 (a) \"no table deposit in the first release\"; the capability ships, disabled by default). Set in Venue Management through `setDepositPolicy` and read by `fnb.createTableReservation`. **Nothing about the amount is in code**: the AED 100 per guest in the rev 3 prototype is an example a venue may type, not a default. With `enabled` false a table booking takes no payment and never enters the cart (rev 3 REV3-8).\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While false every other field is kept but not applied."},"basis":{"type":"string","enum":["fixedPerGuest","fixedPerTable","percentOfMinimumSpend"],"default":"fixedPerGuest","description":"`fixedPerGuest`, `amount` times the party size; `fixedPerTable`, `amount` once per booking; `percentOfMinimumSpend`, `percent` of `minimumSpendPerGuest` times the party size.\n"},"amount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Required for the two fixed bases."},"percent":{"type":"number","minimum":0,"maximum":100,"nullable":true,"description":"Required for `percentOfMinimumSpend`."},"minimumSpendPerGuest":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Required for `percentOfMinimumSpend`."},"appliesFromPartySize":{"type":"integer","minimum":1,"maximum":50,"default":1,"description":"A party smaller than this books with no deposit. Proposed default, client to correct."},"outletIds":{"type":"array","description":"The outlets it applies to. Empty means every outlet of the venue that takes bookings.","items":{"type":"string","format":"uuid"}},"collection":{"type":"string","enum":["authorisationHold","charge"],"default":"authorisationHold","description":"`authorisationHold` authorises the card and captures only on a late cancel or no-show; `charge` takes the money now and holds it as a deposit. Either way it is an `orders.deposit` row, not a sale. A hold the card network would let lapse before the booking date is taken as `charge` instead, and the guest is told so.\n"},"depositVariantId":{"type":"string","format":"uuid","nullable":true,"description":"The catalogue variant the deposit line is sold as: a non-inventory product the venue set up whose ledger mapping posts to deposit liability, not revenue. Required while `enabled` is true.\n"},"refundableUntilHours":{"type":"integer","minimum":0,"maximum":168,"default":24,"description":"Cancelling at least this long before the booking releases the deposit in full. Proposed default, client to correct."},"onLateCancelOrNoShow":{"type":"string","enum":["forfeit","release"],"default":"forfeit","description":"What happens to the deposit on a later cancel or a `noShow`. Settled through `finance.settleDeposit`."},"onArrival":{"type":"string","enum":["releaseHold","applyToBill"],"default":"releaseHold","description":"When the party is seated, release the deposit or put it towards the bill."}}},
"ExchangeRateDecimal": {"type":"string","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,6)","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one — a JavaScript client must not round a rate in transit. **Six decimal places**, the precision `finance.FxRate.rate` asks for, and stored at that precision.\n","pattern":"^\\d+(\\.\\d{1,6})?$"},
"ExternalPaymentPartnerSettlementReferenceMappingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What External Payment, Partner & Settlement Reference Mapping displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ticvaiOrderId":{"type":"string","description":"TICVAI Order ID"},"ticvaiPaymentId":{"type":"string","description":"TICVAI Payment ID"},"provider":{"type":"string","description":"Provider"},"merchantId":{"type":"string","description":"Merchant ID"},"externalTransactionId":{"type":"string","description":"External Transaction ID"},"authorizationCode":{"type":"string","description":"Authorization Code"},"partnerOrderId":{"type":"string","description":"Partner Order ID"},"settlementBatch":{"type":"string","description":"Settlement Batch"},"settlementDate":{"type":"string","format":"date-time","description":"Settlement Date"},"erpReference":{"type":"string","description":"ERP Reference"},"currency":{"type":"string","description":"Currency"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount"},"reason":{"type":"string","description":"Reason"},"user":{"type":"string","description":"User"},"timestamp":{"type":"string","format":"date-time","description":"Timestamp"},"approvalReference":{"type":"boolean","description":"Approval where required"},"sourceSystem":{"type":"string","enum":["paymentGateways","acquirers","banks","posTerminals","b2bPartners","resellers","otas","erp","financeSystems","walletProviders"],"description":"External system the reference comes from."}}},
"ExternalReferenceMapping": {"type":"object","x-ticvai-persistence":"orders.external_reference_mapping","description":"**A reference another system holds for an order, payment or refund, and who mapped it** (DM5, 29 September: data model for the agreed operations). Gateway references already on `orders.payment` and `orders.refund` are not copied; this holds the partner, OTA, ERP and settlement-batch references nothing else stores, and the manual mappings with their reason.\n**Written by the integration jobs** (partner and OTA order sync, ERP posting, settlement-file ingestion) with `isManual` false, and by `recordExternalReference` with `isManual` true; read by `listExternalReferenceMappings`, `listExternalPaymentPartner` and `listFinancialTraceability`. Append-only (decided 29 September, writers pass).","required":["id","orderId","sourceSystem","createdAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"orderId":{"type":"string","format":"uuid"},"paymentId":{"type":"string","format":"uuid","nullable":true},"refundId":{"type":"string","format":"uuid","nullable":true},"sourceSystem":{"type":"string","enum":["paymentGateways","acquirers","banks","posTerminals","b2bPartners","resellers","otas","erp","financeSystems","walletProviders"]},"provider":{"type":"string","maxLength":60,"nullable":true},"merchantId":{"type":"string","maxLength":60,"nullable":true},"externalTransactionId":{"type":"string","maxLength":100,"nullable":true},"authorizationCode":{"type":"string","maxLength":40,"nullable":true},"partnerOrderId":{"type":"string","maxLength":100,"nullable":true},"settlementBatch":{"type":"string","maxLength":100,"nullable":true},"settlementDate":{"type":"string","format":"date","nullable":true},"erpReference":{"type":"string","maxLength":100,"nullable":true},"amount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"isManual":{"type":"boolean","default":false},"reason":{"type":"string","maxLength":500,"nullable":true,"description":"Required when `isManual` is true."},"approvalReference":{"type":"string","maxLength":100,"nullable":true},"createdByPrincipalId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"createdAt":{"type":"string","format":"date-time","readOnly":true}}},
"FinancialTraceabilityControlAuditExplorerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Financial Traceability, Control & Audit Explorer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount"},"currency":{"type":"string","description":"Currency"},"priceVersion":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price Version"},"tax":{"type":"string","description":"Tax"},"fee":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fee"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount"},"paymentMethod":{"type":"string","description":"Payment Method"},"provider":{"type":"string","description":"Provider"},"user":{"type":"string","description":"User"},"channel":{"type":"string","description":"Channel"},"timestamp":{"type":"string","format":"date-time","description":"Timestamp"},"interventionType":{"type":"string","enum":["manualPaymentAdjustment","manualAllocation","manualReconciliation","manualRefund","feeWaiver","creditOverride","manualSettlementMapping"],"description":"Manual intervention recorded."}}},
"MultiPaymentSplitTenderPaymentAllocationConfiguratioInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; lands in `orders.payment_allocation_rule` (DM5, 29 September)","description":"**What Multi-Payment, Split Tender & Payment Allocation Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"channel":{"type":"string","description":"Channel"},"venue":{"type":"string","description":"Venue"},"terminal":{"type":"string","description":"Terminal"},"product":{"type":"string","description":"Product"},"orderType":{"type":"string","description":"Order Type"},"customerType":{"type":"string","description":"Customer Type"},"allocationLevel":{"type":"string","enum":["orderLevel","orderLineLevel","productLevel","taxFeeComponent","specificTicket","deposit"],"description":"What a payment is allocated against."},"isActive":{"type":"boolean","default":true,"description":"False retires the rule for this match key (decided 29 September, writers pass)."}}},
"MultiPaymentSplitTenderPaymentAllocationConfiguratioView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Multi-Payment, Split Tender & Payment Allocation Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channel":{"type":"string","description":"Channel"},"venue":{"type":"string","description":"Venue"},"terminal":{"type":"string","description":"Terminal"},"product":{"type":"string","description":"Product"},"orderType":{"type":"string","description":"Order Type"},"customerType":{"type":"string","description":"Customer Type"},"allocationLevel":{"type":"string","enum":["orderLevel","orderLineLevel","productLevel","taxFeeComponent","specificTicket","deposit"],"description":"What a payment is allocated against."}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**The currency the guest selected and is charged in** (CHG-FIN-001, 2 October 2026). Null or equal to `currency` for a sale in the base currency. Everything else on the order, and every ledger posting, stays in the base currency `currency`."},"chargeFxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"readOnly":true,"description":"Units of `chargeCurrency` per one unit of the base currency, from the region's `tender` rate in force at checkout (`finance.FxRate`), stored on the order so the payment, the receipt, the tax invoice and any refund use the same rate (CHG-FIN-001)."},"chargeFxRateId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `finance.FxRate` row the rate was taken from, for audit."},"chargeTotal":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"`grossAmount` converted at `chargeFxRate` and rounded to the charge currency's scale: what the guest pays and what the payment request to the provider asks for (CHG-FIN-001)."},"chargeRateLockedUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"The quote holds until then (the cart lease). After it, the next payment attempt re-quotes at the rate then in force and the guest confirms the new amount (CHG-FIN-001)."},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderFinancialAnalyticsAiReconciliationIntelligenceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Order Financial Analytics & AI Reconciliation Intelligence displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"grossOrderValue":{"type":"string","description":"Gross Order Value"},"netCollected":{"type":"string","description":"Net Collected"},"outstandingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Outstanding Balance"},"collectionRate":{"type":"number","description":"Collection Rate"},"paymentFailureRate":{"type":"number","description":"Payment Failure Rate"},"reconciliationRate":{"type":"number","description":"Reconciliation Rate"},"settlementVariance":{"type":"string","description":"Settlement Variance"},"averagePaymentMethodsPerOrder":{"type":"number","description":"Average Payment Methods per Order"},"depositExposure":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Deposit Exposure"},"overdueBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Overdue Balance"},"current":{"type":"string","description":"Current"},"approvalRate":{"type":"number","description":"Approval Rate"},"failureRate":{"type":"number","description":"Failure Rate"},"settlementDelay":{"type":"string","description":"Settlement Delay"},"reconciliationExceptions":{"type":"string","description":"Reconciliation Exceptions"}}},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderPaymentDetailTransactionLedgerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Order Payment Detail & Transaction Ledger displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"orderNumber":{"type":"string","description":"Order Number"},"customer":{"type":"string","description":"Customer"},"orderTotal":{"type":"string","description":"Order Total"},"currency":{"type":"string","description":"Currency"},"paid":{"type":"string","description":"Paid"},"refunded":{"type":"string","description":"Refunded"},"outstanding":{"type":"string","description":"Outstanding"},"creditApplied":{"type":"string","description":"Credit Applied"},"paymentStatus":{"type":"integer","description":"Payment Status"},"settlementStatus":{"type":"integer","description":"Settlement Status"},"transactions":{"type":"array","description":"Every financial transaction on the order, one entry each","items":{"type":"object","properties":{"type":{"type":"string","enum":["authorization","capture","payment","deposit","additionalCollection","partialRefund","reversal","walletCredit","voucher","creditNote","adjustment"],"description":"Transaction type"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount"},"status":{"type":"string","description":"Status"},"gateway":{"type":"string","description":"Gateway"},"merchant":{"type":"string","description":"Merchant"},"terminal":{"type":"string","description":"Terminal"},"authorizationCode":{"type":"string","description":"Authorization code"},"gatewayTransactionId":{"type":"string","description":"Gateway transaction ID"},"settlementReference":{"type":"string","description":"Settlement reference"},"externalReference":{"type":"string","description":"External reference"},"occurredAt":{"type":"string","format":"date-time","description":"When"}}}}}},
"OrderSplitMergeTransactionRelationshipManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Order Split, Merge & Transaction Relationship Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"basePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Base Price"},"discount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount"},"fees":{"type":"string","description":"Fees"},"tax":{"type":"string","description":"Tax"},"payments":{"type":"string","description":"Payments"},"refunds":{"type":"string","description":"Refunds"},"credits":{"type":"string","description":"Credits"},"splitBasis":{"type":"string","enum":["ticket","attendee","product","orderLine","paymentResponsibility","department","corporateCostCenter","customer"],"description":"What the order is split by."},"relationshipType":{"type":"string","enum":["parentOrder","childOrder","mergedInto","replacementOrder","amendedFrom","convertedFrom","reissuedFrom"],"description":"How the orders relate."}}},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PayInstalment": {"type":"object","description":"One scheduled charge in an instalment plan.","required":["sequence","dueDate","amount","status"],"properties":{"sequence":{"type":"integer","minimum":1},"dueDate":{"type":"string","format":"date"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["scheduled","paid","failed","waived","cancelled"]},"paymentId":{"type":"string","format":"uuid","nullable":true},"dunningCaseId":{"type":"string","format":"uuid","nullable":true},"attemptedAt":{"type":"string","format":"date-time","nullable":true}}},
"PayInstalmentPlan": {"type":"object","x-ticvai-persistence":"payments.instalment_plan + payments.instalment","description":"4.2.17. A schedule of charges for one order, independent of the product's term.","required":["id","orderId","frequency","status","total","instalments"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"frequency":{"type":"string","enum":["monthly","quarterly","custom"]},"paymentTokenId":{"type":"string","format":"uuid"},"status":{"type":"string","enum":["active","completed","inArrears","cancelled"]},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"paidToDate":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"nextDueDate":{"type":"string","format":"date","nullable":true},"instalments":{"type":"array","items":{"$ref":"#/components/schemas/PayInstalment"}},"createdAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Written at the scope of the venue the order was sold at."}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n**Cash at a till only** (CHG-FIN-001, 2 October 2026). A card or wallet payment the guest made in a currency they selected is refunded in that currency (`Refund.tenderCurrency`).\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"PaymentAllocationRule": {"type":"object","x-ticvai-persistence":"orders.payment_allocation_rule","description":"**At what level a split-tender payment is allocated, per channel, terminal, product, order type or customer type** (DM5, 29 September: data model for the agreed operations; written by `setMultiPaymentSplit`). The tender limits themselves stay in `payments.mixed_tender_rules`; this row says what each tender is allocated against. Narrowest match wins; a row naming nothing is the venue default.","required":["id","allocationLevel","isActive","createdAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"channel":{"type":"string","maxLength":40,"nullable":true},"terminalId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true},"orderType":{"type":"string","maxLength":40,"nullable":true},"customerType":{"type":"string","maxLength":40,"nullable":true},"allocationLevel":{"type":"string","enum":["orderLevel","orderLineLevel","productLevel","taxFeeComponent","specificTicket","deposit"]},"isActive":{"type":"boolean"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"PaymentOrderFinancialCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Payment & Order Financial Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"grossOrderValue":{"type":"string","description":"Gross Order Value"},"fullyPaidOrders":{"type":"integer","description":"Fully Paid Orders"},"partiallyPaidOrders":{"type":"integer","description":"Partially Paid Orders"},"unpaidOrders":{"type":"integer","description":"Unpaid Orders"},"outstandingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Outstanding Balance"},"paymentsToday":{"type":"string","description":"Payments Today"},"failedPayments":{"type":"integer","description":"Failed Payments"},"pendingPayments":{"type":"integer","description":"Pending Payments"},"refundsPending":{"type":"integer","description":"Refunds Pending"},"reconciliationExceptions":{"type":"integer","description":"Reconciliation Exceptions"},"unallocatedPayments":{"type":"integer","description":"Unallocated Payments"},"settlementVariance":{"type":"string","description":"Settlement Variance"},"orderId":{"type":"string","description":"Order ID"},"customer":{"type":"string","description":"Customer"},"channel":{"type":"string","description":"Channel"},"orderValue":{"type":"string","description":"Order Value"},"amountPaid":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount Paid"},"refunded":{"type":"string","description":"Refunded"},"outstanding":{"type":"string","description":"Outstanding"},"paymentMethods":{"type":"integer","description":"Payment Methods"},"settlementStatus":{"type":"integer","description":"Settlement Status"},"reconciliationStatus":{"type":"integer","description":"Reconciliation Status"},"paymentStatus":{"type":"string","enum":["notRequired","unpaid","paymentInitiated","authorized","partiallyPaid","paid","overpaid","partiallyRefunded","refunded","failed","reversed","reconciliationRequired"],"description":"Payment status"}}},
"PaymentReconciliationExceptionManagementView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Payment Reconciliation & Exception Management displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"transactionId":{"type":"string","description":"Transaction ID"},"externalReference":{"type":"string","description":"External Reference"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount"},"currency":{"type":"string","description":"Currency"},"date":{"type":"string","format":"date-time","description":"Date"},"merchant":{"type":"string","description":"Merchant"},"order":{"type":"string","description":"Order"},"authorizationCode":{"type":"string","description":"Authorization Code"},"sourceSystem":{"type":"string","enum":["paymentGateway","acquirer","bank","pos","ota","reseller","wallet","erp"],"description":"Source system."},"exceptionType":{"type":"string","description":"Exception, e.g. amount mismatch, unmatched settlement"},"expectedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Expected amount"},"actualAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Actual amount"}}},
"PaymentsDepositActivity": {"type":"object","x-ticvai-persistence":"payments.deposit_activity","description":"**Taken from the backend workbook, 20 September.** NEW TABLE. Provides an auditable history of every deposit authorization, hold, capture, release, forfeiture, refund, or adjustment.","required":["depositId","type","amount","occurredAt","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"depositId":{"type":"string","format":"uuid"},"paymentId":{"type":"string","format":"uuid","nullable":true},"type":{"type":"string","maxLength":30},"amount":{"type":"number"},"reason":{"type":"string","maxLength":1000,"nullable":true},"createdByPrincipalId":{"type":"string","format":"uuid","nullable":true},"occurredAt":{"type":"string","format":"date-time"},"createdAt":{"type":"string","format":"date-time"}}},
"RelatedOrderTransactionRelationshipExplorerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over orders state, assembled at read time from tables that already exist","description":"**What Related Order & Transaction Relationship Explorer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"relationshipType":{"type":"string","enum":["original","amendment","ticketUpgrade","additionalPayment","partialCancellation","conversion","exchange","cancellation","payment","chargebackWhereIntegrated","externalTransaction"],"description":"Relationship to the original."},"orderId":{"type":"string","description":"Order ID"},"relatedOrderId":{"type":"string","description":"Related order or transaction ID"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount"}}}
}
```
